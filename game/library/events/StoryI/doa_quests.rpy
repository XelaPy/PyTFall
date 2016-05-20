init python:
    q = register_quest("Two Sisters", manual=True)
    register_event("two_sisters0", quest="Two Sisters", locations=["all"], trigger_type="doa_quest", dice=100)
    
label two_sisters0(event):
    $ pytfall.world_events.kill_event("two_sisters0", cached=True)
    show bg hiddenvillage_alley with dissolve
    "A distant alley at the far end of the village led you in a small garden."
    "Hearing a slight noise behind, you turn around."
    $ a = chars["Ayane"]
    $ a_spr = chars["Ayane"].get_vnsprite()
    $ a.override_portrait("portrait", "indifferent")
    show expression a_spr at center with dissolve
    $ pytfall.world_quests.get("Two Sisters").next_in_label("Ayane, a cold kunoichi, proposed you a deal.")
    a.say "Greetings, [hero.name]. My name is Ayane. Do not be alarmed, I have no intentions to attack you. I'm here to offer you a deal."
    "There was nothing there a moment ago, but now there is a young kunoichi standing before you."
    a.say "I ask for cooperation in a serious matter. Follow my instructions, and you will get a huge reward."
    "Her voice is cold as ice."
    a.say "Tell about it to anyone, and you'll never see me again. Until the moment I kill you."
    
    a.say "Or leave now and forget about this conversation."
    menu:
        "She stares at you, waiting for an answer"
        
        "Hear her out":
            $ pytfall.world_quests.get("Two Sisters").next_in_label("You have a few days to find a redhead kunoichi in the city. You probably should check beaches and parks first.")
            a.say "Listen carefully then. Tomorrow a runaway redhead kunoichi will arrive to the city. She will stay here for awhile, her name is Kasumi."
            a.say "I need you to find her and bring here without telling her about me. You have only a few days before she leaves, so make it quick."
            a.say "Then you will get the following instructions and your reward. Like I said, don't tell anyone about it, unless you wish to die."
            hide expression a_spr with dissolve
            $ register_event_in_label("two_sisters1", quest="Two Sisters", priority=1000, locations=choice(["city_parkgates", "city_park", "city_beach", "city_beach_left", "city_beach_cafe_main", "city_beach_cafe"]), start_day=day + 1, dice=100)
            $ register_event_in_label("fail_two_sisters", locations=["all"], start_day=day + 5, run_conditions=["True"], trigger_type="auto")
            "She quickly leaves. Looks like you will be busy tomorrow."
        "Leave her be":
            $ pytfall.world_quests.get("Two Sisters").finish_in_label("You refused. You will not see her again.", "complete")
            hide expression a_spr with dissolve
            "Without wasting words you leave the garden. Almost immediately you hear another slight noise behind. The garden is empty again."
    $ a.restore_portrait()
    return
    
label fail_two_sisters(event):
    $ pytfall.world_events.kill_event("two_sisters1", cached=True)
    $ pytfall.world_quests.get("Two Sisters").fail("Sadly, you missed you chance to meet her.")
    "You waisted too much time. Now you will never meet them again."
    return
    
label two_sisters1(event):
    $ k = chars["Kasumi"]
    $ k.override_portrait("portrait", "happy")
    if event.label_cache in ["city_beach", "city_beach_left"]:
        show expression k.show("00C4-nn-e2-e5-cb-l5-pr-pc.jpg", resize=(800, 600)) as x at truecenter with dissolve
    elif event.label_cache in ["city_beach_cafe_main", "city_beach_cafe"]:
        show expression k.show("00E4-nn-e5-cb-l5-pr.jpg", resize=(800, 600)) as x at truecenter with dissolve
    else:
        show expression k.show("00BE-nn-e6-c1-cm-l3-la-lc-pr-pa.jpg", resize=(800, 600)) as x at truecenter with dissolve
    "You spotted the person you were looking for. Noticing you interest, she friendly smiles."
    k.say "Oh, hi there! Can I help you?"
    menu:
        "Follow the Ayane plan":
            "You quickly make up a story about your relatives being kidnapped by an evil ninja clan, and ask her to help you save them."
            $ pytfall.world_quests.get("Two Sisters").next_in_label("You lured your target into the trap. Time to meet Ayane again.")
            $ k.override_portrait("portrait", "indifferent")
            k.say "How awful... Of course I will help you!"
            $ pytfall.world_events.kill_event("two_sisters1", cached=True)
            $ register_event("two_sisters2", quest="Two Sisters", locations=["all"], trigger_type="doa_quest", dice=100)
            "You ask her to meet you later in the location where Ayane waits and leave."
            hide expression x with dissolve
        "Tell her the truth":
            "You tell her everything. Her face darkens."
            $ k.override_portrait("portrait", "indifferent")
            k.say "I see... Thanks for telling me. She has been hunting me for awhile now."
            k.say "Listen, I need your help. It useless to negotiate with her, we will have to fight."
            k.say "If she beats me, you will be the next. So... let's meet where she is waiting for me."
            hide expression x with dissolve
            $ pytfall.world_events.kill_event("two_sisters1", cached=True)
            $ pytfall.world_quests.get("Two Sisters").next_in_label("You teamed with Kasumi. Time to meet Ayane again.")
            $ register_event("two_sisters3", quest="Two Sisters", locations=["all"], trigger_type="doa_quest", dice=100)
            "She leaves."
    $ k.restore_portrait()
    return
    
label two_sisters2(event):
    $ a = chars["Ayane"]
    $ a_spr = chars["Ayane"].get_vnsprite()
    $ a.override_portrait("portrait", "confident")
    $ k = chars["Kasumi"]
    $ k_spr = chars["Kasumi"].get_vnsprite()
    $ k.override_portrait("portrait", "indifferent")
    $ a.disposition += 250
    show bg hiddenvillage_alley with dissolve
    show expression k_spr at mid_left with dissolve
    "Together you arrived to the appointed location."
    k.say "Um, so where are..."
    show expression a_spr at mid_right with dissolve
    a.say "Hello, dear sister."
    $ k.override_portrait("portrait", "scared")
    k.say "Ayane!"
    a.say "Long time no see, Kasumi. Now then, about our agreement, [hero.name]... After we beat her, I will make a humble and obedient slave from her and give her to you."
    hide expression a_spr
    hide expression k_spr
    with dissolve
    show expression k.show("0059-nn-e2-c1-cm-l3-lb-lc-pb-a8.jpg", resize=(800, 600)) as x at mid_left
    show expression a.show("0037-nn-e2-z2-c1-l3-pb.jpg", resize=(800, 600)) as y at mid_right
    with dissolve
    $ k.override_portrait("portrait", "angry")
    k.say "It's not gonna happen!"
    a.say "It will be your last battle, Kasumi. Let's go, [hero.name]."
    
    $ enemy_team = Team(name="Enemy Team", max_size=3)
    $ your_team = Team(name="Your Team", max_size=3)
    $ k.front_row = True
    $ a.front_row = True
    $ hero.front_row = True
    $ enemy_team.add(k)
    $ your_team.add(a)
    python:
        for member in your_team:
            member.controller = BE_AI(member)
        for member in enemy_team:
            member.controller = BE_AI(member)
    $ your_team.add(hero)
    $ battle = BE_Core(Image("content/gfx/bg/be/forestclearing_smaller.png"), music="content/sfx/music/be/battle (14).mp3", start_sfx=get_random_image_dissolve(1.5), end_sfx=dissolve)
    $ battle.teams.append(your_team)
    $ battle.teams.append(enemy_team)
    $ battle.start_battle()
    $ your_team.reset_controller()
    $ enemy_team.reset_controller()
    if battle.winner != your_team:
        jump game_over # I think the jump shouldn't hurt anything since it's a game over, ie loading a save will be needed
        
    show bg hiddenvillage_alley with dissolve
    show expression k.show("01A4-nd-eb-c1-c5-cm-l3-la-lc-pr.jpg", resize=(800, 600)) as x at truecenter with dissolve
    "Together you quickly overpowered Kasumi."
    a.say "See, I told you it will be your last battle."
    $ k.override_portrait("portrait", "scared")
    k.say "No way..!"
    a.say "Good job, [hero.name]. We are done here, unless you want to have some fun with her..?"
    "She sadistically smiles."
    k.say "N-no! Don't touch me! Please!"
    menu:
        "Nah, maybe later":
            a.say "Ok then, just don't forget she will be your slave, and you can do whatever you want to her. <another sadistic smile>"
            k.say "N-no way..."
        "Force her for a quick blowjob":
            a.say "That's my boy!"
            show expression k.show("004F-sx-e9-c8-l4-ns-p3-sa-p2-sn.jpg", resize=(800, 600)) as x at truecenter with dissolve
            "You force herself into her mouth. She coughs and resists at first, but then begins to do the job."
            a.say "Pretty submissive for a kunoichi, eh? I always knew she would make a good whore ♥"
            "Ayane insatiably looks at her sister. Something is very wrong with this family..."
            $ a.disposition += 100
            $ k.disposition -= 100
    hide expression x with dissolve
    show expression a_spr at center with dissolve
    $ a.override_portrait("portrait", "indifferent")
    $ pytfall.world_quests.get("Two Sisters").next_in_label("Together you managed to capture Kasumi. You have to meet Ayane after a week.")
    $ register_event_in_label("two_sisters4", locations=["all"], start_day=day + 3, run_conditions=["True"], trigger_type="auto")
    a.say "I'm going to do some personal slave training now. Let's meet after a week. Don't worry, I'm not going to run away. Kunoichi are always true to their word."
    hide expression a_spr with dissolve
    $ pytfall.world_events.kill_event("two_sisters2", cached=True)
    $ pytfall.world_events.kill_event("two_sisters3", cached=True)
    $ pytfall.world_events.kill_event("fail_two_sisters", cached=True)
    $ k.restore_portrait()
    $ a.restore_portrait()
    return
    
label two_sisters3(event):
    $ a = chars["Ayane"]
    $ a_spr = chars["Ayane"].get_vnsprite()
    $ a.override_portrait("portrait", "confident")
    $ k = chars["Kasumi"]
    $ k_spr = chars["Kasumi"].get_vnsprite()
    $ k.override_portrait("portrait", "indifferent")
    $ k.disposition += 300
    show bg hiddenvillage_alley with dissolve
    show expression k_spr at mid_left with dissolve
    "Together you arrived to the appointed location."
    k.say "..."
    show expression a_spr at mid_right with dissolve
    a.say "Hello, dear sister."
    k.say "Hello, Ayane. Can't say I missed you."
    $ a.override_portrait("portrait", "indifferent")
    a.say "You... don't look surprised to see me. <she suspiciously looks at you>"
    k.say "My new friend warned me about you. I've been running for too long, we settle it here and now."
    "You can feel murderous intents emanating from Ayane."
    hide expression a_spr
    hide expression k_spr
    with dissolve
    show expression k.show("0059-nn-e2-c1-cm-l3-lb-lc-pb-a8.jpg", resize=(800, 600)) as x at mid_left
    show expression a.show("0037-nn-e2-z2-c1-l3-pb.jpg", resize=(800, 600)) as y at mid_right
    with dissolve
    $ a.override_portrait("portrait", "angry")
    a.say "I was going to be nice with you, but if you insist... I just will kill you both here and now!"
    k.say "Fear not, [hero.name]. I know her fighting style, together we can defeat her."
    a.say "Like hell you can!"

    $ enemy_team = Team(name="Enemy Team", max_size=3)
    $ your_team = Team(name="Your Team", max_size=3)
    $ k.front_row = True
    $ a.front_row = True
    $ hero.front_row = True
    $ enemy_team.add(a)
    $ your_team.add(k)
    python:
        for member in your_team:
            member.controller = BE_AI(member)
        for member in enemy_team:
            member.controller = BE_AI(member)
    $ your_team.add(hero)
    $ battle = BE_Core(Image("content/gfx/bg/be/forestclearing_smaller.png"), music="content/sfx/music/be/battle (14).mp3", start_sfx=get_random_image_dissolve(1.5), end_sfx=dissolve)
    $ battle.teams.append(your_team)
    $ battle.teams.append(enemy_team)
    $ battle.start_battle()
    $ your_team.reset_controller()
    $ enemy_team.reset_controller()
    if battle.winner != your_team:
        jump game_over # I think the jump shouldn't hurt anything since it's a game over, ie loading a save will be needed
        
    show bg hiddenvillage_alley with dissolve
    show expression a.show("0004-nn-e2-c1-l2-pr.jpg", resize=(800, 600)) as x at truecenter with dissolve
    $ a.override_portrait("portrait", "shy")
    $ a.override_portrait("portrait", "angry")
    a.say "Ugh... I can't believe that..."
    "Together you managed to beat Ayane."
    k.say "You leave me no choice, sister. I'm not going to run away from you any longer. As a slave you will be unable to do anything. It pains me, but this is the only option I have."
    a.say "Damn you both..."
    hide expression x with dissolve
    show expression k_spr at center with dissolve
    $ k.override_portrait("portrait", "happy")
    k.say "I'm truly grateful for your help, [hero.name], and I'd like to reward you. Let's meet again after a week."
    $ k.show_portrait_overlay("like", "reset")
    k.say "<she quickly kisses you>"
    $ k.hide_portrait_overlay()
    $ pytfall.world_quests.get("Two Sisters").next_in_label("Together you managed to beat Ayane. You have to meet Kasumi after a week.")
    $ register_event_in_label("two_sisters5", locations=["all"], start_day=day + 7, run_conditions=["True"], trigger_type="auto")
    k.say "Let's go, Ayane. We still have intensive slave training ahead."
    hide expression k_spr with dissolve
    $ pytfall.world_events.kill_event("two_sisters3", cached=True)
    $ pytfall.world_events.kill_event("two_sisters2", cached=True)
    $ pytfall.world_events.kill_event("fail_two_sisters", cached=True)
    $ k.restore_portrait()
    $ a.restore_portrait()
    return
    
label two_sisters5(event):
    show bg hiddenvillage_alley with dissolve
    if not "village" in ilists.world_music:
        $ ilists.world_music["village"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("village")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["village"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")
    $ a = chars["Ayane"]
    $ a_spr = chars["Ayane"].get_vnsprite()
    $ a.override_portrait("portrait", "shy")
    $ k = chars["Kasumi"]
    $ k_spr = chars["Kasumi"].get_vnsprite()
    $ k.override_portrait("portrait", "happy")
    k.say "Hello, [hero.name]. I'm glad you came."
    show expression k.show("00BD-nn-e6-c1-cm-l3-la-lc-pr-pc.jpg", resize=(800, 600)) as x at truecenter with dissolve
    "After a week Kasumi invited you to meet her in a local park."
    k.say "The training is over. My sister will never hurt anyone from now on. Right, Ayane?"
    show expression a.show("0000-nn-e6-c1-l2-pr.jpeg", resize=(800, 600)) as x at truecenter with dissolve
    a.say "Y-yeah..."
    "There is Ayane next to her, in a rather submissive pose."
    k.say "What are we going to do now, Ayane?"
    a.say "W-we going to give [hero.name] his r-reward..."
    k.say "Correct!"
    show expression a.show("0056-sx-e3-c1-l2-gr-g1-g5-g9-gl.jpg", resize=(800, 600)) as x at truecenter with dissolve
    "With these words, sisters together pleasure you until you come."
    hide expression x with dissolve
    $ a.set_status("slave")
    $ k.set_status("free")
    $ hero.add_char(a)
    $ hero.add_char(k)
    show expression k_spr at mid_left
    show expression a_spr at mid_right
    $ k.show_portrait_overlay("note", "reset")
    k.say "Can we stay with you, [hero.name]? I'm sure we can make ourself useful to you."
    $ k.hide_portrait_overlay()
    $ pytfall.world_events.kill_event("two_sisters5", cached=True)
    $ pytfall.world_quests.get("Two Sisters").finish_in_label("Kunoichi sisters joined you.", "complete")
    "Together you return to your home."
    $ k.restore_portrait()
    $ a.restore_portrait()
    return
    
label two_sisters4(event):
    show bg hiddenvillage_alley with dissolve
    if not "village" in ilists.world_music:
        $ ilists.world_music["village"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("village")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["village"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")
    $ a = chars["Ayane"]
    $ a_spr = chars["Ayane"].get_vnsprite()
    $ a.override_portrait("portrait", "confident")
    $ k = chars["Kasumi"]
    $ k_spr = chars["Kasumi"].get_vnsprite()
    $ k.override_portrait("portrait", "indifferent")
    a.say "Hi there, [hero.name]!"
    show expression a.show("00DC-nn-eb-ec-c1-l3-l9-pr.jpg", resize=(800, 600)) as x at truecenter with dissolve
    "After a week Ayane invited you to meet her in a local park."
    a.say "It's been a fun week, thanks to you. Right, Kasumi?"
    show expression k.show("00F8-nd-e6-c1-cm-l3-la-lc-pr.jpg", resize=(800, 600)) as x at truecenter with dissolve
    k.say "Yes, of course."
    "There is Kasumi next to her, her clothes barely cover her body. Look like it doesn't bother her at all."
    a.say "[hero.name] is your master now. What should you tell him?"
    $ k.override_portrait("portrait", "happy")
    k.say "Please use me as you like, master!"
    a.say "Good girl! In fact, it took only two days to break her. So much for a kunoichi, eh?"
    show expression a.show("0071-sx-eb-c1-l2-ns-sk-p1-st.jpg", resize=(800, 600)) as x at truecenter with dissolve
    "Ayane comes to her sister and deeply and passionately kisses her. Kasumi responds in kind."
    hide expression x with dissolve
    $ k.set_status("slave")
    $ a.set_status("free")
    $ hero.add_char(a)
    $ hero.add_char(k)
    show expression k_spr at mid_left
    show expression a_spr at mid_right
    with dissolve
    $ a.show_portrait_overlay("note", "reset")
    a.say "Let's go, [hero.name]. Oh, don't look so surprised, I must oversee my dear sister, and you could use a decent kunoichi at your side, right?"
    $ a.hide_portrait_overlay()
    $ pytfall.world_events.kill_event("two_sisters4", cached=True)
    $ pytfall.world_quests.get("Two Sisters").finish_in_label("Kunoichi sisters joined you.", "complete")
    "Together you return to your home."
    $ k.restore_portrait()
    $ a.restore_portrait()
    return