init python:
    narukoquest = register_quest("Uzumaki Clan")

label naruko_first_meeting:
    scene black
    show bg hidden_village with dissolve
    $ k = chars["Kushina_Uzumaki"]
    $ k_spr = chars["Kushina_Uzumaki"].get_vnsprite()
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
    "She left. What a weird girl."
    "Well, if she is telling the truth, it will be simple enough."
    $ n.restore_portrait()
    $ pytfall.world_quests.get("Uzumaki Clan").next_in_label("You met Naruko, a cheerful and lively kunoichi. She proposed to give away her virginity if you treat her five times in her favorite eatery.")
    jump hiddenVillage_entrance

label eat_with_Naruko:
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
    # show expression n.show("eating", resize=(800, 600), type="first_default") as xxx at mid_right
    "You treat her in her favorite eatery."
    if not(pytfall.world_quests.check_stage("Uzumaki Clan", 2)):
        $ narrator(choice(["The food is clearly unhealthy, like any fastfood. But she enjoys it anyway.", "The food is cheap here, but she eats a lot, meaning you have to pay a lot too.", "She proposes you to try the local food too, but you politely refuse. It's unwise to eat unfamiliar food in unfamiliar place."]))
    $ n.disposition += 40
    $ temp = randint (90, 250)
    if hero.take_money(temp):
        "You pay her bill, it was [temp] G. Not bad for a slim girl..."
    $ n.override_portrait("portrait", "happy")
    n.say "Thanksies for the meal! ♪"
    $ del temp
    $ n.restore_portrait()
    $ gm.set_img("vnsprite", type="first_default")
    jump girl_interactions
        
label naruko_second_meeting: # after feeding her enough times
    $ flash = Fade(.25, 0, .75, color=green)
    stop music
    stop world
    play world "Town2.ogg" fadein 2.0 loop
    scene black
    $ k = chars["Kushina_Uzumaki"]
    $ k_spr = chars["Kushina_Uzumaki"].get_vnsprite()
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    show bg hidden_village with dissolve
    show expression n_spr at center with dissolve
    $ n.override_portrait("portrait", "happy")
    n.say "Phew, I'm full. Thanksies♪"
    n.say "Alright, time to do it! Follow me."
    show bg story girl_room with dissolve
    "She brought you to a small house on the edge of the village. Outside it looks shabby, but inside it is quite cozy."
    hide expression n_spr
    show expression n.show("nude", "simple bg", "everyday", "confident", "stripping", resize=(800, 600), type="first_default") as xxx at truecenter
    "She quickly unbuttoning clothes."
    n.say "C'mon, c'mon, I have other things to do!"
    "Well, if she insists... "
    "You carefully enter inside. Slowly moving forward, eventually you feel a resistance. Here we go, another target for Tsunade is completed. Just a bit more..."
    play sound "content/sfx/sound/be/light1.mp3"
    show bg story girl_room with flash
    "Huh? You see some kind of glow."
    play sound "content/sfx/sound/be/light1.mp3"
    show bg story girl_room with flash
    hide xxx
    show expression k.show("sex", "straight", "partnerhidden", "doggy", "living", "no clothes", resize=(600, 800), type="first_default") as xxx at truecenter with flash
    "Suddenly the resistance disappears. You look down and see an unknown woman instead of Naruko."
    "Fearing the worst, you quickly remove your dick."
    $ k.override_portrait("portrait", "ecstatic")
    k.say "W-wait, don't pull it out!"
    menu:
        "Who are you?":
            $ pass
        "What's going on?":
            $ pass
        "Where is Naruko?":
            $ pass
    k.say "I'll tell you everything later, just keep moving!"
    "Damn, it was suspicious from the beginning. As you continue to move, the woman loudly moans. Looks like she is very horny, so maybe she won't be angry at you for, er, appearing around you dick..."
    hide xxx with dissolve
    show expression k.show("nude", "living", "no clothes", "confident", "happy", resize=(800, 600), type="first_default") as xxx at truecenter
    "After a few minutes you managed to make her come. The woman happily resting now."
    $ k.override_portrait("portrait", "shy")
    k.say "My, what a handsome young man. She has a good taste after all."
    k.say "I suppose you have many questions. We have some time before she returns, so I can answer them."
    $ a = 0
    label kushina_after_sex:
    $ k.override_portrait("portrait", "shy")
    menu:
        "Where is Naruko?":
            k.say "It's a bit complicated. You could say she is resting inside of me right now. She will be back very soon."
            jump kushina_after_sex
        "Who are you?":
            k.say "I'm Naruko's mother, Kushina Uzumaki. Nice to meet you, [hero.name]! Before you ask how do I know you, I can hear my daughter's thoughts sometimes."
            jump kushina_after_sex
        "What's going on?":
            k.say "You have been tricked by my daughter, of course. It wasn't the first time when she got free meal from strangers promising sex in return."
            k.say "Though it's pretty lonely inside, so I don't mind to take her place at all."
            jump kushina_after_sex
        "How can you change places?":
            $ k.override_portrait("portrait", "sad")
            k.say "Ah, it's a long and old story. In short, we sealed a powerful and dangerous creature inside Naruko's body immediately after her birth."
            k.say "And I became a part of the seal inside her. My job is to keep the seal intact, but as you can see, there are some side effects as well."
            $ k.override_portrait("portrait", "shy")
            k.say "During sex your chakras immediately begin to mix. It affects the seal, my chakra suppress hers in order to protect it, and we changing places."
            $ a = 1
            jump kushina_after_sex
        "Is there any way to take her virginity?" if a == 1:
            k.say "You obviously can do it if we will be separated by force, but then most likely the beast will be free and the village will be destroyed."
            k.say "But if you want to know my opinion, she..."
            play sound "content/sfx/sound/be/light1.mp3"
            show bg story girl_room with flash
            k.say "Ah, we don't have much time left, I'm afraid..."
            play sound "content/sfx/sound/be/light1.mp3"
            show bg story girl_room with flash
            hide xxx
            show expression n.show("nude", "simple bg", "everyday", "confident", "stripping", resize=(800, 600), type="first_default") as xxx at truecenter with flash
            $ n.override_portrait("portrait", "happy")
            n.say "<yawns> That was a good nap. How did it go, [hero.name]? You had your fun? We could do it again later if you want, with the same condition..."
    label naruko_after_sex:
    $ n.override_portrait("portrait", "happy")
    menu:
        "Don't you want to do it too?":
            $ n.override_portrait("portrait", "angry")
            $ n.disposition -= 25
            n.say "It's none of your concern, mate. I don't have to report to you."
            jump naruko_after_sex
        "You tricked me!":
            n.say "<she grins> I told you I'll let you do me, and I did. It's not my fault that mom gets lonely and comes out."
            n.say "You did well by the way. Usually people just get scared and immediately run away after we change places like that."
            jump naruko_after_sex
        "Can I talk to your mother again?":
            n.say "Ooh? You getting along or something? Well, you know the drill, it will be three meals."
    hide xxx with dissolve
    show expression n_spr at center with dissolve
    "She quickly dresses up."
    n.say "Ok, see ya later. I have to run now, I have a mission."
    hide expression n_spr with dissolve
    "She left. Weird, why she doesn't lock the door?"
    "Anyway, unlikely Tsunade or anyone else can help you here. You need to talk to Kushina again." #yup, another quest to treat her 5 times
    $ n.restore_portrait()
    $ k.restore_portrait()
    $ del a
    scene black with dissolve
    stop world
    
label naruko_third_meeting:
    $ flash = Fade(.25, 0, .75, color=green)
    stop music
    stop world
    play world "Town2.ogg" fadein 2.0 loop
    scene black
    $ k = chars["Kushina_Uzumaki"]
    $ k_spr = chars["Kushina_Uzumaki"].get_vnsprite()
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    show bg hidden_village with dissolve
    show expression n_spr at center with dissolve
    $ n.override_portrait("portrait", "happy")
    n.say "Aahh, it feels good to eat for free, hehe."
    "This time she ate much more than before, as if on purpose."
    n.say "Well? Wanna have some fun with mom now? I could use some nap after lunch anyway."
    show bg story girl_room with dissolve
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
    show bg story girl_room with flash
    "As soon as you touch each other, it begins."
    play sound "content/sfx/sound/be/light1.mp3"
    show bg story girl_room with flash
    n.say "Hey, say hi to mom, ok?"
    hide xxx
    if a == 1:
        show expression k.show("sex", "straight", "partnerhidden", "indoors", "bc blowjob", "no clothes", "indifferent", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    elif a == 2:
        show expression k.show("sex", "straight", "partnerhidden", "simple bg", "bc handjob", "no clothes", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    else:
        show expression k.show("sex", "straight", "partnerhidden", "indoors", "2c anal", "no clothes", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    "Kushina enthusiastically continues to do the job..."
    scene black with dissolve
    hide xxx
    show bg story girl_room with dissolve
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
            k.say "I'm... glad to hear that. I wish I could take care of her personally."
    $ k.override_portrait("portrait", "shy")
    k.say "Let's not waste any time, I'll try to tell you all I can."
    $ k.override_portrait("portrait", "sad")
    k.say "There have been an accident several years ago. She tried to do it with a boy she liked for the first time."
    k.say "Unlike you, he was shocked and even disgusted by the transformation. Soon he severed all ties with her and left the village."
    k.say "Needless to say, it had a great impact on Naruko. She... doesn't have many friends in the village, people are afraid of her because of the sealed beast inside."
    k.say "In our dreams I tried to teach her how to maintain the seal without my help, but she quickly lost the motivation."
    $ k.override_portrait("portrait", "shy")
    play sound "content/sfx/sound/be/light1.mp3"
    show bg story girl_room with flash
    k.say "So in order to resolve the situation..."
    play sound "content/sfx/sound/be/light1.mp3"
    show bg story girl_room with flash
    "Damn, not enough time again."
    hide xxx
    show expression n.show("nude", "simple bg", "everyday", "confident", "stripping", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    n.say "<yawns> Hm, such a weird dream... Hey, [hero.name], I wanna sleep a bit more. Could you turn the lights off for me?.."
    hide xxx
    "She fell asleep. Turning off the lights, you left the house." #another 5 times eating together
    $ n.restore_portrait()
    $ k.restore_portrait()
    $ del a
    scene black with dissolve
    stop world
    
label naruko_final_meeting: 
    $ flash = Fade(.25, 0, .75, color=green)
    stop music
    stop world
    play world "main menu.mp3" fadein 2.0 loop
    scene black
    $ k = chars["Kushina_Uzumaki"]
    $ k_spr = chars["Kushina_Uzumaki"].get_vnsprite()
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    if n.disposition < 500: # by now eating so many times together should give a lot of disposition already, but just in case
        $ n.disposition = 500
    $ k.disposition += 300
    $ set_friends(hero, n)
    $ set_friends(hero, k)
    stop music
    stop world
    play world "Town2.ogg" fadein 2.0 loop
    scene black
    $ k = chars["Kushina_Uzumaki"]
    $ k_spr = chars["Kushina_Uzumaki"].get_vnsprite()
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    show bg hidden_village with dissolve
    show expression n_spr at center with dissolve
    $ n.override_portrait("portrait", "happy")
    n.say "Ehehe, food tastes better when we eat together♪"
    "For two weeks you have dinner together together. It feels like you do it for a very long time though (especially from the viewpoint of your wallet)."
    $ n.override_portrait("portrait", "shy")
    n.say "Hey, wanna go to my home? We could do... stuff."
    show bg story girl_room with dissolve
    hide expression n_spr
    show expression n.show("nude", "simple bg", "everyday", "confident", "stripping", resize=(800, 600), type="first_default") as xxx at truecenter
    "This is the third time, but for some reason she is much more nervous than before."
    $ n.override_portrait("portrait", "sad")
    n.say "Hey, [hero.name]... Do you want to meet mom again or it's about the Tsunade's mission?"
    menu:
        "I need your virginity.":
            n.say "How long are you going to do it? It's useless, I will never be able to... have sex. If you tell it Tsunade, she will understand."
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
    show bg story girl_room with flash
    $ n.override_portrait("portrait", "sad")
    show expression k.show("sex", "straight", "partnerhidden", "simple bg", "bc handjob", "no clothes", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    $ k.override_portrait("portrait", "shy")
    k.say "Hello there, [hero.name]! ♪"
    "She begins to rapidly stimulate you with her hand. Quickly bringing you to orgasm, she carefully drank every last drop."
    k.say "Ok, another round! Hey, what do think of cumshots? Want to try? Because I want to! ♪"
    menu:
        "Oh yes!":
            $ pass
        "Wait, can we talk?":
            k.say "Later!"
    "Once again she begins to rapidly stimulate you. It fells weird though, as if she carefully measures the time..."
    k.say "You did a great job lately, [hero.name]. You are not a mere stranger to her."
    play sound "content/sfx/sound/be/light1.mp3"
    show bg story girl_room with flash
    "Once again you don't have much time left."
    k.say "Hey, stay with me, ok? Hold it a bit longer. You can do it, right?"
    play sound "content/sfx/sound/be/light1.mp3"
    show bg story girl_room with flash
    "She is clearly up to something..."
    k.say "Just a few seconds... Ok, now! Come on, release it on my naked sexy body! ♪"
    hide xxx
    show expression n.show("after sex", "indoors", resize=(800, 600), type="first_default") as xxx at truecenter with flash
    "You feel how her hand disappears, but it's too late to stop."
    $ n.override_portrait("portrait", "happy")
    n.say "Wow, it's so sticky and thick! Hehe ♪"
    play sound "content/sfx/sound/be/light1.mp3"
    show bg story girl_room with flash
    "Again?"
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
    "After a series of outbreaks you see both girls in front of you."
    scene black with dissolve
    hide xxx
    hide yyy
    show bg story girl_room with dissolve
    show expression n_spr at mid_left with dissolve
    show expression k_spr at mid_right with dissolve
    $ k.override_portrait("portrait", "happy")
    $ n.override_portrait("portrait", "shy")
    k.say "Well done, [hero.name]! I know you can do it."
    n.say "I was sooo worried! I was afraid that we will break the seal for good..."
    $ n.override_portrait("portrait", "happy")
    k.say "It's ok, dear. I believed in you. And in you too, [hero.name]."
    menu:
        "It was part of the plan?":
            k.say "Of course it was. But without your help it would not have happened."
        "What's going on, actually?":
            n.say "Together we released mom from the seal! I'm so happy!"
    k.say "You have my thanks, [hero.name]. Most people would just give up on us."
    n.say "Ya see, my chakra gets all fussy when I do it. But then it gradually calms down."
    k.say "And because our chakra should always be connected, we switched places every time."
    n.say "But mom figured out how to connect us differently. Now we are connected by your white stuff..."
    $ k.override_portrait("portrait", "shy")
    k.say "It is more correct to say that we are bounded by your chakra, [hero.name]. Not by the 'white stuff', at least not only by it..."
    n.say "Hey, hey, are you two going to marry now?"
    $ k.override_portrait("portrait", "confident")
    k.say "Actually, I was thinking about giving my blessing to you two. You look good together ♪"
    $ n.override_portrait("portrait", "shy")
    n.say "Whaat? I... I need to think about it..."
    hide expression n_spr with dissolve
    k.say "She grew up so much..."
    k.say "But more importantly, you are a part of our family now, [hero.name]. And I mean more than just our common chakra." # this is another way to get Karin
    k.say "It wouldn't be possible without your support. She had to trust you as a friend or even more, otherwise this bond would never worked."
    k.say "You always will be welcomed here. Oh, and I wasn't joking about my blessing, you can dispose of her as you like."
    $ k.override_portrait("portrait", "shy")
    k.say "Of course the same goes for me, I always liked young ones ♪"
    "Well, it was worth it at very least."
    $ n.restore_portrait()
    $ k.restore_portrait()
    scene black with dissolve
    stop world