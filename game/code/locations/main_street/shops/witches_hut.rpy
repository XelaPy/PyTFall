label witches_hut:
    
    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5
    
    hide screen forest_entrance
    
    scene bg witches_hut
    with dissolve
    
    show expression npcs["Abby_the_witch"].get_vnsprite() as npc
    with dissolve
    
    $ w = npcs["Abby_the_witch"].say
    
    if global_flags.flag("talk_to_witch"):
        $ global_flags.del_flag("talk_to_witch")
        call witch_menu from _call_witch_menu
        if global_flags.flag("jump_forest_entrance"):
            $ global_flags.del_flag("jump_forest_entrance")
            jump forest_entrance
    elif global_flags.flag('visited_witches_hut'):
        w "Welcome Back!"
    else:
        $ w = Character("???", color=orange, what_color=yellow, show_two_window=True)
        $ global_flags.set_flag('visited_witches_hut')
        w "New Customer!"
        extend " Welcome to my Potion Shop!"
        w "I am Abby, the Witch, both Cool and Wicked."
        w "You'll never know what you run into here!"
        w "Oh, and I also know a few decent {color=[orangered]}Fire{/color} and {color=[lime]}Air{/color} spells if you're interested."
        w "Check out the best home brew in the realm"
        extend " and some other great items in stock!"
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto") 
    $ jump('witches_hut_shopping')
    
label witches_hut_shopping:

    python:
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.witches_hut
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)

    show screen shopping(left_ref=hero, right_ref=shop)
    show screen witches_hut_shopping
    with dissolve
    
    #$ pytfall.world_quests.run_quests("auto") # Shouldn't be needed, as all events in same location
    $ pytfall.world_events.run_events("auto") 
    
    call shop_control from _call_shop_control_1
                    
    $ global_flags.del_flag("keep_playing_music")
    hide screen shopping
    hide screen witches_hut_shopping
    with dissolve
    jump forest_entrance

label witch_menu:
    
    $ w = npcs["Abby_the_witch"].say
    
    $ loop = True
    while loop:
        menu:
            w "What do you want?"
            "Abby The Witch Main":
                $ pass
            "Ask her to teach magic spells!":
                w "Sweet!"
                python:
                    witch_spells_shop = ItemShop("Witch Spells Shop", 18, ["Witch Spells Shop"], gold=5000, sells=["scroll"], sell_margin=0.25, buy_margin=5.0)
                    focus = False
                    item_price = 0
                    filter = "all"
                    amount = 1
                    shop = pytfall.witch_spells_shop
                    shop.inventory.apply_filter(filter)
                    char = hero
                    char.inventory.set_page_size(18)
                    char.inventory.apply_filter(filter)
                show screen shopping(left_ref=hero, right_ref=shop)
                with dissolve
                call shop_control
                hide screen shopping
                with dissolve
                w "Let me know if you need anything else."
                        
            "Ask her to train you!":
                if len(hero.team) > 1:
                    w "Who gets a lesson from a wicked witch today?"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                if not global_flags.has_flag("witches_training_explained"):    
                    w "I will train magic, intelligence and restore some MP."
                    w "I can also guarantee you agility will go up if you pay attention in class!"
                    extend " That however does not often happen for reasons unknown..."
                    w "It will cost you 1000 (+1000 per 5 levels) Gold per training session"
                    extend " and the effects will be instantenious!"
                    w "Yeap! I am That good!"
                    $ global_flags.set_flag("witches_training_explained")
                else:
                    w "You know the deal!"
                    
                $ training_price = char.get_training_price()    
                menu:
                    "Pay [training_price] Gold" if hero.AP > 0:
                        if hero.take_money(training_price, "Training"):
                            $ char.AP -= 1
                            $ char.auto_training("train_with_witch")
                            w "All done! Be sure to use your new powers only on wicked stuff! :)"
                        else:
                            w "Errr, you can't really pay me, can you?"
                            w "Maybe next time then?"
                        
                    "Maybe next time...":
                        $ pass
                $ del training_price

            "Schedule training sessions":
                if not global_flags.has_flag("training_sessions_explained"):
                    "Here you can arrange for daily training sessions at cost of 1AP and 1000 (+1000 per 5 levels) Gold per day."
                    "This will be automatically terminated if you lack the gold to continue."
                    "Sessions can be arranged with multiple trainers at the same day"
                    extend " however you'd be running a risk of not leaving AP to do anything else!"
                    $ global_flags.set_flag("training_sessions_explained")
                
                if len(hero.team) > 1:
                    "Pick a character!"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                menu:
                    "Setup sessions" if not char.has_flag("train_with_witch"):
                        $ char.set_flag("train_with_witch")
                    "Cancel sessions" if char.flag("train_with_witch"):
                        $ char.del_flag("train_with_witch")
                    "Do Nothing...":
                        $ pass
                        
            "Back to shopping please.":
                $ loop = False
                
            "Thanks and goodbye!":
                $ loop = False
                $ global_flags.set_flag("jump_forest_entrance")
            
    return
    
    

screen witches_hut_shopping:
    vbox:
        style_group "basic"
        xfill True
        maximum (500, 400)
        align(0.5, 0.99)
        textbutton "Talk to the witch":
            align (0.5, 1.0)
            action [Function(global_flags.set_flag, "talk_to_witch"), Hide("shopping", transition=dissolve), Hide("witches_hut_shopping", transition=dissolve),
                       Jump("witches_hut")]

