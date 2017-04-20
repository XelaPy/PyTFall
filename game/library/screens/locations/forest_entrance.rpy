label forest_entrance:
    $ gm.enter_location(goodtraits=["Furry", "Monster", "Scars", "Adventurous"], badtraits=["Homebody", "Coward", "Exhibitionist", "Human"], curious_priority=True)

    # Music related:
    if not "forest_entrance" in ilists.world_music:
        $ ilists.world_music["forest_entrance"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("forest_entrance")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["forest_entrance"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("forest_entrance"):
            pytfall.world_actions.add("peevish", "Find Peevish", Jump("peevish_menu"), condition=Iff(global_flag_complex("met_peevish")))
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg forest_entrance at truecenter
    show screen forest_entrance
    with dissolve
    
    if not global_flags.flag('visited_dark_forest'):
        $ global_flags.set_flag('visited_dark_forest')
        $ block_say = True
        "A dark, deep forest surrounds the city from the west. Only a few people live here, and even fewer are brave enough to step away far from city walls without a platoon of guards."
        $ block_say = False
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    while 1:
        
        $ result = ui.interact()
        
        if result[0] == 'jump':
            $ gm.start_gm(result[1])
        if result[0] == 'control':
            if result[1] == 'return':
                hide screen forest_entrance
                jump city
        elif result[0] == 'location':
            $ renpy.music.stop(channel="world")
            $ jump(result[1])
            
            
screen forest_entrance():

    use top_stripe(True)
    
    use location_actions("forest_entrance")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5,0.3)
            spacing 70
            
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show("girlmeets", "nature", "wildness", exclude=["urban", "winter", "night", "beach", "onsen", "dungeon", "stage", "swimsuit", "indoor", "formal"], type="reduce", label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
                    
    $ img_witch_shop = ProportionalScale("content/gfx/interface/icons/witch.png", 90, 90)
    imagebutton:
        pos(670, 490)
        idle (img_witch_shop)
        hover (im.MatrixColor(img_witch_shop, im.matrix.brightness(0.15)))
        action [Jump("witches_hut"), With(dissolve)]
