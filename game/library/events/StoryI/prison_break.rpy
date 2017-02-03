init:
    image map_scroll = ProportionalScale("content/events/StoryI/scroll.png", 900, 900)
    image blueprint = ProportionalScale("content/events/StoryI/blueprint.png", 660, 540)
    
    transform blueprint_position:
        align (0.5, 0.6)
init python:
    q_dissolve = Dissolve(.2)
    def eyewarp(x):
        return x**1.33
    eye_open = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=False, time_warp=eyewarp)
    eye_shut = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=True, time_warp=eyewarp)
    
    def storyi_randomfight():  # initiates fight with random enemy team; TODO: replace with default battle function
        enemy_team = Team(name="Enemy Team", max_size=3)
        your_team = Team(name="Your Team", max_size=3)
        rand_mobs = ["Infantryman", "Archer", "Soldier"]
        for i in range(randint(1, 3)):
            mob = build_mob(id=choice(rand_mobs), level=max(hero.level, 10))
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
        your_team.add(k)
        for member in your_team:
            member.controller = BE_AI(member)
        # your_team.add(hero)
        store.battle = BE_Core(Image("content/gfx/bg/be/b_dungeon_1.jpg"), music="content/sfx/music/be/battle (14).mp3", start_sfx=get_random_image_dissolve(1.5), end_sfx=dissolve)
        battle = store.battle
        battle.teams.append(your_team)
        battle.teams.append(enemy_team)
        battle.start_battle()
        your_team.reset_controller()
        if battle.winner != your_team:
            renpy.jump("game_over")
init:
    $ point = "content/gfx/interface/icons/move15.png"
    $ enemy_soldier = Character("Guard", color=white, what_color=white, show_two_window=True, show_side_image=ProportionalScale("content/npc/mobs/ct1.png", 120, 120))
    $ enemy_soldier2 = Character("Guard", color=white, what_color=white, show_two_window=True, show_side_image=ProportionalScale("content/npc/mobs/h1.png", 120, 120))
    # $ scroll = "content/events/Story/scroll.png"
    # $ blueprint = "content/events/Story/blueprint.png"

    
screen prison_break_controls():
    use top_stripe(True) # <- probably shouldn't be here? unlikely it's safe enough inside closed events
    frame:
        xalign 0.95
        ypos 50
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_prefix "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("prison_break_controls"), Jump("storyi_map")]
                text "Show map" size 15
    
label storyi_start:
    stop music
    stop world fadeout 2.0
    scene black with dissolve
    # show expression Text("Some time later", style="TisaOTM", align=(0.5, 0.33), size=40) as txt1:
        # alpha 0
        # linear 3.5 alpha 1.0
    # pause 2.5
    # hide txt1
    play world "Theme2.ogg" fadein 2.0 loop
    show bg dungeoncell with eye_open
    $ storyi_prison_location = 1
    $ storyi_prison_stage = 1
    show screen prison_break_controls
    while 1:
        $ result = ui.interact()
        
label storyi_move_map_point: # via calls only!
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
        show expression point at Transform(pos=(661, 356)) with move
    elif storyi_prison_location == 8:
        show expression point at Transform(pos=(656, 517)) with move
    elif storyi_prison_location == 9:
        show expression point at Transform(pos=(622, 165)) with move
    elif storyi_prison_location == 10:
        show expression point at Transform(pos=(564, 139)) with move
    elif storyi_prison_location == 11:
        show expression point at Transform(pos=(530, 453)) with move
    elif storyi_prison_location == 12:
        show expression point at Transform(pos=(442, 358)) with move
    elif storyi_prison_location == 13:
        show expression point at Transform(pos=(427, 277)) with move
    return
    
label storyi_map:
    show map_scroll at truecenter 
    show blueprint at blueprint_position
    call storyi_move_map_point
    call screen poly_matrix("library/events/StoryI/coordinates_1.json", cursor="content/gfx/interface/icons/zoom_pen.png", show_exit_button=(1.0, 1.0))
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
            "The prison infirmary. They store there a huge amount of medical supplies."
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
        elif not(storyi_prison_location in [2, 5, 6]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_groom2
    elif _return == "MHall":
        if storyi_prison_location == 5:
            "A huge half-light central hall."
            jump storyi_map
        elif not(storyi_prison_location in [4, 6, 7, 8, 9, 13]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_barracks
    elif _return == "Dung":
        if storyi_prison_location == 6:
            "The entrance to the dungeon."
            jump storyi_map
        elif not(storyi_prison_location in [4, 5, 7]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_dungentr
    elif _return == "Storage":
        if storyi_prison_location == 7:
            "A small storage filled with old armor ans household accessories."
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
        elif not(storyi_prison_location in [10, 5, 11, 12]):
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
        elif not(storyi_prison_location in [9, 5, 12]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_wroom
    elif _return == "CRoom":
        if storyi_prison_location == 12:
            "The dinning hall. Here slaves prepare food for guards and prisoners."
            jump storyi_map
        elif not(storyi_prison_location in [10, 5, 11, 13]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_croom
    elif _return == "GRoom_1":
        if storyi_prison_location == 13:
            "Another small guard post."
            jump storyi_map
        elif not(storyi_prison_location in [12, 5]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_groom_1
    else:
        hide map_scroll
        hide blueprint
        hide expression point
        with dissolve
        show screen prison_break_controls
        while 1:
            $ result = ui.interact()
            
label prison_storyi_event_cell:
    $ storyi_prison_location = 1
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point
    show bg dungeoncell with q_dissolve
    jump storyi_map
            
label prison_storyi_event_prisonblock:
    $ storyi_prison_location = 2
    play events2 "events/prison_cell_door.mp3"
    call storyi_move_map_point
    show bg story prison with q_dissolve
    jump storyi_map
    
label prison_storyi_event_infirmary:
    $ storyi_prison_location = 3
    play events2 "events/door_open.mp3"
    call storyi_move_map_point
    show bg infirmary
    jump storyi_map
    
label prison_storyi_event_groom2:
    $ storyi_prison_location = 4
    call storyi_move_map_point
    show bg story prison_1
    jump storyi_map
    
label prison_storyi_event_dungentr:
    $ storyi_prison_location = 6
    call storyi_move_map_point
    show bg story d_entrance
    jump storyi_map
    
label prison_storyi_event_storage:
    $ storyi_prison_location = 7
    call storyi_move_map_point
    show bg story storage
    play events2 "events/door_open.mp3"
    jump storyi_map
            
label prison_storyi_event_barracks:
    $ storyi_prison_location = 5
    call storyi_move_map_point
    show bg story barracks
    play events2 "events/prison_cell_door.mp3"
    jump storyi_map
    
label prison_storyi_event_iroom:
    $ storyi_prison_location = 9
    call storyi_move_map_point
    show bg dungeoncell
    play events2 "events/prison_cell_door.mp3"
    jump storyi_map

label prison_storyi_event_mentrance:
    $ storyi_prison_location = 8
    call storyi_move_map_point
    show bg story prison_1
    play events2 "events/prison_cell_door.mp3"
    jump storyi_map
    
label prison_storyi_event_troom:
    $ storyi_prison_location = 10
    call storyi_move_map_point
    show bg dung_2
    play events2 "events/prison_cell_door.mp3"
    jump storyi_map

label prison_storyi_event_wroom:
    $ storyi_prison_location = 11
    call storyi_move_map_point
    show bg story weaponry
    play events2 "events/prison_cell_door.mp3"
    jump storyi_map
    
label prison_storyi_event_groom_1:
    $ storyi_prison_location = 13
    call storyi_move_map_point
    show bg story prison_1
    play events2 "events/prison_cell_door.mp3"
    jump storyi_map
    
label prison_storyi_event_croom:
    $ storyi_prison_location = 12
    call storyi_move_map_point
    show bg story dinning_hall
    play events2 "events/prison_cell_door.mp3"
    jump storyi_map