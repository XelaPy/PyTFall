###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - sex - fuck - GI
#  2 - sex - blowjob - GI
#  3 - sex - anal - GI
#  4 - sex - lesbo - GI
#  5 - sex - sex - GM

###### j1
label interactions_fuck:
    if chr.status != "slave":
        if co("SIW") and chr.disposition < 400 - hero.charisma/2:
            
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "swimsuit", "beach"])
            $ rc("Not a chance!", "No freebies!", "And why would I want to do that?")
            
            if dice(50):
                $ chr.disposition -= randint(3, 5)
            
            jump girl_interactions
            
        elif chr.disposition < 700 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "swimsuit", "beach"])
            $ rc("No chance in hell!", "I am a bit tired...", "You're kidding? Right?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
    else:
        # Case: Slave
        if chr.disposition < -500 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "defiant", exclude=["nude", "swimsuit", "beach"])
            $ rc("I'd rather die!", "Get away from me!")
            $ chr.disposition -= randint(3, 5)
            
            jump girl_interactions
            
    # If we got here, we're good to go:
    if chr.normalsex < 30:
        
        $ rc("Lets have some fun!", "Lets fuck just like like bunnies!")
        $ pytfall.gm.img_generate("sex", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        
        "[chr.nickname] clearly needs more training..."
        
        if dice(75):
            extend " and she got slightly better."
            $ chr.normalsex += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
                
    else:
        $ rc("Lets have some fun!", "Lets fuck just like like bunnies!", "Just sit back and relax!")
        $ pytfall.gm.img_generate("sex", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        if dice(75):
            extend "[chr.nickname] has learned a thing or two."
            $ chr.normalsex += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
                
    if "Virgin" in chr.traits:
        "[chr.name] has lost her virginity."
        $ chr.removetrait(traits["Virgin"])
        
    if dice(int(round(hero.sex*0.3))):
        "You both recieve Extra stats bonus for your l33t skillz! :)"
        $ chr.normalsex += 1
        $ hero.sex += 1
        $ chr.joy += 3
        $ chr.disposition += 1
    $ hero.exp += adjust_exp(hero, randint(5, 10))
    $ chr.exp += adjust_exp(chr, randint(5, 10))
        
    jump girl_interactions
    

###### j2
label interactions_blowjob:
    # Take care of rejections first? Maybe put this on a separate label and use for all acts???
    if chr.status != "slave":
        if co("SIW") and chr.disposition < 300  - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("Not a chance!", "No freebies!", "And why would I want to do that?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
        elif chr.disposition < 500 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("No chance in hell!", "I am a bit tired...", "You're kidding? Right?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
    else:
        # Case: Slave
        if chr.disposition < -500 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "defiant", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("I'd rather die!", "Get away from me!")
            $ chr.disposition -= randint(3, 5)
            
            jump girl_interactions
            
    # If we got here, we're good to go:
    if chr.blowjob < 30:
        $ rc("Lets have some fun!", "Take off your pants!")
        $ pytfall.gm.img_generate("blowjob", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        "[chr.nickname] clearly needs more training..."
        if dice(75):
            extend " and she got slightly better."
            $ chr.blowjob += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
                
    else:
        $ rc("Lets have some fun!", "Take off your pants!",  "Just sit back and relax!")
        $ pytfall.gm.img_generate("blowjob", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        if dice(75):
            extend "[chr.nickname] has learned a thing or two."
            $ chr.blowjob += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
                
    if dice(int(round(hero.sex*0.3))):
        "You both recieve Extra stats bonus for your l33t skillz! :)"
        $ chr.blowjob += 1
        $ hero.sex += 1
        $ chr.joy += 3
        $ chr.disposition += 1
    $ hero.exp += adjust_exp(hero, randint(5, 10))
    $ chr.exp += adjust_exp(chr, randint(5, 10))
                
    jump girl_interactions
    

###### j3
label interactions_anal:
    # Take care of rejections first? Maybe put this on a separate label and use for all acts???
    if chr.status != "slave":
        if co("SIW") and chr.disposition < 500 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("Not a chance!", "No freebies!", "And why would I want to do that?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
        elif chr.disposition < 700 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("No chance in hell!", "I am a bit tired...", "You're kidding? Right?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
    else:
        # Case: Slave
        if chr.disposition < -500 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "defiant", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("I'd rather die!", "Get away from me!")
            $ chr.disposition -= randint(3, 5)
            
            jump girl_interactions
            
    # If we got here, we're good to go:
    if chr.analskill < 60:
        $ rc("Lets have some fun!", "Please be gentle, this is new to me...!")
        $ pytfall.gm.img_generate("anal", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        "[chr.nickname] clearly needs more training..."
        if dice(75):
            extend " and she got slightly better."
            $ chr.anal += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
    else:
        $ rc("Lets have some fun!", "Anything to make us both feel good!", "Just sit back and relax!")
        $ pytfall.gm.img_generate("anal", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        if dice(75):
            extend "[chr.nickname] has learned a thing or two."
            $ chr.anal += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
                
    if dice(int(round(hero.sex*0.3))):
        "You both recieve Extra stats bonus for your l33t skillz! :)"
        $ chr.anal += 1
        $ hero.sex += 1
        $ chr.joy += 3
        $ chr.disposition += 1
    $ hero.exp += adjust_exp(hero, randint(5, 10))
    $ chr.exp += adjust_exp(chr, randint(5, 10))
        
    jump girl_interactions
    

###### j4
label interactions_lesbo:
    # Take care of rejections first? Maybe put this on a separate label and use for all acts???
    if chr.status != "slave":
        if co("SIW") and chr.disposition < 300:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("Not a chance!", "And why would I want to do that?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
        elif chr.disposition < 400:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("No chance in hell!", "I am a bit tired...", "You're kidding? Right?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
    else:
        # Case: Slave
        if chr.disposition < - 500:
            $ pytfall.gm.img_generate("profile", "defiant", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("I'd rather die!", "While you watch? Not a chance!")
            $ chr.disposition -= randint(3, 5)
            jump girl_interactions
            
    # If we got here, we're good to go:
    if chr.vaginalskill < 60:
        $ rc("Kinda pervy? Watching two girls go at it?!", "Well, I am willing to try new things!")
        $ pytfall.gm.img_generate("les", exclude=["beach", "generic outdoor"], type="first_default")
        "[chr.nickname] clearly needs more training..."
        if dice(75):
            extend " and she got slightly better."
            $ chr.vaginal += 1
    else:
        $ rc("Kinda pervy? Watching two girls go at it?!", "Just sit back and enjoy the show!")
        $ pytfall.gm.img_generate("les", exclude=["beach", "generic outdoor"], type="first_default")
        if dice(75):
            g "[chr.nickname] has learned a thing or two."
            $ chr.vaginal += 1
            
    $ chr.exp += adjust_exp(chr, randint(5, 10))
        
    jump girl_interactions
    

###### j5
label interactions_sex:   
    
    if chr.disposition > 700:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 20
            $ gm_disp_mult = 0.3
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 99
            $ gm_disp_mult = 0.3
        else:
            $ gm_dice = 95
            $ gm_disp_mult = 0.3

    elif chr.disposition > 650:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 15
            $ gm_disp_mult = 0.5
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 99
            $ gm_disp_mult = 0.4
        else:
            $ gm_dice = 92
            $ gm_disp_mult = 0.5

    elif chr.disposition > 600:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 10
            $ gm_disp_mult = 0.8
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 98
            $ gm_disp_mult = 0.6
        else:
            $ gm_dice = 90
            $ gm_disp_mult = 0.8

    elif chr.disposition > 550:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 5
            $ gm_disp_mult = 1
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 98
            $ gm_disp_mult = 0.7
        else:
            $ gm_dice = 85
            $ gm_disp_mult = 1

    elif chr.disposition > 500:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 3
            $ gm_disp_mult = 1
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 90
            $ gm_disp_mult = 0.7
        else:
            $ gm_dice = 70
            $ gm_disp_mult = 1    

    elif chr.disposition > 400:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 2
            $ gm_disp_mult = 1
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 70
            $ gm_disp_mult = 0.8
        else:
            $ gm_dice = 20
            $ gm_disp_mult = 1
    elif chr.disposition > 300:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 2
            $ gm_disp_mult = 1
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 50
            $ gm_disp_mult = 0.9
        else:
            $ gm_dice = 5
            $ gm_disp_mult = 1
    elif chr.disposition > 100:
        if "Nymphomaniac" in  chr.traits:
            $ gm_dice = 20
            $ gm_disp_mult = 1
        else:
            $ gm_dice = 2
            $ gm_disp_mult = 1
    else:
        if "Nymphomaniac" in  chr.traits:
            $ gm_dice = 5
            $ gm_disp_mult = 1
        else:
            $ gm_dice = 1
            $ gm_disp_mult = 1

    if "Mind Fucked" in chr.traits:
        if gm_dice+20 > 100:
            $ gm_dice = 100
        else:
            $ gm_dice += 20
        $ gm_disp_mult *= 0.5

    if dice(gm_dice):
        $ gm_last_success = True
        $chr.disposition += (randint(15, 45)*(gm_disp_mult))
    else:
        $ gm_last_success = False
        $chr.disposition -= (randint(20, 60)*(gm_disp_mult))
    
    if gm_last_success:
        if ct("Half-Sister") and dice(30):
            if if ct("Impersonal"):
                $rc("I'll take in all your cum, brother.", "Sex with my brother, initiation.", "Let's have incest.", "Even though we're siblings... it's fine to do this, right?", "Let's deepen our bond as siblings.")
            elif ct("Shy") and dice(30):
                $rc("Umm... anything is fine as long as it's you... brother.", "I-if it's you, b-brother, then anything you do makes me feel good.")
            elif ct("Masochist") and dice(25):
                $rc("Are you going to violate me now, brother? Please?", "I'll be your slut any time you wish, brother.", "Hehe, would you prefer your sister to be to be an obedient girl?")
            elif ct("Imouto"):
                $rc("Teach me more things, brother!", "Brother, teach me how to feel good!", "Sis... will try her best.", "Sister's gonna show you her skills as a woman.")
            elif ct("Dandere"):
                $rc("Ah... actually, your sister have been feeling sexually frustrated lately...", "Brother, please do me.", "Even though we're related, we can have sex if we love each other.", "I'm only doing this because you're my brother.", "I'll do whatever you want for you, brother.", "Brother can do anything with me...", "I-is it alright to do something like that with my brother?")
            elif ct("Kuudere"):
                $rc("I... I can't believe I'm doing it with my brother...", "Y-you're lusting for your sister? O-okay, you can be my sex partner.", "I... I don't mind doing it although we're siblings, but...")
            elif ct("Tsundere"):
                $rc("Ugh... I... I have such a lewd brother!", "O... only you are allowed to touch me, brother.", "I... I'm only doing this because you're hard, brother.", "Doing something like this... with my brother... But... truth be told...")
            elif ct("Kamidere"):
                $rc("B...brother...it's... it's wrong to do this...!", "E...even though we're siblings...", "Doing such a thing to my brother. Am I a bad big sister?")
            elif ct("Yandere"):
                $rc("Make love to me, brother. Drive me mad.", "I'm looking forward to see your face writhing in mad ecstacy, bro.", "Shut up and yield yourself to your sister.", "Bro, you're a perv. It runs in the family though.", "Man, who'd have thought that my brother is as perverted as I am...", "My brother is in heat.  That's wonderful.", "As long as the pervy brother has a pervy sis as well, all is right with the world.", "Damn... The thought of incest gets me all excited now...")
            elif ct("Ane"):
                $rc("This is how you've always wanted to claim me, isn't it?", "Doing such things to your sister... Well, it can't be helped...", "Sis will do her best.", "Let sis display her womanly skills.")
            elif ct("Bokukko"):
                $rc("You wanted to have sex with your sister so bad, huh?", "Have you been planning to do this? Man, what a hopeless brother you are...", "I'm gonna show you that I'm a woman too, bro.", "Right on, brother.  Better you just shut up and don't move.", "Leave this to me, you can rely on sis.", "As long as it's for my brother a couple of indecent things is nothing.")
            else:
                $rc("It's alright for siblings to do something like this.", "Make your sister feel good.", "Just for now, we're not siblings... we're just... a man and a woman.", "We're brother and sister. What we're doing now must remain an absolute secret.", "I'll do my best. I want you to feel good, brother.", "I bet our parents would be so mad.")
       
        elif ct("Impersonal"):
            $rc("...Please insert to continue.", "You are authorized so long as it does not hurt.", "You can do me if you want.", "So, I'll begin the sexual interaction...", "Understood. I will... service you…", "I dedicate this body to you.")
        elif ct("Shy") and dice(30):
            $rc("D-do you mean…  Ah, y-yes…  If I'm good enough…", "Eeh?! Th-that's... uh... W- well... I do... want to...", "O...okay. I'll do my best.", "I-I was thinking… That I wanted to be one with you…", "If it's you, I'm fine with anything...", "I too... wanted to be touched by you... ","I want my feelings…  To reach you…", "It's... it's... o-okay to... have... s--s-sex... with me...", "Uh... I... h...how should I say this... It... it'll be great if you could do it gently...", "Aah... p... please... I... I want it... I... I can't think of anything else now!", "I-I'll do my best... for your sake!", "Uhm... I want you... to be gentle...", "Um, I-I want to do it… Please treat me well…", "Uh, uhm, how should I...? Eh? You want it like this...? O-okay! Then, h-here I go…", "Eeh, i-is it ok with someone like me...?", "Sorry if I'm no good at this...", "Uh... p... please... d...do it for me... my whole body's aching right now...", "Umm... anything is fine as long as it's you...", "Umm… please do perverted things to me…", "I don't know how well I will do...")
        elif ct("Nymphomaniac") and dice(40):
            $rc("Come on, I'll do the same for you, so please hurry and do me.", "Ahh, I can't wait anymore... quickly... please do me fast…", "I've been waiting for you all this time, so hurry up.", "Ready anytime you are.", "Please fill my naughty holes with your hot shaft.", " Let's do it all night long, okay? ...What, I'm just a dirty-minded girl~ ♪", "I don't mind. I really loooove to have sex. ♪", "Just watching is boring, right?  So… ♪", "...Shit! Now I'm horny as hell! ...Hey? You up for a go?", "Whenever, wherever…", "If you'd made me wait any longer I would have violated you myself.", "You know, had you kept me waiting any longer I would probably have jumped you myself.", "I hope you know how to handle a pussy...", "Man, who'd have thought that you are as perverted as I am...", "Ah... actually, I have been feeling sexually frustrated lately...", "Aah~~ Geez, I can't hold it anymore! Let's fuck!", "Hyauh…  Geez, do you have any idea how long I've been wet?", "Finally!", "You can ask me as much as you like... We can do it again... and again...", "...These perverted feelings... You can make them go away, can't you...?", "Umm, I-I'm always ready for it, so...!", "Turn me into a sloppy mess...!", "Let's do it! Right now! Take off your clothes! Hurry!", "Hmmm, what should I do～? ...Do you wanna do it THAT much～? I guess there's no stopping it～", "eah, it's okay. If that's what you want. Besides... I kinda like this stuff.")
        elif ct("Masochist") and dice (20):
            $rc("Feel free to make me your personal bitch slave!", "Geez～, you could have just taken me by force～...", "Kya~... I - am - being - molested -... Oh come on, at least play along a little bit...")
        elif ct("Sadist") and dice(20):
            $rc("Become my... sex slave ♪", "Just shut up and surrender yourself to me. Good boy.", "Stay still and let me violate you.", "Come. I'll be gentle with you.")
        elif ct("Tsundere"):
            $rc("*gulp*… W-well... since you're begging to do it with me, I suppose we can…", "It...it can't be helped, right? It... it's not that I like you or anything!", "I-it's not like I want to do it! It's just that you seem to want to do it so much…", "I'll punish you if I don't feel good, got it?", "Hhmph... if...if you wanna do it... uh... go all the way with it!", "Hm hmm! Be amazed at my fabulous technique!", "If you're asking, then I'll listen… B-but it's not like I actually want to do it, too!", "I-I'm actually really good at sex! So... I-I'd like to show you…", "I...I'm only doing it because of your happy face.", "Humph! I'll show you I can do it!", "If-if you say that you really, really want it… Then I won't turn you down…", "L.... leave it to me... you idiot...", "If you want to do it now, it's okay… I just don't want to do anything weird in front of other people.", "Th-things like that should only happen after marriage… but… fine, I'll do it…", "God, people like you… Are way too honest about what they want…", "T...that can't be helped, right? B...but that doesn't mean you can do anything you like!", "You're hopeless.... Well, fine then....", "...Yes, yes, I'll do it, I'll do it so…  geez, stop making that stupid face…", "Geez, you take anything you can get...")
        elif ct("Dandere"):
            $rc("...Very well then. Please go ahead and do as you like.", "I... want you inside me.", "You're welcome to... do that.", "You can do whatever you want to me.", "I'm going to make you cum. You had better prepare yourself.", "I will not go easy on you.", "I... I'm ready for sex.", "Make me feel good...", "...If you do it, be gentle.", "I will handle... all of your urges...", "Then…  I will do it with you…", "...If you want, do it now.", "...I want to do it, too.", "...How do you want it?  ...Okay, I can do it…", "Now is your chance...")
        elif ct("Kuudere"):
            $rc("...I don't particularly mind.", "Heh. I'm just a girl too, you know. Let's do it.", "...V-Very well. I will neither run nor hide.", "Don't forget that I'm a woman after all...", "What a bothersome guy... Alright, I get it.", "...Fine, just don't use the puppy-dog eyes.", "*sigh* ...Fine, fine! I'll do it as many times as you want!", "Fine with me… Wh-what? ...Even I have times when I want to do it…")
        elif ct("Imouto"):
            $rc("Ehehe... It's ok? Doing it...", "Ehehe, I'm going to move a lot for you... ♪", "[chr.name] will show you the power of love♪", "I can do naughty stuff, you know? ...Want to see?", "Uhuhu, Well then, I'll be really nice to you, ok? ♪", "Uhuhu, Well then, what should I tease first~ ♪", "Okayyy! Let's love each other a lot. ♪", "Hey? You want to? You do, don't you? We can do it, if you waaaaant~", "Aah... I want you… To love me lots…", "Ehehe♪ Prepare to receive loads and loads of my love! ♪", "Hold me really tight, kiss me really hard, and make me feel really good. ♪", "Aha, When I am with a certain someone, I do only naughty things~… Uhuhu ♪", "Yeah, let's make lots of love♪", "I-is it okay for me to climb onto you? I'm sorry if I'm heavy...", "I-I'll do my best to pleasure you!", "Yes. I'm happy that I can help make you feel good.", "I don't know how well I will do...", "Geez, you're so forceful...♪")
        elif ct("Ane"):
            $rc("Hmhm, what is going to happen to me, I wonder?", "Come on, show me what you've got...", "This looks like it will be enjoyable.", "If you can do this properly... I'll give you a nice pat on the head.", "Seems like you can't help it, huh...", "Fufufu, please don't overdo it, okay?", "Go ahead and do it as you like, it's okay.")
        elif ct("Bokukko"):
            $rc("Heh heeeh~♪ It's cool, no one's here. ♪", "Y-yeah… I sort of want to do it, too... ehehe…", "Wha!? C-can you read my mind...?", "Ah, eh, right now?", "Okay... but I'll do it like I want, kay?" ,"...Okay, that's it! I can't stand it! I've gotta fuck ya!", "S-sure… Ehehe, I'm, uh, kind of interested, too…", "Hey, let's do it while we got some time to kill...?", "Hehee, just leave it all to me! I'll make this awesome!", "Gotcha, sounds like a plan!", "Hey, maybe… The two of us could have an anatomy lesson?", "Is that ok? Ehehe... I wanted to do it too…", "Huhu… I want to do it with a pervert like you.", "Ehehe… In that case, let's go hog wild~", "Ehehe… So... let's do it. ♪", "Hmph... if you'd like, I'll give ya' some lovin'. ♪", "Got'cha. Hehe. Now I won't go easy on you.", "Y-yeah... if we're going to do it, we should do it now...", "Huhuh, I sort of want to do it now...", "Hey, er…  Wanna try doing it with me...?")
        elif ct("Yandere"):
            $rc("Fine, if you insist...", "Hehe. How should I make you feel good?", "If we have sex you will never forget me, right?♪", "Please do your best... if it's you, it'll be okay.", "Heh heh... You're going to feel a lot of pleasure. Try not to break on me.", "Alright, I'll just kill some time playing around with your body...", "Feel grateful for even having the opportunity to touch my body.", "Huhuh, I'll kill you with my tightness...")
        elif ct("Kamidere"):
            $rc("*giggle* I'll give you a feeling you'll never get from anyone else…", "Oh? You seem quite confident. I'm looking forward to this. ♪", "You're raring to go, aren't you? Very well, let's see what you've got.", "Now then, show me sex appropriate to someone qualified to be my lover...", "Hhmn... My, my... you love my body so much? Of course you do, it can't be helped.", "Oh, you seem to understand what I want from you,.. Good doggy, good doggy ♪", "Be sure to make me feel good, got it?", "Then you're bored, too.", "Feel grateful for even having the opportunity to touch my body.", "You won't be able to think about anybody else besides me after I'm done with you.", "Huhuhu, having sex with me… pretty cheeky for a pet dog~ ♪", "Hmph, Entertain me the best you can…", "Hmph, I'll prove that I'm the greatest you'll ever have...", "...For now, I'm open to the idea.", "Huhuh, I'll be using you until I'm satisfied...", "Huhu, you can't cum until I give you permission, okay? So, get ready to endure it~ ♪", "I don't really want to, but since you look so miserable I'll allow it.", "For me to get in this state... I can't believe it...", "Haa, in the end, it turned out like this…  Fine then, do as you like…")
        else:
            $rc("Oh... I guess if you like me it's ok.", "Fufu… I hope you are looking forward to this…!", "For you, I'll do my best today as well, okay?", "If it's with you... I'd do it, you know...?", "If you're so fascinated with me, let's do it.", "Hn, I want you to feel really good, okay...", "If we're going to do it, then let's make it the best performance possible. Promise?", "Now, let us discover the shape of our love. ♪", "Let's... feel good together...", "Huhn, if you do it, then… please make sure it feels good…", "Huhu, so here we are…  you can't hold it anymore, right?", "Then… Let's do it? ♪", "Sex... O-okay, let's do it...", "I don't mind. Now get yourself ready before I change my mind.", "Please let me make you feel good...", "What do you think about me, let your body answer for you…", "If you feel like it, do what you want, with my body…", "Ok, I'll serve you! ♪", "Now, [chr.name] shall give you some pleasure ~ !", "Want to become one with me? …ok", "You're this horny...? Fine, then…", "If that's what you desire...", "Oh? You've already become like this? Heh, heh... ♪", "Okay… I'd like to.", "That expression on your face... Hehe, do you wanna fuck me that much?", "You insist, hm? Right away, then!", "Heh, how can I say no?", "Hum, What should we do? ...That, there? ..hmm", "I want to do so many dirty things... I can't hold it back...", "Huhuhu, I'll give you a really. Good. Time. ♪", "You can't you think of anything else beside having sex? You're such a perv~", "So you want to do it. Right. Now? Huhu... I very much approve. ♪", "You mean, like, have sex and stuff? ...Hmm~?  Meh, you pass!", "What? You want to do it? Geez, you're so hopeless... ♪", "Come on, I can tell that you're horny… Feel free to partake of me.", "Huhn, fine, do me to your heart's content.", "Um, if you'd like, I can do it for you… I'll do my best!", "I know you wanna feel good too. ...huhu, come here…", "I can't wait any more… Huhu, look how wet I am just thinking about you... ♪", "S-shut up and... entrust your body to me… Okay?", "You've got good intuition. That was just what I had in mind, Huhuh. ♪", "Haa, your lust knows no bounds...", "Huhu, ok then… Surrender yourself to me…", "Now... show me the dirty side of you…", "You really like it, don't you… Huhuh, okay, let's go.", "Y-yes… I don't mind letting you do as you please…", "I want to do it with you...", "Hn…  Looking at you... makes me want to do it…", "If the one corrupting my body is you, then I'll have no regrets.", "Yes. Go ahead and let my body overwhelm you.", "... Leave it to me...", "I'll do it. You better be prepared.", "I wanna do all kinds of dirty things to you. Just let yourself go, okay?", " Leave it to me... I'll make you cum so much.", "All right. Do as you like.", "Let's deepen our love for each other.", "Please, go ahead and do it.", "Are we going... All the way?", "Yup. That's the way. You need more love.", "Not good... I want to do perverted things so badly, I can't stand it...", "Sure, if you want", "Hey... do me...", "I-if it's with you... I'd go skin to skin...") 

        hide screen pyt_girl_interactions
        $renpy.show('chr', what=chr.show('sex', "partner hidden", exclude=["scared"], resize=(int(config.screen_width*0.85), int(config.screen_height*0.785)), type="first_default"), at_list=[Position(ypos = 0.8)])          #temporarily / needs better possitioning and ideally tags
        with dissolve
        $renpy.pause()
        
        if dice(75):
            $ chr.normalsex += 1
        if dice(50):
            $ hero.sex += 1

        if "Virgin" in chr.traits:
            "[chr.name] has lost her virginity."
            $ chr.removetrait(traits["Virgin"])

    else:
        if ct("Half-Sister") and dice(30):
            if ct("Impersonal"):
                $rc("No... no incest please...")
            elif ct("Yandere"):
                $rc("Wait! We're siblings damnit.", "Hey, ummm... Siblings together... Is that really okay?")
            elif ct("Dandere"):
                $rc("We're siblings. We shouldn't do things like this.", "Do you have sexual desires for your sister...?")
            elif ct("Bokukko"):
                $rc("B... brother! P... please don't say things like that!")
            elif ct("Tsundere"):
                $rc("It's... it's wrong to have sexual desire among siblings, isn't it?", "Brother, you idiot! Lecher! Pervert!")
            elif ct("Kuudere"):
                $rc("...You want your sister's body that much? Pathetic.", "How hopeless can you be to do it with a sibling!")
            elif ct("Ane"):
                $rc("What? But... I'm your sister.", "Don't you know how to behave yourself, as siblings?")
            elif ct("Kamidere"):
                $rc("It's unacceptable for siblings to have sex!", "I can't believe... you do that... with your siblings!", "Having sex with a blood relative? That's wrong!")
            elif ct("Bokukko"):
                $rc("Man, you are weird.", "I'm your sis... Are you really okay with that?")
            else:
                $rc("No! Brother! We can't do this!",  "Don't you think that siblings shouldn't be doings things like that?")
        elif ct("Impersonal"):
            $rc("I see no possible benefit in doing that with you so I will have to decline.", "No.")
        elif ct("Not Human") and dice(20):
            $rc("I wonder why humans constantly wish to have sex...")
        elif ct("Shy") and dice(30):
            $rc("I... I don't want that! ","W-we can't do that. ","I-I don't want to. ...sorry.")
        elif ct("Lesbian") and dice(25):
            $rc("Ew, don't wanna. You're a guy.", "I'm terribly sorry, but... I can't do that with a man.", "Men for me are... well...")
        elif ct("Imouto"):
            $rc("Noooo way!", "I, I think perverted things are bad!", "That only happens after you've made your vows to be together forever, right?", "...I-I'm gonna get mad if you say that stuff, you know? Jeez!") 
        elif ct("Dandere"):
            $rc("Keep sexual advances to a minimum.", "No.", "...pathetic.", "...you're no good.")
        elif ct("Tsundere"):
            $rc("I'm afraid I must inform you of your utter lack of common sense. Hmph!", "You are so... disgusting!!", "You pervy little scamp! Not in a million years!", "Hmph! Unfortunately for you, I'm not that cheap!")
        elif ct("Kuudere"):
            $rc("...Perv.", "...Looks like I'll have to teach you about this little thing called reality.", "O-of course the answer is no!", "Hmph, how unromantic!")
        elif ct("Kamidere"):
            $rc("Wh-who do you think you are!?", "W-what are you talking about… Of course I'm against that!", "What?! How could you think that I... NO!", "What? Asking that out of the blue? Know some shame!", "You should really settle down.", "What? Dying wish? You want to die?", "The meaning of 'not knowing your place' must be referring to this, eh...?", "I don't know how anyone so despicable as you could exist outside of hell.")
        elif ct("Bokukko"):
            $rc("He- Hey, Settle down a bit, okay?", "You should keep it in your pants, okay?", "Y-you're talking crazy...")
        elif ct("Ane"):
            $rc("...Give me a bit more time, please.", "Sorry... I'm not ready for that...", "Oh my, can't you think of a better way to seduce me?", "No. I have decided that it would not be appropriate.", "I'm sorry, it's too early for that.", "I don't think our relationship has progressed to that point yet.", "I think that you are being way too aggressive.", "I'm not attracted to you in ‘that’ way.")
        elif ct("Yandere"):
            $rc("I've never met someone who knew so little about how pathetic they are.", "...I'll thank you to turn those despicable eyes away from me.")
        else:
            $rc("No! Absolutely NOT!", "With you? Don't make me laugh.", "Yeah right, dickhead.", "Yeah, get the fuck away from me, you disgusting perve.", "Get lost, pervert!", "Woah, hold on there, killer. Maybe after we get to know each other better.", "Don't tell me that you thought I was a slut...?", "I'm just really tired... ok?", "How about you fix that 'anytime's fine' attitude of yours, hmm?")  
    
    jump girl_interactions
    
