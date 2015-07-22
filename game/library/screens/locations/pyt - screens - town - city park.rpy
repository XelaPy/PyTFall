label city_park:
    $ pytfall.gm.enter_location(goodtraits=["Psychic", "Impersonal"], badtraits=["Energetic", "Aggressive"])
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_park"):
            pytfall.world_actions.add("aine", "Find Aine", [Hide("pyt_city_park", transition=dissolve), Jump("aine_menu")], condition=Iff(global_flag_complex("met_aine")))
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_park
    with dissolve
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto") 
    
    show screen pyt_city_park
    
    python:
        while True:
            
            result = ui.interact()
            
            if result[0] == 'jump':
                pytfall.gm.start_gm(result[1])
            
            if result[0] == 'control':
                if result[1] == 'jumpgates':
                    global_flags.set_flag("keep_playing_music")
                    hs()

                    jump('city_parkgates')

                if result[1] == 'return':
                    break
                    
    $ global_flags.set_flag("keep_music_playing")
    hide screen pyt_city_park
    jump city_parkgates
    

screen pyt_city_park:
    
    use pyt_top_stripe(True)
    
    # use r_lightbutton(img=im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=true), return_value =['control', 'jumpgates'], align=(0.01, 0.5))
    
    $img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
    imagebutton:
        align (0.01, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("pyt_city_park"), Execute(global_flags.set_flag, "keep_playing_music"), Jump("city_parkgates")]
    
    
    use location_actions("city_park")
    
    if pytfall.gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5,0.3)
            spacing 70
            
            for entry in pytfall.gm.display_girls():
            # """
                    # if not entry.flag("city_park_tags") or entry.flag("city_park_tags")[0] < day:
                        # $city_park_tags_list = [] 
                        # # primary tags
                        # if entry.has_image("girl_meets","park"):
                            # $city_park_tags_list.append(("girl_meets","park"))
                        # # adding secondary tags at dice chance    
                        # if city_park_tags_list:    
                            # if entry.has_image("girl_meets","generic outdoor") and dice(40):
                                # $city_park_tags_list.append(("girl_meets","generic outdoor"))
                            # if entry.has_image("girl_meets","simple bg") and dice(40):
                                # $city_park_tags_list.append(("girl_meets","simple bg"))
                            # if entry.has_image("girl_meets","meadow") and dice(50):
                                # $city_park_tags_list.append(("girl_meets","meadow"))
                            # if entry.has_image("girl_meets","forest") and dice(50):
                                # $city_park_tags_list.append(("girl_meets","forest"))
                        # # secondary tags if no primary tags    
                        # if not city_park_tags_list:
                            # if entry.has_image("girl_meets","generic outdoor"):
                                # $city_park_tags_list.append(("girl_meets","generic outdoor"))
                            # if entry.has_image("girl_meets","simple bg"):
                                # $city_park_tags_list.append(("girl_meets","simple bg"))
                            # if entry.has_image("girl_meets","meadow"):
                                # $city_park_tags_list.append(("girl_meets","meadow"))
                            # if entry.has_image("girl_meets","forest"):
                                # $city_park_tags_list.append(("girl_meets","forest"))                                
                        # # giveup    
                        # if not city_park_tags_list:
                            # $city_park_tags_list.append(("girl_meets"))   
                        
                        # $ entry.set_flag("city_park_tags", (day, choice(city_park_tags_list)))
                    
                    # use r_lightbutton(img=entry.show(*entry.flag("city_park_tags")[1], exclude=["bikini", "swimsuit"], label_cache=True, resize=(300, 400)), return_value=['jump', entry])             
            # """
                    use rg_lightbutton(img=entry.show("generic outdoor", "park", "forest", "meadow", exclude=for_gm_selection + all_indoor_tags + water_selection + ["urban"], type="any", label_cache=True, resize=(300, 400)), return_value=['jump', entry])
                        
