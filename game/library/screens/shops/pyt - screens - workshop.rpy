label workshop:
    
    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5
    
    hide screen pyt_main_street
    
    scene bg workshop
    with dissolve
    
    show npc workshop_assistant
    with dissolve
    
    if global_flags.flag('visited_workshop'):
        "Welcome Back!"
    else:
        $ global_flags.set_flag('visited_workshop')
        "Welcome to PyTFall's Workshop!"
        "Best place to go for Weapons and Armor!"
        "Please take a look at our selection: "
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    $ jump('workshop_shopping')
    
label workshop_shopping:

    python:
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.workshop
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)

    show screen pyt_shopping(left_ref=hero, right_ref=shop)
    with dissolve
    
    call shop_control from _call_shop_control
                    
    $ global_flags.del_flag("keep_playing_music")
    hide screen pyt_shopping
    with dissolve
    jump main_street

    
screen pyt_workshop_shopping:
    
    use shop_inventory(root='inv', ref=char, x=0.0, title="Inventory")
    use shop_inventory(root='shop', ref=pytfall.workshop, x=1.0, title="WorkShop")
    
    if focus:
        frame background Frame("content/gfx/frame/mes12.jpg", 5, 5): 
            align (0.5, 0.5)
            xmaximum 650
            ymaximum 600
            
            hbox:
                use itemstats(item=focus)
                
            hbox:
                align (0.5, 0.7)
                python:
                    total_price = item_price * amount
                text("{size=25}Retail Price: [total_price]!") style "agrevue"
                
            hbox:
                align (0.5, 0.85)
                spacing 25
                use r_lightbutton(img = im.Scale('content/gfx/interface/buttons/blue_arrow_left.png', 60, 60), return_value = ['control', "decrease_amount"])
                text ("{size=50}[amount]")  style "agrevue"
                use r_lightbutton(img = im.Scale('content/gfx/interface/buttons/blue_arrow_right.png', 60, 60), return_value = ['control', "increase_amount"])
                
            if purchasing_dir == "buy":
                textbutton "{size=+5}{color=[black]}Buy" action Return(['control', 'buy/sell']) style "vista_button" xsize 100 align (0.5, 0.97)
            elif purchasing_dir == "sell":
                textbutton "{size=+5}{color=[black]}Sell" action Return(['control', 'buy/sell']) style "vista_button" xsize 100 align (0.5, 0.97)
                    
    use exit_button
