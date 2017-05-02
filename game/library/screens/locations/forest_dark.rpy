label forest_dark:

    python:
        # Build the actions
        if pytfall.world_actions.location("forest_entrance"):
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
        background_number = randint(1, 6)
        forest_location = "content/gfx/bg/locations/forest_" + str(background_number) + ".jpg"
    scene expression forest_location
    with dissolve
    
label forest_dark_continue:
    # Music related:
    if not "forest_entrance" in ilists.world_music:
        $ ilists.world_music["forest_entrance"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("forest_entrance")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["forest_entrance"])
    $ global_flags.del_flag("keep_playing_music")
    

    
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

    frame:
        xalign 0.95
        ypos 50
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
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_dark_forest"), Jump("city_dark_forest_rest"), With(dissolve), SensitiveIf(hero.flag("dark_forest_rested_today") != day)]
                text "Rest" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_dark_forest"), Jump("city_dark_forest_hideout"), With(dissolve)]
                text "Test Bandits" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_dark_forest"), Jump("city_dark_forest_fight"), With(dissolve)]
                text "Test Fight" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_dark_forest"), Jump("forest_entrance"), With(dissolve)]
                text "Leave" size 15
                
label city_dark_forest_explore:
    if not(take_team_ap(1)):
        "Unfortunately your team is too tired at the moment. Maybe another time."
        jump forest_dark_continue
    $ background_number_list = list(i for i in range(1, 7) if i != background_number)
    $ background_number = choice(background_number_list)
    $ forest_location = "content/gfx/bg/locations/forest_" + str(background_number) + ".jpg"
    scene expression forest_location
    with dissolve
    $ global_flags.set_flag("keep_playing_music")
    jump forest_dark_continue
    
label city_dark_forest_rest:
    $ hero.set_flag("dark_forest_rested_today", value=day)
    scene bg camp
    with dissolve
    "You take a short rest before moving on"
    python:
        for i in hero.team:
            i.vitality += 25
            i.health += 5
            i.mp += 10
    jump forest_dark_continue
    
label city_dark_forest_hideout:
    hide screen city_dark_forest
    scene bg forest_hideout
    with dissolve
    menu:
        "You found bandits hideout inside an old abandoned castle."
        
        "Attack them":
            $ pass
        "Leave them be":
            show screen city_dark_forest
            jump city_dark_forest_explore
    call city_dark_forest_hideout_fight
    $ N = randint(1, 4)
    while i < N:
        scene bg forest_hideout
        with dissolve
        "Another group is approaching you!"
        call city_dark_forest_hideout_fight
        $ i += 1
    show screen give_exp_after_battle(hero.team)
    pause 2.5
    hide screen give_exp_after_battle
    show screen city_dark_forest
    scene bg forest_hideout
    with dissolve
    "After killing all the bandits you found stash with loot."
    call give_to_mc_item_reward(type="loot", price=300)
    if locked_dice(50):
        call give_to_mc_item_reward(type="loot", price=300)
    call give_to_mc_item_reward(type="restore", price=100)
    if locked_dice(50):
        call give_to_mc_item_reward(type="restore", price=200)
    if locked_dice(50):
        call give_to_mc_item_reward(type="armor", price=300)
    if locked_dice(50):
        call give_to_mc_item_reward(type="weapon", price=300)
    jump city_dark_forest_explore

label city_dark_forest_hideout_fight:
    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        levels = 0
        for i in hero.team:
            levels += i.level
        levels = int(levels/len(hero.team))+randint(0, 5)
        levels = 1
        for i in range(3):
            mob_id = choice(["Samurai", "Warrior", "Archer", "Soldier", "Barbarian", "Orc", "Infantryman", "Thug", "Mercenary", "Dark Elf Archer"])
            mob = build_mob(id=mob_id, level=levels)
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
    $ place = interactions_pick_background_for_fight("forest")
    $ result = run_default_be(enemy_team, background=place, slaves=True, prebattle=False, death=True)
    if result is True:
        python:
            for member in hero.team:
                member.exp += 250
        scene expression forest_location
        return

        
label city_dark_forest_fight:
    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        levels = 0
        for i in hero.team:
            levels += i.level
        levels = int(levels/len(hero.team))+randint(0, 5)
        mob = choice(["slime", "were", "harpy", "goblin", "wolf", "bear", "druid", "rat", "undead", "butterfly"])
    if mob == "slime":
        "You encountered a small group of predatory slimes."
        python:
            for i in range(randint(2, 3)):
                mob_id = choice(["Alkaline Slime", "Slime", "Acid Slime"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "were":
        "A hungry shapeshifters want a piece of you."
        python:
            for i in range(randint(2, 3)):
                mob_id = choice(["Werecat", "Werewolf", "Weregirl"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "harpy":
        "A flock of wild harpies attempts to protects their territory."
        python:
            for i in range(randint(2, 3)):
                mob_id = choice(["Harpy", "Vixen"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "goblin":
        "You find yourself surrounded by a group of goblins."
        python:
            for i in range(3):
                mob_id = choice(["Goblin", "Goblin Archer", "Goblin Warrior", "Goblin Shaman"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "wolf":
        "A pack of wolves picks you for dinner."
        python:
            for i in range(3):
                mob_id = choice(["Wolf", "Black Wolf"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "bear":
        "You disturbed an angry bear."
        python:
            mob_id = choice(["Bear", "Beargirl"])
            mob = build_mob(id=mob_id, level=levels)
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
    elif mob == "druid":
        "Forest fanatics attempt to sacrifice you in the name of «mother nature» or something like that."
        python:
            for i in range(randint(2, 3)):
                mob_id = choice(["Druid", "Wild Dryad"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "rat":
        "A pack of foul-smelling rats picks you for dinner."
        python:
            for i in range(randint(2, 3)):
                mob_id = "Undead Rat"
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "rat":
        "A pack of foul-smelling rats picks you for dinner."
        python:
            for i in range(3):
                mob_id = choice(["Skeleton", "Skeleton Warrior"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    else:
        "You encountered a small group of aggressive giant butterflies."
        python:
            for i in range(randint(2, 3)):
                mob_id = "Black Butterfly"
                mob = build_mob(id=mob_id, level=levels)
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
        pause 2.5
        hide screen give_exp_after_battle
        jump forest_dark_continue
    else:
        jump game_over