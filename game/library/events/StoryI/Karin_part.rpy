init python:
    karinquest = register_quest("Sixth Sense", manual=True)

label Karin_can_heal:
    $ k = chars["Karin"]
    $ k.override_portrait("portrait", "indifferent")
    if k.disposition <= -50 and k.status != "slave":
        k.say "I refuse. You're not worth my time."
    elif hero.health >= hero.get_max('health'):
        k.say "Hm? You seems pretty healthy to me, [hero.name]."
        $ k.restore_portrait()
    elif k.vitality <= 25:
        k.say "I'm too tired for that technique right now."
        $ k.restore_portrait()
    else:
        $ heal = hero.get_max('health') - hero.health
        if k.vitality >= heal:
            k.say "Yes, I can do it."
        else:
            k.say "I'm afraid I don't have enough strength to heal you completely. But I'll do what I can."
            $ heal = heal - k.vitality
        if k.status != "slave" and not(check_lovers(char, hero)):
            $ heal *= 5
            k.say "It will be [heal_money]G."
            if heal > hero.gold:
                "You don't have such amount of gold..."
                k.say "Pathetic..."
                $ k.restore_portrait()
                jump girl_interactions
            else:
                menu:
                    "Are you ready to pay [heal_money]G?"
                
                    "Yes":
                        if hero.take_money(heal):
                            $ k.add_money(heal)
                    "No":
                        k.say "As you wish."
                        $ k.restore_portrait()
                        jump girl_interactions
        $ k.override_portrait("portrait", "suggestive")
        k.say "Well, you know what to do."
        "She rolls her sleeve and gives you hand. You bite through her soft skin, feeling the taste of blood."
        k.say "..."
        $ hero.health += heal
        $ k.vitality -= heal
        "She obviously enjoys it despite the pain. You feel like her energy flows into you, healing your wounds."
        $ k.disposition += 10
        k.say "Alright, we are done here. Come again when you'll need a treatment."
        $ k.restore_portrait()
        $ del heal
    $ del k
    $ del k_spr
    jump girl_interactions
    
label storyi_karin_first_meeting:
    scene black
    $ k = chars["Karin"]
    $ k_spr = chars["Karin"].get_vnsprite()
    $ chars["Karin"].set_flag("event_to_interactions_karincanhealalways", value={"label": "Karin_can_heal", "button_name": "Ask for healing", "condition": "True"})
    show bg hiddenvillage_entrance with dissolve
    "You walk through the village, as you flip through the files that you got from Tsunade."
    "Telepathy, eyesight through any obstacles, superhuman strength... Kunoichi have uncommon and useful perks. It would be wise to have them as allies or slaves..."
    "Deep in thought, you didn't noticed how the folder slipped out. Feeling a presence behind, you turn around."
    show expression k_spr at center with dissolve
    "A girl is standing there reading the files. Damn."
    $ k.override_portrait("portrait", "angry")
    k.say "I am what? Obsessively in..."
    menu:
        "Try to take the folder":
            show expression k_spr at mid_left with move
            "She steps aside without stopping reading."
        "Don't do anything":
            $ pass
    k.say "Cruel to a certain extent... That's rich coming from her..."
    "That can't be good. Look like she's reading her own file."
    menu:
        "Try to catch her":
            show expression k_spr at mid_right with move
            "She does not even look at you, just reads, but still, she seems to be just millimetres away from where you want to grip."
        "Wait":
            $ pass
    "Finally, she looks up, seemingly surprised you are still here."
    k.say "I can sense granny up there. Here, the files back. Are you sure these are files? I mean, they seem to be like the shorthand some of the perverts would use."
    k.say "Anyway, I'm disappointed that you used that crap of a file on me. I would have just told you. It's not as if you would care anyway, most likely you just want to fuck and could care less about me."
    $ k.override_portrait("portrait", "sad")
    k.say "It's a bit... complicated. Not that I am a prude or anything...but I am very sensitive to chakra, as you may have read."
    k.say "For me, it's like a sixth sense, and mind you, you are pretty cute, but your chakra... lets just say you are a choirboy."
    k.say "If you had at least a modestly interesting chakra, I could rethink that, but like this..."
    $ k.override_portrait("portrait", "suggestive")
    k.say "Oh, by the way, I'm the only adequate medic here. Come to the village hospital if you are low on health."
    k.say "Of course it won't be for free."
    hide expression k_spr with dissolve
    "She leaves. You feel moderately offended. Maybe there is a way to make your, er, 'chakra' more attractive or something?"
    $ k.restore_portrait()
    $ del k
    $ del k_spr
    scene black with dissolve
    $ pytfall.world_quests.get("Sixth Sense").next_in_label("You met Karin, one of ninja medics. She wants you to improve your chakra before she will agree to do anything with you.")
    jump hiddenvillage_entrance

label storyi_karin_second_meeting:
    $ k = chars["Karin"]
    $ k_spr = chars["Karin"].get_vnsprite()
    show expression k_spr at center with dissolve
    $ k.override_portrait("portrait", "angry")
    k.say "What is it? I don't have time right now, so..."
    "She stammers and seemed to be sniffing."
    "For a few seconds she looks at you, but at the same time through you."
    $ k.override_portrait("portrait", "suggestive")
    k.say "Ah, I see what you did there. Her chakra combined with someone else is tasty indeed."
    "She licks her lips."
    $ k.set_flag("quest_cannot_be_lover", value=False)
    $ k.set_flag("quest_cannot_be_fucked", value=False)
    k.say "Very well, I'll give you a chance."
    $ pytfall.world_quests.get("Sixth Sense").next_in_label("Now you can try sex with her, providing that she likes you enough of course...")
    $ del k
    $ del k_spr
    return
    
label storyi_karin_finish_quest:
    "It was a bit strange because of her masochistic tendencies, but pleasant in general..."
    $ pytfall.world_quests.get("Sixth Sense").finish_in_label("You took care of Karin's virginity.", "complete")
    jump hiddenvillage_entrance