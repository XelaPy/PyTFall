label girl_equip:
    python:
        focusitem = False
        selectedslot = None
        item_direction = None
        char.inventory.set_page_size(16)
        # char.inventory.famale_filter = True
        hero.inventory.set_page_size(16)
        # hero.inventory.famale_filter = True
        inv_source = char
    
    scene bg gallery3
    
    $ global_flags.set_flag("hero_equip")
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
            
            elif result[0] == 'choice':
                renpy.hide_screen("pyt_girls_list1")
                char = result[1]
                jump('girl_equip')
            elif result[0] == "paging":
                gs = renpy.get_screen("pyt_girls_list1").scope["_kwargs"]["source"]
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
            
            elif result[0] == 'con':
                if result[1] == 'return':
                    selectedslot = False
                    focusitem = False
            
            elif result[0] == 'control':
                if result[1] == 'return':
                    break
    
    hide screen pyt_girl_equip
    $ global_flags.del_flag("hero_equip")
    
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
    
    # Useful keymappings (first time I try this in PyTFall): ====================================>
    if focusitem:
        key "mousedown_2" action Return(["item", "equip/unequip"])
    else:
        key "mousedown_2" action NullAction()
    key "mousedown_3" action Return(['control', 'return'])
    key "mousedown_4" action Function(inv_source.inventory.next)
    key "mousedown_5" action Function(inv_source.inventory.prev)
    key "mousedown_6" action Return(['con', 'return'])
    
    default stats_display = "stats"
    default tt = Tooltip("")
    
    # BASE FRAME 2 "bottom layer" ====================================>
    add "content/gfx/frame/equipment2.png"
    
    # Equipment slots
    frame:
        pos (425, 10)
        xminimum 298
        xmaximum 298
        ymaximum 410
        yminimum 410
        background Frame(Transform("content/gfx/frame/Mc_bg3.png", alpha=0.3), 10, 10)
        use pyt_eqdoll(active_mode=True, char=inv_source, frame_size=[70, 70], scr_align=(0.98, 1.0), return_value=['item', "unequip"], txt_size=17, fx_size=(455, 400))
    
    # BASE FRAME 3 "mid layer" ====================================>
    add "content/gfx/frame/equipment.png"
    
    # Item Info: ====================================>
    hbox:
        align (0.388, 1.0)
        spacing 1
        style_group "content"
        
        # Item Desciption:
        showif focusitem:
            frame:
                xalign 0.6
                xpadding 13
                ypadding 5
                at fade_in_out()
                background Transform(Frame(im.MatrixColor("content/gfx/frame/Mc_bg3.png", im.matrix.brightness(-0.2)), 5, 5), alpha=0.3)
                xysize (710, 296)
                use itemstats2(item=focusitem, size=(710, 296))
        
    # Left Frame: =====================================>
    fixed:
        pos (0, 2)
        xysize (220,724) 
        style_group "content"
        
        # NAME =====================================>
        text (u"{color=#ecc88a}[inv_source.name]") font "fonts/TisaOTM.otf" size 28 outlines [(1, "#3a3a3a", 0, 0)] xalign 0.53 ypos 126
        
        # PORTRAIT ============================>
        add inv_source.show("portrait", resize=(100, 100), cache=True) pos (64, 11)
            
        # LVL ============================>
        hbox:
            spacing 1
            if (inv_source.level) <10:
                xpos 95
            elif (inv_source.level) <100:
                xpos 93
            elif (inv_source.level) <1000:
                xpos 89
            elif (inv_source.level) <10000:
                xpos 83
            else:
                xpos 79
            label "{color=#CDAD00}Lvl" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)] ypos 173
            label "{color=#CDAD00}[inv_source.level]" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)] ypos 173
        
        # Left Frame Buttons: =====================================>
        hbox:
            style_group "pb"
            xalign 0.55
            ypos 198
            spacing 1
            button:
                xsize 100
                action SetScreenVariable("stats_display", "stats"), With(dissolve)
                text "Stats" style "pb_button_text"
            button:
                xsize 100
                action SetScreenVariable("stats_display", "pro"), With(dissolve)
                text "Pro Stats" style "pb_button_text"
        
        vbox:
            yfill True
            yoffset 195
            spacing 2
            xmaximum 218
            
            if stats_display == "stats":
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                    pos (4, 40)
                    yminimum 285
                    
                    # STATS ============================>
                    hbox:
                        xanchor -2
                        if inv_source == hero:
                            $ stats = ["constitution", "charisma", "intelligence", "fame", "reputation", "libido"]
                        else:
                            $ stats = ["constitution", "charisma", "intelligence", "character", "reputation", "joy", "disposition"]
                        vbox:
                            style_group "stats"
                            spacing -7
                            xanchor 2
                            xmaximum 113
                            frame:
                                xysize (207, 8)
                                text "{color=#CD4F39}Health:" xalign (0.02)
                            frame:
                                xysize (207, 8)
                                text "{color=#43CD80}Vitality:" xalign (0.02)
                            for stat in stats:
                                frame:
                                    xysize (207, 8)
                                    text ('{color=#79CDCD}%s'%stat.capitalize()) color ivory size 17 xalign (0.02) 
                        vbox:
                            yalign (0.65)
                            spacing 8
                            xanchor 20
                            xfill True
                            xminimum 0
                            xmaximum 120
                            
                            if inv_source.health <= inv_source.get_max("health")*0.3:
                                text (u"{color=[red]}%s/%s"%(inv_source.health, inv_source.get_max("health"))) style "stats_value_text" xalign (1.0)
                            else:
                                text (u"{color=#F5F5DC}%s/%s"%(inv_source.health, inv_source.get_max("health"))) style "stats_value_text" xalign (1.0)
                            if inv_source.vitality <= inv_source.get_max("vitality")*0.3:
                                text (u"{color=[red]}%s/%s"%(inv_source.vitality, inv_source.get_max("vitality"))) style "stats_value_text" xalign (1.0)
                            else:
                                text (u"{color=#F5F5DC}%s/%s"%(inv_source.vitality, inv_source.get_max("vitality"))) style "stats_value_text" xalign (1.0)
                        
                            for stat in stats:
                                text ('{color=#F5F5DC}%d/%d'%(getattr(inv_source, stat), inv_source.get_max(stat))) style "stats_value_text" xalign (1.0)
            
                # BATTLE STATS ============================>
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                    yalign 1.0
                    xpos 4
                    yoffset -201
                    xmaximum 218
                    ypadding 10
                    
                    vbox:
                        text (u"{size=18}{color=#CDCDC1}{b}Battle Stats:") xalign(0.49) style_group "ddlist"
                        style_group "stats"
                        spacing -6
                        $ stats = [("Attack", "#CD4F39"), ("Defence", "#dc762c"), ("Magic", "#8470FF"), ("MP", "#009ACD"), ("Agility", "#1E90FF"), ("Luck", "#00FA9A")]
                        
                        null height 10
                    
                        for stat, color in stats:
                            frame:
                                xysize (207, 31)
                                text "[stat]" color color size 16 align (0.02, 0.5)
                                text "{}/{}".lower().format(getattr(inv_source, stat.lower()), inv_source.get_max(stat.lower())) style "stats_value_text" color color size 16 align (0.98, 0.5)
            
            elif stats_display == "pro":
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                    pos (4, 40)
                    ymaximum 460
    
    # Right Frame: =====================================>
    vbox:
        align (1.0, 1.0)
        fixed:
            xalign 0.5
            xysize (350, 260)
            vbox:
                yoffset 3
                xalign 0.55
                yfill True
                style_group "pb"
                
                python:
                    if len(char.traits.basetraits) == 1:
                        classes = list(char.traits.basetraits)[0].id
                    elif len(char.traits.basetraits) == 2:
                        classes = list(char.traits.basetraits)
                        classes.sort()
                        classes = ", ".join([str(c) for c in classes])
                    else:
                        raise Exception("Character without prof basetraits detected! line: 267, girlsprofile screen")
                
                # TOOLTIP TEXT ====================================>
                frame:
                    background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.4), 10, 10)
                    xoffset -2
                    xpadding 10
                    xysize (346, 110)
                    has hbox spacing 1
                    xfill True
                    yfill True
                    
                    $ t = "{vspace=17}Classes: [classes]\nLocation: [char.location]\nAction: [char.action]{/color}"
                    
                    if (not tt.value and inv_source == char) and char.status == "slave":
                        text (u"{color=[gold]}[char.name]{/color}{color=#ecc88a}  is Slave%s" % t) size 14 align (0.55, 0.65) font "fonts/TisaOTM.otf" line_leading -5
                    elif (not tt.value and inv_source == char) and char.status == "free":
                        text (u"{color=[gold]}[char.name]{/color}{color=#ecc88a}  is Free%s" % t) size 14 align (0.55, 0.65) font "fonts/TisaOTM.otf" line_leading -5
                    
                    #if isinstance(tt.value, BE_Action):
                        #$ element = tt.value.get_element()
                        #if element:
                            #fixed:
                                #xysize (80, 80)
                                #yalign 0.5
                                #if element.icon:
                                    #$ img = ProportionalScale(element.icon, 70, 70)
                                    #add img align (0.5, 0.5)
                        #text tt.value.desc style "content_text" size 18 color "#ecc88a" yalign 0.1
                    
                    elif tt.value:
                        text (u"{color=#ecc88a}%s" % tt.value) size 14 align (0.5, 0.5) font "fonts/TisaOTM.otf" line_leading -5
                
                # Right Frame Buttons ====================================>
                hbox:
                    xalign 0.5
                    ypos 3
                    spacing 2
                    button:
                        align (0.5, 0.5)
                        xsize 70
                        action [SetVariable("inv_source", hero), Function(char.inventory.apply_filter, hero.inventory.filter), Return(['con', 'return'])], With(dissolve) 
                        hovered tt.Action("Choose a Hero")
                        text "Hero" style "pb_button_text"
                    null width 100
                    button:
                        align (0.5, 0.5)
                        xsize 70
                        action [SetVariable("inv_source", char), Function(char.inventory.apply_filter, hero.inventory.filter), Return(['con', 'return'])], With(dissolve)
                        hovered tt.Action("Choose a Girl")
                        text "Girl" style "pb_button_text"
                button:
                    ypos 17
                    align (0.5, 0.5)
                    xysize (110, 30)
                    action Show("pyt_girls_list1")
                    text "Girls List" style "pb_button_text"
                
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                    align (0.5, 1.0)
                    xysize (345, 80)
                    vbox:
                        align (0.55, 0.5)
                        spacing 1
                        hbox:
                            button:
                                align (0.5, 0.5)
                                xysize (140, 30)
                                action Return(["equip_for"])
                                text "Auto Equip" style "pb_button_text"
                            button:
                                align (0.5, 0.5)
                                xysize (140, 30)
                                action Return(["equip_for"])
                                text "Items Transfer" style "pb_button_text"
                        
                        # Paging: ====================================>
                        use paging(ref=inv_source.inventory, use_filter=False, xysize=(250, 20), align=(0.5, 0.5))
        
        # Filters: ====================================>
        frame:
            style_group "dropdown_gm"
            background Null()
            xalign 0.5
            hbox:
                spacing 4
                xalign 0.5
                xminimum 350
                xmaximum 350
                box_wrap True
                for filter in inv_source.inventory.ALL_FILTERS:
                    frame:
                        xpadding 0
                        ymargin -8
                        background Null() 
                        $ img = ProportionalScale("content/gfx/interface/buttons/filters/%s.png" % filter, 44, 44)
                        $ img_hover = ProportionalScale("content/gfx/interface/buttons/filters/%s hover.png" % filter, 44, 44)
                        $ img_selected = ProportionalScale("content/gfx/interface/buttons/filters/%s selected.png" % filter, 44, 44)
                        imagebutton:
                            idle img
                            hover Transform(img_hover, alpha=1.1)
                            selected_idle img_selected
                            selected_hover Transform(img_selected, alpha=1.15)
                            action [Function(inv_source.inventory.apply_filter, filter), SelectedIf(filter == inv_source.inventory.filter)], With(dissolve)
                            focus_mask True
        
        # Inventory: ====================================>
        frame:
            xalign 0.55
            background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
            use items_inv(char=inv_source, main_size=(333, 333), frame_size=(80, 80), return_value=['item', 'equip'])
            ypos -2
        
    # BASE FRAME 1 "top layer" ====================================>
    add "content/gfx/frame/h1.png"
    
    #imagebutton: # Add this button when the screen is ready :Gismo
        #pos (178, 70)
        #idle im.Scale("content/gfx/interface/buttons/close2.png", 35, 35)
        #hover im.Scale("content/gfx/interface/buttons/close2h.png", 35, 35)
        #action Return(['control', 'return'])
        #hovered tt.Action("Return to previous screen!")
    
screen pyt_girls_list1(source=None, page=0, total_pages=1):
    modal True
    zorder 1
    
    key "mousedown_3" action Hide("pyt_girls_list1")
    
    frame:
        at fade_in_out()
        background Transform(Frame(im.MatrixColor("content/gfx/frame/Mc_bg3.png", im.matrix.brightness(-0.2)), 5, 5), alpha=0.3)
        xysize (710, 295)
        align (0.39, 0.998)
        vbox:
            align (0.5, 0.0)
            hbox:
                style_group "pb"
                align (0.5, 0.0)
                xfill True
                button:
                    align (0.5, 0.0)
                    xysize (100, 30)
                    action Return(["equip_for"])
                    text "Team" style "pb_button_text"
                button:
                    align (0.5, 0.0)
                    xysize (100, 30)
                    action Return(["equip_for"])
                    text "Status" style "pb_button_text"
                imagebutton:
                    #xoffset 9
                    yoffset -3
                    align (1.0, 0.0)
                    idle ("content/gfx/interface/buttons/close3.png")
                    hover ("content/gfx/interface/buttons/close3_h.png")
                    action Hide("pyt_girls_list1")
                
    
    #use pyt_top_stripe(True)
