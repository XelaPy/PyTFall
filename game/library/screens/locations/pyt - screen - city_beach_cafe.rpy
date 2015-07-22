label city_beach_cafe:
    $ pytfall.gm.enter_location()
    
    $ global_flags.set_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach_cafe"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_beach_cafe
    with dissolve
    show screen pyt_city_beach_cafe
    
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
                    
    hide screen pyt_city_beach_cafe
    jump city_beach_cafe_main
    
                
screen pyt_city_beach_cafe:

    use pyt_top_stripe(True)
    
    $img = im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80)
    imagebutton:
        align (0.99, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("pyt_city_beach_cafe"), Jump("city_beach_cafe_main")]
    
    use location_actions("city_beach_cafe")
    
    if pytfall.gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in pytfall.gm.display_girls():
            # """
                    # if not entry.flag("beach_cafe_tags") or entry.flag("beach_cafe_tags")[0] < day:
                        # $beach_cafe_tags_list = []  
                        # # primary tags
                        # if entry.has_image("girl_meets","bikini","simple bg"):
                            # $beach_cafe_tags_list.append(("girl_meets","bikini","simple bg"))
                        # if entry.has_image("girl_meets","swimsuit","simple bg"):
                            # $beach_cafe_tags_list.append(("girl_meets","swimsuit","simple bg"))
                        # if entry.has_image("girl_meets","bikini","generic outdoor"):
                            # $beach_cafe_tags_list.append(("girl_meets","bikini","generic outdoor"))    
                        # if entry.has_image("girl_meets","swimsuit","generic outdoor"):
                            # $beach_cafe_tags_list.append(("girl_meets","swimsuit","generic outdoor"))
                        # if entry.has_image("girl_meets","summer","simple bg"):
                            # $beach_cafe_tags_list.append(("girl_meets","summer","simple bg"))
                        # if entry.has_image("girl_meets","summer","generic outdoor"):
                            # $beach_cafe_tags_list.append(("girl_meets","summer","generic outdoor"))
                        # if entry.has_image("girl_meets","casual","simple bg"):
                            # $beach_cafe_tags_list.append(("girl_meets","casual","simple bg"))
                        # if entry.has_image("girl_meets","casual","generic outdoor"):
                            # $beach_cafe_tags_list.append(("girl_meets","casual","generic outdoor"))    
                        # # adding secondary tags at dice chance
                        # if beach_cafe_tags_list:
                            # if entry.has_image("girl_meets","generic outdoor") and dice(40):
                                # $beach_cafe_tags_list.append(("girl_meets","generic outdoor"))
                            # if entry.has_image("girl_meets","simple bg") and dice(40):
                                # $beach_cafe_tags_list.append(("girl_meets","simple bg")) 
                        # # secondary tags if no primary tags
                        # if not beach_cafe_tags_list:
                            # if entry.has_image("girl_meets","generic outdoor"):
                                # $beach_cafe_tags_list.append(("girl_meets","generic outdoor"))
                            # if entry.has_image("girl_meets","simple bg"):
                                # $beach_cafe_tags_list.append(("girl_meets","simple bg"))    
                        # # giveup    
                        # if not beach_cafe_tags_list:
                            # $beach_cafe_tags_list.append(("girl_meets"))   
                        
                        # $ entry.set_flag("beach_cafe_tags", (day, choice(beach_cafe_tags_list)))
                    
                    # use r_lightbutton(img=entry.show(*entry.flag("beach_cafe_tags")[1], label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
            # """                    
                    use rg_lightbutton(img=entry.show('bikini', "swimsuit", "summer", "casual", exclude=for_gm_selection + all_indoor_tags + ["ruin", "wilderness", "meadow", "forest", "winter"], type="any", label_cache=True, resize=(300, 400)), return_value=['jump', entry])
