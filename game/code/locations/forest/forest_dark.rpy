label forest_dark:
    python:
        background_number = -1
        forest_bg_change = True
        # Build the actions
        if pytfall.world_actions.location("forest_entrance"):
            pytfall.world_actions.finish()

label forest_dark_continue:
    if forest_bg_change:
        $ background_number_list = list(i for i in range(1, 7) if i != background_number)
        $ background_number = choice(background_number_list)
        $ forest_location = "content/gfx/bg/locations/forest_" + str(background_number) + ".webp"
    else:
        $ forest_bg_change = True
    scene expression forest_location
    with dissolve

    # Music related:
    if not "forest_entrance" in ilists.world_music:
        $ ilists.world_music["forest_entrance"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("forest_entrance")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["forest_entrance"])
    $ global_flags.del_flag("keep_playing_music")

    if not hero.flag('visited_deep_forest'):
        $ hero.set_flag('visited_deep_forest')
        $ block_say = True
        "You step away from the city walls and go deep into the forest. It's not safe here, better to be on guard."
        $ block_say = False

    show screen city_dark_forest

    while 1:
        $ result = ui.interact()

        if result in hero.team:
            $ came_to_equip_from = "forest_dark_continue"
            $ eqtarget = result
            $ global_flags.set_flag("keep_playing_music")
            $ equipment_safe_mode = True
            $ forest_bg_change = False

            hide screen city_dark_forest
            jump char_equip

screen city_dark_forest():
    use top_stripe(False, None, False, True)

    frame:
        xalign .95
        ypos 50
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        padding 10, 10
        vbox:
            style_group "wood"
            align (.5, .5)
            spacing 10
            button:
                xysize (120, 40)
                yalign .5
                action [Hide("city_dark_forest"), Jump("city_dark_forest_explore"), With(dissolve)]
                text "Explore" size 15
            button:
                xysize (120, 40)
                yalign .5
                action [Hide("city_dark_forest"), Jump("mc_action_city_dark_forest_rest"), With(dissolve), SensitiveIf(hero.flag("dark_forest_rested_today") != day)]
                text "Rest" size 15
            if hero.has_flag("found_old_ruins"):
                button:
                    xysize (120, 40)
                    yalign .5
                    action [Hide("city_dark_forest"), Jump("city_dark_forest_ruines_part"), With(dissolve)]
                    text "Ruins" size 15
            button:
                xysize (120, 40)
                yalign .5
                action [Hide("city_dark_forest"), Jump("forest_entrance"), With(dissolve)]
                text "Leave" size 15

    key "mousedown_3" action [Hide("city_dark_forest"), Jump("forest_entrance"), With(dissolve)]

label city_dark_forest_explore:
    if not(take_team_ap(1)):
        if len(hero.team) > 1:
            "Unfortunately, your team is too tired at the moment. Maybe another time."
        else:
            "Unfortunately, you are too tired at the moment. Maybe another time."

        "Each member of your party should have at least 1 AP."

        $ global_flags.set_flag("keep_playing_music")
        $ forest_bg_change = False
        jump forest_dark_continue
    else:
        if hero.flag("dark_forest_found_river") != day and hero.vitality < hero.get_max("vitality") and dice(35):
            jump mc_action_city_dark_forest_river
        elif not hero.has_flag("found_old_ruins") and day >= 10 and dice(50):
            $ hero.set_flag("found_old_ruins")
            hide screen city_dark_forest
            jump storyi_start
        elif dice(20) and hero.flag("dark_forest_met_girl") != day:
            jump dark_forest_girl_meet
        elif dice(70) or hero.flag("dark_forest_met_bandits") == day:
            jump city_dark_forest_fight
        else:
            $ hero.set_flag("dark_forest_met_bandits", value=day)
            jump city_dark_forest_hideout

label city_dark_forest_ruines_part:
    if not(take_team_ap(2)):
        if len(hero.team) > 1:
            "Unfortunately, your team is too tired to explore dungeons. Maybe another time."
        else:
            "Unfortunately, you are too tired to explore dungeons. Maybe another time."

        "Each member of your party should have at least 2 AP."

        $ global_flags.set_flag("keep_playing_music")
        jump forest_dark_continue
    else:
        hide screen city_dark_forest
        jump storyi_start

label mc_action_city_dark_forest_rest:
    $ hero.set_flag("dark_forest_rested_today", value=day)
    $ forest_bg_change = False
    scene bg camp
    with dissolve

    "You take a short rest before moving on, restoring mp and vitality."
    $ forest_bg_change = False
    $ global_flags.set_flag("keep_playing_music")

    python:
        for i in hero.team:
            i.vitality += int(i.get_max("vitality")*.25)
            i.health += int(i.get_max("health")*.05)
            i.mp += int(i.get_max("mp")*.2)
    jump forest_dark_continue

label city_dark_forest_hideout:
    hide screen city_dark_forest
    scene bg forest_hideout
    with dissolve

    $ forest_bg_change = False

    menu:
        "You found bandits hideout inside an old abandoned castle."

        "Attack them":
            "You carefully approach the hideout when a group of bandits attacks you."
        "Leave them be":
            show screen city_dark_forest
            $ global_flags.set_flag("keep_playing_music")
            jump forest_dark_continue

    call city_dark_forest_hideout_fight from _call_city_dark_forest_hideout_fight
    if result is None:
        $ be_hero_escaped(hero.team)
        scene black
        pause 1.0
        jump forest_dark_continue

    $ N = randint(1, 3)
    $ j = 0
    while j < N:
        scene bg forest_hideout
        with dissolve

        "Another group is approaching you!"

        call city_dark_forest_hideout_fight from _call_city_dark_forest_hideout_fight_1
        if result is None:
            $ be_hero_escaped(hero.team)
            scene black
            pause 1.0
            jump forest_dark_continue

        $ j += 1

    # Could be wrong... but this looks like double :(
    # if persistent.battle_results:
    #     call screen give_exp_after_battle(hero.team, exp)

    show screen city_dark_forest
    scene bg forest_hideout
    with dissolve

    "After killing all bandits, you found stash with loot."

    $ give_to_mc_item_reward(type="loot", price=300)
    if locked_dice(50):
        $ give_to_mc_item_reward(type="loot", price=300)
    $ give_to_mc_item_reward(type="restore", price=100)
    if locked_dice(50):
        $ give_to_mc_item_reward(type="restore", price=200)
    if locked_dice(50):
        $ give_to_mc_item_reward(type="armor", price=300)
    if locked_dice(50):
        $ give_to_mc_item_reward(type="weapon", price=300)
    jump forest_dark_continue

label city_dark_forest_hideout_fight:
    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        levels = randint(20, 40)
        for i in range(3):
            mob_id = choice(["Samurai", "Warrior", "Archer", "Soldier", "Barbarian", "Orc", "Infantryman", "Thug", "Mercenary", "Dark Elf Archer"])
            mob = build_mob(id=mob_id, level=levels)
            mob.controller = Complex_BE_AI(mob)
            enemy_team.add(mob)

    $ place = interactions_pick_background_for_fight("forest")
    $ result = run_default_be(enemy_team, background=place,
                              slaves=True, prebattle=False,
                              death=False, give_up="escape",
                              use_items=True)
    if result is True:
        scene expression forest_location
        if persistent.battle_results:
            call screen give_exp_after_battle(hero.team, enemy_team)
    elif result is False:
        jump game_over
    return

label city_dark_forest_fight:
    $ forest_bg_change = False

    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        levels = hero.team.get_level()
        levels = randint(levels-5, levels+10)
        levels = min(5, levels)
        mob = choice(["slime", "were", "harpy", "goblin", "wolf", "bear",
                      "druid", "rat", "undead", "butterfly"])
        et_len = min(len(hero.team) + 1, 3)

    if mob == "slime":
        "You encountered a small group of predatory slimes."
        python:
            for i in range(et_len):
                mob_id = choice(["Alkaline Slime", "Slime", "Acid Slime"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = Complex_BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "were":
        "Hungry shapeshifters want a piece of you."
        python:
            for i in range(et_len):
                mob_id = choice(["Werecat", "Werewolf", "Weregirl"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = Complex_BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "harpy":
        "A flock of wild harpies attempts to protect their territory."
        python:
            for i in range(et_len):
                mob_id = choice(["Harpy", "Vixen"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = Complex_BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "goblin":
        "You find yourself surrounded by a group of goblins."
        python:
            for i in range(3):
                mob_id = choice(["Goblin", "Goblin Archer", "Goblin Warrior", "Goblin Shaman"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = Complex_BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "wolf":
        "A pack of wolves picks you for dinner."
        python:
            for i in range(3):
                mob_id = choice(["Wolf", "Black Wolf"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = Complex_BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "bear":
        "You disturbed an angry bear."
        python:
            for i in range(et_len-1):
                mob_id = choice(["Bear", "Beargirl"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = Complex_BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "druid":
        "Forest fanatics attempt to sacrifice you in the name of «mother nature» or something like that."
        python:
            for i in range(et_len):
                mob_id = choice(["Druid", "Wild Dryad"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = Complex_BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "rat":
        "A pack of foul-smelling rats picks you for dinner."
        python:
            for i in range(et_len):
                mob_id = "Undead Rat"
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = Complex_BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "undead":
        "A group of decayed skeletons rise from the ground."
        python:
            for i in range(3):
                mob_id = choice(["Skeleton", "Skeleton Warrior"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = Complex_BE_AI(mob)
                enemy_team.add(mob)
    else:
        "You encountered a small group of aggressive giant butterflies."
        python:
            for i in range(et_len):
                mob_id = "Black Butterfly"
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = Complex_BE_AI(mob)
                enemy_team.add(mob)

    $ place = interactions_pick_background_for_fight("forest")
    $ result = run_default_be(enemy_team, background=place,
                              slaves=True, prebattle=False,
                              death=False, give_up="escape",
                              use_items=True)

    if result is True:
        scene expression forest_location
        $ item = get_item_drops(["loot", "scrolls", "consumables",
                                 "potions", "restore"], tier=hero.tier)
        if item:
            $ gfx_overlay.random_find(item, 'items')
            $ hero.add_item(item)

        if persistent.battle_results:
            call screen give_exp_after_battle(hero.team, enemy_team)

        jump forest_dark_continue
    elif result is False:
        jump game_over
    else:
        $ be_hero_escaped(hero.team)
        scene black
        pause 1.0
        jump forest_dark_continue

label dark_forest_girl_meet:
    $ hero.set_flag("dark_forest_met_girl", value=day)
    python:
        choices = list(i for i in chars.values() if
                       str(i.location) == "City" and
                       i not in hero.chars and
                       not i.arena_active and
                       i not in gm.get_all_girls())
    $ badtraits = ["Homebody", "Indifferent", "Coward"]
    $ choices = list(i for i in choices if not any(trait in badtraits for trait in i.traits))
    if choices:
        $ character = random.choice(choices)
        $ spr = character.get_vnsprite()
        show expression spr at center with dissolve
        "You found a girl lost in the woods and escorted her to the city."
        $ character.override_portrait("portrait", "happy")
        $ character.show_portrait_overlay("love", "reset")
        $ character.say("She happily kisses you in the chick as a thanks. Maybe you should try to find her in the city later.")
        if character.disposition < 450:
            $ character.disposition += 100
        else:
            $ character.disposition += 50
        hide expression spr with dissolve
        $ character.restore_portrait()
        $ character.hide_portrait_overlay()
        $ global_flags.set_flag("keep_playing_music")
        jump forest_dark_continue

label mc_action_city_dark_forest_river:
    play world "forest_lake.ogg"
    $ global_flags.set_flag("keep_playing_music")
    $ hero.set_flag("dark_forest_found_river", value=day)
    $ forest_bg_change = False
    scene bg forest_lake
    with dissolve
    "You found a river. Fresh, clean water restores some of your vitality."
    python:
        for i in hero.team:
            i.vitality += int(i.get_max("vitality")*.5)
    jump forest_dark_continue
