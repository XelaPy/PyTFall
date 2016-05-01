label forest_entrance:
    $ gm.enter_location(goodtraits=["Furry", "Monster", "Scars", "Adventurer"], badtraits=["Homebody", "Coward", "Exhibitionist", "Human"], curious_priority=True)

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
    show screen forest_entrance
    with dissolve
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    while 1:
        
        $ result = ui.interact()
        
        if result[0] == 'jump':
            $ gm.start_gm(result[1])
        if result[0] == 'control':
            if result[1] == 'return':
                hide screen forest_entrance
                jump city
        elif result[0] == 'location':
            $ renpy.music.stop(channel="world")
            $ jump(result[1])
            
            
screen forest_entrance():

    use top_stripe(True)
    
    use location_actions("forest_entrance")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5,0.3)
            spacing 70
            
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show("girlmeets", "nature", "wildness", exclude=["urban", "winter", "night", "beach", "onsen", "dungeon", "stage", "swimsuit", "indoor", "formal"], type="reduce", label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
               

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
