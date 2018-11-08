screen pyp_items():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Items" size 30

            vbox:
                ypos 80
                text ("There are many hundreds of items in the game. They can be bought,"+
                      " found or won as a prize in arena fights.")
                null height 5
                text ("Some items can be equipped to characters to give them certain bonuses."+
                      " Equipping items does not change characters appearance. Other items"+
                      " can be consumed. Finally, some items that can't be used directly, "+
                      "but only sold or used as materials to build something.")
                null height 5
                text ("You can easily add your own items to the game by providing an"+
                      " icon and editing one of the items JSON files located in content/db/items.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/items_1.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_consumables():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Consumables" size 30

            vbox:
                ypos 80
                text ("Consumable items can be used by characters directly. Most of them"+
                      " disappear from inventory after applying, but there are a few rare exceptions.")
                null height 5
                text ("Most consumables give permanent or temporally effects, such"+
                      " as changing stats or skills, or adding or removing traits.")
                null height 5
                text ("There are a few special subtypes: scrolls teach the character a new spell, food"+
                      " and alcohol are cheap but cannot be consumed infinitely without adverse effects,"+
                      " and some consumables have unique hardcoded effects.")
                null height 5
                text "Some potions can be used in combat (see combat section for more info)."
                null height 5
                text "Some consumables have a cooldown timer. It means you only can use them once per several days."

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/items_2.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_weapons():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Weapons" size 30

            vbox:
                ypos 80
                text ("Items for right and left hands slots are considered weapons. Both slots"+
                      " have their own items, i.e. items for the left hand cannot be used in the right hand.")
                null height 5
                text ("Usually they provide bonuses to combat stats and unlock unique attacks usable in combat."+
                      " Slaves cannot equip weapons, but there are items for hands slots that are not considered"+
                      " to be real weapons and can be equipped by anyone.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/items_3.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_materials():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Unequipable Items" size 30

            vbox:
                ypos 80
                text "Some items are stored in inventory, but can't be used or equipped directly."
                null height 10
                label "Materials"
                text "Materials can't be used directly. They are consumed from your inventory automatically when you build an upgrade in one of your buildings."
                null height 5
                label "Gifts"
                text "Gifts can be used during interactions with characters to increase disposition."
                null height 5
                label "Loot"
                text "Loot items can't be used in any way, but you can sell them in a shop for good money."
                null height 5
                label "Quest Items"
                text "Some items obtainable from quests can't be discarded, sold, transferred or used."
                null height 5

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            # Images and maybe details:

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_equippables():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Equippable" size 30

            vbox:
                ypos 80
                text ("Not every character can equip or use any item. Some items can"+
                      " only be used/equipped by male or female characters.")
                null height 5
                text ("Additionally, slaves cannot equip any weapons or armor."+
                      " Of course, they still can wear regular clothes.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/items_5.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_misc():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "MISC items" size 30

            vbox:
                ypos 80
                text "Misc items have a different mechanics behind them."
                null height 5
                text "Instead of providing effects immediately after consuming/equipping, they need some time to work."
                null height 5
                text ("Some of them work every day, others require a few days to affect the character."+
                      " A number of them cannot be used by the same character more than once.")
                null height 5
                text "Finally, some of them disappear after providing bonuses, but many can be reused infinitely."
                null height 5
                text "All related info you can find on the equipment screen, in the Frequency section."

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/items_6.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_stats_bonuses():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Items Effects" size 30

            vbox:
                ypos 80
                text ("When you equip or unequip an item, the equipment screen shows you how"+
                      " stats, traits, effects, etc. will change after that.")
                null height 5
                text ("To see how an item affects character skills you should"+
                      " switch to Items Skills mode (see screenshots).")
                null height 5
                text ("However, some items have special hidden bonuses (like protection"+
                      " against ranged attacks) that are only reflected in the item description.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 80
                spacing 10
                hbox:
                    spacing 2
                    frame:
                        add pscale("content/gfx/interface/pyp/items_7.webp", 160, 1000)
                    frame:
                        add pscale("content/gfx/interface/pyp/items_9.webp", 180, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/items_8.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_inventory():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Inventory" size 30

            vbox:
                ypos 80
                text "The inventory screen is a part of the equipment screen."
                null height 5
                text "It allows to filter items by slot or order them by name/price/etc."
                null height 5
                text ("When you inspect inventory of a girl, you can switch between her"+
                      " and your inventory anytime to equip or use items from either one.")
                null height 5
                text ("Additionally, you can discard unneeded items by clicking a "+
                      "discard button. Some items can't be dropped in the same way.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 80
                spacing 10
                frame:
                    add pscale("content/gfx/interface/pyp/items_10.webp", 200, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/items_15.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_shopping():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Shopping" size 30

            vbox:
                ypos 80
                text ("The game has plenty of shops in different locations. You can buy"+
                      " and sell items there, however not every shop agrees to purchase"+
                      " any item from you. They also have different prices for different types of items.")
                null height 5
                text ("Shopkeepers have limited stock and gold. However, they get"+
                      " new items and more gold every few days. Every item you sold"+
                      " to them also increases the gold they get during the next restock.")
                null height 5
                text ("Some shops focus on weapons and armor, others on potions and so on."+
                      " Make sure to check them all when you are looking for something!")
                null height 5
                text "Note that some items can't be sold in any shop."

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/items_11.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_auto_equip():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Auto Equipment" size 30

            vbox:
                ypos 80
                text ("Usually, free characters decide what to equip by themselves. You cannot"+
                      " control it until you become lovers. However, you can always control equipment for slaves.")
                null height 5
                text ("But additionally, you can use the auto equipment system that"+
                      " orders a character to equip a specific type of items depending"+
                      " on her Class. You can access in on the equipment screen.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/items_12.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_transfer():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Items Exchange" size 30

            vbox:
                ypos 80
                text ("You can exchange items between the main character and a girl via"+
                      " the equipment screen. But often it's more convenient to use the transfer screen.")
                null height 5
                text ("You can access it from buildings menu. There you can quickly exchange"+
                      " items directly between girls, even if they are in different buildings.")
                null height 5
                text ("Note that free characters often do not want to give away their own"+
                      " items, unless you are lovers. However, don't get a say in the matter.")
                null height 5
                text "Some unique items cannot be given to other characters."

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/items_13.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_storage():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Personal Storage" size 30

            vbox:
                ypos 80
                text "If the main character owns a habitable building, he can store his items there. Storage is available from his personal screen."
                null height 5
                text "Each habitable building has its own storage. You can switch between them by putting the main character in different buildings."
                null height 5
                text "Note that inventory of any character is unlimited, so it's just an optional thing to get rid of unneeded items without selling them."

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/items_14.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
