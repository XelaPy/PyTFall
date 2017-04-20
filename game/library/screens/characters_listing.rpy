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
                if result[1] == "loc":
                    renpy.show_screen("set_location_dropdown", result[2], pos=renpy.get_mouse_pos())
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

    default page_size = 10
    default max_page = len(source.sorted)/page_size
    default page = min(chars_list_last_page_viewed, max_page)

    # Keybinds:
    key "mousedown_4" action If(page < max_page, true=SetScreenVariable("page", page+1), false=NullAction())
    key "mousedown_5" action If(page > 0, true=SetScreenVariable("page", page-1), false=NullAction())

    python:
        charz_lists = []
        for start in xrange(0, len(source.sorted), page_size):
             charz_lists.append(source.sorted[start:start+page_size])

    fixed:
        pos 5, 70
        xysize 1010, 670

        $ charz_list = charz_lists[page]
        if charz_list:
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
                                    button:
                                        style_group "ddlist"
                                        action Return(["dropdown", "loc", c])
                                        if c.status == "slave":
                                            alternate Return(["dropdown", "home", c])
                                        text "{image=content/gfx/interface/icons/move15.png}Location: [c.location]"
                                    button:
                                        style_group "ddlist"
                                        action Return(["dropdown", "action", c])
                                        text "{image=content/gfx/interface/icons/move15.png}Action: [c.action]"
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
                label "Filters:" xalign 0.5 text_size 35 text_color white
                hbox:
                    box_wrap True
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Status')
                        text "Status" hover_color red
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Site')
                        text "Site" hover_color brown
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Action')
                        text "Action" hover_color blue
                    button:
                        xalign 0.5
                        style_group "basic"
                        action ToggleSetMembership(selected_filters, 'Class')
                        text "Class" hover_color purple

                null height 20
                hbox:
                    box_wrap True
                    style_group "basic"
                    if "Status" in selected_filters:
                        for f in status_filters:
                            button:
                                action ModFilterSet(source, "status_filters", f)
                                text "[f]" hover_color red
                    if "Site" in selected_filters:
                        for f in location_filters:
                            button:
                                action ModFilterSet(source, "location_filters", f)
                                text "[f]" hover_color brown
                    if "Action" in selected_filters:
                        for f in action_filters:
                            button:
                                action ModFilterSet(source, "action_filters", f)
                                text "[f]" hover_color blue
                    if "Class" in selected_filters:
                        for f in class_filters:
                            button:
                                action ModFilterSet(source, "class_filters", f)
                                text "[f]" hover_color purple
                null height 20
                button:
                    xalign 0.5
                    yalign 1.0
                    style_group "basic"
                    action source.clear
                    text "Reset"
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
                    button: # every of currently filtered, also in next tabs
                        xysize (66, 40)
                        action If(set(source.sorted).difference(the_chosen), [SetVariable("the_chosen", set(source.sorted))])
                        text "All"
                    button: # deselect all
                        xysize (66, 40)
                        action If(len(the_chosen), [SetVariable("the_chosen", set())])
                        text "None"
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
                    button:
                        xysize (150, 40)
                        action If(len(the_chosen), [Hide("chars_list"), With(dissolve), SetVariable("eqtarget", None), Jump('char_equip')])
                        text "Equipment"
                    button:
                        xysize (150, 40)
                        action If(len(the_chosen), [Hide("chars_list"), With(dissolve), Jump('girl_training')])
                        text "Training"

    use top_stripe(True)

    # Two buttons that used to be in top-stripe:
    hbox:
        style_group "basic"
        pos 300, 5
        spacing 3
        textbutton "<--":
            sensitive page > 0
            action SetScreenVariable("page", page-1)
        textbutton "[page]":
            action NullAction()
        textbutton "-->":
            sensitive page < max_page
            action SetScreenVariable("page", page+1)

    $ store.chars_list_last_page_viewed = page # At Darks Request!
