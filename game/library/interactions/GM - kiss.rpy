label interactions_kiss:
    if ct("Lesbian") and not "Yuri Expert" in hero.traits:
        $ m = interactions_flag_count_checker(char, "flag_interactions_kiss_lesbian_refuses")
        if m > 2:
            call interactions_too_many_lines
            $ char.disposition -= randint(4, m+6)
            $ char.joy -= randint(0,1)
            $ del m
            jump girl_interactions
        else:
            call interactions_lesbian_refuse_because_of_gender
            jump girl_interactions
        
    $ interactions_check_for_bad_stuff(char)
    $ interactions_check_for_minor_bad_stuff(char)
    $ m = interactions_flag_count_checker(char, "flag_interactions_kiss")
    if ct("Nymphomaniac") or check_lovers(char, hero):
        $ n = 1
    elif (ct("Half-Sister") and char.disposition < 500 and "Sister Lover" not in hero.traits) or ct("Frigid"):
        $ n = -1
    else:
        $ n = 0
    
    if m > (randint(2,3)+n):
        call interactions_too_many_sex_lines
        $ char.disposition -= randint(4, m+5)
        if char.joy>30:
            $ char.joy -= randint(2,4)
        $ del m
        $ del n
        jump girl_interactions
    
    if check_lovers(char, hero):
        $ temp = 0.6
    elif check_friends(char, hero):
        $ temp = 0.2
    else:
        $ temp = 0.15

    $ sub = check_submissivity(char)
    
    if char.disposition > (350+50*sub) and dice((char.disposition-100*sub)*temp + (hero.charisma*0.1) - 10*m):
        $ result = round(randint(20, 35)+ char.joy*0.06 - m*4 - char.disposition*0.01)
        if result <= 0:
            $ result = rendint(1,2)
        $ hero.exp += randint(10, 20)
        $ char.exp += randint(10, 20)
        $ char.disposition += result
        $ del temp
        $ del m
        $ del sub
        
        $ char.override_portrait("portrait", "shy")
        $ char.show_portrait_overlay("love", "reset")
        
        if check_lovers(char, hero):
            char.say "Your hands slide down her body as your lips press hers."
        elif char.disposition < (300+n*100):
            char.say "Your lips gently slide across hers."
        elif char.disposition < (500+n*100):
            char.say "You two kiss deeply and passionately."
        else:
            char.say "You two kiss deeply and passionately. Her tongue dances around yours."

        if ct("Half-Sister") and not(check_lovers(char, hero)) and char.disposition < (500+n*100) and not "Sister Lover" in hero.traits:
            "She looks a bit uncomfortable."
            if ct("Impersonal"):
                $ rc("It's okay for siblings to kiss, isn't it?", "Do you like your sister's kisses?")
            elif ct("Yandere"):
                $ rc("Such an act... kissing... my [hero.hs]...", "I wonder... if you should proceed to do this... to your sister?")
            elif ct("Dandere"):
                $ rc("This is different from the kisses we had when we were little...", "...[hero.hs], you taste pretty good.")
            elif ct("Shy") and dice(50):
                $ rc("Do you like... kissing... your sister?", "[hero.hs], you're so gentle...")
            if ct("Imouto"):
                $ rc("I want to keep kissing you, [hero.hss]! Hehe ♪", "How does it taste to kiss your sister?")
            elif ct("Kamidere"):
                $ rc("I'm kissing with my [hero.hs]... T...this is just wrong...", "You love your sister that much..?")
            elif ct("Tsundere"):
                $ rc("D...doing such lewd things even though we're siblings... Isn't this incest?", "Doing such things to your sister... *sigh* Well, it can't be helped...")
            elif ct("Kuudere"):
                $ rc("I'm kissing my [hero.hs] like this... I'll never be forgiven for doing this...", "Ugh... I... I can't believe I have such a lewd [hero.hs]...")
            elif ct("Ane"):
                $ rc("You really like my lips, [hero.hs]? ♪", "Do you really like kissing your sis that much?")
            elif ct("Bokukko"):
                $ rc("What's it like to kiss your sister? Does it taste good?", "Going after your sister? Man, what a hopeless [hero.hs] you are... ♪")
            else:
                $ rc("Isn't it a bit strange to kiss your sister?", "I'm your sis... Are you really okay with that?")
        
        elif ct("Yandere"):
            $ rc("*kiss* *slurp* *slosh* <[char.p]'s making patterns with her tongue>", "*kiss* ... *giggle* *kiss*", "momph *kiss* dufu *kiss* gae *kiss* mnn... <trying to talk, perhaps?>", "...Haah... It tastes like you... Hehe ♪", "Huff, *smooch*, *slurp*... Hehe, I got my tongue inside...")    
        elif ct("Impersonal"):
            $ rc("*kiss* Kissing is nothing that special.", "*kiss* My body's getting hotter.", "*kiss*... Hn... I can still taste you.", "*kiss* Your lips feel a little dry... *lick lick lick* That's much better.")
        elif ct("Shy") and dice(50):
            $ rc("Huh... *kiss*... We k-kissed...", "*kiss*  We... kissed... <gives you a dreamy smile>", "Ahm, *slurp, kiss*......kissing feels good...", "*kiss* Nnn... <looks at you dreamily>", "<Gently kisses you> H...how's this? Does it f... feel good...? It... it feels good for me...", "*kiss* ...Did I do that right...?", "Is this really ok...? ...*kiss*...", "<closes her eyes> *kiss* hn...")
        elif ct("Nymphomaniac") and dice(35):
            $ rc("*kiss* Mmmf ♪　Nnh, nnf, mmmf... No, we're gonna kiss more ♪ ...nnf, mmmf♪", "*kiss* This isn't going to end with just a kiss, right?", "*kiss* Even though we're just kissing... I'm already...")
        elif ct("Dandere"):
            $ rc("*kiss* ...Where did you learn to kiss like this?", "*kiss* ...Not enough. More.", "Nn, aah, haah... You're tickling my tongue...", "*kiss*... *smooch*... *huff*... your breath... so hot...", "Do you desire my lips? *kiss*", "*kiss*...  Hn... you like kissing...?")
        elif ct("Kuudere"):
            $ rc("Ok, but don't go overboard. *kiss*", "Nhn... Ah... Do you like my kisses?", "Nh...chu...nnhu...chu... Nhn...chu... Y-you're overdoing it, idiot...", "I-I suppose we can... *kiss*", "*kiss* Ah... J-Jeez, that was too sudden...", "Mmmh, nn, chu, mmchu, nn... Hoh is id, my kish? Nmu, nn, chupuru... nfuu ♪", "Mmh... Nmmh?! You bit my lips! Geez!")
        elif ct("Tsundere"):
            $ rc("*kiss* !? Wh-what do you think you're doing all of a sudden...? Geez.", "Nnn, nn... Ah... Done already...? !? I-I didn't say anything!", "*kiss*, hn, hnn... Puah! Geez! How long are you planning on doing that?!", "*kiss*, *lick*... Hn aah... Geez, too much tongue!", "Hn *kiss*... hnn... Y-you're embarrassing me, geez...", "*kiss* ... Geez! Who told you it was ok to kiss!", "*smooch*, hnn... I don't want, *kiss*, you to, *slurp*, let me go...", "Mmh, chu, nnh... mmmhah!　Jeez, how long are you gonna do this for!")
        elif ct("Ane"):
            $ rc("*kiss* ...Hmhm, there's a kiss mark on you.", "*kiss* ...Hmhm, you're pretty good.", "*kiss* Kissing is a token of my affection...", "*kiss*...Hn... Just having our lips touch like this... makes me so excited.", "*kiss* My heart just beat faster for a bit.", "*kiss* That was a wonderful kiss.", "*kiss* Well now, it was a pleasant experience ♪", "*kiss*... My, you are a good kisser!")
        elif ct("Bokukko"):
            $ rc("*kiss*... What, what? You like kissing me that much?", "Haa, *kiss*, *smooch*, hnm, Puaah! ...haa haa, I totally forgot, to breathe, haaa...", "*kiss*... Hm...? What did you eat today...?", "*smooch*... Hm, if you can lick, so can I...", "*Kiss* I wonder, was it good?", "*kiss* You're skilful, aren't ya?", "*kiss*... Mmmph, nn, mmh, chu, so lewd, geez...")
        elif ct("Imouto"):
            $ rc("*smooch* Ehehe, that's a bit embarrassing ♪", "*smooch*, ahm, *lick*... My tongue moved by itself...", "*kiss*, hn... *slurp*, *kiss*... Ehehe♪ My tongue, it feels good right ♪", "*kiss* Hnn, you're not going to use your tongue? Huhu ♪", "*lick, kiss*... *lick*, hn...  I licked you a lot.. ♪", "*smooch* Hehe, we kissed ♪", "Hn, *kiss*... Haa... Your breath is tickling me...", "Ehehe, kiss time ♪ *kiss*", "Mhm, nnh, chu, hmm...nnh, mmh... Puah!　Gosh, I'm out of breath...")
        elif ct("Kamidere"):
            $ rc("*kiss* How about at least trying to look a bit happier?", "*kiss*... Felt good, right?", "*smooch*... Getting excited?", "*kiss*... I'll leave you with that much.", "Hn, *smoooch*...  Uhuh, now you've got a hickey ♪", "*Kiss*... Haha, why's your face getting so red? ♪", "I, too, can be sweet sometimes... *kiss*, ahm... *smooch*...")
        else:
            $ rc("Don't say anything.... *kiss*", "*kiss*, *lick*, I like, *kiss*, this...", "*kiss*, hmm... *sigh*, kissing feels so good...", "*kiss*...  My heart's racing ♪", "Hmm... *kiss, kiss*, ahm,.. I like... kissing... Hn, *smooch*...", "*slurp, kiss* Kissing this rough... feels so good.", "*kiss* You're sweet...", "Ahm... *kiss, lick*... nnn... Do you think touching tongues is a little... sexy?") 

    else:
        $ char.show_portrait_overlay("sweat", "reset")
        $ char.disposition -= randint(15, 25)
        $ del temp
        $ del n
        if ct("Impersonal"):
            $ char.override_portrait("portrait", "indifferent")
            $ rc("I see no possible benefit in doing that with you so I will have to decline.", "Denied. Please refrain from this in the future.")
        elif ct("Shy") and dice(50):
            $ char.override_portrait("portrait", "shy")
            $ rc("I... I don't want!", "W-we can't do that. ", "I-I don't want to... Sorry.")
        elif ct("Imouto"):
            $ char.override_portrait("portrait", "angry")
            $ rc("Noooo way!", "...I-I'm gonna get mad if you that that stuff, you know? Jeez!", "Y-you dummy! Stay away!") 
        elif ct("Dandere"):
            $ char.override_portrait("portrait", "indifferent")
            $ rc("You're no good...", "You should really settle down.", "No, not with you.")
        elif ct("Tsundere"):
            $ char.override_portrait("portrait", "angry")
            $ rc("I'm afraid I must inform you of your utter lack of common sense. Hmph!", "You are so... disgusting!", "You pervy little scamp! Not in a million years!")
        elif ct("Kuudere"):
            $ char.override_portrait("portrait", "angry")
            $ rc("...Perv. Stay away from me, got it?", "...Looks like I'll have to teach you about this little thing called reality.", "O-of course the answer is no!")
        elif ct("Kamidere"):
            $ char.override_portrait("portrait", "angry")
            $ rc("Wh-who do you think you are!?", "W-what? Of course I'm against that!", "The meaning of 'not knowing your place' must be referring to this, eh...?")
        elif ct("Bokukko"):
            $ char.override_portrait("portrait", "indifferent")
            $ rc("He-hey, settle down a bit, okay?", "You should keep it in your pants, okay?", "Hmph! Well no duh!")
        elif ct("Ane"):
            $ char.override_portrait("portrait", "indifferent")
            $ rc("If I was interested in that sort of thing I might, but unfortunately...", "No. I have decided that it would not be appropriate.", "I think that you are being way too aggressive.")
        elif ct("Yandere"):
            $ char.override_portrait("portrait", "indifferent")
            $ rc("I've never met someone who knew so little about how pathetic they are.", "...I'll thank you to turn those despicable eyes away from me.", "Stay away from me.")
        else:
            $ char.override_portrait("portrait", "indifferent")
            $ rc("With you? Of course not!", "Huh?! No, I don't want to! Pervert...", "Woah, hold on there. Maybe after we get to know each other better.")
        if char.disposition <= (350+50*sub) or (char.disposition <500 and m>1):
            $ char.set_flag("_day_countdown_interactions_blowoff", 3)
            $ del sub
            $ del m
            $ char.restore_portrait()
            $ char.hide_portrait_overlay()
            jump girl_interactions_end
        $ del sub
        $ del m
    $ char.restore_portrait()
    $ char.hide_portrait_overlay()
    jump girl_interactions
    
