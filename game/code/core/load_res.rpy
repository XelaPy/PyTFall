label load_resources:
    python:
        # Scripted Buildings:
        buildings = dict()
        ap = Apartment()
        ap.id = "Studio Apartment"
        ap.name = ap.id
        ap.desc = "Buy this Apartment to live in for an Extra AP point per day!"
        ap.img = "content/gfx/bg/buildings/apartment_1.jpg"
        ap.rooms = 1
        ap.maxrooms = 1
        ap.price = 10000
        buildings[ap.id] = ap

        # fg = FighterGuild()
        # fg.img = "content/gfx/bg/buildings/Chorrol_Fighters_Guild.png"
        # fg.desc = "Send out parties to explore and loot the unstable areas around PyTFall!"
        # fg.price = 10000
        # fg.id = "Fighters Guild"
        # fg.name = fg.id
        # fg.right_sheet = "guild_contol"
        # fg.focus_area = fg_areas["Northern Forest"]
        # fg.focus_gen_area = fg.focus_area.area
        # fg.teams = list()
        # team = Team(name = "Meow x 0", max_size=3)
        # fg.multi = 2
        # fg.fame = 0
        # fg.rep = 0
        # fg.sq_meters = 1000
        # fg.maxfame = 500
        # fg.maxrep = 500
        # fg.teams.append(team)
        # fg.teams_allowed = 4
        # fg.max_teams = 4
        # fg.rooms = 5
        # fg.maxrooms = fg.max_teams * 3
        # buildings[fg.id] = fg

        jail = CityJail()
        jail.id = "City Jail"

        # Add the dungeon to the buildings list
        # Load the hero's dungeon
        # school = TrainingDungeon(load_training("training", PytTraining))
        # schools[school.name] = school
        # buildings[TrainingDungeon.NAME] = schools[TrainingDungeon.NAME]
        # if config.developer:
        #     hero.add_building(buildings[TrainingDungeon.NAME])

        # Variables:
        char = None # Character global
        came_to_equip_from = None # Girl equipment screen came from label holder
        eqtarget = None # Equipment screen
        char_profile = None # Girl profile screen came from label holder
        gallery = None

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
        tl.timer("Loading: JSON Tags (OldStyle)")
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
        tl.timer("Loading: JSON Tags (OldStyle)")
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
