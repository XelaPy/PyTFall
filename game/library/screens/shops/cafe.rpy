label cafe:
    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5
    
    hide screen main_street
    
    scene bg cafe
    with dissolve
    $ pytfall.world_quests.run_quests("auto")  
    $ pytfall.world_events.run_events("auto")
    # show npc cafe_assistant 
    
    if global_flags.flag("waitress_chosen_today") != day:

        $ cafe_waitress_who = (choice(["npc cafe_mel_novel", "npc cafe_monica_novel", "npc cafe_chloe_novel"]))
        $ global_flags.set_flag("waitress_chosen_today", value=day)
        
    $renpy.show(cafe_waitress_who)
    with dissolve

    if global_flags.flag('visited_cafe'):
        "Welcome back! Do you want a table?"
    else:
        $global_flags.set_flag('visited_cafe')
        "Welcome to the Cafe!"
        "Here you can buy food and tasty beverages!"
label cafe_menu: # after she said her lines but before we show menu controls, to return here when needed
    show screen cafe_eating
    while 1:
        $ result = ui.interact()
    
label cafe_shopping:

    python:
        focus = None
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.cafe
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)

    show screen shopping(left_ref=hero, right_ref=shop)
    with dissolve
    
    call shop_control from _call_shop_control_2
                    
    $ global_flags.del_flag("keep_playing_music")      
    hide screen shopping
    with dissolve
    jump cafe_menu

screen cafe_eating:
    frame:
        xalign 0.95
        ypos 20
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_group "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("cafe_eating"), Jump("cafe_shopping")]
                text "Shop" size 15
            if hero.flag("ate_in_cafe") != day:
                button:
                    xysize (150, 40)
                    yalign 0.5
                    action [Hide("cafe_eating"), Jump("cafe_eat_alone")]
                    text "Eat alone" size 15
            if len(hero.team)>1:
                button:
                    xysize (150, 40)
                    yalign 0.5
                    action [Hide("cafe_eating"), Jump("cafe_eat_group")]
                    text "Eat with group" size 15
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("cafe_eating"), Jump("main_street")]
                text "Leave" size 15
    
label cafe_eat_alone:
    menu:
        "What will it be?"
        
        "Junk Food (10 GP)":
            $ hero.set_flag("ate_in_cafe", value=day)
            if hero.take_money(10):
                if hero.vitality < hero.get_max("vitality"):
                    $ result_v = randint(4, 10)
                else:
                    $ result_v = 0
                $ hero.mod("vitality", result_v)
                if hero.mp < hero.get_max("mp"):
                    $ result_m = randint(4, 10)
                else:
                    $ result_m = 0
                $ hero.mod("mp", result_m)
                $ result = "You feel a bit better!"
                if result_v > 0:
                    $ result += " +%d vitality" % result_v
                if result_m > 0:
                    $ result += " +%d MP" % result_m
                $ hero.say ("%s" % result)
                $ hero.exp +=5
                $ del result
                $ del result_v
                $ del result_m
            else:
                "You don't have that amount of gold."
                
        "Ordinary Meal (25 GP)":
            $ hero.set_flag("ate_in_cafe", value=day)
            if hero.take_money(25):
                if hero.vitality < hero.get_max("vitality"):
                    $ result_v = randint(8, 15)
                else:
                    $ result_v = 0
                $ hero.mod("vitality", result_v)
                if hero.mp < hero.get_max("mp"):
                    $ result_m = randint(8, 15)
                else:
                    $ result_m = 0
                $ hero.mod("mp", result_m)
                if hero.health < hero.get_max("health"):
                    $ result_h = randint(8, 15)
                else:
                    $ result_h = 0
                $ hero.mod("health", result_h)
                if dice(4):
                    $ hero.AP +=1
                    $ result_a = 1
                else:
                    $ result_a = 0
                $ result = "You feel full and satisfied."
                if result_v > 0:
                    $ result += " +%d vitality" % result_v
                if result_m > 0:
                    $ result += " +%d MP" % result_m
                if result_h > 0:
                    $ result += " +%d Health" % result_h
                if result_a > 0:
                    $ result += " +1 AP"
                $ hero.say ("%s" % result)
                $ hero.exp +=10
                $ del result
                $ del result_v
                $ del result_m
                $ del result_h
                $ del result_a
            else:
                "You don't have that amount of gold."
        "Extra Large Meal (50 GP)":
            $ hero.set_flag("ate_in_cafe", value=day)
            if hero.take_money(50):
                if hero.vitality < hero.get_max("vitality"):
                    $ result_v = randint(10, 20)
                else:
                    $ result_v = 0
                $ hero.mod("vitality", result_v)
                if hero.mp < hero.get_max("mp"):
                    $ result_m = randint(10, 20)
                else:
                    $ result_m = 0
                $ hero.mod("mp", result_m)
                if hero.health < hero.get_max("health"):
                    $ result_h = randint(10, 20)
                else:
                    $ result_h = 0
                $ hero.mod("health", result_h)
                if dice(6):
                    $ hero.AP +=1
                    $ result_a = 1
                else:
                    $ result_a = 0
                $ result = "You feel extremely full and satisfied."
                if result_v > 0:
                    $ result += " +%d vitality" % result_v
                if result_m > 0:
                    $ result += " +%d MP" % result_m
                if result_h > 0:
                    $ result += " +%d Health" % result_h
                if result_a > 0:
                    $ result += " +1 AP"
                $ hero.say ("%s" % result)
                $ hero.exp +=15
                $ del result
                $ del result_v
                $ del result_m
                $ del result_h
                $ del result_a
    jump cafe_menu
            
label cafe_eat_group:
    # MC always pays for everyone; an algorithm where we check if every character can and wants to pay and then pays separately is too complex without a good reason
    # instead there will be another event when a character with enough money and disposition invites the group and pays for everything
    if hero.gold < 200:
        "Sadly, you don't have enough money to reserve a table." # MC doesn't even have 200 gold, it's not a good idea to spend money here so we just stop it immediately
        jump cafe_menu
    
    $ result = randint (30, 40) # base price MC pays for himself and the table
    python:
        for member in hero.team:
            if member != hero:
                if member.status != "free":
                    if member.disposition < -50:
                        money = randint (5, 10) # slaves with negative disposition will afraid to order too much, and also will have low bonuses
                    else:
                        money = randint (20, 45)
                    if "Always Hungry" in member.traits:
                        money += randint (5, 10)
                else:
                    money = randint (25, 50)
                    if "Always Hungry" in member.traits:
                        money += randint (10, 20)
                result += money
    if hero.take_money(result):
        $ interactions_eating_line(hero.team)
        "You enjoy your meals together."
        $ hero.set_flag("ate_in_cafe", value=day)
        jump cafe_menu
    else:
        "Sadly, you don't have enough money to reserve a table."
        jump cafe_menu
        
                
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            