label hero_profile:
    scene bg profile_1
    
    $ global_flags.set_flag("keep_playing_music")
    
    # $ pytfall.world_quests.run_quests("auto") Goes against squelching policy?
    $ pytfall.world_events.run_events("auto")
    $ renpy.retain_after_load()
    
    show screen pyt_hero_profile
    with dissolve
    
    $ hero.inventory.set_page_size(18)
    
    while 1:
        $ result = ui.interact()
        
        # To kill input error during team renaming:
        if not result:
            pass
        
        elif result[0] == 'control':
            if result[1] == 'return':
                $ pytfall.hp.show_item_info = False
                $ pytfall.hp.item = False
                hide screen pyt_hero_profile
                hide screen pyt_hero_equip
                
                # Reset filters (prevents crap from happening in shops):
                $ hero.inventory.male_filter = False
                $ hero.inventory.apply_filter('all')
                
                # Taking care of Ren'Pys annoying reserves... <-- Prolly obsolete after I rewrote the last label func.
                if pytfall.hp.came_from.startswith("_"):
                    jump mainscreen
                else:
                    jump expression pytfall.hp.came_from
                    
        elif result[0] == "dropdown":
            if result[1] == "loc":
                $ renpy.show_screen("set_location_dropdown", hero, pos=renpy.get_mouse_pos())
            elif result[1] == "home":
                $ renpy.show_screen("set_home_dropdown", hero, pos=renpy.get_mouse_pos())
                
        elif result[0] == 'hero':
            if result[1] == 'equip':
                if renpy.get_screen('pyt_hero_equip'):
                    hide screen pyt_hero_equip
                    $ pytfall.hp.show_item_info = False
                    $ pytfall.hp.item = False
                else:    
                    show screen pyt_hero_equip 
                    
            elif result[1] == 'first_page':
                $ hero.inventory.first()
            elif result[1] == 'last_page':
                $ hero.inventory.last()
            elif result[1] == 'next_page':
                $ hero.inventory.next()
            elif result[1] == 'prev_page':
                $ hero.inventory.prev()
            elif result[1] == 'prev_filter':
                $ hero.inventory.apply_filter('prev')
            elif result[1] == 'next_filter':
                $ hero.inventory.apply_filter('next')
            elif result[1] == 'male_filter':
                $ hero.inventory.male_filter = True
                $ hero.inventory.apply_filter('all')
            elif result[1] == 'unisex_filter':
                $ hero.inventory.male_filter = False
                $ hero.inventory.apply_filter('all')
            
        elif result[0] == 'item':
            if result[1] == 'get':
                $ pytfall.hp.show_item_info = True
                $ pytfall.hp.item = result[2]

            elif result[1] == 'equip':
                $ equip_item(pytfall.hp.item, hero)
                $ pytfall.hp.show_item_info = False
                $ pytfall.hp.item = False
                
            elif result[1] == "transfer":
                $ renpy.hide_screen("pyt_hero_profile")
                $ pytfall.it = GuiItemsTransfer("personal_transfer", char=ap, last_label=last_label)
                jump items_transfer
                
            elif result[1] == 'unequip':
                $ hero.unequip(pytfall.hp.item)
                $ pytfall.hp.show_item_info = False
                $ pytfall.hp.item = False

        elif result[0] == "remove_from_team":
            $ hero.team.remove(result[1])
            
        elif result[0] == "rename_team":
            if result[1] == "set_name":
                $ hero.team.name = renpy.call_screen("pyt_ht_input")
    
    
    # $ pytfall.hp.screen_loop()

    # hide screen pyt_hero_equip
    # hide screen pyt_hero_profile
    # jump mainscreen

# screen pyt_hero_dropdown_loc(pos=()):
    # # Trying to create a drop down screen with choices of buildings:
    # zorder 3
    # modal True
     
    # key "mousedown_4" action NullAction()
    # key "mousedown_5" action NullAction()
     
    # # Get mouse coords:
    # python:
        # x, y = pos
        # if x > 1000:
            # xval = 1.0
        # else:
            # xval = 0.0
        # if y > 500:
            # yval = 1.0
        # else:
            # yval = 0.0
    # frame:
        # style_group "dropdown"
        # pos (x, y)
        # anchor (xval, yval)
        # vbox:
            # for building in hero.buildings:
                # textbutton "[building.name]":
                    # action [SetField(hero, "location", building), Hide("pyt_hero_dropdown_loc")]
            # textbutton "None":
                # action [SetField(hero, "location", hero), Hide("pyt_hero_dropdown_loc")]
            # textbutton "Close":
                # action [Hide("pyt_hero_dropdown_loc")]

screen pyt_hero_profile():
    
    default tt = Tooltip("Welcome to MC profile screen!")
    
    #  Hero Sprite:
    add Transform(hero.show("battle_sprite", resize=(480, 480)), alpha=0.9) align(0.55, 0.53)
    
    # Battle Stats:
    fixed:
        align (0.08, 0.98)
        xysize (270, 270)
        add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                              (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 112, 126, 148, blue), alpha=0.4) align (0.5, 0.5)
        add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                              (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 65, 126, 148, blueviolet), alpha=0.3) align (0.5, 0.5)
        add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                              (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 33, 126, 148, aquamarine), alpha=0.2) align (0.5, 0.5)
        add ProportionalScale("content/gfx/interface/images/pentagon1.png", 250, 250) align (0.01, 0.5)
        
    text("{size=-5}{font=fonts/Rubius.ttf}{color=[red]}ATK [hero.attack]|%d"%(hero.get_max("attack"))) pos(178, 450)
    text("{size=-5}{font=fonts/Rubius.ttf}{color=#dc762c}DEF [hero.defence]|%d"%(hero.get_max("defence"))) pos(33, 518)
    text("{size=-5}{font=fonts/Rubius.ttf}{color=#1E90FF}AGI [hero.agility]|%d"%(hero.get_max("agility"))) pos(103, 698)
    text("{size=-5}{font=fonts/Rubius.ttf}{color=#00FA9A}LCK [hero.luck]|%d"%(hero.get_max("luck"))) pos(248, 698)
    text("{size=-5}{font=fonts/Rubius.ttf}{color=#8470FF}MAG [hero.magic]|%d"%(hero.get_max("magic"))) pos(308, 518)
    
    # Name:
    fixed:
        xalign 0.6
        ypos 45
        label (u"[hero.name]") style "content_label" text_size 26 text_color ivory xalign 0.54 ypos 5
            
    # Level and Exp:
    fixed:
        xalign 0.585
        ypos 80
        xysize (300, 90)
        style_group "content"
        add ProportionalScale("content/gfx/frame/level1.png", 300, 90) align(0.5, 0.5)
        label "[hero.level]" pos (45, 19) text_color ivory text_bold True text_size 17
        text "[hero.exp]" pos (160, 21) color ivory bold True size 18
        text "[hero.goal]" pos (160, 49) color ivory bold True size 18
    
    # Stats + Location:
    frame:
        align (0.0, 0.13)
        background (im.Scale("content/gfx/frame/stats_frame2.png", 245, 470))
        xysize (225, 470)
        has vbox
        vbox:
            xpos 5
            ypos 14
            hbox:
                $ stats = ["constitution", "charisma", "intelligence", "fame", "reputation", "libido"]
                vbox:
                    style_group "stats"
                    spacing -7
                    xanchor 2
                    xmaximum 113
                    frame:
                        xysize (215, 8)
                        text "{color=#CD4F39}Health:" xalign (0.02)
                    frame:
                        xysize (215, 8)
                        text "{color=#009ACD}MP:" size 16 xalign (0.02)
                    frame:
                        xysize (215, 8)
                        text "{color=#43CD80}Vitality:" xalign (0.02)
                    for stat in stats:
                        frame:
                            xysize (215, 8)
                            text ('{color=#79CDCD}%s'%stat.capitalize()) color ivory size 17 xalign (0.02) 
                vbox:
                    yalign (0.65)
                    spacing 8
                    xanchor 20
                    xfill True
                    xminimum 0
                    xmaximum 120
                    
                    if hero.health <= hero.get_max("health")*0.3:
                        text (u"{color=[red]}%s/%s"%(hero.health, hero.get_max("health"))) style "stats_value_text" xalign (1.0)
                    else:
                        text (u"%s/%s"%(hero.health, hero.get_max("health"))) style "stats_value_text" xalign (1.0)
    
                    if hero.mp <= hero.get_max("mp")*0.3:
                        text (u"{color=[red]}%s/%s"%(hero.mp, hero.get_max("mp"))) style "stats_value_text" xalign (1.0)
                    else:
                        text (u"%s/%s"%(hero.mp, hero.get_max("mp"))) style "stats_value_text" xalign (1.0)
    
                    if hero.vitality <= hero.get_max("vitality")*0.3:
                        text (u"{color=[red]}%s/%s"%(hero.vitality, hero.get_max("vitality"))) style "stats_value_text" xalign (1.0)
                    else:
                        text (u"%s/%s"%(hero.vitality, hero.get_max("vitality"))) style "stats_value_text" xalign (1.0)
    
                    for stat in stats:
                        text ('%d/%d'%(getattr(hero, stat), hero.get_max(stat))) style "stats_value_text" xalign (1.0)
                        
            null height 2
            
            # $ loc = hero.location if isinstance(hero.location, basestring) else hero.location.name
            button:
                style_group "ddlist"
                action Return(["dropdown", "loc"])
                alternate Return(["dropdown", "home"])
                text "{image=content/gfx/interface/icons/move15.png}Location:\n       [hero.location]":
                    if len(str(hero.location)) > 18:
                        size 15
                    else:
                        size 16
                hovered tt.Action("Change MCs Home/Location.")

    # Traits (Baseclasses for now):
    frame:
        align (1.0, 0.1)
        has vbox
        for t in hero.traits:
            textbutton "[t.id]" action NullAction() hovered tt.action(t.desc)
    
    # Buttons ------------------------------------>
    frame:
        background Frame("content/gfx/frame/p_frame3.png", 10, 10)
        style_group "basic"
        xsize 150
        xpadding 10
        ypadding 10
        pos (350, 545)
        has vbox
        textbutton "Show PT":
            xsize 150 # make sure buttons don't change size all the time :)
            action Show("pyt_hero_team")
            xfill True
            hovered tt.Action("Show [hero.team.name]!")
        textbutton 'Finances':
            hovered tt.Action("View your Finanaces.")
            xfill True
            action Show("pyt_hero_finances")
        textbutton 'Equipment':
            hovered tt.Action("Take a look at your inventory.")
            xfill True
            action Return(['hero', 'equip'])
                
    # Magic/Attacks  --------------------------->
    hbox:
        pos (915, 400)
        style_group "content"
        
        frame:
            background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 10, 10)
            xysize (160, 200)
            label (u"Attack:") text_size 20 text_color ivory text_bold True
            side "c r":
                align(0, 0.92)
                viewport id "heroprofile_attack_vp":
                    xysize (140, 150)
                    draggable True
                    mousewheel True
                    vbox:
                        spacing 1
                        for entry in hero.attack_skills:
                            button:
                                background Null()
                                xysize (130, 16)
                                action NullAction()
                                text "[entry.name]" size 17 idle_color ivory hover_color red
                                hovered tt.action(entry)
                                
                vbar value YScrollValue("heroprofile_attack_vp")
        
        frame:
            background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 10, 10)
            xysize (160, 200)
            label (u"Magic:") text_size 20 text_color ivory text_bold True
            side "c r":
                align(0, 0.92)
                viewport id "heroprofile_magic_vp":
                    xysize (140, 150)
                    draggable True
                    mousewheel True
                    vbox:
                        align(0, 0.2)
                        spacing 1
                        for entry in hero.magic_skills:
                            button:
                                background Null()
                                xysize (130, 16)
                                action NullAction()
                                text "[entry.name]" size 17 idle_color ivory hover_color red
                                hovered tt.action(entry)
                                
                vbar value YScrollValue("heroprofile_magic_vp")
    
    # Elemental alignment:
    if hasattr(hero, "element"):
        $ img = ProportionalScale("".join(["content/gfx/interface/images/elements/", hero.element.lower(), ".png"]), 120, 120)
        $ element = hero.element.split()[0]
        $ desc = pytfall.desc.elements[element.lower()]
        frame:
            style_group "content"
            background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 10, 10)
            xysize (305, 180)
            pos (926, 115)
            label "[element]" align(0.1, 0.1) text_color purple text_size 30 text_bold True
            imagebutton:
                at elements()
                xcenter 205
                ycenter 95
                idle (img)
                hover (img)
                hovered tt.Action(desc)
                action NullAction()
                                    
    # Equipment   -------------------------------------------------->
    showif not renpy.get_screen('pyt_hero_equip'):
        use pyt_eqdoll(active_mode=False, char=hero)
     

    # Tooltip text:  
    frame:
        background Frame("content/gfx/frame/frame_hor_stripe.png", 10, 10)
        align (0.99, 1.0)
        xysize (660, 115)
        has hbox spacing 1
        if isinstance(tt.value, BE_Action):
            $ element = tt.value.get_element()
            if element:
                fixed:
                    xysize (100, 100)
                    if element.icon:
                        $ img = ProportionalScale(element.icon, 90, 90)
                        add img align (0.5, 0.5)
            text tt.value.desc style "content_text" size 20 color ivory yalign 0.1
        else:
            text (u"{=content_text}{color=[ivory]}%s" % tt.value)  yalign 0.1 xalign 0.1
            
    use pyt_top_stripe(True)


screen pyt_hero_equip():
    modal True
    zorder 1
    default tt = Tooltip(None)
    # Useful keymappings (first time I try this in PyTFall):
    if pytfall.hp.show_unequip_button():
        key "mousedown_2" action Return(["item", "unequip"])
    elif pytfall.hp.show_equip_button():
        key "mousedown_2" action Return(["item", "equip"])
    else:
        key "mousedown_2" action NullAction()
        
    key "mousedown_4" action Return(["hero", "next_page"])
    key "mousedown_5" action Return(["hero", "prev_page"])
    
    # Doll...
    use pyt_eqdoll(char=hero)
    
    # Inventory ------------------------------------------------------------>
    vbox:
        at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)
        pos (394, 440)
        spacing 3
        hbox:
            spacing 52
            use paging(root='hero', ref=hero.inventory, use_filter=True)
            use items_inv(char=hero)
            
        # Buttons:    
        frame:
            background Frame("content/gfx/frame/p_frame3.png", 10, 10)
            style_group "basic"
            xpadding 10
            ypadding 10
            yanchor 60
            has hbox
            textbutton 'Close':
                hovered tt.Action("Take a look at your inventory.")
                action Return(['hero', 'equip'])
            if renpy.get_screen('pyt_hero_equip') and not hero.inventory.male_filter:
                textbutton "Male Filter":
                    hovered tt.Action("Filter out all items suitible for only girls.")
                    action Return(['hero', 'male_filter'])
            if renpy.get_screen('pyt_hero_equip') and hero.inventory.male_filter:
                textbutton "Unisex Filter":
                    hovered tt.Action("Show all items.")
                    action Return(['hero', 'unisex_filter'])
            if pytfall.hp.show_equip_button():
                textbutton "Equip":
                    hovered tt.Action("Equip this item.")
                    action Return(['item', 'equip'])
            if pytfall.hp.show_unequip_button():
                textbutton "Unequip":
                    hovered tt.Action("Unequip this item.")
                    action Return(['item', 'unequip'])  
                        
    # Item Info ------------------------------------------------------------------------>                    
    showif pytfall.hp.show_item_info:
        frame:
            at fade_in_out()
            xalign 0.986
            ypos 43
            background Frame("content/gfx/frame/frame_dec_1.png", 30, 30)
            xpadding 30
            ypadding 30
            xysize (555, 400)
            use itemstats(item=pytfall.hp.item, size=(580, 350), style_group="content", mc_mode=True)
    
            
screen pyt_ht_input():
    zorder 1
    modal True

    fixed:
        align(0.5, 0.5)
        xysize (350, 150)
        add im.Scale("content/gfx/frame/frame_bg.png", 350, 150)
        vbox:
            spacing 30
            align(0.5, 0.5)
            text "{color=[ivory]}Enter your team name:" xalign 0.5
            input default "Player Team" length 20 xalign 0.5

screen pyt_hero_team():
    zorder 1
    modal True
    
    default tt = Tooltip("Welcome to MC profile screen!")
    
    # Hero team ---------------------------------------------->
    frame:
        style_group "content"
        align (0.5, 0.5)
        background Frame(Transform(im.Twocolor("content/gfx/frame/ink_box.png", white, black), alpha=0.7), 10, 10)
        # xysize (400, 500)
        ypadding 20
        xpadding 20
        has vbox
        null height 5
        label ("[hero.team.name]") align(0.5, 0.02) text_size 30 text_color ivory
        null height 5
        vbox:
            # xysize (350, 450)
            spacing 10
            for member in hero.team:
                frame:
                    background Frame("content/gfx/frame/p_frame3.png", 10, 10)
                    xpadding 20
                    ypadding 10
                    has hbox
                    frame:
                        background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                        xysize (10, 10)
                        add (member.show("portrait", resize=(120, 120))) align (0.5, 0.5)
                    null width 10
                    vbox:
                        style_group "stats"
                        spacing 1
                        vbox:
                            text "HP:" color ivory style "stats_value_text"
                            bar:
                                value member.health
                                range member.get_max("health")
                                left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 110, 20), red, red)
                                right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 110, 20), red, red)
                                thumb None
                                maximum (110, 20)
                        vbox:
                            text "MP:" color ivory style "stats_value_text"
                            bar:
                                value member.mp
                                range member.get_max("mp")
                                left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 110, 20), green, green)
                                right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 110, 20), green, green)
                                thumb None
                                maximum (110, 20)
                        vbox:
                            text "Vitality:" color ivory style "stats_value_text"
                            bar:
                                value member.vitality
                                range member.get_max("vitality")
                                left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 110, 20), blue, blue)
                                right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 110, 20), blue, blue)
                                thumb None
                                maximum (110, 20)
                                
                    null width 25
                    vbox:
                        yalign 0.5
                        ysize 50
                        spacing 10
                        text "AP: [member.AP]" xalign 0.5 size 16 color ivory style "stats_value_text"
                        button:
                            style_group "basic"
                            xalign 0.5
                            if member == hero:
                                action Return(["rename_team", "set_name"])
                                hovered tt.Action("Rename Heroes team!")
                                text "RT"
                            else:
                                action Return(["remove_from_team", member])
                                hovered tt.Action("Remove %s for %s!"%(member.nickname, hero.team.name))
                                text "RM"
          
        null height 20
        button:
            style_group "basic"
            xalign 0.5
            action Hide("pyt_hero_team")
            text "Close"

screen pyt_hero_finances():
    modal True
    zorder 1
    
    frame at slide(so1=(0, 700), t1=0.7, so2=(0, 0), t2=0.3, eo2=(0, -config.screen_height)):
        background Frame (Transform("content/gfx/frame/arena_d.png", alpha=1.2), 5, 5)
        align (0.5, 0.5)
        xysize (1120, 600)
        # side "c r":
            # area (20, 43, 1110, 495)
        viewport id "herofin_vp":
            style_group "stats"
            draggable True
            mousewheel True
            if day > 1 and hero.fin.game_fin_log.has_key(str(day-1)):
                $ fin_inc = hero.fin.game_fin_log[str(day-1)][0]["private"]
                $ fin_exp = hero.fin.game_fin_log[str(day-1)][1]["private"]
                
                if pytfall.hp.finance_filter == 'day':
                    label (u"Fin Report (Yesterday)") xalign 0.4 ypos 30 text_size 30
                    # Income:
                    vbox:
                        pos (50, 100)
                        label "Income:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 170
                                xfill True
                                for key in fin_inc:
                                    text "[key]"
                            vbox:
                                null height 1
                                spacing 4
                                for key in fin_inc:
                                    $ val = fin_inc[key]
                                    text "[val]" style "stats_value_text"
                                    
                    # Expense:
                    vbox:
                        pos (450, 100)
                        label "Expense:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 170
                                xfill True
                                for key in fin_exp:
                                    text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in fin_exp:
                                    $ val = fin_exp[key]
                                    text ("[val]") style "stats_value_text"
                                
                    python:
                        total_income = 0
                        total_expenses = 0
                        for key in fin_inc:
                            total_income += fin_inc[key]
                        for key in fin_exp:
                            total_expenses += fin_exp[key]
                        total = total_income - total_expenses
                        
                    vbox:
                        align (0.80, 0.60)
                        text "----------------------------------------"
                        text ("Revenue: [total]"):
                            size 20
                            xpos 15
                            if total > 0:
                                color lawngreen style "stats_value_text"
                            else:
                                color red style "stats_value_text"
                        
                    hbox:
                        style_group "basic"
                        align (0.5, 0.9)
                        textbutton "Show Total" action SetField(pytfall.hp, "finance_filter", "total")
                    
                elif pytfall.hp.finance_filter == 'total':
                    label (u"Fin Report (Game)") xalign 0.4 ypos 30 text_size 30
                    python:
                        income = dict()
                        for _day in hero.fin.game_fin_log:
                            for key in hero.fin.game_fin_log[_day][0]["private"]:
                                income[key] = income.get(key, 0) + hero.fin.game_fin_log[_day][0]["private"][key]
                    # Income:
                    vbox:
                        pos (50, 100)
                        label "Income:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 170
                                xfill True
                                for key in income:
                                    text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in income:
                                    $ val = income[key]
                                    text ("[val]") style "stats_value_text"
                                    
                    python:
                        expenses = dict()
                        for _day in hero.fin.game_fin_log:
                            for key in hero.fin.game_fin_log[_day][1]["private"]:
                                expenses[key] = expenses.get(key, 0) + hero.fin.game_fin_log[_day][1]["private"][key]
                    # Expense:
                    vbox:
                        pos (450, 100)
                        label "Expense:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 170
                                xfill True
                                for key in expenses:
                                    text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in expenses:
                                    $ val = expenses[key]
                                    text ("[val]") style "stats_value_text"
                                
                    python:
                        game_total = 0
                        total_income = sum(income.values())
                        total_expenses = sum(expenses.values())
                        game_total = total_income - total_expenses
                        
                    vbox:
                        align (0.80, 0.60)
                        text "----------------------------------------"
                        text ("Revenue: [game_total]"):
                            size 20
                            xpos 15
                            if game_total > 0:
                                color lawngreen style "stats_value_text"
                            else:
                                color red style "stats_value_text"
                        
                    hbox:
                        style_group "basic"
                        align (0.5, 0.9)
                        textbutton "{size=-3}Show Daily" action SetField(pytfall.hp, "finance_filter", "day")
                
                hbox:
                    pos (750, 100)
                    vbox:
                        xmaximum 140
                        xfill True
                        if hero.fin.property_tax_debt:
                            text ("Property:\n(Tax Debt") color red size 20 outlines [(2, "#424242", 0, 0)]
                        if hero.fin.income_tax_debt:
                            text ("Income:\n(Tax Debt)") color crimson size 20 outlines [(2, "#424242", 0, 0)]
                        if day != 1:
                            text "Taxes:\n(This week)" size 20 outlines [(2, "#424242", 0, 0)]
                    vbox:
                        if hero.fin.property_tax_debt:
                            null height 4
                            spacing 4
                            text ("[hero.fin.property_tax_debt]\n ") color red style "stats_value_text"
                        if hero.fin.income_tax_debt:
                            null height 4
                            spacing 4
                            text ("[hero.fin.income_tax_debt]\n ") color crimson style "stats_value_text"
                        if day != 1:
                            python:
                                days = calendar.days.index(calendar.weekday())
                                taxes = hero.fin.get_total_taxes(days)
                            null height 4
                            spacing 4
                            text ("[taxes]\n ") style "stats_value_text"
                                
            # vbar value YScrollValue("herofin_vp")
        button:
            style_group "basic"
            action Hide('pyt_hero_finances')
            minimum (250, 30)
            align (0.5, 0.96)
            text "OK"
