label interactions_clever:
    if (day - char.flag("gm_praise_day")) > 1 or char.flag("gm_praise_day") == 0: # you can do it once per 3 days, no matter the result
        "You trying to compliment her intelligence."
        $ inter_praise_1 = 0
        $ inter_praise_2 = 0
        $ inter_praise_3 = 0
        $ stats = ["charisma", "intelligence", "character", "constitution"]
        $ mean = sum(getattr(char, i) for i in stats)/len(stats) # we check the difference between the stat and average stats value
        $ int_differ = mean - char.intelligence
        if int_differ >= 0:
            $ inter_praise_1 = 1
      
        $ characters = [hero, char]
        $ char_with_the_highest_stat = max(characters, key=attrgetter("intelligence")) # we check who has higher stat
        if char_with_the_highest_stat != char:
            $ inter_praise_2 = 1

        $ statsmore = {s: getattr(char, s) for s in stats}
        $ stat_with_min_value = min(statsmore.iteritems(), key=itemgetter(1))[0] # we check if the stat is a min stat
        if stat_with_min_value == "intelligence":
            $ inter_praise_3 = 1

        $ inter_praise = inter_praise_1 + inter_praise_2 + inter_praise_3 # the more checks are true, the better result
        if inter_praise == 3:
            "She looks very happy."
        elif inter_praise == 2:
            "She looks happy."
        elif inter_praise == 1:
            "She looks a bit happier than before."
        else:
            "She's not impressed at all."
            jump praise_nope
        if char.disposition < 250:
            if char.character*2 > hero.refinement: # refinement tries to overcome character's stubbornness
                $ char.disposition += (randint (5, 10))*inter_praise
                $ char.joy += randint (10, 20)
            else:
                $ char.disposition += (randint (10, 15))*inter_praise
                $ char.joy += randint (15, 20)
        else:
            if char.character*2 > hero.refinement:
                $ char.joy += randint (10, 20)
            else:
                $ char.joy += randint (15, 20)
        $char.set_flag("gm_praise_day", value=day)
        call praise_yes
        jump girl_interactions
    else:
        "You already complimented her recently, so she's not impressed."
        jump praise_nope
        
label interactions_strong:
    if (day - char.flag("gm_praise_day")) > 1 or char.flag("gm_praise_day") == 0: # you can do it once per 3 days, no matter the result
        "You trying to compliment her physique."
        $ inter_praise_1 = 0
        $ inter_praise_2 = 0
        $ inter_praise_3 = 0
        $ stats = ["charisma", "intelligence", "character", "constitution"]
        $ mean = sum(getattr(char, i) for i in stats)/len(stats) # we check the difference between the stat and average stats value
        $ int_differ = mean - char.constitution
        if int_differ >= 0:
            $ inter_praise_1 = 1
      
        $ characters = [hero, char]
        $ char_with_the_highest_stat = max(characters, key=attrgetter("constitution")) # we check who has higher stat
        if char_with_the_highest_stat != char:
            $ inter_praise_2 = 1

        $ statsmore = {s: getattr(char, s) for s in stats}
        $ stat_with_min_value = min(statsmore.iteritems(), key=itemgetter(1))[0] # we check if the stat is a min stat
        if stat_with_min_value == "constitution":
            $ inter_praise_3 = 1

        $ inter_praise = inter_praise_1 + inter_praise_2 + inter_praise_3 # the more checks are true, the better result
        if inter_praise == 3:
            "She looks very happy."
        elif inter_praise == 2:
            "She looks happy."
        elif inter_praise == 1:
            "She looks a bit happier than before."
        else:
            "She's not impressed at all."
            jump praise_nope
        if char.disposition < 250:
            if char.character*2 > hero.refinement: # refinement tries to overcome character's stubbornness
                $ char.disposition += (randint (5, 10))*inter_praise
                $ char.joy += randint (10, 20)
            else:
                $ char.disposition += (randint (10, 15))*inter_praise
                $ char.joy += randint (15, 20)
        else:
            if char.character*2 > hero.refinement:
                $ char.joy += randint (10, 20)
            else:
                $ char.joy += randint (15, 20)
        $char.set_flag("gm_praise_day", value=day)
        call praise_yes
        jump girl_interactions
    else:
        "You already complimented her recently, so she's not impressed."
        jump praise_nope
        
label interactions_cute:
    if (day - char.flag("gm_praise_day")) > 1 or char.flag("gm_praise_day") == 0: # you can do it once per 3 days, no matter the result
        "You trying to compliment her physique."
        $ inter_praise_1 = 0
        $ inter_praise_2 = 0
        $ inter_praise_3 = 0
        $ stats = ["charisma", "intelligence", "character", "constitution"]
        $ mean = sum(getattr(char, i) for i in stats)/len(stats) # we check the difference between the stat and average stats value
        $ int_differ = mean - char.charisma
        if int_differ >= 0:
            $ inter_praise_1 = 1
      
        $ characters = [hero, char]
        $ char_with_the_highest_stat = max(characters, key=attrgetter("charisma")) # we check who has higher stat
        if char_with_the_highest_stat != char:
            $ inter_praise_2 = 1

        $ statsmore = {s: getattr(char, s) for s in stats}
        $ stat_with_min_value = min(statsmore.iteritems(), key=itemgetter(1))[0] # we check if the stat is a min stat
        if stat_with_min_value == "charisma":
            $ inter_praise_3 = 1

        $ inter_praise = inter_praise_1 + inter_praise_2 + inter_praise_3 # the more checks are true, the better result
        if inter_praise == 3:
            "She looks very happy."
        elif inter_praise == 2:
            "She looks happy."
        elif inter_praise == 1:
            "She looks a bit happier than before."
        else:
            "She's not impressed at all."
            jump praise_nope
        if char.disposition < 250:
            if char.character*2 > hero.refinement: # refinement tries to overcome character's stubbornness
                $ char.disposition += (randint (5, 10))*inter_praise
                $ char.joy += randint (10, 20)
            else:
                $ char.disposition += (randint (10, 15))*inter_praise
                $ char.joy += randint (15, 20)
        else:
            if char.character*2 > hero.refinement:
                $ char.joy += randint (10, 20)
            else:
                $ char.joy += randint (15, 20)
        $char.set_flag("gm_praise_day", value=day)
        call praise_yes
        jump girl_interactions
    else:
        "You already complimented her recently, so she's not impressed."
        jump praise_nope
        
label praise_nope:     
    if ct("Impersonal"):
        $rc("Bigmouth.", "...What'd you want?", "…?", "What a bother...", "...You talk too much.", "Pathetic...", "<She completely ignores you>", "...and?")
    elif ct("Shy") and dice(50):
        $ rc("U-um, you were talking to me? Oh ... <she's embarassed>", "Pl-please ... stop...", "Don't ... make fun of me.", "Uuuuuh <She starts crying>", "Well ... that ... <she looks like she wants to run away>", "Ah, I-I'm not… S-sorry…", "Really? I don't think… I-I'm sorry.", "<looks uncomfortable> No, I... umn... sorry.", "P-please, leave me be...")
    elif ct("Imouto"):
        $rc("Eh? You sound like a perv!", "Booring~!", "Huhn, who would fall for a line like that?")
    elif ct("Kuudere"):
        $rc("Stop that. Empty praises won't do you any good.", "You can stop talking now.", "Can't find something better to say?", "All talk and nothing to back it up. What are you even trying to do?", "I couldn't care less about what you think.")
    elif ct("Dandere"):
        $rc("...?", "That's...not true.", "I find that extremely hard to believe.", "Not funny.", "*sigh*… thank you...<looks bored>", "Please, drop this flattery.")
    elif ct("Tsundere"):
        $rc("What? I have no idea what you're talking about.", "Lay off the jokes; there's already one attached to the front of your head!")
    elif ct("Kamidere"):
        $rc("Don't try to pull the wool over my eyes. I know what you're after.", "Don't you have something better to do?", "What do you want, anyway?", "Are you making fun of me?", "What a supremely boring joke. You've got awful taste.")
    elif ct("Ane"):
        $rc("Whatever are you saying?", "That is simply not true.", "Can we talk about something else?", "<looks unimpressed> Thank you...", "Thanks, but please leave me alone, I'm not interested", "I'm sorry, but I don't have time for this.", "I don't think you are being sincere.")
    elif ct("Bokukko"):
        $rc("Eeh～, I wouldn't say that～♪", "That can't be right, hey～?", "Eh? But that's wrong, right?", "But that's not true at all?", "Eh? What are you talking about?")
    elif ct("Yandere"):
        $rc("I don't understand, what?", "That's not true!", "Don't try too hard, you'll hurt yourself.", "That's definitely not true, so relax, okay?", "Please, don't bother me.")
    else:
        $ rc("Sorry, not interested.", "How many girls have you said that to today?", "Please, stop.", "Does that usually work?", "Don't mock me.", "...I'm sorry, did you say something?", "Can we end this conversation here?", "That doesn't sound sincere at all.", "You don't have to say things you don't mean.", "Too bad. I'm not going to fall for that.", "I've heard it all.", "Huhn, you're far too obvious.", "...What? Don't look at me", "What is it? I don't get what you mean.", "Stop it already...", "Well... guess so. <unimpressed>", "You don't sound as if you mean it.", "......What?", "*sigh*…  I don't really have time for this.", "And so?", "That gets you nowhere!", "I won't be fooled by beautiful words.", "Save your breath!")
    jump girl_interactions
    
label praise_yes: 
    if ct("Impersonal"):
        $rc("There's no need to state the obvious.", "I... see.", "I thank you.")
    elif ct("Shy") and dice(30):
        $rc("Th-thanks...", "You think so? <blush>", "<She quickly looks away, her face red>", "You're ... nice...", "I've never... really been praised much.", "Y-yes... thank you very much... ", "Th... thanks... ", "Ah... ah... really...? I'm so happy...  ", "T-thank you...")
    elif ct("Imouto"):
        $rc("Haha, thank you… Chu ♪", "Huhu ♪ Are you interested in me?", "Fuaaah… Aww, praise me more…", "Really? I'm so happy!", "Ehehe...you praised me♪")
    elif ct("Kuudere"):
        $rc("Heh, good one.", "Of course.", "Um, there's tons of people better than me...", "Is that how you see me...", "Hm? Oh, thanks.")
    elif ct("Dandere"):
        $rc("...Thank you...very much.", "Y-yes... thank you very much...")
    elif ct("Tsundere"):
        $rc("I, I knew that, of course...", "Huh, you finally figured that out?", "It's not like I'm happy or anything. But for now I'll accept your praise.")
    elif ct("Ane"):
        $rc("Well, that was certainly witty.", "O-Oh stop, you're embarrassing me♪", "Thank you, I'm very pleased.", "Huh? I-It's embarrassing, so... please don't look at me so much...  But... hearing you say that I look cute makes me happy, even if it's just flattery.", "Thanks, but it's nothing worth mentioning.", "Thank you. It's very nice of you to say so.", "My, I am happy to hear that.")
    elif ct("Kamidere"):
        $rc("Thanks.", "Be a little serious please. …eh… you are?", "What was that? Are you planning to ask me out?", "You can say that all you want, I'm not going to give you anything～")
    elif ct("Bokukko"):
        $rc("Hey, I really might be cool <giggles>.", "Well, I am cool! Hmph!", "Hehe, did you fall for me?", "Eh? You're interested in me~? That's some good taste, really good!", "Hm-hmm! That's right, respect me lots!", "Well, that's just the way it goes, y'know?", "Thanksiesー♪")
    elif ct("Yandere"):
        $rc("I'm not used to compliments…", "Is that so...?", "…ok.", "<smiles dreamilly> Mhm...", "...I'm happy.", "<gives you a faint smile> Nn...")
    else:
        $ rc("You think so? How nice.", "Thank you. <smiles>", "Hehe, thanks.", "Thanks for the compliment.", "I am, aren't I?", "You mean it?", "Well, I do like being praised.", "<Smiles> Yes, go on ...", "Alright, you've got my attention. <blush>", "..You're too kind.", "Aww♪, so sweet.", "You don't have to say that. <she's blushing and smiling>", "Such flattery won't work on me! <it totally looks like it's working>", "♪Arara, such a smooth talker.", "Gosh, flattery won't get you anything from me, you know?", "Ehehe, thank you very much♪", "Thank you, I'm glad to hear that.","D-Don't say that... I'm starting to blush.", "I sure hope you don't go saying that to every other girl too.", "You are sweet.", "Oh, you're exaggerating.", "Thanks, but it's nothing to boast of.", "Thank you, I'm very pleased.")
    return
###### j2
label interactions_breasts:
    if char.disposition > 400:
        $ gm_dice = 98
        $ gm_disp_mult = 0.2
    elif char.disposition > 550:
        $ gm_dice = 95
        $ gm_disp_mult = 0.4
    elif char.disposition > 450:
        $ gm_dice = 90
        $ gm_disp_mult = 0.7
    elif char.disposition > 400:
        $ gm_dice = 80
        $ gm_disp_mult = 1
    elif char.disposition > 350:
        $ gm_dice = 40
        $ gm_disp_mult = 1
    elif char.disposition > 200:
        $ gm_dice = 35
        $ gm_disp_mult = 1
    elif char.disposition > 100:
        $ gm_dice = 15
        $ gm_disp_mult = 1
    elif char.disposition > 20:
        $ gm_dice = 5
        $ gm_disp_mult = 1
    else:
        $ gm_dice = 1
        $ gm_disp_mult = 1

    if dice(gm_dice):
        $ gm_last_success = True
        $ char.disposition += (randint(10, 30)*(gm_disp_mult))
    else:
        $ gm_last_success = False
        $ char.disposition -= (randint(15, 35)*(gm_disp_mult))

    if gm_last_success:
        if ct("Yandere"):
            $rc("Nfufu, boo-bies♪ boo-bies♪ -bies ♪", "Interested, aren't you? <smiles mischievously>")
        elif ct("Shy") and dice(30):
            $rc("U-Um... Please don't stare at me so much...", "Even though this is embarrassing... I'm glad...", "Don't look at me like that... I-I'm not embarrassed!")
        elif ct("Kamidere"):
            $rc("Do you seriously think so?", "Thanks, but next time keep talk like that for private, ok? ", "So you are that type of person…", "Thanks, I grew them myself.", "Thanks. {p=0.5}Hey, enough. How long will you stare for?!")
        elif ct("Ane"):
            $rc("My, don't stare so hard, okay...?", "If you're gonna look, pay me the viewer's fee!♪", "Thanks, but please don't stare like that, it's embarrassing.", "Do you like my breasts? Glad to hear it...")
        elif ct("Imouto"):
            $rc("Huhu ♪ Lookie, these are my awesome boobs ~ ♪", "Geez, don't loooook～♪")
        elif ct("Kuudere"):
            $rc("G-go ahead, if you're going to look then look!", "D-don't look... You can't!")
        elif ct("Tsundere"):
            $rc("Wh-who said you could look?", "Uuu... Stop staring at me like that...")
        elif ct("Dandere"):
            $rc("Hmmm… Interested?", "You like my body? ...good.")
        elif ct("Bokukko"):
            $rc("Hah hah hah! Go ahead, envy my boobs! Worship them!", "Hmm, already captivated by my exquisite breasts, huh!")
        else:
            $rc("It’s alright to look, but touching is not allowed, oo… fufufu.", "[hero.name], just where are you looking at? It’s alright, look at much as you like.", "Like the view? <pushes her chest up in a pose>", "Do you like my breasts? Glad to hear it...", "You're so perverted. <giggles>", "My body gets you excited, doesn't it?", "Thanks… Hey! Is that why you are interested in me?", "You think so? I'm glad...", "Really? I'm glad to hear that.")

    else:
        if ct("Shy") and dice(30):
            $rc("Ummm... Please don't look....", "D...don't... say that!", "D-don't say such strange things...", "Uu... Don't say such a thing...", "Uwaa! T-this is, that's... I'm, that's… Ugh…")
        elif ct("Impersonal"):
            $rc("I can't really say I'm pleased.", "You are being weird.", "Would you please refrain from commenting on my appearance?")
        elif ct("Kamidere"):
            $rc("It's a good idea to not talk like that, got it?", "Wipe that smug expression from your face.", "Cut that perverted talk.", "*sigh* Just be quiet, okay?")
        elif ct("Tsundere"):
            $rc("Y-you were thinking about something weird, weren't you?", "What are you talking about, geez...?")
        elif ct("Kuudere"):
            $rc("...Perv.", "Shut up. That's disgusting.")
        elif ct("Bokukko"):
            $rc("D-don't stare! It's totally embarrassing...", "Wh-why are you looking at me with such perverted eyes...")    
        elif ct("Ane"):
            $rc("That's no good, you'll dampen the mood like that.")
        elif ct("Dandere"):
            $rc("...Pervert.", "Weirdo...", "...annoying.", "...Shut up.", "Not for you.")
        else:
            $rc("What are you looking at, you idiot.", "I'll shut that annoying mouth of yours, physically.", "That was really kinky.", "What? Stop staring.", "*sigh*… Okay, that's enough…", "That was a bit over the top for a compliment.", "What are you saying, geez!", "Get lost, pervert!", "Hey, look at my eyes not my chest. OK?", "You're annoying...")    
           
    jump girl_interactions
    
