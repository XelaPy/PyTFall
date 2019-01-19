init -11 python:
    def stop_training(char):
        #since there is no slave training yet, this does nothing
        pass

    def char_is_training(char):
        #since there is no slave training yet, this is always false.
        #Should be updated when Slave Training is implemented.
        return False

    def get_average_wage():
        wages = Tier.BASE_WAGES.values()
        wage = sum(wages)/len(wages)
        return round_int(wage)

    def friends_disp_check(char, msg=None):
        """Sets up friendship with characters based on disposition"""
        if hero in char.lovers:
            if (char.disposition < 200 and char.status == "free") or (char.disposition < 50): # and self.status == "slave"):
                    end_lovers(char, hero)
                    if msg:
                        msg.append("\n {} and you are no longer lovers...".format(char.nickname))

        if hero in char.friends:
            if char.disposition <=0:
                end_friends(char, hero)
                if msg:
                    msg.append("\n {} is no longer friends with you...".format(char.nickname))
        elif char.disposition > 400:
            set_friends(char, hero)
            if msg:
                msg.append("\n {} became pretty close to you.".format(char.nickname))

    def retire_chars_from_location(chars, loc):
        if isinstance(chars, PytCharacter):
            chars = [chars]

        for c in chars:
            if c.home == loc:
                if c.status == "slave":
                    c.home = locations["Streets"]
                else: # Weird case for free chars...
                    c.home = location["City Apartments"]
            if c.workplace == loc:
                c.action = None
                c.workplace = None
            if c.location == loc:
                set_location(c, c.home)

    def check_stat_perc(char, stat, value, dir="lower"):
        """Checks if stat/skill is higher/lower (or eq) than given percentage of the max.

        value should be a float to check against. (.1 = 10%, .34 = 34% and etc.)
        """
        if char.stats.is_stat(stat):
            max_value = char.get_max(stat)
            val = getattr(char, stat)
            if dir == "lower":
                if val <= max_value*value:
                    return True
            elif dir == "higher":
                if val >= max_value*value:
                    return True
            return False
        elif char.stats.is_skill(stat):
            raise NotImplementedError("Skills are not yet implemented in this function.")

    def mod_by_max(char, stat, value, prevent_death=True):
        """Modifies a stat by a float multiplier (value) based of it's max value.

        prevent_death will not allow health to go below 1.
        """
        if char.stats.is_stat(stat):
            value = round_int(char.get_max(stat)*value)
            if prevent_death and stat == "health" and (char.health + value <= 0):
                char.health = 1
            else:
                char.mod_stat(stat, value)
        elif char.stats.is_skill(stat):
            value = round_int(char.get_max_skill(stat)*value)
            char.stats.mod_full_skill(stat, value)

    def set_stat_to_percentage(char, stat, value, prevent_death=True):
        """Sets stat/skill to a percentage of max. Forcing the matter.
        DevNote: Use with caution as this can have unexpected side effects.

        prevent_death will not allow health to go below 1.
        """
        stats = char.stats

        if stats.is_stat(stat):
            if stat == "health":
                char.health = 1
            else:
                setattr(char, stat, 0)
                mod_by_max(char, stat, value, prevent_death=prevent_death)
        elif stats.is_skill(stat):
            stats.skills[stat] = [0, 0]
            mod_by_max(char, stat, value, prevent_death=prevent_death)

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

    def elements_calculator(char, text=True): # returns text in proper format for gui if text is true, otherwise numbers
        global red
        global lime
        elements = {}

        for trait in char.traits:
            for element in trait.el_damage:
                if not element in elements.keys():
                    elements[element] = {}

                if "attack" in elements[element].keys():
                    elements[element]["attack"] += int(trait.el_damage[element]*100)
                else:
                    elements[element]["attack"] = int(trait.el_damage[element]*100)

            for element in trait.el_defence:
                if not element in elements.keys():
                    elements[element] = {}

                if "defence" in elements[element].keys():
                    elements[element]["defence"] += int(trait.el_defence[element]*100)
                else:
                    elements[element]["defence"] = int(trait.el_defence[element]*100)

            for i in trait.resist:
                if not i in elements.keys():
                    elements[i] = {}

                elements[i]["resist"] = True

            for element in trait.el_absorbs:
                if not element in elements.keys():
                    elements[element] = {}

                if "abs" in elements[element].keys():
                    elements[element]["abs"] += int(trait.el_absorbs[element]*100)
                else:
                    elements[element]["abs"] = int(trait.el_absorbs[element]*100)

        for i in elements:
            if not "defence" in elements[i].keys():
                elements[i]["defence"] = 0

            if not "attack" in elements[i].keys():
                elements[i]["attack"] = 0



        if text:
            for i in elements:
                if elements[i]["attack"] >= 0:
                    elements[i]["attack_color"] = lime
                else:
                    elements[i]["attack_color"] = red
                elements[i]["attack"] = str(elements[i]["attack"]) + " %"

                if elements[i]["defence"] >= 0:
                    elements[i]["defence_color"] = lime
                else:
                    elements[i]["defence_color"] = red
                elements[i]["defence"] = str(elements[i]["defence"]) + " %"

                if "abs" in elements[i].keys():
                    elements[i]["abs"] = "A " + str(elements[i]["abs"]) + " %"

        return elements

    def kill_char(char):
        # Attempts to remove a character from the game world.
        # This happens automatically if char.health goes 0 or below.
        if "Undead" in char.traits:
            char.health = 1
            return
        atfer_life = locations["After Life"]
        char.home = atfer_life
        set_location(char, atfer_life)
        char.action = None
        char.workplace = None
        char.alive = False
        if char in hero.chars:
            hero.remove_char(char)
        gm.remove_girl(char)

    def take_team_ap(value):
        """
        Checks the whole hero team for enough AP;
        if at least one teammate doesn't have enough AP, AP won't decrease,
        and function will return False, otherwise True
        """
        for i in hero.team:
            if i.AP - value < 0:
                return False
        for i in hero.team:
            i.AP -= value
        return True

    # GUI helpers:
    def controlled_char(char):
        # used in chars profile, most user interface options disabled if this returns False.
        global char_profile_entry
        if char_profile_entry == "employment_agency":
            return False
        elif not char.is_available:
            return False

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
            raise Exception("Unknown argument passed to get_first_name func!")

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
                char_debug(str("Skill: {} for Mob with id: {} is invalid! ".format(skill, id)))

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
                    value = getattr(mob, stat) + abs(value)
                setattr(mob, stat, value)

        return mob

    def build_rc(id=None, name=None, last_name=None,
                 bt_direct=None, bt_go_patterns=None,
                 bt_group=None, bt_preset=None,
                 set_locations=True,
                 set_status="free",
                 tier=0, tier_kwargs=None, add_to_gameworld=True,
                 give_civilian_items=False, gci_kwargs=None,
                 give_bt_items=False, gbti_kwargs=None,
                 spells_to_tier=False, stt_kwargs=None):
        '''Creates a random character!
        id: id to choose from the rchars dictionary that holds rGirl loading data.
            from JSON files, will be chosen at random if none available.
        name: (String) Name for a girl to use. If None one will be chosen from randomNames file!
        last_name: Same thing only for last name :)
        bt_direct: A list of one or more specific base traits
            to use in character creation. If more than two are provided, two will be chosen at random.
        bt_go_patterns: General occupation patterns to use when creating the character!
            Expects general occupation or list of the same.
            Use create_traits_base function to build basetraits.
            Input could be ["Combatant", "Specialist"] for example, we will pick from all
            Combatant and Specialist bts in the game randomly.
        bt_group: Groups of custom selections of basetraits.
        bt_preset: Random choice from custom presets of basetraits.

        teir: Tier of the character... floats are allowed.
        add_to_gameworld: Adds to characters dictionary, should always
            be True unless character is created not to participate in the game world...

        give_civilian_items/gci_kwargs // give_bt_items/gbti_kwargs:
            *Note: bt_ ==> base_traits* (award items for profession)
            Give/Equip item sets using auto_buy without paying cash.
            Expects a dict of kwargs or we just take our best guess.
        spells_to_tier/stt_kwargs: Award spells and kwargs for the func
        '''
        if tier_kwargs is None:
            tier_kwargs = {}
        if gci_kwargs is None:
            gci_kwargs = {}
        if gbti_kwargs is None:
            gbti_kwargs = {}
        if stt_kwargs is None:
            stt_kwargs = {}

        rg = rChar()

        if not id:
            id = choice(rchars.keys())
        elif id not in rchars:
            raise Exception(str("Unknown id %s when creating a random character!" % (id)))
        data = rchars[id]
        rg.id = id

        # Blocking traits:
        for key in ("blocked_traits", "ab_traits"):
            if key in data:
                _traits  = set()
                for t in data[key]:
                    if t in store.traits:
                        _traits.add(store.traits[t])
                    else:
                        char_debug("%s trait is unknown for %s (In %s)!" % (t, id, key))
                setattr(rg.traits, key, _traits)

        # Traits next:
        if "random_traits" in data:
            for item in data["random_traits"]:
                trait, chance = item
                if dice(chance):
                    trait = traits.get(trait, None)
                    if trait is None:
                        char_debug(str("Unknown trait: %s for random girl: %s!" % (item[0], id)))
                    elif trait.basetrait:
                        char_debug(str("Trait: %s for random girl: %s is a basetrait which can not be set this way!" % (trait.id, id)))
                    else:
                        rg.apply_trait(trait)

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

        origin = data.get("origin", None)
        if origin is None:
            origin = choice(["Alkion", "PyTFall", "Crossgate"])
        elif not isinstance(origin, basestring):
            origin = choice(origin)
        rg.origin = origin

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
                rg.home = locations["City Apartments"]
                set_location(rg, locations["City"])

        # BASE TRAITS:
        selection = None
        if bt_direct:
            selection = bt_direct
        elif bt_go_patterns:
            selection = create_traits_base(bt_go_patterns)
        elif bt_group:
            selection = choice(base_trait_presets[choice(base_traits_groups[bt_group])])
        elif bt_preset:
            selection = choice(base_trait_presets[bt_preset])
        else:
            selection = base_trait_presets["Combatant"] + base_trait_presets["SIW"] + base_trait_presets["Maid"]
            selection = choice(selection)

        if len(selection) > 2:
            selection = random.sample(selection, 2)

        basetraits = set()
        for t in selection:
            if isinstance(t, basestring):
                t = traits[t]
            basetraits.add(t)
        rg.traits.basetraits = basetraits
        for t in basetraits:
            rg.apply_trait(t)

        # Battle and Magic skills:
        if "default_attack_skill" in data:
            skill = data["default_attack_skill"]
            if skill in store.battle_skills:
                rg.default_attack_skill = store.battle_skills[skill]
            else:
                char_debug(str("Unknown default battle skill: %s for random girl: %s!" % (skill, id)))

        if "magic_skills" in data:
            for skill, chance in data["magic_skills"]:
                if dice(chance):
                    ms = store.battle_skills.get(skill, None)
                    if ms is None:
                        char_debug(str("Unknown magic skill: %s for random girl: %s!" % (skill, id)))
                    elif ms in rg.magic_skills:
                        char_debug(str("Magic skill: %s added twice for random girl: %s!" (skill, id)))
                    else:
                        rg.magic_skills.append(ms) 

        # Rest of the expected data:
        for i in ("gold", "desc", "height", "full_race"):
            if i in data:
                setattr(rg, i, data[i])

        # Colors in say screen:
        for key in ("color", "what_color"):
            if key in data:
                color = data[key]
                if color in globals():
                    color = getattr(store, color)
                else:
                    try:
                        color = Color(color)
                    except:
                        char_debug("Invalid %s: %s for random girl: %s!" % (key, data[key], id))
                        color = ivory
                rg.say_style[key] = color

        # Normalizing new girl:
        # We simply run the init method of parent class for this:
        super(rChar, rg).init()

        # And at last, leveling up and stats/skills applications:
        tier_up_to(rg, tier, **tier_kwargs)

        # Items, give and/or autoequip:
        initial_item_up(rg, give_civilian_items, give_bt_items,
                            gci_kwargs, gbti_kwargs)

        # if equip_to_tier: # Old (faster but less precise) way of giving items:
        #     give_tiered_items(rg, **gtt_kwargs) # (old/simle(er) func)

        # Spells to Tier:
        if spells_to_tier:
            give_tiered_magic_skills(rg, **stt_kwargs)

        # And add to char! :)
        if add_to_gameworld:
            rg.log_stats()
            dict_id = "_".join([rg.id, rg.name, rg.fullname.split(" ")[1]])
            rg.dict_id = dict_id
            store.chars[dict_id] = rg

        return rg

    def initial_item_up(char, give_civilian_items=False, give_bt_items=False,
                        gci_kwargs=None, gbti_kwargs=None):
        """Gives items to a character as well as equips for a specific task.

        Usually ran right after we created the said character.
        """
        if give_civilian_items or give_bt_items:
            container = []
            limit_tier = ((char.tier/2)+1)
            for i in range(limit_tier):
                container.extend(store.tiered_items.get(i, []))

        if give_civilian_items:
            if not gci_kwargs:
                gci_kwargs = {
                    "slots": {slot: 1 for slot in EQUIP_SLOTS},
                    #"casual": True,  - ignored and not necessary anyway
                    "equip": not give_bt_items, # Equip only for civ items.
                    "purpose": "Slave" if char.status == "slave" else "Casual",
                    "check_money": False,
                    "limit_tier": False, # No need, the items are already limited to limit_tier
                    "container": container,
                    "smart_ownership_limit": False
                }
            char.auto_buy(**gci_kwargs)

        if give_bt_items:
            if not gbti_kwargs:
                gbti_kwargs = {
                    "slots": {slot: 1 for slot in EQUIP_SLOTS},
                    #"casual": True, - ignored and no necessary anyway
                    "equip": True,
                    "check_money": False,
                    "limit_tier": False, # No need, the items are already limited to limit_tier
                    "container": container,
                    "smart_ownership_limit": give_civilian_items,

                    "purpose": None, # Figure out in auto_buy method.
                    "direct_equip": True
                }
            char.auto_buy(**gbti_kwargs)

    def auto_buy_for_bt(char, slots=None, casual=None, equip=True,
                        check_money=False, limit_tier=False,
                        container=None):
        if slots is None:
            slots = {slot: 1 for slot in EQUIP_SLOTS}
        if casual is None:
            casual = True
        if container is None:
            container = []
            limit_tier = ((char.tier/2)+1)
            for i in range(limit_tier):
                container.extend(store.tiered_items.get(i, []))

        char.auto_buy(slots=slots, casual=casual, equip=equip,
                      check_money=check_money, limit_tier=limit_tier,
                      container=container)

    def create_traits_base(patterns):
        """Create a pattern with one or two base traits for a character.

        patterns: Single general occupation or list of the same to build a specific pattern from.
        """
        try:
            if isinstance(patterns, basestring):
                patterns = [patterns]
            patterns = list(chain.from_iterable(gen_occ_basetraits[p] for p in patterns))
            if len(patterns) > 1 and dice(55):
                return random.sample(patterns, 2)
            else:
                return random.sample(patterns, 1)
        except:
            raise Exception("Cannot create base traits list from patterns: {}".format(patterns))

    def give_tiered_items(char, amount=1, gen_occ=None, occ=None, equip=False):
        """Gives items based on tier and class of the character.

        amount: Usually 1, this number of items will be awarded per slot.
            # Note: atm we just work with 1!
        gen_occ: General occupation that we equip for: ("SIW", "Combatant", "Server", "Specialist")
            This must always be provided, even if occ is specified.
        occ: Specific basetrait.
        equip: Run auto_equip function after we're done.
        """
        tier = max(min(round_int(char.tier*.5), 4), 0)
        if gen_occ is None:
            try:
                gen_occ = choice(char.gen_occs)
            except:
                raise Exception(char.name, char.__class__)
        if char.status == "slave" and gen_occ == "Combatant":
            problem = (char.name, char.__class__)
            char_debug("Giving tiered items to a Combatant Slave failed: {}".format(problem))
            return
        # See if we can get a perfect occupation:
        if occ is None:
            basetraits = gen_occ_basetraits[gen_occ]
            basetraits = char.basetraits.intersection(basetraits)
            if basetraits:
                occ = random.sample(basetraits, 1)[0].id
        if char.status == "slave" and occ in gen_occ_basetraits["Combatant"]:
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
                purpose = "Mage"
            elif "Combatant" in char.gen_occs:
                purpose = "Combat"
            elif "SIW" in char.gen_occs:
                purpose = "Sex"
            elif "Server" in char.gen_occs:
                purpose = "Service"
            elif "Specialist" in char.gen_occs:
                purpose = "Manager"
            char.equip_for(purpose)

    def give_tiered_magic_skills(char, amount=None, support_amount=None):
        """Gives spells based on tier and class of the character.
        *We assume that is called on a char that actually needs it.

        amount: Amount of skills to give. "auto" will get it from occupations and tiers.
        support_amount: healing and status spells (forced).
        """
        tier = max(min(round_int(char.tier*.5), 4), 0)
        attributes = set([t.id.lower() for t in char.elements])
        if support_amount is None:
            if traits["Healer"] in char.traits.basetraits:
                s_amount = max(tier, 2)
            elif traits["Healer"] in char.traits:
                s_amount = max(tier, 1)
            else:
                s_amount = 0
        else:
            s_amount = support_amount

        if amount is None:
            if "Caster" in char.gen_occs:
                amount = tier + randint(1, 2)
                s_amount += 1
            elif "Combatant" in char.gen_occs or "Specialist" in char.gen_occs:
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
                    spells = tiered_magic_skills[_][:] # testing spells have tier higher than 10
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
        global CHARS_INIT_PHASE

        # exp = level*(level-1)*500
        # char.stats.level = 1
        # char.exp = 0
        # char.stats.goal = 1000
        # char.stats.goal_increase = 1000

        CHARS_INIT_PHASE = True
        exp = level*1000
        char.exp += exp
        CHARS_INIT_PHASE = False

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
        return exp
        # if isinstance(char, int): # A level was provided directly
        #     level = char
        # else:
        #     level = char.level

        # if char == hero:
        #     if level < 10:
        #         mod = 1.4
        #     elif level < 30:
        #         mod = 1.3
        #     elif level < 40:
        #         mod = 1.2
        #     else:
        #         mod = 1.1
        # else:
        #     if level < 10:
        #         mod = .9
        #     elif level < 20:
        #         mod = .8
        #     elif level < 30:
        #         mod = .75
        #     elif level < 40:
        #         mod = .70
        #     elif level < 50:
        #         mod = .65
        #     elif level < 60:
        #         mod = .6
        #     elif level < 70:
        #         mod = .5
        #     else:
        #         mod = .4
        # return int(math.ceil(level*exp))

    def build_client(id=None, gender="male", caste="Peasant",
                     name=None, last_name=None,
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

        # Names:
        if not name:
            name = get_first_name(gender)
        if not last_name:
            last_name = get_last_name()
        client.name = name
        client.fullname = client.nickname = " ".join([name, last_name])

        # Patterns:
        if pattern is None:
            pattern = choice(tuple(STATIC_CHAR.GEN_OCCS))
        pattern = create_traits_base(pattern)
        for i in pattern:
            client.traits.basetraits.add(i)
            client.apply_trait(i)

        # Add a couple of client traits: <=== This may not be useful...
        trts = random.sample(tgs.client, randint(2, 5))
        for t in trts:
            client.apply_trait(t)

        if dice(20):
            client.apply_trait("Aggressive")

        # Likes:
        # Add some traits from trait groups:
        cl = set()
        cl.add(choice(tgs.breasts))
        cl.add(choice(tgs.body))
        cl.add(choice(tgs.race))
        cl.update(random.sample(tgs.base, randint(1, 2)))
        cl.update(random.sample(tgs.elemental, randint(2, 3)))
        cl.update(random.sample(tgs.ct, randint(2, 4)))
        cl.update(random.sample(tgs.sexual, randint(1, 2)))

        if likes:
            cl.update(likes)
            # We pick some of the traits to like/dislike at random.

        if gender == "female":
            cl.add(traits["Lesbian"])
        else: #if gender == "male":
            cl.discard(traits["Lesbian"])

        client.likes = cl

        tier_up_to(client, tier)

        return client

    def copy_char(char):
        """Attempt to copy a character by remaking it anew in his own image.
        """
        if isinstance(char, PytGroup):
            char = char._first

        new = char.__class__()

        for attr, value in char.__dict__.items():
            if attr == "effects":
                new.effects = deepcopy(value)
            elif isinstance(value, (bool, float, basestring, int, Trait)):
                setattr(new, attr, value)
            elif isinstance(value, (dict, set)):
                setattr(new, attr, value.copy())
            elif isinstance(value, list):
                char_debug("{}".format(value))
                setattr(new, attr, value[:])

        assign_to = new.stats
        for attr, value in char.stats.__dict__.items():
            if attr == "skills":
                assign_to.skills = deepcopy(value)
            if attr == "skills_multipliers":
                assign_to.skills_multipliers = deepcopy(value)
            elif isinstance(value, (bool, float, basestring, int)):
                setattr(assign_to, attr, value)
            elif isinstance(value, (dict, set)):
                setattr(assign_to, attr, deepcopy(value))
            elif isinstance(value, list):
                setattr(assign_to, attr, value[:])

        # Smart Trackers:
        new.traits[:] = list(char.traits)
        new.traits.normal = char.traits.normal.copy()
        new.traits.items = char.traits.items.copy()
        new.traits.ab_traits = char.traits.ab_traits.copy()
        new.traits.blocked_traits = char.traits.blocked_traits.copy()
        new.traits.basetraits = char.traits.basetraits.copy()

        new.resist[:] = list(char.resist)
        new.attack_skills.normal = char.attack_skills.normal.copy()
        new.attack_skills.items = char.attack_skills.items.copy()

        new.attack_skills[:] = list(char.attack_skills)
        new.attack_skills.normal = char.attack_skills.normal.copy()
        new.attack_skills.items = char.attack_skills.items.copy()
        new.magic_skills[:] = list(char.magic_skills)
        new.magic_skills.normal = char.magic_skills.normal.copy()
        new.magic_skills.items = char.magic_skills.items.copy()

        return new

    def remove_from_gameworld(char):
        # Try to properly delete the char...
        char.action = None
        char.location = None
        char.home = None
        char.workplace = None

        sm = pytfall.sm # SlaveMarket
        if char in sm.chars_list:
            sm.chars_list.remove(char)

        global gm
        gm.remove_girl(char) # gm is poorly named and can be overwritten...

        if getattr(char, "dict_id", None):
            id = char.dict_id
        else:
            id = char.id

        global chars
        if id in chars:
            del (chars[id])

        del(char)

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
            jobs = building.get_valid_jobs(char)
            if not jobs:
                job = None
            else:
                job = choice(jobs)

        # We prolly still want to set a workplace...
        char.workplace = building
        char.action = job

    def tier_up_to(char, tier, level_bios=(.9, 1.1),
                   skill_bios=(.65, 1.0), stat_bios=(.65, 1.0)):
        """Tiers up a character trying to set them up smartly

        @params:
        char: Character object or id
        tier: Tier number to level to (10 is max and basically a God)
        bios: When setting up stats and skills, uniform between the two values
              will be used.
              Level, stats and skills biases work in the same way

        Important: Should only be used right after the character was created!
        """
        level_bios = partial(uniform, level_bios[0], level_bios[1])
        skill_bios = partial(uniform, skill_bios[0], skill_bios[1])
        stat_bios = partial(uniform, stat_bios[0], stat_bios[1])
        # Level with base 20
        level = tier*20
        if level:
            level = round_int(level*level_bios())
            initial_levelup(char, level)

        # devlog.info("")
        # devlog.info("MEOW: Char/Tier: {}/{}".format(char.name, tier))
        # devlog.info("Base: {}".format(char.traits.base_to_string))

        # Do the stats/skills:
        base_skills = set()
        base_stats = set()
        # !!! Using weight may actually confuse thing in here... this needs testing.
        # Also, it may be a good idea to do list(s) of stats/skills every ht char should have a bit of...
        for trait in char.traits.basetraits:
            skills = trait.base_skills
            total_weight_points = sum(skills.values())
            total_skill_points = sum(char.get_max_skill(s, tier)*.6 for s in skills)
            for skill, weight in skills.items():
                # devlog.info("SKILL/Pre-Value: {}/{}".format(skill, char.get_skill(skill)))
                base_skills.add(skill)
                weight_ratio = float(weight)/total_weight_points
                # devlog.info("Weight Ratio: {}".format(weight_ratio))
                sp = total_skill_points*weight_ratio
                # devlog.info("Skill Points: {}".format(sp))
                # # weight_sp = weight_ratio*sp
                # # devlog.info("Weighted Points: {}".format(weight_sp))
                biosed_sp = round_int(sp*skill_bios())
                # devlog.info("Biased Points: {}".format(biosed_sp))

                char.stats.mod_full_skill(skill, biosed_sp)

                # devlog.info("Resulting Skill: {}".format(char.get_skill(skill)))

            stats = trait.base_stats
            total_weight_points = sum(stats.values())
            total_stat_points = sum(char.get_relative_max_stat(s, tier) for s in stats)
            for stat, weight in stats.items():
                base_stats.add(stat)
                weight_ratio = float(weight)/total_weight_points
                sp = total_stat_points*weight_ratio
                # weight_sp = weight_ratio*sp
                biosed_sp = round_int(sp*stat_bios())

                char.mod_stat(stat, biosed_sp)

        # devlog.info("")

        # Now that we're done with baseskills, we can play with other stats/skills a little bit
        for stat in char.stats.stats:
            if stat not in char.stats.FIXED_MAX and stat not in base_stats:
                if dice(char.luck*.5):
                    value = char.get_max(stat)*.3
                    value = round_int(value*stat_bios())
                    char.mod_stat(stat, value)
                else:
                    value = char.get_max(stat)*uniform(.05, .15)
                    value = round_int(value*stat_bios())
                    char.mod_stat(stat, value)
        for skill in char.stats.skills:
            if skill not in base_skills:
                if dice(char.luck*.5):
                    value = (SKILLS_MAX[skill]*(tier*.1))*.3
                    value = round_int(value*skill_bios())
                    char.mod_skill(skill, value)
                else:
                    value = (SKILLS_MAX[skill]*(tier*.1))*uniform(.05, .15)
                    value = round_int(value*skill_bios())
                    char.mod_skill(skill, value)

        char.tier = round_int(tier) # Makes sure we can use float tiers

    def exp_reward(char, difficulty, value=None,
                   ap_adjust=True, ap_used=1,
                   char_tier_override=False,
                   final_mod=None):
        """Adjusts the XP to be given to an actor. Doesn't actually award the EXP.

        char: Target actor.
        difficulty: Ranged 1 to 10. (will be normalized otherwise).
            This can be a number, Team or Char.
        value: Value to award, if None, we interpolate.
        ap_adjust: Makes sure that chars with loads of AP don't snowball.
        ap_used: AP used for the action, can be a float!
        char_tier_override: If not False, should be a number between 1 - 10.
            It will be used to match difficulty against.
        final_mod: We multiply the result with it. Could be useful when failing
            a task, give at least 10% of the exp (for example) is to set this mod
            to .1 in case of a failed action.
        """
        # Figure out the value:
        if value is None:
            value = DAILY_EXP_CORE

        if ap_adjust:
            value = float(value)/(char.setAP or 3)

        value *= ap_used

        # Now let's see about the difficulty:
        char_tier = char_tier_override or char.tier
        if isinstance(difficulty, Team):
            difficulty = difficulty.get_level()/20.0
        elif isinstance(difficulty, PytCharacter):
            difficulty = difficulty.tier
        elif isinstance(difficulty, (float, int)):
            difficulty = max(0, min(10, difficulty))
        else:
            raise Exception("Invalid difficulty type {} provided to exp_reward function.")

        # Difficulty modifier:
        # Completed task oh higher difficulty:
        if difficulty >= char_tier:
            diff = difficulty - char_tier
            diff = min(2, diff)
            mod = 1+diff/2.0 # max bonus mod possible is 2x the EXP.
        else: # Difficulty was lower
            diff = char_tier - difficulty
            diff = min(2, diff)
            if diff > 2:
                diff = 2
            mod = 1-diff/2.0

        value *= mod

        # Apply the final mod:
        if final_mod is not None:
            value *= final_mod

        return round_int(value)

    def gold_reward():
        """
        TODO: Do the same as above for money using one or more functions.
        """
        pass

    #def get_act(character, tags): # copypaste from jobs without the self part, allows to randomly select one of existing tags sets
    #        acts = list()
    #        for t in tags:
    #            if isinstance(t, tuple):
    #                if character.has_image(*t):
    #                    acts.append(t)
    #            elif isinstance(t, dict):
    #                if character.has_image(*t.get("tags", []), exclude=t.get("exclude", [])) and dice(t.get("dice", 100)):
    #                    acts.append(t)

    #        if acts:
    #            act = choice(acts)
    #        else:
    #            act = None

    #        return act

    # copypaste of get_act from jobs without the self part, allows to randomly select one of existing tags sets
    #  unlike the function from jobs it supports only one set of excluded tags
    def get_simple_act(char, tags, excluded=None):
        acts = list()
        for t in tags:
            if char.has_image(*t, exclude=excluded):
                acts.append(t)
        if acts:
            act = choice(acts)
        else:
            act = None
        return act