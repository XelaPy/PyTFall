init python:
    qtsunade = register_quest("Medic's Request")
    register_event("intro_storyi_entervillage", quest="Medic's Request", run_conditions=[qtsunade.condition(0, True)], locations=["forest_entrance"], dice=100, max_runs=1)
init:
    $ noisedissolve = ImageDissolve(im.Tile("content/events/StoryI/noisetile.png"), 1.0, 1)
    image orig_2 = ProportionalScale("content/items/quest/orig_2.png", 150, 150)
    image scroll = ProportionalScale("content/items/cons/scr_ice.png", 150, 150)
    image ling = ProportionalScale("content/items/quest/ling.png", 150, 150)
    image protector = ProportionalScale("content/items/quest/konan_protector.png", 150, 150)
    image blossoms = SnowBlossom("content/items/quest/paper.png", count=125,  border=50, xspeed=(20, 50), yspeed=(100, 200), start=0, horizontal=True)
    
label tsunade_request_part_one(event):
    "Your skill now should be sufficient to pass Tsunade exam. You should return to the Hidden Village."
    $ pytfall.world_quests.get(event.quest).next_in_label("Your skill now should be sufficient to pass Tsunade exam. You should return to the Hidden Village.", "part2")
    $ pytfall.world_events.kill_event("tsunade_request_part_one")
    $ register_event_in_label("story_tsunade_first_meeting", trigger_type="auto", locations=["hiddenvillage_entrance"], dice=100, max_runs=1)
    $ pytfall.world_events.force_event("story_tsunade_first_meeting")
    return
    
label intro_storyi_entervillage(event):
    stop music
    stop world
    $ first_try = 1
    $ s = chars["Sakura"]
    $ i = chars["Ino_Yamanaka"]
    $ s_spr = chars["Sakura"].get_vnsprite()
    $ i_spr = chars["Ino_Yamanaka"].get_vnsprite()
    $ t = chars["Tsunade"]
    $ t_spr = chars["Tsunade"].get_vnsprite()
    play world "forest_entrance.mp3" fadein 2.0 loop
    show bg forest_bg_1 with dissolve
    show expression s_spr at center with dissolve
    $ s.override_portrait("portrait", "confident")
    s.say "Listen carefully, [hero.name]. This clearing is one of the places where you can enter the village."
    s.say "I'm going to show you hand signs you need to perform in order to enter. Make sure you remember them!"
    "Her fingers weaved into intricate shapes."
    s.say "Look, first is Dragon, then Hare, Tiger, Snake and Bird."
    "...They don't look like animals at all. Kunoichi must have a wonderful imagination."
    menu:
        "Ask to show one more time":
            s.say "First is Dragon, then Hare, Tiger, Snake and Bird."
        "I get it":
            $ s.disposition += 5
            s.say "Good."
    s.say "Now try to perform it like I do."
    hide expression s_spr with noisedissolve
    "She quickly makes the signs and dissolves in the air."
    "You should try to do it as well."
    label hidden_village_enter_again:
    $ string_value = ""
    $ a = 0
    label hidden_village_enter:
    
    menu:
    
        "You need to perform five signs."
    
        "Bird":
            $ string_value += "a"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Dragon":
            $ string_value += "b"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Tiger":
            $ string_value += "c"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Snake":
            $ string_value += "d"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Hare":
            $ string_value += "e"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
    if string_value != "becda":
        "Nothing happens. You probably made a mistake."
        $ first_try = 0
        jump hidden_village_enter_again
    else:
        "You feel like the world around you changes."
        stop world fadeout 2.0
        play world "park3.mp3" fadein 2.0
        show bg hiddenvillage_entrance with noisedissolve
    "You stand in the middle of a small village."
    if first_try == 1:
        s.say "See? Told you he would not just stare at my chest and get it."
        $ s.disposition += 5
    else:
        $ i.override_portrait("portrait", "happy")
        i.say "Wow. I can't believe it took so long. Like I said, he just stared at your chest instead of listening."
        $ i.disposition += 5
    show expression s_spr at mid_left
    show expression i_spr at mid_right
    show expression t_spr at center 
    with dissolve
    $ t.override_portrait("portrait", "confident")
    t.say "Now, now. Let's see what do we have here."
    "You see an unknown woman standing next to the kunoichi. She looks at you very carefully."
    t.say "Hmm. I suppose it will do. We can't be too picky these days, can we?"
    "You try to say something, but she interrupts you."
    t.say "The girls told me why are you here. We need to discuss it, but not here. And you girls a have job to do, right?"
    $ s.override_portrait("portrait", "indifferent")
    $ i.override_portrait("portrait", "indifferent")
    s.say "Ok, granny."
    i.say "Yeah-yeah. See you later, [hero.name]."
    hide expression s_spr
    hide expression i_spr
    $ s.restore_portrait()
    $ i.restore_portrait()
    with dissolve
    t.say "Now come with me."
    show bg story cab_1 with dissolve
    t.say "Make yourself at home, [hero.name]. Call me Tsunade."
    $ t.override_portrait("portrait", "indifferent")
    label first_tsunade_diag:
    menu:
        "Ask about the village":
            t.say "We call it the hidden village. Once it had another name, but it became meaningless after other villages disappeared."
            t.say "If you want to know more, you should earn our trust at first."
            jump first_tsunade_diag
        "Ask about Sakura calling her granny":
            t.say "It is more of an adopted title. She is my pupil, but I raised her as my own granddaughter."
            jump first_tsunade_diag
        "Ask about the ruins":
            t.say "Indeed, out village sealed those ruins. It was another mission given to us, and a well paid one."
    $ t.override_portrait("portrait", "confident")
    t.say "But before we'll do something for you, let's talk about something you can do for us."
    t.say "I am the head medic for the village. As such, it is my position to watch over certain... customs."
    t.say "Tell me, have you ever been with a girl?"
    menu:
        "Yes":
            t.say "Good."
        "No":
            $ t.override_portrait("portrait", "shy")
            t.say "Oh? How... interesting."
            $ t.disposition += 25
        "Don't answer":
            t.say "Don't be shy. Shyness is a bad quality for something you should do for us."
            $ t.disposition -= 25
    $ t.override_portrait("portrait", "confident")
    t.say "Well, here in the hidden valley, we have an older custom. When a female ninja qualifies for the jobs above a certain clearance, there is a real danger that she gets captured. And while you are a man, you do know that females do get a 'special treatment', right?"
    t.say "Back in my days, we kept it in the family. Don't look at me like that. You usually had an older member of the family, that liked the young ninja a lot, and that agreed to , you know."
    t.say "That was back then, but now, things are different. I have all the young girls, and each and everyone of them has their own head. They have brothers, uncles, friends of the family... But the problem is, they have all those modern ideas about finding love outside."
    $ t.override_portrait("portrait", "indifferent")
    t.say "I am not asking you to rape them, or to force yourself on them. If you get idea, it would be a miracle if you survive the attempt. I am just afraid that they will... get hurt."
    t.say "Their first time should be with someone that they trust, someone that has shown them how beautiful a thing this can be. Not some slobbering pimply faced boy that has to drink his courage, pukes all over their dresses, and then can't get it up."
    t.say "I want my girls to have a first time that will stay with them forever, and that will shield them against all the bad sex they will have. A woman can go through much if she has good memories. Good memories carry you through being imprisoned, captured, and a whole lot more."
    t.say "Before that, however, I need to make sure you know what to do. Like I said, they shouldn't get hurt, so you need a certain experience in this matter."
    $ t.override_portrait("portrait", "shy")
    t.say "Come to me when you are ready and well rested, and I'll test you. You you pass my exam and take care of a certain number of my girls, I'll get the ruins entrance cleared for you."
    $ pytfall.world_quests.get(event.quest).next_in_label("Tsunade, the head medic of the village, wants to test your sex skill. Return to her when you are ready.", "part1")
    $ pytfall.world_events.kill_event("intro_storyi_entervillage")
    $ register_event_in_label("tsunade_request_part_one", quest=event.quest, trigger_type="auto", locations=["all"], run_conditions=["hero.get_skill('vaginal') >= 200"], dice=0, max_runs=1)
    $ t.restore_portrait()
    $ del first_try
    $ del a
    $ del string_value
    scene black with dissolve
    stop world
    jump forest_entrance
    
label story_tsunade_first_meeting(event):
    $ t = chars["Tsunade"]
    $ t_spr = chars["Tsunade"].get_vnsprite()
    $ a = 0
    stop music
    play world "town2.ogg" fadein 2.0 loop
    show bg cafe with dissolve
    show expression t.show("sfw", "indoors", "profile", "rest", "public", "confident", "suggestive", "everyday", resize=(800, 600), type="first_default") as xxx at truecenter
    $ t.override_portrait("portrait", "suggestive")
    t.say "Lets just say sometimes, I just happened to slip, and accidentally get captured, because I liked the way certain of the guards looked. Strong, well in shape, nice big hands.... "
    "Your second visit to the hidden village led you to the local bar."
    t.say "What? I used to be a hormone crazed teenager once as well. And we are pretty good at training our girls how to escape almost anything. Plus, women like me have urges as well..."
    "The head medic was pretty drunk already when you arrived."
    t.say "Come on, drop that look, young man. I know, modern morals, but who do you prefer? Some silly little goose that barely knows what she is doing, or some older, more.... experienced woman that can take care of you?"
    "And she kept drinking for awhile now, until staff had gone home, leaving you two alone."
    t.say "Let's look at it that way: you are hormone crazed, they are hormone crazed, and you have the word of a head medical professional that these encounters will remain without consequence. Take as much or as little time as you need, and work your magic..."
    hide xxx
    show expression t.show("nude", "stripping", "indoors", "confident", "happy", "everyday", resize=(800, 600), type="first_default") as xxx at truecenter
    "Without any warning with fast, confident movement she stripped the upper part of her body."
    t.say "What do you think? I grow them myself. I used to be flat as a board, but medical techniques can improve many things. One day Sakura may have a pair of decent boobs as well."
    hide xxx
    show expression t.show("nude", "stripping", "indoors", "shy", "no clothes", resize=(800, 600), type="first_default") as xxx at truecenter
    t.say "Let's make it quick. I don't want you to spend too much energy on me, not before you finish with my task."
    t.say "Come on, young man. Your exam starts now. Pick your pose."
    menu:
        "On top":
            t.say "Oh? You like to be taken care of, just I thought. Lovely."
            $ a = 1
        "Missionary":
            t.say "You think you can handle it? Very well, as you wish."
            $ a = 2
        "Doggy":
            t.say "Want to to all the job by yourself? Let's see what you are made of."
            $ a = 3
    hide xxx
    if a == 1:
        show expression t.show("sex", "normalsex", "indoors", "shy", "no clothes", "partnerhidden", "ontop", resize=(800, 600), type="first_default") as xxx at truecenter
        "She sits on you."
    elif a == 2:
        show expression t.show("sex", "normalsex", "ecstatic", "indoors", "shy", "everyday", "partnerhidden", "missionary", resize=(600, 800), type="first_default") as xxx at truecenter
        "She lies on her back and spreads her legs."
    elif a == 3:
        show expression t.show("sex", "normalsex", "ecstatic", "indoors", "spooning", "no clothes", "partnerhidden", resize=(800, 600), type="first_default") as xxx at truecenter
        "She lies on her stomach, waiting for you to tahe the action."
    "As you enter and begin to move, you feel like being palpated by walls inside of her. It feels strange, but very good."
    t.say "Drop that look, young man. I'm a doctor, it's my job to make sure that you are healthy. Focus on your job, it becomes cold here."
    "Pulling yourself together, you manage to hold out long enough to make her come."
    hide xxx
    $ t.override_portrait("portrait", "shy")
    show expression t.show("nude", "simple bg", "ecstatic", "indoors", "shy", "everyday", "partnerhidden", "missionary", resize=(600, 800), type="first_default") as xxx at truecenter
    if hero.vaginal >= 400:
        t.say "You have a decent skill, [hero.name]. Not bad for someone in your age."
    else:
        t.say "I can say you lack practice, [hero.name]. But it should be enough for your task."
    t.say "You have my permission to freely operate on the territory of the village."
    t.say "Take care of all young kunoichi it the village, and you will have your access to the ruins."
    t.say "That's all, you may go now, I need some rest."
    "She is going to sleep right here?.."
    hide xxx with dissolve
    show bg hiddenvillage_entrance with dissolve
    "Looks like you have a lot of work to do. Better start as soon as possible."
    $ del a
    $ t.restore_portrait()
    $ pytfall.world_quests.get("Medic's Request").next_in_label("You passed Tsunade's exam. Now you need to find and deflower four kunoichi.", "part3")
    $ pytfall.world_events.kill_event("story_tsunade_first_meeting")
    $ register_event_in_label("story_tsunade_second_meeting", quest="Medic's Request", trigger_type="auto", locations=["all"], run_conditions=["not(pytfall.world_quests.check_quest_not_finished('Sixth Sense', 'Stubborn Kunoichi', 'Uzumaki Clan', 'Weapons Specialist')"], dice=0, max_runs=1)
    scene black with dissolve
    stop world
    return

label story_tsunade_second_meeting(event):
    $ t = chars["Tsunade"]
    $ t_spr = chars["Tsunade"].get_vnsprite()
    stop music
    stop world
    play world "town2.ogg" fadein 2.0 loop
    show bg story cab_1 with dissolve
    show expression t_spr at center with dissolve
    $ t.override_portrait("portrait", "indifferent")
    "Tsunade attentively listening as you report in detail about your success. It took some time, but you managed to take care of young kunoichi in the village."
    "Unfortunately, some of them weren't in the village at the moment, like Ino and Sakura, but there is nothing you can do about it."
    t.say "I see. Well done, [hero.name]. You fulfilled your part of the bargain, and I will do the same. From now on the ruins will not be sealed."
    t.say "You are still welcomed in the village, of course. And you have my permission to hire those five kunoichi you took care of."
    $ chars["Tenten"].set_flag("quest_cannot_be_hired", value=False)
    $ chars["Temari"].set_flag("quest_cannot_be_hired", value=False)
    $ chars["Karin"].set_flag("quest_cannot_be_hired", value=False)
    $ chars["Kushina_Uzumaki"].set_flag("quest_cannot_be_hired", value=False)
    $ chars["Naruko_Uzumaki"].set_flag("quest_cannot_be_hired", value=False)
    # at this point you can send expedition to new zone in SE
    $ t.restore_portrait()
    $ pytfall.world_quests.get(event.quest).finish_in_label("You finished Tsunade's mission and now can enter the ruins.", "complete")
    $ pytfall.world_events.kill_event("story_tsunade_second_meeting")
    scene black with dissolve
    return
    stop world