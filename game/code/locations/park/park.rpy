label city_park:
    $ gm.enter_location(goodtraits=["Elf", "Furry"], badtraits=["Aggressive", "Adventurous"], curious_priority=False)
    $ coords = [[.1, .7], [.4, .45], [.74, .73]]
    python:
        # Build the actions
        if pytfall.world_actions.location("city_park"):
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
            $ gm.start_gm(result[1], img=result[1].show("girlmeets", "outdoors", "nature", "urban", exclude=["swimsuit", "wildness", "indoors", "stage", "beach", "pool", "onsen", "indoor"], type="reduce", label_cache=True, resize=(300, 400), gm_mode=True))

        if result[0] == 'control':
            if result[1] == 'jumpgates':
                $ global_flags.set_flag("keep_playing_music")
                $ clear_screens()
                $ jump('city_parkgates')

            if result[1] == 'return':
                $ global_flags.set_flag("keep_playing_music")
                hide screen city_park
                jump city_parkgates


screen city_park():

    use top_stripe(True)

    # use r_lightbutton(img=im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=true), return_value =['control', 'jumpgates'], align=(.01, .5))

    if not gm.show_girls:
        $ img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
        imagebutton:
            align (.01, .5)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
            action [Hide("city_park"), Function(global_flags.set_flag, "keep_playing_music"), Jump("city_parkgates")]

    use location_actions("city_park")

    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")
        add "content/gfx/images/bg_gradient.webp" yalign .45
        for j, entry in enumerate(gm.display_girls()):
            hbox:
                align (coords[j])
                use rg_lightbutton(return_value=['jump', entry])

    if not gm.show_girls:
        if global_flags.has_flag("met_aine"):
            $ img_aine_shop = ProportionalScale("content/gfx/interface/icons/aine.png", 75, 75)
            imagebutton:
                pos (1090, 340)
                idle (img_aine_shop)
                hover (im.MatrixColor(img_aine_shop, im.matrix.brightness(.15)))
                action [Hide("city_park"), Jump("aine_menu"), With(dissolve)]
