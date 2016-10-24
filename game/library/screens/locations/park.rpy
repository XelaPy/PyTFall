label city_park:
    $ gm.enter_location(goodtraits=["Elf", "Furry"], badtraits=["Aggressive", "Adventurous"], curious_priority=False)
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_park"):
            pytfall.world_actions.add("aine", "Find Aine", [Hide("city_park", transition=dissolve), Jump("aine_menu")], condition=Iff(global_flag_complex("met_aine")))
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_park
    with dissolve
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto") 
    
    show screen city_park
    
    while 1:
        
        $ result = ui.interact()
        
        if result[0] == 'jump':
            $ gm.start_gm(result[1])
        
        if result[0] == 'control':
            if result[1] == 'jumpgates':
                $ global_flags.set_flag("keep_playing_music")
                $ hs()
                $ jump('city_parkgates')

            if result[1] == 'return':
                $ global_flags.set_flag("keep_music_playing")
                hide screen city_park
                jump city_parkgates
                
                
screen city_park():
    
    use top_stripe(True)
    
    # use r_lightbutton(img=im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=true), return_value =['control', 'jumpgates'], align=(0.01, 0.5))
    
    $img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
    imagebutton:
        align (0.01, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("city_park"), Function(global_flags.set_flag, "keep_playing_music"), Jump("city_parkgates")]
    
    
    use location_actions("city_park")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5,0.3)
            spacing 70
            
            for entry in gm.display_girls():

                    use rg_lightbutton(img=entry.show("girlmeets", "outdoors", "nature", "urban", exclude=["swimsuit", "wildness", "indoors", "stage", "beach", "pool", "onsen", "indoor"], type="reduce", label_cache=True, resize=(300, 400)), return_value=['jump', entry])
                        
