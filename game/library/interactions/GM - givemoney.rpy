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
    # $ temp = renpy.input("You decided to give her some money. You have [hero.gold] G.", allow="1234567890")
    # if temp == "":
        # "You changed your mind."
        # jump girl_interactions
    # $ python_BS = int(temp)
    # if hero.gold >= python_BS: # that's right, it is python bullsh*t that you have to use another variable without a reason
        # $ hero.gold -= python_BS
        # $ char.gold += python_BS
        # "You gave her [temp] G."
    # else:
        # "You don't have such amount of gold."
        
    # @BS BS BS BS BS ;)
    # Even Shakespeares works would look like bullsh*t if you did not know how to read/write...
    # Just give it a bit of time, you'll figure out Python soon enough!
    python:
        try:
            temp = int(renpy.input("Enter a Number:", allow="1234567890"))
        except ValueError:
            renpy.jump("girl_interactions")
            
    # This bit is not required for this interaction, but I'll put it here just to point out apparent absence of BS:
    # Do note that none of this interrupts the program in any way or form while the code is run on every interaction:
    $ temp = int(temp)
    if hero.gold >= int(str(temp)):
        $ pass
    # End..
    
            
    if hero.take_money(temp): # This will log the transaction into finances. Since we did not specify a reason, it will take the default reason: Other.
        char.add_money(temp) # Same...
        "You gave her [temp] G."
    else:
        "You don't have such amount of gold."
    jump girl_interactions
    
label interactions_int_take_money:
    $ temp = renpy.input("You decided to take her money. She has [char.gold] G.", allow="1234567890")
    if temp == "":
        "You changed your mind."
        jump girl_interactions
    $ python_BS = int(temp)
    if char.gold >= python_BS:
        $ hero.gold += python_BS
        $ char.gold -= python_BS
        "You took [temp] G."
    else:
        "She doesn't have such amount of gold."
    jump girl_interactions