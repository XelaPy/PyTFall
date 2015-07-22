label brothel_management:
    python:
        if hero.upgradable_buildings:
            try:
                index = index
            
            except:
                index = 0
            
            if index >= len(hero.upgradable_buildings):
                index = 0
            
            brothel = hero.upgradable_buildings[index]
    
    scene bg scroll
    
    # $ renpy.retain_after_load() Causes weird save/load bug CW reported...
    show screen pyt_brothel_management
    with fade
    
    $ pytfall.world_quests.run_quests("auto") # Added for completion, unnecessary?
    $ pytfall.world_events.run_events("auto")
    
    python:
        global_flags.set_flag("keep_playing_music")
        
        while 1:
            if hero.upgradable_buildings:
                brothel = hero.upgradable_buildings[index]
            
            result = ui.interact()
            
            if result[0] == "brothel":
                if result[1] == 'buyroom':
                    if brothel.rooms < brothel.maxrooms:
                        if hero.take_money(brothel.get_room_price()):
                            brothel.modrooms(1)
                        
                        else:
                            renpy.call_screen('pyt_message_screen', "Not enough funds to buy new room!")
                    
                    else:
                        renpy.call_screen('pyt_message_screen', "No more rooms can be added to this brothel!")
                
                elif result[1] == 'items_transfer':
                    pytfall.it = GuiItemsTransfer(brothel, last_label=last_label)
                    jump(result[1])
                
                elif result[1] == "sign":
                    if brothel.flag('bought_sign'):
                        if hero.take_money(20, reason="Ads"):
                            brothel.adverts[result[1]]['active'] = True
                        
                        else:    
                            renpy.show_screen("pyt_message_screen", "Not enough cash on hand!")
                    
                    else:
                        if hero.take_money(200, reason="Ads"):
                            brothel.set_flag('bought_sign')
                            brothel.adverts[result[1]]['active'] = True
                        
                        else:    
                            renpy.show_screen("pyt_message_screen", "Not enough cash on hand!")
                
                elif result[1] == "sell":
                    price = int(brothel.price*0.9)
                    
                    if renpy.call_screen("yesno_prompt",
                                         message="Are you sure you wish to sell %s for %d Gold?" % (brothel.name, price),
                                         yes_action=Return(True), no_action=Return(False)):
                        if hero.location == brothel:
                            hero.location = hero
                        
                        for girl in hero.girls:
                            if girl.location == brothel:
                                girl.location = hero
                                girl.action = None
                        
                        hero.add_money(price, "Property")
                        hero.remove_brothel(brothel)
                        
                        if hero.upgradable_buildings:
                            index = 0
                            brothel = hero.upgradable_buildings[index]
                        
                        else:
                            break
            
            if result[0] == 'control':
                if result[1] == 'left':
                    index = (index - 1) % len(hero.upgradable_buildings)
                
                elif result[1] == 'right':
                    index = (index + 1) % len(hero.upgradable_buildings)
                
                if result[1] == 'return':
                    break
            
            if result[0] == "maintenance":
                # Cleaning controls
                if result[1] == "clean":
                    price = brothel.get_cleaning_price()
                    if hero.take_money(price, reason="Pro-Cleaning"):
                        brothel.fin.log_expense(price, "Pro-Cleaning")
                        brothel.dirt = 0
                    
                    else:
                        renpy.show_screen("pyt_message_screen", "You do not have the required funds!")
                
                elif result[1] == "clean_all":
                    if hero.take_money(result[2], reason="Pro-Cleaning"):
                        for i in hero.dirty_buildings:
                            i.fin.log_expense(i.get_cleaning_price(), "Pro-Cleaning")
                            i.dirt = 0
                    
                    else:
                        renpy.show_screen("pyt_message_screen", "You do not have the required funds!")
                
                elif result[1] == "rename_brothel":
                    brothel.name = renpy.call_screen("pyt_input", default=brothel.name, text="Enter Brothel name:")
                
                elif result[1] == "retrieve_jail":
                    pytfall.ra.retrieve_jail = not pytfall.ra.retrieve_jail
    
    hide screen pyt_brothel_management
    jump mainscreen

screen pyt_brothel_maintenance():
    modal True
    zorder 1
    
    frame:
        style_group "content"
        background Frame("content/gfx/frame/p_frame52.png", 10, 10)
        at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)        
        xpos 936
        yalign 0.95
        xysize(343, 675)
        
        label (u"{size=20}{color=[ivory]}{b}Maintenance!") align(0.5, 0.19) text_outlines [(2, "#424242", 0, 0)]
        
        # Tooltip related ---------------------------------->
        default tt = Tooltip("Maintenance screen!")
        frame:
            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
            align(0.5, 0.88)
            xysize (320, 120)
            xpadding 13
            ypadding 15
            has vbox
            text (u"{color=[ivory]}%s" % tt.value) outlines [(1, "#424242", 0, 0)]
        
        # Controls themselves ---------------------------------->
        vbox:
            style_group "basic"
            align(0.55, 0.5)
            if isinstance(brothel, DirtyBuilding):
                button:
                    xysize(200, 32)
                    action Return(['maintenance', "clean"])
                    hovered tt.action("Hire cleaners to completely clean this building for %d Gold."%brothel.get_cleaning_price())
                    text "Clean: Brothel"

                python:
                    price = 0
                    for __ in hero.buildings:
                        if isinstance(__, DirtyBuilding):
                            price = price + __.get_cleaning_price()
                    
                button:
                    xysize(200, 32)
                    action Return(['maintenance', "clean_all", price])
                    hovered tt.action("Hire cleaners to completely clean all brothels for [price] Gold.")
                    text "Clean: All Brothels"
                
                button:
                            xysize (200, 32)
                            yalign 0.5
                            action ToggleField(brothel, "auto_clean")
                            hovered tt.action("Enable automatic hiring of cleaners if brothel gets to dirty!")
                            text "Auto-Cleaning:" align (0.0, 0.5)
                            if not brothel.auto_clean:
                                add (im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (1.0, 0.5)
                            else:
                                add(im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (1.0, 0.5)
            
            null height 30
            if brothel.name != TrainingDungeon.NAME:
                button:
                    xysize (120, 100)
                    xalign 0.5
                    action Return(['maintenance', "rename_brothel"])
                    hovered tt.Action("Give new name to your Brothel!")
                    text "Rename Brothel"      
                    
        if brothel.name == TrainingDungeon.NAME:
            button:
                style_group "basic"
                xysize (200, 32)
                align (0.5, 0.5)
                action Return(["maintenance", "retrieve_jail"])
                hovered tt.action("Allow your guards to bail your escaped girls out of jail?")
                text "Auto-bail" align (0.0, 0.5)
                if not pytfall.ra.retrieve_jail:
                    add im.Scale("content/gfx/interface/icons/checkbox_unchecked.png", 25, 25) align (1.0, 0.5)
                else:
                    add im.Scale("content/gfx/interface/icons/checkbox_checked.png", 25, 25) align (1.0, 0.5)
        
        button:
            style_group "dropdown_gm"
            action Hide("pyt_brothel_maintenance")
            minimum(50, 30)
            align (0.5, 0.97)
            text  "OK"

screen pyt_brothel_adverts():
    modal True
    zorder 1
    
    frame:
        style_group "content"
        at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)
        background Frame("content/gfx/frame/p_frame52.png", 10, 10)
        xpos 936
        yalign 0.95
        xysize(343, 675)
        
        label (u"{size=20}{color=[ivory]}{b}Advertise!") text_outlines [(2, "#424242", 0, 0)] align (0.5, 0.16)
        
        # Tooltip related ---------------------------------->
        default tt = Tooltip("Attract more and better clients. Choose your advertisement budget carefully so your girls can keep up with quality and quantity of customers!")
        frame:
            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
            align(0.5, 0.88)
            xysize (320, 140)
            xpadding 13
            ypadding 15
            has vbox
            text (u"{color=[ivory]}%s" % tt.value) outlines [(1, "#424242", 0, 0)]
        
        # Buttons themselves ---------------------------------->
        hbox:
            align(0.5, 0.4)
            box_wrap True
            spacing 20
            for name in brothel.adverts:
                $ advert = brothel.adverts[name]
                vbox:
                    style_group "basic"
                    align (0.5, 0.5)
                    if advert['active']:
                        button:
                            xysize(280, 32)
                            hovered tt.action(advert['desc'])
                            action ToggleDict(advert, "active")
                            text ("Stop %s!" % advert['name']) color black align (0.5, 0.5)
                    else:
                        if name == "sign":
                            button:
                                xysize(280, 32)
                                hovered tt.action(advert['desc'])
                                action Return(["brothel", "sign"])
                                text "Put Up Sign!" color black align (0.5, 0.5) size 15
                        else:
                            button:
                                xysize(280, 32)
                                hovered tt.action(advert['desc'])
                                action ToggleDict(advert, "active")
                                text ("Use %s for %s Gold!" % (advert['name'], advert['price'])) color black align (0.5, 0.5) size 15

        button:
            style_group "dropdown_gm"
            action Hide("pyt_brothel_adverts")
            minimum(50, 30)
            align (0.5, 0.97)
            text  "OK"
    
screen pyt_brothel_management():
    default tt = Tooltip("Manage your Brothels here")
    
    if hero.upgradable_buildings:
        # Nameframe, pic and control buttons/security bar
        add "content/gfx/frame/p_frame6.png" xalign 0.488 yalign 0.285 size (613, 595)
        vbox:
            style_group "content"
            xalign 0.487
            ypos 45
            null height 3
            frame:
                xalign 0.5
                xysize (380, 50)
                background Frame("content/gfx/frame/namebox5.png", 10, 10)
                label (u"__ [brothel.name] __") text_size 23 text_color ivory align(0.5, 0.6)
            null height 1
            frame:
                background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.95), 10, 10)
                add (ProportionalScale(brothel.img, 600, 444)) align(0.5, 0.5)
            
        frame:
            style_group "content"
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
            xalign 0.489
            ypos 552
            xysize (628, 74)
            hbox:
                align(0.46, 0.5)
                #use rtt_lightbutton(img=im.Scale("content/gfx/interface/buttons/arrow_button_metal_gold_leftt.png", 140, 40), return_value=['control', 'left'], tooltip="Previous Brothel")
                #use rtt_lightbutton(img=im.Scale("content/gfx/interface/buttons/arrow_button_metal_gold_right.png", 60, 60), return_value=['control', 'right'], tooltip="Next Brothel")
                button:
                    xysize (140, 40)
                    style "left_wood_button"
                    action Return(['control', 'left'])
                    hovered tt.action("<== Previous")
                    text "Previous" style "wood_text" xalign(0.69)
                
                null width 280
                
                button:
                    xysize (140, 40)
                    style "right_wood_button"
                    action Return(['control', 'right'])
                    hovered tt.action("Next ==>")
                    text "Next" style "wood_text" xalign(0.39)
        ## Security Bar:
        if brothel.gui_security_bar()[0]:
            frame:
                xalign 0.490
                ypos 561
                background Frame (Transform("content/gfx/frame/rank_frame.png", alpha=0.4), 5, 5)
                xysize (240, 55)
                xpadding 10
                ypadding 10
                hbox:
                    pos (34, 1)
                    vbox:
                        xsize 135
                        text "Security Presence:" size 12
                    vbox:
                        text (u"%d/%d"%(brothel.security_presence, brothel.gui_security_bar()[1])) size 12
                null height 3
                bar:
                    align (0.45, 0.8)
                    value FieldValue(brothel, 'security_presence', brothel.gui_security_bar()[1], max_is_zero=False, style='scrollbar', offset=0, step=1)
                    xsize 170
                    thumb 'content/gfx/interface/icons/move15.png'
                    
        
        ## Stats/Info - Left Frame
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
            xysize(330, 780)
            xanchor 0.01
            ypos 30
            style_group "content"
            has vbox
            vbox:
                style_group "stats"
                pos(0.015, 10)
                xmaximum 325
                frame:
                    background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xysize (317, 100)
                    xanchor 5
                    yanchor 2
                    hbox:
                        vbox:
                            spacing -7
                            xanchor 0
                            xmaximum 153
                            xfill True
                            frame:
                                text "{color=[ivory]}Rooms:" xalign (0.02)
                            frame:
                                text "{color=[ivory]}Free Rooms:" xalign (0.02)
                            if isinstance(brothel, UpgradableBuilding):
                                if brothel.use_upgrades:
                                    frame:
                                        text "{color=[ivory]}Slots:" xalign (0.02)
                                if brothel.get_upgrade_mod("guards") > 0:
                                    frame:
                                        text "{color=[ivory]}Guard Quarters:" xalign (0.02)
                            frame:
                                text "{color=[ivory]}Security Rating:" xalign (0.02)
                            if isinstance(brothel, DirtyBuilding):
                                frame:
                                    text "{color=[ivory]}Dirt:" xalign (0.02)
                            if isinstance(brothel, FamousBuilding):
                                frame:
                                    text "{color=[ivory]}Fame:" xalign (0.02)
                                frame:
                                    text "{color=[ivory]}Reputation:" xalign (0.02)
                                # frame:
                                    # text "{color=[ivory]}Max Rank:" xalign (0.02)
                        vbox:
                            yalign (0.6)
                            spacing 9
                            xfill True
                            xminimum 142
                            xmaximum 142
                            text (u"%s/%s" % (brothel.rooms, brothel.maxrooms)) style "stats_value_text" xalign (1.0)
                            text (u"%d/%d" % (brothel.free_rooms(), brothel.rooms)) style "stats_value_text" xalign (1.0)
                                
                            if isinstance(brothel, UpgradableBuilding):
                                if brothel.use_upgrades:
                                    text (u"%s/%s" % (brothel.used_upgrade_slots, brothel.upgrade_slots)) style "stats_value_text" xalign (1.0)
                                    
                                if brothel.get_upgrade_mod("guards") > 0:
                                    text (u"%d/5  " % min(len([girl for girl in hero.girls if girl.location == brothel and "Warrior" in girl.occupations]), 5) ) style "stats_value_text" xalign (1.0)
                                
                            text (u"%s/1000" % (brothel.security_rating)) style "stats_value_text" xalign (1.0)
                                
                            if isinstance(brothel, DirtyBuilding):
                                text (u"%s (%s %%)" % (brothel.get_dirt_percentage()[1], brothel.get_dirt_percentage()[0])) style "stats_value_text" xalign (1.0)
                                
                            if isinstance(brothel, FamousBuilding):
                                text (u"%s/%s" % (brothel.fame, brothel.maxfame)) style "stats_value_text" xalign (1.0)
                                text (u"%s/%s" % (brothel.rep, brothel.maxrep)) style "stats_value_text" xalign (1.0)
                                # text (u"%s" % (brothel.maxrank)) style "stats_value_text" xalign (1.0)
                        
                null height 5
                frame:
                    background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xysize (317, 230)
                    xanchor 5
                    yanchor 10
                    if isinstance(brothel, UpgradableBuilding):
                        label 'Upgrades:' text_color ivory xalign 0.5
                        if brothel.use_upgrades:
                            null height 5
                                
                            hbox:
                                spacing -5
                                    
                                for key in brothel.upgrades:
                                    vbox:
                                        null height 30
                                        xpos 5
                                        #spacing 1
                                        for ukey in sorted(brothel.upgrades[key].keys()):
                                            frame:
                                                xysize (10, 10)
                                                xanchor 5
                                                background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                                                if brothel.upgrades[key][ukey]['active']:
                                                    use rtt_lightbutton(img=im.Scale(brothel.upgrades[key][ukey]['img'], 43, 43),
                                                                                    return_value=['do_nothing'],
                                                                                      tooltip=brothel.upgrades[key][ukey]['desc'])
                                
                frame:
                    background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xysize (317, 160)
                    xanchor 5
                    yanchor 10
                    style_group "stats"
                    label "Active Advertisements:" text_color ivory xalign 0.5
                    if brothel.use_adverts:
                        vbox:
                            null height 35
                            spacing -6
                            for advert in brothel.adverts.values():
                                if advert['active']:
                                    frame:
                                        xysize (305, 27)
                                        text (u"%s" % advert['name']) size 16 xalign (0.02)
        
        ## Right frame
        frame:
            ypos 37
            xalign 1.0
            xysize (345, 592)
            background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
            frame:
                yalign 0.5
                xysize (330, 95)
                background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 5, 5)
                hbox:
                    style_group "wood"
                    xalign 0.5
                    spacing 5
                    null height 16
                    vbox:
                        spacing 5
                        button:
                            xysize (150, 40)
                            action Return(['brothel', "buyroom"])
                            hovered tt.action('Add rooms to this Brothel. Price = %d.' % brothel.get_room_price())
                            text "Add Room"
                        if isinstance(brothel, UpgradableBuilding) and brothel.use_adverts:
                            button:
                                xysize (150, 40)
                                action Show("pyt_brothel_adverts")
                                hovered tt.action('Advertise this building to attract more and better customers.')
                                text "Advertise"
                        else:
                            button:
                                xysize (150, 40)
                                action NullAction()
                                hovered tt.action('Advertise this building to attract more and better customers.')
                                text "Advertise"
                        if len(brothel.get_girls()) > 0:
                            button:
                                xysize (150, 40)
                                action [Hide("pyt_brothel_management"), Return(['brothel', "items_transfer"])]
                                hovered tt.action('Transfer items between characters in this brothel!')
                                text "Transfer Items"
                        else:
                            button:
                                xysize (150, 40)
                                action NullAction()
                                hovered tt.action('Transfer items between characters in this brothel!')
                                text "Transfer Items"
                        if isinstance(brothel, DirtyBuilding) or brothel.name == TrainingDungeon.NAME:
                            button:
                                xysize (150, 40)
                                action Show("pyt_brothel_maintenance")
                                hovered tt.action('Perform maintenance of this building.')
                                text "Maintenance"
                        else:
                            button:
                                xysize (150, 40)
                                action NullAction()
                                hovered tt.action('Perform maintenance of this building.')
                                text "Maintenance"
                    vbox:
                        spacing 5
                        if isinstance(brothel, UpgradableBuilding) and brothel.use_upgrades:
                            button:
                                xysize (150, 40)
                                action Jump("brothel_upgrade")
                                hovered tt.action('Upgrade this building.')
                                text "Upgrade"
                        else:
                            button:
                                xysize (150, 40)
                                action NullAction()
                                hovered tt.action('Upgrade this building.')
                                text "Upgrade"
                        button:
                            xysize (150, 40)
                            action SetField(hero, "location", brothel)
                            hovered tt.action('Place MC in this brothel!')
                            text "Settle MC"
                        button:
                            xysize (150, 40)
                            action Show("pyt_brothel_finances")
                            hovered tt.action('Show Finance log.')
                            text "Finance Log"
                        button:
                            xysize (150, 40)
                            action Return(["control", "sell"])
                            hovered tt.action('Get rid of this building')
                            text "Sell"
    
    # Tooltip related:
    frame:
        background Frame(Transform("content/gfx/frame/ink_box.png"), 10, 10)
        align(0, 1.0)
        xanchor -321
        xpadding 10
        xysize (955, 100)
        text (u"{=content_text}{size=20}{color=[ivory]}%s" % tt.value) yalign 0.1
    
    use pyt_top_stripe(True)

screen pyt_brothel_finances():
    modal True
    zorder 1
    
    default show_fin = "day"
    
    frame at slide(so1=(0, 700), t1=0.7, so2=(0, 0), t2=0.3, eo2=(0, -config.screen_height)):
        background Frame("content/gfx/frame/arena_d.png", 5, 5)
        align (0.5, 0.5)
        
        # side "c r":
        viewport id "message_vp":
            style_group "content"
            xysize (1100, 600)
            draggable False
            mousewheel True
            
            if day > 1 and str(day-1) in brothel.fin.game_fin_log:
                $ fin_inc = brothel.fin.game_fin_log[str(day-1)][0]
                $ fin_exp = brothel.fin.game_fin_log[str(day-1)][1]
                
                if show_fin == 'day':
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
                                
                                for key in fin_inc["work"]:
                                    text ("[key]")
                                
                                for key in fin_inc["private"]:
                                    if key != "work": 
                                        text("[key]")
                            
                            vbox:
                                for key in fin_inc["work"]:
                                    $ val = fin_inc["work"][key]
                                    text("[val]")
                                
                                for key in fin_inc["private"]:
                                    $ val = fin_inc["private"][key]
                                    text("[val]")
                    
                    # Expense:
                    vbox:
                        pos (450, 100)
                        label "Expense:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 170
                                xfill True
                                
                                for key in fin_exp["work"]:
                                    text("[key]")
                                
                                for key in fin_exp["private"]:
                                    text("[key]")
                            
                            vbox:
                                for key in fin_exp["work"]:
                                    $ val = fin_exp["work"][key]
                                    text("[val]")
                                
                                for key in fin_exp["private"]:
                                    $ val = fin_exp["private"][key]
                                    text("[val]")
                    
                    python:
                        total_income = sum(fin_inc["work"].values())
                        total_expenses = sum(fin_exp["work"].values())
                        for key in fin_inc["private"]: total_income += fin_inc["private"][key]
                        for key in fin_exp["private"]: total_expenses += fin_exp["private"][key]
                        total = total_income - total_expenses
                    vbox:
                        align (0.80, 0.60)
                        text "----------------------------------------"
                        text ("Revenue: [total]"):
                            size 25
                            xpos 15
                            if total > 0:
                                color lawngreen
                            else:
                                color red
                    
                    hbox:
                        style_group "basic"
                        align (0.5, 0.9)
                        textbutton "{size=-3}Show Total" action SetScreenVariable("show_fin", "total") minimum(200, 30)
                
                elif show_fin == 'total':
                    label (u"Fin Report (Game)") xalign 0.4 ypos 30 text_size 30
                    python:
                        income = dict()
                        for _day in brothel.fin.game_fin_log:
                            for key in brothel.fin.game_fin_log[_day][0]["private"]:
                                income[key] = income.get(key, 0) + brothel.fin.game_fin_log[_day][0]["private"][key]
                            
                            for key in brothel.fin.game_fin_log[_day][0]["work"]:
                                income[key] = income.get(key, 0) + brothel.fin.game_fin_log[_day][0]["work"][key]
                    
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
                                    text("[key]")
                            vbox:
                                for key in income:
                                    $ val = income[key]
                                    text("[val]")
                    
                    python:
                        expenses = dict()
                        for _day in brothel.fin.game_fin_log:
                            for key in brothel.fin.game_fin_log[_day][1]["private"]:
                                expenses[key] = expenses.get(key, 0) + brothel.fin.game_fin_log[_day][1]["private"][key]
                            
                            for key in brothel.fin.game_fin_log[_day][1]["work"]:
                                expenses[key] = expenses.get(key, 0) + brothel.fin.game_fin_log[_day][1]["work"][key]
                    vbox:
                        pos (450, 100)
                        label "Expense:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 170
                                xfill True
                                for key in expenses:
                                    text("[key]")
                            vbox:
                                for key in expenses:
                                    $ val = expenses[key]
                                    text("[val]")
                    
                    python:
                        game_total = 0
                        total_income = sum(income.values())
                        total_expenses = sum(expenses.values())
                        game_total = total_income - total_expenses
                    vbox:
                        align (0.80, 0.60)
                        text "----------------------------------------"
                        text ("Revenue: [game_total]"):
                            size 25
                            xpos 15
                            if game_total > 0:
                                color lawngreen
                            else:
                                color red
                    
                    hbox:
                        style_group "basic"
                        align (0.5, 0.9)
                        textbutton "{size=-3}Show Daily" action SetScreenVariable("show_fin", "day") minimum(200, 30)
            
            else:
                text (u"No financial records availible!") align(0.5, 0.5)
                
            button:
                style_group "basic"
                action Hide('pyt_brothel_finances')
                minimum (250, 30)
                align (0.5, 0.96)
                text "OK"
