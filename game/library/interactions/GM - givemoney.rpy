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

label interactions_eattogether:
    "You propose to eat together somewhere."
    $ b = 0
    $ c = 0
    $ d = 0
    menu:
        "Where would you like to do it?"
        
        "Bar":
            $ a = 1
        "Beach Cafe":
            $ a = 2
        "Eatery":
            $ a = 3
        "Restaurant":
            $ a = 4
        "Change you mind":
            jump girl_interactions
    if a == 1:
        show bg city_bar as back with dissolve
        $ gm.set_img("vnsprite")
    elif a == 2:
        show bg city_beach_cafe as back with dissolve
    elif  == 3:
        show bg cafe as back with dissolve
    else:
        show bg city_restaurant as back with dissolve
    if a == 1:
        "Together you sit behind the bar."
        if ct("Tsundere") or ct("Imouto") or ct("Kamidere") or ct("Shy") or ct("Homebody"):
            $ char.override_portrait("portrait", "shy")
            char.say "She feels a bit uncomfortable in such an establishment."
            $ char.disposition -= randint (15, 35)
            $ char.restore_portrait()
        if ct("Heavy Drinker") and dice(80):
            $ char.override_portrait("portrait", "happy")
            $ d = 1
            char.say "Very soon she welcomes the opportunity to get drunk for free."
            $ char.disposition += 5
            $ b += randint (9, 25)
            if ct("Aggressive") and dice (80):
                $ char.override_portrait("portrait", "angry")
                char.say "Once drunk, she begins to bully other customers. You managed to calm her, but not before they broke some furniture."
                $ char.restore_portrait()
                $ b += randint (15, 35)
            $ char.restore_portrait()
        if dice(50) and not ct("Heavy Drinker"):
            $ d = 1
            char.say "Very soon she becomes a bit drunk."
            $ b += randint(25, 45)
            if ct("Aggressive") and dice (80):
                $ char.override_portrait("portrait", "angry")
                char.say "Once drunk, she begins to bully other customers. You managed to calm her, but not before they broke some furniture."
                $ char.restore_portrait()
                $ b += randint (15, 35)
        if ct("Always Hungry") and dice (80):
            $ char.override_portrait("portrait", "indifferent")
            "They mostly serving light snacks here, so it's difficult for her to eat one's fill."
            $ char.disposition -= 5
            $ char.restore_portrait()
        if ct("Aggressive") and dice (50):
            $ char.override_portrait("portrait", "angry")
            char.say "She didn't liked how some drunk customers loudly discussed her, leading to a small skirmish. You managed to calm her, but not before they broke some furniture."
            $ char.restore_portrait()
            $ b += randint (10, 30)
        if (ct("Sexy Air") and dice (80)) or dice (40):
            $ char.override_portrait("portrait", "shy")
            char.say "A drunk customer tried to hit on her and was driven off by you. She looks grateful."
            $ char.disposition += 15
            $ char.restore_portrait()
        "Over a glass of booze you have a small chat with her."
        call eat_together_chat
        $ b += randint(45, 75)
        "It's time to pay the bill. It will be [b]G."
        
        if (d == 1 or dice(65)) and ct("Exhibitionnist"):
            $ gm.set_img("stripping", "simple bg", type="first_default")
            "Your meeting ends with her drunk, naked and dancing on the table under cheers of customers."
            jump girl_interactions_end

        elif d == 1 and (ct("Nymphomaniac") or check_lovers(char, hero) or char.disposition >= 850):
            $ char.override_portrait("portrait", "shy")
            char.say "Drunk and blushing, she proposes to have some fun together."
            $ char.restore_portrait()
            menu:
                "Of course":
                    "Quickly paying, you leave the establishment together."
                    jump scene_sex_hired
                "Maybe another time":
                    "She looks a but disappointed."
                    $ char.disposition -= 5
    hide back with dissolve
    jump girl_interactions_end
label eat_together_chat:
    if char.disposition > 200:
        if ct("Impersonal") or ct("Dandere") or ct("Kuudere") or ct("Shy"):
            $ narrator(choice(["She didn't talked much, but she enjoyed your company nevertheless.", "You had to do most of the talking, but she listened you with a smile.", "She welcomed the chance to spend some time with you.", "She is visibly at ease when talking to you, even though she didn't talked much."]))
        else:
            $ narrator(choice(["It was quite a friendly chat.", "You gossiped like close friends.", "She welcomed the chance to spend some time with you.", "She is visibly at ease when talking to you.", "You both have enjoyed the conversation."]))
        $ char.disposition += randint (20, 40)
    else:
        if ct("Impersonal") or ct("Dandere") or ct("Kuudere") or ct("Shy"):
            $ narrator(choice(["But there was a lot of awkward silence.", "But you had to do most of the talking.", "There is no sign of her opening up to you yet.", "But it was kind of one-sided."]))      
        else:
            $ narrator(choice(["It's all a little bit stiff.", "There's some reservation though…", "It's hard to find common ground.", "But it was somewhat forced."]))
        $ char.disposition += randint (15, 35)
    return
label eat_together_pay:
    if char.status != "slave":
        if ct("Virtuous") or ct("Well-mannered") or char.disposition >= 900 or check_lovers(char, hero):
            if char.gold >= round(b*0.5) and hero.gold >= round(b*0.5):
                "She doesn't allow you to pay the whole sum, insisting on dividing it in half."
                $ char.take_money(round(b*0.5))
                $ hero.take_money(round(b*0.5))
            elif hero.gold < b and char.gold >= b:
                "You don't have enough money, and she readily pays for both of you."
                $ char.take_money(b)
            elif char.gold + hero.gold >= b:
                "You pay the bill together."
                $ char.disposition += 5
                $ char.take_money(b-hero.gold)
                $ hero.take_money(hero.gold)
            else:
                "You both didn't have enough money and were kicked out. That was a bad idea..."
                $ char.disposition -= 50
                $ hero.take_money(hero.gold)
                $ char.take_money(char.gold)
                $ char.joy -= 30

        else:
            if hero.gold >= b:
                "You pay the whole sum as a true gentleman."
                $ hero.take_money(b)
            elif char.gold + hero.gold >= b:
                "You don't have enough money, and your companion has to pay too. She looks disappointed."
                $ char.take_money(b-hero.gold)
                $ hero.take_money(hero.gold)
                $ char.disposition -= 5
            else:
                "You both didn't have enough money and were kicked out. That was a bad idea..."
                $ char.disposition -= 50
                $ hero.take_money(hero.gold)
                $ char.take_money(char.gold)
                $ char.joy -= 30

    else:
        if hero.gold >= b:
            $ hero.take_money(b)
            "Together you pay the bill."
        elif hero.gold < b and char.gold >= b:
            "Together you pay the bill."
            $ char.take_money(b)
        elif char.gold + hero.gold >= b:
            $ hero.take_money(hero.gold)
            $ char.take_money(b - hero.gold)
            "Together you pay the bill."
        else:
            "You both didn't have enough money and were kicked out. That was a bad idea..."
            $ char.disposition -= 20
            $ hero.take_money(hero.gold)
            $ char.take_money(char.gold)
            $ char.joy -= 20
