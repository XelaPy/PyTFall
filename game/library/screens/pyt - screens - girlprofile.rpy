label girl_profile:
    
    if not hasattr(store, "girls") or girls is None or chr not in girls:
        $ girls = list(girl for girl in hero.girls if girl.action != "Exploring")
    
    scene bg scroll
    show screen pyt_girl_profile
    with dissolve
    
    python:
        while True:
            result = ui.interact()
            
            # If the girl has runaway
            if chr in pytfall.ra:
                if result[0] == "girl":
                    if result[1] == "gallery":
                        pyt_gallery = PytGallery(chr)
                        jump("gallery")
                    
                    elif result[1] == "get_rid":
                        if renpy.call_screen("yesno_prompt", message="Are you sure you wish to stop looking for %s?"%chr.name, yes_action=Return(True), no_action=Return(False)):
                            hero.remove_girl(chr)
                            girls.remove(chr)
                            chr.dispoition -= 300
                            if chr in hero.team: hero.team.remove(chr)
                            if girls:
                                index = (index+1)%len(girls)
                                chr = girls[index]
                                continue
                            else:
                                break
                    else:
                        renpy.show_screen("pyt_message_screen", "This girl has run away!")
                
                elif result[0] != "control":
                    renpy.show_screen("pyt_message_screen", "This girl has run away!")
            
            # Else if you still have the girl
            else:
                if result[0] == "jump":
                    if result[1] == "item_transfer":
                        renpy.hide_screen("pyt_girl_profile")
                        pytfall.it = GuiItemsTransfer("personal_transfer", chr=chr, last_label=last_label)
                        jump("items_transfer")
                
                elif result[0] == "dropdown":
                    if result[1] == "loc":
                        renpy.show_screen("pyt_dropdown_loc", result[2], pos=renpy.get_mouse_pos())
                    elif result[1] == "action":
                        renpy.show_screen("pyt_dropdown_action", result[2], pos=renpy.get_mouse_pos())
                
                elif result[0] == "girl":
                    if result[1] == "gallery":
                        pyt_gallery = PytGallery(chr)
                        jump("gallery")
                    elif result[1] == "it":
                        pytfall.it = GuiItemsTransfer("personal_transfer", chr=chr, last_label=last_label)
                        jump("items_transfer")
                    elif result[1] == "get_rid":
                        if chr.status == "slave":
                            message = "Are you sure you wish to sell {} for {}?".format(chr.name, int(chr.fin.get_price()*0.8))
                        else:
                            message = "Are you sure that you wish to fire {}?".format(chr.name)
                        if renpy.call_screen("yesno_prompt",
                                                        message=message,
                                                        yes_action=Return(True), no_action=Return(False)):
                            if chr.status == 'slave':
                                hero.add_money(int(chr.fin.get_price()*0.8), reason="SlaveTrade")
                                chr.location = 'slavemarket'
                            else:
                                chr.location = 'city'
                            hero.remove_girl(chr)
                            index = girls.index(chr) # Index is not set otherwise???
                            girls.remove(chr)
                            chr.disposition -= 300
                            if chr in hero.team:
                                hero.team.remove(chr)
                            if girls:
                                index = (index + 1) % len(girls)
                                chr = girls[index]
                            else:
                                break
                                
                    elif result[1] == 'buyrank':
                        # Should prolly move this to the Girl method at some point:
                        # TODO: Update to skills (Refinement!)
                        targetrank = chr.rank + 1
                        maxrank = max(b.maxrank for b in hero.brothels)
                        if targetrank > 3 and chr.status == "slave":
                            renpy.call_screen('pyt_message_screen', "Slave Girls cannot be pushed past rank 3!")
                        elif targetrank > maxrank:
                            renpy.call_screen('pyt_message_screen', "You do not currently own any brothels to justify ranking a prostitute to Rank %d" % targetrank)
                        else:    
                            rankinfo = chr.wranks['r%d' % targetrank]
                
                            if chr.exp >= rankinfo['exp']:
                                if chr.refinement >= rankinfo['ref']:
                                    if hero.take_money(rankinfo['price'], reason="Prositute Ranks"):
                                        chr.rank += 1
                                        chr.stats.max['refinement'] += 15
                                
                        del maxrank
                        del targetrank
                elif result[0] == "rename":
                    if result[1] == "name":
                        chr.name = renpy.call_screen("pyt_input", chr.name, "Enter Name", 20)
                    if result[1] == "nick":
                        chr.nickname = renpy.call_screen("pyt_input", chr.name, "Enter Nick-Name", 20)
                    if result[1] == "full":
                        chr.fullname = renpy.call_screen("pyt_input", chr.name, "Enter Full-Name", 20)
            
            if result[0] == 'control':
                index = girls.index(chr)
                if result[1] == 'left':
                    index = (index - 1) % len(girls)
                    chr = girls[index]
                elif result[1] == 'right':
                    index = (index + 1) % len(girls)
                    chr = girls[index]
                    
                elif result[1] == 'return':
                    break
        
    hide screen pyt_girl_profile
    
    $ girls = None
    
    if girl_profile:
        $ last_label, girl_profile = girl_profile, None
        jump expression last_label
    
    else:
        jump girls_list
    

screen pyt_girl_profile:

    key "mousedown_4" action Return(["control", "right"])
    key "mousedown_5" action Return(["control", "left"])
    
    default tt = Tooltip("Manage your girls here!!!")
    default stats_display = "stats"
    
    $ not_escaped = chr not in pytfall.ra
    
    if girls:
        # Picture and left/right buttons:
        add "content/gfx/frame/p_frame6.png" xalign 0.487 yalign 0.185 size (613, 595)
        # Alex: Code by Gismo, messy but gets the job done, I acutally have no idea of how to get this done with just one frame and the image...
        # Vbox is just for more convinient positioning.
        vbox:
            align (0.487, 0.184) #0.487, 0.164
            yfill True
            ymaximum 514 #569
            python:
                frame_image = im.Scale("content/gfx/frame/MC_bg3.png", 1, 1)
                img = chr.show('profile', resize=(600, 514), cache=True)
            button:
                align (0.5, 0.5)
                idle_background frame_image
                idle_foreground Transform(img, align=(0.5, 0.5))
                
                hover_background im.MatrixColor(frame_image, im.matrix.brightness(0.1))
                hover_foreground Transform(im.MatrixColor(img, im.matrix.brightness(0.1)), align=(0.5, 0.5))
                
                insensitive_background frame_image
                insensitive_foreground Transform(img, align=(0.5, 0.5))
                frame:
                    align(0.5, 0.5)
                    background Frame("content/gfx/frame/MC_bg3.png", 10 ,10)
                    add ProportionalScale(img, 600, 514) align(0.5, 0.5)
                
                action If(not_escaped, true=[Hide("pyt_girl_profile"), With(dissolve), Execute(gm.start_int_or_tr, chr)], false=NullAction())
                
                hovered tt.action("Interact with [chr.nickname]!")
            
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
            xalign 0.489
            ypos 560
            xysize (628, 64)
            hbox:
                xalign 0.46
                yalign 0.5
                button:
                    xysize (140, 40)
                    style "left_wood_button"
                    action Return(['control', 'left'])
                    hovered tt.action("<== Previous Girl")
                    text "Previous Girl" style "wood_text" xalign(0.69)
                
                null width 280
                
                button:
                    xysize (140, 40)
                    style "right_wood_button"
                    action Return(['control', 'right'])
                    hovered tt.action("Next Girl ==>")
                    text "Next Girl" style "wood_text" xalign(0.19)  
        
        # Stats and Info:
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
            xysize(330, 780)
            xanchor 0.01
            ypos 30
            style_group "content"
            has vbox
            
            null height 15
            # Name:
            frame:
                #xalign 0.7
                xanchor -0.14
                xysize (250, 50)
                background Frame (Transform("content/gfx/frame/namebox5.png", alpha=0.95), 250, 50)
                label "{color=[gold]}[chr.name]":
                    text_color ivory text_outlines [(2, "#424242", 0, 0)]
                    align (0.5, 0.5)
                    if len(chr.name) < 20:
                        text_size 21
                
            null height 5
            # Rank up for prostitutes:
            # TODO: Adapt ranks to new skills code!
            # @Review: Will not be used until further notice!
            # if traits['Prostitute'] in chr.occupations:
                # frame:
                    # xanchor -0.01
                    # xysize(313, 47)
                    # background Frame("content/gfx/frame/rank_frame.png", 10, 10)
                    # text ('%s:'%chr.wranks['r%s'%chr.rank]['name'][0]) align(0.1, 0.2) color ivory size 16
                    # text ('%s'%chr.wranks['r%s'%chr.rank]['name'][1]) align(0.5, 0.96) color ivory size 16
                    # if chr.rank < 8:
                        # $ rankinfo = chr.wranks['r%d' % (chr.rank+1)]                                
                        # imagebutton:
                            # align (0.95, 0.5)
                            # hover "rank_up"
                            # if chr.refinement >=rankinfo['ref'] and chr.exp >= rankinfo['exp']:
                                # idle "rank_up"
                                # action Return(['girl', 'buyrank'])
                                # hovered tt.Action("Increase this girl's Rank. Rank is one of the most important things for a girl in a brothel to have. \nTo achieve next rank your girl requires: %d of Refinement, %d of Experience and a sum of %d gold."%(rankinfo['ref'], rankinfo['exp'], rankinfo['price']))
                            # else:
                                # idle im.Sepia("content/gfx/animations/rank_up/1.png")
                                # action NullAction()
                                # hovered tt.Action("[chr.nickname] does not meet the requirements for a rank up.\nRank is one of the most important things for a girl in a brothel to have. \nTo achieve next rank your girl requires: %d of Refinement, %d of Experience and a sum of %d gold."%(rankinfo['ref'], rankinfo['exp'], rankinfo['price']))

            null height 8

            # Stats/Info
            fixed:
                xanchor -0.01
                xysize (300, 60)
                vbox:
                    # Prof-Classes
                    python:
                        if len(chr.traits.basetraits) == 1:
                            classes = [list(chr.traits.basetraits)[0]]
                        elif len(chr.traits.basetraits) == 2:
                            classes = list(chr.traits.basetraits).sort()
                        else:
                            raise Exception("Character without prof basetraits detected! line: 262, girlsprofile screen")
                    hbox:
                        ymaximum 18
                        spacing 3
                        button:
                            xmargin 0
                            xpadding 0
                            ypadding 0
                            action NullAction()
                            background Null()
                            text "Classes:" color ivory size 18
                        null width 2
                        for cls in classes:
                            button:
                                yalign 0.9
                                xmargin 0
                                xpadding 0
                                ypadding 0
                                action NullAction()
                                hovered tt.Action(cls.desc)
                                background Null()
                                text  "[cls.id]"  color ivory size 15
                        
                    null height 2
                    $ loc = chr.location if isinstance(chr.location, basestring) else chr.location.name
                    button:
                        style_group "ddlist"
                        action Return(["dropdown", "loc", chr])
                        hovered tt.Action("Choose a location for %s to work at!" % chr.nickname)
                        text "{image=content/gfx/interface/icons/move15.png}Location: [loc]":
                            if len(loc) > 18:
                                size 15
                            else:
                                size 18
                    button:
                        style_group "ddlist"
                        action Return(["dropdown", "action", chr])
                        hovered tt.Action("Choose a task for %s to do!" % chr.nickname)
                        text "{image=content/gfx/interface/icons/move15.png}Action: [chr.action]":
                            if chr.action is not None and len(str(chr.action)) > 18:
                                size 15
                            else:
                                size 18
                    
                imagebutton:
                    align(0.99, 0.45)
                    if chr.status == "slave":
                        idle ProportionalScale("content/gfx/interface/icons/slave.png", 50, 50)
                        hover (im.MatrixColor(ProportionalScale("content/gfx/interface/icons/slave.png", 50, 50), im.matrix.brightness(0.25)))
                        hovered tt.Action("This girl is a slave!")
                    else:
                        idle ProportionalScale("content/gfx/interface/icons/free.png", 50, 50)
                        hover (im.MatrixColor(ProportionalScale("content/gfx/interface/icons/free.png", 50, 50), im.matrix.brightness(0.25)))
                        hovered tt.Action("This girl is free as a bird :)")
                    action NullAction()
                    
            null height 5
            hbox:
                style_group "basic"
                xalign 0.5
                button:
                    yalign 0.5
                    action SetScreenVariable("stats_display", "stats")
                    text "Stats" size 15
                button:
                    yalign 0.5
                    action SetScreenVariable("stats_display", "pro_stats")
                    text "Pro Stats" size 15
                button:
                    yalign 0.5
                    action SetScreenVariable("stats_display", "info")
                    text "Info" size 15
                if config.developer:
                    button:
                        yalign 0.5
                        action SetScreenVariable("stats_display", "skillstest")
                        text "Skills" size 15
                        
            null height 4
            vbox:
                style_group "stats"
                pos(0.015, 10)
                xmaximum 325
                if stats_display == "stats":
                    #label (u"{size=20}{color=[ivory]}{b}Stats:")
                    #null height 1
                    frame:
                        background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                        xysize (317, 100)
                        xanchor 5
                        yanchor 10
                        hbox:
                            $ stats = ["charisma", "character", "reputation", "constitution", "joy", "intelligence", "disposition"]
                            vbox:
                                spacing -7
                                xanchor 0
                                xmaximum 153
                                xfill True
                                frame:
                                    text "{color=#CD4F39}Health:" xalign (0.02) #{color=#00CCCC} 00FFFF 2E8B57
                                frame:
                                    text "{color=#43CD80}Vitality:" xalign (0.02)
                                for stat in stats:
                                    frame:
                                        text ('{color=#79CDCD}%s'%stat.capitalize()) xalign (0.02) 
                                frame:
                                    text "{color=[gold]}Gold:" xalign (0.02)
                            vbox:
                                yalign (0.6)
                                spacing 9
                                xfill True
                                xminimum 142
                                xmaximum 142
                                if chr.health <= chr.get_max("health")*0.3:
                                    text (u"{color=[red]}%s/%s"%(chr.health, chr.get_max("health"))) style "stats_value_text" xalign (1.0)
                                else:
                                    text (u"%s/%s"%(chr.health, chr.get_max("health"))) style "stats_value_text" xalign (1.0)
                                if chr.vitality < chr.get_max("vitality")*0.3:
                                    text (u"{color=[red]}%s/%s"%(chr.vitality, chr.get_max("vitality"))) style "stats_value_text" xalign (1.0)
                                else:
                                    text (u"%s/%s"%(chr.vitality, chr.get_max("vitality"))) style "stats_value_text" xalign (1.0)
                                for stat in stats:
                                    text ('%d/%d'%(getattr(chr, stat), chr.get_max(stat))) style "stats_value_text" xalign (1.0)
                                text (u"{color=[gold]}%s"%chr.gold) style "stats_value_text" xalign (1.0)
                            
                    null height -8
                    label (u"{size=20}{color=[ivory]}{b}Info:") xalign(0.48) text_outlines [(2, "#424242", 0, 0)]
                    #null height 2
                    frame:
                        background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                        xysize (317, 10)
                        xanchor 5
                        hbox:
                            vbox:
                                spacing -7
                                xanchor 0
                                xmaximum 153
                                xfill True
                                if chr.status == "slave":
                                    frame:
                                        text "{color=#79CDCD}Market Price:" xalign (0.02)
                                if traits['Prostitute'] in chr.occupations:
                                    frame:
                                        text "{color=#79CDCD}Work Price:" xalign (0.02)
                                frame:
                                    text "{color=#79CDCD}Upkeep:" xalign (0.02)
                            vbox:
                                yalign (0.5)
                                xfill True
                                xminimum 142
                                xmaximum 142
                                spacing 9
                                if chr.status == "slave":
                                    text (u"%s"%(chr.fin.get_price())) style "stats_value_text" xalign (1.0)
                                if traits['Prostitute'] in chr.occupations:
                                    text (u"%s"%(chr.fin.get_whore_price())) style "stats_value_text" xalign (1.0)
                                text (u"%s"%(chr.fin.get_upkeep())) style "stats_value_text" xalign (1.0)
                            

                    
                ##############################################################################
                # Stats 2 (pro)
                elif stats_display == "pro_stats": 
                    null height 1    
                    label (u"{size=20}{color=[ivory]}{b}Battle Stats:") xalign(0.48) text_outlines [(2, "#424242", 0, 0)]
                    null height -5
                    frame:
                        background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                        xysize (317, 180)
                        xanchor 5
                        hbox:
                            #$ stats = ["Attack", "Defence", "Magic", "MP", "Agility", "Luck"]
                            vbox:
                                spacing -7
                                xanchor 0
                                xmaximum 153
                                xfill True
                                #for stat in stats:
                                    #frame:
                                        #text ('{color=#009ACD}%s{/color}'%stat.capitalize()) size 16 xalign (0.02)
                                frame:
                                    text "{color=#CD4F39}Attack:" size 16 xalign (0.02)
                                frame:
                                    text "{color=#dc762c}Defence:" size 16 xalign (0.02)
                                frame:
                                    text "{color=#8470FF}Magic:" size 16 xalign (0.02)
                                frame:
                                    text "{color=#009ACD}MP:" size 16 xalign (0.02)
                                frame:
                                    text "{color=#1E90FF}Agility:" size 16 xalign (0.02)
                                frame:
                                    text "{color=#00FA9A}Luck:" size 16 xalign (0.02)

                            vbox:
                                yalign (0.6)
                                spacing 4
                                xfill True
                                xminimum 142
                                xmaximum 142
                                text (u"{size=16}{color=#CD4F39}[chr.attack]/%s"%(chr.get_max("attack"))) style "stats_value_text" xalign (1.0)
                                text (u"{size=16}{color=#dc762c}[chr.defence]/%s"%(chr.get_max("defence"))) style "stats_value_text" xalign (1.0)
                                text (u"{size=16}{color=#8470FF}[chr.magic]/%s"%(chr.get_max("magic"))) style "stats_value_text" xalign (1.0)
                                text (u"{size=16}{color=#009ACD}[chr.mp]/%s"%(chr.get_max("mp"))) style "stats_value_text" xalign (1.0)
                                text (u"{size=16}{color=#1E90FF}[chr.agility]/%s"%(chr.get_max("agility"))) style "stats_value_text" xalign (1.0)
                                text (u"{size=16}{color=#00FA9A}[chr.luck]") style "stats_value_text" xalign (1.0)

                    null height 4
                    if hasattr(chr, "elements"): # This should always be true...
                        # Prepear the list:
                        $ els = list()
                        $ crops = list()
                        for e in chr.elements:
                            python:
                                img = ProportionalScale(e.icon, 90, 90)
                                els.append(img)
                        frame:
                            style_group "content"
                            background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 10, 10)
                            xysize (317, 130)
                            ymaximum 120
                            xanchor 5
                            yanchor 5
                            $ x = 0
                            fixed:
                                xysize (100, 100)
                                xcenter 250
                                ycenter 62
                                # at pers_effect
                                for i in els:
                                    add Transform(i, crop=(90/len(els)*els.index(i), 0, 90/len(els), 90), subpixel=True, xpos=(x + 90/len(els)*els.index(i)))
                            viewport:
                                draggable True
                                has vbox
                                for e in chr.elements:
                                    textbutton "{=tisa_otm}[e.id]":
                                        background None
                                        action NullAction()
                                        hovered tt.Action("%s" % e.desc)
                                    
                            
                    null height 4
                    $ _traits = set(list(traits[t] for t in chr.PERSONALITY_TRAITS))
                    $ trait = _traits.intersection(set(chr.traits)).pop()
                    $ img = ProportionalScale("".join(["content/gfx/interface/images/personality/", trait.id.lower(), ".png"]), 90, 90)
                    yalign 0.5
                    frame:
                        style_group "content"
                        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 10, 10)
                        xysize (317, 120)
                        xanchor 5
                        yanchor 5
                        label "[trait.id]" align(0.1, 0.1) text_color purple text_size 30 text_bold True
                        imagebutton at pers_effect():
                            xcenter 250
                            ycenter 53
                            idle (img)
                            hover (img)
                            hovered tt.Action(trait.desc)
                            action NullAction() 
                            
                # Info
                elif stats_display == "info": 
                    null height -10
                    frame:
                        background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                        xysize (317, 100)
                        xanchor 5
                        hbox:
                            yalign 0.5
                            vbox:
                                spacing -3
                                xanchor 0
                                xmaximum 250
                                xfill True
                                label "Full Name:" xpos 20
                                textbutton (u"{color=[gold]}[chr.fullname]"):
                                    background None
                                    xpos 30
                                    xmaximum 220
                                    action Show("chr_rename", chr=chr)
                                    hovered tt.action("Rename %s!" % chr.name)
                                if chr.race:
                                    label "Race:" xpos 20
                                    frame:
                                        text (u"{color=#dc762c}[chr.race]") xpos 30 xmaximum 220
                                label "Origin:" xpos 20
                                frame:
                                    text (u"{color=#43CD80}[chr.origin]") xpos 30 xmaximum 220
                    null height 5
                    label (u"{size=20}{b}Description:") xalign(0.45) text_outlines [(2, "#424242", 0, 0)]
                    null height 5
                    frame:
                        xanchor 0.015
                        background Frame("content/gfx/frame/ink_box.png", 10, 10)
                        minimum (314, 10)
                        text ("{color=[ivory]}[chr.desc]") style "content_text" layout "greedy" justify True minwidth 304 xalign 0.5
                elif stats_display == "skillstest":
                    viewport:
                        scrollbars "vertical"
                        xysize (310, 500)
                        mousewheel True
                        has vbox spacing 1
                        for skill in chr.stats.skills:
                            text "[skill]: {true} <{action}, {training}>".format(true=int(chr.get_skill(skill)), action=int(chr.stats.skills[skill][0]), training=int(chr.stats.skills[skill][1]))

        # Level, experience:
        fixed:
            xalign 0.490
            ypos 570
            xysize (360, 45)
            add(ProportionalScale("content/gfx/frame/level.png", 360, 45)) align(0.5, 0.5)
            text("{font=fonts/Rubius.ttf}{color=[ivory]}{size=16}{b}[chr.level]") pos(106, 7)
            text("{font=fonts/Rubius.ttf}{color=[ivory]}{size=16}{b}[chr.exp]") pos(190, 7)
            text("{font=fonts/Rubius.ttf}{color=[ivory]}{size=16}{b}[chr.goal]") pos(190, 27)

            
    ## Right frame
        frame:
            ypos 37
            xalign 1.0
            xysize (345, 590)
            background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        # Buttons
            frame:
                background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 10, 10)
                xalign 0.5
                ypos 5
                xysize (325, 150)
                hbox:
                    style_group "wood"
                    align (0.5, 0.5)
                    spacing 5
                    vbox:
                        spacing 5
                        button:
                            xysize (150, 40)
                            action If(not_escaped, true=Show("pyt_girl_control"))
                            hovered tt.action('Set desired behaviour for [chr.nickname].')
                            text "Girl Control"
                        button:
                            xysize (150, 40)
                            action If(not_escaped, true=[Hide("pyt_girl_profile"), With(dissolve), Jump('girl_equip')])
                            hovered tt.action('Access girls inverntory and equipment screen!')
                            text "Equipment"
                        button:
                            xysize (150, 40)
                            action [Hide("pyt_girl_profile"), With(dissolve), Return(["girl", "gallery"])]
                            hovered tt.action("View this girl's gallery!")
                            text "Gallery"
                
                    vbox:
                        spacing 5
                        button:
                            xysize (150, 40)
                            action If(not_escaped, true=[Hide("pyt_girl_profile"), With(dissolve), Jump('girl_training')])
                            hovered tt.action("Send her to School!")
                            text "Training"
                        button:
                            xysize (150, 40)
                            action If(not_escaped, true=Show("pyt_girl_finances"))
                            hovered tt.action("Review Finances!")
                            text "Finances"
                        button:
                            xysize (150, 40)
                            action If(not_escaped, true=Return(["girl", "get_rid"]))
                            hovered tt.action("Get rid of her!")
                            text "Get Rid"
            
        # AP:
            frame:
                xalign 0.5
                ypos 160
                xysize (300, 90)
                background ProportionalScale("content/gfx/frame/frame_ap.png", 300, 100)
                label ("[chr.AP]"):
                    pos (200, 0)
                    style "content_label"
                    text_color ivory
                    text_size 28
            
        # Traits/Effects:
            frame:
                background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                xysize (325, 210)
                style_group "stats"
                ypos 225
                xanchor 1
                hbox:
                    fixed:
                        xysize (170, 190)
                        label (u"Traits:") text_size 20 text_color ivory text_bold True align(0.42, 0.03) #text_outlines [(3, "#3a3a3a", 0, 0), (2, "#7A378B", 0, 0), (1, "#3a3a3a", 0, 0)]
                        side "c r":
                            align(0, 0.92)
                            viewport id "girlprofile_traits_vp":
                                xysize (170, 155)
                                draggable True
                                mousewheel True
                                vbox:
                                    spacing -7
                                    for trait in chr.traits:
                                        if trait.id not in chr.PERSONALITY_TRAITS or not trait.hidden:
                                            frame:
                                                xysize (150, 10)
                                                button:
                                                    background Null()
                                                    xysize (150, 10)
                                                    action NullAction()
                                                    text "[trait.id]" idle_color ivory size (15) xanchor (10)
                                                    hovered tt.Action(u"%s"%trait.desc)
                                                    hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.10)), 5, 5)
                            vbar value YScrollValue("girlprofile_traits_vp")
            # Effects:
                    fixed:
                        xanchor 5
                        xysize (165, 190)
                        label (u"Effects:") text_size 20 text_color ivory text_bold True align(0.42, 0.03) #text_outlines [(3, "#3a3a3a", 0, 0), (2, "#458B74", 0, 0), (1, "#3a3a3a", 0, 0)]
                        side "c r":
                            align(0, 0.92)
                            viewport id "girlprofile_effects_vp":
                                xysize (165, 155)
                                draggable True
                                mousewheel True
                                vbox:
                                    spacing -7
                                    for key in chr.effects:
                                        frame:
                                            xysize (155, 37)
                                            if chr.effects[key]['active']:
                                                button:
                                                    background Null()
                                                    xysize (155, 37)
                                                    action NullAction()
                                                    text "[key]" idle_color ivory size(15) xanchor(10)
                                                    hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.10)), 5, 5)
                            vbar value YScrollValue("girlprofile_effects_vp")
                    
        # Attacks/Magic
            frame:
                background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                xysize (327, 105)
                style_group "stats"
                ypos 437
                xanchor 1
                hbox:
                    fixed:
                        xysize (170, 125)
                        label (u"Attack:") text_size 20 text_color ivory text_bold True align(0.42, 0.02) text_outlines [(3, "#3a3a3a", 0, 0), (2, "#8B0000", 0, 0), (1, "#3a3a3a", 0, 0)]
                        side "c r":
                            align(0, 0.98)
                            viewport id "girlprofile_attack_vp":
                                xysize (170, 90)
                                draggable True
                                mousewheel True
                                vbox:
                                    spacing -7
                                    for entry in chr.attack_skills:
                                        frame:
                                            xysize (150, 10)
                                            button:
                                                background Null()
                                                xysize (150, 10)
                                                action NullAction()
                                                text "[entry.name]" idle_color ivory size(15) xanchor(10)
                                                hovered tt.action(entry)
                                                hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.10)), 5, 5)
                            vbar value YScrollValue("girlprofile_attack_vp")
            
                    fixed:
                        xysize (165, 125)
                        xanchor 5
                        label (u"Magic:") text_size 20 text_color ivory text_bold True align(0.42, 0.02) text_outlines [(3, "#3a3a3a", 0, 0), (2, "#104E8B", 0, 0), (1, "#3a3a3a", 0, 0)]
                        side "c r":
                            align(0, 0.98)
                            viewport id "girlprofile_magic_vp":
                                xysize (165, 90)
                                draggable True
                                mousewheel True
                                vbox:
                                    spacing -7
                                    for entry in chr.magic_skills:
                                        frame:
                                            xysize (144, 10)
                                            button:
                                                background Null()
                                                xysize (144, 10)
                                                action NullAction()
                                                text "[entry.name]" idle_color ivory hover_color red size(15) xanchor(10)
                                                hovered tt.action(entry)
                            vbar value YScrollValue("girlprofile_magic_vp")
                    
    frame:
        background Frame(Transform("content/gfx/frame/ink_box.png"), 10, 10) ##alpha=0.5
        yalign(0.998)
        xanchor -321
        xpadding 10
        xysize (955, 100)
        has hbox spacing 1
        if isinstance(tt.value, BE_Action):
            $ element = tt.value.get_element()
            if element:
                frame:
                    background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                    xysize (70, 70)
                    if element.icon:
                        $ img = ProportionalScale(element.icon, 70, 70)
                        add img align (0.5, 0.5)
            text tt.value.desc style "content_text" size 20 color ivory yalign 0.1
        else:        
            text (u"{=content_text}{color=[ivory]}%s" % tt.value)
            
    use pyt_top_stripe(True)
    
screen pyt_girl_control:
    modal True
    zorder 1
    
    frame:
        style_group "content"
        at slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)
        background Frame("content/gfx/frame/p_frame52.png", 10, 10)
        xpos 936
        yalign 0.95
        xysize(343, 675)
        
        # Tooltip Related:
        default tt = Tooltip("Adjust your girls behaviour here.")
        frame:
            background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
            align(0.5, 0.88)
            xysize (320, 120)
            xpadding 13
            ypadding 15
            has vbox
            text (u"{color=[ivory]}%s" % tt.value) outlines [(1, "#424242", 0, 0)]
        
        frame:
            background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.7), 10, 10)
            align (0.6, 0.08)
            xpadding 10
            ypadding 10
            xysize (225, 120)
            button:
                style_group "basic"
                xysize (150, 33)
                align (0.5, 0.05)
                action ToggleDict(chr.autocontrol, "Tips")
                hovered tt.action("Allow girls to keep their tips!")
                text "Tips:" align (0.0, 0.5)
                if chr.autocontrol['Tips']:
                    add (im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (1.0, 0.5)
                else:
                    add (im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (1.0, 0.5)

            fixed:
                align (0.5, 1.0)
                xysize (200, 30)
                hbox:
                    align (0.5, 0.0)
                    vbox:
                        xmaximum 130
                        xfill True
                        text (u"{color=[ivory]}Wage percentage:") outlines [(1, "#424242", 0, 0)]
                    vbox:    
                        text (u"{color=[ivory]}%d %%" % chr.mech_relay['wagemod']) outlines [(1, "#424242", 0, 0)]
                bar:
                    align (0.5, 1.0)
                    value FieldValue(chr, 'wagemod', 200, max_is_zero=False, style='scrollbar', offset=0, step=1)
                    xmaximum 150
                    thumb 'content/gfx/interface/icons/move15.png'
                         
        # BE Row, Job controls + Auto-Buy/Equip
        vbox:
            style_group "basic"
            align (0.55, 0.5)
            button:
                action If(chr.status != "slave", true=ToggleField(chr, "front_row"))
                xysize (200, 32)
                text "Front Row" align (0.0, 0.5)
                if chr.front_row:
                    add (im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (1.0, 0.5)
                elif not chr.front_row:
                    add (im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (1.0, 0.5)
            
            button:
                action ToggleDict(chr.autocontrol, "Rest")
                xysize (200, 32)
                text "Auto Rest" align (0.0, 0.5)
                if chr.autocontrol['Rest']:
                    add (im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (1.0, 0.5)
                elif not chr.autocontrol['Rest']:
                    add (im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (1.0, 0.5)
             
            # Autobuy: 
            button:
                action  If(chr.status != "slave" and chr.disposition > 950, true=ToggleField(chr, "autobuy"))
                xysize (200, 32)
                text "Auto Buy" align (0.0, 0.5)
                if chr.autobuy:
                    add (im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (1.0, 0.5)
                else:
                    add (im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (1.0, 0.5)
                    
            # Autoequip
            button:
                xysize (200, 32)
                action If(chr.status == "slave" or (chr.status != "slave" and chr.disposition > 850), true=ToggleField(chr, "autoequip"))
                text "Auto Equip" align (0.0, 0.5)
                if chr.autoequip:
                    add(im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (1.0, 0.5)
                else:
                    add(im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (1.0, 0.5)
            # ------------------------------------------------------------------------------------------------------------------------------------->>>        
               
            # Disabled until Beta release        
            # if chr.action in ["Whore", "ServiceGirl", "Stripper"]:
                # null height 10
                # hbox:
                    # spacing 20
                    # if chr.autocontrol['SlaveDriver']:
                        # textbutton "{color=[red]}Slave Driver":
                            # yalign 0.5
                            # action Return(['girl_cntr', 'slavedriver'])
                            # minimum(150, 20)
                            # maximum(150, 20)
                            # xfill true
                        # add(im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) yalign 0.5
                    # elif not chr.autocontrol['SlaveDriver']:
                        # textbutton "Slave Driver":
                            # yalign 0.5
                            # action Return(['girl_cntr', 'slavedriver'])
                            # minimum(150, 20)
                            # maximum(150, 20)
                            # xfill true
                        # add(im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) yalign 0.5

            null height 30
            
            # if chr.action == "Whore":
                # for key in chr.autocontrol['Acts']:
                    # null height 10
                    # hbox:
                        # spacing 20
                        # textbutton [key.capitalize()]:
                            # yalign 0.5
                            # action Return(['girl_cntr', 'set_act', key])
                            # minimum(150, 20)
                        # if chr.autocontrol['Acts'][key]:
                            # add(im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) yalign 0.5
                        # elif not chr.autocontrol['Acts'][key]:
                            # add(im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) yalign 0.5
            
            if chr.action == "ServiceGirl":
                for key in chr.autocontrol['S_Tasks']:
                    button:
                        action ToggleDict(chr.autocontrol['S_Tasks'], key)
                        xysize (200, 30)
                        text (key.capitalize()) align (0.0, 0.5)
                        if chr.autocontrol['S_Tasks'][key]:
                            add (im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)) align (1.0, 0.5)
                        elif not chr.autocontrol['S_Tasks'][key]:
                            add (im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)) align (1.0, 0.5)
        
        button:
            style_group "basic"
            action Hide("pyt_girl_control")
            minimum(50, 30)
            align (0.5, 0.95)
            text  "OK"
        
screen confirm_girl_sale:
    modal True
    zorder 1
    
    frame:
        align(0.5, 0.5)
        minimum(300, 200)
        maximum(300, 200)
        xfill True
        yfill True
        
        if chr.status == "slave":
            text("{size=-5}Are you sure you want to sell %s for %d Gold?"%(chr.name, int(chr.fin.get_price()*0.8))) align(0.5, 0.1)
            
            hbox:
                align(0.5, 0.85)
                spacing 40
                textbutton "No":
                    action Hide("confirm_girl_sale")
                textbutton "Yes":
                    action Return(['control', 'sell'])
            
        else:
            text("{size=-5}Are you sure you want to fire the %s?"%chr.name) align(0.5, 0.1)
            
            hbox:
                align(0.5, 0.85)
                spacing 40
                textbutton "No":
                    action Hide("confirm_girl_sale")
                textbutton "Yes":
                    action Return(['control', 'fire'])
        

screen pyt_girl_finances():
    modal True
    zorder 1
    
    default show_fin = "day"
    
    frame:
        at slide(so1=(0, 700), t1=0.7, so2=(0, 0), t2=0.3, eo2=(0, -config.screen_height))
        background Frame (Transform("content/gfx/frame/arena_d.png", alpha=1.2), 5, 5)
        align (0.5, 0.5)
        
        # side "c r":
        viewport id "message_vp":
            style_group "stats"
            xysize (1100, 600)
            draggable False
            mousewheel True
            if day > 1 and chr.fin.game_fin_log.has_key(str(day-1)):
                $ fin_inc = chr.fin.game_fin_log[str(day-1)][0]
                $ fin_exp = chr.fin.game_fin_log[str(day-1)][1]
                
                if show_fin == 'day':
                    label (u"{color=[ivory]}Fin Report (Yesterday)") xalign 0.4 ypos 30 text_size 30
                    # Income:
                    vbox:
                        pos (50, 100)
                        label "Income:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 150
                                xfill True
                                for key in fin_inc["work"]:
                                    text ("[key]")
                                for key in fin_inc["tips"]:
                                    text ("[key]")
                                for key in fin_inc:
                                    if key not in ["work", "tips", "private"]:
                                        text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in fin_inc["work"]:
                                    $ val = fin_inc["work"][key]
                                    text "[val]" style "stats_value_text"
                                for key in fin_inc["tips"]:
                                    $ val = fin_inc['tips'][key]
                                    text "[val]" style "stats_value_text"
                                for key in fin_inc:
                                    if key not in ["work", "tips", "private"]:
                                        $ val = fin_inc[key]
                                        text "[val]" style "stats_value_text"
                    # Expense:
                    vbox:
                        pos (450, 100)
                        label "Expense:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 150
                                xfill True
                                for key in fin_exp["cost"]:
                                    text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in fin_exp["cost"]:
                                    $ val = fin_exp["cost"][key]
                                    text ("[val]") style "stats_value_text"
                                    
                    python:
                        total_list = list(itertools.chain(fin_inc["work"].values(),
                                                                      fin_inc["tips"].values()))
                        total_income = sum(total_list)
                        total_expenses = 0
                        for key in fin_exp["cost"]:
                            total_expenses += fin_exp["cost"][key]
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
                        textbutton "Show Total" action SetScreenVariable("show_fin", 'total') minimum (200, 30)
                        textbutton "Show Personal" action SetScreenVariable("show_fin", 'personal') minimum (200, 30)
                        textbutton "Show P. Total" action SetScreenVariable("show_fin", 'personal_total') minimum (200, 30)
                    
                elif show_fin == 'total':
                    label (u"Fin Report (Game)") xalign 0.4 ypos 30 text_size 30
                    python:
                        income = dict()
                        for _day in chr.fin.game_fin_log:
                            for key in chr.fin.game_fin_log[_day][0]["work"]:
                                income[key] = income.get(key, 0) + chr.fin.game_fin_log[_day][0]["work"][key]
                            for key in chr.fin.game_fin_log[_day][0]["tips"]:
                                income[key] = income.get(key, 0) + chr.fin.game_fin_log[_day][0]["tips"][key]
                                
                    # Income:
                    vbox:
                        pos (50, 100)
                        label "Income:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 150
                                xfill True
                                for key in income:
                                    text "[key]"
                            vbox:
                                null height 1
                                spacing 4
                                for key in income:
                                    $ val = income[key]
                                    text "[val]" style "stats_value_text"
                                    
                    # Expense:
                    python:
                        expenses = dict()
                        for _day in chr.fin.game_fin_log:
                            for key in chr.fin.game_fin_log[_day][1]["cost"]:
                                expenses[key] = expenses.get(key, 0) + chr.fin.game_fin_log[_day][1]["cost"][key]
                    vbox:
                        pos (450, 100)
                        label "Expense:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 150
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
                        for _day in chr.fin.game_fin_log:
                            total_list = list(itertools.chain(chr.fin.game_fin_log[_day][0]["work"].values(),
                                                                          chr.fin.game_fin_log[_day][0]["tips"].values()))
                            total_income = sum(total_list)
                            total_expenses = 0
                            for key in chr.fin.game_fin_log[_day][1]["cost"]:
                                total_expenses += chr.fin.game_fin_log[_day][1]["cost"][key]
                            total = total_income - total_expenses
                            game_total += total
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
                        textbutton "Show Daily" action SetScreenVariable("show_fin", 'day') minimum(200, 30)
                        textbutton "Show Personal" action SetScreenVariable("show_fin", 'personal') minimum(200, 30)
                        textbutton "Show P. Total" action SetScreenVariable("show_fin", 'personal_total') minimum(200, 30)
                    
                elif show_fin == 'personal':
                    label (u"Personal (Yesterday)") xalign 0.4 ypos 30 text_size 30
                    
                    # Income:
                    vbox:
                        pos (50, 100)
                        label "Income:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 150
                                xfill True
                                for key in fin_inc["private"]:
                                    text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in fin_inc["private"]:
                                    $ val = fin_inc["private"][key]
                                    text ("[val]") style "stats_value_text"
                     
                    # Expense:
                    vbox:
                        pos (450, 100)
                        label "Expense:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 150
                                xfill True
                                for key in fin_exp["private"]:
                                    text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in fin_exp["private"]:
                                    $ val = fin_exp["private"][key]
                                    text ("[val]") style "stats_value_text"
                                
                    python:
                        total_income = 0
                        for key in fin_inc["private"]:
                            total_income += fin_inc["private"][key]
                        total_expenses = 0
                        for key in fin_exp["private"]:
                            total_expenses += fin_exp["private"][key]
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
                        textbutton "Show Total" action SetScreenVariable("show_fin", 'total') minimum(200, 30)
                        textbutton "Show Daily" action SetScreenVariable("show_fin", 'daily') minimum(200, 30)
                        textbutton "Show P. Total" action SetScreenVariable("show_fin", 'personal_total') minimum(200, 30)
                    
                elif show_fin == 'personal_total':
                    label (u"Personal (Total)") xalign 0.4 ypos 30 text_size 30
                    
                    python:
                        income = dict()
                        for _day in chr.fin.game_fin_log:
                            for key in chr.fin.game_fin_log[_day][0]["private"]:
                                income[key] = income.get(key, 0) + chr.fin.game_fin_log[_day][0]["private"][key]
                                    
                    # Income:
                    vbox:
                        pos (50, 100)
                        label "Income:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 150
                                xfill True
                                for key in income:
                                    text ("[key]")
                            vbox:
                                null height 1
                                spacing 4
                                for key in income:
                                    $ val = income[key]
                                    text ("[val]") style "stats_value_text"
                      
                    # Expense:
                    python:
                        expenses = dict()
                        for _day in chr.fin.game_fin_log:
                            for key in chr.fin.game_fin_log[_day][1]["private"]:
                                expenses[key] = expenses.get(key, 0) + chr.fin.game_fin_log[_day][1]["private"][key]
                    vbox:
                        pos (450, 100)
                        label "Expense:" text_size 20
                        null height 10
                        hbox:
                            vbox:
                                xmaximum 150
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
                        textbutton "Show Daily" action SetScreenVariable("show_fin", 'day') minimum(200, 30)
                        textbutton "Show Peronal" action SetScreenVariable("show_fin", 'personal') minimum(200, 30)
                        textbutton "Show Total" action SetScreenVariable("show_fin", 'total') minimum(200, 30)
                    
            else:
                text (u"No financial records availible!") align (0.5, 0.5)

            button:
                style_group "basic"
                action Hide('pyt_girl_finances')
                minimum (250, 30)
                align (0.5, 0.96)
                text "OK"