init:
    default status_filters = list()
    default location_filters = list()
    default action_filters = list()
    default occ_filters = list()
    python:
        def sorting_for_chars_list():
            return hero.chars
        
label chars_list:
    scene bg gallery
    # Check if we're the screen was loaded or not:
    if not renpy.get_screen("chars_list"):
        $ char_lists_filters = CharsSortingForGui(sorting_for_chars_list)
        $ char_lists_filters.filter()
        # We create the filters only from those that our chars actually have... not need for gibberish:
        $ status_filters = list(set([c.status for c in hero.chars]))
        $ location_filters = list(set([c.location for c in hero.chars]))
        $ action_filters = list(set([c.action for c in hero.chars]))
        # $ class_filters = set()
        # for c in hero.chars:
        
        show screen chars_list(source=char_lists_filters, page=chars_list_last_page_viewed, total_pages=1)
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
            elif result[0] == "paging":
                gs = renpy.get_screen("chars_list").scope["_kwargs"]["source"]
                if result[1] == "next":
                    if gs.page + 1 > gs.total_pages - 1:
                        gs.page = 0
                    else:
                        gs.page += 1
                elif result[1] == "previous":
                    if gs.page - 1 < 0:
                        gs.page = gs.total_pages - 1
                    else:
                        gs.page -= 1

    hide screen chars_list
    jump mainscreen

screen chars_list(source=None, page=0, total_pages=1):
    frame:
        background Frame("content/gfx/frame/framegp2.png", 10, 10)
        pos (5, 46)
        xysize (1010, 670)
        if source.sorted:
            python:
                chars_list = list()
                chars_list.append([c for ind, c in enumerate(source.sorted) if ind % 2 == 0])
                chars_list.append([c for ind, c in enumerate(source.sorted) if ind % 2 == 1])
                page_lenght = 5
                total_pages = max(int(math.ceil(len(chars_list[0]) / float(page_lenght))), int(math.ceil(len(chars_list[1]) / float(page_lenght))))
                gs = renpy.get_screen("chars_list").scope["_kwargs"]
                gs["total_pages"] = total_pages
                
                # Per Dark's request, we remember the page:
                if page < 0:
                    gs["page"] = 0
                if page > total_pages:
                    gs["page"] = total_pages
                page = gs["page"]
                store.chars_list_last_page_viewed = page
                chars_list[0] = chars_list[0][page*page_lenght:page*page_lenght+page_lenght]
                chars_list[1] = chars_list[1][page*page_lenght:page*page_lenght+page_lenght]
                
            # Keybinds:
            key "mousedown_4" action If(gs["page"] + 1 < gs["total_pages"], true=Show("chars_list", source=gs["source"], page=gs["page"] + 1, total_pages=gs["total_pages"]), false=NullAction())
            key "mousedown_5" action If(gs["page"] > 0, true=Show("chars_list", source=gs["source"], page=gs["page"] - 1, total_pages=gs["total_pages"]), false=NullAction())
                
            hbox:
                style_group "content"
                spacing 14
                pos (17, 15)
                for l in chars_list:
                    vbox:
                        spacing 14
                        for c in l:
                            $ char_profile_img = c.show('portrait', resize=(98, 98), cache=True)
                            $ img = "content/gfx/frame/ink_box.png"
                            button:
                                idle_background Frame(Transform(img, alpha=0.4), 10 ,10)
                                hover_background Frame(Transform(img, alpha=0.9), 10 ,10)
                                xysize (470, 115)
                                action Return(['choice', c])
                                
                                # Girl Image:
                                frame:
                                    background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                                    padding 0, 0
                                    align 0, .5
                                    xysize(100, 100)
                                    add char_profile_img align .5, .5 alpha 0.96
                                   
                                # Texts/Status:
                                frame:
                                    xpos 120
                                    xysize (335, 110)
                                    background Frame (Transform("content/gfx/frame/P_frame2.png", alpha=0.6), 10 ,10)
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
        xysize (270, 668)
        viewport:
            draggable True
            mousewheel True
            has vbox xsize 253
            null height 5
            label "Filters:" xalign 0.5 text_size 35 text_color white
            button:
                xalign 0.5
                style_group "basic"
                action source.clear
                text "Reset"
            null height 10
            label "Status:" text_color white
            hbox:
                style_group "basic"
                for f in status_filters:
                    textbutton "[f]":
                        action ModFilterSet(source, "status_filters", f)
            label "Locations:" text_color white
            hbox:
                style_group "basic"
                for f in location_filters:
                    textbutton "[f]":
                        action ModFilterSet(source, "location_filters", f)
            label "Actions:" text_color white
            hbox:
                style_group "basic"
                box_wrap True
                for f in action_filters:
                    textbutton "[f]":
                        action ModFilterSet(source, "action_filters", f)
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
            
    use top_stripe(True)
    
