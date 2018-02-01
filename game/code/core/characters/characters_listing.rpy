init:
    default status_filters = set()
    default location_filters = set()
    default action_filters = set()
    default class_filters = set()
    python:
        def sorting_for_chars_list():
            return [c for c in hero.chars if c.is_available]

label chars_list:
    scene bg gallery
    # Check if we're the screen was loaded or not:
    if not renpy.get_screen("chars_list"):
        python:
            char_lists_filters = CharsSortingForGui(sorting_for_chars_list)
            char_lists_filters.filter()
            # We create the filters only from those that our chars actually have... not need for gibberish:
            status_filters = set([c.status for c in hero.chars])
            location_filters = set([c.location for c in hero.chars])
            action_filters = set([c.action for c in hero.chars])
            class_filters = set([bt for c in hero.chars for bt in c.traits.basetraits])
            selected_filters = set()
            the_chosen = set()

        show screen chars_list(source=char_lists_filters)
    with dissolve

    python:
        while 1:

            result = ui.interact()

            if result[0] == 'control':
                if result[1] == 'return':
                    break
            elif result[0] == "dropdown":
                if result[1] == "workplace":
                    renpy.show_screen("set_workplace_dropdown", result[2], pos=renpy.get_mouse_pos())
                elif result[1] == "home":
                    renpy.show_screen("set_home_dropdown", result[2], pos=renpy.get_mouse_pos())
                elif result[1] == "action":
                    renpy.show_screen("set_action_dropdown", result[2], pos=renpy.get_mouse_pos())
            elif result[0] == 'choice':
                renpy.hide_screen("chars_list")
                char = result[1]
                jump('char_profile')

    hide screen chars_list
    jump mainscreen

screen chars_list(source=None):

    if len(source.sorted) == 0:
        label "You don't have any workers" text_size 40 text_color ivory align .34, .2

    key "mousedown_3" action Return(['control', 'return'])

    default page_size = 10
    default max_page = len(source.sorted)/page_size
    if len(source.sorted)%page_size == 0:
        $ max_page = len(source.sorted)/page_size - 1
    else:
        $ max_page = len(source.sorted)/page_size
    default page = min(chars_list_last_page_viewed, max_page)
    if page > max_page:
        $ page = max_page
    if chars_list_last_page_viewed > max_page:
        $ chars_list_last_page_viewed = max_page

    default tt = Tooltip("")

    python:
        charz_lists = []
        for start in xrange(0, len(source.sorted), page_size):
             charz_lists.append(source.sorted[start:start+page_size])

    fixed:
        pos 5, 70
        xysize 1010, 670

        if len(source.sorted)%page_size == 0 and max_page !=0:
            $ max_page = len(source.sorted)/page_size - 1
        else:
            $ max_page = len(source.sorted)/page_size
        if page < 0:
            $ page = 0

        if charz_lists:
            $ charz_list = charz_lists[page]

            hbox:
                style_group "content"
                spacing 14
                pos (17, 15)
                xsize 970
                box_wrap True
                for c in charz_list:
                    $ char_profile_img = c.show('portrait', resize=(98, 98), cache=True)
                    $ img = "content/gfx/frame/ink_box.png"
                    button:
                        ymargin 0
                        idle_background Frame(Transform(img, alpha=.4), 10 ,10)
                        hover_background Frame(Transform(img, alpha=.9), 10 ,10)
                        xysize (470, 115)
                        action Return(['choice', c])
                        hovered tt.Action('Show character profile')

                        # Girl Image:
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
                            background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=0.6), 10, 10)
                            label "[c.name]":
                                text_size 18
                                xpos 10
                                yalign 0.06
                                if c.__class__ == Char:
                                    text_color pink
                                else:
                                    text_color ivory

                            vbox:
                                align (0.96, 0.035)
                                spacing 5
                                if c.status == "slave":
                                    add ProportionalScale("content/gfx/interface/icons/slave.png", 50, 50)
                                else:
                                    add ProportionalScale("content/gfx/interface/icons/free.png", 50, 50)
                                text "AP: [c.AP]" size 17 color ivory
                                button:
                                    style_group "basic"
                                    xysize (25, 25)
                                    xpos 30
                                    if c.status == "slave":
                                        ypos 11
                                    action ToggleSetMembership(the_chosen, c)
                                    if c in the_chosen:
                                        add(im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (0.5, 0.5)
                                    else:
                                        add(im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (0.5, 0.5)
                                    hovered tt.Action('Select the character')

                            vbox:
                                yalign 0.98
                                xpos 10
                                # Prof-Classes
                                python:
                                    if len(c.traits.basetraits) == 1:
                                        classes = list(c.traits.basetraits)[0].id
                                    elif len(c.traits.basetraits) == 2:
                                        classes = list(c.traits.basetraits)
                                        classes.sort()
                                        classes = ", ".join([str(t) for t in classes])
                                    else:
                                        raise Exception("Character without prof basetraits detected! line: 211, chars_lists screen")
                                text "Classes: [classes]" color ivory size 18

                                null height 2
                                if c not in pytfall.ra:
                                    if not c.flag("last_chars_list_geet_icon"):
                                        $ c.set_flag("last_chars_list_geet_icon", "work")
                                    if c.status == "free" and c.flag("last_chars_list_geet_icon") != "work":
                                        $ c.set_flag("last_chars_list_geet_icon", "work")

                                    if c.flag("last_chars_list_geet_icon") == "home":
                                        button:
                                            style_group "ddlist"
                                            if c.status == "slave":
                                                action Return(["dropdown", "home", c])
                                                hovered tt.Action("Choose a place for %s to live at!" % c.nickname)
                                            else: # Can't set home for free cs, they decide it on their own.
                                                action NullAction()
                                                hovered tt.Action("%s is free and decides on where to live at!" % c.nickname)
                                            alternate [Function(c.set_flag, "last_chars_list_geet_icon", "work"),
                                                       Return(["dropdown", "workplace", c])]
                                            text "{image=button_circle_green}Home: [c.home]":
                                                if len(str(c.home)) > 18:
                                                    size 15
                                                else:
                                                    size 18
                                    elif c.flag("last_chars_list_geet_icon") == "work":
                                        button:
                                            style_group "ddlist"
                                            action Return(["dropdown", "workplace", c])
                                            if c.status == "slave":
                                                alternate [Function(c.set_flag, "last_chars_list_geet_icon", "home"),
                                                           Return(["dropdown", "home", c])]
                                            hovered tt.Action("Choose a place for %s to work at!" % c.nickname)
                                            text "{image=button_circle_green}Work: [c.workplace]":
                                                if len(str(c.workplace)) > 18:
                                                    size 15
                                                else:
                                                    size 18
                                    button:
                                        style_group "ddlist"
                                        action Return(["dropdown", "action", c])
                                        hovered tt.Action("Choose a task for %s to do!" % c.nickname)
                                        text "{image=button_circle_green}Action: [c.action]":
                                            if c.action is not None and len(str(c.action)) > 18:
                                                size 15
                                            else:
                                                size 18
                                else:
                                    text "{size=15}Location: Unknown"
                                    text "{size=15}Action: Hiding"

    frame:
        background Frame(Transform("content/gfx/frame/p_frame2.png", alpha=0.55), 10 ,10)
        style_prefix "content"
        xmargin 0
        left_padding 10
        ypadding 10
        pos (1005, 47)
        xysize (270, 468)
        vbox:
            spacing 3
            viewport:
                xsize 250
                draggable True
                mousewheel True
                has vbox xsize 253
                null height 5
                label "Filters:" xalign 0.5 text_size 35 text_color goldenrod text_outlines [(1, "#000000", 0, 0)]
                hbox:
                    box_wrap True
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Site')
                        text "Site" color brown size 18 outlines [(1, "#3a3a3a", 0, 0)]
                        xpadding 6
                        hovered tt.Action('Toggle location filters')
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Status')
                        text "Status" color green size 18 outlines [(1, "#3a3a3a", 0, 0)]
                        xpadding 6
                        hovered tt.Action('Toggle status filters')
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Action')
                        text "Action" color darkblue size 18 outlines [(1, "#3a3a3a", 0, 0)]
                        xpadding 6
                        hovered tt.Action('Toggle action filters')
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Class')
                        text "Class" color purple size 18 outlines [(1, "#3a3a3a", 0, 0)]
                        xpadding 6
                        hovered tt.Action('Toggle class filters')
                button:
                    xalign 0.5
                    yalign 1.0
                    style_group "basic"
                    action source.clear, renpy.restart_interaction
                    text "Reset"
                    hovered tt.Action('Reset all filters')

                null height 20
                hbox:
                    box_wrap True
                    style_group "basic"
                    if "Status" in selected_filters:
                        for f in status_filters:
                            button:
                                xsize 125
                                action ModFilterSet(source, "status_filters", f)
                                text f.capitalize() color green
                                hovered tt.Action('Toggle the filter')
                    if "Site" in selected_filters:
                        for f in location_filters:
                            button:
                                xsize 125
                                action ModFilterSet(source, "location_filters", f)
                                text "[f]" color brown:
                                    if len(str(f)) > 12:
                                        size 10
                                hovered tt.Action('Toggle the filter')
                    if "Action" in selected_filters:
                        for f in action_filters:
                            button:
                                xsize 125
                                action ModFilterSet(source, "action_filters", f)
                                $ t = str(f)
                                if t.endswith(" job") or t.endswith(" Job"):
                                    $ t = t[:-4]
                                text "[t]" color darkblue
                                hovered tt.Action('Toggle the filter')
                    if "Class" in selected_filters:
                        for f in class_filters:
                            button:
                                xsize 125
                                action ModFilterSet(source, "class_filters", f)
                                text "[f]" color purple
                                hovered tt.Action('Toggle the filter')
                # for block_name, filters in source.display_filters:
                    # label ("{=della_respira}{b}[block_name]:") xalign 0
                    # for item_1, item_2 in izip_longest(fillvalue=None, *[iter(filters)]*2):
                        # hbox:
                            # style_group "basic"
                            # for filter_item in [item_1, item_2]:
                                # if filter_item:
                                    # $ filter_name, filter_group, filter_key = filter_item
                                    # $ focus = source.get_focus(filter_group, filter_key)
                                    # button:
                                        # action [SelectedIf(focus), Function(source.add_filter, filter_group, filter_key)]
                                        # text "[filter_name]" size 16
            # Mass (de)selection Buttons ====================================>
            null height 3
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
                xalign 0.5
                yalign 0.5
                # ypos 5
                xysize (250, 50)
                has hbox style_group "basic" align .5, .5 spacing 5
                hbox:
                    spacing 3
                    $ chars_on_page = set(charz_list) if hero.chars else set()
                    button: # select all on current listing, deselects them if all are selected
                        xysize (66, 40)
                        if the_chosen.issuperset(chars_on_page):
                            action SetVariable("the_chosen", the_chosen.difference(chars_on_page))
                        else:
                            action SetVariable("the_chosen", the_chosen.union(chars_on_page))
                        text "These"
                        hovered tt.Action('Select all currently visible characters')
                    button: # every of currently filtered, also in next tabs
                        xysize (66, 40)
                        action If(set(source.sorted).difference(the_chosen), [SetVariable("the_chosen", set(source.sorted))])
                        text "All"
                        hovered tt.Action('Select all characters')
                    button: # deselect all
                        xysize (66, 40)
                        action If(len(the_chosen), [SetVariable("the_chosen", set())])
                        text "None"
                        hovered tt.Action('Unselect everyone')
            # Mass action Buttons ====================================>
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
                xalign 0.5
                yalign 0.5
                xysize (250, 145)
                has vbox style_group "basic" align .5, .5 spacing 3
                vbox:
                    spacing 3
                    button:
                        xysize (150, 40)
                        action If(len(the_chosen), [Show("girl_control")])
                        text "Girl Control"
                        hovered tt.Action('Set desired behavior for group')
                    button:
                        xysize (150, 40)
                        action If(len(the_chosen), [Hide("chars_list"), With(dissolve), SetVariable("eqtarget", None), Jump('char_equip')])
                        text "Equipment"
                        hovered tt.Action('Manage group equipment')
                    button:
                        xysize (150, 40)
                        action If(len(the_chosen), [Hide("chars_list"), With(dissolve), Jump('girl_training')])
                        text "Training"
                        hovered tt.Action('Manage group training')

    # Keybinds:
    key "mousedown_4" action If(page < max_page, true=SetScreenVariable("page", page+1), false=NullAction())
    key "mousedown_5" action If(page > 0, true=SetScreenVariable("page", page-1), false=NullAction())

    $ store.chars_list_last_page_viewed = page # At Darks Request!

    frame:
        background Frame("content/gfx/frame/window_frame1.png", 10, 10)
        align(0.09, 1.0)
        xysize (950, 65)
        text (u"{=content_text}{size=24}{color=[ivory]}%s" % tt.value) align(0.5, 0.5)

    use top_stripe(True)

    # Two buttons that used to be in top-stripe:
    hbox:
        style_group "basic"
        pos 300, 5
        spacing 3
        textbutton "<--":
            sensitive page > 0
            action SetScreenVariable("page", page-1)
            hovered tt.Action('Previous page')
        $ temp = page+1
        textbutton "[temp]":
            action NullAction()
        # if len(source.sorted)%page_size == 0 and max_page !=0:
            # $ max_page = len(source.sorted)/page_size - 1
        # else:
            # $ max_page = len(source.sorted)/page_size

        textbutton "-->":
            sensitive page < max_page
            action SetScreenVariable("page", page+1)
            hovered tt.Action('Next page')


style chars_debug_text:
    size 10

screen chars_debug():
    zorder 100
    modal True

    default all_chars = [chars.values(), pytfall.arena.arena_fighters.values()]
    default all_chars_str = ["chars", "arena"]
    default shown_chars = [all_chars[0]]

    style_prefix "chars_debug"

    add black
    vbox:
        hbox:
            spacing 1
            ysize 20
            fixed:
                xysize 80, 20
                text "Name" color red bold 1
            fixed:
                xysize 80, 20
                text "Origin" color crimson bold 1
            fixed:
                xysize 50, 20
                text "Status" color green bold 1
            fixed:
                xysize 80, 20
                text "Location" color blue bold 1
            fixed:
                xysize 80, 20
                text "Home" color blue bold 1
            fixed:
                xysize 80, 20
                text "Work" color blue bold 1
            fixed:
                xysize 80, 20
                text "Action" color orange bold 1

        viewport:
            xysize 1280, 700
            child_size 1280, 10000
            draggable 1 mousewheel 1
            has vbox
            for char in list(sorted(chain.from_iterable(shown_chars), key=attrgetter("name"))):
                hbox:
                    spacing 1
                    fixed:
                        xysize 80, 20
                        text "[char.name]" color red
                    fixed:
                        xysize 80, 20
                        text "[char.origin]" color crimson
                    fixed:
                        xysize 50, 20
                        text "[char.status]" color green
                    fixed:
                        xysize 80, 20
                        text "[char.location]" color blue:
                            if len(str(char.location)) > 12:
                                size 6
                    fixed:
                        xysize 80, 20
                        text "[char.home]" color blue:
                            if len(str(char.home)) > 12:
                                size 6
                    fixed:
                        xysize 80, 20
                        text "[char.workplace]" color blue:
                            if len(str(char.workplace)) > 12:
                                size 6
                    fixed:
                        xysize 80, 20
                        text "[char.action]" color orange


    hbox:
        align 1.0, .0
        for index, container in enumerate(all_chars):
            $ name = all_chars_str[index]
            if container in shown_chars:
                textbutton "[name]":
                    text_color green
                    action Function(shown_chars.remove, container)
            else:
                textbutton "[name]":
                    text_color red
                    action Function(shown_chars.append, container)
        textbutton "X":
            action Hide("chars_debug")
