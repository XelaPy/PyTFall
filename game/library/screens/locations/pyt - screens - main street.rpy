label main_street:
    $ gm.enter_location(goodtraits=["Professional Maid", "Kleptomaniac", "Noble"], badtraits=["Not Human", "Alien", "Artificial Body"])
    
    # Music related:
    if not "main_street" in ilists.world_music:
        $ ilists.world_music["main_street"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("main_street")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["main_street"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("main_street"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    hide screen pyt_city_screen
    scene bg main_street at truecenter
    with dissolve
    
    show screen pyt_main_street
    with dissolve
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    python:

        while True:

            result = ui.interact()

            if result[0] == 'control':
                if result[1] == 'return':
                    break

            elif result[0] == 'location':
                hs()
                jump(result[1])

            if result[0] == 'jump':
                gm.start_gm(result[1])

    $ global_flags.del_flag("keep_playing_music")            
    hide screen pyt_main_street
    jump pyt_city

    
screen pyt_main_street:
    
    use pyt_top_stripe(True)
    
    use location_actions("main_street")
    
    # Girlsmeets screen
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            for entry in gm.display_girls():
            # """
                    # if not entry.flag("main_street_tags") or entry.flag("main_street_tags")[0] < day:
                        # $main_street_tags_list = []
                        # # primary tags
                        # if entry.has_image("girl_meets","urban"):
                            # $main_street_tags_list.append(("girl_meets","urban"))
                        # if entry.has_image("girl_meets","shop"):
                            # $main_street_tags_list.append(("girl_meets","shop")) 
                        # # adding secondary tags at dice chance
                        # if main_street_tags_list:
                            # if entry.has_image("girl_meets","generic indoor") and dice(40):
                                # $main_street_tags_list.append(("girl_meets","generic indoor"))
                            # if entry.has_image("girl_meets","road") and dice(40):
                                # $main_street_tags_list.append(("girl_meets","road"))    
                            # if entry.has_image("girl_meets","generic outdoor") and dice(40):
                                # $main_street_tags_list.append(("girl_meets","generic outdoor"))
                            # if entry.has_image("girl_meets","simple bg") and dice(40):
                                # $main_street_tags_list.append(("girl_meets","simple bg"))
                        # # secondary tags if no primary tags    
                        # if not main_street_tags_list:
                            # if entry.has_image("girl_meets","generic indoor"):
                                # $main_street_tags_list.append(("girl_meets","generic indoor"))
                            # if entry.has_image("girl_meets","road"):
                                # $main_street_tags_list.append(("girl_meets","road"))    
                            # if entry.has_image("girl_meets","generic outdoor"):
                                # $main_street_tags_list.append(("girl_meets","generic outdoor"))
                            # if entry.has_image("girl_meets","simple bg"):
                                # $main_street_tags_list.append(("girl_meets","simple bg"))    
                        # # giveup    
                        # if not main_street_tags_list:
                            # $main_street_tags_list.append(("girl_meets"))   
                        
                        # $ entry.set_flag("main_street_tags", (day, choice(main_street_tags_list)))
                    
                    # use r_lightbutton(img=entry.show(*entry.flag("main_street_tags")[1], exclude=["bikini", "swimsuit"], label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
            # """        
                    use rg_lightbutton(img=entry.show('profile', exclude=for_gm_selection + water_selection + ["forest", "meadow", "ruin", "wilderness", "arena", "bathroom", "bedroom", "classroom", "kitchen", "stage"], label_cache=True, resize=(300, 400), type="any"), return_value=['jump', entry])

    # Normal screen
    else:
        for key in pytfall.maps['MainStreet']:
            python:
                map_point = pytfall.maps['MainStreet'][key]['attr']
                x = int(map_point['x']) / float(config.screen_width)
                y = int(map_point['y']) / float(config.screen_height)
                if "rx" in map_point:
                    rx = map_point["rx"]
                    ry = map_point["rx"]
                else:
                    rx = 25
                    ry = 25
                    
            use r_lightbutton(img=ProportionalScale(map_point['image'], rx, ry), return_value=['location', key], align=(x, y))
            frame background Frame(Transform(im.Twocolor("content/gfx/frame/ink_box.png", white, grey), alpha=0.5), 5, 5):
                align (x, y+0.05)
                text (u"{size=-4}{color=[black]}%s"%(map_point['name']))
                

