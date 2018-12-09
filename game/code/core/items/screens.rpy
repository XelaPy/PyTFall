screen items_inv(char=None, main_size=(553, 282), frame_size=(90, 90), return_value=['item', 'get']):
    frame:
        background Null()
        xysize main_size
        has hbox box_wrap True
        for item in char.inventory.page_content:
            frame:
                xysize frame_size
                if char.inventory[item]:
                    background Frame("content/gfx/frame/frame_it2.png", -1, -1)
                    use r_lightbutton (img=ProportionalScale(item.icon, 70, 70), return_value=return_value+[item], align=(.5, .5))
                    label (u"{color=#ecc88a}%d" % char.inventory[item]):
                        align (.995, .995)
                        style "stats_label_text"
                        text_size 18
                        text_outlines [(2, "#9c8975", 0, 0), (1, "#000000", 0, 0)]
                else:
                    # in groups indicate some have the item
                    background Frame("content/gfx/frame/frame_it1.png", -1, -1)
                    use r_lightbutton (img=ProportionalScale(im.Sepia(item.icon), 70, 70), return_value=return_value+[item], align=(.5, .5))

screen eqdoll(active_mode=True, char=None, frame_size=[55, 55], scr_align=(.23, .23), return_value=['item', 'get'], txt_size=17, fx_size=(300, 320)):
    # active_mode = Allows equipped item to be focused if true, otherwise just dispayes a picture of an item (when equipped).
    # char = source of equipment slots.
    # Slots and the doll ------------------------------------------------------------>
    if char == hero:
        # add Transform(hero.show("sprofile", resize=(400, 720)), alpha=.8) align(.5, 1.0)
        add im.Scale("content/gfx/interface/images/doll_male.png", 286, 400) align (.5, .5)
    elif not isinstance(char, dict):
        #f rame:
            # align (.5, .5)
            # background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
        add (char.show("vnsprite", resize=(288, 400), cache=True)) alpha .9 align (.5, 1.0)
        # add im.Scale("content/gfx/interface/images/doll_fem.png", 350, 500) align (.25, .23)

    fixed:
        style_group "content"
        align scr_align
        xysize fx_size

        for slot in equipSlotsPositions:
            python:
                is_multiple_pytgroup = False

                if isinstance(char, dict):
                    # saved equipment state
                    equipment = char[slot]

                elif isinstance(char.eqslots[slot], list):

                    is_multiple_pytgroup = True
                    equipment = char.eqslots[slot][0]
                else:
                    equipment = char.eqslots[slot]

                if equipment and active_mode:
                    # Frame background:
                    img = im.Sepia(equipment.icon) if is_multiple_pytgroup else equipment.icon
                    bg = im.Scale("content/gfx/frame/frame_it2.png", *frame_size)
                    equipment = [equipment, slot]
                else:
                    bg = im.Scale(im.Twocolor("content/gfx/frame/frame_it2.png", grey, black), *frame_size)
                    key = "ring" if slot.startswith("ring") else slot
                    img = blank
            frame:
                background bg
                pos (equipSlotsPositions[slot][1]+ (0 if not isinstance(char, dict) or equipSlotsPositions[slot][1] < .5 else -0.619), equipSlotsPositions[slot][2])
                xysize (frame_size[0], frame_size[1])
                if active_mode and equipment:
                    if not isinstance(char, dict):
                        use r_lightbutton(img=ProportionalScale(img, frame_size[0]*.78, frame_size[1]*.78), return_value=return_value+equipment)
                    else:
                        add ProportionalScale(img, frame_size[0]*.71, frame_size[1]*.71) align (.5, .5)
                else:
                    add Transform(ProportionalScale("content/gfx/interface/buttons/filters/%s_bg.png"%key, frame_size[0]*.71, frame_size[1]*.71), alpha=.35) align (.5, .5)

screen shopping(left_ref=None, right_ref=None):
    use shop_inventory(ref=left_ref, x=.0)
    use shop_inventory(ref=right_ref, x=1.0)

    if focus:
        vbox:
            align .5, .5
            frame:
                background Frame("content/gfx/frame/frame_dec_1.png", 30, 30)
                xalign .5
                padding 30, 30
                use itemstats(item=focus, size=(580, 350))

            null height 3

            frame:
                background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                xalign .5
                padding 10, 10

                has vbox ysize 100

                frame:
                    xalign .5
                    style_prefix "proper_stats"
                    $ total_price = item_price * amount
                    padding 3, 3
                    fixed:
                        xysize 250, 25
                        label "Retail Price:" text_color gold text_size 22 xalign .0 yalign .5
                        label "[total_price]" text_color gold text_size 22 xalign 1.0 yalign .5

                fixed:
                    xsize 180
                    xalign .5
                    use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 25, 25), return_value=['control', -10], align=(0, .5))
                    use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 30, 30), return_value=['control', -5], align=(.1, .5))
                    use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_left.png', 40, 40), return_value=['control', -1], align=(.25, .5))
                    text ("{size=36}[amount]") align .5, .5 color ivory style "proper_stats_label_text"
                    use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 40, 40), return_value=['control', 1], align=(.75, .5))
                    use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 30, 30), return_value=['control', 5], align=(.9, .5))
                    use r_lightbutton(img=ProportionalScale('content/gfx/interface/buttons/blue_arrow_right.png', 25, 25), return_value=['control', 10], align=(1.0, .5))

                button:
                    style_prefix "basic"
                    action Return(['item', 'buy/sell'])
                    xsize 100
                    xalign .5
                    if purchasing_dir == "buy":
                        text "Buy"
                    elif purchasing_dir == "sell":
                        text "Sell"

    fixed:
        xoffset -281
        use exit_button

screen itemstats(item=None, size=(635, 380), style_group="content", mc_mode=False):
    if item:
        vbox:
            xysize size
            align .5, .5
            frame:
                xalign .5
                xysize (440, 40)
                background Frame("content/gfx/frame/p_frame7.webp", 10, 10)
                label '[item.id]' text_color gold xalign .5 text_size 20 text_outlines [(1, "#000000", 0, 0)] text_style "interactions_text"

            vbox:
                align .5, .5
                label ('{color=#ecc88a}----------------------------------------') xalign .5
                hbox:
                    xalign .5
                    xfill True
                    frame:
                        xalign .0
                        yalign .5
                        background Frame("content/gfx/frame/frame_it2.png", 5, 5)
                        xysize (130, 130)
                        add (ProportionalScale(item.icon, 110, 110)) align .5, .5
                    frame:
                        background Frame("content/gfx/frame/p_frame4.png", 10, 10)
                        padding 15, 15
                        align .5, .5
                        style_prefix "proper_stats"
                        has vbox spacing 1
                        frame:
                            xysize 195, 22
                            padding 4, 1
                            text ('Price:') color gold xalign .0 yoffset -1
                            label ('[item.price]') xalign 1.0 text_size 18 text_color gold yoffset -2
                        frame:
                            xysize 195, 22
                            padding 4, 1
                            text ('Slot:') color ivory xalign .0 yoffset -1
                            python:
                                if item.slot in SLOTALIASES:
                                    slot = SLOTALIASES[item.slot]
                                else:
                                    slot = item.slot.capitalize()
                            label ('{size=-3}[slot]') align 1.0, .5
                        frame:
                            xysize 195, 22
                            padding 4, 1
                            text ('Type:') color ivory yalign .5
                            label ('{size=-3}%s'%item.type.capitalize()) xalign 1.0 text_size 18 yoffset -2
                        frame:
                            xysize 195, 22
                            padding 4, 1
                            text ('Sex:') color ivory xalign .0 yoffset -1
                            if item.slot in ["gift", "resources", "loot"]:
                                label "N/A" xalign 1.0 text_size 18 yoffset -2
                            elif item.type == "food" and item.sex == 'unisex':
                                label "N/A" xalign 1.0 text_size 18 yoffset -2
                            elif item.sex == 'male':
                                label ('{color=#FFA54F}%s'%item.sex.capitalize()) xalign 1.0 text_size 18 yoffset -2
                            elif item.sex == 'female':
                                label ('{color=#FFAEB9}%s'%item.sex.capitalize()) xalign 1.0 text_size 18 yoffset -2
                            elif item.sex == 'unisex':
                                label ('%s'%item.sex.capitalize()) xalign 1.0 text_size 18 yoffset -2
                    frame:
                        xalign 1.0
                        xysize (165, 130)
                        background Frame("content/gfx/frame/p_frame7.webp", 5, 5)
                        has viewport mousewheel True draggable True style_group "proper_stats" xysize (165, 122) child_size 160, 500
                        vbox:
                            spacing 1
                            if item.mod:
                                label ('Stats:') text_size 18 text_color gold xpos 10
                                for stat, value in item.mod.items():
                                    frame:
                                        xysize 153, 20
                                        text stat.capitalize() color ivory size 16 align (.02, .5)
                                        label (u'{size=-4}[value]') align (.98, .5)
                                null height 2
                            if item.max:
                                label ('Max:') text_size 18 text_color gold xpos 10
                                for stat, value in item.max.items():
                                    frame:
                                        xysize 153, 20
                                        text stat.capitalize() color ivory size 16 align (.02, .5)
                                        label u'{size=-4}[value]' align (.98, .5)
                                null height 2
                            if item.min:
                                label ('Min:') text_size 18 text_color gold xpos 10
                                for stat, value in item.min.items():
                                    frame:
                                        xysize 153, 20
                                        text stat.capitalize() color ivory size 16 align (.02, .5)
                                        label (u'{size=-4}%d'%value) align (.98, .5)
                                null height 2
                            if item.addtraits:
                                label ('Adds Traits:') text_size 16 text_color gold xpos 10
                                for trait in item.addtraits:
                                    frame:
                                        xysize 153, 20
                                        text(u'%s'%trait.capitalize()) color ivory size 16 align (.5, .5)
                                null height 2
                            if item.removetraits:
                                label ('Removes Traits:') text_size 16 text_color gold xpos 10
                                for trait in item.removetraits:
                                    frame:
                                        xysize 153, 20
                                        text(u'%s'%trait.capitalize()) color ivory size 16 align (.5, .5)
                                null height 2
                            if item.add_be_spells:
                                label ('Adds Skills:') text_size 16 text_color gold xpos 10
                                for skill in item.add_be_spells:
                                    frame:
                                        xysize 153, 20
                                        text(u'%s'%skill.capitalize()) color ivory size 16 align (.5, .5)
                                null height 2
                            if item.remove_be_spells:
                                label ('Removes Skills:') text_size 16 text_color gold xpos 10
                                for skill in item.remove_be_spells:
                                    frame:
                                        xysize 153, 20
                                        text (u'%s'%skill.capitalize()) color ivory size 16 align (.5, .5)
                                null height 2
                            if item.addeffects:
                                label ('Adds Effects:') text_size 16 text_color gold xpos 10
                                for effect in item.addeffects:
                                    frame:
                                        xysize 153, 20
                                        text(u'%s'%effect.capitalize()) color ivory size 16 align (.5, .5)
                                null height 2
                            if item.removeeffects:
                                label ('Removes Effects:') text_size 16 text_color gold xpos 10
                                for effect in item.removeeffects:
                                    frame:
                                        xysize 153, 20
                                        text(u'%s'%effect.capitalize()) color ivory size 16 align (.5, .5)
                            if hasattr(item, 'mtemp'):
                                if item.mtemp:
                                    label ('Frequency:') text_size 18 text_color gold xpos 10
                                    frame:
                                        xysize 153, 20
                                        if item.mreusable:
                                            if item.mtemp > 1:
                                                text "Every [item.mtemp] days" color ivory size 16 align (.02, .5)
                                            else:
                                                text "Every day" color ivory size 16 align (.02, .5)
                                        else:
                                            if item.mtemp > 1:
                                                text "After [item.mtemp] days" color ivory size 16 align (.02, .5)
                                            else:
                                                text "After one day" color ivory size 16 align (.02, .5)
                                    if hasattr(item, 'mdestruct'):
                                        if item.mdestruct:
                                            frame:
                                                xysize 153, 20
                                                text "Disposable" color ivory size 16 align (.02, .5)
                                    if hasattr(item, 'mreusable'):
                                        if item.mreusable:
                                            frame:
                                                xysize 153, 20
                                                text "Reusable" color ivory size 16 align (.02, .5)
                                    if hasattr(item, 'statmax'):
                                        if item.statmax:
                                            frame:
                                                xysize 153, 20
                                                text "Stat limit" color ivory size 16 align (.02, .5)
                                                label (u'{size=-4}%d'%item.statmax) align (.98, .5)
                            if hasattr(item, 'ctemp'):
                                if item.ctemp:
                                    label ('Duration:') text_size 18 text_color gold xpos 10
                                    frame:
                                        xysize 153, 20
                                        text "Days" color ivory size 16 align (.02, .5)
                                        label u'{size=-4}[item.ctemp]' align (.98, .5)
                label ('{color=#ecc88a}----------------------------------------') xalign .5
                frame:
                    xalign .5
                    background Frame("content/gfx/frame/p_frame7.webp", 10, 10)
                    has viewport mousewheel True xysize (460, 100)
                    text '[item.desc]' style "TisaOTM" size 16 color gold

# Inventory paging
screen paging(path="content/gfx/interface/buttons/", use_filter=True,
              ref=None, xysize=(270, 60),
              root=None, align=(.5, .0)):
    frame:
        background Frame("content/gfx/frame/BG_choicebuttons_flat.png", 10, 10, yoffset=5)
        xysize xysize
        align align
        style_group "content"

        vbox:
            align .5, .5
            null height 10
            # Filter
            if use_filter:
                hbox:
                    xmaximum xysize[0] - 15
                    xfill True
                    xalign .5
                    $ img = "".join([path, 'prev.png'])
                    imagebutton:
                        align .0, .5
                        idle img
                        hover im.MatrixColor(img, im.matrix.brightness(.15))
                        action Function(ref.apply_filter, "prev")

                    python:
                        if ref.slot_filter in SLOTALIASES:
                            slot = SLOTALIASES[ref.slot_filter]
                        else:
                            slot = ref.slot_filter.capitalize()
                    label "[slot] " align .5, .5  text_color ivory

                    imagebutton:
                        align 1.0, .5
                        idle path+'next.png'
                        hover im.MatrixColor(path+'next.png', im.matrix.brightness(.15))
                        action Function(ref.apply_filter, "next")
            # Listing
            hbox:
                align .5, .5
                xmaximum xysize[0] - 5
                xfill True
                hbox:
                    align (.0, .5)
                    imagebutton:
                        yalign .5
                        idle (path+'first.png')
                        hover (im.MatrixColor(path+'first.png', im.matrix.brightness(.15)))
                        action Function(ref.first)
                    imagebutton:
                        yalign .5
                        idle (path+'prev.png')
                        hover (im.MatrixColor(path+'prev.png', im.matrix.brightness(.15)))
                        action Function(ref.prev)
                label ("%d - %d"%(ref.page+1, ref.max_page)) align (.5, .5) text_color ivory
                hbox:
                    align (1.0, .5)
                    imagebutton:
                        yalign .5
                        idle (path+'next.png')
                        hover (im.MatrixColor(path+'next.png', im.matrix.brightness(.15)))
                        action Function(ref.next)
                    imagebutton:
                        yalign .5
                        idle (path+'last.png')
                        hover (im.MatrixColor(path+'last.png', im.matrix.brightness(.15)))
                        action Function(ref.last)

screen shop_inventory(ref=None, x=.0):
    on "show":
        action SetField(ref.inventory, "filter_index", 0), Function(ref.inventory.apply_filter, "all")

    #key "mousedown_4" action Function(ref.inventory.next)
    #key "mousedown_5" action Function(ref.inventory.prev)

    frame at fade_in_out(t1=.5, t2=.5):
        style_group "content"
        background Frame(Transform("content/gfx/frame/mes11.webp", alpha=.5), 5, 5)
        xalign x
        yfill True
        has vbox
        use paging(ref=ref.inventory, xysize=(260, 90))

        null height 5

        hbox:
            xalign .5
            add im.Scale("content/gfx/interface/icons/gold.png", 25, 25) align (.0, .5)
            null width 10
            $ g = gold_text(ref.gold)
            text g align (.5, 1.0) color gold size 23

        null height 5

        if isinstance(ref, ItemShop):
            label "[ref.name]" text_color ivory xalign .5
        elif isinstance(ref, PytCharacter):
            label "[ref.nickname]" text_color ivory xalign .5
        else:
            label "Inventory" text_color ivory xalign .5

        null height 5

        use items_inv(char=ref, main_size=(268, 522), frame_size=(85, 85), return_value=["item", ref])

# Control loop for shopping?
label shop_control:
    $ result = ui.interact()
    if result[0] == "item":
        if result[1] in (char, shop):
            $ amount = 1
            $ focus = result[2]
            if result[1] == char:
                $ purchasing_dir = 'sell'
                $ item_price = int(focus.price*shop.sell_margin)
            else:
                $ purchasing_dir = 'buy'
                $ item_price = int(focus.price*shop.buy_margin)

        elif result[1] == 'buy/sell':
            if purchasing_dir == 'buy':
                $ result = char.take_money(item_price*amount, "Items")
                if result:
                    play sound "content/sfx/sound/world/purchase_1.ogg"
                    python:
                        for i in xrange(amount):
                            shop.inventory.remove(focus)
                            char.inventory.append(focus)
                            shop.gold += item_price
                            shop.total_items_price -= item_price
                else:
                    $ focus = None
                    $ renpy.say("", choice(["Not enough money.", "No freebees.", "You'll need more money for this purchase"]))
                $ amount = 1
                $ focus = False
            elif purchasing_dir == 'sell':
                if not can_sell(focus, silent=False):
                    jump shop_control
                elif shop != pytfall.general_store and not shop.locations.intersection(focus.locations) and focus.type.lower() not in shop.sells:
                    $ focus = None
                    $ renpy.say("", "This shop doesn't buy such things.")
                else:
                    $ result = bool(shop.gold - (item_price*amount) >= 0)
                    if result:
                        play sound "content/sfx/sound/world/purchase_1.ogg"
                        python:
                            for i in xrange(amount):
                                shop.gold -= item_price
                                char.add_money(item_price, reason="Items")
                                char.inventory.remove(focus)
                                shop.inventory.append(focus)
                                shop.total_items_price += item_price
                    else:
                        $ focus = None
                        $ renpy.say("", "The shop doesn't have enough money.")
                    $ amount = 1
                    $ focus = None

    elif result[0] == 'control':
        if isinstance(result[1], basestring):
            if result[1] == 'return':
                $ focus = None
                return
        elif result[1] > 0:
            if purchasing_dir == 'sell':
                $ amount = min(amount + result[1], char.inventory[focus])
            elif purchasing_dir == 'buy':
                $ amount = min(amount + result[1], shop.inventory[focus])
        else:
            $ amount = max(amount + result[1], 1)
    jump shop_control
