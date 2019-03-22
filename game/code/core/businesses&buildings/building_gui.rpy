default BUILDING = None

init python:
    def set_building_index():
        global index
        global BUILDING

        try:
            BUILDING = hero.buildings[index]
        except:
            index = 0
            BUILDING = hero.buildings[index]


label building_management:
    python:
        # Reset screen settings, we do this only if we left this screen directly (No jump to char profile/equip)
        if reset_building_management:
            reset_building_management = False
            bm_mid_frame_mode = "building"
            bm_mid_frame_focus = None
            bm_exploration_view_mode = "team"
            selected_log_area = None

    $ set_building_index()

    python:
        # special cursor for DragAndDrop and the original value
        mouse_drag = {"default" :[("content/gfx/interface/cursors/hand.png", 0, 0)]}
        mouse_cursor = config.mouse

    scene bg scroll

    $ renpy.retain_after_load()
    show screen building_management
    with fade

    $ pytfall.world_quests.run_quests("auto") # Added for completion, unnecessary?
    $ pytfall.world_events.run_events("auto")

    $ global_flags.set_flag("keep_playing_music")

    while 1:
        $ result = ui.interact()
        if not result or not isinstance(result, (list, tuple)):
            pass
        elif result[0] == "bm_mid_frame_mode":
            $ bm_mid_frame_mode = result[1]
            if isinstance(bm_mid_frame_mode, ExplorationGuild):
                # Looks pretty ugly... this might be worth improving upon just for the sake of esthetics.
                $ workers = CoordsForPaging(all_chars_for_se(), columns=6, rows=3,
                        size=(80, 80), xspacing=10, yspacing=10, init_pos=(56, 11))
                $ fg_filters = CharsSortingForGui(all_chars_for_se)
                $ fg_filters.occ_filters.add("Combatant")
                $ fg_filters.target_container = [workers, "content"]
                $ fg_filters.filter()

                $ guild_teams = CoordsForPaging(bm_mid_frame_mode.idle_teams(clear_by_workplace=True), columns=3, rows=3,
                                size=(208, 83), xspacing=0, yspacing=5, init_pos=(4, 340))
        elif result[0] == "fg_team":
            python:
                if result[1] == "rename":
                    n = renpy.call_screen("pyt_input", result[2].name, "Enter Name", 20)
                    if len(n):
                        result[2].name = n
                elif result[1] == "clear":
                    for i in result[2]:
                        workers.add(i)
                    del result[2].members[:]
                elif result[1] == "create":
                    name = get_team_name()
                    name = renpy.call_screen("pyt_input", name, "Enter Name", 20)
                    if len(name):
                        bm_mid_frame_mode.expand_capacity(name=name, mod_gui=guild_teams)
                elif result[1] == "dissolve":
                    bm_mid_frame_mode.reduce_capacity(team=result[2], mod_gui=[workers, guild_teams])
                elif result[1] == "explore_area":
                    result = bm_mid_frame_mode.launch_team(result[2])
                    if isinstance(result, PytCharacter):
                        renpy.show_screen("message_screen", "{} is not in shape to explore anything :(".format(result.name))
                    else:
                        jump("building_management")
        elif result[0] == "building":
            if result[1] == 'items_transfer':
                python:
                    it_members = list(BUILDING.get_all_chars())
                    it_members.sort(key=attrgetter("name"))
                hide screen building_management
                $ items_transfer(it_members)
                show screen building_management
            elif result[1] == "sign":
                python:
                    ad = result[2]

                    if BUILDING.flag('bought_sign'):
                        price = ad['price']/10
                    else:
                        price = ad['price']

                    if hero.take_money(price, reason="Building Ads"):
                        BUILDING.fin.log_logical_expense(price, "Ads")
                        BUILDING.set_flag('bought_sign', True)
                        ad['active'] = not ad['active']
                    else:
                        renpy.show_screen("message_screen", "Not enough cash on hand!")
            elif result[1] == "celeb":
                python:
                    ad = result[2]
                    price = ad['price']
                    if hero.take_money(price, reason="Building Ads"):
                        BUILDING.fin.log_logical_expense(price, "Ads")
                        ad['active'] = True
                    else:
                        renpy.show_screen("message_screen", "Not enough cash on hand!")
            elif result[1] == "sell":
                python:
                    price = int(BUILDING.price*.9)

                    if renpy.call_screen("yesno_prompt",
                                         message="Are you sure you wish to sell %s for %d Gold?" % (BUILDING.name, price),
                                         yes_action=Return(True), no_action=Return(False)):
                        if hero.home == BUILDING:
                            hero.home = locations["Streets"]
                        if hero.workplace == BUILDING:
                            hero.action = None
                            hero.workplace = None
                        if hero.location == BUILDING:
                            set_location(hero, hero.home)

                        retire_chars_from_location(hero.chars, BUILDING)

                        hero.add_money(price, reason="Property")
                        hero.remove_building(BUILDING)

                        if hero.buildings:
                            set_building_index()
                        else:
                            jump("building_management_end")
        # Upgrades:
        elif result[0] == 'upgrade':
            if result[1] == "build":
                python hide:
                    temp = result[2]()
                    if isinstance(temp, BusinessUpgrade):
                        result[3].add_upgrade(temp, pay=True)
                    elif isinstance(temp, Business):
                        BUILDING.add_business(temp, pay=True)
                    elif isinstance(temp, BuildingUpgrade):
                        BUILDING.add_upgrade(temp, pay=True)
                    else:
                        raise Exception("Unknown extension class detected: {}".format(result[2]))
        elif result[0] == "maintenance":
            python:
                # Cleaning controls
                if result[1] == "clean":
                    price = BUILDING.get_cleaning_price()
                    if hero.take_money(price, reason="Pro-Cleaning"):
                        BUILDING.fin.log_logical_expense(price, "Pro-Cleaning")
                        BUILDING.dirt = 0
                    else:
                        renpy.show_screen("message_screen", "You do not have the required funds!")
                elif result[1] == "clean_all":
                    if hero.take_money(result[2], reason="Pro-Cleaning"):
                        for i in hero.dirty_buildings:
                            i.fin.log_logical_expense(i.get_cleaning_price(), "Pro-Cleaning")
                            i.dirt = 0
                    else:
                        renpy.show_screen("message_screen", "You do not have the required funds!")
                elif result[1] == "toggle_clean":
                    BUILDING.auto_clean = 90 if BUILDING.auto_clean == 100 else 100
                elif result[1] == "rename_building":
                    BUILDING.name = renpy.call_screen("pyt_input", default=BUILDING.name, text="Enter Building name:")
                elif result[1] == "retrieve_jail":
                    pytfall.ra.retrieve_jail = not pytfall.ra.retrieve_jail
        elif result[0] == 'control':
            if result[1] == 'return':
                jump building_management_end
            elif result[1] == 'left':
                $ index = (index - 1) % len(hero.buildings)
            elif result[1] == 'right':
                $ index = (index + 1) % len(hero.buildings)
            $ set_building_index()

label building_management_end:
    hide screen building_management

    # Reset the vars on next reentry:
    $ reset_building_management = False
    jump mainscreen

# Screens:
screen building_management():
    if hero.buildings:
        # Main Building mode:
        if bm_mid_frame_mode == "building":
            use building_management_midframe_building_mode
        else: # Upgrade mode:
            use building_management_midframe_businesses_mode

        ## Stats/Upgrades - Left Frame
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
            xysize (330, 720)
            # xanchor .01
            ypos 40
            style_group "content"
            has vbox
            if bm_mid_frame_mode == "building":
                use building_management_leftframe_building_mode
            else: # Upgrade mode:
                use building_management_leftframe_businesses_mode

        ## Right frame:
        frame:
            xysize (330, 720)
            ypos 40
            xalign 1.0
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
            has vbox spacing 1
            if bm_mid_frame_mode == "building":
                use building_management_rightframe_building_mode
            else: # Upgrade mode:
                use building_management_rightframe_businesses_mode
    else:
        text "You don't own any buildings.":
            size 50
            color ivory
            align .5, .5
            style "TisaOTM"

    use top_stripe(True)
    if not bm_mid_frame_mode == "building":
        key "mousedown_3" action Function(setattr, config, "mouse", mouse_cursor), Return(["bm_mid_frame_mode", "building"])
    else:
        key "mousedown_4" action Return(["control", "right"])
        key "mousedown_5" action Return(["control", "left"])

screen building_management_rightframe_building_mode:
    # Buttons group:
    frame:
        xalign .5
        style_prefix "wood"
        xpadding 0
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.9), 5, 5)
        has hbox xalign .5 spacing 5 xsize 315
        null height 16
        vbox:
            spacing 5
            button:
                xysize (135, 40)
                action Show("building_adverts")
                sensitive isinstance(BUILDING, BuildingStats) and BUILDING.workable and BUILDING.can_advert
                tooltip 'Advertise this building to attract more and better customers'
                text "Advertise"
            button:
                xysize (135, 40)
                action Return(['building', "items_transfer"])
                tooltip 'Transfer items between characters in this building'
                sensitive isinstance(BUILDING, HabitableLocation) and (len(BUILDING.inhabitants) >= 2)
                text "Transfer Items"
            button:
                xysize (135, 40)
                action Show("building_controls")
                tooltip 'Perform maintenance of this building'
                sensitive isinstance(BUILDING, BuildingStats) and BUILDING.workable
                text "Controls"
        vbox:
            spacing 5
            button:
                xysize (135, 40)
                action SetField(hero, "location", BUILDING)
                tooltip 'Settle in the building!'
                sensitive False # We prolly want better conditioning to use this!
                text "Settle"
            button:
                xysize (135, 40)
                action Show("finances", None, BUILDING, mode="logical")
                tooltip 'Show finance log for this building'
                sensitive isinstance(BUILDING, BuildingStats) and BUILDING.workable
                text "Finance Log"
            button:
                xysize (135, 40)
                action Return(["building", "sell"])
                tooltip 'Get rid of this building'
                sensitive BUILDING.can_be_sold()
                text "Sell"

    # Slots for New Style Upgradable Buildings:
    if isinstance(BUILDING, UpgradableBuilding):
        frame:
            xalign .5
            style_prefix "proper_stats"
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.9), 5, 5)
            padding 10, 10
            has vbox xalign .5 spacing 2

            frame:
                xysize (296, 27)
                text "Indoor Slots:" xalign .02 color ivory
                text "%d/%d" % (BUILDING.in_slots, BUILDING.in_slots_max) xalign .98 style_suffix "value_text"
            frame:
                xysize (296, 27)
                text "Outdoor Slots:" xalign .02 color ivory
                text "%d/%d" % (BUILDING.ex_slots, BUILDING.ex_slots_max) xalign .98 style_suffix "value_text"
            frame:
                xysize (296, 27)
                text "Workable Capacity:" xalign .02 color ivory
                text "[BUILDING.workable_capacity]" xalign .98 style_suffix "value_text"
            frame:
                xysize (296, 27)
                text "Habitable Capacity:" xalign .02 color ivory
                text "[BUILDING.habitable_capacity]" xalign .98 style_suffix "value_text"

        null height 20

    # Manager?
    if isinstance(BUILDING, UpgradableBuilding):
        vbox:
            xalign .5
            frame:
                xmaximum 220
                ymaximum 220

                xalign .5
                background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.95), 10, 10)
                if BUILDING.manager:
                    add BUILDING.manager.show("profile", resize=(190, 190), add_mood=True, cache=True) align .5, .5
                else:
                    xysize (190, 190)
                    text "No manager" align (.5, .5) size 25 color goldenrod drop_shadow [(1, 2)] drop_shadow_color black antialias True style_prefix "proper_stats"
            if BUILDING.manager:
                text "Current manager" align (.5, .5) size 25 color goldenrod drop_shadow [(1, 2)] drop_shadow_color black antialias True style_prefix "proper_stats"
        null height 20
        if BUILDING.desc:
            text BUILDING.desc xalign.5 style_prefix "proper_stats" text_align .5 color goldenrod outlines [(1, "#3a3a3a", 0, 0)]

screen building_management_rightframe_businesses_mode:
    $ frgr = Fixed(xysize=(315, 680))
    $ frgr.add(ProportionalScale("content/gfx/images/e1.png", 315, 600, align=(.5, .0)))
    $ frgr.add(ProportionalScale("content/gfx/images/e2.png", 315, 600, align=(.5, 1.0)))
    frame:
        style_prefix "content"
        xysize 315, 680
        background Null()
        foreground frgr
        frame:
            pos 25, 20
            xysize 260, 40
            background Frame("content/gfx/frame/namebox5.png", 10, 10)
            label (u"__ [bm_mid_frame_mode.name] __") text_size 18 text_color ivory align .5, .6
        null height 5

        if isinstance(bm_mid_frame_mode, ExplorationGuild):
            use building_management_rightframe_exploration_guild_mode
        else:
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
                align .5, .5
                padding 10, 10
                vbox:
                    style_group "wood"
                    align .5, .5
                    spacing 10
                    button:
                        xysize 150, 40
                        yalign .5
                        action Return(["bm_mid_frame_mode", "building"])
                        tooltip ("Here you can invest your gold and resources for various improvements.\n"+
                                 "And see the different information (reputation, rank, fame, etc.)")
                        text "Building" size 15

screen building_management_leftframe_building_mode:
    # Stats:
    frame:
        background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
        style_prefix "proper_stats"
        xsize 316
        padding 10, 10
        has vbox spacing 1

        # We are not really using this anymore?
        # Security Rating:
        # frame:
        #     xysize (296, 27)
        #     text "Security Rating:" xalign .02 color ivory
        #     text "%s/1000" % building.security_rating xalign .98 style_suffix "value_text" yoffset 4
        # INSTEAD: Report quarter location.
        frame:
            xysize (296, 27)
            text "Location:" xalign .02 color ivory
            text "[BUILDING.location]" xalign .98 style_suffix "value_text" yoffset 4

        # Dirt:
        if isinstance(BUILDING, BuildingStats):
            frame:
                xysize (296, 27)
                button:
                    background Null()
                    xalign .02
                    margin 0, 0 padding 0, 0
                    tooltip "Dirt will never pile up in smaller buildings (10 workable capacity for any and 15 for buildings with a competent manager). Your workers will take care of it before it gets a chance!"
                    action NullAction()
                    text "Dirt:" color brown hover_color green
                text "%s (%s %%)" % (BUILDING.get_dirt_percentage()[1], BUILDING.get_dirt_percentage()[0]) xalign .98 style_suffix "value_text" yoffset 4
            frame:
                xysize (296, 27)
                button:
                    background Null()
                    xalign .02
                    margin 0, 0 padding 0, 0
                    tooltip "Threat will never effect the smaller buildings (15 workable capacity for any and 20 for buildings with a competent manager). Your workers will never allow it to increase!"
                    action NullAction()
                    text "Threat:" color crimson hover_color green
                text "%s %%" % (BUILDING.threat * 100 / BUILDING.max_stats["threat"]):
                    xalign .98
                    style_suffix "value_text"
                    yoffset 4
        if hasattr(BUILDING, "tier"):
            frame:
                xysize (296, 27)
                text "Tier:" xalign .02 color ivory
                text "%s" % (BUILDING.tier) xalign .98 style_suffix "value_text" yoffset 4

        # Fame/Rep:
        if isinstance(BUILDING, FamousBuilding):
            frame:
                xysize (296, 27)
                text "Fame:" xalign .02 color ivory
                text "%s/%s" % (BUILDING.fame, BUILDING.maxfame) xalign .98 style_suffix "value_text" yoffset 4
            frame:
                xysize (296, 27)
                text "Reputation:" xalign .02 color ivory
                text "%s/%s" % (BUILDING.rep, BUILDING.maxrep) xalign .98 style_suffix "value_text" yoffset 4

    null height 5
    # Extensions:
    frame:
        background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
        xysize (317, 480)
        if isinstance(BUILDING, UpgradableBuilding):
            frame:
                align .5, .02
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
                xysize (180, 40)
                label 'Constructed:' text_color ivory xalign .5 text_bold True
            viewport:
                pos 3, 55
                xysize 310, 406
                mousewheel True
                scrollbars "vertical"
                draggable True
                has vbox
                for u in BUILDING.all_extensions():
                    frame:
                        xalign .6
                        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 5, 5)
                        has fixed xysize 280, 80
                        frame:
                            align .05, .1
                            background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.95), 10, 10)
                            if hasattr(u, "img"):
                                add im.Scale(u.img, 100, 65) align .5, .5
                            else:
                                add Solid(black, xysize=(100, 65)) align .5, .5
                        vbox:
                            xpos 125
                            yalign .5
                            xysize 150, 60
                            text "[u.name]" xalign .5 style "proper_stats_text" size 20
                            null height 2
                            textbutton "{size=15}{font=fonts/TisaOTM.otf}{color=[goldenrod]}Details":
                                background Transform(Frame("content/gfx/interface/images/story12.png"), alpha=.8)
                                hover_background Transform(Frame(im.MatrixColor("content/gfx/interface/images/story12.png", im.matrix.brightness(.15))), alpha=1)
                                tooltip "View details or expand {}.\n{}".format(u.name, u.desc)
                                xalign .5
                                top_padding 4
                                action Return(["bm_mid_frame_mode", u])

                        imagebutton:
                            align 1.0, 0 offset 2, -2
                            idle ProportionalScale("content/gfx/interface/buttons/close4.png", 20, 24)
                            hover ProportionalScale("content/gfx/interface/buttons/close4_h.png", 20, 24)
                            insensitive im.Sepia(ProportionalScale("content/gfx/interface/buttons/close4_h.png", 20, 24))
                            action Show("yesno_prompt",
                                 message="Are you sure you wish to close this %s for %d Gold?" % (u.name, u.get_price()),
                                 yes_action=[Function(BUILDING.close_business, u, pay=True), Hide("yesno_prompt")], no_action=Hide("yesno_prompt"))
                            sensitive u.can_be_sold()
                            tooltip "Close the business"

    # frame:
        # background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
        # xysize (317, 160)
        # style_group "stats"
        # label "Active Advertisements:" text_color ivory xalign .5
        # if hasattr(building, "use_adverts") and building.use_adverts:
            # vbox:
                # null height 35
                # spacing -6
                # for advert in building.adverts:
                    # if advert['active']:
                        # frame:
                            # xysize (305, 27)
                            # text (u"%s" % advert['name']) size 16 xalign (.02)

screen building_management_leftframe_businesses_mode:
    if isinstance(bm_mid_frame_mode, ExplorationGuild):
        use building_management_leftframe_exploration_guild_mode
    else:
        use building_management_leftframe_businesses_mode_upgrades

screen building_management_midframe_building_mode:
    frame:
        background Frame("content/gfx/frame/p_frame6.png", 10, 10)
        style_prefix "content"
        xysize (630, 685)
        xalign .5
        ypos 40

        frame:
            xalign .5
            xysize (380, 50)
            background Frame("content/gfx/frame/namebox5.png", 10, 10)
            label (u"[BUILDING.name]") text_size 23 text_color ivory align (.5, .6)

        frame:
            align .5, .0
            ypos 60
            background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.95), 10, 10)
            add pscale(BUILDING.img, 600, 444)

        # Left/Right Controls + Expand button:
        vbox:
            align .5, .99
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.9), 10, 10)
                has hbox xysize (600, 74)
                button:
                    align .1, .5
                    xysize (140, 40)
                    style "left_wood_button"
                    action Return(['control', 'left'])
                    tooltip "<== Previous"
                    text "Previous" style "wood_text" xalign .69
                frame:
                    background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
                    xysize 200, 50
                    align (.5, .5)
                    if isinstance(BUILDING, UpgradableBuilding):
                        button:
                            style_prefix "wood"
                            align .5, .5
                            xysize 135, 40
                            action Return(["bm_mid_frame_mode", BUILDING])
                            tooltip 'Open a new business or upgrade this building!'
                            text "Expand"
                button:
                    align .9, .5
                    xysize (140, 40)
                    style "right_wood_button"
                    action Return(['control', 'right'])
                    tooltip "Next ==>"
                    text "Next" style "wood_text" xalign .39

            # if isinstance(building, UpgradableBuilding):
            #     frame:
            #         align .5, .95
            #         style_group "wood"
            #         background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.9), 5, 5)
            #         xpadding 20
            #         ypadding 10
            #         button:
            #             align .5, .5
            #             xysize (135, 40)
            #             action Return(["bm_mid_frame_mode", building])
            #             tooltip 'Open a new business or upgrade this building!'
            #             text "Expand"

            ## Security Bar:
            # if hasattr(building, "gui_security_bar") and building.gui_security_bar()[0]:
            #     frame:
            #         xalign .490
            #         ypos 561
            #         background Frame(Transform("content/gfx/frame/rank_frame.png", alpha=.4), 5, 5)
            #         xysize (240, 55)
            #         xpadding 10
            #         ypadding 10
            #         hbox:
            #             pos (34, 1)
            #             vbox:
            #                 xsize 135
            #                 text "Security Presence:" size 12
            #             vbox:
            #                 text (u"%d/%d"%(building.security_presence, building.gui_security_bar()[1])) size 12
            #         null height 3
            #         bar:
            #             align (.45, .8)
            #             value FieldValue(building, 'security_presence', building.gui_security_bar()[1], max_is_zero=False, style='scrollbar', offset=0, step=1)
            #             xsize 170
            #             thumb 'content/gfx/interface/icons/move15.png'

screen building_management_midframe_businesses_mode:
    frame:
        background Frame("content/gfx/frame/p_frame6.png", 10, 10)
        style_prefix "content"
        xysize (630, 685)
        xpadding 0
        xalign .5
        ypos 40

        # Fighter Guild, team launch and area info:
        if isinstance(bm_mid_frame_mode, ExplorationGuild):
            use building_management_midframe_exploration_guild_mode
        else:
            use building_management_midframe_businesses_mode_upgrades

screen building_management_leftframe_businesses_mode_upgrades:
    frame:
        background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
        style_group "proper_stats"
        xsize 310
        padding 12, 12
        margin 0, 0
        has vbox spacing 1
        # Slots:
        frame:
            xysize (290, 27)
            xalign .5
            text "Indoor Slots:" xalign .02 color ivory
            text "[bm_mid_frame_mode.in_slots]"  xalign .98 style_suffix "value_text" yoffset 4
        frame:
            xysize (290, 27)
            xalign .5
            text "Exterior Slots:" xalign .02 color ivory
            text "[bm_mid_frame_mode.ex_slots]"  xalign .98 style_suffix "value_text" yoffset 4
    $ c0 = isinstance(bm_mid_frame_mode, CoreExtension) and bm_mid_frame_mode.expands_capacity
    if bm_mid_frame_mode.capacity or c0:
        null height 5
        frame:
            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
            style_prefix "proper_stats"
            xsize 310
            padding 12, 12
            margin 0, 0
            has vbox spacing 1
            frame:
                xysize (290, 27)
                xalign .5
                text "Capacity:" xalign .02 color ivory
                text "[bm_mid_frame_mode.capacity]"  xalign .98 style_suffix "value_text" yoffset 4

            if c0 and not isinstance(bm_mid_frame_mode, ExplorationGuild):
                null height 5
                text "To Expand:"
                frame:
                    xysize (290, 27)
                    xalign .5
                    text "Indoor Slots Required:" xalign .02 color ivory
                    text "[bm_mid_frame_mode.exp_cap_in_slots]"  xalign .98 style_suffix "value_text" yoffset 4
                frame:
                    xysize (290, 27)
                    xalign .5
                    text "Exterior Slots Required:" xalign .02 color ivory
                    text "[bm_mid_frame_mode.exp_cap_ex_slots]"  xalign .98 style_suffix "value_text" yoffset 4
                frame:
                    xysize (290, 27)
                    xalign .5
                    text "Cost:" xalign .02 color ivory
                    text "[bm_mid_frame_mode.exp_cap_cost]"  xalign .98 style_suffix "value_text" yoffset 4
                null height 1
                textbutton "Expand Capacity":
                    style "pb_button"
                    xalign .5
                    if bm_mid_frame_mode.can_extend_capacity():
                        action [Function(bm_mid_frame_mode.expand_capacity),
                                Play("audio", "content/sfx/sound/world/purchase_1.ogg")]
                        tooltip "Add more space to this business!"
                    else:
                        action NullAction()
                        tooltip "Can't add more space to this business at this time!"

                null height 5
                text "To Cut Back:"
                frame:
                    xysize (290, 27)
                    xalign .5
                    text "Indoor Slots Freed:" xalign .02 color ivory
                    text "[bm_mid_frame_mode.exp_cap_in_slots]"  xalign .98 style_suffix "value_text" yoffset 4
                frame:
                    xysize (290, 27)
                    xalign .5
                    text "Exterior Slots Freed:" xalign .02 color ivory
                    text "[bm_mid_frame_mode.exp_cap_ex_slots]"  xalign .98 style_suffix "value_text" yoffset 4
                frame:
                    xysize (290, 27)
                    xalign .5
                    text "Cost:" xalign .02 color ivory
                    text "[bm_mid_frame_mode.exp_cap_cost]"  xalign .98 style_suffix "value_text" yoffset 4
                null height 1
                textbutton "Reduce Capacity":
                    style "pb_button"
                    xalign .5
                    if bm_mid_frame_mode.can_reduce_capacity():
                        action [Function(bm_mid_frame_mode.reduce_capacity),
                                Play("audio", "content/sfx/sound/world/purchase_1.ogg")]
                        tooltip "Add more space to the building!"
                    else:
                        action NullAction()
                        tooltip "The only remaining option is to close the business"

    if getattr(bm_mid_frame_mode, "upgrades", []):
        null height 5
        frame:
            align .5, .02
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
            xysize (180, 40)
            label 'Constructed:' text_color ivory xalign .5 text_bold True
        viewport:
            pos 3, 10
            xysize 310, 406
            mousewheel True
            scrollbars "vertical"
            has vbox
            for u in bm_mid_frame_mode.upgrades:
                button:
                    xsize 291
                    style "pb_button"
                    text "[u.name]":
                        align .5, .5
                        color ivory
                    action NullAction()
                    tooltip u.desc

screen building_management_midframe_businesses_mode_upgrades:
    viewport:
        xysize 620, 668
        mousewheel True
        xalign .5
        has vbox xsize 618
        if hasattr(bm_mid_frame_mode, "all_possible_extensions"):
            for u in bm_mid_frame_mode.all_possible_extensions():
                if not bm_mid_frame_mode.has_extension(u):
                    frame:
                        xalign .5
                        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
                        has fixed xysize 500, 150

                        $ cost, materials, in_slots, ex_slots = BUILDING.get_extension_cost(u)

                        hbox:
                            xalign .5
                            xsize 340
                            textbutton "[u.NAME]":
                                xalign .5
                                ypadding 5
                                style "stats_text"
                                text_size 18
                                action NullAction()
                                tooltip u.DESC

                        # Materials and GOLD
                        vbox:
                            pos 5, 30
                            box_wrap True
                            xysize 340, 100
                            spacing 2
                            frame:
                                background Frame("content/gfx/frame/p_frame5.png", 5, 5)
                                xsize 100
                                has hbox xsize 90
                                button:
                                    background Frame("content/gfx/animations/coin_top 0.13 1/1.webp")
                                    xysize 25, 25
                                    align 0, .5
                                    action NullAction()
                                    tooltip "Gold"
                                style_prefix "proper_stats"
                                if hero.gold >= cost:
                                    text "[cost]" align .95, .5
                                else:
                                    text "[cost]" align .95, .5 color grey

                            # We presently allow for 3 resources each upgrade. If more, this needs to be a conditioned viewport:
                            for r, amount in materials.items():
                                $ r = items[r]
                                # $ amount = u.MATERIALS[r.id]
                                frame:
                                    background Frame("content/gfx/frame/p_frame5.png", 5, 5)
                                    xsize 100
                                    has hbox xsize 90
                                    button:
                                        xysize 25, 25
                                        background Frame(r.icon)
                                        align 0, .5
                                        action NullAction()
                                        tooltip "{}".format(r.id)
                                    style_prefix "proper_stats"
                                    if hero.inventory[r.id] >= amount:
                                        text "[amount]" align .95, .5
                                    else:
                                        text "[amount]" align .95, .5 color grey

                        hbox:
                            align .01, .98
                            spacing 2
                            style_prefix "proper_stats"
                            if in_slots:
                                text "Indoor Slots:"
                                if (BUILDING.in_slots_max - BUILDING.in_slots) >= in_slots:
                                    text "[in_slots]"
                                else:
                                    text "[in_slots]" color grey
                            if ex_slots:
                                text "Exterior Slots:"
                                if (BUILDING.ex_slots_max - BUILDING.ex_slots) >= ex_slots:
                                    text "[ex_slots]"
                                else:
                                    text "[ex_slots]" color grey

                        vbox:
                            align 1.0, .5
                            xsize 150
                            button:
                                xalign .5
                                xysize 133, 83
                                background Frame("content/gfx/frame/MC_bg3.png", 3, 3)
                                foreground Transform(u.IMG, size=(120, 75), align=(.5, .5))
                                action NullAction()
                                tooltip u.DESC
                            textbutton "Build":
                                xalign .5
                                style "pb_button"
                                text_size 15
                                action [Return(["upgrade", "build", u, bm_mid_frame_mode]),
                                        SensitiveIf(BUILDING.eval_extension_build(u,
                                                    price=(cost, materials, in_slots, ex_slots)))]

screen building_controls():
    modal True
    zorder 1

    frame:
        style_prefix "content"
        background Frame("content/gfx/frame/p_frame52.webp", 10, 10)
        at slide(so1=(600, 0), t1=.7, eo2=(1300, 0), t2=.7)
        xpos 936
        yalign .95
        xysize 343, 675

        # Controls themselves ---------------------------------->
        vbox:
            style_group "basic"
            xalign .5 ypos 30

            button:
                xysize 200, 32
                xalign .5
                action Return(['maintenance', "rename_building"])
                tooltip "Give new name to your Building!"
                text "Rename Building"

            if isinstance(BUILDING, BuildingStats):
                null height 20
                label (u"Cleaning Options:"):
                    style "proper_stats_label"
                    align .5, .05
                    text_bold True
                null height 5

                hbox:
                    xysize 200, 32
                    xalign .5
                    bar:
                        xmaximum 120
                        align .5, .5
                        if BUILDING.auto_clean == 100:
                            value 100
                            range 100
                        else:
                            value FieldValue(BUILDING, "auto_clean", 99, style='scrollbar', offset=0, step=1)
                            thumb 'content/gfx/interface/icons/move15.png'
                            tooltip "Cleaners are called if dirt is more than %d%%" % BUILDING.auto_clean
                    button:
                        xalign 1.0
                        action Return(['maintenance', "toggle_clean"])
                        selected BUILDING.auto_clean != 100
                        tooltip "Toggle automatic hiring of cleaners"
                        text "Auto"

                button:
                    xysize 200, 32
                    xalign .5
                    action Return(['maintenance', "clean"])
                    tooltip "Hire cleaners to completely clean this building for %d Gold." % BUILDING.get_cleaning_price()
                    text "Clean: Building"

                python:
                    price = 0
                    for i in hero.buildings:
                        if isinstance(i, BuildingStats):
                            price = price + i.get_cleaning_price()

                button:
                    xysize 200, 32
                    xalign .5
                    action Return(['maintenance', "clean_all", price])
                    tooltip "Hire cleaners to completely clean all buildings for %d Gold." % price
                    text "Clean: All Buildings"

            if isinstance(BUILDING, UpgradableBuilding):
                null height 20
                label u"Management Options:":
                     style "proper_stats_label"
                     xalign .5
                     text_bold True
                null height 5

                default fields = [
                    "init_pep_talk", "cheering_up", "asks_clients_to_wait",
                                 "help_ineffective_workers", "works_other_jobs"]
                default human_readable = [
                    "Pep Talk", "Cheer Up", "Meeting Clients",
                    "Handle Clients", "Work Other Jobs"]
                default tts = [
                    "Manager will talk to workers before the start of every workday to try and motivate them.",
                    "Manager will try to cheer up girls who seem sad or tired.",
                    "Manager will ask clients to wait if there is no spot available in their favorite business.",
                    "Manager will try to talk down clients who received inadequate service and attempt to salvage payment for the service provided.",
                    "Manager will work other Jobs than her own if there are no dedicated worker available."]

                for field, name, tt in zip(fields, human_readable, tts):
                    button:
                        xysize 200, 32
                        xalign .5
                        action ToggleField(BUILDING, field)
                        tooltip tt
                        text "[name]"

                null height 5
                python:
                    desc0 = "==> {} Rule".format(BUILDING.workers_rule.capitalize())
                    desc1 = "Choose a rule your workers are managed by!"
                    desc2 = BUILDING.WORKER_RULES_DESC[BUILDING.workers_rule]
                    desc = "\n".join([desc0, desc1, desc2])
                button:
                    xysize 200, 32
                    xalign .5
                    action Function(BUILDING.toggle_workers_rule)
                    tooltip "{}".format(desc)
                    text "WR: {}".format(BUILDING.workers_rule.capitalize())

        button:
            style_group "dropdown_gm"
            action Hide("building_controls"), With(dissolve)
            minimum 50, 30
            align .5, .97
            text "OK"
            keysym "mousedown_3"

screen building_adverts():
    modal True
    zorder 1

    frame:
        style_group "content"
        at slide(so1=(600, 0), t1=.7, eo2=(1300, 0), t2=.7)
        background Frame("content/gfx/frame/p_frame52.webp", 10, 10)
        xpos 936
        yalign .95
        xysize(343, 675)

        label (u"{size=20}{color=[ivory]}{b}Advertise!") text_outlines [(2, "#424242", 0, 0)] align (.5, .16)

        # Buttons themselves ---------------------------------->
        hbox:
            align .5, .4
            box_wrap True
            spacing 20
            for advert in BUILDING.adverts:
                vbox:
                    style_group "basic"
                    align .5, .5
                    # else:
                    if advert['name'] == "Sign" and not advert['active']:
                        button:
                            xysize 280, 32
                            tooltip advert['desc']
                            action Return(["building", 'sign', advert])
                            text "Put Up Sign for 200 gold" color black align (.5, .5) size 15
                    elif advert['name'] == "Celebrity":
                        button:
                            xysize 280, 32
                            tooltip advert['desc']
                            action Return(["building", 'celeb', advert])
                            sensitive not advert['active']
                            if not not advert['active']:
                                text "Hire a Celeb!" color black align (.5, .5) size 15
                            else:
                                text "Celebrity hired!" color black align (.5, .5) size 15
                    else:
                        button:
                            xysize 280, 32
                            tooltip advert['desc']
                            action ToggleDict(advert, "active")
                            if advert['active']:
                                text ("Stop %s!" % advert['name']) color black align (.5, .5)
                            elif advert['price'] == 0:
                                text ("Use %s for %s Gold a day!" % (advert['name'], advert['upkeep'])) color black align (.5, .5) size 15
                            elif advert['upkeep'] == 0:
                                text ("Use %s for %s Gold!" % (advert['name'], advert['price'])) color black align (.5, .5) size 15
                            else:
                                text ("Use %s for %s Gold and %s a day!" % (advert['name'], advert['price'], advert['upkeep'])) color black align (.5, .5) size 15

        button:
            style_group "dropdown_gm"
            action Hide("building_adverts"), With(dissolve)
            minimum(50, 30)
            align (.5, .97)
            text  "OK"
            keysym "mousedown_3"
