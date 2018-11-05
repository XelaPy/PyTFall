label swimming_pool:
    $ gm.enter_location(has_tags=["swimsuit", "sfw"], has_no_tags=["beach", "sleeping"], curious_priority=False)
    if not "swimming_pool" in ilists.world_music:
        $ ilists.world_music["swimming_pool"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("swimming_pool")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["swimming_pool"])
    $ global_flags.del_flag("keep_playing_music")

    python:
        if pytfall.world_actions.location("swimming_pool"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    scene bg swimming_pool
    with dissolve

    if not global_flags.flag('visited_swimming_pool'):
        $ global_flags.set_flag('visited_swimming_pool')
        $ block_say = True
        show expression npcs["Henry_beach"].get_vnsprite() as henry
        $ h = npcs["Henry_beach"].say
        h "Welcome to the swimming pool!"
        h "It's not free, but we don't have sea monsters and big waves here, so it's perfect for a novice swimmer!"
        h "We also provide swimming lessons at a reasonable price. Feel free to ask anytime!"
        $ block_say = False
        hide henry
    show screen swimming_pool
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    while 1:
        $ result = ui.interact()

        if result[0] == 'jump':
            $ gm.start_gm(result[1])

        if result[0] == 'control':
            if result[1] == 'return':
                hide screen swimming_pool
                jump city_beach


screen swimming_pool():
    use top_stripe(True)

    $ img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
    imagebutton:
        align (.01, .5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(.15)))
        action [Hide("swimming_pool"), Jump("city_beach")]

    use location_actions("swimming_pool")
    $ img_swim_pool = ProportionalScale("content/gfx/interface/icons/sp_swimming.png", 90, 90)
    imagebutton:
        pos(290, 510)
        idle (img_swim_pool)
        hover (im.MatrixColor(img_swim_pool, im.matrix.brightness(.15)))
        action [Hide("swimming_pool"), Show("swimmong_pool_swim"), With(dissolve)]

    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")

        add "content/gfx/images/bg_gradient.webp" yalign .45

        hbox:
            align(.5, .3)
            spacing 70

            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show("sfw", "swimsuit", "pool", exclude=["beach"], type="reduce", label_cache=True, resize=(300, 400), gm_mode=True), return_value=['jump', entry])

screen swimmong_pool_swim():
    style_prefix "dropdown_gm"
    frame:
        pos (.98, .98) anchor (1.0, 1.0)
        has vbox
        textbutton "Swim (10 G)":
            action Hide("swimmong_pool_swim"), Jump("single_swim_pool")
        textbutton "Hire an instructor (50 G)":
            action Hide("swimmong_pool_swim"), Jump("instructor_swim_pool")
        if hero.get_skill("swimming") >= 100:
            textbutton "Work as instructor":
                action Hide("swimmong_pool_swim"), Jump("mc_action_work_swim_pool")
        textbutton "Leave":
            action Hide("swimmong_pool_swim"), Show("swimming_pool"), With(dissolve)
            keysym "mousedown_3"


label single_swim_pool:
    if hero.vitality < 20 or hero.AP <= 0:
        "You are too tired at the moment."
    elif hero.health < hero.get_max("health")*.5:
        "You are too wounded at the moment."
    elif hero.take_money(10, reason="Swimming Pool"):
        play world "underwater.mp3"
        scene bg pool_swim
        with dissolve
        call mc_action_swimming_pool_skill_checks from _call_mc_action_swimming_pool_skill_checks
    else:
        "You don't have enough gold."
    jump swimming_pool

label instructor_swim_pool:
    if hero.vitality < 20 or hero.AP <= 0:
        "You are too tired at the moment."
    elif hero.health < hero.get_max("health")*.5:
        "You are too wounded at the moment."
    elif hero.take_money(50, reason="Swimming Pool"):
        play world "underwater.mp3"
        scene bg pool_swim
        with dissolve
        call mc_action_instructor_swimming_pool_skill_checks from _call_mc_action_instructor_swimming_pool_skill_checks
    else:
        "You don't have enough gold."
    jump swimming_pool

label mc_action_swimming_pool_skill_checks:
    $ hero.AP -= 1
    if hero.get_skill("swimming") < 20:
        if locked_dice(60):
            "You barely stay afloat. Clearly, more practice is needed."
            $ hero.swimming += randint(1,2)
        else:
            "You can barely stay afloat. After a while, you lose your cool and start drowning, but the swimming instructor immediately comes to your aid."
            $ hero.swimming += 1
            $ hero.health = max(1, hero.health - 5)
        $ hero.vitality -= randint (25, 35)
    elif hero.get_skill("swimming") < 50:
        "You can swim well enough to not drown in a swimming pool, but more practice is needed."
        $ hero.swimming += randint(2,3)
        $ hero.vitality -= randint (20, 30)
    elif hero.get_skill("swimming") < 100:
        "You are somewhat confident about your swimming skills."
        $ hero.swimming += randint(2,4)
        $ hero.vitality -= randint (15, 20)
    else:
        "It feels nice swimming in the pool, but the sea is more suitable to learn something new."
        $ hero.swimming += randint(0,1)
        $ hero.vitality -= randint (10, 15)
    if locked_dice(75) and hero.get_skill("swimming") >= 50 and hero.constitution < hero.get_max("constitution"):
        $ hero.mod_stat("constitution", 1)
        "Swimming did you good (constitution+)."
    return

label mc_action_instructor_swimming_pool_skill_checks:
    $ hero.AP -= 1
    if hero.get_skill("swimming") < 20:
        "The instructor teaches you water safety to prevent mouth-to-mouth accidents once and for all."
        $ hero.swimming += randint(2,4)
        $ hero.SWIMMING += randint(2,4) # theoretical part
        $ hero.vitality -= randint (20, 30)
    elif hero.get_skill("swimming") < 50:
        "The instructor shows you the most basic swimming styles."
        $ hero.swimming += randint(4,6)
        $ hero.SWIMMING += randint(4,6)
        $ hero.vitality -= randint (15, 25)
    elif hero.get_skill("swimming") < 100:
        "The instructor shows you common swimming styles and the very basics of underwater swimming."
        $ hero.swimming += randint(4,8)
        $ hero.SWIMMING += randint(4,8)
        $ hero.vitality -= randint (10, 15)
    elif hero.get_skill("swimming") < 250:
        "The instructor shows you advanced swimming styles, including underwater ones."
        $ hero.swimming += randint(1,3)
        $ hero.SWIMMING += randint(5,10)
        $ hero.vitality -= randint (10, 15)
    else:
        "There is nothing else he can show you now, but his knowledge about behavior on the water is second to none nevertheless."
        $ hero.swimming += randint(0,1)
        $ hero.SWIMMING += randint(5,10)
        $ hero.vitality -= randint (5, 10)
    if locked_dice(65) and hero.get_skill("swimming") >= 50:
        $ hero.mod_stat("constitution", 1)
    return

label mc_action_work_swim_pool: # here we could use an option to meet characters with a certain probability
    if hero.vitality < 20:
        "You are too tired for work."
        jump swimming_pool
    elif hero.AP <= 0:
        "You don't have enough Action Points. Try again tomorrow."
        jump swimming_pool
    elif hero.health < hero.get_max("health")*.5:
        "You are too wounded at the moment."
        jump swimming_pool

    $ result = randint(5, round(hero.get_skill("swimming")*.1))
    if result > 200:
        $ result = randint (190, 220)
    $ hero.AP -= 1
    $ hero.swimming += randint(0,2)
    $ hero.SWIMMING += randint(1,2)
    $ hero.vitality -= randint (20, 35)
    $ picture = "content/gfx/images/swim_kids/sk_" + str(renpy.random.randint(1, 4)) + ".webp"
    show expression picture at truecenter with dissolve
    $ narrator ("You teach local kids to swim. The payment is low, but at least you can use the pool for free. (+ %d) G" %result)
    $ hero.add_money (result, reason="Job")
    hide expression picture with dissolve
    $ del result
    jump swimming_pool
