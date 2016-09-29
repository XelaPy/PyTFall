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
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("cafe_eating"), Jump("cafe_eat_alone")]
                text "Eat alone" size 15
            if len(hero.team)>1:
                button:
                    xysize (150, 40)
                    yalign 0.5
                    action SetScreenVariable("stats_display", "Eat with group")
                    text "Eat with group" size 15
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("cafe_eating"), Jump("main_street")]
                text "Leave" size 15
    
label cafe_eat_alone:

    $ pass
    jump cafe_menu