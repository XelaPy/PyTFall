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

label interactions_eattogether:
    "You propose to eat together somewhere."
    if char.flag("gm_eat_together") != day:
        $char.set_flag("gm_eat_together", value=day)
    else:
        "You already did it today. She's not hungry."
        jump girl_interactions
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
        $ gm.set_img("vnsprite")
    elif a == 3:
        show bg cafe as back with dissolve
        $ gm.set_img("vnsprite")
    else:
        show bg city_restaurant as back with dissolve
        $ gm.set_img("vnsprite")
    if a == 1:
        "Together you sit behind the bar and order some snacks and drinks."
        if ct("Dandere") or ct("Imouto") or ct("Kamidere") or ct("Shy") or ct("Homebody") or ct("Nerd"):
            $ char.override_portrait("portrait", "shy")
            char.say "She feels a bit uncomfortable in such an establishment."
            $ char.disposition -= randint (15, 20)
            $ char.restore_portrait()
        if ct("Heavy Drinker"):
            if dice(70):
                $ char.override_portrait("portrait", "happy")
                $ d = 1
                char.say "She welcomes the opportunity to get drunk for free."
                $ char.disposition += dice (2, 6)
                $ b += randint (9, 25)
                if ct("Aggressive") and dice (80):
                    $ char.override_portrait("portrait", "angry")
                    char.say "Once drunk, she begins to bully other customers. You managed to calm her, but not before they broke some furniture."
                    $ char.restore_portrait()
                    $ b += randint (15, 35)
            $ char.restore_portrait()
        elif (char.character+char.intelligence)>=(hero.charisma+hero.intelligence):
            if dice(25):
                $ d = 1
                $ char.override_portrait("portrait", "happy")
                char.say "Very soon she becomes drunk."
                $ b += randint(25, 45)
                if ct("Aggressive") and dice (80):
                    $ char.override_portrait("portrait", "angry")
                    char.say "Once drunk, she begins to bully other customers. You managed to calm her, but not before they broke some furniture."
                    $ char.restore_portrait()
                    $ b += randint (15, 35)
                $ char.restore_portrait()
        elif (char.character+char.intelligence)<(hero.charisma+hero.intelligence):
            menu:
                "Do you want to try getting her drunk?"
            
                "Yes":
                    if dice (char.disposition - 100):
                        $ d = 1
                        $ char.override_portrait("portrait", "happy")
                        char.say "You keep pouring, and very soon she becomes drunk."
                        $ char.restore_portrait()
                        $ b += randint(25, 45)
                        if ct("Aggressive") and dice (80):
                            $ char.override_portrait("portrait", "angry")
                            char.say "Once drunk, she begins to bully other customers. You managed to calm her, but not before they broke some furniture."
                            $ char.restore_portrait()
                            $ b += randint (15, 35)
                        $ char.restore_portrait()
                    else:
                        "You keep pouring, but she politely refuses. Maybe she suspects something?"
                        $ char.disposition -= 10
                "No":
                    $ pass
        if ct("Always Hungry") and dice (70):
            $ char.override_portrait("portrait", "indifferent")
            char.say "They mostly serving light snacks here, so it's difficult for her to eat one's fill."
            $ char.disposition -= 5
            $ b += randint (5, 10)
            $ char.restore_portrait()
        if ct("Aggressive") and dice (50):
            $ char.override_portrait("portrait", "angry")
            char.say "She didn't liked how some drunk customers loudly discussed her, leading to a small skirmish. You managed to calm her, but not before they broke some glasses."
            $ char.restore_portrait()
            $ b += randint (10, 30)
        if ct("Clumsy") and dice (30):
            "She was more clumsy than usual today and smashed her glass. She was upset, but you managed to cheer her up."
            $ b += dice (5, 10)
            $ char.disposition += dice (1, 5)
        if (ct("Sexy Air") and dice (80)) or dice (25):
            $ char.override_portrait("portrait", "shy")
            char.say "A drunk customer tried to hit on her and was driven off by you. She looks grateful."
            $ char.disposition += 10
            $ char.restore_portrait()
        "Over a glass of booze you have a small chat with her."
        call eat_together_chat
        $ b += randint(45, 75)
        "It's time to pay the bill. It will be [b]G."
        call eat_together_pay
        if (d == 1 or dice(55)) and ct("Exhibitionnist"):
            $ gm.set_img("stripping", "simple bg", type="first_default")
            "Your meeting ends with her drunk, naked and dancing on the table under cheers of customers."
            hide back
            jump girl_interactions_end

        elif d == 1 and (ct("Nymphomaniac") or check_lovers(char, hero) or char.disposition >= 850):
            $ char.override_portrait("portrait", "shy")
            char.say "Drunk and blushing, she proposes to have some fun together."
            $ char.restore_portrait()
            menu:
                "Of course":
                    "You leave the establishment together."
                    hide back with dissolve
                    jump scene_sex_hired
                "Maybe another time":
                    "She looks a but disappointed."
                    $ char.disposition -= 5
    elif a == 2:
        "Together you sit at a table under a beach umbrella and order some light meal and soda."
        if dice (50):
            "The weather is nice today."
        else:
            "Cold wind blowing from the sea. Not the best time to sit here..."
            $ char.disposition -= randint (5, 10)
            if dice (50):
                $ char.effects['Down with Cold']['active'] = True
        if ct("Always Hungry") and dice (70):
            $ char.override_portrait("portrait", "happy")
            char.say "They don't serve much besides junk food, but she enjoys it anyway."
            $ b += randint (35, 50)
            $ char.disposition += 5
            $ char.restore_portrait()
        $ b += randint(20, 35)
        "Under the sound of the ocean and the cries of birds you have a small chat with her."
        call eat_together_chat
        "It's time to pay the bill. It will be [b]G."
        call eat_together_pay
    elif a == 3:
        "Together you order some food. It's cheap, but rather tasty and healthy."
        if ct("Kamidere") or ct("Yandere"):
            $ char.override_portrait("portrait", "indifferent")
            char.say "She feels a bit uncomfortable in such an establishment."
            $ char.disposition -= randint (15, 20)
            $ char.restore_portrait()
        if ct("Clumsy") and dice (50):
            $ char.override_portrait("portrait", "sad")
            char.say "She was more clumsy than usual today and smashed a plate. She was upset, but you managed to cheer her up."
            $ char.restore_portrait()
            $ b += dice (5, 15)
            $ char.disposition += dice (1, 5)
        if ct("Always Hungry") and dice (80):
            $ char.override_portrait("portrait", "happy")
            char.say "She enjoys the food here a lot, emptying one dish after another."
            $ b += randint (20, 30)
            $ char.disposition += 15
            $ char.restore_portrait()
        $ b += randint (25, 35)
        if dice (60):
            "Unfortunately, today it's too crowded here for a chat."
        else:
            "You managed to have a small chat with her, though you didn't have much time to talk between eating and waiting in line."
            call eat_together_chat
        "It's time to pay the bill. It will be [b]G."
        call eat_together_pay
    else:
        "Together you booked a table and ordered some expensive food and drinks."
        if ct("Impersonal") or ct("Bokukko") or ct("Homebody") or ct("Messy"):
            $ char.override_portrait("portrait", "indifferent")
            char.say "She feels a bit uncomfortable in such an establishment."
            $ char.disposition -= randint (15, 20)
            $ char.restore_portrait()
        if ct("Heavy Drinker") and dice(80):
            $ char.override_portrait("portrait", "happy")
            $ d = 1
            char.say "She welcomes the opportunity to get drunk for free."
            $ char.disposition += 10
            $ b += randint (20, 45)
            $ char.restore_portrait()
        if ct("Always Hungry") and dice (80):
            $ char.override_portrait("portrait", "happy")
            char.say "The food here is expensive, but very tasty. She enjoys it a lot, emptying one dish after another."
            $ b += randint (40, 80)
            $ char.disposition += 25
            $ char.restore_portrait()
        if ct("Clumsy") and dice (50):
            $ char.override_portrait("portrait", "sad")
            char.say "She was more clumsy than usual today and smashed a plate. She was upset, but you managed to cheer her up."
            $ char.restore_portrait()
            $ b += dice (20, 25)
            $ char.disposition += dice (1, 8)
        if ct("Extremely Jealous") and dice (40):
            "Today you are served by a young flirty waitress, prompting [char.name] to fight for your attention."
            $ char.disposition += dice (1, 10)
            $ char.joy -= dice (10, 20)
        if ct("Ill-mannered") and dice (60):
            "Her lack of good manners lead to a conflict with other customers and staff. You were fined for improper conduct."
            $ b += dice (30, 65)
            $ char.disposition += dice (1, 10)
        "In a pleasant environment you managed to have a good long chat with her."
        call eat_together_chat
        $ b += randint(75, 150)
        "It's time to pay the bill. It will be [b]G."
        call eat_together_pay
    "You say goodbye to each other and part ways."
    hide back with dissolve
    jump girl_interactions_end
label eat_together_chat:
    if char.disposition > 200:
        if ct("Impersonal") or ct("Dandere") or ct("Kuudere") or ct("Shy"):
            $ narrator(choice(["She didn't talked much, but she enjoyed your company nevertheless.", "You had to do most of the talking, but she listened you with a smile.", "She welcomed the chance to spend some time with you.", "She is visibly at ease when talking to you, even though she didn't talked much."]))
        else:
            $ narrator(choice(["It was quite a friendly chat.", "You gossiped like close friends.", "She welcomed the chance to spend some time with you.", "She is visibly at ease when talking to you.", "You both have enjoyed the conversation."]))
        if a == 1:
            $ char.disposition += randint (20, 40)
        elif a == 2:
            $ char.disposition += randint (15, 20)
        elif a == 3:
            $ char.disposition += randint (5, 15)
        else:
            $ char.disposition += randint (30, 40)
    else:
        if ct("Impersonal") or ct("Dandere") or ct("Kuudere") or ct("Shy"):
            $ narrator(choice(["But there was a lot of awkward silence.", "But you had to do most of the talking.", "There is no sign of her opening up to you yet.", "But it was kind of one-sided."]))      
        else:
            $ narrator(choice(["It's all a little bit stiff.", "There's some reservation though…", "It's hard to find common ground.", "But it was somewhat forced."]))
        if a == 1:
            $ char.disposition += randint (15, 30)
        elif a == 2:
            $ char.disposition += randint (10, 15)
        elif a == 3:
            $ char.disposition += randint (5, 10)
        else:
            $ char.disposition += randint (20, 35)
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
        elif hero.gold < b and char.gold >= b:
            $ char.take_money(b)
        elif char.gold + hero.gold >= b:
            $ hero.take_money(hero.gold)
            $ char.take_money(b - hero.gold)
        else:
            "You didn't have enough money and were kicked out. That was a bad idea..."
            $ char.disposition -= 20
            $ hero.take_money(hero.gold)
            $ char.take_money(char.gold)
            $ char.joy -= 20
    return
    
# label interactions_helpwithsomething:
    # "You propose to help with something for free."
    # $ line = rts(char, {
        # "Athletic": ["rts_athletic_choice"],
        # "Manly": ["rts_manly_choice"],
        # "default": ["You chat for some time."]
        # })