###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - givemoney - 25G - GM
#  2 - givemoney - 50G - GM
#  3 - givemoney - 100G - GM
#  4 - givemoney - 500G - GM

###### j1
label interactions_giftmoney:
    if (day - char.flag("gm_give_money")) > 2 or char.flag("gm_give_money") == 0:
        $char.set_flag("gm_give_money", value=day)
    else:
        "You already did it recently, she does not want to abuse your generosity."
        jump girl_interactions
    python:
        try:
            temp = int(renpy.input("You proposed to help her with money. You have [hero.gold] G.", allow="1234567890"))
        except ValueError:
            "You changed your mind."
            renpy.jump("girl_interactions")
    if temp == 0:
        "You changed your mind."
        jump girl_interactions
    if temp > hero.gold:
        "You don't have such amount of gold."
        jump girl_interactions
    if round(char.gold/temp) > 5:
        "She refuses to take your money. Looks like you have insulted her by such a small sum."
        $ char.disposition -= (randint(9, 25))
        jump girl_interactions
    if hero.take_money(temp): # This will log the transaction into finances. Since we did not specify a reason, it will take the default reason: Other.
        $ char.add_money(temp) # Same...
        "You gave her [temp] G."
        if round(char.gold/temp) <= 1:
            "She enthusiastically accepts money. Looks like it's a huge sum for her."
            $ a = 20
            $ b = 50
        elif round(char.gold/temp) <= 3:
            "She gratefully accepts money. It is hard times."
            $ a = 10
            $ b = 25
        else:
            "She takes your money."
            $ a = 5
            $ b = 15
        if char.disposition >= 90:
            $ char.disposition += randint(a, b)/(char.disposition*0.01)
        else:
            $ char.disposition += randint(a, b)
    else:
        "You don't have such amount of gold."
    $ del a
    $ del b
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
        if char.gold < 100:
            "But she's too poor to help you."
            jump girl_interactions
        elif char.gold > hero.gold*10:
            $ temp = randint (round(char.gold*0.2), round(char.gold*0.8))
            label less_money_int:
            if temp > 1000:
                $ temp = round(temp*0.1)
                jump less_money_int
            if char.take_money(temp): # This will log the transaction into finances. Since we did not specify a reason, it will take the default reason: Other.
                $ hero.add_money(temp) # Same...
                "You gave you [temp] G."
                $ char.disposition -= randint (20, 40)
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
    else:
        "You don't have such amount of gold."
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
    else:
        "She doesn't have such amount of gold."
    jump girl_interactions

