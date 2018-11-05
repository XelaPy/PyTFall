label main_street:
    $ gm.enter_location(goodtraits=["Human", "Kleptomaniac"], badtraits=["Not Human", "Alien", "Strange Eyes"], curious_priority=False)
    $ coords = [[.1, .7], [.57, .54], [.93, .61]]
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

    $ global_flags.set_flag("visited_mainstreet", True)

    hide screen city_screen
    scene bg main_street at truecenter
    with dissolve

    show screen main_street
    with dissolve

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")

    while 1:

        $ result = ui.interact()

        if result[0] == 'control':
            if result[1] == 'return':
                $ global_flags.del_flag("keep_playing_music")
                hide screen main_street
                jump city

        elif result[0] == 'location':
            $ hs()
            $ jump(result[1])

        if result[0] == 'jump':
            $ gm.start_gm(result[1])


screen main_street():

    use top_stripe(True)

    use location_actions("main_street")

    if not gm.show_girls:
        $ img_tailor = ProportionalScale("content/gfx/interface/icons/tailor_shop.png", 50, 50)
        imagebutton:
            pos (245, 374)
            idle (img_tailor)
            hover (im.MatrixColor(img_tailor, im.matrix.brightness(.15)))
            action [Hide("main_street"), Jump("tailor_store")]
            tooltip "Tailor Shop"
        $ img_cafe = ProportionalScale("content/gfx/interface/icons/cafe_shop.png", 60, 60)
        imagebutton:
            pos (31, 540)
            idle (img_cafe)
            hover (im.MatrixColor(img_cafe, im.matrix.brightness(.15)))
            action [Hide("main_street"), Jump("cafe")]
            tooltip "Cafe"
        $ img_general = ProportionalScale("content/gfx/interface/icons/general_shop.png", 65, 65)
        imagebutton:
            pos (640, 360)
            idle (img_general)
            hover (im.MatrixColor(img_general, im.matrix.brightness(.15)))
            action [Hide("main_street"), Jump("general_store")]
            tooltip "General Store"
        $ img_workshop = ProportionalScale("content/gfx/interface/icons/work_shop.png", 50, 50)
        imagebutton:
            pos (90, 390)
            idle (img_workshop)
            hover (im.MatrixColor(img_workshop, im.matrix.brightness(.15)))
            action [Hide("main_street"), Jump("workshop")]
            tooltip "Workshop"
        $ img_realtor = ProportionalScale("content/gfx/interface/icons/realtor_shop.png", 50, 50)
        imagebutton:
            pos 245, 203
            idle (img_realtor)
            hover (im.MatrixColor(img_realtor, im.matrix.brightness(.15)))
            action [Hide("main_street"), Jump("realtor_agency")]
            tooltip "Real Estate Agency"
        $ img = "content/gfx/interface/icons/employment_agency.png"
        imagebutton:
            pos 245, 256
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
            action Jump("employment_agency")
            tooltip "Employment Agency"

    # Girlsmeets screen
    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")

        add "content/gfx/images/bg_gradient.webp" yalign .45
        $ j = 0

        for entry in gm.display_girls():
            hbox:
                align (coords[j])
                $ j += 1
                use rg_lightbutton(img=entry.show("girlmeets", "outdoors", "urban", exclude=["swimsuit", "indoor", "wildness", "suburb", "beach", "pool", "onsen", "nature"], label_cache=True, resize=(300, 400), type="reduce", gm_mode=True), return_value=['jump', entry])
