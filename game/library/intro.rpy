init python:
    """
    init phase is initiation phase that is used to declare constant stuff. At most, you will be defining images in it and using it to create events/quest and their conditions! There will be examples of that in different files.
    This file is the first you should read if you wish to get into written/story development of PyTFall as it contains all the basics.
    play music "path/file.ogg"
    Transform("path/img.png", zoom=-1)
    show image_tag:
    pos (100, 100)
    show image_tag at Transform(pos=(100, 100)) with move
    This is a way to leave a long, multiline comment in Python and Ren'Py.
    show tag:
    yalign 1.0
    xpos 100

    show layer master at damage_shake(0.05, (-10, 10))
    pause 2.0
    show layer master
    There is a very detailed Ren'Py and (far more complicated) Python documentation avalible if you want to learn about something in greater detail.
    Ren'Py comes with a number of script languages. Python is the main one, everything can be done with it but it often requires a long and complicated code.
    That's why other script languages were created as wrappers around it:
    
    **Python:
    Everrything that starts with:
    $
    or
    python:
    
    1) Ren'Py Script: It's evething you see in .rpy files that is not declared as being something else.
    *Examples:
    label
    show
    menu
    image
    define
    and so on.
    
    2) Screen Language (short: SL (Ren'Py in 6.18 was updated to Screen Language 2))
    Screens are used to diplay information to the players and enable any interaction that is not anticipated in default Ren'Py (Anything more than default VN capabilities basically)
    evething that comes after:
    screen my_screen:
        # Screen Language statements
    
    3) ATL (Animation and Transformation Language). 
    Used to move displayable, zoom, crop, rotate and so on.
    Examples:
    transform my_transform:
        # Transformation instructions
    image my_image:
        # Transformation instructions
    
    4) Style Script:
    This is used to create styles and customise the displyable.
    style my_syle:
        # style statements
    
    ===
    init: (initiation phase, it runs every time Ren'Py game is launched from the OS) should be mensioned as well.
    """
    
init:
    image terumi normal = ProportionalScale("content/events/Intro/terumi.png", 1700, 500)
    image carstein = ProportionalScale("content/events/Intro/Eric Carstein.png", 1700, 500)
    image bag = ProportionalScale("content/items/quest/bag.png", 150, 150)
    image clocks = ProportionalScale("content/items/quest/cl2.png", 150, 150)
    image letter = ProportionalScale("content/items/quest/letter.png", 150, 150)
    image box = ProportionalScale("content/items/quest/box.png", 150, 150)
    image imag = ProportionalScale("content/events/Intro/imag.png", 1600, 400)
    image sakura_rape = ProportionalScale("content/events/Intro/sakura_rape.jpg", 1133, 850)
    image terumi reversed = Transform(ProportionalScale("content/events/Intro/terumi.png", 1600, 400), xzoom=-1)
    image sinstar = FilmStrip('content/events/Intro/sinstar.png', (192, 192), (5, 6), 0.1, loop=True)
    image skystar = FilmStrip('content/events/Intro/skystar.png', (100, 100), (2, 1), 0.3, loop=True)
    image teleport = FilmStrip('content/events/Intro/Teleport.png', (256, 256), (4, 4), 0.1, loop=False)
    image timestop = FilmStrip('content/events/Intro/time_stop.png', (800, 800), (24, 1), 0.1, loop=False)
    image bg slq = im.Scale("content/events/Intro/slq.jpg", config.screen_width, config.screen_height)
    image bg firetome = im.Scale("content/events/Intro/firetome.jpg", config.screen_width, config.screen_height)
    image bg war = im.Scale("content/events/Intro/war.jpg", config.screen_width, config.screen_height)
    image bg ash1 = im.Scale("content/events/Intro/ash1.jpg", config.screen_width, config.screen_height)
    image bg ash2 = im.Scale("content/events/Intro/ash2.jpg", config.screen_width, config.screen_height)
    image bg dun = im.Scale("content/events/Intro/dungeon.jpg", config.screen_width, config.screen_height)
    image bg fcity = im.Scale("content/events/Intro/fire_city.jpg", config.screen_width, config.screen_height)
    image bg wh = im.Scale("content/events/Intro/wh.jpg", config.screen_width, config.screen_height)
    image bg p1 = im.Scale("content/events/Intro/p1.jpg", config.screen_width, config.screen_height)
    image bg p2 = im.Scale("content/events/Intro/p2.jpg", config.screen_width, config.screen_height)
    image bg p3 = im.Scale("content/events/Intro/p3.jpg", config.screen_width, config.screen_height)
    image bg p4 = im.Scale("content/events/Intro/p4.jpg", config.screen_width, config.screen_height)
    image bg sky1 = im.Scale("content/events/Intro/sky1.jpg", config.screen_width, config.screen_height)
    image bg sky2 = im.Scale("content/events/Intro/sky2.jpg", config.screen_width, config.screen_height)
    image bg sky3 = im.Scale("content/events/Intro/sky3.jpg", config.screen_width, config.screen_height)
    image bg ruin1 = im.Scale("content/events/Intro/ruin1.jpg", config.screen_width, config.screen_height)
    image bg ruin2 = im.Scale("content/events/Intro/ruin2.jpg", config.screen_width, config.screen_height)
    image logo = ProportionalScale("content/events/Intro/logo-transperent.png", 600, 300)
    image cat = ProportionalScale("content/events/Intro/cat.png", 1100, 350)
    image girl = ProportionalScale("content/events/Intro/girl.png", 1300, 400)
    image priest = ProportionalScale("content/events/Intro/priest.png", 1300, 400)
    image soldier1 = ProportionalScale("content/events/Intro/soldier.png", 1800, 550)
    image soldier1 kaputt = HitlerKaputt(ProportionalScale("content/events/Intro/soldier.png", 1300, 400), 50)
    image tergr = ProportionalScale("content/events/Intro/tergr.png", 1700, 500)
    image he = ProportionalScale("content/events/Intro/h1.png", 1750, 550)
    image hes = ProportionalScale("content/events/Intro/he1.png", 1750, 550)
    $ flash = Fade(.75, 0.25, .75, color=darkred)
    $ sflash = Fade(.25, 0, .25, color=darkred)
    $ noisedissolve = ImageDissolve(im.Tile("content/events/Intro/noisetile.png"), 1.0, 1)
    
    transform star:
        subpixel True
        parallel:
            repeated_rotate(t=0.1)
    
label intro:
    stop world
    stop music

    scene black
    
    #show sinstar:
    #    pos (100, 100)
    #    alpha 0
    #    linear 1.0 alpha 1.0
    #    star
    #show sinstar at Transform(pos=(500, 500)) with move:
    #    alpha 0
    #    linear 1.0 alpha 1.0
    #    star
    # play music "content/sfx/music/intro-1.mp3"
    
    show expression Text("Mundiga continent", style="tisa_otm", align=(0.5, 0.33), size=40) as txt1:
        alpha 0
        linear 3.5 alpha 1.0
    show expression Text("3596 AD", style="tisa_otm", align=(0.5, 0.66), size=35) as txt2:
        alpha 0
        1
        linear 3.5 alpha 1.0
    pause 4
    hide txt1
    hide txt2
    with dissolve
    
    play music "content/sfx/music/intro-1.mp3" fadein 2.0 fadeout 2.0
    "Through trade and seemingly endless supply of slaves from the City of Crossgate, which grew from a small provincial city into the SlaveTrade capital of the world in a matter of years, many new city states arose."
    
    show bg humans with dissolve
    "One of them is PyTFall, a relatevely small town in neutral lands on the border of the Median Empire."
    
    show bg city_jail with dissolve
    "It was a time when slaves had less rights than pets..."
    extend " They were severely punished and could executed on spot by their masters without reprecussions for the slightest infraction."
    
    show bg slq with dissolve
    "Cruelty and lust for power of the Masters knew no bounds and they carelessly kept breeding and buying more and more slaves..."
    extend " and soon found themselves outnumbered ten to one."
    
    "They say there were those who sympathized with the oppressed. Those who gave them weapons and magic to fight back. "
    show bg firetome with ImageDissolve("content/gfx/masks/m21.jpg", 2)
    extend "To resist!"

    show bg war with dissolve
    "Riots happened one after the other. It is easy to take up arms when you have nothing to lose."
    "First few incedents were violently suppresed by the Masters..."
    extend " but it was too late."
    "The conflict quickly turned into a full scale warfare."
    
    show bg p2 with dissolve:
        subpixel True
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        linear 30 crop (config.screen_width/2, config.screen_height/2, config.screen_width/8, 100)
    show he with dissolve:
        yalign 1.0 xpos 400
    "Out of nowhere a stranger appeared, claiming to be a historian."
    "He told the Master of underground sanctuary not too far from the city, where an ancient star slept."
    show bg ruin1 with dissolve:
        subpixel True
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        linear 30 crop (config.screen_width/2, config.screen_height/2, config.screen_width/8, 100)
    show hes with dissolve:
        xpos 400 yalign 1.0
    "A dreadful weapon, capable of unimaginable destruction"
    show bg ruin2 with dissolve:
        subpixel True
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        linear 30 crop (config.screen_width/2, config.screen_height/2, config.screen_width/32, 100)
    extend " and of crushing the rebels once and for all..."
    "Carrying magic powerful enough to build a new empire and maybe, even to surpass Crossgates wealth and fame!"
    
    show bg ruin2:
        linear 3 alpha 0
    show hes:
        linear 3 alpha 0
    $ renpy.pause (3.0, hard=True)
    play music "content/events/Intro/tremor.mp3" fadein 2.0 fadeout 2.0
    scene black with dissolve
    show bg humans with dissolve
    pause 1.0
    show layer master at damage_shake(0.05, (-10, 10))
    pause 2.0
    show layer master
    $ renpy.pause (1.0, hard=True)
    show bg sky1 with wipedown:
        alpha 0
        linear 2.0 alpha 1.0
    $ renpy.pause (1.0, hard=True)
    play music "content/sfx/music/intro-2.mp3" fadeout 2.0
    show bg sky2 with flash
    show layer master at damage_shake(0.05, (-10, 10))
    pause 2.0
    show layer master
    show bg sky2 with sflash
    pause 1.0
    show bg sky2 with sflash
    pause 1.0
    show bg sky3 with flash
    pause 1.0
    show bg sky3 with sflash
    pause 1.0
    show bg ash2 with wipeup:
        alpha 0
        linear 2.0 alpha 1.0
    pause 2.0
    show bg ash2:
        subpixel True
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        linear 10 crop (config.screen_width/2, config.screen_height/2, config.screen_width/16, config.screen_height/16)
    pause 5.0
    scene bg ash1 with dissolve:
        subpixel True
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        linear 10 crop (config.screen_width/2, config.screen_height/2, config.screen_width/16, config.screen_height/16)
    pause 0.5
    $ renpy.show("logo", at_list=[szoom(0.5, 2, 8), Transform(pos=(0.5, 0.75), subpixel=True)])
    $ renpy.with_statement(dissolve)
    pause 4.5
    return
    
init python:
    def eyewarp(x):
        return x**1.33
    eye_open = ImageDissolve("content/events/Intro/eye_blink.png", 1.5, ramplen=128, reverse=False, time_warp=eyewarp)
    eye_shut = ImageDissolve("content/events/Intro/eye_blink.png", 1.5, ramplen=128, reverse=True, time_warp=eyewarp)
    # image black:
        # Solid("#000")
    # image white:
        # Solid("#FFF")    
    
label intro_story1:
    
    $ b = Character("???", color=white, what_color=white, show_two_window=True, window_left_padding=230)
    $ t = Character("Terumi", color=green, what_color=green, show_two_window=True, show_side_image="content\events\Intro\pnterumi.png", window_left_padding=230)
    $ ec = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\Intro\EricpCarstein.png", window_left_padding=230)
    
    hide screen pyt_mainscreen
    scene black
    stop world
    stop music
    play music "content/sfx/music/events/Theme2.ogg" fadein 2.0 loop
    play events "events/night_forest.mp3" loop
    show expression Text("Story I", style="tisa_otm", align=(0.5, 0.33), size=40) as txt1:
        alpha 0
        linear 3.5 alpha 1.0
    show expression Text("Hidden from the eyes", style="tisa_otm", align=(0.5, 0.66), size=35) as txt2:
        alpha 0
        1
        linear 3.5 alpha 1.0
    pause 3.5
    hide txt1
    hide txt2
    with dissolve

    show skystar as star1 at truecenter with dissolve
    show skystar as star2 with dissolve:
        pos (100, 100)
    show skystar as star3 with dissolve:
        pos (200, 200)
    "Night quickly descended on the forest, you barely had time to set up camp before dark."
    show skystar as star4 with dissolve:
        pos (500, 250)
    show skystar as star5 with dissolve:
        pos (800, 350)
    "Stars in the sky began to light up."
    show skystar as star6 with dissolve:
        pos (850, 150)
    show skystar as star7 with dissolve:
        pos (250, 400)
    "The air is rapidly getting colder and you hurried to light a fire."
    show bg camp with wipeup
    "The last few days you've traveled with a caravan. It provided you protection and shelter, but it was a tough experience for an inexperienced traveler such as yourself."
    "So on the last day of the journey you said goodbye to your new acquaintances and put up a camp to rest a bit before arriving in the city."
    $ intro_past = False
    $ intro_mast = False
    label setup_intro_menu:
        menu:
            "You need a good rest, but you do not want to sleep yet. What do you want to do?"
        
            "Think about your recent past." if intro_past != True:
                "You spent last few years far from your hometown. Alone, with no family or money, you had to earn money at any cost."
                "Here we call MC setup screen where player selects stuff. We also equip everything that can be equipped after setup screen."
                $ intro_past = True
                jump setup_intro_menu
            "Check your travel bag.":
                show bag at center with dissolve 
                "You don't have much besides your equipment and money."
                label your_bag_intro:
                menu:
                    "Look at chronometer":
                        show clocks at truecenter with dissolve
                        play events2 "events/checking.wav"
                        "The chronometer left over from your father. Many offered to buy it, but it is dear to you as a memory."
                        "It looks very complex and even has a built-in calendar, but it does not work since you left the city."
                        hide clocks with dissolve
                        jump your_bag_intro
                    "Read letter":
                        show letter at truecenter with dissolve
                        "This is the first reason for your return. An unsigned letter sent a month ago."
                        play events2 "events/letter.mp3"
                        "'You have mortal enemies that will find you very soon. If you wish to live, come to Pytfall and find your father's grave.'"
                        "Quite ominous, but does not look like a threat."
                        hide letter with dissolve
                        jump your_bag_intro
                    "Check wooden box":
                        show box at truecenter with dissolve
                        play events2 "events/box.wav"
                        "This is a simple wooden box belonged to your father, and the second reason for your return. His notes are still here, but you have no clue what they mean."
                        "Papers covered with cryptic symbols and drawings that no one was able to decipher over the years."
                        hide box with dissolve
                        jump your_bag_intro
                    "Enough with bag.":
                        hide bag with dissolve
                        jump setup_intro_menu
            "Jerk off" if intro_past != False and intro_mast == False:
                "Nobody's here, might as well to. You unzip your pants."
                "..."
                "It's not going well. Night forest is not the best place for lewd thoughts, and you don't have any pictures too."
                b "Aaah!"
                "You hear someone's yelling in the forest nearby. Sounds pretty hot."
                menu:
                    "Perfect, just what you need. Continue.":
                        jump intro_cont_mast
                    "Looks like you have more interesting things to do.":
                        "You quickly pull the clothes back."
                        $ mast_while_attack = False
                        jump intro_begin_battle
            "Jerk off" if intro_past != True:
                if intro_mast == False:
                    "Nobody's here, might as well to. You unzip your pants."
                    "..."
                    "It's not going well. Night forest is not the best place for lewd thoughts, and you don't have any pictures too."
                    "Perhaps you should try your imagination?"
                    menu:
                        "Yes, it's too early to give up!":
                            label intro_during_mast:
                            "You trying to imagine something sexy."
                            if intro_mast == False:
                                show imag at center with noisedissolve 
                                "Ooohkey, a bit weird, but it will do. You continue your business, trying to focus on your new imaginary friend."
                                "..."
                                "Yeah, it's much better now! You finish your business, taking care not to extinguish the fire."
                                hide imag with noisedissolve
                                "Alright, done."
                                $ intro_mast = True
                                jump setup_intro_menu
                            else:
                                show imag at center with noisedissolve
                                "Somehow, she looks more scornful than before. Or maybe it's just your imagination?"
                                "Well then, let's get going. You unzip your pants and begin."
                                "..."
                                "It's going good enough."
                                b "Aaah!"
                                "Oh yes. You imagination is so good you can hear her moans now!"
                                b "Help! Somebo... Aah!"
                                hide imag with noisedissolve
                                "Oh, it's not your imagination. Someone yells in the forest nearby."
                                menu:
                                    "Moans are fine too. Continue.":
                                        "..."
                                        label intro_cont_mast:
                                        b "N-No! W-w-wait you... Ahh!"
                                        "That was a good one."
                                        b "Ahhhhh!"
                                        "Looks like you both are close."
                                        b "Ahhhhhhhh!♪"
                                        "You managed to come simultaneously, even at a distance. Nice."
                                        $ mast_while_attack = True
                                        "You quickly pull the clothes back."
                                        jump intro_begin_battle
                                    "Put on the pants would be a good start.":
                                        "You quickly pull the clothes back."
                                        $ mast_while_attack = False
                                        jump intro_begin_battle
                                
                        "Nah, better to not force it.":
                            "Well, there always will be another day for that if you won't find a girl soon."
                            jump setup_intro_menu
                else:
                    "You already did it. It takes some time to recover."
                    jump setup_intro_menu
            "Another round?" if intro_past != False and intro_mast == True:
                "It probably will be more difficult so soon, but we are not looking for easy ways."
                jump intro_during_mast
            "Go to sleep":
                if intro_past == True:
                    "It's about time. Tomorrow will be a tough day."
                    $ mast_while_attack = False
                    jump intro_back_to_story
                else:
                    "You don't want to."
                    jump setup_intro_menu
        label intro_back_to_story:
        scene black
        with eye_shut
        "You slowly sink to sleep."
            
        b "Aaah!"
        "Mmmm... Z-Z-Z"
        b "Help! Somebo... Aah!"
        show bg camp with eye_open
        label intro_begin_battle:
        "...Whatever it was, if you want to rest tonight, you need silence."
        "You leave the cozy camp heading into the night forest."
        stop music fadeout 2.0
        show bg night_forest with zoomin
        "As soon as you move away from the fire, the immediately forest becomes much less friendly. You belatedly remember about wolves and other predators of night."
        "You quickly return to the bonfire. That's right, wolves are supposed to be afraid of fire."
        show bg camp with slideawayleft
        "You light a small torch. Hopefully, it will deter animals."
        show bg night_forest with slideawayright
        "You carefully continue to move in the direction of sounds. You can no longer make out individual words, it is more like a soft moans."
        "Sounds become closer. There is a small clearing ahead..."
        stop events
        play music "content/sfx/music/be/battle (8).mp3" loop
        show sakura_rape at truecenter with zoomin
        "And you see a girl caught by forest tentacles!"
        "She tries to break free, but vines firmly hold her. One of the tentacles is already deep in her ass, and another one in close proximity to her pussy."
        if mast_while_attack == True:
            "You notice how heavily she breathes. She already came at least once. You don't have much time left."
        "She tries to say something, but you can only hear moans from her mouth."
        "Time to act quickly. If you won't stop it, her moans will prevent your sleep for the rest of the night."
        $ intro_war = False
        $ intro_mag = False
        label intro_attack_menu:
        menu:
            "Recall what do you know about forest tentacles.":
                "Forest tentacles are predators, so to speak. They don't eat meat, instead they consume... certain female human body fluids. They brought victims to orgasm over and over again, releasing a huge amount of aphrodisiac inside."
                "While it seems like a great experience at first sight, such loads quickly incapacitate the higher nervous system, turning victims into mindless sex slaves."
                "They also die quickly without tentacle's control, what makes them useless for slaves market."
                jump intro_attack_menu
            "<Warriors> Try to attack it." if intro_war != True:
                "You uncover your weapon, slide ahead and to strike at the congestion of vines."
                $ intro_war = True
                play sound "content/sfx/sound/be/scythe_attack.mp3"
                "You cut some of them, but the weapon gets stuck in the fleshy vines and cracks. The creature tries to attack back, and you quickly move away."
            "<Mages> Try to cast a spell." if intro_mag != True:
                "You focus, feeling rising energy inside your body. You take a step forward and raise your hand."
                play sound "content/sfx/sound/be/light1.mp3"
                "A flow of magic strikes from under your nail. It cuts off some vines, but not nearly enough."
                $ intro_mag = True
            "Try the torch":
                "You still have your torch in the left hand. Quickly taking aim, you throw it into the creature."
                "To your surprise, the creature quickly drew back."
        "It wasn't very effective, but you managed to distract the creature. It weakened the grip, and the girl managed to get her own weapon."
        play sound "content/sfx/sound/be/dagger_attack_1.mp3"
        pause 0.5
        play sound "content/sfx/sound/be/dagger_attack_1.mp3"
        "With fast and precise movements she cuts off remaining vines and frees herself. The creature produces frustrated sound and collapses."
        hide sakura_rape with dissolve
        stop music fadeout 2.0
    play music "content/sfx/music/events/Theme2.ogg" fadein 2.0 loop
    play events "events/night_forest.mp3" loop
    $ s = chars["Sakura"]
    $ s.override_portrait("portrait", "sad")
    s.say "T-turn back, I need to change my clothes quickly!"
    "That's right, her clothes are soaked with aphrodisiac as well. It's better to change them before it becomes worse."
    "Although it's too late to be modest after what you saw, but whatever..."
    "..."
    $ s.override_portrait("portrait", "shy")
    s.say "I'm done, thanks. My name is Sakura. Who are you?"
    $ sakspr = chars["Sakura"].get_vnsprite()
    show expression sakspr at center with dissolve
    "She tries to look calm, but you notice how quickly she breathes. You introduce yourself."
    s.say "I see, nice to meet you, [hero.name]. Thanks for your help."
    $ s.disposition += 200
    menu:
        "Be a gentleman. Offer to rest in your camp.":
            $ s.override_portrait("portrait", "happy")
            "She must be tired. You tell her about your camp nearby."
            s.say "<she looks a bit surprised, but happy> Oh, ok! I would like to have some rest indeed."
            $ s.disposition += 50
            $ intro_be_nice = True
        "There is no time to waste. Her ass is compromised already.":
            "You explain that her that her ass is full of aphrodisiac, and needs to be cleaned. You are willing to take the risk and help her."
            $ s.override_portrait("portrait", "shy")
            $ hero.anal += 10
            $ s.anal += 10
            s.say "<she immediately blushes> I-I understand that. I accept you proposition, but please be gentle."
            hide sakspr
            $ intro_be_nice = False
            show expression s.show("sex", "in pain", "uncertain", "outdoors", "suburb", "night", "2c anal", "partnerhidden", resize=(800, 600), type="first_default") as xxx at truecenter
            "She slowly turns around and bends down. You are already hard enough after seeing the raping scene, so you quickly go inside."
            $ s.override_portrait("portrait", "ecstatic")
            s.say "Ah..."
            "She feels very tight. It must be her first time, or rather second one, after the monster."
            "However, because of the aphrodisiac she feels nothing but pleasure, so things go very smoothly."
            "She does her best to keep quite, but soon enough begins to moan."
            s.say "Ah... Yeah, there..."
            "Soon you come, cleaning her ass with your improvised enema. She came three times at very least meanwhile."
            "Damn, this aphrodisiac is a powerful thing. You put your clothes on, feeling a bit numb. There is a chance that you was effected as well through her ass, but it shouldn't be as powerful for men."
            hide expression xxx with dissolve
            show expression sakspr at center with dissolve
            "You tell her about your camp nearby, and together you go there. She still blushes and avoids looking in your direction."
    show bg camp with slideawayleft
    $ s.override_portrait("portrait", "indifferent")
    if intro_be_nice == True:
        $ s.override_portrait("portrait", "happy")
        "With a grateful smile, she sits by the fire."
    else:
        $ s.override_portrait("portrait", "shy")
        "Still shy, she sits by the fire."
    label intro_sarura_diag:
    menu:
        "Ask about her":
            s.say "Um, you already know my name. I'm on a mission here. Sorry, I cannot say more."
            "Judging by her uniform, she is one of those infamous kunoichi, female assassins living outside cities."
            jump intro_sarura_diag
        "Ask for a new weapon" if intro_war == True:
            "You explain that you lost your weapon trying to save her."
            s.say "Alright. Here, take this."
            "She gives you a small sharp dagger."
            $ intro_war = False
            s.say "It's called kunai. I have a spare one, so you can take it."
            $ hero.add_item("Kunai")
            jump intro_sarura_diag
        "Wish her good night and go to sleep":
            "You are too exhausted to keep talking. You wish her good night and go to your tent."
            hide sakspr
            show bg tent with dissolve
    if intro_be_nice == True or mast_while_attack == True:
        "You are ready for bed when Sakura walks in. She avoids to look into your eyes, looking at your crotch instead."
        $ s.override_portrait("portrait", "shy")
        if intro_be_nice == True:
            s.say "Sorry to bother you. That thing poisoned me, I won't be able to sleep without some releasing."
        else:
            s.say "How should I say it... Well, thanks for your hard work, but we need to keep going. I won't be able to sleep without it."
        menu:
            "It can't be helped":
                s.say "Thanks. Please lay down then."
            "You really need some rest already":
                s.say "I'm sorry, but it's not a proposition."
                "She grabs you. You suddenly realise that she much stronger than you. Stronger than anyone you know."
                s.say "I need it. NOW."
        $ s.oral += 10
        hide sakspr
        $ s.restore_portrait()
        show expression s.show("sex", "confident", "suggestive", "indoors", "living", "bc blowjob", "partnerhidden", resize=(800, 600), type="first_default") as xxx at truecenter
        "The last thing you remember is how Sakura licks you while stimulating herself with her left hand. You slowly fall asleep."
    else:
        "You slowly fall asleep. It was a tough night. The last thing you remember is how Sakura walks in and lies on the other side of the tent."
    scene black
    with eye_shut
    hide xxx
    stop events
    stop music fadeout 2.0
    show expression Text("In the next morning", style="tisa_otm", align=(0.5, 0.33), size=40) as txt1:
        alpha 0
        linear 3.5 alpha 1.0
    pause 2.5
    hide txt1
    with dissolve
    play music "content/sfx/music/events/Theme3.ogg" fadein 2.0 loop
    show bg city_street_2 with dissolve
    $ sakspr = chars["Sakura"].get_vnsprite()
    show expression sakspr at center with dissolve
    "At the next morning together you quickly reached the city. Some bandits tried to rob you along the road, but your new companion quickly got rid of them."
    "She kept up the general conversation, but avoided to talk about the last night, probably pretending it never happened."
    "Ultimately, you part ways in the town square. She told you where you can find her in the city if something happens, but asked to not bother without a good reason, since she's on her mission."
    hide expression sakspr at center with dissolve
    "Well then, time to do your own mission."
label intro_story2:
    $ ec = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\Intro\EricpCarstein.png", window_left_padding=230)
    stop music fadeout 2.0
    scene black with dissolve
    play music "content/sfx/music/events/cemetery.ogg" fadein 2.0 loop
    show expression Text("City Cemetery", style="tisa_otm", align=(0.5, 0.33), size=40) as txt1:
        alpha 0
        linear 3.5 alpha 1.0
    pause 2.5
    hide txt1
    show bg cemetery with dissolve
    "You found the cemetery very soon with the help of local residents. It does not look abandoned, but you are almost alone here."
    "..."
    show bg cemetery_1 with dissolve
    show carstein at center with dissolve
    "On the very edge you see an old man standing next to a tombstone. Maybe he is the author of the letter? You come closer with caution."
    ec "Well hello there youngster."
    "His voice is low and raspy."
    ec "Not many people come to this place. Do you have some business with me?"
    $ cem = 0
    label cem_diag:
    menu:
        "Look at the tombstone next to him":
            "Nope, it's not your father. You can not make out the name, but the surname is 'Carstein'."
            jump cem_diag
        "Ask about the cemetery":
            ec "Ah yes, you see, after the riot there were too many dead bodies to bury, and we started to burn them." 
            ec "Over time it has become a tradition, and cemeteries are no longer used as before."
            ec "That's why not many people come here these days. <he glances at the tombstone nearby>"
            jump cem_diag
        "Ask what is he doing here":
            ec "<he laughs softly> The same thing as you, I presume. Pay tribute to the fallen."
            jump cem_diag
        "Ask about your father's grave":
            ec "Oh, so you are looking for HIM. I'm afraid he is not here. I don't know where he is. Maybe nobody knows."
            $ cem = 1
            jump cem_diag
        "Leave" if cem == 1:
            "You turning around, going to leave this place. Obviously, the letter was someone's joke."
            ec "But if you looking for anyone else, we can help each other. [hero.name]."
    ec "Allow me to introduce myself, boy. I am Eric Carstein, retired militia officer."
    ec "I used to know your father. Now I'm just a tired old man, but I still have some connections with military."
    label cem_diag1:
    menu:
        "Ask about the letter":
            ec "So, you got a letter too? In fact, I have a similar letter telling me to meet you here today."
            ec "I don't know who sent them. Handwriting analysis showed complete nonsense."
            jump cem_diag1
        "Ask about the papers of your father":
            ec "<he doesn't look interested> Ah yes, he used to work on something. I don't know what it was, and I don't want to know too."
            ec "I already know enough to sleep bad at night. <he winks at you> Let's not worsen the situation."
            jump cem_diag1
        "Ask about your father":
            ec "We were friends from childhood. Always wanted to make a military career."
            ec "And we both succeeded in killing people. I was on the battlefield, your father was in the laboratory."
            jump cem_diag1
        "Show him your letter":
            "You show him the letter you received two weeks ago. He carefully examines it for a minute or so."
            ec "It is the same handwriting, I'm sure of it. <he gazes at you> I don't know what is it about, but to be manipulated is never a good thing."
    ec "I will need some time to think about it. <he gives you a bag of coins> Here. Buy yourself a house. Find a job. Gather some money."
    menu:
        "Ohh, free money!":
            ec "<he frowns> I don't think so, youngster. I expect you to return them, with interest."
        "No charity is needed":
            ec "<He nods approvingly> It is not a charity. I expect you to return them, with interest."
    $ hero.gold+= 1000
    # Here we give a quest to buy a house and collect, let's say, 5000 gold and get to lvl 5. We will take 2000 when he will return the debt.
    ec "<he gives you address> This is where I live. Meet me there when you will be ready. Until then..."
    hide carstein with dissolve
    "He left. After a short while you go back to the city."
    stop music fadeout 2.0
    scene black with dissolve
label intro_story3:
    $ ec = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\Intro\EricpCarstein.png", window_left_padding=230)
    scene black with dissolve
    play music "content/sfx/music/events/Town5.ogg" fadein 2.0 loop
    show bg cab with dissolve
    show carstein at center with dissolve
    "You managed to settle a bit for the last days. You came to Carstein as he asked."
    ec "First thing's first. Do you have money?"
    "You gave him twice as much as he gave you."
    $ hero.gold -= 2000
    ec "Good, very good. During this time I learned something new. I'm not sure where to start... <he looks somewhat depressed>"
    "You sit on a luxury sofa. It's very comfortable and most likely worth more than your house."
    label last_carst:
    menu:
        "Ask about your father's grave":
            ec "Ah, you see, nobody knows where his body is. There are witnesses of his death, but no one saw what happened after."
            ec "At least no one alive in the city. <he grins slightly>"
            jump last_carst
        "Ask about the letter":
            ec "Nothing new here. It's the same papper, the same inks, the same handwriting."
            ec "But letters are identical to each other. Yet the force pressing the paper is different, so it shouldn't be written by a machine."
            ec "<sigh> ...Or at least my connections think so."
            jump last_carst
        "Ask about new clues":
            ec "Yes, yes. <he looks at you> Do you know what happened in 3596?"
            label last_carst1:
            menu:
                "My father died":
                    ec "Yes, indeed. A tragedy, but just one of many."
                    jump last_carst1
                "The city was wiped put":
                    ec "Close, but not truth. We lost a quarter of the city."
                    jump last_carst1
                "Slaves rebellion":
                    ec "Indeed, but they happened almost every year back then. It was a big one, perhaps the biggest one."
                    ec "<you are alone in the room, but he lowers his voice anyway> They say someone helped them. Someone gave them weapons and magic to fight back."
                    ec "But in the end they were manipulated by someone. The riot was a consequence, not a cause."
                    jump last_carst1
                "You tell me":
                    ec "<he makes a short laugh> I would if I could. The truth is that nobody knows what exactly happened. I spent years looking for witnesses and evidences."
                    ec "Unfortunately, the red flash that vaporized the army of slaves also destroyed most of the clues."
                    ec "And the user of the weapon lost his mind..."
    ec "But enough with history for today. I have an idea where we should start looking."
    ec "The weapon used during the riot was found in ruins not very far from the city. They say an itinerant historian came to the city and told us where to find it."
    ec "<sigh> And everything he said was true. The riot ended with a single flash. The city has grown and become rich."
    ec "And he never told us about the consequences for one who used it in the battle. So technically, he did not lie in anything."
    ec "<he frowns> And that's what scares me. Everyone lies, even if unintentionally. His instructions were absolutely accurate and correct."
    ec "I cannot attract any more attention. Therefore you have to send an expedition to the ruins where we found the weapon on your own."
    ec "This is the best clue I have. The information about its location is still classified, so most likely nobody was there after Terumi."
    ec "See if you can find something. Anything."
    "You get up to leave."
    ec "...And be careful."
    # And so we give a quest to find ruins deep in SE. When the group will return, MC will know that ruins were sealed by impenetrable stone wall.
    # At the wall there is the same symbol you saw at Sakura's equipment.
    scene black with dissolve
    stop music fadeout 2.0
    
label intro_story: # this label goes when MC goes to Sakura's house after it becomes available
    play music "content/sfx/music/events/Theme3.ogg" fadein 2.0 loop
    show bg city_street_2 with dissolve
    "Initially you didn't wanted to bother Sakura at all. Kunoichi are mortally dangerous and unpredictable, everyone knows it."
    "They say one kunoichi worth hundreds of soldiers."
    "But if someone knows how to remove the stone wall in the ruins, it's her. There is no doubt about it, her head protector has the same symbol as the wall."
    "And besides... She didn't looked so dangerous during your time 'together'. Maybe you can do it again, who knows?"
    show bg house with dissolve
    "According to your information, she rented a house outside the city."
    "Well then, time to act!"
    $ a = 0
    $ b = 0
    label sak_house:
    menu:
        "Knock the door":
            "That's right, better to warn her."
            play sound "content/sfx/sound/events/door_knock.mp3"
            "..."
            "No response. Damn."
            $ a = 1
            jump sak_house
        "Look through the window":
            "Unfortunately, curtains effectively prevent it. Too bad."
            jump sak_house
        "Try to open the door":
            "You trying to open the door..."
            play sound "content/sfx/sound/events/door_open.mp3"
            "...and it opens. Strange, why the door is not locked if nobody's home?"
            $ b = 1
            jump sak_house
        "Enter":
            "That's right, fortune favors the bold."
            if b == 0:  
                play sound "content/sfx/sound/events/door_open.mp3"
            if a == 1:
                "At least you always can say that you knocked."
            stop music fadeout 2.0
        "Leave" if a == 1:
            "It's unwise to enter at this point. You should leave."
            stop music fadeout 2.0
            "Something is wrong. At the corner of your eye you saw some movement outside."
            "Carstein warned you to be careful. At least Sakura might help you if someone will attack you."
            if b == 0:  
                play sound "content/sfx/sound/events/door_open.mp3"
    show bg livingroom with dissolve
    "Trying not to make noise, you go inside."
    "It looks like an ordinary living room. You are alone here. Maybe you should..."
    $ s = chars["Sakura"]
    $ i = chars["Ino_Yamanaka"]
    $ s_spr = chars["Sakura"].get_vnsprite()
    $ i_spr = chars["Ino_Yamanaka"].get_vnsprite()
    init:
        image bg sky1 = im.Scale("content/events/Intro/sky1.jpg", config.screen_width, config.screen_height)
    play music "content/sfx/music/events/Scene2.ogg" fadein 2.0 loop
    $ i.override_portrait("portrait", "angry")
    "You feel cold steel near your neck."
    i.say "You have 5 seconds to explain why are you here."
    "Oh crap."
    label ohcrap:
    menu:
        "I'm looking for Sakura":
            i.say "Really? Who are you? How do you know her?"
        "Please don't kill me.":
            i.say "It depends on who are you. I won't hesitate to kill a spy."
            jump ohcrap
        "Wrong door. I'm leaving already.":
            i.say "Oh no you don't! Move, and I'll kill you!"
            jump ohcrap
    "You trying to explain, but she interrupts you."
    i.say "I won't believe you anyway. But there is a way to find out for sure."
    "She removes the weapon from your throat."
    show expression i_spr at center with dissolve
    i.say "Like I said, if you move, I will kill you on spot. Now I'm going to use a special technique to find out who you are."
    stop music fadeout 2.0
    show black with noisedissolve 
    play sound "content/sfx/sound/be/darkness2.mp3"
    hide black with noisedissolve 
    "Suddenly you feel very dizzy. You body is heavy, you cannot move, and thoughts flow very slowly."
    "The girl concentrates, and you beginning to see scattered fragments of your past."
    "..."
    "After a while you realize that she's not very good at it. She tries to find your memories about Sakura, but she cannot control the flow of your memory well enough."
    play music "content/sfx/music/events/Field2.ogg" fadein 2.0 loop
    "Let's see what you can do."
    $ a = 0
    $ b = 0
    $ c = 0
    label ino_mind:
    menu:
        "Focus on jerking off" if a == 0:
            "That's right, if she wants to be in your head, there WILL be consequences!"
            "You recall how and where you did it."
            $ i.override_portrait("portrait", "shy")
            i.say "..."
            "She blushes, but not much. Maybe she masturbates even more often?"
            $ a = 1
            jump ino_mind
        "Remember your childhood" if b == 0:
            "Yes, it should work. You never felt sorry for yourself, but you realised that your childhood was pretty tough."
            $ i.override_portrait("portrait", "sad")
            i.say "..."
            "Good. If she empathizes you, she won't kill you. Probably."
            $ b = 1
            jump ino_mind
        "Remember the events of the riot" if c == 0:
            "You don't like to remember that part of your life. But currently you are not alone in your head, so..."
            $ c = 1
            $ i.override_portrait("portrait", "indifferent")
            show bg sky1 with noisedissolve
            i.say "..."
            "Yes, not every day you see how the sky is torn apart by the red flash."
            show bg livingroom with noisedissolve
            jump ino_mind
        "Focus on Sakura" if b == 1 and c == 1:
            "Okey, if she wants Sakura, you give her Sakura."
            "You recall the events of that night. How you set the camp. How you helped Sakura. And how you two..."
            $ i.override_portrait("portrait", "scared")
            stop music 
            i.say "Whaaat?!"
            
    i.say "Sakura... You... Together..."
    "You don't feel her presence inside your head any longer."
    play sound "content/sfx/sound/events/door_open.mp3"
    $ s.override_portrait("portrait", "confident")
    s.say "I'm home!"
    show expression s_spr at right with dissolve
    s.say "Oh? [hero.name]? What are you..."
    $ i.override_portrait("portrait", "angry")
    i.say "I can't believe you! So while I'm all alone here, you are d-dating like there's no tomorrow!"
    $ s.override_portrait("portrait", "angry")
    s.say "W-what? What are you talking about? I..."
    i.say "I SAW it in his head. Night, forest, you do 'it'."
    "That escalated quickly. You're wondering whether you should intervene or quickly and quietly leave."
    $ s.override_portrait("portrait", "defiant")
    s.say "Whaat? You used it on civilians again? Just wait until lady Tsunade will know about it..."
    i.say "Oh? So you think you can..."
    "That's it, time to go. You make a small step toward the door."
    s.say "You, stay right there!"
    i.say "Where do you think you going?!"
    "It can't be good..."
    show black with dissolve 
    pause 2.0
    play music "content/sfx/music/events/Theme3.ogg" fadein 2.0 loop
    hide black with dissolve
    $ i.override_portrait("portrait", "indifferent")
    $ s.override_portrait("portrait", "indifferent")
    "After they calmed, you finally managed to tell them why are you here."
    "They look at each other."
    i.say "That's... not something we can decide on our own."
    s.say "Right, if someone put a seal, there must be a reason. You probably should speak with someone from our village, but..."
    i.say "But outsiders are not permitted without approval of three ninjas. Too bad, your girlfriend Sakura is not enough for that."
    s.say "Be quite, you! She is right though, you cannot go there."
    $ s.override_portrait("portrait", "confident")
    "You ask her to deliver a letter to the village headman."
    s.say "Oh, alright. No promises though. They might just ignore you."
    s.say "I'll let you know if... when they answer. It may take several days."
    "You thank them and say goodbye."
    play sound "content/sfx/sound/events/door_open.mp3"
    hide expression s_spr
    hide expression i_spr
    show bg house with dissolve
    $ i.override_portrait("portrait", "angry")
    $ s.override_portrait("portrait", "angry")
    "Once beyond the threshold, you sigh. Deeply and with relief."
    i.say "What, no goodbye kiss?"
    s.say "That's it, you asked for that!"
    "You quickly increase the distance between you and the house."
    "If they won't answer to your letter, you need to get to the village in person. For that you will need approval of three ninjas."
    "Sakura most likely will cooperate. Even together with Ino it won't be enough, but two is better than one, right?" # here we give access to Ino in the house and give a quest to rise disposition to 300 and become her friend via interactions
    scene black with dissolve
    stop music
    
    
    pause
    # play music "content/sfx/music/fire-2.mp3" fadein 2.0 fadeout 2.0
    # scene bg fcity with dissolve
    # show terumi normal at left with dissolve
    # t "Ah, what a view! It certainly brings back memories."
    # t "They totally wrecked the shopping district! Marvelous!"
    # t "That's some impressive demonstration of power."
    # t "Will be even more pleasant to trample into the ground all that rebel scum."
    # show terumi normal:
        # linear 2.0 xpos 300
    # show priest:
        # xpos 1500
        # yalign 1.0
        # linear 2.0 xpos 900
    # pr "You late, Terumi! We expected you three days ago! Where the hell have you been?"
    # t "Well hello there, good sir! What can I help you with?"
    # pr "Silence! Since you are finally here, you ought to join our forces and crush rebels army once and for all!"
    # t "I feel like you have anger control problem. May I suggest you to go drink some juice maybe? I have urgent business."
    # show priest:
        # linear 0.1 yoffset 4
        # linear 0.1 yoffset 0
        # repeat 2
    # pr "How dare you! I command you! I..."
    # t "Oh, but no worries. It is easy to fix."
    # show terumi normal:
        # linear 0.1 xpos 900
    # play sound "content/sfx/sound/be/scythe_attack.mp3"
    # pr "..!"
    # show priest:
      # linear 1.1 yoffset 300
      # linear 1.0 alpha 0
    # play sound "content/sfx/sound/be/body_fall.mp3"
    # t "See? You are not angry now. And you command nothing either."
    # t "Ah, the day keeps getting better and better!"
    # show terumi normal:
        # linear 2.0 xpos 1800
    # stop music fadeout 2.0
    # scene black with dissolve
    # stop music
    # play music "content/sfx/music/Explosions.mp3" fadein 2.0 fadeout 2.0
    # scene bg wh with dissolve
    # show girl:
        # xpos 300
        # yalign 1.0
    # show boy at left
    # pause 0.3
    # play sound "content/events/Intro/tel.wav"
    # show cat:
        # alpha 0
        # xpos 800
        # yalign 1.0
        # linear 1.0 alpha 1
    # show teleport:
        # alpha 1
        # xpos 720
        # zoom 1.5
        # yalign 1.0
        # linear 2.0 alpha 0
    # g "Master!"
    # c "Yo. What's up with that kiddo?"
    # b "I'm not a kiddo!"
    # g "Oh, I'm sorry. I picked up him on my way here. He lost his parants, and..."
    # c "I see, I see. Well, finders keepers. Did ya get the package?"
    # g "Yes. Here."
    # show girl:
        # linear 1.5 xpos 500
    # c "Good, good. Now I want ya to remember how to make it work. See, ya move this part there, and there, and then stick it here."
    # g "I see. What should I do now?"
    # c "Ya take this little brat and go to the temple. I have some stuff to check."
    # g "You can't possibly mean..."
    # c "I still might have a chance to affect his time. And even if I don't... "
    # c "I have to make sure that ya guys have enough time. I'll meet ya in the temple."
    # show girl:
        # linear 0.1 yoffset 4
        # linear 0.1 yoffset 0
    # g "...I understand. Just be careful, Master."
    # c "Ya heard me, brat? You should go with this miss and protect her along the road. She can't do it without ya help."
    # b "*blush* I-I will p-protect her. And stop calling me brat, you strange suspicious cat person!"
    # c "Can't hear ya, kiddo!"
    # play sound "content/events/Intro/tel.wav"
    # show teleport:
        # alpha 1
        # xpos 720
        # zoom 1.5
        # yalign 1.0
        # linear 2.0 alpha 0
    # show cat:
        # linear 1.0 alpha 0
    # pause 1
    # scene black with dissolve
    # play music "content/sfx/music/intro-1.mp3" fadein 2.0 fadeout 2.0

    # play music "content/sfx/music/Explosions.mp3" fadein 2.0 fadeout 2.0
    # scene black with dissolve
    # show bg p1 with dissolve
    # show soldier1 at right
    # show terumi normal:
        # xpos -600 yalign 1.0
        # linear 2.1 xpos 50
    # s1 "Yuki Terumi. Who would have thought."
    # t "Yes sir master sir! Ready to report, captain sir master chief sir!"
    # s1 "If you looking for Council, they were evacuated this morning. There is nothing for you here."
    # t "I beg to differ. I heard they also evacuated all valuable staff and stuff. I came to look at the collection of the biggest losers in the city."
    # s1 "..."
    # t "*sigh* No fun, as usual."
    # play sound "content/events/Intro/exp.mp3"
    # show layer master:
        # linear 0.1 yoffset 5
        # linear 0.1 yoffset 0
        # repeat 5
    # show terumi normal:
        # linear 0.1 yoffset 4
        # linear 0.1 yoffset 0
    # t "Holy shit! Did you heard that? Sounds like they aim at the Palace Tower now. What a crazy idea!"
    # s1 "Then perhaps you should leave."
    # t "Oh, I will. I just want to take a stroll, real quick. May I?"
    # s1 "I don't have an authority to stop a captain of Intelligence Department. Even I want to."
    # t "Congratulations! You will live another day! If rebels don't kill you, of course."
    # show terumi normal:
        # linear 1.0 xpos 300
        # linear 1.0 alpha 0
    # s1 "..."
    # scene black with dissolve
    # show bg p2 with dissolve
    # show terumi normal with dissolve:
        # xpos 300
        # yalign 1.0
    # play music "content/sfx/music/intro-1.mp3" fadein 2.0 fadeout 2.0
    # play sound "content/events/Intro/tel.wav"
    # show cat:
        # alpha 0
        # xpos 800
        # yalign 1.0
        # linear 1.0 alpha 1
    # show teleport:
        # alpha 1
        # xpos 720
        # zoom 1.5
        # yalign 1.0
        # linear 2.0 alpha 0
    # t "Ugh. I was expecting you, but the stench of cat hair still took me by surprise."
    # c "Terumi. I'll tell this only once..."
    # t "They say you can see the future. Not you personally, I actually doubt it. But some of you people, who live in the Temple of Time."
    # c "..."
    # t "But I, as the captain of Intelligence Department, can see the present and the past. I know everything about you."
    # t "I know about your excavations in Crossgate. I know about your little cute helper. Damn, I even know the color of your underwear today, though I wish I didn't."
    # t "I know that you supported slaves rebelion all this time. I even know that the device will take the life of the one who activated it."
    # c "..."
    # t "Ah, you are not surprised. Such a good master you are for your slave. Not so different from me, eh?"
    # t "I know that you afraid Sinister Star. I know..."
    # show cat:
        # linear 0.1 yoffset 4
        # linear 0.1 yoffset 0
        # repeat 2
    # c "Itakebackallyourtimebythenameofeternity!"
    # play sound "content/events/Intro/clock.mp3"
    # show timestop:
        # linear 1.5 alpha 0
        # xpos 400
        # yalign 1.0
    # show tergr with dissolve:
        # xpos 300
        # yalign 1.0 
    # c "Wow. Ya big mouth really made it easy, mate. I had all time in the world to make the spell."
    # stop music
    # c "Told ya. You don't follow orders, I take your time back."
    # play music "content/events/Intro/tremor.mp3" fadein 2.0 fadeout 2.0
    # show sinstar:
        # pos (100, 100)
        # anchor (0.5, 0.5)
        # alpha 0
        # subpixel True
        
        # parallel:
            # linear 2.0 alpha 1.0
        # parallel:
            # linear 4.0 pos (800, 600)
        # parallel:
            # 1.0
            # block:
                # rotate 0
                # linear 0.1 rotate 360
            # repeat
        # parallel:
            # block:
                # linear 1.0 zoom 3.0
                # linear 1.0 zoom 1.0
            # repeat
                
                
    # pause    


    # show terumi normal at left
    # with dissolve
    # "Now the reversed version..."
    
    # show terumi reversed at right with move
    
    # "HOWEVER, Do note that it was never require to declare a reverced character at all!"
    # hide terumi
    # show terumi normal at left with dissolve
    
    # "Now... we do not show the reversed image we've declared, it's useless if we use ATL:"
    
    # show terumi normal at right with move:
        # xzoom -1
        # This is one of the ways to use ATL, you can have the image rotating, changing shape and size, flying around the screen, changing alpha and anything like that.
    # $ npc1 = Character("Terumi", color=green, what_color=green, show_two_window=True, show_side_image="content\events\Intro\pnterumi.png", window_left_padding=230)
    # npc1 "Meow!"
    # t "Or not?"
    # "Note that all the good stuff is written as comments in examples.rpy file and you will not be able to see it from the game!"
    # "There is also a very good tutorial availible if you download Ren'Py SDK kit (less than 30 MB and does not require instalation)!"
    # "You should get SDK if you want to develop content for PyTFall. It's not really a 'MUST HAVE' but it's most definetly a should have :)'"
    # "There will be a great demonstration tutorial there of what the engine is capable of! This shows similar things but those that are more relevant to {color=[red]}PyTFall{/color}!"
    # {color=[red]}Text{/color} changes something about text styling! You can use a lot here... like {b}Text{/b} will write text in bold!
    # You can check all properties by googling RenPy + Text + Style + Properties
    
    # return
