label girl_equip:
    python:
        focusitem = False
        selectedslot = None
        item_direction = None
        char.inventory.set_page_size(18)
        # char.inventory.famale_filter = True
        hero.inventory.set_page_size(18)
        # hero.inventory.famale_filter = True
        inv_source = char
    
    scene bg gallery3
    
    # $ renpy.retain_after_load()
    show screen pyt_girl_equip
    
    python:
        
        inv_source.inventory.apply_filter("all")
        
        while 1:
            
            result = ui.interact()
            
            if result[0] == "jump":
                renpy.hide_screen("pyt_girl_equip")
                if result[1] == "item_transfer":
                    renpy.hide_screen("pyt_girl_control")
                    pytfall.it = GuiItemsTransfer("personal_transfer", char=char, last_label=last_label)
                    jump("items_transfer")
                    
            elif result[0] == "equip_for":
                renpy.show_screen("pyt_equip_for", renpy.get_mouse_pos())
                
            elif result[0] == "item":
                    
                if result[1] == 'equip/unequip':
                    if item_direction == 'equip':
                        if focusitem.slot == "quest":
                            renpy.call_screen('pyt_message_screen', "Quest items cannot be equipped!")
                            focusitem = False
                        elif focusitem.unique and item.unque != char.id:
                            renpy.call_screen('pyt_message_screen', "%s cannot be equipped on this character!"  % focusitem.id)
                            focusitem = False
                        elif focusitem.sex == 'male':
                            renpy.call_screen('pyt_message_screen', "%s can only be equiped on Male Characters!" % focusitem.id)
                            focusitem = False
                        elif focusitem.slot == "gift":
                            renpy.call_screen('pyt_message_screen', "Gifts are only used during Girlsmeets!")
                            focusitem = False
                        elif char.status == "slave" and focusitem.slot in ["weapon"] and not focusitem.type.lower().startswith("nw"):
                            renpy.call_screen('pyt_message_screen', "Slaves are forbidden to equip large weapons by law!")
                            focusitem = False
                        else:
                            if inv_source == char:
                                if all([char.status != "slave", char.disposition < 850]) or all([char.status != "slave", (focusitem.badness > 90 or focusitem.eqchance < 10)]):
                                    char.say(choice(["I can manage my own things!", "Get away from my stuff!", "Don't want to..."]))
                                else:
                                    equip_item(focusitem, char)
                                    # char.equip(focusitem)
                            else:
                                if all([char.status != "slave", (focusitem.badness > 90 or focusitem.eqchance < 10)]):
                                    char.say(choice(["No way!", "I do not want this!", "No way in hell!"]))
                                else:
                                    if transfer_items(inv_source, char, focusitem):
                                        equip_item(focusitem, char)
                            
                    elif item_direction == 'unequip':
                        if char.status != "slave" and char.disposition < 850:
                            char.say(choice(["I can manage my own things!", "Get away from my stuff!", "I'll think about it..."]))
                        else:
                            if inv_source == hero and char.status != "slave":
                                if any([(focusitem.slot == "misc" and item.mdestruct), char.given_items.get(focusitem.id, 0) - 1 < 0]):
                                    char.say(choice(["Like hell am I giving away!", "Go get your own!", "Go find your own %s!" % item.id, "Would you like fries with that?",
                                                             "Perhaps you would like me to give you the key to my flat where I keep my money as well?"]))
                                else:
                                    char.unequip(focusitem)
                                    transfer_items(char, hero, focusitem)
                            else: # Slave condition:
                                char.unequip(focusitem)
                                char.inventory.remove(focusitem)
                                inv_source.inventory.append(focusitem)
                            
                    selectedslot = False
                    focusitem = False
                     
                elif result[1] == 'equip':
                    focusitem = result[2]
                    selectedslot = focusitem.slot
                    item_direction = 'equip'
                        
                elif result[1] == 'unequip':
                    selectedslot = result[2].slot
                    if selectedslot:
                        focusitem = result[2]
                        item_direction = 'unequip'
                    
            elif result[0] == 'control':
                if result[1] == 'return':
                    break
                    
    hide screen pyt_girl_equip
    python:
        char.inventory.set_page_size(15)
        hero.inventory.set_page_size(15)
        # char.inventory.female_filter = False
        # hero.inventory.female_filter = False
        if char.location == "After Life":
            renpy.call_screen("pyt_message_screen", "Either your 'awesome' item handling or my 'brilliant' programming have killed %s..." % char.fullname)
            jump("mainscreen")
    if girl_equip:
        $ last_label, girl_equip = girl_equip, None
        jump expression last_label
    else:
        jump girl_profile

screen pyt_equip_for(pos=()):
    zorder 3
    modal True
    
    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()
    
    python:
        x, y = pos
        if x > 1000:
            xval = 1.0
        else:
            xval = 0.0
        if y > 500:
            yval = 1.0
        else:
            yval = 0.0
    frame:
        style_group "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        vbox:
            text "Equip For:" xalign 0 style "della_respira" color ivory
            null height 5
            for t in ["Combat", "Sex", "Service", "Striptease"]:
                if t == "Combat" and char.status == "slave":
                    pass
                else:
                    textbutton "[t]":
                        xminimum 200
                        action [Function(char.equip_for, t), Hide("pyt_equip_for")]
            textbutton "Close":
                action Hide("pyt_equip_for")

screen pyt_girl_equip():
    # Useful keymappings (first time I try this in PyTFall):
    if focusitem:
        key "mousedown_2" action Return(["item", "equip/unequip"])
    else:
        key "mousedown_2" action NullAction()
    key "mousedown_4" action Function(inv_source.inventory.next)
    key "mousedown_5" action Function(inv_source.inventory.prev)
    
    # Equipment slots
    frame:
        pos (0, 40)
        background Frame(Transform("content/gfx/frame/Mc_bg.png", alpha=0.7), 10, 10)
        xysize (520, 680)
        use pyt_eqdoll(active_mode=True, char=char, frame_size=[70, 70], scr_align=(0.5, 0.4), return_value=['item', "unequip"], txt_size=18, fx_size=(450, 600))

    # Middle VBox:
    frame:
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        pos (515, 39)
        xysize (200,282) 
        xpadding 10
        ypadding 10
        style_group "content"
        
        vbox:
            align (0.5, 0.5)
            spacing 2
            # Equip_for button + Paging + Portrait:
            frame:
                background Frame ("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                align (0.5, 0.5)
                add inv_source.show("portrait", resize=(120, 120), cache=True)
            null height 25
            button:
                style_group "basic"
                align (0.5, 0.5)
                xysize (150, 30)
                action Return(["equip_for"])
                text "Auto Equip"
            button:
                style_group "basic"
                xysize (150, 30)
                align (0.5, 0.5)
                if inv_source == char:
                    action [SetVariable("inv_source", hero), Function(hero.inventory.apply_filter, char.inventory.filter)]
                    text "Switch to MC"
                else:
                    action [SetVariable("inv_source", char), Function(char.inventory.apply_filter, hero.inventory.filter)]
                    text "Switch to Girl"
                    
    # Paging:
    frame:
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        pos (515, 317)
        xpadding 5
        ypadding 5
        use paging(ref=inv_source.inventory, use_filter=False, xysize=(190, 50), align=(0.5, 0.5))
        

    frame:
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        pos (515, 385)
        xpadding 5
        ypadding 15
        xysize (200,337) 
        if selectedslot:
            button:
                align (0.5, 0)
                style_group "basic"
                action Return(['item', 'equip/unequip'])
                minimum(190, 30)
                text "Equip / Unequip"

    # Inventory:
    # Filters
    vbox:
        pos (710, 36)
        spacing 1
        style_group "content"
        # Items info:
        frame:
            xalign 0.5
            xpadding 8
            background Null()
            use items_inv(char=inv_source, return_value=['item', 'equip'])
        vbox:
            null height -7
            style_group "dropdown_gm"
            xalign 0.5
            frame:
                ypadding 7
                xpadding 9
                xpos 1
                background Frame("content/gfx/frame/p_frame5.png", 5, 5)
                #xalign 0.5
                xysize (300, 30)
                hbox:
                    spacing 2
                    ypos -1
                    xalign 0.5
                    for filter in inv_source.inventory.GEQ_FILTERS:
                        $ img = ProportionalScale("content/gfx/interface/buttons/filters/%s.png" % filter, 44, 44)
                        $ img_hover = ProportionalScale("content/gfx/interface/buttons/filters/%s hover.png" % filter, 44, 44)
                        $ img_selected = ProportionalScale("content/gfx/interface/buttons/filters/%s selected.png" % filter, 44, 44)
                        imagebutton:
                            idle img
                            hover Transform(img_hover, alpha=1.1)
                            selected_idle img_selected
                            selected_hover Transform(img_selected, alpha=1.15)
                            action [Function(inv_source.inventory.apply_filter, filter), SelectedIf(filter == inv_source.inventory.filter)]
                            focus_mask True
        
        # Item Desciption:
        showif focusitem:
            null height -8
            frame:
                xalign 0.5
                xpadding 26
                background Null()
                frame:
                    ypos -3
                    xalign 0.5
                    at fade_in_out()
                    background Frame (Transform("content/gfx/frame/Mc_bg3.png", alpha=0.7), 10, 10)
                    xysize (517, 341)
                    use itemstats(item=focusitem, size=(542, 341))
                    xpadding 13
                    ypadding 5
        else:
            null height -8
            frame:
                xalign 0.5
                xpadding 26
                background Null()
                frame:
                    ypos -3
                    xalign 0.5
                    at fade_in_out()
                    background Null()
                    xysize (517, 342)
                    xpadding 13
                    ypadding 5
                        
    use pyt_top_stripe(True)
