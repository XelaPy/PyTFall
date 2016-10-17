label hiddenvillage_entrance:
    if not "village" in ilists.world_music:
        $ ilists.world_music["village"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("village")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["village"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("hiddenvillage_entrance"):
            pytfall.world_actions.add("hiddenvillage_matrix", "Explore", Jump("hidden_village_matrix"))
            pytfall.world_actions.finish()

    scene bg hiddenvillage_entrance
    with dissolve
    show screen hiddenvillage_entrance
    
    if not global_flags.flag('visited_hidden_village'):
        $ global_flags.set_flag('visited_hidden_village')
        # place for introduction
        
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
        
    while True:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ gm.start_gm(result[1])
            
        if result[0] == 'control':
            hide screen hiddenvillage_entrance
            if result[1] == 'return':
                $ renpy.music.stop(channel="world")
                hide screen hiddenvillage_entrance
                jump city
                
                
screen hiddenvillage_entrance:

    use top_stripe(True)
    $ img_study = ProportionalScale("content/gfx/interface/icons/studing.png", 70, 70)
    imagebutton: # to do: add conditions for the button!
        pos(120, 200)
        idle (img_study)
        hover (im.MatrixColor(img_study, im.matrix.brightness(0.15)))
        action [Hide("hiddenvillage_entrance"), Jump("hidden_village_study"), With(dissolve)]
    use location_actions("hiddenvillage_entrance")
    if global_flags.flag('hidden_village_shop_first_enter'): # the shop is hidden until found via matrix
        $img = ProportionalScale("content/gfx/interface/icons/ninja_shop.png", 100, 70)
        imagebutton:
            pos(300, 315)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
            action [Hide("hiddenvillage_entrance"), Jump("hidden_village_shop")]
    
label hidden_village_matrix: 
    hide screen hiddenvillage_entrance
    scene bg hiddenvillage_entrance
    $ hidden_list = []
    if global_flags.flag('hidden_village_shop_first_enter'):
        $ hidden_list.append("hidden_village_shop")
    # if chars["Tsunade"].disposition < 50:
        # $ hidden_list.append("Tsunade_Event")
    # if chars["Hinata"].disposition < 50:
        # $ hidden_list.append("Hinata_Event")
    # if chars["Kushina_Uzumaki"].disposition < 50 and chars["Naruko_Uzumaki"].disposition < 50:
        # $ hidden_list.append("Naruko_Event")
    # if chars["Ino_Yamanaka"].disposition < 50:
        # $ hidden_list.append("Ino_Event")
    # if chars["Karin"].disposition < 50:
        # $ hidden_list.append("Karin_Event")
    # if chars["Konan"].disposition < 50:
        # $ hidden_list.append("Konan_Event")
    call screen poly_matrix("library/events/StoryI/coordinates_hidden_village.json", show_exit_button=(0.8, 0.8), hidden=hidden_list)
    if not(_return):
        jump hiddenvillage_entrance
    if _return == "Alley": # to do: clear up the quest
        if pytfall.world_quests.check_quest_not_finished("Two Sisters"):
            if pytfall.world_quests.check_stage("Two Sisters") == 0:
                $ pytfall.world_events.force_event("two_sisters0")
                $ pytfall.world_quests.run_quests("doa_quest")
                $ pytfall.world_events.run_events("doa_quest")
            elif pytfall.world_quests.check_stage("Two Sisters") == 3:
                $ pytfall.world_events.force_event("two_sisters2")
                $ pytfall.world_events.force_event("two_sisters3")
                $ pytfall.world_quests.run_quests("doa_quest")
                $ pytfall.world_events.run_events("doa_quest")
            else:
                "Nothing interesting there."
        else:
            "Nothing interesting there."
    else:
        $ renpy.jump (_return)
    # "Result: [_return]"
    jump hidden_village_matrix
    
label hidden_village_shop:

    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5
        
    hide bg hiddenvillage_entrance
    
    scene bg workshop
    with dissolve
    show npc ninja_assistant
    with dissolve
    $ hidden_village_shop = ItemShop("Ninja Tools Shop", 18, ["Ninja Shop"], gold=1000, sells=["armor", "dagger", "fists", "rod", "claws", "sword", "bow", "amulet", "smallweapon", "restore", "dress"], sell_margin=0.85, buy_margin=3.0)
    $ r = Character("Ren", color=red, what_color=orange, show_two_window=True)
    
    if global_flags.flag('hidden_village_shop_first_enter'):
        r "Hey, [hero.name]. Need something?"
    else:
        $ r = Character("???", color=red, what_color=orange, show_two_window=True)
        $ global_flags.set_flag('hidden_village_shop_first_enter')
        r "Hm? Ah, heard about you."
        extend " Welcome to my Tools Shop."
        r "I'm Ren. We sell ninja stuff here."
        r "If we are interested, I can sell you some leftovers. Of course it won't be cheap for an outsider like you."
        r "But you won't find these things anywhere else, so it is worth it."
        r "Wanna take a look?"
    python:
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.hidden_village_shop
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)
        
    show screen shopping(left_ref=hero, right_ref=shop)
    with dissolve
    $ pytfall.world_events.run_events("auto") 
    
    call shop_control from _call_shop_control_5
                    
    $ global_flags.del_flag("keep_playing_music")
    hide screen shopping
    with dissolve
    jump hiddenvillage_entrance
    
label Tsunade_Event:
    $ interactions_run_gm_anywhere ("Tsunade", "hiddenvillage_entrance", "story cab_2")

label Naruko_Event:
    scene bg girl_room_5 with dissolve
    menu:
        "Find Kushina" if chars["Kushina_Uzumaki"] not in hero.chars:
            $ interactions_run_gm_anywhere ("Kushina_Uzumaki", "hiddenvillage_entrance", "girl_room_5")
        "Find Naruko" if chars["Naruko_Uzumaki"] not in hero.chars:
            $ interactions_run_gm_anywhere ("Naruko_Uzumaki", "hiddenvillage_entrance", "girl_room_5")
        "Leave":
            jump hiddenvillage_entrance
label Hinata_Event:
    $ interactions_run_gm_anywhere ("Hinata", "hiddenvillage_entrance", "story asian_house")
    
label Ino_Event:
    $ interactions_run_gm_anywhere ("Ino_Yamanaka", "hiddenvillage_entrance", "story asian_house_1")
    
label Karin_Event:
    $ interactions_run_gm_anywhere ("Karin", "hiddenvillage_entrance", "story asian_house_2")
    
label Konan_Event:
    $ interactions_run_gm_anywhere ("Konan", "hiddenvillage_entrance", "story small_library")
    
label Sakura_Event:
    $ interactions_run_gm_anywhere ("Sakura", "hiddenvillage_entrance", "girl_room_4")
    
label Dormitory_Event:
    scene bg story dormitory with dissolve
    menu:
        "Tenten":
            $ interactions_run_gm_anywhere ("Tenten", "hiddenvillage_entrance", "girl_room_9")
        "Temari":
            $ interactions_run_gm_anywhere ("Temari", "hiddenvillage_entrance", "girl_room_9")
        "Leave":
            jump hiddenvillage_entrance