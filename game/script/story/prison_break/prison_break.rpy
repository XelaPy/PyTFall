init:
    image map_scroll = ProportionalScale("content/events/StoryI/scroll.webp", 900, 900)
    image blueprint = ProportionalScale("content/events/StoryI/blueprint.webp", 660, 540)
    transform blueprint_position:
        align (0.5, 0.6)
    $ sflash = Fade(.25, 0, .25, color=darkred)
init -10 python:
    q_dissolve = Dissolve(.2) # fast dissolve to quickly show backgrounds
    def eyewarp(x):
        return x**1.33
    eye_open = ImageDissolve("content/gfx/masks/eye_blink.webp", 0.5, ramplen=128, reverse=False, time_warp=eyewarp) # transitions for backgrounds, try to emulate effect of opening or closing eyes
    eye_shut = ImageDissolve("content/gfx/masks/eye_blink.webp", 0.5, ramplen=128, reverse=True, time_warp=eyewarp)

init:
    $ point = "content/gfx/interface/icons/move15.png" # the point which shows location on the map; it's actually a part of the main gui
    $ enemy_soldier = Character("Guard", color=white, what_color=white, show_two_window=True, show_side_image=ProportionalScale("content/npc/mobs/ct1.png", 120, 120))
    $ enemy_soldier2 = Character("Guard", color=white, what_color=white, show_two_window=True, show_side_image=ProportionalScale("content/npc/mobs/h1.png", 120, 120))

screen prison_break_controls(): # control buttons screen
    use top_stripe(False, None, False, True)
    frame:
        xalign 0.95
        ypos 50
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_prefix "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("prison_break_controls"), Play("events2", "events/letter.mp3"), Jump("storyi_map")]
                text "Show map" size 15
            if not hero.has_flag("ndd_storyi_rest"):
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("prison_break_controls"), Jump("mc_action_storyi_rest")]
                    text "Rest" size 15
            if not hero.has_flag("ndd_storyi_heal"):
                if storyi_prison_location == 3:
                    button:
                        xysize (120, 40)
                        yalign 0.5
                        action [Hide("prison_break_controls"), Jump("storyi_treat_wounds")]
                        text "Heal" size 15
            if storyi_prison_location == 5 and not hero.has_flag("defeated_boss_1"):
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("prison_break_controls"), Jump("storyi_bossroom")]
                    text "Go Up" size 15
            if storyi_prison_location in storyi_treasures:
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("prison_break_controls"), Jump("storyi_search_items")]
                    text "Search" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("prison_break_controls"), Jump("forest_dark")]
                text "Exit" size 15

            if DEBUG:
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("prison_break_controls"), Jump("storyi_bossroom")]
                    text "Test Boss" size 15

label storyi_bossroom:
    stop music
    stop world fadeout 2.0
    play world "events/6.ogg" fadein 2.0 loop
    play events2 "events/wind1.mp3" fadein 2.0 loop
    show bg story p2 with dissolve
    show sinister_star:
        pos (704, 91)
        anchor (0.5, 0.5)
        subpixel True
        zoom 0.1
        alpha 0
        linear 1.5 alpha 1.0
    "Finally, you reach the throne room on top of the building. Some windows are broken, and the wind blows through."
    menu:
        "If you continue, there won't be way back."
        "Continue":
            $ pass
        "Return to the ground floor":
            call storyi_show_bg from _call_storyi_show_bg
            play world "Theme2.ogg" fadein 2.0 loop
            stop events2
            hide sinister_star
            show screen prison_break_controls
            jump storyi_gui_loop
    show sinister_star:
        linear 2.5 zoom 0.2
    "You take a step forward, and something changes."
    show bg story p3 with dissolve
    show sinister_star:
        linear 1.5 zoom 0.3
    extend " Daylight fades, being replaced by red glow from above."
    show sinister_star:
        linear 2.0 zoom 0.4
    "There is a tiny red star in the gem on the ceiling."
    show sinister_star:
        linear 2.0 zoom 0.5
    extend " It wakes up, disturbed by your presence."
    show sinister_star:
        linear 8 ypos 375 zoom 1.5
    "The air temperature rises rapidly."
    show bg story p3 with sflash
    show sinister_star:
        linear 4 zoom 2.5
    extend " You prepare for a fight!"
    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        your_team = Team(name="Your Team", max_size=3)
        mob = build_mob(id="Blazing Star", level=25)
        mob.stats.lvl_max["health"] += 500
        mob.stats.max["health"] += 500
        mob.mod_stat("health", 500)
        mob.stats.lvl_max["mp"] += 100
        mob.stats.max["mp"] += 100
        mob.mod_stat("mp", 100)
        mob.controller = Complex_BE_AI(mob)
        enemy_team.add(mob)
        result = run_default_be(enemy_team,
                                background="content/gfx/bg/story/p_b.webp",
                                slaves=True, track="content/sfx/music/be/battle (5)b.ogg",
                                prebattle=False, death=True, use_items=True)

    if result is True:
        show bg story p4 with sflash
        show sinister_star at Position(xpos = 704, xanchor=.5, ypos=375, yanchor=.5):
            anchor (0.5, 0.5)
            zoom 1.0
            alpha 1.0
        $ hero.set_flag("defeated_boss_1")
        "The star loses its strength, and the air temperature drops."
        hide sinister_star with dissolve
        extend " You pick it up and put in your pocket."
        $ hero.add_item("Red Star")
        stop events2
        call storyi_show_bg from _call_storyi_show_bg_1
        play world "Theme2.ogg" fadein 2.0 loop
        "You return to the ground floor."
        show screen prison_break_controls
        jump storyi_gui_loop
    else:
        jump game_over

label mc_action_storyi_rest: # resting inside the dungeon; team may be attacked during the rest
    $ hero.set_flag("ndd_storyi_rest")
    show bg tent with q_dissolve
    python:
        for i in hero.team:
            i.vitality += int(i.get_max("vitality")*0.3)
            i.mp +=  int(i.get_max("mp")*0.1)
    "You set up a small camp and rest for a bit."
    $ fight_chance += 10
    call storyi_show_bg from _call_storyi_show_bg_2
    if dice(fight_chance):
        hide screen prison_break_controls
        "You have been ambushed by enemies!"
        jump storyi_randomfight
    show screen prison_break_controls
    jump storyi_gui_loop

label storyi_randomfight:  # initiates fight with random enemy team
    $ fight_chance = 10

    python:
        enemy_team = Team(name="Enemy Team", max_size=3)

        for j in range(randint(1, 3)):
            mob = build_mob(id=random.choice(enemies), level=15)
            mob.controller = Complex_BE_AI(mob)
            enemy_team.add(mob)

        result = run_default_be(enemy_team,
                                background="content/gfx/bg/be/b_dungeon_1.webp",
                                slaves=True, prebattle=False,
                                death=False, skill_lvl=4, give_up="escape",
                                use_items=True)

    if result is True:
        call storyi_show_bg from _call_storyi_show_bg_3
        play world "Theme2.ogg" fadein 2.0 loop

        if storyi_prison_location in [6, 14, 2, 8, 15, 16, 11, 18] and dice(80):
            $ money = randint(5, 15)
        elif storyi_prison_location in [9, 10] and dice(90):
            $ money = randint(15, 30)
        else:
            $ money = 0

        $ hero.add_money(money, reason="Loot")

        if persistent.battle_results:
            call screen give_exp_after_battle(hero.team, enemy_team, money=money)

        show screen prison_break_controls
        jump storyi_gui_loop
    elif result == "escape":
        $ be_hero_escaped(hero.team)
        scene black
        pause 1.0
        jump forest_entrance
    elif result is False:
        jump game_over


label storyi_treat_wounds:
    $ j = False
    python:
        for i in hero.team:
            if i.health < i.get_max("health"):
                j = True
                break
    if j:
        python:
            for i in hero.team:
                i.health = i.get_max("health")
        $ hero.set_flag("ndd_storyi_heal")
        "Health is restored!"
    else:
        "Everyone is healthy already."
    show screen prison_break_controls
    $ del j
    jump storyi_gui_loop

label storyi_start: # beginning point of the dungeon;
    $ enemies = ["Skeleton", "Skeleton Warrior", "Will-o-wisp"]
    $ fight_chance = 100
    stop music
    stop world fadeout 2.0
    scene black with dissolve
    # show expression Text("Some time later", style="TisaOTM", align=(0.5, 0.33), size=40) as txt1:
        # alpha 0
        # linear 3.5 alpha 1.0
    # pause 2.5
    # hide txt1
    play world "Theme2.ogg" fadein 2.0 loop
    show bg story d_entrance with eye_open
    $ storyi_prison_stage = 1
    $ storyi_prison_location = 6
    if not hero.has_flag("been_in_old_ruins"):
        $ hero.set_flag("been_in_old_ruins")
        $ storyi_treasures = [1, 3, 7, 10, 11, 13]
        hero.say "I've found the ruins of a tower near the city."
        hero.say "It may be not safe here, but I bet there is something valuable deep inside!"
        "You can enter and exit the ruins at any point, but it will consume your AP."
    show screen prison_break_controls

label storyi_gui_loop: # the gui loop; we jump here every time we need to show controlling gui
    while 1:
        $ result = ui.interact()
        if result in hero.team:
            $ came_to_equip_from = "storyi_continue"
            $ eqtarget = result
            $ equipment_safe_mode = True
            hide screen prison_break_controls
            jump char_equip

label storyi_continue: # the label where we return after visiting characters equipment screens
    call storyi_show_bg from _call_storyi_show_bg_4
    $ equipment_safe_mode = False
    show screen prison_break_controls
    jump storyi_gui_loop

label storyi_show_bg: # shows bg depending on matrix location; due to use of BE it must be a call, and not a part of matrix logic itself
    if storyi_prison_location == 1:
        show bg dungeoncell with q_dissolve
    elif storyi_prison_location == 2:
        show bg story prison with q_dissolve
    elif storyi_prison_location == 3:
        show bg infirmary with q_dissolve
    elif storyi_prison_location == 4:
        show bg story barracks with q_dissolve
    elif storyi_prison_location == 6:
        show bg story d_entrance with q_dissolve
    elif storyi_prison_location == 7:
        show bg story storage with q_dissolve
    elif storyi_prison_location == 5:
        show bg story main_hall with q_dissolve
    elif storyi_prison_location == 8:
        show bg story barracks with q_dissolve
    elif storyi_prison_location == 9:
        show bg dungeoncell with q_dissolve
    elif storyi_prison_location == 10:
        show bg dung_2 with q_dissolve
    elif storyi_prison_location == 11:
        show bg story weaponry with q_dissolve
    elif storyi_prison_location == 12:
        show bg story dinning_hall with q_dissolve
    elif storyi_prison_location == 13:
        show bg story storage with q_dissolve
    elif storyi_prison_location == 14:
        show bg story prison_1 with q_dissolve
    elif storyi_prison_location == 15:
        show bg story prison_1 with q_dissolve
    elif storyi_prison_location == 16:
        show bg story prison_1 with q_dissolve
    elif storyi_prison_location == 17:
        show bg story barracks with q_dissolve
    elif storyi_prison_location == 18:
        show bg story prison_1 with q_dissolve
    if storyi_prison_location in [6, 14, 2, 8, 15, 16, 11, 18]:
        $ enemies = ["Skeleton", "Skeleton Warrior", "Will-o-wisp"]
    elif storyi_prison_location in [9, 10]:
        $ enemies = ["Seductive Slime", "Devil Rat"]
    elif storyi_prison_location == 5:
        $ enemies = ["Fire Spirit", "Flame Spirit", "Fiery Shadow"]
    else:
        $ enemies = ["Slime", "Alkaline Slime", "Acid Slime"]
    if storyi_prison_location in storyi_treasures:
        $ notify("It might be worth to search this room...")
    return

label storyi_search_items:
    "You look around the room in search of something useful."
    if not hero.has_flag("storyi_items_room_1"):
        "There is something shiny in the corner of the prison cell..."
        $ give_to_mc_item_reward(type="loot", price=100)
        $ give_to_mc_item_reward(type="loot", price=200)
        if dice(hero.luck + 100):
            $ give_to_mc_item_reward(type="loot", price=300)
        $ hero.set_flag("storyi_items_room_1")

    if storyi_prison_location == 3:
        "Surveying the room, you found a few portable restoration items. Sadly, others are too heavy and big to carry around."
        $ give_to_mc_item_reward(type="restore", price=100)
        $ give_to_mc_item_reward(type="restore", price=200)
        if dice(hero.luck + 100):
            $ give_to_mc_item_reward(type="restore", price=400)
    elif storyi_prison_location == 7:
        "You see some old armor on the shelves."
        $ give_to_mc_item_reward(type="armor", price=500)
        $ give_to_mc_item_reward(type="armor", price=700)
        if dice(hero.luck + 100):
            $ give_to_mc_item_reward(type="armor", price=1000)
    elif storyi_prison_location == 11:
        "Among a heap of rusty blades, you see some good weapons."
        $ give_to_mc_item_reward(type="weapon", price=500)
        $ give_to_mc_item_reward(type="weapon", price=700)
        if dice(hero.luck + 100):
            $ give_to_mc_item_reward(type="weapon", price=1000)
    elif storyi_prison_location == 13:
        "Most of the food is spoiled, but some of it is still edible."
        $ give_to_mc_item_reward(type="food", price=500)
        $ give_to_mc_item_reward(type="food", price=500)
        if dice(hero.luck + 100):
            $ give_to_mc_item_reward(type="food", price=500)
    elif storyi_prison_location == 10:
        "There is a pile of clothes in the corner, probably remained from the former prisoners."
        $ give_to_mc_item_reward(type="dress", price=500)
        $ give_to_mc_item_reward(type="dress", price=500)
        if dice(hero.luck + 100):
            $ give_to_mc_item_reward(type="dress", price=500)
    $ storyi_treasures.remove(storyi_prison_location)
    show screen prison_break_controls
    jump storyi_gui_loop

label storyi_move_map_point: # moves green point to show team location on the map
    if storyi_prison_location == 1:
        show expression point at Transform(pos=(709, 203)) with move
    elif storyi_prison_location == 2:
        show expression point at Transform(pos=(784, 255)) with move
    elif storyi_prison_location == 3:
        show expression point at Transform(pos=(841, 202)) with move
    elif storyi_prison_location == 4:
        show expression point at Transform(pos=(798, 333)) with move
    elif storyi_prison_location == 6:
        show expression point at Transform(pos=(777, 471)) with move
    elif storyi_prison_location == 7:
        show expression point at Transform(pos=(779, 527)) with move
    elif storyi_prison_location == 5:
        show expression point at Transform(pos=(659, 356)) with move
    elif storyi_prison_location == 8:
        show expression point at Transform(pos=(656, 517)) with move
    elif storyi_prison_location == 9:
        show expression point at Transform(pos=(622, 165)) with move
    elif storyi_prison_location == 10:
        show expression point at Transform(pos=(564, 139)) with move
    elif storyi_prison_location == 11:
        show expression point at Transform(pos=(530, 456)) with move
    elif storyi_prison_location == 12:
        show expression point at Transform(pos=(442, 358)) with move
    elif storyi_prison_location == 13:
        show expression point at Transform(pos=(427, 277)) with move
    elif storyi_prison_location == 14:
        show expression point at Transform(pos=(794, 421)) with move
    elif storyi_prison_location == 15:
        show expression point at Transform(pos=(593, 238)) with move
    elif storyi_prison_location == 16:
        show expression point at Transform(pos=(547, 194)) with move
    elif storyi_prison_location == 17:
        show expression point at Transform(pos=(444, 417)) with move
    elif storyi_prison_location == 18:
        show expression point at Transform(pos=(523, 296)) with move
    return

label storyi_map: # shows dungeon map and calls matrix to control it
    show map_scroll at truecenter
    show blueprint at blueprint_position
    call storyi_move_map_point from _call_storyi_move_map_point
    call screen poly_matrix("script/story/prison_break/coordinates_1.json", cursor="content/gfx/interface/icons/zoom_pen.png", xoff=0, yoff=0, show_exit_button=(1.0, 1.0))
    $ setattr(config, "mouse", None)
    $ fight_chance += randint(10, 20)
    if _return == "Cell":
        if storyi_prison_location == 1:
            "A highly guarded prison cell."
            jump storyi_map
        elif storyi_prison_location != 2:
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_cell
    elif _return == "Prison":
        if storyi_prison_location == 2:
            "A prison block with many empty cells."
            jump storyi_map
        elif not(storyi_prison_location in [1, 3, 4]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_prisonblock
    elif _return == "Infirmary":
        if storyi_prison_location == 3:
            "The prison infirmary. They store there a considerable amount of medical supplies."
            jump storyi_map
        elif storyi_prison_location <> 2:
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_infirmary
    elif _return == "GRoom_2":
        if storyi_prison_location == 4:
            "A small guard post."
            jump storyi_map
        elif not(storyi_prison_location in [2, 14]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_groom2
    elif _return == "GRoom_3":
        if storyi_prison_location == 17:
            "A small guard post."
            jump storyi_map
        elif not(storyi_prison_location in [11, 16, 12]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_groom3
    elif _return == "MHall":
        if storyi_prison_location == 5:
            "A huge half-light central hall."
            jump storyi_map
        elif not(storyi_prison_location in [7, 8, 14, 15, 18]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_barracks
    elif _return == "Dung":
        if storyi_prison_location == 6:
            "The entrance to the dungeon. Tightly shut."
            jump storyi_map
        elif not(storyi_prison_location in [14, 7]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_dungentr
    elif _return == "Storage":
        if storyi_prison_location == 7:
            "A small storage filled with old armor and household accessories."
            jump storyi_map
        elif not(storyi_prison_location in [6, 5]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_storage
    elif _return == "MEntrance":
        if storyi_prison_location == 8:
            "The main entrance. It's usually well guarded."
            jump storyi_map
        elif storyi_prison_location <> 5:
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_mentrance
    elif _return == "IRoom":
        if storyi_prison_location == 9:
            "The interrogation room for preliminary inquests."
            jump storyi_map
        elif not(storyi_prison_location in [10, 15, 16]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_iroom
    elif _return == "TRoom":
        if storyi_prison_location == 10:
            "The torturing room. It has all kinds of devices, from vibrators and clamps to whips and scissors."
            jump storyi_map
        elif storyi_prison_location <> 9:
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_troom
    elif _return == "WRoom":
        if storyi_prison_location == 11:
            "The weaponry. It has a good selection of weapons, including the weapons confiscated from the prisoners."
            jump storyi_map
        elif not(storyi_prison_location in [16, 17]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_wroom
    elif _return == "CRoom":
        if storyi_prison_location == 12:
            "The dining hall. Here slaves prepare food for guards and prisoners."
            jump storyi_map
        elif not(storyi_prison_location in [17, 13]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_croom
    elif _return == "GRoom_1":
        if storyi_prison_location == 13:
            "Another small storage filled with food supplies."
            jump storyi_map
        elif not(storyi_prison_location in [12, 18]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_groom_1
    elif _return == "Passage_1":
        if storyi_prison_location == 14:
            "A narrow corridor between the two rooms"
            jump storyi_map
        elif not(storyi_prison_location in [4, 6, 5]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_passage_1
    elif _return == "Passage_2":
        if storyi_prison_location == 15:
            "A narrow corridor between the two rooms"
            jump storyi_map
        elif not(storyi_prison_location in [5, 9, 16]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_passage_2
    elif _return == "Passage_3":
        if storyi_prison_location == 16:
            "A narrow corridor between the two rooms"
            jump storyi_map
        elif not(storyi_prison_location in [15, 9, 11, 17]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_passage_3
    elif _return == "Passage_4":
        if storyi_prison_location == 18:
            "A narrow corridor between the two rooms"
            jump storyi_map
        elif not(storyi_prison_location in [5, 13]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_passage_4
    else:
        play events2 "events/letter.mp3"
        hide map_scroll
        hide blueprint
        hide expression point
        with dissolve
        show screen prison_break_controls
        jump storyi_gui_loop

# further go personal labels for each location to ensure full control over events

label prison_storyi_passage_1:
    $ storyi_prison_location = 14
    call storyi_move_map_point from _call_storyi_move_map_point_1
    call storyi_show_bg from _call_storyi_show_bg_5
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_passage_2:
    $ storyi_prison_location = 15
    call storyi_move_map_point from _call_storyi_move_map_point_2
    call storyi_show_bg from _call_storyi_show_bg_6
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_passage_3:
    $ storyi_prison_location = 16
    call storyi_move_map_point from _call_storyi_move_map_point_3
    call storyi_show_bg from _call_storyi_show_bg_7
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_passage_4:
    $ storyi_prison_location = 18
    call storyi_move_map_point from _call_storyi_move_map_point_4
    call storyi_show_bg from _call_storyi_show_bg_8
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_cell:
    $ storyi_prison_location = 1
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_5
    call storyi_show_bg from _call_storyi_show_bg_9
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_prisonblock:
    $ storyi_prison_location = 2
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_6
    call storyi_show_bg from _call_storyi_show_bg_10
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_infirmary:
    $ storyi_prison_location = 3
    play events2 "events/door_open.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_7
    call storyi_show_bg from _call_storyi_show_bg_11
    jump storyi_map

label prison_storyi_event_groom2:
    $ storyi_prison_location = 4
    play events2 "events/door_open.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_8
    call storyi_show_bg from _call_storyi_show_bg_12
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_groom3:
    $ storyi_prison_location = 17
    play events2 "events/door_open.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_9
    call storyi_show_bg from _call_storyi_show_bg_13
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_dungentr:
    $ storyi_prison_location = 6
    call storyi_move_map_point from _call_storyi_move_map_point_10
    call storyi_show_bg from _call_storyi_show_bg_14
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_storage:
    $ storyi_prison_location = 7
    play events2 "events/door_open.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_11
    call storyi_show_bg from _call_storyi_show_bg_15
    jump storyi_map

label prison_storyi_event_barracks:
    $ storyi_prison_location = 5
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_12
    call storyi_show_bg from _call_storyi_show_bg_16
    if not hero.has_flag("defeated_boss_1"):
        hero.say "I see old stairs. I wonder where they lead."
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_iroom:
    $ storyi_prison_location = 9
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_13
    call storyi_show_bg from _call_storyi_show_bg_17
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_mentrance:
    $ storyi_prison_location = 8
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_14
    call storyi_show_bg from _call_storyi_show_bg_18
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_troom:
    $ storyi_prison_location = 10
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_15
    call storyi_show_bg from _call_storyi_show_bg_19
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_wroom:
    $ storyi_prison_location = 11
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_16
    call storyi_show_bg from _call_storyi_show_bg_20
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_groom_1:
    $ storyi_prison_location = 13
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_17
    call storyi_show_bg from _call_storyi_show_bg_21
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map

label prison_storyi_event_croom:
    $ storyi_prison_location = 12
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point from _call_storyi_move_map_point_18
    call storyi_show_bg from _call_storyi_show_bg_22
    if dice(fight_chance):
        jump storyi_randomfight
    jump storyi_map
