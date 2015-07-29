###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - givemoney - 25G - GM
#  2 - givemoney - 50G - GM
#  3 - givemoney - 100G - GM
#  4 - givemoney - 500G - GM

###### j1
label interactions_gm25g:

    if hero.take_money(25):
        if char.gold < 50: 
            "She gratefully accepts money. It is hard times."        
            if char.disposition > 0:
                $ char.disposition += (randint(2, 4))
            else:
                $ char.disposition += (randint(5, 10))
            $ char.gold += 25
        elif char.gold < 100:
            "She takes your money."        
            if char.disposition > 0:
                $ char.disposition += (randint(1, 2))
            else:
                $ char.disposition += (randint(3, 5))
            $ char.gold += 25
        elif check_lovers(char, hero) or check_friends(char, hero):
            "You are not strangers, so she has nothing against your money. But it's not enough to change much."
            $ char.gold += 25
        else:
            "She refuses to take your money."
            $ char.disposition -= (randint(4, 10))
            $hero.add_money(25)
    else:    
        narrator "You don't have 25g!"
    
    jump girl_interactions
    

###### j2
label interactions_gm50g:

    if hero.take_money(50):
        if char.gold < 100: 
            "She gratefully accepts money. It is hard times."        
            if char.disposition > 0:
                $ char.disposition += (randint(4, 8))
            else:
                $ char.disposition += (randint(10, 20))
            $ char.gold += 50
        elif char.gold < 200:
            "She takes your money."        
            if char.disposition > 0:
                $ char.disposition += (randint(2, 4))
            else:
                $ char.disposition += (randint(6, 10))
            $ char.gold += 50
        elif check_lovers(char, hero) or check_friends(char, hero):
            "You are not strangers, so she has nothing against your money. But it's not enough to change much."
            $ char.gold += 50
        else:
            "She refuses to take your money."
            $ char.disposition -= (randint(8, 20))
            $hero.add_money(50)
    else:    
        narrator "You don't have 50g!"
    
    jump girl_interactions
         

###### j3
label interactions_gm100g:

    if hero.take_money(100):
        if char.gold < 200: 
            "She gratefully accepts money. It is hard times."        
            if char.disposition > 0:
                $ char.disposition += (randint(8, 16))
            else:
                $ char.disposition += (randint(20, 40))
            $ char.gold += 100
        elif char.gold < 400:
            "She takes your money."        
            if char.disposition > 150:
                $ char.disposition += (randint(4, 8))
            else:
                $ char.disposition += (randint(12, 20))
            $ char.gold += 100
        elif check_lovers(char, hero) or check_friends(char, hero):
            "You are not strangers, so she has nothing against your money. But it's not enough to change much."
            $ char.gold += 100
        else:
            "She refuses to take your money."
            $ char.disposition -= (randint(7, 15))
            $hero.add_money(100)
    else:    
        narrator "You don't have 100g!"
    
    jump girl_interactions
    
    
###### j4
label interactions_gm500g:
    
    if hero.take_money(500):
        if char.gold < 1000: 
            "She gratefully accepts money. It is hard times."        
            if char.disposition > 0:
                $ char.disposition += (randint(40, 80))
            else:
                $ char.disposition += (randint(100, 200))
            $ char.gold += 500
        elif char.gold < 2000:
            "She takes your money."        
            if char.disposition > 150:
                $ char.disposition += (randint(20, 40))
            else:
                $ char.disposition += (randint(60, 100))
        elif check_lovers(char, hero) or check_friends(char, hero):
            "You are not strangers, so she has nothing against your money. But it's not enough to change much."
            $ char.gold += 500
        else:
            "She refuses to take your money."
            $ char.disposition -= (randint(9, 20))
            $hero.add_money(500)
    else:    
        narrator "You don't have 500g!"
    
    jump girl_interactions
    
label interactions_int_give_money:
    $ temp = renpy.input("You decided to give her some money. You have [hero.gold] G.", allow="1234567890")
    $ python_BS = int(temp)
    if hero.gold >= python_BS:
        $ hero.gold -= python_BS
        $ char.gold += python_BS
        "You gave her [temp] G."
    else:
        "You don't have such amount of gold."
    jump girl_interactions
    
label interactions_int_take_money:
    $ temp = renpy.input("You decided to take her money. She has [char.gold] G.", allow="1234567890")
    $ python_BS = int(temp)
    if char.gold >= python_BS:
        $ hero.gold += python_BS
        $ char.gold -= python_BS
        "You took [temp] G."
    else:
        "She doesn't have such amount of gold."
    jump girl_interactions