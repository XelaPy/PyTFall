label girls_list:

    scene bg gallery
    # Check if we're the screen was loaded or not:
    if not renpy.get_screen("girlslist"):
        show screen girlslist(source=GuiGirlsList(), page=girlslist_last_page_viewed)
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
                renpy.hide_screen("girlslist")
                char = result[1]
                jump('char_profile')
            elif result[0] == "paging":
                gs = renpy.get_screen("girlslist").scope["_kwargs"]["source"]
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

    hide screen girlslist
    jump mainscreen

screen girlslist(source=None, page=0, total_pages=1):
    
    key "mousedown_3" action Return(['control', 'return'])
    
    frame:
        background Frame("content/gfx/frame/framegp2.png", 10, 10)
        pos (5, 46)
        xysize (1010, 670)
        $ girls = source.get_sorted()
        if girls:
            python:
                girl_list = list()
                girl_list.append([girl for ind, girl in enumerate(girls) if ind % 2 == 0])
                girl_list.append([girl for ind, girl in enumerate(girls) if ind % 2 == 1])
                page_lenght = 5
                total_pages = max(int(math.ceil(len(girl_list[0]) / float(page_lenght))), int(math.ceil(len(girl_list[1]) / float(page_lenght))))
                gs = renpy.get_screen("girlslist").scope["_kwargs"]
                gs["total_pages"] = total_pages
                
                # Per Dark's request, we remember the page:
                if page < 0:
                    gs["page"] = 0
                if page > total_pages:
                    gs["page"] = total_pages
                page = gs["page"]
                store.girlslist_last_page_viewed = page
                girl_list[0] = girl_list[0][page*page_lenght:page*page_lenght+page_lenght]
                girl_list[1] = girl_list[1][page*page_lenght:page*page_lenght+page_lenght]
                
            # Keybinds:
            key "mousedown_4" action If(gs["page"] + 1 < gs["total_pages"], true=Show("girlslist", source=gs["source"], page=gs["page"] + 1, total_pages=gs["total_pages"]), false=NullAction())
            key "mousedown_5" action If(gs["page"] > 0, true=Show("girlslist", source=gs["source"], page=gs["page"] - 1, total_pages=gs["total_pages"]), false=NullAction())
                
            hbox:
                style_group "content"
                spacing 14
                pos (17, 15)
                for gl in girl_list:
                    vbox:
                        spacing 14
                        for girl in gl:
                            $ char_profile_img = girl.show('portrait', resize=(98, 98), cache=True)
                            $ img = "content/gfx/frame/ink_box.png"
                            button:
                                idle_background Frame(Transform(img, alpha=0.4), 10 ,10)
                                hover_background Frame(Transform(img, alpha=0.9), 10 ,10)
                                xysize (470, 115)
                                action Return(['choice', girl])
                                
                                # Girl Image:
                                frame:
                                    align (0, 0.5)
                                    background Frame("content/gfx/frame/MC_bg3.png", 10 ,10)
                                    xysize(100, 100)
                                    add char_profile_img align (0.5, 0.5) alpha 0.96
                                   
                                # Texts/Status:
                                frame:
                                    xpos 120
                                    xysize (335, 110)
                                    background Frame (Transform("content/gfx/frame/P_frame2.png", alpha=0.6), 10 ,10)
                                    label "[girl.name]":
                                        text_size 18
                                        xpos 10
                                        yalign 0.06
                                        if girl.__class__ == Char:
                                            text_color pink
                                        else:
                                            text_color ivory
                                        
                                    vbox:
                                        align (0.96, 0.035)
                                        spacing 5
                                        if girl.status == "slave":
                                            add ProportionalScale("content/gfx/interface/icons/slave.png", 50, 50)
                                        else:
                                            add ProportionalScale("content/gfx/interface/icons/free.png", 50, 50)
                                        text "AP: [girl.AP]" size 17 color ivory
                                    
                                    vbox:
                                        yalign 0.98
                                        xpos 10
                                        # Prof-Classes
                                        python:
                                            if len(girl.traits.basetraits) == 1:
                                                classes = list(girl.traits.basetraits)[0].id
                                            elif len(girl.traits.basetraits) == 2:
                                                classes = list(girl.traits.basetraits)
                                                classes.sort()
                                                classes = ", ".join([str(c) for c in classes])
                                            else:
                                                raise Exception("Character without prof basetraits detected! line: 211, girlslists screen")
                                        text "Classes: [classes]" color ivory size 18
                                        
                                        null height 2
                                        # $ loc = girl.location if isinstance(girl.location, basestring) else girl.location.name
                                        if girl not in pytfall.ra:
                                            button:
                                                style_group "ddlist"
                                                action Return(["dropdown", "loc", girl])
                                                if girl.status == "slave":
                                                    alternate Return(["dropdown", "home", girl])
                                                text "{image=content/gfx/interface/icons/move15.png}Location: [girl.location]"
                                            button:
                                                style_group "ddlist"
                                                action Return(["dropdown", "action", girl])
                                                text "{image=content/gfx/interface/icons/move15.png}Action: [girl.action]"
                                        else:
                                            text "{size=15}Location: Unknown"
                                            text "{size=15}Action: Hiding"
                                        
    frame:
        background Frame(Transform("content/gfx/frame/p_frame2.png", alpha=0.55), 10 ,10)
        xpadding 10
        ypadding 10
        pos (1005, 47)
        xysize(270, 668)
        side "c r":
            viewport id "filterlist":
                draggable True
                mousewheel True
                has vbox
                null height 5
                label "{=della_respira}{size=35}{b}Filters:" xalign 0.5
                button:
                    xalign 0.5
                    style_group "basic"
                    action source.clear
                    text "Reset Filters"
                null height 10
                for block_name, filters in source.display_filters:
                    label ("{=della_respira}{b}[block_name]:") xalign 0
                    for item_1, item_2 in izip_longest(fillvalue=None, *[iter(filters)]*2):
                        hbox:
                            style_group "basic"
                            for filter_item in [item_1, item_2]:
                                if filter_item:
                                    $ filter_name, filter_group, filter_key = filter_item
                                    $ focus = source.get_focus(filter_group, filter_key)
                                    button:
                                        action [SelectedIf(focus), Function(source.add_filter, filter_group, filter_key)]
                                        text "[filter_name]" size 16
            vbar value YScrollValue("filterlist")
            
    use top_stripe(True)
    
