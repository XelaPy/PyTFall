label girl_interactions_greeting:
    if chr.status != "slave":
        if chr.disposition > 900:
            if ct("Half-Sister") and dice(35):
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
                    $rc("I love you so much brother. You're very special to me.", "If it's for you, brother... I'm ready to do anything!")
                elif ct("Ane"):
                    $rc("It's natural for sister to love her brother.", "Sister will always be here to take care of you.")
                else:
                    $rc("I love everything about you... brother.", "Please look at your sister... as a woman.", "We're bound together now, even though we're siblings...", "Is it weird for siblings to stick together all the time?")
        
            elif ct("Shy") and dice(30):
                $rc("I lik-... I love you...!", "U-Um, er, I, um... I-I... I-I love you!", "Um, ah, er... I...l-li... I li-...! I can't do it!", "Um.... I-I love you very much...", "The two of us are going out... Ahhh...")
            elif ct("Nymphomaniac") and dice(45):
                $rc("I'm so lewd, aren't I... I'm thinking of you...doing me...", "Hey, what sorts of things do you think we can do, just the two of us?", "You can have me whenever you want!", "We're lovers, so we should act like lovers, we should get gooey and slap thighs.", "Hufh, I love you♪ Of course, also in a sexual way.", "Even if we are lovers, I wonder what we should do? Ah, you had dirty thoughts just now, didn't you?")
            elif ct("Impersonal"):
                $rc("I want to know everything about you. And I want you to know everything about me.", "I'm glad I could meet you.", "As long as we remain lovers, I believe it is essential to have a sensual relationship.", "I'll protect you.")
            elif ct("Extremely Jealous") and dice(30):
                $rc("I hate it when you just keep ogling other girls.", "I don't want you flirting with other women.", "I'm sorry, but I dislike it when you get too friendly with other women!", "Hey! Don't look at other girls all the time!", "My heart's feeling uneasy and gloomy... I dislike this feeling.", "Erm... I want you to stop looking at other women so much.")
            elif ct("Kuudere"):
                $rc("When y-you're around, I can't think straight...", "I c-can help out too if you need me, you know...", "I love you. ...That's it. Got a problem with that?", "P... Please continue to pursue me. My response will always be positive to you.", "I... I love you! You're very dear to me. I want us to stay together....")
            elif ct("Tsundere"):
                $rc("Wh-what are you planning to have me do...?", "You are NOT to leave my side, okay?", "B-being with you throws me off somehow...", "I deal with your perviness every day, so I deserve some praise!", "Umm... I love you. S-Show a little gratitude for being my choice.")
            elif ct("Dandere"):
                $rc("Sweetheart, sweetheart, sweeeetheart...", "Love you... Mm, it's nothing.", "I want to be with you.", "I want to be your special person...", "I-I'm a lonely person... So don't leave me...", "Saying I love you... Is, is not embarrassing...")
            elif ct("Imouto"):
                $rc("We're sweethearts, ehe!", "Hihi, object of my affection. What is up?", "We'll be together forever!", "Hehe, we're lovers.... do whatever you like.", "Ehehe, looooove youuuu♪", "I love you♪ I love you sooo much♪", "Have I become like a proper lover now?")
            elif ct("Ane"):
                $rc("I want to be both your big sister and your wife!♪", "I love you.  ...No, mere words aren't enough.", "I love you. I don't want to leave your side.", "As I thought, having a caring lover is good♪", "You'll love me forever, right?♪", "I'm really happy, you know? To be together like this with you♪")
            elif ct("Yandere"):
                $rc("Ah... ehhehe... I'm happy...", "We're lovers, aren't we...? Uhehehe...", "I, I'm your girlfriend, right? ...Ehehe", "I think it's really a good thing I've fallen in love with you.", "Ehehe♪ Nothing, just looking at your face♪", "Now how do I get you to fall for me even harder...? Kidding... Ehehe♪", "It would be nice if we could be together forever.")
            elif ct("Kamidere"):
                $rc("Even though we're lovers, doing nothing but ecchi things is not acceptable!", "Haaa... How'd I fall in love with someone like this...", "Just because we're l-lovers, doesn't mean I will spoil you...", "Hehe, what does my lover want from me?", "The only thing you'll ever need is me. Oh yes. Just me. Hehe.", "You think it's about time I turned you into my playtoy~?")
            elif ct("Bokukko"):
                $rc("Being subtle is such a bother so let me tell you straight... I love you.", "Even though we're dating now, not all that much has changed, huh...", "Say, what do you like about me? ...it's~ fine, tell me~!")
            else:
                $rc("I really like you, you know...", "A-As lovers, let's love each other a lot, okay...?", "We shouldn't flirt to much in front of the others, okay?", "I-I love you... Hehehe...♪", "I love you～ I love you so much～", "We're the most compatible couple in the world, aren't we?", "I want you to love me more and more! Prepare yourself for it, okay?", "I love you...I super love you...!", "Ehehe, don't you ever, ever leave me...", "I wish we could be together forever...♪", "What do you think other people think when they see us? ...you think maybe, 'Hey, look at that cute couple'...?")
    
        if chr.disposition < -350:
            if ct("Yandere"):
                $rc("<She looks at you with hostility>", "Stay away~", "...")
            elif ct("Impersonal"):
                $rc("State your business and leave.", "I have no interest in you.")
            elif ct("Shy") and dice(50):
                $rc("P-please, stay away!", "...D-don't come close to me.", "…S-S-Stay away!", "W-w-w-what do you want!?")
            elif ct("Dandere"):
                $rc("What is it? I want to get back to what I was doing...", "I personally dislike you.")
            elif ct("Kuudere"):
                $rc("Hmph, I don't even want to hear it.", "Oh? You've got a lot of nerve showing your face around me.", "...I don't think I have reason to talk to you.")
            elif ct("Tsundere"):
                $rc("Leave me alone!", "Go away. ...I said get the hell away from me!", "...Lowlife.", "Listening to you is a waste of my time.")
            elif ct("Ane"):
                $rc("What is it? Please leave me alone.", "I don't really feel like talking to you ", "Could you leave me alone?", "There is not a single shred of merit to your existence.")
            elif ct(Kamidere):
                $rc("You dirty little...", "It's you again. Don't bother me!", "Could you try to not talk to me, please?  Also, could you not breathe when near me? You're wasting good oxygen.", "Hmph! What an ugly sight.")
            elif ct("Imouto"):
                $rc("Geez, what is it?!", "Loooooooserー!", "Jeezー! Bug off already!", "You good-for-nothing...")
            elif ct("Bokukko"):
                $rc("Why are you bothering me?", "You just won't shut up, will you...", "Geez, you're pissing me off!")
            else:
                $rc("...Hey! Could you not get any closer to me, please?", "Sigh~… What is it?", "...Leave me alone.", "Geez, what is it...", "Leave, will you? I don't want to talk to you.", "You're an eyesore.", "You're so annoying!", "Why do you keep bothering me?", "Ah... I-I have stuff to do, so....", "U-Um... right now is a bit, err...")
    
        elif chr.disposition > 300:
            if ct("Impersonal"):
                $rc("Talk, I'll listen.", "...Being with you makes me feel extraordinarily comfortable.", "...You really like to talk, huh?", "What is your purpose in getting close to me?", "Being with you... calms me.")
            elif ct("Shy") and dice(30):
                $rc("I-I'm getting a little bit... used to you, [hero.name]...", "Hey, am I... do you… Err... nothing. Never mind.", "Being near you calms me down...", "H-Hi…Is it really ok to talk? I don't want to bother you…", "If I am with you, I…  I-it's nothing…")
            elif ct("Tsundere"):
                $rc("...Do you think I'm a tsundere too?", "Come, if you have something to say, say it!", "You really must have a lot of free time.", "Your clothes... it's looks untidy. Pull yourself together.", "Don't be so friendly with me...", "Please do not act like we are close to each other.")
            elif ct("Dandere"):
                $rc("You really enjoy talking, don't you.", "Did you need something?", "Maybe... I like that voice.", "Why are you so nice to me...?", "...Do you like talking to me this much?")
            elif ct("Kuudere"):
                $rc("You certainly like to be with me, don't you...", "Seriously... why is it so hard to be serious...?", "I'm listening. What is it?")
            elif ct("Ane"):
                $rc("If ever you're in trouble... you can always come to me.", "Hm? Something I can do?", "What's the matter? Need some advice?", "My, please continue.", "I'm here. What can I do for you?", "Ah... I was just thinking, it'd be so nice to talk to youー... Ehehe.", "If there's anything I can do, please tell me, okay?", "You can call on me anytime. And I'll do the same with you.", "If something's wrong, you can always talk to me.")
            elif ct("Imouto"):
                $rc("Hn? What's up? You can tell me anything. ♪", "For the people I like, I will do my best. ♪", "It looks like we could become good friends~ ♪", "Hi~~! Tell me, tell me, what'cha doin'?", "Let's have us a chat～ Lalala～♪")
            elif ct("Bokukko"):
                $rc("How's it going? Doing alright?", "Oh, what'cha doing?... What'ya wanna do?", "Ohoh, it's you. ♪", "Yo! What'cha doin'?", "Whazzup?", "Hey [hero.name], let's do something!", "Hi buddy!", "Huh? what, [hero.name]?", "Are you that interested in me? hehehe", "Hey, will you talk with me for a bit?", "C'mon, c'mon, put a smile on!", "Um so hey, you wanna chatー?")             
            elif ct("Kamidere"):
                $rc("Huhu, You seem like you'd be good for some entertainment. ♪", "Huu… You certainly like to be with me, don't you…", "Hu Hu~ ♪ Do you want to chat with me that badly?", "Being around me won't do you any good, you know?", "Ok. I have chosen to give you some of my valuable time today. Don't make me regret that.", "Good timing. Come on, entertain me.", "I have fairly high expectation of you.", "Eh, what? Do you want to consult with me?", "Is there something you would like to consult with me? It's alright.")
            else:
                $rc("Um, what is it?", "Hey, how's it going?", "Well, what shall we talk about..?", "What do you want to do?", "Let's walk together for a while.", "Hi! Another splendid day today!")
    
        else:
            if ct("Impersonal"):
                $rc("Start talking.", "State your business", "You're the kind of person who likes pointless conversations, right? Well, answering your questions makes me similar, I suppose.", "...Please do not get any closer.")
            elif ct("Shy") and dice(30):
                $rc("Ye~s, did you call?", "...Y-you want something from me?", "Um... W-what is it?", "Y-yes? Wh-what's going on?", "Wha... what is it...?", "U-Umm... What is it...?", "Y-yes, what do you need?", "C-can I help you...?", "Ye...yes?", "What... is wrong...?", "Wh-what is it...?")
            elif ct("Kuudere"):
                $rc("Hmph... I wonder if there is any particular purpose to this?", "What business do you have with me?", "Um, was there something you wanted to say?")
            elif ct("Dandere"):
                $rc("If you have business with me, please make it quick.", "You call?", "...?", "...Want something?", "Hmm?", "…", "...What is it?")
            elif ct("Tsundere"):
                $rc("Hmph. I've graced you with my presence, so be thankful.", "So, you want something or what?", "Spit it out already.")
            elif ct("Imouto"):
                $rc("Ehehe. What is it? ♪", "Muhuhu♪ Did you need something?", "Nu~u, what's up?", "Eh? What, what is it?", "Huhu, what is it?", "W-What? Did I do something wrong...?")
            elif ct("Ane"):
                $rc("Well, what shall we talk about..?", "Is there something I can help you with...?", "What business do you have with me?", "May I help you?", "…Yes? Did you need me for something?", "Is there... something I can help you with?")
            elif ct("Kamidere"):
                $rc("Hm? What? It's not like I have too much time to spend. Yes, that's right. I'm busy.", "...Yes? ...Did you call?", "...Do you want something?", "What is it? I'm busy right now.", "If you have business with me, hurry up and say it.")
            elif ct("Bokukko"):
                $rc("Hey-Hey! What do you want?", "Huh? What's up?", "Haa? You got a problem?", "What's up?", "Huh, Is there something you want to know?", "Huh? Do you want something?", "Whazzup?", "Did ya call me?", "Ummm, was there something you wanted to say?")
            elif ct("Yandere"):
                $rc("Yes? If you have no business here, then do please vacate from my sight.", "If you've got something to say, look me in the eyes and say it.", "...I don't recall asking to talk to you, so what is it?", "I don't have any business with you. If you do, make it quick.", "...Spit it out already.")
            else:
                $rc("...Is there something you need?", "Is there something you would like to ask?", "You called?", "Hmm?", "Is something the matter?", "What do you need from me?", "What is it? If you need something, then say it.", "You have business with me...?", "What is it?", "Yes, what is it?", "?...Is there something on your mind?", "...Do you need to talk to me?", "Yes? What do you want?", "...? Is there something on my face?", "Do you need something?", "Did you want to say something?", "You have something to tell me?", "Hm? Yes?", "Yes, what is it...?", "Hm? What's up?")
    else:
        if chr.disposition > 900:
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
                    $rc("I love you so much, brother. You're the best Master for me.", "If it's for you, brother... I'm ready to do anything!")
                elif ct("Ane"):
                    $rc("It's natural for sister to love her brother and Master.", "Sister will always be here to take care of you, Master.")
                else:
                    $rc("I love everything about you... brother.", "We're bound together now, Master, even though we're siblings...", "Is it weird for siblings to stick together all the time, Master?")
        
            elif ct("Shy") and dice(30):
                $rc("I lik-... I love you..., Master!", "U-Um, er, I, um... I-I... I-I love you, Master!", "Um, ah, er... I...l-li... I li-...! I can't do it, Master! I;m so sorry!", "Um.... I-I love you very much, Master...")
            elif ct("Nymphomaniac") and dice(45):
                $rc("I'm so lewd, Master, aren't I... I'm thinking of you...doing me...", "Hey, what sorts of things do you think we can do, Master, just the two of us?", "You can have me whenever you want, Master!", "We're lovers, Master, so we should act like lovers, we should get gooey and slap thighs.", "Hufh, I love you, Master♪ Of course, also in a sexual way.", "Even if we are lovers, I wonder what we should do? Ah, you had dirty thoughts just now, Master, didn't you?")
            elif ct("Impersonal"):
                $rc("I want to know everything about you, Master. And I want you to know everything about me.", "I'm glad I could meet you, Master.", "As long as we remain lovers, I believe it is essential to have a sensual relationship, Master.", "I'll protect you, Master.")
            elif ct("Extremely Jealous") and dice(30):
                $rc("I don't want you flirting with other women, Master...", "I'm sorry, Master, but I dislike it when you get too friendly with other women!", "Hey! Don't look at other girls all the time, Master!", "My heart's feeling uneasy and gloomy... I dislike this feeling.", "Erm... please stop looking at other women so much, Master.")
            elif ct("Kuudere"):
                $rc("When y-you're around, Master, I can't think straight...", "I c-can help out too if you need me, Master...", "I love you, Master. ...That's it.", "My response will always be positive to you, Master.", "I... I love you! You're very dear to me, Master. I want us to stay together....")
            elif ct("Tsundere"):
                $rc("Wh-what are you planning to have me do, Master...?", "B-being with you throws me off somehow, Master...", "I deal with your perviness every day, Master, so I deserve some praise!", "Umm... I love you, Master. S-Show a little gratitude for being my choice.")
            elif ct("Dandere"):
                $rc("Sweetheart, sweetheart, sweeeetheart...", "Love you, Master... Mm, it's nothing.", "I want to be with you, Master.", "I want to be your special person, Master...", "I-I'm a lonely person, Master... So don't leave me...", "Saying I love you... Is, is not embarrassing...")
            elif ct("Imouto"):
                $rc("Master and me are sweethearts, ehe!", "We'll be together forever, Master!", "Hehe, we're lovers.... do whatever you like, Master.", "Ehehe, looooove youuuu♪", "I love you, Master♪ I love you sooo much♪", "Have I become like a proper lover now, Master?")
            elif ct("Ane"):
                $rc("I want to be both your big sister and your wife, Master!♪", "I love you, Master.  ...No, mere words aren't enough.", "I love you, Master. I don't want to leave your side.", "As I thought, having a caring Master is good♪", "You'll love me forever, right, Master?♪", "I'm really happy, Master. To be together like this with you♪")
            elif ct("Yandere"):
                $rc("Ah... ehhehe... I'm happy, Master...", "We're lovers, aren't we, Master...? Uhehehe...", "I, I'm your girlfriend, right, Master? ...Ehehe", "I think it's really a good thing I've fallen in love with you, Master.", "Ehehe♪ Nothing, just looking at your face, Master♪", "Now how do I get you to fall for me even harder, Master...? Kidding... Ehehe♪", "It would be nice if we could be together forever, Master.")
            elif ct("Kamidere"):
                $rc("Even though we're lovers, doing nothing but ecchi things is not acceptable, Master!", "Haaa... How'd I fall in love with my own master...", "Hehe, what does my dear Master want from me?", "The only thing you'll ever need is me, Master. Oh yes. Just me. Hehe.")
            elif ct("Bokukko"):
                $rc("Being subtle is such a bother so let me tell you straight... I love you, Master.", "Even though we're lovers now, Master, not all that much has changed, huh...", "Say, what do you like about me, Master? ...it's~ fine, tell me~!")
            else:
                $rc("I really like you, Master...", "A-As lovers, let's love each other a lot, okay, Master...?", "We shouldn't flirt to much in front of the others, Master.", "I-I love you, Master... Hehehe...♪", "I love you, Master～ I love you so much～", "We're the most compatible couple in the world, aren't we, Master?", "I want you to love me more and more, Master! Prepare yourself for it, okay?", "I love you...I super love you, Master...!", "I wish we could be together forever, Master...♪", "What do you think other people think when they see us, Master? ...you think maybe, 'Hey, look at that cute couple'...?")
    
        if chr.disposition < -350:
            if ct("Yandere"):
                $rc("<She looks at you with hostility>What is it, 'Master'?", "...")
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
            elif ct(Kamidere):
                $rc("...", "You again... <sigh> Yes, Master?", "'Master', could you try to not talk to me without a good reason, please?", "Hmph!")
            elif ct("Imouto"):
                $rc("Geez, what is it, Master?!", "Jeez... I'm listening, Master.", "You good-for-nothing... Ahem, what is it, Master?")
            elif ct("Bokukko"):
                $rc("Yeah-yeah. I'm here, 'Master'.", "Geez, what is it again, Master?")
            else:
                $rc("Sigh~… What is it, Master?", "...Leave me alone, Master. Please.", "...I don't want to talk to you, Master.", "Ah... I-I have stuff to do, so....")
    
        elif chr.disposition > 300:
            if ct("Impersonal"):
                $rc("Yes, Master.", "I'm waiting for your order.", "...You really like to talk to your property, Master.", "Why are you so close to me, Master?", "Being with Master... calms me.")
            elif ct("Shy") and dice(30):
                $rc("M-master?", "Err... y-yes, Master?", "Being near you calms me down, Master...", "I…  I-it's nothing… W-what should I do, Master?")
            elif ct("Tsundere"):
                $rc("Hmph. It's not like enjoy to be your slave or something.", "You really must have a lot of free time, Master... I'm listening.", "Don't be so friendly with me, Master...", "P-please do not act like we are close to each other, Master.")
            elif ct("Dandere"):
                $rc("You really enjoy talking, Master.", "Did you need something, Master?", "I like your voice, Master.", "Why are you so nice to me, Master..?", "...Do you like talking to me this much, Master?")
            elif ct("Kuudere"):
                $rc("You certainly like to be with me, Master...", "Master?", "I'm listening, Master. What is it?")
            elif ct("Ane"):
                $rc("Hm? Something I can do, Master?", "What's the matter, Master? Need something?", "My, please continue, Master.", "I'm here. What can I do for you, Master?", "If there's anything I can do, please tell me, Master!", "Call on me anytime, Master.")
            elif ct("Imouto"):
                $rc("Hn? What's up, Master?", "I will do my best, Master. ♪", "Yes, Master! I'm here.")
            elif ct("Bokukko"):
                $rc("What'ya wanna do, Master?", "Yo, Master! What'cha doin'?", "Whazzup, Master?", "Huh? what, [hero.name]? Er, I mean Master?", "Um, you wanna something, Master?")             
            elif ct("Kamidere"):
                $rc("Huhu, You seem like you'd be good for some entertainment. ♪", "You certainly like to be with me, don't you, Master…", "Do you want to chat with me, Master?", "Being around me won't do you any good, Master.", "I have fairly high expectation of you, Master.", "Eh, what? Do you want to consult with me, Master?")
            else:
                $rc("Um, what is it, Master?", "Hey, how's it going, Master?", "What shall we talk about, Master?", "What do you want me to do, Master?")
    
        else:
            if ct("Impersonal"):
                $rc("Awaiting input.", "Yes, Master?", "Master?")
            elif ct("Shy") and dice(30):
                $rc("Ye~s, M-master?", "Y-you want something from me, Master?", "Um... Y-yes, Master?", "C-can I help you, Master?")
            elif ct("Kuudere"):
                $rc("I'm here, Master.", "I'm listening, Master.", "Yes, Master? Was there something you wanted?")
            elif ct("Dandere"):
                $rc("...Master?", "You call, Master?", "...?", "...What is it, Master?")
            elif ct("Tsundere"):
                $rc("Hmph. Y-yes, Master.", "Yes, Master. You want something or what?", "Well, I'm here, Master. Spit it out already.")
            elif ct("Imouto"):
                $rc("What is it, Master?", "Yes, Master? Did you need something?", "Nu~u, what's up, Master?", "Eh? What, what is it, Master?", "W-What? Did I do something wrong, Master?")
            elif ct("Ane"):
                $rc("Well, what shall we talk about, Master?", "Is there something I can help you with, Master?", "May I help you, Master?", "…Yes, Master? Did you need me for something?", "Is there something I can help you with, Master?")
            elif ct("Kamidere"):
                $rc("...Yes? Did you call, Master?", "...Do you want something, Master?", "If you have an order for me, hurry up and say it.")
            elif ct("Bokukko"):
                $rc("What do you want, Master?", "Huh? What's up, Master?", "Huh, Is there something you want to know, Master?", "Huh? Do you want something, Master?", "Whazzup, Master?", "Did ya call me, Master?")
            elif ct("Yandere"):
                $rc("Yes, Master?", "...What is it, Master?", "...Spit it out already... Er, yes, Master?")
            else:
                $rc("...Is there something you need, Master?", "Is there something you would like to ask, Master?", "You called, Master?", "Hmm?", "Is something the matter, Master?", "What do you need from me, Master?", "Yes, what is it, Master?", "Do you need something?, Master?", "Yes, what is it, Master?")
    
    # Accessed through call rather then jump
    return
    

label girl_trainings_greeting:
    if chr.disposition > 900:
        $rc("Am I doing well Master?", "Master <3")
    
    elif chr.disposition < -70:
        $rc("I'll never listen to you.", "Hmph.")
    
    elif chr.disposition > 300:
        $rc("What am I learning today?", "M-Mas...")
    
    else:
        g "..."
    
    # Accessed through call rather then jump
    return

label girl_meets_greeting:
    if chr.disposition > 900:
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
        
        elif ct("Shy") and dice(30):
            $rc("I lik-... I love you...!", "U-Um, er, I, um... I-I... I-I love you!", "Um, ah, er... I...l-li... I li-...! I can't do it!", "Um.... I-I love you very much...", "The two of us are going out... Ahhh...")
        elif ct("Nymphomaniac") and dice(25):
            $rc("I'm so lewd, aren't I... I'm thinking of you...doing me...", "Hey, what sorts of things do you think we can do, just the two of us?", "You can have me whenever you want!", "We're lovers, so we should act like lovers, we should get gooey and slap thighs.", "Hufh, I love you♪ Of course, also in a sexual way.", "Even if we are lovers, I wonder what we should do? Ah, you had dirty thoughts just now, didn't you?")
        elif ct("Impersonal"):
            $rc("I want to know everything about you. And I want you to know everything about me.", "I'm glad I could meet you.", "As long as we remain lovers, I believe it is essential to have a sensual relationship.", "I'll protect you.")
        elif ct("Extremely Jealous") and dice(20):
            $rc("I hate it when you just keep ogling other girls.", "I don't want you flirting with other women.", "I'm sorry, but I dislike it when you get too friendly with other women!", "Hey! Don't look at other girls all the time!", "My heart's feeling uneasy and gloomy... I dislike this feeling.", "Erm... I want you to stop looking at other women so much.")
        elif ct("Kuudere"):
            $rc("When y-you're around, I can't think straight...", "I c-can help out too if you need me, you know...", "I love you. ...That's it. Got a problem with that?", "P... Please continue to pursue me. My response will always be positive to you.", "I... I love you! You're very dear to me. I want us to stay together....")
        elif ct("Tsundere"):
            $rc("Wh-what are you planning to have me do...?", "You are NOT to leave my side, okay?", "B-being with you throws me off somehow...", "I deal with your perviness every day, so I deserve some praise!", "Umm... I love you. S-Show a little gratitude for being my choice.")
        elif ct("Dandere"):
            $rc("Sweetheart, sweetheart, sweeeetheart...", "Love you... Mm, it's nothing.", "I want to be with you.", "I want to be your special person...", "I-I'm a lonely person... So don't leave me...", "Saying I love you... Is, is not embarrassing...")
        elif ct("Imouto"):
            $rc("We're sweethearts, ehe!", "Hihi, object of my affection. What is up?", "We'll be together forever!", "Hehe, we're lovers.... do whatever you like.", "Ehehe, looooove youuuu♪", "I love you♪ I love you sooo much♪", "Have I become like a proper lover now?")
        elif ct("Ane"):
            $rc("I want to be both your big sister and your wife!♪", "I love you.  ...No, mere words aren't enough.", "I love you. I don't want to leave your side.", "As I thought, having a caring lover is good♪", "You'll love me forever, right?♪", "I'm really happy, you know? To be together like this with you♪")
        elif ct("Yandere"):
            $rc("Ah... ehhehe... I'm happy...", "We're lovers, aren't we...? Uhehehe...", "I, I'm your girlfriend, right? ...Ehehe", "I think it's really a good thing I've fallen in love with you.", "Ehehe♪ Nothing, just looking at your face♪", "Now how do I get you to fall for me even harder...? Kidding... Ehehe♪", "It would be nice if we could be together forever.")
        elif ct("Kamidere"):
            $rc("Even though we're lovers, doing nothing but ecchi things is not acceptable!", "Haaa... How'd I fall in love with someone like this...", "Just because we're l-lovers, doesn't mean I will spoil you...", "Hehe, what does my lover want from me?", "The only thing you'll ever need is me. Oh yes. Just me. Hehe.", "You think it's about time I turned you into my playtoy~?")
        elif ct("Bokukko"):
            $rc("Being subtle is such a bother so let me tell you straight... I love you.", "Even though we're dating now, not all that much has changed, huh...", "Say, what do you like about me? ...it's~ fine, tell me~!")
        else:
            $rc("I really like you, you know...", "A-As lovers, let's love each other a lot, okay...?", "We shouldn't flirt to much in front of the others, okay?", "I-I love you... Hehehe...♪", "I love you～ I love you so much～", "We're the most compatible couple in the world, aren't we?", "I want you to love me more and more! Prepare yourself for it, okay?", "I love you...I super love you...!", "Ehehe, don't you ever, ever leave me...", "I wish we could be together forever...♪", "What do you think other people think when they see us? ...you think maybe, 'Hey, look at that cute couple'...?")
    
    if chr.disposition < -70:
        if ct("Yandere"):
            $rc("...I don't like you...", "<She looks at you with hostility>", "Ugh, stay away~", "...I resent you.", "...!")
        elif ct("Impersonal"):
            $rc("Leave... You're a bother.", "This is a warning. If you continue to follow me, I cannot guarantee your life.", "I have no interest in you.")
        elif ct("Shy") and dice(50):
            $rc("J... just g...go away!", "P-please, stay away!", "...D-don't come close to me.", "<pannicked>…S-S-Stay away!", "W-w-w-what do you want!?", "Ah... I'm busy at the moment...", "P-Please stop trailing me...", "You're making me uncomfortable.")
        elif ct("Dandere"):
            $rc("What is it? I want to get back to what I was doing...", "Your existence is not needed.", "I personally dislike you.", "...Why do you exist again?")
        elif ct("Kuudere"):
            $rc("Hmph, I don't even want to hear it.", "You're the worst. Die, trash.", "Oh? You've got a lot of nerve showing your face around me.", "...I don't think I have reason to talk to you...")
        elif ct("Tsundere"):
            $rc("Leave me alone!", "Go away. ...I said get the hell away from me!", "...Lowlife.", "Listening to you is a waste of my time.")
        elif ct("Ane"):
            $rc("What is it? Please leave me alone.", "I don't really feel like talking to you ", "Ummm... You can stop following me, sir.", "Would you please stop following me?", "Er... uh, I have something I need to take care of, so I'll just...", "Could you leave me alone?", "Please excuse me, I'm a little busy.", "There is not a single shred of merit to your existence.", "Ah! I just remembered, I've got things to do, so...")
        elif ct(Kamidere):
            $rc("From now on you will speak with me only when spoken to! Do you understand that, maggot?", "You dirty little...", "It's you again. Don't bother me!", "<totally suprised> Kyah! Y-you bastard, when did you show up...?!", "Could you try to not talk to me, please?  Also, could you not breathe when near me? You're wasting good oxygen.", "Ahaha ♪ You look entirely unsightly! It fits you well", "That pathetic face of yours isn't fit to show to other people.", "Kukuku… It's unusual running into simpletons like you.", "Hmph! What an ugly sight.", "Hmph, a vulgar person like you doesn't deserve to talk to me!", "Hi monkey! Did someone leave your cage open?")
        elif ct("Imouto"):
            $rc("I hate you!", "Geez, what is it?!", "Geez, what is it?!", "Go away!", "Loooooooserー!", "Jeezー! Bug off already!", "You good-for-nothing...")
        elif ct("Bokukko"):
            $rc("Uwah, a pest has arrived!", "Why are you bothering me?", "No! Stop following me.", "You just won't shut up, will you...", "Geez, you're pissing me off!", "Oh, what's this? There's a weirdo in front of me. Whoa! It looked at me!")
        else:
            $rc("...Hey! Could you not get any closer to me, please?", "You're bothering me… Would you mind getting the hell out of here?", "Sigh~… What is it?", "Stop following me.", "Coming in here... You're a nuisance.", "Ah, please, don't bother me...", "...Leave me alone.", "Geez, what is it...", "Leave, will you? I don't want to talk to you.", "You're an eyesore.", "You're so annoying!", "Why do you keep bothering me?", "Ah... I-I have stuff to do, so....", "U-Um... right now is a bit, err...")
    
    elif chr.disposition > 300:
        if ct("Shy") and dice(30):
            $rc("Even being... with me... is ok...?", "I-I'm getting a little bit... used to you, [hero.name]...", "Hey, am I... do you… Err... nothing. Never mind.", "Being near you calms me down...", "H…H-Hello!", "It's you…H-Hi! …sorry…", "It's nice… to see you again.", "H-Hi…Is it really ok to talk? I don't want to bother you…", "Hello. It's nice of you… umm...to remember me…", "If I am with you, I…  I-it's nothing…")
        elif ct("Impersonal"):
            $rc("You don't need to worry about me.", "Talk, I'll listen.", "...Being with you makes me feel extraordinarily comfortable.", "...You really like to talk, huh?", "What is your purpose in getting close to me?", "Ah, it's you...", "Being with you... calms me...", "...I will escort you.", "...[hero.name]? …good.")
        elif ct("Tsundere"):
            $rc("...Hah! I-I wasn't completely fascinated by you or anything!", "...Do you think I'm a tsundere too?", "Looks like you're... somewhat capable, aren't you?", "Come, if you have something to say, say it!", "You again? You really must have a lot of free time.", "Your clothes... it's looks untidy. Pull yourself together.", "Don't be so friendly with me...", "Please do not act like we are close to each other. It would be terrible if someone got the wrong idea.")
        elif ct("Dandere"):
            $rc("You really enjoy talking, don't you.", "Did you need something?", "In front of you I feel strange...", "Maybe... I like that voice.", "Why are you so nice to me...?", "Sometimes I find myself thinking of you...", "...Do you like talking to me this much?")
        elif ct("Kuudere"):
            $rc("It's okay, come closer.", "Stick around. Alright?", "You certainly like to be with me, don't you...", "Hmph, you are an unusual fellow...", "Seriously... why is it so hard to be serious...?", "Haa... When you're around, I feel strange...")
        elif ct("Ane"):
            $rc("Pleased to meet you again, [hero.name].", "If ever you're in trouble... you can always come to me.", "Hm? Something I can do?", "What's the matter? Need some advice?", "It's you... My, please continue.", "I'm here. What can I do for you?", "Good day Sir. Nice to see you again.", "Oh, what a coincidence. I'm pleased to meet you again.", "Ah... I was just thinking, it'd be so nice to see youー... Ehehe.", "If there's anything I can do, please tell me, okay?", "You can call on me anytime. And I'll do the same with you.", "If something's wrong, you can always talk to me.")
        elif ct("Imouto"):
            $rc("Hi theeeere! Come on, cheer up!", "Hn? What's up? You can tell me anything. ♪", "For the people I like, I will do my best. ♪", "Hi~~~!", "Huhu ♪ Hmm, it's nothing… Ehehe... ♪", "It looks like we could become good friends~ ♪", "Hi~~! Tell me, tell me, what'cha doin'?", "Let's have us a chat～ Lalala～♪")
        elif ct("Bokukko"):
            $rc("Oh! Isn't it [hero.name]! G'day!", "How's it going? Doing alright?", "Oh, what'cha doing?... What'ya wanna do?", "Come on, come on, cheer up, let's go!", "Ohoh, it's you. ♪", "Yo [hero.name]! What'cha doin'?", "Okay, what shall we do today~?", "Hey, it's you! Whazzup?", "Hey~! It's you, come come, let's talk!", "Hey [hero.name], I'm free, so let's do something!", "Hey~ [hero.name], isn't there anything fun to do?", "Hi buddy!", "Huh? what, [hero.name]?", "Are you that interested in me? hehehe", "Hey, will you talk with me for a bit?", "C'mon, c'mon, put a smile on!", "Um so hey, you wanna chatー?")             
        elif ct("Kamidere"):
            $rc("Huhu, You seem like you'd be good for some entertainment. ♪", "Huu… You certainly like to be with me, don't you…", "Hu Hu~ ♪ Do you want to chat with me that badly?", "Being around me won't do you any good, you know?", "You've missed me, right? I know you did. Good boy ♪", "You came to visit me again? I know you couldn't help it, I'm just irresistible ♪", "You came just to see me? That's a point for you, but you have to try a lot harder to impress me, fufu ♪", "Ok. I have chosen to give you some of my valuable time today. Don't make me regret that.", "Good timing. Come on, entertain me.", "I have fairly high expectation of you.", "Eh, what? Do you want to consult with me?", "Is there something you would like to consult with me? It's alright.")
        else:
            $rc("[hero.name]...? Um, what is it?", "Hey! Did you think that I might have forgotten about you?!", "Ah, Hello~ ♪", "Hello, nice to see you again.", "Hey, how's it going?", "Hi! Nice to see you again!", "Hello~. What are you doing?", "Well, what shall we talk about..?", "I have the feeling I could get along with you.", "Hey, I just wanted to see you. ♪", "So? You enjoying life here?", "Oh, hello!", "Ah, it's you. Hi there!", "Oh Hi, it's you again…", "Hi! What a coincidence…", "Hi [hero.name]. How's it going?", "Hello [hero.name].", "Hi! What do you want to do?", "Hi [hero.name]! Let's walk together for a while.", "Ah! Hello♪", "Hi there [hero.name]! So what have you been up to?", "Hi! Another splendid day today!")
    
    else:
        if ct("Impersonal"):
            $rc("Start talking.", "State your business", "You're the kind of person who likes pointless conversations, right? Well, answering your questions makes me similar, I suppose.", "...Please do not get any closer.")
        elif ct("Shy") and dice(30):
            $rc("Ye~s, did you call?", "...Y-you want something from me?", "Um... W-what is it?", "Y-yes? Wh-what's going on?", "Wha... what is it...?", "U-Umm... What is it...?", "Y-yes, what do you need?", "C-can I help you...?", "Ye...yes?", "What... is wrong...?", "Wh-what is it...?")
        elif ct("Kuudere"):
            $rc("Hmph... I wonder if there is any particular purpose to this?", "What business do you have with me?", "Um, was there something you wanted to say?")
        elif ct("Dandere"):
            $rc("If you have business with me, please make it quick.", "Ah! Don't sneak up behind me.", "You call?", "...?", "...Want something?", "...Suspicious person.", "Hmm?", "…", "...What is it?")
        elif ct("Tsundere"):
            $rc("!? H-hey, at least let me know you're there or something...", "Hmph. I've graced you with my presence, so be thankful.", "So, you want something or what?", "Spit it out already.")
        elif ct("Imouto"):
            $rc("Ehehe. What is it? ♪", "Muhuhu♪ Did you need something?", "Nu~u, what's up?", "Eh? What, what is it?", "Huhu, what is it?", "W-What? Did I do something wrong...?", "Aaah! U-um...wh-what...?", "Waah!?　D-don't startle me like that, jeez...")
        elif ct("Ane"):
            $rc("Oh my, you startled me... Hmhm.", "Well, what shall we talk about..?", "Is there something I can help you with...?" ,"What business do you have with me?", "May I help you?", "…Yes? Did you need me for something?", "Is there... something I can help you with?")
        elif ct("Kamidere"):
            $rc("Hm? What? It's not like I have too much time to spend. Yes, that's right. I'm busy.", "Are you a stalker or something?", "...Yes? ...Did you call?", "...Do you want something?", "What is it? I'm busy right now.", "If you have business with me, hurry up and say it.","Did...did you just call me?")
        elif ct("Bokukko"):
            $rc("Huh? You called?", "Hey-Hey! What do you want?", "Huh? What's up?", "Haa? You got a problem?", "What's up?", "Huh, Is there something you want to know?", "Huh? Do you want something?", "Whazzup?", "Did ya call me?", "Ummm, was there something you wanted to say?")
        elif ct("Yandere"):
            $rc("Yes? If you have no business here, then do please vacate from my sight.", "If you've got something to say, look me in the eyes and say it.", "...I don't recall asking to talk to you, so what is it?", "You're in my way. Get lost.", "I don't have any business with you.", "...Spit it out already.")
        else:
            $rc("...Is there something you need?", "Ohhh… What seems to be the matter…? You over there. Is there something you would like to ask?", "You called?", "Hmm?", "...I don't like being stared at. Go away.", "...What? You're bothering me.", "Is something the matter?", "? What do you need from me?", "What is it, I'm busy here...", "What is it? If you need something, then say it.", "You have business with me...?", "What is it?", "Yes, what is it?", "?...Is there something on your mind?", "...Do you need to talk to me?", "Yes? What do you want?", "...? Is there something on my face?", "Do you need something?", "Did you want to say something?", "You have something to tell me?", "Hm? Yes?", "Yes, what is it...?", "Hm? What's up?", "Ah, sorry. Did you call me?")
    
    # Accessed through call rather then jump
    return
    
