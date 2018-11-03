screen pyp_characters():
    # main chars screen.
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        label "Characters Info" align .5, .025 text_size 30

        vbox:
            spacing 8
            align .1, .5
            label "Character types:" text_size 25
            vbox:
                label "Unique Characters"
                text "Only one is allowed in the game, at he moment they are all female. Full range of interactions is available with them."
            vbox:
                label "Random Characters"
                text "Used to populate the city, any number of the same character type is permitted. Full range of interactions is available with them. All Female at the moment."
            vbox:
                label "Non-Playable Characters"
                text "They are the shop owners and other personalities that you will find in the city. They cannot be hired. Male and Female."
            vbox:
                label "Arena Fighters"
                text "Male and Female characters that populate the Arena. MC's avatar is drawn from one of the males, which is later excluded. They normally have a very limited picture database."
            vbox:
                label "Arena Fighter"
                text "Male and Female characters that populate the Arena. MC's avatar is drawn from one of the males, which is later excluded."
            vbox:
                label "Mobs"
                text "People and Monsters you fights against."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_stats():
    # main chars screen.
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            ypos 20
            label "Stats Info" text_size 30 xalign .5
            text ("Stats are used in Jobs, Actions and Events. They have a maximum value that is usually recalculated on each level-up."+
                  " Low-level character use a different manner to calculate maximum than the high(er) level ones, which means that powerful items that modify stat maximums will provide "+
                  "more power effects. Minimums for all stats are fixed, there are however some stats that also have a fixed maximum value (such as 'disposition') that never changes.")

        vbox:
            spacing 8
            ypos 190
            label "Stats:" text_size 25
            hbox:
                spacing 2
                viewport:
                    draggable 1
                    mousewheel 1
                    scrollbars "vertical"
                    xysize 674, 420
                    has vbox spacing 8
                    vbox:
                        label "Disposition"
                        text "Decided how much a character likes the player. Range is fixed with a minimum of -1000 and a maximum of 1000. Characters with low disposition may leave you. Positive interactions and gifts increase it."
                    vbox:
                        label "Character"
                        text "Reversed Obedience. Higher Character means that greater penalties for forcing any undesirable action and a character will generally not accept any task they are not expected to perform. Useful for jobs like Barmaid."
                    vbox:
                        label "Vitality"
                        text "Fixed ranged that depends on traits. Most actions and jobs decrease it, and resting increases. When vitality runs low, a character will need a couple days rest to do any meaningful actions."
                    vbox:
                        label "Constitution"
                        text "Affects the number of actions a character is allowed to preform each day. In combat protects against melee and status attacks. Useful for jobs requiring endurance, such as Cleaner."
                    vbox:
                        label "Luck"
                        text "Important stat that influences events and rewards. Used along with other modifiers to roll Critical Damage in combat. Range is fixed between -50 and 50."
                    vbox:
                        label "Joy"
                        text "High joy gives additional bonuses, while low brings penalties and may force the character to leave you. If you don't pay enough to your workers or harass them too much, it will decrease. Positive interactions and gifts increase it."
                    vbox:
                        label "Charisma"
                        text "Useful for jobs where appearance is the most important thing, such as stripper."
                    vbox:
                        label "Intelligence"
                        text "Useful for jobs where intelligence is important, such as manager. Affects magical attack and defense, protects against status attacks."
                    vbox:
                        label "Agility"
                        text "Affects evasion chance and damage from melee and status attacks in combat. Protects against ranged attacks. Useful for jobs that require some promptness, like waitress."
                    vbox:
                        label "Health"
                        text "Low health prevents most actions. Some events may decrease it. In combat situation zero health leads to K.O., and in some cases to death."
                    vbox:
                        label "MP"
                        text "Also known as magic points. Required for casting most spells and using some of the weapons skills."
                    vbox:
                        label "Attack"
                        text "Affects damage for melee and ranged attacks. Useful for jobs like Guard."
                    vbox:
                        label "Defence"
                        text "Protects from all types of damage, to some point. Useful for jobs like Guard."
                    vbox:
                        label "Upkeep"
                        text "How much gold the character requires per day for her basic needs."

                frame:
                    yalign .5
                    background Frame("content/gfx/frame/mes11.webp", 10, 10)
                    padding 6, 6
                    add "content/gfx/interface/pyp/stats.webp"

    add "content/gfx/frame/h3.png"

screen pyp_skills():
    # main chars screen.
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            ypos 20
            label "Skills Info" text_size 30 xalign .5
            text ("Skills are used mostly in Jobs, but also in some Actions and Events. Their levels are depicted as Stars and "+
                  " not shown if their value is too low to be of significant. The maximum value is 5 starts but that maximum value is "+
                  "recalculated every time a character's Tier is increased (so stars might be lost in such a case as value remains the same)."+
                  " Skills are also governed by a completely different mechanics than stats, they are made of two parts: Action and Knowledge. The best ratio between"+
                  " action and knowledge is 3:1, exact information of this ratio however is obfuscated from player. If one of the parts lags, skill will rise slower but it will be compensated if "+
                  "the character works on increasing the other at later time.")

        vbox:
            spacing 8
            ypos 220
            label "Skills:" text_size 25
            hbox:
                spacing 2
                viewport:
                    draggable 1
                    mousewheel 1
                    scrollbars "vertical"
                    xysize 682, 396
                    has vbox spacing 8
                    vbox:
                        label "MC Skills"
                        text "Some skills such as 'fishing' or 'swimming' are only useful to the Player as they are used for actions in the City. They are governed by the same rules as any other skill."
                    vbox:
                        label "Other"
                        text "The rest of the skills are very straight forward and player can usually tell what they are used for and will know if the skill level fits the tier by the number of Stars."

                frame:
                    yalign .5
                    background Frame("content/gfx/frame/mes11.webp", 10, 10)
                    padding 6, 6
                    add "content/gfx/interface/pyp/skills.webp"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"
