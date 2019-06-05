screen set_action_dropdown(char, pos=()):
    # Trying to create a drop down screen with choices of actions:
    zorder 3
    modal True

    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    # Get mouse coords:
    python:
        x, y = pos
        xval = 1.0 if x > config.screen_width/2 else .0
        yval = 1.0 if y > config.screen_height/2 else .0

    frame:
        style_prefix "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        has vbox

        if isinstance(char.workplace, School):
            textbutton "Change Course":
                action [Hide("set_action_dropdown"),
                        Hide("charslist"),
                        Hide("char_profile"),
                        SetField(store, "char", char),
                        Jump("school_training")]
                tooltip "Change the training course to a different one."
            textbutton "Stop Course":
                action [Function(stop_course, char),
                        Hide("set_action_dropdown"), With(Dissolve(0.1))]
                tooltip "Call your girl back from the Academy to do something useful in one of your businesses."
        elif isinstance(char.workplace, UpgradableBuilding):
            $ jobs = char.workplace.get_valid_jobs(char)
            if char != hero: # Rest is not really useful for MC, which player controls.
                $ jobs.append(simple_jobs["Rest"])
            for i in jobs:
                textbutton "[i.id]":
                    action [SetField(char, "action", i),
                            Hide("set_action_dropdown"), With(Dissolve(0.1))]
                    tooltip i.desc
            textbutton "None":
                action [SetField(char, "action", None),
                        Hide("set_action_dropdown"), With(Dissolve(0.1))]
                tooltip "In case you are in a great need of a slacker..."

        textbutton "Close":
            action [Hide("set_action_dropdown"), With(Dissolve(0.1))]
            keysym "mousedown_3", "K_ESCAPE"

screen set_workplace_dropdown(char, pos=()):
    # Trying to create a drop down screen with choices of actions:
    zorder 3
    modal True

    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    # Get mouse coords:
    python:
        x, y = pos
        xval = 1.0 if x > config.screen_width/2 else .0
        yval = 1.0 if y > config.screen_height/2 else .0

    python:
        workable_buildings = []
        for b in hero.buildings:
            if isinstance(b, UpgradableBuilding) and b.workable:
                workable_buildings.append(b)

    frame:
        style_prefix "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        has vbox
        for building in workable_buildings:
            $ actions = []
            if char.action in building.jobs:
                $ actions.append(SetField(char, "workplace", building))
            else:
                $ actions.append(SetField(char, "action", None))
                $ actions.append(SetField(char, "workplace", building))
            $ actions.extend([Hide("set_workplace_dropdown"), With(Dissolve(0.1))])
            textbutton "[building.name]":
                selected char.workplace == building
                action actions
        textbutton "None":
            selected char.workplace is None
            action [SetField(char, "action", None),
                    SetField(char, "workplace", None),
                    Hide("set_workplace_dropdown"), With(Dissolve(0.1))]
        textbutton "Close":
            action Hide("set_workplace_dropdown"), With(Dissolve(0.1))
            keysym "mousedown_3", "K_ESCAPE"

screen set_home_dropdown(char, pos=()):
    # Trying to create a drop down screen with choices of actions:
    zorder 3
    modal True

    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    # Get mouse coords:
    python:
        x, y = pos
        xval = 1.0 if x > config.screen_width/2 else .0
        yval = 1.0 if y > config.screen_height/2 else .0

    default habitable_locations = [b for b in hero.buildings if (b.habitable and b.vacancies)] + [locations["Streets"]]

    frame:
        style_prefix "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        has vbox

        for loc in habitable_locations:
            textbutton "[loc]":
                selected char.home == loc
                action SetField(char, "home", loc), Hide("set_home_dropdown"), With(Dissolve(0.1))
                tooltip loc.desc
        textbutton "Close":
            action Hide("set_home_dropdown"), With(Dissolve(0.1))
            keysym "mousedown_3", "K_ESCAPE"

screen char_rename(char=None):
    modal True
    zorder 1
    frame:
        if isinstance(char, Player):
            background Frame("content/gfx/frame/post_battle.png", 500, 400)
            xysize(500, 400)
        elif char.status != "slave":
            background Frame("content/gfx/frame/post_battle.png", 500, 300)
            xysize(500, 300)
        else:
            background Frame("content/gfx/frame/post_battle.png", 500, 500)
            xysize(500, 500)
        align (.5, .5)
        vbox:
            style_prefix "wood"
            at fade_in_out()
            align (.5, .5)
            spacing 10
            if isinstance(char, Player) or char.status == "slave":
                text "Name:" size 21 color goldenrod outlines [(2, "#3a3a3a", 0, 0)]
                button:
                    xysize (340, 60)
                    xalign 1.0
                    yalign .5
                    text "[char.name]" size 16 color goldenrod
                    action Return(["rename", "name"])
                    padding (10, 10)
            if not(isinstance(char, Player)): # it's weird to give a nickname to yourself. should be handled by ingame events
                text "Nickname:" size 21 color goldenrod outlines [(2, "#3a3a3a", 0, 0)]
                button:
                    xysize (340, 60)
                    xalign 1.0
                    yalign .5
                    if char.nickname != char.name:
                        text "[char.nickname]" size 16 color goldenrod
                    else:
                        text "None" size 16 color goldenrod
                    action Return(["rename", "nick"])
                    padding (10, 10)
            if isinstance(char, Player) or char.status == "slave":
                text "Full Name:" size 21 color goldenrod outlines [(2, "#3a3a3a", 0, 0)]
                button:
                    xysize (340, 60)
                    xalign 1.0
                    yalign .5
                    text "[char.fullname]" size 16 color goldenrod
                    action Return(["rename", "full"])
                    padding (10, 10)

            null height 20
            button:
                xysize (100, 50)
                xalign .5
                yalign .5
                text "Back" size 16 color goldenrod
                action Hide("char_rename"), With(dissolve)
                keysym "mousedown_3", "K_ESCAPE"
                padding (10, 10)

screen character_pick_screen(): # screen to select someone from the MC team
    frame:
        align (.5, .5)
        xsize 450
        ysize 310
        padding(2, 2)
        background Frame("content/gfx/frame/frame_dec_1.png")
        label "Select a character" align (.5, .08) text_color "#DAA520" text_size 18
        hbox:
            spacing 45
            align (.5, .4)
            for l in hero.team:
                $ char_profile_img = l.show('portrait', resize=(101, 101), cache=True)
                $ img = "content/gfx/frame/ink_box.png"
                vbox:
                    spacing 1
                    xsize 102
                    imagebutton:
                        xalign .5
                        background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                        idle (char_profile_img)
                        hover (im.MatrixColor(char_profile_img, im.matrix.brightness(.15)))
                        action Return(l)
                        xysize (102, 102)
                    bar:
                        xalign .5
                        right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                        left_bar im.Scale("content/gfx/interface/bars/hp2.png", 102, 14)
                        value l.health
                        range l.get_max("health")
                        thumb None
                        left_gutter 0
                        right_gutter 0
                        xysize (102, 14)
                    bar:
                        xalign .5
                        right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                        left_bar im.Scale("content/gfx/interface/bars/mp2.png", 102, 14)
                        value l.mp
                        range l.get_max("mp")
                        thumb None
                        left_gutter 0
                        right_gutter 0
                        xysize (102, 14)
                    bar:
                        xalign .5
                        right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                        left_bar im.Scale("content/gfx/interface/bars/vitality2.png", 102, 14)
                        value l.vitality
                        range l.get_max("vitality")
                        thumb None
                        left_gutter 0
                        right_gutter 0
                        xysize (102, 14)
                    frame:
                        xalign .5
                        xsize 102
                        ysize 30
                        padding(2, 2)
                        background Frame("content/gfx/frame/gm_frame.png")
                        $ name = l.name[:8]
                        label "[name]" align (.5, .5) text_color "#DAA520" text_size 16

        vbox:
            style_group "wood"
            align (.5, .9)
            button:
                xysize (102, 40)
                yalign .5
                action Return(False)
                text "Cancel" size 15 color goldenrod
                keysym "mousedown_3", "K_ESCAPE"

screen finances(obj, mode="logical"):
    modal True
    zorder 1

    default fin_mode = mode
    default focused = obj

    add Transform("content/gfx/images/bg_gradient2.webp", alpha=.3)
    frame:
        at slide(so1=(0, 700), t1=.7, so2=(0, 0), t2=.3, eo2=(0, -config.screen_height))
        background Frame(Transform("content/gfx/frame/frame_gp.webp", alpha=.9), 10, 10)
        style_prefix "proper_stats"
        xysize 1000, 600
        padding 20, 20
        align .5, .5

        $ days, all_income_data, all_expense_data = focused.fin.get_data_for_fin_screen(fin_mode)

        # Days:
        default fin_day = days[-1] if days else None
        # Special check, took some time to track down:
        # Problem here is that we can CTD when switching from Private to Performance...
        # Kind of a hack but it's difficult to do this differently without recoding the screen.
        if fin_day in days:
            pass
        elif days:
            $ fin_day = days[-1]
        else:
            $ fin_day = None

        if fin_day not in all_income_data:
            text "There are no Finances to display for {}!".format(focused.name) align .5, .5
        else:
            hbox:
                style_prefix "basic"
                for d in days:
                    if d == store.day:
                        $ temp = "Today"
                    elif d == -1:
                        pass
                    elif isinstance(d, int):
                        $ temp = "Day " + str(d)
                    else:
                        $ temp = d # All variant...
                    textbutton temp action SetScreenVariable("fin_day", d)

            vbox:
                ypos 40
                text "Income:" size 40 color goldenrod
                viewport:
                    xysize (398, 350)
                    draggable True
                    mousewheel True
                    child_size 398, 1000
                    add Transform(Solid(grey), alpha=.3)
                    vbox:
                        ypos 2
                        for reason, value in sorted(all_income_data[fin_day].items(), key=itemgetter(1), reverse=True):
                            frame:
                                xoffset 4
                                xysize (390, 27)
                                xpadding 7
                                text reason color "#79CDCD"
                                text str(value) xalign 1.0 style_suffix "value_text" color goldenrod

                        null height 10
                        frame:
                            xoffset 4
                            xysize (390, 27)
                            xpadding 7
                            text "Total" color "#79CDCD"
                            $ total_income = sum(all_income_data[fin_day].values())
                            text str(total_income) xalign 1.0 style_suffix "value_text" color lawngreen

            vbox:
                ypos 40 xalign 1.0
                text "Expenses:" size 40 color goldenrod
                viewport:
                    xysize (398, 350)
                    child_size 398, 1000
                    draggable True
                    mousewheel True
                    add Transform(Solid(grey), alpha=.3)
                    vbox:
                        ypos 2
                        for reason, value in sorted(all_expense_data[fin_day].items(), key=itemgetter(1), reverse=True):
                            frame:
                                xoffset 4
                                xysize (390, 27)
                                xpadding 7
                                text reason color "#79CDCD"
                                text str(value) xalign 1.0 style_suffix "value_text" color goldenrod

                        null height 10
                        frame:
                            xoffset 4
                            xysize (390, 27)
                            xpadding 7
                            text "Total" color "#79CDCD"
                            $ total_expenses = sum(all_expense_data[fin_day].values())
                            text str(total_expenses) xalign 1.0 style_suffix "value_text" color red

            frame:
                align .5, .9
                xysize 400, 50
                xpadding 7
                background Frame("content/gfx/frame/rank_frame.png", 3, 3)
                text "Total" size 35 color goldenrod
                $ total = total_income - total_expenses
                $ temp = red if total < 0 else lawngreen
                text str(total) xalign 1.0 style_suffix "value_text" color temp size 35

        # Debt
        if focused.fin.income_tax_debt or focused.fin.property_tax_debt:
            $ total_debt = focused.fin.income_tax_debt + focused.fin.property_tax_debt
            frame:
                background Frame(Transform("content/gfx/frame/MC_bg2.png", alpha=.9), 10, 10)
                style_prefix "proper_stats"
                align 1.0, 1.0
                padding 5, 10
                has vbox
                frame:
                    xysize (200, 20)
                    xpadding 7
                    text "Income Tax Debt:" size 15
                    text "[focused.fin.income_tax_debt]" style_suffix "value_text" xalign 1.0 color red yoffset -1
                frame:
                    xysize (200, 20)
                    xpadding 7
                    text "Property Tax Debt:" size 15
                    text "[focused.fin.property_tax_debt]" style_suffix "value_text" xalign 1.0 color red yoffset -1
                null height 3
                frame:
                    xysize (200, 20)
                    xpadding 7
                    text "Total:" size 15
                    text "[total_debt]" style_suffix "value_text" xalign 1.0 color red yoffset -1

        hbox:
            style_prefix "basic"
            align .5, 1.0
            button:
                minimum (100, 30)
                action Hide('finances'), With(dissolve)
                text "OK"
                keysym ("K_RETURN", "K_ESCAPE", "mousedown_3")
            if isinstance(focused, Char):
                button:
                    minimum (100, 30)
                    if fin_mode == "logical":
                        sensitive focused.allowed_to_view_personal_finances()
                        action SetScreenVariable('fin_mode', "main")
                        text "Personal"
                    elif fin_mode == "main":
                        action SetScreenVariable('fin_mode', "logical")
                        text "Performance"

    if isinstance(focused, Char):
        key "mousedown_4" action SetScreenVariableC("focused", Function(change_char_in_profile, dir="next"))
        key "mousedown_5" action SetScreenVariableC("focused", Function(change_char_in_profile, dir="prev"))

screen race_and_elements(align=(.5, .99), char=None):
    hbox:
        align align
        spacing 20
        # Race:
        frame:
            xysize (100, 100)
            $ trait = char.race
            background Frame(Transform("content/gfx/frame/frame_it1.png", alpha=.6, size=(100, 100)), 10, 10)
            $ img = ProportionalScale(trait.icon, 95, 95)
            button:
                align (.5, .5)
                xysize (95, 95)
                background img
                action Show("show_trait_info", trait=trait.id, place="race_trait")
                hover_background im.MatrixColor(img, im.matrix.brightness(.10))
                tooltip "Race:\n   {}".format(char.full_race)

        # Elements icon:
        $ els = [Transform(e.icon, size=(90, 90)) for e in char.elements]
        $ els_a = [Transform(im.MatrixColor(e.icon, im.matrix.brightness(.10)), size=(90, 90)) for e in char.elements]
        frame:
            xysize (100, 100)
            background Frame(Transform("content/gfx/frame/frame_it1.png", alpha=.6, size=(100, 100)), 10, 10)
            add ProportionalScale("content/gfx/interface/images/elements/hover.png", 98, 98) align (.5, .5)
            $ x = 0
            $ els = [Transform(i, crop=(90/len(els)*els.index(i), 0, 90/len(els), 90), subpixel=True, xpos=(x + 90/len(els)*els.index(i))) for i in els]
            $ els_a = [Transform(i, crop=(90/len(els_a)*els_a.index(i), 0, 90/len(els_a), 90), subpixel=True, xpos=(x + 90/len(els_a)*els_a.index(i))) for i in els_a]
            $ f = Fixed(*els, xysize=(90, 90))
            $ f_a = Fixed(*els_a, xysize=(90, 90))
            if len(char.elements) > 1:
                $ ele = ""
                for e in char.elements:
                    $ ele += e.id + ", "
                $ ele = ele[:-2]
            else:
                $ ele = char.elements[0].id
            button:
                xysize 90, 90
                align .5, .5 offset -1, -1
                action Show("show_trait_info", trait=char, elemental_mode=True, place="ele_trait")
                background f
                hover_background f_a
                tooltip "Elements:\n   {}".format(ele)

screen show_trait_info(trait=None, place="girl_trait", elemental_mode=False):
    default pos = renpy.get_mouse_pos()
    python:
        x, y = pos
        if x > config.screen_width/2:
            x -= 20
            xval = 1.0
        else:
            x += 20
            xval = .0
        temp = config.screen_height/3
        if y < temp:
            yval = .0
        elif y > config.screen_height-temp:
            yval = 1.0
        else:
            yval = .5

    if not elemental_mode:
        $ trait_info = traits[trait]
        fixed:
            pos x, y
            anchor xval, yval
            fit_first True
            frame:
                background Frame("content/gfx/frame/p_frame52.webp", 10, 10)
                padding 10, 10
                has vbox style_prefix "proper_stats" spacing 1

                if any([trait_info.min, trait_info.max, trait_info.mod_stats, trait_info.effects,
                        trait_info.mod_skills, trait_info.mod_ap, hasattr(trait_info, "evasion_bonus")]):
                    if trait_info.max:
                        label (u"Max:") text_size 20 text_color goldenrod text_bold True xalign .45
                        for stat, value in trait_info.max.iteritems():
                            frame:
                                xysize 170, 20
                                if value < 0:
                                    text stat.title() size 15 color red align .0, .5 outlines [(1, "#000000", 0, 0)]
                                    label str(value) text_size 15 text_color red align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                                else:
                                    text stat.title() size 15 color lime align .0, .5 outlines [(1, "#000000", 0, 0)]
                                    label "+" + str(value) text_size 15 text_color lime align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                    if trait_info.min:
                        label (u"Min:") text_size 20 text_color goldenrod text_bold True xalign .45
                        for stat, value in trait_info.min.iteritems():
                            frame:
                                xysize 170, 20
                                if value < 0:
                                    text stat.title() size 15 color red align .0, .5 outlines [(1, "#000000", 0, 0)]
                                    label str(value) text_size 15 text_color red align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                                else:
                                    text stat.title() size 15 color lime align .0, .5 outlines [(1, "#000000", 0, 0)]
                                    label "+" + str(value) text_size 15 text_color lime align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                    if trait_info.mod_stats:
                        label (u"Bonus:") text_size 20 text_color goldenrod text_bold True xalign .45
                        for i in trait_info.mod_stats:
                            frame:
                                xysize 170, 20
                                if str(i) not in ["disposition", "upkeep"]:
                                    if (trait_info.mod_stats[i])[0] < 0:
                                        text (str(i).title() + ": " + str((trait_info.mod_stats[i])[0]) + " every " + str((trait_info.mod_stats[i])[1]) + " lvl") align .5, .5 size 15 color red text_align .5 outlines [(1, "#000000", 0, 0)]
                                    else:
                                        text (str(i).title() + ": +" + str((trait_info.mod_stats[i])[0]) + " every " + str((trait_info.mod_stats[i])[1]) + " lvl") align .5, .5 size 15 color lime text_align .5 outlines [(1, "#000000", 0, 0)]
                                else:
                                    if str(i) == "disposition":
                                        if (trait_info.mod_stats[i])[0] < 0:
                                            text (str(i).title() + ": " + str((trait_info.mod_stats[i])[0])) align .5, .5 size 15 color red text_align .5 outlines [(1, "#000000", 0, 0)]
                                        else:
                                            text (str(i).title() + ": +" + str((trait_info.mod_stats[i])[0])) align .5, .5 size 15 color lime text_align .5 outlines [(1, "#000000", 0, 0)]
                                    else:
                                        if (trait_info.mod_stats[i])[0] < 0:
                                            text (str(i).title() + ": " + str((trait_info.mod_stats[i])[0])) align .5, .5 size 15 color lime text_align .5 outlines [(1, "#000000", 0, 0)]
                                        else:
                                            text (str(i).title() + ": +" + str((trait_info.mod_stats[i])[0])) align .5, .5 size 15 color red text_align .5 outlines [(1, "#000000", 0, 0)]
                    if trait_info.effects:
                        label (u"Effects:") text_size 20 text_color goldenrod text_bold True xalign .45
                        for i in trait_info.effects:
                            frame:
                                xysize 170, 20
                                text (str(i).title()) size 15 color yellow align .5, .5 text_align .5 outlines [(1, "#000000", 0, 0)]

                    if trait_info.mod_skills:
                        label (u"Skills:") text_size 20 text_color goldenrod text_bold True xalign .45
                        for skill, data in trait_info.mod_skills.iteritems():
                            frame:
                                xysize 170, 20
                                text str(skill).title() size 15 color yellowgreen align .0, .5 outlines [(1, "#000000", 0, 0)]

                                $ img_path = "content/gfx/interface/icons/skills_icons/"
                                default PS = ProportionalScale
                                button:
                                    style "default"
                                    xysize 20, 18
                                    action NullAction()
                                    align .99, .5
                                    tooltip "***Icon represents skills changes. Green means bonus, red means penalty. Left one is action counter, right one is training counter, top one is resulting value."
                                    if data[0] > 0:
                                        add PS(img_path + "left_green.png", 20, 20)
                                    elif data[0] < 0:
                                        add PS(img_path + "left_red.png", 20, 20)
                                    if data[1] > 0:
                                        add PS(img_path + "right_green.png", 20, 20)
                                    elif data[1] < 0:
                                        add PS(img_path + "right_red.png", 20, 20)
                                    if data[2] > 0:
                                        add PS(img_path + "top_green.png", 20, 20)
                                    elif data[2] < 0:
                                        add PS(img_path + "top_red.png", 20, 20)
                    if trait_info.mod_ap or hasattr(trait_info, "evasion_bonus") or hasattr(trait_info, "delivery_multiplier"):
                        label (u"Other:") text_size 20 text_color goldenrod text_bold True xalign .45
                        if trait_info.mod_ap:
                            frame:
                                xysize 170, 20
                                $ output = "AP"
                                if trait_info.mod_ap > 0:
                                    $ output += " +" + str(trait_info.mod_ap)
                                else:
                                    $ output += str(trait_info.mod_ap)
                                text (output) align .5, .5 size 15 color yellowgreen text_align .5 outlines [(1, "#000000", 0, 0)]

                        if hasattr(trait_info, "evasion_bonus"):
                            frame:
                                xysize 170, 20
                                if trait_info.evasion_bonus[1] < 0:
                                    text ("Evasion -") size 15 color yellowgreen align .5, .5 text_align .5 outlines [(1, "#000000", 0, 0)]
                                elif trait_info.evasion_bonus[1] > 0:
                                    text ("Evasion +") size 15 color yellowgreen align .5, .5 text_align .5 outlines [(1, "#000000", 0, 0)]
                        if hasattr(trait_info, "delivery_multiplier"):
                            for i in trait_info.delivery_multiplier:
                                frame:
                                    xysize 170, 20
                                    $ output = str(i).title() + " damage "
                                    if trait_info.delivery_multiplier.get(str(i)) > 0:
                                        $ output += "+"
                                    else:
                                        $ output += "-"
                                    text (output) align .5, .5 size 15 color yellowgreen text_align .5 outlines [(1, "#000000", 0, 0)]
                else:
                    label ("-no direct effects-") text_size 15 text_color goldenrod text_bold True xalign .45 text_outlines [(1, "#000000", 0, 0)]

            imagebutton:
                align .99, .01
                xysize 22, 22
                idle pscale("content/gfx/interface/buttons/close4.png", 22, 22)
                hover pscale("content/gfx/interface/buttons/close4_h.png", 22, 22)
                action Hide("show_trait_info"), With(dissolve)
                keysym "mousedown_3"
    else:
        $ traits = elements_calculator(trait)
        fixed:
            pos x, y
            anchor xval, yval
            fit_first True
            frame:
                background Frame("content/gfx/frame/p_frame52.webp", 10, 10)
                padding 10, 5
                has vbox style_prefix "proper_stats" spacing 1
                if not traits:
                    label ("-elements neutralized each other-") text_size 14 text_color goldenrod text_bold True xalign .45
                else:
                    hbox:
                        frame:
                            xysize 80, 20
                            text "element" size 15 color goldenrod align .0, .5 outlines [(1, "#000000", 0, 0)]
                        frame:
                            xysize 60, 20
                            text "damage" size 15 color goldenrod align .5, .5 outlines [(1, "#000000", 0, 0)]
                        frame:
                            xysize 60, 20
                            text "defence" size 15 color goldenrod align .5, .5 outlines [(1, "#000000", 0, 0)]
                    for i in traits:
                        hbox:
                            frame:
                                xysize 80, 20
                                text i size 15 color goldenrod align .0, .5 outlines [(1, "#000000", 0, 0)]
                            frame:
                                xysize 60, 20
                                text traits[i]["attack"] size 15 color traits[i]["attack_color"] align 1.0, .5 outlines [(1, "#000000", 0, 0)]
                            if "abs" in traits[i].keys():
                                frame:
                                    xysize 60, 20
                                    button:
                                        align 1.0, .5
                                        margin 0, 0 padding 0, 0
                                        background Null()
                                        action NullAction()
                                        tooltip "***The character will absorb the damage from this type of attack!"
                                        text traits[i]["abs"] size 13 color lime outlines [(1, "#000000", 0, 0)]
                            elif "resist" in traits[i].keys():
                                frame:
                                    xysize 60, 20
                                    button:
                                        align 1.0, .5
                                        margin 0, 0 padding 0, 0
                                        background Null()
                                        text "RES" size 13 color lime
                                        action NullAction()
                                        tooltip "***The character is immune to this element!"
                            else:
                                frame:
                                    xysize 60, 20
                                    text traits[i]["defence"] size 15 color traits[i]["defence_color"] align 1.0, .5 outlines [(1, "#000000", 0, 0)]

            imagebutton:
                align .99, .01
                xysize 22, 22
                idle pscale("content/gfx/interface/buttons/close4.png", 22, 22)
                hover pscale("content/gfx/interface/buttons/close4_h.png", 22, 22)
                action Hide("show_trait_info"), With(dissolve)
                keysym "mousedown_3"
