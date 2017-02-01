init:
    image map_scroll = ProportionalScale("content/events/StoryI/scroll.png", 900, 900)
    image blueprint = ProportionalScale("content/events/StoryI/blueprint.png", 660, 540)

init python:
    def eyewarp(x):
        return x**1.33
    eye_open = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=False, time_warp=eyewarp)
    eye_shut = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=True, time_warp=eyewarp)
    
    def storyi_randomfight():  # initiates fight with random enemy team
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

label storyi_start:
    stop music
    stop world fadeout 2.0
    scene black with dissolve
    show expression Text("Some time later", style="TisaOTM", align=(0.5, 0.33), size=40) as txt1:
        alpha 0
        linear 3.5 alpha 1.0
    pause 2.5
    hide txt1
    play world "Theme2.ogg" fadein 2.0 loop
    show bg dungeoncell with eye_open
    $ storyi_prison_location = 1
    $ storyi_prison_stage = 1
    "..."
    jump storyi_map
    
label storyi_map:
    show map_scroll at truecenter 
    show blueprint at truecenter
    with dissolve
    if storyi_prison_location == 1:
        show expression point at Transform(pos=(709, 188))
    elif storyi_prison_location == 2:
        show expression point at Transform(pos=(784, 240))
    elif storyi_prison_location == 3:
        show expression point at Transform(pos=(841, 187))
    elif storyi_prison_location == 4:
        show expression point at Transform(pos=(798, 318))
    elif storyi_prison_location == 6:
        show expression point at Transform(pos=(777, 456))
    elif storyi_prison_location == 7:
        show expression point at Transform(pos=(779, 512))
    elif storyi_prison_location == 5:
        show expression point at Transform(pos=(661, 341))
    elif storyi_prison_location == 8:
        show expression point at Transform(pos=(656, 502))
    elif storyi_prison_location == 9:
        show expression point at Transform(pos=(622, 150))
    elif storyi_prison_location == 10:
        show expression point at Transform(pos=(564, 124))
    elif storyi_prison_location == 11:
        show expression point at Transform(pos=(530, 438))
    elif storyi_prison_location == 12:
        show expression point at Transform(pos=(442, 343))
    elif storyi_prison_location == 13:
        show expression point at Transform(pos=(427, 262))
    call screen poly_matrix("library/events/StoryI/coordinates_1.json", show_exit_button=(1.0, 1.0))
    if _return == "Cell":
        "This is your former prison cell. Nothing interesting."
        jump storyi_map
    elif _return == "Prison":
        if storyi_prison_location == 2:
            "This is the prison block. There are many cells, but they are empty."
            jump storyi_map
        elif not(storyi_prison_location in [1, 3, 4]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_prisonblock
    elif _return == "Infirmary":
        if storyi_prison_location == 3:
            "This is prison infirmary. They store there a huge amount of medical supplies."
            jump storyi_map
        elif storyi_prison_location <> 2:
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_infirmary
    elif _return == "GRoom_2":
        if storyi_prison_location == 4:
            "This is a small guard post."
            jump storyi_map
        elif not(storyi_prison_location in [2, 5, 6]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_groom2
    elif _return == "Barracks":
        if storyi_prison_location == 5:
            "This is the main guards barracks. Most of prison guards are located here."
            jump storyi_map
        elif not(storyi_prison_location in [4, 6, 7, 8, 9, 13]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_barracks
    elif _return == "Dung":
        if storyi_prison_location == 6:
            "This is the entrance to prison dungeon. Most prisoners contained there."
            jump storyi_map
        elif not(storyi_prison_location in [4, 5, 7]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_dungentr
    elif _return == "Storage":
        if storyi_prison_location == 7:
            "It's a small storage filled with old armour ans household accessories."
            jump storyi_map
        elif not(storyi_prison_location in [6, 5]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_storage
    elif _return == "MEntrance":
        if storyi_prison_location == 8:
            "The main entrance to the prison. It's usually well guarded."
            jump storyi_map
        elif storyi_prison_location <> 5:
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_mentrance
    elif _return == "IRoom":
        if storyi_prison_location == 9:
            "This is the interrogation room for preliminary inquests."
            jump storyi_map
        elif not(storyi_prison_location in [10, 5, 11, 12]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_iroom
    elif _return == "TRoom":
        if storyi_prison_location == 10:
            "This is the torturing room. It has all kinds of devices, from vibrators and clamps to whips and scissors."
            jump storyi_map
        elif storyi_prison_location <> 9:
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_troom
    elif _return == "WRoom":
        if storyi_prison_location == 11:
            "This is the weaponry. It has a good selection of weapons, including the weapons confiscated from the prisoners."
            jump storyi_map
        elif not(storyi_prison_location in [9, 5, 12]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_wroom
    elif _return == "CRoom":
        if storyi_prison_location == 12:
            "This is the dinning hall. Here slaves prepare food for guards and prisoners."
            jump storyi_map
        elif not(storyi_prison_location in [10, 5, 11, 13]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_croom
    elif _return == "GRoom_1":
        if storyi_prison_location == 13:
            "This is another small guard post."
            jump storyi_map
        elif not(storyi_prison_location in [12, 5]):
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_groom_1
            
label prison_storyi_event_prisonblock:
    hide scroll
    hide blueprint
    hide expression point
    play events2 "events/prison_cell_door.mp3"
    show bg story prison with dissolve
    $ storyi_prison_location = 2
    jump storyi_map
    
label prison_storyi_event_infirmary:
    hide scroll
    hide blueprint
    hide expression point
    play events2 "events/door_open.mp3"
    show bg infirmary with dissolve
    $ storyi_prison_location = 3
    jump storyi_map
    
label prison_storyi_event_groom2:
    hide scroll
    hide blueprint
    hide expression point
    show bg story prison_1 with dissolve
    $ storyi_prison_location = 4
    jump storyi_map
    
label prison_storyi_event_dungentr:
    hide scroll
    hide blueprint
    hide expression point
    show bg story d_entrance with dissolve
    $ storyi_prison_location = 6
    jump storyi_map
    
label prison_storyi_event_storage:
    hide scroll
    hide blueprint
    hide expression point
    show bg story storage with dissolve
    $ storyi_prison_location = 7
    play events2 "events/door_open.mp3"
    jump storyi_map
            
label prison_storyi_event_barracks:
    hide scroll
    hide blueprint
    hide expression point
    show bg story barracks with dissolve
    play events2 "events/prison_cell_door.mp3"
    $ storyi_prison_location = 5
    jump storyi_map
    
label prison_storyi_event_iroom:
    hide scroll
    hide blueprint
    hide expression point
    show bg dungeoncell with dissolve
    play events2 "events/prison_cell_door.mp3"
    $ storyi_prison_location = 9
    jump storyi_map

label prison_storyi_event_mentrance:
    hide scroll
    hide blueprint
    hide expression point
    show bg story prison_1 with dissolve
    play events2 "events/prison_cell_door.mp3"
    $ storyi_prison_location = 8
    jump storyi_map
    
label prison_storyi_event_troom:
    hide scroll
    hide blueprint
    hide expression point
    show bg dung_2 with dissolve
    play events2 "events/prison_cell_door.mp3"
    $ storyi_prison_location = 10
    jump storyi_map

label prison_storyi_event_wroom:
    hide scroll
    hide blueprint
    hide expression point
    show bg story weaponry with dissolve
    play events2 "events/prison_cell_door.mp3"
    $ storyi_prison_location = 11
    jump storyi_map
    
label prison_storyi_event_groom_1:
    hide scroll
    hide blueprint
    hide expression point
    show bg story prison_1 with dissolve
    play events2 "events/prison_cell_door.mp3"
    $ storyi_prison_location = 13
    jump storyi_map
    
label prison_storyi_event_croom:
    hide scroll
    hide blueprint
    hide expression point
    show bg story dinning_hall with dissolve
    play events2 "events/prison_cell_door.mp3"
    $ storyi_prison_location = 12
    jump storyi_map