label city_beach_cafe:
    $ gm.enter_location(goodtraits=["Athletic", "Dawdler"], badtraits=['Scars', "Alien","Not Human"])
    
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
                gm.start_gm(result[1])
            
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
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in gm.display_girls():
                    if not entry.flag("beach_cafe_tags") or entry.flag("beach_cafe_tags")[0] < day:
                        $beach_cafe_tags_list = []  

                        if entry.has_image("girlmeets","simple bg"):
                            $beach_cafe_tags_list.append(("girlmeets","simple bg"))    
                        if entry.has_image("girlmeets","outdoors"):
                            $beach_cafe_tags_list.append(("girlmeets","outdoors"))   
                        # giveup    
                        if not beach_cafe_tags_list:
                            $beach_cafe_tags_list.append(("girlmeets"))   
                        
                        $ entry.set_flag("beach_cafe_tags", (day, choice(beach_cafe_tags_list)))
                    
                    use rg_lightbutton(img=entry.show(*entry.flag("beach_cafe_tags")[1], exclude=["urban", "wildness", "suburb", "nature", "winter", "night"], type="first_default", label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
