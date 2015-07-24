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
        if dice(70):           
            if char.disposition > 600:
                $ char.disposition += (randint(1, 4))
            else:
                $ char.disposition += (randint(5, 15))
            g "Thank you!"
            
        else:
            g "I don't want your money."
            $ char.disposition -= (randint(5, 12))
            $hero.add_money(25)
    
    else:    
        narrator "You don't have 25g!"
    
    jump girl_interactions
    

###### j2
label interactions_gm50g:

    if hero.take_money(50):
        if dice(70):           
            if char.disposition > 600:
                $ char.disposition += (randint(2, 5))
            else:
                $ char.disposition += (randint(10, 20))
            g "Thank you!"
            
        else:
            g "I don't want your money."
            $ char.disposition -= (randint(10, 20))
            $hero.add_money(50)
    
    else:    
        narrator "You don't have 50g!"
    
    jump girl_interactions
         

###### j3
label interactions_gm100g:

    if hero.take_money(100):
        if dice(70):           
            if char.disposition > 600:
                $ char.disposition += (randint(3, 6))
            else:
                $ char.disposition += (randint(15, 30))
            g "Thank you!"
            
        else:
            g "I don't want your money."
            $ char.disposition -= (randint(10, 25))
            $hero.add_money(100)
    
    else:    
        narrator "You don't have 100g!"
    
    jump girl_interactions
    
    
###### j4
label interactions_gm500g:
    
    if hero.take_money(500):
        if dice(70):           
            if char.disposition > 600:
                $ char.disposition += (randint(5, 10))
            else:
                $ char.disposition += (randint(25, 45))
            $rc("Thank you!", "Wow, how generous you are!")
            
        else:
            g "I don't want your money."
            $ char.disposition -= (randint(20, 35))
            $hero.add_money(500)
    
    else:    
        narrator "You don't have 500g!"
    
    jump girl_interactions
    
