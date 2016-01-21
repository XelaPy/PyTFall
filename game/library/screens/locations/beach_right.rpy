label city_beach_right:
    $ gm.enter_location(goodtraits=["Not Human", "Alien"], badtraits=["Shy", "Coward", "Homebody", "Human"], curious_priority=False)
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach_right"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_beach_right
    with dissolve
    show screen city_beach_right
    
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
    hide screen city_beach_right
    jump city_beach
    
                
screen city_beach_right:

    use top_stripe(True)
    
    $img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
    imagebutton:
        align (0.01, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("city_beach_right"), Function(global_flags.set_flag, "keep_playing_music"), Jump("city_beach")]
    
    use location_actions("city_beach_right")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in gm.display_girls():

                    if not entry.flag("beach_right_tags") or entry.flag("beach_right_tags")[0] < day:
                        $beach_right_tags_list = []
                        # main set
                        if entry.has_image("girlmeets","beach"):
                            $beach_right_tags_list.append(("girlmeets","beach"))
                        if entry.has_image("girlmeets","swimsuit","simple bg"):
                            $beach_right_tags_list.append(("girlmeets","swimsuit","simple bg"))
                        if entry.has_image("girlmeets","swimsuit","outdoors"):
                            $beach_right_tags_list.append(("girlmeets","swimsuit","outdoors"))                                   
                        # secondary set if nothing found
                        if not beach_right_tags_list:
                            if entry.has_image("girlmeets","outdoors"):
                                $beach_right_tags_list.append(("girlmeets","outdoors"))
                            if entry.has_image("girlmeets","simple bg"):
                                $beach_right_tags_list.append(("girlmeets","simple bg"))    
                        # giveup    
                        if not beach_right_tags_list:
                            $beach_right_tags_list.append(("girlmeets"))   
                    
                        $ entry.set_flag("beach_right_tags", (day, choice(beach_right_tags_list)))
            
                    use rg_lightbutton(img=entry.show(*entry.flag("beach_right_tags")[1], exclude=["urban", "wildness", "suburb", "nature", "winter", "night"], type="first_default", label_cache=True, resize=(300, 400)), return_value=['jump', entry])             
