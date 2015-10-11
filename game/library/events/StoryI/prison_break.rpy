init python:
    def eyewarp(x):
        return x**1.33
    eye_open = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=False, time_warp=eyewarp)
    eye_shut = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=True, time_warp=eyewarp)
init:
    $ point = "content/gfx/interface/icons/move15.png"
    $ enemy_soldier = Character("Guard", color=white, what_color=white, show_two_window=True, show_side_image=ProportionalScale("content/npc/mobs/ct1.png", 120, 120))
label intro_story:
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
    "When you slowly walked up, your weapon was gone, you hands were chained, and your head hurted as hell."
    label prison_eventi_actions_1:
    menu:
        "Check you head":
            "You carefully touch back of the head. Hair matted with dried blood. Your head is buzzing like a bell, you might have a concussion. Not good..."
            jump prison_eventi_actions_1
        "Check your pockets":
            "Nothing. They are empty."
            jump prison_eventi_actions_1
        "Call someone":
            "You need to find out what's going on. You begin to shout. Soon enough you hear footsteps."
    play events2 "events/prison_cell_door.mp3"
    show expression g1s with dissolve
    g1 "I'll say it only one time, prisoner. If you going make noise, there will be unpleasant consequences."
    "A tall guard in heavy armor enters the cell."
    "You trying to ask him what's going on, but he interupts you."
    g1 "The execution will be held in two days, but it doesn't mean you have nothing to lose. Trust me, you don't want to meet our torturer. So keep quite."
    hide expression g1s with dissolve
    play events2 "events\prison_cell_door.mp3"
    "What's going on? They want to execute you? You need to find a way to get out of here."
    "There is not much you can do though... Your headache intensifies and you get dizzy. In such a condition you are not going anywhere."
    "Reasoning that nothing can be done at this point, you lie down and close your eyes in hopes to get better after a small rest..."
    scene black
    with eye_shut
    stop world fadeout 1.0
    play events2 "be/throwing_attack_1.mp3"
    g1 "Ugh!"
    play events "events/body_fall.mp3"
    play world "Theme2.ogg" fadein 2.0 loop
    show bg dung_1 with eye_open
    "Something's going on outside. You hear footsteps again, but much lighter than before."
    play events2 "events\prison_cell_door.mp3"
    show expression k_spr at center with dissolve
    $ k.override_portrait("portrait", "indifferent")
    k.say "We don't have much time, [hero.name]. I hope you can walk."
    menu:
        "Who are you?":
            $ pass
        "What's going on?":
            $ pass
    k.say "The Hidden Village found out that you need help in your mission. The head of the Village asked me to assist you. That's all."
    k.say "...You can call me Konan."
    "Staggering and holding onto the wall, you however managed to stand up."
    k.say "Good. Let's go."
    $ storyi_prison_location = 1
    $ storyi_prison_stage = 1
    "She gives you a carelessly drawn map."
    k.say "This dungeon used to be slaves training ground before the riot. They use it as a prison now, but blueprints are still the same."
    $ k_is_here = True
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
        elif storyi_prison_location <> 1 and storyi_prison_location <> 3 and storyi_prison_location <> 4 and storyi_prison_location <> 5:
            "You are too far to go there."
            jump storyi_map
        else:
            jump prison_storyi_event_prisonblock
    elif _return == "Infirmary":
        if storyi_prison_location <> 2 and storyi_prison_location <> 3:
            "You are too far to go there."
            jump storyi_map
        elif storyi_prison_location == 3:
            "This is prison infirmary. They store there a huge amount of medical supplies."
        else:
            jump prison_storyi_event_infirmary
    elif _return == "GRoom_2":
        if storyi_prison_location == 4:
            "This is a small guard post."
            jump storyi_map
        elif storyi_prison_location <> 2 and storyi_prison_location <> 5:
            "You are too far to go there."
            jump storyi_map
        elif storyi_prison_stage == 2:
            k.say "Are you ready? There will be guards for sure. We will have to fight."
            menu:
                "Yes":
                    k.say "Good, let's go."
                    jump prison_storyi_event_groom2
                "No":
                    k.say "Be quick. The Village prefers to avoid drawing attention, we should do it quickly."
                    jump storyi_map
        else:
            jump prison_storyi_event_groom2
        
label prison_storyi_event_prisonblock:
    hide scroll
    hide blueprint
    hide expression point
    play events2 "events/prison_cell_door.mp3"
    show bg story prison with dissolve
    $ storyi_prison_location = 2
    if storyi_prison_stage == 1:
        k.say "This is the prison block. They keep here prisoners that should be executed or interrogated soon. The rest kept in dungeon."
        menu:
            "Do you know where Ino and Sakura?":
                k.say "I was hoping I can find them here, but other cells are empty. We need to keep looking."
            "Let's go.":
                k.say "Stay behing me if there will be troubles. I don't think you can fight well in your condition."
        k.say "There should be infirmary nearby if you wish to treat your wounds."
        $ storyi_prison_stage = 2
    jump storyi_map
    
label prison_storyi_event_infirmary:
    hide scroll
    hide blueprint
    hide expression point
    play events2 "events/door_open.mp3"
    show bg infirmary with dissolve
    $ storyi_prison_location = 3
    if k_is_here:
        k.say "Go on, see what you can find. I'll watch for guards."
    "You were able to find some medical supplies. Your condition was greatly improved."
    jump storyi_map
    
label prison_storyi_event_groom2:
    hide scroll
    hide blueprint
    hide expression point
    $ storyi_prison_location = 4
    play events2 "events/prison_cell_door.mp3"
    show bg story prison_1
    if storyi_prison_stage == 2:
        $ storyi_prison_stage = 3
        enemy_soldier "What the ..? Who the hell are you?!"
        $ k.override_portrait("portrait", "angry")
        k.say "We are angels of death!"
        $ k.override_portrait("portrait", "indifferent")
        "...What?"
        scene black
        $ enemy_team = Team(name="Enemy Team", max_size=1)
        $ your_team = Team(name="Your Team", max_size=2)
        $ mob_1 = build_mob("Infantryman", level=1)
        $ enemy_team.add(mob_1)
        $ your_team.add(k)
        python:
            for member in your_team:
                member.controller = BE_AI(member)
        # $ your_team.add(hero)
        $ battle = BE_Core(Image("content/gfx/bg/be/dungeon.jpg"), music="content/sfx/music/be/battle (14).ogg", start_sfx=get_random_image_dissolve(1.5), end_sfx=dissolve)
        $ battle.teams.append(your_team)
        $ battle.teams.append(enemy_team)
        $ battle.start_battle()
        $ your_team.reset_controller()
        if battle.winner != your_team:
            jump game_over
        show bg story prison_1
        play world "Theme2.ogg" fadein 2.0 loop
        show expression k_spr at center with dissolve
        k.say "We are done here."
        menu:
            "...angels of death?":
                $ k.override_portrait("portrait", "shy")
                k.say "Never mind that. Let's go."
                $ k.override_portrait("portrait", "indifferent")
            "Let's go.":
                $ pass
    jump storyi_map