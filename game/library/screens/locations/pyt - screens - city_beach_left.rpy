label city_beach_left:
    $ gm.enter_location()
    
    # Music related:
    if not "beach_main" in ilists.world_music:
        $ ilists.world_music["beach_main"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("beach_main")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["beach_main"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach_left"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_beach_left
    with dissolve
    show screen pyt_city_beach_left
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
        
    python:

        while True:

            result = ui.interact()

            if result[0] == 'jump':
                gm.start_gm(result[1])
            
            if result[0] == 'control':
                if result[1] == 'return':
                    break
                    
    $ global_flags.set_flag("keep_playing_music")
    hide screen pyt_city_beach_left
    jump city_beach
    
                
screen pyt_city_beach_left:

    use pyt_top_stripe(True)
    
    # Jump buttons:
    $img = ProportionalScale("content/gfx/interface/icons/beach_cafe.png", 80, 80)
    imagebutton:
        pos(380, 300)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("pyt_city_beach_left"), Jump("city_beach_cafe_main")]
        
    $img = im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80)
    imagebutton:
        align (0.99, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("pyt_city_beach_left"), Execute(global_flags.set_flag, "keep_playing_music"), Jump("city_beach")]    
    
    use location_actions("city_beach_left")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in gm.display_girls():
            # """
                    # if not entry.flag("beach_left_tags") or entry.flag("beach_left_tags")[0] < day:
                        # $beach_left_tags_list = []                    
                        # if entry.has_image("girl_meets","beach"):
                            # $beach_left_tags_list.append(("girl_meets","beach"))
                        # if entry.has_image("girl_meets","bikini","simple bg"):
                            # $beach_left_tags_list.append(("girl_meets","bikini","simple bg"))
                        # if entry.has_image("girl_meets","swimsuit","simple bg"):
                            # $beach_left_tags_list.append(("girl_meets","swimsuit","simple bg"))
                        # if entry.has_image("girl_meets","bikini","generic outdoor"):
                            # $beach_left_tags_list.append(("girl_meets","bikini","generic outdoor"))    
                        # if entry.has_image("girl_meets","swimsuit","generic outdoor"):
                            # $beach_left_tags_list.append(("girl_meets","swimsuit","generic outdoor")) 

                        # if not beach_left_tags_list:
                            # if entry.has_image("girl_meets","generic outdoor"):
                                # $beach_left_tags_list.append(("girl_meets","generic outdoor"))
                            # if entry.has_image("girl_meets","simple bg"):
                                # $beach_left_tags_list.append(("girl_meets","simple bg"))    
                            
                        # if not beach_left_tags_list:
                            # $beach_left_tags_list.append(("girl_meets"))   
                    
                        # $ entry.set_flag("beach_left_tags", (day, choice(beach_left_tags_list)))
            
                    # use r_lightbutton(img=entry.show(*entry.flag("beach_left_tags")[1], label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
            # """        
                    use rg_lightbutton(img=entry.show("bikini", "beach", "swimsuit", exclude=for_gm_selection + all_indoor_tags + ["pool", "onsen", "winter"], type="any", label_cache=True, resize=(300, 400)), return_value=['jump', entry])
