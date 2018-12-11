label arena_inside:

    # Music related:
    if not "arena_inside" in ilists.world_music:
        $ ilists.world_music["arena_inside"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("arena_inside")]
    play world choice(ilists.world_music["arena_inside"]) fadein 1.5

    scene expression "content/gfx/bg/be/battle_arena_1.webp"
    show screen arena_inside
    with fade

    # Predicting:
    python:
        arena_img_predict = ["chainfights", "bg battle_dogfights_1", "bg battle_arena_1"]
        arena_scr_predict = ["chain_fight", "arena_minigame", "confirm_chainfight",
                             "arena_finished_chainfight", "arena_rep_ladder",
                             "arena_matches", "arena_lineups", "arena_dogfights",
                             "arena_bestiary", "arena_aftermatch", "arena_report"]
        renpy.start_predict(*arena_img_predict)
    python hide:
        for scr in store.arena_scr_predict:
            renpy.start_predict_screen(scr)


    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    $ renpy.retain_after_load()

    while 1:

        $ result = ui.interact()

        if result[0] == 'control':
            if result[1] == "hide_vic":
                hide screen arena_aftermatch
            if result[1] == 'return':
                jump arena_inside_end

        elif result[0] == "show":
            if result[1] == "bestiary":
                hide screen arena_inside
                show screen arena_bestiary
            elif result[1] == "arena":
                hide screen arena_bestiary
                show screen arena_inside

        elif result[0] == "challenge":
            if result[1] == "dogfights":
                $ pytfall.arena.dogfight_challenge(result[2])
                # pytfall.arena.start_dogfight(result[2])
            elif result[1] == "match":
                $ pytfall.arena.setup = result[2]
                $ pytfall.arena.match_challenge(result[2])
            elif result[1] == "start_match":
                $ pytfall.arena.check_before_matchfight()
            elif result[1] == "start_chainfight":
                $ pytfall.arena.check_before_chainfight()
            elif result[1] == "chainfight":
                $ pytfall.arena.execute_chainfight()

label arena_inside_end:
    $ renpy.stop_predict(*arena_img_predict)
    python hide:
        for scr in store.arena_scr_predict:
            renpy.stop_predict_screen(scr)

    stop world fadeout 1.5
    hide screen arena_inside
    jump arena_outside

init: # Main Screens:
    style arena_channenge_frame:
        clear
        background Frame("content/gfx/frame/p_frame4.png", 10, 10)
        yalign .5
        yoffset 2
        padding (3, 12)
        margin (0, 0)
        xysize (250, 135)

    style arena_channenge_button:
        yalign .5
        yoffset 2
        margin (0, 0)
        xysize (250, 135)
        background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
        hover_background Frame("content/gfx/frame/p_frame4.png", 10, 10)

    screen arena_inside():
        add "content/gfx/bg/be/battle_arena_1.webp"  xpos 100 ypos 35

        # Start match button:
        if day in hero.fighting_days:
            button:
                align .5, .28
                # xysize (200, 40)
                ypadding 15
                left_padding 15
                right_padding 40
                style "right_wood_button"
                action Return(["challenge", "start_match"])
                text "Start Match!":
                    font "fonts/badaboom.ttf"
                    size 20
                    color ivory
                    hover_color crimson

        # Kickass sign:
        frame:
            xalign .5
            ypos 39
            background Frame("content/gfx/frame/Mc_bg.png", 10, 10)
            xysize (725, 120)
            text "Get your ass kicked in our Arena!" align .5, .5 font "fonts/badaboom.ttf" color crimson size 45

        # LEFT FRAME:
        # Buttons:
        frame:
            style_group "content"
            pos (2, 39)
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=1.0), 10, 10)
            xysize (280, 682)
            has vbox align .5, .03 spacing 1

            # Beast Fights:
            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.7), 5, 5)
                padding 10, 10
                has vbox spacing 2

                frame:
                    xfill True
                    align .5, .5
                    background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                    label "{size=28}{color=[bisque]}== Beast Fights ==" xalign .5 text_outlines [(1, "#3a3a3a", 0, 0)]
                hbox:
                    style_group "basic"
                    align .5, .5
                    spacing 5
                    textbutton "{size=20}{color=[black]}Bestiary":
                        action Return(["show", "bestiary"])
                        tooltip "Info about known enemies"
                    textbutton "{size=20}{color=[black]}Survival":
                        action Return(["challenge", "start_chainfight"])
                        tooltip "Unranked fights vs beasts and monsters"

            # Ladders (Just Info):
            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.7), 5, 5)
                padding 10, 10
                has vbox spacing 2

                frame:
                    xfill True
                    align .5, .5
                    background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                    label "{size=28}{color=[bisque]}== Ladders ==" xalign .5 text_outlines [(1, "#3a3a3a", 0, 0)]
                hbox:
                    style_group "basic"
                    align .5, .5
                    spacing 5
                    textbutton "{size=20}{color=[black]}1v1":
                        action Show("arena_lineups", transition=dissolve, container=pytfall.arena.lineup_1v1)
                        tooltip "Best 1v1 fighters"
                    textbutton "{size=20}{color=[black]}2v2":
                        action Show("arena_lineups", transition=dissolve, container=pytfall.arena.lineup_2v2)
                        tooltip "Best 2v2 teams"
                    textbutton "{size=20}{color=[black]}3v3":
                        action Show("arena_lineups", transition=dissolve, container=pytfall.arena.lineup_3v3)
                        tooltip "Best 3v3 teams"

            # Official matches:
            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.7), 5, 5)
                padding 10, 10
                has vbox spacing 2

                frame:
                    xfill True
                    align .5, .5
                    background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                    label "{size=28}{color=[bisque]}== Matches ==" xalign .5 text_outlines [(1, "#3a3a3a", 0, 0)]
                hbox:
                    align .5, .5
                    spacing 5
                    style_group "basic"
                    textbutton "{size=20}{color=[black]}1v1":
                        action Show("arena_matches", container=pytfall.arena.matches_1v1, transition=dissolve, vs_img=ProportionalScale("content/gfx/interface/images/vs_2.webp", 100, 100))
                        tooltip "Ranked 1v1 fights"
                    textbutton "{size=20}{color=[black]}2v2":
                        action Show("arena_matches", container=pytfall.arena.matches_2v2, transition=dissolve, vs_img=ProportionalScale("content/gfx/interface/images/vs_3.webp", 100, 100))
                        tooltip "Ranked team 2v2 fights"
                    textbutton "{size=20}{color=[black]}3v3":
                        action Show("arena_matches", container=pytfall.arena.matches_3v3, transition=dissolve, vs_img=ProportionalScale("content/gfx/interface/images/vs_4.webp", 100, 100))
                        tooltip "Ranked team fights 3v3 fights"


            # Dogfights:
            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.7), 5, 5)
                padding 10, 10
                has vbox spacing 2

                frame:
                    xfill True
                    align .5, .5
                    background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                    label ("{size=28}{color=[bisque]}== Dogfights ==") xalign .5 text_outlines [(1, "#3a3a3a", 0, 0)]
                hbox:
                    style_group "basic"
                    align .5, .5
                    spacing 5
                    textbutton "{size=20}{color=[black]}1v1":
                        action Show("arena_dogfights", transition=dissolve, container=pytfall.arena.dogfights_1v1)
                        tooltip "Unranked 1v1 fights"
                    textbutton "{size=20}{color=[black]}2v2":
                        action Show("arena_dogfights", transition=dissolve, container=pytfall.arena.dogfights_2v2)
                        tooltip "Unranked team 2v2 fights"
                    textbutton "{size=20}{color=[black]}3v3":
                        action Show("arena_dogfights", transition=dissolve, container=pytfall.arena.dogfights_3v3)
                        tooltip "Unranked team 3v3 fights"

        # RIGHT FRAME::
        # Hero stats + Some Buttons:
        frame:
            xalign 1.0
            ypos 39
            background Frame("content/gfx/frame/p_frame5.png", 5, 5)
            xysize 282, 682
            style_prefix "proper_stats"
            has vbox align .5, .0

            null height 10

            # Player Stats:
            frame:
                xalign .5
                padding 5, 1
                background Frame("content/gfx/frame/ink_box.png", 5, 5)
                has hbox spacing 2

                frame:
                    background Frame("content/gfx/frame/MC_bg3.png", 5, 5)
                    $ img = hero.show("portrait", resize=(95, 95), cache=True)
                    padding 2, 2
                    yalign .5
                    add img align .5, .5

                # Name + Stats:
                frame:
                    padding 8, 2
                    background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=.6), 5, 5)
                    xsize 155
                    has vbox

                    label "[hero.name]":
                        text_size 16
                        text_bold True
                        yalign .03
                        text_color ivory

                    fixed: # HP:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/hp1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value hero.health
                            range hero.get_max("health")
                            thumb None
                            xysize (150, 20)
                        text "HP" size 14 color ivory bold True xpos 8
                        if hero.health <= hero.get_max("health")*.2:
                            text "[hero.health]" size 14 color red style_suffix "value_text" xpos 125 yoffset -8
                        else:
                            text "[hero.health]" size 14 color ivory bold True style_suffix "value_text" xpos 125 yoffset -8

                    fixed: # MP:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/mp1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value hero.mp
                            range hero.get_max("mp")
                            thumb None
                            xysize (150, 20)
                        text "MP" size 14 color ivory bold True xpos 8
                        if hero.mp <= hero.get_max("mp")*.2:
                            text "[hero.mp]" size 14 color red bold True style_suffix "value_text" xpos 125 yoffset -8
                        else:
                            text "[hero.mp]" size 14 color ivory bold True style_suffix "value_text" xpos 125 yoffset -8

                    fixed: # VP:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/vitality1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value hero.vitality
                            range hero.get_max("vitality")
                            thumb None
                            xysize (150, 20)
                        text "VP" size 14 color ivory bold True xpos 8
                        if hero.vitality <= hero.get_max("vitality")*.2:
                            text "[hero.vitality]" size 14 color red bold True style_suffix "value_text" xpos 125 yoffset -8
                        else:
                            text "[hero.vitality]" size 14 color ivory bold True style_suffix "value_text" xpos 125 yoffset -8

            # Rep:
            frame:
                background im.Scale("content/gfx/frame/frame_bg.png", 270, 110)
                xysize (270, 110)
                label "Reputation: [hero.arena_rep]" text_size 25 text_color ivory align .5, .5:
                    if len(str(hero.arena_rep)) > 7:
                        text_size 20

            # Buttons:
            frame:
                background im.Scale("content/gfx/frame/frame_bg.png", 270, 110)
                style_group "basic"
                xysize (270, 110)
                vbox:
                    align (.5, .5)
                    spacing 10
                    textbutton "Show Daily Report":
                        xalign .5
                        action Show("arena_report")
                        tooltip "View yesterday's Arena events"
                    textbutton "Reputation Ladder":
                        xalign .5
                        action Show("arena_rep_ladder")
                        tooltip "View top fighters by highest reputation"

        use top_stripe(True)

    screen arena_matches(container=None, vs_img=None):
        # Screens used to display and issue challenges in the official matches inside of Arena:
        modal True
        zorder 1

        frame:
            background Frame("content/gfx/frame/p_frame52.webp", 10, 10)
            xysize (721, 565)
            at slide(so1=(0, 1200), t1=.7, eo2=(0, 1200), t2=.7)
            pos (280, 154)

            side "c r":
                pos (5, 5)
                maximum (710, 515)
                viewport id "vp_matches":
                    draggable True
                    mousewheel True
                    child_size (710, 10000)
                    has vbox spacing 5

                    # for lineup in pytfall.arena.matches_3v3:
                    $ temp = sorted(container, key=itemgetter(2))
                    for lineup in temp:
                        if lineup[1]:
                            frame:
                                style_group "content"
                                xalign .5
                                xysize (690, 150)
                                margin 0, 0
                                padding 3, 3
                                background Frame(Transform("content/gfx/frame/p_frame7.webp", alpha=1.0), 10, 10)
                                has hbox # xysize (690, 150)

                                # Day of the fight:
                                fixed:
                                    xoffset 15
                                    xysize (100, 100)
                                    align (.5, .5)
                                    frame:
                                        background Frame(Transform("content/gfx/frame/rank_frame.png", alpha=1.0), 10, 10)
                                        xsize 80
                                        vbox:
                                            xalign .5
                                            label "Day:":
                                                align .5, .5
                                                text_color goldenrod
                                                text_size 20
                                            null height 10

                                            label "[lineup[2]]":
                                                align .5, .5
                                                text_color goldenrod
                                                text_size 25

                                # Challenge button:
                                if not lineup[0]:
                                    button:
                                        style "arena_channenge_button"
                                        action Return(["challenge", "match", lineup])
                                        vbox:
                                            align (.5, .5)
                                            $ team = lineup[1]
                                            style_prefix "arena_badaboom"
                                            text "Challenge!" size 40 
                                            text ("Enemy level: %s" % team.get_level()) outlines [(1, "#3a3a3a", 0, 0)]
                                            text ("Reputation: %s" % team.get_rep()) size 20 outlines [(1, "#3a3a3a", 0, 0)] 

                                # Or we show the team that challenged:
                                else:
                                    frame:
                                        style "arena_channenge_frame"
                                        frame:
                                            align .5, .0
                                            padding 5, 3
                                            background Frame("content/gfx/frame/rank_frame.png", 5, 5)
                                            $ name = lineup[0][0].nickname if len(lineup[0]) == 1 else lineup[0].name
                                            label "[name]" align .5, .5 text_size 20 text_style "proper_stats_text" text_color gold:
                                                if len(name) > 15:
                                                    text_size 15
                                        hbox:
                                            spacing 3
                                            align .5, 1.0
                                            for fighter in lineup[0]:
                                                frame:
                                                    background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                                                    padding 2, 2
                                                    add fighter.show("portrait", resize=(60, 60))

                                add vs_img yalign .5

                                # Waiting for the challenge or been challenged by former:
                                frame:
                                    style "arena_channenge_frame"
                                    $ team = lineup[1]
                                    $ name = team[0].nickname if len(team) == 1 else team.name
                                    $ size = 15 if len(name) > 15 else 25
                                    frame:
                                        align .5, .0
                                        padding 5, 1
                                        background Frame("content/gfx/frame/rank_frame.png", 5, 5)
                                        $ text = "[name]"
                                        text text:
                                            align .5, .0
                                            size size
                                            style "proper_stats_text"
                                            color gold
                                    hbox:
                                        spacing 3
                                        align .5, 1.0
                                        for fighter in lineup[1]:
                                            frame:
                                                background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                                                padding 2, 2
                                                add fighter.show("portrait", resize=(60, 60))

                vbar value YScrollValue("vp_matches")
            button:
                style_group "basic"
                action Hide("arena_matches")
                minimum(50, 30)
                align (.5, .9995)
                text  "Close"
                keysym "mousedown_3"

    screen arena_lineups(container): # Ladders
        modal True
        zorder 1

        frame:
            background Frame("content/gfx/frame/p_frame52.webp", 10, 10)
            at slide(so1=(0, 1200), t1=.7, eo2=(0, 1200), t2=.7)
            style_group "content"
            pos (280, 154)
            xysize (721, 565)

            side "c r":
                pos (5, 5)
                maximum (710, 515)
                viewport:
                    id "arena_lineups"
                    draggable True
                    mousewheel True
                    child_size (700, 10000)
                    has vbox spacing 5
                    for index, team in enumerate(container):
                        $ index += 1
                        frame:
                            xalign .5
                            xysize (695, 60)
                            background Frame(Transform("content/gfx/frame/p_frame7.webp", alpha=1.0), 10, 10)
                            padding 1, 1
                            has hbox spacing 5
                            fixed:
                                xysize 60, 55
                                yalign .5
                                label "[index]":
                                    text_color goldenrod
                                    text_size 30
                                    align .5, .5
                            if team:
                                frame:
                                    align (.5, .6)
                                    xysize (100, 45)
                                    background Frame("content/gfx/frame/rank_frame.png", 5, 5)
                                    $ lvl = team.get_level
                                    text("Lvl [team[0].level]") align .5, .5 size 25 style "proper_stats_text" color gold
                                $ name = team[0].nickname if len(team) == 1 else team.name
                                hbox:
                                    yoffset 1
                                    yalign .5
                                    spacing 1
                                    ysize 55
                                    for fighter in team:
                                        frame:
                                            yalign .5
                                            background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                                            padding 3, 3
                                            add fighter.show("portrait", resize=(45, 45), cache=True)
                                null width 12
                                frame:
                                    align (.5, .5)
                                    xfill True
                                    background Frame("content/gfx/frame/rank_frame.png", 5, 5)
                                    label "[name]" align .5, .5 text_size 25 text_style "proper_stats_text" text_color gold:
                                        if len(name) > 15:
                                            text_size 15

                vbar value YScrollValue("arena_lineups")

            button:
                style_group "basic"
                action Hide("arena_lineups")
                minimum(50, 30)
                align (.5, .9995)
                text  "Close"
                keysym "mousedown_3"

    screen arena_rep_ladder():
        modal True
        zorder 1

        frame:
            background Frame("content/gfx/frame/p_frame52.webp", 10, 10)
            xysize (721, 565)
            at slide(so1=(0, 1200), t1=.7, eo2=(0, 1200), t2=.7)
            pos (280, 154)

            side "c r":
                pos (5, 5)
                maximum (710, 515)
                viewport id "arena_rep_vp":
                    draggable True
                    mousewheel True
                    child_size (700, 1000)
                    has vbox spacing 5
                    for index, fighter in enumerate(pytfall.arena.ladder):
                        $ index += 1
                        frame:
                            style_group "content"
                            xalign .5
                            xysize (690, 60)
                            background Frame(Transform("content/gfx/frame/p_frame7.webp", alpha=1.0), 10, 10)
                            has hbox spacing 20
                            textbutton "{color=[red]}[index]":
                                ypadding 5
                                background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                                xysize (50, 50)
                                text_size 20
                                xfill True
                            if fighter:
                                frame:
                                    background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                                    padding 2, 2
                                    add fighter.show("portrait", resize=(40, 40))
                                    yalign .5
                                frame:
                                    align (.5, .5)
                                    xsize 100
                                    background Frame("content/gfx/frame/rank_frame.png", 5, 5)
                                    text("Lvl [fighter.level]") align .5, .5 size 25 style "proper_stats_text" color gold
                                frame:
                                    xfill True
                                    align (.5, .5)
                                    background Frame("content/gfx/frame/rank_frame.png", 5, 5)
                                    hbox:
                                        xfill True
                                        align (.5, .5)
                                        text("[fighter.name]") align .03, .5 size 25 style "proper_stats_text" color gold
                                        text("[fighter.arena_rep]") align .99, .5 size 20 style "proper_stats_value_text" color gold

                vbar value YScrollValue("arena_rep_vp")

            button:
                style_group "basic"
                action Hide("arena_rep_ladder")
                minimum(50, 30)
                align (.5, .9995)
                text  "Close"
                keysym "mousedown_3"

    screen arena_dogfights(container):
        modal True
        zorder 1

        frame:
            style_group "content"
            background Frame("content/gfx/frame/p_frame52.webp", 10, 10)
            xysize (721, 565)
            at slide(so1=(0, 1200), t1=.7, eo2=(0, 1200), t2=.7)
            pos (280, 154)

            side "c r":
                pos (5, 5)
                maximum (710, 515)
                viewport:
                    id "vp_dogfights"
                    draggable True
                    mousewheel True
                    child_size (700, 10000)
                    has vbox spacing 5
                    for team in sorted(container, key=methodcaller("get_level")):
                        frame:
                            style_group "content"
                            padding 5, 3
                            xalign .5
                            xysize (695, 150)
                            background Frame(Transform("content/gfx/frame/p_frame7.webp", alpha=1.0), 10, 10)
                            has hbox xalign .5
                            button:
                                style "arena_channenge_button"
                                action Hide("arena_dogfights"), Return(["challenge", "dogfights", team])
                                $ level = team.get_level()
                                vbox:
                                    align (.5, .5)
                                    text "Challenge!" size 40 color red + "85" hover_color red align .5, .5 font "fonts/badaboom.ttf" outlines [(2, "#3a3a3a", 0, 0)]
                                    text "Enemy level: [level]" size 30 color red + "85" hover_color red align .5, .5 font "fonts/badaboom.ttf" outlines [(1, "#3a3a3a", 0, 0)]

                            add ProportionalScale("content/gfx/interface/images/vs_1.webp", 130, 130) yalign .5

                            frame:
                                style "arena_channenge_frame"
                                $ name = team[0].nickname if len(team) == 1 else team.name
                                $ size = 15 if len(name) > 15 else 25
                                frame:
                                    align .5, .0
                                    padding 5, 1
                                    background Frame("content/gfx/frame/rank_frame.png", 5, 5)
                                    text ("[name] {color=[red]}"):
                                        align .5, .0
                                        size size
                                        style "proper_stats_text"
                                        color gold
                                hbox:
                                    spacing 3
                                    align .5, 1.0
                                    for fighter in team:
                                        frame:
                                            padding 2, 2
                                            background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                                            add fighter.show("portrait", resize=(60, 60))

                vbar value YScrollValue("vp_dogfights")

            button:
                style_group "basic"
                action Hide("arena_dogfights")
                minimum(50, 30)
                align (.5, .9995)
                text  "Close"
                keysym "mousedown_3"

    python:
        def set_bestiary_mob(data):
            id = data["id"]
            level = data['min_lvl']
            store.mob = build_mob(id=id, level=level)

    screen arena_bestiary():
        default in_focus_mob = False
        default scr_mobs = sorted(mobs.values(), key=itemgetter("min_lvl"))

        add("content/gfx/bg/locations/arena_bestiary.webp")

        vpgrid:
            at fade_in_out()
            cols 4
            ysize 720
            draggable True
            mousewheel True
            scrollbars "vertical"
            for data in scr_mobs:
                $ creature = data["name"]
                $ img = ProportionalScale(data["battle_sprite"], 200, 200)
                frame:
                    background Frame("content/gfx/frame/bst.png", 5, 5)
                    margin 2, 2
                    has vbox spacing 2 xysize 230, 250
                    if not defeated_mobs.get(data["id"], 0): # <------------------------------ Note for faster search, change here to test the whole beasts screen without the need to kill mobs
                        text "-Unknown-" xalign .5  style "TisaOTM" color indianred
                        add im.Twocolor(img, black, black) xalign .5
                    else:
                        text creature xalign .5 style "TisaOTM" color gold
                        imagebutton:
                            xalign .5
                            idle img
                            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
                            action [SetScreenVariable("in_focus_mob", creature),
                                    Function(set_bestiary_mob, data)]

        frame:
            xalign 1.0
            background Frame("content/gfx/frame/p_frame5.png")
            xysize 277, 720
            has vbox
            if in_focus_mob:
                $ data = mobs[in_focus_mob]
                $ img = ProportionalScale(data["battle_sprite"], 200, 200)
                $ portrait = im.Scale(data["portrait"], 100, 100)

                null height 5
                hbox:
                    frame:
                        xalign .5
                        yalign .0
                        background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                        add portrait

                    vbox:
                        style_group "proper_stats"
                        xalign .0
                        spacing 1
                        frame:
                            xalign .5
                            yfill True
                            background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.6), 10, 10)
                            xysize (145, 30)
                            text (u"{color=#CDAD00} Race") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] align (.5, .7)
                        frame:
                            xalign .5
                            yfill True
                            xysize (148, 30)
                            text (data["race"]) xalign .5 yalign .5 style "stats_value_text" color "#79CDCD" size 15


                null height 5
                hbox:
                    frame:
                        $ els = [traits[el] for el in data["traits"] if traits[el] in tgs.elemental]
                        $ els_transforms = [Transform(e.icon, size=(100, 100)) for e in els]
                        $ other_traits = data["traits"]
                        style_group "content"
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=.5), 10, 10)
                        xysize 110, 110
                        xalign .5

                        $ x = 0
                        $ els_args = [Transform(i, crop=(100/len(els_transforms)*els_transforms.index(i), 0, 100/len(els), 100), subpixel=True, xpos=(x + 100/len(els)*els_transforms.index(i))) for i in els_transforms]
                        $ f = Fixed(*els_args, xysize=(100, 100))
                        add f align (.5, .5)
                        add ProportionalScale("content/gfx/interface/images/elements/hover.png", 100, 100) align (.5, .5)
                    vbox:
                        style_group "proper_stats"
                        xalign .0
                        spacing 1
                        frame:
                            xalign .5
                            yfill True
                            background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.6), 10, 10)
                            xysize (145, 30)
                            text (u"{color=#CDAD00} Class") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] align (.5, .7)
                        for t in data["basetraits"]:
                            frame:
                                xalign .5
                                xysize (148, 30)
                                yfill True
                                text t xalign .5 yalign .5 style "stats_value_text" color "#79CDCD" size 15
                null height 5
                # Stats:
                frame:
                    xalign .5
                    yfill True
                    background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.6), 10, 10)
                    xysize (260, 30)
                    text (u"{color=#CDAD00}Level %s" % data['min_lvl']) font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] xalign .5# align (.5, 1.0)
                hbox:
                    null width 2
                    vbox:
                        $ stats = ["health", "vitality", "attack", "defence", "agility"]
                        style_group "proper_stats"
                        box_wrap 1
                        spacing 1
                        for stat in stats:
                            frame:
                                xysize (130, 22)
                                xalign .5
                                text '{}'.format(stat.capitalize()) xalign .02 color "#43CD80" size 16
                                # if stat in data["stats"]:
                                text "{}".format(getattr(mob, stat)) xalign .98 style "stats_value_text" color "#79CDCD" size 17
                                # else:
                                #     text str(20) xalign .98 style "stats_value_text" color "#79CDCD" size 17
                    null width 2
                    vbox:
                        $ stats = ["mp", "charisma", "magic", "intelligence", "luck"]
                        style_group "proper_stats"
                        box_wrap 1
                        spacing 1
                        for stat in stats:
                            frame:
                                xysize (130, 22)
                                xalign .5
                                text '{}'.format(stat.capitalize()) xalign .02 color "#43CD80" size 16
                                text "{}".format(getattr(mob, stat)) xalign .98 style "stats_value_text" color "#79CDCD" size 17
                                # if stat in data["stats"]:
                                #     text str(data["stats"][stat]) xalign .98 style "stats_value_text" color "#79CDCD" size 17
                                # else:
                                #     text str(20) xalign .98 style "stats_value_text" color "#79CDCD" size 17
                null height 5

                # Bottom Viewport:
                viewport:
                    xalign .5
                    xoffset 3
                    edgescroll (100, 100)
                    draggable True
                    mousewheel True
                    xysize 278, 350
                    child_size 278, 1000
                    has vbox
                    # Desc:
                    frame:
                        xalign .5
                        yfill True
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.6), 10, 10)
                        xysize (155, 30)
                        text (u"{color=#CDAD00} Description") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] xalign .5
                    vbox:
                        style_group "proper_stats"
                        xalign .5
                        if data["desc"]:
                                frame:
                                    xalign .5
                                    xsize 261
                                    text (data["desc"]) size 14 xalign .5 yalign .5 style "stats_value_text" color "#79CDCD"
                        else:
                            frame:
                                xalign .5
                                xysize (150, 30)
                                yfill True
                                text "-None-" size 17 xalign .5 yalign .5 style "stats_value_text" color indianred
                    null height 5
                    hbox:
                    # Attacks:
                        vbox:
                            frame:
                                xalign .5
                                yfill True
                                background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.6), 10, 10)
                                xysize (130, 30)
                                text (u"{color=#CDAD00} Attacks") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] xalign .5

                            vbox:
                                style_group "proper_stats"
                                xalign .5
                                if data["attack_skills"]:
                                    for s in sorted(data["attack_skills"]):
                                        frame:
                                            xalign .5
                                            xysize (130, 22)
                                            yfill True
                                            text s size 16 xalign .5 yalign .5 style "stats_value_text" color "#79CDCD":
                                                if len(s) > 12:
                                                    size 12
                                else:
                                    frame:
                                        xalign .5
                                        xysize (130, 22)
                                        yfill True
                                        text "-None-" size 17 xalign .5 yalign .5 style "stats_value_text" color indianred

                    # Spells:
                        vbox:
                            frame:
                                xalign .5
                                yfill True
                                background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.6), 10, 10)
                                xysize (130, 30)
                                text (u"{color=#CDAD00} Spells") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] xalign .5

                            vbox:
                                style_group "proper_stats"
                                xalign .5
                                spacing 1
                                if data["magic_skills"]:
                                    for s in sorted(data["magic_skills"]):
                                        frame:
                                            xalign .5
                                            xysize (130, 22)
                                            yfill True
                                            text s size 16 xalign .5 yalign .5 style "stats_value_text" color "#79CDCD":
                                                if len(s) > 12:
                                                    size 12
                                else:
                                    frame:
                                        xalign .5
                                        xysize (130, 22)
                                        yfill True
                                            text "-None-" size 17 xalign .5 yalign .5 style "stats_value_text" color indianred
                    frame:
                        xalign .5
                        yfill True
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.6), 10, 10)
                        xysize (130, 30)
                        text (u"{color=#CDAD00} Traits") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] xalign .5

                    vbox:
                        style_group "proper_stats"
                        xalign .5
                        spacing 1

                        if data["traits"]:
                            for s in sorted(data["traits"]):
                                frame:
                                    xalign .5
                                    xysize (260, 22)
                                    yfill True
                                    text s size 16 xalign .5 yalign .5 style "stats_value_text" color "#79CDCD":
                                        if len(s) > 12:
                                            size 12
                        else:
                            frame:
                                xalign .5
                                xysize (260, 22)
                                yfill True
                                text "-None-" size 17 xalign .5 yalign .5 style "stats_value_text" color indianred

        imagebutton:
            pos (1233, 670)
            idle im.Scale("content/gfx/interface/buttons/close2.png", 35, 35)
            hover im.Scale("content/gfx/interface/buttons/close2_h.png", 35, 35)
            action Return(["show", "arena"])
            keysym "mousedown_3"

    screen arena_aftermatch(w_team, l_team, condition):
        modal True
        zorder 2

        on "show" action If(condition=="Victory", true=Play("music", "content/sfx/music/world/win_screen.mp3"))

        default winner = w_team[0]
        default loser = l_team[0]

        if hero.team == w_team:
            add "content/gfx/images/battle/victory_l.webp" at move_from_to_pos_with_ease(start_pos=(-config.screen_width/2, 0), end_pos=(0, 0), t=.7, wait=0)
            add "content/gfx/images/battle/victory_r.webp" at move_from_to_pos_with_ease(start_pos=(config.screen_width/2, 0), end_pos=(0, 0), t=.7)
            add "content/gfx/images/battle/battle_c.webp" at fade_from_to(start_val=.5, end_val=1.0, t=2.0, wait=0)
            add "content/gfx/images/battle/victory.webp":
                align (.5, .5)
                at simple_zoom_from_to_with_easein(start_val=50.0, end_val=1.0, t=2.0)
        else:
            add "content/gfx/images/battle/defeat_l.webp" at move_from_to_pos_with_ease(start_pos=(-config.screen_width/2, 0), end_pos=(0, 0), t=.7)
            add "content/gfx/images/battle/defeat_r.webp" at move_from_to_pos_with_ease(start_pos=(config.screen_width/2, 0), end_pos=(0, 0), t=.7)
            add "content/gfx/images/battle/battle_c.webp" at fade_from_to(start_val=.5, end_val=1.0, t=2.0, wait=0)
            add "content/gfx/images/battle/defeat.webp":
                align (.5, .5)
                at simple_zoom_from_to_with_easein(start_val=50.0, end_val=1.0, t=2.0)

        frame:
            background Null()
            xsize 95
            xpos 2
            yalign .5
            xpadding 8
            ypadding 8
            xmargin 0
            ymargin 0
            has vbox spacing 5 align(.5, .5) box_reverse True
            $ i = 0
            for member in w_team:
                $ img = member.show("portrait", resize=(70, 70), cache=True)
                fixed:
                    align (.5, .5)
                    xysize (70, 70)
                    imagebutton:
                        at fade_from_to(start_val=0, end_val=1.0, t=2.0, wait=i)
                        ypadding 1
                        xpadding 1
                        xmargin 0
                        ymargin 0
                        align (.5, .5)
                        style "basic_choice2_button"
                        idle img
                        hover img
                        selected_idle Transform(img, alpha=1.05)
                        action SetScreenVariable("winner", member), With(dissolve)
                    $ i = i + 1

        frame:
            background Null()
            xsize 95
            align (1.0, .5)
            xpadding 8
            ypadding 8
            xmargin 0
            ymargin 0
            has vbox spacing 5 align(.5, .5)
            $ i = 0
            for member in l_team:
                $ img = member.show("portrait", resize=(70, 70), cache=True)
                fixed:
                    align (.5, .5)
                    xysize (70, 70)
                    imagebutton:
                        at fade_from_to(start_val=0, end_val=1.0, t=2.0, wait=i)
                        ypadding 1
                        xpadding 1
                        xmargin 0
                        ymargin 0
                        align (.5, .5)
                        style "basic_choice2_button"
                        idle img
                        hover img
                        selected_idle Transform(img, alpha=1.05)
                        action NullAction()
                    $ i = i + 1

        button:
            xysize (100, 30)
            align (.5, .63)
            style_group "pb"
            action [Function(renpy.music.stop, channel="music", fadeout=1.0), Return(["control", "hide_vic"])]
            text "Continue" style "pb_button_text" yalign 1.0 

        # Winner Details Display on the left:
        if winner.combat_stats == "K.O.":
            frame:
                at fade_from_to_with_easeout(start_val=.0, end_val=1.0, t=.9, wait=0)
                background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                add im.Sepia(winner.show('battle_sprite', resize=(200, 200), cache=True))
                align .2, .2
        else:
            frame:
                at fade_from_to_with_easeout(start_val=.0, end_val=1.0, t=.9, wait=0)
                background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                add winner.show("battle_sprite", resize=(200, 200), cache=True)
                align .2, .2
            null height 20
            if hero.team == w_team: # Show only if we won...
                frame:
                    style_group "proper_stats"
                    align (.2, .5)
                    background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
                    xpadding 12
                    ypadding 12
                    xmargin 0
                    ymargin 0
                    has vbox spacing 1
                    for stat in winner.combat_stats:
                        frame:
                            xalign .5
                            xysize (190, 27)
                            text '{}'.format(stat.capitalize()) xalign .02 color "#79CDCD"
                            label str(winner.combat_stats[stat]) xalign 1.0 yoffset -1

        # Looser Details Display on the left:
        if loser.combat_stats == "K.O.":
            frame:
                background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                add im.Sepia(loser.show("battle_sprite", resize=(200, 200), cache=True))
                align (.8, .2)
        else:
            frame:
                background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                add loser.show("battle_sprite", resize=(200, 200), cache=True)
                align (.8, .2)

        add "content/gfx/frame/h1.webp"

    screen arena_report():
        modal True
        frame:
            at slide(so1=(0, 1200), t1=.7, eo2=(0, 1200), t2=.7)
            pos (280, 154)
            background im.Scale("content/gfx/frame/frame_dec_1.png", 720, 580)
            xysize (720, 580)
            viewport:
                pos (50, 50)
                xysize (620, 400)
                child_size 620, 10000
                mousewheel True
                has vbox xsize 620
                if not len(pytfall.arena.daily_report):
                    text "Nothing interesting happened yesterday..." color goldenrod align .5, .5
                else:
                    text "{size=-4}%s" % "\n".join(pytfall.arena.daily_report) color goldenrod

            button:
                style_group "basic"
                action Hide("arena_report")
                minimum (50, 30)
                align (.5, .9)
                text  "Close"
                keysym "mousedown_3"

init: # ChainFights vs Mobs:
    screen chain_fight():
        modal True
        if not pytfall.arena.cf_mob:
            frame:
                background Frame("content/gfx/frame/p_frame52.webp", 10, 10)
                at slide(so1=(0, 1200), t1=.7, eo2=(0, 1200), t2=.7)
                style_group "content"
                pos (280, 154)
                xysize (721, 580)
                has vbox
                viewport:
                    scrollbars "vertical"
                    maximum (710, 515)
                    draggable True
                    mousewheel True
                    child_size (700, 5000)
                    has vbox spacing 5
                    $ i = -1
                    for setup in pytfall.arena.chain_fights_order:
                        $ i+= 1
                        frame:
                            xysize (695, 55)
                            background Frame(Transform("content/gfx/frame/p_frame7.webp", alpha=1.0), 10, 10)
                            padding 1, 1
                            # has hbox spacing 5
                            hbox:
                                yalign .5
                                frame:
                                    yalign .5
                                    xysize (350, 45)
                                    background Frame("content/gfx/frame/rank_frame.png", 5, 5)
                                    text("[setup]") align .5, .5 size 25 style "proper_stats_text" color gold
                                frame:
                                    yalign .5
                                    xysize (45, 45)
                                    background Frame("content/gfx/frame/rank_frame.png", 5, 5)
                                    add pytfall.arena.chain_fights_order_portraits[i]:
                                        align (.5, .5)
                                frame:
                                    yalign .5
                                    xysize (100, 45)
                                    background Frame("content/gfx/frame/rank_frame.png", 5, 5)
                                    $ lvl = pytfall.arena.chain_fights[setup]["level"]

                                    text("Lvl [lvl]") align .5, .5 size 25 style "proper_stats_text" color gold
                                button:
                                    xfill True
                                    ysize 60
                                    background None
                                    action [SetField(pytfall.arena, "result", setup), Return("Bupkis")]
                                    align (.5, .5)
                                    text "Fight!" size 40 color red + "85" hover_color red align .5, .5 font "fonts/badaboom.ttf" outlines [(2, "#3a3a3a", 0, 0)]
                null height 5
                button:
                    style_group "basic"
                    action SetField(pytfall.arena, "result", "break"), Return("Bupkis")
                    minimum(50, 30)
                    align (.5, .9995)
                    text  "Close"
                    keysym "mousedown_3"
        else:
            timer .5 action [SetField(pytfall.arena, "result", "break"), Return("Bupkis")]

    screen arena_minigame(data, length):
        zorder 2
        modal True

        default rolled = None

        add "content/gfx/bg/be/battle_arena_1.webp"
        text "Special Bonus Time!":
            align (.5, .1)
            italic True
            color red
            style "arena_header_text"
            size 75

        # Bonus Roll: ===========================================================================>>>
        default my_udd = ArenaBarMinigame(data, length)
        style_prefix "dropdown_gm"
        frame:
            align .5, .9
            xysize 300, 460

            add my_udd pos 50, 60

            # Results:
            if not rolled:
                text "Bonus Roll":
                    xalign .5 ypos 10
                    style "arena_header_text"
                    color red
                    size 35
            else:
                timer 3.0 action Return()
                key "mousedown_1" action Return()

                if rolled == "hp":
                    text "Rolled: HP" style "arena_header_text" color red size 30 xalign .5 ypos 10
                elif rolled == "mp":
                    text "Rolled: MP" style "arena_header_text" color blue size 30 xalign .5 ypos 10
                elif rolled == "vp":
                    text "Rolled: Vitality" style "arena_header_text" color green size 30 xalign .5 ypos 10
                else:
                    text "Rolled: Bupkis" style "arena_header_text" color black size 30 xalign .5 ypos 10

            textbutton "Stop!":
                align .5, .95
                xsize 100
                sensitive my_udd.update
                action [SetField(my_udd, "update", False),
                        SetScreenVariableC("rolled", pytfall.arena.settle_minigame,
                            udd=my_udd, d=data)]

        # Legenda:
        frame:
            align (.99, .99)
            background Frame("content/gfx/frame/p_frame4.png", 10, 10)
            padding (20, 20)
            vbox:
                spacing 10
                for color, text in [(red, "Restore HP"),
                                    (blue, "Restore MP"),
                                    (green, "Restore Vitality"),
                                    (black, "Nothing...")]:
                    hbox:
                        xalign 0
                        spacing 10
                        add Solid(color, xysize=(20, 20))
                        text text style "garamond" color goldenrod yoffset -4

    screen confirm_chainfight():
        zorder 2
        modal True

        add "content/gfx/bg/be/battle_arena_1.webp"

        if pytfall.arena.cf_count and pytfall.arena.cf_mob:

            # Fight Number:
            text "Round  [pytfall.arena.cf_count]":
                at move_from_to_pos_with_ease(start_pos=(560, -100), end_pos=(560, 150), t=.7)
                italic True
                color red
                style "arena_header_text"
                size 45

            # Opposing Sprites:
            add hero.show("battle_sprite", resize=(200, 200)) at slide(so1=(-600, 0), t1=.7, eo2=(-1300, 0), t2=.7) align .35, .5
            add pytfall.arena.cf_mob.show("battle_sprite", resize=(200, 200)) at slide(so1=(600, 0), t1=.7, eo2=(1300, 0), t2=.7) align .65, .5

            # Title Text and Boss name if appropriate:
            if pytfall.arena.cf_count == 5:
                text "Boss Fight!":
                    align .5, .01
                    at fade_in_out(t1=1.5, t2=1.5)
                    style "arena_header_text"
                    size 80
                text pytfall.arena.cf_setup["boss_name"]:
                    align .5, .75
                    at fade_in_out(t1=1.5, t2=1.5)
                    size 40
                    outlines [(2, "#000000", 0, 0)]
                    color crimson
                    style "garamond"
            else:
                text pytfall.arena.cf_setup["id"]:
                    align .5, .01
                    at fade_in_out(t1=1.5, t2=1.5)
                    style "arena_header_text"
                    size 80

        # hbox at slide(so1=(0, 700), t1=.7, so2=(0, 700), t2=.7):
        frame:
            style_prefix "dropdown_gm"
            align(.5, .9)
            has hbox spacing 40
            textbutton "Give Up":
                action [Hide("arena_inside"), Hide("chain_fight"), Hide("confirm_chainfight"),
                        SetField(pytfall.arena, "cf_count", 0),
                        SetField(pytfall.arena, "cf_mob", None),
                        SetField(pytfall.arena, "cf_setup", None),
                        Stop("music"), Jump("arena_inside")]
            textbutton "Fight":
                action [Hide("arena_inside"), Hide("chain_fight"),
                        Hide("confirm_chainfight"),
                        Return(["challenge", "chainfight"])]
            # button:
            #     text "Give Up":
            #         size 25 color goldenrod outlines [(1, "#000000", 0, 0)]
            #     xysize (180, 60)
            #     action [Hide("arena_inside"), Hide("chain_fight"), Hide("confirm_chainfight"),
            #             SetField(pytfall.arena, "cf_count", 0),
            #             SetField(pytfall.arena, "cf_mob", None),
            #             SetField(pytfall.arena, "cf_setup", None),
            #             Stop("music"), Jump("arena_inside")]
            # button:
            #     text "Fight" size 25 color goldenrod outlines [(1, "#000000", 0, 0)]
            #     xysize (180, 60)
            #     action [Hide("arena_inside"), Hide("chain_fight"),
            #             Hide("confirm_chainfight"),
            #             Return(["challenge", "chainfight"])]

    screen arena_finished_chainfight(w_team, rewards):
        zorder  3
        modal True

        key "mousedown_3" action [Hide("arena_finished_chainfight"), Hide("arena_inside"), Hide("chain_fight"), Hide("confirm_chainfight"), SetField(pytfall.arena, "cf_count", 0), Jump("arena_inside")]
        timer 9.0 action [Hide("arena_finished_chainfight"), Hide("arena_inside"), Hide("chain_fight"), Hide("confirm_chainfight"), SetField(pytfall.arena, "cf_count", 0), Jump("arena_inside")]

        add "content/gfx/bg/be/battle_arena_1.webp"

        text "Victory!":
            at move_from_to_align_with_linear(start_align=(.5, .3), end_align=(.5, .03), t=2.2)
            italic True
            color red
            style "arena_header_text"
            size 75

        vbox:
            at fade_from_to_with_easeout(start_val=.0, end_val=1.0, t=.9)
            align .95, .5
            maximum 500, 400 spacing 30
            text "Rewards:":
                xalign .5
                style "arena_header_text"

            hbox:
                xalign .5
                spacing 10
                box_wrap True
                if rewards:
                    for reward in rewards:
                        frame:
                            background Frame("content/gfx/frame/24-1.png", 5, 5)
                            xysize (90, 90)
                            add ProportionalScale(reward.icon, 80, 80) align .5, .5
                else:
                    text "No extra rewards... this is unlucky :(":
                        xalign .5
                        style "arena_header_text"
                        size 25

        # Chars + Stats
        frame:
            at fade_from_to_with_easeout(start_val=0, end_val=1.0, t=.9, wait=0)
            background Frame("content/gfx/frame/MC_bg.png", 10, 10)
            add hero.show("battle", resize=(426, 376), cache=True)
            align .1, .5

        vbox:
            at arena_stats_slide
            pos (600, 405)
            spacing 1
            if not isinstance(w_team[0].combat_stats, basestring):
                for stat in w_team[0].combat_stats:
                    fixed:
                        xysize (170, 18)
                        text stat.capitalize() xalign .03 style "dropdown_gm2_button_text" color red size 25
                        text str(w_team[0].combat_stats[stat]) xalign .97 style "dropdown_gm2_button_text" color crimson size 25
            else:
                text("{size=+20}{color=[red]}K.O.")
