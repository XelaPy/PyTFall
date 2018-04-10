# The whole thing should one day be recoded over a single renpy.list_files loop.
init 11 python:
    def load_webms():
        webms = {}
        for path in renpy.list_files():
            if "content/gfx/autowebm/" in path:
                split_path = path.split("/")
                folder = split_path[-2]
                file = split_path[-1]
                if "mask" in file:
                    webms.setdefault(folder, {})["mask"] = path
                if "movie" in file:
                    webms.setdefault(folder, {})["movie"] = path
                if "moviemask" in file: # rare cases when movie itself is also the mask
                    webms.setdefault(folder, {})["movie"] = path
                    webms.setdefault(folder, {})["mask"] = path

        for folder in webms:
            temp = folder.split(" ")

            tag = temp[0]
            channel = temp[2] if len(temp) == 3 else "main_gfx_attacks"
            loops = temp[1] if len(temp) >= 2 else 1
            if loops == "inf":
                renpy.image(tag, Movie(channel=channel, play=webms[folder]["movie"], mask=webms[folder].get("mask", None)))
            else:
                loops = int(loops)
                renpy.image(tag, MovieLooped(channel=channel, loops=loops, play=webms[folder]["movie"], mask=webms[folder].get("mask", None)))

    load_webms()

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

                            # if "stats" in gd:
                            #     for stat in gd["stats"]:
                            #         if stat in char.STATS:
                            #             value = gd["stats"][stat]
                            #             if stat != "luck":
                            #                 value = int(round(float(value)*char.get_max(stat))/100)
                            #             char.mod_stat(stat, value)
                            #         else:
                            #             devlog.warning("%s stat is unknown for %s!" % (stat, gd["id"]))
                            #     del gd["stats"]
                            #
                            # if "skills" in gd:
                            #     for skill, value in gd["skills"].items():
                            #         if char.stats.is_skill(skill):
                            #             char.stats.mod_full_skill(skill, value)
                            #         else:
                            #             devlog.warning("%s skill is unknown for %s!" % (skill, gd["id"]))
                            #     del gd["skills"]

                            if "default_attack_skill" in gd:
                                skill = gd["default_attack_skill"]
                                if skill in store.battle_skills:
                                    char.default_attack_skill = store.battle_skills[skill]
                                else:
                                    devlog.warning("%s JSON Loading func tried to apply unknown default attack skill: %s!" % (gd["id"], skill))

                            if "magic_skills" in gd:
                                # Skills can be either a list or a dict:
                                skills = gd["magic_skills"]
                                if isinstance(skills, list):
                                    pass
                                else:
                                    skills = skills.keys()
                                for skill in skills:
                                    if skill in store.battle_skills:
                                        skill = store.battle_skills[skill]
                                        char.magic_skills.append(skill)
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

                            # Note: Location is later normalized in init method.
                            for key in ("name", "nickname", "fullname", "origin", "gold", "desc", "status", "location", "height", "full_race"):
                                if key in ["name", "nickname", "fullname"] and key in gd:
                                    if len(gd[key]) > 20:
                                        temp = gd[key][0:20]
                                        setattr(char, key, gd[key][0:20])
                                    else:
                                        setattr(char, key, gd[key])
                                elif key in gd:
                                    setattr(char, key, gd[key])

                            folder = char.id
                            if os.path.isdir("/".join([dir, packfolder, folder])):
                                # We set the path to the character so we know where to draw images from:
                                setattr(char, "_path_to_imgfolder", "/".join(["content/{}".format(path), packfolder, folder]))
                                # We load the new tags!:
                                for fn in os.listdir("/".join([dir, packfolder, folder])):
                                    if check_image_extension(fn):
                                        rp_path = "/".join(["content/{}".format(path), packfolder, folder, fn])
                                        tags = fn.split("-")
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

                            # Tearing up:
                            # if "level" in gd:
                            #     initial_levelup(char, gd["level"])
                            #     del gd["level"]
                            if "tier" in gd:
                                tier = gd["tier"]
                                if isinstance(tier, dict):
                                    tier_up_to(char, **tier)
                                else:
                                    tier_up_to(char, tier)

                            item_up = gd.get("item_up", "auto")
                            if item_up == "auto":
                                if char.status == "slave":
                                    initial_item_up(char,
                                                    give_civilian_items=True,
                                                    give_bt_items=False)
                                else:
                                    initial_item_up(char,
                                                    give_civilian_items=True,
                                                    give_bt_items=True)
                            elif item_up:
                                initial_item_up(char,
                                                give_civilian_items=True,
                                                give_bt_items=True)

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
                            # if check_image_extension(fn):
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
                            if check_image_extension(fn):
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
                                if check_image_extension(fn):
                                    rp_path = "/".join(["content/rchars", packfolder, folder, fn])
                                    tags = fn.split("-")
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

    def load_special_arena_fighters():
        male_fighters = {}
        female_fighters = {}
        json_fighters = {}
        json_data_raw = json.load(renpy.file("content/db/arena_fighters.json"))
        json_data = {}
        for i in json_data_raw:
            json_data[i["name"]] = i["basetraits"]

        tagdb = store.tagdb
        tags_dict = store.tags_dict

        img_db = {}
        path_db = {}
        gender_db = {}
        for fn in renpy.list_files():
            if "content/npc/arena_males" in fn and fn.lower().endswith(IMAGE_EXTENSIONS):
                split = fn.split("/")
                id = split[-2]
                img_db.setdefault(id, []).append(split[-1])
                path_db[id] = "/".join(split[:-1])
                gender_db[id] = "male"
            elif "content/npc/arena_females" in fn and fn.lower().endswith(IMAGE_EXTENSIONS):
                split = fn.split("/")
                id = split[-2]
                img_db.setdefault(id, []).append(split[-1])
                path_db[id] = "/".join(split[:-1])
                gender_db[id] = "female"
            elif "content/npc/arena_json_adjusted" in fn and fn.lower().endswith(IMAGE_EXTENSIONS):
                split = fn.split("/")
                id = split[-2]
                img_db.setdefault(id, []).append(split[-1])
                path_db[id] = "/".join(split[:-1])
                gender_db[id] = "JSON"

        for id, images in img_db.items():
            path = path_db[id]
            gender = gender_db[id]
            for fn in images:
                rp_path = "/".join([path, fn])
                tags = fn.split("-")
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
                tagdb.tagmap.setdefault(id, set()).add(fn)
            el = list(i.id for i in tgs.elemental)
            elements = []
            random_traits = ["Courageous", "Aggressive", "Vicious"]
            if gender == "JSON":
                base = [traits[t] for t in json_data[id]]
            elif "assassins" in path:
                base = [traits["Assassin"]]
            elif "healers" in path:
                base = [traits["Healer"]]
                base.append(traits["Mage"])
                elements = [traits["Light"]]
                if dice(50):
                    elements.append(traits["Water"])
                if dice(50):
                    elements.append(traits["Air"])
            elif "knights" in path:
                base = [traits["Knight"]]
                if dice(25):
                    base.append(traits["Assassin"])
                if dice(25):
                    base.append(traits["Mage"])
                    elements = [traits[random.choice(el)]]
            elif "mages" in path:
                base = [traits["Mage"]]
                elements = [traits[random.choice(el)]]
            elif "maids" in path:
                base = [traits["Warrior"]]
                base.append(traits["Maid"])
            elif "shooters" in path:
                base = [traits["Shooter"]]
                if dice(25):
                    base.append(traits["Assassin"])
                if dice(25):
                    base.append(traits["Mage"])
                    elements = [traits[random.choice(el)]]
            elif "warriors" in path:
                base = [traits["Warrior"]]
            else:
                base = [traits["Warrior"]]
            if not elements:
                elements = [traits["Neutral"]]
            fighter = NPC()
            fighter._path_to_imgfolder = path
            fighter.id = id
            if gender == "female":
                fighter.name = get_first_name()
                fighter.gender == "female"
                fighter.fullname = " ".join([fighter.name, get_last_name()])
                fighter.nickname = fighter.name
                female_fighters[id] = fighter
            elif gender == "male":
                fighter.gender = "male"
                fighter.name = fighter.fullname = fighter.nickname = id
                male_fighters[id] = fighter
            else: # JSON adjusted
                fighter.id = id
                fighter.name = fighter.fullname = fighter.nickname = id
                json_fighters[id] = fighter

            for t in random.sample(base, min(2, len(base))):
                fighter.traits.basetraits.add(t)
                fighter.apply_trait(t)

            for e in random.sample(elements, max(1, len(elements)-randint(0, 7))):
                fighter.apply_trait(e)

            random_traits = [traits[t] for t in random_traits]
            for e in random.sample(random_traits, max(1, randint(1, len(random_traits)))):
                fighter.apply_trait(e)

            fighter.init()

        return male_fighters, female_fighters, json_fighters

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

    def load_buildings():
        # Load json content
        buildings_data = json.load(renpy.file("content/db/buildings/buildings.json"))
        adverts_data = json.load(renpy.file("content/db/buildings/adverts.json"))

        # Populate into brothel objects:
        buildings = dict()
        for building in buildings_data:
            b = Building()
            # Allowed upgrades for businesses we have not built yet!
            b.allowed_business_upgrades = building.get("allowed_business_upgrades", {})

            for key, value in building.iteritems():
                if key == "adverts":
                    b.add_adverts([adv for adv in adverts_data if adv['name'] in value])
                elif key == "build_businesses":
                    for business_data in value:
                        cls = getattr(store, business_data["class"])
                        kwargs = business_data.get("kwargs", {})

                        # Load allowed business upgrades if there are any:
                        au = [getattr(store, u) for u in kwargs.get("allowed_upgrades", [])]
                        kwargs["allowed_upgrades"] = au

                        b.add_business(cls(**kwargs))
                elif key == "allowed_businesses":
                    for business in value:
                        business = getattr(store, business)
                        b.allowed_businesses.append(business)
                elif key == "allowed_upgrades":
                    for u in value:
                        u = getattr(store, u)
                        if u not in b.allowed_upgrades:
                            b.allowed_upgrades.append(u)
                else:
                    setattr(b, key, value)

            buildings[b.id] = b

        return buildings

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
        folder = content_path('db/traits')
        for file in os.listdir(folder):
            # New file "content/db/traits_chances.json" crashes this function as it matches the naming scheme for the traits files, but not the content scheme
            # Added check to remove it from consideration to prevent crashing, should look into changing its name, conforming to scheme, or better check.
            #
            if file.startswith("traits") and file.endswith(".json") and "_chances" not in file:
                in_file = content_path("".join(["db/traits/", file]))
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
        folder = content_path('db/items')
        content = list()

        for file in os.listdir(folder):
            if file.startswith("items") and file.endswith(".json"):
                in_file = content_path("".join(["db/items/", file]))
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
        folder = content_path('db/items')
        for file in os.listdir(folder):
            if file.startswith("gifts") and file.endswith(".json"):
                in_file = content_path("/".join(["db/items/", file]))
                with open(in_file) as f:
                    unprocessed = json.load(f)

                for key in unprocessed:
                    item = Item()
                    item.slot = "gift"
                    item.type = "gift"
                    item.__dict__.update(key)
                    content[item.id] = item
        return content

    def load_dungeons():
        content = []
        for file in os.listdir(content_path('db')):
            if file.startswith("dungeon") and file.endswith(".json"):

                in_file = content_path("".join(["db/", file]))
                with open(in_file) as f:
                    content.extend(json.load(f))

        return { d['id']: Dungeon(**d) for d in content }

label load_resources:
    $ buildings = dict()

    python hide:
        # MC Apartments:
        ap = InvLocation(id="Studio Apartment", daily_modifier=.15, rooms=1,
                         desc="Comfortable apartment with plenty of storage space!",
                         img="content/gfx/bg/buildings/apartment_1.jpg",
                         price=5000)
        buildings[ap.id] = ap
        # hero.buildings.append(ap)
        # hero.home = ap # Note, we may condition this in MC setup? Maybe? One day :D

        ap = InvLocation(id="Large Apartment", daily_modifier=.12, rooms=3,
                         desc="Comfortable apartment with enough living space for three and a large storage area for all of your items!",
                         img="content/gfx/bg/buildings/Rooms/decent (1).jpg",
                         price=10000)
        buildings[ap.id] = ap
        # hero.buildings.append(ap)
        # hero.home = ap # Note, we may condition this in MC setup? Maybe? One day :D

        ap = InvLocation(id="Lux Apartment", daily_modifier=.25, rooms=6,
                         desc="Enough space for six people and nearly magical restorative effects for all who sleep here.",
                         img="content/gfx/bg/buildings/Rooms/luxury (3).jpg",
                         price=50000)
        buildings[ap.id] = ap
        # hero.buildings.append(ap)
        # hero.home = ap # Note, we may condition this in MC setup? Maybe? One day :D

        if config.debug and not hero.home:
            hero.buildings.append(ap)
            hero.home = ap

    python: # Jail:
        jail = CityJail()
        jail.id = "City Jail"

        # Add the dungeon to the buildings list
        # Load the hero's dungeon
        # school = TrainingDungeon(load_training("training", PytTraining))
        # schools[school.name] = school
        # buildings[TrainingDungeon.NAME] = schools[TrainingDungeon.NAME]
        # if config.developer:
        #     hero.add_building(buildings[TrainingDungeon.NAME])

    python:
        # Descriptions for: *Elements
        pytfall.desc = object()
        pytfall.desc.elements = {
        "fire": str("The wildest of all elements bringing a change that can never be undone. In a blink of an eye, it can turn any obstacle to dust leaving nothing but scorched earth in its path. In unskilled hands, it can be more dangerous to its wielders than to their enemies… Fire Element regardless to its power, is weak against Water but have the advantage versus Air."),
        "air": str("The most agile of the elements. Utilizing its transparency and omnipresence to maximum. Wielders of this element are also capable of performing lighting based spells. Being able to strike swiftly and undetected, in capable hands this element does not give opponents much time to defend themselves. The Air Element excels against Earth but struggles greatly when dealing with Fire."),
        "earth": str("The slowest and sturdiest among the elements. Known for sacrificing speed in exchange for overwhelming destructive power. Unlike other elements that leaves evidence of their devastating acts, Earth is capable of literally burying the truth. The Earth Element have the upper hand against Water, but have a hard time against the swift Air."),
        "water": str("The most mysterious among the elements. Hiding it twisted and destructive nature under the calm surface. Leaving behind only rumble and bodies as proof of it fatal capabilities. Dominating Fire with ease, the Water Element is relatively weak against Earth."),
        "darkness": str("One of the two elements born from men desires, thoughts and deeds. Fuelling itself from anger, impure thoughts and evil acts. Dwelling deep in everyone’s soul, patiently expanding, slowly consuming ones soul. Evenly matched and locked in the ethereal struggle Light and Darkness, these opposites can cause chaotic damage against each other."),
        "neutral": str("Neutral alignment is the most popular option among warriors that do not rely on use of magic. It will ensure good degree of resistance from anything some silly mage may throw at its wielder. On other hand, this is possibly the worst choice for any magic user."),
        "light": str("One of the two elements born from men desires, thoughts and deeds. Light nests itself inside everyone souls. Gaining its force from good acts and pure thoughts. Evenly matched and locked in the ethereal struggle Light and Darkness, these opposites can cause chaotic damage against each other.")
        }

    call load_building_upgrades
    return

label load_building_upgrades:
    return

label load_json_tags:
    python:
        # -----------------------------------------------
        # load image tags into the tag database
        tl.start("Loading: JSON Tags (OldStyle)")
        charsdir = os.path.join(gamedir, "content", "chars")
        rcharsdir = os.path.join(gamedir, "content", "rchars")
        jsonfiles = locate_files("tags.json", charsdir)
        rg_jsonfiles = locate_files("tags.json", rcharsdir)

        jsontagdb = TagDatabase.from_json([jsonfiles, rg_jsonfiles])
        tagslog.info("loaded %d images from tags.json files" % jsontagdb.count_images())

        del charsdir
        del rcharsdir
        del jsonfiles
        del rg_jsonfiles

        # raise Exception, tagdb.__dict__["tagmap"].keys()[1:10]
        for tag in jsontagdb.tagmap.keys():
            if tag.startswith("("):
                del jsontagdb.tagmap[tag]
            try:
                int(tag)
                del jsontagdb.tagmap[tag]
            except ValueError:
                pass
        tl.end("Loading: JSON Tags (OldStyle)")
    return

label convert_json_to_filenames:
    if not jsontagdb.tagmap:
        $ renpy.show_screen("message_screen", "No JSON tags were found!")
        return
    else:
        python:
            alltags = set(tags_dict.values())
            nums = "".join(list(str(i) for i in range(10)))
            pool = list("".join([string.ascii_lowercase, nums]))
            inverted = {v:k for k, v in tags_dict.iteritems()}
            # Carefully! We write a script to rename the image files...
            for img in jsontagdb.get_all_images():
                # Normalize the path:
                f = normalize_path("".join([gamedir, "/", img]))
                tags = list(alltags & jsontagdb.get_tags_per_path(img))
                if not tags:
                    devlog.warning("Deleting the file (No tags found): %s" % f)
                    os.remove(f)
                    continue
                tags.sort()
                tags = list(inverted[tag] for tag in tags)
                # New filename string:
                fn = "".join(["-".join(tags), "-", "".join(list(choice(pool) for i in range(4)))])
                if img.endswith(".png"):
                    fn = fn + ".png"
                elif img.endswith(".jpg"):
                    fn = fn + ".jpg"
                elif img.endswith(".jpeg"):
                    fn = fn + ".jpeg"
                elif img.endswith(".gif"):
                    fn = fn + ".gif"
                oldfilename = f.split(os.sep)[-1]
                if oldfilename == fn:
                    continue
                else:
                    newdir = f.replace(oldfilename, fn)
                    try:
                        os.rename(f, newdir)
                    except:
                        devlog.warning("Could not find: %s"%str(f))

            # Delete the tagfiles:
            charsdir = os.path.join(gamedir, "content", "chars")
            rcharsdir = os.path.join(gamedir, "content", "rchars")
            jsonfiles = locate_files("tags.json", charsdir)
            jsonfiles = list(chain(jsonfiles, locate_files("tags.json", rcharsdir)))
            for file in jsonfiles:
                os.remove(file)
            del charsdir
            del rcharsdir
            del jsonfiles
            renpy.show_screen("message_screen", "%d images converted!" % jsontagdb.count_images())
    return
