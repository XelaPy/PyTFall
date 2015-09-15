label academy_town:

    if not "library" in ilists.world_music:
        $ ilists.world_music["library"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("library")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["library"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("academy_town"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.add("library_matrix", "Read the books", Jump("library_read_matrix"))
            pytfall.world_actions.finish()
            
    scene bg library
    with dissolve
    show screen pyt_academy_town_entrance
        
    python:

        while True:

            result = ui.interact()

            if result[0] == 'jump':
                gm.start_gm(result[1])
            if result[0] == 'control':
                renpy.hide_screen("pyt_academy_town_entrance")
                if result[1] == 'return':
                    break

    $ renpy.music.stop(channel="world")
    hide screen pyt_cemetery_entrance
    jump pyt_city
    
screen pyt_academy_town_entrance():

    use pyt_top_stripe(True)
    
    use location_actions("academy_town")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show('girlmeets', exclude=["swimsuit", "wildness", "beach", "pool", "urban", "stage","onsen", "indoors"], type="first_default",label_cache=True, resize=(300, 400)), return_value=['jump', entry])
label library_read_matrix:
    hide screen pyt_academy_town_entrance
    scene bg library
    call screen poly_matrix("library/screens/locations/coordinates_library.json", show_exit_button=(1.0, 1.0))
    if not(_return):
        jump academy_town