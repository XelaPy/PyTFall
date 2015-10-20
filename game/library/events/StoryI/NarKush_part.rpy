init python:
    narukoquest = register_quest("Uzumaki Clan", manual=True)

label storyi_naruko_first_meeting:
    scene black
    show bg hiddenvillage_entrance with dissolve
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    show expression n_spr at center with dissolve
    $ n.override_portrait("portrait", "happy")
    n.say "Hey, you are [hero.name]!"
    "A cheerful girl suddenly approached you."
    n.say "Nice to meet ya! I'm Naruko Uzumaki."
    menu:
        "How do you know my name?":
            n.say "Who doesn't? I mean, you are the guy who is supposed to take care of everyone here."
            "You have to wonder if you were the only one who did suspect Tsunade's plan to remain a secret?"
        "What do you want?":
            n.say "Nothin' special. Just wanna say hi and maybe speed up things."
    n.say "I don't like complicating things. I trust granny, so I think you are not a bad person."
    $ n.override_portrait("portrait", "shy")
    n.say "But I want something in return for my, you know..."
    $ n.override_portrait("portrait", "happy")
    n.say "So here's a deal: you treat me five times, and I will allow you to do your thing. Deal?"
    "That sounds very simple. Prices shouldn't be high either."
    menu:
        "Deal":
            n.say "Awesome!"
            $ n.disposition += 20
            "It's hard to believe, but she is already drooling..."
        "Don't you want to know each other better for a start?":
            $ n.disposition -= 20
            $ n.override_portrait("portrait", "angry")
            n.say "Why? I don't care about you. Let's just do it and be done with it."
            n.say "I told ya, I don't like complicating things."
        "It's too simple to be truth":
            n.say "I dunno, it seems fair. Sex is not a big deal, yeah?"
            $ n.override_portrait("portrait", "shy")
            n.say "I mean, ladies in the city do it for a small fee every day."
    $ n.override_portrait("portrait", "happy")
    n.say "Let me know when you are ready to treat me. See ya!"
    hide expression n_spr with dissolve
    $ chars["Naruko_Uzumaki"].set_flag("event_to_interactions_eatwithnarukotogether", value={"label": "eat_with_Naruko", "button_name": "Treat Her", "condition": "True"})
    $ chars["Naruko_Uzumaki"].set_flag("naruko_eat", value=0)
    "She left. What a weird girl."
    "Well, if she is telling the truth, it will be simple enough."
    $ n.restore_portrait()
    $ del n
    $ del n_spr
    $ pytfall.world_quests.get("Uzumaki Clan").next_in_label("You met Naruko, a cheerful and lively kunoichi. She proposed to give away her virginity if you treat her for a week in her favourite eatery.")
    jump hiddenvillage_entrance

label storyi_eat_with_Naruko:
    if hero.gold <= 200:
        "You don't have enough money for that."
        jump girl_interactions
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    if n.flag("gm_eat_together") != day:
        $ n.set_flag("gm_eat_together", value=day)
    else:
        "You already did it today. She's not hungry."
        jump girl_interactions
    scene black
    show bg cafe with dissolve
    $ gm.set_img("eating", type="first_default")
    "You treat her in her favourite eatery."
    $ chars["Naruko_Uzumaki"].mod_flag("naruko_eat", 1)
    $ n.disposition += 40
    $ temp = randint (90, 250)
    if hero.take_money(temp):
        "You pay her bill, it was [temp] G. Not bad for a slim girl..."
    $ n.override_portrait("portrait", "happy")
    n.say "Thanksies for the meal! ♪"
    $ del temp
    $ n.restore_portrait()
    $ gm.set_img("vnsprite", type="first_default")
    if (chars["Naruko_Uzumaki"].flag("naruko_eat") >= 7) and (pytfall.world_quests.check_stage("Uzumaki Clan") == 1):
        $ pytfall.world_quests.get("Uzumaki Clan").next_in_label("You paid her bills for a week. Time to visit her and demand you reward!")
    elif (chars["Naruko_Uzumaki"].flag("naruko_eat") >= 7) and (pytfall.world_quests.check_stage("Uzumaki Clan") == 3):
        $ pytfall.world_quests.get("Uzumaki Clan").next_in_label("You paid her bills for another week. Time to pay her a visit.")
    elif (chars["Naruko_Uzumaki"].flag("naruko_eat") >= 7) and (pytfall.world_quests.check_stage("Uzumaki Clan") == 5):
        $ pytfall.world_quests.get("Uzumaki Clan").next_in_label("You paid her bills for one more week. You are pretty close to her now, after three weeks of eating together. Another try?")
    $ del n
    $ del n_spr
    jump girl_interactions
        
label storyi_naruko_second_meeting:
    $ flash = Fade(.25, 0, .75, color=green)
    scene black
    stop music
    stop world
    play world "Town2.ogg" fadein 2.0 loop
    $ k = chars["Kushina_Uzumaki"]
    $ k_spr = chars["Kushina_Uzumaki"].get_vnsprite()
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    show bg hiddenvillage_entrance with dissolve
    show expression n_spr at center with dissolve
    $ n.override_portrait("portrait", "happy")
    n.say "Phew, I'm full. Thanksies♪"
    n.say "Alright, time to do it! Follow me."
    show bg girl_room_4 with dissolve
    stop world
    "She brought you to a small house on the edge of the village. Outside it looks shabby, but inside it is quite cozy."
    hide expression n_spr
    show expression n.show("nude", "simple bg", "everyday", "confident", "stripping", resize=(800, 600), type="first_default") as xxx at truecenter
    "She quickly unbuttoning clothes."
    n.say "C'mon, c'mon, I have other things to do!"
    "Well, if she insists... "
    "You carefully enter inside. Slowly moving forward, eventually you feel a resistance. Just a bit more..."
    play sound "content/sfx/sound/be/light1.mp3"
    show bg girl_room_4 with flash
    "Huh?"
    play sound "content/sfx/sound/be/light1.mp3"
    show bg girl_room_4 with flash
    hide xxx
    show expression k.show("sex", "straight", "partnerhidden", "doggy", "living", "no clothes", resize=(600, 800), type="first_default") as xxx at truecenter with flash
    "Suddenly the resistance disappears. You look down and see an unknown woman instead of Naruko."
    $ k.override_portrait("portrait", "ecstatic")
    k.say "Um, hi there. Could you please begin moving already?"
    menu:
        "Who are you?":
            $ pass
        "What's going on?":
            $ pass
        "Where is Naruko?":
            $ pass
    k.say "Could it wait? I'd like to have a proper sex while I can."
    "Damn, it was suspicious from the beginning. As you continue to move, the woman loudly moans. Looks like she is very horny, so maybe she won't be angry at you for, er, appearing around you dick..."
    hide xxx with dissolve
    show expression k.show("nude", "living", "no clothes", "confident", "happy", resize=(800, 600), type="first_default") as xxx at truecenter
    "After a few minutes you both come. The woman happily resting now."
    $ k.override_portrait("portrait", "shy")
    k.say "I suppose you have many questions. We have some time before she returns, so I can answer them."
    $ a = 0
    $ k.override_portrait("portrait", "shy")
    $ i = 1
    while i == 1:
        menu:
            "Where is Naruko?":
                k.say "It's a bit complicated. You could say she is resting inside of me right now. She will be back very soon."
            "Who are you?":
                k.say "I'm Naruko's mother, Kushina Uzumaki. Nice to meet you, [hero.name]!"
            "What's going on?":
                k.say "You have been tricked by my daughter, of course. It wasn't the first time when she got free meal from strangers promising sex in return."
                k.say "Though it's pretty lonely inside, so I don't mind to take her place at all."
            "How can you change places?":
                $ k.override_portrait("portrait", "sad")
                k.say "Ah, it's a long and old story. In short, we sealed a powerful and dangerous creature inside Naruko's body immediately after her birth."
                k.say "And I became a part of the seal inside her. My job is to keep the seal intact, but as you can see, there are some side effects as well."
                $ k.override_portrait("portrait", "shy")
                k.say "During sex your chakras immediately begin to mix. It affects the seal, my chakra suppress hers in order to protect it, and we changing places."
                $ a = 1
            "Is there any way to take her virginity?" if a == 1:
                $ i = 0
                k.say "You obviously can do it if we will be separated by force, but then most likely the beast will be free and the village will be destroyed."
                k.say "But..."
                play sound "content/sfx/sound/be/light1.mp3"
                show bg girl_room_4 with flash
                k.say "Ah, we don't have much time left, I'm afraid..."
                play sound "content/sfx/sound/be/light1.mp3"
                show bg girl_room_4 with flash
                hide xxx
                show expression n.show("nude", "simple bg", "everyday", "confident", "stripping", resize=(800, 600), type="first_default") as xxx at truecenter with flash
                $ n.override_portrait("portrait", "happy")
                n.say "<yawns> That was a good nap. How did it go, [hero.name]? You had your fun? We could do it again later if you want, with the same condition..."
    $ n.override_portrait("portrait", "happy")
    menu:
        "You tricked me!":
            n.say "<she grins> I told you I'll let you do me, and I did. It's not my fault that mom gets lonely and comes out."
            n.say "You did well by the way. Often people just get scared and immediately run away after we change places like that."
            jump naruko_after_sex
        "Can I talk to your mother again?":
            n.say "Ooh? You getting along or something? Well, you know the drill, it will be a weak of meals."
    hide xxx with dissolve
    show expression n_spr at center with dissolve
    "She quickly dresses up."
    n.say "Ok, see ya later. I have to run now, I have a mission soon."
    hide expression n_spr with dissolve
    "She left... You probably need to talk to Kushina again." #yup, another quest to treat her 5 times
    $ n.restore_portrait()
    $ k.restore_portrait()
    $ del a
    $ del i
    $ del n
    $ del n_spr
    $ del k
    $ del k_spr
    $ chars["Naruko_Uzumaki"].set_flag("naruko_eat", value=0)
    $ pytfall.world_quests.get("Uzumaki Clan").next_in_label("This turned out not as you expected... In order to try again you need to treat her for a week once more.")
    scene black with dissolve
    stop world
    jump hiddenvillage_entrance
    
label storyi_naruko_third_meeting:
    $ flash = Fade(.25, 0, .75, color=green)
    stop music
    stop world
    play world "Town2.ogg" fadein 2.0 loop
    scene black
    $ k = chars["Kushina_Uzumaki"]
    $ k_spr = chars["Kushina_Uzumaki"].get_vnsprite()
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    show bg hiddenvillage_entrance with dissolve
    show expression n_spr at center with dissolve
    $ n.override_portrait("portrait", "happy")
    n.say "Aahh, it feels good to eat for free, hehe."
    "This time she ate much more than before, as if on purpose."
    n.say "Well? Wanna have some fun with mom now? I could use some nap after lunch anyway."
    show bg girl_room_4 with dissolve
    hide expression n_spr
    show expression n.show("nude", "simple bg", "everyday", "confident", "stripping", resize=(800, 600), type="first_default") as xxx at truecenter
    n.say "Here we go."
    "You won't be able to take her virginity anyway, so you could try something else."
    $ n.override_portrait("portrait", "shy")
    $ a = 0
    menu:
        "Blowjob":
            n.say "Wait, what? You want me to... take it in my mouth?"
            n.say "Mmm, if it tastes good, then why not..."
            $ a = 1
        "Handjob":
            n.say "Hm? You want me to take it in my hand?"
            n.say "Alright, whatever..."
            $ a = 2
        "Anal":
            n.say "Wha? You can do it there too?"
            n.say "Well, I don't mind, but I hope mom will be ok..."
            $ a = 3
    play sound "content/sfx/sound/be/light1.mp3"
    show bg girl_room_4 with flash
    "It begins."
    play sound "content/sfx/sound/be/light1.mp3"
    show bg girl_room_4 with flash
    n.say "Hey, say hi to mom, ok?"
    hide xxx
    if a == 1:
        show expression k.show("sex", "straight", "partnerhidden", "indoors", "bc blowjob", "no clothes", "indifferent", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    elif a == 2:
        show expression k.show("sex", "straight", "partnerhidden", "simple bg", "bc handjob", "no clothes", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    else:
        show expression k.show("sex", "straight", "partnerhidden", "indoors", "2c anal", "no clothes", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    $ k.override_portrait("portrait", "shy")
    "Kushina enthusiastically continues to do the job..."
    if a == 1:
        k.say "...slurp...slurp..."
    elif a == 2:
        k.say "Hm? Let's see what do we have here... ♪"
    else:
        k.say "Oh my, that's unexpected ♪"
    scene black with dissolve
    hide xxx
    show bg girl_room_4 with dissolve
    show expression k.show("nude", "living", "no clothes", "confident", "happy", resize=(800, 600), type="first_default") as xxx at truecenter with dissolve
    $ k.override_portrait("portrait", "shy")
    k.say "Pleased to meet you again, [hero.name]. Hmm, I wonder if you wanted to meet me again or actually tried to it with my daughter? ♪"
    menu:
        "I wanted to meet you again.":
            $ k.disposition += 100
            k.say "I enjoy our time together too, but I'm afraid we will spoil Naruko too much if you'll continue to treat her like that ♪"
        "I just wanted to help her.":
            $ k.disposition += 50
            $ n.disposition += 25
            $ k.override_portrait("portrait", "sad")
            k.say "I'm glad to hear that. I wish I could take care of her personally."
    $ k.override_portrait("portrait", "shy")
    k.say "But enough with it, let's not waste any more time."
    $ k.override_portrait("portrait", "sad")
    k.say "There have been an accident several years ago. She tried to do it with a boy she liked for the first time."
    k.say "Unlike you, he was shocked and even disgusted by the transformation. Soon he severed all ties with her and left the village."
    k.say "Since then doesn't have many friends in the village..."
    k.say "But you are on a right way, I think. If she will trust you enough, her body will not perceive you as a threat."
    $ k.override_portrait("portrait", "shy")
    play sound "content/sfx/sound/be/light1.mp3"
    show bg girl_room_4 with flash
    k.say "Just keep trying. Eventually..."
    play sound "content/sfx/sound/be/light1.mp3"
    show bg girl_room_4 with flash
    "And she disappears again."
    hide xxx
    show expression n.show("nude", "simple bg", "everyday", "confident", "stripping", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    n.say "<yawns> Hm, such a weird dream... Hey, [hero.name], I wanna sleep a bit more. Could you turn the lights off for me?.."
    hide xxx
    "She fell asleep. Turning off the lights, you left the house." #another 5 times eating together
    $ n.restore_portrait()
    $ k.restore_portrait()
    $ del a
    $ del n
    $ del n_spr
    $ del k
    $ del k_spr
    $ chars["Naruko_Uzumaki"].set_flag("naruko_eat", value=0)
    $ pytfall.world_quests.get("Uzumaki Clan").next_in_label("You have to keep treating her. Hopefully, it will pay off eventually.")
    scene black with dissolve
    stop world
    jump hiddenvillage_entrance
    
label storyi_naruko_final_meeting: 
    $ flash = Fade(.25, 0, .75, color=green)
    stop music
    stop world
    play world "Town2.ogg" fadein 2.0 loop
    scene black
    $ k = chars["Kushina_Uzumaki"]
    $ k_spr = chars["Kushina_Uzumaki"].get_vnsprite()
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    if n.disposition < 500: # by now eating so many times together should give a lot of disposition already, but just in case
        $ n.disposition = 500
    $ k.disposition += 100
    $ set_friends(hero, n)
    $ set_friends(hero, k)
    show bg hiddenvillage_entrance with dissolve
    show expression n_spr at center with dissolve
    $ n.override_portrait("portrait", "happy")
    n.say "Ehehe, food tastes better when we eat together♪"
    "For three weeks you have dinner together. It feels like you do it for a very long time though (especially from the viewpoint of your wallet)."
    $ n.override_portrait("portrait", "shy")
    n.say "Hey, wanna go to my home? We could do... stuff."
    show bg girl_room_4 with dissolve
    hide expression n_spr
    show expression n.show("nude", "simple bg", "everyday", "confident", "stripping", resize=(800, 600), type="first_default") as xxx at truecenter
    "This is the third time, but for some reason she is much more nervous than before."
    $ n.override_portrait("portrait", "sad")
    n.say "Hey, [hero.name]... Do you want to meet mom again or it's about the Tsunade's mission?"
    menu:
        "I need your virginity.":
            $ n.override_portrait("portrait", "shy")
            n.say "I-I see. Well, you know I cannot promise you that, but I'll try..."
            $ n.disposition += 100
        "I have to see your mother":
            $ n.override_portrait("portrait", "happy")
            $ k.disposition += 100
            n.say "Are you two in love or something? Good for me then, I will have free food rest of my life!"
            $ n.override_portrait("portrait", "shy")
            n.say "Just kidding... If you really... like each other, you can meet her any time. I know how lonely she is after father's death."
        "I want to help both of you":
            $ n.override_portrait("portrait", "sad")
            $ k.disposition += 50
            $ n.disposition += 50
            n.say "Help us? Well, t-thanks, I guess..."
    n.say "Never mind, let's just do it."
    "She suddenly puts her hand under your clothes and grabs you there. She really got used to it..."
    play sound "content/sfx/sound/be/light1.mp3"
    show bg girl_room_4 with flash
    "Looks like it doesn't work after all. Damn."
    $ n.override_portrait("portrait", "sad")
    show expression k.show("sex", "straight", "partnerhidden", "simple bg", "bc handjob", "no clothes", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    $ k.override_portrait("portrait", "shy")
    k.say "Hello there, [hero.name]! ♪ How do you do?"
    "She begins to rapidly stimulate you."
    k.say "You did a great job lately. You are not a mere stranger to her."
    play sound "content/sfx/sound/be/light1.mp3"
    show bg girl_room_4 with flash
    k.say "Hey, stay with me, ok? Hold it a bit longer. You can do it, right?"
    play sound "content/sfx/sound/be/light1.mp3"
    show bg girl_room_4 with flash
    "She is clearly up to something..."
    k.say "Just a few seconds... Ok, now! Come on, release it on my naked sexy body! ♪"
    hide xxx
    show expression n.show("after sex", "indoors", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    "You feel how her hand disappears, but it's too late to stop."
    $ n.override_portrait("portrait", "happy")
    n.say "Wow, it's so sticky and thick! Hehe ♪"
    play sound "content/sfx/sound/be/light1.mp3"
    show bg girl_room_4 with flash
    hide xxx
    play sound "content/sfx/sound/be/light1.mp3"
    show expression k.show("nude", "living", "no clothes", "confident", "happy", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    pause 0.5
    hide xxx
    play sound "content/sfx/sound/be/light1.mp3"
    show expression n.show("after sex", "indoors", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    pause 0.5
    hide xxx
    play sound "content/sfx/sound/be/light1.mp3"
    show expression k.show("nude", "living", "no clothes", "confident", "happy", resize=(800, 600), type="first_default") as xxx at mid_left
    show expression n.show("after sex", "indoors", resize=(800, 600), type="first_default") as yyy at mid_right
    with flash
    "After a series of outbreaks you see both girls in front of you. Suddenly, you feel a surge of weakness, and it's getting dark..."
    stop world fadeout 2.0
    scene black with dissolve
    hide xxx
    hide yyy
    pause 3.0
    play world "Town2.ogg" fadein 2.0 loop
    show bg girl_room_4 with dissolve
    show expression n_spr at mid_left with dissolve
    show expression k_spr at mid_right with dissolve
    $ k.override_portrait("portrait", "sad")
    $ n.override_portrait("portrait", "shy")
    "When you woke up, both girls still were there."
    k.say "Please don't move much, [hero.name]! You need to rest."
    n.say "Will he be ok?"
    k.say "Er, I think so, dear. I wasn't expected him to lose consciousness. I guess his chakra was too weak to withstand it..."
    "You feel a bit dizzy. And you also feel how something inside you is different now..."
    label talk_with_naruko_and_kushina:
    menu:
        "What just happened?":
            $ pass
        "I feel different...":
            $ pass
    $ hero.constitution -= 30
    k.say "I'm very sorry, [hero.name]. I had to try it, I was afraid there won't be another chance..."
    k.say "I mixed our chakra together. Now we have a piece of yours, and you have a piece of ours."
    k.say "Now we are connected by you, [hero.name]. As long as you are alive, we can live separately."
    n.say "Wha? For real? Now we are connected by his white stuff?"
    $ k.override_portrait("portrait", "shy")
    k.say "It is more correct to say that we are bounded by his chakra, dear. Not by the 'white stuff', at least not only by it."
    n.say "Oh. So... are you two going to marry now? I mean, you did it so many times already..."
    $ k.override_portrait("portrait", "confident")
    k.say "Actually, I was thinking about giving my blessing to you two. You look good together ♪"
    $ n.override_portrait("portrait", "happy")
    n.say "Nah, I am for an open relationship. Damn, I'm hungry. Gonna check the kitchen, I think there should be some leftovers from yesterday..."
    hide expression n_spr with dissolve
    $ k.override_portrait("portrait", "sad")
    k.say "She grew up so much..."
    k.say "I'm really sorry that I had to do it with you. I'm afraid there will be consequences for your health because your chakra wasn't as strong as ours."
    $ k.override_portrait("portrait", "confident")
    k.say "But on the other hand, now you have out chakra instead. You are a part of our family now, [hero.name]."
    k.say "You always will be welcomed here. Oh, and I wasn't joking about my blessing, you can dispose of her as you like."
    $ k.override_portrait("portrait", "shy")
    k.say "Of course the same goes for me. It's the least I can do. Come to visit us when you can."
    $ pytfall.world_quests.get("Uzumaki Clan").next_in_label("With your help Naruko was separated from her mother, and can participate in sex actions now. Now you can take her virginity (long overdue).")
    $ n.restore_portrait()
    $ k.restore_portrait()
    $ k.set_flag("quest_cannot_be_lover", value=False)
    $ k.set_flag("quest_cannot_be_fucked", value=False)
    $ n.set_flag("quest_cannot_be_lover", value=False)
    $ n.set_flag("quest_cannot_be_fucked", value=False)
    $ chars["Naruko_Uzumaki"].del_flag("naruko_eat")
    $ chars["Naruko_Uzumaki"].del_flag("event_to_interactions_eatwithnarukotogether")
    $ del a
    $ del n
    $ del n_spr
    $ del k
    $ del k_spr
    scene black with dissolve
    stop world
    jump hiddenvillage_entrance
    
label naruko_finish_quest:
    "Ultimately you took care of Naruko, and got her hot mother as a bonus. Nice!"
    $ pytfall.world_quests.get("Uzumaki Clan").finish_in_label("You took care of Naruko's virginity.", "complete")
    jump hiddenvillage_entrance