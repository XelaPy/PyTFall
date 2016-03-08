label interactions_badgift:
    $ char.override_portrait("portrait", "sad")
    if ct("Impersonal"):
        $rc("I don't need it.", "Can I return it later?", "What's it for?", "Please, never bring this to me again.", "This isn't exactly my favorite...")
    elif ct("Shy") and dice(50):
        $rc("<sigh>", "It's... for me? Um... why?", "Uh, it's for me? Ah... It's a... what is this, exactly? ...I see.")
    elif ct("Tsundere"):
        $rc("Who would want this crap?", "Hmph! What an idiot!", "Whaaat? What am I supposed to do with this?!", "How stupid are you?! <she looks ready to throw it at you>", "What the...? This is terrible!")
    elif ct("Kuudere"):
        $rc("Just this? Don't expect any thanks.", "And what should I do with this... thing?", "You know, a girl like me has no use for this.", "Oh? I thought you knew me better than that.", "Is this a gift? Oh...", "Is this some kind of mean joke?")
    elif ct("Yandere"):
        $rc("What were you thinking? This is awful!", "This is absolute junk. I'm offended.", "Ugh...that's such a stupid gift.", "Looks like your gifts are as desirable as you are right now.")
    elif ct("Dandere"):
        $rc("I don't want it.", "Oh. I guess I'll take it.", "..? <she does not look any happier>", "This is a pretty terrible gift, isn't it?", "This item gives me a terrible feeling. I'll have to dispose of it.")
    elif ct("Ane"):
        $rc("Not to be ungrateful, but... I really don't like this.", "<Sigh> I'll take it, but only this once.", "Umm... this is... interesting.", "Well, I guess it's the thought that counts...")
    elif ct("Imouto"):
        $rc("Hey! I don't want this!", "Oh, a present!... Ack! <her mood does a 180>", "Yuck! You thought I would like this?", "*sigh* This makes me depressed.", "Yuck, what is this? This isn't very fun...")
    elif ct("Kamidere"):
        $rc("This junk isn't useful at all.", "Hmm... I'm not a huge fan of this.", "This is probably the worst gift I've ever seen. Thanks a lot.", "Please refrain from bothering me with this in the future.")
    elif ct("Bokukko"):
        $rc("Man... this is bad...", "Hmm, so my zodiac was right... today's a bad day.", "Hey, is this a joke? What am I supposed to do with this?")
    else:
       $ rc("Hmm... I guess everone has different tastes...", "Thanks, but I don't like these kinds of things.", "I'll receive it, but... <sigh>", "Ugh...I'm sorry, but I absolutely hate this.")
    $ char.restore_portrait()
    jump girl_interactions
    
label interactions_goodgift:
    $ char.override_portrait("portrait", "happy")
    if ct("Impersonal"):
        $rc("Don't mind if I do.", "Thank you. I'll take it.", "I suddenly feel better now.", "I'll take that off your hands, if you don't mind.")
    elif ct("Shy") and dice(50):
        $ rc("Oh... th-thank you.", "Er, um... Thank you!", "<Blush> Is it ok if I take this?..", "That's... very nice.")
    elif ct("Tsundere"):
        $rc("What's this? To do something for someone like me... A-alright then.", "I was just thinking that I wanted one of these.", "Isn't this... too fancy for me?", "Hmm? Not bad. Thank you.",)
    elif ct("Kuudere"):
        $rc("Well... since you offered... <smiling>", "That's very kind of you. I like this.", "Oh, this is pretty good. I'll take it.", "You did good with this one, [hero.name]. Thanks." )
    elif ct("Yandere"):
        $rc("Now I have something you've given me. <blush>", "I don't mind if you spoil me. <smiles>", "*gasp*...for me? Thank you!")
    elif ct("Dandere"):
        $rc("...Thanks.", "Is it ok if I have this? Thanks.", "Is it alright for me to have this?", "Thanks.")
    elif ct("Ane"):
        $rc("Thank you. You have my regards.", "Oh my, I'm grateful ♪", "Trying to earn points, huh? <giggle>", "Oh, this is rather good.", "Oh, goodness! Are you sure? Thanks!")
    elif ct("Imouto"):
        $rc("Oh! You got me something! <giggles>", "Hehehe, if you keep doing this I'll be spoiled.", "Waa? Giving me things all of the sudden...", "I love presents! Thank you!")
    elif ct("Kamidere"):
        $rc("I will accept this; as a first-class lady.", "<Laughs> You just keep giving me things.", "Yes, this is how you should be treating me.")
    elif ct("Bokukko"):
        $rc("Oh? This is pretty good! Thanks.", "Yeah, looks good! Thanks!", "This is a fun gift. Thanks!", "Oh, a present! Thank you!", "This is a super gift! Thank you!")
    else:
        $ rc("Thank you so much!", "Yes, you have my thanks.", "Thank you...! I'm happy.", "This is a really nice gift! Thank you!", "Haha. Can't say 'no' to that.",  "No! I won't take it! Just kidding ♪", "Well, that's nice.")
    $ char.restore_portrait()
    jump girl_interactions

label interactions_perfectgift:
    $ char.override_portrait("portrait", "shy")
    if ct("Impersonal"):
        $rc("You really know what I like, don't you?", "It's incredible. Thank you.", "It... it's perfect.")
    elif ct("Shy") and dice(50):
        $rc("Oh!! A-amazing!", "<Blush> Is it alright if I have something this incredible?..", "Waaaa!? Is it worth it? ...Giving me something this valuable?")
    elif ct("Tsundere"):
        $rc("I-if you keep giving me things like this... <she's blushing>", "Am I really that special to you? ...I see <her face is completely red>", "I-it's not like I like it a lot!")
    elif ct("Kuudere"):
        $rc("Wh-where did you get one of these?! You're awesome!", "Tch... you're getting me indebted to you, [hero.name]")
    elif ct("Yandere"):
        $rc("You are sweet,[hero.name]... thank you... I like it.", "Oh, this is my favorite thing! ♪", "That's such a nice gift. Thank you!")
    elif ct("Dandere"):
        $rc("I really love this. How did you know?", "Thanks, I like this.", "<her smile is radiant>")
    elif ct("Ane"):
        $rc("Oh, you're such a sweetheart! I really love this!", "You're giving this... to me? I love it ♪ <smiles gently>", "With this we can get married! Just kidding ♪ <giggles>", "Oh my. It's really too much. <blush>", "Oh my, it looks wonderful! That's very kind of you.")
    elif ct("Imouto"):
        $rc("Hurray!", "Thank you! Chuuu ♥", "You didn't take out a loan for this, I hope ♪", "I seriously love this! You're the best, [hero.name]!", "*gasp* ...Wow! Thank you!")
    elif ct("Kamidere"):
        $rc("Hehe ♪, all this for one girl? Just kidding ♪", "Fantastic! You have a great taste.", "How... don't go blowing your money, alright? <she's got a huge grin>", "[hero.name], this is a beautiful gift! Thank you.")
    elif ct("Bokukko"):
        $rc("Man, this is good stuff... thanks!", "A-are you a mind reader? Because that would be unfair! ♥ <hugs> ♥", "Is that...? This is spectacular! Whoa! No way! Thank you!", "Hey, hey! Now this is really something! Thanks a million!")
    else:
        $rc("I'm so happy! Many thanks, [hero.name].", "You're amazing. This is exactly what I wanted! Thank you.", "Oh, you shouldn't have. Thank you, I really love this.", "This gift is fabulous! Thank you so much!")
    
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
        $rc("What do you think you're doing? You already gave it.", "Stop it. I have this already.")
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
    $ char.disposition -= randint(5, 15)
    jump girl_interactions
