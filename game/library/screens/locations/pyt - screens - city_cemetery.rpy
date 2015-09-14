label graveyard_town:

    if not "cemetery" in ilists.world_music:
        $ ilists.world_music["cemetery"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("cemetery")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["cemetery"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("graveyard_town"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.finish()
            
    scene bg cemetery
    with dissolve
    show screen pyt_cemetery_entrance
        
    python:

        while True:

            result = ui.interact()

            if result[0] == 'jump':
                gm.start_gm(result[1])
            if result[0] == 'control':
                renpy.hide_screen("pyt_hiddenVillage_entrance")
                if result[1] == 'return':
                    break

    $ renpy.music.stop(channel="world")
    hide screen pyt_cemetery_entrance
    jump pyt_city
    
screen pyt_cemetery_entrance():

    use pyt_top_stripe(True)
    
    use location_actions("graveyard_town")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show('girlmeets', exclude=["swimsuit", "wildness", "beach", "pool", "urban", "stage","onsen", "indoors"], type="first_default",label_cache=True, resize=(300, 400)), return_value=['jump', entry])
