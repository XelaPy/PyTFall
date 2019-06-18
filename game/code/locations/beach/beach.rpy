label city_beach:
    $ gm.enter_location(goodtraits=["Energetic", "Exhibitionist"], badtraits=["Scars", "Undead", "Furry", "Monster", "Not Human"], curious_priority=False)
    $ coords = [[.14, .65], [.42, .6], [.85, .45]]

    # Music related:
    if not "beach_main" in ilists.world_music:
        $ ilists.world_music["beach_main"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("beach_main")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["beach_main"])
    $ global_flags.del_flag("keep_playing_music")

    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()

    scene bg city_beach
    with dissolve
    show screen city_beach

    if not global_flags.flag('visited_city_beach'):
        $ global_flags.set_flag('visited_city_beach')
        $ block_say = True
        "Welcome to the beach!"
        "Sand, sun, and girls in bikinis, what else did you expect?"
        "Oh, we might have a Kraken hiding somewhere as well :)"
        $ block_say = False

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")

    while 1:
        $ result = ui.interact()

        if result[0] == 'jump':
            $ girl = result[1]
            $ tags = girl.get_tags_from_cache(last_label)
            if not tags:
                $ img_tags = (["girlmeets", "beach"], ["girlmeets", "swimsuit", "simple bg"], ["girlmeets", "swimsuit", "no bg"])
                $ result = get_simple_act(girl, img_tags)
                if not result:
                    $ img_tags = (["girlmeets", "simple bg"], ["girlmeets", "no bg"])
                    $ result = get_simple_act(girl, img_tags)
                    if not result:
                        # giveup
                        $ result = ("girlmeets", "swimsuit")
                $ tags.extend(result)

            $ gm.start_gm(girl, img=girl.show(*tags, type="reduce", label_cache=True, resize=I_IMAGE_SIZE, gm_mode=True))

        if result[0] == 'control':
            if result[1] == 'return':
                hide screen city_beach
                jump city

screen city_beach():
    use top_stripe(True)
    if not gm.show_girls:
        # Jump buttons:
        $ img = im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80)
        imagebutton:
            align (.99, .5)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
            action [Hide("city_beach"), Jump("city_beach_right")]

        $ img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
        imagebutton:
            align (.01, .5)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
            action [Hide("city_beach"), Function(global_flags.set_flag, "keep_playing_music"), Jump("city_beach_left")]

        $ img_pool = ProportionalScale("content/gfx/interface/icons/swimming_pool.png", 60, 60)
        imagebutton:
            pos(1040, 80)
            idle (img_pool)
            hover (im.MatrixColor(img_pool, im.matrix.brightness(.15)))
            action [Hide("city_beach"), Jump("swimming_pool")]
            tooltip "Swimming Pool"

        $ img_beach_swim = ProportionalScale("content/gfx/interface/icons/sp_swimming.png", 90, 90)
        imagebutton:
            pos(280, 240)
            idle (img_beach_swim)
            hover (im.MatrixColor(img_beach_swim, im.matrix.brightness(.15)))
            action [Hide("city_beach"), Show("city_beach_swim"), With(dissolve)]
            tooltip "Swim"

    use location_actions("city_beach")

    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")

        add "content/gfx/images/bg_gradient.webp" yalign .45
        for j, entry in enumerate(gm.display_girls()):
            hbox:
                align (coords[j])
                use rg_lightbutton(return_value=['jump', entry])

screen city_beach_swim():
    style_prefix "dropdown_gm"
    frame:
        pos (.98, .98) anchor (1.0, 1.0)
        has vbox

        textbutton "Swim":
            action Hide("city_beach_swim"), Jump("city_beach_swimming_checks")

        if hero.get_skill("swimming") >= 150:
            textbutton "Diving":
                action Hide("city_beach_swim"), Jump("mc_action_city_beach_diving_checks")

        if global_flags.has_flag('swam_city_beach'):
            textbutton "About swimming":
                action Hide("city_beach_swim"), Jump("city_beach_about_swimming")

        textbutton "Leave":
            action Hide("city_beach_swim"), Show("city_beach"), With(dissolve)
            keysym "mousedown_3"

label city_beach_about_swimming:
    "By swimming here you can increase max constitution and, if you manage to avoid sea monsters, agility."
    "But you need high enough swimming skill. Consider practicing in the swimming pool first."
    "With high enough swimming skill you can try diving, where you can obtain some valuable items."
    $ global_flags.set_flag("keep_playing_music")
    jump city_beach

label city_beach_swimming_checks:

    if not global_flags.flag('swam_city_beach'):
        $ global_flags.set_flag('swam_city_beach')
        $ hero.set_flag("constitution_bonus_from_swimming_at_beach", value=0)
        "The water is quite warm all year round, but it can be pretty dangerous for novice swimmers due to big waves and sea monsters."
        "Those who are not confident in their abilities prefer the local swimming pool, although it's not free, unlike the sea."
        "In general, the swimming skill will increase faster in the ocean, unless you drown immediately due to low skill."
        scene bg open_sea
        with dissolve
        "You stay in shallow water not too far from land to get used to the water. It feels nice, but the real swimming will require some skills next time."
    else:
        if hero.vitality < 30:
            "You are too tired at the moment."
        elif hero.AP <= 0:
            "You don't have Action Points at the moment. Try again tomorrow."
        elif hero.health < hero.get_max("health")*.25:
            "You are too wounded at the moment."
        else:
            scene bg open_sea with dissolve
            jump mc_action_hero_ocean_skill_checks
    $ global_flags.set_flag("keep_playing_music")
    jump city_beach

label mc_action_hero_ocean_skill_checks:
    $ hero.AP -= 1
    if locked_dice(20):
        $ narrator ("A group of sea monsters surrounded you!")
        if hero.get_skill("swimming") < 50:
            if hero.health > 100 and locked_dice(75):
                $ narrator ("They managed to attack you a few times before you got a chance to react.")
                $ hero.health -= randint(15, 30)
            jump city_beach_monsters_fight
        elif hero.get_skill("swimming") < 200:
            jump city_beach_monsters_fight
        else:
            menu:
                "You are fast enough to avoid the fight."
                "Swim away":
                    $ narrator ("You quickly increase the distance between you and the monsters {color=[green]}(max agility +1){/color}.")
                    $ hero.swimming += randint(2, 4)
                    $ hero.stats.lvl_max["agility"] += 1
                    $ hero.stats.max["agility"] += 1
                    $ hero.mod_stat("agility", 1)
                "Fight":
                    jump city_beach_monsters_fight
    if hero.get_skill("swimming") < 50:
        if locked_dice(40):
            $ narrator ("You try to swim, but strong tide keeps you away {color=[red]}(no bonus to swimming skill this time){/color}.")
            $ narrator ("You need higher swimming skill to prevent it. Consider training in the swimming pool.")
        else:
            scene bg ocean_underwater with dissolve
            "Waves are pretty big today. You try fighting them, but quickly lose, pulling you under the water."
            $ narrator ("Nearly drowned, you get out of the ocean {color=[red]}(- health){/color}.")
            $ narrator ("You need higher swimming skill to prevent it. Consider training in the swimming pool.")
            $ hero.health = max(1, hero.health - 50)
            $ hero.swimming += randint(1, 2)
        $ hero.vitality -= randint (40, 50)
    elif hero.get_skill("swimming") < 100:
        "You try to swim, but rapid underwater currents make it very difficult for a novice swimmer."
        if locked_dice(10):
            scene bg ocean_underwater with dissolve
            "Waves are pretty big today. You try to fight them, but they win, sending you under the water."
            $ narrator ("You need higher swimming skill to prevent it. Consider training in the swimming pool.")
            $ narrator ("Nearly drowned, you get out of the ocean {color=[red]}(- health){/color}.")
            $ hero.health = max(1, hero.health - 50)
        $ hero.swimming += randint(4, 8)
        $ hero.vitality -= randint (30, 40)
    elif hero.get_skill("swimming") < 200:
        "You cautiously swim in the ocean, trying to stay close to the shore just in case."
        $ hero.swimming += randint(6, 12)
        $ hero.vitality -= randint (20, 30)
    else:
        "You take your time enjoying the water. Even big ocean waves are no match for your swimming skill."
        $ hero.swimming += randint(10, 15)
        $ hero.vitality -= randint (15, 25)
    if locked_dice(hero.get_skill("swimming")) and hero.flag("constitution_bonus_from_swimming_at_beach") <= 30:
        $ hero.stats.lvl_max["constitution"] += 1
        $ hero.stats.max["constitution"] += 1
        $ hero.mod_stat("constitution", 1)
        $ hero.set_flag("constitution_bonus_from_swimming_at_beach", value=hero.flag("constitution_bonus_from_swimming_at_beach")+1)
        $ narrator ("You feel more endurant than before {color=[green]}(max constitution +1){/color}.")

    $ global_flags.set_flag("keep_playing_music")
    jump city_beach

label city_beach_monsters_fight:
    hide screen city_beach
    hide screen city_beach_swim

    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        for i in range(randint(2, 3)):
            mob = build_mob(id="Skyfish", level=randint(5, 15))
            mob.be.front_row = True
            enemy_team.add(mob)
        back = interactions_pick_background_for_fight("beach")
        result = run_default_be(enemy_team, background=back, give_up="escape",
                                use_items=True)

    scene bg city_beach

    if result is True:
        python:
            for member in hero.team:
                member.exp += exp_reward(member, enemy_team)
    elif result is False:
        "The guards managed to drive away monsters, but your wounds are deep..."
    else:
        $ be_hero_escaped(hero.team)
        scene black
        pause 1.0
    jump city_beach

transform alpha_dissolve:
    alpha .0
    linear .5 alpha 1.0
    on hide:
        linear .5 alpha 0

screen diving_progress_bar(o2, max_o2): # oxygen bar for diving
    default oxigen = o2
    default max_oxigen = max_o2

    timer .1 repeat True action If(oxigen > 0, true=SetScreenVariable('oxigen', oxigen-1), false=(Hide("diving_progress_bar"), Return("All out of Air!")))
    key "mousedown_3" action (Hide("diving_progress_bar"), Return("Swim Out"))
    key "K_ESCAPE" action (Hide("diving_progress_bar"), Return("Swim Out"))
    if DEBUG:
        vbox:
            xalign .5
            text str(oxigen)
            text str(max_oxigen)
    vbox:
        xsize 300
        bar:
            right_bar im.Scale("content/gfx/interface/bars/oxigen_bar_empty.png", 300, 50)
            left_bar im.Scale("content/gfx/interface/bars/oxigen_bar_full.png", 300, 50)
            value oxigen
            range max_oxigen
            thumb None
            xysize (300, 50)
            at alpha_dissolve
        label "Find hidden items!" text_color gold text_size 18 xalign .5 yalign .5
        label "Right click or Esc to exit" text_color gold text_size 18 xalign .5 yalign .5

label mc_action_city_beach_diving_checks:

    if not hero.has_flag('vitality_bonus_from_diving_at_beach'):
         $ hero.set_flag("vitality_bonus_from_diving_at_beach", value=0)

    if not global_flags.flag('diving_city_beach'):
        $ global_flags.set_flag('diving_city_beach')
        "With high enough swimming skill you can try diving. The amount of oxygen is based on your swimming skill."
        "You need vitality to pick up items. Vitality is not consumed, but the more vitality you have in general, the more items you can pick up."
        "The goal is to find invisible items hidden on the seabed."
        "You can leave the sea anytime by clicking the right mouse button, and you will lose some health if you don't leave before the oxygen is over."
    if hero.AP <= 0:
        "You don't have Action Points at the moment. Try again tomorrow."
        jump city_beach
    elif hero.vitality < 20:
        "You're too tired at the moment."
        jump city_beach
    elif hero.health < hero.get_max("health")*.5:
        "You are too wounded at the moment."
        jump city_beach
    $ total_items_found = 0
    play world "underwater.mp3"
    $ hero.AP -= 1
    scene bg ocean_underwater_1 with dissolve
    if has_items("Snorkel Mask", [hero], equipped=True):
        $ i = int(hero.get_skill("swimming")+1) + 250
    else:
        $ i = int(hero.get_skill("swimming")+1)

    if has_items("Underwater Lantern", [hero], equipped=True):
        $ j = 120
    else:
        $ j = 40
    $ start_vitality = hero.vitality
    show screen diving_progress_bar(i, i)
    while hero.vitality > 10:
        if not renpy.get_screen("diving_progress_bar"):
            hide screen hidden_area
            "You've run out of air! (health -40)"
            $ hero.health = max(1, hero.health - 40)
            jump city_beach

        $ underwater_loot = tuple([choice(list(i for i in items.values() if "Diving" in i.locations and dice(i.chance) and hero.tier>=i.tier) or [False]), (j, j), (random.random(), random.random())] for i in range(4))
        show screen hidden_area(underwater_loot)

        $ result = ui.interact()

        if result == "All out of Air!":
            hide screen hidden_area
            "You've run out of air! {color=[red]}(health -40)"
            $ hero.health = max(1, hero.health - 40)
            jump city_beach
        elif result == "Swim Out":
            hide screen hidden_area
            "You return to the surface before you run out of air."
            jump city_beach

        if isinstance(result, Item):
            $ total_items_found += 1
            hide screen hidden_area
            $ item = result
            $ hero.add_item(item)
            $ our_image = ProportionalScale(item.icon, 150, 150)
            $ tkwargs = {"color": blue,
                               "outlines": [(1, black, 0, 0)]}
            $ gfx_overlay.notify("You caught %s!" % item.id, tkwargs=tkwargs)
            $ gfx_overlay.random_find(item, 'fishy')
            $ hero.vitality -= 5
        else:
            $ tkwargs = {"color": blue,
                               "outlines": [(1, black, 0, 0)]}
            $ gfx_overlay.notify("There is nothing there...", tkwargs=tkwargs)
            $ hero.vitality -= 10

    $ setattr(config, "mouse", None)
    hide screen hidden_area
    hide screen diving_progress_bar
    "You're too tired to continue!"
    $ hero.vitality = start_vitality
    $ hero.vitality -= randint(10, 20)
    $ del start_vitality
    if locked_dice(hero.get_skill("swimming")) and hero.flag("vitality_bonus_from_diving_at_beach") < 100 and total_items_found >= 10:
        $ hero.stats.lvl_max["vitality"] += 1
        $ hero.stats.max["vitality"] += 1
        $ hero.mod_stat("vitality", 1)
        $ hero.set_flag("vitality_bonus_from_diving_at_beach", value=hero.flag("vitality_bonus_from_diving_at_beach")+1)
        $ narrator ("You feel more endurant than before {color=[green]}(max vitality +1){/color}.")
    $ del total_items_found
    jump city_beach
