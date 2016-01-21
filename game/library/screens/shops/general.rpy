label general_store:
    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5

    hide screen main_street
    
    # scene bg general_store
    scene bg general_store_alt
    with dissolve
    
    show npc shop_yukiko_novel
    with dissolve
    
    if global_flags.flag('visited_general_store'):
        "Welcome Back!"

    else:
        $ global_flags.set_flag('visited_general_store')
        "Welcome to PyTFall's General Store!"
        "Here you can buy all sorts of items!"
        "Please take a look at our selection: "
    python:
        pytfall.world_quests.run_quests("auto")
        pytfall.world_events.run_events("auto")
        
        jump('general_store_shopping')
        
label general_store_shopping:

    python:
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.general_store
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter("all")

    show screen shopping(left_ref=hero, right_ref=shop)
    with dissolve
    
    call shop_control from _call_shop_control_3 
                    
    $ global_flags.del_flag("keep_playing_music")         
    hide screen shopping
    with dissolve
    jump main_street
