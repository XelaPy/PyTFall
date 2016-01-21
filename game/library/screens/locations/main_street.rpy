label main_street:
    $ gm.enter_location(goodtraits=["Human", "Kleptomaniac"], badtraits=["Not Human", "Alien", "Strange Eyes"], curious_priority=False)
    
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
    
    hide screen city_screen
    scene bg main_street at truecenter
    with dissolve
    
    show screen main_street
    with dissolve
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    python:

        while 1:

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
    hide screen main_street
    jump city

    
screen main_street():
    
    use top_stripe(True)
    
    use location_actions("main_street")
    
    # Girlsmeets screen
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show("girlmeets", "outdoors", "urban", exclude=["swimsuit", "indoors", "wildness", "suburb", "beach", "pool", "onsen", "nature"], label_cache=True, resize=(300, 400), type="reduce"), return_value=['jump', entry])

    # Normal screen
    else:
        for key in pytfall.maps("pytfall_ms"):
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
