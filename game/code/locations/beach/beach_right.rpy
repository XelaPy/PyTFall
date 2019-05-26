label city_beach_right:
    $ gm.enter_location(goodtraits=["Not Human", "Alien"], badtraits=["Shy", "Coward", "Homebody", "Human"], curious_priority=False)
    $ coords = [[.4, .9], [.6, .8], [.9, .7]]
    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach_right"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_beach_right
    with dissolve
    show screen city_beach_right
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
        
    while 1:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ girl = result[1]
            $ tags = girl.get_tags_from_cache(last_label)
            if not tags:
                $ img_tags = (["girlmeets", "beach"], ["girlmeets", "swimsuit", "simple bg"], ["girlmeets", "swimsuit", "no bg"])
                $ result = get_simple_act(girl, img_tags)
                if not result:
                    $ img_tags = (["girlmeets", "simple bg"], ["girlmeets", "no bg"])
                    $ result = get_simple_act(girl, img_tags)
                    if not result:
                        # giveup
                        $ result = ("girlmeets", "swimsuit")
                $ tags.extend(result)

            $ gm.start_gm(girl, img=girl.show(*tags, type="reduce", label_cache=True, resize=I_IMAGE_SIZE, gm_mode=True))

        if result[0] == 'control':
            if result[1] == 'return':
                $ global_flags.set_flag("keep_playing_music")
                hide screen city_beach_right
                jump city_beach


screen city_beach_right():

    use top_stripe(True)
    if not gm.show_girls:
        $img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
        imagebutton:
            align (.01, .5)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
            action [Hide("city_beach_right"), Function(global_flags.set_flag, "keep_playing_music"), Jump("city_beach")]
    
    use location_actions("city_beach_right")

    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")

        add "content/gfx/images/bg_gradient.webp" yalign .45
        
        for j, entry in enumerate(gm.display_girls()):
            hbox:
                align (coords[j])
                use rg_lightbutton(return_value=['jump', entry])
