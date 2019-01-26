init:
    default rebuild_chars_listings = None

    default status_filters = set()
    default location_filters = set()
    default action_filters = set()
    default class_filters = set()
    python:
        def sorting_for_chars_list():
            return [c for c in hero.chars if c.is_available]

        def clear_selected_filters():
            global selected_filters
            selected_filters = set()

label chars_list:
    scene bg gallery
    # Check if we're the screen was loaded or not:
    if rebuild_chars_listings:
        python:
            char_lists_filters = CharsSortingForGui(sorting_for_chars_list)
            char_lists_filters.sorting_order = "level"
            char_lists_filters.filter()

            status_filters = set([c.status for c in hero.chars])
            # location_filters = set([c.location for c in hero.chars])
            home_filters = set([c.home for c in hero.chars])
            work_filters = set([c.workplace for c in hero.chars])
            action_filters = set([c.action for c in hero.chars])
            class_filters = set([bt for c in hero.chars for bt in c.traits.basetraits])
            selected_filters = set()
            the_chosen = set()

            rebuild_chars_listings = False
            char = None

    show screen chars_list(source=char_lists_filters)
    with dissolve

    while 1:

        $ result = ui.interact()

        if result[0] == 'control':
            if result[1] == 'return':
                $ the_chosen = set()
                hide screen chars_list
                jump mainscreen
        elif result[0] == "dropdown":
            if result[1] == "workplace":
                $ renpy.show_screen("set_workplace_dropdown", result[2], pos=renpy.get_mouse_pos())
            elif result[1] == "home":
                $ renpy.show_screen("set_home_dropdown", result[2], pos=renpy.get_mouse_pos())
            elif result[1] == "action":
                $ renpy.show_screen("set_action_dropdown", result[2], pos=renpy.get_mouse_pos())
        elif result[0] == 'choice':
            hide screen chars_list
            $ char = result[1]
            jump char_profile

    hide screen chars_list
    jump mainscreen

screen chars_list(source=None):
    if not source.sorted:
        text "You don't have any workers.":
            size 40
            color ivory
            align .5, .2
            style "TisaOTM"

    key "mousedown_3" action Return(['control', 'return']) # keep in sync with button - alternate

    # Normalize pages.
    default page_size = 10
    default page = chars_list_last_page_viewed

    $ max_page = len(source.sorted)/page_size-1
    if len(source.sorted) % page_size:
        $ max_page += 1
    if page > max_page:
        $ page = max_page

    python:
        listed_chars = []
        for start in xrange(0, len(source.sorted), page_size):
             listed_chars.append(source.sorted[start:start+page_size])

    # Chars:
    if listed_chars:
        $ charz_list = listed_chars[page]
        hbox:
            style_group "content"
            spacing 14
            pos 27, 94
            xsize 970
            box_wrap True
            for c in charz_list:
                $ char_profile_img = c.show('portrait', resize=(98, 98), cache=True)
                $ img = "content/gfx/frame/ink_box.png"
                $ available = c.is_available and c in hero.chars
                button:
                    ymargin 0
                    idle_background Frame(Transform(img, alpha=.4), 10 ,10)
                    hover_background Frame(Transform(img, alpha=.9), 10 ,10)
                    xysize (470, 115)
                    alternate Return(['control', 'return']) # keep in sync with mousedown_3
                    if available:
                        action Return(['choice', c])
                        tooltip "Show {}'s Profile!".format(c.name)
                    else:
                        action NullAction()

                    # Image:
                    frame:
                        background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                        padding 0, 0
                        align 0, .5
                        xysize 100, 100
                        add char_profile_img align .5, .5 alpha .96

                    # Texts/Status:
                    frame:
                        xpos 120
                        xysize (335, 110)
                        background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=.6), 10, 10)
                        label "[c.name]":
                            text_size 18
                            xpos 10
                            yalign .06
                            if c.__class__ == Char:
                                text_color pink
                            else:
                                text_color ivory

                        vbox:
                            yalign .98
                            xpos 10
                            # Prof-Classes
                            python:
                                classes = list(c.traits.basetraits)
                                if len(classes) == 1:
                                    classes = classes[0].id
                                else:
                                    classes.sort()
                                    classes = ", ".join(t.id for t in classes)
                            text "Classes: [classes]" color ivory size 18

                            if available:
                                null height 2
                                $ circle_green = im.Scale("content/gfx/interface/icons/move15.png", 16, 16)
                                $ icon_flag = c.get_flag("last_chars_list_geet_icon", "work")
                                hbox:
                                    if icon_flag == "home":
                                        imagebutton:
                                            yalign 0.5
                                            xoffset -2
                                            idle circle_green
                                            hover im.MatrixColor(circle_green, im.matrix.brightness(.15))
                                            action [Function(c.set_flag, "last_chars_list_geet_icon", "work")]
                                            tooltip "Switch to set Work!"
                                        button:
                                            style_group "ddlist"
                                            if c.status == "slave":
                                                action Return(["dropdown", "home", c])
                                                tooltip "Choose a place for %s to live at!" % c.nickname
                                            else: # Can't set home for free cs, they decide it on their own.
                                                action NullAction()
                                                tooltip "%s is free and decides on where to live at!" % c.nickname
                                            text "{size=18}Home:{/size} [c.home]":
                                                if len(str(c.home)) > 18:
                                                    size 15
                                                    yalign 0.5
                                                else:
                                                    size 18
                                    else: # if icon_flag == "work":
                                        imagebutton:
                                            yalign 0.5
                                            xoffset -2
                                            idle circle_green
                                            hover im.MatrixColor(circle_green, im.matrix.brightness(.15))
                                            action [Function(c.set_flag, "last_chars_list_geet_icon", "home")]
                                            tooltip "Switch to set Home!"
                                        button:
                                            style_group "ddlist"
                                            action Return(["dropdown", "workplace", c])
                                            tooltip "Choose a place for %s to work at!" % c.nickname
                                            text "{size=18}Work:{/size} [c.workplace]":
                                                if len(str(c.workplace)) > 18:
                                                    size 15
                                                    yalign 0.5
                                                else:
                                                    size 18
                                hbox:
                                    imagebutton:
                                        yalign 0.5
                                        xoffset -2
                                        idle circle_green
                                        action NullAction()
                                    button:
                                        style_group "ddlist"
                                        action Return(["dropdown", "action", c])
                                        tooltip "Choose a task for %s to do!" % c.nickname
                                        text "{size=18}Action:{/size} [c.action]":
                                            if c.action is not None and len(str(c.action)) > 18:
                                                size 15
                                                yalign 0.5
                                            else:
                                                size 18

                        vbox:
                            align (.96, .035)
                            python:
                                if available:
                                    if c.status == "slave":
                                        status_img = "content/gfx/interface/icons/slave.png"
                                    else:
                                        status_img = "content/gfx/interface/icons/free.png"
                                elif c.action == "Exploring":
                                    status_img = "content/gfx/interface/icons/exploring.png"
                                elif c in pytfall.ra:
                                    status_img = "content/gfx/interface/images/MC/reflexes.png"
                                elif not c.alive:
                                    status_img = "content/gfx/interface/icons/gravestone.png"
                                else:
                                    status_img = "content/gfx/interface/icons/question.png"
                            add ProportionalScale(status_img, 40, 40)

                        vbox:
                            align 1.0, .6 xoffset 5
                            hbox:
                                xsize 60
                                text "AP:" xalign .0 color ivory
                                text "[c.AP]" xalign .1 color ivory
                            hbox:
                                xsize 60
                                text "Tier:" xalign .0 color ivory
                                text "[c.tier]" xalign .1 color ivory

                    # Add to Group Button:
                    if available:
                        button:
                            style_group "basic"
                            xysize (25, 25)
                            align 1.0, 1.0 offset 9, -2
                            action ToggleSetMembership(chars_list_state.the_chosen, c)
                            if c in chars_list_state.the_chosen:
                                add(im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align .5, .5
                            else:
                                add(im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align .5, .5
                            tooltip 'Select the character'

    # Filters:
    frame:
        background Frame(Transform("content/gfx/frame/p_frame2.png", alpha=.55), 10 ,10)
        style_prefix "content"
        xmargin 0
        padding 5, 5
        pos (1005, 47)
        xysize (270, 468)
        vbox:
            xalign .5
            spacing 3
            label "Filters:":
                xalign .5
                text_size 35
                text_color goldenrod
                text_outlines [(1, "#000000", 0, 0)]

            hbox:
                xalign .5
                box_wrap True
                for f, c, t in [('Home', saddlebrown, 'Toggle home filters'),
                                ('Work', brown, 'Toggle workplace filters'),
                                ("Status", green, 'Toggle status filters'),
                                ("Action", darkblue, 'Toggle action filters'),
                                ('Class', purple, 'Toggle class filters')]:
                    button:
                        style_prefix "basic"
                        xpadding 6
                        xsize 100
                        action ToggleSetMembership(selected_filters, f)
                        tooltip t
                        text f color c size 18 outlines [(1, "#3a3a3a", 0, 0)]

                button:
                    style_group "basic"
                    xsize 100
                    action source.clear, clear_selected_filters, renpy.restart_interaction
                    tooltip 'Reset all filters'
                    text "Reset"

            null height 3

            vpgrid:
                style_prefix "basic"
                xysize 256, 289
                xalign .5
                cols 2
                draggable True edgescroll (30, 100)
                if "Status" in selected_filters:
                    for f in status_filters:
                        button:
                            xysize 125, 32
                            action ModFilterSet(source, "status_filters", f)
                            text f.capitalize() color green
                            tooltip 'Toggle the filter'
                if "Home" in selected_filters:
                    for f in home_filters:
                        button:
                            xysize 125, 32
                            action ModFilterSet(source, "home_filters", f)
                            text "[f]" color saddlebrown:
                                if len(str(f)) > 12:
                                    size 10
                                    line_spacing -6
                                else:
                                    layout "nobreak"
                            tooltip 'Toggle the filter'
                if "Work" in selected_filters:
                    for f in work_filters:
                        button:
                            xysize 125, 32
                            action ModFilterSet(source, "work_filters", f)
                            text "[f]" color brown:
                                if len(str(f)) > 12:
                                    size 10
                                    line_spacing -6
                                else:
                                    layout "nobreak"
                            tooltip 'Toggle the filter'
                if "Action" in selected_filters:
                    for f in action_filters:
                        button:
                            xysize 125, 32
                            action ModFilterSet(source, "action_filters", f)
                            $ t = str(f)
                            if t.lower().endswith(" job"):
                                $ t = t[:-4]
                            text "[t]" color darkblue:
                                if len(str(t)) > 12:
                                    size 10
                                    line_spacing -6
                                else:
                                    layout "nobreak"
                            tooltip 'Toggle the filter'
                if "Class" in selected_filters:
                    for f in class_filters:
                        button:
                            xysize 125, 32
                            action ModFilterSet(source, "class_filters", f)
                            text "[f]" color purple
                            tooltip 'Toggle the filter'

    # Mass (de)selection Buttons ====================================>
    vbox:
        pos 1015, 518
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.9), 10, 10)
            xysize (250, 50)
            style_prefix "basic"
            has hbox spacing 5 align .5, .5
            python:
                try:
                    chars_on_page = set(charz_list)
                except:
                    chars_on_page = set()
            button: # select all on current page
                xysize (66, 40)
                # if the_chosen.issuperset(chars_on_page):
                #     action SetVariable("the_chosen", the_chosen.difference(chars_on_page))
                # else:
                #     action SetVariable("the_chosen", the_chosen.union(chars_on_page))
                action SetVariable("the_chosen", chars_on_page)
                sensitive chars_on_page and (chars_on_page != the_chosen)
                text "These"
                tooltip 'Select all currently visible characters'
            button: # every of currently filtered, also in next tabs
                xysize (66, 40)
                action If(set(source.sorted).difference(the_chosen), [SetVariable("the_chosen", set(source.sorted))])
                sensitive listed_chars
                text "All"
                tooltip 'Select all characters'
            button: # deselect all
                xysize (66, 40)
                action SetVariable("the_chosen", set())
                sensitive the_chosen
                text "None"
                tooltip "Clear Selection"

        # Mass action Buttons ====================================>
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.9), 10, 10)
            align .5, .5
            style_prefix "basic"
            xysize (250, 145)
            has vbox align .5, .5 spacing 3
            button:
                xysize (150, 40)
                action If(len(the_chosen), [SetVariable("char", PytGroup(the_chosen)), Show("char_control")])
                text "Controls"
                selected False
                tooltip 'Set desired behavior for group'
            button:
                xysize (150, 40)
                action If(len(the_chosen), [Hide("chars_list"), With(dissolve), SetVariable("came_to_equip_from", "chars_list"), Jump('char_equip')])
                text "Equipment"
                selected False
                tooltip "Manage Group's Equipment"
            button:
                xysize (150, 40)
                action If(len(the_chosen), [Hide("chars_list"), With(dissolve),
                          Jump('school_training')])
                text "Training"
                selected False
                tooltip "Send the entire group to School!"

    use top_stripe(True)

    # Two buttons that used to be in top-stripe:
    hbox:
        style_group "basic"
        pos 300, 5
        spacing 3
        textbutton "<--":
            sensitive page > 0
            action SetScreenVariable("page", page-1)
            tooltip 'Previous page'
            keysym "mousedown_4"

        $ temp = page + 1
        textbutton "[temp]":
            xsize 40
            action NullAction()
        textbutton "-->":
            sensitive page < max_page
            action SetScreenVariable("page", page+1)
            tooltip 'Next page'
            keysym "mousedown_5"

    $ store.chars_list_last_page_viewed = page # At Darks Request!
    # Normalize stored page, should we done 'on hide' but we can't trust those atm.
    if chars_list_last_page_viewed > max_page:
        $ chars_list_last_page_viewed = max_page
