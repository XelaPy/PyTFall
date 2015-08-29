label hiddenVillage_entrance:

    if not "park" in ilists.world_music:
        $ ilists.world_music["park"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("park")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["park"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("hiddenVillage_entrance"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.add("hiddenvillage_matrix", "Explore", Jump("hidden_village_matrix"))
            pytfall.world_actions.finish()
            
    scene bg hidden_village
    with dissolve
    show screen pyt_hiddenVillage_entrance
    
    if not global_flags.flag('visited_hidden_village'):
        $ global_flags.set_flag('visited_hidden_village')
        "From now on you have an access to the hidden village."
        
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
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
    hide screen pyt_city_parkgates
    jump pyt_city
    
screen pyt_hiddenVillage_entrance():

    use pyt_top_stripe(True)
    
    use location_actions("hiddenVillage_entrance")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show('girlmeets', exclude=["swimsuit", "wildness", "beach", "pool", "urban", "stage","onsen", "indoors"], type="first_default",label_cache=True, resize=(300, 400)), return_value=['jump', entry])
                
label Karin:
    $ gm.start("girl_meets", chars["Karin"], chars["Karin"].get_vnsprite(), "hiddenVillage_entrance", "girl_room_12")
    
label hidden_village_matrix:
    call screen poly_matrix("library/events/StoryI/coordinates_hidden_village.json", show_exit_button=(0.8, 0.8))
    if not(_return):
        jump hiddenVillage_entrance
    # if _return == "House_5" and not chars["Karin"].flag('Karin_intro'):
        # chars["Karin"].set_flag("Karin_intro", value="True")
        # jump karin_first_meeting
    if _return == "House_5":
        # show bg girl_room_12 with dissolve
        # $ gm.start("girl_meets", chars["Karin"],  chars["Karin"].get_vnsprite(), "hiddenVillage_entrance", "girl_room_12")
        jump Karin
    "Result: [_return]"
    jump hidden_village_matrix