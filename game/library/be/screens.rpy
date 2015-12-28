init: # screens:
    screen target_practice(skill, targets):
        default highlight_idle = False
        default return_all = False
        if "all" in skill.type:
            $ return_all = True
            
        for t in targets:
            $ pos = battle.get_cp(t, type="tc", yo=-40)
            imagebutton:
                pos pos
                xanchor 0.5
                if highlight_idle:
                    idle im.Flip(im.MatrixColor("content/gfx/interface/buttons/blue_arrow_up.png", im.matrix.brightness(0.15)), vertical=True)
                else:    
                    idle im.Flip("content/gfx/interface/buttons/blue_arrow_up.png", vertical=True)
                hover im.Flip(im.MatrixColor("content/gfx/interface/buttons/blue_arrow_up.png", im.matrix.brightness(0.15)), vertical=True)
                if return_all:
                    action Return(targets)
                else:
                    action Return(t)
                if return_all: 
                    hovered SetScreenVariable("highlight_idle", True)
                    unhovered SetScreenVariable("highlight_idle", False)
                    
            if t in battle.corpses:
                add Transform(t.besprite, pos=t.cpos, alpha=0.4)
                    
        if config.developer:
            textbutton "Terminate":
                align (0.5, 0)
                action Hide("be_test"), Hide("target_practice"), Hide("pick_skill"), Hide("battle_overlay"), Jump("mainscreen")
                 
    screen pick_skill(char):
        
        default tt = Tooltip("")
        default menu_mode = "top"
        
        vbox:
            xalign 0.5
            ypos 0.9
            yanchor 1.0
            spacing 1
            if tt.value:
                frame: # This is the spell/attack description frame:
                    style "dropdown_gm_frame"
                    ymaximum 400
                    has hbox spacing 10
                    # Elements:
                    $ element = tt.value.get_element()
                    if element:
                        fixed:
                            xysize (100, 100)
                            if element.icon:
                                $ img = ProportionalScale(element.icon, 90, 90)
                                add img align (0.5, 0.5)
                    text tt.value.desc style "content_text" size 20 color ivory
            
            frame:
                style_group "dropdown_gm"
                # align (0.5, 0.9)
                ymaximum 400
                has hbox box_wrap True 
                
                at fade_in_out(t1=0.6, t2=0.3)
                
                # First we'll get all the skills and sort them into:
                # *Attack (battle) skills.
                # *Magic skills.
                # *Skills (That use vitality) later?.?
                # And then sort them in alphabetical order.
                python:
                    attacks = copy.copy(char.attack_skills)
                    attacks.sort(key=attrgetter("name"))
                    magic = copy.copy(char.magic_skills)
                    try:
                        magic.sort(key=attrgetter("name"))
                    except AttributeError:
                        raise Exception, char.name
                    
                    # We'll also try to figure out if there is at least one usable attack for them:
                    active_attacks = list() # list(a for a in attacks if battle_skills[a].check_conditions(char)) # BUG IN REN'PY!
                    for i in attacks:
                        if i.check_conditions(char):
                            active_attacks.append(char)
                            break
                    # active_magic = list(s for s in magic if battle_skills[s].check_conditions(char)) # BUG IN REN'PY!
                    active_magic = list()
                    for i in magic:
                        if i.check_conditions(char):
                            active_magic.append(char)
                            break
                
                if menu_mode == "top":
                    textbutton "Attacks":
                        action SensitiveIf(active_attacks), SetScreenVariable("menu_mode", "attacks")
                    textbutton "Magic":
                        action SensitiveIf(active_magic), SetScreenVariable("menu_mode", "magic")
                    textbutton "Skip":
                        xminimum 100
                        action Return(BE_Skip())
                        
                elif menu_mode == "attacks":
                    for skill in attacks:
                        textbutton "[skill.mn]":
                            action SensitiveIf(skill.check_conditions(char)), Return(skill)
                    textbutton "Back":
                        xminimum 100
                        action SetScreenVariable("menu_mode", "top")
                            
                elif menu_mode == "magic":
                    for skill in magic:
                        textbutton "{=text}{color=[black]}{size=-3}[skill.mn]":
                            action SensitiveIf(skill.check_conditions(char)), Return(skill)
                            hovered tt.action(skill)
                    textbutton "Back":
                        xminimum 100
                        action SetScreenVariable("menu_mode", "top")
                        
        if config.developer:
            textbutton "Terminate":
                align (0.99, 0)
                action Hide("be_test"), Hide("target_practice"), Hide("pick_skill"), Hide("battle_overlay"), Stop("music"), Jump("mainscreen")
          
    screen battle_overlay():
        # Averything that is displayed all the time:
        frame:
            align (0.5, 0.99)
            background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
            style "dropdown_gm_frame"
            has viewport:
                xysize (440, 50)
                scrollbars "vertical"
                has vbox
                for entry in reversed(battle.combat_log):
                    label "%s"%entry style_group "stats_value_text" text_size 14 text_color ivory 
                    
        
        # I'll need to condition this more appropriatly later, for now this will do:
        hbox:
            spacing 4
            align (0.5, 0.01)
            if hero.team in battle.teams:
                for member in hero.team:
                    if member not in battle.corpses:
                        python:
                            profile_img = member.show('portrait', resize=(95, 95), cache=True)
                            scr = renpy.get_screen("pick_skill")
                            if scr:
                                char = scr.scope["_args"][0] # This is not the best code :(
                            if scr and member == char:
                                portrait_frame = im.Twocolor("content/gfx/frame/MC_bg3.png", grey, grey)
                                img = "content/gfx/frame/ink_box.png"
                            else:
                                portrait_frame = "content/gfx/frame/MC_bg3.png"
                                img = "content/gfx/frame/ink_box.png"
                                
                        button:
                            # if member not in battle.corpses:
                                # at be_stats_slideout
                            style_group "content"
                            background Frame(Transform(img, alpha=0.5), 10 ,10)
                            # idle_background Frame(Transform(img, alpha=0.4), 10 ,10)
                            # hover_background Frame(Transform(img, alpha=0.9), 10 ,10)
                            xysize (280, 120)
                            action NullAction()
                            
                            # Girl Image:
                            frame:
                                xoffset -5
                                yalign 0.5
                                background Frame(portrait_frame, 10 ,10)
                                xysize (95, 95)
                                add profile_img align (0.5, 0.5) alpha 0.96
                               
                            # Texts/Status:
                            frame:
                                style_group "stats"
                                yalign 0.5
                                xpos 102
                                xysize (152, 105)
                                background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=0.6), 10, 10)
                                vbox:
                                    label "[member.name]":
                                        text_size 16
                                        text_bold True
                                        xpos 38
                                        yalign 0.03
                                        if isinstance(member, Char):
                                            text_color pink
                                        else:
                                            text_color ivory
                                            
                                    # null height 5
                                    
                                    hbox:
                                        xpos 8
                                        vbox:
                                            # yfill true
                                            fixed:
                                                xysize (150, 25)
                                                yfill True
                                                bar:
                                                    yalign 1.0
                                                    left_bar ProportionalScale("content/gfx/interface/bars/hp1.png", 150, 20)
                                                    right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                                    value member.health
                                                    range member.get_max("health")
                                                    thumb None
                                                    xysize (150, 20)
                                                text "HP" size 14 color ivory bold True yalign 0.2 xpos 7
                                                if member.health <= member.get_max("health")*0.2:  # <== 20% ## need a percentage system ### 
                                                    text "[member.health]" size 14 color red bold True style "stats_value_text" yoffset -3 xpos 95
                                                else:
                                                    text "[member.health]" size 14 color ivory bold True style "stats_value_text" yoffset -3 xpos 95
                                            fixed:
                                                xysize (150, 25)
                                                xanchor 3
                                                yfill True
                                                bar:
                                                    yalign 1.0
                                                    left_bar ProportionalScale("content/gfx/interface/bars/mp1.png", 150, 20)
                                                    right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                                    value member.mp
                                                    range member.get_max("mp")
                                                    thumb None
                                                    xysize (150, 20)
                                                text "MP" size 14 color ivory bold True yalign 0.2 xpos 7
                                                if member.mp <= member.get_max("mp")*0.2:
                                                    text "[member.mp]" size 14 color red bold True style "stats_value_text" yoffset -3 xpos 95
                                                else:
                                                    text "[member.mp]" size 14 color ivory bold True style "stats_value_text" yoffset -3 xpos 95
                                            fixed:
                                                xysize (150, 25)
                                                xanchor 6
                                                yfill True
                                                bar:
                                                    yalign 1.0
                                                    left_bar ProportionalScale("content/gfx/interface/bars/vitality1.png", 150, 20)
                                                    right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                                    value member.vitality
                                                    range member.get_max("vitality")
                                                    thumb None
                                                    xysize (150, 20)
                                                text "VP" size 14 color ivory bold True yalign 0.2 xpos 7
                                                if member.vitality <= member.get_max("vitality")*0.2:
                                                    text "[member.vitality]" size 14 color red bold True style "stats_value_text" yoffset -3 xpos 95
                                                else:
                                                    text "[member.vitality]" size 14 color ivory bold True style "stats_value_text" yoffset -3 xpos 95
                    
        if config.developer:
            vbox:
                align (0.99, 0)
                textbutton "Terminate":
                    action Hide("be_test"), Hide("target_practice"), Hide("pick_skill"), Hide("battle_overlay"), Jump("mainscreen")
                
