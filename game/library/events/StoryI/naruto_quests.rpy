init python:
    q = register_quest("Drunk Lady")
    register_event("drunk_lady1", quest="Drunk Lady", locations=["tavern_inside"], dice=100, restore_priority=0)
    
label drunk_lady1(event):
    $ t = chars["Tsunade"]
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
            t.say "Now, now. Let's see what do we have here."
            "She is clearly drunk."
            t.say "Hmm. I suppose it will do. We can't be too picky these days, can we?"
            "You try to say something, but she interrupts you."
            t.say "Come on, drop that look, young man. I know, modern morals, but who do you prefer? Some silly little goose that barely knows what she is doing, or some older, more... experienced woman that can take care of you?"
            "She seductively holds her hand over her huge boobs."
            t.say "I just... need some money, to pay a gambling debt. Two thousands coins."
            if hero.gold >= 2000:
                menu:
                    "Do you want to give her 2000 coins?"
                    "Hell yeah":
                        $ pytfall.world_quests.get(event.quest).next_in_label("You've met a woman with huge knockers who proposed you her body for gold. An excellent deal.")
                        $ pytfall.world_events.kill_event("drunk_lady1", cached=True)
                        "She quickly hides your coins."
                        $ hero.gold -= 2000
                        t.say "Niiice. Tell you what, I have a room here on the second floor. Just tell the guard Tsunade invited you, that's my name by the way."
                        t.say "I'll wait you there..."
                        "She stands up and unsteadily goes to the second floor. It's going to be interesting."
                        $ register_event_in_label("drunk_lady3", quest=event.quest, locations=["tavern_inside"], dice=50, restore_priority=0)
                    "No way":
                        "She shrugs with disappointment."
                        t.say "A shame. Back to my drink then."
                        $ pytfall.world_quests.get(event.quest).next_in_label("You've met a woman with huge knockers who proposed you her body for 2000 gold coins. You refused, for now.")
                        $ pytfall.world_events.kill_event("drunk_lady1", cached=True)
                        $ register_event_in_label("drunk_lady2", quest=event.quest, locations=["tavern_inside"], dice=50, restore_priority=0, run_conditions=["hero.gold >= 2000"])
                        $ pytfall.world_events.force_event("drunk_lady2")
                        hide x with dissolve
            else:
                "Unfortunately, you don't have that amount of gold at the moment."
                t.say "I see... My proposition still stands. You know where to find me."
                "She returns to her drink."
                $ pytfall.world_quests.get(event.quest).next_in_label("You've met a woman with huge knockers who proposed you her body for 2000 gold coins. Sadly, you couldn't afford her.")
                $ pytfall.world_events.kill_event("drunk_lady1", cached=True)
                $ register_event_in_label("drunk_lady2", quest=event.quest, locations=["tavern_inside"], dice=50, restore_priority=0, run_conditions=["hero.gold >= 2000"])
                $ pytfall.world_events.force_event("drunk_lady2")
                hide x with dissolve
        "Maybe another time":
            "Perhaps some another day."
    hide x with dissolve
    $ t.restore_portrait()
    return
    
label drunk_lady2(event):
    $ t = chars["Tsunade"]
    show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter with dissolve:
        zoom 0.7
    "You see the woman you met before. If you want, you can accept her proposition and pay 2000 coins."
    menu:
        "Pay her?"
        "Yes":
            show expression t.show("00AD-nn-e2-ec-c1-l4-lf-pr-pc.jpg", resize=(800, 600)) as x at truecenter:
                zoom 0.7
                linear 1 zoom 1.0
            "You sit next to her as she friendly nods, and gave her a purse of gold."
            $ t.override_portrait("portrait", "suggestive")
            $ hero.gold -= 2000
            t.say "Niiice. Tell you what, I have a room here on the second floor. Just tell the guard Tsunade invited you, that's my name by the way."
            t.say "I'll wait you there..."
            "She stands up and unsteadily goes to the second floor. It's going to be interesting."
            $ pytfall.world_quests.get(event.quest).next_in_label("You paid Tsunade and she invited you to her room on the second floor.")
            $ pytfall.world_events.kill_event("drunk_lady2", cached=True)
            $ register_event_in_label("drunk_lady3", quest=event.quest, locations=["tavern_inside"], dice=50, restore_priority=0)
            $ pytfall.world_events.force_event("drunk_lady3")
        "No":
            "Maybe some other time."
    hide x with dissolve
    $ t.restore_portrait()
    return
    
label drunk_lady3(event):
    $ pass
    return