label hiddenVillage_entrance:

    if not "park" in ilists.world_music:
        $ ilists.world_music["park"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("park")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["park"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("hiddenVillage_entrance"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.add("hiddenvillage_matrix", "Explore", Jump("hidden_village_matrix"))
            pytfall.world_actions.finish()
            
    scene bg hidden_village
    with dissolve
    show screen pyt_hiddenVillage_entrance
    
    if not global_flags.flag('visited_hidden_village'):
        $ global_flags.set_flag('visited_hidden_village')
        "From now on you have an access to the hidden village."
        
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    if pytfall.world_quests.check_stage("Sixth Sense") == 2 and not('Virgin' in chars['Karin'].traits) and pytfall.world_quests.check_quest_not_finished("Sixth Sense"):
        jump karin_finish_quest
    if pytfall.world_quests.check_stage("Stubborn Kunoichi") == 3 and not('Virgin' in chars['Temari'].traits) and pytfall.world_quests.check_quest_not_finished("Stubborn Kunoichi"):
        jump temari_finish_quest
    if pytfall.world_quests.check_stage("Uzumaki Clan") == 7 and not('Virgin' in chars['Naruko_Uzumaki'].traits) and pytfall.world_quests.check_quest_not_finished("Uzumaki Clan"):
        jump naruko_finish_quest
    if pytfall.world_quests.check_stage("Weapons Specialist") >= 2 and not('Virgin' in chars['Tenten'].traits) and pytfall.world_quests.check_quest_not_finished("Weapons Specialist"):
        jump tenten_finish_quest
    python:

        while True:

            result = ui.interact()

            if result[0] == 'jump':
                gm.start_gm(result[1])
            if result[0] == 'control':
                renpy.hide_screen("pyt_hiddenVillage_entrance")
                if result[1] == 'return':
                    break

    $ renpy.music.stop(channel="world")
    hide screen pyt_hiddenVillage_entrance
    jump pyt_city
    
screen pyt_hiddenVillage_entrance():

    use pyt_top_stripe(True)
    
    use location_actions("hiddenVillage_entrance")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show('girlmeets', exclude=["swimsuit", "wildness", "beach", "pool", "urban", "stage","onsen", "indoors"], type="first_default",label_cache=True, resize=(300, 400)), return_value=['jump', entry])
    
label hidden_village_matrix:
    hide screen pyt_hiddenVillage_entrance
    scene bg hidden_village
    call screen poly_matrix("library/events/StoryI/coordinates_hidden_village.json", show_exit_button=(0.8, 0.8))
    if not(_return):
        jump hiddenVillage_entrance
    if _return == "House_5":
        if pytfall.world_quests.check_quest_not_finished("Sixth Sense"):
            if pytfall.world_quests.check_stage("Sixth Sense") == 0:
                hide screen pyt_hiddenVillage_entrance
                jump karin_first_meeting
            elif not('Virgin' in chars['Naruko_Uzumaki'].traits) and pytfall.world_quests.check_stage("Sixth Sense") == 1:
                hide screen pyt_hiddenVillage_entrance
                show bg girl_room_12
                call karin_second_meeting
                $ gm.start("girl_meets", chars["Karin"], chars["Karin"].get_vnsprite(), "hiddenVillage_entrance", "girl_room_12")
            else:
                $ interactions_run_gm_anywhere ("Karin", "hiddenVillage_entrance", "girl_room_12")
        else:
            hide screen pyt_hiddenVillage_entrance
            $ interactions_run_gm_anywhere ("Karin", "hiddenVillage_entrance", "girl_room_12")
    elif _return == "House_6":
        jump hidden_village_shop
    elif _return == "House_2":
        if pytfall.world_quests.check_quest_not_finished("Uzumaki Clan"):
            if pytfall.world_quests.check_stage("Uzumaki Clan") == 0:
                jump naruko_first_meeting
            elif pytfall.world_quests.check_stage("Uzumaki Clan") == 2:
                jump naruko_second_meeting
            elif pytfall.world_quests.check_stage("Uzumaki Clan") == 4:
                jump naruko_third_meeting
            elif pytfall.world_quests.check_stage("Uzumaki Clan") == 6:
                jump naruko_final_meeting
            else:
                hide screen pyt_hiddenVillage_entrance
                $ interactions_run_gm_anywhere ("Naruko_Uzumaki", "hiddenVillage_entrance", "girl_room_4")
        else:
            hide screen pyt_hiddenVillage_entrance
            $ interactions_run_gm_anywhere ("Naruko_Uzumaki", "hiddenVillage_entrance", "girl_room_4")
    elif _return == "Training":
        if pytfall.world_quests.check_quest_not_finished("Stubborn Kunoichi"):
            if pytfall.world_quests.check_stage("Stubborn Kunoichi") == 0:
                hide screen pyt_hiddenVillage_entrance
                jump temari_first_meeting
            elif pytfall.world_quests.check_stage("Stubborn Kunoichi") == 2:
                hide screen pyt_hiddenVillage_entrance
                jump temari_before_fight
            elif pytfall.world_quests.check_quest_not_finished("Weapons Specialist"):
                # if pytfall.world_quests.check_stage("Stubborn Kunoichi") >= 3 and pytfall.world_quests.check_stage("Weapons Specialist") == 0:
                if pytfall.world_quests.check_stage("Weapons Specialist") == 0:
                    hide screen pyt_hiddenVillage_entrance
                    jump tenten_first_meeting
                elif pytfall.world_quests.check_stage("Weapons Specialist") == 1:
                    hide screen pyt_hiddenVillage_entrance
                    jump tenten_second_meeting
    elif _return == "House_9":
        if pytfall.world_quests.check_stage("Stubborn Kunoichi") == 0 and not(pytfall.world_quests.check_quest_not_finished("Stubborn Kunoichi")):
            "The door is locked. Looks like there is no one here..."
        elif (pytfall.world_quests.check_stage("Stubborn Kunoichi") == 1) and (chars["Temari"].disposition >= 200) and (pytfall.world_quests.check_quest_not_finished("Stubborn Kunoichi")):
            hide screen pyt_hiddenVillage_entrance
            show bg girls_dorm with dissolve
            jump temari_second_meeting
        else:
            menu:
                "It's a dormitory for those kunoichi who don't own a house. Who you want to see?"
                
                "Temari" if pytfall.world_quests.check_stage("Stubborn Kunoichi") >= 1:
                    $ interactions_run_gm_anywhere ("Temari", "hiddenVillage_entrance", "girls_dorm")
                "Tenten" if pytfall.world_quests.check_stage("Weapons Specialist") >= 2:
                    $ interactions_run_gm_anywhere ("Tenten", "hiddenVillage_entrance", "girls_dorm")
                "Leave":
                    jump hiddenVillage_entrance
    "Result: [_return]"
    jump hidden_village_matrix
    
label hidden_village_shop:

    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5
        
    hide bg hidden_village
    
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
        r "Hm? Ah, you are that new guy."
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
        
    show screen pyt_shopping(left_ref=hero, right_ref=shop)
    with dissolve
    $ pytfall.world_events.run_events("auto") 
    
    call shop_control from _call_shop_control_5
                    
    $ global_flags.del_flag("keep_playing_music")
    hide screen pyt_shopping
    with dissolve
    jump hiddenVillage_entrance