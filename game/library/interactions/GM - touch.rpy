label interactions_hug:
    "You try to hug her."
    $ interactions_check_for_bad_stuff(char)
    if char.disposition > 600:
        $ gm_dice = 98
        $ gm_disp_mult = 0.2
    elif char.disposition > 400:
        $ gm_dice = 98
        $ gm_disp_mult = 0.4
    elif char.disposition > 300:
        $ gm_dice = 95
        $ gm_disp_mult = 0.5
    elif char.disposition > 200:
        $ gm_dice = 90
        $ gm_disp_mult = 0.7
    elif char.disposition > 150:
        $ gm_dice = 90
        $ gm_disp_mult = 1
    elif char.disposition > 100:
        $ gm_dice = 70
        $ gm_disp_mult = 1
    elif char.disposition > 50:
        $ gm_dice = 50
        $ gm_disp_mult = 1
    elif char.disposition > 20:
        $ gm_dice = 20
        $ gm_disp_mult = 1
    elif char.disposition > -1:
        $ gm_dice = 5
        $ gm_disp_mult = 1
    else:
        $ gm_dice = 1
        $ gm_disp_mult = 1
    
    if dice(gm_dice) or check_lovers(char, hero):
        $ gm_last_success = True
        $ char.disposition += (randint(10, 30)*(gm_disp_mult))
    
    else:
        $ gm_last_success = False
        $ char.disposition -= (randint(10, 30)*(gm_disp_mult))
    
    if gm_last_success:
        $ char.override_portrait("portrait", "confident")
        $ hero.exp += randint(5, 10)
        if ct("Impersonal"):
            $rc("Yes?", "Is something wrong?", "Having your arms around me is so comfortable.", "You are... very warm...")
        elif ct("Shy") and dice(30):
            $ char.override_portrait("portrait", "shy")
            $rc("Hm... You are... very warm...", "I feel like I'm safe.", "Being so close...", "A... are you feeling cold? It's m... much warmer like this, right?", "It's... it's okay to do it like this, right?", "Y-yes… Please hold me… hold me tight…")
        elif ct("Nymphomaniac") and dice(20):
            $rc("Geez, you're such a perv♪", "Well, aren't you too close～♪", "Hau～... I'm...starting to feel funny...", "Being so close... Exciting?")
        elif ct("Frigid") and dice(20):
            $rc("H-Huh? Why is my pulse getting so...", "I-I'm not a body pillow...", "What are you nervous for? I'm the one who's embarrassed here.")
        elif ct("Kamidere"):
            $rc("Having your arms around me is so comfortable.", "When you're so gentle I get embarrassed all of a sudden...", "Did something happen?", "I'm for you to embrace.", "You can hear the sound of my heart beating.", "Would you please hug me tight.")
        elif ct("Kuudere"):
            $rc("...Jeez, how long are you going to do this? ...It's embarrassing.", "Oh...? This is nice, isn't it...? Being just like this.", "Hold me... Just do it!", "W-what are you doing so suddenly?!")
        elif ct("Dandere"):
            $rc("...My face is burning.", "Nn... Please hold me closer...", "It feels better this way.", "Nn… hold me…", "Ah… Hold me tighter…", "…come to me…", "Hmhmm… I expected perverted things... Pity…")
        elif ct("Tsundere"):
            $rc("Hey you, who said you could get this close without permission?", "D-don't do anything weird, okay...?", "I-I'm not n-nervous or anything...", "It's... it's okay to do it like this, right?", "How long do you plan to... It's embarassing!")
        elif ct("Imouto"):
            $rc("Okay, I'll comfort you…  There, there. ♪", "Hold me lots...", "<Hugs you back with a smile> Heheh ♪ Let's stay like this just a bit more. ♪", "*Squeeze!*", "What, what? Did something happen?", "Come, come! Come to my chest! ♪", "I-isn't something touching...?　R-really? ...Nn...", "Hehehe... It feels kinda warm...", "I feel like I'm safe.", "I wish you would hold me forever.")
        elif ct("Ane"):
            $rc("I wanted to stay together for a bit longer... just kidding...", "Hm? You're kind of close... Oh, so that's what this is all about...", "Fufu, you're like a spoiled kid...♪", "Come on, hold me tighter.", "There's no helping it. Only a little longer, got it?", "Hn… Yeah, alright, if it's just a hug…", "Heh... I never thought I'd be comforted by you...")
        elif ct("Yandere"):
            $rc("Mhmhm♪　Go ahead, come a little closer♪", "Nnh...more, squeeze me tighter...", "Ehehe, looks like you really calm down when I give you a rub-rub～♪", "Um... Don't hold out on me, okay...? Go a little harder...", "It's just a hug, but... It feels so nice♪", "I'm for you to embrace.")
        elif ct("Bokukko"):
            $rc("How's it feel, holding me...?", "Wha... What's this? Heartbeat?", "Doesn't this make you happy?", "mh～ Yeah. It really feels nice to embrace you～♪", "Geez, quit flailing around～. It's just a hug!", "Ah, hey... Fine, just a little...")
        else:
            $rc("There's no helping it, huh? Come to me.", "Whoa there... Are you all right? Hold onto me tightly.", "Just what I wanted! <Hugs you warmly>", "Can you hear my heartbeat too? ", "Don't worry about anything else… Come to me.", "Yes, you can hold me tighter if you wish.", "Let me melt in your arms...", "...mm, it feels good to be held like this. ♪", "<Hugs you tightly> What do you think? Can you feel me up against you?")

    else:
        $ char.override_portrait("portrait", "angry")
        if ct("Impersonal"):
            $rc("Please get off me, I can't breathe.", "<she moved back you as you tried to hug her>")
        elif ct("Shy") and dice(30):
            $rc("Ah... ah! W... what are you doing!?", "Please, leave me alone...", "W-w-w-what are you doing so suddenly?!")
        elif ct("Dandere"):
            $rc("...Please don't get so close.", "I won't let you.")
        elif ct("Kuudere"):
            $rc("I don't think so.", "I refuse.")
        elif ct("Ane"):
            $rc("[hero.name], I don't need comforting or anything....", "I'm sorry… I'm not really in the mood right now…", "You're making me uncomfortable.", "Sorry, but I don't want to.", "Please, keep your distance…")
        elif ct("Kamidere"):
            $rc("<Steps back> W...what are you... doing!?", "<Escapes your embrace> This... This is embarrassing after all… Stop it.", "I'm fine… so just leave me alone!", "S... Stop it. What else? This is embarrassing.")
        elif ct("Imouto"):
            $rc("Kya! He- hey, Let go of me...", "Huhuh, Not right now.", "No waay~!", "<slipped away from you> Hehe, you won't catch me ♪", "Uuu... I'm boooored! Let's do something else!")
        elif ct("Tsundere"):
            $rc("W-What's with you all of a sudden!?", "W-Why do we have to do that!?")
        elif ct("Bokukko"):
            $rc("Nice try.", "Kya! He-hey, let go of me!", "Wha-wha-what is this about?")
        elif ct("Yandere"):
            $rc("Hn... Let me go...", "Don't want to.", "I refuse.", "…stay…away.")
        else:
            $rc("<Steps back> Don't think so.", "! What are you doing all of a sudden!?", "[hero.name], you're too close, too clooose.", "Maybe later.", "That's no good.", "No, cut it out!", "<Shrinks back> Don't get weird.", "What are you doing! Please don't bother me!", "I'm not in the mood.")    
    $ char.restore_portrait()
    $ del gm_last_success
    $ del gm_dice
    $ del gm_disp_mult
    jump girl_interactions
    

    

###### j3    
label interactions_slapbutt:
    "You try to slap her butt."
    $ interactions_check_for_bad_stuff(char)
    if char.disposition > 600:
        $ gm_dice = 98
        $ gm_disp_mult = 0.2
    elif char.disposition > 500:
        $ gm_dice = 98
        $ gm_disp_mult = 0.4
    elif char.disposition > 400:
        $ gm_dice = 95
        $ gm_disp_mult = 0.6
    elif char.disposition > 350:
        $ gm_dice = 90
        $ gm_disp_mult = 1
    elif char.disposition > 300:
        $ gm_dice = 70
        $ gm_disp_mult = 1
    elif char.disposition > 200:
        $ gm_dice = 50
        $ gm_disp_mult = 1
    elif char.disposition > 100:
        $ gm_dice = 40
        $ gm_disp_mult = 1
    elif char.disposition > 50:
        $ gm_dice = 20
        $ gm_disp_mult = 1
    elif char.disposition > -1:
        $ gm_dice = 15
        $ gm_disp_mult = 1        
    else:
        $ gm_dice = 1
        $ gm_disp_mult = 1
    
    if "Lesbian" in char.traits: 
        $ gm_dice = 0
    
    if dice(gm_dice) or check_lovers(char, hero):
        $ gm_last_success = True
        $ char.disposition += (randint(7, 20)*(gm_disp_mult))
    
    else:
        $ gm_last_success = False
        $ char.disposition -= (randint(10, 20)*(gm_disp_mult))
    
    if gm_last_success:
        $ char.override_portrait("portrait", "confident")
        $ hero.exp += randint(5, 10)
        if ct("Yandere"):
            $rc("<She smiles and slaps you back.>", "Ha... That touching... so lewd...", "How lewd...", "Blossoming youth?", "Such a perverted hand...")
        elif ct("Impersonal"):
            $rc("Aah... my hips... it feels... kind of strange.", "Hnn, fuaah... if you touch there, I won't be able to hold myself back...")
        elif ct("Nymphomaniac") and dice(20):
            $rc("...Alright, any lower and I'll have to charge extra.", "Hehehe, I just got a bit horny...", "That... Ahh... Hehe... So perverted...", "Ahh... You made me cum a little.", "You're lewd～♪", "Ahaha, you're pervy～♪", "If you keep touching me, I'll touch you back~")
        elif ct("Shy") and dice(30):
            $ char.override_portrait("portrait", "shy")
            $rc("Aauh… Wh-what's up...?", "Nwa, Y-you surprised me...", "Umm... I get nervous when others touch me.", "U-uhm… touch me gently, please…", "Umm.. Do you like... my butt?")
        elif ct("Kamidere"):
            $rc("Wha! D-don't be such a perv when you touch me~", "Hyaa! G-Geez! Don't do that out of the blue.", "You can touch me just a bit... Just a bit, got it?", "Hn, ah… If you touch like that, it's sort of perverse…", "Hmm, don't tell me... you're horny?", "Hn… How is it? Have I got a tasty ass?", "Ahn... It looks like I've found someone with perverted hands.")
        elif ct("Kuudere"):
            $rc("Kyah!? You touched me someplace weird, that's why...!", "Kuh... Why do I feel so...", "...I don't mind if it's you.")
        elif ct("Dandere"):
            $rc("If it wasn't you I'd have filed a city guards report.", "...I feel aroused.", "Nn?! This is just... a physiological reaction...", "Nnn... Somehow, my body is getting hotter...")
        elif ct("Tsundere"):
            $rc("Kuh... This is so humiliating, so disgraceful... But I...", "Hhmn... My-My... you love my body so much? Of course you do, it can't be helped.", "Ah! Y-y-you idiot... D...don't do that!")
        elif ct("Bokukko"):
            $rc("What's that, that's sneaky!", "Hyah! Ugh, you caught me…", "Hm? If you do that, I'll treat you roughly too~", "...That's it? You're not going any further?", "Hey, c'mon... don't go touching me anywhere weird... Ah!")
        elif ct("Imouto"):
            $rc("Hyaa! T-that tickles...!", "So lewd...Uhuhuhuhu... ♪", "Hu? Why you are touching me there~?", "Uh, I'm spoiled, huh? Ehehe... I... like it.. Ahh…")
        elif ct("Ane"):
            $rc("Hmhm, don't feel like you have to hold back, hey?", "Hmhm, are you getting turned on?", "Your appetite for lust is proof of your health.")
        else:
            $rc("Hya! If you keep doing that, Hnn! I'll get in the mood…", "Geez, you're hopeless.", "Even if you touch me, nothing interesting is going to happen.", "Teasing people isn't good, you know~", "*giggle* How troublesome ♪", "Such a surprise attack is not fair!", "Kya…  Doing this all of sudden, that surprised me.", "So pushy…  Are you proposing or something?", "Is touching me really that fun? I don't really get it... but if you're enjoying it, then sure, I guess.", "Whoa... We're energetic, aren't we...", "Hya! S-such shameful hands... hnn") 

    else:
        $ char.override_portrait("portrait", "angry")
        if ct("Yandere"):
            $rc("Hey, it hurts! Stop it!", "Touching is forbidden~ That hand, don't blame me if it falls off.", "You have some nerve putting your hands on me!", "Could you refrain from touching me with your dirty hands?", "It looks like you are in dire need of punishment...")
        elif ct("Impersonal"):
            $rc("I see you lack common sense.", "How about you stop your pointless struggling?", "It hurts.", "Why are you touching me? So annoying.", "No... don't touch my butt...", "Hate it...", "...I'll hit you.")
        elif ct("Shy") and dice(30):
            $rc("No... D-don't... Do that!", "W-w-what? D-don't do it please...", "Wah! Th-That scared me!", "That hurts...", "I think you shouldn't do p-perverted things..", "P-please stop doing this!")
        elif ct("Dandere"):
            $rc("...Please do not do it again.", "No... I have had enough for today.", "...Don't touch me.")
        elif ct("Tsundere"):
            $rc("Y-you dumbass! You pervert!", "Quit. That. Riiiight. Nooooooow!", "Hey, you creep, what do you think you're doing!?", "Aah! C...cut it out!")
        elif ct("Kuudere"):
            $rc("Show some restraint with your indecent actions.", "...Tch.", "Hmph. You should be grateful I'm so lenient today.", "Come on, it tickles.", "What what? Sexual harrasment? Is that okay?")
        elif ct("Ane"):
            $rc("You're too lustful. Consider a bit more self-restraint, okay?", "Come now, don't touch anywhere inappropriate.", "I'm gonna scold you if you continue.")
        elif ct("Kamidere"):
            $rc("D-don't be touching anywhere weird!", "What are you doing, geez~!", "Don't touch me in weird places!", "Hyauu! Hey! Nn, sexual harassment is not allowed!", "Hnyaah! Geez, don't grab me in weird places!", "Hnn, Geez, lay off my butt. ","S-stop that! Despicable!", "Hya! Stop acting like a pervert!", "Geez, stop that!")
        elif ct("Bokukko"):
            $rc("Umm... Don't go touchin' me...", "Da heck ya' doing?", "Wha~t? It hurts~", "You better stop that... got it?", "Owwie… Geez... why'd you do that..?", "Whoa, What're you doing, geez…", "Fweh, hey, don't grab that~!", "What the hell!?", "Fugaa, What are you doin'!?", "Hey! Where are you aiming?")
        elif ct("Imouto"):
            $rc("Nooo, What are you doing!?", "Hya! Don't touch me there!", "*sob* that hurts...", "O-owowowowow! Sto-, Wai-, AGYAAA!!", "P-Pervert! Pervert!! Help!", "Perv!")
        else:
            $rc("...Hey! Why are you touching me!", "Why are you touching me without permission!?", "Geez! If you don't stop, I'm gonna get mad!", "Geez! If you don't stop, I'll get angry.", "Whoa! Hey, don't just touch me out of the blue!", "Aahn! Stop it!", "Ow! How dare you!", "Hey~! Stop that~!", "[hero.name]...! I'd rather you do this sort of thing with someone else...!", "If you have the free time to be doing that, I'm leaving.", "What? Don't touch me that much.", "Hey! Quit it, already!", "Aah! C...cut it out! ","What are you doing over there, you sneak?", "Kyaa-! Y... you idiot!", "What?! What is the meaning of this? Hey!", "Hmph, how unromantic! Know some shame!", "Don't touch me.", "What are you doing, weirdo???", "Don't anger me...", "Jeez～, gimme a break already～...")   
    $ char.restore_portrait()
    $ del gm_last_success
    $ del gm_dice
    $ del gm_disp_mult
    jump girl_interactions
    

###### j4
label interactions_grabbreasts:
    "You try to grab her breasts."
    $ interactions_check_for_bad_stuff(char)
    if char.disposition > 700:
        $ gm_dice = 98
        $ gm_disp_mult = 0.2
    elif char.disposition > 650:
        $ gm_dice = 98
        $ gm_disp_mult = 0.4
    elif char.disposition > 600:
        $ gm_dice = 95
        $ gm_disp_mult = 0.5
    elif char.disposition > 550:
        $ gm_dice = 90
        $ gm_disp_mult = 0.7
    elif char.disposition > 500:
        $ gm_dice = 80
        $ gm_disp_mult = 1
    elif char.disposition > 450:
        $ gm_dice = 70
        $ gm_disp_mult = 1
    elif char.disposition > 350:
        $ gm_dice = 30
        $ gm_disp_mult = 1       
    elif char.disposition > 300:
        $ gm_dice = 20
        $ gm_disp_mult = 1
    elif char.disposition > 150:
        $ gm_dice = 5
        $ gm_disp_mult = 1
    else:
        $ gm_dice = 1
        $ gm_disp_mult = 1

    if "Lesbian" in char.traits: 
        $ gm_dice = 0

    if dice(gm_dice) or check_lovers(char, hero):
        $ gm_last_success = True
        $ char.disposition += (randint(13, 30)*(gm_disp_mult))
    else:
        $ gm_last_success = False
        $ char.disposition -= (randint(15, 60)*(gm_disp_mult))
    
    if gm_last_success:
        $ char.override_portrait("portrait", "shy")
        $ hero.exp += randint(5, 10)
        if ct("Impersonal"):
            $rc("This is...unexpectedly embarrassing.", "...Do you like my tits?", "You're rubbing my nipples.", "Uh... my chest, it feels so tight...", "Hnn, no matter how hard you squeeze, nothing will come out, auh.", "Hnn, you don't need to rub so hard...", "Can't control yourself?")
        elif ct("Half-Sister") and dice(30):
            $rc("Ah... tell me... what do you think about your sister's body...?", "It's... it's wrong to lust for your sister....", "A-are you getting excited over your sister's body?", "I wonder... if you should proceed to do this... to your sister?")
        elif ct("Shy") and dice(25):
            $rc("Ah... your hand is so gentle...", "When I get touched so much, [hero.name], I get confused...", "Aah... N...no... If you do it like that…I...", "P... please be more... gentle...", "Y-yes... You can.. like this...")
        elif ct("Dandere"):
            $rc("Nn... Right there...is good...", "Nh... Harder...", "I love when you slowly rub my breasts.", "Aah... t...this is also... a form of massage... aaah...", "Ah! Jeez, why does everyone go for my breasts!?", "Kya!? Don't...grope them... Ah...", "Hnn, is my chest... soft...?", "M...more... my body... feels so hot...", "This is good...", "Becoming... more perverted... by the minute...", "Hn… You shouldn't grope people.", "Ah. Feels much better than rubbing myself...", "My nipples are tingling... Feels... Weird...")
        elif ct("Kuudere"):
            $rc("Ah... You've got some nerve, grabbing me like that all of a sudden...", "Nn!? Don't, pinch...! ...Ahn!", "Ngh... These things just get in the way...", "Nn...mm... Are you...trying to make them bigger...?")
        elif ct("Tsundere"):
            $rc("Eh? You like me? But of course. Well, I don't exactly dislike you, myself. Hey! Not there... Don't be so pushy. You can't...", "Nnnaaah! Stop being so rough, you dummy...!", "Kyauu! You dummy! Stop pulling on them!", "N...no... I...I don't feel a thing at all.")
        elif ct("Imouto"):
            $rc("Hnn… Uhuhu, If you want to rub them, then just go for it. ♪", "Huh... My nipples are getting harder and harder...?", "Aah... I want you to touch it more, wauu, more, ah, more…", "Eh! Huhu ♪ My nipples are getting harder, can you tell?", "...What is it? Are my breasts working you up? ♪", "J-Just for a little bit, okay?", "Hya! N-no, stop. ♪ Hahya, please, stop. ♪", "Haha, that tickles ♪")
        elif ct("Kamidere"):
            $rc("Nhaa, nn, wait, my bra just came undone...", "Uah, don't just run up and touch them… Hnn, how long are you… Hauu…", "Hnn, ah, wait, what are you… Oh Geez, just do whatever you want! <resigned>", "Do you... like my breasts...that much?", "Who'd have thought it would feel so good from just breast-fondling...", "Uwah, that is a really perverted face, you know? Ahaha, that's so cute~♪", "Hnnn, I know, aauh, that my breasts are incredible, but... haaa…", "Huhu, I like that perverted side of you ♪", "My tits feel great, don't they?", "Ah... Right there, keep your hands there...")
        elif ct("Bokukko"):
            $rc("Oh~ this is nice... my body, feels, light?", "Ah... That's crafty of ya...", "Hyaa, Hnn, Geez, my bra will slip off.", "It feels good here, doesn't it?", "Fuwaah!? Don't ask me, they just got big on their own!", "Ehehe, I'm all sticky...♪", "Ahaha, you're pervy～♪", "Kya! Geez... If you're gonna play with it, be gentle... Hauu...♪")
        elif ct("Ane"):
            $rc("Mm... You're considerably skilled.　Ah...oh yes, please, over there too...", "Be as spoiled as you like. I'll accept all of it...", "Nnh, how do I feel, hmm?", "There... When you fondle gently, it feels really good...", "Nn... I want to be touched by you...", "Ah... please keep rubbing me like that...", "Gently rubbing me like this... It's very good.", "When you play with my breasts like that my body feels so light." ,"Yes, like that. Be gentle with them...")
        elif ct("Yandere"):
            $rc("Mmh, little to the left... Ahyes, yes, right there, oh god...", "Hyah! Ahn... please, spare me from this lewdness～", "Ah... Wait! When did you...?")
        else:
            $rc("Nnn… It's okay to rub it just a little.", "Mm~ Being touched every now and then isn't so bad, I guess?", "...You're surprisingly bold. I like that", "Kya, Hnn, Geez~, you've got such perverted hands!", "Hmm, *moan*, phew... It feels good, even over the clothes…", "My soft tits feel good, don't they?", "Oh my~ You're even touching there!?", "Ah... fondle my breasts...", "You like my breasts, don't you?", "Y... Yes... Continue massaging...like that.", "Aah... my chest... it feels so good.", "No... This is no good... Ahhh... Doing a thing like this... But... I…", "I... Ah… Do you like my boobs...?", "Ahhh, that feels so good.", "Hnnn, you've got... some naughty hands... uhn!", "Hnn, you don't need to rub so hard...", "With this... my breasts... are very easy to stimulate...", "Rubbing my tits... I love this!", "It feels good... m...my nipples... What you did just now felt so good!", "You're pretty damn good... ", "This feeling... from your massage... is so good.", "God you are such a perve! <Smiles>", "Aahhh... you can do it harder if you want～") 

    else:
        $ char.override_portrait("portrait", "angry")
        if ct("Yandere"):
            $rc("Hey, it hurts! Stop it!", "How filthy.", "How... dare you...", "No, don't touch...")
        elif ct("Impersonal"):
            $rc("Don't touch.", "You're damaging the shape of my breasts.", "You shouldn't grope people.")
        elif ct("Half-Sister") and dice(25):
            $rc("You're a no good brother to be doing it with your sister.")
        elif ct("Shy") and dice(20):
            $rc("N... no... s...stop... p... please stop...", "Wait... aren't you overdoing it?", "Ugh... what... w...w-w-wwhat are you doing!?", "*sob* Why you are so mean...", "NO! D-don't do that!", "N-no, you can't, that's too p-perverted...")
        elif ct("Kuudere"):
            $rc("...! Who told you you could touch me there!?", "No, cut it out!", "Nn...Where in the world are you touching? Jeez...!", "Geez! Don't touch them!", "Wha-... What? Aah... Wai-... Idiot! Stop it!")
        elif ct("Dandere"):
            $rc("Ugh... not there...", "...not good.", "...not allowed.", "Eh? W-, ah, wait, that's too fast! Uwaa!", "Nya! Don't rub right there! Don't be mean...")
        elif ct("Tsundere"):
            $rc("Kyaa-! Y... you idiot!", "Hii~! Hey, what do you think you're grabbing at?!", "Kya! W-what are you doing!?", "Wha!? N-no! Why would I enjoy it!?", "G-geez... NOW I'm angry!", "That's terrible! You beast! Pervert! Idiot!")
        elif ct("Ane"):
            $rc("Stop. I feel ill.", "That's sexual harassment, you know?", "If you grasp them so rough they'll lose shape.", "Auh! Uuh, my boobs aren't for rubbing, Hyauh! Geez, stop it, hnaaah!", "This is a bit too daring…", "I think you have gone a bit too far...", "W-Wait, here is a bit... Please hold back for now.", "Please! Don't touch me!", "Don't be so perverted!", "Stop it please! I don't want this.")
        elif ct("Bokukko"):
            $rc("Hey! Where do ya think you're touching, you pervert!", "Whoah, wait! Where are you touching me?", "Hya! ...What are you, a molester!?", "What?! You dumbass, what are you doing?!", "Hey! Don't be such a dick.", "W-wait, not there, hnn, hey, you're going too far...")
        elif ct("Imouto"):
            $rc("Kyaa! Geez! Help! There's a lewd molester here~!", "Oww..! You've made me mad..!", "Hyauuu! Noo, youuu, boob freak!", "Ueh. Hey, get away from me~", "Jeez, don't be doing lewd stuff, okay?", "Whoa, what're you trying to do")
        elif ct("Kamidere"):
            $rc("What an idiot. What do you mean by 'Oops'?", "How dare you?! Know your place your filthy piece of trash!", "Piss off you fucktard!", "<jumps away> Ha! Like I'll ever let a loser like you touch me.", "Huhuhuh… I wonder how warm it would be to bathe in your blood...?")
        else:
            $rc("You certainly have courage, asshole!", "The hell!?", "Hey! I won't let you touch me that easily.", "You graceless swine! Can you not calm down a little?", "<steps back> Wow. No need to hurry like that.", "Huh? Stop it! Where are you touching!?", "<Screams> What are you doing!!! They are not an invitation, asshole!", "Hey! Where are those hands of yours going?", "<Angrily> Don't touch me, asshole!", "You're... terrible! Must you do such a thing!", "Don't ever think about it!", "What are you trying to...?! To hell with you!", "You filthy pig! Who gave you permission to touch me?!")   
    $ char.restore_portrait()
    $ del gm_last_success
    $ del gm_dice
    $ del gm_disp_mult
    jump girl_interactions
    
