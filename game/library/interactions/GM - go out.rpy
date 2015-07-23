###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - go out - beach
#  2 - go out - date finish
#  3 - go out - date fight

###### j1
label interactions_beach:
    # Transition
    python:
        renpy.scene()
        hs()
    
    show bg city_beach
    with fade
    
    "You take a walk on the beach. "
    
    $ renpy.show('chr', what=chr.show('datebeach', resize=(700,600)), at_list=[Position(ypos = 0.77)])
    with dissolve
    
    "The weather is really nice. "
    "After a while of walking down the beach chatting, you see a cafe/restaurant on the beach! "
    
    g "I wouldn't say no to a soda. "
    
    menu:
        "Do you want to get drinks? "
        
        "Go in":
            $ interact_date_beach_goin = True
        
        "Forget it":
            $ interact_date_beach_goin = False
    
    if  interact_date_beach_goin:
        show bg city_beach_cafe
        with fade
        
        g "What should we get? "
        
        menu:
            "Drinks Menu: "
            
            "Water: 10 Gold ":
                $interact_date_beach_drinkmenu = 'Water'
            
            "Lemonade: 50 Gold":
                $interact_date_beach_drinkmenu = 'Lemonade'
            
            "Cocktail: 100 Gold":
                $interact_date_beach_drinkmenu = 'Cocktail'
        
        if interact_date_beach_drinkmenu == 'Water':
            if hero.take_money(10, "Gifts"):
                "Well, at least I am not thirsty anymore."
            
            else:
                "You do not have enough money to pay for the drink, so you leave."
        
        elif interact_date_beach_drinkmenu == 'Lemonade':
            if hero.take_money(50, "Gifts"):
                "Thanks, this is a great drink!"
                $chr.mod('disposition', 20)
                $chr.mod('joy', 3)
            
            else:
                "You do not have enough money to pay for the drink, so you leave."
                $chr.mod('disposition', -5)
        
        elif interact_date_beach_drinkmenu == 'Cocktail':
            if hero.take_money(100, "Gifts"):
                "Wow, this tastes amazing! Thank you!"
                $chr.mod('disposition', randint(25, 30))
                $chr.mod('joy', randint(4, 7))
            
            else:
                "You do not have enough money to pay for the drink, so you leave."
                $chr.mod('disposition', -10)
    
    else:
        g "To bad, I was really thirsty."
        $chr.mod('disposition', -10) 
        
    $renpy.show('bg city_street_1')
    $renpy.show('chr', what=chr.show('date', resize=(700,600)), at_list=[Position(ypos = 0.77)])
    with fade
    
    "As you walk back home... "
    "You see a couple of rough looking guys staring at you and your date. "
    
    if dice(33):
        $ gm_fight_bg = "city_beach"
        jump interactions_datefight
    
    else:
        "But they know better than to try and jump you. "
        jump interactions_datefinish
    

###### j2
label interactions_datefinish:
    show bg wood
    
    show screen pyt_girl_interactions
    
    "Back at home:"
    
    if chr.libido > 60:
        "She is pretty horny so you:"
        $ gm.generate_img("sex")
        "End the date with a bang."
        jump girl_interactions
    
    elif chr.refinement > 60:
        $ gm.generate_img("date")
        "She is learning to behave like a noble so she courteously says goodbye and goes to her room. "
        $chr.mod('reputation', 5)
        $chr.mod('joy', 5)
        jump girl_interactions
    
    elif chr.charisma > 40:
        $ gm.generate_img("date")
        "She looks really nice, going back to her room and friends. "
        "But you feel that the date went well. "
        $chr.mod('joy', 2)
        $chr.mod('reputation', 2)
    
    else:
        $ gm.generate_img("date")
        "The date went as well as could be expected... "
        $chr.mod('joy', 2)
        $chr.mod('constitution', 2)
    
    jump girl_interactions
    

###### j3
label interactions_datefight:
    
    $ renpy.scene()
    
    python:
        # Prepear the teams:
        enemy_team = Team(name="Enemy Team", max_size=3)
        mob = copy.deepcopy(pytfall.mobs["Barbarian"])
        for stat in ilists.battlestats:
            stat_value = int(getattr(mob, stat) * 0.8)
            setattr(mob, stat, stat_value)
        
        enemy_team.add(mob)
        
        mob = copy.deepcopy(pytfall.mobs["Barbarian"])
        for stat in ilists.battlestats:
            stat_value = int(getattr(mob, stat) * 0.4)
            setattr(mob, stat, stat_value)
        
        enemy_team.add(mob)
        enemy_team.add(mob)
        
        result = start_battle([hero, chr], enemy_team, music=choice(ilists.battle_tracks), background="bg %s"%gm_fight_bg)
        
        gm_fight_bg = "battle_arena_1"
        
        if result[0]:
            renpy.play("content/sfx/sound/events/go_for_it.mp3")
            
            for member in hero.team:
                if member not in result[1]:
                    member.attack += 2
                    member.luck += 2
                    member.defence += 2
                    member.magic += 2
                    member.vitality -= 100
                    member.exp += adjust_exp(member, 500)
        
        else:
            jump("game_over")
    
    "You've beat the shit out of these losers. "
    "[chr.name] seems happy! "
    
    jump interactions_datefinish
    
