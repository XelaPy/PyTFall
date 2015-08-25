label karin_first_meeting:
    stop music
    stop world
    play world "park.mp3" fadein 2.0 loop
    scene black
    $ k = chars["Karin"]
    $ k_spr = chars["Karin"].get_vnsprite()
    show bg hidden_village with dissolve
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
    hide expression k_spr with dissolve
    "She leaves. You feel moderately offended. Maybe there is a way to make your, er, 'chakra' more attractive?" #giving quest to change chakra
    $ k.restore_portrait()
    scene black with dissolve
    stop world

label karin_second_meeting: #ask tsunade how to change chakra
    stop music
    stop world
    play world "Field2.ogg" fadein 2.0 loop
    $ t = chars["Tsunade"]
    $ t_spr = chars["Tsunade"].get_vnsprite()
    $ t.override_portrait("portrait", "indifferent")
    show bg story cab_1 with dissolve
    show expression t_spr at center with dissolve
    t.say "Huh? Why would you want to... Ah, I get it. It's her again."
    t.say "She has rather... unique taste. Like her desire for masochism with all those weird biting techniques."
    t.say "I'm sorry, but it would take years of training to improve your chakra even a little. We don't have that time."
    $ t.override_portrait("portrait", "confident")
    t.say "But I might have an idea. Karin always had a thing for chakra produced by the wielders of eyes techniques."
    t.say "They are pretty rare these days, but I believe we have a kunoichi with such a technique. You will recognise her immediately."
    t.say "If you mix your life energies, your weak charka will change for a few days, becoming similar to her."
    $ t.override_portrait("portrait", "confident")
    t.say "You certainly understand what I mean by mixing life energies, but just to clarify, you have to do 'it' more than once. Like, a lot."
    t.say "Well then, good luck. I need to dr... er, do some important work."
    $ t.restore_portrait()
    hide expression t_spr with dissolve # we implant a counter to hinata that counts sex actions. about 5 should be enough.
    scene black with dissolve
    stop world

label karin_third_meeting: # returning with proper chakra
    stop music
    stop world
    play world "park.mp3" fadein 2.0 loop
    scene black
    $ k = chars["Karin"]
    $ k_spr = chars["Karin"].get_vnsprite()
    show bg hidden_village with dissolve
    show expression k_spr at center with dissolve
    $ k.override_portrait("portrait", "angry")
    k.say "Oh? You again? I don't have time right now, so..."
    "She stammers and seemed to be sniffing."
    menu:
        "Ask what's wrong":
            $ k.disposition += 50
            $ k.override_portrait("portrait", "indifferent")
            k.say "Wrong? There is nothing wrong. Not with me at least."
        "Propose to just talk a bit":
            k.say "Nah, just stay still. I need to..."
        "Turn around and leave":
            $ k.disposition += 100
            $ k.override_portrait("portrait", "shy")
            k.say "H-Hey, wait! I didn't told you to leave!"
    "For a few seconds she looks at you, but at the same time through you."
    $ k.override_portrait("portrait", "suggestive")
    k.say "Ah, I see what you did there. Clever, clever indeed."
    k.say "I never liked that depressive damsel in distress, but her chakra combined with someone else is tasty indeed."
    "She licks her lips."
    $ k.set_flag("allowed_sex", value="True")
    $ k.set_flag("quest_no_sex", value="False")
    k.say "Very well, I'll give you a chance. Just don't bring her with you, and we are good." # here we unlock her sex/romance options
    # also we could add additional mechanics like 1 sex with hinata = 1 available sex with karin
    hide expression k_spr with dissolve
    $ k.restore_portrait()
    scene black with dissolve
    stop world