label hiddenvillage_entrance:
    $ gm.enter_location(limited_location=True)
    if not "village" in ilists.world_music:
        $ ilists.world_music["village"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("village")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["village"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("hiddenvillage_entrance"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    if global_flags.flag('visited_hidden_village'): # should be changed to not global_flags.flag('visited_hidden_village') before the release !!!!!!!!!!!!!!!!!!!
        $ global_flags.set_flag('visited_hidden_village')

    scene bg hiddenvillage_entrance
    with dissolve
    show screen hiddenvillage_entrance
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
        
    while True:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ gm.start_gm(result[1])
            
        if result[0] == 'control':
            hide screen hiddenvillage_entrance
            if result[1] == 'return':
                $ renpy.music.stop(channel="world")
                hide screen hiddenvillage_entrance
                jump city
                
                
screen hiddenvillage_entrance:

    use top_stripe(True)

    use location_actions("hiddenvillage_entrance")
    
    $img = ProportionalScale("content/gfx/interface/icons/ninja_shop.png", 100, 70)
    imagebutton:
        pos(300, 315)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("hiddenvillage_entrance"), Jump("hidden_village_shop")]
        
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show("girlmeets", exclude=["beach", "winter", "night", "formal", "indoors", "swimsuit"], type="reduce", label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
    
label hidden_village_shop: # ninja shop logic
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5
        
    hide bg hiddenvillage_entrance
    
    scene bg workshop
    with dissolve
    show npc ninja_assistant
    with dissolve
    $ hidden_village_shop = ItemShop("Ninja Tools Shop", 18, ["Ninja Shop"], gold=1000, sells=["armor", "dagger", "fists", "rod", "claws", "sword", "bow", "amulet", "smallweapon", "restore", "dress"], sell_margin=0.85, buy_margin=3.0)
    $ r = Character("Ren", color=red, what_color=orange, show_two_window=True)
    
    if global_flags.flag('hidden_village_shop_first_enter'):
        r "Hey, [hero.name]. Need something?"
    else:
        $ r = Character("???", color=red, what_color=orange, show_two_window=True)
        $ global_flags.set_flag('hidden_village_shop_first_enter')
        r "Hm? Ah, heard about you."
        extend " Welcome to my Tools Shop."
        r "I'm Ren. We sell ninja stuff here."
        r "If we are interested, I can sell you some leftovers. Of course it won't be cheap for an outsider like you."
        r "But you won't find these things anywhere else, so it is worth it."
        r "Wanna take a look?"
    python:
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.hidden_village_shop
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)
        
    show screen shopping(left_ref=hero, right_ref=shop)
    with dissolve
    $ pytfall.world_events.run_events("auto") 
    
    call shop_control from _call_shop_control_5
                    
    $ global_flags.del_flag("keep_playing_music")
    hide screen shopping
    with dissolve
    jump hiddenvillage_entrance
    