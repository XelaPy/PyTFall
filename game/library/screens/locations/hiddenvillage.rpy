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
    
    if global_flags.flag('visited_hidden_village'): # should be changed to not global_flags.flag('visited_hidden_village') before the release !!!!!!!!!!!!!!!!!!!
        $ global_flags.set_flag('visited_hidden_village')
        $ naruto_quest_characters_list = list(i for i in chars.values() if "Naruto" in i.origin and i.name != "Tsunade" and i.name != "Konan") # list of all quest characters from the pack that are still a part of the quest; we'll remove them from here as player finishes their personal quests
        python:
            for i in naruto_quest_characters_list:
                i.set_flag("quest_cannot_be_hired") # cannot be hired until the quest is finished
                i.set_flag("quest_cannot_be_fucked") # cannot be fucked until we remove this flag via an event
                i.set_flag("event_to_interactions_hidden_village_teaching", value={"label": "hidden_village_home_teaching", "button_name": "Teach her about the world", "condition": "True"})
                if i.name != "Naruko":
                    i.set_flag("village_quest_knowledge_level", value=0) # all chars have integer flags = 0, it's the starting level of their knowledge
                else:
                    i.set_flag("village_quest_knowledge_level", value=20) # except her since she had a quest in the city already
                    i.set_flag("village_quest_house_is_visible") # these flags control if MC has access to character house inside the matrix, we give one to her
            chars["Tsunade"].set_flag("quest_cannot_be_hired")
            chars["Tsunade"].set_flag("event_to_interactions_hidden_village_hiring_tsunade", value={"label": "hidden_village_hiring_tsunade", "button_name": "Ask her to join you", "condition": "True"})
            chars["Tsunade"].set_flag("village_quest_house_is_visible")
            chars["Konan"].set_flag("quest_cannot_be_hired")
            chars["Konan"].set_flag("event_to_interactions_hidden_village_hiring_konan", value={"label": "hidden_village_hiring_konan", "button_name": "Ask her to join you", "condition": "True"})
            chars["Konan"].set_flag("village_quest_house_is_visible")
        jump first_arrive_to_the_hidden_village
    scene bg hiddenvillage_entrance
    with dissolve
    show screen hiddenvillage_entrance
    
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
    if global_flags.flag('hidden_village_study_icon'):
        imagebutton:
            pos(120, 200)
            idle (img_study)
            hover (im.MatrixColor(img_study, im.matrix.brightness(0.15)))
            action [Hide("hiddenvillage_entrance"), Jump("hidden_village_study_building"), With(dissolve)]
    use location_actions("hiddenvillage_entrance")
    if global_flags.flag('hidden_village_shop_first_enter'): # the shop is hidden until found via matrix
        $img = ProportionalScale("content/gfx/interface/icons/ninja_shop.png", 100, 70)
        imagebutton:
            pos(300, 315)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
            action [Hide("hiddenvillage_entrance"), Jump("hidden_village_shop")]
    
label hidden_village_study_building:
    scene bg story study
    show screen hidden_village_study_menu

    while 1:
        $ result = ui.interact()
        
screen hidden_village_study_menu():
    frame:
        xalign 0.95
        ypos 20
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_group "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("hidden_village_study_menu"), Jump("hidden_village_check_knowledge")]
                text "Exam" size 15
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("hidden_village_study_menu"), Jump("hidden_village_study")]
                text "Teach" size 15
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("hidden_village_study_menu"), Jump("hiddenvillage_entrance"), With(dissolve)]
                text "Leave" size 15
    
label hidden_village_check_knowledge: # here we form a screen of characters and return the level of knowledge for the selected one
    if not global_flags.flag('visited_hidden_village_exam'):
        $ global_flags.set_flag('visited_hidden_village_exam')
        "Here you can check the level of knowledge for every villager. Once their knowledge about the world will be high enough, you will be able to hire them at this screen."
    python:
        characters = {}
        for i in naruto_quest_characters_list:
            if i.disposition < 100:
                l = "indifferent"
            elif i.disposition < 300:
                l = "happy"
            else:
                l = "shy"
            characters[i]=l
        del l
    $ q = renpy.call_screen("hidden_village_chars_list", characters)
    $ level = q.flag("village_quest_knowledge_level")
    if level < 20:
        q.say "[q.name] knows nothing about the world outside. It's too dangerous for her to even leave the village unattended."
    elif level < 40:
        q.say "[q.name] knows the most basic facts about the world outside, but she's still far from self-dependence."
    elif level < 60:
        q.say "[q.name] knows enough about the world outside to avoid problems with the law, but not enough to not get into awkward situations."
    elif level < 80:
        q.say "[q.name] can act naturally most of the time, but flawless communication with the locals is sill problematic for her."
    elif level < 100:
        q.say "[q.name] knows enough about the world outside to pass for a tourist from a nearby country. There is still a room for improvement though."
    else:
        q.say "[q.name] is ready for the outside world, there is nothing more you can teach her."
    if level >= 100 and "Virgin" not in q.traits:
        menu:
            "You fulfilled all conditions. Do you wish to hire her?"
            "Yes":
                $ q.del_flag("quest_cannot_be_hired")
                "You propose [q.name] to work for you."
                call interactions_agrees_to_be_hired
                $ hero.add_char(q)
                $ naruto_quest_characters_list.remove(q)
                if q.flag("village_quest_house_is_visible"):
                    $ q.del_flag("village_quest_house_is_visible")
                $ q.del_flag("village_quest_knowledge_level")
                $ q.del_flag("event_to_interactions_hidden_village_teaching")
                if not naruto_quest_characters_list:
                    $ global_flags.del_flag('hidden_village_study_icon')
                    jump hiddenvillage_entrance
            "Maybe later":
                $ pass
    jump hidden_village_study_building
    
label hidden_village_matrix: 
    hide screen hiddenvillage_entrance
    scene bg hiddenvillage_entrance
    $ hidden_list = []
    # the shop is hidden in matrix after found once, could be accessed via icon outside of the matrix instead
    if global_flags.flag('hidden_village_shop_first_enter'):
        $ hidden_list.append("hidden_village_shop")
    # here we check personal characters flags and decide if their houses should be hidden from MC or not
    # in theory it could be automated via "for" loop; however we sometimes have 2 characters per matrix location, and location should be available even if only one of the characters has the needed flag, so it won't be a simple loop anyway
    if not chars["Tsunade"].flag("village_quest_house_is_visible"):
        $ hidden_list.append("Tsunade_Event")
    if not chars["Hinata"].flag("village_quest_house_is_visible"):
        $ hidden_list.append("Hinata_Event")
    if not chars["Kushina_Uzumaki"].flag("village_quest_house_is_visible") and not chars["Naruko_Uzumaki"].flag("village_quest_house_is_visible"):
        $ hidden_list.append("Naruko_Event")
    if not chars["Ino_Yamanaka"].flag("village_quest_house_is_visible"):
        $ hidden_list.append("Ino_Event")
    if not chars["Karin"].flag("village_quest_house_is_visible"):
        $ hidden_list.append("Karin_Event")
    if not chars["Konan"].flag("village_quest_house_is_visible"):
        $ hidden_list.append("Konan_Event")
    if not chars["Sakura"].flag("village_quest_house_is_visible"):
        $ hidden_list.append("Sakura_Event")
    if not chars["Temari"].flag("village_quest_house_is_visible") and not chars["Tenten"].flag("village_quest_house_is_visible"):
        $ hidden_list.append("Dormitory_Event")
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
    
label hidden_village_shop: # ninja shop logic
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
    
# further go personal chars events when MC visits their houses
label Tsunade_Event:
    $ interactions_run_gm_anywhere ("Tsunade", "hiddenvillage_entrance", "story cab_2")

label Naruko_Event:
    scene bg girl_room_5 with dissolve
    menu:
        "Find Kushina" if chars["Kushina_Uzumaki"].flag("village_quest_house_is_visible"):
            $ interactions_run_gm_anywhere ("Kushina_Uzumaki", "hiddenvillage_entrance", "girl_room_5")
        "Find Naruko" if chars["Naruko_Uzumaki"].flag("village_quest_house_is_visible"):
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
        "Find Tenten" if chars["Tenten"].flag("village_quest_house_is_visible"):
            $ interactions_run_gm_anywhere ("Tenten", "hiddenvillage_entrance", "girl_room_9")
        "Find Temari" if chars["Temari"].flag("village_quest_house_is_visible"):
            $ interactions_run_gm_anywhere ("Temari", "hiddenvillage_entrance", "girl_room_9")
        "Leave":
            jump hiddenvillage_entrance
            
label hidden_village_home_teaching:
    if hero.AP > 0:
        "You tell her stories about the outside world. She listens with interest."
        $ char.set_flag("village_quest_knowledge_level", value=char.flag("village_quest_knowledge_level")+500)
        call interactions_teaching_lines
        $ hero.AP -= 1
    else:
        "You don't have Action Points left. Try again tomorrow."
    jump girl_interactions