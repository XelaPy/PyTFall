label city_beach_cafe_main:
    $ gm.enter_location(goodtraits=["Athletic", "Dawdler", "Always Hungry"], badtraits=["Scars", "Undead", "Furry", "Monster"], curious_priority=False)
    $ coords = [[.15, .75], [.5, .6], [.9, .8]]
    # Music related:
    if not "beach_cafe" in ilists.world_music:
        $ ilists.world_music["beach_cafe"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("beach_cafe")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["beach_cafe"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach_cafe_main"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_beach_cafe_main
    with dissolve
    show screen city_beach_cafe_main
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
        
    while 1:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ gm.start_gm(result[1])
        
        if result[0] == 'control':
            if result[1] == 'return':
                hide screen city_beach_cafe_main
                jump city_beach_left
                    
                    
screen city_beach_cafe_main:

    use top_stripe(True)
    if not gm.show_girls:
        # Jump buttons:
        $img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
        imagebutton:
            align (.01, .5)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
            action [Hide("city_beach_cafe_main"), Function(global_flags.del_flag, "keep_playing_music"), Jump("city_beach_cafe")]
        
        $img = im.Scale(im.Flip("content/gfx/interface/buttons/blue_arrow_up.png", vertical=True), 80, 70)
        imagebutton:
            align (.5, .99)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
            action [Hide("city_beach_cafe_main"), Jump("city_beach_left")]        
    
    use location_actions("city_beach_cafe_main")
    
    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")
    
        add "content/gfx/images/bg_gradient.webp" yalign .45
    
        $ j = 0
        for entry in gm.display_girls():
            hbox:
                align (coords[j])
                $ j += 1
                use rg_lightbutton(img=entry.show("girlmeets", "swimsuit", "beach", exclude=["urban", "wildness", "suburb", "nature", "winter", "night", "formal", "indoor"], type="reduce", label_cache=True, resize=(300, 400), gm_mode=True), return_value=['jump', entry])