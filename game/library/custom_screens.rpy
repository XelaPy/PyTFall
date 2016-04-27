################### Specialized ####################
init: # Items:
    screen items_inv(char=None, main_size=(553, 282), frame_size=(90, 90), return_value=['item', 'get']):
        frame:
            background Null()
            #background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
            xysize main_size
            has hbox box_wrap True
            #align (0.5, 0.5)
            for item in list(item for item in char.inventory.getpage()):
                frame:
                    if item.bg_color == "dark":
                        background Frame("content/gfx/frame/frame_it2.png", -1, -1)
                    else:
                        background Frame("content/gfx/frame/frame_it2.png", -1, -1)
                    xysize frame_size
                    use r_lightbutton (img=ProportionalScale(item.icon, 70, 70), return_value=return_value+[item], align=(0.5, 0.5))
                    label (u"{color=#ecc88a}%d" % char.inventory.content[item.id]):
                        align (0.995, 0.995)
                        style "stats_label_text"
                        text_size 18
                        text_outlines [(2, "#9c8975", 0, 0), (1, "#000000", 0, 0)]
                        #if item.bg_color == "dark":
                            #text_color ivory
    
    screen eqdoll(active_mode=True, char=None, frame_size=[55, 55], scr_align=(0.23, 0.23), return_value=['item', 'get'], txt_size=17, fx_size=(300, 320)):
        # active_mode = Allows equipped item to be focused if true, otherwise just dispayes a picture of an item (when equipped).
        # char = source of equipment slots.
        # Slots and the doll ------------------------------------------------------------>
        if char == hero:
            # add Transform(hero.show("sprofile", resize=(400, 720)), alpha=0.8) align(0.5, 1.0)
            add im.Scale("content/gfx/interface/images/doll_male.png", 286, 400) align (0.5, 0.5)
        else:
            #f rame:
                # align (0.5, 0.5)
                # background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
            add (char.show("vnsprite", resize=(288, 400), cache=True)) alpha 0.9 align (0.5, 1.0)
            # add im.Scale("content/gfx/interface/images/doll_fem.png", 350, 500) align (0.25, 0.23)
            
        fixed:
            style_group "content"
            align scr_align
            xysize fx_size
            
            for key in equipSlotsPositions:
                python:
                    if char.eqslots[key]:
                        img = char.eqslots[key].icon
                        # Frame background:
                        # Old dark/light frame codes, to be removed at review.
                        if char.eqslots[key].bg_color == "dark":
                            bg = im.Scale(im.Twocolor("content/gfx/frame/frame_it2.png", grey, black), *frame_size)
                        else:
                            bg = im.Scale(im.Twocolor("content/gfx/frame/frame_it2.png", grey, black), *frame_size)
                    else:
                        bg = im.Scale(im.Twocolor("content/gfx/frame/frame_it2.png", grey, black), *frame_size)
                        img = blank
                frame:
                    background bg
                    pos (equipSlotsPositions[key][1], equipSlotsPositions[key][2]-0.1)
                    xysize (frame_size[0], frame_size[1])
                    if active_mode and char.eqslots[key]:
                        use r_lightbutton(img=ProportionalScale(img, frame_size[0]-15, frame_size[1]-15), return_value=return_value+[char.eqslots[key]])
                    elif char.eqslots[key]:
                        add ProportionalScale(img, frame_size[0]-10, frame_size[1]-10) align (0.5, 0.5)
                    else:
                        text (u"{color=#CDCDC1}%s"%equipSlotsPositions[key][0]) align (0.5, 0.5) size txt_size
                        
        vbox:
            spacing 4
            align(1.0, 0.5)
            xoffset 150
            for key in ['ring', 'ring2',  'ring1']:
                python:
                    if char.eqslots[key]:
                        img = char.eqslots[key].icon
                        # Frame background:
                        if char.eqslots[key].bg_color == "dark":
                            bg = im.Scale(im.Twocolor("content/gfx/frame/frame_it2.png", grey, black), *frame_size)
                        else:
                            bg = im.Scale(im.Twocolor("content/gfx/frame/frame_it2.png", grey, black), *frame_size)
                    else:
                        bg = im.Scale(im.Twocolor("content/gfx/frame/frame_it2.png", grey, black), *frame_size)
                        img = blank
                frame:
                    background bg
                    xysize (frame_size[0], frame_size[1])
                    if active_mode and char.eqslots[key]:
                        # We add extra return to return value to control which ring exactly is removed...
                        use r_lightbutton(img=ProportionalScale(img, frame_size[0]-15, frame_size[1]-15), return_value=return_value+[char.eqslots[key], key])
                    elif char.eqslots[key]:
                        add (ProportionalScale(hero.eqslots[key].icon, frame_size[0]-15, frame_size[1]-15)) align (0.5, 0.5)
                    else:
                        text (u"{color=#CDCDC1}Ring") align (0.5, 0.5) size 14
    
    screen shopping(left_ref=None, right_ref=None):
        use shop_inventory(ref=left_ref, x=0.0)
        use shop_inventory(ref=right_ref, x=1.0)
        
        if focus:
            vbox:
                align (0.5, 0.5)
                frame:
                    background Frame("content/gfx/frame/frame_dec_1.png", 30, 30)
                    align (0.5, 0.5)
                    xpadding 30
                    ypadding 30
                    xysize (555, 400)
                    style_group "content"
    
                    use itemstats(item=focus, size=(580, 350))
                    
                frame:
                    background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                    align (0.5, 1.0)
                    xysize (300, 110)
                    vbox:
                        align (0.5, 1.0)
                        xysize (400, 110)
                        frame:
                            align (0.5, 0.5)
                            style_group "stats"
                            $ total_price = item_price * amount
                            label "Retail Price: [total_price]":
                                text_color gold
                                text_size 22
                                xalign 0.5
                        
                        fixed:
                            xsize 150
                            xalign 0.5
                            spacing 25
                            use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 40, 40), return_value=['control', "decrease_amount"], align=(0, 0.5))
                            text ("{size=36}[amount]") align (0.5, 0.5) color ivory style "proper_stats_label_text"
                            use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 40, 40), return_value=['control', "increase_amount"], align=(1.0, 0.5))
                        
                        button:
                            style_group "basic"
                            action Return(['item', 'buy/sell'])
                            xsize 100
                            xalign 0.5
                            if purchasing_dir == "buy":
                                text "Buy"
                            elif purchasing_dir == "sell":
                                text "Sell"
        
        use exit_button
    
    # Frame for item in girl inventory or a shop
    screen itemframe(txt="", value=None, img=None):
        frame:
            background Frame("content/gfx/frame/24-1.png", 5, 5)
            xysize (90, 90)
            imagebutton:
                align(0.0, 0.5)
                idle img
                hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
                action Return(value)
            text (txt) align(1.0, 1.0) style "content_text" size 20
    
    screen itemstats(item=None, size=(635, 380), style_group="content", mc_mode=False):
        if item:
            fixed:
                maximum (size[0], size[1])
                vbox:
                    align (0.5, 0.5)
                    yfill True
                    frame:
                        xalign 0.5
                        xysize (440, 40)
                        background Frame("content/gfx/frame/p_frame7.png", 10, 10)
                        label '[item.id]' text_color gold xalign 0.5 text_size 20 text_outlines [(1, "#000000", 0, 0)] text_style "interactions_text"
                    vbox:
                        yfill True
                        align (0.5, 0.5)
                        #xmaximum (size[0]-15-175)
                        null height -15
                        label ('{color=#ecc88a}_____________________________________') align (0.5, 0.5)
                        hbox:
                            align (0.5, 0.5)
                            xfill True
                            frame:
                                xpos 0
                                yalign 0.5
                                background Frame("content/gfx/frame/frame_it2.png", 5, 5)
                                xysize (130, 130)
                                add (ProportionalScale(item.icon, 110, 110)) align(0.5, 0.5)
                            frame:
                                background Frame("content/gfx/frame/p_frame4.png", 10, 10)
                                xysize (205, 130)
                                vbox:
                                    style_group "stats"
                                    spacing -7
                                    xfill True
                                    null height 15
                                    frame:
                                        xsize 195
                                        text ('Price:') color gold yalign 0.5
                                        label ('{size=-3}{color=[gold]}[item.price]') align (1.0, 0.5)
                                    frame:
                                        xsize 195
                                        text ('Slot:') color ivory yalign 0.5
                                        label ('{size=-3}%s'%item.slot.capitalize()) align (1.0, 0.5)
                                    frame:
                                        xsize 195
                                        text ('Type:') color ivory yalign 0.5
                                        label ('{size=-3}%s'%item.type.capitalize()) xalign 1.0 align (1.0, 0.5)
                                    frame:
                                        xsize 195
                                        text ('Sex:') color ivory yalign 0.5
                                        if item.slot in ["gift", "resources", "loot"]:
                                            label "{size=-3}N/A" xalign 1.0 align (1.0, 0.5)
                                        elif item.type == "food" and item.sex == 'unisex':
                                            label "{size=-3}N/A" xalign 1.0 align (1.0, 0.5)
                                        elif item.sex == 'male':
                                            label ('{size=-3}{color=#FFA54F}%s'%item.sex.capitalize()) xalign 1.0 align (1.0, 0.5)
                                        elif item.sex == 'female':
                                            label ('{size=-3}{color=#FFAEB9}%s'%item.sex.capitalize()) xalign 1.0 align (1.0, 0.5)
                                        elif item.sex == 'unisex':
                                            label ('{size=-3}%s'%item.sex.capitalize()) xalign 1.0 align (1.0, 0.5)
                            frame:
                                xysize (165, 130)
                                background Frame("content/gfx/frame/p_frame7.png", 5, 5)
                                has viewport scrollbars "vertical" mousewheel True style_group "proper_stats" xysize (165, 125) child_size 160, 500
                                vbox:
                                    spacing 1
                                    if item.mod:
                                        label ('Stats:') text_size 18 text_color gold xpos 10
                                        for stat, value in item.mod.items():
                                            frame:
                                                xysize 140, 20
                                                text stat.capitalize() color ivory size 16 align (0.02, 0.5)
                                                label (u'{size=-4}[value]') align (0.98, 0.5)
                                        null height 2
                                    if item.max:
                                        label ('Max:') text_size 18 text_color gold xpos 10
                                        for stat, value in item.max.items():
                                            frame:
                                                xysize 140, 20
                                                text stat.capitalize() color ivory size 16 align (0.02, 0.5)
                                                label u'{size=-4}[value]' align (0.98, 0.5)
                                        null height 2
                                    if item.min:
                                        label ('Min:') text_size 18 text_color gold xpos 10
                                        for stat, value in item.min.items():
                                            frame:
                                                xysize 140, 20
                                                text stat.capitalize() color ivory size 16 align (0.02, 0.5)
                                                label (u'{size=-4}%d'%value) align (0.98, 0.5)
                                        null height 2
                                    if item.addtraits:
                                        label ('Adds Traits:') text_size 16 text_color gold xpos 10
                                        for trait in item.addtraits:
                                            frame:
                                                xysize 140, 20
                                                text(u'%s'%trait.capitalize()) color ivory size 16 align (0.5, 0.5)
                                        null height 2
                                    if item.removetraits:
                                        label ('Removes Traits:') text_size 16 text_color gold xpos 10
                                        for trait in item.removetraits:
                                            frame:
                                                xysize 140, 20
                                                text(u'%s'%trait.capitalize()) color ivory size 16 align (0.5, 0.5)
                                        null height 2
                                    if item.add_be_spells:
                                        label ('Adds Skills:') text_size 16 text_color gold xpos 10
                                        for skill in item.add_be_spells:
                                            frame:
                                                xysize 140, 20
                                                text(u'%s'%skill.capitalize()) color ivory size 16 align (0.5, 0.5)
                                        null height 2
                                    if item.remove_be_spells:
                                        label ('Removes Skills:') text_size 16 text_color gold xpos 10
                                        for skill in item.remove_be_spells:
                                            frame:
                                                xysize 140, 20
                                                text (u'%s'%skill.capitalize()) color ivory size 16 align (0.5, 0.5)
                                        null height 2
                                    if item.addeffects:
                                        label ('Adds Effects:') text_size 16 text_color gold xpos 10
                                        for effect in item.addeffects:
                                            frame:
                                                xysize 140, 20
                                                text(u'%s'%effect.capitalize()) color ivory size 16 align (0.5, 0.5)
                                        null height 2
                                    if item.removeeffects:
                                        label ('Removes Effects:') text_size 16 text_color gold xpos 10
                                        for effect in item.removeeffects:
                                            frame:
                                                xysize 140, 20
                                                text(u'%s'%effect.capitalize()) color ivory size 16 align (0.5, 0.5)
                                                
                        null height -15
                        label ('{color=#ecc88a}_____________________________________') align (0.5, 0.5)
                        frame:
                            xalign .5
                            background Frame("content/gfx/frame/p_frame7.png", 10, 10)
                            has viewport mousewheel True xysize (460, 120)
                            text '[item.desc]' style "TisaOTM" size 16 color gold
                                    
    # Equipment slot frame (of an item)
    screen equipment_slot(pos=(0.5, 0.5), name="", img=None, value=None):
        frame:
            style_group "content"
            background Frame("content/gfx/frame/textbox_15.png", 5, 5)
            pos pos
            anchor (0.5, 0.5)
            yanchor 0.5
            xysize (90, 90)
            text (name) align(0.5, 0.0) size 18 color ivory
            imagebutton:
                align(0.5, 1.0)
                idle im.Scale(img, 70, 70)
                hover (im.MatrixColor(im.Scale(img, 70, 70), im.matrix.brightness(0.15)))
                action Return(value)
    
    # Inventory paging
    screen paging(path="content/gfx/interface/buttons/", use_filter=True, ref=None, xysize=(270, 60), root=None, align=(0.5, 0.0)):
        frame:
            if global_flags.flag("hero_equip"):
                background Frame("content/gfx/frame/BG_choicebuttons.png", 10, 10)
                ypadding 2
            else:
                background Frame("content/gfx/frame/frame_bg.png", 5, 5)
                ypadding 15
            style_group "content"
            xpadding 15
            xysize xysize
            align align
            vbox:
                align (0.5, 0.5)
                # Filter
                if use_filter:
                    hbox:
                        xmaximum xysize[0] - 15
                        xfill True
                        xalign 0.5
                        $ img = "".join([path, 'prev.png'])
                        imagebutton:
                            align (0.0, 0.5)
                            idle img
                            hover im.MatrixColor(img, im.matrix.brightness(0.15))
                            action Function(ref.apply_filter, "prev")
                        label ("%s " % (ref.filter).capitalize()) align (0.5, 0.5)  text_color ivory
                        imagebutton:
                            align (1.0, 0.5)
                            idle (path+'next.png')
                            hover (im.MatrixColor(path+'next.png', im.matrix.brightness(0.15)))
                            action Function(ref.apply_filter, "next")
                # Listing
                hbox:
                    xalign 0.5
                    xmaximum xysize[0] - 5
                    xfill True
                    hbox:
                        align (0.0, 0.5)
                        imagebutton:
                            yalign 0.5
                            idle (path+'first.png')
                            hover (im.MatrixColor(path+'first.png', im.matrix.brightness(0.15)))
                            if root:
                                action Return([root, 'first_page'])
                            else:
                                action Function(ref.first)
                        imagebutton:
                            yalign 0.5
                            idle (path+'prev.png')
                            hover (im.MatrixColor(path+'prev.png', im.matrix.brightness(0.15)))
                            if root:
                                action Return([root, 'prev_page'])
                            else:
                                action Function(ref.prev)
                    label ("%d - %d"%(ref.page+1, ref.max_page+1)) align (0.5, 0.5) text_color ivory
                    hbox:
                        align (1.0, 0.5)
                        imagebutton:
                            yalign 0.5
                            idle (path+'next.png')
                            hover (im.MatrixColor(path+'next.png', im.matrix.brightness(0.15)))
                            if root:
                                action Return([root, 'next_page'])
                            else:    
                                action Function(ref.next)
                        imagebutton:
                            yalign 0.5
                            idle (path+'last.png')
                            hover (im.MatrixColor(path+'last.png', im.matrix.brightness(0.15)))
                            if root:
                                action Return([root, 'last_page'])
                            else:    
                                action Function(ref.last)
                        
    screen shop_inventory(ref=None, x=0.0):
        key "mousedown_4" action ref.inventory.next
        key "mousedown_5" action ref.inventory.prev
        frame at fade_in_out(t1=0.5, t2=0.5):
            style_group "content"
            background Frame(Transform("content/gfx/frame/mes11.jpg", alpha=0.5), 5, 5)
            xalign x
            yfill True
            has vbox
            
            use paging(ref=ref.inventory, xysize=(260, 90))
            
            null height 5
            
            hbox:
                xalign 0.5
                add im.Scale("content/gfx/interface/icons/gold.png", 25, 25) align (0.0, 0.5)
                null width 10
                text u'[ref.gold]' align (0.5, 1.0) color gold size 23
                
            null height 5
            
            if isinstance(ref, ItemShop):
                label "[ref.name]" text_color ivory xalign 0.5
            elif isinstance(ref, PytCharacter):
                label "[ref.nickname]" text_color ivory xalign 0.5
            else:
                label "Inventory" text_color ivory xalign 0.5
                
            null height 5
            
            use items_inv(char=ref, main_size=(268, 522), frame_size=(85, 85), return_value=["item", ref])
            
init: # PyTFall:
    screen r_lightbutton:
        default align = (0, 0)
        imagebutton:
            align align
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
            action Return(return_value)
    
    screen rg_lightbutton:
        default align = (0, 0)
        frame:
            background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
            imagebutton:
                align align
                idle (img)
                hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
                action Return(return_value)
    
    screen rtt_lightbutton:
        imagebutton yalign 0.5:
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
            action Return(return_value)
            hovered tt.action(u"%s"%tooltip)

    python:
        def get_screens(*args):
            """
            Simple checks for active screens.
            Returns True if at least one of the screens is shown and False if not.
            """
            for scr in args:
                if renpy.get_screen(scr):
                    return True
            return False
            
    screen top_stripe(show_return_button=True, use_hide_transform=False, normal_op=True):
        default tt = Tooltip("")
        if not normal_op:
            mousearea:
                pos(0, 0)
                xysize(config.screen_width, 43)
                hovered SetField(pytfall, "city_dropdown", True)
                unhovered SetField(pytfall, "city_dropdown", False)
    
        # Hotkeys:
        if show_return_button and not get_screens("girl_interactions", "building_management_leftframe_upgrades_mode"):
            key "mousedown_3" action Return(['control', 'return'])
        if renpy.current_screen().tag not in ["girl_interactions", "hero_profile", "quest_log"]:
            if global_flags.flag("visited_arena"):
                key "a" action [Function(hs), Jump("arena_inside")]
            if global_flags.flag("visited_city_beach"):
                key "c" action [Function(hs), Function(global_flags.del_flag, "keep_playing_music"), Jump("city_beach_cafe")]
            key "g" action [Function(hs), Function(global_flags.del_flag, "keep_playing_music"), Jump("general_store")] 
            key "m" action [Function(hs), Function(global_flags.del_flag, "keep_playing_music"), Jump("mainscreen")]
            key "j" action ShowMenu("quest_log")
          
        # Top Stripe:
        showif normal_op or pytfall.city_dropdown:
            # Mainframe:
            add "content/gfx/frame/top_stripe.png":
                pos (0, 0)
                if use_hide_transform:
                    at auto_slide()
                    
        # Screen frame, always visible:            
        if show_return_button:
            add "content/gfx/frame/h3.png"
        else:
            add "content/gfx/frame/h2.png"
         
        # All buttons:
        showif normal_op or pytfall.city_dropdown:
            fixed:
                if use_hide_transform:
                    at auto_slide()
                xysize(config.screen_width, 43)
                pos (0, 0)
                hbox:
                    style_group "content"
                    align(0.023, 0.5)
                    null width 10 
                    add "coin_top" yalign 0.5
                    null width 5
                    text (u"%d"%int(hero.gold)) size 20 color gold yalign 0.5
                    null width 15
                    text (u'Day [day]') size 20 color ivory yalign 0.5
                    null width 15
                    button:
                        style "sound_button"
                        xysize (37, 37)
                        action [SelectedIf(not (_preferences.mute["music"] or _preferences.mute["sfx"])),
                                    If(_preferences.mute["music"] or _preferences.mute["sfx"],
                                    true=[Preference("sound mute", "disable"), Preference("music mute", "disable")],
                                    false=[Preference("sound mute", "enable"), Preference("music mute", "enable")])]
                            
                # Left HBox:
                hbox:
                    align(0.3, 0.5)
                    
                    if renpy.get_screen("char_profile") and char not in pytfall.ra:
                        if char in hero.team:
                            imagebutton:
                                idle im.Scale("content/gfx/interface/buttons/RG.png" , 36, 40)
                                hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/RG.png", 36, 40), im.matrix.brightness(0.25))
                                action Function(hero.team.remove, char)
                                hovered tt.Action("Remove [char.nickname] from player team!")
                        else:
                            imagebutton:
                                idle im.Scale("content/gfx/interface/buttons/AG.png" , 36, 40)
                                hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/AG.png", 36, 40), im.matrix.brightness(0.25))
                                action Function(hero.team.add, char)
                                hovered tt.Action("Add [char.nickname] to player team!")
                  
                # Girlslist paging buttons:
                if renpy.current_screen().tag == "girlslist":
                    hbox:
                        style_group "basic"
                        align(0.3, 0.5)
                        spacing 3
                        
                        $ gs = renpy.get_screen("girlslist").scope["_kwargs"]
                        
                        textbutton "<--":
                            action SensitiveIf(gs["page"] > 0), Show("girlslist", source=gs["source"], page=gs["page"] - 1, total_pages=gs["total_pages"])
                        $ page_2_display = gs["page"] + 1
                        textbutton "[page_2_display]":
                            action NullAction()
                        textbutton "-->":
                            action SensitiveIf(gs["page"] + 1 < gs["total_pages"]), Show("girlslist", source=gs["source"], page=gs["page"] + 1, total_pages=gs["total_pages"])
                    
                # AP Frame/Next Day button:
                if any([renpy.current_screen().tag == "next_day", hero.AP == 0]) and renpy.current_screen().tag not in ["mainscreen", "girl_interactions"]:
                    button:
                        style_group "basic"
                        align (0.5, 0.6)
                        action (hs, Function(global_flags.set_flag, "nd_music_play"), Hide("hero_equip"), Jump("next_day"))
                        text "Next Day"
                else:
                    add ProportionalScale("content/gfx/frame/frame_ap.png", 170, 50) align (0.5, 0.7)
                    label "[hero.AP]" align (0.53, 0.6) style "content_label"  text_size 23 text_color ivory text_bold True
                    
                # Right HBox:    
                hbox:
                    align(0.8, 0.5)
                    spacing 5
                    
                    if config.developer:
                        textbutton "{size=20}{color=[ivory]}{b}F":
                            action Jump("fonts")
                            hovered tt.Action("View availible Fonts!")
                            
                    if renpy.current_screen().tag not in ["quest_log"]:
                        imagebutton:
                            idle im.Scale("content/gfx/interface/buttons/journal1.png", 36, 40)
                            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/journal1.png", 36, 40), im.matrix.brightness(0.25))
                            hovered tt.Action("Quest Journal!")
                            action ShowMenu("quest_log")
                            
                    if renpy.current_screen().tag == "mainscreen":
                        imagebutton:
                            idle im.Scale("content/gfx/interface/buttons/preference.png", 39, 40)
                            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/preference.png", 39, 40), im.matrix.brightness(0.25))
                            action Show("s_menu", transition=dissolve)
                            hovered tt.Action("Game Preferences!")
                            
                    if renpy.current_screen().tag not in ["mainscreen", "girl_interactions", "quest_log"]:
                        imagebutton:
                            idle im.Scale("content/gfx/interface/buttons/MS.png" , 38, 37)
                            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/MS.png" , 38, 37), im.matrix.brightness(0.25))
                            action (Hide(renpy.current_screen().tag), Function(global_flags.del_flag, "keep_playing_music"),  Jump("mainscreen"))
                            hovered tt.Action("Return to Main Screen!")
                            
                    if renpy.current_screen().tag in ["char_profile", "char_equip"] and char.action != "Exploring":
                        imagebutton:
                            idle im.Scale("content/gfx/interface/buttons/IT2.png" , 34, 37)
                            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/IT2.png" , 34, 37), im.matrix.brightness(0.25))
                            action Return(["jump", "item_transfer"])
                            hovered tt.Action("Transfer items between MC and and [char.nickname]!")
                            
                    if renpy.get_screen("hero_profile") and hero.location == ap:
                        imagebutton:
                            idle im.Scale("content/gfx/interface/buttons/IT2.png" , 34, 37)
                            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/IT2.png" , 34, 37), im.matrix.brightness(0.25))
                            action Return(["item", "transfer"])
                            hovered tt.Action("Leave your crap at your place (Inside of a safe chest)!")
                    
                    if renpy.current_screen().tag not in ["hero_profile", "girl_interactions", "quest_log"]:
                        imagebutton:
                            idle im.Scale("content/gfx/interface/buttons/profile.png", 35, 40)
                            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/profile.png", 35, 40), im.matrix.brightness(0.25))
                            action [SetField(pytfall.hp, "came_from", last_label), Hide(renpy.current_screen().tag), Jump("hero_profile")]
                            hovered tt.Action("View Hero Profile!")
                        
                    null width 10    
                    
                    imagebutton:
                            idle im.Scale("content/gfx/interface/buttons/save.png" , 40, 40)
                            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/save.png" , 40, 40), im.matrix.brightness(0.25))
                            hovered tt.Action("QuickSave!")
                            action QuickSave()
                            
                    imagebutton:
                        idle im.Scale("content/gfx/interface/buttons/load.png" , 38, 40)
                        hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/load.png" , 38, 40), im.matrix.brightness(0.25))
                        hovered tt.Action("QuickLoad!")
                        action QuickLoad()
    
                if show_return_button:
                    imagebutton:
                        align(0.993, 0.5)
                        idle im.Scale("content/gfx/interface/buttons/close.png", 35, 35)
                        hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/close.png", 35, 35), im.matrix.brightness(0.25))
                        action Return(['control', 'return'])
                        hovered tt.Action("Return to previous screen!")
                    
                    
    screen message_screen(msg, size=(500, 300), use_return=False):
        modal True
        zorder 10
        
        fixed:
            align(0.5, 0.5)
            xysize(size[0], size[1])
            xfill True
            yfill True
            
            add im.Scale("content/gfx/frame/frame_bg.png", size[0], size[1])
            
            vbox:
                spacing 30
                align(0.5, 0.5)
                vbox:
                    xmaximum (size[0] - 50) 
                    text msg xalign 0.5
                textbutton "Ok" action If(use_return, true=Return(), false=Hide("message_screen")) minimum(250, 30) xalign 0.5 style "yesno_button"
        
    screen display_disposition(tag, d, size, x, y, t):
        tag tag
        text "[d]" font "fonts/rubius.ttf" size size color crimson at found_cash(x, y, t)
        timer t+0.2 action Hide("display_disposition")
        
    screen pyt_input(default="", text="", length=20, size=(350, 150)):
        modal True
        zorder 10
    
        fixed:
            align(0.5, 0.5)
            minimum(size[0], size[1])
            maximum(size[0], size[1])
            xfill True
            yfill True
            
            add im.Scale("content/gfx/frame/frame_bg.png", size[0], size[1])
            
            vbox:
                spacing 30
                align(0.5, 0.5)
                text text xalign 0.5
                input default default length length xalign 0.5
                
    screen exit_button(size=(35, 35), align=(1.0, 0.0)):
        $ img = im.Scale("content/gfx/interface/buttons/close.png" , size[0], size[1])
        imagebutton:
            align(align[0], align[1])
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(0.25))
            action Return(['control', 'return'])
            
    screen set_action_dropdown(char, pos=()):
        # Trying to create a drop down screen with choices of actions:
        zorder 3
        modal True
        
        key "mousedown_4" action NullAction()
        key "mousedown_5" action NullAction()
        
        # Get mouse coords:
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
                if isinstance(char.location, NewStyleUpgradableBuilding):
                    # Jobs:
                    $ jobs = char.location.get_valid_jobs(char)
                    for i in jobs:
                        textbutton "[i.id]":
                            # Without Equipping for the job!
                            action [Function(set_char_to_work, char, char.location, i), Hide("set_action_dropdown")]
                            
                # Buildings:
                # TODO: This needs to be rewritten:
                elif isinstance(char.location, Building):
                    for entry in Building.ACTIONS:
                        if entry == 'Stripper':
                            if char.location.upgrades['stripclub']['1']['active']:
                                textbutton "[entry]":
                                    action [SetField(char, "action", entry), Function(equip_for, char, entry), Hide("set_action_dropdown")]
                        elif entry == 'Guard':
                            if char.status != 'slave' and ("Warrior" in char.occupations or char.disposition <= 950): # The not inversion here seems wrong, so I removed it -Thewlis
                                textbutton "[entry]":
                                    action [SetField(char, "action", entry), Function(equip_for, char, entry), Hide("set_action_dropdown")]
                        else:
                            textbutton "[entry]":
                                action [SetField(char, "action", entry), Function(equip_for, char, entry), Hide("set_action_dropdown")]
                
                # Fighters Guild
                elif isinstance(char.location, FighterGuild):
                    for entry in FighterGuild.ACTIONS:
                        if entry == 'Training':
                            if char.status != "slave":
                                textbutton "[entry]":
                                    action [SetField(char, "action", entry), Function(equip_for, char, entry), Hide("set_action_dropdown")]
                        elif entry == 'ServiceGirl':
                            if (char.status == "slave" or "Server" in char.occupations) and not list(g for g in fg.get_chars() if g.action == "ServiceGirl"):
                                textbutton "[entry]":
                                    action [SetField(char, "action", entry), Function(equip_for, char, entry), Hide("set_action_dropdown")]
                        elif entry == 'BarGirl':
                            if fg.upgrades["bar"][0] and (char.status == "slave" or "Server" in char.occupations) and not list(g for g in fg.get_chars() if g.action == "BarGirl"):
                                textbutton "[entry]":
                                    action [SetField(char, "action", entry), Function(equip_for, char, "ServiceGirl"), Hide("set_action_dropdown")]
                        elif entry == 'Rest':
                            textbutton "[entry]":
                                action [SetField(char, "action", entry), Function(equip_for, char, entry), Hide("set_action_dropdown")]
                        else:
                            textbutton "[entry]":
                                action [SetField(char, "action", entry), Function(equip_for, char, entry), Hide("set_action_dropdown")]
                
                # Other buildings
                elif hasattr(char.location, "actions"):
                    for entry in char.location.actions:
                        if entry == "Guard":
                            if char.status != "slave" and ("Warrior" in char.occupations or char.disposition <= 950):
                                textbutton "[entry]":
                                    action [SetField(char, "action", entry), Function(equip_for, char, entry), Hide("set_action_dropdown")]
                        
                        elif entry == "Take Course":
                            textbutton "[entry]":
                                action [Hide("set_action_dropdown"), Hide("charslist"), Hide("char_profile"), # Hide the dropdown screen, the chars list and char profile screens
                                        SetField(store, "char", char, True), # Ensure that the global var char is set to the current char
                                        Jump("char_training")] # Jump to the training screen
                        
                        else:
                            textbutton "[entry]":
                                    action [SetField(char, "action", entry), Function(equip_for, char, entry), If(char_is_training(char), true=Function(stop_training, char)), Hide("set_action_dropdown")]
                
                # Prevent none action in schools
                if not hasattr(char.location, "is_school") or not char.location.is_school:
                    textbutton "None":
                        action [SetField(char, "action", None), If(char_is_training(char), true=Function(stop_training, char)), Hide("set_action_dropdown")]
                
                textbutton "Rest":
                    # TODO: Temporary way to set action to Rest, this needs to be rewritten completely.
                    action [SetField(char, "action", Rest()), Hide("set_action_dropdown")]
                        
                textbutton "Close":
                    action [Hide("set_action_dropdown")]
                
    screen set_location_dropdown(char, pos=()):
        # Trying to create a drop down screen with choices of buildings:
        zorder 3
        modal True
        
        key "mousedown_4" action NullAction()
        key "mousedown_5" action NullAction()
        
        # Get mouse coords:
        python:
            x, y = pos
            if x > config.screen_width/2:
                xval = 1.0
            else:
                xval = 0.0
            if y > config.screen_height/2:
                yval = 1.0
            else:
                yval = 0.0
        frame:
            style_group "dropdown_gm"
            pos (x, y)
            anchor (xval, yval)
            
            vbox:
                # Updating to new code: *Ugly code atm, TODO: Fix IT!
                for building in hero.buildings:
                    if isinstance(building, NewStyleUpgradableBuilding):
                        if char.action in building.jobs:
                            $ can_keep_action = True
                        else:
                            $ can_keep_action = False
                        if can_keep_action:
                            textbutton "[building.name]":
                                action [SelectedIf(char.location==building), If(char_is_training(char), true=Function(stop_training, char)), Function(change_location, char, building), Hide("set_location_dropdown")]
                        else:
                            textbutton "[building.name]":
                                action [SelectedIf(char.location==building), SetField(char, "action", None), If(char_is_training(char), true=Function(stop_training, char)), Function(change_location, char, building), Hide("set_location_dropdown")]
                    elif building.free_rooms():
                        $ can_keep_action = False
                        if isinstance(building, Building):
                            if char.action in Building.ACTIONS:
                                $ can_keep_action = True
                        elif isinstance(building, FighterGuild):
                            if char.action in FighterGuild.ACTIONS:
                                $ can_keep_action = True
                        elif hasattr(building, "actions"):
                            if char.action in building.actions:
                                $ can_keep_action = True
                        if can_keep_action:
                            textbutton "[building.name]":
                                action [SelectedIf(char.location==building), If(char_is_training(char), true=Function(stop_training, char)), Function(change_location, char, building), Hide("set_location_dropdown")]
                        else:
                            textbutton "[building.name]":
                                action [SelectedIf(char.location==building), SetField(char, "action", None), If(char_is_training(char), true=Function(stop_training, char)), Function(change_location, char, building), Hide("set_location_dropdown")]
                
                textbutton "Home":
                    action [If(char_is_training(char), true=Function(stop_training, char)), Function(change_location, char, char.home), Hide("set_location_dropdown")]
                
                textbutton "Close":
                    action Hide("set_location_dropdown")
                    
    screen set_home_dropdown(char, pos=()):
        # Trying to create a drop down screen with choices of buildings:
        zorder 3
        modal True
        
        key "mousedown_4" action NullAction()
        key "mousedown_5" action NullAction()
        
        # Get mouse coords:
        python:
            x, y = pos
            if x > config.screen_width/2:
                xval = 1.0
            else:
                xval = 0.0
            if y > config.screen_height/2:
                yval = 1.0
            else:
                yval = 0.0
        frame:
            style_group "dropdown_gm"
            pos (x, y)
            anchor (xval, yval)
            has vbox
            
            for building in hero.buildings:
                if isinstance(building, NewStyleUpgradableBuilding) and building.habitable:
                    textbutton "[building.name]":
                        action SelectedIf(char.home==building), SetField(char, "home", building), Hide("set_home_dropdown")
            textbutton "Streets":
                action SetField(char, "home", locations["Streets"]), Hide("set_home_dropdown")
            textbutton "Close":
                action Hide("set_home_dropdown")
        
    screen char_rename(char=None):
        modal True
        zorder 1
        
        vbox:
            style_group "basic"
            at fade_in_out()
            align (0.5, 0.5)
            spacing 10
            if isinstance(char, Player) or char.status == "slave":
                textbutton "Name: [char.name]":
                    action Return(["rename", "name"])
            textbutton "Nick: [char.nickname]":
                action Return(["rename", "nick"])
            if isinstance(char, Player) or char.status == "slave":
                textbutton "Full: [char.fullname]":
                    action Return(["rename", "full"])
                
            null height 20
            
            textbutton "Back":
                action Hide("char_rename")
                
    screen poly_matrix(in_file, show_exit_button=False):
        # If a tuple with coordinates is provided instead of False for show_exit_button, exit button will be placed there.
        
        default tooltip = False
        
        on "hide":
            action SetField(config, "mouse", None), Hide("show_poly_matrix_tt")
        
        python:
            with open(renpy.loader.transfn(in_file)) as f:
                matrix = json.load(f)
                
        $ func = renpy.curry(point_in_poly)
        for i in matrix:
            if "tooltip" in i:
                if "align" in i:
                    python:
                        align = tuple(i["align"])
                        pos = ()
                        anchor = ()
                else:
                    python:
                        align = ()
                        # Get a proper placement:
                        allx, ally = list(), list()
                        
                        for t in i["xy"]:
                            allx.append(t[0])
                            ally.append(t[1])
                            
                        maxx = max(allx)
                        maxy = max(ally)
                        minx = min(allx)
                        miny = min(ally)
                        
                        w, h = config.screen_width, config.screen_height
                        
                        side = i.get("place", "left")
                        
                        if side == "left":
                            pos = (minx - 10, sum(ally)/len(ally))
                            anchor = (1.0, 0.5)
                        elif side == "right":
                            pos = (maxx + 10, sum(ally)/len(ally))
                            anchor = (0.0, 0.5)
                        elif side == "bottom":
                            pos = (sum(allx)/len(allx), maxy + 10)
                            anchor = (0.5, 0.0)
                        elif side == "top":
                            pos = (sum(allx)/len(allx), miny - 10)
                            anchor = (0.5, 1.0)
            
                button:
                    background Null()
                    focus_mask func(i["xy"])
                    action Return(i["id"])      
                    hovered [SetField(config, "mouse", {"default": [("content/gfx/interface/icons/zoom_32x32.png", 0, 0)]}),
                                   Show("show_poly_matrix_tt", pos=pos, anchor=anchor, align=align, text=i["tooltip"]), With(dissolve)]
                    unhovered [SetField(config, "mouse", None),
                                       Hide("show_poly_matrix_tt"), With(dissolve)]
            else:
                button:
                    background Null()
                    focus_mask func(i["xy"])
                    action Return(i["id"])
                    hovered SetField(config, "mouse", {"default": [("content/gfx/interface/icons/zoom_32x32.png", 0, 0)]})
                    unhovered SetField(config, "mouse", None)
                
        if show_exit_button:
            textbutton "All Done":
                align show_exit_button
                action Return(False)
                
    screen show_poly_matrix_tt(pos=(), anchor=(), align=(), text=""):
        zorder 1
        frame:
            if align:
                align align
            if pos:
                pos pos
                anchor anchor
            text text
        
    ##############################################################################
    screen notify:
        zorder 500
        
        vbox:
            at fade_in_out(t1=0.25, t2=0.25)
            style_group "notify_bubble"
            
            frame:
                text message
        
        timer 1.5 action Hide("notify")
        
init: # Settings:
    screen s_menu(s_menu="Settings"):
        zorder 10**5 + 1
        modal True
        
        key "mousedown_3" action Hide("s_menu"), With(dissolve)
    
        # default s_menu = "Settings"
        
        add Transform("content/gfx/images/bg_gradient2.png", alpha=0.8)
        
        frame:
            # at fade_in_out(sv1=0.0, ev1=1.0, t1=0.7,
                                    # sv2=1.0, ev2=0.0, t2=0.5)
            background Frame (Transform("content/gfx/frame/framegp2.png", alpha=0.8), 10, 10)
            align (0.315, 0.5)
            xysize (690, 414)
            style_group "smenu"
            has hbox align (0.5, 0.5) xfill True
            
            if s_menu == "Settings":
                grid 3 1:
                    align (0.5, 0.5)
                    spacing 7
                    # Left column...
                    frame:
                        align (0.5, 0.5)
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.3), 10, 10)
                        xpadding 10
                        ypadding 10
                        has vbox spacing 5
                        # frame:
                            # background Frame(Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            # xsize 194
                            # ypadding 8
                            # style_group "dropdown_gm2"
                            # has vbox align (0.5, 0.5)
                            
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame(Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
                                text _("- Display -") style "TisaOTMolxm"
                            textbutton _("Window") action Preference("display", "window") xsize 150 xalign 0.5 text_size 16
                            textbutton _("Fullscreen") action Preference("display", "fullscreen") xsize 150 xalign 0.5 text_size 16
                                
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
                                text _("- Transitions -") style "TisaOTMolxm"
                            textbutton _("All") action Preference("transitions", "all") xsize 150 xalign 0.5 text_size 16
                            textbutton _("None") action Preference("transitions", "none") xsize 150 xalign 0.5 text_size 16
                            
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 10
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
                                text _("- Text Speed -") style "TisaOTMolxm"
                            null height 8
                            bar value Preference("text speed") align (0.5, 0.5)
                            
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            textbutton _("Joystick...") action Preference("joystick") xsize 150 text_size 16
                                
                    # Middle column...
                    frame:
                        align (0.5, 0.5)
                        background Frame (Transform("content/gfx/frame/ink_box.png", alpha=0.3), 10, 10)
                        xpadding 10
                        ypadding 10
                        has vbox spacing 5
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
                                text _("- Skip -") style "TisaOTMolxm"
                            textbutton _("Seen Messages") action Preference("skip", "seen") xsize 150 xalign 0.5 text_size 16
                            textbutton _("All Messages") action Preference("skip", "all") xsize 150 xalign 0.5 text_size 16
                            
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
                                text _("- After Choices -") style "TisaOTMolxm"
                            textbutton _("Stop Skipping") action Preference("after choices", "stop") xsize 150 xalign 0.5 text_size 16
                            textbutton _("Keep Skipping") action Preference("after choices", "skip") xsize 150 xalign 0.5 text_size 16
                            
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 10
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
                                text _("- A-Forward Time -") style "TisaOTMolxm"
                            null height 8
                            bar value Preference("auto-forward time") align (0.5, 0.5)
                            if config.has_voice:
                                textbutton _("Wait for Voice") action Preference("wait for voice", "toggle") xsize 150 xalign 0.5 text_size 16
                                
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            textbutton _("Begin Skipping") action Skip() xsize 150 text_size 16
                                    
                    # Right column...
                    frame:
                        align (0.5, 0.5)
                        background Frame (Transform("content/gfx/frame/ink_box.png", alpha=0.3), 10, 10)
                        xpadding 10
                        ypadding 10
                        has vbox spacing 5
                        
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 8
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
                                text _("- Mute -") style "TisaOTMolxm"
                            textbutton "Music" action Preference("music mute", "toggle") xsize 150 xalign 0.5 text_size 16
                            textbutton "Sound" action Preference("sound mute", "toggle") xsize 150 xalign 0.5 text_size 16
                            
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 10
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
                                text _("- Music Volume -") align (0.5, 0.0) style "TisaOTMolxm"
                            null height 8
                            bar value Preference("music volume") align (0.5, 0.5)
                            
                        frame:
                            background Frame (Transform("content/gfx/frame/settings1.png", alpha=0.9), 10, 10)
                            xsize 194
                            ypadding 10
                            style_group "dropdown_gm2"
                            has vbox align (0.5, 0.5)
                            frame:
                                xsize 184
                                align (0.5, 0.5)
                                background Frame (Transform("content/gfx/frame/stat_box.png", alpha=0.9), 10, 10)
                                text _("- Sound Volume -") style "TisaOTMolxm"
                            null height 8
                            bar value Preference("sound volume") align (0.5, 0.5)
                            if config.sample_sound:
                                textbutton _("Test"):
                                    action Play("sound", config.sample_sound)
                                    style "soundtest_button"

            elif s_menu in ("Save", "Load"):
                vbox:
                    yfill True
                    xfill True
                    spacing 5
                    null height 5
                    hbox:
                        spacing 3
                        style_group "dropdown_gm2"
                        align (0.5, 0.5)
                        textbutton _("Previous") action FilePagePrevious(), With(dissolve) text_size 16
                        textbutton _("Auto") action FilePage("auto"), With(dissolve) text_size 16
                        textbutton _("Quick") action FilePage("quick"), With(dissolve) text_size 16
                        for i in range(1, 9):
                            textbutton str(i):
                                action FilePage(i), With(dissolve)
                        textbutton _("Next") action FilePageNext(), With(dissolve) text_size 16
                    $ columns = 2
                    $ rows = 3
                    grid columns rows:
                        transpose True
                        style_group "dropdown_gm2"
                        xfill True
                        yfill True
                        spacing -10
                        for i in range(1, columns * rows + 1):
            
                            $ file_name = FileSlotName(i, columns * rows)
                            $ file_time = FileTime(i, empty=_("Empty Slot"))
                            # $ file_time = "0"
                            $ json_info = FileJson(i, empty= _(""))
                            $ save_name = FileSaveName(i)
            
                            hbox:
                                align (0.5, 0.5)
                                if "portrait" in json_info:
                                    frame:
                                        background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                                        align (0.5, 0.5)
                                        add ProportionalScale(json_info["portrait"], 90, 90) align (0.5, 0.5)
                                else:
                                    frame:
                                        background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                                        align (0.5, 0.5)
                                        xysize (102, 102)
                                button:
                                    style "smenu2_button"
                                    align (0.5, 0.5)
                                    xysize (220, 100)
                                    if s_menu == "Save":
                                        action FileSave(i)
                                        text " - [file_name] -" align (1.0, 0) style "TisaOTMol" size 14 outlines [(3, "#3a3a3a", 0, 0), (2, "#458B00", 0, 0), (1, "#3a3a3a", 0, 0)]
                                        text "[file_time!t]\n[save_name!t]" style "TisaOTMol" size 12 align (1.05, 1.25)
                                    elif s_menu == "Load":
                                        action FileLoad(i)
                                        text " - [file_name] -" align (1.0, 0) style "TisaOTMol" size 14 outlines [(3, "#3a3a3a", 0, 0),(2, "#009ACD", 0, 0), (1, "#3a3a3a", 0, 0)]
                                        text "[file_time!t]\n[save_name!t]" style "TisaOTMol" size 12 align (1.05, 1.25)
                                    vbox:
                                        xpos 0
                                        yalign 0.5
                                        spacing -7
                                        if "name" in json_info:
                                            text "[json_info[name]]" style "TisaOTMol" color gold size 17
                                        if "level" in json_info:
                                            text "Level: [json_info[level]]" style "TisaOTMol" ypos 0
                                        if "chars" in json_info:
                                            text "Chars: [json_info[chars]]" style "TisaOTMol" ypos 0
                                        if "gold" in json_info:
                                            text "Gold: [json_info[gold]]" style "TisaOTMol" ypos 0
                                        if "buildings" in json_info:
                                            text "Buildings: [json_info[buildings]]" style "TisaOTMol" ypos 0

                                    key "save_delete" action FileDelete(i)

        frame:
            # at fade_in_out(sv1=0.0, ev1=1.0, t1=1.0,
                                    # sv2=1.0, ev2=0.0, t2=1.0)
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
            align (0.765, 0.505)
            xysize (150, 409)
            style_group "smenu"
            xpadding 8
            has vbox spacing 5 align (0.5, 0.5)
            null height 3            
            vbox:
                xfill True
                spacing -10
                align (0.5, 0.5)
                text "-------------" style "TisaOTMol" size 20 align (0.5, 0.5)
                if s_menu == "Settings":
                    text "Settings" style "TisaOTMol" size 26 align (0.5, 0.5)
                elif s_menu == "Save":
                    text "Save" style "TisaOTMol" size 26 align (0.5, 0.5)
                elif s_menu == "Load":
                    text "Load" style "TisaOTMol" size 26 align (0.5, 0.5)
                text "----------" style "TisaOTMol" size 20 align (0.5, 0.5)
            button:
                yalign 0.5
                action Hide("s_menu"), With(dissolve)
                text "Return" size 18 align (0.5, 0.5) # style "mmenu_button_text"
            button:
                yalign 0.5
                action SelectedIf(s_menu == "Settings"), Hide("s_menu"), Show("s_menu", s_menu="Settings"), With(dissolve) # SetScreenVariable("s_menu", "Settings")
                text "Settings" size 18 align (0.5, 0.5) # style "mmenu_button_text"
            button:
                yalign 0.5
                action SensitiveIf(not main_menu), SelectedIf(s_menu == "Save"), Hide("s_menu"), Show("s_menu", s_menu="Save"), With(dissolve)#, SetScreenVariable("s_menu", "Save")
                text "Save" size 18 align (0.5, 0.5) # style "mmenu_button_text"
            button:
                yalign 0.5
                action SelectedIf(s_menu == "Load"), Hide("s_menu"), Show("s_menu", s_menu="Load"), With(dissolve)#, SetScreenVariable("s_menu", "Load")
                text "Load" size 18 align (0.5, 0.5) # style "mmenu_button_text"
            button:
                yalign 0.5
                action MainMenu()
                text "Main Menu" size 18 align (0.5, 0.5) #  style "mmenu_button_text"
            button:
                yalign 1.0
                action Quit()
                text "Quit" size 18 align (0.5, 0.5) # style "mmenu_button_text"
            null height 3
        
    
