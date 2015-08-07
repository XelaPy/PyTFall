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
    # image terumi normal = ProportionalScale("content/events/Intro/terumi.png", 1700, 500)
    image carstein = ProportionalScale("content/events/Intro/Eric Carstein.png", 1700, 500)

    # image terumi reversed = Transform(ProportionalScale("content/events/Intro/terumi.png", 1600, 400), xzoom=-1)
    # image sinstar = FilmStrip('content/events/Intro/sinstar.png', (192, 192), (5, 6), 0.1, loop=True)
    # image teleport = FilmStrip('content/events/Intro/Teleport.png', (256, 256), (4, 4), 0.1, loop=False)
    # image timestop = FilmStrip('content/events/Intro/time_stop.png', (800, 800), (24, 1), 0.1, loop=False)
    image logo = ProportionalScale("content/events/Intro/logo-transperent.png", 600, 300)
    # image soldier1 kaputt = HitlerKaputt(ProportionalScale("content/events/Intro/soldier.png", 1300, 400), 50)
    image he = ProportionalScale("content/events/Intro/h1.png", 1750, 550)
    image hes = ProportionalScale("content/events/Intro/he1.png", 1750, 550)
    $ flash = Fade(.75, 0.25, .75, color=darkred)
    $ sflash = Fade(.25, 0, .25, color=darkred)
    $ t = Character("Terumi", color=green, what_color=green, show_two_window=True, show_side_image="content\events\Intro\pnterumi.png")
    $ ec = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\Intro\EricpCarstein.png")
    # transform star:
        # subpixel True
        # parallel:
            # repeated_rotate(t=0.1)
    
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
    
    play world "intro-1.mp3" fadein 2.0 fadeout 2.0
    "Through trade and seemingly endless supply of slaves from the City of Crossgate, which grew from a small provincial city into the SlaveTrade capital of the world in a matter of years, many new city states arose."
    
    show bg story dark_city with dissolve
    "One of them is PyTFall, a relatevely small town in neutral lands on the border of the Median Empire."
    
    show bg city_jail with dissolve
    "It was a time when slaves had less rights than pets..."
    extend " They were severely punished and could executed on spot by their masters without reprecussions for the slightest infraction."
    
    show bg story slq with dissolve
    "Cruelty and lust for power of the Masters knew no bounds and they carelessly kept breeding and buying more and more slaves..."
    extend " and soon found themselves outnumbered ten to one."
    
    "They say there were those who sympathized with the oppressed. Those who gave them weapons and magic to fight back. "
    show bg story firetome with ImageDissolve("content/gfx/masks/m21.jpg", 2)
    extend "To resist!"

    show bg story war with dissolve
    "Riots happened one after the other. It is easy to take up arms when you have nothing to lose."
    "First few incedents were violently suppresed by the Masters..."
    extend " but it was too late."
    "The conflict quickly turned into a full scale warfare."
    
    show bg story p2 with dissolve:
        subpixel True
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        linear 30 crop (config.screen_width/2, config.screen_height/2, config.screen_width/8, 100)
    show he with dissolve:
        yalign 1.0 xpos 400
    "Then out of nowhere a stranger appeared, claiming to be a historian."
    "He told the Master of underground sanctuary not too far from the city, where an ancient star slept."
    show bg story ruin1 with dissolve:
        subpixel True
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        linear 30 crop (config.screen_width/2, config.screen_height/2, config.screen_width/8, 100)
    show hes with dissolve:
        xpos 400 yalign 1.0
    "A dreadful weapon, capable of unimaginable destruction"
    show bg story ruin2 with dissolve:
        subpixel True
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        linear 30 crop (config.screen_width/2, config.screen_height/2, config.screen_width/32, 100)
    extend " and of crushing the rebels once and for all..."
    "Carrying enough power to build a new empire and maybe, even to surpass Crossgates wealth and fame..."
    
    show bg story ruin2:
        linear 3 alpha 0
    show hes:
        linear 3 alpha 0
    $ renpy.pause (3.0, hard=True)
    play world "tremor.mp3" fadein 2.0 fadeout 2.0
    scene black with dissolve
    show bg story dark_city with dissolve
    pause 1.0
    show layer master at damage_shake(0.05, (-10, 10))
    pause 2.0
    show layer master
    $ renpy.pause (1.0, hard=True)
    show bg story sky1 with wipedown:
        alpha 0
        linear 2.0 alpha 1.0
    $ renpy.pause (1.0, hard=True)
    play music "content/sfx/music/intro-2.mp3" fadeout 2.0
    show bg story sky2 with flash
    show layer master at damage_shake(0.05, (-10, 10))
    pause 2.0
    show layer master
    show bg story sky2 with sflash
    pause 1.0
    show bg story sky2 with sflash
    pause 1.0
    show bg story sky3 with flash
    pause 1.0
    show bg story sky3 with sflash
    pause 1.0
    show bg story ash2 with wipeup:
        alpha 0
        linear 2.0 alpha 1.0
    pause 2.0
    show bg story ash2:
        subpixel True
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        linear 10 crop (config.screen_width/2, config.screen_height/2, config.screen_width/16, config.screen_height/16)
    pause 5.0
    scene bg story ash1 with dissolve:
        subpixel True
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        linear 10 crop (config.screen_width/2, config.screen_height/2, config.screen_width/16, config.screen_height/16)
    pause 0.5
    $ renpy.show("logo", at_list=[szoom(0.5, 2, 8), Transform(pos=(0.5, 0.75), subpixel=True)])
    $ renpy.with_statement(dissolve)
    pause 4.5
    return
    

label intro_story2:
    $ ec = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\Intro\EricpCarstein.png")
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
    $ ec = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\Intro\EricpCarstein.png")
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
    
label intro_story_sk: # this label goes when MC goes to Sakura's house after it becomes available
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
    play world "Field2.ogg" fadein 2.0 loop
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
    # $ npc1 = Character("Terumi", color=green, what_color=green, show_two_window=True, show_side_image="content\events\Intro\pnterumi.png")
    # npc1 "Meow!"
    # t "Or not?"
    # "Note that all the good stuff is written as comments in examples.rpy file and you will not be able to see it from the game!"
    # "There is also a very good tutorial availible if you download Ren'Py SDK kit (less than 30 MB and does not require instalation)!"
    # "You should get SDK if you want to develop content for PyTFall. It's not really a 'MUST HAVE' but it's most definetly a should have :)'"
    # "There will be a great demonstration tutorial there of what the engine is capable of! This shows similar things but those that are more relevant to {color=[red]}PyTFall{/color}!"
    # {color=[red]}Text{/color} changes something about text styling! You can use a lot here... like {b}Text{/b} will write text in bold!
    # You can check all properties by googling RenPy + Text + Style + Properties
    
    # return
