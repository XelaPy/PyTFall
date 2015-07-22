label shop_control:
    python:
        while True:
            result = ui.interact()
            if result[0] == "item":
                if result[1] in (chr, shop):
                    amount = 1
                    focus = result[2]
                    if result[1] == chr:
                        purchasing_dir = 'sell'
                        item_price = int(focus.price*0.8)
                    else:
                        purchasing_dir = 'buy'
                        item_price = int(focus.price*1.2)
                    
                elif result[1] == 'buy/sell':
                    if purchasing_dir == 'buy':
                        result = chr.take_money(item_price*amount, "Items")
                        if result:
                            renpy.play("content/sfx/sound/world/purchase_1.ogg")
                            for __ in xrange(amount):
                                shop.inventory.remove(focus)
                                chr.inventory.append(focus)
                                shop.gold += item_price
                        else:
                            focus = None
                            renpy.say("", choice(["Not enought money!",
                                                              "No freebees I fear...",
                                                              "You'll need more money for this purchase"]))
                        amount = 1        
                        focus = False
                        
                    elif purchasing_dir == 'sell':
                        if focus.unique:
                            renpy.show_screen("pyt_message_screen", "Unique Items cannot be sold!")
                            continue
                        elif focus.slot == "quest":
                            renpy.show_screen("pyt_message_screen", "Items used in quests cannot be sold!")
                            continue
                        elif shop != pytfall.general_store and (not shop.locations.intersection(focus.locations) or focus.type.lower() not in shop.sells):
                            focus = None
                            renpy.say("", "I will not buy this item from you!")
                        else:                         
                            result = bool(shop.gold - (item_price*amount) >= 0)
                            if result:
                                renpy.play("content/sfx/sound/world/purchase_1.ogg")
                                for __ in xrange(amount):
                                    shop.gold -= item_price
                                    chr.add_money(item_price, "Items")
                                    chr.inventory.remove(focus)
                                    shop.inventory.append(focus)
                            else:
                                focus = None
                                renpy.say("", "This is a bit more than I can pay!")
                            amount = 1
                            focus = None
                    
            elif result[0] == 'control':
                if result[1] == "increase_amount":
                    if purchasing_dir == 'sell':
                        if amount < chr.inventory.get_item_count(focus):
                            amount += 1
                    elif purchasing_dir == 'buy':
                        if amount < shop.inventory.get_item_count(focus):
                            amount += 1
                elif result[1] == "decrease_amount":
                    if amount >= 2:
                        amount -= 1
                elif result[1] == 'return':
                    focus = None
                    break
    return
    
label cafe:
    
    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5
    
    hide screen pyt_main_street
    
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
        chr = hero
        chr.inventory.set_page_size(18)
        chr.inventory.apply_filter(filter)

    show screen pyt_shopping(left_ref=hero, right_ref=shop)
    with dissolve
    
    call shop_control from _call_shop_control_2
                    
    $ global_flags.del_flag("keep_playing_music")      
    hide screen pyt_shopping
    with dissolve
    jump main_street
