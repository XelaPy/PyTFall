init python:
    # The dice value for gm scenes
    gm_dice = 100

    # The disposition multiplier for gm scenes
    gm_disp_mult = 1

    # Whether the gm scene was successful
    gm_last_success = False

    # List for possible about her text
    gm_abouther_list = None

    # The background for the date fight
    gm_fight_bg = None

    # The job for the GT mode
    gm_job = None


label girl_interactions:
    python:
        if "girl_meets" in pytfall.world_actions.locations:
            del pytfall.world_actions.locations["girl_meets"]
        pytfall.world_actions.clear()

    python:
        # Set default characters
        g = char.say
        h = hero.say
        nvl_gm = Character(None, kind=nvl)

        # Run quests and events
        pytfall.world_quests.run_quests("auto")
        pytfall.world_events.run_events("auto")

        # Hide menus till greeting
        gm.show_menu = False
        gm.show_menu_givegift = False

    scene expression gm.bg_cache
    show screen girl_interactions
    with dissolve

    if char.flag("quest_cannot_be_fucked") != True and interactions_silent_check_for_bad_stuff(char): # chars with flag will propose sex once per day once you try to talk to them
        if char.effects['Horny']['active'] and interactions_silent_check_for_bad_stuff(char) and check_lovers(char, hero):
            call interactions_girl_proposes_sex
            menu:
                "Do you wish to have sex with [char.name]?"
                "Yes":
                    $ char.set_flag("gm_char_proposed_sex", value=day)
                    if char.effects['Horny']['active']:
                        $ char.disable_effect("Horny")
                    jump interactions_sex_scene_select_place
                "No":
                    $ char.set_flag("gm_char_proposed_sex", value=day)
                    $ char.override_portrait("portrait", "indifferent")
                    $ rc("...", "I see...", "Maybe next time then...")
                    $ char.joy -= randint(1, 5)
                    $ char.restore_portrait()
                    jump girl_interactions_after_greetings

    # Show greeting:
    if gm.see_greeting:
        $ gm.see_greeting = False

        if renpy.has_label("%s_greeting"%gm.mode):
            call expression ("%s_greeting"%gm.mode) from _call_expression

label girl_interactions_after_greetings: # when character wants to say something in the start of interactions, we need to skip greetings and go here
    python:
        # Show menu
        gm.show_menu = True

        # GM labels can now be of the following formats (where %l is the label and %g is the girl's id):
        # girl_meets_%l_%g
        # girl_meets_%l
        # girl_interactions_%l_%g
        # girl_interactions_%l
        # girl_trainings_%l_%g
        # girl_trainings_%g
        # interaction_%l_%g
        # interaction_%l
        #
        # The GM system will pick the most specific available label. Possible choices can be restricted by setting the follow arguments as False:
        # allow_gm
        # allow_int
        # allow_tr
        # allow_unique
        #
        # Note, the above doesn't work for actions generated through the ST module, although they will use girl-specific labels if available.
        #
        # You can limit what action is available under what mode by setting the mode argument to:
        # girl_meets = When meeting free girls in the city.
        # girl_interactions = When interacting with girls under your employ.
        # girl_training = When training slaves.
        #
        # If you wish to limit an entire menu you need to set condition to either _gm_mode, _gi_mode or _gt_mode for girl_meets, girl_interactions or girl_trainings respectively.
        #

        # Create actions
        if pytfall.world_actions.location("girl_meets"):
            _gm_mode = Iff(S((gm, "mode")), "==", "girl_meets")
            _gi_mode = Iff(S((gm, "mode")), "==", "girl_interactions")
            _gt_mode = Iff(S((gm, "mode")), "==", "girl_trainings")

            _not_gm_mode = IffOr(_gi_mode, _gt_mode)
            _not_gi_mode = IffOr(_gm_mode, _gt_mode)
            _not_gt_mode = IffOr(_gm_mode, _gi_mode)

            # CHAT
            m = 0
            pytfall.world_actions.menu(m, "Chat")
            pytfall.world_actions.gm_choice("Small Talk", index=(m, 0))
            pytfall.world_actions.gm_choice("About Job", mode="girl_interactions", index=(m, 1))
            pytfall.world_actions.gm_choice("How She Feels", mode="girl_interactions", index=(m, 2))
            pytfall.world_actions.gm_choice("About Her", index=(m, 3))
            pytfall.world_actions.gm_choice("About Occupation", mode="girl_meets", index=(m, 4))
            pytfall.world_actions.gm_choice("Interests", index=(m, 5))
            pytfall.world_actions.gm_choice("Flirt", index=(m, 6))


            # TRAINING
            m = 1
            n = 0
            pytfall.world_actions.menu(m, "Training", condition=_gt_mode)

            # Loop through all courses that don't belong to a school, and return the real dict
            #for k,c in get_all_courses(no_school=True, real=True).iteritems():

            # Loop through all courses in the training dungeon:
            for b in hero.buildings:
                if isinstance(b, TrainingDungeon):
                    for k,c in schools[TrainingDungeon.NAME].all_courses.iteritems():
                        # Get the lessons that are one off events
                        ev = [l for l in c.options if l.is_one_off_event]

                        if ev:
                            # Create the menu for the course
                            pytfall.world_actions.menu((m, n), k, condition=OneOffTrainingAction("menu", c))

                            for l in range(len(ev)):
                                # Add the lesson
                                pytfall.world_actions.add((m, n, l), ev[l].name, OneOffTrainingAction("action", ev[l]), condition=OneOffTrainingAction("condition", ev[l]))

                            n += 1

            # PRAISE
            m = 2
            pytfall.world_actions.menu(m, "Praise", condition="not(char in hero.chars)")
            pytfall.world_actions.gm_choice("Clever", mode="girl_meets", index=(m, 0))
            pytfall.world_actions.gm_choice("Strong", mode="girl_meets", index=(m, 1))
            pytfall.world_actions.gm_choice("Cute", mode="girl_meets", index=(m, 2))


            # GIVE MONEY
            m = 3
            pytfall.world_actions.menu(m, "Money", condition="char.status != 'slave'")
            pytfall.world_actions.gm_choice("Propose to give money", label="giftmoney", index=(m, 0))
            pytfall.world_actions.gm_choice("Ask for money", label="askmoney", index=(m, 1))

            m = 4
            pytfall.world_actions.menu(m, "Money", condition="char.status == 'slave'")
            pytfall.world_actions.gm_choice("Give", label="give_money", index=(m, 0))
            pytfall.world_actions.gm_choice("Take", label="take_money", index=(m, 1))

            # GIVE GIFT
            m = 5
            flag_name = "_day_countdown_interactions_gifts"
            flag_value = int(char.flag(flag_name))
            pytfall.world_actions.add(m, "Give Gift", Return(["gift", True]), condition="flag_value < 3")

            # PROPOSITION
            m = 6
            pytfall.world_actions.menu(m, "Propose", condition="not(char in hero.chars) or not(check_friends(char, hero)) or not(check_lovers(char, hero))")
            pytfall.world_actions.gm_choice("Friends", condition="not check_friends(char, hero)", index=(m, 0))
            pytfall.world_actions.gm_choice("Girlfriend", condition="not check_lovers(char, hero)", index=(m, 1))
            pytfall.world_actions.gm_choice("Hire", condition="not(char in hero.chars) and not char.flag('quest_cannot_be_hired')", index=(m, 2))

            # INTIMACY
            m = 7
            pytfall.world_actions.menu(m, "Intimacy")
            pytfall.world_actions.gm_choice("Hug", index=(m, 0))
            pytfall.world_actions.gm_choice("Grab Butt", index=(m, 1))
            pytfall.world_actions.gm_choice("Grab Breasts", index=(m, 2))
            pytfall.world_actions.gm_choice("Kiss", index=(m, 3))
            pytfall.world_actions.gm_choice("Sex", index=(m, 4))
            pytfall.world_actions.gm_choice("Hire For Sex", index=(m, 5), condition="not(check_lovers(char, hero)) and cgo('SIW') and char.status != 'slave'")
            pytfall.world_actions.gm_choice("Become Fr", index=(m, 6), condition="config.developer")
            pytfall.world_actions.gm_choice("Become Lv", index=(m, 7), condition="config.developer")
            pytfall.world_actions.gm_choice("Disp", index=(m, 8), condition="config.developer")
            # Quests/Events to Interactions Menu:
            """
            Expects a dictionary with the following k/v pairs to be set as a flag that starts with :
            event_to_interactions_  as a flag and {"label": "some_label", "button_name='Some Name'", "condition": "True"}
            """
            m = 8
            # First add the Menu:
            for f in char.flags:
                if f.startswith("event_to_interactions_") and renpy.has_label(char.flag(f)["label"]):
                    if "condition" in char.flag(f) and eval(char.flag(f)["condition"]):
                        pytfall.world_actions.menu(m, "U-Actions")
                        break
            i = 0
            for f in char.flags:
                if f.startswith("event_to_interactions_") and renpy.has_label(char.flag(f)["label"]):
                    if "condition" in char.flag(f) and eval(char.flag(f)["condition"]):
                        pytfall.world_actions.gm_choice(char.flag(f)["button_name"], label=char.flag(f)["label"], index=(m, i))
                        i = i + 1
            m = 9
            pytfall.world_actions.menu(m, "Harassment", condition="not(char in hero.team) and char in hero.chars") # no fights between team members
            pytfall.world_actions.gm_choice("Insult", index=(m, 0))
            pytfall.world_actions.gm_choice("Escalation", index=(m, 1))
            # Back
            pytfall.world_actions.add("zzz", "Leave", Return(["control", "back"]))

            # Developer mode switches
            if config.developer:
                pytfall.world_actions.menu("dev", "Developer")
                pytfall.world_actions.add(("dev", "gm"), "GM", Return(["test", "GM"]), condition=_not_gm_mode)
                pytfall.world_actions.add(("dev", "gi"), "GI", Return(["test", "GI"]), condition=_not_gi_mode)
                pytfall.world_actions.add(("dev", "gt"), "GT", Return(["test", "GT"]), condition=_not_gt_mode)

            pytfall.world_actions.finish()

    jump interactions_control

label girl_interactions_end:
        # End the GM:
        $ gm.end()

label interactions_control:
    while 1:
        $ result = ui.interact()

        # Testing
        if result[0] == "test":
            python:
                gm.end(safe=True)

                # Girls Meets
                if result[1] == "GM":
                    # Include img as coming from int and tr prevents the "img from last location" from working
                    gm.start_gm(char, img=char.show("profile", resize=gm.img_size, exclude=["nude", "bikini", "swimsuit", "beach", "angry", "scared", "ecstatic"]))

                # Interactions
                elif result[1] == "GI":
                    gm.start_int(char)

                # Training
                elif result[1] == "GT":
                    gm.start_tr(char)

        # Gifts
        elif result[0] == "gift":
            python:
                # Show menu:
                if result[1] is True:
                    gm.show_menu = False
                    gm.show_menu_givegift = True

                # Hide menu:
                elif result[1] is None:
                    gm.show_menu = True
                    gm.show_menu_givegift = False

                # Give gift:
                else:
                    # Prevent repetition of this action (any gift, we do this on per gift basis already):
                    flag_name = "_day_countdown_interactions_gifts"
                    flag_value = int(char.flag(flag_name))

                    char.set_flag(flag_name, flag_value + 1)

                    item = result[1]
                    item.hidden = False # We'll use existing hidden flag to hide items effectiveness.
                    dismod = getattr(item, "dismod", 0)

                    if item.type == "romantic" and not(check_lovers(char, hero)) and char.disposition < 700:  # cannot give romantic gifts to anyone
                            dismod = -10
                    else:
                        for t, v in getattr(item, "traits", {}).iteritems():
                            if t in char.traits:
                                dismod += v

                    flag_name = "_day_countdown_{}".format(item.id)
                    flag_value = int(char.flag(flag_name))

                    # We never award more than 70 disposition for a single gift:
                    if dismod > 70:
                        dismod = 70

                    # Add the appropriate dismod value:
                    if flag_value != 0:
                        if flag_value < item.cblock:
                            char.disposition = int(round(float(dismod)*(item.cblock-flag_value)/item.cblock))
                        elif flag_value >= item.cblock:
                            setattr(gm, "show_menu", True)
                            setattr(gm, "show_menu_givegift", False)
                            gm.jump("refusegift")
                    else:
                        char.disposition += dismod

                    hero.inventory.remove(item)
                    setattr(gm, "show_menu", True)
                    setattr(gm, "show_menu_givegift", False)

                    char.up_counter(flag_name, item.cblock)
                    if dismod <= 0:
                        gm.jump("badgift")
                    elif dismod <= 30:
                        gm.jump("goodgift")
                    else:
                        gm.jump("perfectgift")

        # Controls
        elif result[0] == "control":
            # Return / Back
            if result[1] in ("back", "return"):
                jump girl_interactions_end


screen girl_interactions():
    # BG
    add "content/gfx/images/bg_gradient.png" yalign 0.2

    # Disposition bar
    vbox:
        align (0.95, 0.31)

        vbar:
            top_gutter 13
            bottom_gutter 0
            value AnimatedValue(value=gm.char.disposition, range=gm.char.get_max("disposition"), delay=4.0)
            bottom_bar "content/gfx/interface/bars/progress_bar_full1.png"
            top_bar "content/gfx/interface/bars/progress_bar_1.png"
            thumb None
            xysize (22, 175)

        python:
            # Trying to invert the values (bar seems messed up with negative once):
            if gm.char.disposition < 0:
                inverted_disposition = -gm.char.disposition
            else:
                inverted_disposition = 0

        vbar:
            bar_invert True
            top_gutter 12
            bottom_gutter 0
            value AnimatedValue(value=inverted_disposition, range=-gm.char.stats.min["disposition"], delay=4.0)
            bottom_bar im.Flip("content/gfx/interface/bars/progress_bar_1.png", vertical=True)
            top_bar "content/gfx/interface/bars/bar_mine.png"
            thumb None
            xysize(22, 175)

    # Girl image
    hbox:
        xanchor 0
        xpos 0.22
        yalign 0.22

        frame:
            background Frame("content/gfx/frame/MC_bg.png", 10, 10)
            # basestring assumes that image is coming from cache, so it simply a path.
            if isinstance(gm.img, basestring):
                add ProportionalScale(gm.img, gm.img_size[0], gm.img_size[1])
            else:
                add gm.img

        if config.developer:
            null width 15

            vbox:
                null height 60
                text "{color=[white]}Mode: [gm.mode]"
                text "{color=[white]}Label: [gm.jump_cache]"
                text ("{color=[white]}Girl.AP: [gm.char.AP] / %s"%gm.char.get_ap())
                text "{color=[white]}Points: [gm.gm_points]"

    # Actions
    if gm.show_menu:
        use location_actions("girl_meets", gm.char, pos=(1180, 315), anchor=(1.0, 0.5), style="main_screen_3")

    # Give gift interface
    if gm.show_menu_givegift:
        frame:
            style "dropdown_gm_frame"
            xysize (385, 455)
            align (0.89, 0.27)
            viewport:
                xysize (365, 433)
                scrollbars "vertical"
                mousewheel True
                has vbox

                for item in hero.inventory:
                    if item.slot == "gift":
                        python:
                            dismod = getattr(item, "dismod", 0)
                            if item.type == "romantic" and not(check_lovers(char, hero)) and char.disposition < 700:  # cannot give romantic gifts to anyone
                                dismod = -10
                            else:
                                for t, v in getattr(item, "traits", {}).iteritems():
                                    if t in char.traits:
                                        dismod += v
                            flag_name = "_day_countdown_{}".format(item.id)
                            flag_value = int(char.flag(flag_name))

                        button:
                            style "main_screen_3_button"
                            xysize (350, 100)
                            hbox:
                                fixed:
                                    yoffset 3
                                    xysize (90, 90)
                                    add im.Scale(item.icon, 90, 90)
                                    text str(hero.inventory[item]) color ivory style "library_book_header_main" align (0, 0)
                                    if not item.hidden:
                                        if dismod <= 0:
                                            if flag_value != 0:
                                                add im.Sepia(im.Scale("content/gfx/interface/icons/gifts_0.png", 65, 35)) align (.0, 0.9)
                                            else:
                                                add im.Scale("content/gfx/interface/icons/gifts_0.png", 65, 35) align (.0, 0.9)
                                        elif dismod <= 30:
                                            if flag_value != 0:
                                                add im.Sepia(im.Scale("content/gfx/interface/icons/gifts_1.png", 65, 35)) align (.0, 0.9)
                                            else:
                                                add im.Scale("content/gfx/interface/icons/gifts_1.png", 65, 35) align (.0, 0.9)
                                        elif dismod > 30:
                                            if flag_value != 0:
                                                add im.Scale(im.Scale("content/gfx/interface/icons/gifts_2.png", 65, 35)) align (.0, 0.9)
                                            else:
                                                add im.Scale("content/gfx/interface/icons/gifts_2.png", 65, 35) align (.0, 0.9)
                                null width 10
                                text "[item.id]" yalign 0.5 style "library_book_header_sub" color ivory

                            action If(hero.AP > 0, Return(["gift", item]))

                null height 10
                textbutton "Back":
                    action Return(["gift", None])
                    minimum(220, 30)
                    xalign 0.5
                    style "main_screen_3_button"
                    text_style "library_book_header_sub"
                    text_color ivory

    use top_stripe(False)


screen girl_interactions_old:

    # Controls
    frame:
        pos (860, 50)
        xysize (420, 560)
        background "content/gfx/frame/frame12.png"
        style_group "interactions"

        text "TALK" xalign 0.49 ypos 130 size 22 color white

        text "SEX" xalign 0.49 ypos 260 size 22 color white

        text "GO OUT" xalign 0.49 ypos 380 size 22 color white

        hbox:
            xalign 0.47
            ypos 150
            button:
                xysize (78, 30)
                action gi_action("chat")
                text "Chat"

            null width 65

            button:
                xysize (78, 30)
                action gi_action("praise")
                text "Praise"

        button:
            xalign 0.48
            ypos 192
            xysize (78, 30)
            action gi_action("scold")
            text "Scold"

        button:
            xalign 0.195
            ypos 285
            xysize (78, 30)
            action gi_action("fuck")
            text "Fuck"

        button:
            xalign 0.493
            ypos 285
            xysize (110, 30)
            action gi_action("blowjob")
            text "Blowjob"

        button:
            xalign 0.79
            ypos 285
            xysize (78, 30)
            action gi_action("anal")
            text "Anal"

        button:
            xalign 0.488
            ypos 325
            xysize (160, 30)
            action gi_action("lesbo")
            text "Lesbo Action"

        button:
            xalign 0.193
            ypos 394
            xysize (78, 30)
            action gi_action("date")
            text "Date"

        button:
            xalign 0.493
            ypos 394
            xysize (110, 30)
            action gi_action("shopping")
            text "Shopping"

        button:
            xalign 0.79
            ypos 394
            xysize (78, 30)
            action gi_action("other")
            text "Other"

        button:
            xalign 0.484
            ypos 435
            xysize (170, 30)
            action gi_action("entertainment")
            text "Entertainment"

    # Move to General GM
    if config.developer:
        textbutton "Test GM":
            align (0.5, 0.1)
            action Return(['test_gm'])

    # Girl image
    frame:
        background Frame("content/gfx/frame/FrameGP.png", 40, 40)
        xanchor 0
        xpos 0.05
        yalign 0.2
        add ProportionalScale(gm.img, 900, 530)

    use top_stripe(True)
