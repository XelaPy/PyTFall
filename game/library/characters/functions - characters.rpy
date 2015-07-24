init -11 python:
    # Characters related:
    def load_random_names(amount):
        # Loads random amount of names from our name files:
        file = open(renpy.loader.transfn(content_path("db/RandomGirlNames_1.txt")))
        randomNames = file.readlines()
        file.close()
        file = open(renpy.loader.transfn(content_path("db/RandomGirlNames_2.txt")))
        randomNames.extend(file.readlines())
        file.close()
        
        # @Review: Remove empty space:
        randomNames = list(n.replace('\n', '') for n in randomNames)
        return random.sample(randomNames, amount)
        
    def load_random_last_names(amount):
        # Loads random amount of last names from our last names file:
        file = open(renpy.loader.transfn(content_path("db/RandomLastNames.txt")))
        randomLastNames = file.readlines()
        file.close()
        
        # @Review: Remove empty space:
        randomLastNames = list(n.replace('\n', '') for n in randomLastNames)
        return random.sample(randomLastNames, amount)
        
    def build_mob(id=None, level=1):
        mob = Mob()
        Stats = mob.STATS
        Skills = mob.stats.skills.keys()
        
        if not id:
            id = choice(mobs.keys())
            
        if id in mobs:
            data = mobs[id]
            mob.id = id
        else:
            raise Exception("Unknown id {} when creating a mob!".format(id))
        
        if "name" in data:
            mob.name = data["name"]
        else:
            mob.name = mob.id
            
        if "desc" in data:
            mob.desc = data["desc"]
        else:
            mob.desc = "A Mob!"
            
        for i in ("battle_sprite", "portrait", "origin", "locations", "base_race", "race", "front_row"):
            if i in data:
                setattr(mob, i, data[i])
        
        if "stats" in data:
            d = data["stats"]
            for key in d:
                if key in Stats:
                    if key != "luck":
                        value = d[key]
                        value = int(round(float(value)*100 / mob.get_max(key)))
                        mob.mod(key, value)
                    elif key == "luck":
                        mob.mod(key, d[key])
                else:
                    devlog.warning(str("Stat: {} for Mob with id: {} is invalid! ".format(key, id)))
                    
        if "skills" in data:
            d = data["skills"]
            for key in d:
                if key.lower() in Skills:
                    value = d[key]
                    setattr(mob, key.lower(), value * (2/3.0))
                    setattr(mob, key.capitalize(), value * (1/3.0))
                else:
                    devlog.warning(str("Skill: {} for Mob with id: {} is invalid! ".format(key, id)))
                    
        # Get and normalize basetraits:
        if "basetraits" in data:
            basetraits = set()
            if data["basetraits"]:
                for trait in data["basetraits"]:
                    if trait in traits:
                        basetraits.add(traits[trait])
                    else:
                        devlog.warning("{} besetrait is unknown for Mob {}!".format(trait, id))
                        
            if len(basetraits) > 2:
                while len(basetraits) > 2:
                    basetraits.pop()
                    
            # In case that we have basetraits:
            if basetraits:
                mob.traits.basetraits = basetraits
            
            for trait in mob.traits.basetraits:
                mob.apply_trait(trait)
            
                    
        if "traits" in data:
            d = data["traits"]
            for trait in d:
                if trait in traits:
                    trait = traits[trait]
                else:
                    devlog.warning(str("Trait: {} for Mob with id: {} is invalid! ".format(trait, id)))
                    continue
                mob.apply_trait(trait)
                
        if "attack_skills" in data:
            d = data["attack_skills"]
            for skill in d:
                if skill in store.battle_skills:
                    mob.attack_skills.append(store.battle_skills[skill])
                else:
                    devlog.warning(str("{} Mob tried to apply unknown battle skill: {}!".format(id, skill)))
        
        if "magic_skills" in data:
            d = data["magic_skills"]
            for skill in d:
                if skill in store.battle_skills:
                    mob.magic_skills.append(store.battle_skills[skill])
                else:
                    devlog.warning(str("{} Mob tried to apply unknown battle skill: {}!".format(id, skill)))
            
        mob.init()
        
        if level != 1:
            initial_levelup(mob, level)
            
        return mob
        
    def build_rc(id=None, name=None, last_name=None, pattern=None, level=1, add_to_gameworld=True):
        '''
        Creates a random character!
        id: id to choose from the rchar dictionary that holds rGirl loading data from JSON files, will be chosen at random if none availible.
        name: (String) Name for a girl to use. If None one will be chosen from randomNames file!
        last_name: Same thing only for last name :)
        pattern: Pattern to use when creating the character! (Options atm: Warrior, ServiceGirl, Prostitute, Stripper) If None, we use data or normalize in init()
        level: Level of the character...
        add_to_gameworld: Adds to characters dictionary, should always be True unless character is created not to participate in the game world...
        '''
        rg = rGirl()
        Stats = rg.STATS
        Skills = rg.stats.skills.keys()
        
        if not id:
            id = choice(rchar.keys())
        
        if id in rchar:
            data = rchar[id]
            rg.id = id
        else:
            raise Exception("Unknown id {} when creating a random character!".format(id))
        
        # rg.id = id
        
        # Elements:
        if "elements" in data:
            for key in data["elements"]:
                if dice(data["elements"][key]):
                    if key not in traits:
                        key = key.split(" ")[0]
                    if key not in traits:
                        devlog.warning("Element (*Split with ' '): {} for random girl with id: {} is not a valid element for this game!".format(str(key), str(id)))
                        continue
                    rg.apply_trait(traits[key])
                    
        # Traits next:
        if "random_traits" in data:
            for trait in data["random_traits"]:
                chance = trait[1]
                trait = trait[0]
                if dice(chance):
                    if trait in traits:
                        rg.apply_trait(traits[trait])
                    else:
                        devlog.warning("Trait: {} for random girl with id: {} is not a valid trait for this game!".format(str(trait), str(id))) # Added str() call to avoid cp850 encoding
        
        # Names/Origin:
        if not name:
            if not store.random_names:
                store.random_names = load_random_names(200)
            rg.name = random_names.pop()
        else:
            rg.name = name
            
        if not last_name:
            if not store.random_last_names:
                store.random_last_names = load_random_last_names(200)
            rg.fullname = " ".join([rg.name, random_last_names.pop()])
            
        rg.nickname = rg.name
        
        if "origin" not in data:
            rg.origin = "Random Girl"
        
        # Status next:
        if "force_status" in data:
            if data["force_status"]:
                rg.status = data["force_status"]
            else:
                rg.status = choice(["slave", "free"])
        
        # Location if forced:
        if "force_location" in data:
            if data["force_location"]:
                rg.location = data["force_location"]
                
        # Occupations:
        # This is possibly temporary: TODO: Update after discussion:
        if "init_basetraits" in data:
            d = data["init_basetraits"]
            if pattern not in d:
                devlog.warning(str("{} Random Girl tried to apply blocked pattern: {}!".format(id, pattern)))
            rg.occupation = choice(d)    
        
        # Battle and Magic skills:
        # TODO: This should be battle_skills! (plural and a list))
        if "battle_skill" in data:
            d = data["battle_skill"]
            if d in store.battle_skills:
                rg.attack_skills.append(store.battle_skills[d])
            else:
                devlog.warning(str("%s Random Girl tried to apply unknown battle skill: %s!" % (id, d)))
            
        if "magic_skills" in data:
            d = data["magic_skills"]
            for skill in d:
                if dice(skill[1]):
                    if skill[0] in store.battle_skills:
                        rg.magic_skills.append(store.battle_skills[skill[0]])
                    else:
                        devlog.warning(str("%s Random Girl tried to apply unknown battle skill: %s!" % (id, skill[0])))
                        
        # SKILLS:
        if "random_skills" in data:
            d = data["random_skills"]
            for key in d:
                if key.lower() in Skills:
                    value = randint(d[key][0], d[key][1])
                    setattr(rg, key.lower(), value * (2/3.0))
                    setattr(rg, key.capitalize(), value * (1/3.0))
                else:
                    devlog.warning(str("Skill: %s for random girl with id: %s is invalid! "%(key, id)))
                    
        # STATS:
        if "random_stats" in data:
            d = data["random_stats"]
            for key in d:
                if key in Stats:
                    if key != "luck":
                        value = randint(d[key][0], d[key][1])
                        value = int(round(float(value)*100 / rg.get_max(key)))
                        rg.mod(key, value)
                    elif key == "luck":
                        rg.mod(key, randint(d[key][0], d[key][1]))
                else:
                    devlog.warning(str("Stat: %s for random girl with id: %s is invalid! " % (key, id)))
        
        # Normalizing if not all stats were supplied:
        for stat in Stats:
            if stat not in rg.stats.FIXED_MAX and getattr(rg, stat) == 0:
                setattr(rg, stat, randint(10, 25))
                    
        # Rest of the expected data:
        for i in ("desc", "race", "base_race"):
            if i in data:
                setattr(rg, i, data[i])
        
        # Normalizing new girl:
        # We simply run the init method of parent class for this:
        super(rGirl, rg).init()
        
        # And at last, leveling up and stats/skills applications:
        if level != 1:
            initial_levelup(rg, level)
            
        # And add to char! :)
        if add_to_gameworld:
            store.char["_".join([rg.id, rg.name, rg.fullname.split(" ")[1]])] = rg
            
        return rg
    
    def initial_levelup(chr, level, max_out_stats=False):
        """
        This levels up the character, usually when it's first created.
        """
        exp = level*(level-1)*500
        chr.stats.level = 1
        chr.exp = 0
        chr.stats.goal = 1000
        chr.stats.goal_increase = 1000

        chr.exp += exp
        
        if max_out_stats:
            for stat in chr.stats.stats:
                if stat not in ["alignment"]:
                    setattr(chr, stat, chr.get_max(stat))
        # -------- 
        
    def adjust_exp(chr, exp):
        '''
        Adjusts experience according to a level of character.
        We will find a better way to handle experience in the future.
        '''
        if chr == hero:
            if chr.level < 10:
                return int(math.ceil(chr.level * exp)*1.4)
            elif chr.level < 30:
                return int(math.ceil(chr.level * exp)*1.3)
            elif chr.level < 40:
                return int(math.ceil(chr.level * exp)*1.2)
            else:
                return int(math.ceil(chr.level * exp)*1.1)
        elif isinstance(chr, Girl):
            if chr.level < 10:
                return int(math.ceil(chr.level * exp)*0.9)
            elif chr.level < 20:
                return int(math.ceil(chr.level * exp)*0.8)
            elif chr.level < 30:
                return int(math.ceil(chr.level * exp)*0.75)
            elif chr.level < 40:
                return int(math.ceil(chr.level * exp)*0.70)
            elif chr.level < 50:
                return int(math.ceil(chr.level * exp)*0.65)
            elif chr.level < 60:
                return int(math.ceil(chr.level * exp)*0.6)
            elif chr.level < 70:
                return int(math.ceil(chr.level * exp)*0.5)
            else:
                return int(math.ceil(chr.level * exp)*0.4)
        return int(math.ceil(chr.level * exp))
        
    def create_traits_base(pattern):
        """
        Mostly used for NPCs and Random Characters.
        The idea is to attempt creation of interesting and dynamic blue-prints. 
        For the future this prolly should return a matrix or a dict with prof-base and support traits separetly...
        """
        _traits = list()
        if pattern == "Warrior":
            basetrait = choice([traits["Warrior"], traits["Mage"]])
            _traits.append(basetrait)
        elif pattern == "ServiceGirl":
            _traits.append(traits["Service"])
        elif pattern == "Prostitute":
            _traits.append(traits["Prostitute"])
        elif pattern == "Stripper":
            _traits.append(traits["Stripper"])
        else:
            raise Exception("Cannot create base traits list from pattern: {}".format(pattern))
            
        return _traits
