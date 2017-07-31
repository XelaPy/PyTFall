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
        # $ kayo_music_on = False
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
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")       
    $ jump('tailor_store_shopping')

    
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
    $ kayo_music_on = False
    hide screen shopping
    hide screen tailor_store_shopping
    with dissolve
    jump main_street

screen tailor_store_shopping:
    vbox:
        style_group "basic"
        xfill True
        maximum (500, 400)
        align(0.5, 0.99)
        textbutton "I want to order something special":
            action [Function(global_flags.set_flag, "tailor_special_order_ask", True), Hide("shopping", transition=dissolve), Jump("tailor_store")]
            xalign 0.5
            xfill True
            
