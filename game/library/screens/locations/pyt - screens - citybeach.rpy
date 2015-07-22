label city_beach:
    $ pytfall.gm.enter_location(goodtraits=["Athletic", "Tomboy", "Not Human", "Exhibitionnist"], badtraits=['Old Scars', "Shy", "Sensitive"])
    
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
    show screen pyt_city_beach
    
    if not global_flags.flag('visited_city_beach'):
        $ global_flags.set_flag('visited_city_beach')
        "Welcome to the beach!"
        "Sand, sun and girls in bikinis, what else did you expect?"
        "Oh, we might have a kraken hiding somewhere as well :)"
    
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
    
    hide screen pyt_city_beach
    jump pyt_city
    

screen pyt_city_beach:
    
    use pyt_top_stripe(True)
    
    # Jump buttons:
    $img = im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80)
    imagebutton:
        id "meow"
        align (0.99, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("pyt_city_beach"), Jump("city_beach_right")]
        
    $img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
    imagebutton:
        align (0.01, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("pyt_city_beach"), Execute(global_flags.set_flag, "keep_playing_music"), Jump("city_beach_left")]
    
    use location_actions("city_beach")
    
    if pytfall.gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in pytfall.gm.display_girls():
            # """
                    # if not entry.flag("beach_tags") or entry.flag("beach_tags")[0] < day:
                        # $citybeach_tags_list = [] 
                        # # primary tags
                        # if entry.has_image("girl_meets","beach"):
                            # $citybeach_tags_list.append(("girl_meets","beach"))
                        # if entry.has_image("girl_meets","bikini","simple bg"):
                            # $citybeach_tags_list.append(("girl_meets","bikini","simple bg"))
                        # if entry.has_image("girl_meets","swimsuit","simple bg"):
                            # $citybeach_tags_list.append(("girl_meets","swimsuit","simple bg"))
                        # if entry.has_image("girl_meets","bikini","generic outdoor"):
                            # $citybeach_tags_list.append(("girl_meets","bikini","generic outdoor"))    
                        # if entry.has_image("girl_meets","swimsuit","generic outdoor"):
                            # $citybeach_tags_list.append(("girl_meets","swimsuit","generic outdoor")) 
                        # # secondary tags if no primary tags
                        # if not citybeach_tags_list:
                            # if entry.has_image("girl_meets","generic outdoor"):
                                # $citybeach_tags_list.append(("girl_meets","generic outdoor"))
                            # if entry.has_image("girl_meets","simple bg"):
                                # $citybeach_tags_list.append(("girl_meets","simple bg"))    
                        # # giveup    
                        # if not citybeach_tags_list:
                            # $citybeach_tags_list.append(("girl_meets"))   
                        
                        # $ entry.set_flag("beach_tags", (day, choice(citybeach_tags_list)))
                    
                    # use r_lightbutton(img=entry.show(*entry.flag("beach_tags")[1], label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
            # """        
                    use rg_lightbutton(img=entry.show("bikini", "beach", "swimsuit", exclude=for_gm_selection + all_indoor_tags + ["pool", "onsen", "winter"], type="any", label_cache=True, resize=(300, 400)), return_value=['jump', entry])
    
