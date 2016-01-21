label cafe:
    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5
    
    hide screen main_street
    
    scene bg cafe
    with dissolve
    
    # show npc cafe_assistant 
    
    if global_flags.flag("waitress_chosen_today") != day:

        $ cafe_waitress_who = (choice(["npc cafe_mel_novel", "npc cafe_monica_novel", "npc cafe_chloe_novel"]))
        $ global_flags.set_flag("waitress_chosen_today", value=day)

    $renpy.show(cafe_waitress_who)
    with dissolve
    
    if global_flags.flag('visited_cafe'):
        "Welcome Back!"
    else:
        $global_flags.set_flag('visited_cafe')
        "Welcome to PyTFall's Cafe!"
        "Here you can buy food and tasty beverages!"
        "Please take a look at our selection: "
    
    $ pytfall.world_quests.run_quests("auto")  
    $ pytfall.world_events.run_events("auto")
    
    jump cafe_shopping
    
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
    jump main_street
