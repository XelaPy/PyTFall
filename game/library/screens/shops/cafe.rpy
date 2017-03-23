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
        
    $ renpy.show(cafe_waitress_who, at_list=[left])
    with dissolve

    if global_flags.flag('visited_cafe'):
        "Welcome back! Do you want a table?"
    else:
        $ global_flags.set_flag('visited_cafe')
        $ hero.set_flag("health_bonus_from_eating_in_cafe", value=0)
        "Welcome to the Cafe!"
        "Here you can buy food and tasty beverages!"
    $ inviting_character = hero
    if dice(30) and len(hero.team)>1 and hero.flag("ate_in_cafe") != day: # the chance for a member of MC team to invite team
        python:
            members = [] # all chars willing to invite will be in this list
            for member in hero.team:
                if member != hero:
                    if member.status == "free" and member.gold >= randint(500, 1000) and member.disposition >= 200 and member.joy >= 30:
                        members.append(member)
            if members:
                inviting_character = random.choice(members)
                interactions_eating_propose(inviting_character)
    if inviting_character != hero:
        menu:
            "Do you want to accept her invitation (free of charge)?"
            
            "Yes":
                $ del members
                jump cafe_invitation
            "No":
                $ del members
                
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
            if len(hero.team)>1 and hero.flag("ate_in_cafe") != day:
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

        "Light Snack (10 G)":
            if hero.take_money(10):
                $ name = "small_food_" + str(renpy.random.randint(1, 3))
                show image name at truecenter with dissolve
                # show image random.choice(movie_list)
                $ hero.set_flag("ate_in_cafe", value=day)
                $ result = "You feel a bit better!"
                if hero.vitality < hero.get_max("vitality"):
                    $ result_v = randint(4, 10)
                else:
                    $ result_v = 0
                $ hero.mod_stat("vitality", result_v)
                if hero.mp < hero.get_max("mp"):
                    $ result_m = randint(4, 10)
                else:
                    $ result_m = 0
                $ hero.mod_stat("mp", result_m)
                if result_v > 0:
                    $ result += "{color=[green]} +%d Vitality{/color}" % result_v
                if result_m > 0:
                    $ result += "{color=[blue]} +%d MP{/color}" % result_m
                $ hero.say ("%s" % result)
                $ hero.exp +=5
                $ del result
                $ del result_v
                $ del result_m
                hide image name with dissolve
                $ del name
            else:
                "You don't have that amount of gold."
                
        "Ordinary Meal (25 G)":
            if hero.take_money(25):
                $ name = "medium_food_" + str(renpy.random.randint(1, 3))
                show image name at truecenter with dissolve
                $ hero.set_flag("ate_in_cafe", value=day)
                $ result = "You feel quite satisfied."
                if hero.vitality < hero.get_max("vitality"):
                    $ result_v = randint(8, 15)
                else:
                    $ result_v = 0
                $ hero.mod_stat("vitality", result_v)
                if hero.mp < hero.get_max("mp"):
                    $ result_m = randint(8, 15)
                else:
                    $ result_m = 0
                $ hero.mod_stat("mp", result_m)
                if hero.health < hero.get_max("health"):
                    $ result_h = randint(8, 15)
                else:
                    $ result_h = 0
                $ hero.mod_stat("health", result_h)
                if result_v > 0:
                    $ result += "{color=[green]} +%d Vitality{/color}" % result_v
                if result_m > 0:
                    $ result += "{color=[blue]} +%d MP{/color}" % result_m
                if result_h > 0:
                    $ result += "{color=[red]} +%d Health{/color}" % result_h
                $ hero.say ("%s" % result)
                $ hero.exp +=10
                $ del result
                $ del result_v
                $ del result_m
                $ del result_h
                hide image name with dissolve
                $ del name
            else:
                "You don't have that amount of gold."
        "Extra Large Meal (50 G)":   # by eating big meals hero can increase max health by 2 with 75% chance; after increasing it by 50 the chance drops to 10% with smaller bonus
            if hero.take_money(50):
                $ name = "big_food_" + str(renpy.random.randint(1, 3))
                show image name at truecenter with dissolve
                $ hero.set_flag("ate_in_cafe", value=day)
                $ result = "You feel extremely full and satisfied."
                if hero.vitality < hero.get_max("vitality"):
                    $ result_v = randint(10, 20)
                else:
                    $ result_v = 0
                $ hero.mod_stat("vitality", result_v)
                if hero.mp < hero.get_max("mp"):
                    $ result_m = randint(10, 20)
                else:
                    $ result_m = 0
                $ hero.mod_stat("mp", result_m)
                if hero.health < hero.get_max("health"):
                    $ result_h = randint(10, 20)
                else:
                    $ result_h = 0
                $ hero.mod_stat("health", result_h)
                if hero.flag("health_bonus_from_eating_in_cafe") <= 25 and dice(75):
                    $ hero.stats.lvl_max["health"] += 2
                    $ hero.stats.max["health"] += 2
                    $ hero.mod_stat("health", 2)
                    $ result += "{color=[goldenrod]} +2 Max Health{/color}"
                    $ hero.set_flag("health_bonus_from_eating_in_cafe", value=hero.flag("health_bonus_from_eating_in_cafe")+1)
                elif dice(10) and hero.flag("health_bonus_from_eating_in_cafe") <= 50: # after 50 successful attempts bonus no longer applies
                    $ hero.stats.lvl_max["health"] += 1
                    $ hero.stats.max["health"] += 1
                    $ hero.mod_stat("health", 1)
                    $ result += "{color=[goldenrod]} +1 Max Health{/color}"
                    $ hero.set_flag("health_bonus_from_eating_in_cafe", value=hero.flag("health_bonus_from_eating_in_cafe")+1)
                    
                if result_v > 0:
                    $ result += "{color=[green]} +%d vitality{/color}" % result_v
                if result_m > 0:
                    $ result += "{color=[blue]} +%d MP{/color}" % result_m
                if result_h > 0:
                    $ result += "{color=[red]} +%d Health{/color}" % result_h
                $ hero.say ("%s" % result)
                $ hero.exp +=15
                $ del result
                $ del result_v
                $ del result_m
                $ del result_h
                hide image name with dissolve
                $ del name
    jump cafe_menu
            
label cafe_eat_group:
    # MC always pays for everyone; an algorithm where we check if every character can and wants to pay and then pays separately is too complex without a good reason
    # instead there will be another event when a character with enough money and disposition invites the group and pays for everything
    if hero.gold < 200:
        "Sadly, you don't have enough money to reserve a table." # MC doesn't even have 200 gold, it's not a good idea to spend money here so we just stop it immediately
        jump cafe_menu
label cafe_invitation: # we jump here when the group was invited by one of chars
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
    if inviting_character.take_money(result):
        $ n = renpy.random.randint(1, 9)
        $ img = "content/gfx/images/food/cafe_mass_%d.jpg" % n
        show expression img at truecenter with dissolve
        $ interactions_eating_line(hero.team)
        "You enjoy your meals together. Overall health and mood were improved." 
        $ hero.set_flag("ate_in_cafe", value=day)
        python:
            for member in hero.team:
                if member.status != "free" and member.disposition < -50:
                    d = 0.5
                else:
                    d = 1
                stat = round(randint(5, 10)*d)
                member.mod_stat("vitality", stat)
                stat = round(randint(5, 10)*d)
                member.mod_stat("health", stat)
                stat = round(randint(5, 10)*d)
                member.mod_stat("mp", stat)
                if member != hero:
                    stat = round(randint(4, 8)*d)
                    member.mod_stat("joy", stat)
                    stat = round(randint(10, 20)*d)
                    if len(hero.team)<3: # when there is only one char, disposition bonus is higher
                        stat += randint(5, 10)
                    member.mod_stat("disposition", stat)
        $ del result
        $ del stat
        $ del img
        $ del n
        hide expression img with dissolve
        jump cafe_menu
    else:
        $ del result
        jump cafe_menu
