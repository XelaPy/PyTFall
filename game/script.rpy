init 100 python:
    tagdb = TagDatabase()
    for tag in tags_dict.values():
        tagdb.tagmap[tag] = set()

    tl.start("Loading: Mobs")
    mobs = load_mobs()
    tl.end("Loading: Mobs")

    def update_object(old, new, kind):
        for key, value in vars(old).iteritems():
            if hasattr(new, key):
                updated = getattr(new, key)
                if value != updated:
                    dlog("{} {}: {} Updated: {} -> {}".format(kind, str(old), key, str(value), str(updated)))
                setattr(old, key, updated)
            else:
                dlog("{} {}: Deleted: {}: {}".format(kind, str(old), key, str(value)))
                delattr(old, key)

        for key, updated in vars(new).iteritems():
            if not hasattr(old, key):
                dlog("{} {}: New Attr: {}: {}".format(kind, str(old), key, str(updated)))
                setattr(old, key, updated)

default defeated_mobs = {}
default gazette = Gazette()

label start:
    $ renpy.block_rollback()
    $ locked_random("random") # Just making sure that we have set the variable...

    if DEBUG:
        $ renpy.show_screen("debug_tools")
    $ renpy.show_screen("new_style_tooltip")
    $ gfx_overlay = GFXOverlay()
    $ renpy.show("pf_gfx_overlay", what=gfx_overlay, layer="pytfall")

    python: # Variable defaults:
        chars_list_last_page_viewed = 0
        char = None # Character global
        came_to_equip_from = None # Girl equipment screen came from label holder
        eqtarget = None # Equipment screen
        gallery = None

    python: # Day/Calendar/Names/Menu Extensions and some other defaults.
        # Global variables and loading content:
        day = 1
        calendar = Calendar(day=28, month=2, year=125)
        global_flags = Flags()

        ilists = ListHandler()
        # difficulty = Difficulties()

        # Locations (we need this here cause we'll write to it soon):
        locations = dict()

        # Load random names selections for rGirls:
        tl.start("Loading: Random Name Files")
        female_first_names = load_female_first_names(200)
        male_first_names = load_male_first_names(200)
        random_last_names = load_random_last_names(200)
        random_team_names = load_team_names(50)
        tl.end("Loading: Random Name Files")

        tl.start("Loading: PyTFallWorld")
        pytfall = PyTFallWorld()
        tl.end("Loading: PyTFallWorld")

    python:
        tl.start("Loading: Menu Extensions")
        menu_extensions = MenuExtension()
        menu_extensions["Abby The Witch Main"] = []
        menu_extensions["Xeona Main"] = []
        tl.end("Loading: Menu Extensions")

    python hide: # Base locations:
        # Create locations:
        loc = HabitableLocation(id="Streets", daily_modifier=-.1, rooms=float("inf"), desc="Cold and unneighborly city alleys")
        locations[loc.id] = loc

        loc = HabitableLocation(id="City Apartments", daily_modifier=.2, rooms=float("inf"), desc="Girls apartments somewhere in the city")
        locations[loc.id] = loc

        loc = Location(id="City")
        locations[loc.id] = loc

        loc = HabitableLocation(id="After Life", daily_modifier=.0, rooms=float("inf"), desc="No one knows where is this place and what's going on there")
        locations[loc.id] = loc

    python: # Traits:
        # Load all game elements:
        tl.start("Loading/Sorting: Traits")
        traits = load_traits()
        global_flags.set_flag("last_modified_traits", os.path.getmtime(content_path('db/traits')))

    call sort_traits_for_gameplay from _call_sort_traits_for_gameplay

    $ tl.end("Loading/Sorting: Traits")

    python: # Items/Shops:
        tl.start("Loading/Sorting: Items")
        items = load_items()
        items.update(load_gifts())
        global_flags.set_flag("last_modified_items", os.path.getmtime(content_path('db/items')))
        items_upgrades = json.load(renpy.file("content/db/upgrades.json"))

        # Build shops:
        pytfall.init_shops()

    call sort_items_for_gameplay from _call_sort_items_for_gameplay

    $ tl.end("Loading/Sorting: Items")

    call city_map_predict
    call items_ptedict

    python: # Dungeons (Building (Old))
        tl.start("Loading: Dungeons")
        dungeons = load_dungeons()
        tl.end("Loading: Dungeons")

        # Battle Skills:
        tl.start("Loading: Battle Skills")
        battle_skills = load_battle_skills()
        tiered_magic_skills = dict()
        for s in battle_skills.values():
            tiered_magic_skills.setdefault(s.tier, []).append(s)
        tl.end("Loading: Battle Skills")

    $ hero = Player()

    python: # Jobs:
        tl.start("Loading: Jobs")
        # This jobs are usually normal, most common type that we have in PyTFall
        temp = [WhoreJob(), StripJob(), BarJob(), Manager(), CleaningJob(), GuardJob(), Rest(), AutoRest()]
        simple_jobs = {j.id: j for j in temp}
        del temp
        tl.end("Loading: Jobs")

    python: # Ads and Buildings:
        tl.start("Loading: Businesses")
        adverts = json.load(renpy.file("content/db/buildings/adverts.json"))
        businesses = load_businesses()
        tl.end("Loading: Businesses")

    $ tl.start("Loading: Schools")
    $ schools = {}
    python hide: # Training/Schools/Weird Proxies by Thewlis:
        school = School()
        school.add_courses()
        schools[school.name] = school
        # schools = load_schools()
        # pytFlagProxyStore = shallowcopy(pytFlagProxyStore)
    $ tl.end("Loading: Schools")

    # python: # Picked Tags and maps (afk atm):
    #     maps = xml_to_dict(content_path('db/map.xml'))
    #
    #     import cPickle as pickle
    #     tl.start("Loading: Binary Tag Database")
    #     # pickle.dump(tagdb.tagmap, open(config.gamedir + "/save.p", "wb"))
    #     tagdb = TagDatabase()
    #     tagdb.tagmap = pickle.load(open(config.gamedir + "/save.p", "rb"))
    #     tagslog.info("loaded %d images from binary files" % tagdb.count_images())
    #     tl.end("Loading: Binary Tag Database")

    python: # Tags/Loading Chars/Mobs/Quests.first_day
        # Loading characters:
        # tagdb = TagDatabase()
        # for tag in tags_dict.values():
        #     tagdb.tagmap[tag] = set()

        tl.start("Loading: All Characters!")
        chars = load_characters("chars", Char)
        #global_flags.set_flag("last_modified_chars", os.path.getmtime(content_path('chars')))
        npcs = load_characters("npc", NPC)
        #global_flags.set_flag("last_modified_npcs", os.path.getmtime(content_path('npc')))
        rchars = load_random_characters()
        #global_flags.set_flag("last_modified_rchars", os.path.getmtime(content_path('rchars')))
        tl.end("Loading: All Characters!")
        if DEBUG_LOG:
            devlog.info("Loaded %d images from filenames!" % tagdb.count_images())

        # Start auto-quests
        pytfall.world_quests.first_day()

        # tl.start("Loading: Mobs")
        # mobs = load_mobs()
        # tl.end("Loading: Mobs")

    python: # SE (Areas)
        tl.start("Loading: Exploration Areas")
        # pytfall.forest_1 = Exploration()
        fg_areas = load_se_areas()
        tl.end("Loading: Exploration Areas")

    python: # Move to a World AI method:
        tl.start("Loading: Populating World with RChars")
        pytfall.populate_world()
        tl.end("Loading: Populating World with RChars")

    python: # Girlsmeets:
        tl.start("Loading: GirlsMeets")
        gm = GirlsMeets()
        tl.end("Loading: GirlsMeets")

    # Loading apartments/guilds:
    call load_resources from _call_load_resources
    jump dev_testing_menu_and_load_mc

label dev_testing_menu_and_load_mc:
    if DEBUG:
        menu:
            "Debug Mode":
                $ hero.traits.basetraits.add(traits["Mage"])
                $ hero.apply_trait(traits["Mage"])
                menu:
                    "Level 1":
                        $ n = 0
                    "Overpowered":
                        $ n = 10
                $ tier_up_to(hero, n, level_bios=(.9, 1.1), skill_bios=(.8, 1.2), stat_bios=(.8, 1.0))
                $ del n
            "Content":
                menu:
                    "Test Intro":
                        call intro from _call_intro
                        call mc_setup from _call_mc_setup
                    "MC Setup":
                        call mc_setup from _call_mc_setup_1
                    "Skip MC Setup":
                        $ pass
                    "Back":
                        jump dev_testing_menu_and_load_mc
            "GFX":
                while 1:
                    menu gfx_testing_menu:
                        "Particle":
                            scene black
                            show expression ParticleBurst([Solid("#%06x"%renpy.random.randint(0, 0xFFFFFF), xysize=(5, 5)) for i in xrange(50)], mouse_sparkle_mode=True) as pb
                            pause
                            hide pb
                        "Back":
                            jump dev_testing_menu_and_load_mc
    else:
        call intro from _call_intro_1
        call mc_setup from _call_mc_setup_2

    python: # We run this in case we skipped MC setup in devmode!
        if not getattr(hero, "_path_to_imgfolder", None):
            renpy.music.stop()
            if not DEBUG:
                # We're fucked if this is the case somehow :(
                raise Exception("Something went horribly wrong with MC setup!")

            male_fighters, female_fighters, json_fighters = load_special_arena_fighters()
            af = choice(male_fighters.values())
            del male_fighters[af.id]

            hero._path_to_imgfolder = af._path_to_imgfolder
            hero.id = af.id
            hero.say = Character(hero.nickname, color=ivory, show_two_window=True, show_side_image=hero.show("portrait", resize=(120, 120)))
            hero.restore_ap()
            hero.log_stats()

            if DEBUG and not hero.home:
                ap = None
                for b in buildings.values():
                    if ap is None or b.price > ap.price:
                        ap = b
                if ap:
                    hero.buildings.append(ap)
                    hero.home = ap
                del ap

    # Set Human trait for the MC: (We may want to customize this in the future)
    python:
        if not isinstance(hero.race, Trait):
            hero.apply_trait(traits["Human"])
            hero.full_race = "Human"

    jump continue_with_start

label continue_with_start:
    python: # Load Arena
        tl.start("Loading: Arena!")
        pytfall.arena = Arena()
        locations[pytfall.arena.id] = pytfall.arena
        pytfall.arena.setup_arena()
        pytfall.arena.update_matches()
        pytfall.arena.update_teams()
        pytfall.arena.find_opfor()
        pytfall.arena.update_dogfights()
        tl.end("Loading: Arena!")

    # Call girls starting labels:
    $ all_chars = chars.values()
    while all_chars:
        $ temp = all_chars.pop()
        $ chars_unique_label = "_".join(["start", temp.id])
        if renpy.has_label(chars_unique_label):
            call expression chars_unique_label from _call_expression_1

    # Clean up globals after loading chars:
    python:
        for i in ("chars_unique_label", "char", "girl", "testBrothel", "all_chars", "temp", "utka"):
            del(i)

    #  --------------------------------------
    # Put here to facilitate testing:
    if DEBUG and renpy.has_label("testing"):
        call testing from _call_testing

    python in _console:
        if store.DEBUG:
            stdio_lines = []
            stderr_lines = []
            console.history = []

    if hero.name.lower() == "darktl": # LoL! :D
        $ hero.gold += 888888888

    # last minute checks:
    if not hero.home:
        $ hero.home = locations["Streets"]

    python: # Populate Slave Market:
        tl.start("Loading: Populating SlaveMarket")
        pytfall.sm.populate_chars_list()
        tl.end("Loading: Populating SlaveMarket")

    $ hero.clear_img_cache()

    jump mainscreen

label sort_items_for_gameplay:
    python:
        # Items sorting for AutoBuy:
        shop_items = [item for item in items.values() if (set(pytfall.shops) & set(item.locations))]
        all_auto_buy_items = [item for item in shop_items if item.usable and not item.jump_to_label]

        trait_selections = {"goodtraits": {}, "badtraits": {}}
        auto_buy_items = {k: [] for k in ("body", "restore", "food", "dress", "rest", "warrior", "scroll")}

        for item in all_auto_buy_items:
            for k in ("goodtraits", "badtraits"):
                if hasattr(item, k):
                    for t in getattr(item, k):
                        # same item may occur multiple times for different traits.
                        trait_selections[k].setdefault(t, []).append(item)

            if item.type != "permanent":
                if item.type == "armor" or item.slot == "weapon":
                    auto_buy_items["warrior"].append(item)
                else:
                    if item.slot == "body":
                        auto_buy_items["body"].append(item)
                    if item.type in ("restore", "food", "scroll", "dress"):
                        auto_buy_items[item.type].append(item)
                    else:
                        auto_buy_items["rest"].append(item)

        for k in trait_selections:
            for v in trait_selections[k].values():
                v = sorted(v, key=lambda i: i.price)

        for k in ("body", "restore", "food", "dress", "rest", "warrior", "scroll"):
            auto_buy_items[k] = [(i.price, i) for i in auto_buy_items[k]]
            auto_buy_items[k].sort()

        # Items sorting per Tier:
        tiered_items = {}
        for i in items.values():
            tiered_items.setdefault(i.tier, []).append(i)

    # Max Arena price:
    $ MAX_ARENA_ITEM_PRICE = max([i.price for i in items.values() if "Arena" in i.locations])
    return

label sort_traits_for_gameplay:
    python:
        # This should be reorganized later:
        tgs = object() # TraitGoups!
        tgs.breasts = [i for i in traits.values() if i.breasts]
        tgs.body = [i for i in traits.values() if i.body]
        tgs.base = [i for i in traits.values() if i.basetrait and not i.mob_only]
        tgs.elemental = [i for i in traits.values() if i.elemental]
        tgs.el_names = set([i.id.lower() for i in tgs.elemental])
        tgs.ct = [i for i in traits.values() if i.character_trait]
        tgs.sexual = [i for i in traits.values() if i.sexual] # This is a subset of character traits!
        tgs.race = [i for i in traits.values() if i.race]
        tgs.client = [i for i in traits.values() if i.client]

        # Base classes such as: {"SIW": [Prostitute, Stripper]}
        gen_occ_basetraits = defaultdict(set)
        for t in tgs.base:
            for occ in t.occupations:
                gen_occ_basetraits[occ].add(t)
        gen_occ_basetraits = dict(gen_occ_basetraits)
    return

label after_load:
    # Resets:
    python:
        config.mouse = None

        if hasattr(store, "stored_random_seed"):
            renpy.random.setstate(stored_random_seed)

        if hasattr(store, "dummy"):
            del(dummy)

    # Clear cache, may reduce PScale errors, maybe...
    python hide:
        for c in store.chars.values():
            c.clear_img_cache()

    # Updating Databases:
    # Items:
    python hide:
        last_modified_items = global_flags.get_flag("last_modified_items", 0)
        last_modified = os.path.getmtime(content_path('db/items'))
        if last_modified_items < last_modified:
            tl.start("Updating items")
            updated_items = load_items()
            updated_items.update(load_gifts())

            for id, item in updated_items.iteritems():
                curr_item = store.items.get(id, None)
                if curr_item is None:
                    # Add new item
                    store.items[id] = item
                    dlog("New Item: {}".format(id))
                else:
                    # Update the existing item
                    update_object(curr_item, item, "Item")

            del updated_items
            tl.end("Updating items")
            global_flags.set_flag("last_modified_items", last_modified)
            renpy.call("sort_items_for_gameplay")

    # Traits:
    python hide:
        last_modified_traits = global_flags.get_flag("last_modified_traits", 0)
        last_modified = os.path.getmtime(content_path('db/traits'))
        if last_modified_traits < last_modified:
            tl.start("Updating traits")
            updated_traits = load_traits()
            for id, trait in updated_traits.iteritems():
                curr_trait = store.traits.get(id, None)
                if curr_trait is None:
                    # Add new trait
                    store.traits[id] = trait
                    dlog("New Trait: {}".format(id))
                else:
                    # Update the existing trait
                    update_object(curr_trait, trait, "Trait")

            del updated_traits
            tl.end("Updating traits")
            global_flags.set_flag("last_modified_traits", last_modified)
            renpy.call("sort_traits_for_gameplay")

    # SE Areas:
    # Not safe :(
    # python hide:
    #     tl.start("Updating: Exploration Areas")
    #     updated = load_se_areas()
    #     for id, area in updated.iteritems():
    #         old = store.fg_areas.get(id, None)
    #         if old is None:
    #             store.fg_areas[id] = area
    #             dlog("New SE Area: {}".format(id))
    #         else:
    #             update_object(old, area, "SE Area")
    #     tl.end("Updating: Exploration Areas")

    # All kinds of chars:
    python hide:
        # uChars:
        updated_chars = load_characters("chars", Char)
        for id, char in updated_chars.items():
            curr_char = store.chars.get(id, None)
            if curr_char is None:
                # Add new char
                store.chars[id] = char

        # rChars:
        store.rchars = load_random_characters()

        # NPCs:
        updated_npcs = load_characters("npc", NPC)
        for id, npc in updated_npcs.items():
            curr_npc = store.npcs.get(id, None)
            if curr_npc is None:
                # Add new NPC
                store.npcs[id] = npc

        # Arena Chars (We need this for databases it would seem...):
        load_special_arena_fighters()

    # Maps/BE Skills data overloads?/tiered_items/Be controllers?
    python hide:
        pytfall.maps = OnScreenMap()

        # Update battle skills?
        for s in store.battle_skills.values():
            if "initial_pause" not in s.target_damage_effect.keys():
                s.target_damage_effect["initial_pause"] = s.main_effect["duration"] * .75
            gfx = s.attacker_effects["gfx"]
            if isinstance(gfx, basestring):
                if gfx == "orb":
                    s.attacker_effects["gfx"] = "cast_orb_1"
                    s.attacker_effects["zoom"] = 1.85
                    s.attacker_effects["duration"] = 0.84
                elif gfx == "wolf":
                    s.attacker_effects["gfx"] = "wolf_1_webm"
                    s.attacker_effects["zoom"] = .85
                    s.attacker_effects["duration"] = 1.27
                    s.attacker_effects["cast"] = { "align": (.0, .5) }
                elif gfx == "bear":
                    s.attacker_effects["gfx"] = "bear_1_webm"
                    s.attacker_effects["zoom"] = .85
                    s.attacker_effects["duration"] = 0.97
                    s.attacker_effects["cast"] = { "align": (.0, .5) }
                elif gfx in ["dark_1", "light_1", "water_1", "air_1", "fire_1", "earth_1", "electricity_1", "ice_1"]:
                    s.attacker_effects["gfx"] = "cast_" + gfx
                    s.attacker_effects["zoom"] = 1.5
                    s.attacker_effects["duration"] = 0.84
                    s.attacker_effects["cast"] = { "point": "bc", "yo": -75}
                elif gfx in ["dark_2", "light_2", "water_2", "air_2", "fire_2", "earth_2", "ice_2", "electricity_2"]:
                    s.attacker_effects["gfx"] = "cast_" + gfx
                    s.attacker_effects["zoom"] = .9
                    s.attacker_effects["duration"] = 1.4
                elif gfx == "default_1":
                    s.attacker_effects["gfx"] = "cast_" + gfx
                    s.attacker_effects["zoom"] = 1.6
                    s.attacker_effects["duration"] = 1.12
                    s.attacker_effects["cast"] = { "ontop": False, "point": "bc" }
                elif gfx == "circle_1":
                    s.attacker_effects["gfx"] = "cast_" + gfx
                    s.attacker_effects["zoom"] = 1.9
                    s.attacker_effects["duration"] = 1.05
                    s.attacker_effects["cast"] = { "ontop": False, "point": "bc", "yo": -10 }
                elif gfx == "circle_2":
                    s.attacker_effects["gfx"] = "cast_" + gfx
                    s.attacker_effects["zoom"] = 1.8
                    s.attacker_effects["duration"] = 1.1
                    s.attacker_effects["cast"] = { "point": "bc", "yo": -100 }
                elif gfx == "circle_3":
                    s.attacker_effects["gfx"] = "cast_" + gfx
                    s.attacker_effects["zoom"] = 1.8
                    s.attacker_effects["duration"] = 0.96
                    s.attacker_effects["cast"] = { "yo": -50 }
                elif gfx == "runes_1":
                    s.attacker_effects["gfx"] = "cast_" + gfx
                    s.attacker_effects["zoom"] = 1.1
                    s.attacker_effects["duration"] = 0.75
                    s.attacker_effects["cast"] = { "ontop": False, "point": "bc", "yo": -50}

        # Handle on tier 0 items?
        tierless_items = store.tiered_items.get(None)
        if tierless_items:
            for item in tierless_items:
                item.tier = 0
                store.tiered_items[0].append(item)
            del store.tiered_items[None]

    stop music
    return

label splashscreen:
    show expression Image("presplash.png")
    pause 1.5
    return
