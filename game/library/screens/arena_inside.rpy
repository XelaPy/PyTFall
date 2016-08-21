label arena_inside:
    
    # Music related:
    if not "arena_inside" in ilists.world_music:
        $ ilists.world_music["arena_inside"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("arena_inside")]
    play world choice(ilists.world_music["arena_inside"]) fadein 1.5
    
    scene bg arena_inside
    show screen arena_inside
    with fade
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    $ renpy.retain_after_load()
    
    while 1:
        
        $ result = ui.interact()
        
        if result[0] == 'control':
            if result[1] == "hide_vic":
                hide screen arena_aftermatch
            if result[1] == 'return':
                jump arena_inside_end
                
        elif result[0] == "show":
            if result[1] == "bestiary":
                hide screen arena_inside
                show screen arena_bestiary
            elif result[1] == "arena":
                hide screen arena_bestiary
                show screen arena_inside
                
        elif result[0] == "challenge":
            if result[1] == "dogfights":
                $ pytfall.arena.dogfight_challenge(result[2])
                # pytfall.arena.start_dogfight(result[2])
            elif result[1] == "match":
                $ pytfall.arena.setup = result[2]
                $ pytfall.arena.match_challenge(n=True)
            elif result[1] == "confirm_match":
                $ pytfall.arena.match_challenge()
            elif result[1] == "start_match":
                $ pytfall.arena.check_before_matchfight()
            elif result[1] == "start_chainfight":
                $ pytfall.arena.check_before_chainfight()
            elif result[1] == "chainfight":
                $ pytfall.arena.start_chainfight()

label arena_inside_end:
    stop world fadeout 1.5
    hide screen arena_inside
    jump arena_outside

init: # Main Screens:
    screen arena_inside():
        
        #use top_stripe(True)
        add "content/gfx/bg/locations/arena_inside.jpg"  xpos 100 ypos 35
        
        # Start match button:
        if day in hero.fighting_days:
            button:
                align (0.97, 0.5)
                xysize (200, 40)
                style "right_wood_button"
                action Return(["challenge", "start_match"])
                text "Start Match!" style "wood_text" xalign(0.4) size 20
                 
        # Kickass sign:
        frame:
            xalign .5
            ypos 39
            background Frame("content/gfx/frame/Mc_bg.png", 10, 10)
            xysize (725, 120)
            add Transform(Text("{=content}{size=30}{color=[crimson]}Get your ass kicked in our Arena!"), alpha=0.8) align (0.5, 0.5)
                    
        # LEFT FRAME:
        # Buttons:
        frame:
            style_group "content"
            pos (2, 39)
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=1.0), 10, 10)
            xysize (280, 682)
            has vbox align .5, .03 spacing 1
            
            # Beast Fights:
            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.7), 5, 5)
                padding 10, 10
                has vbox spacing 2
                
                frame:
                    xfill True
                    align .5, .5
                    background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                    label "{size=28}{color=[bisque]}== Beast Fights ==" xalign .5 text_outlines [(1, "#3a3a3a", 0, 0)]
                hbox:
                    style_group "basic"
                    align .5, .5
                    spacing 5
                    textbutton "{size=20}{color=[black]}Bestiary":
                        action Return(["show", "bestiary"])
                    textbutton "{size=20}{color=[black]}Survival!":
                        action Return(["challenge", "start_chainfight"])
                    
            # Ladders (Just Info):
            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.7), 5, 5)
                padding 10, 10
                has vbox spacing 2
                
                frame:
                    xfill True
                    align .5, .5
                    background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                    label "{size=28}{color=[bisque]}== Ladders ==" xalign .5 text_outlines [(1, "#3a3a3a", 0, 0)]
                hbox:
                    style_group "basic"
                    align .5, .5
                    spacing 5
                    textbutton "{size=20}{color=[black]}1v1":
                        action Show("arena_lineups", transition=dissolve, container=pytfall.arena.lineup_1v1)
                    textbutton "{size=20}{color=[black]}2v2":
                        action Show("arena_lineups", transition=dissolve, container=pytfall.arena.lineup_2v2)
                    textbutton "{size=20}{color=[black]}3v3":
                        action Show("arena_lineups", transition=dissolve, container=pytfall.arena.lineup_3v3)

            # Official matches:
            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.7), 5, 5)
                padding 10, 10
                has vbox spacing 2
            
                frame:
                    xfill True
                    align .5, .5
                    background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                    label "{size=28}{color=[bisque]}== Matches ==" xalign .5 text_outlines [(1, "#3a3a3a", 0, 0)]
                hbox:
                    align .5, .5
                    spacing 5
                    style_group "basic"
                    textbutton "{size=20}{color=[black]}1v1":
                        action Show("arena_matches", container=pytfall.arena.matches_1v1, transition=dissolve, vs_img=ProportionalScale("content/gfx/interface/images/vs_3.png", 130, 130))
                    textbutton "{size=20}{color=[black]}2v2":
                        action Show("arena_matches", container=pytfall.arena.matches_2v2, transition=dissolve, vs_img=ProportionalScale("content/gfx/interface/images/vs_2.png", 130, 130))
                    textbutton "{size=20}{color=[black]}3v3":
                        action Show("arena_matches", container=pytfall.arena.matches_3v3, transition=dissolve, vs_img=ProportionalScale("content/gfx/interface/images/vs_4.png", 130, 130))
     
            # Dogfights:
            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.7), 5, 5)
                padding 10, 10
                has vbox spacing 2
                
                frame:
                    xfill True
                    align .5, .5
                    background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                    label ("{size=28}{color=[bisque]}== Dogfights ==") xalign .5 text_outlines [(1, "#3a3a3a", 0, 0)]
                hbox:
                    style_group "basic"
                    align .5, .5
                    spacing 5
                    textbutton "{size=20}{color=[black]}1v1":
                        action Show("arena_dogfights", transition=dissolve, container=pytfall.arena.dogfights_1v1)
                    textbutton "{size=20}{color=[black]}2v2":
                        action Show("arena_dogfights", transition=dissolve, container=pytfall.arena.dogfights_2v2)
                    textbutton "{size=20}{color=[black]}3v3":
                        action Show("arena_dogfights", transition=dissolve, container=pytfall.arena.dogfights_3v3)
                        
        # RIGHT FRAME::
        # Hero stats + Some Buttons:
        frame:
            xalign 1.0
            ypos 39
            background Frame("content/gfx/frame/p_frame5.png", 5, 5)
            xysize 282, 682
            style_prefix "proper_stats"
            has vbox align .5, .0
            
            null height 10
            
            # Player Stats:
            frame:
                xalign .5
                padding 5, 1
                background Frame("content/gfx/frame/ink_box.png", 5, 5)
                has hbox spacing 2
                
                frame:
                    background Frame("content/gfx/frame/MC_bg3.png", 5, 5)
                    $ img = hero.show("portrait", resize=(95, 95), cache=True)
                    padding 2, 2
                    yalign .5
                    add img align .5, .5
                    
                # Name + Stats:
                frame:
                    padding 8, 2
                    background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=0.6), 5, 5)
                    xsize 155
                    has vbox
                    
                    label "[hero.name]":
                        text_size 16
                        text_bold True
                        yalign .03
                        text_color ivory
                        
                    fixed: # HP:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/hp1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value hero.health
                            range hero.get_max("health")
                            thumb None
                            xysize (150, 20)
                        text "HP" size 14 color ivory bold True xpos 8
                        if hero.health <= hero.get_max("health")*0.2:
                            text "[hero.health]" size 14 color red style_suffix "value_text" xpos 125 yoffset -8
                        else:
                            text "[hero.health]" size 14 color ivory bold True style_suffix "value_text" xpos 125 yoffset -8
            
                    fixed: # MP:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/mp1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value hero.mp
                            range hero.get_max("mp")
                            thumb None
                            xysize (150, 20)
                        text "MP" size 14 color ivory bold True xpos 8
                        if hero.mp <= hero.get_max("mp")*0.2:
                            text "[hero.mp]" size 14 color red bold True style_suffix "value_text" xpos 125 yoffset -8
                        else:
                            text "[hero.mp]" size 14 color ivory bold True style_suffix "value_text" xpos 125 yoffset -8
            
                    fixed: # VP:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/vitality1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value hero.vitality
                            range hero.get_max("vitality")
                            thumb None
                            xysize (150, 20)
                        text "VP" size 14 color ivory bold True xpos 8
                        if hero.vitality <= hero.get_max("vitality")*0.2:
                            text "[hero.vitality]" size 14 color red bold True style_suffix "value_text" xpos 125 yoffset -8
                        else:
                            text "[hero.vitality]" size 14 color ivory bold True style_suffix "value_text" xpos 125 yoffset -8
                                
            # Rep:
            frame:
                background im.Scale("content/gfx/frame/frame_bg.png", 270, 110)
                xysize (270, 110)
                label "Reputation: [hero.arena_rep]" text_size 25 text_color ivory align .5, .5
                
            # Buttons:
            frame:
                background im.Scale("content/gfx/frame/frame_bg.png", 270, 110)
                style_group "basic"
                xysize (270, 110)
                vbox:
                    align (0.5, 0.5)
                    spacing 10
                    textbutton "Show Daily Report":
                        xalign 0.5
                        action [ShowTransient("arena_report")]
                    textbutton "Reputation Ladder":
                        xalign 0.5
                        action [ShowTransient("arena_rep_ladder")]
                                
        use top_stripe(True)
                 
    screen arena_matches(container=None, vs_img=None):
        # Screens used to display and issue challenges in the official matches inside of Arena:
        modal True
        zorder 1
        
        frame:
            background Frame("content/gfx/frame/p_frame52.png", 10, 10)
            xysize (721, 565)
            at slide(so1=(0, 1200), t1=.7, eo2=(0, 1200), t2=.7)
            pos (280, 154)
            
            side "c r":
                pos (5, 5)
                maximum (710, 515)
                viewport id "vp_matches":
                    draggable True
                    mousewheel True
                    child_size (710, 1000)
                    has vbox spacing 5
                    
                    # for lineup in pytfall.arena.matches_3v3:
                    for lineup in container:
                        if lineup[1]:
                            frame:
                                style_group "content"
                                xalign 0.5
                                xysize (690, 150)
                                background Frame(Transform("content/gfx/frame/p_frame7.png", alpha=1.0), 10, 10)
                                # Day of the fight:
                                has hbox xalign 0.5
                                fixed:
                                    xysize (50, 50)
                                    label "[lineup[2]]":
                                        align (0.5, 0.5)
                                        text_color red
                                        text_size 35
                                # Challenge button:
                                if not lineup[0]:
                                    textbutton "{size=+10}{color=[red]}Challenge!":
                                        background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                                        hover_background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=1), 10, 10)
                                        yalign 0.5
                                        xysize (250, 150)
                                        action Return(["challenge", "match", lineup])
                                # Or we show the team that challenged:
                                else:
                                    frame:
                                        background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                                        xysize (250, 150)
                                        xpadding 10
                                        ypadding 10
                                        yalign 0.5
                                        frame:
                                            xfill True
                                            align (0.5, 0.01)
                                            background Frame("content/gfx/frame/stat_box_proper.png", 5, 5)
                                            $ name = lineup[0][0].nickname if len(lineup[0]) == 1 else lineup[0].name
                                            label "[name]" align (0.5, 0) text_size 25 text_style "stats_text" text_color gold
                                        hbox:
                                            spacing 3
                                            align (0.5, 1.0)
                                            for fighter in lineup[0]:
                                                frame:
                                                    background Frame ("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                                                    add fighter.show("portrait", resize=(60, 60))
                                    
                                add vs_img yalign 0.5
                            
                                # Waiting for the challenge or been challenged by former:
                                frame:
                                    background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                                    xysize (250, 150)
                                    xpadding 10
                                    ypadding 10
                                    yalign 0.5
                                    frame:
                                        xfill True
                                        align (0.5, 0.01)
                                        background Frame("content/gfx/frame/stat_box_proper.png", 5, 5)
                                        $ name = lineup[1][0].nickname if len(lineup[1]) == 1 else lineup[1].name
                                        label "[name]" align (0.5, 0) text_size 25 text_style "stats_text" text_color gold
                                    hbox:
                                        spacing 3
                                        align (0.5, 1.0)
                                        for fighter in lineup[1]:
                                            frame:
                                                background Frame ("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                                                add fighter.show("portrait", resize=(60, 60))
                    
                vbar value YScrollValue("vp_matches")
            
            button:
                style_group "basic"
                action Hide("arena_matches")
                minimum(50, 30)
                align (0.5, 0.9995)
                text  "OK"
                
            
    screen arena_lineups(container):
        modal True
        zorder 1
        
        frame:
            background Frame("content/gfx/frame/p_frame52.png", 10, 10)
            at slide(so1=(0, 1200), t1=.7, eo2=(0, 1200), t2=.7)
            style_group "content"
            pos (280, 154)
            xysize (721, 565)
            
            side "c r":
                pos (5, 5)
                maximum (710, 515)
                viewport id "arena_lineups":
                    draggable True
                    mousewheel True
                    child_size (700, 1000)
                    has vbox spacing 5
                    for index, team in enumerate(container):
                        $ index = index+1
                        frame:
                            xalign 0.5
                            xysize (695, 60)
                            background Frame(Transform("content/gfx/frame/p_frame7.png", alpha=1.0), 10, 10)
                            has hbox spacing 5
                            fixed:
                                xysize (60, 60)
                                align (0.5, 0.5)
                                label "[index]":
                                    text_color red
                                    text_size 35
                                    align (0.5, 0.5)
                            if team:
                                $ name = team[0].nickname if len(team) == 1 else team.name
                                hbox:
                                    align (0.5, 0.5)
                                    spacing 3
                                    ysize 55
                                    for fighter in team:
                                        frame:
                                            background Frame ("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                                            add fighter.show("portrait", resize=(60, 60), cache=True) yalign 0.5
                                null width 12
                                frame:
                                    xfill True
                                    align (0.5, 0.5)
                                    xminimum 300
                                    background Frame("content/gfx/frame/stat_box_proper.png", 5, 5)
                                    label "[name]" align (0.5, 0.5) text_size 25 text_style "stats_text" text_color gold
                                    
                vbar value YScrollValue("arena_lineups")
                
            button:
                style_group "basic"
                action Hide("arena_lineups")
                minimum(50, 30)
                align (0.5, 0.9995)
                text  "OK"
                
            
    screen arena_rep_ladder():
        modal True
        zorder 1
        
        frame:
            background Frame("content/gfx/frame/p_frame52.png", 10, 10)
            xysize (721, 565)
            at slide(so1=(0, 1200), t1=.7, eo2=(0, 1200), t2=.7)
            pos (280, 154)
            
            side "c r":
                pos (5, 5)
                maximum (710, 515)
                viewport id "arena_rep_vp":
                    draggable True
                    mousewheel True
                    child_size (700, 1000)
                    has vbox spacing 5
                    for index, fighter in enumerate(pytfall.arena.ladder):
                        $index = index+1
                        frame:
                            style_group "content"
                            xalign 0.5
                            xysize (690, 60)
                            background Frame(Transform("content/gfx/frame/p_frame7.png", alpha=1.0), 10, 10)
                            has hbox spacing 20
                            textbutton "{color=[red]}[index]":
                                ypadding 5
                                background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                                xysize (50, 50)
                                text_size 20
                                xfill True
                            if fighter:    
                                frame:
                                    xfill True
                                    align (0.5, 0.5)
                                    background Frame("content/gfx/frame/stat_box_proper.png", 5, 5)
                                    hbox:
                                        xfill True
                                        align (0.5, 0.5)
                                        text("[fighter.name]") align (0.03, 0.5) size 25 style "stats_text" color gold
                                        text("[fighter.arena_rep]") align (0.99, 0.5) size 20 style "stats_value_text" color gold
                    
                vbar value YScrollValue("arena_rep_vp")
            
            button:
                style_group "basic"
                action Return([''])
                minimum(50, 30)
                align (0.5, 0.9995)
                text  "OK"
            
    
    screen arena_dogfights(container={}):
        modal True
        zorder 1
        
        frame:
            style_group "content"
            background Frame("content/gfx/frame/p_frame52.png", 10, 10)
            xysize (721, 565)
            at slide(so1=(0, 1200), t1=.7, eo2=(0, 1200), t2=.7)
            pos (280, 154)
            
            side "c r":
                pos (5, 5)
                maximum (710, 515)
                viewport:
                    id "vp_dogfights"
                    draggable True
                    mousewheel True
                    child_size (700, 1000)
                    has vbox spacing 5
                    for team in container:
                        frame:
                            style_group "content"
                            xalign 0.5
                            xysize (695, 150)
                            background Frame(Transform("content/gfx/frame/p_frame7.png", alpha=1.0), 10, 10)
                            has hbox xalign 0.5
                            textbutton "{size=+7}Ask for a Fight":
                                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                                hover_background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=1), 10, 10)
                                xysize (250, 150)
                                yalign 0.5
                                action Return(["challenge", "dogfights", team])
                                text_color bisque
                                text_outlines [(1, "#3a3a3a", 0, 0)]
                                
                            add ProportionalScale("content/gfx/interface/images/vs_1.png", 130, 130) yalign 0.5
                        
                            frame:
                                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                                xysize (250, 150)
                                xpadding 10
                                ypadding 10
                                yalign 0.5
                            
                                frame:
                                    xfill True
                                    align (0.5, 0.01)
                                    background Frame("content/gfx/frame/stat_box_proper.png", 5, 5)
                                    $ name = team[0].nickname if len(team) == 1 else team.name
                                    label ("[name]") align(0.5, 0.0) text_size 25 text_style "stats_text" text_color gold
                                hbox:
                                    spacing 3
                                    align(0.5, 1.0)
                                    for fighter in team:
                                        frame:
                                            background Frame ("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                                            add fighter.show("portrait", resize=(60, 60))
                    
                vbar value YScrollValue("vp_dogfights")
            
            button:
                style_group "basic"
                action Hide("arena_dogfights")
                minimum(50, 30)
                align (0.5, 0.9995)
                text  "OK"
            
    screen arena_bestiary():
        default in_focus_mob = False
        
        add("content/gfx/bg/locations/arena_bestiary.jpg") at fade_in_out()
        hbox:
            viewport:
                at fade_in_out()
                xysize 995, 720
                draggable True
                mousewheel True
                scrollbars "vertical"
                has hbox xysize 995, 720 box_wrap True spacing 2
                
                # Prepare the list of mobs:
                $ _mobs = sorted(mobs.values(), key=itemgetter("min_lvl"))
                for data in _mobs:
                    $ creature = data["name"]
                    $ img = ProportionalScale(data["battle_sprite"], 200, 200)
                    vbox:
                        frame:
                            background "content/gfx/frame/bst.png"
                            xysize 230, 240
                            if not data["defeated"]: # <------------------------------ Note for faster search, change here to test the whole beasts screen without the need to kill mobs
                                vbox:
                                    xalign .5
                                    xysize 230, 240
                                    spacing 2
                                    text "-Unknown-" xalign .5  style "TisaOTM" color indianred
                                    add im.Twocolor(img, black, black) align .5, .6
                            else:
                                vbox:
                                    xalign 0.5
                                    xysize 230, 240
                                    spacing 2
                                    text creature xalign .5  style "TisaOTM" color gold
                                    imagebutton:
                                        align .5, .6
                                        idle img
                                        hover (im.MatrixColor(img, im.matrix.brightness(0.25)))
                                        action SetScreenVariable("in_focus_mob", creature)
                        null height 2
                    
            null width 1
            
            if in_focus_mob:
                $ data = mobs[in_focus_mob]
                $ img = ProportionalScale(data["battle_sprite"], 200, 200)
                $ portrait = im.Scale(data["portrait"], 100, 100)
                frame:
                    background Frame("content/gfx/frame/p_frame5.png")
                    xysize 277, 720
                    xoffset -5
                    has vbox
                    
                    null height 5
                    hbox:
                        frame:
                            xalign .5
                            yalign 0.0
                            background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                            add portrait
                    
                        vbox:
                            style_group "proper_stats"
                            xalign 0.0
                            spacing 1
                            frame:
                                xalign 0.5
                                yfill True
                                background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.6), 10, 10)
                                xysize (145, 30)
                                text (u"{color=#CDAD00} Race") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.7)
                            frame:
                                xalign 0.5
                                yfill True
                                xysize (148, 30)
                                text (data["race"]) xalign 0.5 yalign 0.5 style "stats_value_text" color "#79CDCD"

                    
                    null height 5
                    hbox:
                        frame:
                            $ els = [traits[el] for el in data["traits"] if traits[el] in tgs.elemental]
                            $ els_transforms = [Transform(e.icon, size=(100, 100)) for e in els]
                            $ other_traits = data["traits"]
                            style_group "content"
                            background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 10, 10)
                            xysize 110, 110
                            xalign .5
                            
                            $ x = 0
                            $ els_args = [Transform(i, crop=(100/len(els_transforms)*els_transforms.index(i), 0, 100/len(els), 100), subpixel=True, xpos=(x + 100/len(els)*els_transforms.index(i))) for i in els_transforms]
                            $ f = Fixed(*els_args, xysize=(100, 100))
                            add f align (0.5, 0.5) 
                            add ProportionalScale("content/gfx/interface/images/elements/hover.png", 100, 100) align (0.5, 0.5)
                        vbox:
                            style_group "proper_stats"
                            xalign 0.0
                            spacing 1
                            frame:
                                xalign 0.5
                                yfill True
                                background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.6), 10, 10)
                                xysize (145, 30)
                                text (u"{color=#CDAD00} Class") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] align (0.5, 0.7)
                            for t in data["basetraits"]:
                                frame:
                                    xalign 0.5
                                    xysize (148, 30)
                                    yfill True
                                    text t xalign 0.5 yalign 0.5 style "stats_value_text" color "#79CDCD"
                    
                    # Stats:
                    frame:
                        xalign 0.5
                        yfill True
                        background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.6), 10, 10)
                        xysize (260, 30)
                        text (u"{color=#CDAD00} Relative stats") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] xalign 0.5# align (0.5, 1.0)
                    hbox:
                        null width 2
                        vbox:
                            $ stats = ["attack", "defence", "magic", "agility"]
                            style_group "proper_stats"
                            box_wrap 1
                            spacing 1
                            for stat in stats:
                                frame:
                                    xysize (130, 22)
                                    xalign 0.5
                                    text '{}'.format(stat.capitalize()) xalign 0.02 color "#43CD80"
                                    text str(data["stats"][stat]) xalign 0.98 style "stats_value_text" color "#79CDCD"
                        null width 2
                        vbox:
                            $ stats = ["charisma", "constitution", "intelligence", "luck"]
                            style_group "proper_stats"
                            box_wrap 1
                            spacing 1
                            for stat in stats:
                                frame:
                                    xysize (130, 22)
                                    xalign 0.5
                                    text '{}'.format(stat.capitalize()) xalign 0.02 color "#43CD80"
                                    text str(data["stats"][stat]) xalign 0.98 style "stats_value_text" color "#79CDCD"
                    null height 5
                    
                    # Bottom Viewport:
                    viewport:
                        xalign .5
                        xoffset 3
                        edgescroll (100, 100)
                        draggable True
                        mousewheel True
                        xysize 278, 350
                        child_size 278, 1000
                        has vbox
                        # Desc:
                        frame:
                            xalign .5
                            yfill True
                            background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.6), 10, 10)
                            xysize (155, 30)
                            text (u"{color=#CDAD00} Description") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] xalign 0.5
                        vbox:
                            style_group "proper_stats"
                            xalign .5
                            if data["desc"]:
                                    frame:
                                        xalign 0.5
                                        xsize 261
                                        text (data["desc"]) size 14 xalign 0.5 yalign 0.5 style "stats_value_text" color "#79CDCD"
                            else:
                                frame:
                                    xalign 0.5
                                    xysize (150, 30)
                                    yfill True
                                    text "-None-" size 17 xalign 0.5 yalign 0.5 style "stats_value_text" color indianred
                        hbox:
                        # Attacks:
                            vbox:
                                frame:
                                    xalign 0.5
                                    yfill True
                                    background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.6), 10, 10)
                                    xysize (130, 30)
                                    text (u"{color=#CDAD00} Attacks") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] xalign 0.5
                                    
                                vbox:
                                    style_group "proper_stats"
                                    xalign .5
                                    if data["attack_skills"]:
                                        for s in sorted(data["attack_skills"]):
                                            frame:
                                                xalign 0.5
                                                xysize (130, 22)
                                                yfill True
                                                text s size 16 xalign 0.5 yalign 0.5 style "stats_value_text" color "#79CDCD"
                                    else:
                                        frame:
                                            xalign 0.5
                                            xysize (130, 22)
                                            yfill True
                                            text "-None-" size 17 xalign 0.5 yalign 0.5 style "stats_value_text" color indianred
                        
                        # Spells:
                            vbox:
                                frame:
                                    xalign 0.5
                                    yfill True
                                    background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.6), 10, 10)
                                    xysize (130, 30)
                                    text (u"{color=#CDAD00} Spells") font "fonts/Rubius.ttf" size 20 outlines [(1, "#3a3a3a", 0, 0)] xalign 0.5
                                    
                                vbox:
                                    style_group "proper_stats"
                                    xalign .5
                                    spacing 1
                                    if data["magic_skills"]:
                                        for s in sorted(data["magic_skills"]):
                                            frame:
                                                xalign 0.5
                                                xysize (130, 22)
                                                yfill True
                                                text s size 16 xalign 0.5 yalign 0.5 style "stats_value_text" color "#79CDCD"
                                    else:
                                        frame:
                                            xalign 0.5
                                            xysize (130, 22)
                                            yfill True
                                            text "-None-" size 17 xalign 0.5 yalign 0.5 style "stats_value_text" color indianred
        imagebutton:
            pos (1233, 670)
            idle im.Scale("content/gfx/interface/buttons/close2.png", 35, 35)
            hover im.Scale("content/gfx/interface/buttons/close2_h.png", 35, 35)
            action Return(["show", "arena"])
            
    screen arena_aftermatch(w_team, l_team, condition):
        modal True
        zorder 2
        
        on "show" action If(condition=="Victory", true=Play("music", "content/sfx/sound/world/win_screen.mp3"))
        
        default winner = w_team[0]
        default loser = l_team[0]
            
        if hero.team == w_team:
            add "content/gfx/images/battle/victory_l.png" at move_from_to_pos_with_ease(start_pos=(-config.screen_width/2, 0), end_pos=(0, 0), t=0.7, wait=0)
            add "content/gfx/images/battle/victory_r.png" at move_from_to_pos_with_ease(start_pos=(config.screen_width/2, 0), end_pos=(0, 0), t=0.7)
            add "content/gfx/images/battle/battle_c.png" at fade_from_to(start_val=0.5, end_val=1.0, t=2.0, wait=0)
            add "content/gfx/images/battle/victory.png":
                align (0.5, 0.5)
                at simple_zoom_from_to_with_easein(start_val=50.0, end_val=1.0, t=2.0)
        else:
            add "content/gfx/images/battle/defeat_l.png" at move_from_to_pos_with_ease(start_pos=(-config.screen_width/2, 0), end_pos=(0, 0), t=0.7)
            add "content/gfx/images/battle/defeat_r.png" at move_from_to_pos_with_ease(start_pos=(config.screen_width/2, 0), end_pos=(0, 0), t=0.7)
            add "content/gfx/images/battle/battle_c.png" at fade_from_to(start_val=0.5, end_val=1.0, t=2.0, wait=0)
            add "content/gfx/images/battle/defeat.png":
                align (0.5, 0.5)
                at simple_zoom_from_to_with_easein(start_val=50.0, end_val=1.0, t=2.0)
                
        # timer 10 action Function(renpy.music.stop, channel="music", fadeout=1.0), Return(["control", "hide_vic"])
        
        frame:
            background Null()
            xsize 95
            xpos 2
            yalign 0.5
            xpadding 8
            ypadding 8
            xmargin 0
            ymargin 0
            has vbox spacing 5 align(0.5, 0.5) box_reverse True
            $ i = 0
            for member in w_team :
                $ img = member.show("portrait", resize=(70, 70), cache=True)
                fixed:
                    align (0.5, 0.5)
                    xysize (70, 70)
                    imagebutton:
                        at fade_from_to(start_val=0, end_val=1.0, t=2.0, wait=i)
                        ypadding 1
                        xpadding 1
                        xmargin 0
                        ymargin 0
                        align (0.5, 0.5)
                        style "basic_choice2_button"
                        idle img
                        hover img
                        selected_idle Transform(img, alpha=1.05)
                        action SetScreenVariable("winner", member), With(dissolve)
                    $ i = i + 1
            
        frame:
            background Null()
            xsize 95
            align (1.0, 0.5)
            xpadding 8
            ypadding 8
            xmargin 0
            ymargin 0
            has vbox spacing 5 align(0.5, 0.5)
            $ i = 0
            for member in l_team:
                $ img = member.show("portrait", resize=(70, 70), cache=True)
                fixed:
                    align (0.5, 0.5)
                    xysize (70, 70)
                    imagebutton:
                        at fade_from_to(start_val=0, end_val=1.0, t=2.0, wait=i)
                        ypadding 1
                        xpadding 1
                        xmargin 0
                        ymargin 0
                        align (0.5, 0.5)
                        style "basic_choice2_button"
                        idle img
                        hover img
                        selected_idle Transform(img, alpha=1.05)
                        action NullAction()
                    $ i = i + 1
                    
        button:
            align (0.5, 0.63)
            style_group "pb"
            action [Function(renpy.music.stop, channel="music", fadeout=1.0), Return(["control", "hide_vic"])]
            text "Continue" style "pb_button_text"
         
        # Winner Details Display on the left:
        if winner.combat_stats == "K.O.":
            frame:
                at fade_from_to_with_easeout(start_val=.0, end_val=1.0, t=.9, wait=0)
                background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                add im.Sepia(winner.show('fighting', resize=(200, 200), cache=True)) 
                align .2, .2
        else:
            frame:
                at fade_from_to_with_easeout(start_val=.0, end_val=1.0, t=.9, wait=0)
                background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                add winner.show("fighting", resize=(200, 200), cache=True)
                align .2, .2
                
            if hero.team == w_team: # Show only if we won...
                frame:
                    style_group "proper_stats"
                    align (0.2, 0.5)
                    background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                    xpadding 12
                    ypadding 12
                    xmargin 0
                    ymargin 0
                    has vbox spacing 1
                    for stat in winner.combat_stats:
                        frame:
                            xalign 0.5
                            xysize (190, 27)
                            text '{}'.format(stat.capitalize()) xalign 0.02 color "#79CDCD"
                            label str(winner.combat_stats[stat]) xalign 1.0 yoffset -1
        
        # Looser Details Display on the left:
        if loser.combat_stats == "K.O.":
            add im.Sepia(loser.show("fighting", resize=(200, 200), cache=True)) align (0.2, 0.2)
        else:
            add loser.show("fighting", resize=(200, 200), cache=True) align (0.8, 0.2)
            
        add "content/gfx/frame/h1.png"
        
    screen confirm_match():
        modal True
        zorder 1
        
        frame:
            align(0.5, 0.5)
            minimum(300, 200)
            maximum(300, 200)
            xfill True
            yfill True
            
            text("{size=-5}Are you sure you want to schedule a fight? Backing out of it later will mean a hit on reputation...") align(0.5, 0.1)
            
            hbox:
                align(0.5, 0.85)
                spacing 40
                textbutton "No":
                    action Hide("confirm_match")
                textbutton "Yes":
                    action Return(["challenge", "confirm_match"])
                
    screen arena_report():
        
        frame:
            pos (280, 154)
            at fade_in_out(t1=1.5, t2=1.5)
            background im.Scale("content/gfx/frame/frame_dec_1.png", 720, 580)
            minimum(720, 580)
            maximum(720, 580)
            xfill True
            yfill True
            hbox:
                align(0.5, 0.2)
                minimum(650, 550)
                maximum(650, 550)
                text("{size=-4}%s"%pytfall.arena.daily_report)
                
            button:
                style_group "basic"
                action Hide("arena_report")
                minimum(50, 30)
                align (0.5, 0.9)
                text  "OK"
                    
    screen arena_stats(member):
        hbox at arena_stats_slide:
            align (1.0, 1.0)
            if not isinstance(member.combat_stats, basestring):
                vbox:
                    spacing 1
                    xmaximum 100
                    xminimum 100
                    xfill True
                    for stat in member.combat_stats:
                        text("{size=-5}{=della_respira}{color=[red]}%s:"%(stat.capitalize()))
                vbox:
                    spacing 1
                    for stat in member.combat_stats:
                        text("{size=-5}{color=[red]}%s"%(member.combat_stats[stat]))
            else:
                text("{size=+20}{color=[red]}K.O.")
            
init: # ChainFights vs Mobs:
    screen chain_fight():
        zorder 1
        
        add "content/gfx/bg/locations/arena_bestiary.jpg"
        
        if not pytfall.arena.cf_mob:
            text "Choose your Fight!":
                style "arena_header_text"
                align (0.5, 0.1)
                size 50
                
            vbox:
                style "menu"
                spacing 1
                align (0.5, 0.55)
                for setup in pytfall.arena.chain_fights_order:
                    button:
                        style "menu_choice_button_blue"
                        action [SetField(pytfall.arena, "result", setup), Return("Bupkis")]
                        
                        text "[setup]" style "menu_choice"
                        
                button:
                    style "menu_choice_button"
                    action [SetField(pytfall.arena, "result", "break"), Return("Bupkis")]
                    
                    text "Back" style "menu_choice" 
                    
                key "mousedown_3" action [SetField(pytfall.arena, "result", "break"), Return("Bupkis")]
        else:
            timer 0.5 action [SetField(pytfall.arena, "result", "break"), Return("Bupkis")]
        
    screen arena_minigame(range, interval, length_multiplier, d):
        zorder 2
        modal True
        
        default reverse = False
        default rolled = False
        default value = 0
        default run = True
        default step = 2
        
        if rolled:
            timer 1.0 action Return()
        
        add "bg mc_setup"
        
        # Bonus Roll: ===========================================================================>>>
        if pytfall.arena.cf_bonus:
            if run:
                if reverse:
                    if value == 0:
                        $ reverse = False
                        timer interval action SetScreenVariable("value", value + step) repeat True
                    else:
                        timer interval action SetScreenVariable("value", value - step) repeat True
                else:
                    if value == range:
                        $ reverse = True
                        timer interval action SetScreenVariable("value", value - step) repeat True
                    else:
                        timer interval action SetScreenVariable("value", value + step) repeat True
            
            python:
                y_w = 0
                y_r = d["white"] * length_multiplier
                y_b = d["blue"] + y_r
                y_g = d["green"] + y_b
                y_w2 = y_g + d["white"]
                
            frame:
                background Frame(im.Twocolor("content/gfx/interface/bars/thvslider_thumb.png", white, red), 0, 0)
                xysize(4, 4)
                pos(110, 245 + value * length_multiplier)
                
            vbox:
                pos (70, 250)
                add im.Scale("content/gfx/interface/bars/testbar.png", 40, d["white"] * length_multiplier)
                for i in d:
                    if i != "white":
                        add im.Twocolor(im.Scale("content/gfx/interface/bars/testbar.png", 40, d[i] * length_multiplier), store.__dict__[i], store.__dict__[i])
                add im.Scale("content/gfx/interface/bars/testbar.png", 40, d["white"] * length_multiplier)
                
            # vbox:
                # pos (90, 250)
                # # box_reverse True
                # frame:
                    # background Frame(white, 0, 0)
                    # xysize(20, (d["white"]) * length_multiplier)
                # for i in d:
                    # if i != "white":
                        # frame:
                            # # background Frame(store.__dict__[i], 0, 0)
                            # background im.Twocolor(im.Scale("content/gfx/interface/bars/testbar.png", 20, d[i] * length_multiplier), white, store.__dict__[i])
                            # xysize(20, d[i] * length_multiplier)
                # frame:
                    # background Frame(white, 0, 0)
                    # xysize(20, (d["white"]) * length_multiplier)
                  
            if not rolled:
                text "Bonus Roll":
                    pos (150, 200)
                    style "arena_header_text"
                    color red
                    size 35
            else:
                # Do the calculations, flag is set in the class so it is done once:
                $ bonus = pytfall.arena.award_cf_bonus()
                if bonus == "HP":
                    text "Bonus Roll: HP" pos (200, 200) style "black_serpent" color red size 30
                elif bonus == "MP":
                    text "Bonus Roll: MP" pos (200, 200) style "black_serpent" color blue size 30
                elif bonus == "Restore":
                    text "Bonus Roll: Full!" pos (200, 200) style "black_serpent" color green size 30
                else:
                    text "Bonus Roll: Bupkis" pos (200, 200) style "black_serpent" color white size 30
                    
            vbox:
                align (0.2, 0.5)
                spacing 10
                hbox:
                    xalign 0
                    spacing 10
                    frame:
                        background Frame(red, 0, 0)
                        xysize(1, 1)
                    text "{color=[red]}Restore HP" xalign 0.5 style "garamond"
                hbox:
                    xalign 0
                    spacing 10
                    frame:
                        background Frame(blue, 0, 0)
                        xysize(1, 1)
                    text "{color=[blue]}Restore MP" xalign 0.5 style "garamond"
                hbox:
                    xalign 0
                    spacing 10
                    frame:
                        background Frame(green, 0, 0)
                        xysize(1, 1)
                    text "{color=[green]}Restore HP/MP" xalign 0.5 style "garamond"
                hbox:
                    xalign 0
                    spacing 10
                    frame:
                        background Frame(grey, 0, 0)
                        xysize(1, 1)
                    text "{color=[grey]}Bupkis Award!" xalign 0.5 style "garamond"
                    
                if run:
                    textbutton "{color=[blue]}Freeze":
                        style "basic_button"
                        action SetScreenVariable("run", False), SetScreenVariable("rolled", True), SetField(pytfall.arena, "cf_bonus", value)
                        
                # if config.developer:
                    # python:
                        # d = pytfall.arena.d
                        # v = value
                        # result = None
                        # # And lastly, mutating to a bonus: range pair, pairs dict :)
                        # bonus = dict()
                        # bonus["bupkis"] = (0, d["white"])
                        # level = d["white"]
                        # newlevel = level + d["red"]
                        # bonus["HP"] = (level, newlevel)
                        # level = newlevel
                        # newlevel = newlevel + d["blue"]
                        # bonus["MP"] = (level, newlevel)
                        # level = newlevel
                        # newlevel = newlevel + d["green"]
                        # bonus["restore"] = (level, newlevel)
                        # level = newlevel
                        # newlevel = newlevel + d["white"]
                        # bonus["bupkis_2"] = (level, newlevel)
                        # # raise Exception, bonus
            
                        # for i in bonus:
                            # if bonus[i][0] <= v <= bonus[i][1]:
                                # result = i
                                # break
                    # text "Value: [v], Reward: [result]"
            
    screen confirm_chainfight():
        zorder 2
        modal True
        
        add "bg mc_setup"
        
        if pytfall.arena.cf_count and pytfall.arena.cf_mob:
            
            # Fight Number:
            text "Fight #[pytfall.arena.cf_count], proceed?":
                at move_from_to_pos_with_ease(start_pos=(640, -100), end_pos=(640, 150), t=0.7)
                italic True
                color darkred
                style "arena_header_text"
                size 35
                
            # Opposing Sprites:
            add hero.show("battle_sprite", resize=(200, 200)) at slide(so1=(-600, 0), t1=0.7, eo2=(-1300, 0), t2=0.7) align .35, .5
            add pytfall.arena.cf_mob.show("battle_sprite", resize=(200, 200)) at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7) align .65, .5
            
            # Title Text and Boss name if appropriate:
            if pytfall.arena.cf_count == 7:
                text "Boss Fight!":
                    align .5, .01
                    at fade_in_out(t1=1.5, t2=1.5)
                    style "arena_header_text"
                    size 80
                text pytfall.arena.cf_setup["boss_name"]:
                    align .65, .4
                    at fade_in_out(t1=1.5, t2=1.5)
                    size 25
                    color crimson
                    style "garamond"
            else:
                $ neow = pytfall.arena.cf_setup["id"]
                text pytfall.arena.cf_setup["id"]:
                    align .5, .01
                    at fade_in_out(t1=1.5, t2=1.5)
                    style "arena_header_text"
                    size 80
            
        hbox at slide(so1=(0, 700), t1=0.7, so2=(0, 700), t2=0.7):
            spacing 40
            align(0.5, 0.9)
            textbutton "{color=[blue]}Give Up :( ":
                style "basic_button"
                action [Hide("arena_inside"), Hide("chain_fight"), Hide("confirm_chainfight"), SetField(pytfall.arena, "cf_count", 0),
                           SetField(pytfall.arena, "cf_mob", None), SetField(pytfall.arena, "cf_setup", None), SetField(pytfall.arena, "cf_bonus", False),
                           Stop("music"), Jump("arena_inside")]
            textbutton "{color=[red]}Fight!!!":
                style "basic_button"
                action [Hide("arena_inside"), Hide("chain_fight"), Hide("confirm_chainfight"), SetField(pytfall.arena, "cf_bonus", False), Return(["challenge", "chainfight"])]
    
    screen arena_finished_chainfight(w_team):
        zorder  3
        modal True
        
        timer 9.0 action [Hide("arena_finished_chainfight"), Hide("arena_inside"), Hide("chain_fight"), Hide("confirm_chainfight"), SetField(pytfall.arena, "cf_count", 0), Jump("arena_inside")]
        
        add "bg mc_setup"
        
        add "arena_victory":
            at move_from_to_align_with_linear(start_align=(.5, .3), end_align=(.5, .03), t=2.2)
        
        vbox:
            at fade_from_to_with_easeout(start_val=.0, end_val=1.0, t=.9)
            align .95, .5
            maximum 500, 400 spacing 30
            text "Rewards:":
                xalign 0.5
                style "arena_header_text"
                
            hbox:
                xalign 0.5
                spacing 10
                box_wrap True
                if pytfall.arena.cf_rewards:
                    for reward in pytfall.arena.cf_rewards:
                        frame:
                            background Frame("content/gfx/frame/24-1.png", 5, 5)
                            xysize (90, 90)
                            add ProportionalScale(reward.icon, 80, 80) align .5, .5
                else:
                    text "No extra rewards... this is unlucky :(":
                        xalign 0.5
                        style "arena_header_text"
                        size 25
    
        # Chars + Stats
        frame:
            at fade_from_to_with_easeout(start_val=.0, end_val=1.0, t=.9, wait=0)
            background Frame("content/gfx/frame/MC_bg.png", 10, 10)
            add hero.show("battle", resize=(426, 376), cache=True)
            align .1, .5
            
        vbox:
            at arena_stats_slide
            pos (275, 405)
            spacing 1
            if not isinstance(w_team[0].combat_stats, basestring):
                for stat in w_team[0].combat_stats:
                    fixed:
                        xysize (170, 18)
                        text stat.capitalize() xalign .03 style "dropdown_gm2_button_text" color red
                        text str(w_team[0].combat_stats[stat]) xalign .97 style "dropdown_gm2_button_text" color crimson
            else:
                text("{size=+20}{color=[red]}K.O.")
