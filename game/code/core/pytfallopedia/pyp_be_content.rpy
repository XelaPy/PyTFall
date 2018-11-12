screen pyp_battle_engine():
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
                text "Combat System" size 30

            vbox:
                ypos 80
                text ("The game uses a classic turn-based combat system. Two teams exchange"+
                      " hits until only one is left. A team can have from one to three characters.")
                null height 5
                text ("Slaves have a special place in the combat. The laws of the city forbid them to fight,"+
                      " so while they can be taken into battle, they cannot attack anyone nor use spells.")
                null height 5
                text ("All attacks and spells have one or more elements. The enemy may be valuable to certain"+
                      " elements and resistant to others. Some enemies health is restored as they are capable of absorbing elemental bonus!")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/combat_1.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_teams():
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
                text "Teams" size 30

            vbox:
                ypos 80
                text "You can add characters to hero team by pressing a button in their profiles. The same button removes them from the team."
                null height 5
                text "The team cannot have more than 3 members, meaning the Hero and two girls."
                null height 5
                text "In the Hero profile you can use the team screen to rename your team, exclude girls from it or quickly access their profiles."


        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/team1.webp", 350, 1000)

        fixed:
            xpos 601
            ypos 250
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/team2.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
    
screen pyp_attacks():
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
                text "Attacks" size 30

            vbox:
                ypos 80
                text ("Each character has one (sometimes more) basic attack when unarmed. Other"+
                      " than that, the primary way to get more attacks is to equip a weapon. "+
                      "Each weapon has its own set of attacks, usually unique. The attacks "+
                      "will be available as long as the weapon is equipped. However, the "+
                      "default unarmed attack becomes unavailable if you have a weapon in hand.")
                null height 5
                text ("In battle, you can pick one of the available attacks. The tooltip "+
                      "shows some base info about the attack, such as involved elements or cost of the attack.")
                null height 5
                text ("Each skill has its cost. It can be Health, MP, Vitality and"+
                      " their combinations. Powerful abilities use relative values,"+
                      " like 20% of max MP. Naturally, you can't use a skill"+
                      " if you can't cover its cost.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/combat_2.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_magic():
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
                text "Magic" size 30

            vbox:
                ypos 80
                text ("Unlike attacks, spells can be learned by reading scrolls, and they stay"+
                      " in characters arsenal forever. You can buy scrolls in shops or find them."+
                      " Spells tend to use mostly MP. However, there are a few exceptions.")
                null height 5
                text ("In battle, you can pick one of the available spells sorted by their"+
                      " elements. The tooltip shows some base info about the spell,"+
                      " just like for attacks.")
                null height 5
                text ("Unlike attacks, not all spells are offensive. There are healing spells, "+
                      "resurrection spell and a few buffing spells. However, for"+
                      " now, they can be used only in battle.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 80
                spacing 20
                frame:
                    add pscale("content/gfx/interface/pyp/magic1.webp", 350, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/magic0.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"


screen pyp_be_items():
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
                text ("A few items can be used in combat to restore Health, MP, and Vitality."+
                      " Only items from the character inventory can be used, but they can be used on any character.")
                null height 5
                text "The tooltip shows item effects when you hover the cursor over them."
                null height 5
                text "During some fights, you won't be able to use items, for example, arena rules forbid it."

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/combat_4.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_escape():
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
                text "Escape and Surrender" size 30

            vbox:
                ypos 80
                text ("If your fight doesn't go well, you can escape it. The escape is "+
                     "always successful, but it counts as losing regarding rewards. "+
                     "During arena fights and duels, it's replaced by surrender, but it has the same function.")
                null height 5
                text "Not all conflicts allow to escape or surrender, but it happens very rarely."
                null height 5
                text ("In most cases losing in battle doesn't lead to  the game over, "+
                      "but there are a few exceptions when characters killed in action die for"+
                      " real. Losing such battles leads to Game Over. In other cases, "+
                      "characters remain alive with 1 Health left.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 10
                spacing 20
                frame:
                    add pscale("content/gfx/interface/pyp/combat_5.webp", 350, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/combat_6.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
