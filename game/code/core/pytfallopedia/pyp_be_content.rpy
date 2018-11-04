screen pyp_battle_engine():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            add "content/gfx/interface/pyp/combat_1.webp" align .5, .05
            label "Combat System"
            text "The game uses a classic turn based combat system. Two teams exchange hits until only one is left. A team can have from one to three characters."
            null height 5
            text "Slaves have a special place in the combat. The laws of the city forbid them to fight, so while they can be taken into combat, they cannot attack anyone nor use spells."
            null height 5
            text "All attacks and spells have one or more elements. The enemy may be valuable to certain elements and resistant to others. Some enemies even restore health if attacked by a certain element, so be careful!"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_attacks():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            add "content/gfx/interface/pyp/combat_2.webp" align .5, .05
            label "Attacks"
            text "Each character has one (sometime more) basic attack when unarmed. Other than that, the main way to get more attacks is to equip a weapon. Each weapon has its own set of attacks, usually unique. The attacks will be available as long as the weapon is equipped. However, the default unarmed attack becomes unavailable if you have a weapon in hand."
            null height 5
            text "In battle you can pick one of the available attacks. The tooltip shows some base info about the attack, such as involved elements or cost of the attack."
            null height 5
            text "Each skill has its cost. It can be Health, MP, Vitality and their combinations. Powerful skills use relative values, like 20% of max MP. Naturally, you can't use a skill if you can't cover its cost."
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_magic():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            add "content/gfx/interface/pyp/combat_3.webp" align .5, .05
            label "Magic"
            text "Unlike attacks, spells can be learned by reading scrolls, and they stay in characters arsenal forever. You can buy scrolls in shops or find them. Spells tend to use mostly MP, however there are a few exceptions."
            null height 5
            text "In battle you can pick one of the available spells sorted by their elements. The tooltip shows some base info about the spell, just like for attacks."
            null height 5
            text "Unlike attacks, not all spells are offensive. There are healing spells, resurrection spell and a few buffing spells. However, for now they can be used only in battle."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_be_items():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            add "content/gfx/interface/pyp/combat_4.webp" align .5, .05
            label "Items"
            text "A few items can be used in combat to restore Health, MP and Vitality. Only items from the character inventory can be used, but they can be used on any character."
            null height 5
            text "The tooltip shows item effects when you hover cursor over them."
            null height 5
            text "During some fights you won't be able to use items, for example arena rules forbid it."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_escape():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            hbox:
                xalign .5
                frame:
                    yalign .5
                    background Frame("content/gfx/frame/mes11.webp", 10, 10)
                    padding 6, 6
                    add "content/gfx/interface/pyp/combat_5.webp"
                null width 100
                frame:
                    yalign .5
                    background Frame("content/gfx/frame/mes11.webp", 10, 10)
                    padding 6, 6
                    add "content/gfx/interface/pyp/combat_6.webp"
            label "Escape and Surrender"
            text "If your fight doesn't go well, you can escape it. The escape is always successful, but it counts as losing in terms of rewards. During arena fights and duels it's replaced by surrender, but it has the same function."
            null height 5
            text "Not all fights allow to escape or surrender, but it happens very rarely."
            null height 5
            text "In most cases losing in battle doesn't lead to game over, but there are a few exceptions when characters killed in battle die for real. Losing such battles leads to game over. In other cases characters remain alive with 1 Health left."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"
