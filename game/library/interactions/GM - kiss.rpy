label interactions_kiss:
    "You trying to kiss her."
    if ct("Lesbian"): 
        call interactions_lesbian_refuse_because_of_gender
        jump girl_interactions
    $ interactions_check_for_bad_stuff(char)
    $ interactions_check_for_minor_bad_stuff(char)
    if char.disposition > 700:
        $ gm_dice = 98
        $ gm_disp_mult = 0.2
    elif char.disposition > 650:
        $ gm_dice = 95
        $ gm_disp_mult = 0.3
    elif char.disposition > 600:
        $ gm_dice = 95
        $ gm_disp_mult = 0.5
    elif char.disposition > 550:
        $ gm_dice = 95
        $ gm_disp_mult = 0.6  
    elif char.disposition > 500:
        $ gm_dice = 90
        $ gm_disp_mult = 0.8
    elif char.disposition > 450:
        $ gm_dice = 85
        $ gm_disp_mult = 1
    elif char.disposition > 400:
        $ gm_dice = 70
        $ gm_disp_mult = 1
    elif char.disposition > 300:
        $ gm_dice = 30
        $ gm_disp_mult = 1
    elif char.disposition > 250:
        $ gm_dice = 15
        $ gm_disp_mult = 1
    elif char.disposition > 200:
        $ gm_dice = 5
        $ gm_disp_mult = 1
    else:
        $ gm_dice = 1
        $ gm_disp_mult = 1


    if (dice(gm_dice) and check_friends(char, hero)) or check_lovers(char, hero):
        $ gm_last_success = True
        $ char.disposition += (randint(20, 40)*(gm_disp_mult))
    else:
        $ gm_last_success = False
        $ char.disposition -= (randint(25, 45)*(gm_disp_mult))
    
    if gm_last_success:
        if char.disposition < 250: # a placeholder to save lines, better checks will be needed
            "You and [char.name] make out for a while."
        elif char.disposition < 500:
            "You kiss deeply and passionately.."
        elif char.disposition < 750:
            "She's really getting into it, there's some heavy tongue action."
        else:
            "She's all over you, kissing all over your face and grinding against you."
        $ hero.exp += randint(3, 10)
        $ char.exp += randint(3, 10)
        $ char.override_portrait("portrait", "shy")
        if ct("Half-Sister") and dice(40):
            if ct("Dandere", "Impersonal", "Yandere"):
                $rc("*kiss*")
            elif ct("Shy") and dice(30):
                $rc("*kiss* Do you like... kissing... your sister?", "*kiss* B-brother, you're so gentle...")
            if ct("Imouto"):
                $rc("*kiss* I want to keep kissing you, brother! ♪", "This whole time, brother... wanted to... kiss me! ♪")
            elif ct("Kamidere"):
                $rc("*kiss* I'm kissing with my brother... T...this is just wrong.", "Such an act... kissing... my brother...")
            elif ct("Tsundere"):
                $rc("*kiss* D...doing such lewd things even though we're siblings... Isn't this incest?", "*kiss* Ah... Your sister... can't control herself.")
            elif ct("Kuudere"):
                $rc("I'm kissing my brother like this... I'll never be forgiven for doing this...", "*kiss* This is different from the kisses we had when we were little...")
            elif ct("Ane"):
                $rc("*kiss* Brother, you taste so good! ♪", "You really like my lips, brother? ♪")
            elif ct("Bokukko"):
                $rc("*kiss* What's it like to kiss your sister? Tastes good, doesn't it?")
            else:
                $rc("*kiss* Isn't it a bit strange to kiss your sister?", "*kiss* It's okay for siblings to kiss, isn't it?")
        elif ct("Yandere"):
            $rc("... *kiss*", "*kiss* *slurp* *slosh* <She's making patterns with her tongue>", "*kiss* ... *giggle* *kiss*", "momph *kiss* dufu *kiss* gae *kiss* mnn... <Trying to talk, perhaps?>", "...Haah... It tastes like you... Hehe ♪", "Huff, *smooch*, *slurp*... Hehe, I got my tongue inside...")    
        elif ct("Impersonal"):
            $rc("*kiss* Kissing is nothing that special.", "*kiss* My body's getting hotter.", "*kiss*... Hn... I can still taste you.", "Your lips look a little dry... *lick lick lick* That's much better.")
        elif ct("Shy") and dice(30):
            $rc("Huh... *kiss*... We k-kissed...", "*kiss*  We... kissed... <gives you a dreamy smile>", "Ahm, *slurp, kiss*......kissing feels good...", "*kiss* Nnn... <looks at you dreamily>", "<Gently kisses you> H...how's this? Does it f... feel good...? It... it feels good for me...", "*kiss* ...Did I do that right...?", "Is this really ok...? ...*kiss*...", "<closes her eyes> *kiss* hn...")
        elif ct("Nymphomaniac") and dice(25):
            $rc("Mmmf ♪　Nnh, nnf, mmmf... No, we're gonna kiss more ♪ ...nnf, mmmf♪", "This isn't going to end with just a kiss, right?", "*kiss* Even though we're just kissing... I'm already...")
        elif ct("Dandere"):
            $rc("*kiss* ...Not enough. More.", "Nn, aah, haah... You're tickling my tongue...", "*kiss*... *smooch*... *huff*... your breath... so hot...", "Do you desire my lips? *kiss*", "*kiss*...  Hn... you like kissing...?")
        elif ct("Kuudere"):
            $rc("Ok, but don't go overboard. *kiss*", "*kiss* How about at least trying to look a bit happier?", "Nhn... Ah... Do you like my kisses?", "Nh...chu...nnhu...chu... Nhn...chu... Y-you're overdoing it, idiot...", "I-I suppose we can... *kiss*", "*kiss* Ah... J-Jeez, that was too sudden...", "Mmmh, nn, chu, mmchu, nn... Hoh is id, my kish? Nmu, nn, chupuru... nfuu ♪", "Mmh... Nmmh?! You bit my lips! Geez!")
        elif ct("Tsundere"):
            $rc("*kiss* !? Wh-what do you think you're doing all of a sudden...? Geez.", "Nnn, nn... Ah... Done already...? !? I-I didn't say anything!", "Nnh, mmm, nyuu, nnnh! I won't lose! mmf, aumph, mph, mph, mph, mmf... Pfaah! How was that? ♪", "*kiss*, hn, hnn... Puah! Geez! How long are you planning on doing that?!", "*kiss*, *lick*... Hn aah... Geez, too much tongue!", "Hn *kiss*... hnn... Y-you're embarrassing me, geez...", "*kiss* ... Geez! Who told you it was ok to kiss!", "*smooch*, hnn... I don't want, *kiss*, you to, *slurp*, let me go...", "Mmh, chu, nnh... mmmhah!　Jeez, how long are you gonna do this for!")
        elif ct("Ane"):
            $rc("...Hmhm, there's a kiss mark on you.", "*kiss* ...Hmhm, you're pretty good.", "*kiss* Kissing is a token of my affection...", "*kiss*...Hn... Just having our lips touch like this... makes me so excited.", "*kiss* My heart just beat faster for a bit.", "*kiss* That was a wonderful kiss.", "*kiss* Well now, it was a pleasant experience ♪", "*kiss*... My, you are a good kisser!")
        elif ct("Bokukko"):
            $rc("*kiss*... What, what? You like kissing me that much?", "Haa, *kiss*, *smooch*, hnm, Puaah! ...haa haa, I totally forgot, to breathe, haaa...", "*kiss*... Hm...? What did you eat today...?", "*smooch*... Hm, if you can lick, so can I...", "*Kiss* I wonder, was it good?", "*kiss* You're skilful, aren't ya?", "*kiss*... Mmmph, nn, mmh, chu, so lewd, geez...")
        elif ct("Imouto"):
            $rc("*smooch* Ehehe, that's a bit embarrassing ♪", "*smooch*, ahm, *lick*... My tongue moved by itself...", "*kiss*, hn... *slurp*, *kiss*... Ehehe♪ My tongue, it feels good right ♪", "*kiss* Hnn, you're not going to use your tongue? Huhu ♪", "*lick, kiss*... *lick*, hn...  I licked you a lot.. ♪", "*smooch* Hehe, we kissed ♪", "Hn, *kiss*... Haa... Your breath is tickling me...", "Ehehe, kiss time ♪ *kiss*", "Mhm, nnh, chu, hmm...nnh, mmh... Puah!　Gosh, I'm out of breath...")
        elif ct("Kamidere"):
            $rc("*kiss*... Felt good, right?", "*smooch*... Getting excited?", "*kiss*... I'll leave you with that much.", "Hn, *smoooch*...  Uhuh, now you've got a hickey ♪", "*Kiss*... Haha, why's your face getting so red ♪", "I, too, can be sweet sometimes... *kiss*, ahm... *smooch*...")
        else:
            $rc("Don't say anything.... *kiss*", "*kiss*, *lick*, I like, *kiss*, this...", "*kiss*, hmm... *sigh*, kissing feels so good...", "*kiss*...  My heart's racing ♪", "Hmm... *kiss, kiss*, ahm,.. I like... kissing... Hn, *smooch*...", "*slurp, kiss* Kissing this rough... feels so good.", "*kiss* hmm...Where did you learn to kiss like this?", "*kiss* You're sweet...", "Ahm... *kiss, lick*... nnn... Do you think touching tongues is a little... sexy?") 
    else:
        if ct("Impersonal"):
            $rc("I see no possible benefit in doing that with you so I will have to decline.", "Denied. Please refrain from this in the future.")
        elif ct("Shy") and dice(50):
            $rc("I... I don't want! ", "W-we can't do that. ", "I-I don't want to... Sorry.")
        elif ct("Imouto"):
            $rc("Noooo way!", "...I-I'm gonna get mad if you that that stuff, you know? Jeez!", "Y-you dummy! Stay away!") 
        elif ct("Dandere"):
            $rc("You're no good...", "You should really settle down.")
        elif ct("Tsundere"):
            $rc("I'm afraid I must inform you of your utter lack of common sense. Hmph!", "You are so... disgusting!", "You pervy little scamp! Not in a million years!")
        elif ct("Kuudere"):
            $rc("...Perv.", "...Looks like I'll have to teach you about this little thing called reality.", "O-of course the answer is no!")
        elif ct("Kamidere"):
            $rc("Wh-who do you think you are!?", "W-what? Of course I'm against that!", "The meaning of 'not knowing your place' must be referring to this, eh...?")
        elif ct("Bokukko"):
            $rc("He- Hey, Settle down a bit, okay?", "You should keep it in your pants, okay?", "Hmph! Well no duh!")
        elif ct("Ane"):
            $rc("If I was interested in that sort of thing I might, but unfortunately...", "No. I have decided that it would not be appropriate.", "I don't think our relationship has progressed to that point yet.", "I think that you are being way too aggressive.")
        elif ct("Yandere"):
            $rc("I've never met someone who knew so little about how pathetic they are.", "...I'll thank you to turn those despicable eyes away from me.", "What? Is that your dying wish? You want to die?")
        else:
            $rc("No! Absolutely NOT!", "With you? Don't make me laugh.", "Get lost, pervert!", "Woah, hold on there. Maybe after we get to know each other better.")  
    $ char.restore_portrait()
    $ del gm_dice
    $ del gm_disp_mult
    jump girl_interactions
    
