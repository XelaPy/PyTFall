screen target_practice(skill, source, targets):
    zorder 2

    on "hide":
        action Function(hide_all_targeting_closshairs, targets)

    style_group "dropdown_gm"

    default highlight_idle = False
    default return_all = False
    if "all" in skill.type:
        $ return_all = True

    python:
        img = im.Flip("content/gfx/interface/buttons/blue_arrow_up.png", vertical=True)
        idle_image = im.MatrixColor(img, im.matrix.opacity(.7))
        selected_img = im.MatrixColor(img, im.matrix.tint(1.0, .6, 1.0)*im.matrix.brightness(.15))

    if persistent.use_be_menu_targeting:
        frame:
            style_prefix "dropdown_gm"
            align .5, .5
            margin 0, 0
            padding 5, 5
            has vpgrid yminimum 30 ymaximum 300 cols 1 draggable True mousewheel True
            if return_all and len(targets) > 1:
                button:
                    padding 10, 2
                    ysize 30
                    hovered Function(show_all_targeting_closshairs, targets)
                    unhovered Function(hide_all_targeting_closshairs, targets)
                    action Return(targets)
                    text "Use on all targets!":
                        align .5, .5
                        size 15
                        hover_color red
                        style "dropdown_gm_button_text"
            else:
                for index, t in enumerate(targets):
                    $ temp = dict(what=crosshair_red,
                                  at_list=[Transform(pos=battle.get_cp(t, "center",
                                                     use_absolute=True),
                                  anchor=(.5, .5))], zorder=t.besk["zorder"]+1)
                    $ hide_action = Function(renpy.hide, "enemy__"+str(index))
                    button:
                        padding 10, 2
                        ysize 30
                        hovered Function(renpy.show, "enemy__"+str(index), **temp)
                        unhovered hide_action
                        action Return(t)
                        text "[t.name]":
                            align .5, .5
                            style "dropdown_gm_button_text"
                            size 15
                            hover_color red
    else:
        for index, t in enumerate(targets):
            $ pos = battle.get_cp(t, type="tc", yo=-40)
            $ temp = dict(what=crosshair_red,
                          at_list=[Transform(pos=battle.get_cp(t, "center",
                                             use_absolute=True),
                          anchor=(.5, .5))], zorder=t.besk["zorder"]+1)
            $ hide_action = Function(renpy.hide, "enemy__"+str(index))
            imagebutton:
                pos pos
                xanchor .5
                if highlight_idle:
                    idle selected_img
                else:
                    idle idle_image
                hover selected_img
                if return_all:
                    hovered Function(show_all_targeting_closshairs, targets), SetScreenVariable("highlight_idle", True)
                    unhovered Function(hide_all_targeting_closshairs, targets), SetScreenVariable("highlight_idle", False)
                    action Return(targets)
                else:
                    hovered Function(renpy.show, "enemy__"+str(index), **temp)
                    unhovered hide_action
                    action Return(t)

    for t in targets: # Show killed things for revival..
        if t in battle.corpses:
            add Transform(t.besprite, pos=t.cpos, alpha=.4)

        frame:
            style "dropdown_gm_frame"
            align (.5, .88)
            textbutton "Cancel":
                style "basic_button"
                action Return(False)
                keysym "mouseup_3"

screen pick_skill(char):
    zorder 2

    default menu_mode = "top"

    if menu_mode != "top":
        frame:
            align (.95, .07)
            style "dropdown_gm_frame"
            textbutton "{color=[black]}{size=-5}Back":
                style "basic_choice_button"
                xsize 100
                action SetScreenVariable("menu_mode", "top")
                keysym "mousedown_3"

    # First we'll get all the skills and sort them into: @Review: Might be a good idea to move this sorting off the screen!
    # *Attack (battle) skills.
    # *Magic skills.
    default be_items = char.get_be_items()
    python:
        attacks = list(char.attack_skills)
        attacks =  list(set(attacks)) # This will make sure that we'll never get two of the same attack skills.
        attacks.sort(key=attrgetter("name"))
        magic = list(char.magic_skills)
        try:
            magic.sort(key=attrgetter("name"))
        except AttributeError:
            raise Exception, char.name

        # We'll also try to figure out if there is at least one usable attack for them:
        # list(a for a in attacks if battle_skills[a].check_conditions(char)) # BUG IN REN'PY!
        active_attacks = list()
        for i in attacks:
            if i.check_conditions(char):
                active_attacks.append(i)
                break
        # active_magic = list(s for s in magic if battle_skills[s].check_conditions(char)) # BUG IN REN'PY!
        active_magic = list()
        for i in magic:
            if i.check_conditions(char):
                active_magic.append(i)
                break

    if menu_mode == "top":
        frame:
            style_group "dropdown_gm"
            align .5, .3
            ymaximum 400
            has vbox

            at fade_in_out(t1=.6, t2=.3)
            textbutton "Attacks":
                action SetScreenVariable("menu_mode", "attacks")
                sensitive active_attacks
            textbutton "Magic":
                action SetScreenVariable("menu_mode", "magic")
                sensitive active_magic
            textbutton "Items":
                if battle.use_items and bool(be_items):
                    action SetScreenVariable("menu_mode", "items")
                elif bool(be_items):
                    text_color dimgrey
                    action Function(notify, "You can't use items in this battle!")
                else:
                    text_color dimgrey
                    action Function(notify, "You don't have items usable in battle!")
            textbutton "Skip":
                xminimum 100
                action Return(BESkip(char))
            if battle.give_up == "surrender":
                textbutton "Surrender":
                    xminimum 100
                    action Return(BESurrender(char))
            elif battle.give_up == "escape":
                textbutton "Escape":
                    xminimum 100
                    action Return(BEEscape(char))
    elif menu_mode == "items":
        frame:
            style_prefix "dropdown_gm"
            pos (.5, .2) anchor (.5, .0)
            margin 0, 0
            padding 5, 5
            at fade_in_out(t1=.6, t2=.3)
            has vpgrid yminimum 200 ymaximum 400 cols 1 draggable True mousewheel True
            for i, amount in be_items.iteritems():
                button:
                    padding 10, 2
                    xysize 250, 30
                    action Return(i)
                    tooltip mod_to_tooltip(i.mod)
                    hbox:
                        yalign .5
                        add pscale(i.icon, 25, 25) yalign .5
                        text "[i.id]" yalign .5 style "dropdown_gm_button_text" size 12
                    text "[amount]" align 1.0, .5 style "proper_stats_label_text" color purple
    elif menu_mode == "attacks":
        frame:
            at fade_in_out(t1=.6, t2=.3)

            style_prefix "dropdown_gm"
            align .5, .36

            # Sorting off menu_pos:
            $ attacks.sort(key=attrgetter("menu_pos"))

            if not DEBUG_BE:
                vbox:
                    for skill in attacks:
                        textbutton "[skill.mn]":
                            action SensitiveIf(skill.check_conditions(char)), Return(skill)
                            tooltip ["be", skill]
            else:
                vpgrid:
                    cols 6
                    spacing 3
                    scrollbars "vertical"
                    xysize (1280, 380)
                    side_xalign .5
                    $ attacks.sort(key=attrgetter("mn"))
                    for skill in attacks:
                        textbutton "%s"%skill.mn:
                            xysize 200, 25
                            action SensitiveIf(skill.check_conditions(char)), Return(skill)
                            tooltip ["be", skill]
    elif menu_mode == "magic":
        python:
            d = OrderedDict()
            ne = []
            me = []

            for e in tgs.elemental:
                d[e] = []

            for skill in magic:
                e = skill.get_element()
                if e in d:
                    d[e].append(skill)
                else:
                    me.append(skill)
                # else:
                    # ne.append(skill)

            for e in d:
                if d[e]:
                    d[e].sort(key=attrgetter("menu_pos"))
            if me:
                me.sort(key=attrgetter("menu_pos"))

        frame:
            style_group "dropdown_gm"
            pos (.5, .2) anchor (.5, .0)
            margin 0, 0
            padding 5, 5
            has vbox

            at fade_in_out(t1=.6, t2=.3)

            hbox:
                spacing 1
                xalign .5
                for e in d:
                    if d[e]:
                        frame:
                            margin 0, 0
                            padding 1, 3
                            xalign .5
                            xysize 140, 320
                            vbox:
                                if e.icon:
                                    $ img = ProportionalScale(e.icon, 70, 70)
                                    add img align .5, .1
                                for skill in d[e]:
                                    textbutton "{=text}{color=[black]}{size=-6}[skill.mn]":
                                        padding 0, 1
                                        margin 0, 0
                                        xsize 138
                                        xalign .5
                                        action SensitiveIf(skill.check_conditions(char)), Return(skill)
                                        tooltip ["be", skill]
                if me:
                    frame:
                        margin 0, 0
                        padding 3, 3
                        xalign .5
                        xysize 140, 320
                        default me_icon = build_multi_elemental_icon()
                        vbox:
                            add ProportionalScale("content/gfx/interface/images/elements/multi.png", 70, 70) align (.5, .1) # xcenter 230 ycenter 58
                            for skill in me:
                                textbutton "{=text}{color=[black]}{size=-6}[skill.mn]":
                                    padding 0, 1
                                    margin 0, 0
                                    xsize 125
                                    xalign .5
                                    action SensitiveIf(skill.check_conditions(char)), Return(skill)
                                    tooltip ["be", skill]

screen battle_overlay(be):
    zorder 2

    # be refers to battle core instance, we access the global directly atm.
    # Everything that is displayed all the time:
    frame:
        align (.5, .99)
        background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
        style "dropdown_gm_frame"
        has viewport:
            xysize (600, 50)
            scrollbars "vertical"
            has vbox
            for entry in reversed(battle.combat_log):
                label "%s"%entry style_group "stats_value_text" text_size 14 text_color ivory

    # I'll need to condition this more appropriately later, for now this will do:
    hbox:
        spacing 2
        align .5, .01
        for member in battle.teams[0]:
            python:
                profile_img = member.show('portrait', resize=(93, 93), cache=True)
                if member in battle.corpses:
                    try:
                        profile_img = im.Sepia(profile_img)
                    except:
                        pass
                scr = renpy.get_screen("pick_skill")
                if scr:
                    char = scr.scope["_args"][0] # This is not the best code :(
                if scr and member == char:
                    portrait_frame = im.Twocolor("content/gfx/frame/MC_bg3.png", grey, grey)
                    img = "content/gfx/frame/ink_box.png"
                else:
                    portrait_frame = "content/gfx/frame/MC_bg3.png"
                    img = "content/gfx/frame/ink_box.png"

            frame:
                style_prefix "proper_stats"
                background Frame(Transform(img, alpha=.5), 5, 5)
                padding 5, 3
                has hbox spacing 3

                # Girl Image:
                frame:
                    background Frame(portrait_frame, 5 ,5)
                    xysize 95, 95
                    padding 2, 2
                    yalign .5
                    add profile_img align .5, .5 alpha .96

                # Name/Stats:
                frame:
                    padding 8, 2
                    xsize 155
                    background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=.6), 5, 5)
                    has vbox

                    label "[member.name]":
                        text_size 16
                        text_bold True
                        yalign .03
                        if isinstance(member, Char):
                            text_color pink
                        else:
                            text_color ivory

                    $ health = member.stats.delayed_stats["health"]
                    fixed:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/hp1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value AnimatedValue(value=health, range=member.get_max("health"), delay=.5, old_value=None)
                            # value health
                            # range member.get_max("health")
                            thumb None
                            xysize (150, 20)
                        text "HP" size 14 color ivory bold True xpos 8

                        if health <= member.get_max("health")*.2:
                            text "[health]" size 14 color red bold True style_suffix "value_text" xpos 125 yoffset -8
                        else:
                            text "[health]" size 14 color ivory bold True style_suffix "value_text" xpos 125 yoffset -8

                    $ mp = member.stats.delayed_stats["mp"]
                    fixed:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/mp1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value AnimatedValue(value=mp, range=member.get_max("mp"), delay=.5, old_value=None)
                            # value mp
                            # range member.get_max("mp")
                            thumb None
                            xysize (150, 20)
                        text "MP" size 14 color ivory bold True xpos 8
                        if mp <= member.get_max("mp")*.2:
                            text "[mp]" size 14 color red bold True style_suffix "value_text" xpos 125 yoffset -8
                        else:
                            text "[mp]" size 14 color ivory bold True style_suffix "value_text" xpos 125 yoffset -8

                    $ vitality = member.stats.delayed_stats["vitality"]
                    fixed:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/vitality1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value AnimatedValue(value=vitality, range=member.get_max("vitality"), delay=.5, old_value=None)
                            # value vitality
                            # range member.get_max("vitality")
                            thumb None
                            xysize (150, 20)
                        text "VP" size 14 color ivory bold True xpos 8
                        if vitality <= member.get_max("vitality")*.2:
                            text "[vitality]" size 14 color red bold True style_suffix "value_text" xpos 125 yoffset -8
                        else:
                            text "[vitality]" size 14 color ivory bold True style_suffix "value_text" xpos 125 yoffset -8

    # Overlay for stats:
    # use be_status_overlay() Moving to a better location...

    if DEBUG_BE:
        vbox:
            align (.99, 0)
            textbutton "Terminate":
                action SetField(be, "terminate", True)

    $ img = im.Scale("content/gfx/interface/buttons/close.png", 35, 35)

    if DEBUG:
        imagebutton:
            align(.995, .005)
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(.25))
            insensitive_background im.Sepia(img)
            action MainMenu()

    # Pos visualization:
    # if True:
    #     for placement, coords in BDP.items():
    #         if len(placement) == 2:
    #             for pos in coords:
    #                 add Solid("F00", xysize=(5, 5)):
    #                     pos pos
    #                     anchor .5, .5
    #         else: # Middle!
    #             add Solid("000", xysize=(10, 10)):
    #                 pos coords
    #                 anchor .5, .5

screen be_status_overlay():
    zorder 1
    # This screen will add overlay to the screen.
    for fighter in battle.get_fighters(state="alive"):
        # Get coords for each box:
        $ temp = battle.get_cp(fighter, type="sopos", yo=-45)

        hbox:
            pos temp xanchor .5
            for status_icon in fighter.status_overlay:
                add Text(ProportionalScale(status_icon, 30, 30)) at status_overlay(sv1=.8, ev1=1.0, t1=.9, sv2=1.0, ev2=.8, t2=.9) yalign .5
