label tailor_store:
    
    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5

    hide screen main_street
    
    scene bg tailor_store
    with dissolve
    
    $ t = npcs["Kayo_Sudou"].say
    
    if not global_flags.has_flag("tailor_special_order_ask"):    
        $ global_flags.set_flag("tailor_special_order_ask", value=False)
    
    # TODO: Gotta add those special request, its a good idea
    
    # if global_flags.flag("tailor_special_order_ask"):
        # $ global_flags.set_flag("tailor_special_order_ask", value=False)
        # hide screen tailor_store_shopping
        
        # "A tailor lady comes in from the backroom."
        
        # show npc tailor_kayo_novel
        # with dissolve 
        
        # tailor_kayo "Yes? How can I be of service?"
        # menu:
            # "I would like..." if global_flags.flag("tailor_special_order"):
                # "dev message" "Hey! I didn't set one yet!"
            # "I don't have anything on my mind right now":
                # show npc tailor_kayo_angry_novel
                # tailor_kayo "Do vacate yourself then. Loitering is not allowed here." 

        # $ global_flags.del_flag("keep_playing_music")
        # jump main_street

        
    if global_flags.flag('visited_tailor_store'):
        show expression npcs["Kayo_Sudou"].get_vnsprite() as npc
        with dissolve
        t "Welcome back, take a look at our latest arrivals!"
        
    else:
        $global_flags.set_flag('visited_tailor_store')
            
        "You entered the shop. The shelves are filled with colorful silks and some exquisite dresses are displayed on the mannequins.{p}Noticing your arrival, a tailor lady comes in from the backroom and approaches you."
 
        show expression npcs["Kayo_Sudou"].get_vnsprite() as npc
        with dissolve
        
        t "Oh, a new customer! Welcome to my store."
        t "I'm honored to present you our wares. All pieces you see were acquired from the most renowned merchants. "
        t "But If you have any special requests, just tell me. I'm sure I will be able to help you."
    

    
label tailor_store_shopping:
    python:
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.tailor_store
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)

    show screen shopping(left_ref=hero, right_ref=shop)
    show screen tailor_store_shopping
    with dissolve
    call shop_control from _call_shop_control_4
    
    $ global_flags.del_flag("keep_playing_music") 

    hide screen shopping
    hide screen tailor_store_shopping
    with dissolve
    jump main_street

screen tailor_store_shopping: # TODO in the future: vertical scrolling may be needed eventually
    vbox:
        style_group "basic"
        xfill True
        maximum (500, 400)
        align(0.5, 0.99)
        button:
            xysize (200, 50)
            style_prefix "wood"
            text "Special Order" size 16 color goldenrod
            xalign 0.5
            action Jump("tailor_special_order")
            
screen shopkeeper_items_upgrades(upgrades_list):
    modal True
    frame:
        align (0.5, 0.5)
        background Frame("content/gfx/frame/frame_dec_1.png", 75, 75)
        xpadding 75
        ypadding 75
        has vbox
        for i in upgrades_list:
            frame:
                style_prefix "wood"
                background Frame("content/gfx/frame/cry_box.png", 5, 5)
                xpadding 10
                ypadding 10
                hbox:
                    spacing 0
                    xsize 600
                    xalign 0.5
                    vbox:
                        add ProportionalScale(items[i[0]].icon, 80, 80) xalign 0.5
                        text "%s" %i[0] style "proper_stats_value_text" outlines [(1, "#181818", 0, 0)] color "#DAA520" size 15 xalign 0.5
                    text "+ %s GP =" %i[1] style "proper_stats_value_text" outlines [(1, "#181818", 0, 0)] color "#DAA520" size 25 yalign .5 xalign 0.0
                    add ProportionalScale(items[i[2]].icon, 80, 80) xalign 0.5
                    null width 10
                    button:
                        xysize (100, 50)
                        xalign 1.0
                        yalign 0.5
                        text "Order" size 16 color goldenrod
                        action Return(i[0])
                        padding (10, 10)
                    null height 1
        null height 5
        button:
            xysize (180, 50)
            style_prefix "wood"
            text "Cancel" size 16 color goldenrod
            xalign 0.5
            action Return(-1)

label tailor_special_order:
    hide screen tailor_store_shopping
    hide screen shopping
    t "For a small price I can upgrade your clothes to better versions. What would you like to order?"
    $ upgrade_list = [["Casual Clothes", "100", "Armored Casual Clothes"], ["Artisan Outfit", "200", "Elite Artisan Outfit"], ["Leather Jacket", "300", "Altered Leather Jacket"], ["Mercenary Clothes", "400", "Proper Mercenary Clothes"]]
    $ result = renpy.call_screen("shopkeeper_items_upgrades", upgrade_list)
    if result != -1:
        t "[result]"
    t "Please come again!"
    hide screen shopping
    hide screen tailor_store_shopping
    with dissolve
    jump main_street