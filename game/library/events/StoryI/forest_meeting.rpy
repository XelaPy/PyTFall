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
    image letter = ProportionalScale("content/items/quest/letter.png", 150, 150)
    image box = ProportionalScale("content/items/quest/box.png", 150, 150)
    
label storyi_forest_begining:
    $ look_at_it = poison_intro = False
    python:
        for i in chars.values():
            if i.origin == "Naruto":
                i.set_flag("quest_cannot_be_hired", True)
                i.set_flag("quest_cannot_be_fucked", True)
                i.set_flag("quest_cannot_be_lover", True)
    $ b = Character("???", color=white, what_color=white, show_two_window=True)
    hide screen mainscreen
    scene black
    stop world
    stop music
    $ s = chars["Sakura"]
    play world "Theme2.ogg" fadein 2.0 loop
    play events "events/night_forest.mp3" loop
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
    $ intro_mast = 0
    $ i = 1
    while i == 1:
        menu:
            "You need a good rest, but you do not want to sleep yet. What do you want to do?"
            "Check your travel bag.":
                show bag at center with dissolve 
                "You don't have much besides your equipment and money."
                $ j = 1
                while j == 1:
                    menu:
                        "Read letter":
                            show letter at truecenter with dissolve
                            "An unsigned letter sent a month ago."
                            play events2 "events/letter.mp3"
                            "'You have enemies that will find you very soon. If you wish to live, come to Pytfall and find your father's grave.'"
                            "Quite ominous, but does not look like a threat."
                            hide letter with dissolve
                        "Check wooden box":
                            show box at truecenter with dissolve
                            play events2 "events/box.wav"
                            "This is a simple wooden box belonged to your father, and the second reason for your return. His notes are still here, but you have no clue what they mean."
                            "Papers covered with cryptic symbols and drawings that no one was able to decipher over the years."
                            hide box with dissolve
                        "Enough with bag.":
                            hide bag with dissolve
                            $ j = 0
                $ del j
            "Jerk off":
                "Nobody's here, might as well to. You unzip your pants."
                "..."
                "It's not going well. Night forest is not the best place for lewd thoughts, and you don't have any pictures too."
                "Perhaps you should try your imagination?"
                menu:
                    "Yes, it's too early to give up!":
                        "You trying to imagine something sexy."
                        if intro_mast == 0:
                            $ intro_mast = 1
                            show imag at center with noisedissolve 
                            "Ooohkey, a bit weird, but it will do. You continue your business, trying to focus on your new imaginary friend."
                            "..."
                            "Yeah, it's much better now! You finish your business, taking care not to extinguish the fire."
                            hide imag with noisedissolve
                            "Alright, done."
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
                                "Moans are fine too. Continue":
                                    "..."
                                    b "N-No! W-w-wait you... Ahh!"
                                    "That was a good one."
                                    b "Ahhhhh!"
                                    "Looks like you both are close."
                                    b "Ahhhhhhhh!♪"
                                    "You managed to come simultaneously, even at a distance. Nice."
                                    $ mast_while_attack = True
                                    "You quickly pull the clothes back."
                                    $ i = 0
                                "Put on the pants would be a good start.":
                                    "You quickly pull the clothes back."
                                    $ mast_while_attack = False
                                    $ i = 0   
                    "Nah, better to not force it":
                        "Well, there always will be another day for that if you won't find a girl soon."
            "Go to sleep":
                "It's about time. Tomorrow will be a tough day."
                $ mast_while_attack = False
                $ i = 0
                scene black
                with eye_shut
                "You slowly sink to sleep."
                b "Aaah!"
                "Mmmm... Z-Z-Z"
                b "Help! Somebo... Aah!"
                show bg camp with eye_open
                menu:
                    "You hear screams nearby."
        
                    "Too bad, you are not a white knight":
                        "Yawning, you close your eyes. It's unwise to wander through the forest at night."
                        scene black
                        with eye_shut
                        "Maybe in the morning you will check what was going on there... Z-Z-Z"
                        b "Ahhhhh! N-n... AAAAH!"
                        show bg camp with eye_open
                        "Agh! Do they do it on purpose or something? It's too loud to sleep, you need to stop it an once."
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
    "You see a girl caught by forest tentacles!"
    $ intro_war = False
    "She tries to break free, but vines firmly hold her. One of the tentacles is already deep in her ass, and another one in close proximity to her pussy."
    if mast_while_attack == True:
        "You notice how heavily she breathes. She already came at least once. You don't have much time left."
    if intro_torch == True:
        "She notices you and tries to say something, but you can only hear moans from her mouth. The monster noticed you too and threateningly raised armoured tentacles."
    else:
        "She didn't noticed you yet, as well as the monster. Time to act quickly."
    if intro_torch == True:
        $ i = 1
        while i == 1:
            menu:
                "Recall what do you know about forest tentacles":
                    "Forest tentacles are predators, so to speak. They don't eat meat, instead they consume... certain female human body fluids. They brought victims to orgasm over and over again, releasing a huge amount of aphrodisiac inside."
                    "While it seems like a great experience at first sight, such loads quickly incapacitate the higher nervous system, turning victims into mindless sex slaves."
                    "They also die quickly without tentacle's control, what makes them useless for slaves market."
                "Try to attack it": # for warriors only
                    "You uncover your weapon, jump ahead and to strike at the congestion of vines."
                    $ i = 0
                    $ hero.attack += 5
                    $ intro_war = True
                    play sound "content/sfx/sound/be/scythe_attack.mp3"
                    "You cut some of them, but the weapon gets stuck in the armoured vines and cracks. The creature tries to attack back, and you quickly move away."
                "Try to cast a spell.": # for mages only
                    $ i = 0
                    "You focus, feeling rising energy inside your body. You take a step forward and raise your hand."
                    $ hero.magic += 5
                    play sound "content/sfx/sound/be/light1.mp3"
                    "A small flow of magic strikes from under your nail. It damages some vines, but not nearly enough to kill the monster."
                    $ s.disposition += 20
                "Try the torch":
                    $ i = 0
                    "You still have your torch in the left hand. Quickly taking aim, you throw it into the creature."
                    "To your surprise, the creature quickly drew back. Looks like it is afraid of fire!"
        "It wasn't very effective, but you managed to distract the creature. It weakened the grip, and the girl managed to get her own weapon."
    else:
        $ i = 1
        while i == 1:
            menu:
                "Recall what do you know about forest tentacles.":
                    "Forest tentacles are predators, so to speak. They don't eat meat, instead they consume... certain female human body fluids. They brought victims to orgasm over and over again, releasing a huge amount of aphrodisiac inside."
                    "While it seems like a great experience at first sight, such loads quickly incapacitate the higher nervous system, turning victims into mindless sex slaves."
                    "They also die quickly without tentacle's control, what makes them useless for slaves market."
                "Relax and enjoy the view.":
                    $ mast_while_attack = True
                    "You sit down on the ground and make yourself comfortable."
                    "Tentacles crumple her body, especially boobs. The tentacle in her ass rhythmically moves."
                    "The girl straining every muscle to break free, but the vines are almost impossible to damage without cutting weapons."
                    "You wonder why only her ass was occupied, and look closer to tentacles. Some of them are dry and brown, with traces of burns."
                    "Looks like parts of the monster meant for other holes were damaged by big fire or a powerful fire spell. Unfortunately, you lack both."
                    $ hero.intelligence += 5
                    $ look_at_it = True
                "Try sneak attack": # assassin only
                    "You uncover your weapon. You will only get one chance, but it's more than enough."
                    "You slide ahead, under clusters of tentacles, and cut in one motion the tentacle in her ass."
                    "The monster yelps and squeals, lashing tentacles on the ground. It weakened the grip, and the girl managed to get her own weapon."
                    $ s.disposition += 50
                    $ hero.agility += 5
                    $ i = 0
                "Inspect the area" if look_at_it == True and poison_intro == False:
                    $ poison_intro = True
                    "You look at the ground and notice a small bag in the bushes. It probably belongs to the girl."
                    "You carefully pick it up and look inside. There are many strange bottles and flasks smells of herbs."
                    "On one of the bottles you notice a small note 'Poison'."
                "Throw the poison bottle into the monster" if poison_intro == True:
                    "You shrug your shoulders, carefully take aim and throw the bottle at the monster with the full force."
                    "The bottle breaks on impact, a viscous liquid spills on tentacles. The creature begins to twitch erratically. It weakened the grip, and the girl managed to get her own weapon."
                    $ i = 0
    play sound "content/sfx/sound/be/dagger_attack_1.mp3"
    pause 0.5
    play sound "content/sfx/sound/be/dagger_attack_1.mp3"
    "With fast and precise movements she cuts off remaining vines and frees herself. The creature produces frustrated sound and collapses."
    hide sakura_rape with dissolve
    stop music fadeout 2.0
    play world "Theme2.ogg" fadein 2.0 loop
    play events "events/night_forest.mp3" loop
    if poison_intro == True:
        "You give her the bag you found earlier. Gratefully nod, she takes it."
    else:
        "She quickly picks up the bag from the bushes nearby."
    "She tries to look calm, but you notice how quickly and heavily she breathes."
    "The lower part of her clothes was torn apart. She gets out of the bag spare clothes and changes in the bushes."
    "Although it's too late to be modest after what you saw, but whatever..."
    "..."
    $ sakspr = chars["Sakura"].get_vnsprite()
    $ s.override_portrait("portrait", "indifferent")
    show expression sakspr at center with dissolve
    s.say "Thanks for the help. My name is Sakura."
    "You introduce yourself."
    s.say "I see. Nice to meet you, [hero.name]."
    $ s.disposition += 100
    menu:
        "Offer to rest in your camp":
            $ s.override_portrait("portrait", "happy")
            "She must be tired. You tell her about your camp nearby."
            s.say "<she looks a bit surprised, but happy> Oh, ok! I would like to have some rest indeed."
            $ s.disposition += 30
            $ intro_be_nice = True
        "There is no time to waste. Her ass is compromised already":
            "You explain that her that her ass is full of very powerful aphrodisiac, and needs to be cleaned. You are willing to take the risk and help her."
            $ s.override_portrait("portrait", "shy")
            $ hero.anal += 10
            $ s.anal += 10
            s.say "<she immediately blushes> I-I see. I accept you proposition, but please be gentle."
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
        "Demand a reward":
            "You quickly explain what that thing could do to her without your help, and ask for reward."
            $ intro_be_nice = True
            $ s.override_portrait("portrait", "indifferent")
            "She doesn't look surprised, she probably expected it."
            s.say "Naturally. I don't have much gold, but you can have it if you want. I have some healing potions too."
            menu:
                "Take gold":
                    "She gives you 200 G."
                    $ hero.gold += 200
                "Take potions":
                    $ hero.add_item("Small Healing Potion")
                    "She gives you a bottle."
                    "You tell her about your camp nearby, and together you go there."
                "Ask for a new weapon" if intro_war == True:
                    "You explain that you lost your weapon trying to save her."
                    s.say "Alright. Here, take this."
                    "She gives you a small sharp dagger."
                    $ intro_war = False
                    s.say "It's called kunai. I have a spare one, so you can take it."
                    $ hero.add_item("Kunai")
                    "You tell her about your camp nearby, and together you go there."
    show bg camp with slideawayleft
    $ s.override_portrait("portrait", "indifferent")
    if intro_be_nice == True:
        $ s.override_portrait("portrait", "happy")
        "With a grateful smile, she sits by the fire."
    else:
        $ s.override_portrait("portrait", "shy")
        "Still shy, she sits by the fire."
    $ i = 1
    while i == 1:
        menu:
            "Ask about her":
                s.say "Um, you already know my name. I'm on a mission here. Sorry, I cannot say more."
                "Judging by her uniform, she is one of those infamous kunoichi, female assassins living outside cities."
            "Ask about what happened":
                $ s.override_portrait("portrait", "shy")
                s.say "I was on my to the city. I took a shortcut through the forest, we did it many times."
                s.say "But I never used this route alone before, so maybe that's why it attacked me..."
            "Wish her good night and go to sleep":
                "You are too exhausted after a long day and recent events to keep talking, or doing anything else. You wish her good night and go to your tent."
                $ i = 0
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
    else:
        "You slowly fall asleep. It was a tough night."
        $ s.override_portrait("portrait", "ecstatic")
        s.say "Mmm... Ah..."
        "Really? Again?"
        s.say "Ah..."
        "You quietly get up and carefully peeking out of the tent."
        show expression s.show("nude", "stripping", "uncertain", "outdoors", "nature", "shy", "uncertain", "revealing", resize=(800, 600), type="first_default") as xxx at truecenter
        "Looks like the aphrodisiac still does its job. You see Sakura touching herself."
        menu:
            "What a healthy girl. Sleepy time":
                "Yeap, sex cannot replace night sleep. You return to your bed."
                hide xxx with dissolve
            "Lend her a helping, ahem, hand":
                "It could be dangerous to let her know that you saw it. You retreat into the depths of the tent and call her."
                hide xxx with dissolve
                "After some time she enters the tent. Looks like dressed in a hurry. You notice the blush on her cheeks."
                $ s.override_portrait("portrait", "shy")
                s.say "Yes, what do you want?"
                "You explain her that you understand how she feels, and propose to help with burning out remains of aphrodisiac."
                "As you talk, she blushes even more, but doesn't interrupt you."
                s.say "I... accept your offer. Please lay down."
    $ s.oral += 10
    hide sakspr
    show expression s.show("sex", "confident", "suggestive", "indoors", "living", "bc blowjob", "partnerhidden", resize=(800, 600), type="first_default") as xxx at truecenter
    $ hero.vitality -= 100            
    scene black
    with eye_shut
    hide xxx
    stop events
    stop world fadeout 2.0
    show expression Text("In the next morning", style="TisaOTM", align=(0.5, 0.33), size=40) as txt1:
        alpha 0
        linear 3.5 alpha 1.0
    pause 2.5
    hide txt1
    with dissolve
    play world "Theme3.ogg" fadein 2.0 loop
    show bg story city_street_2 with dissolve
    $ sakspr = chars["Sakura"].get_vnsprite()
    show expression sakspr at center with dissolve
    "At the next morning together you quickly reached the city. Some bandits tried to rob you along the road, but your new companion quickly got rid of them."
    "She kept up the general conversation, but avoided to talk about the last night, probably pretending it never happened."
    "Ultimately, you part ways in the town square. She told you where you can find her in the city if something happens, but asked to not bother without a good reason, since she's on her mission."
    hide expression sakspr at center with dissolve
    $ s.restore_portrait()
    "Well then, time to do your own mission."
    $ del i
    $ del b
    $ del s
    $ del intro_mast
    $ del intro_torch
    $ del mast_while_attack
    $ del intro_war
    $ del poison_intro