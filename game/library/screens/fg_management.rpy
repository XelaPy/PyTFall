label fg_management:
    scene bg profile_2
    
    # We check if any of the girls in teams had been fired and remove them:
    python:
        if not hasattr(store, "char"):
            char = None
        if not hasattr(store, "girls"):
            girls = None
        # for team in fg.teams[:]:
            # for girl in team:
                # if girl not in hero.chars:
                    # if team[0] == girl:
                        # fg.teams.remove(team)
                        # global_flags.set_flag("teams_changed")
                        # break
                    # else:
                        # team.remove(girl)
                        # global_flags.set_flag("teams_changed")
        if global_flags.flag("teams_changed"):
            global_flags.del_flag("teams_changed")
            renpy.show_screen("message_screen", "Your teams setup has been changed, due to girls leaving your service or dieing!")
            
    # $ fg_drags = FG_Drags()

    # $ renpy.retain_after_load()
    show screen fg_management
    with fade
    
    $ pytfall.world_quests.run_quests("auto") # Added for completion, unnecessary?
    $ pytfall.world_events.run_events("auto")
    
    python:
        
        global_flags.set_flag("keep_playing_music")
        
        while 1:
            result = ui.interact()
            
            if isinstance(result, list):
                if result[0] == 'control':
                    if result[1] == 'return':
                        break
                elif result[0] == "team":
                    if result[1] == "add":
                        if hero.take_money(fg.get_team_price(), "Fighers Guild"):
                            team_name = len(fg.teams)
                            team_name = renpy.call_screen("pyt_input", "Meow x %s" % team_name, "Name the Team!", 15)
                            if team_name in list(team.name for team in fg.teams):
                                renpy.call_screen("message_screen", "Team name must be unique!")
                            else:
                                team = Team(name=team_name, max_size=3)
                                fg.teams.append(team)
                                fg.rooms += 3
                        else:
                            renpy.call_screen("message_screen", "You do not have the required funds (%d)!" % fg.get_team_price())
                    elif result[1] == "disband":
                        if renpy.call_screen("yesno_prompt", message="Are you sure that you wish to disband this team?\n\nThis cannot be reversed and creating new team will cost you money!", yes_action=Return(True), no_action=Return(False)):
                            fg.teams.remove(result[2])
                            fg.rooms -= 3
                    elif result[1] == "rename":
                        team_name = renpy.call_screen("pyt_input", result[2].name, "Enter Team name:", 15)
                        if team_name in list(team.name for team in fg.teams):
                            renpy.call_screen("message_screen", "Team name must be unique!")
                        else:    
                            result[2].name = team_name
                            
                elif result[0] == "fg":
                    if result[1] == "upgrade":
                        upgrade = fg.upgrades[result[2]]
                        if renpy.call_screen("yesno_prompt", message="Are you sure you wish to buy %s for %d Gold?" % (string.capwords(result[2]), upgrade[2]),
                                                        yes_action=Return(True), no_action=Return(False)):
                            if hero.take_money(upgrade[2], "Upgrades"):
                                upgrade[0] = True
                                renpy.call_screen("message_screen", "%s added to the Guild!" % string.capwords(result[2]))
                            else:
                                renpy.call_screen("message_screen", "Not enough money...")
                        
                elif result[0] == "dd":
                    if result[1] == "run_exploration":
                        FG_ExplorationJob(result[2], result[3])
                    if result[1] == "area_pick":
                        pos = renpy.get_mouse_pos()
                        ua = list() # Unlocked areas!
                        # We will create a list containing all availible areas.
                        for area in fg_areas.values():
                            if area.area == fg.focus_gen_area and area.unlocked:
                                ua.append(area)
                        ua.sort(key=attrgetter("id"))
                        renpy.show_screen("area_pick", ua, pos=pos)
                    if result[1] == "gen_area_pick":
                        pos = renpy.get_mouse_pos()
                        ua = list() # Unlocked areas!
                        # We will create a list containing all unlocked "general" Areas
                        for area in fg_areas.values():
                            if area.area in list(a.area for a in ua):
                                pass
                            elif area.unlocked:
                                ua.append(area)    
                        ua.sort(key=attrgetter("id"))
                        fg.focus_gen_area = renpy.call_screen("gen_area_pick", ua, pos=pos)
                        # Get all unlocked areas:
                        ua = list()
                        for area in fg_areas.values():
                            if area.area == fg.focus_gen_area and area.unlocked:
                                ua.append(area)
                        ua.sort()
                        if ua:
                            fg.focus_area = ua[0]
                    if result[1] == "girl_menu":
                        pos = renpy.get_mouse_pos()
                        renpy.show_screen("fg_girl_menu", result[2], team=result[3], remove=result[4], pos=pos)
                                              
    hide screen fg_management
    jump mainscreen
        
init python:
    # Drag&Drop Control Function:
    def fg_dragged(drags, drop):
        content = fg_drags.get_page_content()
        for girl in content:
            if girl.fullname == drags[0].drag_name:
                char = girl
                break
        else:
            raise Exception, "Unknown drag name: %s!" % drags[0].drag_name
                
        index = content.index(char)
        x = fg_drags.pos[index][0]
        y = fg_drags.pos[index][1]
        
        if not drop:
            drags[0].snap(x, y, delay=0.2)
            renpy.restart_interaction()
            return

        if char.status == "slave":
            drags[0].snap(x, y, delay=0.2)
            renpy.show_screen("message_screen", "Slaves are not allowed to participate in combat!")
            renpy.restart_interaction()
            return

        for team in fg.teams:
            if drop.drag_name == team.name:
                team = team
                break
        else:
            raise Exception, ["Team unknown during drag/drop!", drop.drag_name, team.name]
            
        for t in fg.teams:
            if t and t[0] == char:
                drags[0].snap(x, y, delay=0.2)
                renpy.show_screen("message_screen", "%s is already a leader of %s!" % (char.nickname, t.name))
                renpy.restart_interaction()
                return
            
            if not team:
                for girl in t:
                    if girl == char:
                        drags[0].snap(x, y, delay=0.2)
                        renpy.show_screen("message_screen", "%s cannot lead %s as she's already on %s!" % (char.nickname, team.name, t.name))
                        renpy.restart_interaction()
                        return
                        
        for girl in team:
            if girl == char:
                drags[0].snap(x, y, delay=0.2)
                renpy.show_screen("message_screen", "%s is already on %s!" % (char.nickname, team.name))
                renpy.restart_interaction()
                return
                
        if len(team) == 3:
            drags[0].snap(x, y, delay=0.2)
            renpy.restart_interaction()
            return
        else:
            team.add(char)
            fg_drags.remove(char)
            drags[0].snap(x, y)

        return True
    
screen fg_management():
    
    default focus_team = None
    default stats_display = "Building"
    default team_display = "Team"
    default tt = Tooltip("")
    
    frame:    # Image
        xalign 0.405
        ypos 37
        background Frame("content/gfx/frame/MC_bg3.png", 10 ,10)
        if stats_display == "Building":
            add ProportionalScale("content/gfx/bg/buildings/Adventurers_Guild.png", 742 ,700)
        elif stats_display == "Main Hall":
            add ProportionalScale("content/gfx/bg/buildings/main_hall.png", 742 ,700)
        elif stats_display == "Team Builder":
            add ProportionalScale("content/gfx/bg/buildings/team.png", 742 ,700)
        elif stats_display == "Exploration":
            add ProportionalScale("content/gfx/bg/buildings/Exploration.png", 742 ,700)
        elif stats_display == "Log":
            add ProportionalScale("content/gfx/bg/buildings/log.png", 742 ,700)
    
    # Central (Main Frame)
    frame:
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xysize(746, 201)
        pos (221, 520)
        if stats_display == "Building":
            hbox:
                frame:
                    background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xysize (250, 190)
                    vbox:
                        null height 8
                        style_group "stats"
                        spacing -5
                        xalign 0.5
                        frame:
                            background Frame (Transform("content/gfx/frame/ink_box.png", alpha=0.5), 10, 10)
                            xsize 236
                            text "Building Info:" color ivory xalign (0.5)
                        null height 22
                        # frame:
                            # xalign 0.5
                            # xsize 220
                            # text "{size=-1}Rooms:" color ivory pos (3, -4)
                            # label (u"{size=-5}%s/[fg.rooms]" % len(fg.get_girls())) style "stats_value_text" align (1.0, 0.5)
                        # frame:
                            # xalign 0.5
                            # xsize 220
                            # text "{size=-1}Dirt:" color ivory pos (3, -4)
                            # label (u"{size=-5}%s (%s %%)" % (fg.get_dirt_percentage()[1], fg.get_dirt_percentage()[0])) style "stats_value_text" align (1.0, 0.5)
                        # frame:
                            # xalign 0.5
                            # xsize 220
                            # text "{size=-1}Fame:" color ivory pos (3, -4)
                            # label (u"{size=-5}[fg.fame]/[fg.maxfame]") style "stats_value_text" align (1.0, 0.5)
                        # frame:
                            # xalign 0.5
                            # xsize 220
                            # text "{size=-1}Reputation:" color ivory pos (3, -4)
                            # label (u"{size=-5}[fg.rep]/[fg.maxrep]") style "stats_value_text" align (1.0, 0.5)
                null width 110
                vbox:
                    style_group "basic"
                    align (0.55, 0.5)
                    # button:
                        # action ToggleField(fg, "capture_girls")
                        # xysize (250, 32)
                        # text "Capture Girls!" align (0.0, 0.5)
                        # if fg.capture_girls:
                            # add (im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (1.0, 0.5)
                        # else:
                            # add (im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (1.0, 0.5)
                     
                    # Autobuy: 
                    button:
                        action ToggleField(jail, "auto_sell_captured")
                        xysize (250, 32)
                        text "AutoSell Captives!" align (0.0, 0.5)
                        if jail.auto_sell_captured:
                            add (im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (1.0, 0.5)
                        else:
                            add (im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (1.0, 0.5)
    
        elif stats_display == "Team Builder":  ### Gismo: Just example ###
            null height 20
            hbox:
                style_group "basic"
                xalign 0.5
                button:
                    yalign 0.5
                    action NullAction()
                    text "team 1 name" size 15
                button:
                    yalign 0.5
                    action NullAction()
                    text "team 2 name" size 15
                button:
                    yalign 0.5
                    action NullAction()
                    text "team 3 name" size 15
                button:
                    yalign 0.5
                    action NullAction()
                    text "team 4 name" size 15
    
        elif stats_display == "Exploration":
            vbox: ### Gismo: Just example ###
                null height 4
                xfill True
                hbox:
                    style_group "dropdown_gm2"
                    xalign 0.5
                    spacing -4
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xysize (150, 90)
                        text "{color=[gold]}Peaceful Grove" style "interactions_text" size 16 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                        hbox:
                            align (0.5, 0.45)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                        button:
                            align (0.5, 0.95)
                            action Show("explorer")
                            text "Stage 1" size 14
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xysize (150, 90)
                        text "{color=[gold]}Misty Thicket" style "interactions_text" size 16 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                        hbox:
                            align (0.5, 0.45)
                            add ProportionalScale("content/gfx/bg/example/star3.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                        button:
                            align (0.5, 0.95)
                            action NullAction()
                            text "Stage 2" size 14
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xysize (150, 90)
                        text "{color=[gold]}Forbidden Cove" style "interactions_text" size 16 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                        hbox:
                            align (0.5, 0.45)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                        button:
                            align (0.5, 0.95)
                            action NullAction()
                            text "Stage 3" size 14
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xysize (150, 90)
                        text "{color=[gold]}Flowing Lagoon" style "interactions_text" size 16 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                        hbox:
                            align (0.5, 0.45)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star3.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                        button:
                            align (0.5, 0.95)
                            action NullAction()
                            text "Stage 4" size 14
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xysize (150, 90)
                        text "{color=[gold]}Poison Forest" style "interactions_text" size 16 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                        hbox:
                            align (0.5, 0.45)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                        button:
                            align (0.5, 0.95)
                            action NullAction()
                            text "Stage 5" size 14
                hbox:
                    style_group "dropdown_gm2"
                    xalign 0.5
                    spacing -4
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xysize (150, 90)
                        text "{color=[gold]}???????" style "interactions_text" size 16 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                        hbox:
                            align (0.5, 0.45)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star3.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                        button:
                            align (0.5, 0.95)
                            action NullAction()
                            text "Stage 6" size 14
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xysize (150, 90)
                        text "{color=[gold]}???????" style "interactions_text" size 16 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                        hbox:
                            align (0.5, 0.45)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star3.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                        button:
                            align (0.5, 0.95)
                            action NullAction()
                            text "Stage 7" size 14
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xysize (150, 90)
                        text "{color=[gold]}???????" style "interactions_text" size 16 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                        hbox:
                            align (0.5, 0.45)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                        button:
                            align (0.5, 0.95)
                            action NullAction()
                            text "Stage 8" size 14
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xysize (150, 90)
                        text "{color=[gold]}???????" style "interactions_text" size 16 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                        hbox:
                            align (0.5, 0.45)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star3.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                        button:
                            align (0.5, 0.95)
                            action NullAction()
                            text "Stage 9" size 14
                    frame:
                        background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xysize (150, 90)
                        text "{color=[gold]}???????" style "interactions_text" size 16 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                        hbox:
                            align (0.5, 0.45)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                            add ProportionalScale("content/gfx/bg/example/star2.png", 18, 18)
                        button:
                            align (0.5, 0.95)
                            action NullAction()
                            text "Stage 10" size 14
    
        elif stats_display == "Log":  ### Gismo: Just example ###
            null height 20
            vbox:
                xalign 0.5
                hbox:
                    style_group "basic"
                    xalign 0.5
                    button:
                        yalign 0.5
                        action NullAction()
                        text "team 1 name" size 15
                    button:
                        yalign 0.5
                        action NullAction()
                        text "team 2 name" size 15
                    button:
                        yalign 0.5
                        action NullAction()
                        text "team 3 name" size 15
                    button:
                        yalign 0.5
                        action NullAction()
                        text "team 4 name" size 15
                null height 20
                hbox:
                    xfill True
                    spacing 2
                    add "content/gfx/bg/example/1.png" align (0.5, 0.5)
                    add "content/gfx/bg/example/2.png" align (0.5, 0.5)
                    add "content/gfx/bg/example/3.png" align (0.5, 0.5)
    
    # Right (Main Frame)
    frame:
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xysize(320, 691)
        xalign 1.0
        ypos 30
        vbox:
            xalign 0.5
            null height 40
            frame: 
                style_group "content"
                xalign 0.5
                ypos 17
                xysize (280, 50)
                background Frame("content/gfx/frame/namebox5.png", 10, 10)
                label (u"Adventurers' Guild") text_size 23 text_color ivory align(0.5, 0.8)
    
            null height 80
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                #xysize(310, 380)
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
                        action SetScreenVariable("stats_display", "Building")
                        hovered tt.action("Here you can invest your gold and resources for various improvements.\nAnd see the different information (reputation, rank, fame, etc.)")
                        text "Building" size 15
                        # add ProportionalScale("content/gfx/bg/example/e1.png", 307, 392) pos (-91, -174)
                        # add ProportionalScale("content/gfx/bg/example/e1.png", 307, 392) pos (-91, -174)
                        # add ProportionalScale("content/gfx/bg/example/e2.png", 307, 392) pos (-91, -82)
                        # add ProportionalScale("content/gfx/bg/example/e2.png", 307, 392) pos (-91, -82)
                    button:
                        xysize (150, 40)
                        yalign 0.5
                        action SetScreenVariable("stats_display", "Main Hall")
                        hovered tt.action("All the meetings and conversations are held in this Hall. On the noticeboard, you can take job that available for your rank. Sometimes guild members or the master himself and his Council, can offer you a rare job.")
                        text "Main Hall" size 15
                    button:
                        xysize (150, 40)
                        yalign 0.5
                        action SetScreenVariable("stats_display", "Team Builder")
                        hovered tt.action("You can customize your team here or hire Guild members.")
                        text "Team" size 15
                    button:
                        xysize (150, 40)
                        yalign 0.5
                        action SetScreenVariable("stats_display", "Exploration")
                        hovered tt.action("On this screen you can organize the expedition. Also, there is a possibility to see all available information on the various places, enemies and items drop.")
                        text "Exploration" size 15
                    button:
                        xysize (150, 40)
                        yalign 0.5
                        action SetScreenVariable("stats_display", "Log")
                        hovered tt.action("For each of your teams, recorded one last adventure, which you can see here in detail.")
                        text "Log" size 15
    
            null height 58
            # Tooltip Frame
            frame:
                background Frame("content/gfx/frame/ink_box.png", 10, 10)
                xysize (307, 190)
                xpadding 10
                #xpos -1
                text (u"{=stats_text}{color=[bisque]}{size=-1}%s" % tt.value) outlines [(1, "#3a3a3a", 0, 0)]
            
    
    # Left (Main Frame)
    frame:
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xysize(227, 691)
        xpos 1
        ypos 30
        vbox:
            style_group "stats"
            xalign 0.5
            if stats_display == "Building":
                # Upgrades:
                vbox:
                    align (0.5, 0.5)
                    spacing 5
                    null height 12
                    frame: 
                        style_group "content"
                        xalign 0.5
                        xysize (200, 50)
                        background Frame("content/gfx/frame/namebox5.png", 10, 10)
                        label (u"Upgrades") text_size 23 text_color ivory align(0.5, 0.8)
                    null height 10
                    # for u in fg.upgrades:
                        # hbox:
                            # xalign 0.5
                            # style_group "stats"
                            # $ img = ProportionalScale(fg.upgrades[u][1], 200, 100)
                            # $ u_name = string.capwords(u)
                            # if not fg.upgrades[u][0]:
                                # vbox:
                                    # null height 5
                                    # frame:
                                        # background Frame("content/gfx/frame/stat_box_proper.png", 5, 5)
                                        # text "[u_name]   Inactive" color ivory size 16 xalign 0.5
                                        # xmaximum 200
                                        # xminimum 100
                                        # xalign 0.5
                                    # frame: 
                                        # background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                                        # xmaximum 100
                                        # xminimum 100
                                        # xalign 0.5
                                        # imagebutton:
                                            # xalign 0.5
                                            # idle im.Sepia(img)
                                            # hover img
                                            # action Return(["fg", "upgrade", u])
                            # else:
                                # vbox:
                                    # null height 5
                                    # frame:
                                        # background Frame("content/gfx/frame/stat_box_proper.png", 5, 5)
                                        # xmaximum 200
                                        # xminimum 100
                                        # xalign 0.5
                                        # text "[u_name]   Active" color gold size 16 xalign 0.5
                                    # frame: 
                                        # background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                                        # xmaximum 100
                                        # xminimum 100
                                        # xalign 0.5
                                        # imagebutton:
                                            # xalign 0.5
                                            # idle im.Sepia(img)
                                            # hover img
                                            # action NullAction()
            elif stats_display == "Team Builder":
                null height 20
                vbox:
                    style_group "wood"
                    xalign 0.5
                    button:
                        xysize (150, 40)
                        align (0.5, 0.5)
                        action SetScreenVariable("team_display", "Team")
                        text "[hero.name]" size 15
                    button:
                        xysize (150, 40)
                        align (0.5, 0.5)
                        action SetScreenVariable("team_display", "Guild")
                        text "Guild Members" size 15
                    frame:
                        background Frame("content/gfx/frame/p_frame5.png", 15, 15)
                        xysize(220, 600)
                        # side "c r":
                            # maximum(220, 600)
                            # id "team_dg"
                            # viewport id "team_dg":
                                # draggable True
                                # mousewheel True
                                # hbox:
                                    # xalign 0.5
                                    # spacing 5
                                    # ysize 10000
                                    # box_wrap True
                                    # xsize 200
                                    # if team_display == "Team":
                                        # for girl in fg_drags.get_page_content():
                                            # $ index = fg_drags.get_page_content().index(girl)
                                            # $ img = girl.show("portrait", resize=(70, 70), cache=True)
                                            # vbox:
                                                # spacing 5
                                                # frame:
                                                    # xalign 0.5
                                                    # background Frame("content/gfx/frame/p_frame5.png", 15, 15)
                                                    # xysize(162, 120)
                                                    # imagebutton:
                                                        # align (0.5, 0.93)
                                                        # style "basic_choice2_button"
                                                        # idle img
                                                        # hover img
                                                        # selected_idle Transform(img, alpha=1.05)
                                                        # action NullAction()
                                                    # frame:
                                                        # xalign 0.5
                                                        # background Frame("content/gfx/frame/Mc_bg3.png", 5, 5)
                                                        # xysize(150, 10)
                                                        # ypadding 0
                                                        # if len(girl.name) > 10:
                                                            # text "{color=[gold]}[girl.name]" style "interactions_text" selected_color red size 14 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
                                                        # else:
                                                            # text "{color=[gold]}[girl.name]" style "interactions_text" selected_color red size 20 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
                                # vbar value YScrollValue("team_dg")
    
            elif stats_display == "Exploration":
                vbox: ### Gismo: Just example ###
                    null height 18
                    frame: 
                        style_group "content"
                        xalign 0.5
                        xysize (200, 50)
                        background Frame("content/gfx/frame/namebox5.png", 10, 10)
                        label (u"Maps") text_size 23 text_color ivory align(0.5, 0.8)
                    null height 15
                    frame:
                        $ img = ProportionalScale("content/gfx/bg/example/Teeny Woods.png", 200, 130)
                        background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xsize 170
                        imagebutton:
                            align (0.5, 0.93)
                            idle img
                            hover im.MatrixColor(img, im.matrix.brightness(0.10))
                            action NullAction()
                    frame:
                        xalign 0.5
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 5, 5)
                        xysize(207, 2)
                        ypos -128
                        text "{color=[gold]}Teeny Woods" style "interactions_text" size 18 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
    
                    null height -40
                    frame:
                        $ img = ProportionalScale("content/gfx/bg/example/The Vast Caves.jpg", 200, 130)
                        background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xsize 170
                        imagebutton:
                            align (0.5, 0.93)
                            idle img
                            hover im.MatrixColor(img, im.matrix.brightness(0.10))
                            action NullAction()
                    frame:
                        xalign 0.5
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 5, 5)
                        xysize(207, 2)
                        ypos -122
                        text "{color=[gold]}The Vast Caves" style "interactions_text" size 18 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
    
                    null height -40
                    frame:
                        $ img = ProportionalScale("content/gfx/bg/example/The Emerald Marsh.jpg", 200, 130)
                        background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xsize 170
                        imagebutton:
                            align (0.5, 0.93)
                            idle img
                            hover im.MatrixColor(img, im.matrix.brightness(0.10))
                            action NullAction()
                    frame:
                        xalign 0.5
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 5, 5)
                        xysize(207, 2)
                        ypos -135
                        text "{color=[gold]}The Emerald Marsh" style "interactions_text" size 18 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
                    null height -40
                    frame:
                        $ img = ProportionalScale("content/gfx/bg/example/Orcs Kingdom.jpg", 200, 130)
                        background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xsize 170
                        imagebutton:
                            align (0.5, 0.93)
                            idle img
                            hover im.MatrixColor(img, im.matrix.brightness(0.10))
                            action NullAction()
                    frame:
                        xalign 0.5
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.4), 5, 5)
                        xysize(207, 2)
                        ypos -122
                        text "{color=[gold]}Orcs Kingdom" style "interactions_text" size 18 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
                    null height -30
                    hbox:
                        xalign 0.5
                        spacing 20
                        add ProportionalScale("content/gfx/interface/buttons/arrow_button_metal_gold_up.png", 50, 50) #pos (150, -50)
                        add ProportionalScale("content/gfx/interface/buttons/arrow_button_metal_gold_down.png", 50, 50) #pos (150, -50)
            elif stats_display == "Log":
                # Log:
                vbox:
                    align (0.5, 0.5)
                    spacing 5
                    null height 4
                    frame: 
                        style_group "content"
                        xalign 0.5
                        xysize (205, 50)
                        background Frame("content/gfx/frame/namebox5.png", 10, 10)
                        label (u"Map") text_size 23 text_color ivory align(0.52, 0.8)
                    null height -10
                    frame:
                        $ img = ProportionalScale("content/gfx/bg/example/Teeny Woods.png", 200, 130)
                        background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.9), 10, 10)
                        xsize 170
                        imagebutton:
                            align (0.5, 0.93)
                            idle img
                            hover im.MatrixColor(img, im.matrix.brightness(0.10))
                            action NullAction()
                    frame:
                        xalign 0.5
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 5, 5)
                        xysize(207, 2)
                        ypos -132
                        text "{color=[gold]}Teeny Woods" style "interactions_text" size 18 outlines [(1, "#3a3a3a", 0, 0)] ypos 17
    
                    null height -55
                    hbox:
                        style_group "dropdown_gm2"
                        xalign 0.5
                        vbox:
                            spacing 1
                            xalign 0.5
                            button:
                                xysize (180, 18)
                                yalign 0.5
                                action Show("log1")
                                text "Stage 1" size 12 xpos -2
                                label (u"{color=#66CD00}Completed!") text_size 12 align (1.0, 0.5)
                            button:
                                xysize (180, 18)
                                yalign 0.5
                                action NullAction()
                                text "Stage 2" size 12 xpos -3
                                label (u"Retreat!") text_size 12 align (1.0, 0.5) text_color red
                            button:
                                xysize (180, 18)
                                yalign 0.5
                                action NullAction()
                                text "Stage 3" size 12 xpos -3
                            button:
                                xysize (180, 18)
                                yalign 0.5
                                action NullAction()
                                text "Stage 4" size 12 xpos -3
                            button:
                                xysize (180, 18)
                                yalign 0.5
                                action NullAction()
                                text "Stage 5" size 12 xpos -3
                            button:
                                xysize (180, 18)
                                yalign 0.5
                                action NullAction()
                                text "Stage 6" size 12 xpos -3
                            button:
                                xysize (180, 18)
                                yalign 0.5
                                action NullAction()
                                text "Stage 7" size 12 xpos -3
                            button:
                                xysize (180, 18)
                                yalign 0.5
                                action NullAction()
                                text "Stage 8" size 12 xpos -3
                            button:
                                xysize (180, 18)
                                yalign 0.5
                                action NullAction()
                                text "Stage 9" size 12 xpos -3
                            button:
                                xysize (180, 18)
                                yalign 0.5
                                action NullAction()
                                text "Stage 10" size 12 xpos -3
    
                    null height -5
                    frame: 
                        style_group "content"
                        xalign 0.5
                        xysize (205, 50)
                        background Frame("content/gfx/frame/namebox5.png", 10, 10)
                        label (u"Total") text_size 23 text_color ivory align(0.48, 0.8)
                    null height -10
                    frame:
                        background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                        xysize (190, 240)
                        vbox:
                            null height 6
                            style_group "stats"
                            spacing -5
                            null height 5
                            frame:
                                xalign 0.5
                                xsize 190
                                text "{size=-1}Killing monsters:" color ivory pos (3, -4)
                                label (u"{size=-5}8") style "stats_value_text" align (1.0, 0.5)
                            frame:
                                xalign 0.5
                                xsize 190
                                text "{size=-1}Experience:" color ivory pos (3, -4)
                                label (u"{size=-5}1273") style "stats_value_text" align (1.0, 0.5)
                            frame:
                                xalign 0.5
                                xsize 190
                                text "{size=-1}Gold:" color ivory pos (3, -4)
                                label (u"{size=-5}437") text_color gold style "stats_value_text" align (1.0, 0.5)
                            frame:
                                xalign 0.5
                                xsize 190
                                text "{size=-1}Items found:" color ivory pos (3, -4)
                                label (u"{size=-5}7") style "stats_value_text" align (1.0, 0.5)
    
                            null height 10
                            frame:
                                xalign 0.5
                                xsize 190
                                text "{size=-1}Reputation:" color ivory pos (3, -4)
                                label (u"{size=-5}+6") style "stats_value_text" align (1.0, 0.5)
                            frame:
                                xalign 0.5
                                xsize 190
                                text "{size=-1}Fame:" color ivory pos (3, -4)
                                label (u"{size=-5}+1") style "stats_value_text" align (1.0, 0.5)
                            frame:
                                xalign 0.5
                                xsize 190
                                text "{size=-1}Rank:" color ivory pos (3, -4)
                                label (u"{size=-5}+2") style "stats_value_text" align (1.0, 0.5)
    
                            null height 10
                            frame:
                                xalign 0.5
                                xsize 190
                                text "{size=-1}Lucky ticket:" color ivory pos (3, -4)
                                label (u"{size=-5}1") style "stats_value_text" align (1.0, 0.5)
    
    
    use top_stripe(True)
    
screen explorer: ### Gismo: Just example ###
    modal True
    zorder 1
    frame:
        pos (223, 42)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xysize (725,677)
        vbox:
            yfill True
            frame:
                xalign 0.5
                background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.9), 10, 10)
                xysize (730, 90)
                text "{color=[gold]}Peaceful Grove" style "interactions_text" size 18 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                hbox:
                    align (0.5, 0.45)
                    add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                    add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                    add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                    add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                    add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                button:
                    align (0.5, 0.95)
                    action NullAction()
                    text "Stage 1" size 14
            vbox:
                xfill True
                spacing 7
                frame:
                    style_group "content"
                    align (0.5, 0.015)
                    xysize (210, 30)
                    background Frame (Transform("content/gfx/frame/Namebox.png", alpha=0.9), 10, 10)
                    label (u"Team name") text_size 20 text_color ivory align(0.5, 0.5)
                hbox:
                    xfill True
                    spacing 2
                    add "content/gfx/bg/example/1.png" align (0.5, 0.5)
                    add "content/gfx/bg/example/2.png" align (0.5, 0.5)
                    add "content/gfx/bg/example/3.png" align (0.5, 0.5)
            hbox:
                frame:
                    background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xysize (340, 380)
                    yalign 1.0
                    frame:
                        style_group "content"
                        align (0.5, 0.015)
                        xysize (210, 40)
                        background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.6), 10, 10)
                        label (u"Enemies") text_size 23 text_color ivory align(0.5, 0.5)
                    vbox:    ### Need Side-scrolling ###
                        style_group "stats"
                        hbox:
                            yfill True
                            ypos 53
                            vbox:
                                spacing 2
                                xanchor 0
                                xmaximum 220
                                xfill True
                                hbox:
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 220
                                        text("Horrorbeast")
                                    frame:
                                        yalign 0.5
                                        xsize 50
                                        text("Lvl\n1-7") align (0.5, 0.5)
                                    frame:
                                        background Frame (Transform("content/gfx/interface/buttons/choice_buttons2.png", alpha=0.5), 5, 5)
                                        xsize 30
                                        add ProportionalScale("content/gfx/bg/example/Plague.png", 48, 48) 
                                hbox:
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 220
                                        text("Stonebeast")
                                    frame:
                                        yalign 0.5
                                        xsize 50
                                        text("Lvl\n3-9") align (0.5, 0.5)
                                    frame:
                                        background Frame (Transform("content/gfx/interface/buttons/choice_buttons2.png", alpha=0.5), 5, 5)
                                        xsize 30
                                        add ProportionalScale("content/gfx/bg/example/Earth.png", 48, 48)
                                hbox:
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 220
                                        text("???????????")
                                    frame:
                                        yalign 0.5
                                        xsize 50
                                        text("Lvl\n?-?") align (0.5, 0.5)
                                    frame:
                                        background Frame (Transform("content/gfx/interface/buttons/choice_buttons2.png", alpha=0.5), 5, 5)
                                        xsize 30
                                        add ProportionalScale("content/gfx/bg/example/unknown.png", 48, 48)
                                hbox:
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 220
                                        text("???????????")
                                    frame:
                                        yalign 0.5
                                        xsize 50
                                        text("Lvl\n?-?") align (0.5, 0.5)
                                    frame:
                                        background Frame (Transform("content/gfx/interface/buttons/choice_buttons2.png", alpha=0.5), 5, 5)
                                        xsize 30
                                        add ProportionalScale("content/gfx/bg/example/unknown.png", 48, 48)
                frame:
                    background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xysize (390, 380)
                    yalign 1.0
                    frame:
                        style_group "content"
                        align (0.5, 0.015)
                        xysize (200, 40)
                        background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.6), 10, 10)
                        label (u"Loot") text_size 23 text_color ivory align(0.5, 0.5)
                    vbox:    ### Need Side-scrolling ###
                        style_group "stats"
                        vbox:
                            xalign 0.5
                            ypos 53
                            vbox:
                                spacing 2
                                xanchor 0
                                xmaximum 210
                                xfill True
                                hbox:
                                    xfill True
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 210
                                        text("\"Lorekeeper\" Staff")
                                    frame:
                                        yalign 0.5
                                        xsize 140
                                        text("Weapon") xalign 0.5
                                    frame:
                                        yalign 0.5
                                        xsize 20
                                        add ProportionalScale("content/gfx/bg/example/legendary.png", 25, 25)
                            vbox:
                                spacing 2
                                xanchor 0
                                xmaximum 210
                                xfill True
                                hbox:
                                    xfill True
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 210
                                        text("Ashwood Flatbow")
                                    frame:
                                        yalign 0.5
                                        xsize 140
                                        text("Weapon") xalign 0.5
                                    frame:
                                        yalign 0.5
                                        xsize 20
                                        add ProportionalScale("content/gfx/bg/example/uncommon.png", 25, 25)
                            vbox:
                                spacing 2
                                xanchor 0
                                xmaximum 220
                                xfill True
                                hbox:
                                    xfill True
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 210
                                        text("???????")
                                    frame:
                                        yalign 0.5
                                        xsize 140
                                        text("???????") xalign 0.5
                                    frame:
                                        yalign 0.5
                                        xsize 20
                                        add ProportionalScale("content/gfx/bg/example/unknown2.png", 25, 25)
                            vbox:
                                spacing 2
                                xanchor 0
                                xmaximum 220
                                xfill True
                                hbox:
                                    xfill True
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 210
                                        text("Honey")
                                    frame:
                                        yalign 0.5
                                        xsize 140
                                        text("Consumable") xalign 0.5
                                    frame:
                                        yalign 0.5
                                        xsize 20
                                        add ProportionalScale("content/gfx/bg/example/common.png", 25, 25)
                            vbox:
                                spacing 2
                                xanchor 0
                                xmaximum 220
                                xfill True
                                hbox:
                                    xfill True
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 210
                                        text("???????")
                                    frame:
                                        yalign 0.5
                                        xsize 140
                                        text("???????") xalign 0.5
                                    frame:
                                        yalign 0.5
                                        xsize 20
                                        add ProportionalScale("content/gfx/bg/example/unknown2.png", 25, 25)
                            vbox:
                                spacing 2
                                xanchor 0
                                xmaximum 220
                                xfill True
                                hbox:
                                    xfill True
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 210
                                        text("???????")
                                    frame:
                                        yalign 0.5
                                        xsize 140
                                        text("???????") xalign 0.5
                                    frame:
                                        yalign 0.5
                                        xsize 20
                                        add ProportionalScale("content/gfx/bg/example/unknown2.png", 25, 25)
                            vbox:
                                spacing 2
                                xanchor 0
                                xmaximum 220
                                xfill True
                                hbox:
                                    xfill True
                                    spacing -3
                                    frame:
                                        yalign 0.5
                                        xsize 210
                                        text("???????")
                                    frame:
                                        yalign 0.5
                                        xsize 140
                                        text("???????") xalign 0.5
                                    frame:
                                        yalign 0.5
                                        xsize 20
                                        add ProportionalScale("content/gfx/bg/example/unknown2.png", 25, 25)
            hbox:
                align (0.5, 0.98)
                button:
                    style_group "basic"
                    action Hide("explorer")
                    minimum(50, 30)
                    align (0.5, 0.98)
                    text  "Back"
                button:
                    style_group "basic"
                    action NullAction()
                    minimum(50, 30)
                    align (0.5, 0.98)
                    text  "Launch!!! Days 1" # Gismo: AutoCalculate. 1 day per stage (1-5), 2 days per stage (6-10).
    
screen log1: ### Gismo: Just example ###
    modal True
    zorder 1
    default tt = Tooltip("")
    
    frame:
        pos (223, 42)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xysize (725,484)
        vbox:
            yfill True
            frame:
                xalign 0.5
                background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.9), 10, 10)
                xysize (730, 90)
                text "{color=[gold]}Peaceful Grove" style "interactions_text" size 18 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.01)
                hbox:
                    align (0.5, 0.45)
                    add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                    add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                    add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                    add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                    add ProportionalScale("content/gfx/bg/example/star1.png", 18, 18)
                button:
                    align (0.5, 0.95)
                    action NullAction()
                    text "Stage 1" size 14
            hbox:
                frame:
                    background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xysize (406, 320)
                    yalign 1.0
                    frame:
                        style_group "content"
                        align (0.5, 0.015)
                        xysize (200, 40)
                        background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.6), 10, 10)
                        label (u"Events") text_size 23 text_color ivory align(0.5, 0.5)
                    vbox:    ### Need Side-scrolling ###
                        style_group "stats"
                        xalign 0.5
                        ypos 53
                        spacing 2
                        xmaximum 390
                        xfill True
                        hbox:
                            xfill True
                            spacing -3
                            button:
                                style_group "dropdown_gm2"
                                action NullAction()
                                xsize 390
                                align (0.5, 0.98)
                                text("1:  Nothing happened") size 16
                        hbox:
                            xfill True
                            spacing -3
                            button:
                                style_group "dropdown_gm2"
                                action NullAction()
                                xsize 390
                                align (0.5, 0.98)
                                text("2:  You have found a {color=[gold]}treasure!{/color}") size 16
                        hbox:
                            xfill True
                            spacing -3
                            button:
                                style_group "dropdown_gm2"
                                action NullAction()
                                xsize 390
                                align (0.5, 0.98)
                                text("3:  {color=[red]}Monster{/color} appeared - Stonebeast!  {color=#66CD00}WIN{/color}") size 16
                        hbox:
                            xfill True
                            spacing -3
                            button:
                                style_group "dropdown_gm2"
                                action NullAction()
                                xsize 390
                                align (0.5, 0.98)
                                text("4:  Chest with {color=[red]}poison trap!{/color}") size 16
                        hbox:
                            xfill True
                            spacing -3
                            button:
                                style_group "dropdown_gm2"
                                action NullAction()
                                xsize 390
                                align (0.5, 0.98)
                                text("5:  Wandering {color=[gold]}merchant!{/color}") size 16
                        hbox:
                            xfill True
                            spacing -3
                            button:
                                style_group "dropdown_gm2"
                                action NullAction()
                                xsize 390
                                align (0.5, 0.98)
                                text("6:  You saved a {color=[gold]}girl!{/color}") size 16
                                hovered tt.action("You saved a girl from a hunting trap, and captured her as slave.\n{color=#66CD00}Nerin{/color} now your slave.")
                        hbox:
                            xfill True
                            spacing -3
                            button:
                                style_group "dropdown_gm2"
                                action NullAction()
                                xsize 390
                                align (0.5, 0.98)
                                text("7:  {color=#66CD00}Examine{/color} territory!") size 16
                        hbox:
                            xfill True
                            spacing -3
                            button:
                                style_group "dropdown_gm2"
                                action NullAction()
                                xsize 390
                                align (0.5, 0.98)
                                text("8:  You've found the {color=[gold]}gold +34!{/color}") size 16
                        hbox:
                            xfill True
                            spacing -3
                            button:
                                style_group "dropdown_gm2"
                                action NullAction()
                                xsize 390
                                align (0.5, 0.98)
                                text("9:  {color=[red]}BOSS{/color} appeared - The Blind Hunter!  {color=#66CD00}WIN{/color}") size 16
                        hbox:
                            xfill True
                            spacing -3
                            button:
                                style_group "dropdown_gm2"
                                action NullAction()
                                xsize 390
                                align (0.5, 0.98)
                                text("10:  Stage 1 {color=#66CD00}Completed!{/color}") size 16 xpos -2
                frame:
                    background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xysize (320, 320)
                    yalign 1.0
                    vbox:
                        align(0.5, 0.5)
                        frame:
                            style_group "content"
                            align (0.5, 0.015)
                            xysize (200, 40)
                            background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.6), 10, 10)
                            label (u"Story") text_size 23 text_color ivory align(0.5, 0.5)
                        # Tooltip Frame
                        frame:
                            align(0.5, 0.5)
                            background Frame("content/gfx/frame/ink_box.png", 10, 10)
                            xysize (300, 250)
                            xpadding 10
                            text (u"{=stats_text}{color=[bisque]}{size=-1}%s" % tt.value) outlines [(1, "#3a3a3a", 0, 0)]

            hbox:
                align (0.5, 0.98)
                button:
                    style_group "basic"
                    action Hide("log1")
                    minimum(50, 30)
                    align (0.5, 0.98)
                    text  "Back"
                button:
                    style_group "basic"
                    action NullAction()
                    minimum(50, 30)
                    align (0.5, 0.98)
                    text  "List of found items"
