init -11 python:
    # ---------------------- Loading game data:
    def load_team_names(amount):
        with open(content_path("db/names/team_names.json")) as f:
            rn = json.load(f)
        return random.sample(rn, amount)
        
    def load_male_first_names(amount):
        with open(content_path("db/names/male_first_names.json")) as f:
            rn = json.load(f)
        return random.sample(rn, amount)
    
    def load_female_first_names(amount):
        with open(content_path("db/names/female_first_names_1.json")) as f:
            rn1 = json.load(f)
        with open(content_path("db/names/female_first_names_2.json")) as f:
            rn2 = json.load(f)
        rn = rn1 + rn2
        return random.sample(rn, amount)
        
    def load_random_last_names(amount):
        with open(content_path("db/names/last_names.json")) as f:
            rn = json.load(f)
        return random.sample(rn, amount)
        
    def load_mc_images():
        dir = content_path("gfx/sprites/mc")
        dirlist = os.listdir(dir)
        content = OrderedDict()
        
        for folder in dirlist:
            content[folder] = dict()
            for file in os.listdir('/'.join([dir, folder])):
                tag = file.split(" ")[0]
                path = '/'.join(["content/gfx/sprites/mc", folder, file])
                if tag in content[folder]:
                    content[folder][tag].append(path)
                else:
                    content[folder][tag] = list()
                    content[folder][tag].append(path)
                    
        return content            
    
    def load_characters(path, cls):
        """Loads a Full character from JSON file.
        
        path: Path to main folder.
        class: Class to use in creating the character.
        
        This will walk through folders inside of a folder where the path leads, looking for JSONs and reading image tags off file names.
        """
        dir = content_path(path)
        dirlist = os.listdir(dir)
        content = dict()
        
        tagdb = store.tagdb
        tags_dict = store.tags_dict
        
        for packfolder in dirlist:
            kind = None
            if os.path.isdir('/'.join([dir, packfolder])):
                # Get to a folder with unique girl datafiles and imagefolders:
                girlfolders = os.listdir('/'.join([dir, packfolder]))
                for file in girlfolders: # Load data files one after another.
                    if file.startswith("data") and file.endswith(".json"):
                        kind = "pytfall_native"
                        
                        # Load the file:
                        in_file = os.sep.join([dir, packfolder, file])
                        devlog.info("Loading from %s!"%str(in_file)) # Str call to avoid unicode
                        with open(in_file) as f:
                            ugirls = json.load(f)
                            
                        # Apply the content of the file to the character:
                        for gd in ugirls: # We go over each dict one mainaining correct order of application:
                            
                            char = cls()
                            
                            if "id" not in gd:
                                # Only time we throw an error instead of writing to log.
                                raise Exception("No id was specified in %s JSON Datafile!" % str(in_file))
                            char.id = gd["id"]
                            
                            # Check if there is a gender:
                            if "gender" in gd:
                                char.gender = gd["gender"]
                            
                            # @Review: We make sure all traits get applied first!
                            for key in ("blocked_traits", "ab_traits"):
                                if key in gd:
                                    _traits  = set()
                                    for t in gd[key]:
                                        if t in store.traits:
                                            _traits.add(store.traits[t])
                                        else:
                                            devlog.warning("%s trait is unknown for %s (In %s)!" % (t, gd["id"], key))
                                    setattr(char.traits, key, _traits)
                                    
                            # Get and normalize basetraits:
                            if "basetraits" in gd:
                                basetraits = set()
                                if gd["basetraits"]:
                                    for trait in gd["basetraits"]:
                                        if trait in traits:
                                            basetraits.add(traits[trait])
                                        else:
                                            devlog.warning("%s besetrait is unknown for %s!" % (trait, gd["id"]))
                                            
                                if len(basetraits) > 2:
                                    while len(basetraits) > 2:
                                        basetraits.pop()
                                        
                                # In case that we have basetraits:
                                if basetraits:
                                    char.traits.basetraits = basetraits
                                
                                for trait in char.traits.basetraits:
                                    char.apply_trait(trait)
                                    
                            for key in ("personality", "breasts", "body", "race"):
                                if key in gd:
                                    trait = gd[key]
                                    if trait in traits:
                                        char.apply_trait(traits[trait])
                                    else:
                                        devlog.warning("%s %s is unknown for %s!" % (trait, key, gd["id"]))
                                    
                            if "elements" in gd:
                                for trait in gd["elements"]:
                                    if trait in traits:
                                        char.apply_trait(traits[trait])
                                    else:
                                        devlog.warning("%s element is unknown for %s!" % (trait, gd["id"]))
                                        
                            if "traits" in gd:
                                for trait in gd["traits"]:
                                    if trait in traits:
                                        char.apply_trait(traits[trait])
                                    else:
                                        devlog.warning("%s trait is unknown for %s!" % (trait, gd["id"]))
                                
                            # Leveling up:
                            if "level" in gd:
                                initial_levelup(char, gd["level"])
                                del gd["level"]
                                
                            if "stats" in gd:
                                for stat in gd["stats"]:
                                    if stat in char.STATS:
                                        value = gd["stats"][stat]
                                        if stat != "luck":
                                            value = int(round(float(value)*char.get_max(stat))/100)
                                        char.mod(stat, value)
                                    else:
                                        devlog.warning("%s stat is unknown for %s!" % (stat, gd["id"]))
                                del gd["stats"]
                                
                            if "skills" in gd:
                                for skill in gd["skills"]:
                                    if skill in char.stats.skills:
                                        value = gd["skills"][skill]
                                        setattr(char, skill.lower(), value * (2/3.0))
                                        setattr(char, skill.capitalize(), value * (1/3.0))
                                    else:
                                        devlog.warning("%s skill is unknown for %s!" % (skill, gd["id"]))
                                del gd["skills"]
                                
                            for key in ("magic_skills", "attack_skills"):
                                if key in gd:
                                    # Skills can be either a list or a dict:
                                    if isinstance(gd[key], list):
                                        skills = gd[key]
                                    else:
                                        skills = gd[key].keys()
                                    for skill in skills:
                                        if skill in store.battle_skills:
                                            skill = store.battle_skills[skill]
                                            char.__dict__[key].append(skill)
                                        else:
                                            devlog.warning("%s JSON Loading func tried to apply unknown battle skill: %s!" % (gd["id"], skill))
                            
                            for key in ("color", "what_color"):
                                if key in gd:
                                    if gd[key] in globals():
                                        color = getattr(store, gd[key])
                                    else:
                                        try:
                                            color = Color(gd[key])
                                        except:
                                            devlog.warning("{} color supplied to {} is invalid!".format(gd[key], gd["id"]))
                                            color = ivory
                                    char.say_style[key] = color
                                            
                            for key in ("name", "nickname", "fullname", "origin", "gold", "desc", "location", "status", "height", "full_race"):
                                if key in gd:
                                    setattr(char, key, gd[key])
                            
                            folder = char.id
                            if os.path.isdir("/".join([dir, packfolder, folder])):
                                # We set the path to the character so we know where to draw images from:
                                setattr(char, "_path_to_imgfolder", "/".join(["content/{}".format(path), packfolder, folder]))
                                # We load the new tags!:
                                for fn in os.listdir("/".join([dir, packfolder, folder])):
                                    if fn.lower().endswith((".jpg", ".png", ".gif", ".jpeg")):
                                        rp_path = "/".join(["content/{}".format(path), packfolder, folder, fn])
                                        tags = fn.split("-")
                                        # TODO: REMOVE TRY BEFORE BUILDING THE GAME! MAY SLOW THINGS DOWN!
                                        try:
                                            del tags[0]
                                            tags[-1] = tags[-1].split(".")[0]
                                        except IndexError:
                                            raise Exception("Invalid file path for image: %s" % rp_path)
                                        for tag in tags:
                                            if tag not in tags_dict:
                                                raise Exception("Unknown image tag: %s, path: %s" % (tag, rp_path))
                                            tagdb.tagmap[tags_dict[tag]].add(fn)
                                        # Adding filenames to girls id:
                                        tagdb.tagmap.setdefault(folder, set()).add(fn)
                                        
                            char.init() # Normalize!
                            content[char.id] = char
                                    
        return content
        
    def load_crazy_characters():
        # Presently broken...
        dir = content_path("chars")
        dirlist = os.listdir(dir)
        content = dict()
        crazy_folders = set()
        all_tags = set(tags_dict.values())
        tagdb = store.tagdb
        for folder in dirlist:
            if os.path.isdir('/'.join([dir, folder])):
                for file in os.listdir('/'.join([dir, folder])):
                    if file.endswith(".girlsx"):
                        crazy_folders.add(folder)
                        content.update(load_database("%s/%s/%s" % (dir, folder, file), entity=Char))
                        
                    # if os.path.isdir("/".join([dir, folder, file])):
                        # # We load the new tags!:
                        # for fn in os.listdir("/".join([dir, folder, file])):
                            # if fn.endswith((".jpg", ".png", ".gif")):
                                # rp_path = "/".join(["content/chars", folder, file, fn])
                                # fn = fn.split(".")[0]
                                # fn = fn.split("-")[1:]
                                # for tag in fn:
                                    # tagdb.tagmap[tags_dict[tag]].add(rp_path)
                                # tagdb.tagmap.setdefault(file, set()).add(rp_path)  
        for folder in crazy_folders:
            if os.path.isdir('/'.join([dir, folder])):
                for file in os.listdir('/'.join([dir, folder])):
                    if os.path.isdir("/".join([dir, folder, file])):
                        # Crazy tags!:
                        for fn in os.listdir("/".join([dir, folder, file])):
                            if fn.lower().endswith((".jpg", ".png", ".gif", ".jpeg")):
                                rp_path = "/".join(["content/chars", folder, file, fn])
                                fn = fn.lower()
                                filetag = None
                                if fn.startswith("profile"):
                                    filetag = "profile"
                                elif fn.startswith("anal"):
                                    filetag = "anal"
                                elif fn.startswith("bdsm"):
                                    filetag = "bdsm"    
                                elif fn.startswith("bunny"):
                                    filetag = "bunny"
                                elif fn.startswith("card"):
                                    filetag = "gambling"
                                elif fn.startswith("combat"):
                                    filetag = "battle"
                                elif fn.startswith("ecchi"):
                                    filetag = "provocative"
                                elif fn.startswith("group"):
                                    filetag = "group"
                                elif fn.startswith("les"):
                                    filetag = "les"
                                elif fn.startswith("mast"):
                                    filetag = "mast"
                                elif fn.startswith("nude"):
                                    filetag = "nude"
                                elif fn.startswith("oral"):
                                    filetag = "blowjob"
                                elif fn.startswith("profile"):
                                    filetag = "profile"
                                elif fn.startswith("sex"):
                                    filetag = "sex"
                                elif fn.startswith("strip"):
                                    filetag = "strip"
                                elif fn.startswith("titty"):
                                    filetag = ["titsjob", "blowjob"]
                                elif fn.startswith("wait"):
                                    filetag = "waitress"
                                elif fn.split()[0] in all_tags:
                                        filetag = fn.split()[0]
                                if filetag != None:
                                    if isinstance(filetag, basestring):
                                        tagdb.tagmap.setdefault(filetag, set()).add(rp_path)
                                    else:
                                        for tag in filetag:
                                            if tag in all_tags:
                                                tagdb.tagmap.setdefault(tag, set()).add(rp_path)
                                    tagdb.tagmap.setdefault(file, set()).add(rp_path)
                                
                                
                                
        for key in content:
            for entry in content[key].xml:
                if entry.tag == 'Trait':
                    # raise Exception, entry.__dict__
                    if entry.attrib["Name"] in traits.keys():
                        content[key].init_traits.append(entry.attrib["Name"])
            setattr(content[key], "name", content[key].id)
            del content[key].__dict__['xml']
            content[key].init()
        # raise Exception, [key.name for key in content.values()]
            
        return content

    def load_random_characters():
        dir = content_path('rchars')
        dirlist = os.listdir(dir)
        random_girls = {}
        tags_dict = store.tags_dict
        
        devlog.info("Loading Random Characters:")
        
        # Loading all rgirls into the game:
        for packfolder in dirlist:
            if os.path.isdir(os.sep.join([dir, packfolder])): #if not packfolder.endswith('.gitignore'):
                girlfolders = os.listdir(os.sep.join([dir, packfolder]))
                for file in girlfolders:
                    if file.startswith('data') and file.endswith('.json'):
                        in_file = os.sep.join([dir, packfolder, file])
                        devlog.info("Loading from %s!"%str(in_file)) # Str call to avoid unicode
                        with open(in_file) as f:
                            rgirls = json.load(f)
                            
                        for gd in rgirls:
                            # @Review: We will return dictionaries instead of blank instances of rGirl from now on!
                            # rg = rChar()
                            if "id" not in gd:
                                # Only time we throw an error instead of writing to log.
                                raise Exception("No id was specified in %s JSON Datafile!" % str(in_file))
                                    
                            random_girls[gd["id"]] = gd
                    
                            folder = gd["id"]
                            
                            # Set the path to the folder:
                            random_girls[gd["id"]]["_path_to_imgfolder"] = "/".join(["content/rchars", packfolder, folder])
                            # We load the new tags!:
                            for fn in os.listdir(os.sep.join([dir, packfolder, folder])):
                                if fn.lower().endswith((".jpg", ".png", ".gif", ".jpeg")):
                                    rp_path = "/".join(["content/rchars", packfolder, folder, fn])
                                    tags = fn.split("-")
                                    # TODO: REMOVE TRY BEFORE BUILDING THE GAME! MAY SLOW THINGS DOWN!
                                    try:
                                        del tags[0]
                                        tags[-1] = tags[-1].split(".")[0]
                                    except IndexError:
                                        raise Exception("Invalid file path for image: %s" % rp_path)   
                                    for tag in tags:
                                        if tag not in tags_dict:
                                            raise Exception("Unknown image tag: %s, path: %s" % (tag, rp_path))
                                        tagdb.tagmap[tags_dict[tag]].add(fn)
                                    # Adding filenames to girls id:
                                    tagdb.tagmap.setdefault(folder, set()).add(fn)
                                    
        return random_girls

    def load_arena_fighters():
        in_file = content_path("db/arena_fighters.json")
        with open(in_file) as f:
            content = json.load(f)
        ac = dict()
        for fighter in content:
            f = ArenaFighter()
            # statz:
            for stat in ilists.battlestats:
                f.stats.max[stat] = 500
                f.stats.lvl_max[stat] = 500
            for attr in fighter:
                # Right now this works off stats so exp does almost nothing.
                if attr == "stats":
                    stats = fighter[attr]
                elif attr == "exp":
                    f.stats.exp + fighter[attr]
                else:
                    f.__dict__[attr] = fighter[attr]
            for stat in stats:
                f.mod(stat, fighter["stats"][stat])
            # Get da picz:     
            dir = content_path("npc/arena")
            for file in os.listdir("/".join([dir, f.name])):
                tag = file.split(" ")[0]
                path = '/'.join([dir, f.name, file])
                if tag in f.img_db:
                    f.img_db[tag].append(path)
                else:
                    f.img_db[tag] = list()
                    f.img_db[tag].append(path)
                
            f.init()
            ac[f.name] = f
        return ac
        
    def load_mobs():
        in_file = content_path("db/mobs.json")
        mobs = dict()
        with open(in_file) as f:
            content = json.load(f)
        
        for mob in content:
            if "id" not in mob:
                mob["id"] = mob["name"]
            mob["defeated"] = 0 # We need to track if the mob was defeated for bestiary.
            mobs[mob["id"]] = mob
        return mobs

    def load_brothels():
        # Outdated, may not be used in the future...
        # Load json content
        in_file = content_path('db/buildings.json')
        with open(in_file) as f:
            content = json.load(f)
        # Populate into brothel objects
        brothels = dict()
        for building in content:
            b = Brothel()
            for attr in building:
                b.__dict__[attr] = building[attr]
            b.init()
            brothels[b.id] = b
        return brothels

    def load_tiles():
        # Load json content
        in_file = content_path('db/tiles.json')
        with open(in_file) as f:
            content = json.load(f)

        tiles = {}
        for tile in content:
            t = Tile()
            for attr in tile:
                t.__dict__[attr] = tile[attr]
            t.init()
            tiles[t.id] = t
        return tiles
        
    def load_json(file):
        """
        Directly returns contents of JSON located in db folder
        """
        in_file = content_path("/".join(["db", file]))
        with open(in_file) as f:
            content = json.load(f)
        return content
        
    def load_traits():
        content = list()
        folder = content_path('db')
        for file in os.listdir(folder):
            # New file "content/db/traits_chances.json" crashes this function as it matches the naming scheme for the traits files, but not the content scheme
            # Added check to remove it from consideration to prevent crashing, should look into changing its name, conforming to scheme, or better check.
            #
            if file.startswith("traits") and file.endswith(".json") and "_chances" not in file:
                in_file = content_path("".join(["db/", file]))
                with open(in_file) as f:
                    content.extend(json.load(f))
        traits = dict()
        for trait in content:
            t = Trait()
            for attr in trait:
                setattr(t, attr, trait[attr])
            traits[t.id] = t
        return traits
        
    def load_fg_areas():
        content = list()
        folder = content_path('db')
        for file in os.listdir(folder):
            if file.startswith("fg_areas") and file.endswith(".json"):
                in_file = content_path("".join(["db/", file]))
                with open(in_file) as f:
                    content.extend(json.load(f))            
        areas = dict()
        for area in content:
            a = FG_Area()
            for attr in area:
                setattr(a, attr, area[attr])
            if not hasattr(a, "name"):
                a.name = a.id
            areas[a.id] = a
        return areas

    def load_items():
        items = dict()
        folder = content_path('db')
        content = list()
        
        for file in os.listdir(folder):
            if file.startswith("items") and file.endswith(".json"):
                in_file = content_path("".join(["db/", file]))
                with open(in_file) as f:
                    content.extend(json.load(f))
                    
        for item in content:
            iteminst = Item()
            for attr in item:
                # We prolly want to convert to objects in case of traits:
                if attr in ("badtraits", "goodtraits"):
                    setattr(iteminst, attr, set(traits[i] for i in item[attr])) # More convinient to have these as sets...
                else:
                    setattr(iteminst, attr, item[attr])
            iteminst.init()
            items[iteminst.id] = iteminst
            
        return items
        
    def load_gifts():
        """
        Returns items dict with gift items to be used during girl_meets.
        """
        unprocessed = dict()
        content = dict()
        folder = content_path('db')
        for file in os.listdir(folder):
            if file.startswith("gifts") and file.endswith(".json"):
                in_file = content_path("/".join(["db", file]))
                with open(in_file) as f:
                    unprocessed = json.load(f)
                for key in unprocessed:
                    item = Item()
                    item.slot = "gift"
                    item.type = "gift"
                    item.__dict__.update(key)
                    content[item.id] = item
        return content
