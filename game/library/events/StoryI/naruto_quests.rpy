init python:
    q = register_quest("A Fugitive")
    # register_event("drunk_lady1", quest="Drunk Lady", locations=["tavern_inside"], dice=100, restore_priority=0, jump=True)
    register_event("naruko_first_meeting", quest="A Fugitive", simple_conditions=["hero.level >= 20", "hero.gold >= 1000"], locations=["cafe"], dice=100, restore_priority=0, jump=True, trigger_type="auto")
# label drunk_lady1:
    # $ t = chars["Tsunade"]
    # scene bg tavern_inside # ChW: This is to get rid of tavent picture until I create a more complex solution...
    # show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter with dissolve:
        # zoom 0.7
    # "Examining the room, you notice a middle aged woman with impressive knockers drinking alone in the corner."
    # menu:
        # "Maybe you could join her?"
        # "Definitely":
            # show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter:
                # zoom 0.7
                # linear 1 zoom 1.0
            # "Getting a drink, you sit next to her."
            # $ t.override_portrait("portrait", "suggestive")
            # t.say "Let's see what do we have here. Hmm... I suppose it will do. We can't be too picky these days, can we?"
            # "She is clearly drunk."
            # t.say "Call me Tsunade. No last names, I'm too old for this shit."
            # "You try to say something, but she interrupts you."
            # t.say "Come on, drop that look, young man. I know, modern morals, but who do you prefer? Some silly little goose that barely knows what she is doing, or some older, more... experienced woman that can take care of you?"
            # show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter:
                # zoom 1.0
                # linear 0.5 zoom 1.1
                # linear 0.5 zoom 1.0
            # "She seductively pushes her huge boobs towards you."
            # t.say "I just... need some money to pay off a gambling debt. One thousand coins."
            # if hero.gold >= 1000:
                # menu:
                    # "Do you want to give her 1000 coins?"
                    # "Hell yeah":
                        # $ pytfall.world_quests.get("Drunk Lady").next_in_label("You've met a woman with huge knockers who proposed you her body for gold. An excellent deal.")
                        # $ pytfall.world_events.kill_event("drunk_lady1", cached=True)
                        # "She quickly hides your coins."
                        # $ hero.gold -= 1000
                        # t.say "Niiice. Tell you what, I have a room here on the second floor."
                        # t.say "I'll wait you there..."
                        # "She stands up and unsteadily goes to the second floor. It's going to be interesting."
                        # hide x with dissolve
                        # jump drunk_lady_quest_scene
                    # "No way":
                        # "She shrugs with disappointment."
                        # t.say "A shame. Back to my drink then."
                        # $ pytfall.world_quests.get("Drunk Lady").next_in_label("You've met a woman with huge knockers who proposed you her body for 1000 gold coins. You refused, for now.")
                        # $ pytfall.world_events.kill_event("drunk_lady1", cached=True)
                        # $ register_event_in_label("drunk_lady2", quest="Drunk Lady", locations=["tavern_inside"], dice=0, restore_priority=0, run_conditions=["hero.gold >= 1000"], jump=True)
                        # $ pytfall.world_events.force_event("drunk_lady2")
                        # hide x with dissolve
            # else:
                # "Unfortunately, you don't have that amount of gold at the moment."
                # t.say "I see... My proposition still stands. You know where to find me."
                # "She returns to her drink."
                # $ pytfall.world_quests.get("Drunk Lady").next_in_label("You've met a woman with huge knockers who proposed you her body for 1000 gold coins. Sadly, you couldn't afford her.")
                # $ pytfall.world_events.kill_event("drunk_lady1", cached=True)
                # $ register_event_in_label("drunk_lady2", quest="Drunk Lady", locations=["tavern_inside"], restore_priority=0, dice=0, run_conditions=["hero.gold >= 1000"], jump=True)
                # $ pytfall.world_events.force_event("drunk_lady2")
                # hide x with dissolve
        # "Maybe another time":
            # "Perhaps some another day."
    # hide x with dissolve
    # $ t.restore_portrait()
    # jump tavern_inside
    
# label drunk_lady2:
    # $ t = chars["Tsunade"]
    # scene bg tavern_inside
    # show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter with dissolve:
        # zoom 0.7
    # "You see the woman you met before. If you want, you can accept her proposition and pay 1000 coins."
    # menu:
        # "Pay her?"
        # "Yes":
            # show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter:
                # zoom 0.7
                # linear 1 zoom 1.0
            # "You sit next to her as she friendly nods, and gave her a purse of gold."
            # $ t.override_portrait("portrait", "suggestive")
            # $ hero.gold -= 1000
            # t.say "Niiice. Tell you what, I have a room here on the second floor."
            # t.say "I'll wait you there..."
            # "She stands up and unsteadily goes to the second floor."
            # $ pytfall.world_quests.get("Drunk Lady").next_in_label("You paid Tsunade and she invited you to her room on the second floor.")
            # $ pytfall.world_events.kill_event("drunk_lady2", cached=True)
            # jump drunk_lady_quest_scene
        # "No":
            # "Maybe some other time."
    # hide x with dissolve
    # $ t.restore_portrait()
    # jump tavern_inside
    
# label drunk_lady_quest_scene:
    # $ t = chars["Tsunade"]
    # $ t_spr = chars["Tsunade"].get_vnsprite()
    # $ t.override_portrait("portrait", "indifferent")
    # scene black with dissolve
    # stop music fadeout 1.0
    # stop world fadeout 1.0
    # play world "town2.ogg" fadein 1.0 loop
    # show bg girl_room_4 with dissolve
    # "You follow her to her room. It's definitely not the cheapest room in the tavern, but on the other hand the best rooms are located on the third floor."
    # show expression t_spr at center with dissolve
    # t.say "Well then, now we can talk. No one can here us here."
    # "You still can feel how she reeks of alcohol, but she doesn't look drunk at all. She smirks looking at your puzzled face."
    # $ t.override_portrait("portrait", "confident")
    # t.say "I have a proposition for you, [hero.name]. I used to know your father, we helped each other a lot in the past. But since he's gone, I was hoping you can do me a small favor instead of him."
    # $ t.override_portrait("portrait", "indifferent")
    # t.say "You see, until recently I used to lead a ninja clan here in the city. But they said I was too committed to traditions, and picked another leader."
    # t.say "It's simple. Help me to regain position as the clan leader, and you will get full clan support plus a few hot young kunoichi to have fun with ♫"
    # t.say "I'm not forcing you or something, you can do as you please. But think about the possibilities first."
    # "The possibilities are promising indeed."
    # t.say "I even can return your money..."
    # $ t.override_portrait("portrait", "confident")
    # t.say "...or work them out, if you prefer that ♥"
    # menu:
        # "Money":
            # $ t.override_portrait("portrait", "indifferent")
            # t.say "Damn, I hoped you'll pick the other option... Here."
            # "She returns your gold."
        # "Sex":
            # $ t.override_portrait("portrait", "happy")
            # t.say "Nice! It's been awhile..."
            # hide expression t_spr with dissolve
            # show expression t.show("00B1-nd-e2-e5-c1-l4-a1.jpg", resize=(800, 600)) as x at truecenter with dissolve
            # $ t.override_portrait("portrait", "suggestive")
            # t.say "...but I think I still remember how to do it. What do you think? I grow them myself. I used to be flat as a board, but medical techniques can improve many things ♥"
            # show expression t.show("0025-sx-e6-c8-l2-ns-p3-p2-sn-su.jpg", resize=(800, 600)) as x at truecenter with dissolve
            # "Without further ado she kneels down and masterfully brings you to the finish. You feel that you learned a thing a two about sex."
            # $ hero.sex += 50
            # $ hero.health = hero.get_max("health")
            # $ hero.mp = hero.get_max("mp")
            # $ hero.vitality = hero.get_max("vitality")
            # hide x with dissolve
            # show expression t_spr at center with dissolve
            # $ t.override_portrait("portrait", "confident")
            # t.say "Oh, that was quick. You have a long way to go if you wish to surpass you father ♫"
    # $ t.override_portrait("portrait", "indifferent")
    # t.say "That aside... You first task is to take care of two kunoichi here in the city. Eh, you know what kunoichi is, right? It's basically a female ninja."
    # $ t.override_portrait("portrait", "confident")
    # t.say "And by taking care I mean to pop their cherries, if you catch my meaning."
    # $ t.override_portrait("portrait", "indifferent")
    # t.say "I am not asking you to rape them, or to force yourself on them. If you get idea, it would be a miracle if you survive the attempt."
    # t.say "We should avoid unneeded attention, find me in the tavern only after you finish with it. So long..."
    # hide expression t_spr with dissolve
    # $ t.restore_portrait() 
    # "She leaves. You notice at the table nearby a package of documents with information about your 'targets'."
    # $ pytfall.world_quests.get("Drunk Lady").finish_in_label("Turns out Tsunade has a mission for you. You probably should accept it.", "complete")
    # # if we allow here to refuse, it will make the village and all characters inside unavailable forever. so yeah, it will be linear.
    # scene black
    # jump tavern_inside
    
label naruko_first_meeting:
    $ hero.AP -=1
    if global_flags.flag("waitress_chosen_today") != day:
        $ cafe_waitress_who = choice(["npc cafe_mel_novel", "npc cafe_monica_novel", "npc cafe_chloe_novel"])
        $ global_flags.set_flag("waitress_chosen_today", value=day)
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    $ waitress = Character("Waitress", color=white, what_color=white, show_two_window=True)
    show expression Transform(cafe_waitress_who, zoom=0.7) at center
    show expression n_spr at right
    with dissolve
    
    waitress "Welcome to the Ca... Oh, it's you again."
    $ n.override_portrait("portrait", "angry")
    n.say "What's wrong with you, people? I just want some food!"
    waitress "Like I said, the food is not free. Get a work if you don't have money."
    n.say "But I have money! Look!"
    "She demonstrates a bag of coins. It's clearly not gold."
    waitress "I'm sorry, Naruko, but we only accept gold. These coins are worthless here."
    hide expression Transform(cafe_waitress_who, zoom=0.7) with dissolve
    $ n.override_portrait("portrait", "sad")
    n.say "Man, this sucks... I'm starving..."
    hide n_spr with dissolve
    $ pytfall.world_quests.get("A Fugitive").next_in_label("You've met a weird starving girl near the cafe. Perhaps you could offer help?")
    $ pytfall.world_events.kill_event("naruko_first_meeting", cached=True)
    jump cafe
    
label naruko_first_feeding:
    $ renpy.hide(cafe_waitress_who)
    with dissolve
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    $ waitress = Character("Waitress", color=white, what_color=white, show_two_window=True)
    show expression n_spr at center with dissolve
    if pytfall.world_quests.check_stage("A Fugitive") == 1:
        $ n.override_portrait("portrait", "sad")
        n.say "What is it?"
        hero.say "You ask her if she is in trouble."
        $ n.override_portrait("portrait", "indifferent")
        n.say "Uhh, maybe a little. I have not eaten for four days, and no one wants my money, and this damn city is so big I keep going astray, ha ha..."
        hero.say "You propose to help her with money."
        $ n.override_portrait("portrait", "happy")
        n.say "For real? That's awesome! I'm fine though, I just need some food to restore my strength."
        hero.say "You call the waitress and offer Naruko to make an order."
        $ cost = randint(190, 210)
        if hero.take_money(cost):
            $ name = "content/gfx/images/food/animated/big_" + str(renpy.random.randint(1, 3)) + ".webm"
            show image Movie(channel="main_gfx_attacks", play=name) at truecenter with dissolve
        waitress "It will be [cost] gold, thank you very much!"
        hide image Movie(channel="main_gfx_attacks", play=name) with dissolve
        "It cost you more than you expected. She ate a whole mountain of food."
        n.say "Aaaah, it feels so good... You are a lifesaver!"
        $ n.disposition += 100
        n.say "I'll repay you, I promise. Let's meet here tomorrow, ok?"
        hide expression n_spr with dissolve
        $ pytfall.world_quests.get("A Fugitive").next_in_label("You paid for her food. Perhaps later you will meet her again at the same place.")
        $ n.set_flag("quest_ate_in_cafe", value=day)
    elif pytfall.world_quests.check_stage("A Fugitive") == 2:
        $ n.override_portrait("portrait", "happy")
        n.say "Sup, [hero.name]! Feeling good?"
        $ hero.set_flag("ate_in_cafe", value=day)
        n.say "Yesterday I tried to find a job, but lost and ended up in a huge garden. It was sooo cool! There were those red flowers everywhere, and they smelled so funny! Here, I got one for you too!"
        $ hero.add_item ("Red Rose")
        "She gives you a red rose. There is only one place in the city where they grow in a garden, called royal gardens."
        "Now it's too dangerous to hire her or give her a room since she could be wanted for illegal entry. They will look for her for weeks."
        hide expression our_image with dissolve
        n.say "I wanted to stay there a bit more, but some angry people showed up and chased me away..."
        n.say "Anyway, I'm really hungry! Let's eat!"
        $ cost = randint(100, 150)
        if hero.take_money(cost):
            $ name = "content/gfx/images/food/animated/big_" + str(renpy.random.randint(1, 3)) + ".webm"
            show image Movie(channel="main_gfx_attacks", play=name) at truecenter with dissolve
        "You order some food too, and you eat together as she tells you about her misadventures in the city."
        hide image Movie(channel="main_gfx_attacks", play=name) with dissolve
        waitress "It will be [cost] gold, thank you very much!"
        $ n.disposition += 50
        n.say "Aaaah, so tasty! See ya around!"
        hide expression n_spr with dissolve
        $ n.set_flag("quest_ate_in_cafe", value=day)
        $ pytfall.world_quests.get("A Fugitive").next_in_label("You've met again. She's still broke.")
    elif pytfall.world_quests.check_stage("A Fugitive") == 3:
        $ n.override_portrait("portrait", "happy")
        $ hero.set_flag("ate_in_cafe", value=day)
        n.say "Hey, [hero.name]! Look what I've found!"
        "She handles you a small gem."
        $ hero.add_item ("Amethyst")
        n.say "I've found a really huge river and wanted to swim. But there were big waves, and one of them..."
        "There are no rivers near the city. She must be talking about the ocean."
        $ n.override_portrait("portrait", "shy")
        n.say "Well, it took my bra. I tried to find it, but instead found a small underwater cave with this pretty stone. You can have it."
        $ n.override_portrait("portrait", "happy")
        n.say "Oh well, I can live without it anyway. I still have the remaining clothes. Let's eat."
        $ cost = randint(100, 150)
        $ n.disposition += 50
        if hero.take_money(cost):
            $ name = "content/gfx/images/food/animated/big_" + str(renpy.random.randint(1, 3)) + ".webm"
            show image Movie(channel="main_gfx_attacks", play=name) at truecenter with dissolve
        "You order some food too, and you eat together as she tells you about her misadventures at the beach."
        hide image Movie(channel="main_gfx_attacks", play=name) with dissolve
        waitress "It will be [cost] gold, thank you very much!"
        n.say "Aaaah, so tasty! See ya around!"
        hide expression n_spr with dissolve
        $ n.set_flag("quest_ate_in_cafe", value=day)
        $ pytfall.world_quests.get("A Fugitive").next_in_label("She's lost her bra, but found a gem for you.")
    elif pytfall.world_quests.check_stage("A Fugitive") == 4:
        $ n.override_portrait("portrait", "happy")
        $ hero.set_flag("ate_in_cafe", value=day)
        n.say "[hero.name]! Doing alright?"
        n.say "This place is so big! And it's never boring here, unlike my home."
        hero.say "You ask about her home."
        $ n.override_portrait("portrait", "indifferent")
        n.say "Oh, it's just a small, boring village. Nothing ever happens there, and they don't allow us to leave it too."
        n.say "So, you know, I said 'screw it' and ran away. I'm not gonna waste my life hiding in a bushes when there is a huge, amazing world around."
        $ n.override_portrait("portrait", "happy")
        n.say "No matter. Hey, let's try those cupcakes, they look awesome!"
        $ n.disposition += 50
        $ n.override_portrait("portrait", "happy")
        $ cost = randint(100, 150)
        if hero.take_money(cost):
            $ name = "content/gfx/images/food/animated/big_" + str(renpy.random.randint(1, 3)) + ".webm"
            show image Movie(channel="main_gfx_attacks", play=name) at truecenter with dissolve
        "You order some food too, and you eat together. You trying to find out more about her homeland, but she quickly changes the subject, and bombards you with questions about the city."
        hide image Movie(channel="main_gfx_attacks", play=name) with dissolve
        waitress "It will be [cost] gold, thank you very much!"
        n.say "Mmm, delicious! Hey, we should go to the beach together sometime, what do you say?"
        $ n.override_portrait("portrait", "shy")
        n.say "I mean, after I get another swimsuit..."
        hide expression n_spr with dissolve
        $ n.set_flag("quest_ate_in_cafe", value=day)
        $ pytfall.world_quests.get("A Fugitive").next_in_label("Looks like she ran away from a small village. Although, there are no villages near the city as far as you know.")
    elif pytfall.world_quests.check_stage("A Fugitive") == 5:
        $ n.override_portrait("portrait", "happy")
        $ hero.set_flag("ate_in_cafe", value=day)
        n.say "Hey, you late, [hero.name]! I'm starving!"
        n.say "Let's see, today I want these eggs in tomato sauce, raspberry muffins and..."
        $ k = chars["Kushina_Uzumaki"]
        $ k_spr = chars["Kushina_Uzumaki"].get_vnsprite()
        show expression k_spr at left with dissolve
        $ k.override_portrait("portrait", "happy")
        k.say "Hey guys, mind if I join?"
        $ n.override_portrait("portrait", "indifferent")
        $ n.show_portrait_overlay("surprised", "reset")
        n.say "..!"
        "A woman suddenly approaches you."
        k.say "I just had a little chat with the waitress here, and she told me you two are regular visitors! Who would have thought that I'll find you so fast."
        k.say "I appreciate you concern about my daughter, [hero.name]. Even though a small diet wouldn't hurt in her case, it was a worthy act."
        $ n.override_portrait("portrait", "sad")
        $ n.hide_portrait_overlay()
        n.say "Mom, I..."
        $ k.override_portrait("portrait", "angry")
        k.say "We'll speak at home, darling. Take a good look at these muffins by the way. Then there will be something to remember the next two years on bread and water."
        $ k.override_portrait("portrait", "indifferent")
        k.say "Now, I believe she owns you quite a sum, eh?"
        menu:
            "Indeed":
                k.say "Here, it should cover your expenses and then some more."
                $ hero.add_money(700)
            "Refuse":
                $ k.override_portrait("portrait", "happy")
                $ n.disposition += 50
                $ k.disposition += 100
                k.say "Oh? That's very nice of you."
        $ k.override_portrait("portrait", "angry")
        k.say "Now then, time to return home, Naruko. And don't even try to pull something."
        n.say "...Ok. Bye, [hero.name]."
        hide k_spr
        hide n_spr
        with dissolve
        $ pytfall.world_quests.get("A Fugitive").finish_in_label("Her mother found her and took home. Perhaps you'll see them again in the future.", "complete")
        $ n.del_flag("quest_ate_in_cafe")
        $ n.restore_portrait()
        $ k.restore_portrait()
    jump main_street
    
label qwe:
    scene bg story study
    python:
        temp = list(i for i in chars.values() if "Naruto" in i.origin)
        characters = {}
        for i in temp:
            emo=random.choice(["happy", "sad", "indifferent", "shy"])
            characters[i]=emo
    $ q = renpy.call_screen("hidden_village_chars_list", characters)
    hero.say "[q.id]"
    $ ff = characters[q]
    hero.say "[ff]"
    
    
screen hidden_village_chars_list(characters):
    # $ img = chars["Naruko_Uzumaki"].show("0007-po-e5.png", resize=(100, 100))
    # imagebutton:
        # pos(380, 300)
        # idle (img)
        # hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        # action [Hide("city_beach_left"), Jump("city_beach_cafe_main")]
    
    
    hbox:
        spacing 25
        pos (17, 605)
        for l in characters.keys():
            $ char_profile_img = l.show('portrait', characters[l], resize=(98, 98), cache=True, type="reduce")
            $ img = "content/gfx/frame/ink_box.png"
            imagebutton:
                background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                idle (char_profile_img)
                hover (im.MatrixColor(char_profile_img, im.matrix.brightness(0.15)))
                action [Return(l), Hide("qqq")]
                align 0, .5
                xysize (102, 102)

            # button:
                # idle_background Frame(Transform(img, alpha=0.4), 10 ,10)
                # hover_background Frame(Transform(img, alpha=0.9), 10 ,10)
                # align 0, .5
                # xysize (102, 102)
                # action Return(['choice', l])
                

                # frame:
                    # background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                    # padding 0, 0
                    # align 0, .5
                    # xysize(100, 100)
                    # add char_profile_img align .5, .5 alpha 0.96
