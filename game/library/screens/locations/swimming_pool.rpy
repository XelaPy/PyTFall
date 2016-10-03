label swimming_pool:
    # gm.enter_location(goodtraits=["Energetic", "Exhibitionist"], badtraits=["Scars", "Undead", "Furry", "Monster", "Not Human"], curious_priority=False) # should be reconsidered!
    # Music related:
    $ gm.enter_location(has_tags=["swimsuit", "sfw"], has_no_tags=["beach", "sleeping"], curious_priority=False)
    if not "swimming_pool" in ilists.world_music:
        $ ilists.world_music["swimming_pool"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("swimming_pool")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["swimming_pool"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("swimming_pool"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg pool_inside
    with dissolve
    show screen swimming_pool
    
    if not global_flags.flag('visited_swimming_pool'):
        $ global_flags.set_flag('visited_swimming_pool')
        "Welcome to the swimming pool!"
        "It's not free, but they don't have sea monsters and big waves here, so it's perfect for a novice swimmer."
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    while 1:
        $ result = ui.interact()
        
        if result[0] == 'jump':
            $ gm.start_gm(result[1])
        
        if result[0] == 'control':
            if result[1] == 'return':
                hide screen city_beach
                jump city
                
                
screen swimming_pool():
    
        
    $ img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
    imagebutton:
        align (0.01, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("swimming_pool"), Jump("city_beach")]
    
    use location_actions("swimming_pool")
    $ img_swim_pool = ProportionalScale("content/gfx/interface/icons/sp_swimming.png", 90, 90)
    imagebutton:
        pos(290, 510)
        idle (img_swim_pool)
        hover (im.MatrixColor(img_swim_pool, im.matrix.brightness(0.15)))
        action [Hide("swimming_pool"), Jump("swimming_pool_swimming")]
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
        
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show("sfw", "swimsuit", "pool", exclude=["beach"], type="reduce", label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 