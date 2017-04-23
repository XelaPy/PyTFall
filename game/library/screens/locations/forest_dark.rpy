label forest_dark:

    # Music related:
    if not "forest_entrance" in ilists.world_music:
        $ ilists.world_music["forest_entrance"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("forest_entrance")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["forest_entrance"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("forest_entrance"):
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
        n = randint(1, 4)
    scene expression "content/gfx/bg/locations/forest_" + str(n) + ".jpg"
    with dissolve
    
    if not global_flags.flag('visited_deep_forest'):
        $ global_flags.set_flag('visited_deep_forest')
        $ block_say = True
        "You step away from the city walls and go deep into the forest. It's not safe here, better to be on guard."
        $ block_say = False
    
    show screen city_dark_forest
    
    while 1:
        $ result = ui.interact()
        
        if result[0] == 'jump':
            $ gm.start_gm(result[1])
        if result[0] == 'control':
            if result[1] == 'return':
                hide screen city_dark_forest
                $ global_flags.set_flag("keep_playing_music")
                jump forest_entrance
        elif result[0] == 'location':
            $ renpy.music.stop(channel="world")
            $ jump(result[1])
            
screen city_dark_forest():

    use top_stripe(True)
    frame:
        xalign 0.95
        ypos 20
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_group "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_dark_forest"), Jump("city_dark_forest_explore"), With(dissolve)]
                text "Explore" size 15
                
label city_dark_forest_explore:
    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        your_team = Team(name="Your Team", max_size=3)
        for j in range(randint(1, 3)):
            mob = build_mob(id="Undead Rat", level=15)
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
        place = interactions_pick_background_for_fight("forest")
        result = run_default_be(enemy_team, background=place, slaves=True, prebattle=False, death=True, skill_lvl=3)
    jump forest_dark