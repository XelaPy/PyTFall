screen pyp_items():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            add "content/gfx/interface/pyp/items_1.webp" align .5, .05
            label "Items"
            text "There are many hundreds items in the game. Some of them can be bought, some found or won as a prize in arena fights."
            null height 5
            text "Some items can be equipped of characters to give them certain bonuses. Equipping items does not change characters appearance. Other items can be consumed. Finally, there are items that can't used directly, but only sold or used as materials to build something."
            null height 5
            text "You can easily add your own items to the game by providing an icon and editing one of the items json files located in content/db/items."
            
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_consumables():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            frame:
                align .5, .5
                background Frame("content/gfx/frame/mes11.webp", 10, 10)
                padding 6, 6
                add "content/gfx/interface/pyp/items_2.webp"
            label "Consumables"
            text "Consumable items can be used by characters directly. Most of them disappear from inventory after using, but there are a few rare exceptions."
            null height 5
            text "Most consumables give permanent or temporally effects, such as changing stats or skills, or adding or removing traits."
            null height 5
            text "There are a few special subtypes: scrolls teach character a new spell, food and alcohol are cheap but cannot be consumed infinitely without negative effects, and some consumables have unique hardcoded effects."
            null height 5
            text "A number of potions can be used in combat (see combat section for more info)."
            null height 5
            text "Some consumables have a cooldown timer. It means you only can use them once per several days."
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_weapons():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            frame:
                align .5, .5
                background Frame("content/gfx/frame/mes11.webp", 10, 10)
                padding 6, 6
                add "content/gfx/interface/pyp/items_3.webp"
            label "Weapons"
            text "Items for right and left hands slots are considered weapons. Both slots have their own items, ie items for the left hand cannot be used in the right hand."
            null height 5
            text "Usually they provide bonuses to combat stats and unlock unique attacks usable in combat. Slaves cannot equip weapons, but there are items for hands slots that are not considered true weapons, and can be equipped by anyone."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_materials():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            label "Unequipable Items"
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
            text "Some items obtainable from quests can't be discarded, sold, transfered or used."
            null height 5
            
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_equippables():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            frame:
                align .5, .5
                background Frame("content/gfx/frame/mes11.webp", 10, 10)
                padding 6, 6
                add "content/gfx/interface/pyp/items_5.webp"
            text "Not every character can equip or use any item. Some items can only be used/equipped by male or female characters."
            null height 5
            text "Additionally, slaves cannot equip any weapons and armor. Of course they still can wear normal clothes."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_misc():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            add "content/gfx/interface/pyp/items_6.webp" align .5, .05
            label "MISC items"
            text "Misc items have a different mechanics behind them."
            null height 5
            text "Instead of providing effects immediatly after consuming/equipping, they need some time to work."
            null height 5
            text "Some of them work every day, others need a few days to affect the character. A number of them cannot be used by the same character more than once."
            null height 5
            text "Finally, some of them disappear after providing bonuses, but many can be reused infinitely." 
            null height 5
            text "All related info you can find on the equipment screen, in the Frequency section." 
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_stats_bonuses():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            hbox:
                frame:
                    align .5, .5
                    background Frame("content/gfx/frame/mes11.webp", 10, 10)
                    padding 6, 6
                    add "content/gfx/interface/pyp/items_7.webp"
                vbox:
                    frame:
                        align .5, .5
                        background Frame("content/gfx/frame/mes11.webp", 10, 10)
                        padding 6, 6
                        add "content/gfx/interface/pyp/items_8.webp"
                    frame:
                        align .0, .5
                        background Frame("content/gfx/frame/mes11.webp", 10, 10)
                        padding 6, 6
                        add "content/gfx/interface/pyp/items_9.webp"
            label "Items Effects"
            text "When you equip or unequip an item, the equipment screen shows you how stats, traits, effects, etc. will change after that."
            null height 5
            text "In order to see how item affects character skills you should switch to Items SKills mode (see screenshots)."
            null height 5
            text "However, some items have special hidden bonuses (like protection against ranged attacks) that are only reflected in the item description."
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_inventory():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            hbox:
                null width 20
                frame:
                    align .5, .5
                    background Frame("content/gfx/frame/mes11.webp", 10, 10)
                    padding 6, 6
                    add "content/gfx/interface/pyp/items_10.webp"
                null width 30
                frame:
                    align .5, .5
                    background Frame("content/gfx/frame/mes11.webp", 10, 10)
                    padding 6, 6
                    add "content/gfx/interface/pyp/items_15.webp"
            label "Inventory"
            text "The inventory screen is a part of equipment screen."
            null height 5
            text "It allows to filter items by slot, or order them by name/price/etc."
            null height 5
            text "When you inspect inventory of a girl, you can switch between her and your inventory anytime to equip or use items from either one."
            null height 5
            text "Additionally you can discard unneeded items by clicking special button. Some items can't be discarded."
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_shopping():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            add "content/gfx/interface/pyp/items_11.webp" align .5, .05
            label "Shopping"
            text "The game has plenty of shops in different locations. You can buy and sell items there, however not every shop agrees to buy any item from you. They also have different prices for different types of items."
            null height 5
            text "Shopkeepers have limited stock and gold, however they get new items and more gold every few days. Every item you sold to them also increases the gold they get during the next restock."
            null height 5
            text "Some shops focus on weapons and armor, others on potions and so on. Make sure to check them all when you are looking for something!"
            null height 5
            text "Note that some items can't be sold in any shop."
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_auto_equip():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            frame:
                align .5, .5
                background Frame("content/gfx/frame/mes11.webp", 10, 10)
                padding 6, 6
                add "content/gfx/interface/pyp/items_12.webp"
            label "Auto Equipment"
            text "Usually free characters decide what to equip by themselves. You cannot control it until you become lovers. However you can always control equipment for slaves."
            null height 5
            text "But additionally you can use the auto equipment system that orders a character to equip a certain type of items depending on her Class. You can access in on the equipment screen."
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_transfer():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            add "content/gfx/interface/pyp/items_13.webp" align .5, .05
            label "Items Exchange"
            text "You can exchange items between the main character and a girl via equipment screen. But often it's more convenient to use the transfer screen."
            null height 5
            text "You can access it from buildings menu. There you can quickly exchange items directly between girls, even if they are in different buildings."
            null height 5
            text "Note that free characters often do not want to give away their own items, unless you are lovers. However slaves have no choice."
            null height 5
            text "Some special items cannot be given to other chartacter no matter what."
            
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_storage():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            add "content/gfx/interface/pyp/items_14.webp" align .5, .05
            label "Personal Storage"
            text "If the main character owns a living building, he can store his items there. Storage is available from his personal screen."
            null height 5
            text "Each living building has its own storage. You can switch between them by putting the main character into a different building."
            null height 5
            text "Note that inventory of any character is unlimited, so it's just an optional thing to get rid of unneeded items without selling them."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"
