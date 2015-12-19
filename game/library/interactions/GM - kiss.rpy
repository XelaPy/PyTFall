label interactions_kiss:
    "You trying to kiss her."
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

        
    if ct("Lesbian"): 
        $ gm_dice = ((gm_dice)*0.5)

    if (dice(gm_dice) and check_friends(char, hero)) or check_lovers(char, hero):
        $ gm_last_success = True
        $ char.disposition += (randint(20, 40)*(gm_disp_mult))
    else:
        $ gm_last_success = False
        $ char.disposition -= (randint(25, 45)*(gm_disp_mult))
    
    if gm_last_success:
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
                $rc("I'm kissing my brother like this... I'll never be forgiven for doing this...")
            elif ct("Ane"):
                $rc("*kiss* Brother, you taste so good! ♪")
            elif ct("Bokukko"):
                $rc("*kiss* What's it like to kiss your sister? Tastes good, doesn't it?")
            else:
                $rc("*kiss* Isn't it a bit strange to kiss your sister?", "*kiss* It's okay for siblings to kiss, isn't it?", "*kiss* Do you like Nee-chan's kisses?", "*kiss* This is different from the kisses we had when we were little.")
        elif ct("Yandere"):
            $rc("... *kiss*", "*kiss* *slurp* *slosh* <She's making patterns with her tongue>", "*kiss* ... *giggle* *kiss*", "momph*kiss*dufu*kiss*gae*kiss*mnn ... <Trying to talk, perhaps?>", "...Haah... It tastes like you... Hehe♪")    
        elif ct("Impersonal"):
            $rc("*kiss* Kissing is nothing that special.", "*kiss* My body's getting hotter...", "*smooch*, *kiss*... Hn... I can still taste you.", "Your lips look a little dry... *lick lick lick* Phew... that's much better.")
        elif ct("Shy") and dice(30):
            $rc("Huh... *kiss*… We k-kissed…", "*kiss*  We... kissed... <gives you a dreamy smile>", "Ahm, *slurp, kiss*......kissing feels good...", "*kiss* Nnn... <looks at you dreamily>", "<Gently kisses you back> H...how's this? Does it f... feel good...? It... it feels good for me...", "*kiss* ...Did I do that right...?", "Is this really ok...? ...*kiss*...", "<closes her eyes> *kiss* hn…")
        elif ct("Nymphomaniac") and dice(25):
            $rc("Mmmf♪　Nnh, nnf, mmmf... No, we're gonna kiss more♪ ...nnf, mmmf♪", "This isn't going to end with just a kiss, right?", "*kiss* Even though we're just kissing... I'm already...", "Nnn...Chu, nn... Let's...nn, exchange...saliva... nn, chu...", "Geez, do you really like my boobs that much? You perv～♪")
        elif ct("Dandere"):
            $rc("*kiss* ...Not enough. More.", "Nn, aah, haah... You're tickling my tongue...", "Hmmm... M-my lips… ", "*kiss* ...More...", "*kiss*… Your lips are dry…", "*smooch*… Done…", "*kiss*... *smooch*… *huff*... your breath... so hot…", "Do you desire my lips? *kiss*", "*kiss*...  Hn... you like kissing...?")
        elif ct("Kuudere"):
            $rc("*kiss* ...I just tripped, that's all.", "*kiss* How about at least trying to look a bit happier?", "Nhn... Ah... Do you like my kisses?", "Nh...chu...nnhu...chu... Nhn...chu... Y-you're overdoing it, idiot...", "<looking around> I suppose we can... *kiss*", "Ah... J-Jeez, that was too sudden...", "Mmmh, nn, chu, mmchu, nn... Hoh is id, my kish? Nmu, nn, chupuru... nfuu ♪")
        elif ct("Tsundere"):
            $rc("!? Wh-what do you think you're doing all of a sudden...? Geez.", "Nnn, nn... Ah... Done already...? !? I-I didn't say anything!", "Nnh, mmm, nyuu, nnnh! I won't lose! mmf, aumph, mph, mph, mph, mmf... Pfaah! How was that? Mhmhm♪", "*smooch*, hnn  Puah! Please don't go overboard!", "*kiss*, hn, hnn... Puah! Geez! How long are you planning on doing that?!", "*kiss*, *lick*… Hn aah... Geez, too much tongue!", "Hn *kiss*... hnn… Y-you're embarrassing me, geez…", "Nmuu … Geez! Who told you it was ok to kiss!", "*smooch*, hnn… I don't want, *kiss*, you to, *slurp*, let me go…", "Mmh, chu, nnh... mmmhah!　Jeez, how long are you gonna do this for!", "Mmh... Nmmh?! You bit my lips! Geez!")
        elif ct("Ane"):
            $rc("...Hmhm, there's a kiss mark on you.", "Nh... I've been saving this one for you. Hmhm.", "Mmh...nn... Hmhm, you're so good...", "*kiss* Kissing is a token of my affection...", "*kiss*...Hn… Just having our lips touch like this... makes me so excited.", "*kiss*… It's okay… ", "*kiss* My heart just beat faster for a bit.", "*kiss* That was a wonderful kiss.", "*kiss* I'm getting all aroused...", "*kiss* It was a pleasant experience.")
        elif ct("Bokukko"):
            $rc("*kiss*… What, what? You like kissing me that much?", "Take this! ...Hn *smooch* ♪", "Haa, *kiss*, *smooch*, hnm, Puaah! ...haa haa, I totally forgot, to breathe, haaa…", "*kiss*… Hm...? What did you eat today...?", "*smooch*… Hm, if you can lick, so can I…", "*Kiss* I wonder, was it good?", "*kiss* You're skillful, aren't ya?", "This isn't going to end with just a kiss, huh?", "*kiss*… Mmmph, nn, mmh, chu, so lewd, geez...")
        elif ct("Imouto"):
            $rc("*smooch* Ehehe, that's a bit embarrassing. ♪", "*smooch*, ahm, *lick*… Wafu, My tongue, moved by itself…", "*kiss*, hn... *slurp*, *kiss*… Pheew, ehehe♪ My tongue, it feels good right. ♪", "*slurp*, Ahm, *kiss*… Haha, It's a sign of my love. ♪", "*kiss* Hnn, you're not going to use your tongue? Huhu ♪", "*lick, kiss*... *lick*, hn…  I licked you a lot... ♪", "Hmm, ...*kiss* ...How was that? Like a lover's kiss, right? ♪", "*smooch* Hehe, we kissed ♪", "Hn, *kiss*… Haa... Your breath is tickling me…", "Ehehe, kiss time♪ *kiss*", "*kiss* Mmm... Come onnn...mmm", "Mhm, nnh, chu, hmm...nnh, mmh... Puah!　Gosh, I'm out of breath...♪")
        elif ct("Kamidere"):
            $rc("*kiss*… I'll leave you with that much.", "Hn, *smoooch*…  ...Uhuh♪ Now you've got a hickey", "*kiss kiss*, Huhuh, it's fine, because you belong to me... ♪", "*Kiss*… Haha, why's your face getting so red. ♪", "I, too, can be sweet sometimes… *kiss*, ahm... *smooch*…", "*kiss* Hmmm, *lick*… Hmpf. No~ I won't let you go that easily. ♪")
        else:
            $rc("*smooch*… Getting excited?", "Don't say anything.... *kiss*","*kiss*, *lick*, I like, *kiss*, this…", "*kiss*… Felt good, right?", "*kiss*, hmm… *sigh*, kissing feels so good…", "<Smiles after your kiss> You're good at kissing.", "*kiss*... Was that good enough for a passing grade, [hero.name]", "*kiss*...  My heart's racing...", "Even though we're just kissing... I'm already…<Blushes>", "Hmm... *kiss, kiss*, ahm,.. I like... kissing… Hn, *smooch*…", "Hn,chu… Eh, what've you been eating? I can taste it~", "*kiss*… Hn... My body's getting hotter…", "A kiss? Why not. *smooch*","Just what I was thinking about♪ *kiss*", "*slurp, kiss* Kissing this rough... feels so good.", "*kiss* hmm...Where did you learn to kiss like this?", "*kiss*,*lick*… This is great... got me all excited...", "Ok, but don't go overboard. *kiss*","*kiss* You're sweet...", "Ahm... *kiss, lick*... nnn… Do you think touching tongues is a little... sexy?", "*kiss*… My, you are a good kisser!") 
    else:
        "She refuses."
    $ char.restore_portrait()
    $ del gm_dice
    $ del gm_disp_mult
    jump girl_interactions
    
