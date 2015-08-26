label forest_entrance:
    $ gm.enter_location(goodtraits=["Not Human", "Courageous", "Alien","Scars","Adventurer"], badtraits=["Homebody", "Coward", "Exhibitionist"])

    # Music related:
    if not "forest_entrance" in ilists.world_music:
        $ ilists.world_music["forest_entrance"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("forest_entrance")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["forest_entrance"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("forest_entrance"):
            pytfall.world_actions.add("peevish", "Find Peevish", Jump("peevish_menu"), condition=Iff(global_flag_complex("met_peevish")))
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg forest_entrance at truecenter
    show screen pyt_forest_entrance
    with dissolve
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    python:

        while 1:
            result = ui.interact()
            if result[0] == 'jump':
                gm.start_gm(result[1])
            if result[0] == 'control':
                if result[1] == 'return':
                    break
            elif result[0] == 'location':
                renpy.music.stop(channel="world")
                jump(result[1])
                
    hide screen pyt_forest_entrance
    jump pyt_city
    return


screen pyt_forest_entrance:

    use pyt_top_stripe(True)
    
    use location_actions("forest_entrance")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5,0.3)
            spacing 70
            
            for entry in gm.display_girls():
                    if not entry.flag("forest_entrance_tags") or entry.flag("forest_entrance_tags")[0] < day:
                        $forest_entrance_tags_list = []
                        
                        if entry.has_image("girlmeets","outdoors"):
                            $forest_entrance_tags_list.append(("girlmeets","outdoors"))
                        # adding with dice chance
                        if forest_entrance_tags_list:    
                            if entry.has_image("girlmeets","simple bg") and dice(50):
                                $forest_entrance_tags_list.append(("girlmeets","simple bg"))
                        #and without if empty    
                        if not forest_entrance_tags_list:
                            if entry.has_image("girlmeets","simple bg"):
                                $forest_entrance_tags_list.append(("girlmeets","simple bg"))   
                        # giveup    
                        if not forest_entrance_tags_list:
                            $forest_entrance_tags_list.append(("girlmeets"))   
                        
                        $ entry.set_flag("forest_entrance_tags", (day, choice(forest_entrance_tags_list)))
                    
                    use rg_lightbutton(img=entry.show(*entry.flag("forest_entrance_tags")[1], exclude=["urban", "wildness", "suburb", "winter", "swimsuit"], type="first_default",label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 

    for key in pytfall.maps("pytfall_fe"):
        if not key.get("hidden", False):
            if "img" in key:
                python:
                    rx = int(key["rx"]) if "rx" in key else 25
                    ry = int(key["ry"]) if "ry" in key else 25
                    x = int(key['x']) / float(config.screen_width)
                    y = int(key['y']) / float(config.screen_height)
                use r_lightbutton(img=ProportionalScale(key['img'], rx, ry), return_value=['location', key["id"]], align=(x, y))
                frame:
                    background Frame(Transform(im.Twocolor("content/gfx/frame/ink_box.png", white, grey), alpha=0.5), 5, 5)
                    align (x, y+0.05)
                    text (u"%s"%(key['name'])) size 16 color black
