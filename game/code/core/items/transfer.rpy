init python:
    def items_transfer(it_members):
        store._skipping = False
        renpy.show_screen("items_transfer", it_members)
        while 1:
            result = ui.interact()
            if isinstance(result, (list, tuple)):
                if result[0] == "control":
                    break
                elif result[0] == "transfer":
                    source, target, items, amount = result[1:]
                    for item in items:
                        for i in xrange(amount):
                            if not transfer_items(source, target, item):
                                break
        renpy.hide_screen("items_transfer")
        store._skipping = True

    def it_on_show(it_members):
        for c in it_members:
            c.inventory.set_page_size(14)

    def it_item_click(selection, source, item):
        selected_items = selection[1]
        selected_source = selection[0]
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]:
            #if selected_source == source:
                if item in selected_items:
                    selected_items.remove(item)
                else:
                    selected_items.add(item)
        elif pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_RSHIFT]:
            if selected_source == source:
                if item in selected_items:
                    selected_items.remove(item)
                else:
                    front_idx = tail_idx = item_idx = -1
                    for idx, it in enumerate(source.inventory.page_content):
                        if it == item:
                            item_idx = idx
                        elif it in selected_items:
                            if item_idx == -1:
                                front_idx = idx
                            else:
                                tail_idx = idx
                                break
                    if item_idx == -1:
                        selected_items.add(item)
                    else:
                        if front_idx != -1:
                            selected_items.update([it for it in source.inventory.page_content][front_idx:item_idx+1])
                        elif tail_idx != -1:
                            selected_items.update([it for it in source.inventory.page_content][item_idx:tail_idx+1])
                        else:
                            selected_items.add(item)
            else:
                if item in selected_items:
                    selected_items.remove(item)
                else:
                    selected_items.add(item)
        else:
            if source is not None:
                selection[0] = source
            selection[1] = set([item])

screen items_transfer(it_members):
    on "show":
        action Function(it_on_show, it_members)

    default lc = it_members[0]
    default rc = it_members[1]
    default selection = [None, set()]
    default transfer_amount = 1
    default slot_filter = it_members[0].inventory.slot_filter

    add "bg gallery"

    frame:
        style_group "dropdown_gm"
        xalign .5
        ypos 41
        xysize 250, 157
        text "Transfer Items between Characters!" align .5, .5 style "content_text" color ivory

    # Left/Right employment info:
    frame:
        background Frame("content/gfx/frame/p_frame5.png", 10, 10)
        style_group "dropdown_gm"
        xysize (1280, 45)
        if isinstance(lc, Char):
            text "[lc.traits.base_to_string] ---- [lc.action]" align (.09, .5) style "content_text" color ivory size 20
        if isinstance(rc, Char):
            text "[rc.traits.base_to_string] ---- [rc.action]" align (.92, .5) style "content_text" color ivory size 20

        use exit_button(size=(35, 35), align=(1.0, .6))

    # Members + Items
    for scr_var, fc, xalign in [("lc", lc, .0), ("rc", rc, 1.0)]: # Focused characters...
        vbox:
            ypos 41
            spacing -4
            xalign xalign
            frame:
                background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                padding 5, 5
                has viewport draggable True mousewheel True xysize 331, 300 child_size 330, 10000
                hbox:
                    spacing 1
                    box_wrap True
                    for c in it_members:
                        $ img = c.show("portrait", resize=(70, 70), cache=True)
                        vbox:
                            spacing 1
                            frame:
                                xpos 4
                                background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                                xysize (162, 120)
                                imagebutton:
                                    align .5, .93
                                    style "basic_choice2_button"
                                    idle img
                                    hover img
                                    selected_idle Transform(img, alpha=1.05)
                                    action SetScreenVariable(scr_var, c), SelectedIf(c == fc), SensitiveIf(c != (rc if fc == lc else lc))
                                frame:
                                    xalign .5
                                    background Frame("content/gfx/frame/Mc_bg3.png", 5, 5)
                                    xysize(150, 22)
                                    ypadding 0
                                    text "{color=[gold]}[c.name]" style "interactions_text" selected_color red size (14 if len(c.name) > 10 else 20) outlines [(1, "#3a3a3a", 0, 0)] align .5, .5

            frame:
                background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                style_group "dropdown_gm2"
                xysize 341, 375
                has vbox
                for item, amount in [(item, fc.inventory[item]) for item in fc.inventory.page_content]:
                    button:
                        xysize (330, 26)
                        action SensitiveIf(amount), Function(it_item_click, selection, fc, item)
                        selected fc == selection[0] and item in selection[1]
                        text "[item.id]" align .0, .5 style "dropdown_gm2_button_text"
                        text "[amount]" align 1.0, .7 style "dropdown_gm2_button_value_text"

        # RC and LC Portraits:
    for fc, pos, xanchor in [(lc, (360, 43), 0), (rc, (920, 43), 1.0)]:
        frame:
            pos pos
            xanchor xanchor
            background Frame("content/gfx/frame/Mc_bg3.png", 10, 10)
            padding 1, 1
            add fc.show("portrait", resize=(150, 150), cache=True) align .5, .5

    frame:
        ypos 643
        xalign .5
        xysize (600, 80)
        background Frame("content/gfx/frame/p_frame5.png", 10, 10)
        hbox:
            yalign  .5
            spacing 210
            use paging(xysize=(190, 50), ref=lc.inventory, use_filter=False)
            use paging(xysize=(190, 50), ref=rc.inventory, use_filter=False)

    # Transfer Buttons:
    vbox:
        xalign .5
        ypos 653
        style_group "dropdown_gm"
        frame:
            xalign .5
            xysize 200, 30
            $ img = ProportionalScale('content/gfx/interface/buttons/left.png', 25, 25, align=(.5, .5))
            button:
                xysize (40, 30)
                style "default"
                align (0, .5)
                idle_background img
                hover_background im.MatrixColor(img, im.matrix.brightness(.15), align=(.5, .5))
                insensitive_background im.Sepia(img, align=(.5, .5))
                action Return(["transfer", rc, lc, selection[1], transfer_amount])
                sensitive selection[1] and lc and rc
                if len(selection[1]) == 1:
                    tooltip "Transfer %s from %s to %s!" % (iter(selection[1]).next().id, rc.nickname, lc.nickname)
                else:
                    tooltip "Transfer the selected items from %s to %s!" % (rc.nickname, lc.nickname)

            $ img = ProportionalScale('content/gfx/interface/buttons/right.png', 25, 25, align=(.5, .5))
            button:
                xysize 40, 30
                style "default"
                align 1.0, .5
                idle_background img
                hover_background im.MatrixColor(img, im.matrix.brightness(.15), align=(.5, .5))
                insensitive_background im.Sepia(img, align=(.5, .5))
                action Return(["transfer", lc, rc, selection[1], transfer_amount])
                sensitive selection[1] and lc and rc
                if len(selection[1]) == 1:
                    tooltip "Transfer %s from %s to %s!" % (iter(selection[1]).next().id, lc.nickname, rc.nickname)
                else:
                    tooltip "Transfer the selected items from %s to %s!" % (lc.nickname, rc.nickname)

        null height 1
        frame:
            xalign .5
            xysize 200, 30
            $ img = ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 25, 25, align=(.5, .5))
            button:
                xysize (40, 30)
                style "default"
                align 0, .5
                idle_background img
                hover_background im.MatrixColor(img, im.matrix.brightness(.15), align=(.5, .5))
                insensitive_background im.Sepia(img, align=(.5, .5))
                action SetScreenVariable("transfer_amount", 1 if transfer_amount - 5 < 1 else transfer_amount - 5)
                tooltip 'Decrease transfer amount by 5!'

            hbox:
                yalign .5
                spacing 5
                text 'Amount:' yalign .5 xpos 46 size 20 color ivory style "garamond"
                text '[transfer_amount]' yalign .5 xpos 60 size 18 color ivory style "proper_stats_value_text" yoffset -1

            $ img = ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 25, 25, align=(.5, .5))
            button:
                xysize 40, 30
                style "default"
                align 1.0, .5
                idle_background img
                hover_background im.MatrixColor(img, im.matrix.brightness(.15), align=(.5, .5))
                insensitive_background im.Sepia(img, align=(.5, .5))
                action SetScreenVariable("transfer_amount", transfer_amount + 5)
                tooltip 'Increase transfer amount by 5!'

    # Filters Buttons:
    frame:
        style_group "dropdown_gm"
        background Frame("content/gfx/frame/Mc_bg3.png", 10, 10)
        ypos 200
        padding 3, 3
        xalign .5
        has hbox spacing 1

        for filter in list(sorted(set(rc.inventory.filters + lc.inventory.filters))):
            $ img = ProportionalScale("content/gfx/interface/buttons/filters/%s.png" % filter, 40, 40)
            $ img_hover = ProportionalScale("content/gfx/interface/buttons/filters/%s hover.png" % filter, 40, 40)
            $ img_selected = ProportionalScale("content/gfx/interface/buttons/filters/%s selected.png" % filter, 40, 40)
            imagebutton:
                idle img
                hover im.MatrixColor(img_hover, im.matrix.brightness(.10))
                selected_idle img_selected
                selected_hover im.MatrixColor(img_selected, im.matrix.brightness(.10))
                action SetScreenVariable("slot_filter", filter), Function(rc.inventory.apply_filter, filter), Function(lc.inventory.apply_filter, filter)
                selected filter == slot_filter
                focus_mask True

    # Selected Item(s):
    if selection[1]:
        frame:
            ypos 247
            xalign .5
            background Frame("content/gfx/frame/frame_dec_1.png", 10, 10)
            padding 30, 34
            if len(selection[1]) == 1:
                use itemstats(item=iter(selection[1]).next(), size=(540, 330))
            else:
                vpgrid:
                    cols 6
                    draggable True
                    mousewheel True
                    xysize(540, 330)
                    #yminimum 330
                    spacing 12
                    #scrollbars 'vertical'

                    $ fc = selection[0]
                    for item in selection[1]:
                        frame:
                            background Frame("content/gfx/frame/frame_it2.png", 5, 5)
                            xysize (80, 80)
                            imagebutton:
                                idle pscale(item.icon, 60, 60)
                                hover pscale(im.MatrixColor(item.icon, im.matrix.brightness(.10)), 60, 60)
                                action Function(it_item_click, selection, None, item)
                                tooltip "%s" % item.id
                            $ amount = fc.inventory[item] if (fc and fc.inventory) else 0
                            text "[amount]" align 1.0, 1.0 style "dropdown_gm2_button_value_text"
