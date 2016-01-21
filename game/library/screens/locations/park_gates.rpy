label city_parkgates:
    $ gm.enter_location(goodtraits=["Elf", "Furry", "Human"], badtraits=["Aggressive", "Adventurer"], curious_priority=False)
    
    # Music related:
    if not "park" in ilists.world_music:
        $ ilists.world_music["park"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("park")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["park"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_parkgates"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_parkgates
    with dissolve
    show screen city_parkgates
    
    if not global_flags.flag('visited_park_gates'):
        $ global_flags.set_flag('visited_park_gates')
        "Gates to the park on city outskirts! Great place to meet people. "
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
        
    python:

        while True:

            result = ui.interact()

            if result[0] == 'jump':
                gm.start_gm(result[1])
                
            if result[0] == 'control':
                renpy.hide_screen("city_parkgates")
                if result[1] == 'jumppark':
                    jump('city_park')
                
                if result[1] == 'return':
                    break
                    
    $ renpy.music.stop(channel="world")
    hide screen city_parkgates
    jump city
    
                
screen city_parkgates():

    use top_stripe(True)
    
    use r_lightbutton(img=im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), return_value=['control', 'jumppark'], align=(0.99,0.5))
    
    use location_actions("city_parkgates")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            for entry in gm.display_girls():
          
                use rg_lightbutton(img=entry.show("girlmeets", "outdoors", "nature", "urban", exclude=["swimsuit", "wildness", "indoors", "stage", "beach", "pool", "onsen"], type="reduce", label_cache=True, resize=(300, 400)), return_value=['jump', entry])
