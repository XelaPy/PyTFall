init -11 python:
    def retire_chars_from_location(chars, loc):
        if isinstance(chars, PytCharacter):
            chars = [chars]

        for c in chars:
            if c.home == loc:
                if c.status == "slave":
                    c.home = locations["Streets"]
                else: # Weird case for free chars...
                    c.home = location["City Apartment"]
            if c.workplace == loc:
                c.workplace = None
                c.action = None
            if c.location == loc:
                set_location(c, c.home)

    def mod_by_max(char, stat, value, prevent_death=True):
        """Modifies a stat by a float multiplier based of it's max value.

        prevent_death will not allow health to go below 0.
        """
        value = round_int(char.get_max(stat)*value)

        if prevent_death and stat == "health" and (char.health + value <= 0):
            char.health = 1
        else:
            char.mod_stat(stat, value)

    def restore_battle_stats(char):
        for stat in ["health", "mp", "vitality"]:
            char.mod_stat(stat, char.get_max(stat))

    def build_multi_elemental_icon(size=70, elements=None):
        if elements is None: # Everything except "Neutral"
            icons = [Transform(e.icon, size=(size, size)) for e in tgs.elemental if e.id != "Neutral"]
        else:
            icons = [Transform(e.icon, size=(size, size)) for e in elements]

        xcsize = round_int(float(size)/(len(icons)))
        fixed = Fixed(xysize=(size, size))
        for index, icon in enumerate(icons):
            crop = (absolute(index*xcsize), absolute(0), xcsize, size)
            xpos = absolute(index*xcsize)
            i = Transform(icon, crop=crop, subpixel=True, xpos=xpos)
            fixed.add(i)
        return fixed

    def calculate_elementals(char): # returns a dict of character elemental defences and attacks, based on elemental traits
        el_attacks = {}
        el_defence = {}
        el_keys = []
        for trait in char.elements:
            for element in trait.el_damage:
                if element in el_attacks:
                    el_attacks[element] += int(trait.el_damage[element]*100)
                else:
                    el_attacks[element] = int(trait.el_damage[element]*100)
            for element in trait.el_defence:
                if element in el_defence:
                    el_defence[element] += int(trait.el_defence[element]*100)
                else:
                    el_defence[element] = int(trait.el_defence[element]*100)
        el_attacks = {x:y for x,y in el_attacks.items() if y!=0}
        el_defence = {x:y for x,y in el_defence.items() if y!=0}
        el_keys = el_attacks.keys() + list(set(el_defence.keys()) - set(el_attacks.keys()))
        return el_attacks, el_defence, el_keys

    def kill_char(char):
        # Attempts to remove a character from the game world.
        # This happens automatiaclly if char.health goes 0 or below.
        char._location = "After Life"
        char.alive = False
        if char in hero.chars:
            hero.corpses.append(char)
            hero.remove_char(char)
        if char in hero.team:
            hero.team.remove(char)
        gm.remove_girl(char)

    def take_team_ap(value):
        """
        Checks the whole hero team for enough AP; if at least one teammate doesn't have enough AP, AP won't decrease, and function will return False, otherwise True
        """
        for i in hero.team:
            if i.AP - value < 0:
                return False
        for i in hero.team:
            i.AP -= value
        return True

    # Characters related:
    def get_first_name(sex="female"):
        """Gets a randomly generated first name.

        sex: male/female
        """
        if sex == "female":
            if not store.female_first_names:
                store.female_first_names = load_female_first_names(200)
            return store.female_first_names.pop()
        elif sex == "male":
            if not store.male_first_names:
                store.male_first_names = load_male_first_names(200)
            return store.male_first_names.pop()
        else:
            raise Exception("Unknow argument passed to get_first_name func!")

    def get_last_name():
        if not store.random_last_names:
            store.random_last_names = load_random_last_names(200)
        return random_last_names.pop()

    def get_team_name():
        if not hasattr(store, "random_team_names") or not store.random_team_names:
            store.random_team_names = load_team_names(50)
        return random_team_names.pop()

    def build_mob(id=None, level=1, max_out_stats=False):
        mob = Mob()
        stats = mob.STATS
        skills = mob.stats.skills.keys()

        if not id:
            id = choice(mobs.keys())

        if not id in mobs:
            raise Exception("Unknown id {} when creating a mob!".format(id))

        data = mobs[id]
        mob.id = id
        mob.min_lvl = data.get("min_lvl", 1)
        mob.name = data.get("name", id)
        mob.desc = data.get("desc", "Some Random Monsta!")

        for i in ("battle_sprite", "portrait", "origin", "locations", "base_race", "race", "front_row"):
            if i in data:
                setattr(mob, i, data[i])

        for skill, value in data.get("skills", {}).iteritems():
            if mob.stats.is_skill(skill):
                mob.stats.mod_full_skill(skill, value)
            else:
                devlog.warning(str("Skill: {} for Mob with id: {} is invalid! ".format(skill, id)))

        # Get and normalize basetraits:
        mob.traits.basetraits = set(traits[t] for t in data.get("basetraits", []))
        for trait in mob.traits.basetraits:
            mob.apply_trait(trait)

        for trait in data.get("traits", []):
            mob.apply_trait(trait)

        if "default_attack_skill" in data:
            skill = data["default_attack_skill"]
            mob.default_attack_skill = store.battle_skills[skill]
        for skill in data.get("attack_skills", []):
            mob.attack_skills.append(store.battle_skills[skill])
        for skill in data.get("magic_skills", []):
            mob.magic_skills.append(store.battle_skills[skill])

        mob.init()

        if level != 1:
            initial_levelup(mob, level, max_out_stats=max_out_stats)

        if not max_out_stats:
            for stat, value in data.get("stats", {}).iteritems():
                if stat != "luck":
                    value = int(round(mob.get_max(stat)*value/float(100)))
                setattr(mob, stat, value)

        return mob

    def build_rc(id=None, name=None, last_name=None, patterns=None,
                 specific_patterns=None, set_locations=True,
                 set_status="free",
                 tier=0, tier_kwargs=None, add_to_gameworld=True,
                 equip_to_tier=False, gtt_kwargs=None,
                 spells_to_tier=False, stt_kwargs=None):
        '''Creates a random character!
        id: id to choose from the rchars dictionary that holds rGirl loading data
            from JSON files, will be chosen at random if none availible.
        name: (String) Name for a girl to use. If None one will be chosen from randomNames file!
        last_name: Same thing only for last name :)
        patterns: Pattern to use when creating the character!
            Expects general occupation or list of the same.
        specific_patterns: A list of one or more specific base traits
            to use in character creation. If more than two are provided, two will be chosen at random.
        teir: Tier of the character... floats are allowed.
        add_to_gameworld: Adds to characters dictionary, should always
        be True unless character is created not to participate in the game world...
        equip_to_tier/gtt_kwargs: Do we run equip to tier func and kwargs for it.
        spells_to_tier/stt_kwargs: Award spells and kwargs for the func
        '''
        if tier_kwargs is None:
            tier_kwargs = {}
        if gtt_kwargs is None:
            gtt_kwargs = {}
        if stt_kwargs is None:
            stt_kwargs = {}

        rg = rChar()
        Stats = rg.STATS
        Skills = rg.stats.skills.keys()

        if not id:
            id = choice(rchars.keys())

        if id in rchars:
            data = rchars[id]
            rg.id = id
        else:
            raise Exception("Unknown id {} when creating a random character!".format(id))

        # rg.id = id

        # Elements:
        # if "elements" in data:
        #     for key, value in data["elements"]:
        #         if dice(value):
        #             if key not in traits:
        #                 key = key.split(" ")[0]
        #             if key not in traits:
        #                 devlog.warning("Element (*Split with ' '): {} for random girl with id: {} is not a valid element for this game!".format(str(key), str(id)))
        #                 continue
        #             rg.apply_trait(traits[key])

        # Blocking traits:
        for key in ("blocked_traits", "ab_traits"):
            if key in data:
                _traits  = set()
                for t in data[key]:
                    if t in store.traits:
                        _traits.add(store.traits[t])
                    else:
                        devlog.warning("%s trait is unknown for %s (In %s)!" % (t, id, key))
                setattr(rg.traits, key, _traits)

        # Traits next:
        if "random_traits" in data:
            for item in data["random_traits"]:
                trait, chance = item
                if dice(chance):
                    if trait in traits:
                        rg.apply_trait(traits[trait])
                    else:
                        # Added str() call to avoid cp850 encoding
                        devlog.warning("Trait: {} for random girl with id: {} is not a valid trait for this game!".format(str(trait), str(id)))

        # Names/Origin:
        if not name:
            if not store.female_first_names:
                store.female_first_names = load_female_first_names(200)
            rg.name = get_first_name()
        else:
            rg.name = name

        if not last_name:
            rg.fullname = " ".join([rg.name, get_last_name()])

        rg.nickname = rg.name

        if "origin" not in data:
            rg.origin = choice(["Alkion", "PyTFall", "Crossgate"])
        else:
            origin = data["origin"]
            if isinstance(origin, basestring):
                origin = [origin]
            rg.origin = choice(origin)

        # Status next:
        if set_status is False:
            pass
        elif set_status is not True:
            rg.set_status(set_status)
        else:
            rg.set_status(choice(["free", "slave"]))

        # Locations:
        if set_locations:
            if rg.status == "slave":
                rg.home = locations["PyTFall Slavemarket"]
                set_location(rg, rg.home)
            else:
                rg.home = locations["City Apartment"]
                set_location(rg, locations["City"])

        # BASE TRAITS:
        basetraits = []
        if specific_patterns:
            for p in specific_patterns:
                if isinstance(p, basestring):
                    p = traits[p]
                basetraits.append(p)
        if not basetraits and patterns:
            basetraits = create_traits_base(patterns)
        if basetraits:
            basetraits = random.sample(basetraits, min(len(basetraits), 2))
            rg.traits.basetraits = set(basetraits)
            for t in basetraits:
                rg.apply_trait(t)

        # Battle and Magic skills:
        if "default_attack_skill" in data:
            skill = data["default_attack_skill"]
            if skill in store.battle_skills:
                rg.default_attack_skill = store.battle_skills[skill]
            else:
                devlog.warning(str("%s Random Girl tried to apply unknown battle skill: %s!" % (id, skill)))

        if "magic_skills" in data:
            d = data["magic_skills"]
            for skill, chance in d:
                if dice(chance):
                    if skill in store.battle_skills:
                        rg.magic_skills.append(store.battle_skills[skill])
                    else:
                        devlog.warning(str("%s Random Girl tried to apply unknown battle skill: %s!" % (id, skill)))

        # SKILLS:
        # if "random_skills" in data:
        #     d = data["random_skills"]
        #     for key in d:
        #         if key.lower() in Skills:
        #             value = randint(d[key][0], d[key][1])
        #             rg.stats.mod_full_skill(key)
        #         else:
        #             devlog.warning(str("Skill: %s for random girl with id: %s is invalid! "%(key, id)))
        #
        # # STATS:
        # if "random_stats" in data:
        #     d = data["random_stats"]
        #     for key in d:
        #         if key in Stats:
        #             if key != "luck":
        #                 value = randint(d[key][0], d[key][1])
        #                 value = int(round(float(value)*100 / rg.get_max(key)))
        #                 rg.mod_stat(key, value)
        #             elif key == "luck":
        #                 rg.mod_stat(key, randint(d[key][0], d[key][1]))
        #         else:
        #             devlog.warning(str("Stat: %s for random girl with id: %s is invalid! " % (key, id)))

        # Normalizing if not all stats were supplied:
        # for stat in Stats:
        #     if stat not in rg.stats.FIXED_MAX and getattr(rg, stat) == 0:
        #         setattr(rg, stat, randint(10, 25))

        # Rest of the expected data:
        for i in ("gold", "desc", "height", "full_race"):
            if i in data:
                setattr(rg, i, data[i])

        # if "race" in data:
        #     trait = data["race"]
        #     if trait in traits:
        #         rg.apply_trait(traits[trait])
        #     else:
        #         devlog.warning("%s is not a valid race (build_rc)!" % (trait))

        # Colors in say screen:
        for key in ("color", "what_color"):
            if key in data:
                if data[key] in globals():
                    color = getattr(store, data[key])
                else:
                    try:
                        color = Color(data[key])
                    except:
                        devlog.warning("{} color supplied to {} is invalid!".format(gd[key], gd["id"]))
                        color = ivory
                rg.say_style[key] = color

        # Normalizing new girl:
        # We simply run the init method of parent class for this:
        super(rChar, rg).init()

        # And at last, leveling up and stats/skills applications:
        tier_up_to(rg, tier, **tier_kwargs)

        if equip_to_tier:
            give_tiered_items(rg, **gtt_kwargs)
        if spells_to_tier:
            give_tiered_magic_skills(rg, **stt_kwargs)

        # And add to char! :)
        if add_to_gameworld:
            store.chars["_".join([rg.id, rg.name, rg.fullname.split(" ")[1]])] = rg

        return rg

    def give_tiered_items(char, amount=1, gen_occ=None, occ=None, equip=False):
        """Gives items based on tier and class of the character.

        amount: Usually 1, this number of items will be awarded per slot.
            # Note: atm we just work with 1!
        gen_occ: General occupation that we equip for: ("SIW", "Warrior", "Server", "Specialist")
            This must always be provided, even if occ is specified.
        occ: Specific basetrait.
        equip: Run auto_equip function after we're done.
        """
        tier = max(min(round_int(char.tier*.5), 4), 0)
        # TODO: Update to char.occupation once that is implemented:
        if gen_occ is None:
            try:
                gen_occ = choice(char.gen_occs)
            except:
                raise Exception(char.name, char.__class__)
        if char.status == "slave" and gen_occ == "Warrior":
            problem = (char.name, char.__class__)
            devlog.warning("Giving tiered items to a Warrior Slave failed: {}".format(problem))
            return
        # See if we can get a perfect occupation:
        if occ is None:
            basetraits = gen_occ_basetraits[gen_occ]
            basetraits = char.basetraits.intersection(basetraits)
            if basetraits:
                occ = random.sample(basetraits, 1)[0].id
        if char.status == "slave" and occ in gen_occ_basetraits["Warrior"]:
            return

        # print("gen_occ: {}, occ: {}".format(gen_occ, occ))

        filled_slots = {s: [] for s in EQUIP_SLOTS}
        # Perfect matches are subclass matches, such as a Bow would be for a Shooter

        for _ in reversed(range(tier+1)):
            _items = [i for i in tiered_items[_] if i.sex in (char.gender, 'unisex')]
            # print(", ".join([i.id for i in _items]))
            perfect = defaultdict(list)
            normal = defaultdict(list)
            _any = defaultdict(list)

            for i in _items:
                if occ in i.pref_class:
                    perfect[i.slot].append(i)
                elif gen_occ in i.pref_class:
                    normal[i.slot].append(i)
                elif "Any" in i.pref_class:
                    _any[i.slot].append(i)

            for slot in EQUIP_SLOTS:
                if not filled_slots[slot]:
                    if slot in perfect:
                        filled_slots[slot].append(choice(perfect[slot]))
                    elif slot in normal:
                        filled_slots[slot].append(choice(normal[slot]))
                    elif slot in _any:
                        filled_slots[slot].append(choice(_any[slot]))

        for i in filled_slots.values():
            if i:
                char.add_item(i.pop())

        if equip:
            if "Caster" in char.gen_occs:
                purpose = "Wizard"
            elif "Warrior" in char.gen_occs:
                purpose = "Combat"
            elif "SIW" in char.gen_occs:
                purpose = "Sex"
            elif "Server" in char.gen_occs:
                purpose = "Service"
            elif "Specialist" in char.gen_occs:
                purpose = "???" # TODO Not implemented yet
            char.equip_for(purpose)

    def give_tiered_magic_skills(char, amount="auto", support_amount="auto"):
        """Gives spells based on tier and class of the character.
        *We assume that is called on a char that actually needs it.

        amount: Amount of skills to give. "auto" will get it from occupations and tiers.
        support_amount: healing and status spells (forced).
        """
        tier = max(min(round_int(char.tier*.5), 4), 0)
        attributes = set([t.id.lower() for t in char.elements])
        if support_amount == "auto":
            if traits["Healer"] in char.traits.basetraits:
                s_amount = max(tier, 2)
            elif traits["Healer"] in char.traits:
                s_amount = max(tier, 1)
            else:
                s_amount = 0
        else:
            s_amount = support_amount

        if amount == "auto":
            if "Caster" in char.gen_occs:
                amount = tier + randint(1, 2)
                s_amount += 1
            elif "Warrior" in char.gen_occs or "Specialist" in char.gen_occs:
                if "neutral" in attributes:
                    amount = randint(0, 1)
                else:
                    amount = randint(0, 2)
            else:
                amount = 0

        if amount <= 0 and s_amount <= 0:
            return

        for _ in reversed(range(tier+1)):
            if amount > 0:
                if "neutral" in attributes:
                    spells = tiered_magic_skills[_]
                else:
                    spells = [s for s in tiered_magic_skills[_] if attributes.intersection(s.attributes)]
                shuffle(spells)
                for s in spells:
                    if s not in char.magic_skills:
                        char.magic_skills.append(s)
                        amount -= 1
                    if amount <= 0:
                        break

            if s_amount > 0:
                spells = [s for s in tiered_magic_skills[_] if \
                    set(["status", "healing"]).intersection(s.attributes) or s.kind == "revival"]
                shuffle(spells)
                for s in spells:
                    if s not in char.magic_skills:
                        char.magic_skills.append(s)
                        s_amount -= 1

                    if s_amount <= 0:
                        break

            # print(", ".join([s.name for s in spells]))
            if amount <= 0 and s_amount <= 0:
                break

    def initial_levelup(char, level, max_out_stats=False):
        """
        This levels up the character, usually when it's first created.
        """
        exp = level*(level-1)*500
        char.stats.level = 1
        char.exp = 0
        char.stats.goal = 1000
        char.stats.goal_increase = 1000

        char.exp += exp

        if max_out_stats:
            for stat in char.stats.stats:
                if stat not in char.stats.FIXED_MAX:
                    setattr(char, stat, char.get_max(stat))
        # --------

    def adjust_exp(char, exp):
        '''
        Adjusts experience according to a level of character.
        We will find a better way to handle experience in the future.
        '''
        if char == hero:
            if char.level < 10:
                return int(math.ceil(char.level * exp)*1.4)
            elif char.level < 30:
                return int(math.ceil(char.level * exp)*1.3)
            elif char.level < 40:
                return int(math.ceil(char.level * exp)*1.2)
            else:
                return int(math.ceil(char.level * exp)*1.1)
        elif isinstance(char, Char):
            if char.level < 10:
                return int(math.ceil(char.level * exp)*0.9)
            elif char.level < 20:
                return int(math.ceil(char.level * exp)*0.8)
            elif char.level < 30:
                return int(math.ceil(char.level * exp)*0.75)
            elif char.level < 40:
                return int(math.ceil(char.level * exp)*0.70)
            elif char.level < 50:
                return int(math.ceil(char.level * exp)*0.65)
            elif char.level < 60:
                return int(math.ceil(char.level * exp)*0.6)
            elif char.level < 70:
                return int(math.ceil(char.level * exp)*0.5)
            else:
                return int(math.ceil(char.level * exp)*0.4)
        return int(math.ceil(char.level * exp))

    def create_traits_base(patterns):
        """Create a pattern with one or two base traits for a character.

        patterns: Single general occupation or list of the same to build a specific pattern from.
        """
        try:
            if isinstance(patterns, basestring):
                patterns = [patterns]
            patterns = list(chain.from_iterable(gen_occ_basetraits[p] for p in patterns))
            if len(patterns) > 1 and dice(50):
                return random.sample(patterns, 2)
            else:
                return random.sample(patterns, 1)
        except:
            raise Exception("Cannot create base traits list from patterns: {}".format(patterns))

    def build_client(id=None, gender="male", caste="Peasant", name=None, last_name=None,
                     pattern=None, likes=None, dislikes=None, tier=1):
        """
        This function creates Customers to be used in the jobs.
        Some things are initiated in __init__ and funcs/methods that call this.

        - pattern: Pattern (string) to be supplied to the create_traits_base function.
        - likes: Expects a list/set/tuple of anything a client may find attractive in a worker/building/upgrade, will be added to other likes (mostly traits), usually adds a building...
        """
        client = Customer(gender, caste)

        if not id:
            client.id = "Client" + str(random.random())

        if name:
            client.name = name
        else:
            client.name = get_first_name(gender)

        if last_name:
            client.fullname = client.name + " " + last_name
        else:
            client.fullname = client.name + " " + get_last_name()

        # Patterns:
        if not pattern:
            pattern = random.sample(client.GEN_OCCS, 1).pop()
        pattern = create_traits_base(pattern)
        for i in pattern:
            client.traits.basetraits.add(i)
            client.apply_trait(i)

        # Add a couple of client traits: <=== This may not be useful...
        trts = random.sample(tgs.client, randint(2, 5))
        for t in trts:
            client.apply_trait(t)

        # Likes:
        # Add some traits from trait groups:
        cl = set()
        cl.add(choice(tgs.breasts))
        cl.add(choice(tgs.body))
        cl.add(choice(tgs.race))
        cl = cl.union(random.sample(tgs.base, randint(1, 2)))
        cl = cl.union(random.sample(tgs.elemental, randint(2, 3)))
        cl = cl.union(random.sample(tgs.ct, randint(2, 4)))
        cl = cl.union(random.sample(tgs.sexual, randint(1, 2)))
        client.likes = cl

        if likes:
            client.likes = client.likes.union(likes)
            # We pick some of the traits to like/dislike at random.

        tier_up_to(client, tier)

        return client

    def copy_char(char):
        """Due to some sh!tty coding on my part, just a simple deepcopy/copy will not do :(

        This func cannot be used to make a playable character that can properly interact with the game world.
        """
        if isinstance(char, PytGroup):
            char = char._first

        # new = deepcopy(char)
        # Trying to improve the performace:
        new = pickle.loads(pickle.dumps(char, -1))

        # One More Attempt through class Instantiation, does not work yet:
        # new = char.__class__()
        # Stats copy (Only for the new instance attempt)
        # new.id = char.id
        # new.location = shallowcopy(char.location)
        # new.stats = shallowcopy(char.stats)
        # new.stats.instance = new
        # # Effects (Also, just for the new instance attempt)
        # if hasattr(char, "effects"):
            # new.effects = char.effects.copy()

        # Traits copy:
        # real_traits = list(traits[t] for t in [trait.id for trait in char.traits])
        # new.traits[:] = real_traits
        new.traits[:] = list(char.traits)
        new.traits.normal = char.traits.normal.copy()
        new.traits.items = char.traits.items.copy()
        new.traits.ab_traits = char.traits.ab_traits.copy()
        new.traits.blocked_traits = char.traits.blocked_traits.copy()
        new.traits.basetraits = char.traits.basetraits.copy()

        # Equipment slots/Item mods:
        new.eqslots = char.eqslots.copy()
        new.miscitems = char.miscitems.copy()
        new.consblock = char.consblock.copy()
        new.constemp = char.constemp.copy()

        # Skills:
        # real_attack_skills = list(battle_skills[s] for s in [skill.name for skill in char.attack_skills])
        # new.attack_skills[:] = real_attack_skills
        new.attack_skills[:] = list(char.attack_skills)
        new.attack_skills.normal = char.attack_skills.normal.copy()
        new.attack_skills.items = char.attack_skills.items.copy()

        # real_magic_skills = list(battle_skills[s] for s in [skill.name for skill in char.magic_skills])
        # new.magic_skills[:] = real_magic_skills
        new.magic_skills[:] = list(char.magic_skills)
        new.magic_skills.normal = char.magic_skills.normal.copy()
        new.magic_skills.items = char.magic_skills.items.copy()

        return new

    def set_char_to_work(char, building, job=False):
        """Attempts to find the best possible job to the char in given building.

        For now it just randomly picks any fitting job or sets to None.
        In the future, this should find the best possible job and set the char to it.

        Note: Due to older logic, this function expects job argument to be None when a character is made jobless by player input or game logic!
        """
        if isinstance(char, PytGroup):
            for c in char.lst:
                set_char_to_work(c, building, job)
            return
        if job is False:
            available_jobs = list(j for j in building.jobs if j.all_occs & char.occupations)
            job = choice(available_jobs) if available_jobs else None

        # We want to remove char as a building manager if he/she leave the post, we don't do that when char is set to rest or auto-rest.
        if building.manager == char:
            sj = store.simple_jobs
            if job not in (sj["Manager"], sj["Rest"], sj["AutoRest"]):
                building.manager = None

        char.action = job
        # We prolly still want to set a workplace...
        char.workplace = building

        if job is None:
            return

        if hasattr(building, "all_workers"):
            if char not in building.all_workers:
                building.all_workers.append(char)

        # Make sure that the manager is set:
        if job == simple_jobs["Manager"]:
            building.manager = char

    def tier_up_to(char, tier, level_bios=(.9, 1.1),
                   skill_bios=(.8, 1.2), stat_bios=(.8, 1.0)):
        """Tiers up a character trying to set them up smartly

        @params:
        char: Character object or id
        tier: Tier number to level to (10 is max and basically a God)
        bios: When setting up stats and skills, uniform between the two values
              will be used.
              Level, stats and skills bioses work in the same way

        Important: Should only be used right after the character was created!
        """
        level_bios = partial(random.uniform, level_bios[0], level_bios[1])
        skill_bios = partial(random.uniform, skill_bios[0], skill_bios[1])
        stat_bios = partial(random.uniform, stat_bios[0], stat_bios[1])
        # Level with base 20
        level = tier*20
        if level:
            level = round_int(level*level_bios())
            initial_levelup(char, level)

        # Do the stats/skills:
        base_skills = set()
        base_stats = set()
        # !!! Using weight may actually confuse thing in here... this needs testing.
        # Also, it may be a good idea to do list(s) of stats/skills every ht char should have a bit of...
        for trait in char.traits.basetraits:
            skills = trait.base_skills
            total_weight_points = sum(skills.values())
            for skill, weight in skills.items():
                base_skills.add(skill)
                weight_ratio = float(weight)/total_weight_points
                sp = char.get_max_skill(skill, tier)
                weight_sp = weight_ratio*sp
                biosed_sp = round_int(weight_sp*skill_bios())

                char.mod_skill(skill, biosed_sp)

            stats = trait.base_stats
            total_weight_points = sum(stats.values())
            for stat, weight in stats.items():
                base_stats.add(stat)
                weight_ratio = float(weight)/total_weight_points
                sp = char.get_max(stat)
                weight_sp = weight_ratio*sp
                biosed_sp = round_int(weight_sp*stat_bios())

                char.mod_stat(stat, biosed_sp)

        # Now that we're done with baseskills, we can play with other stats/skills a little bit
        for stat in char.stats.stats:
            if stat not in char.stats.FIXED_MAX and stat not in base_stats:
                if dice(char.luck*.5):
                    value = char.get_max(stat)*.3
                    value = round_int(value*stat_bios())
                    char.mod_stat(stat, value)
                else:
                    value = char.get_max(stat)*random.uniform(.05, .15)
                    value = round_int(value*stat_bios())
                    char.mod_stat(stat, value)
        for skill in char.stats.skills:
            if skill not in base_skills:
                if dice(char.luck*.5):
                    value = (SKILLS_MAX[skill]*(tier*.1))*.3
                    value = round_int(value*skill_bios())
                    char.mod_skill(skill, value)
                else:
                    value = (SKILLS_MAX[skill]*(tier*.1))*random.uniform(.05, .15)
                    value = round_int(value*skill_bios())
                    char.mod_skill(skill, value)

        char.tier = round_int(tier) # Makes sure we can use float tiers
