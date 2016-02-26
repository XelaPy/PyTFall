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
        jump girl_interactions
    if temp > hero.gold:
        "You don't have that amount of gold."
        jump girl_interactions
    if round(char.gold/temp) > 5:
        "She refuses to take your money. Looks like you have insulted her with such a small sum."
        $ char.disposition -= (randint(9, 25))
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
        if char.disposition >= 90:
            $ char.disposition += round(randint(a, b)/(char.disposition*0.01))
        else:
            $ char.disposition += randint(a, b)
        $ del a
        $ del b
        $ del temp
    else:
        "You don't have that amount of gold."
    jump girl_interactions

label interactions_askmoney:
    if (day - char.flag("gm_ask_money")) > 5 or char.flag("gm_ask_money") == 0:
        $char.set_flag("gm_ask_money", value=day)
    else:
        "You already did it recently, she cannot afford it."
        $ char.disposition -= randint(1, 4)
        jump girl_interactions
    "You asked her to help you with money."
    if char.disposition >= 400 or check_lovers(char, hero) or check_friends(char, hero):
        if char.gold < 200:
            "But she's too poor to help you."
            jump girl_interactions
        elif char.gold > hero.gold*10:
            $ temp = randint (round(char.gold*0.2), round(char.gold*0.8))
            while temp >= 1000: # we will continue to divide it by 10 until it becomes less than 1000. a countermeasure against becoming too rich by persuading a high lvl rich character to give you money.
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

