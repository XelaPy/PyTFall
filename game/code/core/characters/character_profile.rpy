label char_profile:

    if not hasattr(store, "girls") or girls is None or char not in girls:
        $ girls = list(girl for girl in hero.chars if girl.action != "Exploring")
        # TODO !!! Find a solid way to handle this.

    scene bg scroll
    $ renpy.retain_after_load()
    show screen char_profile
    with dissolve

    # reset the_chosen so it doesn't mess with any future checks.
    $ the_chosen = None

    while 1:
        $ result = ui.interact()

        if isinstance(result, (list, tuple)):
            # If the girl has runaway
            if char in pytfall.ra:
                if result[0] == "girl":
                    if result[1] == "gallery":
                        $ tl.start("Loading Gallery")
                        $ gallery = PytGallery(char)
                        $ tl.end("Loading Gallery")
                        jump gallery
                    elif result[1] == "get_rid":
                        if renpy.call_screen("yesno_prompt", message="Are you sure you wish to stop looking for %s?"%char.name, yes_action=Return(True), no_action=Return(False)):
                            python:
                                hero.remove_char(char)
                                girls.remove(char)
                                char.disposition -= 400
                                if char in hero.team:
                                    hero.team.remove(char)

                                char.action = None

                                if char.status == "slave":
                                    set_location(char, pytfall.sm)
                                else:
                                    set_location(char, store.locations["City"])

                            if girls:
                                $ index = (index+1) % len(girls)
                                $ char = girls[index]
                            else:
                                jump char_profile_end
                    else:
                        $ renpy.show_screen("message_screen", "This girl has run away!")
                elif result[0] != "control":
                    $ renpy.show_screen("message_screen", "This girl has run away!")
            # Else if you still have the girl
            else:
                if result[0] == "jump":
                    if result[1] == "item_transfer":
                        hide screen char_profile
                        $ items_transfer([hero, char])
                        show screen char_profile
                elif result[0] == "dropdown":
                    python:
                        if result[1] == "workplace":
                            renpy.show_screen("set_workplace_dropdown", result[2], pos=renpy.get_mouse_pos())
                        elif result[1] == "home":
                            renpy.show_screen("set_home_dropdown", result[2], pos=renpy.get_mouse_pos())
                        elif result[1] == "action":
                            renpy.show_screen("set_action_dropdown", result[2], pos=renpy.get_mouse_pos())
                elif result[0] == "girl":
                    if result[1] == "gallery":
                        $ tl.start("Loading Gallery")
                        $ gallery = PytGallery(char)
                        $ tl.end("Loading Gallery")
                        jump gallery
                    elif result[1] == "get_rid":
                        if char.status == "slave":
                            $ message = "Are you sure you wish to sell {} for {}?".format(char.name, int(char.fin.get_price()*.8))
                        else:
                            $ message = "Are you sure that you wish to fire {}?".format(char.name)
                        if renpy.call_screen("yesno_prompt",
                                             message=message,
                                             yes_action=Return(True),
                                             no_action=Return(False)):
                            if char.status == 'slave':
                                python:
                                    hero.add_money(int(char.fin.get_price()*.8), reason="SlaveTrade")
                                    char.home = pytfall.sm
                                    char.action = None
                                    char.workplace = None
                                    set_location(char, char.home)
                            else:
                                if char.disposition >= 500:
                                    $ block_say = True
                                    call interactions_good_goodbye from _call_interactions_good_goodbye
                                    $ block_say = False
                                else:
                                    $ block_say = True
                                    call interactions_bad_goodbye from _call_interactions_bad_goodbye
                                    $ block_say = False

                                python:
                                    char.disposition -= 400
                                    char.home = locations["City Apartments"]
                                    char.action = None
                                    char.workplace = None
                                    set_location(char, locations["City"])
                            python:
                                hero.remove_char(char)
                                index = girls.index(char) # Index is not set otherwise???
                                girls.remove(char)
                            if char in hero.team:
                                $ hero.team.remove(char)
                            if girls:
                                $ index = (index + 1) % len(girls)
                                $ char = girls[index]
                            else:
                                jump char_profile_end
                elif result[0] == "rename":
                    if result[1] == "name":
                        $ n = renpy.call_screen("pyt_input", char.name, "Enter Name", 20)
                        if len(n):
                            $ char.name = n
                    if result[1] == "nick":
                        $ n = renpy.call_screen("pyt_input", char.nickname, "Enter Nick Name", 20)
                        if len(n):
                            $ char.nickname = n
                    if result[1] == "full":
                        $ n = renpy.call_screen("pyt_input", char.fullname, "Enter Full Name", 20)
                        if len(n):
                            $ char.fullname = n

            if result[0] == 'control':
                $ index = girls.index(char)
                if result[1] == 'left':
                    $ index = (index - 1) % len(girls)
                    $ char = girls[index]
                    hide screen show_trait_info
                elif result[1] == 'right':
                    $ index = (index + 1) % len(girls)
                    $ char = girls[index]
                    hide screen show_trait_info
                elif result[1] == 'return':
                    jump char_profile_end

label char_profile_end:
    hide screen char_profile

    $ girls = None

    if char_profile:
        $ last_label, char_profile = char_profile, None
        jump expression last_label
    else:
        jump chars_list


screen char_profile():

    key "mousedown_4" action Return(["control", "right"])
    key "mousedown_5" action Return(["control", "left"])
    key "mousedown_3" action Return(['control', 'return'])

    on "hide":
        action Hide("show_trait_info")

    default stats_display = "main"

    $ not_escaped = char not in pytfall.ra

    if girls:
        # Picture and left/right buttons ====================================>
        frame:
            background Frame("content/gfx/frame/p_frame6.png", 10, 10)
            align .5, .5
            xysize 620, 700
            # in these cases we are less strict with NSFW pictures:
            if check_lovers(char, hero) or "Exhibitionist" in char.traits:
                $ img = char.show('profile', resize=(590, 600), cache=True)
            elif check_friends(hero, char):
                $ img = char.show('profile', resize=(590, 600), exclude=["nude"], cache=True)
            else:
                python:
                    img = char.show('profile', resize=(590, 600),
                                    exclude=["nude", "revealing", "lingerie", "swimsuit"], cache=True)

            python:
                image_tags = img.get_image_tags()
                tt_str = "\n".join(["Click to interact with {}!".format(char.nickname),
                                    "{}".format(char.desc)])

            if "Exhibitionist" in char.traits:
                $ gm_img = char.show("girlmeets", resize=gm.img_size)
            elif check_friends(hero, char) or check_lovers(char, hero):
                $ gm_img = char.show("girlmeets", exclude=["nude"], resize=gm.img_size)
            else:
                python:
                    gm_img = char.show("girlmeets",
                                       exclude=["nude",
                                                "revealing",
                                                "lingerie",
                                                "swimsuit"],
                                       resize=gm.img_size)

            if "no bg" in image_tags:
                $ frame_image = "content/gfx/frame/MC_bg3_white.png"
            else:
                $ frame_image = "content/gfx/frame/MC_bg3.png"
            $ bg = Frame(frame_image, 10, 10)
            $ hbg = Frame(im.MatrixColor(frame_image, im.matrix.brightness(.1)), 10, 10)

            button:
                align .5, .38
                padding 4, 4
                background bg
                hover_background hbg
                action If(not_escaped,
                          true=[Hide("char_profile"),
                                With(dissolve),
                                Function(gm.start_int, char, img=gm_img)],
                          false=NullAction())
                tooltip tt_str
                add img

        # Mid-Bottom Frame: Level, experience ====================================>
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.9), 10, 10)
            align .5, 1.0
            xysize 630, 64
            padding 15, 10
            has hbox spacing 20 xalign .5
            button:
                xysize 140, 40
                yalign .5
                style "left_wood_button"
                action Hide("show_trait_info"), Return(['control', 'left'])
                text "Previous Girl" style "wood_text" xalign(.69)
                tooltip "<== Previous Girl"
            fixed:
                align .5, .5
                xysize 230, 45
                add pscale("content/gfx/frame/level.png", 230, 45) align .5, .5
                text "{font=fonts/Rubius.ttf}{color=[ivory]}{size=16}{b}[char.level]" pos 38, 7
                text "{font=fonts/Rubius.ttf}{color=[ivory]}{size=16}{b}[char.exp]" pos 114, 7
                text "{font=fonts/Rubius.ttf}{color=[ivory]}{size=16}{b}[char.goal]" pos 114, 27
            button:
                xysize 140, 40
                yalign .5
                style "right_wood_button"
                action Hide("show_trait_info"), Return(['control', 'right'])
                text "Next Girl" style "wood_text" xalign .19
                tooltip "Next Girl ==>"

        # Left Frame with most of the info ====================================>
        frame:
            align .0, 1.0
            xysize 340, 680
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
            style_group "content"
            # # Base frame ====================================>
            # # Prof-Classes ==================================>
            python:
                if len(char.traits.basetraits) == 1:
                    classes = list(char.traits.basetraits)[0].id
                elif len(char.traits.basetraits) == 2:
                    classes = list(char.traits.basetraits)
                    classes.sort()
                    classes = ", ".join([str(c) for c in classes])
                else:
                    raise Exception("Character without prof basetraits detected in girlsprofile screen")

                trait = char.personality
                img = ProportionalScale("".join(["content/gfx/interface/images/personality/", trait.id.lower(), ".png"]), 120, 120)

            fixed:
                xoffset 4
                align .0, .0
                xysize 330, 126
                imagebutton:
                    at pers_effect()
                    focus_mask True
                    xcenter 55
                    ycenter 65
                    idle img
                    hover img
                    action Show("show_trait_info", trait=trait.id, place="main_trait")
                    tooltip "{}".format("\n".join([trait.id, trait.desc]))

                add Transform("content/gfx/frame/base_frame.png", alpha=.9, size=(330, 126)):
                    xoffset -5

                label "[classes]":
                    text_color gold
                    if len(classes) < 18:
                        text_size 17
                        pos 113, 100
                    else:
                        text_size 15
                        pos 113, 98
                    text_outlines [(2, "#424242", 0, 0)]
                    pos 113, 100
                    anchor 0, 1.0

                textbutton "[char.name]":
                    background Null()
                    text_style "content_label_text"
                    text_color gold text_hover_color green
                    text_outlines [(2, "#424242", 0, 0)]
                    pos 100, 47
                    anchor 0, 1.0
                    if len(char.name) < 15:
                        text_size 21
                    else:
                        text_size 18
                    action Show("char_rename", char=char)
                    tooltip "Click to rename {} (renaming is limited for free girls).".format(char.fullname)

                label "Tier:  [char.tier]":
                    text_color gold
                    text_outlines [(2, "#424242", 0, 0)]
                    pos 113, 77
                    anchor 0, 1.0

                imagebutton:
                    if char.status == "slave":
                        pos 80, 97
                        idle ProportionalScale("content/gfx/interface/icons/slave.png", 30, 30)
                        hover (im.MatrixColor(ProportionalScale("content/gfx/interface/icons/slave.png", 30, 30), im.matrix.brightness(.25)))
                        tooltip "This girl is a slave!"
                    else:
                        pos 75, 95
                        idle ProportionalScale("content/gfx/interface/icons/free.png", 30, 30)
                        hover (im.MatrixColor(ProportionalScale("content/gfx/interface/icons/free.png", 30, 30), im.matrix.brightness(.25)))
                        tooltip "This girl is free as a bird :)"
                    action NullAction()

            # Locations/Action Buttons and Stats/Info ====================================>
            fixed:
                xysize 300, 60
                ypos 130
                vbox:
                    button:
                        style_group "ddlist"
                        if char.status == "slave":
                            action Return(["dropdown", "home", char])
                            tooltip "Choose a place for %s to live at!" % char.nickname
                        else: # Can't set home for free chars, they decide it on their own.
                            action NullAction()
                            tooltip "%s is a free citizen and decides on where to live at!" % char.nickname
                        text "{image=button_circle_green}Home: [char.home]":
                            size 18
                    button:
                        style_group "ddlist"
                        action Return(["dropdown", "workplace", char])
                        tooltip "Choose a place for %s to work at!" % char.nickname
                        text "{image=button_circle_green}Work: [char.workplace]":
                            size 18
                    button:
                        style_group "ddlist"
                        action Return(["dropdown", "action", char])
                        tooltip "Choose a task for %s to do!" % char.nickname
                        text "{image=button_circle_green}Action: [char.action]":
                            size 18

            hbox:
                style_group "basic"
                xalign .5 ypos 196
                button:
                    yalign .5
                    action SetScreenVariable("stats_display", "main"), With(dissolve)
                    text "Main" size 15
                    tooltip "Show Main Info!"
                button:
                    yalign .5
                    action SetScreenVariable("stats_display", "stats"), With(dissolve)
                    text "Stats" size 15
                    tooltip "Show Stats!"
                button:
                    yalign .5
                    action SetScreenVariable("stats_display", "skills"), With(dissolve)
                    text "Skills" size 15
                    tooltip "Show Skills!"
                if DEBUG:
                    button:
                        yalign .5
                        action SetScreenVariable("stats_display", "dev_skills"), With(dissolve)
                        text "S" size 15
                        tooltip "Show devmod skills"

            $ base_ss = char.stats.get_base_ss()

            if stats_display == "main":
                frame:
                    style_prefix "proper_stats"
                    style_suffix "main_frame"
                    xsize 300
                    ypos 230 xalign .5
                    has vbox spacing 1

                    frame:
                        xoffset 4
                        xysize (270, 27)
                        xpadding 7
                        text "Health:" color "#CD4F39"
                        if "health" in base_ss:
                            button:
                                xysize 20, 20
                                offset -10, -5
                                background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                                action NullAction()
                                tooltip "This is a Class Stat!"
                        if char.health <= char.get_max("health")*.3:
                            text (u"{color=[red]}%s/%s"%(char.health, char.get_max("health"))) xalign 1.0 style_suffix "value_text"
                        else:
                            text (u"%s/%s"%(char.health, char.get_max("health"))) xalign 1.0 style_suffix "value_text"
                    frame:
                        xoffset 4
                        xysize (270, 27)
                        xpadding 7
                        text "Vitality:" color "#43CD80"
                        if "vitality" in base_ss:
                            button:
                                xysize 20, 20
                                offset -10, -5
                                background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                                action NullAction()
                                tooltip "This is a Class Stat!"
                        if char.vitality < char.get_max("vitality")*.3:
                            text (u"{color=[red]}%s/%s"%(char.vitality, char.get_max("vitality"))) xalign 1.0 style_suffix "value_text"
                        else:
                            text (u"%s/%s"%(char.vitality, char.get_max("vitality"))) xalign 1.0 style_suffix "value_text"

                    $ stats = [("MP", "#009ACD"), ("Luck", "#00FA9A")]
                    for stat, color in stats:
                        frame:
                            xoffset 4
                            xysize (270, 27)
                            xpadding 7
                            text "[stat]" color color
                            if stat.lower() in base_ss:
                                button:
                                    xysize 20, 20
                                    offset -10, -5
                                    background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                                    action NullAction()
                                    tooltip "This is a Class Stat!"
                            text "{}/{}".lower().format(getattr(char, stat.lower()), char.get_max(stat.lower())) style_suffix "value_text" color color

                    null height 10

                    $ stats = ["joy", "disposition"]
                    for stat in stats:
                        frame:
                            xoffset 4
                            xysize (270, 27)
                            xpadding 7
                            text '{}'.format(stat.capitalize()) color "#79CDCD"
                            if stat.lower() in base_ss:
                                button:
                                    xysize 20, 20
                                    offset -10, -5
                                    background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                                    action NullAction()
                                    tooltip "This is a Class Stat!"
                            text ('%d/%d'%(getattr(char, stat), char.get_max(stat))) xalign 1.0 style_suffix "value_text"

                    null height 10

                    frame:
                        xoffset 4
                        xysize (270, 27)
                        xpadding 7
                        text "Gold:" color gold
                        text (u"{color=[gold]}[char.gold]") xalign 1.0 style_suffix "value_text"
                    frame:
                        xoffset 4
                        xysize (270, 27)
                        xpadding 7
                        text "{color=#79CDCD}Upkeep:"
                        text u"%s"%(char.fin.get_upkeep()) xalign 1.0 style_suffix "value_text"
                    if char.status == "slave":
                        frame:
                            xoffset 4
                            xysize (270, 27)
                            xpadding 7
                            text "{color=#79CDCD}Market Price:"
                            text (u"%s"%(char.fin.get_price())) xalign 1.0 style_suffix "value_text"

                use race_and_elements(char=char)
            elif stats_display == "stats":
                frame:
                    style_prefix "proper_stats"
                    style_suffix "main_frame"
                    xsize 300
                    ypos 230 xalign .5
                    has vbox spacing 1
                    $ stats = ["charisma", "character", "reputation", "constitution", "intelligence"]
                    for stat in stats:
                        frame:
                            xoffset 4
                            xysize (270, 27)
                            xpadding 7
                            text '{}'.format(stat.capitalize()) color "#79CDCD"
                            if stat.lower() in base_ss:
                                button:
                                    xysize 20, 20
                                    offset -10, -5
                                    background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                                    action NullAction()
                                    tooltip "This is a Class Stat!"
                            text ('%d/%d'%(getattr(char, stat), char.get_max(stat))) xalign 1.0 style_suffix "value_text"

                    null height 10

                    $ stats = [("Attack", "#CD4F39"), ("Defence", "#dc762c"), ("Magic", "#8470FF"), ("Agility", "#1E90FF")]
                    for stat, color in stats:
                        frame:
                            xoffset 4
                            xysize (270, 27)
                            xpadding 7
                            text "[stat]" color color
                            if stat.lower() in base_ss:
                                button:
                                    xysize 20, 20
                                    offset -10, -5
                                    background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                                    action NullAction()
                                    tooltip "This is a Class Stat!"
                            text "{}/{}".lower().format(getattr(char, stat.lower()), char.get_max(stat.lower())) style_suffix "value_text" color color
                use race_and_elements(char=char)
            elif stats_display == "skills":
                frame:
                    style_prefix "proper_stats"
                    style_suffix "main_frame"
                    xsize 300
                    ypos 230 xalign .5
                    has viewport scrollbars "vertical" xysize (310, 392) mousewheel True child_size (300, 1000)
                    vbox:
                        spacing 1
                        xpos 10
                        for skill in char.stats.skills:
                            $ skill_val = int(char.get_skill(skill))
                            $ skill_limit = int(char.get_max_skill(skill))
                            # We don't care about the skill if it's less than 10% of limit:
                            if skill in base_ss or skill_val/float(skill_limit) > .1:
                                hbox:
                                    xsize 250
                                    text "{}:".format(skill.capitalize()):
                                        style_suffix "value_text"
                                        color gold
                                        xalign .0
                                        size 18
                                    hbox:
                                        xalign 1.0
                                        yoffset 8
                                        $ step = skill_limit/10.0
                                        for i in range(5):
                                            if (2*step) <= skill_val:
                                                add Transform("content/gfx/interface/icons/stars/star2.png", size=(18, 18))
                                                $ skill_val -= 2*step
                                            elif step <= skill_val:
                                                add Transform("content/gfx/interface/icons/stars/star3.png", size=(18, 18))
                                                $ skill_val -= step
                                            else:
                                                add Transform("content/gfx/interface/icons/stars/star1.png", size=(18, 18))
                    vbox:
                        spacing 1
                        for skill in char.stats.skills:
                            $ skill_val = int(char.get_skill(skill))
                            $ skill_limit = int(char.get_max_skill(skill))
                            # We don't care about the skill if it's less than 10% of limit:
                            if skill in base_ss or skill_val/float(skill_limit) > .1:
                                if skill in base_ss:
                                    fixed:
                                        xysize 20, 26
                                        button:
                                            xysize 20, 20
                                            background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                                            action NullAction()
                                            tooltip "This is a Class Skill!"
                                else:
                                    null height 26
            elif stats_display == "dev_skills":
                frame:
                    style_prefix "proper_stats"
                    style_suffix "main_frame"
                    xsize 300
                    ypos 230 xalign .5
                    has viewport scrollbars "vertical" xysize(310, 392) mousewheel True child_size (300, 1000)
                    vbox spacing 1:
                        for skill in char.stats.skills:
                            $ skill_val = int(char.get_skill(skill))
                            if DEBUG or skill_val > char.level * 10:
                                frame:
                                    xoffset 4
                                    xysize (270, 27)
                                    xpadding 7
                                    text "{}:".format(skill.capitalize())
                                    text "{true} <{action}, {training}>".format(true=skill_val, action=int(char.stats.skills[skill][0]), training=int(char.stats.skills[skill][1])) style_suffix "value_text"

        # Right frame ====================================>
        frame:
            align 1.0, 1.0
            xysize 340, 680
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)

            # Buttons ====================================>
            frame:
                background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.9), 10, 10)
                xalign .5 ypos 1
                xysize 325, 150
                has hbox style_group "wood" align .5, .5 spacing 5

                vbox:
                    spacing 5
                    button:
                        xysize (150, 40)
                        action Hide("show_trait_info"), If(not_escaped, true=Show("char_control"))
                        tooltip "Set desired behavior for {}!".format(char.nickname)
                        text "Girl Control"
                    button:
                        xysize (150, 40)
                        action If(not_escaped, true=[Hide("char_profile"), With(dissolve), SetVariable("eqtarget", char), Jump('char_equip')])
                        tooltip "Manage this girl's inventory and equipment!"
                        text "Equipment"
                    button:
                        xysize (150, 40)
                        action [Hide("char_profile"), With(dissolve), Return(["girl", "gallery"])]
                        tooltip "View this girl's gallery!\n(building a gallery may take some time for large packs)"
                        text "Gallery"

                vbox:
                    spacing 5
                    button:
                        xysize (150, 40)
                        action If(not_escaped, true=[Hide("char_profile"), With(dissolve), Jump('school_training')])
                        tooltip "Send her to School!"
                        text "Training"
                    button:
                        xysize (150, 40)
                        action Hide("show_trait_info"), If(not_escaped, true=Show("finances", None, char, mode="logical"))
                        tooltip "Review Finances!"
                        text "Finances"
                    button:
                        xysize (150, 40)
                        action If(not_escaped, true=Return(["girl", "get_rid"]))
                        tooltip "Get rid of her!"
                        if char.status == "slave":
                            text "Sell"
                        else:
                            text "Dismiss"

            # AP ====================================>
            frame:
                xalign .5 ypos 160
                xysize 300, 90
                background ProportionalScale("content/gfx/frame/frame_ap.png", 300, 100)
                label ("[char.AP]"):
                    pos (200, 0)
                    style "content_label"
                    text_color ivory
                    text_size 28

            # Traits/Effects/Attacks/Magix ====================================>
            frame:
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6))
                xsize 335 ypos 230 xalign .5
                style_group "proper_stats"
                padding 7, 8
                has vbox spacing 2 xoffset 4
                # Traits/Effects ====================================>
                hbox:
                    # Traits:
                    vbox:
                        xysize (160, 210)
                        label (u"Traits:") text_size 20 text_color ivory text_bold True xalign .5
                        viewport:
                            xysize (160, 165)
                            scrollbars "vertical"
                            draggable True
                            mousewheel True
                            has vbox spacing 1
                            for trait in list(t for t in char.traits if not any([t.basetrait, t.personality, t.race, t.elemental])):
                                if not trait.hidden:
                                    frame:
                                        xsize 147
                                        button:
                                            background Null()
                                            xsize 147
                                            action Show("show_trait_info", trait=trait.id)
                                            text trait.id idle_color ivory align .5, .5 hover_color crimson text_align .5 size min(15, int(250 / max(1, len(trait.id))))
                                            tooltip "%s" % trait.desc
                                            hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(.10)), 5, 5)
                    # Effects:
                    vbox:
                        xysize (160, 210)
                        label (u"Effects:") text_size 20 text_color ivory text_bold True xalign .5
                        viewport:
                            xysize (160, 165)
                            scrollbars "vertical"
                            draggable True
                            mousewheel True
                            has vbox spacing 1
                            for effect in char.effects.itervalues():
                                frame:
                                    xysize (147, 25)
                                    button:
                                        background Null()
                                        xysize (147, 25)
                                        action NullAction()
                                        text "[effect.name]" idle_color ivory align .5, .5 hover_color crimson size min(15, int(250 / max(1, len(effect.name))))
                                        tooltip "%s" % effect.desc
                                        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(.10)), 5, 5)

                # Attacks/Magic ====================================>
                hbox:
                    vbox:
                        xysize (160, 210)
                        label (u"Attacks:") text_size 20 text_color ivory text_bold True xalign .5 text_outlines [(3, "#3a3a3a", 0, 0), (2, "#8B0000", 0, 0), (1, "#3a3a3a", 0, 0)]
                        viewport:
                            xysize (160, 165)
                            scrollbars "vertical"
                            draggable True
                            mousewheel True
                            has vbox spacing 1
                            for entry in char.attack_skills:
                                frame:
                                    xysize (147, 25)
                                    button:
                                        xysize (147, 25)
                                        background Null()
                                        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(.10)), 5, 5)
                                        action NullAction()
                                        tooltip ["be", entry]
                                        text "[entry.name]" idle_color ivory align .5, .5 hover_color crimson size min(15, int(250 / max(1, len(entry.name))))

                    vbox:
                        xysize (160, 210)
                        xanchor 5
                        label (u"Spells:") text_size 20 text_color ivory text_bold True xalign .5 text_outlines [(3, "#3a3a3a", 0, 0), (2, "#104E8B", 0, 0), (1, "#3a3a3a", 0, 0)]
                        viewport:
                            xysize (160, 165)
                            scrollbars "vertical"
                            draggable True
                            mousewheel True
                            has vbox spacing 1
                            for entry in char.magic_skills:
                                frame:
                                    xysize (147, 25)
                                    button:
                                        xysize (147, 25)
                                        background Null()
                                        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(.10)), 5, 5)
                                        action NullAction()
                                        tooltip ["be", entry]
                                        text "[entry.name]" idle_color ivory align .5, .5 hover_color crimson size min(15, int(250 / max(1, len(entry.name))))

    use top_stripe(True)

screen race_and_elements(align=(.5, .99), char=None):
    hbox:
        align align
        spacing 20
        # Race:
        frame:
            xysize (100, 100)
            $ trait = char.race
            background Frame(Transform("content/gfx/frame/frame_it1.png", alpha=.6, size=(100, 100)), 10, 10)
            $ img = ProportionalScale(trait.icon, 95, 95)
            button:
                align (.5, .5)
                xysize (95, 95)
                background img
                action Show("show_trait_info", trait=trait.id, place="race_trait")
                hover_background im.MatrixColor(img, im.matrix.brightness(.10))
                tooltip "Race:\n   {}".format(char.full_race)

        # Elements icon:
        $ els = [Transform(e.icon, size=(90, 90)) for e in char.elements]
        $ els_a = [Transform(im.MatrixColor(e.icon, im.matrix.brightness(.10)), size=(90, 90)) for e in char.elements]
        frame:
            xysize (100, 100)
            background Frame(Transform("content/gfx/frame/frame_it1.png", alpha=.6, size=(100, 100)), 10, 10)
            add ProportionalScale("content/gfx/interface/images/elements/hover.png", 98, 98) align (.5, .5)
            $ x = 0
            $ els = [Transform(i, crop=(90/len(els)*els.index(i), 0, 90/len(els), 90), subpixel=True, xpos=(x + 90/len(els)*els.index(i))) for i in els]
            $ els_a = [Transform(i, crop=(90/len(els_a)*els_a.index(i), 0, 90/len(els_a), 90), subpixel=True, xpos=(x + 90/len(els_a)*els_a.index(i))) for i in els_a]
            $ f = Fixed(*els, xysize=(90, 90))
            $ f_a = Fixed(*els_a, xysize=(90, 90))
            if len(char.elements) > 1:
                $ ele = ""
                for e in char.elements:
                    $ ele += e.id + ", "
                $ ele = ele[:-2]
            else:
                $ ele = char.elements[0].id
            button:
                xysize 90, 90
                align .5, .5 offset -1, -1
                action Show("show_trait_info", trait=char, elemental_mode=True, place="ele_trait")
                background f
                hover_background f_a
                tooltip "Elements:\n   {}".format(ele)

screen show_trait_info(trait=None, place="girl_trait", elemental_mode=False):
    if place == "girl_trait":
        if trait != "Manly":
            $ al = (.69, .4)
        else:
            $ al = (.69, .2)
    elif place == "mc_trait":
        $ al = (.86, .45)
    elif place == "main_trait":
        $ al = (.1, .2)
    elif place == "ele_trait":
        $ al = (.35, .9)
    elif place == "race_trait":
        $ al = (.2, 1.0)
    if not(elemental_mode):
        $ trait_info = traits[trait]
        fixed:
            align al
            xysize 190, 450
            frame:
                background Frame("content/gfx/frame/p_frame52.png", 10, 10)
                xminimum 190
                padding 10, 5
                has vbox style_prefix "proper_stats" spacing 1 
                 
                if any([trait_info.min, trait_info.max, trait_info.mod_stats, trait_info.effects,
                        trait_info.mod_skills, trait_info.mod_ap, hasattr(trait_info, "evasion_bonus")]):
                    if trait_info.max:
                        label (u"Max:") text_size 20 text_color goldenrod text_bold True xalign .45
                        for stat, value in trait_info.max.iteritems():
                            frame:
                                xysize 170, 20
                                if value < 0:
                                    text stat.title() size 15 color red align .0, .5 outlines [(1, "#000000", 0, 0)]
                                    label str(value) text_size 15 text_color red align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                                else:
                                    text stat.title() size 15 color lime align .0, .5 outlines [(1, "#000000", 0, 0)]
                                    label "+" + str(value) text_size 15 text_color lime align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                    if trait_info.min:
                        label (u"Min:") text_size 20 text_color goldenrod text_bold True xalign .45
                        for stat, value in trait_info.min.iteritems():
                            frame:
                                xysize 170, 20
                                if value < 0:
                                    text stat.title() size 15 color red align .0, .5 outlines [(1, "#000000", 0, 0)]
                                    label str(value) text_size 15 text_color red align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                                else:
                                    text stat.title() size 15 color lime align .0, .5 outlines [(1, "#000000", 0, 0)]
                                    label "+" + str(value) text_size 15 text_color lime align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                    if trait_info.mod_stats:
                        label (u"Bonus:") text_size 20 text_color goldenrod text_bold True xalign .45
                        for i in trait_info.mod_stats:
                            frame:
                                xysize 170, 20
                                if str(i) not in ["disposition", "upkeep"]:
                                    if (trait_info.mod_stats[i])[0] < 0:
                                        text (str(i).title() + ": " + str((trait_info.mod_stats[i])[0]) + " every " + str((trait_info.mod_stats[i])[1]) + " lvl") align .5, .5 size 15 color red text_align .5 outlines [(1, "#000000", 0, 0)]
                                    else:
                                        text (str(i).title() + ": +" + str((trait_info.mod_stats[i])[0]) + " every " + str((trait_info.mod_stats[i])[1]) + " lvl") align .5, .5 size 15 color lime text_align .5 outlines [(1, "#000000", 0, 0)]
                                else:
                                    if str(i) == "disposition":
                                        if (trait_info.mod_stats[i])[0] < 0:
                                            text (str(i).title() + ": " + str((trait_info.mod_stats[i])[0])) align .5, .5 size 15 color red text_align .5 outlines [(1, "#000000", 0, 0)]
                                        else:
                                            text (str(i).title() + ": +" + str((trait_info.mod_stats[i])[0])) align .5, .5 size 15 color lime text_align .5 outlines [(1, "#000000", 0, 0)]
                                    else:
                                        if (trait_info.mod_stats[i])[0] < 0:
                                            text (str(i).title() + ": " + str((trait_info.mod_stats[i])[0])) align .5, .5 size 15 color lime text_align .5 outlines [(1, "#000000", 0, 0)]
                                        else:
                                            text (str(i).title() + ": +" + str((trait_info.mod_stats[i])[0])) align .5, .5 size 15 color red text_align .5 outlines [(1, "#000000", 0, 0)]
                    if trait_info.effects:
                        label (u"Effects:") text_size 20 text_color goldenrod text_bold True xalign .45
                        for i in trait_info.effects:
                            frame:
                                xysize 170, 20
                                text (str(i).title()) size 15 color yellow align .5, .5 text_align .5 outlines [(1, "#000000", 0, 0)]

                    if trait_info.mod_skills:
                        label (u"Skills:") text_size 20 text_color goldenrod text_bold True xalign .45
                        for skill, data in trait_info.mod_skills.iteritems():
                            frame:
                                xysize 170, 20
                                text str(skill).title() size 15 color yellowgreen align .0, .5 outlines [(1, "#000000", 0, 0)]

                                $ img_path = "content/gfx/interface/icons/skills_icons/"
                                default PS = ProportionalScale
                                button:
                                    style "default"
                                    xysize 20, 18
                                    action NullAction()
                                    align .99, .5
                                    tooltip "Icon represents skills changes. Green means bonus, red means penalty. Left one is action counter, right one is training counter, top one is resulting value."
                                    if data[0] > 0:
                                        add PS(img_path + "left_green.png", 20, 20)
                                    elif data[0] < 0:
                                        add PS(img_path + "left_red.png", 20, 20)
                                    if data[1] > 0:
                                        add PS(img_path + "right_green.png", 20, 20)
                                    elif data[1] < 0:
                                        add PS(img_path + "right_red.png", 20, 20)
                                    if data[2] > 0:
                                        add PS(img_path + "top_green.png", 20, 20)
                                    elif data[2] < 0:
                                        add PS(img_path + "top_red.png", 20, 20)
                    if trait_info.mod_ap or hasattr(trait_info, "evasion_bonus") or hasattr(trait_info, "delivery_multiplier"):
                        label (u"Other:") text_size 20 text_color goldenrod text_bold True xalign .45
                        if trait_info.mod_ap:
                            frame:
                                xysize 170, 20
                                $ output = "AP"
                                if trait_info.mod_ap > 0:
                                    $ output += " +" + str(trait_info.mod_ap)
                                else:
                                    $ output += str(trait_info.mod_ap)
                                text (output) align .5, .5 size 15 color yellowgreen text_align .5 outlines [(1, "#000000", 0, 0)]

                        if hasattr(trait_info, "evasion_bonus"):
                            frame:
                                xysize 170, 20
                                if trait_info.evasion_bonus[1] < 0:
                                    text ("Evasion -") size 15 color yellowgreen align .5, .5 text_align .5 outlines [(1, "#000000", 0, 0)]
                                elif trait_info.evasion_bonus[1] > 0:
                                    text ("Evasion +") size 15 color yellowgreen align .5, .5 text_align .5 outlines [(1, "#000000", 0, 0)]
                        if hasattr(trait_info, "delivery_multiplier"):
                            for i in trait_info.delivery_multiplier:
                                frame:
                                    xysize 170, 20
                                    $ output = str(i).title() + " damage "
                                    if trait_info.delivery_multiplier.get(str(i)) > 0:
                                        $ output += "+"
                                    else:
                                        $ output += "-"
                                    text (output) align .5, .5 size 15 color yellowgreen text_align .5 outlines [(1, "#000000", 0, 0)]
                else:
                    label ("-no direct effects-") text_size 15 text_color goldenrod text_bold True xalign .45 text_outlines [(1, "#000000", 0, 0)]

            imagebutton:
                align .99, .01
                xysize 22, 22
                idle ProportionalScale("content/gfx/interface/buttons/close4.png", 22, 22)
                hover ProportionalScale("content/gfx/interface/buttons/close4_h.png", 22, 22)
                action Hide("show_trait_info")

    else:
        $ traits = calculate_elementals(trait)
        fixed:
            align al
            xysize 450, 190
            frame:
                background Frame("content/gfx/frame/p_frame52.png", 10, 10)
                padding 10, 5
                has vbox style_prefix "proper_stats" spacing 1
                hbox:
                    frame:
                        xysize 80, 20
                        text "element" size 15 color goldenrod align .0, .5
                    frame:
                        xysize 60, 20
                        text "damage" size 15 color goldenrod align .5, .5
                    frame:
                        xysize 60, 20
                        text "defense" size 15 color goldenrod align .5, .5
                hbox:
                    vbox:
                        for element in traits[2]:
                            frame:
                                xysize 80, 20
                                text element size 15 color goldenrod align .0, .5
                    vbox:
                        for element in traits[2]:
                            if element in traits[0].keys():
                                frame:
                                    xysize 60, 20
                                    if traits[0][element] < 0:
                                        label str(traits[0][element])+" %" text_size 15 text_color red align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                                    else:
                                        label str(traits[0][element])+" %" text_size 15 text_color lime align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                            else:
                                frame:
                                    xysize 60, 20
                                    label "0 %" text_size 15 text_color lime align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                    vbox:
                        for element in traits[2]:
                            if element in traits[1].keys():
                                if traits[1][element] != "RES":
                                    $ temp = " %"
                                else:
                                    $ temp = ""
                                frame:
                                    xysize 60, 20
                                    if traits[1][element] < 0:
                                        label str(traits[1][element])+ temp text_size 15 text_color red align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                                    else:
                                        label str(traits[1][element])+ temp text_size 15 text_color lime align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]
                            else:
                                frame:
                                    xysize 60, 20
                                    label "0 %" text_size 15 text_color lime align 1.0, .5 text_outlines [(1, "#000000", 0, 0)]

                if not(traits[0]) and not(traits[1]):
                    label ("-elements overlapped each other-") text_size 14 text_color goldenrod text_bold True xalign .45
            imagebutton:
                align .465, .01
                xysize 22, 22
                idle ProportionalScale("content/gfx/interface/buttons/close4.png", 22, 22)
                hover ProportionalScale("content/gfx/interface/buttons/close4_h.png", 22, 22)
                action Hide("show_trait_info")

screen char_control():
    modal True
    zorder 1

    default cb_checked = im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)
    default cd_unchecked = im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)
    default cb_some_checked = im.Scale('content/gfx/interface/icons/checkbox_some_checked.png', 25, 25)

    frame:
        style_group "content"
        at slide(so1=(600, 0), t1=.7, eo2=(1300, 0), t2=.7)
        background Frame("content/gfx/frame/p_frame52.png", 10, 10)
        xpos 936
        yalign .95
        xysize(343, 675)

        # Tooltip Related:
        frame:
            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
            align (.5, .0)
            padding 40, 10
            text "Adjust your workers behavior here." align .5, .5 color ivory

        # Tips/Wagemod
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.7), 10, 10)
            align .5, .12
            padding 10, 10
            xysize 225, 120
            # Tips:
            button:
                style_group "basic"
                xysize 150, 33
                align .5, .05
                action ToggleDict(char.autocontrol, "Tips")
                tooltip "Does {} keep her tips?".format(char.nickname)
                text "Tips:" align .0, .5
                if isinstance(char.autocontrol["Tips"], list):
                    add cb_some_checked align 1.0, .5
                elif char.autocontrol['Tips']:
                    add cb_checked align 1.0, .5
                else:
                    add cd_unchecked align 1.0, .5
            # Wagemod, basically it allows you to pay more/less to your workers,
            # effecting disposition.
            hbox:
                align (.5, .5)
                imagebutton:
                    yalign .5

                    idle ('content/gfx/interface/buttons/prev.png')
                    hover (im.MatrixColor('content/gfx/interface/buttons/prev.png', im.matrix.brightness(.15)))
                    action SetField(char, "wagemod", max(0, char.wagemod-1))
                null width 5
                bar:
                    align .5, 1.0
                    value FieldValue(char, 'wagemod', 200, max_is_zero=False, style='scrollbar', offset=0, step=1)
                    xmaximum 150
                    thumb 'content/gfx/interface/icons/move15.png'
                    tooltip "What percentage of a fair wage are you willing to pay?"
                null width 5
                imagebutton:
                    yalign .5
                    idle ('content/gfx/interface/buttons/next.png')
                    hover (im.MatrixColor('content/gfx/interface/buttons/next.png', im.matrix.brightness(.15)))
                    action SetField(char, "wagemod", min(200, char.wagemod+1))
            fixed:
                align .5, 1.0
                xysize 200, 30
                hbox:
                    align .5, .0
                    vbox:
                        xmaximum 130
                        xfill True
                        text (u"Wage percentage:") outlines [(1, "#424242", 0, 0)] color ivory
                    vbox:
                        text "[char.wagemod]%" outlines [(1, "#424242", 0, 0)] color ivory

        # BE Row, Job controls + Auto-Buy/Equip
        vbox:
            style_group "basic"
            align (.55, .5)
            if isinstance(char, PytGroup):
                if char not in pytfall.ra:
                    button:
                        xysize (200, 32)
                        style_group "basic"
                        action Return(["dropdown", "workplace", char])
                        tooltip "Choose a location for %s to work at" % char.nickname
                        if len(str(char.location)) > 18:
                            text "[char.location]" size 15
                        elif len(str(char.location)) > 10:
                            text "[char.location]" size 18
                        else:
                            text "Work: [char.location]" size 18
                    button:
                        xysize (200, 32)
                        style_group "basic"
                        action Return(["dropdown", "action", char])
                        tooltip "Choose a task for %s to do" % char.nickname
                        if len(str(char.action)) > 18:
                            text "[char.action]" size 15
                        elif len(str(char.action)) > 12:
                            text "[char.action]" size 18
                        else:
                            text "Action: [char.action]" size 18
                else:
                    text "{size=15}Location: Unknown"
                    text "{size=15}Action: Hiding"

            null height 30
            button:
                action ToggleField(char, "front_row")
                xysize (200, 32)
                text "Front Row" align (.0, .5)
                if char.front_row:
                    tooltip "{} fights in the front row!".format(char.name)
                else:
                    tooltip "{} fights in the back row!".format(char.name)
                if isinstance(char.front_row, list):
                    add cb_some_checked align (1.0, .5)
                elif char.front_row:
                    add cb_checked align (1.0, .5)
                elif not char.front_row:
                    add cd_unchecked align (1.0, .5)

            button:
                action ToggleDict(char.autocontrol, "Rest")
                xysize (200, 32)
                text "Auto Rest" align (.0, .5)
                tooltip "Automatically rest when no longer capable of working!"
                if isinstance(char.autocontrol['Rest'], list):
                    add cb_some_checked align (1.0, .5)
                elif char.autocontrol['Rest']:
                    add cb_checked align (1.0, .5)
                elif not char.autocontrol['Rest']:
                    add cd_unchecked align (1.0, .5)

            # Autobuy:
            button:
                xysize (200, 32)
                sensitive char.status == "slave"
                action ToggleField(char, "autobuy")
                tooltip "Give {} permission to go shopping for items if she has enough money.".format(char.nickname)
                text "Auto Buy" align (.0, .5)
                if isinstance(char.autobuy, list):
                    add cb_some_checked align (1.0, .5)
                elif char.autobuy:
                    add cb_checked align (1.0, .5)
                else:
                    add cd_unchecked align (1.0, .5)

            # Autoequip:
            use aeq_button(char)

            # ------------------------------------------------------------------------------------------------------------------------------------->>>
            # TODO lt: If we ever restore this, char actions are not Jobs!
            # Disabled until Beta release
            # if char.action in ["Server", "SIW"]:
                # null height 10
                # hbox:
                    # spacing 20
                    # if char.autocontrol['SlaveDriver']:
                        # textbutton "{color=[red]}Slave Driver":
                            # yalign .5
                            # action Return(['girl_cntr', 'slavedriver'])
                            # minimum(150, 20)
                            # maximum(150, 20)
                            # xfill true
                        # add cb_checked yalign .5
                    # elif not char.autocontrol['SlaveDriver']:
                        # textbutton "Slave Driver":
                            # yalign .5
                            # action Return(['girl_cntr', 'slavedriver'])
                            # minimum(150, 20)
                            # maximum(150, 20)
                            # xfill true
                        # add cd_unchecked yalign .5

            null height 30

            # if char.action == "Whore":
                # for key in char.autocontrol['Acts']:
                    # null height 10
                    # hbox:
                        # spacing 20
                        # textbutton [key.capitalize()]:
                            # yalign .5
                            # action Return(['girl_cntr', 'set_act', key])
                            # minimum(150, 20)
                        # if char.autocontrol['Acts'][key]:
                            # add cb_checked yalign .5
                        # elif not char.autocontrol['Acts'][key]:
                            # add cd_unchecked yalign .5

            # if char.action == "Server":
            #     for key in char.autocontrol['S_Tasks']:
            #         $ devlog.warn("key:"+key)
            #         button:
            #             action ToggleDict(char.autocontrol['S_Tasks'], key)
            #             xysize (200, 30)
            #             text (key.capitalize()) align (.0, .5)
            #             if isinstance(char.autocontrol['S_Tasks'][key], list):
            #                 add cb_some_checked align (1.0, .5)
            #             elif char.autocontrol['S_Tasks'][key]:
            #                 add cb_checked align (1.0, .5)
            #             elif not char.autocontrol['S_Tasks'][key]:
            #                 add cd_unchecked align (1.0, .5)

        button:
            style_group "basic"
            action Hide("char_control")
            minimum(50, 30)
            align (.5, .95)
            text  "OK"

    key "mousedown_3" action Hide("char_control")

screen aeq_button(char):
    style_prefix "basic"

    default cb_checked = im.Scale('content/gfx/interface/icons/checkbox_checked.png', 25, 25)
    default cd_unchecked = im.Scale('content/gfx/interface/icons/checkbox_unchecked.png', 25, 25)
    default cb_some_checked = im.Scale('content/gfx/interface/icons/checkbox_some_checked.png', 25, 25)

    button:
        xysize (200, 32)
        sensitive char.status == "slave" or char.disposition > 850
        action ToggleField(char, "autoequip")
        tooltip "Try to equip items favorable for the job automatically (results may vary)."
        text "Auto Equip" align (.0, .5)
        if isinstance(char.autoequip, list):
            add cb_some_checked align (1.0, .5)
        elif char.autoequip:
            add cb_checked align (1.0, .5)
        else:
            add cd_unchecked align (1.0, .5)

screen confirm_girl_sale():
    modal True
    zorder 1

    frame:
        align(.5, .5)
        minimum(300, 200)
        maximum(300, 200)
        xfill True
        yfill True

        if char.status == "slave":
            text("{size=-5}Are you sure you want to sell [char.name] for %d Gold?"%(int(char.fin.get_price()*.8))) align(.5, .1)

            hbox:
                align(.5, .85)
                spacing 40
                textbutton "No":
                    action Hide("confirm_girl_sale")
                textbutton "Yes":
                    action Return(['control', 'sell'])

        else:
            text("{size=-5}Are you sure you want to fire the %s?"%char.name) align(.5, .1)

            hbox:
                align(.5, .85)
                spacing 40
                textbutton "No":
                    action Hide("confirm_girl_sale")
                textbutton "Yes":
                    action Return(['control', 'fire'])

    key "K_RETURN" action Return(['control', 'fire'])
    key "K_ESCAPE" action Hide("confirm_girl_sale")

screen finances(obj, mode="logical"):
    modal True
    zorder 1

    key "mousedown_3" action Hide("finances")

    default fin_mode = mode

    add Transform("content/gfx/images/bg_gradient2.png", alpha=.3)
    frame:
        at slide(so1=(0, 700), t1=.7, so2=(0, 0), t2=.3, eo2=(0, -config.screen_height))
        background Frame(Transform("content/gfx/frame/FrameGP.png", alpha=.9), 10, 10)
        style_prefix "proper_stats"
        xysize 1000, 600
        padding 20, 20
        align .5, .5

        $ days, all_income_data, all_expense_data = obj.fin.get_data_for_fin_screen(fin_mode)

        # Days:
        default fin_day = days[-1] if days else None
        # Special check, took some time to track down:
        # Problem here is that we can CTD when switching from Private to Performance...
        # Kind of a hack but it's difficult to do this differently without recoding the screen.
        if fin_day in days:
            pass
        elif days:
            $ fin_day = days[-1]
        else:
            $ fin_day = None

        if fin_day not in all_income_data:
            text "There are no Finances to display for {}!".format(obj.name) align .5, .5
        else:
            hbox:
                style_prefix "basic"
                for d in days:
                    if d == store.day:
                        $ temp = "Today"
                    elif isinstance(d, int):
                        $ temp = "Day " + str(d)
                    else:
                        $ temp = d # All variant...
                    textbutton temp action SetScreenVariable("fin_day", d)

            vbox:
                ypos 40
                text "Income:" size 40 color goldenrod
                viewport:
                    xysize (398, 350)
                    draggable True
                    mousewheel True
                    add Transform(Solid(grey), alpha=.3)
                    vbox:
                        ypos 2
                        for reason, value in all_income_data[fin_day].iteritems():
                            frame:
                                xoffset 4
                                xysize (390, 27)
                                xpadding 7
                                text reason.capitalize() color "#79CDCD"
                                text str(value) xalign 1.0 style_suffix "value_text" color goldenrod

                        frame:
                            xoffset 4
                            xysize (390, 27)
                            xpadding 7
                            text "Total" color "#79CDCD"
                            $ total_income = sum(all_income_data[fin_day].values())
                            text str(total_income) xalign 1.0 style_suffix "value_text" color goldenrod

            vbox:
                ypos 40 xalign 1.0
                text "Expenses:" size 40 color goldenrod
                viewport:
                    xysize (398, 350)
                    draggable True
                    mousewheel True
                    add Transform(Solid(grey), alpha=.3)
                    vbox:
                        ypos 2
                        for reason, value in all_expense_data[fin_day].iteritems():
                            frame:
                                xoffset 4
                                xysize (390, 27)
                                xpadding 7
                                text reason.capitalize() color "#79CDCD"
                                text str(value) xalign 1.0 style_suffix "value_text" color goldenrod

                        frame:
                            xoffset 4
                            xysize (390, 27)
                            xpadding 7
                            text "Total" color "#79CDCD"
                            $ total_expenses = sum(all_expense_data[fin_day].values())
                            text str(total_expenses) xalign 1.0 style_suffix "value_text" color goldenrod

            frame:
                align .5, .9
                xysize (400, 50)
                xpadding 7
                background Frame("content/gfx/frame/rank_frame.png", 3, 3)
                text "Total" size 35 color goldenrod
                $ total = total_income - total_expenses
                $ temp = red if total < 0 else lawngreen
                text str(total) xalign 1.0 style_suffix "value_text" color temp size 35

        hbox:
            style_prefix "basic"
            align .5, 1.0
            button:
                minimum (100, 30)
                action Hide('finances')
                text "OK"
            if isinstance(obj, Char):
                button:
                    minimum (100, 30)
                    if fin_mode == "logical":
                        sensitive obj.allowed_to_view_personal_finances()
                        action SetScreenVariable('fin_mode', "main")
                        text "Personal"
                    elif fin_mode == "main":
                        action SetScreenVariable('fin_mode', "logical")
                        text "Performance"

    key "K_RETURN" action Hide('finances')
    key "K_ESCAPE" action Hide('finances')
    key "mouseup_3" action Hide('finances')
