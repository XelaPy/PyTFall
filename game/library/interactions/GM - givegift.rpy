label interactions_badgift:
    $ char.override_portrait("portrait", "sad")
    if ct("Impersonal"):
        $rc("I don't need it.", "Can I return it later?", "What's it for?")
    elif ct("Shy") and dice(50):
        $rc("But ... what?... <sigh>", "It's ... for me? ... <she looks sad>", "<She takes it, but there are tears in her eyes>")
    elif ct("Tsundere"):
        $rc("Hmph! What an idiot!", "Whaaat? What am I supposed to do with this?!", "How stupid are you?! <she looks ready to throw it at you>")
    elif ct("Kuudere"):
        $rc("And what should I do with this... thing?", "You know, a girl like me has no use for this.", "Oh? I thought you knew me better than that.")
    elif ct("Yandere"):
        $rc("<She takes it, but something dangerous flashes in her eyes.>", "... <for a brief moment she looks pissed>", "Looks like your gifts are as desirable as you are right now.")
    elif ct("Dandere"):
        $rc("I don't want it.", "No thanks.", "... <she does not look any happier>")
    elif ct("Ane"):
        $rc("Not to be ungrateful, but ... I really don't like this.", "<Sigh> I'll take it, but only this once.", "Umm ... thanks. <Her response is forced>")
    elif ct("Imouto"):
        $rc("Hey! I don't want this!", "Oh, a present! ... Ack! <her mood does a 180>", "Arg, I'm so unlucky.")
    elif ct("Kamidere"):
        $rc("Just this? Don't expect any thanks.", "Who would want this crap?", "This junk isn't useful at all.")
    elif ct("Bokukko"):
        $rc("Man... this is bad...", "Hmm, so my zodiac was right ... today's a bad day.", "Hey, is this a joke?")
    else:
       $ rc("Just as I feared, it's pretty bad...", "Thanks, but I don't like these kinds of things.", "I'll receive it, but... <sigh>")
    $ char.restore_portrait()
    jump girl_interactions
    
label interactions_goodgift:
    $ char.override_portrait("portrait", "happy")
    if ct("Impersonal"):
        $rc("Don't mind if I do.", "Thank you. I'll take it.", "I suddenly feel better now.", "I'll take that off your hands, if you don't mind.")
    elif ct("Shy") and dice(50):
        $ rc("Oh... th-thank you.", "Er, um... Thank you!", "<Blush> Is it ok if I take this?...", "That's ... very nice.")
    elif ct("Tsundere"):
        $rc("What's this? To do something for someone like me... A-alright then.", "I was just thinking that I wanted one of these.", "Isn't this... too fancy for me?", "Hmm? Not bad. Thank you.",)
    elif ct("Kuudere"):
        $rc("Well ... since you offered ... <smiling>", "Heh. Thank… you.", "Well, I guess this works.", "Oh, this is pretty good. I'll take it.")
    elif ct("Yandere"):
        $rc("Now I have something you've given me. <blush>", "I don't mind if you spoil me. <smiles>", "This is it, this is it! I've always wanted something like this! Let me have it now!")
    elif ct("Dandere"):
        $rc("Is..it ok?", "Is it ok if I have this? Thanks.", "Is it alright for me to have this?", "Thanks.")
    elif ct("Ane"):
        $rc("Thank you. You have my regards.", "Oh my, I'm grateful~.", "Trying to earn points, huh? <giggle>", "Oh, this is rather good.",)
    elif ct("Imouto"):
        $rc("Oh! You got me something! <giggles>", "Hehehe, if you keep doing this I'll be spoiled.", "Waa? Giving me things all of the sudden...", "Lucky♪")
    elif ct("Kamidere"):
        $rc("I will accept this; as a first-class lady.", "<Laughs> You just keep giving me things.", "Yes, this is how you should be treating me.", "I shall express my gratitude.")
    elif ct("Bokukko"):
        $rc("Oh? This is pretty good! Thanks.", "You know about karma, right? This is good karma.", "Yeah, looks good! Thanks!", "Hey, thanks.", "Hmm... Not bad!", )
    else:
        $ rc("Thank you so much!", "Yes, you have my thanks.", "Thank you...! I'm happy.", "Uhm, I greatly appreciate it!", "Many thanks!", "Haha. Can't say 'no' to that.",  "No! I won't take it! Just kidding~", "Well, that's nice.")
    $ char.restore_portrait()
    jump girl_interactions

label interactions_perfectgift:
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $rc("You really know what I like, don't you?", "It's incredible. Thank you.", "It ... it's perfect.")
    elif ct("Shy") and dice(50):
        $rc("Oh!! ... A-amazing!", "<Blush> Is it alright if I have something this incredible?...", "Waaaa!? Is it worth it? .... Giving me something this valuable?")
    elif ct("Tsundere"):
        $rc("I-if you keep giving me things like this ... <she's blushing>", "Am I really that special to you? ... I see <her face is completely red>", "I-it's not like I like it a lot!")
    elif ct("Kuudere"):
        $rc("Wh-where did you get one of these?! You're awesome!", "Tch... you're getting me indebted to you, [hero.name]")
    elif ct("Yandere"):
        $rc("You are sweet,[hero.name]...thank you...I like it.", "I ... I think I'm in love with you...")
    elif ct("Dandere"):
        $rc("♥♥♥♥ ... <she's so happy she's speechless>", "I'm...happy.", "<her smile is radiant>")
    elif ct("Ane"):
        $rc("I love it. <smiles gently>", "With this we can get married! Just kidding♪. <giggles>", "Oh my. It's really too much. <blush>")
    elif ct("Imouto"):
        $rc("Hurray!", "Thank you~. Chuuu ♥", "You didn't take out a loan for this, I hope. Chuu~")
    elif ct("Kamidere"):
        $rc("Hehe♪, all this for one girl? Just kidding♪", "Fantastic! You have a great taste.", "How ... don't go blowing your money, alright? <she's got a huge grin>")
    elif ct("Bokukko"):
        $rc("Man, this is good stuff... thanks!", "A-are you a mind reader? Because that would be unfair! ♥ <hugs> ♥", "Whoa! No way! Thank you!")
    else:
        $rc("I'm so happy! Many thanks, [hero.name]", "You're amazing.", "Oh, you shouldn't have. <blush>")
    
    if check_lovers(char, hero) and ct("Nymphomaniac"):
        g "I think you deserve a reward."
        $gm.generate_img("blowjob", "partner hidden", "simple bg", type="reduce")
        $ g("Did you like it? ♥")
    $ char.restore_portrait()
    jump girl_interactions
    
label interactions_refusegift:
    $ char.override_portrait("portrait", "angry")
    if ct("Impersonal"):
        $rc("This particular item is not required at the moment.", "I have one of these already.")
    elif ct("Shy") and dice(50):
        $rc("Um... I-I think you gave it to me already...", "It's... I already have one, sorry...")
    elif ct("Tsundere"):
        $rc("As expected from an idiot like you.", "Again? Really? What's wrong with your head?")
    elif ct("Kuudere"):
        $rc("What do you think you doing? You already gave it.", "Stop it. I have this already.")
    elif ct("Yandere"):
        $rc("Don't you remember? I have this already.", "Huh? You want to give me this again?")
    elif ct("Dandere"):
        $rc("Again?..", "One more? Why?")
    elif ct("Ane"):
        $rc("I appreciate the thought, but giving the same gift again and again is not a good idea.", "Oh, but I have this already. Don't you remember?")
    elif ct("Imouto"):
        $rc("Wha? I have it already!", "Ugh. I have this already. Boring!")
    elif ct("Kamidere"):
        $rc("You can't remember something so simple? Pathetic.", "Pfft. Naturally, I have no need for another one of these.")
    elif ct("Bokukko"):
        $rc("Man, really? Another one of these?", "Another one? Do you have a collection or something?")
    else:
        $rc("Sorry, I don't want another one of these.", "Didn't you give me it not so long ago?")
    $ char.restore_portrait()
    $ char.disposition -= 10
    jump girl_interactions
