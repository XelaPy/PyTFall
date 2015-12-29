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
            mob = build_mob(id=choice(rand_mobs), level=randint(1, 2))
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
        your_team.add(k)
        for member in your_team:
            member.controller = BE_AI(member)
        # your_team.add(hero)
        store.battle = BE_Core(Image("content/gfx/bg/be/dungeon.jpg"), music="content/sfx/music/be/battle (14).ogg", start_sfx=get_random_image_dissolve(1.5), end_sfx=dissolve)
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
    

label prison_storyi_event:
    stop world
    stop music
    $ s = chars["Sakura"]
    $ i = chars["Ino_Yamanaka"]
    $ s_spr = chars["Sakura"].get_vnsprite()
    $ i_spr = chars["Ino_Yamanaka"].get_vnsprite()
    $ k = chars["Konan"]
    $ k_spr = chars["Konan"].get_vnsprite()
    $ g1 = npcs["black_guard"].say
    $ g1s = npcs["black_guard"].get_vnsprite()
    stop world fadeout 2.0
    scene black with dissolve
    show expression Text("Some time later", style="TisaOTM", align=(0.5, 0.33), size=40) as txt1:
        alpha 0
        linear 3.5 alpha 1.0
    pause 2.5
    hide txt1
    play world "Theme2.ogg" fadein 2.0 loop
    show bg dung_1 with eye_open
    # "When you slowly walked up, your weapon was gone, you hands were chained, and your head hurted as hell."
    # $ i = 1
    # while i == 1:
        # menu:
            # "Check you head":
                # "You carefully touch back of the head. Hair matted with dried blood. Your head is buzzing like a bell, you might have a concussion. Not good..."
            # "Check your pockets":
                # "Nothing. They are empty."
            # "Call someone":
                # "You need to find out what's going on. You begin to shout. Soon enough you hear footsteps"
                # $ i = 2
    # play events2 "events/prison_cell_door.mp3"
    # show expression g1s with dissolve
    # g1 "I'll say it only one time, prisoner. If you going make noise, there will be unpleasant consequences."
    # "A tall guard in heavy armor enters the cell."
    # "You trying to ask him what's going on, but he interupts you."
    # g1 "The execution will be held in two days, but it doesn't mean you have nothing to lose. Trust me, you don't want to meet our torturer. So keep quite."
    # hide expression g1s with dissolve
    # play events2 "events\prison_cell_door.mp3"
    # "What's going on? They want to execute you? You need to find a way to get out of here."
    # "There is not much you can do though... Your headache intensifies and you get dizzy. In such a condition you are not going anywhere."
    # "Reasoning that nothing can be done at this point, you lie down and close your eyes in hopes to get better after a small rest..."
    # scene black
    # with eye_shut
    # stop world fadeout 1.0
    # play events2 "be/throwing_attack_1.mp3"
    # g1 "Ugh!"
    # play events "events/body_fall.mp3"
    # play world "Theme2.ogg" fadein 2.0 loop
    # show bg dung_1 with eye_open
    # "Something's going on outside. You hear footsteps again, but much lighter than before."
    # play events2 "events\prison_cell_door.mp3"
    # show expression k_spr at center with dissolve
    # $ k.override_portrait("portrait", "indifferent")
    # k.say "We don't have much time, [hero.name]. I hope you can walk."
    # menu:
        # "Who are you?":
            # $ pass
        # "What's going on?":
            # $ pass
    # k.say "The Hidden Village found out that you need help in your mission. The head of the Village asked me to assist you. That's all."
    # k.say "...You can call me Konan."
    # "Staggering and holding onto the wall, you however managed to stand up."
    # k.say "Good. Let's go."
    $ storyi_prison_location = 1
    $ storyi_prison_stage = 1
    # "She gives you a carelessly drawn map."
    # k.say "This dungeon used to be slaves training ground before the riot. They use it as a prison now, but blueprints are still the same."
    $ k_is_here = True
    $ sol_is_here = 0
    $ storyi_disguise = False
    jump storyi_map
    
label storyi_map:
    show scroll at truecenter 
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
        if k_is_here and storyi_prison_location <> 1:
            $ k.override_portrait("portrait", "happy")
            k.say "Hm? You want to return to your cell? Should I lock you there?"
            $ k.override_portrait("portrait", "indifferent")
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
        # elif storyi_prison_stage == 2:
            # k.say "Are you ready? There will be guards for sure. We will have to fight."
            # menu:
                # "Yes":
                    # jump prison_storyi_event_groom2
                # "No":
                    # jump storyi_map
        else:
            jump prison_storyi_event_groom2
    elif _return == "Barracks":
        if storyi_prison_location == 5:
            "This is the main guards barracks. Most of prison guards are located here."
            jump storyi_map
        elif not(storyi_prison_location in [4, 6, 7, 8, 9, 13]):
            "You are too far to go there."
            jump storyi_map
        # elif storyi_prison_stage <= 3:
            # k.say "Not there. It's the main barracks, I've already been there."
            # jump storyi_map
        else:
            jump prison_storyi_event_barracks
    elif _return == "Dung":
        if storyi_prison_location == 6:
            "This is the entrance to prison dungeon. Most prisoners contained there."
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
    # if storyi_prison_stage == 1:
        # k.say "This is the prison block. They keep here prisoners that should be executed or interrogated soon. The rest kept in dungeon."
        # menu:
            # "Do you know where Ino and Sakura?":
                # k.say "I was hoping I can find them here, but other cells are empty. We need to keep looking."
            # "Let's go.":
                # k.say "Stay behing me if there will be troubles. I don't think you can fight well in your condition."
        # k.say "There should be infirmary nearby if you wish to treat your wounds."
        # $ storyi_prison_stage = 2
    jump storyi_map
    
label prison_storyi_event_infirmary:
    hide scroll
    hide blueprint
    hide expression point
    play events2 "events/door_open.mp3"
    show bg infirmary with dissolve
    $ storyi_prison_location = 3
    # if k_is_here:
        # k.say "Go on, see what you can find. I'll watch for guards."
    # "You were able to find some medical supplies. Your condition was greatly improved."
    jump storyi_map
    
label prison_storyi_event_groom2:
    hide scroll
    hide blueprint
    hide expression point
    $ storyi_prison_location = 4
    # play events2 "events/prison_cell_door.mp3"
    # show bg story prison_1
    # if storyi_prison_stage == 2:
        # $ storyi_prison_stage = 3
        # enemy_soldier "What the ..? Who the hell are you?!"
        # $ enemy_team = Team(name="Enemy Team", max_size=1)
        # $ your_team = Team(name="Your Team", max_size=2)
        # $ mob_1 = build_mob("Infantryman", level=1)
        # $ enemy_team.add(mob_1)
        # $ your_team.add(k)
        # python:
            # for member in your_team:
                # member.controller = BE_AI(member)
        # $ your_team.add(hero)
        # $ battle = BE_Core(Image("content/gfx/bg/be/dungeon.jpg"), music="content/sfx/music/be/battle (14).ogg", start_sfx=get_random_image_dissolve(1.5), end_sfx=dissolve)
        # $ battle.teams.append(your_team)
        # $ battle.teams.append(enemy_team)
        # $ battle.start_battle()
        # $ your_team.reset_controller()
        # if battle.winner != your_team:
            # jump game_over
        # show bg story prison_1
        # play world "Theme2.ogg" fadein 2.0 loop
        # show expression k_spr at center with dissolve
        # k.say "We are done here."
    jump storyi_map
    
label prison_storyi_event_dungentr:
    hide scroll
    hide blueprint
    hide expression point
    show bg story prison with dissolve
    $ storyi_prison_location = 6
    # play events2 "events/prison_cell_door.mp3"
    # if storyi_prison_stage <= 3:
        # $ storyi_prison_stage = 4
        # $ k_is_here = False
        # k.say "Dungeons. This is where they keep most of the prisoners. We should look here too."
        # k.say "We have to split up here. I'll search the dungeon, you'll search this floor."
        # menu:
            # "Alright":
                # k.say "I'll find you later."
            # "This is a bad idea":
                # $ k.override_portrait("portrait", "happy")
                # k.say "You can return to your cell and wait for my return. But it won't help Sakura and Ino."
                # $ k.override_portrait("portrait", "indifferent")
        # k.say "Well, be careful."
        # play events2 "events/prison_cell_door.mp3"
        # hide expression k_spr with dissolve
        # "She left. Now you are on your own."
    jump storyi_map
    
label prison_storyi_event_storage:
    hide scroll
    hide blueprint
    hide expression point
    show bg story storage with dissolve
    $ storyi_prison_location = 7
    # play events2 "events/door_open.mp3"
    # menu:
        # "Look around":
            # if storyi_prison_stage <= 4 and storyi_disguise == False:
                # "After rummaging in closets, you found an old set of armour. It's too old and heavy to be helpful in battle, but it will be a great disguise."
                # "Equip it?" 
                # menu:
                    # "Yes":
                        # "You equip the armour."
                        # $ storyi_disguise = True
                    # "No":
                        # $ pass
                # jump storyi_map
            # else:
                # "There is nothing useful."
        # "Keep going":
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
    show bg prison_1 with dissolve
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
    show bg storage with dissolve
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