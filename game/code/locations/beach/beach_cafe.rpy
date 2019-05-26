label city_beach_cafe:
    $ gm.enter_location(goodtraits=["Athletic", "Dawdler", "Always Hungry"], badtraits=["Scars", "Undead", "Furry", "Monster"], curious_priority=False)
    $ coords = [[.2, .75], [.5, .65], [.87, .6]]
    $ global_flags.set_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach_cafe"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_beach_cafe
    with dissolve
    show screen city_beach_cafe
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
        
    while 1:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ girl = result[1]
            $ tags = girl.get_tags_from_cache(last_label)
            if not tags:
                $ img_tags = (["girlmeets", "beach"], ["girlmeets", "swimsuit", "simple bg"], ["girlmeets", "swimsuit", "no bg"], ["girlmeets", "swimsuit", "outdoors"])
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
                hide screen city_beach_cafe
                jump city_beach_cafe_main


screen city_beach_cafe:

    use top_stripe(True)
    if not gm.show_girls:
        $ img = im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80)
        imagebutton:
            align (.99, .5)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
            action [Hide("city_beach_cafe"), Jump("city_beach_cafe_main")]
    
    use location_actions("city_beach_cafe")
    
    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")
    
        add "content/gfx/images/bg_gradient.webp" yalign .45
    
        for j, entry in enumerate(gm.display_girls()):
            hbox:
                align (coords[j])
                use rg_lightbutton(return_value=['jump', entry])