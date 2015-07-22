label city_beach_right:
    $ pytfall.gm.enter_location(goodtraits=["Not Human", "Exhibitionnist"])
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach_right"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_beach_right
    with dissolve
    show screen pyt_city_beach_right
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
        
    python:

        while True:

            result = ui.interact()

            if result[0] == 'jump':
                pytfall.gm.start_gm(result[1])
            
            if result[0] == 'control':
                if result[1] == 'return':
                    break
                    
    $ global_flags.set_flag("keep_playing_music")
    hide screen pyt_city_beach_right
    jump city_beach
    
                
screen pyt_city_beach_right:

    use pyt_top_stripe(True)
    
    $img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
    imagebutton:
        align (0.01, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("pyt_city_beach_right"), Execute(global_flags.set_flag, "keep_playing_music"), Jump("city_beach")]
    
    use location_actions("city_beach_right")
    
    if pytfall.gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in pytfall.gm.display_girls():
            # """
                    # if not entry.flag("beach_right_tags") or entry.flag("beach_right_tags")[0] < day:
                        # $beach_right_tags_list = []                    
                        # if entry.has_image("girl_meets","beach"):
                            # $beach_right_tags_list.append(("girl_meets","beach"))
                        # if entry.has_image("girl_meets","bikini","simple bg"):
                            # $beach_right_tags_list.append(("girl_meets","bikini","simple bg"))
                        # if entry.has_image("girl_meets","swimsuit","simple bg"):
                            # $beach_right_tags_list.append(("girl_meets","swimsuit","simple bg"))
                        # if entry.has_image("girl_meets","bikini","generic outdoor"):
                            # $beach_right_tags_list.append(("girl_meets","bikini","generic outdoor"))    
                        # if entry.has_image("girl_meets","swimsuit","generic outdoor"):
                            # $beach_right_tags_list.append(("girl_meets","swimsuit","generic outdoor"))
                        # if entry.has_image("girl_meets","summer","simple bg"):
                            # $beach_right_tags_list.append(("girl_meets","summer","simple bg"))
                        # if entry.has_image("girl_meets","summer","generic outdoor"):
                            # $beach_right_tags_list.append(("girl_meets","summer","generic outdoor"))                                    

                        # if not beach_right_tags_list:
                            # if entry.has_image("girl_meets","generic outdoor"):
                                # $beach_right_tags_list.append(("girl_meets","generic outdoor"))
                            # if entry.has_image("girl_meets","simple bg"):
                                # $beach_right_tags_list.append(("girl_meets","simple bg"))    
                            
                        # if not beach_right_tags_list:
                            # $beach_right_tags_list.append(("girl_meets"))   
                    
                        # $ entry.set_flag("beach_right_tags", (day, choice(beach_right_tags_list)))
            
                    # use r_lightbutton(img=entry.show(*entry.flag("beach_right_tags")[1], label_cache=True, resize=(300, 400)), return_value=['jump', entry])             
            # """
                    use rg_lightbutton(img=entry.show("bikini", "beach", "swimsuit", "summer", exclude=for_gm_selection + all_indoor_tags + ["pool", "onsen", "winter"], type="any", label_cache=True, resize=(300, 400)), return_value=['jump', entry])
