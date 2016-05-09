label building_management:
    python:
        # Some Global Vars we use to pass data between screens:
        if hero.upgradable_buildings:
            try:
                index = index
            except:
                index = 0
            
            if index >= len(hero.upgradable_buildings):
                index = 0
            
            building = hero.upgradable_buildings[index]
            char = None
            temp_chars = [c for c in building.get_workers() if c.status =="free"] # Move to class with moar filters?
            workers = CoordsForPaging(temp_chars, columns=6, rows=3, size=(80, 80), xspacing=10, yspacing=10, init_pos=(47, 15))
            try:
                temp = [u for u in building._upgrades if u.__class__ == ExplorationGuild][0]
                guild_teams = CoordsForPaging(temp.teams, columns=2, rows=3, size=(310, 83), xspacing=3, yspacing=3, init_pos=(-2, 420))
            except:
                pass
    
    scene bg scroll
    
    $ renpy.retain_after_load() # Causes weird save/load bug CW reported...
    show screen building_management
    with fade
    
    $ pytfall.world_quests.run_quests("auto") # Added for completion, unnecessary?
    $ pytfall.world_events.run_events("auto")
    
    $ global_flags.set_flag("keep_playing_music")
    
label building_management_loop:
    
    $ last_label = "building_management" # We need this so we can come back here from screens that depends on this variable.
    
    while 1:
        if hero.upgradable_buildings:
            $ building = hero.upgradable_buildings[index]
        
        $ result = ui.interact()
        if not result or not isinstance(result, (list, tuple)):
            jump building_management_loop
        
        if result[0] == "building":
            if result[1] == 'buyroom':
                python:
                    if building.rooms < building.maxrooms:
                        if hero.take_money(building.get_room_price()):
                            building.modrooms(1)
                        else:
                            renpy.call_screen('message_screen', "Not enough funds to buy new room!")
                    else:
                        renpy.call_screen('message_screen', "No more rooms can be added to this building!")
            
            elif result[1] == 'items_transfer':
                $ pytfall.it = GuiItemsTransfer(building, last_label=last_label)
                $ jump(result[1])
            
            elif result[1] == "sign":
                python:
                    if building.flag('bought_sign'):
                        if hero.take_money(20, reason="Ads"):
                            building.adverts[result[1]]['active'] = True
                        
                        else:    
                            renpy.show_screen("message_screen", "Not enough cash on hand!")
                    
                    else:
                        if hero.take_money(200, reason="Ads"):
                            building.set_flag('bought_sign')
                            building.adverts[result[1]]['active'] = True
                        
                        else:
                            renpy.show_screen("message_screen", "Not enough cash on hand!")
            
            elif result[1] == "sell":
                python:
                    price = int(building.price*0.9)
                    
                    if renpy.call_screen("yesno_prompt",
                                         message="Are you sure you wish to sell %s for %d Gold?" % (building.name, price),
                                         yes_action=Return(True), no_action=Return(False)):
                        if hero.location == building:
                            hero.location = hero
                        
                        for girl in hero.girls:
                            if girl.location == building:
                                girl.location = hero
                                girl.action = None
                        
                        hero.add_money(price, "Property")
                        hero.remove_building(building)
                        
                        if hero.upgradable_buildings:
                            index = 0
                            building = hero.upgradable_buildings[index]
                        else:
                            jump("building_management_end")
        
        # Upgrades:
        elif result[0] == 'upgrade':
            if result[1] == "build":
                python:
                    temp = result[2]()
                    building.add_upgrade(temp, main_upgrade=result[3])
                    del temp
                            
        elif result[0] == "maintenance":
            python:
                # Cleaning controls
                if result[1] == "clean":
                    price = building.get_cleaning_price()
                    if hero.take_money(price, reason="Pro-Cleaning"):
                        building.fin.log_expense(price, "Pro-Cleaning")
                        building.dirt = 0
                    
                    else:
                        renpy.show_screen("message_screen", "You do not have the required funds!")
                
                elif result[1] == "clean_all":
                    if hero.take_money(result[2], reason="Pro-Cleaning"):
                        for i in hero.dirty_buildings:
                            i.fin.log_expense(i.get_cleaning_price(), "Pro-Cleaning")
                            i.dirt = 0
                    
                    else:
                        renpy.show_screen("message_screen", "You do not have the required funds!")
                
                elif result[1] == "rename_building":
                    building.name = renpy.call_screen("pyt_input", default=building.name, text="Enter Building name:")
                
                elif result[1] == "retrieve_jail":
                    pytfall.ra.retrieve_jail = not pytfall.ra.retrieve_jail
                
        elif result[0] == 'control':
            if result[1] == 'left':
                $ index = (index - 1) % len(hero.upgradable_buildings)
            
            elif result[1] == 'right':
                $ index = (index + 1) % len(hero.upgradable_buildings)
            
            if result[1] == 'return':
                jump building_management_end
                    
label building_management_end:
    hide screen building_management
    jump mainscreen

init: # Screens:
    screen building_management():
        
        key "mousedown_4" action SetScreenVariable("mid_frame_mode", "building"), Return(["control", "right"])
        key "mousedown_5" action Return(["control", "left"])
        
        default tt = Tooltip("Manage your Buildings here.")
        default mid_frame_mode = "building"
        default mid_frame_focus = None
        default exploration_view_mode = "explore"
        
        if hero.upgradable_buildings:
            # Middle Frame:
                # has vbox xsize 630
                
            # Main Building mode:
            if mid_frame_mode == "building":
                use building_management_midframe_building_mode
            else: # Upgrade mode:
                use building_management_midframe_upgrades_mode
            
            ## Stats/Upgrades - Left Frame
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                xysize (330, 720)
                # xanchor 0.01
                ypos 40
                style_group "content"
                has vbox
                if mid_frame_mode == "building":
                    use building_management_leftframe_building_mode
                else: # Upgrade mode:
                    use building_management_leftframe_upgrades_mode
            
            ## Right frame:
            frame:
                xysize (330, 720)
                ypos 40
                xalign 1.0
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                has vbox spacing 1
                if mid_frame_mode == "building":
                    use building_management_rightframe_building_mode
                else: # Upgrade mode:
                    use building_management_rightframe_upgrades_mode
                                
        use top_stripe(True)
        if not mid_frame_mode == "building":
            key "mousedown_3" action SetScreenVariable("mid_frame_mode", "building")
        
    screen building_management_rightframe_building_mode:
        # Buttons group:
        frame:
            xalign .5
            style_group "wood"
            xpadding 0
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 5, 5)
            has hbox xalign .5 spacing 5 xsize 315
            null height 16
            vbox:
                spacing 5
                # if isinstance(building, UpgradableBuilding):
                    # button:
                        # xysize (135, 40)
                        # action Return(['building', "buyroom"])
                        # hovered tt.action('Add rooms to this Building. Price = %d.' % building.get_room_price())
                        # text "Add Room"
                if hasattr(building, "use_adverts") and building.use_adverts:
                    button:
                        xysize (135, 40)
                        action Show("building_adverts")
                        hovered tt.action('Advertise this building to attract more and better customers.')
                        text "Advertise"
                else:
                    button:
                        xysize (135, 40)
                        action NullAction()
                        hovered tt.action('Advertise this building to attract more and better customers.')
                        text "Advertise"
                if len(building.get_girls()) > 0:
                    button:
                        xysize (135, 40)
                        action [Hide("building_management"), Return(['building', "items_transfer"])]
                        hovered tt.action('Transfer items between characters in this building!')
                        text "Transfer Items"
                else:
                    button:
                        xysize (135, 40)
                        action NullAction()
                        hovered tt.action('Transfer items between characters in this building!')
                        text "Transfer Items"
                if isinstance(building, DirtyBuilding) or building.name == TrainingDungeon.NAME:
                    button:
                        xysize (135, 40)
                        action Show("building_maintenance")
                        hovered tt.action('Perform maintenance of this building.')
                        text "Maintenance"
                else:
                    button:
                        xysize (135, 40)
                        action NullAction()
                        hovered tt.action('Perform maintenance of this building.')
                        text "Maintenance"
            vbox:
                spacing 5
                # if isinstance(building, UpgradableBuilding) and building.use_upgrades:
                    # button:
                        # xysize (135, 40)
                        # action Jump("building_upgrade")
                        # hovered tt.action('Upgrade this building.')
                        # text "Upgrade"
                button:
                    xysize (135, 40)
                    action SetField(hero, "location", building)
                    hovered tt.action('Place MC in this building!')
                    text "Settle MC"
                button:
                    xysize (135, 40)
                    action Show("building_finances")
                    hovered tt.action('Show Finance log.')
                    text "Finance Log"
                button:
                    xysize (135, 40)
                    action Return(["control", "sell"])
                    hovered tt.action('Get rid of this building')
                    text "Sell"
        
        # Slots for New Style Upgradable Buildings:
        if isinstance(building, NewStyleUpgradableBuilding):
            frame:
                xalign .5
                style_group "wood"
                xpadding 0
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 5, 5)
                has vbox xalign 0.5 spacing 2 xsize 315
                hbox:
                    xoffset 5
                    xalign .5
                    xsize 300
                    spacing 3
                    frame:
                        has vbox xysize (130, 40)
                        text "Indoor Slots:" size 10 color yellow xalign .5
                        text "%d/%d" % (building.in_slots, building.in_slots_max) color beige size 12 xalign .5 style "stats_value_text"
                    frame:
                        has vbox xysize (130, 40)
                        text "Outdoor Slots:" size 10 color yellow xalign .5
                        text "%d/%d" % (building.ex_slots, building.ex_slots_max) color beige size 12 xalign .5 style "stats_value_text"
                frame:
                    xysize (145, 40)
                    xalign .5
                    # has vbox
                    text "Construction" size 10 color yellow align .5, .5
                    # text "%d/%d" % (building.ex_slots, building.ex_slots_max) color beige size 12 xalign .5 style "stats_value_text"
                    
        # Tooltip related:
        frame:
            background Frame(Transform("content/gfx/frame/ink_box.png"), 10, 10)
            xalign .5
            xpadding 10
            xysize (310, 200)
            text (u"{=content_text}{size=20}{color=[ivory]}%s" % tt.value) yalign 0.02 size 14

        # Manager?
        if isinstance(building, NewStyleUpgradableBuilding):
            frame:
                xalign .5
                background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.95), 10, 10)
                if building.manager:
                    add building.manager.show("profile", resize=(190, 190), add_mood=True, cache=True) align .5, .5
                else:
                    add Solid(black, xysize=(190, 190)) align .5, .5
        
    screen building_management_rightframe_upgrades_mode:
        $ frgr = Fixed(xysize=(315, 680))
        $ frgr.add(ProportionalScale("content/gfx/images/e1.png", 315, 600, align=(.5, .0)))
        $ frgr.add(ProportionalScale("content/gfx/images/e2.png", 315, 600, align=(.5, 1.0)))
        frame:
            style_prefix "content"
            xysize (315, 680)
            background Null()
            foreground frgr
            frame:
                pos 25, 20
                xysize (260, 40)
                background Frame("content/gfx/frame/namebox5.png", 10, 10)
                label (u"__ [mid_frame_mode.name] __") text_size 18 text_color ivory align (0.5, 0.6)
            null height 5
            
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                align (0.5, 0.5)
                xpadding 10
                ypadding 10
                vbox:
                    style_group "wood"
                    align (0.5, 0.5)
                    spacing 10
                    button:
                        xysize (150, 40)
                        yalign 0.5
                        action SetScreenVariable("mid_frame_mode", "building")
                        hovered tt.action("Here you can invest your gold and resources for various improvements.\nAnd see the different information (reputation, rank, fame, etc.)")
                        text "Building" size 15
                    if False and isinstance(mid_frame_mode, ExplorationGuild):
                        button:
                            xysize (150, 40)
                            yalign 0.5
                            action NullAction()
                            hovered tt.action("All the meetings and conversations are held in this Hall. On the noticeboard, you can take job that available for your rank. Sometimes guild members or the master himself and his Council, can offer you a rare job.")
                            text "Main Hall" size 15
                    if isinstance(mid_frame_mode, ExplorationGuild):
                        button:
                            xysize (150, 40)
                            yalign 0.5
                            action SetScreenVariable("exploration_view_mode", "team")
                            hovered tt.action("You can customize your team here or hire Guild members.")
                            text "Team" size 15
                        button:
                            xysize (150, 40)
                            yalign 0.5
                            action SetScreenVariable("exploration_view_mode", "explore")
                            hovered tt.action("On this screen you can organize the expedition. Also, there is a possibility to see all available information on the various places, enemies and items drop.")
                            text "Exploration" size 15
                        button:
                            xysize (150, 40)
                            yalign 0.5
                            action SetScreenVariable("exploration_view_mode", "log")
                            hovered tt.action("For each of your teams, recorded one last adventure, which you can see here in detail.")
                            text "Log" size 15
            
            # Tooltip Frame
            frame:
                background Frame("content/gfx/frame/ink_box.png", 10, 10)
                xysize (307, 190)
                xpadding 10
                align .5, .99
                text (u"{=stats_text}{color=[bisque]}{size=-1}%s" % tt.value) outlines [(1, "#3a3a3a", 0, 0)]
            
                    
    screen building_management_leftframe_building_mode:
        frame:
            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
            style_group "proper_stats"
            xsize 300
            xpadding 12
            ypadding 12
            xmargin 0
            ymargin 0
            has vbox spacing 1
            
            # Old Style Rooms:
            # if isinstance(building, UpgradableBuilding):
                # frame:
                    # xysize (290, 27)
                    # xalign 0.5
                    # text "Rooms:" xalign 0.02 color ivory
                    # text "%d/%d" % (building.rooms, building.maxrooms) xalign .98 style "stats_value_text" xoffset 12 yoffset 4
                # frame:
                    # xysize (290, 27)
                    # xalign 0.5
                    # text "Free Rooms:" xalign 0.02 color ivory
                    # text "%d/%d" % (building.free_rooms(), building.rooms) xalign .98 style "stats_value_text" xoffset 12 yoffset 4
                
            # Security Rating:
            frame:
                xysize (290, 27)
                xalign 0.5
                text "Security Rating:" xalign 0.02 color ivory
                text "%s/1000" % building.security_rating xalign .98 style "stats_value_text" xoffset 12 yoffset 4
                
            # Old Style Slots and Quarters:
            # if isinstance(building, UpgradableBuilding):
                # if building.use_upgrades:
                    # frame:
                        # xysize (290, 27)
                        # xalign 0.5
                        # text "Slots:" xalign 0.02 color ivory
                        # text "%s/%s" % (building.used_upgrade_slots, building.upgrade_slots) xalign .98 style "stats_value_text" xoffset 12 yoffset 4
                # if building.get_upgrade_mod("guards") > 0:
                    # frame:
                        # xysize (290, 27)
                        # xalign 0.5
                        # text "Guard Quarters:" xalign 0.02 color ivory
                        # text "%d/5  " % min(len([girl for girl in hero.girls if girl.location == building and "Warrior" in girl.occupations]), 5) xalign .98 style "stats_value_text" xoffset 12 yoffset 4
            
            # Dirt:
            if isinstance(building, DirtyBuilding):
                frame:
                    xysize (290, 27)
                    xalign 0.5
                    text "Dirt:" xalign 0.02 color ivory
                    text "%s (%s %%)" % (building.get_dirt_percentage()[1], building.get_dirt_percentage()[0]) xalign .98 style "stats_value_text" xoffset 12 yoffset 4
                    
            # Fame/Rep:
            if isinstance(building, FamousBuilding):
                frame:
                    xysize (290, 27)
                    xalign 0.5
                    text "Fame:" xalign 0.02 color ivory
                    text "%s/%s" % (building.fame, building.maxfame) xalign .98 style "stats_value_text" xoffset 12 yoffset 4
                frame:
                    xysize (290, 27)
                    xalign 0.5
                    text "Reputation:" xalign 0.02 color ivory
                    text "%s/%s" % (building.rep, building.maxrep) xalign .98 style "stats_value_text" xoffset 12 yoffset 4
                    
        null height 5
        frame:
            background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
            xysize (317, 430)
            # if isinstance(building, UpgradableBuilding):
                # label 'Upgrades:' text_color ivory xalign 0.5
                # if building.use_upgrades:
                    # null height 5
                    # hbox:
                        # spacing -5
                        # for key in building.upgrades:
                            # vbox:
                                # null height 30
                                # xpos 5
                                # for ukey in sorted(building.upgrades[key].keys()):
                                    # frame:
                                        # xysize (10, 10)
                                        # xanchor 5
                                        # background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                                        # if building.upgrades[key][ukey]['active']:
                                            # use rtt_lightbutton(img=im.Scale(building.upgrades[key][ukey]['img'], 43, 43),
                                                                          # return_value=['do_nothing'],
                                                                          # tooltip=building.upgrades[key][ukey]['desc'])
            if isinstance(building, NewStyleUpgradableBuilding):
                frame:
                    align .5, 0.02
                    background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                    xysize (180, 30)
                    label 'Constructed:' text_color ivory xalign 0.5 text_bold True
                vbox:
                    ypos 55
                    xalign 0.5
                    for u in building._upgrades:
                        frame:
                            xalign .6
                            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                            has fixed xysize 290, 80
                            frame:
                                align .05, .1
                                background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.95), 10, 10)
                                if hasattr(u, "img"):
                                    add im.Scale(u.img, 100, 65) align .5, .5
                                else:
                                    add Solid(black, xysize=(100, 65)) align .5, .5
                            vbox:
                                xpos 125
                                yalign 0.5
                                xysize 150, 60
                                text "[u.name]" xalign .5 style "stats_text" size 20
                                null height 2
                                textbutton "{size=15}Upgrade" xalign .5 action SetScreenVariable("mid_frame_mode", u)
                                            
        # frame:
            # background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
            # xysize (317, 160)
            # style_group "stats"
            # label "Active Advertisements:" text_color ivory xalign 0.5
            # if hasattr(building, "use_adverts") and building.use_adverts:
                # vbox:
                    # null height 35
                    # spacing -6
                    # for advert in building.adverts.values():
                        # if advert['active']:
                            # frame:
                                # xysize (305, 27)
                                # text (u"%s" % advert['name']) size 16 xalign (0.02)
        
    screen building_management_leftframe_upgrades_mode:
        frame:
            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
            style_group "proper_stats"
            xsize 300
            xpadding 12
            ypadding 12
            xmargin 0
            ymargin 0
            has vbox spacing 1
                
            # Slots:
            frame:
                xysize (290, 27)
                xalign 0.5
                text "In Slots:" xalign 0.02 color ivory
                text "[mid_frame_mode.in_slots]"  xalign .98 style "stats_value_text" xoffset 12 yoffset 4
            frame:
                xysize (290, 27)
                xalign 0.5
                text "Ext Slots:" xalign 0.02 color ivory
                text "[mid_frame_mode.ex_slots]"  xalign .98 style "stats_value_text" xoffset 12 yoffset 4
                
        if isinstance(mid_frame_mode, ExplorationGuild): # Only for FG.
            if exploration_view_mode == "explore":
                frame: 
                    style_group "content"
                    xalign 0.5
                    xysize (200, 50)
                    background Frame("content/gfx/frame/namebox5.png", 10, 10)
                    label (u"Maps") text_size 23 text_color ivory align (.5, .8)
                    
                null height 10
                viewport:
                    xysize 220, 500
                    xalign .5
                    has vbox spacing 4
                    $ temp = sorted([a for a in fg_areas.values() if a.main and a.unlocked])
                    if temp and not mid_frame_focus:
                        $ mid_frame_focus = temp[0]
                        
                    for area in temp:
                        $ img = im.Scale(area.img, 200, 130)
                        frame:
                            background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                            xpadding 5
                            ypadding 6
                            xmargin 0
                            ymargin 0
                            xysize 200, 130
                            button:
                                align .5, .5
                                xysize 200, 130
                                background Frame(img)
                                hover_background Frame(im.MatrixColor(img, im.matrix.brightness(0.10)))
                                action SetScreenVariable("mid_frame_focus", area)
                                frame:
                                    align .5, .0
                                    xysize 180, 30
                                    background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 5, 5)
                                    text area.name color gold style "interactions_text" size 18 outlines [(1, "#3a3a3a", 0, 0)] align .5, .5
    
                # hbox:
                    # xalign 0.5
                    # spacing 20
                    # add ProportionalScale("content/gfx/interface/buttons/arrow_button_metal_gold_up.png", 50, 50)
                    # add ProportionalScale("content/gfx/interface/buttons/arrow_button_metal_gold_down.png", 50, 50)
        
    screen building_management_midframe_building_mode:
        frame:
            background Frame("content/gfx/frame/p_frame6.png", 10, 10)
            style_prefix "content"
            xysize (630, 685)
            xalign .5
            ypos 40
            has vbox xsize 630
            null height 5
            frame:
                xalign 0.5
                xysize (380, 50)
                background Frame("content/gfx/frame/namebox5.png", 10, 10)
                label (u"__ [building.name] __") text_size 23 text_color ivory align (0.5, 0.6)
            null height 5
            
            frame:
                xalign 0.5
                background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.95), 10, 10)
                add ProportionalScale(building.img, 600, 444) align (0.5, 0.5)
            
            # Left/Right Controls.
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
                has hbox xysize (600, 74)
                button:
                    align .1, .5
                    xysize (140, 40)
                    style "left_wood_button"
                    action Return(['control', 'left'])
                    hovered tt.action("<== Previous")
                    text "Previous" style "wood_text" xalign 0.69
                
                frame:
                    background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                    xysize (200, 50)
                    align (0.5, 0.5)
                
                button:
                    align .9, .5
                    xysize (140, 40)
                    style "right_wood_button"
                    action Return(['control', 'right'])
                    hovered tt.action("Next ==>")
                    text "Next" style "wood_text" xalign 0.39
                    
            if isinstance(building, NewStyleUpgradableBuilding):
                frame:
                    align .5, .95
                    style_group "wood"
                    background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 5, 5)
                    xpadding 20
                    ypadding 10                                
                    button:
                        align .5, .5
                        xysize (135, 40)
                        action SetScreenVariable("mid_frame_mode", building)
                        hovered tt.action('Open a new business in this building!.')
                        text "Expand"
                        
            ## Security Bar:
            if hasattr(building, "gui_security_bar") and building.gui_security_bar()[0]:
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
                            text (u"%d/%d"%(building.security_presence, building.gui_security_bar()[1])) size 12
                    null height 3
                    bar:
                        align (0.45, 0.8)
                        value FieldValue(building, 'security_presence', building.gui_security_bar()[1], max_is_zero=False, style='scrollbar', offset=0, step=1)
                        xsize 170
                        thumb 'content/gfx/interface/icons/move15.png'
            
    screen building_management_midframe_upgrades_mode:
        frame:
            background Frame("content/gfx/frame/p_frame6.png", 10, 10)
            style_prefix "content"
            xysize (630, 685)
            xalign .5
            ypos 40       
            if isinstance(mid_frame_mode, ExplorationGuild):
                if exploration_view_mode == "explore":
                    has vbox xsize 630
                    frame: # Image
                        xalign 0.5
                        background Frame("content/gfx/frame/MC_bg3.png", 10 ,10)
                        add im.Scale("content/gfx/bg/buildings/Exploration.png", 615, 390)
                    
                    hbox:
                        box_wrap 1
                        spacing 2
                        xalign .5
                        if isinstance(mid_frame_focus, FG_Area):
                            $ temp = sorted([a for a in fg_areas.values() if a.area == mid_frame_focus.name])
                            for area in temp:
                                $ fbg = "content/gfx/frame/mes12.jpg"
                                $ hfbg = im.MatrixColor("content/gfx/frame/mes11.jpg", im.matrix.brightness(0.10))
                                button:
                                    background Transform(Frame(fbg, 10, 10), alpha=0.9)
                                    hover_background Transform(Frame(hfbg, 10, 10), alpha=0.9)
                                    xysize (150, 90)
                                    ymargin 1
                                    ypadding 1
                                    if area.unlocked:
                                        $ temp = area.name
                                        action Show("fg_area", dissolve, area)
                                    else:
                                        $ temp = "?????????"
                                        action NullAction()
                                    text temp color gold style "interactions_text" size 14 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                                    hbox:
                                        align (0.5, 0.9)
                                        # Get the correct stars:
                                        python:
                                            temp = []
                                            for i in range(area.explored//20):
                                                temp.append(ProportionalScale("content/gfx/bg/example/star2.png", 18, 18))
                                            if len(temp) != 5:
                                                if area.explored%20 >= 10:
                                                    temp.append(ProportionalScale("content/gfx/bg/example/star3.png", 18, 18))
                                            while len(temp) != 5:
                                                temp.append(ProportionalScale("content/gfx/bg/example/star1.png", 18, 18))
                                        for i in temp:
                                            add i
                                            
                if exploration_view_mode == "team":
                    # Backgrounds:
                    frame:
                        background Frame(gfxframes + "p_frame52.png", 10, 10)
                        xysize 622, 330
                        yoffset -1
                        xalign .5
                        hbox:
                            xalign .5
                            box_wrap 1
                            for i in xrange(18):
                                frame:
                                    xysize 90, 90
                                    xmargin 2
                                    ymargin 2
                                    background Frame(gfxframes + "p_frame53.png", 5, 5)
                        # Page control buttons:
                        hbox:
                            style_prefix "paging_green"
                            align .5, .99
                            hbox:
                                spacing 1
                                button:
                                    style_suffix "button_left2x"
                                    hovered tt.action("<== First Page")
                                    action Function(workers.first_page), SensitiveIf(workers.page != 0)
                                button:
                                    style_suffix "button_left"
                                    hovered tt.action("<== Previous Page")
                                    action Function(workers.prev_page), SensitiveIf(workers.page - 1 >= 0)
                            null width 60
                            hbox:
                                spacing 1
                                button:
                                    style_suffix "button_right"
                                    hovered tt.action("Next Page ==>")
                                    action Function(workers.next_page), SensitiveIf(workers.page + 1 <= workers.max_page)
                                button:
                                    style_suffix "button_right2x"
                                    hovered tt.action("Last Page ==>")
                                    action Function(workers.last_page), SensitiveIf(workers.page != workers.max_page)
                    
                    hbox:
                        style_prefix "paging_green"
                        align .5, .55
                        hbox:
                            spacing 1
                            button:
                                style_suffix "button_left2x"
                                hovered tt.action("<== First Page")
                                action guild_teams.first_page, SensitiveIf(guild_teams.page != 0)
                            button:
                                style_suffix "button_left"
                                hovered tt.action("<== Previous Page")
                                action guild_teams.prev_page, SensitiveIf(guild_teams.page - 1 >= 0)
                        null width 40
                        hbox:
                            spacing 1
                            button:
                                style_suffix "button_right"
                                hovered tt.action("Next Page ==>")
                                action guild_teams.next_page, SensitiveIf(guild_teams.page + 1 < guild_teams.max_page)
                            button:
                                style_suffix "button_right2x"
                                hovered tt.action("Last Page ==>")
                                action guild_teams.last_page, SensitiveIf(guild_teams.page != guild_teams.max_page)

                    
                    # We'll prolly have to do two layers, one for backgrounds and other for drags...
                    draggroup:
                        id "team_builder"
                        for t, pos in guild_teams:
                            drag:
                                drag_name t
                                xysize (310, 83)
                                draggable 0
                                droppable 1
                                pos pos
                                add gfxframes + "team_frame_1.png"
                                hbox:
                                    yalign .5
                                    xpos 117
                                    spacing 15
                                    for i in t:
                                        $ img = i.show("portrait", resize=(46, 46), cache=1)
                                        button:
                                            xysize (46, 46)
                                            background img
                                            hover_background im.MatrixColor(img, im.matrix.brightness(0.10))
                                            action Show("fg_char_dropdown", dissolve, i, team=t, remove=True)
                                            hovered tt.action(i.fullname)
                                frame:
                                    xysize (310, 83)
                                    background gfxframes + "team_frame_2.png"
                                    text t.name xpos 50 xanchor .5 yalign .5
                                    
                        for w, pos in workers:
                            drag:
                                dragged dragged
                                droppable 0
                                hovered tt.action(w.fullname)
                                drag_name w
                                pos pos
                                clicked Show("fg_char_dropdown", dissolve, w, team=None, remove=False)
                                add w.show("portrait", resize=(70, 70), cache=1)
                                    
                                # fixed:
                                    # xysize (172, 65)
                                    # hbox:
                                        # yalign .3
                                        # xpos 10
                                        # spacing 20
                                        # for i in hero.team:
                                            # add i.show("portrait", resize=(38, 38), cache=1)
                                    # add gfxframes + "small_port_empty.png"
                                 
            else: # TODO: This needs an extra variable and better conditioning...
                has vbox xsize 630
                for u in mid_frame_mode.allowed_upgrades:
                    if building._has_upgrade(u):
                        frame:
                            xalign .5
                            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                            has fixed xysize 500, 150
                            
                            frame:
                                align .3, .5
                                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                                xpadding 15
                                text "Active" align .5, .5 style "stats_text" size 35
                            
                            vbox:
                                align 1.0, 0
                                xsize 150
                                frame:
                                    xalign .5
                                    background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                                    xpadding 10
                                    text "[u.ID]" align .5, .5 style "stats_text" size 15
                                frame:
                                    xalign .5
                                    background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.95), 10, 10)
                                    if hasattr(u, "IMG"):
                                        add im.Scale(u.IMG, 120, 75) align .5, .5
                                    else:
                                        add Solid(black, xysize=(120, 75)) align .5, .5
                            
                    else:
                        frame:
                            xalign .5
                            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                            has fixed xysize 500, 150
                            
                            frame:
                                align .3, 0
                                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                                xpadding 10
                                text "Resources Needed:" align .5, .5 style "stats_text" size 15
                                    
                            hbox:
                                pos 15, 35
                                box_wrap True
                                xsize 330
                                spacing 10
                                frame:
                                    background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                                    has hbox xysize 135, 40
                                    text "Gold: [u.COST]" align .5, .5 style "stats_text" size 20 color gold
                                # We presently allow for 3 resources each upgrade. If more, this needs to be a conditioned viewport:
                                for r in sorted(u.MATERIALS):
                                    $ r = items[r]
                                    frame:
                                        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                                        has hbox xysize 135, 40
                                        text "[r.id] x {}".format(u.MATERIALS[r.id]) align .01, .5 style "stats_text" color ivory size 15
                                        frame:
                                            align .99, .5
                                            background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.95), 10, 10)
                                            add im.Scale(r.icon, 33, 33) align .5, .5
                                
                            vbox:
                                align 1.0, 0
                                xsize 150
                                frame:
                                    xalign .5
                                    background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                                    xpadding 10
                                    text "[u.ID]" align .5, .5 style "stats_text" size 15
                                frame:
                                    xalign .5
                                    background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.95), 10, 10)
                                    if hasattr(u, "IMG"):
                                        add im.Scale(u.IMG, 120, 75) align .5, .5
                                    else:
                                        add Solid(black, xysize=(120, 75)) align .5, .5
                                textbutton "{size=15}Build" xalign .5 action Return(["upgrade", "build", u, mid_frame_mode]), SensitiveIf(building.can_upgrade(u))
                
                textbutton "Back" align .5, .95 action SetScreenVariable("mid_frame_mode", "building")
        
 
    screen building_maintenance():
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
                if isinstance(building, DirtyBuilding):
                    button:
                        xysize(200, 32)
                        action Return(['maintenance', "clean"])
                        hovered tt.action("Hire cleaners to completely clean this building for %d Gold."%building.get_cleaning_price())
                        text "Clean: Building"
    
                    python:
                        price = 0
                        for i in hero.buildings:
                            if isinstance(i, DirtyBuilding):
                                price = price + i.get_cleaning_price()
                        
                    button:
                        xysize(200, 32)
                        action Return(['maintenance', "clean_all", price])
                        hovered tt.action("Hire cleaners to completely clean all buildings for [price] Gold.")
                        text "Clean: All Buildings"
                    
                    button:
                                xysize (200, 32)
                                yalign 0.5
                                action ToggleField(building, "auto_clean")
                                hovered tt.action("Enable automatic hiring of cleaners if building gets to dirty!")
                                text "Auto-Cleaning:" align (0.0, 0.5)
                                if not building.auto_clean:
                                    add (im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (1.0, 0.5)
                                else:
                                    add(im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (1.0, 0.5)
                
                null height 30
                if building.name != TrainingDungeon.NAME:
                    button:
                        xysize (120, 100)
                        xalign 0.5
                        action Return(['maintenance', "rename_building"])
                        hovered tt.Action("Give new name to your Building!")
                        text "Rename Building"      
                        
            if building.name == TrainingDungeon.NAME:
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
                action Hide("building_maintenance")
                minimum(50, 30)
                align (0.5, 0.97)
                text  "OK"
    
    screen building_adverts():
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
                for name in building.adverts:
                    $ advert = building.adverts[name]
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
                                    action Return(["building", "sign"])
                                    text "Put Up Sign!" color black align (0.5, 0.5) size 15
                            else:
                                button:
                                    xysize(280, 32)
                                    hovered tt.action(advert['desc'])
                                    action ToggleDict(advert, "active")
                                    text ("Use %s for %s Gold!" % (advert['name'], advert['price'])) color black align (0.5, 0.5) size 15
    
            button:
                style_group "dropdown_gm"
                action Hide("building_adverts")
                minimum(50, 30)
                align (0.5, 0.97)
                text  "OK"
        
    screen building_finances():
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
                
                if day > 1 and str(day-1) in building.fin.game_fin_log:
                    $ fin_inc = building.fin.game_fin_log[str(day-1)][0]
                    $ fin_exp = building.fin.game_fin_log[str(day-1)][1]
                    
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
                            for _day in building.fin.game_fin_log:
                                for key in building.fin.game_fin_log[_day][0]["private"]:
                                    income[key] = income.get(key, 0) + building.fin.game_fin_log[_day][0]["private"][key]
                                
                                for key in building.fin.game_fin_log[_day][0]["work"]:
                                    income[key] = income.get(key, 0) + building.fin.game_fin_log[_day][0]["work"][key]
                        
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
                            for _day in building.fin.game_fin_log:
                                for key in building.fin.game_fin_log[_day][1]["private"]:
                                    expenses[key] = expenses.get(key, 0) + building.fin.game_fin_log[_day][1]["private"][key]
                                
                                for key in building.fin.game_fin_log[_day][1]["work"]:
                                    expenses[key] = expenses.get(key, 0) + building.fin.game_fin_log[_day][1]["work"][key]
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
                    action Hide('building_finances')
                    minimum (250, 30)
                    align (0.5, 0.96)
                    text "OK"
                    
                    
    # Customized screens for specific businesses:
    screen fg_area(area):
        modal True
        zorder 1
        
        key "mousedown_3" action Hide("fg_area")
        
        # frame:
            # background Frame("content/gfx/frame/p_frame6.png", 10, 10)
            # style_prefix "content"
            # xysize (630, 720)
            # xalign .5
            # ypos 40
        
        frame:
            ypos 40
            xalign .5
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
            style_prefix "content"
            xysize (630, 680)
            
            $ fbg = "content/gfx/frame/mes11.jpg"
            frame:
                background Transform(Frame(fbg, 10, 10), alpha=0.9)
                xysize (620, 90)
                ymargin 1
                ypadding 1
                $ temp = area.name
                text temp color gold style "interactions_text" size 35 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.3)
                hbox:
                    align (0.5, 0.9)
                    # Get the correct stars:
                    python:
                        temp = []
                        for i in range(area.explored//20):
                            temp.append(ProportionalScale("content/gfx/bg/example/star2.png", 18, 18))
                        if len(temp) != 5:
                            if area.explored%20 >= 10:
                                temp.append(ProportionalScale("content/gfx/bg/example/star3.png", 18, 18))
                        while len(temp) != 5:
                            temp.append(ProportionalScale("content/gfx/bg/example/star1.png", 18, 18))
                    for i in temp:
                        add i
                    # button:
                        # align (0.5, 0.95)
                        # action NullAction()
                        # text "Stage 1" size 14
                # vbox:
                    # xfill True
                    # spacing 7
                    # frame:
                        # style_group "content"
                        # align (0.5, 0.015)
                        # xysize (210, 30)
                        # background Frame (Transform("content/gfx/frame/Namebox.png", alpha=0.9), 10, 10)
                        # label (u"Team name") text_size 20 text_color ivory align(0.5, 0.5)
                    # hbox:
                        # xfill True
                        # spacing 2
                        # add "content/gfx/bg/example/1.png" align (0.5, 0.5)
                        # add "content/gfx/bg/example/2.png" align (0.5, 0.5)
                        # add "content/gfx/bg/example/3.png" align (0.5, 0.5)
            hbox:
                align .5, .5
                frame:
                    background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xysize (310, 410)
                    xpadding 5
                    frame:
                        style_group "content"
                        align (0.5, 0.015)
                        xysize (210, 40)
                        background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.6), 10, 10)
                        label (u"Enemies") text_size 23 text_color ivory align .5, .5
                    viewport:
                        style_prefix "proper_stats"
                        xysize (300, 340)
                        ypos 50
                        xalign .5
                        has vbox spacing 3
                        for m in area.mobs:
                            $ m = mobs[m]
                            fixed:
                                xysize 300, 65
                                frame:
                                    xpos 6
                                    left_padding 2
                                    align .01, .5
                                    xsize 197
                                    text m["name"]
                                frame:
                                    yalign 0.5
                                    xanchor 1.0
                                    ysize 40
                                    xpadding 4
                                    xminimum 25
                                    xpos 233
                                    $ temp = m["min_lvl"]
                                    text ("Lvl\n[temp]+") align (0.5, 0.5) style "TisaOTM" size 18
                                frame:
                                    background Frame(Transform("content/gfx/interface/buttons/choice_buttons2.png", alpha=0.75), 10, 10)
                                    xpadding 3
                                    ypadding 3
                                    xysize 60, 60
                                    align .99, .5
                                    add ProportionalScale(m["portrait"], 60, 60)
                                    
                frame:
                    background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xysize (310, 410)
                    xpadding 5
                    frame:
                        style_group "content"
                        align (0.5, 0.015)
                        xysize (210, 40)
                        background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.6), 10, 10)
                        label (u"Items") text_size 23 text_color ivory align .5, .5
                    viewport:
                        style_prefix "proper_stats"
                        mousewheel 1
                        xysize (300, 340)
                        ypos 50
                        xalign .5
                        has vbox spacing 3
                        for i in area.items:
                            $ i = items[i]
                            fixed:
                                xysize 300, 65
                                frame:
                                    xpos 6
                                    left_padding 2
                                    align .01, .5
                                    xsize 197
                                    text i.id
                                frame:
                                    yalign 0.5
                                    xanchor 1.0
                                    ysize 40
                                    xsize 35
                                    xpadding 4
                                    xpos 233
                                    #$ temp = m["min_lvl"]
                                    #text ("Lvl\n[temp]+") align (0.5, 0.5) style "TisaOTM" size 18
                                frame:
                                    background Frame(Transform("content/gfx/interface/buttons/choice_buttons2.png", alpha=0.75), 10, 10)
                                    xpadding 3
                                    ypadding 3
                                    xysize 60, 60
                                    align .99, .5
                                    add ProportionalScale(i.icon, 60, 60)
                    # frame:
                        # background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                        # xysize (390, 380)
                        # yalign 1.0
                        # frame:
                            # style_group "content"
                            # align (0.5, 0.015)
                            # xysize (200, 40)
                            # background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.6), 10, 10)
                            # label (u"Loot") text_size 23 text_color ivory align(0.5, 0.5)
                        # vbox:    ### Need Side-scrolling ###
                            # style_group "stats"
                            # vbox:
                                # xalign 0.5
                                # ypos 53
                                # vbox:
                                    # spacing 2
                                    # xanchor 0
                                    # xmaximum 210
                                    # xfill True
                                    # hbox:
                                        # xfill True
                                        # spacing -3
                                        # frame:
                                            # yalign 0.5
                                            # xsize 210
                                            # text("\"Lorekeeper\" Staff")
                                        # frame:
                                            # yalign 0.5
                                            # xsize 140
                                            # text("Weapon") xalign 0.5
                                        # frame:
                                            # yalign 0.5
                                            # xsize 20
                                            # add ProportionalScale("content/gfx/bg/example/legendary.png", 25, 25)
                                # vbox:
                                    # spacing 2
                                    # xanchor 0
                                    # xmaximum 210
                                    # xfill True
                                    # hbox:
                                        # xfill True
                                        # spacing -3
                                        # frame:
                                            # yalign 0.5
                                            # xsize 210
                                            # text("Ashwood Flatbow")
                                        # frame:
                                            # yalign 0.5
                                            # xsize 140
                                            # text("Weapon") xalign 0.5
                                        # frame:
                                            # yalign 0.5
                                            # xsize 20
                                            # add ProportionalScale("content/gfx/bg/example/uncommon.png", 25, 25)
                                # vbox:
                                    # spacing 2
                                    # xanchor 0
                                    # xmaximum 220
                                    # xfill True
                                    # hbox:
                                        # xfill True
                                        # spacing -3
                                        # frame:
                                            # yalign 0.5
                                            # xsize 210
                                            # text("???????")
                                        # frame:
                                            # yalign 0.5
                                            # xsize 140
                                            # text("???????") xalign 0.5
                                        # frame:
                                            # yalign 0.5
                                            # xsize 20
                                            # add ProportionalScale("content/gfx/bg/example/unknown2.png", 25, 25)
                                # vbox:
                                    # spacing 2
                                    # xanchor 0
                                    # xmaximum 220
                                    # xfill True
                                    # hbox:
                                        # xfill True
                                        # spacing -3
                                        # frame:
                                            # yalign 0.5
                                            # xsize 210
                                            # text("Honey")
                                        # frame:
                                            # yalign 0.5
                                            # xsize 140
                                            # text("Consumable") xalign 0.5
                                        # frame:
                                            # yalign 0.5
                                            # xsize 20
                                            # add ProportionalScale("content/gfx/bg/example/common.png", 25, 25)
                                # vbox:
                                    # spacing 2
                                    # xanchor 0
                                    # xmaximum 220
                                    # xfill True
                                    # hbox:
                                        # xfill True
                                        # spacing -3
                                        # frame:
                                            # yalign 0.5
                                            # xsize 210
                                            # text("???????")
                                        # frame:
                                            # yalign 0.5
                                            # xsize 140
                                            # text("???????") xalign 0.5
                                        # frame:
                                            # yalign 0.5
                                            # xsize 20
                                            # add ProportionalScale("content/gfx/bg/example/unknown2.png", 25, 25)
                                # vbox:
                                    # spacing 2
                                    # xanchor 0
                                    # xmaximum 220
                                    # xfill True
                                    # hbox:
                                        # xfill True
                                        # spacing -3
                                        # frame:
                                            # yalign 0.5
                                            # xsize 210
                                            # text("???????")
                                        # frame:
                                            # yalign 0.5
                                            # xsize 140
                                            # text("???????") xalign 0.5
                                        # frame:
                                            # yalign 0.5
                                            # xsize 20
                                            # add ProportionalScale("content/gfx/bg/example/unknown2.png", 25, 25)
                                # vbox:
                                    # spacing 2
                                    # xanchor 0
                                    # xmaximum 220
                                    # xfill True
                                    # hbox:
                                        # xfill True
                                        # spacing -3
                                        # frame:
                                            # yalign 0.5
                                            # xsize 210
                                            # text("???????")
                                        # frame:
                                            # yalign 0.5
                                            # xsize 140
                                            # text("???????") xalign 0.5
                                        # frame:
                                            # yalign 0.5
                                            # xsize 20
                                            # add ProportionalScale("content/gfx/bg/example/unknown2.png", 25, 25)
            hbox:
                align (0.5, 0.98)
                button:
                    style_group "basic"
                    action Hide("fg_area")
                    minimum (50, 30)
                    text  "Back"
                # button:
                        # style_group "basic"
                        # action NullAction()
                        # minimum(50, 30)
                        # align (0.5, 0.98)
                        # text  "Launch!!! Days 1" # Gismo: AutoCalculate. 1 day per stage (1-5), 2 days per stage (6-10).
                        
    screen fg_char_dropdown(char, team=None, remove=False):
        # Trying to create a drop down screen with choices of actions:
        zorder 3
        modal True
        
        default pos = renpy.get_mouse_pos()
        
        key "mousedown_4" action NullAction()
        key "mousedown_5" action NullAction()
        
        # Get mouse coords:
        python:
            x, y = pos
            xval = 1.0 if x > config.screen_width/2 else .0
            yval = 1.0 if y > config.screen_height/2 else .0
            
        frame:
            style_prefix "dropdown_gm"
            pos (x, y)
            anchor (xval, yval)
            has vbox
            
            textbutton "Profile":
                action [SetVariable("char_profile", last_label), SetVariable("char", char), SetVariable("girls", [char]), Hide("fg_char_dropdown"), Hide("pyt_fg_management"), Jump("char_profile")]
            textbutton "Equipment":
                action [SetVariable("came_to_equip_from", "building_management"), SetVariable("eqtarget", char), SetVariable("char", char), SetVariable("girls", [char]), Hide("fg_char_dropdown"), Hide("pyt_fg_management"), Jump("char_equip")]
            if remove: # and team[0] != girl:
                textbutton "Remove from the Team":
                    action [Function(team.remove, char), Function(workers.add, char), Hide("fg_char_dropdown")]
            
            # null height 10
            # text "Jobs:" style "della_respira" color ivory bold True
            # for entry in FighterGuild.ACTIONS:
                # if entry == 'Training':
                    # if girl.status != "slave":
                        # textbutton "[entry]":
                            # action [SetField(girl, "action", entry), Execute(equip_for, girl, entry), Hide("pyt_fg_girl_menu")]
                # elif entry == 'ServiceGirl':
                    # if (girl.status == "slave" or "Server" in girl.occupations) and not list(g for g in fg.get_girls() if g.action == "ServiceGirl"):
                        # textbutton "[entry]":
                            # action [SetField(girl, "action", entry), Execute(equip_for, girl, entry), Hide("pyt_fg_girl_menu")]
                # elif entry == 'BarGirl':
                    # if fg.upgrades["bar"][0] and (girl.status == "slave" or "Server" in girl.occupations) and not list(g for g in fg.get_girls() if g.action == "BarGirl"):
                        # textbutton "[entry]":
                            # action [SetField(girl, "action", entry), Execute(equip_for, girl, "ServiceGirl"), Hide("pyt_fg_girl_menu")]
                # elif entry == 'Rest':
                    # textbutton "[entry]":
                        # action [SetField(girl, "action", entry), Execute(equip_for, girl, entry), Hide("pyt_fg_girl_menu")]
                # else:
                    # textbutton "[entry]":
                            # action [SetField(girl, "action", entry), Execute(equip_for, girl, entry), Hide("pyt_fg_girl_menu")]
            
            null height 10
                
            textbutton "Close":
                action Hide("fg_char_dropdown")
