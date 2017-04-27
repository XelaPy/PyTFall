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
        forest_location = "content/gfx/bg/locations/forest_" + str(n) + ".jpg"
    scene expression forest_location
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
    jump city_dark_forest_fight

label city_dark_forest_fight:
    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        levels = 0
        for i in hero.team:
            levels += i.level
        levels = int(levels/len(hero.team))
        mob = choice(["slime", "were", "harpy", "goblin", "wolf", "bear", "druid", "rat", "undead", "butterfly"])
    if mob == "slime":
        "You encountered a small group of predatory slimes."
        python:
            for i in range(randint(2, 3)):
                mod_id = choice(["Alkaline Slime", "Slime", "Acid Slime"])
                mob = build_mob(id=mod_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "were":
        "A hungry shapeshifters want a piece of you."
        python:
            for i in range(randint(2, 3)):
                mod_id = choice(["Werecat", "Werewolf", "Weregirl"])
                mob = build_mob(id=mod_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "harpy":
        "A flock of wild harpies attempts to protects their territory."
        python:
            for i in range(randint(2, 3)):
                mod_id = choice(["Harpy", "Vixen", "Weregirl"])
                mob = build_mob(id=mod_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "goblin":
        "You find yourself surrounded by a group of goblins."
        python:
            for i in range(3):
                mod_id = choice(["Goblin", "Goblin Archer", "Goblin Warrior", "Goblin Shaman"])
                mob = build_mob(id=mod_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "wolf":
        "A pack of wolves picks you for dinner."
        python:
            for i in range(3):
                mod_id = choice(["Wolf", "Black Wolf"])
                mob = build_mob(id=mod_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "bear":
        "You disturbed an angry bear."
        python:
            mod_id = choice(["Bear", "Beargirl"])
            mob = build_mob(id=mod_id, level=levels)
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
    elif mob == "druid":
        "Forest fanatics attempt to sacrifice you in the name of «mother nature» or something like that."
        python:
            for i in range(randint(2, 3)):
                mod_id = choice(["Druid", "Wild Dryad"])
                mob = build_mob(id=mod_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "rat":
        "A pack of foul-smelling rats picks you for dinner."
        python:
            for i in range(randint(2, 3)):
                mod_id = "Undead Rat"
                mob = build_mob(id=mod_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "rat":
        "A pack of foul-smelling rats picks you for dinner."
        python:
            for i in range(3):
                mod_id = choice(["Skeleton", "Skeleton Warrior"])
                mob = build_mob(id=mod_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    else:
        "You encountered a small group of aggressive giant butterflies."
        python:
            for i in range(randint(2, 3)):
                mod_id = "Black Butterfly"
                mob = build_mob(id=mod_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    $ place = interactions_pick_background_for_fight("forest")
    $ result = run_default_be(enemy_team, background=place, slaves=True, prebattle=False, death=True)
    if result is True:
        python:
            for member in hero.team:
                member.exp += 150
        scene expression forest_location
        show screen give_exp_after_battle(hero.team)
        pause 2.0
        hide screen give_exp_after_battle
        jump forest_dark
    else:
        jump game_over