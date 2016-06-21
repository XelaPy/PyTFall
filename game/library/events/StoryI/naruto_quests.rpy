init python:
    q = register_quest("Drunk Lady")
    register_event("drunk_lady1", quest="Drunk Lady", locations=["tavern_inside"], dice=100, restore_priority=0, jump=True)
    
label drunk_lady1:
    $ t = chars["Tsunade"]
    scene bg tavern_inside # ChW: This is to get rid of tavent picture until I create a more complex solution...
    show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter with dissolve:
        zoom 0.7
    "Examining the room, you notice a middle aged woman with impressive knockers drinking alone in the corner."
    menu:
        "Maybe you could join her?"
        "Definitely":
            show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter:
                zoom 0.7
                linear 1 zoom 1.0
            "Getting a drink, you sit next to her."
            $ t.override_portrait("portrait", "suggestive")
            t.say "Let's see what do we have here. Hmm... I suppose it will do. We can't be too picky these days, can we?"
            "She is clearly drunk."
            t.say "Call me Tsunade. No last names, I'm too old for this shit."
            "You try to say something, but she interrupts you."
            t.say "Come on, drop that look, young man. I know, modern morals, but who do you prefer? Some silly little goose that barely knows what she is doing, or some older, more... experienced woman that can take care of you?"
            show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter:
                zoom 1.0
                linear 0.5 zoom 1.1
                linear 0.5 zoom 1.0
            "She seductively pushes her huge boobs towards you."
            t.say "I just... need some money to pay off a gambling debt. One thousand coins."
            if hero.gold >= 1000:
                menu:
                    "Do you want to give her 1000 coins?"
                    "Hell yeah":
                        $ pytfall.world_quests.get("Drunk Lady").next_in_label("You've met a woman with huge knockers who proposed you her body for gold. An excellent deal.")
                        $ pytfall.world_events.kill_event("drunk_lady1", cached=True)
                        "She quickly hides your coins."
                        $ hero.gold -= 1000
                        t.say "Niiice. Tell you what, I have a room here on the second floor."
                        t.say "I'll wait you there..."
                        "She stands up and unsteadily goes to the second floor. It's going to be interesting."
                        hide x with dissolve
                        jump drunk_lady_quest_scene
                    "No way":
                        "She shrugs with disappointment."
                        t.say "A shame. Back to my drink then."
                        $ pytfall.world_quests.get("Drunk Lady").next_in_label("You've met a woman with huge knockers who proposed you her body for 1000 gold coins. You refused, for now.")
                        $ pytfall.world_events.kill_event("drunk_lady1", cached=True)
                        $ register_event_in_label("drunk_lady2", quest="Drunk Lady", locations=["tavern_inside"], dice=0, restore_priority=0, run_conditions=["hero.gold >= 1000"], jump=True)
                        $ pytfall.world_events.force_event("drunk_lady2")
                        hide x with dissolve
            else:
                "Unfortunately, you don't have that amount of gold at the moment."
                t.say "I see... My proposition still stands. You know where to find me."
                "She returns to her drink."
                $ pytfall.world_quests.get("Drunk Lady").next_in_label("You've met a woman with huge knockers who proposed you her body for 1000 gold coins. Sadly, you couldn't afford her.")
                $ pytfall.world_events.kill_event("drunk_lady1", cached=True)
                $ register_event_in_label("drunk_lady2", quest="Drunk Lady", locations=["tavern_inside"], restore_priority=0, dice=0, run_conditions=["hero.gold >= 1000"], jump=True)
                $ pytfall.world_events.force_event("drunk_lady2")
                hide x with dissolve
        "Maybe another time":
            "Perhaps some another day."
    hide x with dissolve
    $ t.restore_portrait()
    jump tavern_inside
    
label drunk_lady2:
    $ t = chars["Tsunade"]
    scene bg tavern_inside
    show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter with dissolve:
        zoom 0.7
    "You see the woman you met before. If you want, you can accept her proposition and pay 1000 coins."
    menu:
        "Pay her?"
        "Yes":
            show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter:
                zoom 0.7
                linear 1 zoom 1.0
            "You sit next to her as she friendly nods, and gave her a purse of gold."
            $ t.override_portrait("portrait", "suggestive")
            $ hero.gold -= 1000
            t.say "Niiice. Tell you what, I have a room here on the second floor."
            t.say "I'll wait you there..."
            "She stands up and unsteadily goes to the second floor."
            $ pytfall.world_quests.get("Drunk Lady").next_in_label("You paid Tsunade and she invited you to her room on the second floor.")
            $ pytfall.world_events.kill_event("drunk_lady2", cached=True)
            jump drunk_lady_quest_scene
        "No":
            "Maybe some other time."
    hide x with dissolve
    $ t.restore_portrait()
    jump tavern_inside
    
label drunk_lady_quest_scene:
    $ t = chars["Tsunade"]
    $ t_spr = chars["Tsunade"].get_vnsprite()
    $ t.override_portrait("portrait", "indifferent")
    scene black with dissolve
    stop music fadeout 1.0
    stop world fadeout 1.0
    play world "town2.ogg" fadein 1.0 loop
    show bg girl_room_4 with dissolve
    "You follow her to her room. It's definitely not the cheapest room in the tavern, but on the other hand the best rooms are located on the third floor."
    show expression t_spr at center with dissolve
    t.say "Well then, now we can talk. No one can here us here."
    "You still can feel how she reeks of alcohol, but she doesn't look drunk at all. She smirks looking at your puzzled face."
    $ t.override_portrait("portrait", "confident")
    t.say "I have a proposition for you, [hero.name]. I used to know your father, we helped each other a lot in the past. But since he's gone, I was hoping you can do me a small favor instead of him."
    $ t.override_portrait("portrait", "indifferent")
    t.say "You see, until recently I used to lead a ninja clan here in the city. But they said I was too committed to traditions, and picked another leader."
    t.say "It's simple. Help me to regain position as the clan leader, and you will get full clan support plus a few hot young kunoichi to have fun with ♫"
    t.say "I'm not forcing you or something, you can do as you please. But think about the possibilities first."
    "The possibilities are promising indeed."
    t.say "I even can return your money..."
    $ t.override_portrait("portrait", "confident")
    t.say "...or work them out, if you prefer that ♥"
    menu:
        "Money":
            $ t.override_portrait("portrait", "indifferent")
            t.say "Damn, I hoped you'll pick the other option... Here."
            "She returns your gold."
        "Sex":
            $ t.override_portrait("portrait", "happy")
            t.say "Nice! It's been awhile..."
            hide expression t_spr with dissolve
            show expression t.show("00B1-nd-e2-e5-c1-l4-a1.jpg", resize=(800, 600)) as x at truecenter with dissolve
            $ t.override_portrait("portrait", "suggestive")
            t.say "...but I think I still remember how to do it. What do you think? I grow them myself. I used to be flat as a board, but medical techniques can improve many things ♥"
            show expression t.show("0025-sx-e6-c8-l2-ns-p3-p2-sn-su.jpg", resize=(800, 600)) as x at truecenter with dissolve
            "Without further ado she kneels down and masterfully brings you to the finish. You feel that you learned a thing a two about sex."
            $ hero.sex += 50
            $ hero.health = hero.get_max("health")
            $ hero.mp = hero.get_max("mp")
            $ hero.vitality = hero.get_max("vitality")
            hide x with dissolve
            show expression t_spr at center with dissolve
            $ t.override_portrait("portrait", "confident")
            t.say "Oh, that was quick. You have a long way to go if you wish to surpass you father ♫"
    $ t.override_portrait("portrait", "indifferent")
    t.say "That aside... You first task is to take care of two kunoichi here in the city. Eh, you know what kunoichi is, right? It's basically a female ninja."
    $ t.override_portrait("portrait", "confident")
    t.say "And by taking care I mean to pop their cherries, if you catch my meaning."
    $ t.override_portrait("portrait", "indifferent")
    t.say "I am not asking you to rape them, or to force yourself on them. If you get idea, it would be a miracle if you survive the attempt."
    t.say "We should avoid unneeded attention, find me in the tavern only after you finish with it. So long..."
    hide expression t_spr with dissolve
    $ t.restore_portrait() 
    "She leaves. You notice at the table nearby a package of documents with information about your 'targets'."
    $ pytfall.world_quests.get("Drunk Lady").finish_in_label("Turns out Tsunade has a mission for you. You probably should accept it.", "complete")
    # if we allow here to refuse, it will make the village and all characters inside unavailable forever. so yeah, it will be linear.
    scene black
    jump tavern_inside
