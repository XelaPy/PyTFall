label start:
    $ renpy.block_rollback()
    $ locked_random("random") # Just making sure that we have set the variable...

    if config.debug:
        $ renpy.show_screen("debug_tools", _layer="screens")

    python: # Variable defaults:
        chars_list_last_page_viewed = 0
        char = None # Character global
        came_to_equip_from = None # Girl equipment screen came from label holder
        eqtarget = None # Equipment screen
        char_profile = None # Girl profile screen came from label holder
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
        tl.timer("Loading: Random Name Files")
        female_first_names = load_female_first_names(200)
        male_first_names = load_male_first_names(200)
        random_last_names = load_random_last_names(200)
        random_team_names = load_team_names(50)

        # Load random names selections for Teams:
        file = open(content_path("db/RandomTeamNames_1.txt"))
        randomTeamNames = file.readlines()
        shuffle(randomTeamNames)
        file.close()

        tl.timer("Loading: PyTFallWorld", nested=False)
        pytfall = PyTFallWorld()

        tl.timer("Loading: Menu Extensions", nested=False)
        menu_extensions = MenuExtension()
        menu_extensions["Abby The Witch Main"] = []
        menu_extensions["Xeona Main"] = []
        tl.timer("Loading: Menu Extensions")

    python hide: # Base locations:
        # Create locations:
        for loc in (Apartments, Streets, CityLoc):
            loc = loc()
            locations[loc.id] = loc
        loc = HabitableLocation(id="After Life", daily_modifier=.0, rooms=float("inf"))
        locations[loc.id] = loc

    python: # Traits:
        # Load all game elements:
        tl.timer("Loading: Traits")
        traits = load_traits()

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

    python: # Items/Shops:
        tl.timer("Loading: Items", nested=False)
        items = load_items()
        items.update(load_gifts())

        # Build shops:
        pytfall.init_shops()

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

    python: # Dungeons (Building (Old))
        tl.timer("Loading: Dungeons", nested=False)
        dungeons = load_dungeons()

    # Battle Skills:
    $ tl.timer("Loading: Battle Skills", nested=False)
    $ battle_skills = dict()
    call load_battle_skills
    $ tiered_magic_skills = {}
    python:
        for s in battle_skills.values():
            tiered_magic_skills.setdefault(s.tier, []).append(s)

    # $ tl.timer("Loading: Battle Skills")

    $ hero = Player()

    python: # Jobs:
        tl.timer("Loading: SimpleJobs")
        # This jobs are usually normal, most common type that we have in PyTFall
        temp = [WhoreJob(), StripJob(), BarJob(), Manager(), CleaningJob(), GuardJob()]
        simple_jobs = {j.id: j for j in temp}
        del temp

    python: # Ads and Buildings:
        tl.timer("Loading: Businesses", nested=False)
        adverts = json.load(renpy.file("content/db/buildings/adverts.json"))
        businesses = load_buildings()

    python: # Training/Schools/Weird Proxies by Thewlis:
        tl.timer("Loading: Training", nested=False)
        schools = load_schools()
        pytFlagProxyStore = shallowcopy(pytFlagProxyStore)
        pytRelayProxyStore = shallowcopy(pytRelayProxyStore)
        tl.timer("Loading: Training")

    python: # Picked Tags and maps (afk atm):
        pass
        # maps = xml_to_dict(content_path('db/map.xml'))

        # import cPickle as pickle
        # tl.timer("Loading: Binary Tag Database")
        # # pickle.dump(tagdb.tagmap, open(config.gamedir + "/save.p", "wb"))
        # tagdb = TagDatabase()
        # tagdb.tagmap = pickle.load(open(config.gamedir + "/save.p", "rb"))
        # tagslog.info("loaded %d images from binary files" % tagdb.count_images())
        # tl.timer()

    python: # Tags/Loading Chars/Mobs/Quests.first_day
        # Loading characters:
        tagdb = TagDatabase()
        for tag in tags_dict.values():
            tagdb.tagmap[tag] = set()
        tl.timer("Loading: All Characters!")
        chars = load_characters("chars", Char)
        npcs = load_characters("npc", NPC)
        # Trying to load crazy characters:
        crazy_chars = load_crazy_characters()
        chars.update(crazy_chars)
        rchars = load_random_characters()
        del crazy_chars
        tl.timer("Loading: All Characters!")
        devlog.info("Loaded %d images from filenames!" % tagdb.count_images())

        # Start auto-quests
        pytfall.world_quests.first_day()

        tl.timer("Loading: Mobs")
        mobs = load_mobs()

    python: # SE (Areas)
        tl.timer("Loading: Exploration", nested=False)
        # pytfall.forest_1 = Exploration()
        fg_areas = load_fg_areas()

    python: # Move to a World AI method:
        tl.timer("Loading: Generating Random girls", nested=False)

        # Some random girls (if there are any):
        if rchars:
            rgirls = rchars.keys()
            shuffle(rgirls)
            for i in xrange(25):
                if rgirls:
                    rgirl = rgirls.pop()
                    new_random_girl = build_rc(id=rgirl, tier=random.uniform(.3, 1.5))
                else:
                    rgirls = rchars.keys()
                    shuffle(rgirls)

            del rgirls
            del rgirl
            del new_random_girl

    python: # Girlsmeets/Items Upgrades:
        tl.timer("Loading: GirlsMeets", nested=False)
        gm = GirlsMeets()

        items_upgrades = json.load(renpy.file("content/db/upgrades.json"))

    # Loading apartments/guilds:
    call load_resources
    jump dev_testing_menu_and_load_mc

label dev_testing_menu_and_load_mc:
    if config.developer:
        menu:
            "Debug Mode":
                $ hero.traits.basetraits.add(traits["Mage"])
                $ hero.apply_trait(traits["Mage"])
                $ tier_up_to(hero, 2.5, level_bios=(.9, 1.1), skill_bios=(.8, 1.2), stat_bios=(.8, 1.0))
            "Content":
                menu:
                    "Test Intro":
                        call intro
                        call mc_setup
                    "MC Setup":
                        call mc_setup
                        $ neow = True
                    "Skip MC Setup":
                        $ pass
                    "Back":
                        jump dev_testing_menu
            "GFX":
                while 1:
                    menu gfx_testing_menu:
                        "Webm":
                            call test_webm
                        "Chain UDD":
                            call testing_chain_udd
                        "Water Effect":
                            call gfx_water_effect_test
                            jump gfx_testing_menu
                        "Test Matrix":
                            call test_matrix
                        "Test Vortex":
                            call test_vortex
                        # "Quality Test":
                            # call screen testing_image_quality
                        "FilmStrip":
                            call screen testing_new_filmstrip
                        "Particle":
                            scene black
                            show expression ParticleBurst([Solid("#%06x"%renpy.random.randint(0, 0xFFFFFF), xysize=(5, 5)) for i in xrange(50)], mouse_sparkle_mode=True) as pb
                            pause
                            hide pb
                        "Test Robert Penners Easing":
                            call screen test_penners_easing
                        "Back":
                            jump dev_testing_menu
    else:
        call mc_setup

    python: # We run this in case we skipped MC setup in devmode!
        if not getattr(hero, "_path_to_imgfolder", None):
            if not config.developer:
                # We're fucked if this is the case somehow :(
                raise Exception("Something went horribly wrong with MC setup!")
            renpy.music.stop()

            male_fighters, female_fighters, json_fighters = load_special_arena_fighters()
            af = choice(male_fighters.values())
            del male_fighters[af.id]

            hero._path_to_imgfolder = af._path_to_imgfolder
            hero.id = af.id
            hero.say = Character(hero.nickname, color=ivory, show_two_window=True, show_side_image=hero.show("portrait", resize=(120, 120)))
            hero.restore_ap()
            hero.log_stats()

    jump continue_with_start

label continue_with_start:
    python: # Load Arena
        tl.timer("Loading: Arena!")
        pytfall.arena = Arena()
        locations[pytfall.arena.id] = pytfall.arena
        pytfall.arena.setup_arena()
        pytfall.arena.update_matches()
        pytfall.arena.update_teams()
        pytfall.arena.find_opfor()
        pytfall.arena.update_dogfights()
        tl.timer("Loading: Arena!")

    # Call girls starting labels:
    $ all_chars = chars.values()
    while all_chars:
        $ temp = all_chars.pop()
        $ chars_unique_label = "_".join(["start", temp.id])
        if renpy.has_label(chars_unique_label):
            call expression chars_unique_label

    # Clean up globals after loading chars:
    python:
        for i in ("chars_unique_label", "char", "girl", "testBrothel", "all_chars", "temp"):
            del(i)

    #  --------------------------------------
    # Put here to facilitate testing:
    if config.developer and renpy.has_label("testing"):
        call testing

    python in _console:
        if config.debug:
            stdio_lines = []
            stderr_lines = []
            console.history = []

    if hero.name.lower() == "darktl": # LoL! :D
        $ hero.gold += 888888888

    # last minute checks:
    if not hero.home:
        $ hero.home = locations["Streets"]

    python: # Populate Slave Market:
        tl.timer("Loading: Populating SlaveMarket", nested=False)
        pytfall.sm.populate_chars_list()
        # tl.timer("Loading: Populating SlaveMarket")

    jump mainscreen

label after_load:
    if hasattr(store, "stored_random_seed"):
        $ renpy.random.setstate(stored_random_seed)
    stop music
    return
