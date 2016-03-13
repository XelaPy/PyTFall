label girl_interactions_greeting:
    if interactions_checks_for_bad_stuff_greetings(char):
        return
    if char.status != "slave":
        if check_lovers(hero, char) and dice(70):
            $ char.override_portrait("portrait", "shy")
            if ct("Half-Sister") and dice(30):
                if ct("Impersonal"):
                    $rc("I love you, even though we're siblings.", "I love you. I think.", "...Love you.")
                elif ct("Tsundere"):
                    $rc("We're drawn to each other even though we're siblings... it's inevitable that we would fall in love with each other.", "You're the best brother ever! Well, if you weren't so perverted you'd be even better... hehe.")
                elif ct("Dandere"):
                    $rc("You are my favorite person.", "Be mine alone, brother.", "Can't siblings love each other..?")
                elif ct("Kuudere"):
                    $rc("Brother, you belong to only me, got it? I won't let anyone else have you.", "Do you hate it that your sister always takes care of you? If you do... well...")
                elif ct("Imouto"):
                    $rc("Every part of my brother belongs to me!", "Brother and I are bound now. Hehe.", "Brother is stylish and kind... Hehe....")
                elif ct("Bokukko"):
                    $rc("All I need is you, bro.", "I won't share my brother with anybody!", "Siblings getting along well... Own family is best, na?", "How should I say this... Brother you're sexy... Hehe!")
                elif ct("Yandere"):
                    $rc("I love you so much brother. You're very special to me.", "If it's for you, brother... I'm ready to do anything!", "*She smiles and stares at you.*")
                elif ct("Ane"):
                    $rc("It's natural for sister to love her brother.", "Sister will always be here to take care of you.")
                else:
                    $rc("I love everything about you... brother.", "Please look at your sister... as a woman.", "We're bound together now, even though we're siblings...", "Is it weird for siblings to stick together all the time?")
        
            elif ct("Shy") and dice(50):
                $rc("I lik-... I love you...!", "U-Um, er, I, um... I-I... I-I love you!", "Um, ah, er... I...l-li... I li-...! I can't do it!", "Um.... I-I love you very much...", "The two of us are going out... Ahhh...")
            elif ct("Nymphomaniac") and dice(65):
                $rc("I'm so lewd, aren't I... I'm thinking of you...doing me...", "Hey, what sorts of things do you think we can do, just the two of us?", "You can have me whenever you want!", "We're lovers, so we should act like lovers, we should get gooey and slap thighs.", "Huhu, I love you ♪ Of course, also in a sexual way.", "Even if we are lovers, I wonder what we should do? Ah, you had dirty thoughts just now, didn't you?", "Um... You don't hate naughty girls... right...?")
            elif ct("Impersonal"):
                $rc("I want to know everything about you. And I want you to know everything about me.", "I'm glad I could meet you.", "As long as we remain lovers, I believe it is essential to have a sensual relationship.", "I'll protect you. You can rely on me.")
            elif ct("Extremely Jealous") and dice(45):
                $rc("I hate it when you just keep ogling other girls.", "I don't want you flirting with other women.", "I'm sorry, but I dislike it when you get too friendly with other women!", "Hey! Don't look at other girls all the time!", "My heart's feeling uneasy and gloomy... I dislike this feeling.", "Erm... I want you to stop looking at other women so much.")
            elif ct("Kuudere"):
                $rc("When y-you're around, I can't think straight...", "I c-can help out too if you need me, you know...", "I love you. ...That's it. Got a problem with that?", "P... Please continue to pursue me. My response will always be positive to you.", "You're very dear to me. I want us to stay together...")
            elif ct("Tsundere"):
                $rc("Wh-what are you planning to have me do...?", "You are NOT to leave my side, okay?", "B-being with you throws me off somehow...", "I deal with your perviness every day, so I deserve some praise!", "Umm... I love you. S-Show a little gratitude for being my choice.", "W-what kind of girls do you like? N-no, pretend I didn't say anything...")
            elif ct("Dandere"):
                $rc("Sweetheart, sweetheart, sweeeetheart...", "Love you... Mm, it's nothing.", "I want to be with you.", "I want to be your special person...", "I-I'm a lonely person... So don't leave me...", "What can I do to make you look at me...?")
            elif ct("Imouto"):
                $rc("Hihi, object of my affection. What is up?", "Hehe, we're lovers.... do whatever you like.", "Ehehe, looooove youuuu♪", "I love you♪ I love you sooo much♪", "Have I become like a proper lover now?")
            elif ct("Ane"):
                $rc("I want to be both your big sister and your wife! ♪", "I love you.  ...No, mere words aren't enough.", "I love you. I don't want to leave your side.", "As I thought, having a caring lover is good ♪", "You'll love me forever, right? ♪", "I'm really happy, you know? To be together like this with you ♪")
            elif ct("Yandere"):
                $rc("Ah... ehhehe... I'm happy...", "We're lovers, aren't we...? Uhehehe...", "I, I'm your girlfriend, right? ...Ehehe", "I think it's really a good thing I've fallen in love with you.", "Ehehe ♪ Nothing, just looking at your face ♪", "Now how do I get you to fall for me even harder...? Ehehe♪", "It would be nice if we could be together forever.", "We're the most compatible couple in the world, aren't we?", "*She smiles and stares at you.*")
            elif ct("Kamidere"):
                $rc("Even though we're lovers, doing nothing but ecchi things is not acceptable!", "Haaa... How'd I fall in love with someone like this...", "Just because we're l-lovers, doesn't mean I will spoil you...", "Well? What does my lover want from me?", "The only thing you'll ever need is me. Oh yes. Just me. Hehe.", "You think it's about time I turned you into my playtoy? ♪")
            elif ct("Bokukko"):
                $rc("Being subtle is such a bother so let me tell you straight... I love you.", "Even though we're dating now, not all that much has changed, huh...", "Say, what do you like about me? ...it's fine, tell me!", "I love you...I super love you...!")
            else:
                $rc("I really like you, you know...", "A-As lovers, let's love each other a lot, okay...?", "We shouldn't flirt too much in front of the others, okay?", "I-I love you... Hehehe...♪", "I love you ♪ I love you so much ♪", "I want you to love me more and more! Prepare yourself for it, okay?", "Ehehe, don't you ever, ever leave me...", "I wish we could be together forever...♪", "What do you think other people think when they see us? ...you think maybe, 'Hey, look at that cute couple'...?")
            $ char.restore_portrait()
        elif char.disposition <= -250:
            $ char.override_portrait("portrait", "angry")
            if ct("Yandere"):
                $rc("I want to hear your screaming voice muffled by tears...", "Stay away...", "What? You want to die?", "You're an eyesore.")
            elif ct("Impersonal"):
                $rc("State your business and leave.", "I have no interest in you.", "...Leave me alone.")
            elif ct("Shy") and dice(50):
                $rc("P-please, stay away!", "...D-don't come close to me.", "...S-S-Stay away!", "W-w-w-what do you want!?")
            elif ct("Dandere"):
                $rc("What is it? I want to get back to what I was doing...", "I personally dislike you.")
            elif ct("Kuudere"):
                $rc("Hmph, I don't even want to hear it.", "Oh? You've got a lot of nerve showing your face around me.", "...I don't think I have reason to talk to you.", "You're so annoying!")
            elif ct("Tsundere"):
                $rc("Leave me alone!", "Go away. ...I said get the hell away from me!", "...Lowlife.", "Listening to you is a waste of my time.")
            elif ct("Ane"):
                $rc("What is it? Please leave me alone.", "I don't really feel like talking to you ", "Could you leave me alone?", "There is not a single shred of merit to your existence.")
            elif ct("Kamidere"):
                $rc("You dirty little...", "It's you again. Don't bother me!", "Could you try to not talk to me, please?  Also, could you not breathe when near me? You're wasting good oxygen.", "Hmph! What an ugly sight.")
            elif ct("Imouto"):
                $rc("Geez, what is it?!", "Loooooooser!", "Jeez! Bug off already!", "You good-for-nothing...")
            elif ct("Bokukko"):
                $rc("Why are you bothering me?", "You just won't shut up, will you...", "Geez, you're pissing me off!")
            else:
                $rc("...Hey! Could you not get any closer to me, please?", "Sigh... What is it?", "Geez, what is it...", "Leave, will you? I don't want to talk to you.", "Why do you keep bothering me?", "Ah... I-I have stuff to do, so....", "U-Um... right now is a bit, err...")
            $ char.restore_portrait()
        elif check_friends(hero, char) or char.disposition >= 500:
            $ char.override_portrait("portrait", "happy")
            if ct("Impersonal"):
                $rc("Talk, I'll listen.", "...Being with you makes me feel extraordinarily comfortable.", "...You really like to talk, huh?", "What is your purpose in getting close to me?", "Being with you... calms me.")
            elif ct("Shy") and dice(50):
                $rc("I-I'm getting a little bit... used to you, [hero.name]...", "Hey, am I... do you... Err... nothing. Never mind.", "Being near you calms me down...", "H-Hi...Is it really ok to talk? I don't want to bother you...", "If I am with you, I...  I-it's nothing...")
            elif ct("Tsundere"):
                $rc("Come, if you have something to say, say it!", "You really must have a lot of free time.", "Your clothes... it's looks untidy. Pull yourself together.", "Don't be so friendly with me...", "Please do not act like we are close to each other.")
            elif ct("Dandere"):
                $rc("You really enjoy talking, don't you.", "Did you need something?", "Maybe... I like that voice.", "Why are you so nice to me...?", "...Do you like talking to me this much?")
            elif ct("Kuudere"):
                $rc("You certainly like to be with me, don't you...", "Seriously... why is it so hard to be serious...?", "I'm listening. What is it?", "Is there something you would like to consult with me? It's alright.")
            elif ct("Ane"):
                $rc("If ever you're in trouble... you can always come to me.", "What's the matter? Need some advice?", "My, please continue.", "I'm here. What can I do for you?", "Ah... I was just thinking, it'd be so nice to talk to you... Ehehe.", "If there's anything I can do, please tell me, okay?", "You can call on me anytime. And I'll do the same with you.", "If something's wrong, you can always talk to me.")
            elif ct("Imouto"):
                $rc("Hn? What's up? You can tell me anything ♪", "For the people I like, I will do my best ♪", "It looks like we could become good friends ♪", "Hi! Tell me, tell me, what'cha doin'?", "Let's have us a chat ♪ Lalala ♪")
            elif ct("Bokukko"):
                $rc("How's it going? Doing alright?", "Oh, what'cha doing?... What'ya wanna do?", "Ohoh, it's you, [hero.name] ♪", "Yo! What'cha doin'?", "Whazzup?", "Hey [hero.name], let's do something!", "Hi buddy!", "Huh? what, [hero.name]?", "Are you that interested in me? hehehe", "Hey, will you talk with me for a bit?", "C'mon, c'mon, put a smile on!", "Um, so hey, you wanna chat?")
            elif ct("Yandere"):
                $rc("Eh, what? Do you want to consult with me?", "Huu... You certainly like to be with me, don't you...", "Hm? Something I can do?")
            elif ct("Kamidere"):
                $rc("Huhu, You seem like you'd be good for some entertainment ♪", "...Do you want to chat with me that badly?", "Ok. I have chosen to give you some of my valuable time today. Don't make me regret that.", "Good timing. Come on, entertain me.", "I have fairly high expectation of you.")
            else:
                $rc("Um, what is it, [hero.name]?", "Hey, how's it going?", "Well, what shall we talk about..?", "What do you want to do?", "Ah, [hero.name]! Let's talk for a while.", "Hi! Another splendid day today!")
            $ char.restore_portrait()
        else:
            $ char.override_portrait("portrait", "indifferent")
            if ct("Impersonal"):
                $rc("Start talking.", "State your business", "You're the kind of person who likes pointless conversations, right? Well, answering your questions makes me similar, I suppose.", "...Please do not get any closer.")
            elif ct("Shy") and dice(50):
                $rc("Y-yes, did you call?", "...Y-you want something from me?", "Um... W-what is it?", "Y-yes? Wh-what's going on?", "Wha... what is it...?", "U-Umm... What is it...?", "Y-yes, what do you need?", "C-can I help you...?", "Ye...yes?", "What... is wrong...?", "Wh-what is it...?")
            elif ct("Kuudere"):
                $rc("Hmph... I wonder if there is any particular purpose to this?", "What business do you have with me?", "Um, was there something you wanted to say?", "Hm? Yes?")
            elif ct("Dandere"):
                $rc("If you have business with me, please make it quick.", "You call?", "...?", "...Want something?", "...Hmm?", "...What is it?", "You have business with me...?")
            elif ct("Tsundere"):
                $rc("Hmph. I've graced you with my presence, so be thankful.", "So, you want something or what?", "Spit it out already.")
            elif ct("Imouto"):
                $rc("Ehehe. What is it? ♪", "Muhuhu ♪ Did you need something?", "Eh? What, what is it?", "Huhu, what is it?", "W-What? Did I do something wrong...?")
            elif ct("Ane"):
                $rc("Well, what shall we talk about..?", "Is there something I can help you with...?", "What business do you have with me?", "May I help you?", "...Yes? Did you need me for something?", "Is there... something I can help you with?")
            elif ct("Kamidere"):
                $rc("Hm? What? It's not like I have too much time to spend. Yes, that's right. I'm busy.", "...Yes? ...Did you call?", "...Do you want something?", "What is it? I'm busy right now.", "If you have business with me, hurry up and say it.")
            elif ct("Bokukko"):
                $rc("Hey-Hey! What do you want?", "Huh? What's up?", "Haa? You got a problem?", "Huh, Is there something you want to know?", "Huh? Do you want something?", "Whazzup?", "Did ya call me?", "Ummm, was there something you wanted to say?")
            elif ct("Yandere"):
                $rc("Yes? If you have no business here, then do please vacate from my sight.", "If you've got something to say, look me in the eyes and say it.", "...I don't recall asking to talk to you, so what is it?", "I don't have any business with you. If you do, make it quick.")
            else:
                $rc("...Is there something you need?", "Is there something you would like to ask?", "Is something the matter?", "What do you need from me?", "What is it? If you need something, then say it.", "What is it?", "Yes, what is it?", "?...Is there something on your mind?", "...Do you need to talk to me?", "Yes? What do you want?", "...? Is there something on my face?", "Do you need something?", "Did you want to say something?", "You have something to tell me?", "Yes, what is it...?")
            $ char.restore_portrait()
    else:
        if check_lovers(hero, char) and dice(70):
            $ char.override_portrait("portrait", "shy")
            if ct("Half-Sister") and dice(35):
                if ct("Impersonal"):
                    $rc("I love you, Master, even though we're siblings.", "I love you, Master. I think.", "...Love you, Master.")
                elif ct("Tsundere"):
                    $rc("We're drawn to each other even though we're siblings... it's inevitable that we would fall in love with each other, Master.", "You're the best Master a sister could wish for! Well, if you weren't so perverted you'd be even better... hehe.")
                elif ct("Dandere"):
                    $rc("You are my favorite person, Master.", "I'm yours alone, brother.", "Can't siblings love each other, Master..?")
                elif ct("Kuudere"):
                    $rc("Brother, I belong to only you, got it? I won't let anyone else have me.", "Do you hate it that your sister always takes care of you, Master? If you do... well...")
                elif ct("Imouto"):
                    $rc("Every part of me belongs to my brother!", "Brother and I are bound now. Hehe.", "Hehe.... Yes, what can I do for you, my dear bro?")
                elif ct("Bokukko"):
                    $rc("All I need is you, bromaster.", "I won't share my brother with anybody!", "Siblings getting along well, Master... Own family is best, na?", "How should I say this... Brother you're sexy... Hehe! Sorry, Master ♪")
                elif ct("Yandere"):
                    $rc("I love you so much, brother. You're the best Master for me.", "If it's for you, brother... I'm ready to do anything!", "*She smiles and stares at you.*")
                elif ct("Ane"):
                    $rc("It's natural for sister to love her brother and Master.", "Sister will always be here to take care of you, Master.")
                else:
                    $rc("I love everything about you... brother.", "We're bound together now, Master, even though we're siblings...", "Is it weird for siblings to stick together all the time, Master?")
        
            elif ct("Shy") and dice(50):
                $rc("I lik-... I love you..., Master!", "U-Um, er, I, um... I-I... I-I love you, Master!", "Um, ah, er... I...l-li... I li-...! I can't do it, Master! I;m so sorry!", "Um.... I-I love you very much, Master...")
            elif ct("Nymphomaniac") and dice(45):
                $rc("I'm so lewd, Master, aren't I... I'm thinking of you...doing me...", "Hey, what sorts of things do you think we can do, Master, just the two of us?", "You can have me whenever you want, Master!", "We're lovers, Master, so we should act like lovers, we should get gooey and slap thighs.", "Hufh, I love you, Master ♪ Of course, also in a sexual way.", "Even if we are lovers, I wonder what we should do? Ah, you had dirty thoughts just now, Master, didn't you?")
            elif ct("Impersonal"):
                $rc("I want to know everything about you, Master. And I want you to know everything about me.", "I'm glad I could meet you, Master.", "As long as we remain lovers, I believe it is essential to have a sensual relationship, Master.", "I'll protect you, Master. You can count on me.")
            elif ct("Extremely Jealous") and dice(35):
                $rc("I don't want you flirting with other women, Master...", "I'm sorry, Master, but I dislike it when you get too friendly with other women!", "Hey! Don't look at other girls all the time, Master!", "My heart's feeling uneasy and gloomy... I dislike this feeling.", "Erm... please stop looking at other women so much, Master.")
            elif ct("Kuudere"):
                $rc("When y-you're around, Master, I can't think straight...", "I c-can help out too if you need me, Master...", "I love you, Master. ...That's it.", "My response will always be positive to you, Master.", "You're very dear to me, Master. I want us to stay together...")
            elif ct("Tsundere"):
                $rc("Wh-what are you planning to have me do, Master...?", "B-being with you throws me off somehow, Master...", "I deal with your perviness every day, Master, so I deserve some praise!", "Umm... I love you, Master. S-Show a little gratitude for being my choice.")
            elif ct("Dandere"):
                $rc("Sweetheart, sweetheart, sweeeetheart...", "Love you, Master... Mm, it's nothing.", "I want to be with you, Master.", "I want to be your special person, Master...", "I-I'm a lonely person, Master... So don't leave me...", "What can I do to make you look at me, Master...?")
            elif ct("Imouto"):
                $rc("Master and me are sweethearts, ehe!", "We'll be together forever, Master!", "Hehe, we're lovers.... do whatever you like, Master.", "Ehehe, looooove youuuu ♪", "I love you, Master♪ I love you sooo much ♪", "Have I become like a proper lover now, Master?")
            elif ct("Ane"):
                $rc("I want to be both your big sister and your wife, Master! ♪", "I love you, Master.  ...No, mere words aren't enough.", "I love you, Master. I don't want to leave your side.", "As I thought, having a caring Master is good ♪", "You'll love me forever, right, Master?♪", "I'm really happy, Master. To be together like this with you ♪")
            elif ct("Yandere"):
                $rc("Ah... ehhehe... I'm happy, Master...", "We're lovers, aren't we, Master...? Uhehehe...", "I, I'm your girlfriend, right, Master? ...Ehehe", "I think it's really a good thing I've fallen in love with you, Master.", "Ehehe ♪ Nothing, just looking at your face, Master ♪", "Now how do I get you to fall for me even harder, Master...? Kidding... Ehehe ♪", "It would be nice if we could be together forever, Master.", "We're the most compatible couple in the world, aren't we, Master?", "*She smiles and stares at you.*")
            elif ct("Kamidere"):
                $rc("Even though we're lovers, doing nothing but ecchi things is not acceptable, Master!", "Haaa... How'd I fall in love with my own master...", "Hehe, what does my dear Master want from me?", "The only thing you'll ever need is me, Master. Oh yes. Just me. Hehe.")
            elif ct("Bokukko"):
                $rc("Being subtle is such a bother so let me tell you straight... I love you, Master.", "Even though we're lovers now, Master, not all that much has changed, huh...", "Say, what do you like about me, Master? ...it's fine, tell me! ♪")
            else:
                $rc("I really like you, Master...", "A-As lovers, let's love each other a lot, okay, Master...?", "We shouldn't flirt to much in front of the others, Master.", "I-I love you, Master... Hehehe...♪", "I love you, Master ♪ I love you so much ♪", "I want you to love me more and more, Master! Prepare yourself for it, okay?", "I love you...I super love you, Master...!", "I wish we could be together forever, Master...♪", "What do you think other people think when they see us, Master? ...you think maybe, 'Hey, look at that cute couple'...?")
            $ char.restore_portrait()
        elif char.disposition <= -200:
            $ char.override_portrait("portrait", "sad")
            if ct("Yandere"):
                $rc("<She looks at you with hostility> What is it, 'Master'?", "..? What is it, Master?")
            elif ct("Impersonal"):
                $rc("State your business, Master.", "...")
            elif ct("Shy") and dice(50):
                $rc("P-please, stay away, Master...", "...D-don't come close to me, Master...", "W-w-w-what do you want, Master!?")
            elif ct("Dandere"):
                $rc("What is it, Master? I want to get back to what I was doing...", "I personally dislike you, Master.", "...")
            elif ct("Kuudere"):
                $rc("Hmph. Yes, Master?", "...I don't think I have reason to talk to you, Master. Give me your orders and leave.")
            elif ct("Tsundere"):
                $rc("L-leave me alone...", "Go away...", "...")
            elif ct("Ane"):
                $rc("What is it? Please leave me alone, Master...", "I don't really feel like talking to you, Master.", "Could you leave me alone, Master?")
            elif ct("Kamidere"):
                $rc("...", "You again... <sigh> Yes, Master?", "'Master', could you try to not talk to me without a good reason, please?", "Hmph!")
            elif ct("Imouto"):
                $rc("Geez, what is it, Master?!", "Jeez... I'm listening, Master.", "You good-for-nothing... Ahem, what is it, Master?")
            elif ct("Bokukko"):
                $rc("Yeah-yeah. I'm here, 'Master'.", "Geez, what is it again, Master?")
            else:
                $rc("Sigh... What is it, Master?", "...Leave me alone, Master. Please.", "...I don't want to talk to you, Master.", "Ah... I-I have stuff to do, so....")
            $ char.restore_portrait()
        elif char.disposition >= 500 or check_friends(hero, char):
            $ char.override_portrait("portrait", "happy")
            if ct("Impersonal"):
                $rc("Yes, Master.", "I'm waiting for your order.", "...You really like to talk to your property, Master.", "Why are you so close to me, Master?", "Being with Master... calms me.")
            elif ct("Shy") and dice(50):
                $rc("M-master?", "Err... y-yes, Master?", "Being near you calms me down, Master...", "I...  I-it's nothing... W-what should I do, Master?")
            elif ct("Tsundere"):
                $rc("Hmph. It's not like enjoy to be your slave or something.", "You really must have a lot of free time, Master... I'm listening.", "Don't be so friendly with me, Master...", "P-please do not act like we are close to each other, Master.")
            elif ct("Dandere"):
                $rc("You really enjoy talking, Master.", "Did you need something, Master?", "I like your voice, Master.", "Why are you so nice to me, Master..?", "...Do you like talking to me this much, Master?")
            elif ct("Kuudere"):
                $rc("You certainly like to be with me, Master...", "Master?", "I'm listening, Master. What is it?")
            elif ct("Ane"):
                $rc("Hm? Something I can do, Master?", "What's the matter, Master? Need something?", "My, please continue, Master.", "I'm here. What can I do for you, Master?", "If there's anything I can do, please tell me, Master!")
            elif ct("Imouto"):
                $rc("Hn? What's up, Master?", "I will do my best, Master ♪", "Yes, Master! I'm here.")
            elif ct("Bokukko"):
                $rc("What'ya wanna do, Master?", "Yo, Master! What'cha doin'?", "Whazzup, Master?", "Huh? What is it, [hero.name]? Er, I mean Master?", "Um, you wanna something, Master?")    
            elif ct("Yandere"):
                $rc("Being around me won't do you any good, Master...", "Call on me anytime, Master.", "Yes, my Master?")                
            elif ct("Kamidere"):
                $rc("You certainly like to be with me, don't you, Master...", "Do you want to chat with me, Master?",  "I have fairly high expectation of you, Master.", "Eh, what? Do you want to consult with me, Master?")
            else:
                $rc("Um, what is it, Master?", "Hey, how's it going, Master?", "What shall we talk about, Master?", "What do you want me to do, Master?")
            $ char.restore_portrait()
        else:
            $ char.override_portrait("portrait", "indifferent")
            if ct("Impersonal"):
                $rc("Awaiting input.", "Yes, Master?", "Master?")
            elif ct("Shy") and dice(30):
                $rc("Y-yes, M-master?", "Y-you want something from me, Master?", "Um... Y-yes, Master?", "C-can I help you, Master?")
            elif ct("Kuudere"):
                $rc("I'm here, Master.", "I'm listening, Master.", "Yes, Master? Was there something you wanted?")
            elif ct("Dandere"):
                $rc("...Master?", "You called, Master?", "...What is it, Master?")
            elif ct("Tsundere"):
                $rc("Hmph. Y-yes, Master.", "Yes, Master. You want something or what?", "Well, I'm here, Master. Spit it out already.")
            elif ct("Imouto"):
                $rc("What is it, Master?", "Yes, Master? Did you need something?", "Nuu, what's up, Master?", "Eh? What, what is it, Master?", "W-What? Did I do something wrong, Master?")
            elif ct("Ane"):
                $rc("Well, what shall we talk about, Master?", "Is there something I can help you with, Master?", "May I help you, Master?", "...Yes, Master? Did you need me for something?", "Is there something I can help you with, Master?")
            elif ct("Kamidere"):
                $rc("...Yes? Did you call, Master?", "...Do you want something, Master?", "If you have an order for me, say it.")
            elif ct("Bokukko"):
                $rc("What do you want, Master?", "Huh? What's up, Master?", "Huh, Is there something you want to know, Master?", "Huh? Do you want something, Master?", "Whazzup, Master?", "Did ya call me, Master?")
            elif ct("Yandere"):
                $rc("Yes, Master?", "...What is it, Master?", "...Spit it out already... Er, yes, Master?")
            else:
                $rc("...Is there something you need, Master?", "Is there something you would like to ask, Master?", "You called, Master?", "Hmm?", "Is something the matter, Master?", "What do you need from me, Master?", "Yes, what is it, Master?", "Do you need something?, Master?")
            $ char.restore_portrait()
    return
    

label girl_trainings_greeting: # should be remade properly once ST will be added
    if char.disposition > 900:
        $rc("Am I doing well Master?", "Master <3")
    
    elif char.disposition < -70:
        $rc("I'll never listen to you.", "Hmph.")
    
    elif char.disposition > 300:
        $rc("What am I learning today?", "M-Mas...")
    
    else:
        g "..."
    return

label girl_meets_greeting:
    if interactions_checks_for_bad_stuff_greetings(char):
        return
    if check_lovers(hero, char) and dice(70):
        $ char.override_portrait("portrait", "shy")
        if ct("Half-Sister") and dice(35):
            if ct("Impersonal"):
                $rc("I love you, even though we're siblings.", "I love you. I think.", "...Love you.")
            elif ct("Tsundere"):
                $rc("We're drawn to each other even though we're siblings... it's inevitable that we would fall in love with each other.", "You're the best brother ever! Well, if you weren't so perverted you'd be even better... hehe.")
            elif ct("Dandere"):
                $rc("Brother, you are my favorite person.", "Be mine alone, brother.", "Can't siblings love each other..?")
            elif ct("Kuudere"):
                $rc("Brother, you belong to only me, got it? I won't let anyone else have you.", "Do you hate it that your sister always takes care of you? If you do... well...")
            elif ct("Imouto"):
                $rc("Every part of my brother belongs to me!", "Brother and I are bound now. Hehe.", "Brother is stylish and kind... Hehe....")
            elif ct("Bokukko"):
                $rc("All I need is you, bro.", "I won't share my brother with anybody!", "Siblings getting along well... Own family is best, na?", "How should I say this... Brother you're sexy... Hehe!")
            elif ct("Yandere"):
                $rc("I love you so much brother. You're very special to me.", "If it's for you, brother... I'm ready to do anything!")
            elif ct("Ane"):
                $rc("It's natural for sister to love her brother.", "Sister will always be here to take care of you.")
            else:
                $rc("I love everything about you... brother.", "Please look at your sister... as a woman.", "We're bound together now, even though we're siblings...", "Is it weird for siblings to stick together all the time?")
        
        elif ct("Shy") and dice(50):
            $rc("I lik-... I love you...!", "U-Um, er, I, um... I-I... I-I love you!", "Um, ah, er... I...l-li... I li-...! I can't do it!", "Um.... I-I love you very much...", "The two of us are going out... Ahhh...")
        elif ct("Nymphomaniac") and dice(65):
            $rc("I'm so lewd, aren't I... I'm thinking of you...doing me...", "Hey, what sorts of things do you think we can do, just the two of us?", "You can have me whenever you want!", "We're lovers, so we should act like lovers, we should get gooey and slap thighs.", "Huhu, I love you ♪ Of course, also in a sexual way.", "Even if we are lovers, I wonder what we should do? Ah, you had dirty thoughts just now, didn't you?", "Um... You don't hate naughty girls... right...?")
        elif ct("Impersonal"):
            $rc("I want to know everything about you. And I want you to know everything about me.", "I'm glad I could meet you.", "As long as we remain lovers, I believe it is essential to have a sensual relationship.", "I'll protect you. You can rely on me.")
        elif ct("Extremely Jealous") and dice(45):
            $rc("I hate it when you just keep ogling other girls.", "I don't want you flirting with other women.", "I'm sorry, but I dislike it when you get too friendly with other women!", "Hey! Don't look at other girls all the time!", "My heart's feeling uneasy and gloomy... I dislike this feeling.", "Erm... I want you to stop looking at other women so much.")
        elif ct("Kuudere"):
            $rc("When y-you're around, I can't think straight...", "I c-can help out too if you need me, you know...", "I love you. ...That's it. Got a problem with that?", "P... Please continue to pursue me. My response will always be positive to you.", "You're very dear to me. I want us to stay together...")
        elif ct("Tsundere"):
            $rc("Wh-what are you planning to have me do...?", "You are NOT to leave my side, okay?", "B-being with you throws me off somehow...", "I deal with your perviness every day, so I deserve some praise!", "Umm... I love you. S-Show a little gratitude for being my choice.", "W-what kind of girls do you like? N-no, pretend I didn't say anything...")
        elif ct("Dandere"):
            $rc("Sweetheart, sweetheart, sweeeetheart...", "Love you... Mm, it's nothing.", "I want to be with you.", "I want to be your special person...", "I-I'm a lonely person... So don't leave me...", "What can I do to make you look at me...?")
        elif ct("Imouto"):
            $rc("Hihi, object of my affection. What is up?", "Hehe, we're lovers.... do whatever you like.", "Ehehe, looooove youuuu♪", "I love you♪ I love you sooo much♪", "Have I become like a proper lover now?")
        elif ct("Ane"):
            $rc("I want to be both your big sister and your wife! ♪", "I love you.  ...No, mere words aren't enough.", "I love you. I don't want to leave your side.", "As I thought, having a caring lover is good ♪", "You'll love me forever, right? ♪", "I'm really happy, you know? To be together like this with you ♪")
        elif ct("Yandere"):
            $rc("Ah... ehhehe... I'm happy...", "We're lovers, aren't we...? Uhehehe...", "I, I'm your girlfriend, right? ...Ehehe", "I think it's really a good thing I've fallen in love with you.", "Ehehe ♪ Nothing, just looking at your face ♪", "Now how do I get you to fall for me even harder...? Ehehe♪", "It would be nice if we could be together forever.", "We're the most compatible couple in the world, aren't we?")
        elif ct("Kamidere"):
            $rc("Even though we're lovers, doing nothing but ecchi things is not acceptable!", "Haaa... How'd I fall in love with someone like this...", "Just because we're l-lovers, doesn't mean I will spoil you...", "Well? What does my lover want from me?", "The only thing you'll ever need is me. Oh yes. Just me. Hehe.", "You think it's about time I turned you into my playtoy? ♪")
        elif ct("Bokukko"):
            $rc("Being subtle is such a bother so let me tell you straight... I love you.", "Even though we're dating now, not all that much has changed, huh...", "Say, what do you like about me? ...it's fine, tell me!", "I love you...I super love you...!")
        else:
            $rc("I really like you, you know...", "A-As lovers, let's love each other a lot, okay...?", "We shouldn't flirt to much in front of the others, okay?", "I-I love you... Hehehe...♪", "I love you♪ I love you so much♪", "I want you to love me more and more! Prepare yourself for it, okay?", "Ehehe, don't you ever, ever leave me...", "I wish we could be together forever...♪", "What do you think other people think when they see us? ...you think maybe, 'Hey, look at that cute couple'...?")
        $ char.restore_portrait()
    elif char.disposition < -300:
        $ char.override_portrait("portrait", "angry")
        if ct("Yandere"):
            $rc("...I don't like you...", "<She looks at you with hostility>", "Ugh, stay away...", "...I resent you.", "...!")
        elif ct("Impersonal"):
            $rc("Leave... You're a bother.", "This is a warning. If you continue to follow me, I cannot guarantee your life.", "I have no interest in you.", "State your business before someone gets hurt.")
        elif ct("Shy") and dice(50):
            $rc("J... just g...go away!", "P-please, stay away!", "...D-don't come close to me.", "S-S-Stay away!", "W-w-w-what do you want!?", "Ah... I'm busy at the moment...", "P-Please stop trailing me...", "You're making me uncomfortable.")
        elif ct("Dandere"):
            $rc("What is it? I want to get back to what I was doing...", "Your existence is not needed.", "I personally dislike you.", "...Why do you exist again?")
        elif ct("Kuudere"):
            $rc("Hmph, I don't even want to hear it.", "You're the worst. Die, trash.", "Oh? You've got a lot of nerve showing your face around me.", "...I don't think I have reason to talk to you...")
        elif ct("Tsundere"):
            $rc("Leave me alone!", "Go away. ...I said get the hell away from me!", "...Lowlife.", "Listening to you is a waste of my time.", "Don't come near me, you trash lower than worms.")
        elif ct("Ane"):
            $rc("What is it? Please leave me alone.", "I don't really feel like talking to you ", "Ummm... You can stop following me, sir.", "Would you please stop following me?", "Er... uh, I have something I need to take care of, so I'll just...", "Could you leave me alone?", "Please excuse me, I'm a little busy.", "There is not a single shred of merit to your existence.", "Ah! I just remembered, I've got things to do, so...")
        elif ct("Kamidere"):
            $rc("From now on you will speak with me only when spoken to! Do you understand that, maggot?", "You dirty little...", "It's you again. Don't bother me!", "<totally suprised> Kyah! Y-you bastard, when did you show up...?!", "Could you try to not talk to me, please?  Also, could you not breathe when near me? You're wasting good oxygen.", "Ahaha ♪ You look entirely unsightly! It fits you well", "That pathetic face of yours isn't fit to show to other people.", "Kukuku... It's unusual running into simpletons like you.", "Hmph! What an ugly sight.", "Hmph, a vulgar person like you doesn't deserve to talk to me!", "Hi monkey! Did someone leave your cage open?", "Some piece of shit just showed up in front of me. What's the meaning of this?")
        elif ct("Imouto"):
            $rc("I hate you!", "Geez, what is it?!", "Geez, what is it?!", "Go away!", "Loooooooser!", "Jeez! Bug off already!", "You good-for-nothing...")
        elif ct("Bokukko"):
            $rc("Uwah, a pest has arrived!", "Why are you bothering me?", "No! Stop following me.", "You just won't shut up, will you...", "Geez, you're pissing me off!", "Oh, what's this? There's a weirdo in front of me. Whoa! It looked at me!")
        else:
            $rc("...Hey! Could you not get any closer to me, please?", "You're bothering me... Would you mind getting the hell out of here?", "Sigh... What is it?", "Stop following me.", "Coming in here... You're a nuisance.", "Ah, please, don't bother me...", "...Leave me alone.", "Geez, what is it...", "Leave, will you? I don't want to talk to you.", "You're an eyesore.", "You're so annoying!", "Why do you keep bothering me?", "Ah... I-I have stuff to do, so....", "U-Um... right now is a bit, err...")
        $ char.restore_portrait()
    elif char.disposition > 500 or check_friends(hero, char):
        $ char.override_portrait("portrait", "happy")
        if ct("Shy") and dice(50):
            $rc("Even being... with me... is ok...?", "I-I'm getting a little bit... used to you, [hero.name]...", "Hey, am I... do you... Err... nothing. Never mind.", "Being near you calms me down...", "H...H-Hello!", "It's you...H-Hi! ...sorry...", "It's nice... to see you again.", "H-Hi...Is it really ok to talk? I don't want to bother you...", "Hello. It's nice of you... umm...to remember me...", "If I am with you, I...  I-it's nothing...")
        elif ct("Impersonal"):
            $rc("You don't need to worry about me.", "Talk, I'll listen.", "...Being with you makes me feel extraordinarily comfortable.", "...You really like to talk, huh?", "What is your purpose in getting close to me?", "Ah, it's you...", "Being with you... calms me...", "...I will escort you.", "...[hero.name]? ...good.")
        elif ct("Tsundere"):
            $rc("...Hah! I-I wasn't completely fascinated by you or anything!", "...Do you think I'm a tsundere too?", "Looks like you're... somewhat capable, aren't you?", "Come, if you have something to say, say it!", "You again? You really must have a lot of free time.", "Your clothes... it's looks untidy. Pull yourself together.", "Don't be so friendly with me...", "Please do not act like we are close to each other. It would be terrible if someone got the wrong idea.")
        elif ct("Dandere"):
            $rc("You really enjoy talking, don't you.", "Did you need something?", "In front of you I feel strange...", "Maybe... I like that voice.", "Why are you so nice to me...?", "Sometimes I find myself thinking of you...", "...Do you like talking to me this much?")
        elif ct("Kuudere"):
            $rc("It's okay, come closer.", "Stick around. Alright?", "You certainly like to be with me, don't you...", "Hmph, you are an unusual fellow...", "Seriously... why is it so hard to be serious...?", "Haa... When you're around, I feel strange...")
        elif ct("Ane"):
            $rc("Pleased to meet you again, [hero.name].", "If ever you're in trouble... you can always come to me.", "Hm? Something I can do?", "What's the matter? Need some advice?", "It's you... My, please continue.", "I'm here. What can I do for you?", "Good day Sir. Nice to see you again.", "Oh, what a coincidence. I'm pleased to meet you again.", "Ah... I was just thinking, it'd be so nice to see you... Ehehe.", "If there's anything I can do, please tell me, okay?", "You can call on me anytime. And I'll do the same with you.", "If something's wrong, you can always talk to me.")
        elif ct("Imouto"):
            $rc("Hi theeeere! Come on, cheer up!", "Hn? What's up? You can tell me anything ♪", "For the people I like, I will do my best ♪", "Hi!", "Huhu ♪ Hmm, it's nothing... Ehehe.. ♪", "It looks like we could become good friends ♪", "Hi! Tell me, tell me, what'cha doin'?", "Let's have us a chat! Lalala ♪", "Mhmhm♪　Go ahead, come a little closer ♪")
        elif ct("Bokukko"):
            $rc("Oh! Isn't it [hero.name]! G'day!", "How's it going? Doing alright?", "Oh, what'cha doing?... What'ya wanna do?", "Come on, come on, cheer up, let's go!", "Ohoh, it's you ♪", "Yo [hero.name]! What'cha doin'?", "Okay, what shall we do today?", "Hey, it's you! Whazzup?", "Hey! It's you, come come, let's talk!", "Hey [hero.name], I'm free, so let's do something!", "Hey [hero.name], isn't there anything fun to do?", "Hi buddy!", "Huh? what, [hero.name]?", "Are you that interested in me? hehehe", "Hey, will you talk with me for a bit?", "C'mon, c'mon, put a smile on!", "Um so hey, you wanna chat?", "Ah, whatcha up to?")             
        elif ct("Kamidere"):
            $rc("Huhu, You seem like you'd be good for some entertainment ♪", "Huu... You certainly like to be with me, don't you...", "Hu Hu ♪ Do you want to chat with me that badly?", "You've missed me, right? I know you did. Good boy ♪", "You came to visit me again? I know you couldn't help it, I'm just irresistible ♪", "You came just to see me? That's a point for you, but you have to try a lot harder to impress me, fufu ♪", "Ok. I have chosen to give you some of my valuable time today. Don't make me regret that.", "Good timing. Come on, entertain me.", "I have fairly high expectation of you.", "Eh, what? Do you want to consult with me?", "Is there something you would like to consult with me? It's alright.")
        elif ct("Yandere"):
            $rc("Hey! Did you think that I might have forgotten about you?!", "Hi [hero.name]! Let's walk together for a while.", "I have the feeling I could get along with you.", "Being around me won't do you any good, you know?")
        else:
            $rc("[hero.name]...? Um, what is it?", "Ah, Hello ♪", "Hello, nice to see you again.", "Hey, how's it going?", "Hi! Nice to see you again!", "Hello. What are you doing?", "Well, what shall we talk about..?", "Hey, I just wanted to see you ♪", "So? You enjoying life here?", "Oh, hello!", "Ah, it's you. Hi there!", "Oh Hi, it's you again...", "Hi! What a coincidence...", "Hi [hero.name]. How's it going?", "Hello [hero.name].", "Hi! What do you want to do?",  "Ah! Hello♪", "Hi there [hero.name]! So what have you been up to?", "Hi! Another splendid day today!")
        $ char.restore_portrait()
    else:
        $ char.override_portrait("portrait", "indifferent")
        if ct("Impersonal"):
            $rc("Start talking.", "State your business", "You're the kind of person who likes pointless conversations, right? Well, answering your questions makes me similar, I suppose.", "...Please do not get any closer.")
        elif ct("Shy") and dice(50):
            $rc("Yes, did you call?", "...Y-you want something from me?", "Um... W-what is it?", "Y-yes? Wh-what's going on?", "Wha... what is it...?", "U-Umm... What is it...?", "Y-yes, what do you need?", "C-can I help you...?", "Ye...yes?", "What... is wrong...?", "Wh-what is it...?", "Aaah! U-um...wh-what...?")
        elif ct("Kuudere"):
            $rc("Hmph... I wonder if there is any particular purpose to this?", "What business do you have with me?", "Um, was there something you wanted to say?")
        elif ct("Dandere"):
            $rc("If you have business with me, please make it quick.", "Ah! Don't sneak up behind me.", "You call?", "...?", "...Want something?", "...Suspicious person.", "Hmm?", "...", "...What is it?")
        elif ct("Tsundere"):
            $rc("!? H-hey, at least let me know you're there or something...", "Hmph. I've graced you with my presence, so be thankful.", "So, you want something or what?", "Spit it out already.")
        elif ct("Imouto"):
            $rc("Ehehe. What is it? ♪", "Muhuhu♪ Did you need something?", "Nuu, what's up?", "Eh? What, what is it?", "Huhu, what is it?", "W-What? Did I do something wrong...?", "Aaah! U-um...wh-what...?", "Waah!?　D-don't startle me like that, jeez...", "Aah!　D-don't scare me like that...")
        elif ct("Ane"):
            $rc("Oh my, you startled me... Hmhm.", "Well, what shall we talk about..?", "Is there something I can help you with...?" , "What business do you have with me?", "May I help you?", "...Yes? Did you need me for something?", "Is there... something I can help you with?")
        elif ct("Kamidere"):
            $rc("Hm? What? It's not like I have too much time to spend. Yes, that's right. I'm busy.", "Are you a stalker or something?", "...Yes? ...Did you call?", "...Do you want something?", "What is it? I'm busy right now.", "If you have business with me, hurry up and say it.", "Did...did you just call me?")
        elif ct("Bokukko"):
            $rc("Huh? You called?", "Hey-Hey! What do you want?", "Huh? What's up?", "Haa? You got a problem?", "What's up?", "Huh, Is there something you want to know?", "Huh? Do you want something?", "Whazzup?", "Did ya call me?", "Ummm, was there something you wanted to say?")
        elif ct("Yandere"):
            $rc("Yes? If you have no business here, then do please vacate from my sight.", "If you've got something to say, look me in the eyes and say it.", "...I don't recall asking to talk to you, so what is it?", "You're in my way. Get lost.", "I don't have any business with you.", "...Spit it out already.")
        else:
            $rc("...Is there something you need?", "Ohhh... What seems to be the matter...? You over there. Is there something you would like to ask?", "You called?", "Hmm?", "...I don't like being stared at. Go away.", "...What? You're bothering me.", "Is something the matter?", "? What do you need from me?", "What is it, I'm busy here...", "What is it? If you need something, then say it.", "You have business with me...?", "What is it?", "Yes, what is it?", "?...Is there something on your mind?", "...Do you need to talk to me?", "Yes? What do you want?", "...? Is there something on my face?", "Do you need something?", "Did you want to say something?", "You have something to tell me?", "Hm? Yes?", "Yes, what is it...?", "Hm? What's up?", "Ah, sorry. Did you call me?")
        $ char.restore_portrait()
    return
    
label interactions_girl_never_come: 
    $ char.override_portrait("portrait", "sad")
    if ct("Impersonal"):
        $rc("Doesn't it count as sex only if we've actually both came?", "I'm not sure how to feel about this kind of sex.", "I guess you need to get used to this. Can I count on you to practice with me?")
    elif ct("Shy") and dice(60):
        $rc("But I'm still not... You're so cruel...", "But I'm... Not yet...", "Is... is it already over? No, that's fine...")
    elif ct("Tsundere"):
        $rc("Uuh... But, but...! I just got so horny!", "Gosh, how could you forget! About what...? About me c-cumming!!", "Hey, can't you even tell whether or not your partner came?")
    elif ct("Dandere"):
        $rc("...What? Done already?", "Did you...do that...on purpose?", "I can't say I really approve of this sort of one-sided sex...", "Hmph, so selfish...")
    elif ct("Kuudere"):
        $rc("I'll forgive you this time, but...be ready for the next.", "Tch, and it was just getting good.", "I know you want to feel good, but you could throw me a bone... It's nothing...", "Really... isn't that kinda unfair?")
    elif ct("Imouto"):
        $rc("Mrrr♪, I still haven't cum yet!", "Didn't you forgot...the important stuff? I mean... me...", "Huh? Are we already done? But...", "That was fast... whatever it was, it was way too quick!")
    elif ct("Ane"):
        $rc("Hey, you do know what an orgasm is, yes? ...Then you understand, right?", "Come now, there's still something you haven't done, right?", "...What's wrong? You didn't do much...", "I haven't been satisfied yet...", "Don't worry, it'll get better... Next time, let's try to make it so both of us enjoy it.")
    elif ct("Bokukko"):
        $rc("Stopping after you've only satisfied yourself? You're the lowest.", "Hold on, aren't you forgetting something? ...Yeah, that! You know, that...yeah... N-not that!", "Wha-... but we barely did anything!")
    elif ct("Yandere"):
        $rc("What's the meaning of this? I wanted to do it, you know...", "No no no, there's no way we can just end it like that...", "Come on, now, you can do better than that...")
    elif ct("Kamidere"):
        $rc("No self-centred sex allowed, you can't skip the important parts!", "I am not pleased. Please figure out the reason on your own.", "I'm still far from being satisfied though...", "You're still a long way from satisfying me... Work on it for next time.")
    else:
        $rc("Hey! I-I didn't cum at all!", "I haven't had anywhere near enough yet, you know?", "Th-this happens sometimes, right...? Still...", "Eh, but I only got a little! Geez...", "Wait, I haven't even cum yet!")
    $ char.restore_portrait()
    return
    
label interactions_girl_virgin_line:  # character agrees to get rid of virgin trait
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $rc("I'm not going to stay a virgin all my life. Please make me an ex-virgin.", "W-would you make me... a woman?", "You can confirm for yourself that I'm a virgin.", "I understand... When you put it in, please tear my hymen apart slowly, okay?", "This is my first time, so I won't be any good... Please help and guide me.", "You're going to break my hymen... Okay.")
    elif ct("Shy") and dice(60):
        $rc("Um, I'm a virgin! ...Please, umm, take my first time...", "I, um... I've never did it before... So...", "I've never done this before, but... If you'll be gentle, then...", "Eh? H-how would we do that... Eh!? Th-that goes... in here...? Y-yeah! ...Let's do it...", "Pl-please... Be my... first time...", "I'm, uh... still... a virgin, okay? So... you know...")
    elif ct("Nymphomaniac") and dice(40):
        $rc("...T-this is...unexpectedly embarrassing... It is my first time and all.", "Y-you'll have to teach me a few things...")
    elif ct("Tsundere"):
        $rc("F-fine then, let's get to it! I-it's not like this is my first time, okay!?", "H-hmph! Sex is nothing to me! Fine, let's do this!", "I-if you say you want it, I can give you my virginity... If you'd like...?", "O-okay... But! This is my first time, so... be gentle... Y-you got that!?", "I-if you really, really want my ch-chastity... Then I'll give it to you...")
    elif ct("Dandere"):
        $rc("...I don't mind if it's you. Teach me to fuck.", "...If you're alright with me being inexperienced, then let's do it.", "You'll be my first partner.", "Very well. I will give you my chastity.", "It's my.. first time. I'm giving it to you.", "I'm inexperienced, but I hope that you enjoy my performance.")
    elif ct("Kuudere"):
        $rc("I've... never done it before... Okay, then let's do it.", "Take my virginity. It's n-not really a big deal, you don't have to overthink it.", "I-it's my first time... So I want you to do it gently.", "Yeah, my cherry is still right where nature put it... Please pop it gently, okay?", "I feel like I should warn you that... That I'm a v-virgin... So... you know...")
    elif ct("Imouto"):
        $rc("Alright, you're going to be my first.", "I-if you're okay with me... I don't know if I'll be very good at it, ahaha...", "U-Um, well... If you're gentle...♪", "Umm... I-I don't know how it's done! ...Please, take the lead...")
    elif ct("Ane"):
        $rc("Hmhm, I'm still a virgin. Please be gentle with me... I'll be angry if you're not, ok?", "Hmhm, it looks like you'll become my first...", "I'm a virgin but... I want you to make me a woman.", "Hey... This is my first time... Could I entrust that to you?", "I've never done it before, so don't complain, okay?")
    elif ct("Bokukko"):
        $rc("Virgins are a real pain. ...You okay with that?", "Yeah, okay, take my virginity.", "You know, mine... Mine's new, unbroken seal and everything... no one's been there before...", "A-are you okay with me even if I'm still a virgin? ...V-very well, challenge accepted!")
    elif ct("Yandere"):
        $rc("Yes... My chastity... is yours...", "I've heard how it works, but... I don't have any experience, okay?", "You can't become a 'woman' without having sex right? Well, I want to be a 'woman'...", "I know the idea of it... But I never actually did it before. Is that still okay...?")
    elif ct("Kamidere"):
        $rc("My first time... Will be tested on your body.", "Hmph, you'll do as my first partner.", "I don't really like pain... I'm okay. let's do it.", "Hurry up and do it, or I'll give my virginity away to whoever.", "Right now, an unplucked fruit is standing before you. Hungry?")
    else:
        $rc("I've never done it before, but... I think I could do it with you.", "It's my first, so... Be gentle, alright?", "Hmm... well, it should be fine if it's with you you, first time or not.", "I-it's okay with you if I make you my first partner... Right...?") 
    $ char.restore_portrait()
    return
    
label interactions_guy_never_came: # due to low sex skill character was unable to make MC come
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $rc("...Was my technique that bad?", "I'm sorry, I'm just so incompetent...")
    elif ct("Shy") and dice(60):
        $rc("I'm sorry... I wasn't very good...", "Sorry... Because of my weakness...", "I'm very sorry... Y-yes, I made sure to practice...")
    elif ct("Tsundere"):
        $rc("S-sorry... I'll try harder next time, okay...?", "I-if I'm bad at this, j-just say so already...", "Wh-what? Are you trying to say I'm bad at this? ...Kuh, just you wait.")
    elif ct("Dandere"):
        $rc("This was not something I had any control over... Sorry.", "Please forgive me, this is all due to my insufficient knowledge.")
    elif ct("Kuudere"):
        $rc( "I can't even satisfy one man...What am I missing?", "Forgive me for having disappointed you... How can I fix things?")
    elif ct("Imouto"):
        $rc("Was it not good for you? ...Sorry", "...My bad. I'm sorry, ok?", "Ah, um... Next time, I'll make you feel good...")
    elif ct("Ane"):
        $rc("I was unable to satisfy you... My apologies...", "I'm so sorry...I couldn't satisfy you...", "I'm bad at this, so...maybe you can teach me how?")
    elif ct("Bokukko"):
        $rc("Jeez, how come you never came!", "Is it cause I'm so bad? ...I'm sorry, okay?")
    elif ct("Yandere"):
        $rc("I'm sorry... I'll do something about it next time, so forgive me, okay?", "Mmm, I need to learn more about your body, huh...")
    elif ct("Kamidere"):
        $rc( "Hmph, if you didn't want it you could've refused, you know?", "It's your own fault for masturbating so much you can't finish.", "W-what's with this face that says 'She did her best...'?!")
    else:
        $rc("Um. I'm sorry! I'll study up for next time.", "Sorry... I'll do some more studying, so...") 
    $ char.restore_portrait()
    return
    
label interactions_guy_cum_alot:
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $rc("Is it normal for someone to be able to cum so much? Are you not a human?", "As a side note, creampies are okay.", "Nn... Your load exceeded my maximum capacity...", "I have all your weak spots memorized.", "I want to shower... Together, if possible.")
    elif ct("Shy") and dice(60):
        $rc("Y-You came so much... You were really saving it up...!", "Snf snf... It smells...", "I-I... what an embarrassing thing to do...", "I-I can't believe I... did that... Aaahhh...", "I made you feel really good, huh... I-I'm glad...")
    elif ct("Nymphomaniac") and dice(40):
        $rc("Hehehe, thanks for the meal ♪", "The flavor of semen differs depending on the food you eat and how you're feeling...", "What a perverted scent... ehehe.", "Huhuh... look at me, I'm a dirty girl covered in your spunk.")
    elif ct("Tsundere"):
        $rc("Ah jeez...It's cause you came so much.", "T-That's embarrassing! Geez...", "I'm happy that you came so many times because of me, but... Didn't you come too much?", "Yes, yes, you did well by cumming so much... Seriously...", "And? I'm great, right? ...Tell me that I am G-R-E-A-T!")
    elif ct("Dandere"):
        $rc("Your semen's still so warm...", "I could get used to this scent...", "You came quite a bit...", "Don't worry, it's not unpleasant. Don't hold back on me next time.", "I became all slimy...", "How was it? My technique is something else, don't you think?", "I love it... when you cum for me.")
    elif ct("Kuudere"):
        $rc("Um, so, are you gonna be okay, cumming that much?", "...Where did this much even come from?", "I know it feels good, but...you came too much.", "My god, are you bottomless...?", "So, what did you think...? I won't let you say that it didn't feel great!")
    elif ct("Imouto"):
        $rc("Hey, lookie lookie! Look how much you came ♪", "Hehehe... It feels kinda warm...", "Nnh, hey look ♪ It's all that semen you shot out ♪", "Hey, can't you change the taste? Something that goes down a little easier would be nice.", "You've marked me with your cum, ehehe", "Waa, It's sticky... Did you cum a lot?", "I-I don't have a runny nose! This is semen!")
    elif ct("Ane"):
        $rc("Fuaha... You came so much...♪", "Hehehe, your sweet spots were so easy to find ♪", "There's so much of your cum... Hmhm, want me to drink it?", "Mhmhm, you seem to be quite satisfied.", "That was enjoyable in its own way, thank you.", "Are you okay letting that much out... not dehydrated?")
    elif ct("Bokukko"):
        $rc("You really went all out... Is that how good it felt?", "More protein than I should be having... Oh well.", "...You look pretty strung out, hey? Eat up and get a good night's sleep, mkay?", "Ugh, my face is all sticky... But this is how I'm supposed to take it, right?")
    elif ct("Yandere"):
        $rc( "Hehe... What a nice smell... I want to smell it forever...", "I know every inch of your body better than anyone.", "Hmhm, the face you make when you cum is adorable.", "It felt good, right? That's great...", "Uhuhu, it's good to know that I could be of use...")
    elif ct("Kamidere"):
        $rc("Ew, I'm all sticky... Does the smell even come off...?", "Ahh, you're so naughty to cum this much...", "Nha... H-haven't you got anything to wipe with?", "I need to take a shower...", "Geez, to cum just from a little teasing... That's pathetic.", "Heh, should I tie a ribbon on it so you don't cum so fast?", "You REALLY let loose a lot of this stuff, huh...")
    else:
        $rc("Wow, look, look! Look at all of it... How did you even cum this much ♪...", "You came so much...", "Are you okay? Want some water? Are you going to be okay without rehydrating yourself?", "If it felt good for you, then that makes me feel good, too.") 
    $ char.restore_portrait()
    return

label interactions_after_good_sex: # after very good sex
    $ char.override_portrait("portrait", "happy")
    if ct("Impersonal"):
        $rc("Thanks for your hard work... Let's have fun the next time too.", "When our membranes make direct contact, it feels like we are melting into each other.", "I thought you would break me...", "I came too much...", "I guess it's possible for something to feel too good...")
    elif ct("Shy") and dice(30):
        $rc("Ah, please, don't make me feel so much pleasure... You'll turn me into a bad girl...", "No, please... I can't look you in the eye right now...", "Uuugh... I did such an embarrassing thing... Pl-please forget about it...", "Auh... I'm sorry for being so perverted...")
    elif ct("Nymphomaniac") and dice(40):
        $rc("Hafu... It was totally worth it practising with all those bananas...♪", "That was incredible... I thought I was gonna lose myself there.", "Ah♪, I did it again today... Alright, starting tomorrow I'll control myself!")
    elif ct("Tsundere"):
        $rc("I-I was... C-cute? ...S-Shut up! One more word and I'll kill you!", "You made me cum so many times, it's kind of frustrating...", "Hu-hmph! Don't get a big head just 'cause you did it right once!", "H-hmph! Just because you're a little good doesn't make you the king of the world!", "I-it's not like you've got good technique or anything! Don't get so full of yourself!")
    elif ct("Dandere"):
        $rc("If you do it like that, anyone would go crazy...", "Mn... You did good...", "...Looks like we're a good match.", "We're quite compatible, you and I." "I came way too many times... Haa...", "D-do I also have such a shameful erotic face?", "Whew... I came so much... I surprised myself...")
    elif ct("Kuudere"):
        $rc("You're really good... I came right away...", "...Please don't look at me. At least for now.", "Yeah, I knew you were the type who gets things done.", "Wh-what? Y-you know just where I like it...?", "Uuu... It did feel amazing... but... I thought you were gonna rip me apart...")
    elif ct("Imouto"):
        $rc("You got me off just like that... You're like some kind of pro!", "Ah... I came right away... You're so good at this...", "It was surprisingly cute... I-I don't m-mean it was small or anything!", "I felt so good... Huhu, you are pretty good at this.", "Haah, I came so fast... What's wrong with me?")
    elif ct("Ane"):
        $rc("Exhausted? ...But you'll be wanting to do it again soon, right?　Hmhm♪", "You're so good. ...Hmhm.", "Oh my, you've already found all my weak spots.", "Haah... If you make me feel pleasure this intense... I won't be able to live without you♪", "Hauh... ok, that really was going too far... But it did feel really good...", "My goodness, you've really gotten quite skilled at this♪")
    elif ct("Bokukko"):
        $rc("Hehe, well? What, you totally looked like you enjoyed that", "Haah♪... Man, sex feels sooo good♪", "Fuwa... I turned into such a pervert... that surprised me...", "Ehehe, thanks for timing it just right...♪")
    elif ct("Yandere"):
        $rc("Nh... I came so much... Hehehe♪" , "That felt incredible... Fufu, thank you!♪", "This kind of sex really leaves my heart satisfied...", "Ehehe... We had sex♪ Sex, sex, sex sex sex sexsexsexsehehe♪ Ahahahaha ♪", "I've got so much love, I think I may go crazy...", "To be violently messed up like this, isn't so bad sometimes... huhu ♪")
    elif ct("Kamidere"):
        $rc("There there, that felt pretty damn good, hey?", "Aau... I thought I was going to break...",  "Ohh, who's a good boy, yes you are.", "Mmh... I could become addicted to this pleasure.", "Ah... If it's this good, I guess it's ok to do it everyday.", "It just so happened that I got more sensitive all of a sudden, alright?")
    else:
        $rc("Ahh... My hips are all worn out... Ahaha", "It kinda feels like we're one body one mind now ♪", "Haah... Well done... Was it good for you...?", "Haah... Your sexual technique is simply admirable...", "Sorry, it felt so good that I didn't want to stop...", "Haa... It looks like the two of us are pretty compatible...", "Ah, I can't even move... That felt too amazing...") 
    $ char.restore_portrait()
    return
    
label interactions_after_normal_sex: # after not good and not bad sex, not via raping
    $ char.override_portrait("portrait", "happy")
    if ct("Impersonal"):
        $rc("I can still feel you between my legs.", "So how was it, sex with me? Are you satisfied?", "Yeah... felt good.", "Haa... Satisfying...", "Please entertain me again sometime.")
    elif ct("Shy") and dice(30):
        $rc("I... I wonder how good I was... I don't want you to hate me...", "I-I need to reflect... On the things that I've done...", "Aah... I want it like that, again... Maybe I'm a really dirty girl..?", "I'm very happy... Because... you know... huhuh...")
    elif ct("Nymphomaniac") and dice(40):
        $rc("Hehe... It looks like we were naughty, huh...", "Ehehe... I feel like doing it again...", "Um, how about we do it again? Maybe even two or three more times, if you want...")
    elif ct("Tsundere"):
        $rc("Well, that didn't feel too bad.", "Geez, what are you grinning for!? Yes, yes, it felt good, I get it!", "D-did I... make a funny face? Geez, I'm so embarrassed...", "W-what... Of course it felt good! You got a problem with that!?", "Geez, it was standing up so stiffly, I just couldn't stop myself!")
    elif ct("Dandere"):
        $rc("I want to do it again sometime...", "Did I... do well? I see. Thank you so much.", "It still feels like you are inside me.", "*huff* I can't go on... anymore... *puff*", "That felt really good... I'd be happy to do it again with you sometime.")
    elif ct("Kuudere"):
        $rc("Mmmfhh... I really am exhausted... You should take it easy too.", "That was awesome... Huhuh, let's do it again real soon.", "Geez, me doing such a thing... But it does feel really good...", "Well then... Let's do this again sometime, alright?")
    elif ct("Imouto"):
        $rc("Hey, hey, was I sexy or what?", "Ehehe... I'm good in bed, right?", "Hehe, it looks like we've been naughty...", "Haaaa... Sex really is wonderful...", "Huhuh, the sex felt really nice. Thank you ♪", "Hey, hey, what'd you think? It felt good, right? Tell me straight ♪", "Making love is a wonderful thing, hmhm♪")
    elif ct("Ane"):
        $rc("What did you think? My insides feel wonderful, don't they?", "*sigh*... I'm exhausted... Hehe ♪", "I didn't expect it to be that good... Good job, hehe.", "Huhu... please keep desiring me as many times as you want.", "You did it very well... Uhuhu, it felt great.", "I'm ready for you any time, okay? ♪")
    elif ct("Bokukko"):
        $rc("Hum, thank you for letting me cum...", "Muhuhu... your orgasm face is nice ♪", "Aha, still erect? ...But, sorry! You'll have to wait.", "Geez... You made me feel so too good...", "Weeell, I s'pose you're pretty good. Not as good as me, though.")
    elif ct("Yandere"):
        $rc("How was it? Are you refreshed? ...Fufu, you should thank me.", "That wasn't bad, I guess... I'm sure you'll do even better next time.", "How does my face look when I cum? ...It doesn't go weird, does it?", "Ahaha♪　It's so floppy ♪ And warm ♪")
    elif ct("Kamidere"):
        $rc("Aaaah, that was great... It was really awesome.", "Kuuh... Y-you're fucking like a cat in heat! There's no way I can continue after this...", "It felt really good. Well done.", "It wasn't bad, I guess... Yeah... I won't turn you down if you ask again.", "I expect next time will be equally enjoyable.")
    else:
        $rc("That felt so good... Let's do it again someday.", "Hey, it felt good, right?", "Well, I'm looking forward to the next time.", "We really, really have to do this again ♪", "Ehehe, I'll let you borrow me again sometime.") 
    $ char.restore_portrait()
    return
    
label interactions_after_virginity_was_taken: # right after removing virgin trait not via raping
    $ char.override_portrait("portrait", "happy")
    if ct("Impersonal"):
        $rc("With this, next time I'll be able to feel good, right?", "Hmm, It did hurt, but... I'm happy.", "It was so big that I thought it would hurt a lot... It is all because of your gentleness.	Thank you very much.", "Hm... So this makes me an ex-virgin, it seems.")
    elif ct("Shy") and dice(30):
        $rc("Uh, i-it's ok... I can endure it...", "Kuh... I'm okay... But... I didn't think it would hurt so much...", "I-It's alright. It did hurt a little, but... I'm really happy ♪", "I-It's okay... You were very gentle...")
    elif ct("Tsundere"):
        $rc("Uuh... That really hurt... Of-of course you could have helped it!", "Kuh... I had to go through this one day anyway so it's fine!", "Kuh... This pain makes the world so dazzling...", "What's with this...? Why does it hurt so much? Geez...")
    elif ct("Dandere"):
        $rc("I can still feel the pain of it going in... But it only hurt at first, you know? I wonder how it'll feel next time.", "This pain... it's carved into my body and my heart... I'll never forget this.", "...No, I'm okay. It just... hurt a little more than I expected.", "This pain...I am sure it will become an unforgettable memory...")
    elif ct("Kuudere"):
        $rc("Kuh... It hurts and it's not easy to do... Will it really begin to feel good...?", "Tch!... I-it's not... okay... It hurt so much...", "Kuh... This much pain is nothing...", "Ku... So this is the pain of deflowering... I'm jealous that men don't need to suffer the first time...")
    elif ct("Imouto"):
        $rc("Uuh... It was scary, and painful... Sniff... Be a little more gentle next time...", "Aha, now I've become an adult... after that... uhuhu...", "Uuu, it still stings... It's gonna be okay, right...?", "Uu... Should I smear some medicine on it...?", "Fufu, I gave you my first time♪")
    elif ct("Ane"):
        $rc("As I expected, the first time hurt...", "How was my first? Did it make you happy...?", "Ouch... er, n-no, I'm fine... This is another good memory.", "Kuh, I'll need to practice to get used to this, I think... Of course you'll help me, don't you?")
    elif ct("Bokukko"):
        $rc("Does it hurt this bad for everyone? And they still do it?", "Damn! That really freakin' hurt! Buy me something as an apology, kay?", "The time has come! Virginity lost!", "I can still feel you inside me... So this is sex huh...?")
    elif ct("Yandere"):
        $rc("Hmm... Next time it'll feel good right? Hehe, I can't wait.", "Ahhh, it hurts... I-it can't be helped...", "Ugh... That really hurt... I'm glad I will never have to do that again...", "Phew... It really went in there, huh... It did kind of hurt, though...")
    elif ct("Kamidere"):
        $rc("Ugh. Can this really begin to feel good...?", "Haa... Geez, It hurt and it's disgusting, that's the worst...", "Hng... It hurt and I'm tired... Do people really enjoy this sorta thing...?", "Tch... Huhu, I guess, I won't be called a virgin anymore...", "Nnn.... It's my first time, of course it hurts.")
    else:
        $rc( "Khh... That, that hurt a little bit...", "Ouch... I need to get more practice taking it in...", "Aauu... It hurt even more than I expected...", "I'm fine... This pain is something I have to overcome, so...") 
    $ char.restore_portrait()
    return
    
label interactions_lesbian_refuse_because_of_gender: # for lesbians, when they refuse lover or sex propositions
        $ char.override_portrait("portrait", "indifferent")
        if ct("Impersonal"):
            $rc("Opposite sex... Dismissed.", "You are a male. Denied.")
        elif ct("Shy") and dice(50):  
            $rc("Ah, I'm sorry, I can't do that with a boy...", "Um, I-I like girls... Sorry!")
        elif ct("Imouto"):
            $rc("If you were a girl...it'd be alright, but...", "I don't really like boys... So no.")
        elif ct("Dandere"):
            $rc("Guys are...not for me.", "Wrong gender. Consider changing it.", "I turn down anyone who's not a girl.")
        elif ct("Kuudere"):
            $rc("Men for me are...well...", "I'm afraid men are not attractive to me.", "Doing that with a man is... a bit...")
        elif ct("Tsundere"):
            $rc("Hmph. And that's why I don't like men.", "Ugh, not again... I like girls, understood?", "Huh? You're a guy, so no way!")
        elif ct("Bokukko"):  
            $rc("Ew, don't wanna. You're a guy.", "Nah, I'm not interested in boys. Do you have a sister, by the way?", "Aah, I'm a lesbo, y'know.")
        elif ct("Ane"):
            $rc("My apologies, I'm a lesbian.", "I'm terribly sorry, but... I can't do that with a man.")
        elif ct("Yandere"):  
            $rc("Sorry, I only like girls.", "I dislike men, nothing personal.", "I... I can't do men.")
        elif ct("Kamidere"):
            $rc("I have no interest in men.", "Eww. I prefer girls, is it clear?", "Because you're a guy, no.")
        else: 
            $rc("Sorry. I'm weird, so... I'm not into guys.", "Well, I kinda prefer girls... If you know what I mean.", "If you were a girl... it'd be alright, but...")
        $ char.restore_portrait()
        return

label interactions_refused_because_tired: # a universal answer for tired characters, when they don't want to do something
    $ char.override_portrait("portrait", "tired")
    if ct("Impersonal"):
        $rc("I don't have required endurance at the moment. Let's postpone it.", "No. Not enough energy.")
    elif ct("Shy") and dice(50):
        $rc("W-well, I'm a bit tired right now... Maybe some other time...", "Um, I-I don't think I can do it, I'm exhausted. Sorry...")
    elif ct("Imouto"):
        $rc("Noooo, I'm tired. I want to sleep.", "Z-z-z *she falls asleep on the feet*") 
    elif ct("Dandere"):
        $rc("No. Too tired.", "Not enough strength. I need to rest.")
    elif ct("Tsundere"):
        $rc("I must rest at first. Can't you tell?", "I'm too tired, don't you see?! Honestly, some people...")
    elif ct("Kuudere"):
        $rc("I'm quite exhausted. Maybe some other time.", "I really could use some rest right now, my body is tired.")
    elif ct("Kamidere"):
        $rc("I'm tired, and have to intentions to do anything but rest.", "I need some rest. Please don't bother me.")
    elif ct("Bokukko"):
        $rc("Naah, don't wanna. Too tired.", "*yawns* I could use a nap first...")
    elif ct("Ane"):
        $rc("Unfortunately I'm quite tired at the moment. I'd like to rest a bit.", "Sorry, I'm quite sleepy. Let's do it another time.")
    elif ct("Yandere"):
        $rc("Ahh, my whole body aches... I'm way too tired.", "The only thing I can do properly now is to take a good nap...")
    else:
        $rc("*sign* I'm soo tired lately, all I can think about is a cozy warm bed...", "I am ready to drop. Some other time perhaps.")
    $ char.restore_portrait()
    return
    
label interactions_girl_dissapointed: # a universal answer when character is displeased by something
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $rc("... *you see disappointment in her eyes before she turns away*", "I see. A waste of time after all.")
    elif ct("Shy") and dice(50):
        $rc("I suppose you have your reasons...", "Err... Do you... nothing. Never mind.")
    elif ct("Imouto"):
        $rc("Whaaa? Are you serious?", "What, that's it? Boring and stupid!") 
    elif ct("Dandere"):
        $rc("Pathetic...", "You are a boring person.")
    elif ct("Tsundere"):
        $rc("You really must have a lot of free time to fool around like this...", "Hmph! Stop wasting my time!")
    elif ct("Kuudere"):
        $rc("How unreliable...", "That was quite pathetic, admit it.")
    elif ct("Kamidere"):
        $rc("As expected... You are wasting my time, you know that?", "It was entirely unsightly. Refrain from doing it from now on.")
    elif ct("Bokukko"):
        $rc("Man, that was lame. I mean, really lame.", "Oh c'mon, it's not even funny!")
    elif ct("Ane"):
        $rc("My, is that it? I expected something... better.", "*sigh* How troublesome...")
    elif ct("Yandere"):
        $rc("My time is precious for something like that, you know?", "Could you refrain from acting so in the future?")
    else:
        $rc("*sign* No wonder, my horoscope predicted a bad day.", "What a nuisance...")
    $ char.restore_portrait()
    return
    
label interactions_girl_proposes_sex: # character proposes MC sex
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $rc("So... do you want to have sex?", "I need sex. Let's do it.", "Please do perverted things to me. I'm ready.", "Please allow me to check if our bodies match. I'll take full responsibility.", "I would like to have sex with you. Is that going to be a problem?", "Can we have sex? I feel like I need it.")
    elif ct("Shy") and dice(50):
        $rc("Uh... p-please d-do it for me... my whole body's aching right now...", "Aah... p-please... I-I want it... I can't think of anything else now!", "Ummm.... do you... not wish to do it...? ...I... really want it...", "I-I want to... be... with you...", "Right now... I want you to do it with me now... Please...", "I-I'm actually really good at sex! So... I-I'd like to show you...", "Um, I-I want to do it... So... Could we have sex?")
    elif ct("Imouto"):
        $rc("Let's do kinky things... Come on? Puh-leaaase.", "I've got a huge favor to ask! Fuck me right now! Pleaaase!", "So, um... are you interested in sex? I mean, uhm... I'd kinda like to... do it with you?", "Uuu... I'm boooored! Let's do something fun! Like um...maybe have sex or something...") 
    elif ct("Dandere"):
        $rc("Looking at you... makes me want to do it. Do you want to?", "You want to feel good too, don't you?", "How about we do *it*? It'll be fine, leave it to me.", "Let's... feel good together.", "Do you want to spend some time inside of me?", "You are interested in sex and stuff, right? In that case, come on...")
    elif ct("Tsundere"):
        $rc("Hey, want to do it? S-sex, I mean...", "C'mon, you want to put it in too, right?", "Maybe I could agree if you asked me...  Geez! I'm telling you it's ok to have sex with me!", "You know... You wanna to have sex... with me?", "D-do you want to do that with me, maybe...? It's fine with me if you want to...", "C'mon. We're doing it. Doing what...? Haven't you figured it out?"),
    elif ct("Kuudere"):
        $rc("I-I was thinking...That I wanted to be one with you...", "Hey, I want to feel you inside me. Okay?", "Come on, I can tell that you're horny... Feel free to partake of me.", "Uhm... you're interested, right? In sex and stuff...", "H-hey, maybe the two of us could have... an anatomy lesson?", "I sort of want to do it now... You're cool with it, right?")
    elif ct("Kamidere"):
        $rc("Hey. Want to fuck...?", "Hey, you want to do perverted stuff...?", "So, let's do it. ...Huh? You were watching me because you wanted to fuck, right?", "You want to do me, don't you? Then step up and honestly say, 'hey, I want to do you'!", "What, you're looking at me like you want me, right? Then come over here.", "I'm specially allowing you to do whatever you like with me... You'll do it, right?", "You look like you really want to, so I'll let you do me.")
    elif ct("Bokukko"):
        $rc("Hey... if you'd like, I'll give ya' some lovin' ♪", "C'mon, it's time to put it in, what do you say?", "...Okay, that's it! I can't stand it! Sorry, I've gotta fuck ya!", "Hey... You want to have sex, don't ya?", "C'mon, c'mon, let's get kinky? C'mon, let's fuck!", "Shit, I'm horny as hell. Hey? You up for a go?", "Hey... you wanna mess around...? Let's do it while we got some time to kill...", "Aah geez, I can't hold it anymore! Let's fuck!", "Hey, d'you wanna do me? D'you wanna fuck me?")
    elif ct("Ane"):
        $rc("I was thinking of having sex with you... Is it ok...?", "Do you want to do it right now? I very much approve.", "Um... Is it ok with you if we have sex?", "How about this? That is to say... getting to know each other a bit better through sex?", "If you wish, shall I take care of your sexual needs?", "Excuse me... Would you like to have sex?", "You feel like doing it, don't you...? I really want it right now ♪")
    elif ct("Yandere"):
        $rc("Come on, I can tell that you're horny... Feel free to partake of me.", "I can do naughty stuff, you know? ...Want to see?", "Hey, you want to do it with me, right? There's no use trying to lie about it.", "Uhuhu... don't you want to have sex with me?", "Come on, I can tell you need some release... just leave it to me.", "Let's do it! Right now! Take off your clothes! Hurry!")
    else:
        $rc("Hey... Let's have sex.", "Say... d-do you want to do it... too?", "Um.. w-would you mind... having sex with me?", "Um... Please, have sex with me.", "Hey... do you think... we could do it?", "H-hey... Hmm, do I really need to be the one to say it... F-fuck me!", "Hey... I wanna have sex with you. Is that okay?")
    $ char.restore_portrait()
    return
    
label interactions_sex_begins: # lines in the beginning of a non-rape scene
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $rc("So, I'll begin the sexual interaction...", "I want you to feel really good.", "Hmm. Now how should I fuck you?", "Come. Touch me gently...", "...I have high expectations.", "I will try to do my best to meet your expectations.", "Now, let's enjoy some sex.", "I'll serve you.")
    elif ct("Shy") and dice(50):
        $rc("I-I'll do my best... for your sake!", "Uhm... I want you... to be gentle...", "Uuh... Don't stare at me so much, it's embarrassing...", "...I'm ready now... Do it any time...", "Uh, uhm, how should I...? Eh? You want it like this...? O-okay! Then, h-here I go...", "As I thought, I'm nervous... B-but that's ok... I prepared myself...", "P-Please look... It's become so gushy just from thinking about you...♪", "Sorry if I'm no good at this...")
    elif ct("Imouto"):
        $rc("Uhuhu, well then, what should I tease first ♪", "Hm hmm! Be amazed at my fabulous technique!", "Umm... please do perverted things to me ♪", "Hehe, I'm going to move a lot for you...", "Aah... I want you...To love me lots...", "Ehehe... now my clothes are all soaked...", "Ehehe, make me feel really good, okay?", "Please be gentle, ok?") 
    elif ct("Dandere"):
        $rc("Be sure to make me feel good too, ok?", "There's no reason for us to hold back... Come on, let's do this.", "I can't wait any more. Look how wet I am just thinking about you...", "Come on... Let's be one, body and soul.", "I will handle... all of your urges.", "My body can't wait any longer...")
    elif ct("Tsundere"):
        $rc("S-shut up and... entrust your body to me... Okay?", "Humph! I'll show you I can do it!", "I-I'm actually really good at sex! So... I-I'd like to show you...", "D-do it properly, would you? ...I don't want a shoddy performance." , "I'm gonna have sex with you! ..G-get ready!", "You can be rough, I guess... If it's just a little bit...", "Y-you just need to be still and let me do everything... You got that?", "D-do whatever you want..."),
    elif ct("Kuudere"):
        $rc("I'm going to make you cum. You had better prepare yourself.", "C'mon, I'll do kinky things, so make the preparations.", "Well then, shall I do something that'll make you feel good?", "Let's make this feel really good.", "L-leave it to me... Here, I'll take off your clothes...", "I-I'll make sure to satisfy you...!", "You can do with me... as you'd like...", "In the end, I'm just a normal woman too, you know...")
    elif ct("Kamidere"):
        $rc("Hmph, I'll prove that I'm the greatest you'll ever have.", "Now... show me the dirty side of you...", "I won't let you go until I'm fully satisfied, so prepare yourself.", "I'll give you a run you'll never forget ♪", "Okay... I suppose I'll just do as I please, uhuhu...", "Now, why don't you just give up and let me at that body of yours?", "Please, show me what you can do... I'm expecting great things.")
    elif ct("Bokukko"):
        $rc("C'mon, make me feel completely satisfied!", "You've been holding it in, right? You can do it with me, big time. Really big ♪", "Alright then, I'll give ya' some lovin'.", "You can do whatever you want. T-that's 'cause, I wanna know how you like it...", "C'mon, let's make love till every part of our bodies is tired... Uhuhu...")
    elif ct("Ane"):
        $rc("Now, let us discover the shape of our love ♪", "Hmhm, what is going to happen to me, I wonder? ♪", "Hehe, I won't let you go... Now quiet down and take this like an adult.", "Fufuh, it's okay to do it a little harder ♪", "Hehe... So you're ready to go just from looking at me?  Hehe, that makes me happy.", "There's no need to be ashamed... Please let me take care of you.", "Hmhm, go easy on me, okay?", "Hmhm, be good to me, will you?")
    elif ct("Yandere"):
        $rc("Ehehe... you can do whatever you want.", "Huhuhu, I'll give you a really. Good. Time.", "Huhu, so here we are... You can't hold it anymore, right?", "I want to try lots of things with you...", "I can't control myself anymore... uhuhu...", "Please let me have a clear look at your face when you cum.", "Huhuh, you'll fuck me like a beast, right?", "Yes! I can't take it anymore, I want it so bad! Ah!")
    else:
        $rc("I want to do so many dirty things... I can't hold it back ♪", "Leave it to me! I'll do my very best!", "Prepare to receive loads and loads of my love!", "Hehee, just leave it all to me! I'll make this awesome!", "Hehe, I'll give it everything I've got ♪")
    $ char.restore_portrait()
    return
    
label interactions_seen_mast_propose:
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $rc("If you got excited watching me, we could... Want to?", "I just can't do it alone... Can I count on you for support?")
    elif ct("Shy") and dice(50):
        $rc("...T-these perverted feelings... You can make them go away, can't you...?", "I- I'm sorry, I just couldn't hold it in any more... So, please, can we...")
    elif ct("Imouto"):
        $rc("I can't ask for it any more obviously than this! Just fuck me already, pleaaaaaase!", "Hey, come on, won't you touch me? I can't satisfy myself alone...") 
    elif ct("Dandere"):
        $rc("You caught me... Hey, please, can you take over from here?", "Watching me masturbate got you going, right? You wanna mess me up now, don't you?")
    elif ct("Tsundere"):
        $rc("Even I m...masturbate sometimes! ...S...so, what will you do?", "Y-you saw me masturbating... I demand s-sex as an apology!"),
    elif ct("Kuudere"):
        $rc("Hey, if you were watching, you know what I wanna do, right..?", "Nn... This urge, I need you to satisfy it for me...")
    elif ct("Kamidere"):
        $rc("At this point I don't even care.　Fuck me.", "I've been seen indulging in such a foolish act...　There's nothing left for you to do but take responsibility.")
    elif ct("Bokukko"):
        $rc("Hey... I want you to help me feel even better... Please...♪", "Masturbating's too much work... Hey, you wanna do it for me?")
    elif ct("Ane"):
        $rc("I can't simply let you go after you saw me pleasuring myself.", "How convenient, you came in at just the right time... Hey, you know what I mean, right?")
    elif ct("Yandere"):
        $rc("I'm all warmed up and ready to go... Want to do it?", "I would so much rather you do it than have to do it myself... Won't you?")
    else:
        $rc("Uuu, it's not enough by myself... Help me out here ♪", "Oh, it's you, [hero.name]... What to join?")
    $ char.restore_portrait()
    return
    
label interactions_seen_mast:
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $rc("What is it? I want to get back to what I was doing...", "Looks like I've been caught touching myself.")
    elif ct("Shy") and dice(50):
        $rc("Hyah!? I-I'm sorry! I'll wipe it off right away...!", "I-I... what an embarrassing thing to do...")
    elif ct("Imouto"):
        $rc("Ehehe, I'm all sticky...♪", "I-It's nothing, I was just a little itchy...") 
    elif ct("Dandere"):
        $rc("Aw, I was almost there...", "...Even you have times when you need to...do it yourself, right?")
    elif ct("Tsundere"):
        $rc("Kuh... Sometimes I masturbate too, you know. What's wrong with that...?!", "...I wasn't really doing anything, you know? Yeah."),
    elif ct("Kuudere"):
        $rc("Hya!? I-I wasn't... Ah, no, well...You're not wrong, but...", "Even I have times when I wish to console myself.")
    elif ct("Kamidere"):
        $rc("God, can't you see I'm playing with myself here? What is it?", "...I've shown you something foolish. Please forget about it.")
    elif ct("Bokukko"):
        $rc("Geez, I was in the zone! Quit bothering me!", "What do you want? And it was just getting good too, jeez...")
    elif ct("Ane"):
        $rc("Hehe, you caught me...", "Um, that's embarrassing... Please don't look at me so much.")
    elif ct("Yandere"):
        $rc("Hehehe, I just got a bit horny...", "Hey, can't you take a hint...? I'm kinda busy here...")
    else:
        $rc("Hyaa!?　Eh, ah, um, I just, well... Ahaha...", "Hyaaah!? I, I don't do anything..!")
    $ char.restore_portrait()
    return
    
label interactions_too_many_lines: # overused non-sexual line
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $rc("I request change of the subject.", "I don't feel the need to discuss this anymore.")
    elif ct("Shy") and dice(50):
        $rc("Um... Can you stop already?", "Um... Please, this is honestly too much...")
    elif ct("Imouto"):
        $rc("Stop it, that's annoying and boring!", "Uuuh, aren't you bored, talking about it again and again?") 
    elif ct("Dandere"):
        $rc("...You want to talk about that again?", "...It is a bother talking so much about the same thing.")
    elif ct("Tsundere"):
        $rc("Geez, give it a rest already!", "Ugh, you're really persistent!"),
    elif ct("Kuudere"):
        $rc("The more persistent you get, the more I want to shoot down whatever you say.", "Geez, you're too persistent.")
    elif ct("Kamidere"):
        $rc("How many times are you going to talk about it?", "Why do you keep talking about it? We already discussed it.")
    elif ct("Bokukko"):
        $rc("Gawd, stop repeating yourself!", "Hey, it becomes annoying. Don't you want to talk about something else?")
    elif ct("Ane"):
        $rc("You keep going back to the same thing again and again... You're bothering me.", "Persistence is not a virtue, you know?")
    elif ct("Yandere"):
        $rc("I hate people who are too persistent.", "Give it a rest. We already discussed it.")
    else:
        $rc("Why do you keep repeating yourself?", "Goodness, how many times are you going to talk about it?")
    "Maybe you should talk about something else."
    $ char.restore_portrait()
    return
    
label interactions_too_many_sex_lines: # overused sexual line
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $rc("I believe it's enough for today.", "I don't feel the need to do it one more time.")
    elif ct("Shy") and dice(50):
        $rc("S-sorry, let's do it later m-maybe..?", "Um... Please, this is honestly too much for today...")
    elif ct("Imouto"):
        $rc("Stop it, that's annoying and boring!", "Uuuh, aren't you bored, doing it again and again?") 
    elif ct("Dandere"):
        $rc("...You want to do it again? I don't want to.", "...Let's stop here. I'm tired of it.")
    elif ct("Tsundere"):
        $rc("Geez, give it a rest already!", "Ugh, you're really persistent. Stop it."),
    elif ct("Kuudere"):
        $rc("I think we should take a break.", "You're too persistent.")
    elif ct("Kamidere"):
        $rc("How many times are you going to do it?", "Unfortunately, I have no intentions to do it again.")
    elif ct("Bokukko"):
        $rc("Geez, enough already! I don't wanna to.", "Hey, it becomes annoying. Don't you want to do something else?")
    elif ct("Ane"):
        $rc("We keep doing it again and again... Let's stop it, alright?", "Persistence is not a virtue, you know?")
    elif ct("Yandere"):
        $rc("You are too persistent. I don't feel like it.", "Give it a rest. We already did it.")
    else:
        $rc("Aren't you tired of it? I am.", "How many times are you going to do it?")
    "Maybe you should try something else."
    $ char.restore_portrait()
    return