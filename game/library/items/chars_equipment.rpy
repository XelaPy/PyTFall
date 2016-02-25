# Temp code, should be moved to items funcs:
init:
    style positive_item_eqeffects_change:
        is text
        size 9
        color lawngreen
        
    style negative_item_eqeffects_chage:
        is positive_item_eqeffects_change
        color "#ff1a1a"
        
    screen discard_item(char, item):
        zorder 10
        modal True
        
        add Transform("content/gfx/images/bg_gradient2.png", alpha=0.3)
        frame:
            background Frame (Transform("content/gfx/frame/ink_box.png", alpha=0.75), 10, 10)
            style_group "dropdown_gm2"
            align (0.42, 0.61)
            xsize 500
            xpadding 10
            ypadding 10
            xmargin 0
            ymargin 0
            has vbox spacing 5 xfill True
            text "{=TisaOTM}{size=-3}Discard {color=#ffd700}[item.id]{/color}?" xalign 0.52 color "#ecc88a"
            hbox:
                xalign 0.5
                spacing 10
                textbutton "{size=-1}Yes":
                    xalign 0.5
                    action Function(char.inventory.remove, item), Hide("discard_item"), With(dissolve)
                $ amount = char.inventory.get_item_count(item)
                textbutton "{size=-1}Discard All":
                    xalign 0.5
                    action SensitiveIf(amount > 1), Function(char.inventory.remove, item, amount), Hide("discard_item"), With(dissolve)
                textbutton "{size=-1}No":
                    xalign 0.5
                    action Hide("discard_item"), With(dissolve)
                

init python:
    def build_str_for_eq(eqtarget, dummy, stat, tempc):
        temp = getattr(dummy, stat) - getattr(eqtarget, stat) if dummy else False
        tempmax = dummy.get_max(stat) - eqtarget.get_max(stat) if dummy else False
        if temp: # Case: Any Change to stat
            # The first is the absolute change, we want it to be colored green if it is positive, and red if it is not.
            tempstr = "{color=[green]}%s{/color}"%getattr(dummy, stat) if temp > 0 else "{color=[red]} %d{/color}"%getattr(dummy, stat)
            # Next is the increase:
            tempstr = tempstr + "{=positive_item_eqeffects_change}(+%d){/=}"%temp if temp > 0 else tempstr + "{=negative_item_eqeffects_chage}(%d){/=}"%temp
        else: # No change at all...
            tempstr = "{color=[tempc]}%s{/color}"%getattr(eqtarget, stat)
            
        tempstr = tempstr + "{color=[tempc]}/{/color}"
            
        if tempmax:
            # Absolute change of the max values, same rules as the actual values apply:
            tempstr = tempstr + "{color=[green]}%s{/color}"%dummy.get_max(stat) if tempmax > 0 else tempstr + "{color=[red]} %d{/color}"%dummy.get_max(stat)
            tempstr = tempstr + "{=positive_item_eqeffects_change}(+%d){/=}"%tempmax if tempmax > 0 else tempstr + "{=negative_item_eqeffects_chage}(%d){/=}"%tempmax
        else:
            tempstr = tempstr + "{color=[tempc]}%s{/color}"%eqtarget.get_max(stat)
        return tempstr

label char_equip:
    python:
        focusitem = None
        selectedslot = None
        unequip_slot = None
        item_direction = None
        dummy = None
        
        eqtarget.inventory.set_page_size(16)
        # eqtarget.inventory.famale_filter = True
        hero.inventory.set_page_size(16)
        # hero.inventory.famale_filter = True
        inv_source = eqtarget
    
    scene bg gallery3
    
    $ global_flags.set_flag("hero_equip")
    $ renpy.retain_after_load()
    show screen char_equip
    
    $ inv_source.inventory.apply_filter("all")
    
label char_equip_loop:
    while 1:
        
        $ result = ui.interact()
        
        if not result:
            jump char_equip_loop
        
        if result[0] == "jump":
            if result[1] == "item_transfer":
                hide char_equip
                $ pytfall.it = GuiItemsTransfer("personal_transfer", char=eqtarget, last_label="char_equip")
                jump items_transfer
                
        elif result[0] == "equip_for":
            python:
                renpy.show_screen("equip_for", renpy.get_mouse_pos())
                dummy = None
            
        elif result[0] == "item":
            if result[1] == 'equip/unequip':
                python:
                    if item_direction == 'equip':
                        # Common to any eqtarget:
                        if not can_equip(focusitem, eqtarget, silent=False):
                            focusitem = None
                            selectedslot = None
                            unequip_slot = None
                            item_direction = None
                            dummy = None
                            jump("char_equip_loop")
                        if eqtarget == hero: # Simpler MCs logic:
                            equip_item(focusitem, eqtarget, area_effect=True)
                        else: # Actors: Maybe it's a good idea to encapsulate this:
                            if eqtarget.status == "slave" and focusitem.slot in ["weapon"] and not focusitem.type.lower().startswith("nw"):
                                renpy.show_screen('message_screen', "Slaves are forbidden to equip large weapons by law!")
                            else:
                                if inv_source == eqtarget:
                                    if all([eqtarget.status != "slave", eqtarget.disposition < 850]) or all([eqtarget.status != "slave", (focusitem.badness > 90 or focusitem.eqchance < 10)]):
                                        eqtarget.say(choice(["I can manage my own things!", "Get away from my stuff!", "Don't want to..."]))
                                    else:
                                        equip_item(focusitem, eqtarget, area_effect=True)
                                else:
                                    if all([eqtarget.status != "slave", (focusitem.badness > 90 or focusitem.eqchance < 10)]):
                                        eqtarget.say(choice(["No way!", "I do not want this!", "No way in hell!"]))
                                    else:
                                        if transfer_items(inv_source, eqtarget, focusitem):
                                            equip_item(focusitem, eqtarget, area_effect=True)
                            
                    elif item_direction == 'unequip':
                        if eqtarget == hero:
                            hero.unequip(focusitem, unequip_slot)
                        else: # Not MC
                            if eqtarget.status == "slave": # Slave condition:
                                eqtarget.unequip(focusitem, unequip_slot)
                                eqtarget.inventory.remove(focusitem)
                                inv_source.inventory.append(focusitem)
                            else: # Free Girl
                                if inv_source == hero:
                                    eqtarget.unequip(focusitem, unequip_slot)
                                    if not transfer_items(eqtarget, hero, focusitem, silent=False):
                                        eqtarget.equip(focusitem)
                                        eqtarget.say(choice(["I can manage my own things!", "Get away from my stuff!", "I'll think about it..."]))
                                elif eqtarget.disposition < 850:
                                    eqtarget.say(choice(["I can manage my own things!", "Get away from my stuff!", "I'll think about it..."]))
                                else:
                                    eqtarget.unequip(focusitem, unequip_slot)
                                
                    focusitem = None
                    selectedslot = None
                    unequip_slot = None
                    item_direction = None
                    dummy = None
                 
            elif result[1] == "discard":
                python:
                    if inv_source == hero:
                        renpy.call_screen("discard_item", inv_source, focusitem)
                    else:
                        if eqtarget.disposition < 850:
                            eqtarget.say(choice(["I can manage my own things!", "Get away from my stuff!", "I'll think about it..."]))
                        else:
                            renpy.call_screen("discard_item", inv_source, focusitem)
                            
                    focusitem = None
                    selectedslot = None
                    unequip_slot = None
                    item_direction = None
                    dummy = None
                
            elif result[1] == "transfer":
                python:
                    if inv_source == hero:
                        transfer_items(hero, eqtarget, focusitem, silent=False)
                    else:
                        transfer_items(eqtarget, hero, focusitem, silent=False)
                    
            elif result[1] == 'equip':
                python:
                    focusitem = result[2]
                    selectedslot = focusitem.slot
                    item_direction = 'equip'
                    
                    # # To Calc the effects:
                    dummy = copy_char(eqtarget)
                    equip_item(focusitem, dummy, silent=True)
                    # renpy.show_screen("diff_item_effects", eqtarget, dummy)
                    
            elif result[1] == 'unequip':
                python:
                    if len(result) == 4:
                        unequip_slot = result[3]
                        
                    selectedslot = result[2].slot
                    if selectedslot:
                        focusitem = result[2]
                        item_direction = 'unequip'
                        
                    # To Calc the effects:
                    dummy = copy_char(eqtarget)
                    dummy.eqslots[selectedslot] = focusitem
                    dummy.unequip(focusitem, unequip_slot)
                    # renpy.show_screen("diff_item_effects", eqtarget, dummy)
        
        elif result[0] == 'con':
            if result[1] == 'return':
                python:
                    focusitem = None
                    selectedslot = None
                    unequip_slot = None
                    item_direction = None
                    dummy = None
                    
        elif result[0] == 'control':
            if result[1] == 'return':
                jump char_equip_finish
    
label char_equip_finish:
    hide screen char_equip
    $ global_flags.del_flag("hero_equip")
    
    python:
        eqtarget.inventory.set_page_size(15)
        hero.inventory.set_page_size(15)
        # eqtarget.inventory.female_filter = False
        # hero.inventory.female_filter = False
        if eqtarget.location == "After Life":
            renpy.show_screen("message_screen", "Either your 'awesome' item handling or my 'brilliant' programming have killed %s..." % eqtarget.fullname)
            jump("mainscreen")
            
    if came_to_equip_from:
        $ last_label, came_to_equip_from = came_to_equip_from, None
        jump expression last_label
    else:
        jump char_profile

screen equip_for(pos=()):
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
                if t == "Combat" and eqtarget.status == "slave":
                    pass
                else:
                    textbutton "[t]":
                        xminimum 200
                        # action NullAction()
                        action [Function(eqtarget.equip_for, t), Hide("equip_for")]
            textbutton "Close":
                action Hide("equip_for")
    
screen char_equip():
    
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
        use eqdoll(active_mode=True, char=eqtarget, frame_size=[70, 70], scr_align=(0.98, 1.0), return_value=['item', "unequip"], txt_size=17, fx_size=(455, 400))
    
    # BASE FRAME 3 "mid layer" ====================================>
    add "content/gfx/frame/equipment.png"
    
    # Item Info (Mid-Bottom Frame): ====================================>
    hbox:
        align (0.388, 1.0)
        spacing 1
        style_group "content"
        
        # Item Desciption:
        showif focusitem:
            frame:
                xalign 0.6
                at fade_in_out()
                background Transform(Frame(im.MatrixColor("content/gfx/frame/Mc_bg3.png", im.matrix.brightness(-0.2)), 5, 5), alpha=0.3)
                xysize (710, 296)
                use itemstats2(item=focusitem, size=(703, 296), tt=tt)
        
    # Left Frame: =====================================>
    fixed:
        pos (0, 2)
        xysize (220,724) 
        style_group "content"
        
        # NAME =====================================>
        text (u"{color=#ecc88a}[eqtarget.name]") font "fonts/TisaOTM.otf" size 28 outlines [(1, "#3a3a3a", 0, 0)] xalign 0.53 ypos 126
        
        # PORTRAIT ============================>
        add eqtarget.show("portrait", resize=(100, 100), cache=True) pos (64, 11)
            
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
            label "{color=#CDAD00}[eqtarget.level]" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)] ypos 173
        
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
                vbox spacing 5:
                    pos (4, 40)
                    frame:
                        background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                        yminimum 270
                        xsize 218
                        xpadding 0
                        ypadding 0
                        xmargin 0
                        ymargin 0
                        style_group "stats"
                        has vbox spacing -7
                        # STATS ============================>
                        $ stats = ["constitution", "charisma", "intelligence", "fame", "reputation", "libido"] if eqtarget == hero else ["constitution", "charisma", "intelligence", "character", "reputation", "joy", "disposition"]
                        null height 10
                        frame:
                            xalign 0.5
                            xysize (215, 35)
                            style "base_stats_frame"
                            text "{color=#CD4F39}Health:" xalign (0.02)
                            $ tempc = red if eqtarget.health <= eqtarget.get_max("health")*0.3 else "#F5F5DC"
                            if dummy:
                                $ tempstr = build_str_for_eq(eqtarget, dummy, "health", tempc)
                                text tempstr style "stats_value_text" xalign 1.0 yoffset 3
                            else:
                                text u"[eqtarget.health]/{}".format(eqtarget.get_max("health")) style "stats_value_text" xalign 1.0 color tempc  yoffset 3
                        
                        frame:
                            xalign 0.5
                            xysize (215, 35)
                            left_padding 9
                            right_padding 11
                            top_padding 4
                            bottom_padding 1
                            xmargin 0
                            ymargin 0
                            text "{color=#43CD80}Vitality:" xalign (0.02)
                            $ tempc = red if eqtarget.vitality <= eqtarget.get_max("vitality")*0.3 else "#F5F5DC"
                            if dummy:
                                $ tempstr = build_str_for_eq(eqtarget, dummy, "vitality", tempc)
                                text tempstr style "stats_value_text" xalign 1.0 yoffset 3
                            else:
                                text u"[eqtarget.vitality]/{}".format(eqtarget.get_max("vitality")) style "stats_value_text" xalign 1.0 color tempc  yoffset 3
                            
                        for stat in stats:
                            frame:
                                xalign 0.5
                                xysize (215, 35)
                                style "base_stats_frame"
                                text "{color=#79CDCD}%s"%stat.capitalize() xalign (0.02)
                                if dummy:
                                    $ tempstr = build_str_for_eq(eqtarget, dummy, stat, tempc)
                                    text tempstr style "stats_value_text" xalign 1.0 yoffset 3
                                else:
                                    text u"{}/{}".format(getattr(eqtarget, stat), eqtarget.get_max(stat)) style "stats_value_text" xalign 1.0 color ivory yoffset 3
                                            
                    # BATTLE STATS ============================>
                    frame:
                        background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                        xysize (218, 230)
                        xpadding 0
                        ypadding 0
                        xmargin 0
                        ymargin 0
                        style_group "stats"
                        has vbox spacing -7
                        
                        null height 10
                        label (u"{size=18}{color=#CDCDC1}{b}Battle Stats:") xalign(0.49)
                        $ stats = [("Attack", "#CD4F39"), ("Defence", "#dc762c"), ("Magic", "#8470FF"), ("MP", "#009ACD"), ("Agility", "#1E90FF"), ("Luck", "#00FA9A")]
                        
                        null height 10
                    
                        for stat, color in stats:
                            frame:
                                style "base_stats_frame"
                                xalign 0.5
                                xysize (215, 35)
                                text "[stat]" color color size 16 xalign (0.02)
                                $ stat = stat.lower()
                                if stat == "mp":
                                    $ tempc = red if eqtarget.mp <= eqtarget.get_max("mp")*0.3 else color
                                else:
                                    $ tempc = color
                                if dummy:
                                    $ tempstr = build_str_for_eq(eqtarget, dummy, stat, tempc)
                                    text tempstr style "stats_value_text" xalign 1.0 yoffset 3
                                else:
                                    text "{}/{}".lower().format(getattr(eqtarget, stat.lower()), eqtarget.get_max(stat.lower())) style "stats_value_text" color color  xalign 1.0  yoffset 3
                                
            
            elif stats_display == "pro":
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                    pos (4, 40)
                    ymaximum 460
    
    # Right Frame: =====================================>
    # TOOLTIP TEXT or Applied Traits and Skills ====================================>
    frame:
        pos (930, 4)
        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.4), 10, 10)
        xpadding 10
        xysize (345, 110)
        
        python:
            if len(eqtarget.traits.basetraits) == 1:
                classes = list(eqtarget.traits.basetraits)[0].id
            elif len(eqtarget.traits.basetraits) == 2:
                classes = list(eqtarget.traits.basetraits)
                classes.sort()
                classes = ", ".join([str(c) for c in classes])
            else:
                if eqtarget != hero:
                    raise Exception("Character without prof basetraits detected! line: 267, girlsprofile screen")
                else:
                    classes = "MC baseclasses are still AFK :("
        
        $ t = "{vspace=17}Classes: [classes]\nLocation: [eqtarget.location]\nAction: [eqtarget.action]{/color}"
        
        if dummy:
            # Traits and skills:
            vbox:
                hbox:
                    add "content/gfx/interface/images/add.png" yalign 0.7
                    add "content/gfx/interface/images/remove.png" yalign 0.9
                    label ('Traits:') text_size 16 text_color gold style "stats_label"
                viewport:
                    mousewheel True
                    has vbox
                    style_group "stats"
                    python:
                        t_old = set(t.id for t in eqtarget.traits)
                        if hasattr(eqtarget, "effects"):
                            for effect in eqtarget.effects:
                                if eqtarget.effects[effect]['active']:
                                    t_old.add(effect)
                        t_new = set(t.id for t in dummy.traits)
                        if hasattr(eqtarget, "effects"):
                            for effect in dummy.effects:
                                if dummy.effects[effect]['active']:
                                    t_new.add(effect)
                        temp = t_new.difference(t_old)
                        temp = sorted(list(temp))
                    if temp:
                        for skill in temp:
                            frame:
                                xpadding 3
                                text u'{color=#43CD80}%s'%trait.capitalize() size 16 yalign 0.5
                                    
                    python:
                        t_old = set(t.id for t in dummy.traits)
                        t_new = set(t.id for t in eqtarget.traits)
                        temp = t_new.difference(t_old)
                        temp = sorted(list(temp))
                    if temp:
                        for skill in temp:
                            frame:
                                xpadding 3
                                text u'{color=#CD4F39}%s'%trait.capitalize() size 16 yalign 0.5
                                
            vbox:
                xoffset 165
                hbox:
                    add "content/gfx/interface/images/add.png" yalign 0.7
                    add "content/gfx/interface/images/remove.png" yalign 0.9
                    label ('Skills:') text_size 16 text_color gold style "stats_label"
                viewport:
                    mousewheel True
                    has vbox
                    style_group "proper_stats"
                    python:
                        s_old = set(s.name for s in eqtarget.attack_skills + eqtarget.magic_skills)
                        s_new = set(s.name for s in dummy.attack_skills + dummy.magic_skills)
                        temp = s_new.difference(s_old)
                        temp = sorted(list(temp)) 
                    if temp:
                        for skill in temp:
                            frame:
                                xpadding 3
                                text u'{color=#43CD80}%s'%skill.capitalize() size 16 
                                    
                    python:
                        s_old = set(s.name for s in dummy.attack_skills + dummy.magic_skills)
                        s_new = set(s.name for s in eqtarget.attack_skills + eqtarget.magic_skills)
                        temp = s_new.difference(s_old)
                        temp = sorted(list(temp))
                    if temp:
                        for skill in temp:
                            frame:
                                xalign 0.98
                                xpadding 3
                                text u'{color=#CD4F39}%s'%skill.capitalize() size 16 yalign 0.5
                    
                    
        elif not tt.value and eqtarget.status == "slave":
            text (u"{color=[gold]}[eqtarget.name]{/color}{color=#ecc88a}  is Slave%s" % t) size 14 align (0.55, 0.65) font "fonts/TisaOTM.otf" line_leading -5
        elif not tt.value and eqtarget.status == "free":
            text (u"{color=[gold]}[eqtarget.name]{/color}{color=#ecc88a}  is Free%s" % t) size 14 align (0.55, 0.65) font "fonts/TisaOTM.otf" line_leading -5
        
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
            text "{color=#ecc88a}%s"%tt.value size 14 align (0.5, 0.5) font "fonts/TisaOTM.otf" line_leading -5
            
    # Right Frame Buttons ====================================>
    vbox:
        pos (931, 118)
        xsize 345
        spacing 4
        style_group "pb"
        hbox:
            xalign 0.5
            spacing 100
            button:
                xsize 70
                action SelectedIf(eqtarget == hero or inv_source == hero), If(eqtarget != hero, true=[SetVariable("inv_source", hero), Function(eqtarget.inventory.apply_filter, hero.inventory.filter), Return(['con', 'return']), With(dissolve)]) 
                hovered tt.Action("Equip from [hero.nickname]'s Inventory")
                text "Hero" style "pb_button_text"
            button:
                xsize 70
                action SelectedIf(inv_source != hero), SensitiveIf(eqtarget != hero), If(eqtarget != hero, true=[SetVariable("inv_source", eqtarget), Function(eqtarget.inventory.apply_filter, hero.inventory.filter), Return(['con', 'return']), With(dissolve)])
                hovered tt.Action("Equip from [eqtarget.nickname]'s Inventory")
                text "Girl" style "pb_button_text"
        button:
            xalign 0.5
            xysize (110, 30)
            action If(eqtarget != hero, true=Show("girls_list1"))
            text "Girls List" style "pb_button_text"
            
    # Auto-Equip/Item Transfer Buttons and Paging: ================>
    frame:
        background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
        pos (931, 184)
        xysize (345, 80)
        has vbox spacing 1 xalign 0.5
        hbox:
            button:
                xysize (140, 30)
                action Return(["equip_for"])
                text "Auto Equip" style "pb_button_text"
            button:
                xysize (140, 30)
                action If(eqtarget != hero, true=Return(["jump", "item_transfer"]))
                text "Items Transfer" style "pb_button_text"
        use paging(ref=inv_source.inventory, use_filter=False, xysize=(250, 20), align=(0.5, 0.5))
        
    # Filters: ====================================>
    hbox:
        pos (935, 268)
        box_wrap True
        style_group "dropdown_gm"
        xsize 340
        spacing 2 
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
        pos (931, 372)
        background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
        use items_inv(char=inv_source, main_size=(333, 333), frame_size=(80, 80), return_value=['item', 'equip'])
        
    # BASE FRAME 1 "top layer" ====================================>
    add "content/gfx/frame/h1.png"
    
    imagebutton:
        pos (178, 70)
        idle im.Scale("content/gfx/interface/buttons/close2.png", 35, 35)
        hover im.Scale("content/gfx/interface/buttons/close2_h.png", 35, 35)
        action Return(['control', 'return'])
        hovered tt.Action("Return to previous screen!")
    
screen girls_list1(source=None, page=0, total_pages=1):
    modal True
    zorder 1
    
    key "mousedown_3" action Hide("girls_list1")
    
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
                    action Hide("girls_list1")
                
                    
screen itemstats2(item=None, char=None, size=(635, 380), style_group="content", mc_mode=False, tt=None):
    
    key "mousedown_3" action Return(['con', 'return'])
    
    # One of the most difficult code rewrites I've ever done (How Gismo aligned everything in the first place is a work of (weird and clumsy) art...):
    # Recoding this as three vertically aligned HBoxes...
    if item:
        $ xs = size[0]
        $ ys = size[1]
        fixed:
            xysize (xs, ys)
            
            # Top HBox: Discard/Close buttons and the Item ID:
            hbox:
                align .5, 0
                xsize xs-10
                imagebutton:
                    xalign 0
                    idle ("content/gfx/interface/buttons/discard.png")
                    hover ("content/gfx/interface/buttons/discard_h.png")
                    action Return(["item", "discard"])
                    if tt:
                        hovered tt.Action("Discard item")
                frame:
                    xalign .5
                    xysize (439, 20)
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                    label ('[item.id]') text_color gold xalign 0.5 text_size 19 text_outlines [(1, "#000000", 0, 0)] text_style "interactions_text"
                imagebutton:
                    xalign 1.0
                    idle ("content/gfx/interface/buttons/close3.png")
                    hover ("content/gfx/interface/buttons/close3_h.png")
                    action Return(['con', 'return'])
                    if tt:
                        hovered tt.Action("Close item info")
            
            # Separation Strip (Outside of alignments):
            label ('{color=#ecc88a}__________________________________________') text_style "stats_value_text" xalign .5 ypos 28
            label ('{color=#ecc88a}__________________________________________') text_style "stats_value_text" xalign .5 ypos 163
            
            # Mid HBox:
            hbox:
                xsize xs
                xalign .5
                ypos 47
                spacing 5
                
                # Left Items Info:
                frame:
                    xalign 0.02
                    style_group "proper_stats"
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                    xysize (180, 130)
                    xpadding 0
                    xmargin 0
                    has vbox spacing 1 xoffset 10
                    null height 15
                    frame:
                        xysize (160, 25)
                        text ('Price:') color gold xalign 0.02
                        label ('{size=-4}{color=[gold]}[item.price]') align (0.98, 0.5) style "stats_value_text" text_outlines [(1, "#3a3a3a", 0, 0)]
                    frame:
                        xysize (160, 25)
                        text ('{color=#F5F5DC}Slot:') xalign 0.02
                        label ('{color=#F5F5DC}{size=-4}%s'%item.slot.capitalize()) align (0.98, 0.5) style "stats_value_text" text_outlines [(1, "#3a3a3a", 0, 0)]
                    frame:
                        xysize (160, 25)
                        text ('{color=#F5F5DC}Type:') xalign 0.02
                        label ('{color=#F5F5DC}{size=-4}%s'%item.type.capitalize()) align (0.98, 0.5) style "stats_value_text" text_outlines [(1, "#3a3a3a", 0, 0)]
                    frame:
                        xysize (160, 25)
                        text ('{color=#F5F5DC}Sex:') xalign 0.02
                        if item.sex == 'male':
                            label ('{color=#F5F5DC}{size=-4}{color=#FFA54F}%s'%item.sex.capitalize()) align (0.98, 0.5) style "stats_value_text" text_outlines [(1, "#3a3a3a", 0, 0)]
                        if item.sex == 'female':
                            label ('{color=#F5F5DC}{size=-4}{color=#FFAEB9}%s'%item.sex.capitalize()) align (0.98, 0.5) style "stats_value_text" text_outlines [(1, "#3a3a3a", 0, 0)]
                        if item.sex == 'unisex':
                            label ('{color=#F5F5DC}{size=-4}%s'%item.sex.capitalize()) align (0.98, 0.5) style "stats_value_text" text_outlines [(1, "#3a3a3a", 0, 0)]
                
                # Buttons and image:
                button:
                    style_group "pb"
                    align (0.0, 0.5)
                    xysize (80, 45)
                    action SensitiveIf(eqtarget != hero), Return(['item', 'transfer'])
                    if eqtarget == hero:
                        hovered tt.Action("Disabled")
                        text "Disabled" style "pb_button_text" align (0.5, 0.5)
                    elif inv_source == hero:
                        hovered tt.Action("Transfer {} from {} to {}".format(item.id, hero.nickname, eqtarget.nickname))
                        text "Give to\n {color=#FFAEB9}[eqtarget.nickname]{/color}" style "pb_button_text" align (0.5, 0.5) line_leading 3
                    else:
                        text "Give to\n {color=#FFA54F}[hero.nickname]{/color}" style "pb_button_text" align (0.5, 0.5) line_leading 3
                        hovered tt.Action("Transfer {} from {} to {}".format(item.id, eqtarget.nickname, hero.nickname))
                        
                frame:
                    align (0.5, 0.5)
                    background Frame("content/gfx/frame/frame_it2.png", 5, 5)
                    xysize (120, 120)
                    add (ProportionalScale(item.icon, 100, 100)) align(0.5, 0.5)
                    
                if item_direction == 'unequip':
                    $ temp = "Unequip"
                    $ temp_msg = "Unequip {}".format(item.id)
                elif item_direction == 'equip':
                    if item.slot == "consumable":
                        $ temp = "Use"
                        $ temp_msg = "Use {}".format(item.id)
                    else:
                        $ temp = "Equip"
                        $ temp_msg = "Equip {}".format(item.id)
                button:
                    style_group "pb"
                    align (1.0, 0.5)
                    xysize (80, 45)
                    if tt:
                       hovered tt.Action(temp_msg)
                    action Return(['item', 'equip/unequip'])
                    text "[temp]" style "pb_button_text" align (0.5, 0.5)
                    
                # Right items info (Stats):
                frame:
                    xalign 0.98
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                    xysize (185, 130)
                    has viewport scrollbars "vertical" draggable True mousewheel True child_size 200, 500
                    vbox:
                        if item.mod:
                            label ('Stats:') text_size 18 text_color gold xpos 30
                            vbox:
                                spacing 1
                                style_group "proper_stats"
                                for stat, value in item.mod.items():
                                    frame:
                                        xysize (160, 18)
                                        text (u'{color=#F5F5DC}%s' % stat.capitalize()) size 15 xalign 0.02 yoffset -2
                                        label (u'{color=#F5F5DC}{size=-4}[value]') style "stats_value_text" align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                            null height 7
                            
                        if item.max:
                            label ('Max:') text_size 16 text_color gold xpos 30
                            vbox:
                                spacing 1
                                style_group "proper_stats"
                                for stat, value in item.max.items():
                                    frame:
                                        xysize (160, 18)
                                        text (u'{color=#F5F5DC}%s'%stat.capitalize()) size 15 xalign 0.02 yoffset -2
                                        label (u'{color=#F5F5DC}{size=-4}[value]') style "stats_value_text" align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                            null height 7
                            
                        if item.min:
                            label ('Min:') text_size 16 text_color gold xpos 30
                            vbox:
                                spacing 1
                                style_group "proper_stats"
                            for stat, value in item.min.items():
                                frame:
                                    xysize (160, 18)
                                    text (u'{color=#F5F5DC}%s'%stat.capitalize()) size 15 xalign 0.02 yoffset -2
                                    label (u'{color=#F5F5DC}{size=-4}%d'%value) style "stats_value_text" align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                
            # Bottom HBox: Desc/Traits/Effects/Skills:
            hbox:
                yalign 0.98
                # Traits, Effects:
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                    xysize (158, 108)
                    has viewport scrollbars "vertical" draggable True mousewheel True
                    
                    # Traits:
                    vbox:
                        style_group "proper_stats"
                        if item.addtraits or item.removetraits:
                            hbox:
                                align (0.1, 0.5)
                                label ('Traits:') text_size 14 text_color gold xoffset 7
                                if item.addtraits:
                                    add "content/gfx/interface/images/add.png" yalign 0.7 xoffset 26
                                if item.removetraits:
                                    add "content/gfx/interface/images/remove.png" yalign 0.9 xoffset 26
                                    
                            for trait in item.addtraits:
                                frame:
                                    xalign 0.02
                                    xpadding 2
                                    text (u'{color=#43CD80}%s'%trait.capitalize()) size 15 align .5, .5
                            for trait in item.removetraits:
                                frame:
                                    xalign 0.98
                                    xpadding 2
                                    text (u'{color=#CD4F39}%s'%trait.capitalize()) size 15 align .5, .5
                                
                        # Effects:
                        if item.addeffects or item.removeeffects:
                            null height 5
                            hbox:
                                align (0.1, 0.5)
                                label ('Effects:') text_size 14 text_color gold xoffset 7
                                if item.addeffects:
                                    add "content/gfx/interface/images/add.png" yalign 0.7 xoffset 25
                                if item.removeeffects:
                                    add "content/gfx/interface/images/remove.png" yalign 0.9 xoffset 25
    
                            for effect in item.addeffects:
                                frame:
                                    xalign 0.02
                                    xpadding 2
                                    text (u'{color=#43CD80}%s'%effect.capitalize()) size 15 align .5, .5
                            for effect in item.removeeffects:
                                frame:
                                    xalign 0.98
                                    xpadding 2
                                    text (u'{color=#CD4F39}%s'%effect.capitalize()) size 15 align .5, .5
                
                frame:
                    xysize 382, 108 
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.9)
                    has viewport scrollbars "vertical" mousewheel True
                    text '[item.desc]' font "fonts/TisaOTM.otf" size 15 color "#ecc88a" outlines [(1, "#3a3a3a", 0, 0)] xalign 0.5
                    
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                    xysize (158, 108)
                    has viewport scrollbars "vertical" draggable True mousewheel True
                    vbox:
                        style_group "proper_stats"
                        if item.add_be_spells or item.remove_be_spells:
                            hbox:
                                align (0.1, 0.5)
                                label ('Skills:') text_size 14 text_color gold xoffset 7
                                if item.add_be_spells:
                                    add "content/gfx/interface/images/add.png" yalign 0.7 xoffset 26
                                if item.remove_be_spells:
                                    add "content/gfx/interface/images/remove.png" yalign 0.9 xoffset 26
                                    
                            for skill in item.add_be_spells:
                                frame:
                                    xalign 0.02
                                    xpadding 2
                                    text (u'{color=#43CD80}%s'%skill.capitalize()) size 15 align .5, .5
                            for skill in item.remove_be_spells:
                                frame:
                                    xalign 0.98
                                    xpadding 2
                                    text (u'{color=#CD4F39}%s'%skill.capitalize()) size 15 align .5, .5
                                                        
                                                        
screen diff_item_effects(char, dummy):
    zorder 10
    textbutton "X":
        align (1.0, 0.0)
        action Hide("diff_item_effects")
    frame:
        xysize (1000, 500)
        background Solid("#F00", alpha=0.1)
        align (0.1, 0.5)
        has hbox
        
        vbox:
            text "Stats:"
            for stat in char.stats:
                text "[stat]: {}".format(getattr(dummy, stat) - getattr(char, stat))
        vbox:
            text "Max Stats:"
            for stat in char.stats:
                text "[stat]: {}".format(dummy.get_max(stat) - char.get_max(stat))
        vbox:
            for skill in char.stats.skills:
                text "[skill]: {}".format(dummy.get_skill(skill) - char.get_skill(skill))
        vbox:
            text "Traits (any):"
            python:
                t_old = set(t.id for t in char.traits)
                t_new = set(t.id for t in dummy.traits)
                temp = t_new.difference(t_old)
                temp = sorted(list(temp))
            for t in temp:
                text "[t]"
