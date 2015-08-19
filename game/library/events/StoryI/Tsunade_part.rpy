# after a couple days mc gets a paper airplane with instructions written to meet with kunoichi ub the forest
init:
    $ noisedissolve = ImageDissolve(im.Tile("content/events/StoryI/noisetile.png"), 1.0, 1)
    image orig_2 = ProportionalScale("content/items/quest/orig_2.png", 150, 150)
    image scroll = ProportionalScale("content/items/cons/scr_ice.png", 150, 150)
    image ling = ProportionalScale("content/items/quest/ling.png", 150, 150)
    image protector = ProportionalScale("content/items/quest/konan_protector.png", 150, 150)
    image blossoms = SnowBlossom("content/items/quest/paper.png", count=125,  border=50, xspeed=(20, 50), yspeed=(100, 200), start=0, horizontal=True)
label intro_story:
    stop music
    stop world
    $ first_try = 1
    $ k = chars["Konan"]
    $ k_spr = chars["Konan"].get_vnsprite()
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
    $ string = ""
    $ a = 0
    label hidden_village_enter:
    
    menu:
    
        "You need to perform five signs."
    
        "Bird":
            $ string += "a"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Boar":
            $ string += "b"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Dog":
            $ string += "c"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Dragon":
            $ string += "d"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Ox":
            $ string += "e"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Tiger":
            $ string += "f"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Snake":
            $ string += "g"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Rat":
            $ string += "h"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Horse":
            $ string += "i"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Monkey":
            $ string += "j"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Hare":
            $ string += "k"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
        "Ram":
            $ string += "l"
            $ a += 1
            if a < 5:
                jump hidden_village_enter
    if string != "dkfga":
        "Nothing happens. You probably made a mistake."
        $ first_try = 0
        jump hidden_village_enter_again
    else:
        "You feel like the world around you changes."
        stop world fadeout 2.0
        play world "park3.mp3" fadein 2.0
        show bg hidden_village with noisedissolve
    "You stand in the middle of a small village."
    if first_try == 1:
        s.say "See? Told you he would not just stare at my chest and get it."
    else:
        $ i.override_portrait("portrait", "happy")
        i.say "Wow. I can't believe took so long. Like I said, he just stared at your chest instead of listening."
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
            t.say "Oh? That sounds.... not bad."
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
    "Here we give quest to rise vaginal skill, let's say, to 200, and return to the hidden village after that."
    scene black with dissolve
    stop world