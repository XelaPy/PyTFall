label interactions_giftmoney:
    if (day - char.flag("flag_interactions_giftmoney")) > 3 or char.flag("flag_interactions_giftmoney") == 0:
        $ char.set_flag("flag_interactions_giftmoney", value=day)
    else:
        "You already did it recently, she does not want to abuse your generosity."
        jump girl_interactions
        
    $ temp = renpy.input("You proposed to help her with money. You have {} G.".format(hero.gold), allow="1234567890")
        
    if not temp:
        "You changed your mind."
        jump girl_interactions
    else:
        $ temp = int(temp)
            
    if temp == 0:
        "You changed your mind."
        $ del temp
        jump girl_interactions
    if temp > hero.gold:
        "You don't have that amount of gold."
        $ del temp
        jump girl_interactions
    if char.gold >= randint(500, 1000):
        if round(char.gold/temp) > 5:
            call interactions_not_enough_gold
            $ char.disposition -= (randint(9, 25))
            $ del temp
            jump girl_interactions
    if hero.take_money(temp): # This will log the transaction into finances. Since we did not specify a reason, it will take the default reason: Other.
        $ char.add_money(temp) # Same...
        "You gave her [temp] G."
        if round(char.gold/temp) <= 1:
            "She enthusiastically accepts money. Looks like it's a huge sum for her."
            $ a = 20
            $ b = 50
            $ hero.exp += randint(10, 20)
            $ char.exp += randint(10, 20)
        elif round(char.gold/temp) <= 3:
            "She gratefully accepts your money. Times are tough."
            $ a = 10
            $ b = 25
            $ hero.exp += randint(5, 10)
            $ char.exp += randint(5, 10)
        else:
            "She takes your money."
            $ a = 5
            $ b = 15
            $ hero.exp += randint(2, 5)
            $ char.exp += randint(2, 5)
        call interactions_enough_gold
        if char.disposition >= 90:
            $ char.disposition += round(randint(a, b)/(char.disposition*0.01))
        else:
            $ char.disposition += randint(a, b)
        $ del a
        $ del b
        $ del temp
    else:
        "You don't have that amount of gold."
        $ del temp
    jump girl_interactions

label interactions_askmoney:
    if (day - char.flag("flag_interactions_askmoney")) > 7 or char.flag("flag_interactions_askmoney") == 0:
        $char.set_flag("flag_interactions_askmoney", value=day)
    else:
        call interactions_recently_gave_money
        $ char.disposition -= randint(2, 5)
        jump girl_interactions
    "You asked her to help you with money."
    if char.disposition >= 400 or check_lovers(char, hero) or check_friends(char, hero):
        if char.gold < randint(500, 1000):
            call interactions_girl_is_too_poor_to_give_money
            jump girl_interactions
        elif char.gold > hero.gold*2:
            $ temp = randint (round(char.gold*0.01), round(char.gold*0.1))
            while temp >= randint(500, 1000): # we will continue to divide it by 10 until it becomes less than 500-1000. a countermeasure against becoming too rich by persuading a high lvl rich character to give you money.
                $ temp = round(temp*0.1)
            if char.take_money(temp): # This will log the transaction into finances. Since we did not specify a reason, it will take the default reason: Other.
                $ hero.add_money(temp) # Same...
                "She gave you [temp] G."
                $ hero.exp += randint(3, 8)
                $ char.disposition -= randint (20, 40)
                $ del temp
        else:
            "But looks like she needs money more than you."
            call interactions_girl_is_too_poor_to_give_money
            $ char.disposition -= randint (10, 20)
            jump girl_interactions
    else:
        "But she doesn't know you well enough yet."
        $ interactions_girl_disp_is_too_low_to_give_money()
        $ char.disposition -= randint (5, 15)
    jump girl_interactions    
    
label interactions_give_money:
    python:
        try:
            temp = int(renpy.input("You decided to give her some money. You have [hero.gold] G.", allow="1234567890"))
        except ValueError:
            "You changed your mind."
            renpy.jump("girl_interactions")
    if temp == 0:
        "You changed your mind."
        jump girl_interactions
    if hero.take_money(temp): # This will log the transaction into finances. Since we did not specify a reason, it will take the default reason: Other.
        $ char.add_money(temp) # Same...
        "You gave her [temp] G."
        $ del temp
    else:
        "You don't have that amount of gold."
    jump girl_interactions
    
label interactions_take_money:
    python:
        try:
            temp = int(renpy.input("You decided to take her money. She has [char.gold] G.", allow="1234567890"))
        except ValueError:
            "You changed your mind."
            renpy.jump("girl_interactions")
    if temp == 0:
        "You changed your mind."
        jump girl_interactions
    if char.take_money(temp): # This will log the transaction into finances. Since we did not specify a reason, it will take the default reason: Other.
        $ hero.add_money(temp) # Same...
        "You took [temp] G."
        $ del temp
    else:
        "She doesn't have that amount of gold."
    jump girl_interactions

label interactions_not_enough_gold:
    $ char.override_portrait("portrait", "indifferent")
    $ char.show_portrait_overlay("puzzled", "reset")
    if ct("Impersonal"):
        $ rc("I don't need it.", "What do you expect me to do with these money?")
    elif ct("Shy") and dice(50):
        $ rc("It's... for me? ...Um, thanks, but I cannot accept it.", "Oh... th-thank you, but I d-don't need it.")
    elif ct("Tsundere"):
        $ rc( "Huh? You think I'm that poor?!", "Hmph! I don't need your money! Idiot...")
    elif ct("Kuudere"):
        $ rc("Too bad, I'm not that cheap.", "I can perfectly live without your money, thanks you very much.")
    elif ct("Yandere"):
        $ rc("Money? I don't need them.", "I'm not interested.")
    elif ct("Dandere"):
        $ rc("I don't want it.", "No thanks.")
    elif ct("Ane"):
        $ rc("Not to be ungrateful, but... I really don't need money.", "I appreciate it, but I'm capable to live on my own.")
    elif ct("Imouto"):
        $ rc("Oh, a present! ...Money? Boring!", "Hey, I don't want your money!")
    elif ct("Kamidere"):
        $ rc("Is it the best you can do? Hehe, seems like you need money more than me ♪", "Is that all? Really? Pathetic.")
    elif ct("Bokukko"):
        $ rc("Wha? Money? Huhu, don't need them ♪", "Hey, is this a joke?")
    else:
       $ rc("Thanks, but no thanks.", "Um, I think you should keep these money for yourself.")
    $ char.restore_portrait()
    $ char.hide_portrait_overlay()
    return
    
label interactions_enough_gold:
    $ char.override_portrait("portrait", "happy")
    $ char.show_portrait_overlay("note", "reset")
    if ct("Impersonal"):
        $ rc("Thanks for your donation.", "I accept it. You have my thanks.")
    elif ct("Shy") and dice(50):
        $ rc("Oh... th-thank you.", "<Blush> Is it ok if I take this?...")
    elif ct("Tsundere"):
        $ rc("I guess I could use some... A-alright then.", "Your money? Are you sure..? Fine then, thanks.")
    elif ct("Kuudere"):
        $ rc("Well... since you offered... I could use some.", "...Thank you. I promise to spend them wisely.")
    elif ct("Yandere"):
        $ rc("You want to give me money?.. Fine, I don't mind.", "Alright, but I'll give you something in return one day, ok?")
    elif ct("Dandere"):
        $ rc("Is it really ok? Thanks then.", "Thanks.")
    elif ct("Ane"):
        $ rc("Thank you. You have my regards.", "Oh my, I'm grateful. I'll be sure to put your money to good use.")
    elif ct("Imouto"):
        $ rc("Oh! Money! ♪ <giggles>", "Hehehe, if you keep doing this I'll be spoiled.")
    elif ct("Kamidere"):
        $ rc("I'm accepting your generous offer.", "Very well. You have my gratitude.")
    elif ct("Bokukko"):
        $ rc("Oh? This is pretty cool! Thanks.", "Hey, thanks. It's shoppin' time ♪")
    else:
        $ rc("Thank you! I greatly appreciate it.", "Um, thank you. Can't say 'no' to free money, I guess ♪")
    $ char.restore_portrait()
    $ char.hide_portrait_overlay()
    return
    
label interactions_recently_gave_money:
    $ char.override_portrait("portrait", "indifferent")
    $ char.show_portrait_overlay("sweat", "reset")
    if ct("Impersonal"):
        $ rc("Denied. Your requests are too frequent.")
    elif ct("Shy") and dice(50):
        $ rc("I-I'd really like to... But... Um... Sorry.")
    elif ct("Tsundere"):
        $ rc("What, again?! What happened to the money I gave you the last time?")
    elif ct("Kuudere"):
        $ rc("Show some restraint. You cannot depend on others all the time.")
    elif ct("Yandere"):
        $ rc("You want my money again? I don't feel like it, sorry. Maybe next time.")
    elif ct("Dandere"):
        $ rc("No. You ask too much.")
    elif ct("Ane"):
        $ rc("You need to learn how to live on your own. Let's discuss it again after a while, alright?")
    elif ct("Imouto"):
        $ rc("Whaat? Again? All you think about is money!!")
    elif ct("Kamidere"):
        $ rc("I don't think so. Get a job, will you?")
    elif ct("Bokukko"):
        $ rc("No way! If you goin' to ask for money so often, I will become poor too.")
    else:
        $ rc("I cannot help you again, sorry. Maybe another time.")
    $ char.hide_portrait_overlay()
    $ char.restore_portrait()
    return
    
label interactions_girl_is_too_poor_to_give_money:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("Denied. Not enough funds.")
    elif ct("Shy") and dice(50):
        $ rc("Err... S-sorry, I don't have much money at the moment...")
    elif ct("Tsundere"):
        $ rc("*sigh* I'm not made of money, you know.")
    elif ct("Kuudere"):
        $ rc("I'm afraid you overestimate me. I'm not that rich *sadly smiles*")
    elif ct("Yandere"):
        $ rc("*sigh* I barely make ends meet, so... no.")
    elif ct("Dandere"):
        $ rc("No. I need money too.")
    elif ct("Ane"):
        $ rc("Unfortunately, I can't afford it.")
    elif ct("Imouto"):
        $ rc("Ugh... I don't have much money. Sorry ♪")
    elif ct("Kamidere"):
        $ rc("I refuse. Since I'm low on gold, my own needs take priority.")
    elif ct("Bokukko"):
        $ rc("Not gonna happen. I'm running out of money.")
    else:
        $ rc("I cannot help you, sorry. Maybe another time.")
    $ char.restore_portrait()
    return
    
init python:
    def interactions_girl_disp_is_too_low_to_give_money(): # also used for refusing to give access to items
        char.override_portrait("portrait", "indifferent")
        if ct("Impersonal"):
            rc("Denied.", "It won't happen.")
        elif ct("Shy") and dice(50):
            rc("S-sorry, I can't do it...", "Um, that's... not something I'm willing to do.")
        elif ct("Tsundere"):
            rc("Yeah, right. Don't even think about it, smartass.", "Not in a thousand years.")
        elif ct("Kuudere"):
            rc("I don't think so.", "I don't see the point.")
        elif ct("Yandere"):
            rc("I don't feel like it. Bother someone else.", "Right. As if I'm going to listen you.")
        elif ct("Dandere"):
            rc("No. Go away.", "I don't want to.")
        elif ct("Ane"):
            rc("Unfortunately, I must refuse.", "No, I believe it would be highly unwise.")
        elif ct("Imouto"):
            rc("Whaat?! Why should I do that?!", "No way!")
        elif ct("Kamidere"):
            rc("I refuse. Get lost.", "Know your place, fool.")
        elif ct("Bokukko"):
            rc("Not gonna happen.", "Nah, don't wanna.")
        else:
            rc("I think this is not a good idea.", "Why should I do it?")
        char.restore_portrait()
        return
    
    def interactions_character_doesnt_want_bad_item():
        char.override_portrait("portrait", "indifferent")
        char.show_portrait_overlay("sweat", "reset")
        if ct("Impersonal"):
            rc("I don't need it. It's useless.", "I' afraid I'm incompatible with this thing.")
        elif ct("Shy") and dice(50):
            rc("It's... for me? Um... I don't really need it...", "It's a... what is this, exactly? ...I see. Sorry, but...")
        elif ct("Tsundere"):
            rc("Who would want this crap?", "Whaaat? What am I supposed to do with this?!")
        elif ct("Kuudere"):
            rc("And what should I do with this... thing?", "You know, someone like me has no use for this.")
        elif ct("Yandere"):
            rc("What were you thinking? This is awful!", "This is absolute junk. I'm offended.")
        elif ct("Dandere"):
            rc("I don't want it.", "This item gives me a terrible feeling.")
        elif ct("Ane"):
            rc("Not to be ungrateful, but... I really don't like this.", "This is... interesting choice, but I think I'll pass.")
        elif ct("Imouto"):
            rc("Hey! I don't want this!", "Yuck, what is this? Looks terrible...")
        elif ct("Kamidere"):
            rc("This junk isn't useful at all.", "Please refrain from bothering me with this in the future.")
        elif ct("Bokukko"):
            rc("Hey, is this a joke? What am I supposed to do with this?", "Get this thing away from me.")
        else:
           rc("Thanks, but I don't like these kinds of things.", "I'm sorry, but I absolutely hate this.")
        char.hide_portrait_overlay()
        char.restore_portrait()
        return
        
    def interactions_character_doesnt_want_to_equip_item():
        char.override_portrait("portrait", "indifferent")
        if ct("Impersonal"):
            rc(choice(["Access denied.", "You are not authorised to make such decisions."]))
        elif ct("Shy") and dice(50):
            rc(choice(["M-maybe another time?", "Um... I'll think about it."]))
        elif ct("Dandere"):
            rc(choice(["I'm fine as it is.", "I don't feel like it."]))
        elif ct("Kuudere"):
            rc(choice(["I'm perfectly fine without your advices, thank you very much.", "I can handle myself without your intervention."]))
        elif ct("Yandere"):
            rc(choice(["I don't think we are close enough to even discuss such things.", "It's not for you to decide."]))
        elif ct("Tsundere"):
            rc(choice(["I can manage my things without your help!", "Hey, don't just decide something like that on your own!"]))
        elif ct("Imouto"):
            rc(choice(["You think I'm too stupid to take care of myself?", "Hey! Don't tell me what to do, I'm not a kid!"]))
        elif ct("Bokukko"):
            rc(choice(["Hey, aren't you too cocky tellin' me what to do?", "Nah, not in the mood for this stuff..."]))
        elif ct("Kamidere"):
            rc(choice(["You think I just will agree to do anything for you?", "If you wish to control someone's life, get yourself a pretty slave."]))
        elif ct("Ane"):
            rc(choice(["Thanks for the proposition, but I'm fine.", "I find this quite inappropriate."]))
        else:
            rc(choice(["Sorry, but I don't want to.", "Eh? Don't worry, I think I'm doing great already."]))
        char.restore_portrait()
        return