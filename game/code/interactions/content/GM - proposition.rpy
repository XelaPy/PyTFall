# USED TO BE FRIENDSHIP LINES, MAY BE USEFUL IN THE FUTURE
        # if ct("Impersonal"):
            # $ rc("Very well.", "Alright.")
        # elif ct("Shy") and dice(50):
            # $ rc("Umm... That is... I-I'm in your care...!", "I think of you as a precious friend too.")
        # elif ct("Kuudere"):
            # $ rc("I can't think of any reason to refuse. Sure, why not.", "...It looks like we're a good match.")
        # elif ct("Dandere"):
            # $ rc("I agree.", "I understand...", "Please...take good care of me.")
        # elif ct("Tsundere"):
            # $ rc("I suppose I have no choice.", "Fine ...I-it's not like this makes me happy!")
        # elif ct("Imouto"):
            # $ rc("R-Really...? Fuaah, I'm so glad!", "We'll be friends forever, right?", "Hehehe ♪ We somehow became good friends, huh?")
        # elif ct("Bokukko"):
            # $ rc("Hmm, okay, sounds good!", "I s'pose I could.", "Feels nice having someone support me for a change.")
        # elif ct("Ane"):
            # $ rc("Yes, that would be acceptable.", "It looks like you and I could be good partners.")
        # elif ct("Kamidere"):
            # $ rc("Yes, with pleasure. Treat me well, okay? ♪", "Please continue to be good friends with me.")
        # elif ct("Yandere"):
            # $ rc("I have the feeling I could get along with you.",  "Well, we get along fine... Alright.")
        # else:
           # $ rc("Mm, alright.", "Okay!", "Hehehe, it's great to be friends ♪", "Of course. Let's get along ♪")
    # else:
        # $ char.override_portrait("portrait", "indifferent")
        # if ct("Impersonal"):
            # $ rc("Not interested.", "I cannot understand. Please give me a detailed explanation.")
        # elif ct("Shy") and dice(50):
            # $ rc("I-I'm really sorry...", "Another time, maybe...")
        # elif ct("Tsundere"):
            # $ rc("Huh? Why should I agree to that?", "Uh? Wha...what are you talking about?")
        # elif ct("Kuudere"):
            # $ rc("There's all sorts of problems with that.", "A bother. Don't want to.")
        # elif ct("Dandere"):
            # $ rc("Smells suspicious. I will refrain.", "If I feel like it.")
        # elif ct("Imouto"):
            # $ rc("Umm, uh... Sorry. Hehe ♪", "Sure... Pfft... Just kidding, I lied!")
        # elif ct("Yandere"):
           # $ rc("I don't see any prerequisites to this.", "I don't trust you.")
        # elif ct("Ane"):
            # $ rc("Could you perhaps not get me involved in this? It is quite the bother.", "Sorry. Maybe some other time.")
        # elif ct("Kamidere"):
            # $ rc("I don't think I should...", "No way! You're looking at me all lewd!")
        # elif ct("Bokukko"):
            # $ rc("Ah... This's kind of a huge pain...", "Mm, sounds kinda boring, y'know?")
        # else:
            # $ rc("I don't feel like it.", "Something about this seems kinda suspicious... I think I'll pass.")

label interactions_sparring: # sparring with MC, for Combatant occupations only
    $ interactions_check_for_bad_stuff(char)
    $ m = interactions_flag_count_checker(char, "flag_interactions_girlfriend")

    if char.health < char.get_max("health")*.5:
        call interactions_refused_because_tired from _call_interactions_refused_because_tired
        jump girl_interactions
    elif hero.health < hero.get_max("health")*.5:
        "Unfortunately, you are not in shape for sparring."
        jump girl_interactions
    elif m > 1:
        call interactions_refused_because_tired from _call_interactions_refused_because_tired_1
        jump girl_interactions

    call interactions_presparring_lines from _call_interactions_presparring_lines
    hide screen girl_interactions

    $ last_track = renpy.music.get_playing("world")
    $ back = interactions_pick_background_for_fight(gm.label_cache)

    python:
        enemy_team = Team(name="Enemy Team")
        enemy_team.add(char)

        your_team = Team(name="Your Team")
        your_team.add(hero)
        result = run_default_be(enemy_team, your_team=your_team,
                                background=back, give_up="surrender")

    if result is True:
        $ hero.exp += exp_reward(hero, char, ap_used=.33)
    elif result is False:
        $ char.exp += exp_reward(char, hero, ap_used=.33)

    if char.health < char.get_max("health")*.5:
        $ char.health = int(char.get_max("health")*.5)
    if hero.health < hero.get_max("health")*.5:
        $ hero.health = int(hero.get_max("health")*.5)
    if last_track:
        play world last_track

    $ gm.restore_img()

    show screen girl_interactions

    if gm.mode == "girl_interactions":
        scene expression select_girl_room(char, gm.img)
    else:
        show expression gm.bg_cache

    call interactions_postsparring_lines from _call_interactions_postsparring_lines
    jump girl_interactions

label interactions_presparring_lines: # lines before sparring
    if ct("Impersonal") in  char.traits:
        $ rc("Understood. Initialising battle mode.", "Very well. Switching to training mode.")
    elif ct("Imouto"):
        $ rc("Behold of my amazing combat techniques, [char.mc_ref]! ♪", "Activate super duper mega ultra assault mode! ♪")
    elif ct("Dandere"):
        $ rc("Let's end this quickly, [char.mc_ref]. We have many other things to do.",  "Let's see who's stronger.")
    elif ct("Kuudere"):
        $ rc("Fine, I accept your challenge.", "Let's fight fair and square.")
    elif ct("Tsundere"):
        $ rc("I won't go easy on you!", "Fine, I'll show you how it's done.")
    elif ct("Bokukko"):
        $ rc("I'm gonna whack you good!", "All right, let's clean this up fast!")
    elif ct("Ane"):
        $ rc("Hehe, let's both do our best.", "Fine, but let's be careful, ok?")
    elif ct("Kamidere"):
        $ rc("Alright, let's see what you can do.", "I suppose a have a few minutes to spare.")
    elif ct("Yandere"):
        $ rc("Sure, but don't blame me if it gets a little rough...", "I'll try to be gentle, but no promises.")
    else:
        $ rc("I don't mind. Let's do it.", "Sure, I can use some exercises. ♪")
    return

label interactions_postsparring_lines: # lines after sparring
    if result:
        $ char.disposition += randint(15, 30)
    else:
        $ char.disposition += randint(2, 5)
    if ct("Impersonal") in  char.traits:
        $ rc("Practice is over. Switching to standby mode.", "An unsurprising victory.")
    elif ct("Imouto"):
        $ rc("Woohoo! Getting stronger every day!", "Haha, it was fun! We should do it again!")
    elif ct("Dandere"):
        $ rc("Guess that does it. Good fight.", "Ok, I suppose we can leave it at this.")
    elif ct("Kuudere"):
        $ rc("You are a worthy opponent.", "We both still have much to learn.")
    elif ct("Tsundere"):
        $ rc("Jeez, now I'm tired after all that.", "Haaa... It was pretty intense.")
    elif ct("Bokukko"):
        $ rc("Oh, we done fighting already?", "Not a bad exercise, was it?")
    elif ct("Ane"):
        $ rc("Oh my, I think I may have overdone it a little. Apologies.", "It didn't look pretty, but what matters is who's standing at the end.")
    elif ct("Kamidere"):
        $ rc("I'm tired. We are done here.", "I suppose it was a valuable experience.")
    elif ct("Yandere"):
        $ rc("Sorry, I got carried away. But you did well nevertheless.", "Goodness, look at this. I got my clothes all dirty.")
    else:
        $ rc("You're pretty good.", "Phew... We should do this again sometime.")
    return

label interactions_girlfriend:
    $ interactions_check_for_bad_stuff(char)
    if check_lovers(char, hero): # you never know
        "But you already are!"
        jump girl_interactions
    $ m = interactions_flag_count_checker(char, "flag_interactions_girlfriend")
    if m > 1:
        call interactions_too_many_lines from _call_interactions_too_many_lines_8
        $ char.disposition -= randint(1,m)
        if char.joy > 50:
            $ char.joy -= randint(0,1)
        $ del m
        jump girl_interactions
    if ct("Lesbian") and not "Yuri Expert" in hero.traits:
        call interactions_lesbian_refuse_because_of_gender from _call_interactions_lesbian_refuse_because_of_gender_1
        jump girl_interactions
    $ l_ch = 0
    if ct("Shy"):
        $ l_ch -= 10
    if ct("Virgin"):
        $ l_ch -= 10
    elif ct("MILF"):
        $ l_ch += 10
    if ct("Nymphomaniac"):
        $ l_ch += 30
    if ct("Frigid"):
        $ l_ch -= 30
    if ct("Lesbian") and not "Yuri Expert" in hero.traits:
        $ l_ch -= 50
    if ct("Impersonal"):
        $ l_ch += 50
    elif ct("Kuudere"):
        $ l_ch += 30
    elif ct("Dandere"):
        $ l_ch += 20
    elif ct("Tsundere"):
        $ l_ch += 40
    elif ct("Imouto"):
        $ l_ch += 60
    elif ct("Bokukko"):
        $ l_ch += 70
    elif ct("Ane"):
        $ l_ch += 50
    elif ct("Kamidere"):
        $ l_ch += 60
    elif ct("Yandere"):
        $ l_ch += 80
    else:
        $ l_ch += 70
        
    if char.status == "slave":
        $ l_ch += 200

    if (char.flag("quest_cannot_be_lover") != True) and (char.disposition >= (600 - l_ch)) and (dice(round((l_ch + char.disposition)*.2))):
        $ set_lovers(hero, char)
        # $ hero.exp += randint(15, 35)
        # $ char.exp += randint(15, 35)
        $ hero.exp += exp_reward(hero, char, ap_used=.33)
        $ char.exp += exp_reward(char, hero, ap_used=.33)
        $ char.joy += 25
        $ char.override_portrait("portrait", "shy")
        if ct("Impersonal") in  char.traits:
            $ rc("You want me to have an affair with you. Understood.", "As you wish. I'm yours.", "I understand. I suppose we're now lovers.")
        elif ct("Shy") and dice(20):
            $ rc("I-If you're okay with me...", "V-very well...  I-I'll work hard to be a woman fit to be with you.", "F-fine then...")
        elif ct("Imouto"):
            $ rc("Mufufu... Behold, the birth of a new lovey-dovey couple!", "I-I um, I like you too, actually, ehehe♪", "Yes... Give me lots of love, please ♪")
        elif ct("Dandere"):
            $ rc("Okay. From this moment on, we are completely bound by destiny... Ehe.", "I will dedicate all of my passionate feelings to you.")
        elif ct("Kuudere"):
            $ rc("There's nothing about you I hate. I suppose I could let you have an affair with me.", "I don't mind, but... Prepare yourself.", "I'm, umm... yours...", "Are you really ok with me? Okay, let's go out together.")
        elif ct("Tsundere"):
            $ rc("Haah... Why did I fall in love with someone like this...? I guess it's fine, though.", "Hmph... It's YOU we're talking about, so I thought something like this might happen.")
        elif ct("Bokukko"):
            $ rc("I-I guess I could if you're g-gonna go that far.", "You've got weird taste, falling for a girl like me... Don't regret this, okay?", "I like you too, so we should be good to go, right?")
        elif ct("Ane"):
            $ rc("Hmhm, I'll try establishing a relationship.", "Hmhmhm... I'm quite the troublesome woman, you know...?", "I swear I'll make you happy!")
        elif ct("Kamidere"):
            $ rc("Yes, I suppose it's time things got serious.", "I feel the same way.", "Alright, you'd better take good care of me as your girlfriend.")
        elif ct("Yandere"):
            $ rc("Of course! Now no one can keep us apart! Hehe ♪", "We're sweethearts now?　Finally! ♪", "I want to be yours as well ♪", "Huhu, I'm not responsible if you regret it...", "You wanna do something dirty with me, right? You'd better!")
        else:
            $ rc("Yes... I'll be by your side forever... Hehehe ♪", "O-Okay... Ahaha, this is kinda embarrassing...", "I guess I'm your girlfriend now. Hehe ♪")
    else:
        $ char.override_portrait("portrait", "indifferent")
        if ct("Impersonal"):
            $ rc("Unable to process.", "I'm sorry, but I must refuse you.")
        elif ct("Shy") and dice(30):
            $ rc("Sorry... I'm... still not ready to go that far...", "Ah... Eh... Aah! This is a joke... Right?")
        elif ct("Imouto"):
            $ rc("Sure, wh-... Mmmm! ...Come to think of it...it's a bad idea after all...", "Ufufu, I'm not falling for that joke!", "Geez♪, stop joking around♪")
        elif ct("Dandere"):
            $ rc("Nice weather today.", "I am not interested at the moment.", "Sorry, you're not my type.")
        elif ct("Kuudere"):
            $ rc("That...wasn't very funny, you know?", "...No.", "I'm not strong enough to date someone I don't care for...", "...L-let me think about it.")
        elif ct("Tsundere"):
            $ rc("Hmph. You're out of your league.", "How about you go kill yourself?", "Y...you idiot! D... don't say something so embarassing like that!", "Jeez, please take your relationships more seriously!")
        elif ct("Bokukko"):
            $ rc("Drop it, this sounds like it'll be a huge pain in the ass.", "S-stop asking that stuff, you embarrass me...", "No way, what kind of girl do you think I am, geez...", "But you're my friend. Friends are friends, duh.")
        elif ct("Ane"):
            $ rc("...I'm sure you'll find someone that matches you better than I do.", "There's no sense losing your head over something you can't possibly achieve, you know?", "I'm sorry, but I can't go out with you", "I appreciate your feelings... But I can't answer them.")
        elif ct("Yandere"):
            $ rc("No way!", "Don't ask me that", "What d'you mean...?", "Come on, if you wanna have me you gotta get out there and break a leg.")
        elif ct("Kamidere"):
            $ rc("That's not for you to decide.", "That's too bad, I have no interest in you.", "That sort of relationship will be a big problem for both of us, you know?", "Being in a relationship is more trouble than it's worth.", "No way. I mean, you're just not good enough for me.")
        else:
            $ rc("I-I'm sorry! Let's just be good friends!", "That's... I'm sorry! Please let's continue being good friends!", "What's your problem? Saying that out of nowhere.", "That's nice of you to say, but... I can't help you there.")
    $ char.restore_portrait()
    $ del l_ch
    jump girl_interactions

label int_girl_proposes_girlfriend: # character proposes to become lovers
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $ rc("I love you. I want to stay by your side.", "I love you. Let me hear your answer.", "I request permission to date you.", "I seem to have taken a liking to you...  Please go out with me.")
    elif ct("Shy") and dice(50):
        $ rc("I... like you, and I want to be with you forever...", "I-I-I-I am in love with y-you...", "Sorry... No matter what I do, I can't get you out of my head... So... Go out with me!", "Do you want to try, um...going out with me?")
    elif ct("Imouto"):
        $ rc("I-I... I love... you... I'm in love with you...", "Uhm... I love you! ...Please go out with me!", "I really like you, you know... So um...I want you to go out with me!")
    elif ct("Dandere"):
        $ rc("I want to be your special person...", "I love you... Please let me be beside you, from now on.", "It seems like I really fell in love with you... So... won't you make me your lover?")
    elif ct("Tsundere"):
        $ rc("L-listen up. I'm only gonna say this once.. I love you... S-so! G-go out with me!", "I l-like you... Like you so much that I can't do anything about it!", "So, um... Should we, maybe, start dating... or something?", "I'll only say this once, so listen up... I love you... I want you to date me!"),
    elif ct("Kuudere"):
        $ rc("*sigh*... Dammit, I won't hide it anymore... I just can't help it... I'm totally in love with you...", "Even though I don't get it myself... It seem like I've fallen in love with you.", "E-Excuse me... would you like to date me?")
    elif ct("Kamidere"):
        $ rc("This really sucks for me, but... I love you... I said I love you!", "I like you... I love you. I'd like to hear how you feel.", "There's nothing about you I hate. So, would you become my lover?")
    elif ct("Bokukko"):
        $ rc("Um... Would you try going out with me? I mean... I'm in love with you...", "You know, the two of us get along really well, right? So then, well... Do you want to try going out with me...?", "Um, so... What're your thoughts on like, me bein' your girlfriend...?")
    elif ct("Ane"):
        $ rc("It seems like I fell in love with you... Won't you go out with me?", "I've fallen in love with you... Won't you go out with me?", "If I'm not a bother, would you... like to go out together?", "I love you... Please go out with me.")
    elif ct("Yandere"):
        $ rc("I love you! Your heart and soul, I want it all!", "I... I like you! Please be my lover!", "I love you... Please date me.", "Um... I love you.. So be my 'darling'!")
    else:
        $ rc("I... love you. Please go out with me!", "I... I love you... M-make me your girlfriend!", "Hey, listen. I want you... to go out with me.", "I love you... I want to be by your side forever... So, please be my sweetheart!", "Um, so hey... I like you, please go out with me...")
    $ char.restore_portrait()
    return

##### j3
label interactions_hire:
    if char.flag("quest_cannot_be_hired") == True:
        call interactions_refuses_to_be_hired from _call_interactions_refuses_to_be_hired
        jump girl_interactions

    python:
        heroskillz = 0
        girlskillz = 0
        mod_chance = 0

    python hide:
        mtraits = []
        for t in char.traits:
            if t.basetrait:
                mtraits.append(t)

        for i in mtraits:
            for s in i.base_stats:
                store.heroskillz += getattr(hero, s)
                store.girlskillz += getattr(char, s)

        store.heroskillz += hero.charisma

        if char.arena_willing and hero.arena_rep > char.arena_rep:
            store.heroskillz += 100

        store.heroskillz *= (hero.tier+1)*.1 + 1
        store.girlskillz *= (char.tier+1)*.1 + 1

        # and finally get the difference and make sure overwhelming difference
        # will not allow a girl to join at -900 disposition :):
        store.mod_chance = heroskillz - girlskillz

        if store.mod_chance > 700:
            store.mod_chance = 700

    if DEBUG:
        $ notify("Hero|Char| Mod: {}|{}| {}".format(heroskillz, girlskillz, mod_chance))

    python:
       del girlskillz
       del heroskillz

    # Solve chance
    if char.disposition > 500 - mod_chance:
        call interactions_agrees_to_be_hired from _call_interactions_agrees_to_be_hired

        $ del mod_chance

        menu:
            "Hire her? Her average wage will be [char.expected_wage]":
                $ gm.remove_girl(char)
                $ hero.add_char(char)
                hide screen girl_interactions

                $ gm.see_greeting = True

                jump expression gm.label_cache

            "Maybe later." :
                jump girl_interactions

    else:
        $ del mod_chance

        call interactions_refuses_to_be_hired from _call_interactions_refuses_to_be_hired_1
        jump girl_interactions

label interactions_agrees_to_be_hired:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("You want me work for you. Understood.")
    elif ct("Shy") and dice(50):
        $ rc("P-please take care of me...")
    elif ct("Imouto"):
        $ rc("Okey! Just, you know, don't boss me around too much ♪")
    elif ct("Dandere"):
        $ rc("Your proposition meets my goals. I accept it.")
    elif ct("Tsundere"):
        $ rc("Fine, fine. If you want it so much, I won't refuse."),
    elif ct("Kuudere"):
        $ rc("Very well. Please treat me well.")
    elif ct("Kamidere"):
        $ rc("I suppose I don't have any reasons to refuse.")
    elif ct("Bokukko"):
        $ rc("Sure, why not. Just be a good boss, ok?")
    elif ct("Ane"):
        $ rc("It's an acceptable proposition.")
    elif ct("Yandere"):
        $ rc("I don't have any objections.")
    else:
        $ rc("Alright, I agree ♪")
    $ char.restore_portrait()
    return

label interactions_refuses_to_be_hired:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("Denied.")
    elif ct("Shy") and dice(50):
        $ rc("S-sorry, I don't think I can...")
    elif ct("Imouto"):
        $ rc("Sounds boring... Think I'm gonna pass.")
    elif ct("Dandere"):
        $ rc("Thanks, but I will refrain.")
    elif ct("Tsundere"):
        $ rc("Are you out of your mind? Why should I agree to that?"),
    elif ct("Kuudere"):
        $ rc("No. Don't want to.")
    elif ct("Kamidere"):
        $ rc("Please don't involve me in your business. I have enough things to worry about already.")
    elif ct("Bokukko"):
        $ rc("Nah, too much trouble.")
    elif ct("Ane"):
        $ rc("Sorry. Maybe some other time.")
    elif ct("Yandere"):
        $ rc("No, I have no such intentions.")
    else:
        $ rc("Sorry, not interested.")
    $ char.restore_portrait()
    return
