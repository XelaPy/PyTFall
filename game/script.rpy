init python:
    # Generating some random girls for the arena
    def create_arena_girls():
        rchars = rchar
        rgirls = rchars.keys()
        for __ in xrange(85):
            if not rgirls: rgirls = rchars.keys()
            if rgirls:
                rgirl = rgirls.pop()
                arena_girl = build_rc(id=rgirl, pattern="Warrior")
                arena_girl.arena_willing = True
                arena_girl.arena_active = False # Should prolly be moved to preparation?
                arena_girl.status = "free"


label start:
    $ renpy.block_rollback()
    
    python:
        # Global variables and loading content:
        day = 1
        difficulty = Difficulties()
        
        # Load random names selections for rGirls:
        tl.timer("Loading: Random Name Files")
        random_names = load_random_names(200)
        random_last_names = load_random_last_names(200)
        
        # Load random names selections for Teams:
        file = open(renpy.loader.transfn(content_path("db/RandomTeamNames_1.txt")))
        randomTeamNames = file.readlines()
        shuffle(randomTeamNames)
        file.close()
        tl.timer("Loading: Random Name Files")
            
        # Load all game elements:
        tl.timer("Loading: Traits")
        traits = load_traits()
        tl.timer("Loading: Traits")
        
        tl.timer("Loading: Items")
        items = load_items()
        items.update(load_gifts())
        tl.timer("Loading: Items")
        
        # MC:
        hero = Player()
        
        ilists = ListHandler()
        
        tl.timer("Loading: Brothels")
        brothels = load_brothels()
        pytWhoringActs = build_whoring_acts()
        tl.timer("Loading: Brothels")
        
        tl.timer("Loading: Training")
        schools = load_schools()
        pytFlagProxyStore = shallowcopy(pytFlagProxyStore)
        pytRelayProxyStore = shallowcopy(pytRelayProxyStore)
        tl.timer("Loading: Training")
        
        # maps = xml_to_dict(content_path('db/map.xml'))
        calendar = Calendar(day=28, month=2, year=125)
        global_flags = Flags()
        
        # import cPickle as pickle
        # tl.timer("Loading: Binary Tag Database")
        # # pickle.dump(tagdb.tagmap, open(config.gamedir + "/save.p", "wb"))
        # tagdb = TagDatabase()
        # tagdb.tagmap = pickle.load(open(config.gamedir + "/save.p", "rb"))
        # tagslog.info("loaded %d images from binary files" % tagdb.count_images())
        # tl.timer()
        
    python:
        # Loading characters:
        tagdb = TagDatabase()
        for tag in tags_dict.values():
            tagdb.tagmap[tag] = set()
        tl.timer("Loading: All Characters!")
        char = load_characters()
        # Trying to load crazy characters:
        crazy_chars = load_crazy_characters()
        char.update(crazy_chars)
        rchar = load_random_characters()
        del crazy_chars
        tl.timer("Loading: All Characters!")
        devlog.info("Loaded %d images from filenames!" % tagdb.count_images())
        
        tl.timer("Loading: PyTFallWorld")
        pytfall = PyTFallWorld()
        tl.timer("Loading: PyTFallWorld")
        
        # Start auto-quests
        pytfall.world_quests.first_day()
        
        tl.timer("Loading: Mobs")
        mobs = load_mobs()
        tl.timer("Loading: Mobs")
        
        tl.timer("Loading: Exploration")
        pytfall.forest_1 = Exploration()
        fg_areas = load_fg_areas()
        tl.timer("Loading: Exploration")
        
        # ---------------------------------------
        # Temporary code
        tl.timer("Loading: Generating Random girls")
        
        # Some random girls (if there are any):
        if rchar:
            rgirls = rchar.keys()
            shuffle(rgirls)
            for __ in xrange(25):
                if rgirls:
                    rgirl = rgirls.pop()
                    new_random_girl = build_rc(id=rgirl)
                else:
                    rgirls = rchar.keys()
                    shuffle(rgirls)

            del rgirls
            del rgirl
            del new_random_girl
                
            create_arena_girls()
        tl.timer("Loading: Generating Random girls")

        tl.timer("Loading: GirlsMeets")
        gm = GirlsMeets()
        tl.timer("Loading: GirlsMeets")
        
        tl.timer("Loading: Populating SlaveMarket")
        pytfall.sm.populate_girls_list()
        tl.timer("Loading: Populating SlaveMarket")
        
    # Loading apartments/guilds:
    call load_resources
    
    if config.developer:
        menu:
            "Test Intro":
                call intro
            "Skip":
                pass
            
    if config.developer:
        menu:
            "MC Setup Screen":
                call mc_setup
                $ neow = True
            "Skip MC Setup (Zero MC)":
                $ pass
            "MC Level 100":
                $ initial_levelup(hero, 100, max_out_stats=True)
        python:
            if not hasattr(store, "neow"):
                renpy.music.stop()
                mc_pics = load_mc_images()
                picbase = choice(mc_pics.keys())
                hero.img_db = mc_pics[picbase]
                del mc_pics[picbase]
                af_pics = mc_pics
                del mc_pics
                hero.say = Character(hero.nickname, color=ivory, show_two_window=True, show_side_image=hero.show("portrait", resize=(140, 140)), window_left_padding=230)
                hero.restore_ap()
                hero.log_stats()
    else:
        call mc_setup
    
    python:
        tl.timer("Loading: Arena!")
        pytfall.arena = Arena()
        
        for key in af_pics:
            f = ArenaFighter()
            f.name = key
            f.img_db = af_pics[key]
            f.init()
            pytfall.arena.ac[f.name] = f
        
        del af_pics
        
        pytfall.arena.ac.update(load_arena_fighters())
        pytfall.arena.setup_arena()
        pytfall.arena.update_matches()
        pytfall.arena.update_teams()
        pytfall.arena.find_opfor()
        pytfall.arena.update_dogfights()
        tl.timer("Loading: Arena!")
        
    # Call girls starting labels:
    $ all_chars = char.values()
    while all_chars:
        $ popped_girl = all_chars.pop()
        $ girl_unique_label = "_".join(["start", popped_girl.id])
        if renpy.has_label(girl_unique_label):
            call expression girl_unique_label
    $ del all_chars
    if girl_unique_label in globals():
        $ del girl_unique_label
        
    if "chr" in store.__dict__:
        $ del store.__dict__["chr"]
    if "girl" in store.__dict__:
        $ del store.__dict__["girl"]
    if "testBrothel" in store.__dict__:
        $ del store.__dict__["testBrothel"]
    
    $ shop_items = list(item for item in items.values() if (set(pytfall.shops) & set(item.locations)))
    
    #  --------------------------------------
    # Put here to facilitate testing:
    if config.developer and renpy.has_label("testing"):
        call testing
    
    jump mainscreen
    

# This is very convinient, but could prove slow...
# Disabled until 0.9...
label after_load:
    stop music
    return
    # python:
        # new_chars = load_characters(content_dir)
 
        # for stat in StatList:
            # for girl in new_chars:
                # if stat not in new_chars[girl].stats.keys():
                    # new_chars[girl].__dict__['stats'][stat] = 0
                    
        # for girl in new_chars:
            # if new_chars[girl].status == 'slave':
                # new_chars[girl].houseper = 100
            # else:
                # new_chars[girl].houseper = 50
 
        # for key in new_chars.keys():
            # if key in char:
                # pass
            # else:
                # char[key] = new_chars[key]
        # del new_chars
        # jump('pyt_mainscreen')
