label city_parkgates:
    $ gm.enter_location(goodtraits=["Elf", "Furry", "Human"], badtraits=["Aggressive", "Adventurous"], curious_priority=False)
    $ coords = [[.1, .75], [.4, .67], [.9, .7]]
    # Music related:
    if not "park" in ilists.world_music:
        $ ilists.world_music["park"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("park")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["park"]) fadein .5
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
        $ block_say = True
        "Gates to the park on city outskirts. Great place to hit on girls or take a walk after lunch on a sunny day."
        $ block_say = False

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")

    while 1:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ gm.start_gm(result[1], img=result[1].show("girlmeets", "outdoors", "nature", "urban", exclude=["swimsuit", "wildness", "indoors", "stage", "beach", "pool", "onsen", "indoor"], type="reduce", label_cache=True, resize=I_IMAGE_SIZE, gm_mode=True))

        if result[0] == 'control':
            hide screen city_parkgates
            if result[1] == 'jumppark':
                $ jump('city_park')

            if result[1] == 'return':
                $ renpy.music.stop(channel="world")
                hide screen city_parkgates
                jump city




screen city_parkgates():

    use top_stripe(True)

    if not gm.show_girls:
        use r_lightbutton(img=im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), return_value=['control', 'jumppark'], align=(.99,0.5))

    use location_actions("city_parkgates")

    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")

        add "content/gfx/images/bg_gradient.webp" yalign .45

        for j, entry in enumerate(gm.display_girls()):
            hbox:
                align (coords[j])
                use rg_lightbutton(return_value=['jump', entry])
