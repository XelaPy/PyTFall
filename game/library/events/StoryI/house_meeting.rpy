init:
    image orig_1 = ProportionalScale("content/items/quest/orig_1.png", 150, 150)
    image orig_2 = ProportionalScale("content/items/quest/orig_2.png", 150, 150)
label change_alpha:
    hide bg1
    hide bg2
    show expression Transform("bg hiddenvillage_entrance", alpha=a) as bg1
    show expression Transform("bg night_forest", alpha=b) as bg2
    return
label intro_story_dy:
    $ sex_is_must = 0
    $ s = chars["Sakura"]
    $ i = chars["Ino_Yamanaka"]
    $ s_spr = chars["Sakura"].get_vnsprite()
    $ i_spr = chars["Ino_Yamanaka"].get_vnsprite()
    stop music
    stop world
    play world "Theme3.ogg" fadein 2.0 loop
    show bg story city_street_2 with dissolve
    "Initially you didn't wanted to bother Sakura at all. Kunoichi are mortally dangerous and unpredictable, everyone knows it. They say one kunoichi worth hundreds of soldiers."
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
            play events2 "events/door_knock.mp3"
            "..."
            "No response. Damn."
            $ a = 1
            jump sak_house
        "Look through the window":
            "Unfortunately, curtains effectively prevent it. Too bad."
            jump sak_house
        "Try to open the door":
            "You trying to open the door..."
            play events2 "events/door_open.mp3"
            "...and it opens. Strange, why the door is not locked if nobody's home?"
            $ b = 1
            jump sak_house
        "Enter" if b == 1:
            "That's right, fortune favors the bold."
            if a == 1:
                "At least you always can say that you knocked."
            stop world fadeout 2.0
        "Leave" if a == 1:
            "You think how unwise it might be to enter without an invitation, but you cannot wait. You already contacted Carstein, and he made it clear that it is your job to find a way into the ruins."
            "If nobody's home, you will leave a note."
            jump sak_house
    show bg livingroom with dissolve
    "Trying not to make noise, you go inside."
    "It looks like an ordinary living room. You are alone here. Maybe you should..."
    play world "Scene2.ogg" fadein 2.0 loop
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
    play sound "content/sfx/sound/be/darkness2.mp3"
    $ double_vision_on("bg livingroom")
    "Suddenly you feel very dizzy. You body is heavy, you cannot move, and thoughts flow very slowly."
    show expression i_spr at center with dissolve
    "The girl concentrates, and you beginning to see scattered fragments of your past."
    "..."
    "After a while you realize that she's not very good at it. She tries to find your memories about Sakura, but she cannot control the flow of your memory well enough."
    play world "Field2.ogg" fadein 2.0 loop
    menu:
        "Give her what she wants":
            "There is no point to resist, she's knows Sakura too. Once she makes sure you are not an enemy, she won't attack you."
            jump give_up
        "Resist":
            "The girl thinks she can read your mind just like that? Let's teach her a lesson!"
    $ a = 0.6
    $ b = 0.4
    call change_alpha
    "You focus too, and see inside of your linked minds unknown to you village. The girl focuses, the picture changes."
    $ a = 0.1
    $ b = 0.9
    call change_alpha
    "She tries to read you memory about the events in the forest. You look into her mind, and the picture changes again."
    $ a = 0.5
    $ b = 0.5
    call change_alpha
    "Looks like she is not very good in it."
    label mind_duel:
        if a >= 1:
            jump mind_success
        if b >= 1:
            jump mind_fail
    menu:
        "Think about her village":
            $c = 0
            "You trying to look deeper into her mind."
        "Close your mind":
            $ c = 1
            "You trying to not allow her to change the flow of your thoughts."
        "Confront her":
            $ c = 2
            "You trying to overcome her willpower with yours."
        "Just give up":
            "Ok, that's enough. There is no point to resist, she's knows Sakura too. Once she makes sure you are not an enemy, she won't attack you."
            jump give_up
    $ d = randint (0, 2)
    if d == 0:
        if c == 0:
            "Nothing happens. Your efforts cancel each other out."
            jump mind_duel
        elif c == 1:
            "It wasn't very effective. She gets an upper hand."
            $ a -= 0.15
            $ b += 0.15
            call change_alpha
            jump mind_duel
        elif c == 2:
            "It was quite effective. You get an upper hand."
            $ a += 0.15
            $ b -= 0.15
            call change_alpha
            jump mind_duel
    elif d == 1:
        if c == 0:
            "It was quite effective. You get an upper hand."
            $ a += 0.15
            $ b -= 0.15
            call change_alpha
            jump mind_duel
        elif c == 1:
            "Nothing happens. Your efforts cancel each other out."
            jump mind_duel
        elif c == 2:
            "It wasn't very effective. She gets an upper hand."
            $ a -= 0.15
            $ b += 0.15
            call change_alpha
            jump mind_duel
    elif d == 2:
        if c == 0:
            "It wasn't very effective. She gets an upper hand."
            $ a -= 0.15
            $ b += 0.15
            call change_alpha
            jump mind_duel
        elif c == 1:
            "It was quite effective. You get an upper hand."
            $ a += 0.15
            $ b -= 0.15
            call change_alpha
            jump mind_duel
        elif c == 2:
            "Nothing happens. Your efforts cancel each other out."
            jump mind_duel
    jump change_alpha
    
    label mind_success:
        $ i.disposition += 100
        $ double_vision_off()
        "Eventually you managed to overcome her resistance. You are in her mind now, and can do whatever you want."
        $ a = 0
        $ b = 0
        $ c = 0
        label inside_mind:
        menu:
            "Try to find out where the village is located" if a == 0:
                $ a = 1
                "You trying to find clues about the village location, but something prevents it. There is a seal in her mind made by someone much more experienced."
                "You see fragmentary memories about a tall man with strange red eyes, but nothing more."
                $ i.disposition -= 100
                jump inside_mind
            "Try to learn about her" if b == 0:
                $ b = 1
                "You see her memories about training in some kind of kunoichi school. You don't see many boys, and as time passes, only girls remain."
                "Then you see countless missions in different countries. She's not a very good fighter, so she usually has to stand behind, using her mind abilities to help others. She hates it."
                $ i.disposition += 30
                jump inside_mind
            "Try to find something about Sakura" if c == 0:
                $ c = 1
                "You see fragmentary memories about their friendship and rivalry since childhood. You see how they vie for a boy who rejects both and then disappears."
                "After that rivalry slowly disappears, only friendship remains."
                $ i.disposition += 10
                jump inside_mind
            "Try something kinky":
                "Indeed, she deserved it when she attacked you without a reason."
                label sex_inside_mind:
                menu:
                    "Blowjob":
                        show expression i.show("sex", "straight", "simple bg", "uncertain", "partnerhidden", "no clothes", "bc deepthroat", resize=(800, 600), type="first_default") as xxx at truecenter
                        "In your mind you force her to kneel and take your dick deep inside her mouth. She hesitates at first, but soon begins to please you."
                        "After some time you come. She looks aroused. but maybe it's just your mind playing tricks with you?"
                        $ i.disposition += 50
                        $ i.oral += 5
                        $ sex_is_must = 1
                    "Anal": 
                        show expression i.show("sex", "straight", "outdoors", "wildness", "partnerhidden", "ecstatic", "no clothes", "2c anal", resize=(600, 800), type="first_default") as xxx at truecenter
                        "In your mind you force her to lay down and then insert your dick inside her ass. You feel some resistance at first, but soon it disappears."
                        "After some time you come. She looks aroused. but maybe it's just your mind playing tricks with you?"
                        $ i.anal += 5
                        $ i.disposition += 40
                        $ sex_is_must = 1
                    "Vaginal":
                        "You trying to imagine how you do it, but something prevents it. When you trying to find answers in her mind, you understand she never did it before, and subconsciously afraid to do it even here."
                        "It is dangerous to force her, you might lose control over her mind."
                        jump sex_inside_mind
    hide xxx with dissolve
    play sound "content/sfx/sound/events/door_open.mp3"
    s.say "I'm home!"
    $ double_vision_off()
    "Sakura's voice broke your concentration."
    show expression s_spr at mid_right with dissolve
    stop world
    s.say "Hey Ino, I brought some... Whaat? What are you two doing?!"
    $ i.override_portrait("portrait", "ecstatic")
    i.say "..."
    "Oh. She is in complete mess. And your pants are too."
    $ i.override_portrait("portrait", "shy")
    i.say "Sakura, wait... I-It's not what you think it is..."
    $ s.override_portrait("portrait", "angry")
    s.say "Oh, really? It looks pretty clear to me. How long you two doing it behind my back?!"
    $ i.override_portrait("portrait", "angry")
    i.say "Like you can talk after you did back then while I was on the mission!"
    "That escalated quickly. You're wondering whether you should intervene or quickly and quietly leave."
    s.say "Whaat? You dare to bring that up after what you did when I was..."
    jump mind_is_done
    label mind_fail:
        "You did your best, but eventually she forced you to show her what happened in the forest."
    label give_up:
        $ double_vision_off()
        $ a = 0.1
        $ b = 0.9
        call change_alpha
        "You begin to remember in details the events of that night. How you set up a camp, how you help Sakura. How you two together..."
        stop world
        i.say "Whaaaat?!"
        i.say "Sakura... You... Together..."
    label mind_is_done:
    "You don't feel her presence inside your head any longer."
    hide bg1
    hide bg2
    play sound "content/sfx/sound/events/door_open.mp3"
    $ s.override_portrait("portrait", "confident")
    s.say "I'm home!"
    show expression s_spr at mid_right with dissolve
    s.say "Oh? [hero.name]? What are you..."
    $ s.disposition += 50
    $ i.override_portrait("portrait", "angry")
    i.say "I can't believe you! So while I'm all alone here, you are f-fucking like there's no tomorrow!"
    $ s.override_portrait("portrait", "angry")
    s.say "W-what? What are you talking about? I..."
    i.say "I SAW it in his head. Night, forest, you do 'it'."
    "That escalated quickly. You're wondering whether you should intervene or quickly and quietly leave."
    $ s.override_portrait("portrait", "defiant")
    s.say "Whaat? You used it on civilians again? Just wait until lady Tsunade will know about it..."
    i.say "Oh? So you think you can..."
    label mind_is_done:
    "That's it, time to go. You make a small step toward the door."
    s.say "You, stay right there!"
    i.say "Where do you think you going?!"
    "Damn it."
    show black with dissolve 
    pause 2.0
    play world "Theme3.ogg" fadein 2.0 loop
    hide black with dissolve
    $ i.override_portrait("portrait", "indifferent")
    $ s.override_portrait("portrait", "indifferent")
    "After they calmed, you finally managed to tell them why are you here."
    "They look at each other."
    i.say "That's... not something we can decide on our own."
    s.say "Right, if someone put a seal, there must be a reason. You probably should speak with someone from our village, but..."
    if sex_is_must == 0:
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
    else:
        i.say "But outsiders are not permitted without approval of three ninjas."
        s.say "Unfortunately, your sweetheart Ino cannot get you there, [hero.name]."
        $ i.override_portrait("portrait", "shy")
        i.say "I told you already, we are..."
        s.say "Yeah-yeah, I know. You can't get a man in reality, so you do it in dreams."
        $ s.override_portrait("portrait", "angry")
        i.say "Why you..."
        "You quickly ask Sakura to deliver a letter to the village headman."
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
        i.say "Why are you so proud anyway? Is there something between you and him?!"
        s.say "Why wouldn't you try and read it in my mind?"
        i.say "You think I cannot..."
        "You quickly increase the distance between you and the house."
    "If they won't answer to your letter, you need to get to the village in person. For that you will need approval of three ninjas."
    $ s.restore_portrait()
    $ i.restore_portrait()
    "Sakura most likely will cooperate. Even together with Ino it won't be enough, but two is better than one, right?"
    "here we give access to Ino and give a quest to rise disposition to 300 and become her friend via interactions"
    scene black with dissolve
    stop world
    
label intro_story_wrf: #this label goes when player will complete the last quest, ie became friends with Ino
    $ s = chars["Sakura"]
    $ i = chars["Ino_Yamanaka"]
    $ s_spr = chars["Sakura"].get_vnsprite()
    $ i_spr = chars["Ino_Yamanaka"].get_vnsprite()
    stop music
    stop world
    play world "Theme3.ogg" fadein 2.0 loop
    show bg house with dissolve
    "After a few days you got a message from the kunoichi to meet in their house."
    play events2 "events/door_knock.mp3"
    $ i.override_portrait("portrait", "happy")
    i.say "Yes, come in!"
    play sound "content/sfx/sound/events/door_open.mp3"
    show bg livingroom with dissolve
    show expression i_spr at center with dissolve
    i.say "Hi, [hero.name]!"
    "For the last days you managed to get closer to her. Unlike constantly absent Sakura, she can do her missions without leaving the house thanks to her mind abilities."
    $ a = 0
    label ino_diag_one:
    menu:
        "Where's Sakura?" if a == 0:
            $ i.override_portrait("portrait", "indifferent")
            i.say "On another mission, of course. She takes all missions she can lately."
            $ i.override_portrait("portrait", "happy")
            i.say "But who cares about her when I'm here? ♪"
            $ a = 1
            jump ino_diag_one
        "Any news from your village?":
            i.say "Actually, yes. Here, take this."
            show orig_1 at truecenter with dissolve
    $ a = 0
    $ b = 0
    label ino_diag_two:
    menu:
        "You did it for me?" if a == 0:
            $ i.override_portrait("portrait", "shy")
            i.say "Jeez, why should I do something like that? It's stupid."
            $ a = 1
            jump ino_diag_two
        "What is this... thing?" if b == 0:
            $ i.override_portrait("portrait", "indifferent")
            $ b = 1
            i.say "In our village we call it origami. But it's not the important part."
            jump ino_diag_two
        "What should I do with it?":
            $ i.override_portrait("portrait", "indifferent")
            i.say "I think it's a test. There is a rule they don't want to break, but they give you a chance."
    hide orig_1 with dissolve
    i.say "They told me to tell you that it will help you to find the third kunoichi."
    "That's right, you need the approval of three kunoichi to get to their village."
    i.say "We can't help you with it, you should do it on your own. Oh, and you can't ask others to do it for you too."
    $ i.override_portrait("portrait", "happy")
    i.say "Good luck, I guess. I'll be rooting for you ♪" # here we give quest to find kunoichi in the city
    $ i.restore_portrait()
    scene black with dissolve
    stop world
    return