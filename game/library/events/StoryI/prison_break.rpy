init python:
    def eyewarp(x):
        return x**1.33
    eye_open = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=False, time_warp=eyewarp)
    eye_shut = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=True, time_warp=eyewarp)
init:
    $ point = "content/gfx/interface/icons/move15.png"
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
    $ storyi_prison = 1
    "She gives you a carelessly drawn map."
    k.say "This dungeon used to be slaves training ground before the riot. They use it as a prison now, but blueprints are still the same."
    jump storyi_map
    
label storyi_map:
    show scroll at truecenter with dissolve
    show blueprint at truecenter with dissolve
    if storyi_prison == 1:
        show expression point at Transform(pos=(709, 188))
    call screen poly_matrix("library/events/StoryI/coordinates_1.json", show_exit_button=(1.0, 1.0))
