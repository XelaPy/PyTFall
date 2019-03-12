label mainscreen:
    # Music related:
    # First Run (Fadeout added)
    if global_flags.flag("game_start"):
        $ global_flags.del_flag("game_start")
        $ fadein = 15
    else:
        $ fadein = 0

    if not "pytfall" in ilists.world_music:
        $ ilists.world_music["pytfall"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("pytfall")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["pytfall"]) fadein fadein
    $ global_flags.del_flag("keep_playing_music")

    scene black
    show screen mainscreen

    if not persistent.showed_pyp_hint:
        $ persistent.showed_pyp_hint = True
        show screen tutorial

    # Prediction Helpers:
    # TODO lt: Stop predictions when we've moved to far away from the images!
    python hide:
        main_img_predict = [item for sl in (("".join([pytfall.map_pattern, key, ".webp"]),
                            "".join([pytfall.map_pattern, key, "_hover.webp"]),
                            "".join(["content/gfx/interface/buttons/locations/", key, ".png"]))
                              for key in (i["id"] for i in pytfall.maps("pytfall")))
                            for item in sl]
        main_img_predict.extend(("bg gallery",
                                 "content/gfx/frame/h2.webp",
                                 "content/gfx/frame/p_frame.png",
                                 "content/gfx/frame/rank_frame.png",
                                 "content/gfx/images/m_1.webp",
                                 "content/gfx/images/m_2.webp",
                                 "content/gfx/images/fishy.png",
                                 "content/gfx/interface/buttons/compass.png",
                                 "content/gfx/interface/buttons/IT2.png",
                                 "content/gfx/interface/buttons/sl_idle.png",
                                 "content/gfx/interface/icons/exp.webp",
                                 "content/gfx/interface/icons/gold.png",
                                 "content/gfx/interface/images/work.webp"))
        # for i in store.items.values():
        #     main_img_predict.append(i.icon)
        renpy.start_predict(*main_img_predict)

        main_scr_predict = ["city_screen", "chars_list"]
        for scr in main_scr_predict:
            renpy.start_predict_screen(scr)

    $ pytfall.world_events.next_day() # Get new set of active events
    $ pytfall.world_quests.run_quests("auto") # Unsquelch active quests
    $ pytfall.world_events.run_events("auto") # Run current events
    $ pytfall.world_quests.next_day() # Garbage collect quests

    while 1:
        $ result = ui.interact()

        if len(result) > 1:
            python:
                pytfall.sm.set_index()
                renpy.hide_screen("mainscreen")
                pytfall.arena.seen_report = True
                jump(result[1])
        elif result[0] == "chars_list":
            stop world
            $ renpy.hide_screen("mainscreen")
            $ pytfall.arena.seen_report = True
            # scene bg gallery
            # with irisin
            $ jump(result[0])
        elif result[0] == "city":
            $ global_flags.set_flag("keep_playing_music")
            $ renpy.hide_screen("mainscreen")
            $ pytfall.arena.seen_report = True
            scene bg pytfall
            # with irisin
            $ jump(result[0])
        elif result[0] == "hero_eq":
            $ came_to_equip_from = "mainscreen"
            $ eqtarget = hero
            jump char_equip
        else:
            python:
                renpy.hide_screen("mainscreen")
                pytfall.arena.seen_report = True
                jump(result[0])

screen mainscreen():
    key "mousedown_3" action Show("s_menu", transition=dissolve)

    # Main pic:
    add im.Scale("content/gfx/bg/main_brothel.webp", config.screen_width, config.screen_height-40) at fade_from_to(.0, 1.0, 2.0) ypos 40

    frame:
        align (.995, .88)
        background Frame("content/gfx/frame/window_frame2.webp", 30, 30)
        xysize (255, 670)
        xfill True
        yfill True

        add "".join(["content/gfx/interface/images/calendar/","cal ", calendar.moonphase(), ".png"]) xalign .485 ypos 83

        text "{font=fonts/TisaOTM.otf}{k=-1}{color=#FFEC8B}{size=18}%s" % calendar.weekday() xalign .5 ypos 210

        text "{font=fonts/TisaOTM.otf}{k=-0.5}{color=#FFEC8B}{size=18}%s" % calendar.string() xalign .5 ypos 250

        vbox:
            style_group "main_screen_3"
            xalign .5
            ypos 305
            spacing 15
            textbutton "Characters":
                action Stop("world"), Hide("mainscreen"), SetVariable("rebuild_chars_listings", True), Jump("chars_list")
                tooltip "A list of all of your workers"
            textbutton "Buildings":
                action Return(["building_management"])
                sensitive hero.buildings
                tooltip "Manage here your properties and businesses"
            textbutton "Go to the City":
                action Return(["city"])
                tooltip 'Explore the city'

            null height 50

            textbutton "-Next Day-":
                style "main_screen_4_button"
                if day > 1:
                    tooltip "Advance to next day!\nClick RMB to review reports!"
                    action [Hide("mainscreen"), Jump("next_day")]
                    alternate SetVariable("just_view_next_day", True), Hide("mainscreen"), Jump("next_day")
                else:
                    tooltip "Advance to next day!"
                    action [Hide("mainscreen"), Jump("next_day")]

    if DEBUG:
        vbox:
            style_group "dropdown_gm"
            spacing 1
            align (.01, .5)
            textbutton "MD test":
                action Hide("mainscreen"), Jump("storyi_start")
            textbutton "Arena Inside":
                action Hide("mainscreen"), Jump("arena_inside")
            textbutton "Realtor":
                action Hide("mainscreen"), Jump("realtor_agency")
            textbutton "Test BE":
                action Hide("mainscreen"), Jump("test_be")
            textbutton "Test BE Logical":
                action Hide("mainscreen"), Jump("test_be_logical")
            textbutton "Peak Into SE":
                action Show("se_debugger")
            textbutton "Examples":
                action [Hide("mainscreen"), Jump("examples")]
            textbutton "Return on callstack":
                action [Hide("mainscreen"), Jump("debug_callstack")]
            textbutton "Show Chars Debug":
                action Show("chars_debug")
            textbutton "Clear Console":
                action Jump("force_clear_console")

    showif day > 1 and (gazette.first_view or gazette.show):
        default gazette_map = (
        ("arena", "Today at the Arena!"),
        ("shops", "Shopkeepers in PyTFall reporting:"),
        ("jail", "Jailbird Chronic:"),
        ("other", "Also:")
        )

        frame:
            background Frame("content/gfx/frame/settings1.webp", 10, 10)
            style_prefix "proper_stats"
            xysize 500, 600
            padding 10, 10
            pos 500, 60
            has vbox spacing 10
            label "PyTFall's GAZETTE" xalign .5
            viewport:
                xysize 480, 550
                xalign .5
                scrollbars "vertical"
                mousewheel True
                has vbox
                for attr, t in gazette_map:
                    $ content = getattr(gazette, attr)
                    if content:
                        label "[t]" text_size 17
                        text "\n".join(content)
                        null height 10
            if gazette.first_view:
                timer 6 action ToggleField(gazette, "first_view")

    use top_stripe(False)
