label items_transfer:
    
    $ renpy.retain_after_load()
    show screen items_transfer
    with fade
    
    python:
        
        while 1:
            
            result = ui.interact()
            
            if result[0] == 'select_left_char':
                pytfall.it.select_left_char(result[1])
                pytfall.it.left_char.inventory.apply_filter(pytfall.it.filter)
            if result[0] == 'select_left_item':
                pytfall.it.select_left_item(result[1])
                if pytfall.it.right_char:
                    pytfall.it.right_char.inventory.apply_filter(pytfall.it.filter)
            if result[0] == 'select_right_char': pytfall.it.select_right_char(result[1])
            if result[0] == 'select_right_item':
                pytfall.it.select_right_item(result[1])
                if pytfall.it.left_char:
                    pytfall.it.left_char.inventory.apply_filter(pytfall.it.filter)
            if result[0] == 'transfer_left': pytfall.it.transfer_item_left()
            if result[0] == 'transfer_right': pytfall.it.transfer_item_right()
            if result[0] == 'set_filter':
                pytfall.it.filter = result[1]
                if pytfall.it.left_char: pytfall.it.left_char.inventory.apply_filter(result[1])
                if pytfall.it.right_char: pytfall.it.right_char.inventory.apply_filter(result[1])
            if result[0] == 'incr_amount':
                if pytfall.it.items_amount == 1:
                    pytfall.it.items_amount = 5
                else:    
                    pytfall.it.items_amount += 5
            if result[0] == 'decr_amount':
                if pytfall.it.items_amount - 5 <= 1:
                    pytfall.it.items_amount = 1
                else:
                    pytfall.it.items_amount -= 5
            elif result[0] == 'left_inv':
                if result[1] == 'first_page': pytfall.it.left_char.inventory.first()
                elif result[1] == 'last_page': pytfall.it.left_char.inventory.last()
                elif result[1] == 'next_page': pytfall.it.left_char.inventory.next()
                elif result[1] == 'prev_page': pytfall.it.left_char.inventory.prev()
                elif result[1] == 'prev_filter': pytfall.it.left_char.inventory.apply_filter('prev')
                elif result[1] == 'next_filter': pytfall.it.left_char.inventory.apply_filter('next') 
                
            elif result[0] == 'right_inv':
                if result[1] == 'first_page': pytfall.it.right_char.inventory.first()
                elif result[1] == 'last_page': pytfall.it.right_char.inventory.last()
                elif result[1] == 'next_page': pytfall.it.right_char.inventory.next()
                elif result[1] == 'prev_page': pytfall.it.right_char.inventory.prev()
                elif result[1] == 'prev_filter': pytfall.it.right_char.inventory.apply_filter('prev')
                elif result[1] == 'next_filter': pytfall.it.right_char.inventory.apply_filter('next') 

            if result[0] == 'control':
                if result[1] == 'return':
                    break
                    
    hide screen items_transfer
    python:
        # Restore inventory page size (We do this for all characters to make sure)
        for i in chars.values():
            i.inventory.set_page_size(15)
        hero.inventory.set_page_size(15)
        last_label = pytfall.it.last_label
        del pytfall.it
        jump(last_label)
    
screen items_transfer():
    
    # Tooltip related ------------------------>
    default tt = Tooltip(u'Transfer Items between characters! ')
    
    add "bg gallery"
    
    frame:
        style_group "dropdown_gm"
        xalign 0.5
        ypos 41
        xysize (188, 180)
        text "[tt.value]" align (0.5, 0.5) style "content_text" color ivory
        
    # Left/Right employment info:
    frame:
        background Frame("content/gfx/frame/p_frame5.png", 10, 10)
        style_group "dropdown_gm"
        xpos -2
        ypos -2
        xysize (1285, 46)
        if hasattr(pytfall, "it") and pytfall.it.populate_character_viewports()[0]:
            if pytfall.it.left_char and isinstance(pytfall.it.left_char, Char):
                text "[pytfall.it.left_char.traits.base_to_string] ---- [pytfall.it.left_char.action]" align (0.09, 0.5) style "content_text" color ivory size 20
        if hasattr(pytfall, "it") and pytfall.it.populate_character_viewports()[0]:
            if pytfall.it.right_char and isinstance(pytfall.it.right_char, Char):
                text "[pytfall.it.right_char.traits.base_to_string] ---- [pytfall.it.right_char.action]" align (0.92, 0.5) style "content_text" color ivory size 20
                
    # Members + Items
    if hasattr(pytfall, "it") and pytfall.it.populate_character_viewports()[0]:
        # Left Members + Items
        vbox:
            pos(-2, 75)
            frame:
                ypos -35
                background Frame("content/gfx/frame/p_frame5.png", 15, 15)
                xysize (550, 310)
                has viewport draggable True mousewheel True xysize 355, 300 child_size 355, 10000 scrollbars "vertical"
                hbox:
                    xpos 5
                    spacing 5
                    box_wrap True
                    xsize 355
                    for lmember in pytfall.it.populate_character_viewports()[1]:
                        $ img = lmember.show("portrait", resize=(70, 70), cache=True)
                        vbox:
                            spacing 5
                            frame:
                                xpos 4
                                background Frame("content/gfx/frame/p_frame5.png", 15, 15)
                                xysize (162, 120)
                                imagebutton:
                                    align (0.5, 0.93)
                                    style "basic_choice2_button"
                                    idle img
                                    hover img
                                    selected_idle Transform(img, alpha=1.05)
                                    action [Return(['select_left_char', lmember]), SelectedIf(lmember == pytfall.it.left_char), SensitiveIf(lmember != pytfall.it.right_char)]
                                frame:
                                    xalign 0.5
                                    background Frame("content/gfx/frame/Mc_bg3.png", 5, 5)
                                    xysize(150, 10)
                                    ypadding 0
                                    if len(lmember.name) > 10: # Gismo: For buildings???
                                        text "{color=[gold]}[lmember.name]" style "interactions_text" selected_color red size 14 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
                                    else:
                                        text "{color=[gold]}[lmember.name]" style "interactions_text" selected_color red size 20 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
                
            frame:
                ypos -40
                background Frame("content/gfx/frame/p_frame5.png", 15, 15)
                style_group "dropdown_gm2"
                xysize (378, 378)
                has vbox
                if pytfall.it.show_left_items_selection():
                    for litem in pytfall.it.get_left_inventory():
                        $ left_vp_items_amount = pytfall.it.left_char.inventory.content[litem.id]
                        button:
                            xysize (330, 28)
                            action [Return(['select_left_item', litem]), SelectedIf(litem == pytfall.it.left_item)]
                            text "[litem.id]" align (0.0, 0.5) style "dropdown_gm2_button_text"
                            text "[left_vp_items_amount]" align (1.0, 0.7) style "dropdown_gm2_button_value_text"
            
        # Right members + Items
        vbox:
            pos (733, 75)
            frame:
                ypos -35
                background Frame("content/gfx/frame/p_frame5.png", 15, 15)
                style_group "dropdown_gm"
                xysize (550, 310)
                has side "c l" ypos -4 xpos 180 maximum (360, 560)
                viewport id "right_members":
                    draggable True
                    mousewheel True
                    xysize 355, 300
                    child_size 355, 10000
                    hbox:
                        spacing 5
                        box_wrap True
                        xsize 355
                        for rmember in pytfall.it.populate_character_viewports()[1]:
                            $ img = rmember.show("portrait", resize=(70, 70), cache=True)
                            vbox:
                                spacing 5
                                frame:
                                    xpos 4
                                    background Frame("content/gfx/frame/p_frame5.png", 15, 15)
                                    xysize(162, 120)
                                    imagebutton:
                                        ypos 27
                                        xalign 0.5
                                        style "basic_choice2_button"
                                        idle img
                                        hover img
                                        selected_idle Transform(img, alpha=1.05)
                                        action [Return(['select_right_char', rmember]), SelectedIf(rmember == pytfall.it.right_char), SensitiveIf(rmember != pytfall.it.left_char)]
                                    frame:
                                        ypos -4
                                        xalign 0.5
                                        background Frame("content/gfx/frame/Mc_bg3.png", 5, 5)
                                        xysize(150, 10)
                                        ypadding 0
                                        if len(rmember.name) > 10: # Gismo: For buildings???
                                            text "{color=[gold]}[rmember.name]" style "interactions_text" selected_color red size 14 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
                                        else:
                                            text "{color=[gold]}[rmember.name]" style "interactions_text" selected_color red size 20 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
                vbar value YScrollValue("right_members")
                
            frame:
                pos (172, -40)
                background Frame("content/gfx/frame/p_frame5.png", 15, 15)
                xysize (378, 378)
                style_group "dropdown_gm2"
                has vbox xoffset 33
                if pytfall.it.show_right_items_selection():
                    for ritem in pytfall.it.get_right_inventory():
                        $ right_vp_items_amount = pytfall.it.right_char.inventory.content[ritem.id]  
                        button:
                            xysize (330, 28)
                            action [Return(['select_right_item', ritem]), SelectedIf(ritem == pytfall.it.right_item)]
                            text "[ritem.id]" align (0.0, 0.5) style "dropdown_gm2_button_text"
                            text "[right_vp_items_amount]" align (1.0, 0.7) style "dropdown_gm2_button_value_text"
                    
                    
        # Paging Left and Right:
        if pytfall.it.left_image_cache:
            vbox:
                pos(380, 50)
                spacing 53
                frame:
                    background Frame("content/gfx/frame/Mc_bg3.png", 10, 10)
                    add ProportionalScale(pytfall.it.left_image_cache, 150, 150) align (0.5, 0.5)
        if pytfall.it.right_image_cache:
            vbox:
                pos(738, 52)
                spacing 53
                frame:
                    background Frame("content/gfx/frame/Mc_bg3.png", 10, 10)
                    add ProportionalScale(pytfall.it.right_image_cache, 150, 150) align (0.5, 0.5)
                    
        frame:
            ypos 643
            xalign 0.5
            xysize (600, 80)
            background Frame("content/gfx/frame/p_frame5.png", 10, 10)
            hbox:
                yalign  0.5
                spacing 210
                if pytfall.it.left_image_cache:
                    use paging(root='left_inv', xysize=(190, 50), ref=pytfall.it.left_char.inventory, use_filter=False)
                if pytfall.it.right_image_cache:
                    use paging(root='right_inv', xysize=(190, 50), ref=pytfall.it.right_char.inventory, use_filter=False)
                
        # Transfer Buttons:
        vbox:
            xalign 0.5
            ypos 653
            style_group "dropdown_gm"
            frame:
                xalign 0.5
                xysize(200, 30)
                $ img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 25, 25, align=(0.5, 0.5))
                button:
                    xysize (40, 30)
                    style "default"
                    align (0, 0.5)
                    idle_background img
                    hover_background im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
                    insensitive_background im.Sepia(img, align=(0.5, 0.5))
                    action [Return(['transfer_left']), SensitiveIf(pytfall.it.show_left_transfer_button())]
                    if pytfall.it.show_left_transfer_button():
                        hovered tt.action("Transfer %s from %s to %s!" % (pytfall.it.right_item.id, pytfall.it.right_char.name, pytfall.it.left_char.name))
                
                hbox:
                    align (0.5, 0.5)
                    spacing 5
                    text(u'{size=-5}Transfer') align (0.5, 0.5)  size 20 color ivory style "garamond"
                    text(u'{size=-5}%s' % plural("Item", pytfall.it.items_amount)) align (0.5, 0.5)  size 20 color ivory style "garamond"
                    
                $ img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 25, 25, align=(0.5, 0.5))
                button:
                    xysize (40, 30)
                    style "default"
                    align (1.0, 0.5)
                    idle_background img
                    hover_background im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
                    insensitive_background im.Sepia(img, align=(0.5, 0.5))
                    action [Return(['transfer_right']), SensitiveIf(pytfall.it.show_right_transfer_button())]
                    if pytfall.it.show_right_transfer_button():
                        hovered tt.action("Transfer %s from %s to %s!" % (pytfall.it.left_item.id, pytfall.it.left_char.name, pytfall.it.right_char.name))
                        
            null height 1
            frame:
                xalign 0.5
                xysize(200, 30)
                $ img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 25, 25, align=(0.5, 0.5))
                button:
                    xysize (40, 30)
                    style "default"
                    align (0, 0.5)
                    idle_background img
                    hover_background im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
                    insensitive_background im.Sepia(img, align=(0.5, 0.5))
                    action Return(['decr_amount'])
                    hovered tt.action('Decrease transfer amount by 5!')
                
                hbox:
                    yalign 0.5
                    spacing 5
                    text (u'{size=-5}Amount:') yalign 0.5 xpos 46 size 20 color ivory style "garamond"
                    text (u'{size=-5}[pytfall.it.items_amount]') yalign 0.5 xpos 60 size 20 color ivory style "proper_stats_value_text"

                $ img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 25, 25, align=(0.5, 0.5))
                button:
                    xysize (40, 30)
                    style "default"
                    align (1.0, 0.5)
                    idle_background img
                    hover_background im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
                    insensitive_background im.Sepia(img, align=(0.5, 0.5))
                    action Return(['incr_amount'])
                    hovered tt.action('Increase transfer amount by 5!')
                    
                
        # Filters Buttons:
        frame:
            style_group "dropdown_gm"
            background Frame("content/gfx/frame/Mc_bg3.png", 10, 10)
            ypos 215
            xalign 0.5
            xysize (400, 65)
            has hbox spacing 2
            
            for filter in hero.inventory.GEQ_FILTERS:
                $ img = ProportionalScale("content/gfx/interface/buttons/filters/%s.png" % filter, 44, 44)
                $ img_hover = ProportionalScale("content/gfx/interface/buttons/filters/%s hover.png" % filter, 44, 44)
                $ img_selected = ProportionalScale("content/gfx/interface/buttons/filters/%s selected.png" % filter, 44, 44)
                imagebutton:
                    idle img
                    hover im.MatrixColor(img_hover, im.matrix.brightness(0.10))
                    selected_idle img_selected
                    selected_hover im.MatrixColor(img_selected, im.matrix.brightness(0.10))
                    action Return(['set_filter', filter]), SelectedIf(filter == pytfall.it.filter)
                    focus_mask True
           
                    
        frame:
            ypos 263
            style_group "content"
            xalign 0.5
            background Frame("content/gfx/frame/frame_dec_1.png", 30, 30)
            xpadding 30
            ypadding 30
            xysize (555, 400)
            use itemstats(item=pytfall.it.item_cache, size=(580, 350))
     
    use exit_button

