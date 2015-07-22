###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - proposition - friends
#  2 - proposition - girlfriend
#  3 - proposition - hire

###### j1
label interactions_friends:
    if chr.disposition > 500:
        if ct("Impersonal"):
            $rc("Very well.", "Alright.")
        elif ct("Shy") and dice(30):  
            $rc("Umm... That is... I-I'm in your care...!", "I think of you as a precious friend too.")
        elif ct("Kuudere"):  
            $rc("I can't think of any reason to refuse. Sure, why not.", "...Looks like we're a good match.")
        elif ct("Dandere"):
            $rc("I agree.", "I understand...", "Please...take good care of me.")
        elif ct("Tsundere"):
            $rc("I suppose I have no choice.", "Fine ...I-it's not like this makes me happy!")
        elif ct("Imouto"):
            $rc("R-Really...? Fuaah, I'm so glad!", "We'll be friends forever, right?", "Hehehe♪ We somehow became good friends, huh?")
        elif ct("Bokukko"):
            $rc("Hmm, okay, sounds good!", "I s'pose I could.", "Feels nice having someone support me for a change.")
        elif ct("Ane"):
            $rc("Yes, that would be acceptable.", "Looks like you and I could be good partners.")
        elif ct("Kamidere"):  
            $rc("Yes, with pleasure. Treat me well, okay?♪", "Please continue to be good friends with me.")
        elif ct("Yandere"):  
            $rc("You know, I'd be totally up for sex friend status.♪", "Well, we get along fine...")
        else:
           $rc("Mm, alright.", "Okay!", "I have the feeling I could get along with you.", "Hehehe, it's great to be friends～♪", "Of course. Let's get along♪")
    else:
        if ct("Impersonal"):  
            $rc("Not interested.", "I cannot understand. Please give me a detailed explanation.")
        elif ct("Shy") and dice(30):
            $rc("I-I'm really sorry...", "Another time, maybe...", "Eh?")
        elif ct("Tsundere"):
            $rc("Huh? Why should I agree to that?", "Uh? Wha...what are you talking about?")
        elif ct("Kuudere"):
            $rc("There's all sorts of problems with that.", "A bother. Don't wanna.")
        elif ct("Dandere"):
            $rc("Smells suspicious. I will refrain.", "If I feel like it.")
        elif ct("Imouto"):
            $rc("Umm, uh... Sorry. Tehe♪", "Sure... Pfft... Just kidding, I lied～!", "I... don't trust you.")
        elif ct("Yandere"):
           $rc("Maybe laterー", "Eeeh～...?")
        elif ct("Ane"):
            $rc("Could you perhaps not get me involved in this? It is quite the bother.")
        elif ct("Kamidere"):
            $rc("I don't think I should...", "No way! You're looking at me all lewd!")
        elif ct("Bokukko"):
            $rc("Ahー... This's kind of a huge pain...", "Mm, sounds kinda boring, y'know?")
        else:
            $rc("Maybe some other time.", "Something about this seems kinda suspicious... I think I'll pass.", "Nope", "Sorry. Maybe some other time.")
    
    jump girl_interactions
    

###### j2    
label interactions_girlfriend:
    if chr.disposition > 800:
        if ct("Impersonal") in  chr.traits:
            $rc("You want me to have an affair with you. Understood.", "As you wish. I'm yours.", "I understand. I suppose we're now lovers.")
        elif ct("Shy") and dice(20):  
            $rc("I-If you're okay with me...", "V-very well...  I-I'll work hard to be a woman fit to be with you.", "F-fine then...")
        elif ct("Imouto"):
            $rc("Mufufu... Behold, the birth of a new lovey-dovey couple!", "I-I um, I like you too, actuallyー, ehehe♪", "Yes... Give me lots of love, please♪")
        elif ct("Dandere"):
            $rc("Okay. From this moment on, we are completely bound by destiny... Ehe.", "I will dedicate all of my passionate feelings to you.")
        elif ct("Kuudere"):  
            $rc("There's nothing about you I hate. I suppose I could let you have an affair with me.", "Didn't expect you of all people to say that... Haha.", "I don't mind, but... Prepare yourself.", "I'm, umm... yours...")
        elif ct("Tsundere"):
            $rc("Haah... Why did I fall in love with someone like this...? I guess it's fine, though.", "Hmph... It's YOU we're talking about, so I thought something like this might happen.")
        elif ct("Bokukko"):  
            $rc("I-I guess I could if you're g-gonna go that far.", "You've got weird taste, falling for a girl like me... Don't regret this, okay?")
        elif ct("Ane"):
            $rc("Hmhm, I'll try establishing a relationship.", "Hmhmhm... I'm quite the troublesome woman, you know...?", "I swear I'll make you happy!")
        elif ct("Kamidere"):
            $rc("Yes, I suppose it's time things got serious.", "I feel the same way.")
        elif ct("Yandere"):
            $rc("Of course! Now no one can keep us apart! Hehe♪", "We're sweethearts now?　Finally!♪", "I want to be yours as well♪", "Huhu, I'm not responsible if you regret it...", "You wanna do something dirty with me, right? You'd better!")
        else:
            $rc("Yes... I'll be by your side forever... Hehehe♪", "Gosh. Fine...", "O-Okay... Ahaha, this is kinda embarrassing...", "I guess I'm your girlfriend now.")
    else:
        if ct("Impersonal"):
            $rc("Unable to process.", "I'm sorry, but I must refuse you.")
        elif ct("Lesbian") and dice(50):  
            $rc("I'm terribly sorry, but... I can't do that with a man!", "Men for me are...well...", "Sorry. I'm weird, so... I'm not into guys.", "Men are...no.")
        elif ct("Shy") and dice(30):  
            $rc("Sorry... I'm... still not ready to go that far...", "Ah... Eh... Aah! This is a joke... Right?")
        elif ct("Imouto"):
            $rc("Sure, wh-... Mmmm! ...Come to think of it...it's a bad idea after all...", "Ufufu, I'm not falling for that joke!", "Geez～, stop joking around～")
        elif ct("Dandere"):
            $rc("Nice weather today.", "I am not interested at the moment.", "Sorry, you're not my type.")
        elif ct("Kuudere"):
            $rc("That...wasn't very funny, you know?", "...No.", "I'm not strong enough to date someone I don't care for...", "...L-let me think about it.")
        elif ct("Tsundere"):
            $rc("Hmph. You're out of your league.", "How about you go kill yourself?", "Y...you idiot! D... don't say something so embarassing like that!", "Jeez, please take your relationships more seriously!")
        elif ct("Bokukko"):  
            $rc("Drop it, this sounds like it'll be a huge pain in the ass.", "S-stop asking that stuff, you embarrass me...", "No way, what kind of girl do you think I am, geez...")
        elif ct("Ane"):
            $rc("...I'm sure you'll find someone that matches you better than I do.", "There's no sense losing your head over something you can't possibly achieve, you know?", "I'm sorry, but I can't go out with you", "I appreciate your feelings... But I can't answer them.")
        elif ct("Yandere"):  
            $rc("No way!", "Don't ask me that", "What d'you mean...?")
        elif ct("Kamidere"):
            $rc("That's not for you to decide.", "That's too bad, I have no interest in you.", "That sort of relationship will be a big problem for both of us, you know?", "Being in a relationship is more trouble than it's worth.")
        else: 
            $rc("I-I'm sorry! Let's just be good friends!", "That's... I'm sorry! Please let's continue being good friends!", "What's your problem? Saying that out of nowhere.", "That's nice of you to say, but... I can't help you there.")
    
    jump girl_interactions

##### j3    
label interactions_hire:
    
    if co("Warrior"):
        python:
            # get skills relevant to occupation:
            heroskillz = 0
            girlskillz = 0
            
            for stat in ilists.battlestats:
                heroskillz += getattr(hero, stat)
                girlskillz += getattr(chr, stat)
            
            # add charisma:    
            heroskillz += hero.charisma
            girlskillz += chr.charisma
            
            # if girl wants to be in the arena and heros arena rep is a lot higher, we'll throw in another 100
            if chr.arena_willing and chr.arena_rep > 0:
                if hero.arena_rep > chr.arena_rep * 5:
                    heroskillz += 100
            
            # and finally get the difference and make sure overwhelming difference will not allow a girl to join at -900 desposition :):
            mod_chance = heroskillz - girlskillz
            
            # if mod_chance in on heros side, we should increase girls disposition just because he asked:
            if mod_chance > 50:
                chr.disposition += randint(10, 15)
            
            if mod_chance > 500: mod_chance = 500
    
    elif co("Server"):
        python:
            # get skills relevant to occupation:
            heroskillz = hero.charisma * 3
            girlskillz = chr.charisma * 3
            
            # and finally get the difference and make sure overwhelming difference will not allow a girl to join at -900 desposition :):
            mod_chance = heroskillz - girlskillz
            
            # if mod_chance in on heros side, we should increase girls disposition just because he asked:
            if mod_chance > 50:
                chr.disposition += randint(10, 15)
            
            if mod_chance > 200: mod_chance = 200
    
    elif co("Specialist"):
        python:
            # get skills relevant to occupation:
            heroskillz = hero.character * 4
            girlskillz = chr.character * 4
            
            # and finally get the differense and make sure overwhelming difference will not allow a girl to join at -900 desposition :):
            mod_chance = heroskillz - girlskillz
            
            # if mod_chance in on heros side, we should increase girls disposition just because he asked:
            if mod_chance > 50:
                chr.disposition += randint(10, 15)
            
            if mod_chance > 400: mod_chance = 400
    
    elif co("SIW"):
        python:
            # get skills relevant to occupation:
            heroskillz = hero.charisma * 4
            girlskillz = chr.charisma * 4
            
            # if girl wants to be in the arena and heros arena rep is a lot higher, we'll throw in another 100
            if chr.arena_willing and chr.arena_rep > 0:
                if hero.arena_rep > chr.arena_rep * 5:
                    heroskillz += 100
            
            # and finally get the differense and make sure overwhelming difference will not allow a girl to join at -900 desposition :):
            mod_chance = heroskillz - girlskillz
            
            # if mod_chance in on heros side, we should increase girls disposition just because he asked:
            if mod_chance > 50:
                chr.disposition += randint(10, 15)
            
            if mod_chance > 400: mod_chance = 400
    
    else:
        $ raise Error, "Unknown occupation @ girl_interactions/hire"
    
    python:
       del girlskillz
       del heroskillz
    
    # Solve chance
    if chr.disposition > 500 - mod_chance:
        $g(choice(["Ok. I guess I could try working for you.",
                   "You seem like a good employer!",
                   "Thanks, I'll take the offer!"]))
        
        $ del mod_chance
        
        menu:
            "Hire her as [chr.occupation].":
                $pytfall.gm.remove_girl(chr)
                $hero.add_girl(chr)
                hide screen pyt_girl_interactions
                
                $ pytfall.gm.see_greeting = True
                
                jump expression pytfall.gm.label_cache
            
            "Maybe later." :
                jump girl_interactions
    
    else:
        $ del mod_chance
        
        $g(choice(["You're kidding, right?", "I don't want to work for you.", "Me working for you? Seriously?"]))
        jump girl_interactions
    
