init python:
    def eyewarp(x):
        return x**1.33
    eye_open = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=False, time_warp=eyewarp)
    eye_shut = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=True, time_warp=eyewarp)
    
init:
    image electricity_1 = FilmStrip('content/gfx/be/filmstrips/electricity_1.png', (192, 192), (5, 2), 0.1, loop=False)
    image skystar = FilmStrip('content/events/StoryI/skystar.png', (100, 100), (2, 1), 0.3, loop=True)
    $ noisedissolve = ImageDissolve(im.Tile("content/events/StoryI/noisetile.png"), 1.0, 1)
    image imag = ProportionalScale("content/events/StoryI/imag.png", 1600, 400)
    image sakura_rape = ProportionalScale("content/events/StoryI/sakura_rape.jpg", 1133, 850)
    image bag = ProportionalScale("content/items/quest/bag.png", 150, 150)
    image clocks = ProportionalScale("content/items/quest/cl2.png", 150, 150)
    image letter = ProportionalScale("content/items/quest/letter.png", 150, 150)
    image box = ProportionalScale("content/items/quest/box.png", 150, 150)
    
label intro_story:
    $ b = Character("???", color=white, what_color=white, show_two_window=True)
    hide screen pyt_mainscreen
    scene black
    stop world
    stop music
    $ s = chars["Sakura"]
    $ s.override_portrait("portrait", "sad")
    play world "Theme2.ogg" fadein 2.0 loop
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
        menu:
            "You hear screams nearby."
        
            "Too bad, you are not a white knight":
                "Yawning, you close your eyes. It's unwise to wander through the forest at night."
                scene black
                with eye_shut
                "Maybe in the morning you will check what was going on there... Z-Z-Z"
                b "Ahhhhh! N-n... AAAAH!"
                show bg camp with eye_open
                "Agh, for hell's sake! Do they do it on purpose or something? It's too loud to sleep, you need to stop it an once."
            "Sounds sexy, check it up!":
                "Judging by sounds, it's worth it to have a look. You bet something hot's going on out there."
            "Come to the rescue":
                "Alright, alright, let's help that damsel in distress. She better be hot though."
        "You leave the cozy camp heading into the night forest."
        stop music fadeout 2.0
        show bg night_forest with zoomin
        "As soon as you move away from the fire, the immediately forest becomes much less friendly. You belatedly remember about wolves and other predators of night."
        $ intro_torch = False
        menu:
            "Maybe you should get a torch?"
            
            "Yes":
                "You quickly return to the bonfire. That's right, wolves are supposed to be afraid of fire."
                show bg camp with slideawayleft
                "You light a small torch. Hopefully, it will deter animals."
                show bg night_forest with slideawayright
                $ intro_torch = True
            "Nope":
                "Nah, it attracts too much attention in the night forest. Better be stealthy."
        "You carefully continue to move in the direction of sounds. You can no longer make out individual words, it is more like a soft moans."
        "Sounds become closer. There is a small clearing ahead..."
        stop events
        stop world
        play music "content/sfx/music/be/battle (8).mp3" loop
        show sakura_rape at truecenter with zoomin
        "And you see a girl caught by forest tentacles!"
        "She tries to break free, but vines firmly hold her. One of the tentacles is already deep in her ass, and another one in close proximity to her pussy."
        if mast_while_attack == True:
            "You notice how heavily she breathes. She already came at least once. You don't have much time left."
        if intro_torch == True:
            "She notices you and tries to say something, but you can only hear moans from her mouth. The monster noticed you too and threateningly raised armored tentacles."
        else:
            "She didn't noticed you yet, as well as the monster. Time to act quickly."
        if intro_torch == True:
            $ intro_war = False
            label intro_attack_menu:
            menu:
                "Recall what do you know about forest tentacles.":
                    "Forest tentacles are predators, so to speak. They don't eat meat, instead they consume... certain female human body fluids. They brought victims to orgasm over and over again, releasing a huge amount of aphrodisiac inside."
                    "While it seems like a great experience at first sight, such loads quickly incapacitate the higher nervous system, turning victims into mindless sex slaves."
                    "They also die quickly without tentacle's control, what makes them useless for slaves market."
                    jump intro_attack_menu
                "<Warriors only> Try to attack it.":
                    "You uncover your weapon, jump ahead and to strike at the congestion of vines."
                    $ hero.attack += 5
                    $ intro_war = True
                    play sound "content/sfx/sound/be/scythe_attack.mp3"
                    "You cut some of them, but the weapon gets stuck in the armored vines and cracks. The creature tries to attack back, and you quickly move away."
                "<Mages only> Try to cast a spell.":
                    "You focus, feeling rising energy inside your body. You take a step forward and raise your hand."
                    $ hero.magic += 5
                    play sound "content/sfx/sound/be/light1.mp3"
                    "A small flow of magic strikes from under your nail. It damages some vines, but not nearly enough to kill the monster."
                    $ s.disposition += 20
                "Try the torch":
                    "You still have your torch in the left hand. Quickly taking aim, you throw it into the creature."
                    "To your surprise, the creature quickly drew back. Looks like it is afraid of fire!"
                    
            "It wasn't very effective, but you managed to distract the creature. It weakened the grip, and the girl managed to get her own weapon."
        else:
            $ look_at_it = False
            $ poison_intro = False
            label intro_attack_menu_st:
            menu:
                "Recall what do you know about forest tentacles.":
                    "Forest tentacles are predators, so to speak. They don't eat meat, instead they consume... certain female human body fluids. They brought victims to orgasm over and over again, releasing a huge amount of aphrodisiac inside."
                    "While it seems like a great experience at first sight, such loads quickly incapacitate the higher nervous system, turning victims into mindless sex slaves."
                    "They also die quickly without tentacle's control, what makes them useless for slaves market."
                    jump intro_attack_menu_st
                "Relax and enjoy the view.":
                    $ mast_while_attack = True
                    "You sit down on the ground and make yourself comfortable."
                    "Tentacles crumple her body, especially boobs. The tentacle in her ass rhythmically moves."
                    "The girl straining every muscle to break free, but the vines are almost impossible to damage without cutting weapons."
                    "You wonder why only her ass was occupied, and look closer to tentacles. Some of them are dry and brown, with traces of burns."
                    "Looks like parts of the monster meant for other holes were damaged by big fire or a powerful fire spell. Unfortunately, you lack both."
                    $ hero.intelligence += 5
                    $ look_at_it = True
                    jump intro_attack_menu_st
                "Try sneak attack <assassin only>":
                    "You uncover your weapon. You will only get one chance, but it's more than enough."
                    "You slide ahead, under clusters of tentacles, and cut in one motion the tentacle in her ass."
                    "The monster yelps and squeals, lashing tentacles on the ground. It weakened the grip, and the girl managed to get her own weapon."
                    $ s.disposition += 50
                    $ hero.agility += 5
                "Inspect the area" if look_at_it == True and poison_intro == False:
                    $ poison_intro = True
                    "You look at the ground and notice a small bag in the bushes. It probably belongs to the girl."
                    "You carefully pick it up and look inside. There are many strange bottles and flasks smells of herbs."
                    "On one of the bottles you notice a small note 'Poison'."
                "Throw the poison bottle into the monster." if poison_intro == True:
                    "You shrug your shoulders, carefully take aim and throw the bottle at the monster with the full force."
                    "The bottle breaks on impact, a viscous liquid spills on tentacles. The creature begins to twitch erratically. It weakened the grip, and the girl managed to get her own weapon."
                    
        play sound "content/sfx/sound/be/dagger_attack_1.mp3"
        pause 0.5
        play sound "content/sfx/sound/be/dagger_attack_1.mp3"
        "With fast and precise movements she cuts off remaining vines and frees herself. The creature produces frustrated sound and collapses."
        hide sakura_rape with dissolve
        stop music fadeout 2.0
    stop music
    play world "Theme2.ogg" fadein 2.0 loop
    play events "events/night_forest.mp3" loop
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