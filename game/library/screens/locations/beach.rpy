label city_beach:
    $ gm.enter_location(goodtraits=["Energetic", "Exhibitionist"], badtraits=["Scars", "Undead", "Furry", "Monster", "Not Human"], curious_priority=False)
    # Music related:
    if not "beach_main" in ilists.world_music:
        $ ilists.world_music["beach_main"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("beach_main")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["beach_main"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_beach
    with dissolve
    show screen city_beach
    
    if not global_flags.flag('visited_city_beach'):
        $ global_flags.set_flag('visited_city_beach')
        "Welcome to the beach!"
        "Sand, sun and girls in bikinis, what else did you expect?"
        "Oh, we might have a kraken hiding somewhere as well :)"
    
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
                
                
screen city_beach():
    
    use top_stripe(True)
    
    # Jump buttons:
    $ img = im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80)
    imagebutton:
        id "meow"
        align (0.99, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("city_beach"), Jump("city_beach_right")]
        
    $ img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
    imagebutton:
        align (0.01, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("city_beach"), Function(global_flags.set_flag, "keep_playing_music"), Jump("city_beach_left")]
    
    use location_actions("city_beach")
    $ img_pool = ProportionalScale("content/gfx/interface/icons/swimming_pool.png", 60, 60)
    imagebutton:
        pos(1040, 80)
        idle (img_pool)
        hover (im.MatrixColor(img_pool, im.matrix.brightness(0.15)))
        action [Hide("city_beach"), Jump("swimming_pool")]
        
    $ img_beach_swim = ProportionalScale("content/gfx/interface/icons/sp_swimming.png", 90, 90)
    imagebutton:
        pos(280, 240)
        idle (img_beach_swim)
        hover (im.MatrixColor(img_beach_swim, im.matrix.brightness(0.15)))
        action [Hide("city_beach"), Show("city_beach_swim"), With(dissolve)]
        
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
        
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show("girlmeets", "swimsuit", "beach", exclude=["urban", "wildness", "suburb", "nature", "winter", "night", "formal", "indoor", "indoors"], type="reduce", label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
                
screen city_beach_swim():
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
                xysize (240, 40)
                yalign 0.5
                action [Hide("city_beach_swim"), Jump("city_beach_swimming_checks")]
                text "Swim" size 15
            button:
                xysize (240, 40)
                yalign 0.5
                action [Hide("city_beach_swim"), Show("city_beach"), With(dissolve)]
                text "Leave" size 15
                
label city_beach_swimming_checks:   
    if not global_flags.flag('swam_city_beach'):
        $ global_flags.set_flag('swam_city_beach')
        "The city is washed by the ocean. The water is quite warm all year round, but it can be pretty dangerous for a novice swimmers due to big waves and sea monsters."
        "Those who are not confident in their abilities prefer the local swimming pool, although it's not free unlike the sea."
        scene bg open_sea
        with dissolve
        "You stay in shallow water not too far from land to get used to the water. It feels nice, but the real swimming will require some skills next time."
    $ global_flags.set_flag("keep_playing_music")
    jump city_beach