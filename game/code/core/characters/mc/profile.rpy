label hero_profile:
    scene bg h_profile

    $ global_flags.set_flag("keep_playing_music")

    # $ pytfall.world_quests.run_quests("auto") Goes against squelching policy?
    $ pytfall.world_events.run_events("auto")
    $ renpy.retain_after_load()

    show screen hero_profile
    with dissolve

    $ hero.inventory.set_page_size(18)

    while 1:
        $ result = ui.interact()

        # To kill input error during team renaming:
        if not result:
            pass
        elif result[0] == "rename":
            if result[1] == "name":
                $ n = renpy.call_screen("pyt_input", hero.name, "Enter Name", 20)
                if len(n):
                    $ hero.name = n
                    $ hero.nickname = hero.name
                    $ hero.fullname = hero.name
                    if hero.name.lower() == "darktl": # LoL! :D
                        $ hero.gold += 888888888
            if result[1] == "nick":
                $ n = renpy.call_screen("pyt_input", hero.name, "Enter Name", 20)
                if len(n):
                    $ hero.nickname = renpy.call_screen("pyt_input", hero.name, "Enter Nick Name", 20)
            if result[1] == "full":
                $ n = renpy.call_screen("pyt_input", hero.name, "Enter Full Name", 20)
                if len(n):
                    $ hero.fullname = n
        elif result[0] == "item":
            if result[1] == "transfer":
                hide screen hero_profile
                $ items_transfer([hero, hero.home])
                show screen hero_profile
        elif result[0] == 'control':
            if result[1] == 'return':
                $ pytfall.hp.show_item_info = False
                $ pytfall.hp.item = False
                hide screen hero_profile

                # Reset filters (prevents crap from happening in shops):
                $ hero.inventory.male_filter = False
                $ hero.inventory.apply_filter('all')

                jump expression pytfall.hp.came_from
        elif result[0] == "dropdown":
            if result[1] == "workplace":
                $ renpy.show_screen("set_workplace_dropdown", hero, pos=renpy.get_mouse_pos())
            elif result[1] == "home":
                $ renpy.show_screen("set_home_dropdown", hero, pos=renpy.get_mouse_pos())
            elif result[1] == "action":
                $ renpy.show_screen("set_action_dropdown", hero, pos=renpy.get_mouse_pos())
        elif result[0] == 'hero':
            if result[1] == 'equip':
                $ came_to_equip_from = "hero_profile"
                $ eqtarget = hero
                jump char_equip
        elif result[0] == "remove_from_team":
            $ hero.team.remove(result[1])
        elif result[0] == "rename_team":
            if result[1] == "set_name":
                $ hero.team.name = renpy.call_screen("pyt_input", hero.team.name, "Enter Team Name", 20, (350, 200))

# Screens:
screen hero_profile():
    on "hide":
        action Hide("show_trait_info")

    default lframe_display = "status"
    default rframe_display = "skills"
    default base_ss = hero.stats.get_base_ss()

    key "mousedown_3" action Return(['control', 'return'])

    # HERO SPRITE ====================================>
    add Transform(hero.show("profile", resize=(550, 550)), alpha=.97) align .65, .9

    # BASE FRAME 2 "bottom layer" and portrait ====================================>
    add "content/gfx/frame/h_profile.png"
    add hero.show("everyday", resize=(100, 100)) pos (64, 8) # portrait should be between "Base Frame 2" and "Base Frame 1" :Gismo

    # BATTLE STATS ====================================>
    fixed:
        xysize (270, 270)
        pos (300, 413)
        add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                              (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 112, 126, 148, darkgreen), alpha=.4) align (.5, .5)
        add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                              (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 65, 126, 148, green), alpha=.3) align (.5, .5)
        add Transform(child=RadarChart((float(hero.attack)/hero.get_max("attack")), (float(hero.defence)/hero.get_max("defence")), (float(hero.agility)/hero.get_max("agility")),
                                                              (float(hero.luck)/hero.get_max("luck")), (float(hero.magic)/hero.get_max("magic")), 33, 126, 148, lightgreen), alpha=.2) align (.5, .5)
        add ProportionalScale("content/gfx/interface/images/pentagon1.png", 250, 250) align (.01, .5)

    fixed:
        frame:
            pos (375, 402)
            background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=.9), 10, 10)
            xysize 100, 30
            hbox:
                align .5, .5
                add pscale("content/gfx/interface/images/atk.png", 24, 24)
                text("{size=-5}[hero.attack]|%d"%(hero.get_max("attack"))):
                    yalign .5
                    font "fonts/Rubius.ttf"
                    color red
                    outlines [(1, "#0d0d0d", 0, 0)]
            if "attack" in base_ss:
                button:
                    xysize 20, 20
                    offset -10, -16
                    background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                    action NullAction()
                    tooltip "This is a Class Stat!"
        frame:
            pos (223, 483)
            background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=.9), 10, 10)
            xysize 100, 30
            hbox:
                align .5, .5
                add pscale("content/gfx/interface/images/def.png", 24, 24)
                text("{size=-5}[hero.defence]|%d"%(hero.get_max("defence"))):
                    yalign .5
                    color "#dc762c"
                    font "fonts/Rubius.ttf"
                    outlines [(1, "#0d0d0d", 0, 0)]
            if "defence" in base_ss:
                button:
                    xysize 20, 20
                    offset -10, -16
                    background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                    action NullAction()
                    tooltip "This is a Class Stat!"
        frame:
            pos (255, 643)
            background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=.9), 10, 10)
            xysize 100, 30
            hbox:
                align .5, .5
                add pscale("content/gfx/interface/images/agi.png", 24, 24)
                text("{size=-5}[hero.agility]|%d"%(hero.get_max("agility"))):
                    yalign .5
                    color "#1E90FF"
                    font "fonts/Rubius.ttf"
                    outlines [(1, "#0d0d0d", 0, 0)]
            if "agility" in base_ss:
                button:
                    xysize 20, 20
                    offset -10, -16
                    background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                    action NullAction()
                    tooltip "This is a Class Stat!"
        frame:
            pos (495, 643)
            background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=.9), 10, 10)
            xysize 100, 30
            hbox:
                align .5, .5
                add pscale("content/gfx/interface/images/luck.png", 24, 24)
                text("{size=-5}[hero.luck]|%d" % (hero.get_max("luck"))):
                    yalign .5
                    color "#00FA9A"
                    font "fonts/Rubius.ttf"
                    outlines [(1, "#0d0d0d", 0, 0)]
            if "luck" in base_ss:
                button:
                    xysize 20, 20
                    offset -10, -16
                    background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                    action NullAction()
                    tooltip "This is a Class Stat!"
        frame:
            pos (526, 483)
            background Frame(Transform("content/gfx/frame/stat_box_proper.png", alpha=.9), 10, 10)
            xysize 100, 30
            hbox:
                align .5, .5
                add pscale("content/gfx/interface/images/mag.png", 24, 24)
                text("{size=-5}{color=#8470FF}[hero.magic]|%d" % (hero.get_max("magic"))):
                    yalign .5
                    font "fonts/Rubius.ttf"
                    outlines [(1, "#0d0d0d", 0, 0)]
            if "magic" in base_ss:
                button:
                    xysize 20, 20
                    offset -10, -16
                    background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                    action NullAction()
                    tooltip "This is a Class Stat!"

    # LEFT FRAME (Stats/Friends/Etc) ====================================>
    vbox:
        xsize 217
        pos (8, 110)
        style_prefix "proper_stats"

        # NAME^   LVL   (ok for 1m lvls) ====================================>
        textbutton "[hero.name]":
            background Null()
            text_style "TisaOTMol"
            text_size 28
            text_outlines [(2, "#424242", 0, 0)]
            xalign .492
            ypos 5
            action Show("char_rename", char=hero)
            tooltip "Click to rename yourself."

        hbox:
            spacing 1
            if (hero.level) < 10:
                pos (89, 11)
            elif (hero.level) < 100:
                pos (86, 11)
            elif (hero.level) < 10000:
                pos (77, 11)
            else:
                pos (73, 11)
            label "{color=#CDAD00}Lvl" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)]
            label "{color=#CDAD00}[hero.level]" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)]
        hbox:
            pos (84, 21)
            label "{color=#CDAD00}Tier " text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)]
            label "{color=#CDAD00}[hero.tier]" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)]


        if lframe_display == "status":
            # STATS ====================================>
            null height 20
            $ stats = ["constitution", "charisma", "intelligence", "fame", "reputation"]
            vbox:
                style_group "proper_stats"
                spacing 1
                xsize 212
                frame:
                    xysize (212, 27)
                    xalign .5
                    text "Health:" xalign .02 color "#CD4F39"
                    if "health" in base_ss:
                        button:
                            xysize 20, 20
                            offset -5, -5
                            background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                            action NullAction()
                            tooltip "This is a Class Stat!"
                    if hero.health <= hero.get_max("health")*.3:
                        text (u"{color=[red]}%s/%s"%(hero.health, hero.get_max("health"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                    else:
                        text (u"{color=#F5F5DC}%s/%s"%(hero.health, hero.get_max("health"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                frame:
                    xysize (212, 27)
                    xalign .5
                    text "MP:" xalign .02 color "#009ACD"
                    if "mp" in base_ss:
                        button:
                            xysize 20, 20
                            offset -5, -5
                            background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                            action NullAction()
                            tooltip "This is a Class Stat!"
                    if hero.mp <= hero.get_max("mp")*.3:
                        text (u"{color=[red]}%s/%s"%(hero.mp, hero.get_max("mp"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                    else:
                        text (u"{color=#F5F5DC}%s/%s"%(hero.mp, hero.get_max("mp"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                frame:
                    xysize (212, 27)
                    xalign .5
                    text "{color=#43CD80}Vitality:" xalign (.02)
                    if "vitality" in base_ss:
                        button:
                            xysize 20, 20
                            offset -5, -5
                            background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                            action NullAction()
                            tooltip "This is a Class Stat!"
                    if hero.vitality <= hero.get_max("vitality")*.3:
                        text (u"{color=[red]}%s/%s"%(hero.vitality, hero.get_max("vitality"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                    else:
                        text (u"{color=#F5F5DC}%s/%s"%(hero.vitality, hero.get_max("vitality"))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4
                for stat in stats:
                    frame:
                        xysize (212, 27)
                        xalign .5
                        text '{}'.format(stat.capitalize()) xalign .02 color "#79CDCD"
                        if stat in base_ss:
                            button:
                                xysize 20, 20
                                offset -5, -5
                                background pscale("content/gfx/interface/icons/stars/legendary.png", 20, 20)
                                action NullAction()
                                tooltip "This is a Class Stat!"
                        text ('%d/%d'%(getattr(hero, stat), hero.get_max(stat))) xalign 1.0 style_suffix "value_text" xoffset -6 yoffset 4

            null height 5

            # LOCATION ====================================>
            # No point in Work here...?
            button:
                style_group "ddlist"
                action Return(["dropdown", "home"])
                tooltip "Choose a place to live at!"
                text "{image=button_circle_green}Home: [hero.home]":
                    if len(str(hero.home)) > 18:
                        size 14
                    else:
                        size 17
            button:
                style_group "ddlist"
                action Return(["dropdown", "workplace"])
                tooltip "Choose a place to work at!"
                text "{image=button_circle_green}Work: [hero.workplace]":
                    if len(str(hero.workplace)) > 18:
                        size 14
                    else:
                        size 17
            button:
                style_group "ddlist"
                action Return(["dropdown", "action"])
                tooltip "Pick a task!"
                text "{image=button_circle_green}Action: [hero.action]":
                    if len(str(hero.action)) > 18:
                        size 14
                    else:
                        size 17
        elif lframe_display == "skills":
            null height 26
            viewport:
                xysize (230, 500)
                mousewheel True
                vbox:
                    xpos 10
                    spacing 1
                    for skill in hero.stats.skills:
                        $ skill_val = int(hero.get_skill(skill))
                        $ skill_limit = int(hero.get_max_skill(skill))
                        # We don't care about the skill if it's less than 10% of limit:
                        if skill in base_ss or skill_val/float(skill_limit) > .1:
                            hbox:
                                xsize 200
                                text "{}:".format(skill.capitalize()) style_suffix "value_text" color gold xalign .0 size 18
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
                    for skill in hero.stats.skills:
                        $ skill_val = int(hero.get_skill(skill))
                        $ skill_limit = int(hero.get_max_skill(skill))
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

    # BUTTONS on the "bottom layer" ------------------------------------>
    hbox:
        style_group "pb"
        spacing 1
        pos (1142, 156)
        button:
            action Hide("show_trait_info"), SetScreenVariable("rframe_display", "skills"), With(dissolve)
            text "Skills" style "pb_button_text"
        button:
            action SetScreenVariable("rframe_display", "traits"), With(dissolve)
            text "Traits" style "pb_button_text"

    # RIGHT FRAME ====================================>
    vbox:
        pos (1124, 60)
        xsize 153
        frame:
            xalign .5
            yfill True
            background Frame(Transform("content/gfx/frame/MC_bg3.png", alpha=.6), 10, 10)
            xysize (153, 60)
            text (u"{color=#CDAD00} Day [day]") font "fonts/Rubius.ttf" size 26 outlines [(1, "#3a3a3a", 0, 0)] align (.5, .6)
        null height 2
        frame:
            xalign .5
            xysize 142, 22
            style_prefix "proper_stats"
            text "Gold:" size 16  outlines [(1, "#3a3a3a", 0, 0)] color gold xalign .1
            text "[hero.gold]" size 14 outlines [(1, "#3a3a3a", 0, 0)] style_suffix "value_text" color gold xalign .9 yoffset 2

    # ATTACKS/MAGIC SKILLS ====================================>
    if rframe_display == "skills":
        vbox:
            pos (1125, 205)
            style_group "proper_stats"

            frame:
                background Frame("content/gfx/frame/hp_1.png", 5, 5)
                xysize (160, 192)
                has vbox
                label (u"Attacks:") text_size 20 text_color ivory text_bold True xalign .45 text_outlines [(3, "#3a3a3a", 0, 0), (2, "#8B0000", 0, 0), (1, "#3a3a3a", 0, 0)]
                viewport:
                    xysize (160, 155)
                    scrollbars "vertical"
                    draggable True
                    mousewheel True
                    has vbox spacing 1
                    for entry in list(sorted(hero.attack_skills, key=attrgetter("menu_pos"))):
                        frame:
                            xysize (147, 25)
                            button:
                                xysize (147, 25)
                                background Null()
                                hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(.10)), 5, 5)
                                action NullAction()
                                tooltip ["be", entry]
                                text "[entry.name]" idle_color ivory align .5, .5 hover_color crimson size min(15, int(250 / max(1, len(entry.name))))

            frame:
                background Frame("content/gfx/frame/hp_1.png", 5, 5)
                xysize (160, 192)
                has vbox
                label (u"Spells:") text_size 20 text_color ivory text_bold True xalign .45 text_outlines [(3, "#3a3a3a", 0, 0), (2, "#104E8B", 0, 0), (1, "#3a3a3a", 0, 0)]
                viewport:
                    xysize (160, 155)
                    scrollbars "vertical"
                    draggable True
                    mousewheel True
                    has vbox spacing 1
                    for entry in list(sorted(hero.magic_skills, key=attrgetter("menu_pos"))):
                        frame:
                            xysize (147, 25)
                            button:
                                xysize (147, 25)
                                background Null()
                                hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(.10)), 5, 5)
                                action NullAction()
                                tooltip ["be", entry]
                                text "[entry.name]" idle_color ivory align .5, .5 hover_color crimson size min(15, int(250 / max(1, len(entry.name))))


    # TRAITS ====================================>
    elif rframe_display == "traits":
        frame:
            pos (1125, 205)
            background Frame("content/gfx/frame/hp_1long.png", 5, 5)
            xysize (160, 389)
            style_group "proper_stats"
            has vbox
            label (u"Traits:") text_size 20 text_color ivory text_bold True xalign .45
            viewport:
                xysize (160, 150)
                draggable True
                mousewheel True
                has vbox spacing 1
                # for i in range(200):
                    # add Solid("#F00", xysize=(100, 20))
                for trait in list(t for t in hero.traits if not any([t.personality, t.race, t.elemental])):
                    if not trait.hidden:
                        frame:
                            xsize 147
                            button:
                                background Null()
                                xsize 147
                                action Show("show_trait_info", trait=trait.id, place="mc_trait")
                                text trait.id idle_color ivory align .5, .5 hover_color crimson text_align .5 size min(15, int(250 / max(1, len(trait.id))))
                                tooltip "%s"%trait.desc
                                hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(.10)), 5, 5)

            null height 10

            label (u"Effects:") text_size 20 text_color ivory text_bold True xalign .45
            viewport:
                xysize (160, 150)
                draggable True
                mousewheel True
                has vbox spacing 1
                for effect in hero.effects.itervalues():
                    frame:
                        xysize (147, 25)
                        button:
                            background Null()
                            xysize (147, 25)
                            action NullAction()
                            text "[effect.name]" idle_color ivory align .5, .5 hover_color crimson size min(15, int(250 / max(1, len(trait.id))))
                            tooltip "%s"%effect.desc
                            hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(.10)), 5, 5)

    # BASE FRAME 1 "top layer" ====================================>
    add "content/gfx/frame/h_profile2.png"

    # BUTTONS and UI elements on the "top layer" ====================================>
    hbox:
        style_prefix "pb"
        spacing 2
        pos (472, 9)
        button:
            action SetScreenVariable("lframe_display", "status"), With(dissolve)
            text "Stats" style "pb_button_text"
            tooltip "Inspect your personal statistics and place of residence"
        button:
            action SetScreenVariable("lframe_display", "skills"), With(dissolve)
            text "Skills" style "pb_button_text"
            tooltip "Check the progress of your skills"
        button:
            action Hide("show_trait_info"), Show("hero_team", transition=dissolve)#, With(dissolve)
            text "Team" style "pb_button_text"
            tooltip "Display your team's current composition; Team Name: %s" % hero.team.name
        button:
            action Hide("show_trait_info"), Return(['hero', 'equip'])#, With(dissolve)
            text "Equipment" style "pb_button_text"
            tooltip "Browse and manage your own inventory and equipment"
        button:
            action Hide("show_trait_info"), Show("finances", None, hero, mode="main")#, With(dissolve)
            text "Finance" style "pb_button_text"
            tooltip "View the log of financial information, letting you see your income and expenses"
        button:
            action Hide("show_trait_info"), [Show("mc_friends_list")]
            text "Friends" style "pb_button_text"
            tooltip "Show the list friends and lovers who don't work for {}, allowing you to find them immediately when needed".format(hero.name)
        # Items Transfer to Home Location Inventory:

    # Storage button:
    frame:
        background Frame("content/gfx/frame/settings1.png", 10, 10)
        pos 300, 5
        style_prefix "pb"
        xysize 100, 40
        showif hasattr(hero.home, "inventory"):
            button:
                align .5, .5
                action Return(["item", "transfer"])
                text "Storage" style "pb_button_text"
                tooltip "Open the location storage to leave or take items"

    imagebutton:
        pos (900, 7) # (178, 70)
        idle im.Scale("content/gfx/interface/buttons/close2.png", 35, 35)
        hover im.Scale("content/gfx/interface/buttons/close2_h.png", 35, 35)
        action Hide("show_trait_info"), Return(['control', 'return'])
        tooltip "Return to previous screen!"

    # EXP BAR ====================================>
    fixed:
        pos (259, 697)
        bar:
            value hero.stats.exp + hero.stats.goal_increase - hero.stats.goal
            range hero.stats.goal_increase
            left_bar ("content/gfx/interface/bars/exp_full.png")
            right_bar ("content/gfx/interface/bars/exp_empty.png")
            thumb None
            maximum (324, 18)
        hbox:
            spacing 10
            pos (90, -17)
            xmaximum 160
            xfill True
            add "content/gfx/interface/images/exp_b.png" ypos 2 xalign .8
            text "[hero.exp]/[hero.goal]" style "proper_stats_value_text" bold True outlines [(1, "#181818", 0, 0)] color "#DAA520"

    # Race/Elements
    use race_and_elements(align=(.78, .98), char=hero)

    # AP ====================================>
    frame:
        align .5, .95
        background ProportionalScale("content/gfx/frame/frame_ap2.png", 190, 80)
        label "[hero.AP]":
            pos (130, -2)
            style "content_label"
            text_color ivory
            text_size 22

screen hero_team():
    zorder 1
    modal True

    key "mousedown_3" action Hide("hero_team"), With(dissolve)

    add Transform("content/gfx/images/bg_gradient2.png", alpha=.3)

    # Hero team ====================================>
    frame:
        style_prefix "proper_stats"
        align .54, .4
        background Frame(Transform(im.Twocolor("content/gfx/frame/ink_box.png", white, black), alpha=.7), 5, 5)
        padding 10, 5
        has vbox spacing 10

        hbox:
            spacing 2
            xalign .5
            label "[hero.team.name]" text_color "#CDAD00" text_size 30
            imagebutton:
                idle im.Scale("content/gfx/interface/buttons/edit.png", 24, 30)
                hover im.Scale("content/gfx/interface/buttons/edit_h.png", 24, 30)
                action Return(["rename_team", "set_name"]), With(dissolve)
                tooltip "Rename the team"

        for member in hero.team:
            $ img = member.show("portrait", resize=(120, 120), cache=True)
            hbox:
                spacing 7
                # Portrait/Button:
                fixed:
                    align .5, .5
                    xysize 120, 120
                    imagebutton:
                        padding 1, 1
                        align .5, .5
                        style "basic_choice2_button"
                        idle img
                        hover img
                        selected_idle Transform(img, alpha=1.05)
                        action None

                    python:
                        if member.front_row:
                            img = ProportionalScale("content/gfx/interface/buttons/row_switch.png", 40, 20)
                        else:
                            img = im.Flip(ProportionalScale("content/gfx/interface/buttons/row_switch.png", 40, 20), horizontal=True)

                    imagebutton:
                        align (0, 1.0)
                        idle Transform(img, alpha=.9)
                        hover Transform(img, alpha=1.05)
                        insensitive im.Sepia(img)
                        action If(hasattr(member, "front_row"), true=[ToggleField(member, "front_row")])
                        if member.front_row:
                            tooltip "Toggle between rows in battle, currently character fights from the front row"
                        else:
                            tooltip "Toggle between rows in battle, currently character fights from the back row"

                    if member != hero:
                        imagebutton:
                            align (1.0, 1.0)
                            idle Transform("content/gfx/interface/buttons/Profile.png", alpha=.9)
                            hover Transform("content/gfx/interface/buttons/Profile.png", alpha=1.0)
                            insensitive im.Sepia("content/gfx/interface/buttons/Profile.png")
                            sensitive member in hero.chars
                            action If(member not in pytfall.ra, true=[Hide("hero_profile"), Hide("hero_team"), SetVariable("char", member), SetVariable("char_profile", "hero_profile"), Jump("char_profile")], false=NullAction())
                            tooltip "See character profile"

                # Name/Status:
                frame:
                    xsize 162
                    padding 10, 5
                    background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=.6), 5, 5)
                    has vbox spacing 4 xfill True
                    fixed:
                        xysize 158, 25
                        xalign .5
                        text "{=TisaOTMolxm}[member.name]" xalign .06
                        if not member == hero:
                            imagebutton:
                                xalign .92
                                idle ProportionalScale("content/gfx/interface/buttons/close4.png", 24, 30)
                                hover ProportionalScale("content/gfx/interface/buttons/close4_h.png", 24, 30)
                                action Return(["remove_from_team", member])
                                tooltip "Remove %s from %s"%(member.nickname, hero.team.name)

                    # HP:
                    fixed:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/hp1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value member.health
                            range member.get_max("health")
                            thumb None
                            xysize (150, 20)
                        text "HP" size 14 color "#F5F5DC" bold True xpos 8
                        $ tmb = red if member.health <= member.get_max("health")*.3 else "#F5F5DC"
                        text "[member.health]" size 14 color tmb bold True style_suffix "value_text" xpos 125 yoffset -8

                    # MP:
                    fixed:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/mp1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value member.mp
                            range member.get_max("mp")
                            thumb None
                            xysize (150, 20)
                        text "{color=#F5F5DC}MP" size 14 bold True xpos 8
                        $ tmb = red if member.mp <= member.get_max("mp")*.3 else "#F5F5DC"
                        text "[member.mp]" size 14 color tmb bold True style_suffix "value_text" xpos 125 yoffset -8

                    # VP
                    fixed:
                        ysize 25
                        bar:
                            left_bar ProportionalScale("content/gfx/interface/bars/vitality1.png", 150, 20)
                            right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                            value member.vitality
                            range member.get_max("vitality")
                            thumb None
                            xysize (150, 20)
                        text "{color=#F5F5DC}VP" size 14 bold True xpos 8
                        $ tmb = red if member.vitality <= member.get_max("vitality")*.3 else "#F5F5DC"
                        text "[member.vitality]" size 14 color tmb bold True style_suffix "value_text" xpos 125 yoffset -8

        button:
            style_group "pb"
            xalign .5
            xsize 120
            action Hide("hero_team"), With(dissolve)
            text "Close" style "pb_button_text"
            tooltip "Close team screen"

screen hero_finances():
    modal True
    zorder 1

    key "mousedown_3" action Hide("hero_finances"), With(dissolve)

    add Transform("content/gfx/images/bg_gradient2.png", alpha=.3)
    frame:
        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=.65), 10, 10)
        style_group "content"
        align (.5, .5)
        xysize (1120, 600)
        # side "c r":
            # area (20, 43, 1110, 495)
        viewport id "herofin_vp":
            style_group "stats"
            draggable True
            mousewheel True
            if day > 1:
                $ fin_inc = hero.fin.game_main_income_log[day-1]
                $ fin_exp = hero.fin.game_main_expense_log[day-1]

                if pytfall.hp.finance_filter == 'day':
                    label (u"Fin Report (Yesterday)") xalign .4 ypos 30 text_size 30
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
                                    text "[val]" style_suffix "value_text"

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
                                    text ("[val]") style_suffix "value_text"

                    python:
                        total_income = 0
                        total_expenses = 0
                        for key in fin_inc:
                            total_income += fin_inc[key]
                        for key in fin_exp:
                            total_expenses += fin_exp[key]
                        total = total_income - total_expenses

                    vbox:
                        align (.80, .60)
                        text "----------------------------------------"
                        text ("Revenue: [total]"):
                            size 20
                            xpos 15
                            if total > 0:
                                color lawngreen style_suffix "value_text"
                            else:
                                color red style_suffix "value_text"

                    hbox:
                        style_group "basic"
                        align (.5, .9)
                        textbutton "Show Total" action SetField(pytfall.hp, "finance_filter", "total")

                elif pytfall.hp.finance_filter == 'total':
                    label (u"Fin Report (Game)") xalign .4 ypos 30 text_size 30
                    python:
                        income = dict()
                        for d in hero.fin.game_main_income_log:
                            for key, value in hero.fin.game_main_income_log[d].iteritems():
                                income[key] = income.get(key, 0) + value
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
                                    text ("[val]") style_suffix "value_text"

                    python:
                        expenses = dict()
                        for d in hero.fin.game_main_expense_log:
                            for key, value in hero.fin.game_main_expense_log[d].iteritems():
                                expenses[key] = expenses.get(key, 0) + value
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
                                    text ("[val]") style_suffix "value_text"

                    python:
                        game_total = 0
                        total_income = sum(income.values())
                        total_expenses = sum(expenses.values())
                        game_total = total_income - total_expenses

                    vbox:
                        align (.80, .60)
                        text "----------------------------------------"
                        text ("Revenue: [game_total]"):
                            size 20
                            xpos 15
                            if game_total > 0:
                                color lawngreen style_suffix "value_text"
                            else:
                                color red style_suffix "value_text"

                    hbox:
                        style_group "basic"
                        align (.5, .9)
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
                            text ("[hero.fin.property_tax_debt]\n ") color red style_suffix "value_text"
                        if hero.fin.income_tax_debt:
                            null height 4
                            spacing 4
                            text ("[hero.fin.income_tax_debt]\n ") color crimson style_suffix "value_text"
                        if day != 1:
                            python:
                                days = calendar.days.index(calendar.weekday())
                                taxes = hero.fin.get_total_taxes(days)
                            null height 4
                            spacing 4
                            text ("[taxes]\n ") style_suffix "value_text"

            # vbar value YScrollValue("herofin_vp")
        button:
            style_group "basic"
            action Hide('hero_finances')
            minimum (250, 30)
            align (.5, .96)
            text "OK"

screen mc_friends_list:

    modal True
    key "mousedown_3" action Hide("mc_friends_list")
    frame:
        at slide(so1=(-2000, 0), t1=.7, so2=(0, 0), t2=.3, eo2=(-2000, 0))
        xysize (930, 450)
        pos(210, 115)
        background Frame("content/gfx/frame/p_frame7.png", 5, 5)
        $ temp = sorted(list(hero.friends | hero.lovers), key=attrgetter("name"))
        $ temp = list(i for i in temp if (i not in hero.chars) and i.is_available)
        if temp:
            text "Click on the character to meet her in the city" style "TisaOTMol" size 23 xalign .5
        else:
            text "No unhired friends/lovers" style "TisaOTMol" size 23 xalign .5
        imagebutton:
            align (1.0, .0)
            idle im.Scale("content/gfx/interface/buttons/close2.png", 35, 35)
            hover im.Scale("content/gfx/interface/buttons/close2_h.png", 35, 35)
            action Hide("mc_friends_list")

        vpgrid:
            ypos 40
            cols 5
            draggable True
            mousewheel True
            scrollbars "vertical"
            xysize (930, 390)



            for char in temp:
                frame:
                    background Frame(Transform("content/gfx/frame/ink_box.png", alpha=.6), 5, 5)
                    top_padding 10
                    bottom_padding 3
                    xpadding 5
                    xmargin 0
                    ymargin 0
                    xminimum 180
                    align (.5, .5)
                    has vbox spacing 1 xalign .5
                    button:
                        ypadding 1
                        xpadding 1
                        xmargin 0
                        ymargin 0
                        align (.5, .5)
                        style "basic_choice2_button"
                        add char.show("portrait", resize=(120, 120), cache=True) align (.5, .5)
                        action [Hide("mc_friends_list"), Hide("hero_profile"), With(dissolve), Function(friends_list_gms, char)]

                    text "{=TisaOTMolxm}[char.nickname]" align (.5, 1.0) yoffset 5 xmaximum 190
                    if char in hero.lovers:
                        add ProportionalScale("content/gfx/interface/images/love.png", 35, 35) xalign .5
                    else:
                        add ProportionalScale("content/gfx/interface/images/friendship.png", 35, 35) xalign .5
