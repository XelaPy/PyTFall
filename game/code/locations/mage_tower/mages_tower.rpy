#Angelica

label mages_tower:
    $ gm.enter_location(goodtraits=["Psychic"], badtraits=["Indifferent"], goodoccupations=["Caster"], badoccupations=["SIW"], curious_priority=True)
    
    # Music related:
    if not "mages_tower" in ilists.world_music:
        $ ilists.world_music["mages_tower"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("mages_tower")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["mages_tower"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("mages_tower"):
            pytfall.world_actions.add("angelica", "Find Angelica", Jump("angelica_menu"), condition=Iff(global_flag_complex("met_angelica")))
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg mages_tower
    with dissolve
    show screen mages_tower
    
    if not global_flags.flag('visited_mages_tower'):
        $ global_flags.set_flag('visited_mages_tower')
        "Real mages, other practitioners of Arcane Arts and some plain weirdos hang around here."
        "Try not to get yourself blown up :)"
    if not global_flags.flag("met_angella"):
        if not global_flags.flag('mt_counter'):
            $ global_flags.set_flag('mt_counter', 1)
        else:    
            $ global_flags.set_flag('mt_counter', global_flags.flag('mt_counter') + 1)
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    while 1:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ gm.start_gm(result[1])
        
        if result[0] == 'control':
            if result[1] == 'return':
                hide screen mages_tower
                jump city
                
                
screen mages_tower():
    
    use top_stripe(True)
    
    use location_actions("mages_tower")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show("girlmeets", "urban",  exclude=["swimsuit", "beach", "pool", "urban", "stage", "onsen", "indoors", "indoor"], type="reduce", label_cache=True, resize=(300, 400)), return_value=['jump', entry])
