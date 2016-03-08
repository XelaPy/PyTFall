label interactions_friends:
    "You ask her to become your friend."
    if check_friends(char, hero):
        "But you already are!"
        python:
            char.AP += 1
            hero.AP += 1
        jump girl_interactions
    if ct("Shy"):  
        $ fr_ch = -10
    else:
        $ fr_ch = 0
    if ct("Impersonal"):
        $ fr_ch += 50
    elif ct("Kuudere"):  
        $ fr_ch += 30
    elif ct("Dandere"):
        $ fr_ch += 20
    elif ct("Tsundere"):
        $ fr_ch += 40
    elif ct("Imouto"):
        $ fr_ch += 80
    elif ct("Bokukko"):
        $ fr_ch += 70
    elif ct("Ane"):
        $ fr_ch += 90
    elif ct("Kamidere"):  
        $ fr_ch += 60
    elif ct("Yandere"):  
        $ fr_ch += 50
    else:
        $ fr_ch += 70
    if (char.disposition >= (250 - fr_ch)) and (dice(round((fr_ch + char.disposition)*0.25))):
        $ set_friends(hero, char)
        $ hero.exp += randint(10, 30)
        $ char.exp += randint(10, 30)
        $ char.joy += 20
        $ char.override_portrait("portrait", "happy")
        if ct("Impersonal"):
            $rc("Very well.", "Alright.")
        elif ct("Shy") and dice(40):  
            $rc("Umm... That is... I-I'm in your care...!", "I think of you as a precious friend too.")
        elif ct("Kuudere"):  
            $rc("I can't think of any reason to refuse. Sure, why not.", "...Looks like we're a good match.")
        elif ct("Dandere"):
            $rc("I agree.", "I understand...", "Please...take good care of me.")
        elif ct("Tsundere"):
            $rc("I suppose I have no choice.", "Fine ...I-it's not like this makes me happy!")
        elif ct("Imouto"):
            $rc("R-Really...? Fuaah, I'm so glad!", "We'll be friends forever, right?", "Hehehe ♪ We somehow became good friends, huh?")
        elif ct("Bokukko"):
            $rc("Hmm, okay, sounds good!", "I s'pose I could.", "Feels nice having someone support me for a change.")
        elif ct("Ane"):
            $rc("Yes, that would be acceptable.", "Looks like you and I could be good partners.")
        elif ct("Kamidere"):  
            $rc("Yes, with pleasure. Treat me well, okay? ♪", "Please continue to be good friends with me.")
        elif ct("Yandere"):  
            $rc("I have the feeling I could get along with you.",  "Well, we get along fine... Alright.")
        else:
           $rc("Mm, alright.", "Okay!", "Hehehe, it's great to be friends ♪", "Of course. Let's get along ♪")
    else:
        $ char.override_portrait("portrait", "indifferent")
        if ct("Impersonal"):  
            $rc("Not interested.", "I cannot understand. Please give me a detailed explanation.")
        elif ct("Shy") and dice(40):
            $rc("I-I'm really sorry...", "Another time, maybe...")
        elif ct("Tsundere"):
            $rc("Huh? Why should I agree to that?", "Uh? Wha...what are you talking about?")
        elif ct("Kuudere"):
            $rc("There's all sorts of problems with that.", "A bother. Don't want to.")
        elif ct("Dandere"):
            $rc("Smells suspicious. I will refrain.", "If I feel like it.")
        elif ct("Imouto"):
            $rc("Umm, uh... Sorry. Hehe♪", "Sure... Pfft... Just kidding, I lied!")
        elif ct("Yandere"):
           $rc("Maybe later", "I don't trust you.")
        elif ct("Ane"):
            $rc("Could you perhaps not get me involved in this? It is quite the bother.", "Sorry. Maybe some other time.")
        elif ct("Kamidere"):
            $rc("I don't think I should...", "No way! You're looking at me all lewd!")
        elif ct("Bokukko"):
            $rc("Ah... This's kind of a huge pain...", "Mm, sounds kinda boring, y'know?")
        else:
            $rc("I don't feel like it.", "Something about this seems kinda suspicious... I think I'll pass.")
    $ char.restore_portrait()
    $ del fr_ch
    jump girl_interactions
    

###### j2    
label interactions_girlfriend:
    "You proposing to become lovers."
    if check_lovers(char, hero): # you never know
        "But you already are!"
        jump girl_interactions
    if ct("Lesbian"):
        call interactions_lesbian_refuse_because_of_gender
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
    if ct("Lesbian"):
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
    
    if (char.flag("quest_cannot_be_lover") != True) and (char.disposition >= (500 - l_ch)) and (dice(round((l_ch + char.disposition)*0.2))):
        $ set_lovers(hero, char)
        $ hero.exp += randint(15, 35)
        $ char.exp += randint(15, 35)
        $ char.joy += 25
        $ char.override_portrait("portrait", "shy")
        if ct("Impersonal") in  char.traits:
            $rc("You want me to have an affair with you. Understood.", "As you wish. I'm yours.", "I understand. I suppose we're now lovers.")
        elif ct("Shy") and dice(20):  
            $rc("I-If you're okay with me...", "V-very well...  I-I'll work hard to be a woman fit to be with you.", "F-fine then...")
        elif ct("Imouto"):
            $rc("Mufufu... Behold, the birth of a new lovey-dovey couple!", "I-I um, I like you too, actually, ehehe♪", "Yes... Give me lots of love, please ♪")
        elif ct("Dandere"):
            $rc("Okay. From this moment on, we are completely bound by destiny... Ehe.", "I will dedicate all of my passionate feelings to you.")
        elif ct("Kuudere"):  
            $rc("There's nothing about you I hate. I suppose I could let you have an affair with me.", "I don't mind, but... Prepare yourself.", "I'm, umm... yours...", "Are you really ok with me? Okay, let's go out together.")
        elif ct("Tsundere"):
            $rc("Haah... Why did I fall in love with someone like this...? I guess it's fine, though.", "Hmph... It's YOU we're talking about, so I thought something like this might happen.")
        elif ct("Bokukko"):  
            $rc("I-I guess I could if you're g-gonna go that far.", "You've got weird taste, falling for a girl like me... Don't regret this, okay?", "I like you too, so we should be good to go, right?")
        elif ct("Ane"):
            $rc("Hmhm, I'll try establishing a relationship.", "Hmhmhm... I'm quite the troublesome woman, you know...?", "I swear I'll make you happy!")
        elif ct("Kamidere"):
            $rc("Yes, I suppose it's time things got serious.", "I feel the same way.", "Alright, you'd better take good care of me as your girlfriend.")
        elif ct("Yandere"):
            $rc("Of course! Now no one can keep us apart! Hehe ♪", "We're sweethearts now?　Finally! ♪", "I want to be yours as well♪", "Huhu, I'm not responsible if you regret it...", "You wanna do something dirty with me, right? You'd better!")
        else:
            $rc("Yes... I'll be by your side forever... Hehehe ♪", "O-Okay... Ahaha, this is kinda embarrassing...", "I guess I'm your girlfriend now. Hehe ♪")
    else:
        $ char.override_portrait("portrait", "indifferent")
        if ct("Impersonal"):
            $rc("Unable to process.", "I'm sorry, but I must refuse you.")
        elif ct("Shy") and dice(30):  
            $rc("Sorry... I'm... still not ready to go that far...", "Ah... Eh... Aah! This is a joke... Right?")
        elif ct("Imouto"):
            $rc("Sure, wh-... Mmmm! ...Come to think of it...it's a bad idea after all...", "Ufufu, I'm not falling for that joke!", "Geez♪, stop joking around♪")
        elif ct("Dandere"):
            $rc("Nice weather today.", "I am not interested at the moment.", "Sorry, you're not my type.")
        elif ct("Kuudere"):
            $rc("That...wasn't very funny, you know?", "...No.", "I'm not strong enough to date someone I don't care for...", "...L-let me think about it.")
        elif ct("Tsundere"):
            $rc("Hmph. You're out of your league.", "How about you go kill yourself?", "Y...you idiot! D... don't say something so embarassing like that!", "Jeez, please take your relationships more seriously!")
        elif ct("Bokukko"):  
            $rc("Drop it, this sounds like it'll be a huge pain in the ass.", "S-stop asking that stuff, you embarrass me...", "No way, what kind of girl do you think I am, geez...", "But you're my friend. Friends are friends, duh.")
        elif ct("Ane"):
            $rc("...I'm sure you'll find someone that matches you better than I do.", "There's no sense losing your head over something you can't possibly achieve, you know?", "I'm sorry, but I can't go out with you", "I appreciate your feelings... But I can't answer them.")
        elif ct("Yandere"):  
            $rc("No way!", "Don't ask me that", "What d'you mean...?", "Come on, if you wanna have me you gotta get out there and break a leg.")
        elif ct("Kamidere"):
            $rc("That's not for you to decide.", "That's too bad, I have no interest in you.", "That sort of relationship will be a big problem for both of us, you know?", "Being in a relationship is more trouble than it's worth.", "No way. I mean, you're just not good enough for me.")
        else: 
            $rc("I-I'm sorry! Let's just be good friends!", "That's... I'm sorry! Please let's continue being good friends!", "What's your problem? Saying that out of nowhere.", "That's nice of you to say, but... I can't help you there.")
    $ char.restore_portrait()
    $ del l_ch
    jump girl_interactions

label int_girl_proposes_girlfriend: # character proposes to become lovers
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $rc("I love you. I want to stay by your side.", "I love you. Let me hear your answer.", "I request permission to date you.", "I seem to have taken a liking to you...  Please go out with me.")
    elif ct("Shy") and dice(50):
        $rc("I... like you, and I want to be with you forever...", "I-I-I-I am in love with y-you...", "Sorry... No matter what I do, I can't get you out of my head...	So... Go out with me!", "Do you want to try, um...going out with me?")
    elif ct("Imouto"):
        $rc("I-I... I love... you... I'm in love with you...", "Uhm... I love you! ...Please go out with me!", "I really like you, you know... So um...I want you to go out with me!") 
    elif ct("Dandere"):
        $rc("I want to be your special person...", "I love you... Please let me be beside you, from now on.", "It seems like I really fell in love with you... So... won't you make me your lover?")
    elif ct("Tsundere"):
        $rc("L-listen up. I'm only gonna say this once.. I love you... S-so! G-go out with me!", "I l-like you... Like you so much that I can't do anything about it!", "So, um... Should we, maybe, start dating... or something?", "I'll only say this once, so listen up... I love you... I want you to date me!"),
    elif ct("Kuudere"):
        $rc("*sigh*... Dammit, I won't hide it anymore... I just can't help it... I'm totally in love with you...", "Even though I don't get it myself... It seem like I've fallen in love with you.", "E-Excuse me... would you like to date me?")
    elif ct("Kamidere"):
        $rc("This really sucks for me, but... I love you... I said I love you!", "I like you... I love you. I'd like to hear how you feel.", "There's nothing about you I hate. So, would you become my lover?")
    elif ct("Bokukko"):
        $rc("Um... Would you try going out with me? I mean... I'm in love with you...", "You know, the two of us get along really well, right? So then, well... Do you want to try going out with me...?", "Um, so... What're your thoughts on like, me bein' your girlfriend...?")
    elif ct("Ane"):
        $rc("It seems like I fell in love with you... Won't you go out with me?", "I've fallen in love with you... Won't you go out with me?", "If I'm not a bother, would you... like to go out together?", "I love you... Please go out with me.")
    elif ct("Yandere"):
        $rc("I love you! Your heart and soul, I want it all!", "I... I like you! Please be my lover!", "I love you... Please date me.", "Um... I love you.. So be my 'darling'!")
    else:
        $rc("I... love you. Please go out with me!", "I... I love you... M-make me your girlfriend!", "Hey, listen. I want you... to go out with me.", "I love you... I want to be by your side forever... So, please be my sweetheart!", "Um, so hey... I like you, please go out with me...")
    $ char.restore_portrait()
    return
    
##### j3    
label interactions_hire:
    if char.flag("quest_cannot_be_hired") == True:
        $g(choice(["You're kidding, right?", "I don't want to work for you.", "Me working for you? Seriously?"]))
        jump girl_interactions
    if cgo("Warrior"):
        python:
            # get skills relevant to occupation:
            heroskillz = 0
            girlskillz = 0
            
            for stat in ilists.battlestats:
                heroskillz += getattr(hero, stat)
                girlskillz += getattr(char, stat)
            
            # add charisma:    
            heroskillz += hero.charisma
            girlskillz += char.charisma
            
            # if girl wants to be in the arena and heros arena rep is a lot higher, we'll throw in another 100
            if char.arena_willing and char.arena_rep > 0:
                if hero.arena_rep > char.arena_rep * 5:
                    heroskillz += 100
            
            # and finally get the difference and make sure overwhelming difference will not allow a girl to join at -900 desposition :):
            mod_chance = heroskillz - girlskillz
            
            # if mod_chance in on heros side, we should increase girls disposition just because he asked:
            if mod_chance > 50:
                char.disposition += randint(10, 15)
            
            if mod_chance > 500: mod_chance = 500
    
    elif cgo("Server"):
        python:
            # get skills relevant to occupation:
            heroskillz = hero.charisma * 3
            girlskillz = char.charisma * 3
            
            # and finally get the difference and make sure overwhelming difference will not allow a girl to join at -900 desposition :):
            mod_chance = heroskillz - girlskillz
            
            # if mod_chance in on heros side, we should increase girls disposition just because he asked:
            if mod_chance > 50:
                char.disposition += randint(10, 15)
            
            if mod_chance > 200: mod_chance = 200
    
    elif cgo("Specialist"):
        python:
            # get skills relevant to occupation:
            heroskillz = hero.character * 4
            girlskillz = char.character * 4
            
            # and finally get the differense and make sure overwhelming difference will not allow a girl to join at -900 desposition :):
            mod_chance = heroskillz - girlskillz
            
            # if mod_chance in on heros side, we should increase girls disposition just because he asked:
            if mod_chance > 50:
                char.disposition += randint(10, 15)
            
            if mod_chance > 400: mod_chance = 400
    
    elif cgo("SIW"):
        python:
            # get skills relevant to occupation:
            heroskillz = hero.charisma * 4
            girlskillz = char.charisma * 4
            
            # if girl wants to be in the arena and heros arena rep is a lot higher, we'll throw in another 100
            if char.arena_willing and char.arena_rep > 0:
                if hero.arena_rep > char.arena_rep * 5:
                    heroskillz += 100
            
            # and finally get the differense and make sure overwhelming difference will not allow a girl to join at -900 desposition :):
            mod_chance = heroskillz - girlskillz
            
            # if mod_chance in on heros side, we should increase girls disposition just because he asked:
            if mod_chance > 50:
                char.disposition += randint(10, 15)
            
            if mod_chance > 400: mod_chance = 400
    
    else:
        $ raise Exception, "Unknown occupation @ girl_interactions/hire"
    
    python:
       del girlskillz
       del heroskillz
    
    # Solve chance
    if char.disposition > 500 - mod_chance:
        $g(choice(["Ok. I guess I could try working for you.",
                   "You seem like a good employer!",
                   "Thanks, I'll take the offer!"]))
        
        $ del mod_chance
        
        menu:
            # TODO: NEEDS TO BE UPDATED.
            "Hire her as [char.occupation].":
                $gm.remove_girl(char)
                $hero.add_girl(char)
                hide screen girl_interactions
                
                $ gm.see_greeting = True
                
                jump expression gm.label_cache
            
            "Maybe later." :
                jump girl_interactions
    
    else:
        $ del mod_chance
        
        $g(choice(["You're kidding, right?", "I don't want to work for you.", "Me working for you? Seriously?"]))
        jump girl_interactions
    