# Temp code, should be moved to items funcs:
init:
    style positive_item_eqeffects_change:
        is text
        size 9
        color lawngreen

    style negative_item_eqeffects_chage:
        is positive_item_eqeffects_change
        color "#ff1a1a"

    screen discard_item(eq_sourse, item):
        zorder 10
        modal True

        add Transform("content/gfx/images/bg_gradient2.png", alpha=0.3)
        frame:
            background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.75), 10, 10)
            style_group "dropdown_gm2"
            align .42, .61
            xsize 500
            padding 10, 10
            margin 0, 0
            has vbox spacing 5 xfill True
            text "{=TisaOTM}{size=-3}Discard {color=#ffd700}[item.id]{/color}?" xalign 0.52 color "#ecc88a"
            hbox:
                xalign 0.5
                spacing 10
                textbutton "{size=-1}Yes":
                    xalign 0.5
                    action Function(eq_sourse.inventory.remove, item), Hide("discard_item"), With(dissolve)
                $ amount = eq_sourse.inventory[item]
                textbutton "{size=-1}Discard All":
                    xalign 0.5
                    action SensitiveIf(amount > 1), Function(eq_sourse.inventory.remove, item, amount), Hide("discard_item"), With(dissolve)
                textbutton "{size=-1}No":
                    xalign 0.5
                    action Hide("discard_item"), With(dissolve)

init python:
    def build_str_for_eq(eqtarget, dummy, stat, tempc):
        temp = getattr(dummy, stat) - getattr(eqtarget, stat) if dummy else False
        tempmax = dummy.get_max(stat) - eqtarget.get_max(stat) if dummy else False
        if temp: # Case: Any Change to stat
            # The first is the absolute change, we want it to be colored green if it is positive, and red if it is not.
            tempstr = "{color=[green]}%s{/color}"%getattr(dummy, stat) if temp > 0 else "{color=[red]} %d{/color}"%getattr(dummy, stat)
            # Next is the increase:
            tempstr = tempstr + "{=positive_item_eqeffects_change}(+%d){/=}"%temp if temp > 0 else tempstr + "{=negative_item_eqeffects_chage}(%d){/=}"%temp
        else: # No change at all...
            tempstr = "{color=[tempc]}%s{/color}"%getattr(eqtarget, stat)

        tempstr = tempstr + "{color=[tempc]}/{/color}"

        if tempmax:
            # Absolute change of the max values, same rules as the actual values apply:
            tempstr = tempstr + "{color=[green]}%s{/color}"%dummy.get_max(stat) if tempmax > 0 else tempstr + "{color=[red]} %d{/color}"%dummy.get_max(stat)
            tempstr = tempstr + "{=positive_item_eqeffects_change}(+%d){/=}"%tempmax if tempmax > 0 else tempstr + "{=negative_item_eqeffects_chage}(%d){/=}"%tempmax
        else:
            tempstr = tempstr + "{color=[tempc]}%s{/color}"%eqtarget.get_max(stat)
        return tempstr

label char_equip:
    python:
        focusitem = None
        selectedslot = None
        unequip_slot = None
        item_direction = None
        dummy = None
        eqsave = [False, False, False]

        if not eqtarget:
            came_to_equip_from = "chars_list"
            eqtarget = PytGroup(the_chosen) if the_chosen else char

        if not hasattr(store, "equip_girls") or equip_girls is None or char not in equip_girls:
            if isinstance(eqtarget, PytGroup) or eqtarget == hero:
                equip_girls = []
            else:
                equip_girls = list(girl for girl in hero.chars if girl.action != "Exploring")

        eqtarget.inventory.set_page_size(16)
        hero.inventory.set_page_size(16)
        inv_source = eqtarget

    scene bg gallery3

    $ global_flags.set_flag("hero_equip")
    $ renpy.retain_after_load()
    show screen char_equip

    $ inv_source.inventory.apply_filter("all")

label char_equip_loop:
    while 1:
        $ result = ui.interact()
        #$ char = eqtarget

        if not result:
            jump char_equip_loop

        if result[0] == "jump":
            if result[1] == "item_transfer":
                hide screen char_equip
                $ items_transfer([hero] + (list(eqtarget.lst) if isinstance(eqtarget,PytGroup) else [eqtarget]))
                $ eqtarget.inventory.set_page_size(16)
                $ hero.inventory.set_page_size(16)
                show screen char_equip

        elif result[0] == "equip_for":
            python:
                renpy.show_screen("equip_for", renpy.get_mouse_pos())
                dummy = None

        elif result[0] == "item":
            if result[1] == 'equip/unequip':
                $ dummy = None # Must be set here so the items that jump away to a label work properly.
                python:
                    # Equipping:
                    if item_direction == 'equip':
                        # Common to any eqtarget:
                        if not can_equip(focusitem, eqtarget, silent=False):
                            focusitem = None
                            selectedslot = None
                            unequip_slot = None
                            item_direction = None
                            jump("char_equip_loop")

                        # See if we can access the equipment first:
                        if equipment_access(eqtarget, focusitem):
                            # If we're not equipping from own inventory, check if we can transfer:
                            if eqtarget != inv_source:
                                if not transfer_items(inv_source, eqtarget, focusitem):
                                    # And terminate if we can not...
                                    jump("char_equip_loop")

                            # If we got here, we just equip the item :D
                            equip_item(focusitem, eqtarget)

                    elif item_direction == 'unequip':
                        # Check if we are allowed to access inventory and act:
                        if equipment_access(eqtarget):
                            eqtarget.unequip(focusitem, unequip_slot)

                            # We should try to transfer items in case of:
                            # We don't really care if that isn't possible...
                            if inv_source != eqtarget:
                                transfer_items(eqtarget, inv_source, focusitem, silent=False)

                    focusitem = None
                    selectedslot = None
                    unequip_slot = None
                    item_direction = None

            elif result[1] == "discard":
                python:
                    # Check if we can access the inventory:
                    if equipment_access(inv_source):
                        renpy.call_screen("discard_item", inv_source, focusitem)

                    focusitem = None
                    selectedslot = None
                    unequip_slot = None
                    item_direction = None
                    dummy = None
                    eqsave = {0:False, 1:False, 2:False}

            elif result[1] == "transfer":
                python:
                    if inv_source == hero:
                        transfer_items(hero, eqtarget, focusitem, silent=False)
                    else:
                        transfer_items(eqtarget, hero, focusitem, silent=False)

            elif result[1] == 'equip':
                python:
                    focusitem = result[2]
                    if isinstance(inv_source, PytGroup) and inv_source.inventory[focusitem] == 0:

                        selected_chars = inv_source.all
                        inv_source.lst = set([c for c in selected_chars if c.inventory[focusitem]])
                        inv_source.unselected = set([c for c in selected_chars if not c.inventory[focusitem]])

                    selectedslot = focusitem.slot
                    item_direction = 'equip'

                    # # To Calc the effects:
                    dummy = copy_char(eqtarget._first if isinstance(eqtarget, PytGroup) else eqtarget)
                    equip_item(focusitem, dummy, silent=True)
                    # renpy.show_screen("diff_item_effects", eqtarget, dummy)

            elif result[1] == 'unequip':
                python:
                    unequip_slot = result[3]

                    if isinstance(eqtarget, PytGroup):

                        if isinstance(result[2], list):
                            # chars have different items in the equipslots. Will show the most abundant in sepia
                            chosen_item = result[2][0]
                        else:
                            # This (sub)group has only one item. shown in color.
                            chosen_item = result[2]
                            # ring itemslot can be ring while actual slot is ring1 or ring2

                            if focusitem == chosen_item:
                                # The focusitem was clicked a 2nd time, so determine next item and subgroup from all chars.
                                eqtarget.lst = set(eqtarget.all)
                                eqtarget.unselected = set()

                                all_slotequip = eqtarget.eqslots[unequip_slot]

                                if isinstance(all_slotequip, list):
                                    # a list, so there is a next subgroup
                                    chosen_item = all_slotequip[(all_slotequip.index(chosen_item) + 1) % len(all_slotequip)]
                                    eqtarget.lst = set(eqtarget.all)

                        if focusitem != chosen_item:
                            subgroup_equipped = set([c for c in eqtarget.lst if c.eqslots[unequip_slot] == chosen_item])
                            eqtarget.unselected = set(eqtarget.all).difference(subgroup_equipped)
                            eqtarget.lst = subgroup_equipped

                        result[2] = chosen_item
                        dummy = copy_char(eqtarget._first)
                    else:
                        dummy = copy_char(eqtarget)

                    focusitem = result[2]
                    item_direction = 'unequip'

                    if focusitem:
                        # To Calc the effects:
                        dummy.eqslots[unequip_slot] = focusitem
                        dummy.unequip(focusitem, unequip_slot)
                        #renpy.show_screen("diff_item_effects", eqtarget, dummy)

        elif result[0] == "unequip_all":
            python:
                if isinstance(eqtarget, PytGroup):
                    for c in eqtarget.lst:
                        # Check if we are allowed to access inventory and act:
                        if equipment_access(c, silent=True):
                            for slot in c.eqslots.values():
                                if slot:
                                    c.unequip(slot)

                elif equipment_access(eqtarget, silent=False):
                    for slot in eqtarget.eqslots.values():
                        if slot:
                            eqtarget.unequip(slot)

                focusitem = None
                selectedslot = None
                unequip_slot = None
                item_direction = None

        elif result[0] == "auto_discard": # TODO: remove
            python:
                if isinstance(eqtarget, PytGroup):
                    for c in eqtarget.lst:
                        # Check if we are allowed to access inventory and act:
                        if equipment_access(c, silent=True):
                            c.auto_discard()

                elif equipment_access(eqtarget, silent=False) and eqtarget != hero:
                    eqtarget.auto_discard()

                focusitem = None
                selectedslot = None
                unequip_slot = None
                item_direction = None

        elif result[0] == 'con':
            if result[1] == 'return':
                python:
                    focusitem = None
                    selectedslot = None
                    unequip_slot = None
                    item_direction = None
                    dummy = None
                    eqsave = {0:False, 1:False, 2:False}

        elif result[0] == 'control':
            if result[1] == 'return':
                jump char_equip_finish
            elif equip_girls:
                python:

                    focusitem = None
                    selectedslot = None
                    unequip_slot = None
                    item_direction = None
                    dummy = None

                    index = equip_girls.index(char)
                    if result[1] == 'left':
                        char = equip_girls[ (index - 1) % len(equip_girls)]
                    elif result[1] == 'right':
                        char = equip_girls[(index + 1) % len(equip_girls)]

                    if inv_source == eqtarget:
                        inv_source = char
                    eqtarget = char

label char_equip_finish:
    hide screen char_equip
    $ global_flags.del_flag("hero_equip")

    python:
        eqtarget.inventory.set_page_size(15)
        hero.inventory.set_page_size(15)

        # eqtarget.inventory.female_filter = False
        # hero.inventory.female_filter = False
        if eqtarget.location == "After Life":
            renpy.show_screen("message_screen", "Either your 'awesome' item handling or my 'brilliant' programming killed %s..." % eqtarget.fullname)
            jump("mainscreen")

    python:
        # Reset all globals so screens that lead here don't get thrown off:
        focusitem = None
        selectedslot = None
        unequip_slot = None
        item_direction = None
        dummy = None
        eqtarget = None
        eqsave = None
        equip_girls = None

    if came_to_equip_from:
        $ last_label, came_to_equip_from = came_to_equip_from, None
        jump expression last_label
    else:
        jump char_profile

screen equip_for(pos=()):
    zorder 3
    modal True

    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    python:
        x, y = pos
        if x > 1000:
            xval = 1.0
        else:
            xval = 0.0
        if y > 500:
            yval = 1.0
        else:
            yval = 0.0

        specializations = ["Sex", "Service", "Striptease"]

        if eqtarget.status != "slave" and eqtarget.status != "various":
            specializations = ["Battle Mage", "Barbarian", "Wizard"] + specializations
    frame:
        style_group "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        vbox:
            text "Equip For:" xalign 0 style "della_respira" color ivory
            null height 5
            for t in specializations:
                textbutton "[t]":
                    xminimum 200
                    # action NullAction()
                    action [Function(eqtarget.equip_for, t), Hide("equip_for")]
            textbutton "Close":
                action Hide("equip_for")

screen char_equip():

    # Useful keymappings (first time I try this in PyTFall): ====================================>
    if focusitem:
        key "mousedown_2" action Return(["item", "equip/unequip"])
    else:
        key "mousedown_2" action NullAction()
    key "mousedown_3" action Return(['control', 'return'])
    key "mousedown_4" action Function(inv_source.inventory.next)
    key "mousedown_5" action Function(inv_source.inventory.prev)
    key "mousedown_6" action Return(['con', 'return'])

    default stats_display = "stats"
    default tt = Tooltip("")

    # BASE FRAME 2 "bottom layer" ====================================>
    add "content/gfx/frame/equipment2.png"

    # Equipment slots:
    frame:
        pos (425, 10)
        xysize 298, 410
        # xminimum 298
        # xmaximum 298
        # ymaximum 410
        # yminimum 410
        background Frame(Transform("content/gfx/frame/Mc_bg3.png", alpha=0.3), 10, 10)
        use eqdoll(active_mode=True, char=eqtarget, frame_size=[70, 70], scr_align=(0.98, 1.0), return_value=['item', "unequip"], txt_size=17, fx_size=(455, 400))

    # BASE FRAME 3 "mid layer" ====================================>
    add "content/gfx/frame/equipment.png"

    # Item Info (Mid-Bottom Frame): ====================================>
    hbox:
        align (0.388, 1.0)
        spacing 1
        style_group "content"

        # Item Description:
        frame:
            xalign 0.6
            at fade_in_out()
            background Transform(Frame(im.MatrixColor("content/gfx/frame/Mc_bg3.png", im.matrix.brightness(-0.2)), 5, 5), alpha=0.3)
            xysize (710, 296)
            use char_equip_item_info(item=focusitem, size=(703, 287), tt=tt)

    if not isinstance(eqtarget, PytGroup):
        use char_equip_left_frame(tt, stats_display)
    else:
        use group_equip_left_frame(tt)

screen char_equip_left_frame(tt, stats_display):
    # Left Frame: =====================================>
    fixed:
        pos (0, 2)
        xysize (220,724)
        style_group "content"

        # NAME =====================================>
        text (u"{color=#ecc88a}[eqtarget.name]") font "fonts/TisaOTM.otf" size 28 outlines [(1, "#3a3a3a", 0, 0)] xalign .53 ypos 126
        hbox:
            button:
                xysize (32, 32)
                background Null()
                if equip_girls and not(equipment_safe_mode):
                    action Return(['control', 'left'])
                    foreground "content/gfx/interface/buttons/small_button_wood_left_idle.png" pos (10, 14)
                    hover_foreground "content/gfx/interface/buttons/small_button_wood_left_hover.png"
            # PORTRAIT ============================>
            frame:
                xysize (100, 100)
                pos (32, 11)
                background Frame("content/gfx/frame/mes12.jpg", 5, 5)
                add eqtarget.show("portrait", resize=(90, 90), cache=True) align .5, .5
            button:
                xysize (32, 32)
                background Null()
                if equip_girls and not(equipment_safe_mode):
                    action Return(['control', 'right'])
                    foreground "content/gfx/interface/buttons/small_button_wood_right_idle.png" pos (45, 14)
                    hover_foreground "content/gfx/interface/buttons/small_button_wood_right_hover.png"

        # LVL ============================>
        hbox:
            spacing 1
            if (inv_source.level) < 10:
                xpos 95
            elif (inv_source.level) < 100:
                xpos 93
            elif (inv_source.level) < 1000:
                xpos 89
            elif (inv_source.level) < 10000:
                xpos 83
            else:
                xpos 79
            label "{color=#CDAD00}Lvl" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)] ypos 173
            label "{color=#CDAD00}[eqtarget.level]" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)] ypos 173

        # Left Frame Buttons: =====================================>
        hbox:
            style_group "pb"
            xalign 0.55
            ypos 198
            spacing 1
            button:
                xsize 100
                action SetScreenVariable("stats_display", "stats"), With(dissolve)
                text "Stats" style "pb_button_text" yoffset 2
            button:
                xsize 100
                action SetScreenVariable("stats_display", "pro"), With(dissolve)
                text "Skills" style "pb_button_text" yoffset 2

        # Stats/Skills:
        vbox:
            yfill True
            yoffset 195
            spacing 2
            xmaximum 218

            if stats_display == "stats":
                vbox:
                    spacing 5
                    pos (4, 40)
                    frame:
                        background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                        xsize 218
                        padding 6, 6
                        margin 0, 0
                        style_group "proper_stats"
                        has vbox spacing 1
                        # STATS ============================>
                        $ stats = ["constitution", "charisma", "intelligence", "fame", "reputation"] if eqtarget == hero else ["constitution", "charisma", "intelligence", "character", "reputation", "joy", "disposition"]

                        # Health:
                        frame:
                            xysize 204, 25
                            text "Health:" xalign .02 color "#CD4F39"
                            $ tempc = red if eqtarget.health <= eqtarget.get_max("health")*0.3 else "#F5F5DC"
                            if dummy:
                                $ tempstr = build_str_for_eq(eqtarget, dummy, "health", tempc)
                                text tempstr style_suffix "value_text" xalign .98 yoffset 3
                            else:
                                text u"[eqtarget.health]/{}".format(eqtarget.get_max("health")) xalign .98 yoffset 3 style_suffix "value_text" color tempc

                        # Vitality:
                        frame:
                            xysize 204, 25
                            text "Vitality:" xalign .02 color "#43CD80"
                            $ tempc = red if eqtarget.vitality <= eqtarget.get_max("vitality")*0.3 else "#F5F5DC"
                            if dummy:
                                $ tempstr = build_str_for_eq(eqtarget, dummy, "vitality", tempc)
                                text tempstr style_suffix "value_text" xalign .98 yoffset 3
                            else:
                                text u"[eqtarget.vitality]/{}".format(eqtarget.get_max("vitality")) xalign .98 yoffset 3 style_suffix "value_text" color tempc

                        # Rest of stats:
                        for stat in stats:
                            frame:
                                xysize 204, 25
                                text "{}".format(stat.capitalize()) xalign .02 color "#79CDCD"
                                $ tempc = "#F5F5DC"
                                if dummy:
                                    $ tempstr = build_str_for_eq(eqtarget, dummy, stat, "#F5F5DC")
                                    text tempstr style_suffix "value_text" xalign .98 yoffset 3
                                else:
                                    text u"{}/{}".format(getattr(eqtarget, stat), eqtarget.get_max(stat)) xalign .98 yoffset 3 style_suffix "value_text" color "#F5F5DC"

                    # BATTLE STATS ============================>
                    frame:
                        background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                        xsize 218
                        padding 6, 6
                        style_group "proper_stats"
                        has vbox spacing 1

                        null height 1
                        label (u"{size=18}{color=#CDCDC1}{b}Battle Stats:") xalign .49
                        $ stats = [("Attack", "#CD4F39"), ("Defence", "#dc762c"), ("Magic", "#8470FF"), ("MP", "#009ACD"), ("Agility", "#1E90FF"), ("Luck", "#00FA9A")]
                        null height 1

                        for stat, color in stats:
                            frame:
                                xysize 204, 25
                                text "[stat]" color color
                                $ stat = stat.lower()
                                if stat == "mp":
                                    $ tempc = red if eqtarget.mp <= eqtarget.get_max("mp")*0.3 else color
                                else:
                                    $ tempc = color
                                if dummy:
                                    $ tempstr = build_str_for_eq(eqtarget, dummy, stat, tempc)
                                    text tempstr style_suffix "value_text" xalign .98 yoffset 3
                                else:
                                    text "{}/{}".lower().format(getattr(eqtarget, stat.lower()), eqtarget.get_max(stat.lower())) xalign .98 yoffset 3 style_suffix "value_text" color tempc
            elif stats_display == "pro":
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-.1)), 5, 5), alpha=.7)
                    pos (4, 40)
                    ymaximum 460
                    has vbox style_prefix "proper_stats" spacing 1
                    if getattr(focusitem, "mod_skills", {}):
                        label (u"Pure Bonus:") text_size 20 text_color goldenrod text_bold True xalign .45
                    for skill, data in getattr(focusitem, "mod_skills", {}).iteritems():
                        frame:
                            xysize 208, 22
                            text str(skill).title() size 16 color yellowgreen align .0, .5

                            $ img_path = "content/gfx/interface/icons/skills_icons/"

                            default PS = ProportionalScale

                            hbox:
                                align .99, .5
                                spacing 2
                                yoffset 1
                                button:
                                    style "default"
                                    xysize 20, 18
                                    action NullAction()
                                    yoffset 2
                                    hovered tt.action("Icon represents skills modifier changes. Green means bonus, red means penalty. Left one is action counter, right one is training counter, top one is resulting value.")
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
                                if data[3]:
                                    button:
                                        style "default"
                                        action NullAction()
                                        hovered tt.action("Direct bonus to action skill values.")
                                        label "A: " + str(data[3]) text_size 15
                                if data[4]:
                                    button:
                                        style "default"
                                        action NullAction()
                                        hovered tt.action("Direct bonus to knowledge skill values.")
                                        label "K: " + str(data[4]) text_size 15

    use char_equip_right_frame(tt)

screen group_equip_left_frame(tt):

    # Left Frame: =====================================>
    fixed:
        pos (0, 2)
        xysize (220,724)
        style_group "content"
        hbox:
            button:
                xysize (32, 32)
                action SetField(eqtarget, "lst", set(eqtarget.all)), SetField(eqtarget, "unselected", set()), SetVariable("focusitem", None), SetVariable("dummy", None)
                background Null()
                foreground ProportionalScale("content/gfx/interface/buttons/Group_full.png", 32, 32) pos (14, 70)
                hover_foreground ProportionalScale(im.MatrixColor("content/gfx/interface/buttons/Group_full.png", im.matrix.brightness(0.20)), 34, 34)
            # PORTRAIT ============================>
            frame:
                xysize (100, 100)
                background Frame("content/gfx/frame/mes12.jpg", 5, 5)
                foreground eqtarget.show("portrait", resize=(100, 100), cache=True) pos (32, 11)

        # list of names of characters in group with selection options.
        viewport:
            ymaximum 590
            pos (4, 120)
            style_group "proper_stats"
            frame:
                padding 4, 4
                ymaximum 590
                background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                xsize 218
                has hbox
                hbox:
                    for offs in [0, 1]:
                        vbox:
                            yfill True
                            spacing 5
                            frame:
                                xsize 104
                                ymaximum 585
                                padding 6, 6
                                margin 0, 0
                                has vbox spacing 1
                                # character togglebuttons:
                                for k in eqtarget.all[offs::2]:
                                    button:
                                        action ToggleSetMembership(eqtarget.lst, k), ToggleSetMembership(eqtarget.unselected, k), SetVariable("focusitem", None), SetVariable("dummy", None)
                                        background Null()
                                        if k in eqtarget.lst:
                                            if len(eqtarget) == 1:
                                                sensitive False
                                            text u"[k.name]" xalign .98 yoffset 3 style_suffix "value_text" color "#F5F5DC"
                                        else:
                                            text u"[k.name]" xalign .98 yoffset 3 style_suffix "value_text" color "#75755C"
                                        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.10)), 0, 0)


    use char_equip_right_frame(tt)

screen char_equip_right_frame(tt):
    # Right Frame: =====================================>
    # TOOLTIP TEXT or Applied Traits and Skills ====================================>
    frame:
        pos (930, 4)
        background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.4), 10, 10)
        xpadding 10
        xysize (345, 110)

        python:
            if not isinstance(eqtarget, PytGroup):
                if len(eqtarget.traits.basetraits) == 1:
                    classes = list(eqtarget.traits.basetraits)[0].id
                elif len(eqtarget.traits.basetraits) == 2:
                    classes = list(eqtarget.traits.basetraits)
                    classes.sort()
                    classes = ", ".join([str(c) for c in classes])
                else:
                    if eqtarget != hero:
                        raise Exception("Character without prof basetraits detected! line: 267, girlsprofile screen")
                    else:
                        classes = "MC baseclasses are still AFK :("

                t = "{vspace=17}Classes: [classes]\nLocation: [eqtarget.location]\nAction: [eqtarget.action]{/color}"
            else:
                t = "{vspace=17}[eqtarget.name]{/color}"

        if tt.value:
            text "{color=#ecc88a}%s"%tt.value size 14 align (0.5, 0.5) font "fonts/TisaOTM.otf" line_leading -5
        elif dummy:
            # Traits and skills:
            vbox:
                hbox:
                    add "content/gfx/interface/images/add.png" yalign .5 yoffset -3
                    add "content/gfx/interface/images/remove.png" yalign .5 yoffset -5
                    label ('Traits|Effects:') text_size 16 text_color gold style "stats_label"
                viewport:
                    mousewheel True
                    has vbox
                    style_group "proper_stats"
                    python:
                        eqt = eqtarget._first if isinstance(eqtarget, PytGroup) else eqtarget
                        t_old = set(t.id for t in eqt.traits)
                        for effect, data in getattr(eqt, "effects", {}).iteritems():
                            if data['active']: t_old.add(effect)
                        t_new = set(t.id for t in dummy.traits)
                        for effect, data in getattr(dummy, "effects", {}).iteritems():
                            if data['active']: t_new.add(effect)
                        temp = t_new.difference(t_old)
                        temp = sorted(list(temp))
                    for i in temp:
                        frame:
                            xpadding 3
                            text u'{color=#43CD80}%s'%i size 16 yalign 0.5

                    python:
                        t_old = set(t.id for t in dummy.traits)
                        for effect, data in getattr(dummy, "effects", {}).iteritems():
                            if data['active']: t_old.add(effect)
                        t_new = set(t.id for t in eqt.traits)
                        for effect, data in getattr(eqt, "effects", {}).iteritems():
                            if data['active']: t_new.add(effect)
                        temp = t_new.difference(t_old)
                        temp = sorted(list(temp))
                    for i in temp:
                        frame:
                            xpadding 3
                            text u'{color=#CD4F39}%s'%i size 16 yalign 0.5

            vbox:
                xoffset 165
                hbox:
                    add "content/gfx/interface/images/add.png" yalign .5 yoffset -3
                    add "content/gfx/interface/images/remove.png" yalign .5 yoffset -5
                    label ('Battle Skills:') text_size 16 text_color gold style "stats_label"
                viewport:
                    mousewheel True
                    has vbox
                    style_group "proper_stats"
                    python:
                        s_old = set(s.name for s in list(eqt.attack_skills) + list(eqt.magic_skills))
                        s_new = set(s.name for s in list(dummy.attack_skills) + list(dummy.magic_skills))
                        temp = s_new.difference(s_old)
                        temp = sorted(list(temp))
                    if temp:
                        for skill in temp:
                            frame:
                                xpadding 3
                                text u'{color=#43CD80}%s'%skill size 16

                    python:
                        s_old = set(s.name for s in list(dummy.attack_skills) + list(dummy.magic_skills))
                        s_new = set(s.name for s in list(eqt.attack_skills) + list(eqt.magic_skills))
                        temp = s_new.difference(s_old)
                        temp = sorted(list(temp))
                    if temp:
                        for skill in temp:
                            frame:
                                xalign 0.98
                                xpadding 3
                                text u'{color=#CD4F39}%s'%skill size 16 yalign 0.5
        elif not tt.value:
            if isinstance(eqtarget, PytGroup):
                text (u"{color=#ecc88a}%s" % t) size 14 align (0.55, 0.65) font "fonts/TisaOTM.otf" line_leading -5
            elif eqtarget.status == "slave":
                text (u"{color=[gold]}[eqtarget.name]{/color}{color=#ecc88a}  is Slave%s" % t) size 14 align (0.55, 0.65) font "fonts/TisaOTM.otf" line_leading -5
            elif eqtarget.status == "free":
                text (u"{color=[gold]}[eqtarget.name]{/color}{color=#ecc88a}  is Free%s" % t) size 14 align (0.55, 0.65) font "fonts/TisaOTM.otf" line_leading -5


    # Right Frame Buttons ====================================>
    vbox:
        pos (931, 118)
        xsize 345
        spacing 4
        style_group "pb"
        hbox:
            xalign 0.5
            spacing 100
            button:
                xsize 70
                action SelectedIf(eqtarget == hero or inv_source == hero), If(eqtarget != hero, true=[SetVariable("inv_source", hero), Function(eqtarget.inventory.apply_filter, hero.inventory.slot_filter), Return(['con', 'return']), With(dissolve)])
                hovered tt.Action("Equip from [hero.nickname]'s Inventory")
                text "Hero" style "pb_button_text"
            button:
                xsize 70
                action SelectedIf(inv_source != hero), SensitiveIf(eqtarget != hero), If(eqtarget != hero, true=[SetVariable("inv_source", eqtarget), Function(eqtarget.inventory.apply_filter, hero.inventory.slot_filter), Return(['con', 'return']), With(dissolve)])
                hovered tt.Action("Equip from [eqtarget.nickname]'s Inventory")
                text "Girl" style "pb_button_text"
        button: # TODO: remove
            xalign 0.5
            xysize (110, 30)
            action If(eqtarget != hero, true=Return(["auto_discard"]))
            text "Auto discard" style "pb_button_text"

    # Auto-Equip/Item Transfer Buttons and Paging: ================>
    frame:
        background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
        pos (931, 184)
        xysize (345, 80)
        has vbox spacing 1 xalign 0.5
        hbox:
            button:
                xysize (110, 30)
                action Return(["equip_for"])
                text "Auto equip" style "pb_button_text"
            button:
                xysize (110, 30)
                action Return(["unequip_all"])
                text "Unequip all" style "pb_button_text"
            button:
                xysize (110, 30)
                action If(eqtarget != hero, true=Return(["jump", "item_transfer"]))
                text "Exchange" style "pb_button_text"
        use paging(ref=inv_source.inventory, use_filter=False, xysize=(250, 20), align=(0.5, 0.5))

    # Filters: ====================================>
    hbox:
        pos (935, 268)
        box_wrap True
        style_group "dropdown_gm"
        xsize 340
        spacing 2
        for filter in inv_source.inventory.filters:
            frame:
                xpadding 0
                ymargin -8
                background Null()
                if renpy.loadable("content/gfx/interface/buttons/filters/%s.png" % filter):
                    $ img = ProportionalScale("content/gfx/interface/buttons/filters/%s.png" % filter, 44, 44)
                    $ img_hover = ProportionalScale("content/gfx/interface/buttons/filters/%s hover.png" % filter, 44, 44)
                    $ img_selected = ProportionalScale("content/gfx/interface/buttons/filters/%s selected.png" % filter, 44, 44)
                else:
                    $ img = Solid("#FFF", xysize=(44, 44))
                    $ img_hover = Solid("#FFF", xysize=(44, 44))
                    $ img_selected = Solid("#FFF", xysize=(44, 44))
                imagebutton:
                    idle img
                    hover Transform(img_hover, alpha=1.1)
                    selected_idle img_selected
                    selected_hover Transform(img_selected, alpha=1.15)
                    action [Function(inv_source.inventory.apply_filter, filter), SelectedIf(filter == inv_source.inventory.slot_filter)], With(dissolve)
                    focus_mask True

    # Inventory: ====================================>
    frame:
        pos (931, 372)
        background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
        use items_inv(char=inv_source, main_size=(333, 333), frame_size=(80, 80), return_value=['item', 'equip'])

    # BASE FRAME 1 "top layer" ====================================>
    add "content/gfx/frame/h1.png"

    imagebutton:
        pos (178, 70)
        idle im.Scale("content/gfx/interface/buttons/close2.png", 35, 35)
        hover im.Scale("content/gfx/interface/buttons/close2_h.png", 35, 35)
        action Return(['control', 'return'])
        hovered tt.Action("Return to previous screen!")

screen char_equip_item_info(item=None, char=None, size=(635, 380), style_group="content", mc_mode=False, tt=None):

    key "mousedown_3" action Return(['con', 'return'])

    # One of the most difficult code rewrites I've ever done (How Gismo aligned everything in the first place is a work of (weird and clumsy) art...):
    # Recoding this as three vertically aligned HBoxes...
    if item:
        $ xs = size[0]
        $ ys = size[1]
        fixed:
            style_prefix "proper_stats"
            xysize size

            # Top HBox: Discard/Close buttons and the Item ID:
            hbox:
                align .5, .0
                xsize xs-10
                imagebutton:
                    xalign 0
                    idle ("content/gfx/interface/buttons/discard.png")
                    hover ("content/gfx/interface/buttons/discard_h.png")
                    action Return(["item", "discard"])
                    if tt:
                        hovered tt.Action("Discard item")
                frame:
                    align .5, .5
                    xysize (439, 35)
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 10, 10), alpha=0.9)
                    label ('[item.id]') text_color gold align .5, .5 text_size 19 text_outlines [(1, "#000000", 0, 0)] text_style "interactions_text"
                imagebutton:
                    xalign 1.0
                    idle ("content/gfx/interface/buttons/close3.png")
                    hover ("content/gfx/interface/buttons/close3_h.png")
                    action Return(['con', 'return'])
                    if tt:
                        hovered tt.Action("Close item info")

            # Separation Strip (Outside of alignments):
            label ('{color=#ecc88a}--------------------------------------------------------------------------------------------------') xalign .5 ypos 25
            label ('{color=#ecc88a}--------------------------------------------------------------------------------------------------') xalign .5 ypos 163

            # Mid HBox:
            hbox:
                xsize xs
                xalign .5
                ypos 47
                spacing 5

                # Left Items Info:
                frame:
                    xalign .02
                    style_prefix "proper_stats"
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                    xysize (180, 130)
                    xpadding 0
                    xmargin 0
                    has vbox spacing 1 xoffset 10
                    null height 15
                    frame:
                        xysize (160, 25)
                        text 'Price:' color gold xalign .02
                        label '{size=-4}{color=[gold]}[item.price]' align .98, .5 text_outlines [(1, "#3a3a3a", 0, 0)]
                    frame:
                        xysize (160, 25)
                        text ('{color=#F5F5DC}Slot:') xalign 0.02
                        python:
                            if item.slot in SLOTALIASES:
                                slot = SLOTALIASES[item.slot]
                            else:
                                slot = item.slot.capitalize()
                        label ('{color=#F5F5DC}{size=-4}%s'%slot) align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                    frame:
                        xysize (160, 25)
                        text ('{color=#F5F5DC}Type:') xalign 0.02
                        label ('{color=#F5F5DC}{size=-4}%s'%item.type.capitalize()) align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                    frame:
                        xysize (160, 25)
                        text ('{color=#F5F5DC}Sex:') xalign 0.02
                        if item.slot in ["gift", "resources", "loot"]:
                            label "{size=-4}N/A" align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                        elif item.type == "food" and item.sex == "unisex":
                            label "{size=-4}N/A" align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                        elif item.sex == 'male':
                            label ('{color=#F5F5DC}{size=-4}{color=#FFA54F}%s'%item.sex.capitalize()) align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                        elif item.sex == 'female':
                            label ('{color=#F5F5DC}{size=-4}{color=#FFAEB9}%s'%item.sex.capitalize()) align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                        elif item.sex == 'unisex':
                            label ('{color=#F5F5DC}{size=-4}%s'%item.sex.capitalize()) align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]

                # Buttons and image:
                button:
                    style_group "pb"
                    align (0.0, 0.5)
                    xysize (80, 45)
                    action SensitiveIf(eqtarget != hero and ((eqtarget.inventory[item] > 0 and inv_source == eqtarget) or (hero.inventory[item] > 0 and inv_source == hero))), Return(['item', 'transfer'])
                    if eqtarget == hero:
                        hovered tt.Action("Disabled")
                        text "Disabled" style "pb_button_text" align (0.5, 0.5)
                    elif inv_source == hero:
                        hovered tt.Action("Transfer {} from {} to {}".format(item.id, hero.nickname, eqtarget.nickname))
                        text "Give to\n {color=#FFAEB9}[eqtarget.nickname]{/color}" style "pb_button_text" align (0.5, 0.5) line_leading 3
                    else:
                        text "Give to\n {color=#FFA54F}[hero.nickname]{/color}" style "pb_button_text" align (0.5, 0.5) line_leading 3
                        hovered tt.Action("Transfer {} from {} to {}".format(item.id, eqtarget.nickname, hero.nickname))

                frame:
                    align (0.5, 0.5)
                    background Frame("content/gfx/frame/frame_it2.png", 5, 5)
                    xysize (120, 120)
                    add (ProportionalScale(item.icon, 100, 100)) align(0.5, 0.5)

                if item_direction == 'unequip':
                    $ temp = "Unequip"
                    $ temp_msg = "Unequip {}".format(item.id)
                elif item_direction == 'equip':
                    if item.slot == "consumable":
                        $ temp = "Use"
                        $ temp_msg = "Use {}".format(item.id)
                    else:
                        $ temp = "Equip"
                        $ temp_msg = "Equip {}".format(item.id)
                button:
                    style_group "pb"
                    align (1.0, 0.5)
                    xysize (80, 45)
                    if tt:
                       hovered tt.Action(temp_msg)
                    action SensitiveIf(focusitem), Return(['item', 'equip/unequip'])
                    if item_direction == 'equip' and not can_equip(focusitem, eqtarget):
                        text "[temp]" style "pb_button_text" align (0.5, 0.5) color red strikethrough True
                    else:
                        text "[temp]" style "pb_button_text" align (0.5, 0.5)

                # Right items info (Stats):
                frame:
                    xalign 0.98
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                    xysize (185, 130)
                    style_group "proper_stats"
                    left_padding 6
                    right_padding 3
                    ypadding 5
                    has viewport draggable True mousewheel True child_size 200, 500
                    vbox:
                        if item.mod:
                            label ('Stats:') text_size 18 text_color gold xpos 30
                            vbox:
                                spacing 1
                                for stat, value in item.mod.items():
                                    frame:
                                        xysize (172, 18)
                                        text (u'{color=#F5F5DC}%s' % stat.capitalize()) size 15 xalign 0.02 yoffset -2
                                        label (u'{color=#F5F5DC}{size=-4}[value]') align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                            null height 3

                        if item.max:
                            label ('Max:') text_size 16 text_color gold xpos 30
                            vbox:
                                spacing 1
                                for stat, value in item.max.items():
                                    frame:
                                        xysize (172, 18)
                                        text (u'{color=#F5F5DC}%s'%stat.capitalize()) size 15 xalign 0.02 yoffset -2
                                        label (u'{color=#F5F5DC}{size=-4}[value]') align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                            null height 3

                        if item.min:
                            label ('Min:') text_size 16 text_color gold xpos 30
                            vbox:
                                spacing 1
                                for stat, value in item.min.items():
                                    frame:
                                        xysize (172, 18)
                                        text (u'{color=#F5F5DC}%s'%stat.capitalize()) size 15 xalign 0.02 yoffset -2
                                        label (u'{color=#F5F5DC}{size=-4}%d'%value) align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                        if hasattr(item, 'mtemp'):
                            if item.mtemp:
                                label ('Frequency:') text_size 16 text_color gold xpos 30
                                vbox:
                                    frame:
                                        xysize (172, 18)
                                        if hasattr(item, 'mreusable'):
                                            if item.mreusable:
                                                if item.mtemp > 1:
                                                    text (u'{color=#F5F5DC}Every %d days'%item.mtemp) size 15 xalign 0.02 yoffset -2
                                                else:
                                                    text (u'{color=#F5F5DC}Every day') size 15 xalign 0.02 yoffset -2
                                            else:
                                                if item.mtemp > 1:
                                                    text (u'{color=#F5F5DC}After %d days'%item.mtemp) size 15 xalign 0.02 yoffset -2
                                                else:
                                                    text (u'{color=#F5F5DC}After one day') size 15 xalign 0.02 yoffset -2
                                    if hasattr(item, 'mdestruct'):
                                        if item.mdestruct:
                                            frame:
                                                xysize (172, 18)
                                                text (u'{color=#F5F5DC}Disposable') size 15 xalign 0.02 yoffset -2
                                    if hasattr(item, 'mreusable'):
                                        if item.mreusable:
                                            frame:
                                                xysize (172, 18)
                                                text (u'{color=#F5F5DC}Reusable') size 15 xalign 0.02 yoffset -2
                                    if hasattr(item, 'statmax'):
                                        if item.statmax:
                                            frame:
                                                xysize (172, 18)
                                                text (u'{color=#F5F5DC}Stat limit') size 15 xalign 0.02 yoffset -2
                                                label (u'{color=#F5F5DC}{size=-4}%d'%item.statmax) align (0.98, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                        if hasattr(item, 'ctemp'):
                            if item.ctemp:
                                label ('Duration:') text_size 16 text_color gold xpos 30
                                frame:
                                    xysize (172, 18)
                                    if item.ctemp > 1:
                                        text (u'{color=#F5F5DC}%d days'%item.ctemp) size 15 xalign 0.02 yoffset -2
                                    else:
                                        text (u'{color=#F5F5DC}One day') size 15 xalign 0.02 yoffset -2

            # Bottom HBox: Desc/Traits/Effects/Skills:
            hbox:
                yalign 1.0
                # Traits, Effects:
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                    xysize 158, 104
                    padding 2, 3
                    has viewport draggable True mousewheel True

                    # Traits:
                    vbox:
                        style_group "proper_stats"
                        xsize 150
                        if item.addtraits or item.removetraits:
                            hbox:
                                xalign .5
                                if item.addtraits:
                                    add "content/gfx/interface/images/add.png" yalign .5
                                if item.removetraits:
                                    add "content/gfx/interface/images/remove.png"  yalign .5 yoffset -2
                                null width 4
                                label ('Traits:') text_size 14 text_color gold

                            for trait in item.addtraits:
                                frame:
                                    xalign .1
                                    xpadding 2
                                    text (u'{color=#43CD80}%s'%trait) size 15 align .5, .5
                            for trait in item.removetraits:
                                frame:
                                    xalign 0.9
                                    xpadding 2
                                    text (u'{color=#CD4F39}%s'%trait) size 15 align .5, .5

                        # Effects:
                        if item.addeffects or item.removeeffects:
                            null height 5
                            hbox:
                                xalign .5
                                if item.addeffects:
                                    add "content/gfx/interface/images/add.png" yalign .5
                                if item.removeeffects:
                                    add "content/gfx/interface/images/remove.png"  yalign .5 yoffset -2
                                null width 4
                                label ('Effects:') text_size 14 text_color gold xoffset 7

                            for effect in item.addeffects:
                                frame:
                                    xalign .1
                                    xpadding 2
                                    text (u'{color=#43CD80}%s'%effect) size 15 align .5, .5
                            for effect in item.removeeffects:
                                frame:
                                    xalign 0.9
                                    xpadding 2
                                    text (u'{color=#CD4F39}%s'%effect) size 15 align .5, .5

                frame:
                    xysize 382, 104
                    padding 10, 5
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.9)
                    has viewport draggable True mousewheel True
                    text '[item.desc]' font "fonts/TisaOTM.otf" size 15 color "#ecc88a" outlines [(1, "#3a3a3a", 0, 0)]

                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                    xysize 158, 104
                    padding 2, 3
                    has viewport draggable True mousewheel True
                    vbox:
                        xsize 150
                        style_group "proper_stats"
                        if item.add_be_spells or item.remove_be_spells:
                            hbox:
                                xalign .5
                                if item.add_be_spells:
                                    add "content/gfx/interface/images/add.png" yalign .5
                                if item.remove_be_spells:
                                    add "content/gfx/interface/images/remove.png" yalign .5 yoffset -2
                                null width 4
                                label ('Skills:') text_size 14 text_color gold xoffset 7

                            for skill in item.add_be_spells:
                                frame:
                                    xalign .1
                                    xpadding 2
                                    text (u'{color=#43CD80}%s'%skill) size 15 align .5, .5
                            for skill in item.remove_be_spells:
                                frame:
                                    xalign 0.9
                                    xpadding 2
                                    text (u'{color=#CD4F39}%s'%skill) size 15 align .5, .5

    elif not isinstance(eqtarget, PytGroup): # equipment saves
        frame:
            style_prefix "proper_stats"
            background Null()
            left_padding 66
            hbox:
                for i in range(0, 3):
                    vbox:
                        frame:
                            xpadding -50
                            background Null()
                            hbox:
                                button:
                                    xysize (90, 30)
                                    action SelectedIf(eqsave[i] and any(eqtarget.eqsave[i].values())), ToggleDict(eqsave, i), With(dissolve)
                                    hovered tt.Action("Save [eqtarget.nickname]'s equipment state")
                                    text "Outfit %d" % (i + 1) style "pb_button_text"
                                button:
                                    align (0.5, 0.5)
                                    xysize (30, 30)
                                    action Function(eqtarget.eqsave.__setitem__, i, eqtarget.eqslots.copy()), SetDict(eqsave, i, True), With(dissolve)
                                    text u"\u2193"
                                    padding (9, 1)
                                    if tt:
                                        hovered tt.Action("Save equipment state")
                                if any(eqtarget.eqsave[i].values()):
                                    button:
                                        align (0.5, 0.5)
                                        xysize (30, 30)
                                        action Function(eqtarget.load_equip, eqtarget.eqsave[i]), With(dissolve)
                                        text u"\u2191"
                                        padding (9, 1)
                                        if tt:
                                            hovered tt.Action("Load equipment state")
                                    button:
                                        align (0.5, 0.5)
                                        xysize (30, 30)
                                        action Function(eqtarget.eqsave.__setitem__, i, {k: False for k in eqtarget.eqslots}), SetDict(eqsave, i, False), With(dissolve)
                                        text u"\u00D7"
                                        padding (8, 1)
                                        if tt:
                                            hovered tt.Action("Discard equipment state")
                        frame:
                            xysize (234, 246)
                            background Null()
                            if eqsave[i] and any(eqtarget.eqsave[i].values()):
                                use eqdoll(active_mode=True, char=eqtarget.eqsave[i], scr_align=(0.98, 1.0), return_value=['item', "save"], txt_size=17, fx_size=(304, 266))

screen diff_item_effects(char, dummy):
    zorder 10
    textbutton "X":
        align (1.0, 0.0)
        action Hide("diff_item_effects")
    frame:
        xysize (1000, 500)
        background Solid("#F00", alpha=0.1)
        align (0.1, 0.5)
        has hbox

        vbox:
            text "Stats:"
            for stat in char.stats:
                text "[stat]: {}".format(getattr(dummy, stat) - getattr(char, stat))
        vbox:
            text "Max Stats:"
            for stat in char.stats:
                text "[stat]: {}".format(dummy.get_max(stat) - char.get_max(stat))
        vbox:
            for skill in char.stats.skills:
                text "[skill]: {}".format(dummy.get_skill(skill) - char.get_skill(skill))
        vbox:
            text "Traits (any):"
            python:
                t_old = set(t.id for t in char.traits)
                t_new = set(t.id for t in dummy.traits)
                temp = t_new.difference(t_old)
                temp = sorted(list(temp))
            for t in temp:
                text "[t]"
