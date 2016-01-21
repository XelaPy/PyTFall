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
                
        # elif result[0] == "pick_chain":
            # if result[1] == "break":
                # pytfall.arena.result = "break"
            # else:
                # pytfall.arena.result = result[1]
                
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
             
    # Kickass sign         
    frame:
        xalign 0.501
        ypos 39
        background Frame("content/gfx/frame/Mc_bg.png", 10, 10)
        xysize (725, 120)
        add Transform(Text("{=content}{size=30}{color=[crimson]}Get your ass kicked in our Arena!"), alpha=0.8) align (0.5, 0.5)
        
    # Daily report and Hero info:
    # Hero stats at Jaeke's request:
    # Now a vbox:
    frame:
        xalign 1.0
        ypos 39
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=1.0), 10, 10)
        xysize (270, 682)
        vbox:
            align(0.5, 0.0)
            style_group "content"
            vbox:
                xalign 0.5
                #label "Hero Stats:" xalign 0.5 text_size 20 text_color ivory
                frame:
                    xalign 0.5
                    xysize (270, 120)
                    background Frame("content/gfx/frame/ink_box.png", 10 ,10)
                    $ img = hero.show("portrait", resize=(95, 95), cache=True)
                    frame:
                        background Frame("content/gfx/frame/MC_bg3.png", 10 ,10)
                        align (0.0, 0.9)
                        imagebutton:
                            idle (img)
                            hover (img) #(im.MatrixColor(img ,im.matrix.brightness(0.15)))
                            action NullAction()
                    frame:
                        style_group "stats"
                        yalign 0.5
                        xpos 103
                        xysize (148, 105)
                        background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=0.6), 10, 10)
                        vbox:
                            label "[hero.name]":
                                text_size 16
                                text_bold True
                                xpos 38
                                yalign 0.03
                                text_color ivory
                            fixed: # HP
                                xysize (150, 25)
                                xanchor -8
                                bar:
                                    yalign 0.5
                                    left_bar ProportionalScale("content/gfx/interface/bars/hp1.png", 150, 20)
                                    right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                    value hero.health
                                    range hero.get_max("health")
                                    thumb None
                                    xysize (150, 20)
                                text "HP" size 14 color ivory bold True yalign 0.1 xpos 8
                                if hero.health <= hero.get_max("health")*0.2:
                                    text "[hero.health]" size 14 color red bold True style "stats_value_text" yoffset -3 xpos 102
                                else:
                                    text "[hero.health]" size 14 color ivory bold True style "stats_value_text" yoffset -3 xpos 102
                    
                            fixed: # MP
                                xysize (150, 25)
                                xanchor -5
                                bar:
                                    yalign 0.2
                                    left_bar ProportionalScale("content/gfx/interface/bars/mp1.png", 150, 20)
                                    right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                    value hero.mp
                                    range hero.get_max("mp")
                                    thumb None
                                    xysize (150, 20)
                                text "MP" size 14 color ivory bold True yalign 0.8 xpos 7
                                if hero.mp <= hero.get_max("mp")*0.2:
                                    text "[hero.mp]" size 14 color red bold True style "stats_value_text" yoffset 2 xpos 99
                                else:
                                    text "[hero.mp]" size 14 color ivory bold True style "stats_value_text" yoffset 2 xpos 99
                    
                            fixed: # VIT
                                xysize (150, 25)
                                xanchor -2
                                bar:
                                    yalign 0.5
                                    left_bar ProportionalScale("content/gfx/interface/bars/vitality1.png", 150, 20)
                                    right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                    value hero.vitality
                                    range hero.get_max("vitality")
                                    thumb None
                                    xysize (150, 20)
                                text "VP" size 14 color ivory bold True yalign 0.8 xpos 7
                                if hero.vitality <= hero.get_max("vitality")*0.2:
                                    text "[hero.vitality]" size 14 color red bold True style "stats_value_text" yoffset 2 xpos 99
                                else:
                                    text "[hero.vitality]" size 14 color ivory bold True style "stats_value_text" yoffset 2 xpos 99
                    
                            #fixed:
                               # align(0.1, 0.5)
                               # xysize (105, 105)
                               # add hero.show("battle_sprite", resize=(100, 100)) align(0.5, 0.5)
                        
                                        
            frame:
                background im.Scale("content/gfx/frame/frame_bg.png", 270, 110)
                xysize (270, 110)
                label "Reputation: [hero.arena_rep]" text_size 25 text_color ivory align (0.5, 0.5)
        
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
          
    # Buttons:
    # Beast Fights:
    frame:
        pos (2, 39)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=1.0), 10, 10)
        xysize (280, 682)
        vbox:
            align (0.5, 0.03)
            frame:
                xysize (270, 90)
                style_group "content"
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.7), 10, 10)
                xpadding 10
                ypadding 10
                vbox:
                    align (0.5, 0.5)
                    spacing 2
                    frame:
                        xfill True
                        align (0.5, 0.5)
                        background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                        label "{size=28}{color=[bisque]}== Beast Fights ==" xalign 0.5 text_outlines [(1, "#3a3a3a", 0, 0)]
                    hbox:
                        style_group "basic"
                        align (0.5, 0.5)
                        spacing 5
                        textbutton "{size=24}{color=[black]}Bestiary":
                            action [Hide("arena_inside"), Show("arena_bestiary")]
                        textbutton "{size=24}{color=[black]}Survival!":
                            action Return(["challenge", "start_chainfight"])
                    
            # Ladders (Just Info):
            frame:
                xysize (270, 90)
                style_group "content"
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.7), 10, 10)
                xpadding 10
                ypadding 10
                vbox:
                    align (0.5, 0.5)
                    spacing 2
                    frame:
                        xfill True
                        align (0.5, 0.5)
                        background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                        label "{size=28}{color=[bisque]}== Ladders ==" xalign 0.5 text_outlines [(1, "#3a3a3a", 0, 0)]
                    hbox:
                        style_group "basic"
                        align (0.5, 0.5)
                        spacing 5
                        textbutton "{size=24}{color=[black]}1v1":
                            action Show("arena_lineups", transition=dissolve, container=pytfall.arena.lineup_1v1)
                        textbutton "{size=24}{color=[black]}2v2":
                            action Show("arena_lineups", transition=dissolve, container=pytfall.arena.lineup_2v2)
                        textbutton "{size=24}{color=[black]}3v3":
                            action Show("arena_lineups", transition=dissolve, container=pytfall.arena.lineup_3v3)

            # Official matches:
            frame:
                xysize (270, 90)
                style_group "content"
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.7), 10, 10)
                xpadding 10
                ypadding 10
                vbox:
                    align (0.5, 0.5)
                    spacing 2
                    frame:
                        xfill True
                        align (0.5, 0.5)
                        background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                        label "{size=28}{color=[bisque]}== Matches ==" xalign 0.5 text_outlines [(1, "#3a3a3a", 0, 0)]
                    hbox:
                        align (0.5, 0.5)
                        spacing 5
                        style_group "basic"
                        textbutton "{size=24}{color=[black]}1v1":
                            action Show("arena_matches", container=pytfall.arena.matches_1v1, transition=dissolve, vs_img=ProportionalScale("content/gfx/interface/images/vs_3.png", 130, 130))
                        textbutton "{size=24}{color=[black]}2v2":
                            action Show("arena_matches", container=pytfall.arena.matches_2v2, transition=dissolve, vs_img=ProportionalScale("content/gfx/interface/images/vs_2.png", 130, 130))
                        textbutton "{size=24}{color=[black]}3v3":
                            action Show("arena_matches", container=pytfall.arena.matches_3v3, transition=dissolve, vs_img=ProportionalScale("content/gfx/interface/images/vs_4.png", 130, 130))
     
            # Dogfights:
            frame:
                xysize (270, 90)
                style_group "content"
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.7), 10, 10)
                xpadding 10
                ypadding 10
                vbox:
                    align (0.5, 0.5)
                    spacing 2
                    frame:
                        xfill True
                        align (0.5, 0.5)
                        background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
                        label ("{size=28}{color=[bisque]}== Dogfights ==") xalign 0.5 text_outlines [(1, "#3a3a3a", 0, 0)]
                    hbox:
                        style_group "basic"
                        align (0.5, 0.5)
                        spacing 5
                        textbutton "{size=24}{color=[black]}1v1":
                            action Show("arena_dogfights", transition=dissolve, container=pytfall.arena.dogfights_1v1)
                        textbutton "{size=24}{color=[black]}2v2":
                            action Show("arena_dogfights", transition=dissolve, container=pytfall.arena.dogfights_2v2)
                        textbutton "{size=24}{color=[black]}3v3":
                            action Show("arena_dogfights", transition=dissolve, container=pytfall.arena.dogfights_3v3)
    use top_stripe(True)
             
screen arena_matches(container=None, vs_img=None):
    # Screens used to display and issue challenges in the official matches inside of Arena:
    modal True
    zorder 1
    
    frame:
        background Frame("content/gfx/frame/p_frame52.png", 10, 10)
        xysize (721, 565)
        at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)
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
                                        background Frame("content/gfx/frame/stat_box.png", 5, 5)
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
                                    background Frame("content/gfx/frame/stat_box.png", 5, 5)
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
        at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)
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
                                background Frame("content/gfx/frame/stat_box.png", 5, 5)
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
        at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)
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
                                background Frame("content/gfx/frame/stat_box.png", 5, 5)
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
        at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)
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
                                background Frame("content/gfx/frame/stat_box.png", 5, 5)
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
        align(0, 0)
        frame at fade_in_out():
            minimum(1000, 750)
            maximum(1000, 750)
            background Null()
            
            side "c r" at fade_in_out():
                viewport id "vp_bestiary":
                    draggable True
                    mousewheel True
                    hbox:
                        minimum(1000, 750)
                        maximum(1000, 750)
                        box_wrap True
                        spacing 2
                        for creature in mobs.itervalues():
                            vbox:
                                frame:
                                    background Solid((100, 100, 200, 150))
                                    minimum(230, 240)
                                    maximum(230, 240)
                                    if not creature.defeated:
                                        vbox:
                                            xalign 0.5
                                            minimum(230, 240)
                                            maximum(230, 240)
                                            spacing 2
                                            text("???") xalign 0.5
                                            add(im.Twocolor(creature.show("battle_sprite", resize=(200, 200), cache=True), black, black))
                                    else:
                                        vbox:
                                            xalign 0.5
                                            minimum(230, 240)
                                            maximum(230, 240)
                                            spacing 2
                                            text("[creature.name]") xalign 0.5
                                            imagebutton:
                                                xalign 0.5 
                                                idle (creature.show("battle_sprite", resize=(200, 200), cache=True))
                                                hover (im.MatrixColor(creature.show("battle_sprite", resize=(200, 200), cache=True), im.matrix.brightness(0.25)))
                                                action SetScreenVariable("in_focus_mob", creature)
                                null height 2
                                     
                vbar value YScrollValue("vp_bestiary")
                
        null width 10
        
        if in_focus_mob:
            frame:
                ypos 7
                background Solid((100, 100, 200, 150))
                minimum(240, 500)
                maximum(240, 500)
                vbox:
                    minimum(240, 500)
                    maximum(240, 500)
                    spacing 5
                    text("[in_focus_mob.name]") xalign 0.5
                    frame:
                        background Null()
                        minimum(200, 220)
                        maximum(200, 220)
                        xfill True
                        yfill True
                        add(in_focus_mob.show("battle_sprite", resize=(200, 220))) xalign 0.5
                    null height 10
                    text("{b}{color=[red]}----------------------")
                    text("Relative Stats:") xalign 0
                    hbox:
                        xalign 0
                        spacing 9
                        vbox:
                            minimum(150, 20)
                            maximum(150, 20)
                            xfill True
                            for stat in ilists.battlestats:
                                text("{size=17}%s"%stat.capitalize())
                        vbox:
                            minimum(30, 20)
                            maximum(30, 20)
                            for stat in ilists.battlestats:
                                text("{size=17}%s"%in_focus_mob.stats[stat])
        
    textbutton "{color=[red]}Ok" action [Hide("arena_bestiary"), Show("arena_inside")] minimum(50, 30) align(0.5, 0.985)
    key "mousedown_3" action [Hide("arena_bestiary"), Show("arena_inside")]
      
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
                    action SetScreenVariable("wteam_display", member)
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
        add im.Sepia(winner.show("sprite", resize=(200, 200), cache=True)) align (0.2, 0.2)
    else:
        add winner.show("sprite", resize=(200, 200), cache=True) align (0.2, 0.2)
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
        add im.Sepia(loser.show("sprite", resize=(200, 200), cache=True)) align (0.2, 0.2)
    else:
        add loser.show("sprite", resize=(200, 200), cache=True) align (0.8, 0.2)
        
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
        
        add "content/gfx/bg/locations/arena_bestiary.jpg" # at fade_in_out()
        
        if not pytfall.arena.cf_mob:
            text "Choose your Fight!" style "garamond" color red size 50 align (0.5, 0.1)
            hbox:
                spacing 10
                align (0.5, 0.5)
                box_wrap True
                minimum (690, 400)
                maximum (690, 400)
                for setup in pytfall.arena.chain_fights_order:
                    textbutton "{font=fonts/serpentn.ttf}[setup]":
                        xminimum 335
                        xfill True
                        action [SetField(pytfall.arena, "result", setup), ui.returns("Bupkis")]
                textbutton "{font=fonts/serpentn.ttf}Back":
                    xminimum 335
                    xfill True
                    action [SetField(pytfall.arena, "result", "break"), ui.returns("Bupkis")]
                key "mousedown_3" action [SetField(pytfall.arena, "result", "break"), ui.returns("Bupkis")]
        else:
            timer 0.5 action [SetField(pytfall.arena, "result", "break"), ui.returns("Bupkis")]
        
    screen confirm_chainfight(range, interval, length_multiplier, d):
        zorder 2
        modal True
        
        default reverse = False
        default rolled = False
        default value = 0
        default run = True
        default step = 2
        
        add("content/gfx/bg/locations/arena_bestiary.jpg")
        
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
                text "Bonus Roll" pos (150, 200) style "black_serpent" color red size 30
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
                    text "{color=[red]}Restore HP" xalign 0.5
                hbox:
                    xalign 0
                    spacing 10
                    frame:
                        background Frame(blue, 0, 0)
                        xysize(1, 1)
                    text "{color=[blue]}Restore MP" xalign 0.5
                hbox:
                    xalign 0
                    spacing 10
                    frame:
                        background Frame(green, 0, 0)
                        xysize(1, 1)
                    text "{color=[green]}Restore HP/MP" xalign 0.5
                hbox:
                    xalign 0
                    spacing 10
                    frame:
                        background Frame(grey, 0, 0)
                        xysize(1, 1)
                    text "{color=[grey]}Bupkis Award!" xalign 0.5
                if run:
                    textbutton "{color=[blue]}Freeze":
                        action [SetScreenVariable("run", False), SetScreenVariable("rolled", True), SetField(pytfall.arena, "cf_bonus", value)]
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
                                
        # ====================================================================================>>>            
        if pytfall.arena.cf_count and pytfall.arena.cf_mob:
            text("{b}{i}{color=[darkred]}Fight #[pytfall.arena.cf_count], proceed?"):
                at move_from_to_pos_with_ease(start_pos=(640, -100), end_pos=(640, 200), t=0.7)
                
            frame at slide(so1=(-600, 0), t1=0.7, eo2=(-1300, 0), t2=0.7):
                background Null()
                align(0.35, 0.5)
                add(hero.show("battle_sprite", resize=(200, 200)))
            frame at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7):
                background Null()
                align(0.65, 0.5)
                add(pytfall.arena.cf_mob.show("battle_sprite", resize=(200, 200)))
            
            if pytfall.arena.cf_count == 7:
                text ("{=myriadpro_sb}{size=50}{color=[crimson]}Boss Fight!") align(0.5, 0.2) at fade_in_out(t1=1.5, t2=1.5)
                $ neow = pytfall.arena.cf_setup["boss_name"]
                text ("{=myriadpro_sb}{size=25}{color=[crimson]}[neow]") align(0.65, 0.40) at fade_in_out(t1=1.5, t2=1.5)
            else:
                $ neow = pytfall.arena.cf_setup["id"]
                text ("{=myriadpro_sb}{size=50}{color=[crimson]}[neow]") align(0.5, 0.2) at fade_in_out(t1=1.5, t2=1.5)
            
        hbox at slide(so1=(0, 700), t1=0.7, so2=(0, 700), t2=0.7):
            spacing 40
            align(0.5, 0.9)
            textbutton "{b}{color=[blue]}Give Up :( ":
                action [Hide("arena_inside"), Hide("chain_fight"), Hide("confirm_chainfight"), SetField(pytfall.arena, "cf_count", 0),
                           SetField(pytfall.arena, "cf_mob", None), SetField(pytfall.arena, "cf_setup", None), SetField(pytfall.arena, "cf_bonus", False),
                           Stop("music"), Jump("arena_inside")]
            textbutton "{b}{color=[red]}Fight!!!":
                action [Hide("arena_inside"), Hide("chain_fight"), Hide("confirm_chainfight"), SetField(pytfall.arena, "cf_bonus", False), Return(["challenge", "chainfight"])]
    
    screen arena_finished_chainfight(w_team):
        zorder  3
        modal True
        
        timer 9.0 action [Hide("arena_finished_chainfight"), Hide("arena_inside"), Hide("chain_fight"), Hide("confirm_chainfight"), SetField(pytfall.arena, "cf_count", 0), Jump("arena_inside")]
        
        text("{size=+25}{i}{color=[red]}{font=fonts/rubius.ttf}Congratulation! You've Survived!!! :)"):
            at move_from_to_pos_with_ease(start_pos=(100, config.screen_height), end_pos=(640, 600), t=0.7)
        
        frame at fade_in_out():
            background Frame(Transform(im.Twocolor("content/gfx/frame/window_frame.png", white, white), alpha=0.5), 30, 30)
            align (0.7, 0.7)
            maximum(600, 300)
            xfill True
            yfill True
            vbox:
                maximum(600, 270)
                xfill True
                spacing 20
                text("{size=30}{font=fonts/rubius.ttf}{color=[crimson]}Rewards:") xalign 0.5
                hbox:
                    xalign 0.5
                    spacing 10
    
                    box_wrap True
                    if pytfall.arena.cf_rewards:
                        for reward in pytfall.arena.cf_rewards:
                            vbox:
                                xmaximum 70
                                xfill True
                                text("{size=10}{color=[black]}%s"%reward.id) xalign 0.5
                                add ProportionalScale(reward.icon, 50, 50) xalign 0.5
                    else:
                        text ("{font=fonts/rubius.ttf}{size=30}No extra rewards... this is unlucky :(")
    
                
        frame at fade_in_out():
            align(0, 0.7)
            background Null()
            minimum(426, 376)
            maximum(426, 376)
            xfill True
            add(hero.show("battle", resize=(426, 376), cache=True)) align(0.5, 0.5)
            frame at arena_stats_slide:
                background Null()
                align(1.0, 1.0)
                vbox:
                    if not isinstance(w_team[0].combat_stats, basestring):
                        for stat in w_team[0].combat_stats:
                            text("{size=-5}{color=[red]}%s: %d"%(stat.capitalize(), w_team[0].combat_stats[stat]))
                    else:
                        text("{size=+20}{color=[red]}K.O.")
