label interactions_giftmoney:
    if (day - char.flag("gm_give_money")) > 2 or char.flag("gm_give_money") == 0:
        $ char.set_flag("gm_give_money", value=day)
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
            "She refuses to take your money. Looks like you have insulted her with such a small sum."
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
    if (day - char.flag("gm_ask_money")) > 5 or char.flag("gm_ask_money") == 0:
        $char.set_flag("gm_ask_money", value=day)
    else:
        call interactions_recently_gave_money
        $ char.disposition -= randint(1, 5)
        jump girl_interactions
    "You asked her to help you with money."
    if char.disposition >= 300 or check_lovers(char, hero) or check_friends(char, hero):
        if char.gold < 250:
            call interactions_girl_is_too_poor_to_give_money
            jump girl_interactions
        elif char.gold > hero.gold*5:
            $ temp = randint (round(char.gold*0.01), round(char.gold*0.1))
            while temp >= 500: # we will continue to divide it by 10 until it becomes less than 500. a countermeasure against becoming too rich by persuading a high lvl rich character to give you money.
                $ temp = round(temp*0.1)
            if char.take_money(temp): # This will log the transaction into finances. Since we did not specify a reason, it will take the default reason: Other.
                $ hero.add_money(temp) # Same...
                "She gave you [temp] G."
                $ hero.exp += randint(3, 8)
                $ char.disposition -= randint (20, 40)
                $ del temp
        else:
            "You are already much richer than her. She needs money more than you."
            $ char.disposition -= randint (10, 30)
    else:
        "But she doesn't know you well enough yet."
        $ char.disposition -= randint (5, 15)
    jump girl_interactions    
    
label interactions_int_give_money:
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
    
label interactions_int_take_money:
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
    if ct("Impersonal"):
        $rc("I don't need it.", "What do you expect me to do with these money?")
    elif ct("Shy") and dice(50):
        $rc("It's... for me? ...Um, thanks, but I cannot accept it.", "Oh... th-thank you, but I d-don't need it.")
    elif ct("Tsundere"):
        $rc( "Huh? You think I'm that poor?!", "Hmph! I don't need your money! Idiot...")
    elif ct("Kuudere"):
        $rc("Too bad, I'm not that cheap.", "I can perfectly live without your money, thanks you very much.")
    elif ct("Yandere"):
        $rc("Money? I don't need them.", "I'm not interested.")
    elif ct("Dandere"):
        $rc("I don't want it.", "No thanks.")
    elif ct("Ane"):
        $rc("Not to be ungrateful, but ... I really don't need money.", "I appreciate it, but I'm capable to live on my own.")
    elif ct("Imouto"):
        $rc("Oh, a present! ...Money? Boring!", "Hey, I don't want your money!")
    elif ct("Kamidere"):
        $rc("Is it the best you can do? Hehe, seems like you need money more than me ♪", "Is that all? Really? Pathetic.")
    elif ct("Bokukko"):
        $rc("Wha? Money? Huhu, don't need them ♪", "Hey, is this a joke?")
    else:
       $ rc("Thanks, but no thanks.", "Um, I think you should keep these money for yourself.")
    $ char.restore_portrait()
    return
    
label interactions_enough_gold:
    $ char.override_portrait("portrait", "happy")
    if ct("Impersonal"):
        $rc("Thanks for your donation.", "I accept it. You have my thanks.")
    elif ct("Shy") and dice(50):
        $ rc("Oh... th-thank you.", "<Blush> Is it ok if I take this?...")
    elif ct("Tsundere"):
        $rc("I guess I could use some... A-alright then.", "Your money? Are you sure..? Fine then, thanks.")
    elif ct("Kuudere"):
        $rc("Well... since you offered... I could use some.", "...Thank you. I promise to spend them wisely.")
    elif ct("Yandere"):
        $rc("You want to give me money?.. Fine, I don't mind.", "Alright, but I'll give you something in return one day, ok?")
    elif ct("Dandere"):
        $rc("Is it really ok? Thanks then.", "Thanks.")
    elif ct("Ane"):
        $rc("Thank you. You have my regards.", "Oh my, I'm grateful. I'll be sure to put your money to good use.")
    elif ct("Imouto"):
        $rc("Oh! Money! ♪ <giggles>", "Hehehe, if you keep doing this I'll be spoiled.")
    elif ct("Kamidere"):
        $rc("I'm accepting your generous offer.", "Very well. You have my gratitude.")
    elif ct("Bokukko"):
        $rc("Oh? This is pretty cool! Thanks.", "Hey, thanks. It's shoppin' time ♪")
    else:
        $ rc("Thank you! I greatly appreciate it.", "Um, thank you. Can't say 'no' to free money, I guess ♪")
    $ char.restore_portrait()
    return
    
label interactions_recently_gave_money:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $rc("Denied. Your requests are too frequent.")
    elif ct("Shy") and dice(50):
        $ rc("I-I'd really like to... But... Um... Sorry.")
    elif ct("Tsundere"):
        $rc("What, again?! What happened to the money I gave you the last time?")
    elif ct("Kuudere"):
        $rc("Show some restraint. You cannot depend on others all the time.")
    elif ct("Yandere"):
        $rc("You want my money again? I don't feel like it, sorry. Maybe next time.")
    elif ct("Dandere"):
        $rc("No. You ask too much.")
    elif ct("Ane"):
        $rc("You need to learn how to live on your own. Let's discuss it again after a while, alright?")
    elif ct("Imouto"):
        $rc("Whaat? Again? All you think about is money. Boooring!")
    elif ct("Kamidere"):
        $rc("I don't think so. Get a job, will you?")
    elif ct("Bokukko"):
        $rc("No way! If you goin' to ask for money so often, I will become poor too.")
    else:
        $ rc("I cannot help you again, sorry. Maybe another time.")
    $ char.restore_portrait()
    return
    
label interactions_girl_is_too_poor_to_give_money:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $rc("Denied. Not enough funds.")
    elif ct("Shy") and dice(50):
        $ rc("Err... S-sorry, I don't have much money at the moment...")
    elif ct("Tsundere"):
        $rc("*sigh* I'm not made of money, you know.")
    elif ct("Kuudere"):
        $rc("I'm afraid you overestimate me. I'm not that rich *sadly smiles*")
    elif ct("Yandere"):
        $rc("*sigh* I barely make ends meet, so... no.")
    elif ct("Dandere"):
        $rc("No. I need money too.")
    elif ct("Ane"):
        $rc("Unfortunately, I can't afford it.")
    elif ct("Imouto"):
        $rc("Ugh... I don't have much money. Sorry ♪")
    elif ct("Kamidere"):
        $rc("I refuse. Since I'm low on gold, my own needs take priority.")
    elif ct("Bokukko"):
        $rc("Not gonna happen. I'm running out of money.")
    else:
        $ rc("I cannot help you, sorry. Maybe another time.")
    $ char.restore_portrait()
    return