screen pyp_characters():
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
                text "Characters Info" size 30

            vbox:
                spacing 8
                ypos 80
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
                    text ("Male and Female characters that populate the Arena. "+
                          "MC's avatar is drawn from one of the males, which is "+
                          "later excluded. They normally have a very limited picture database.")
                vbox:
                    label "Mobs"
                    text "People and Monsters you fights against."

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            # Images and maybe details:

    add "content/gfx/frame/h3.webp"

screen pyp_tiers():
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
                text "Tiers/Levels" size 30

            text ("Each level-up requires 1000 Experience points. Each tier, in turn,"+
                 " is about 20 levels but tiering up can occur earlier or later than"+
                 " that depending on class relevant stats and skills values relevant to the process.\n\n"+
                 "Tiers are of utmost importance to Jobs, Management, and Actions"+
                 " that Characters can take in the game world.\n\n"+
                 "Every time the Character levels up, his/her class stats and skill are pushed "+
                 "higher and recalculated. Don't be surprised if items that offer max-stat bonuses"+
                 " provided greater bonuses after a level up or if an amount of skill stars drops"+
                 " after a tier up, your skill didn't decrease, it's the level of"+
                 " expected skill from the next tier that is more demanding!"):
                     ypos 80

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 80
                spacing 10
                frame:
                    add pscale("content/gfx/interface/pyp/char_base_info.webp", 350, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/level_mc.webp", 350, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/level_char.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
    
screen pyp_ctrl():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        
        fixed:
            xysize 370, 664
            style_prefix "pyp"
            hbox:
                xpos 40
                frame:
                    add "content/gfx/interface/pyp/ctrl_1.webp"
                null width 20
                frame:
                    add "content/gfx/interface/pyp/ctrl_2.webp"

        text "There are two ways to control characters locations and jobs: from their profiles and from the characters list. Just click on {b}Home{/b}, {b}Work{/b} or {b}Job{/b}. Only in case of slaves you can set up their home locations, free characters have their own homes. In order to set up home locations for slaves from the characters list click right mouse button on the {b}Work{/b}":
              ypos 380

     # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_stats():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"

        text ("Stats are used in Jobs, Actions and Events. They have a maximum value that is usually recalculated on each level-up."+
              " Low-level character use a different manner to calculate maximum than the high(er) level ones, which means that powerful items that modify stat maximums will provide "+
              "more power effects. Minimums for all stats are fixed, there are however some stats that also have a fixed maximum value (such as 'disposition') that never changes."):
              ypos 80

        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Stats Info" size 30

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
                            text "Useful for jobs where appearance is the most important thing, such as stripper. For the Main Character, useful during interactions with girls."
                        vbox:
                            label "Intelligence"
                            text "Useful for jobs where intelligence is important, such as manager. Affects magical attack and defense, protects against status attacks."
                        vbox:
                            label "Agility"
                            text "Affects evasion chance and damage from melee and status attacks in combat. Protects against ranged attacks. Useful for jobs that require some promptness, like waitress. Determines the order of turns in combat."
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

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 300
                add "content/gfx/interface/pyp/stats.webp"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_skills():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        text ("Skills are used mostly in Jobs, but also in some Actions and Events. Their levels are depicted as Stars and "+
              " not shown if their value is too low to be of significant. The maximum value is 5 stars but that maximum value is "+
              "recalculated every time a character's Tier is increased (so stars might be lost in such a case as value remains the same)."+
              " Skills are also governed by a completely different mechanics than stats, they are made of two parts: Action and Knowledge. The best ratio between"+
              " action and knowledge is 3:1, exact information of this ratio however is obfuscated from player. If one of the parts lags, skill will rise slower but it will be compensated if "+
              "the character works on increasing the other at later time."):
                  ypos 80
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Skills Info" size 30

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
                            text ("Some skills such as 'fishing' or 'swimming' are only"+
                                  " useful to the Player as they are used for actions in"+
                                  " the City. They are governed by the same rules as any other skill.")
                        vbox:
                            label "Girls Skills"
                            text ("The girls skills serve as a measure of their capabilities to do the job,"+
                                 " for example cleaning skill for cleaners. You can usually"+
                                 " tell what they are used for and will know if the skill"+
                                 " level fits the tier by the number of Stars.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 300
                add "content/gfx/interface/pyp/skills.webp"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_char_controls():
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
                text "Controls Info" size 30

            text ("Controls allow you to change certain settings of the characters such as wages,"+
                  " tips, battle row and etc. Some options will be blocked depending on"+
                  " status and/or disposition.\n\nPaying more or allowing a character to"+
                  " keep tips will have a very positive effect on Joy and Disposition."):
                      ypos 80

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 10
                spacing 10
                frame:
                    add pscale("content/gfx/interface/pyp/char_controls_0.webp", 350, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/char_controls_1.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_status():
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
                text "Status Info" size 30

            vbox:
                ypos 80
                spacing 20
                text "There are two options for status at this stage: slave and free."

                text ("Slaves are not allowed to partake in Combat or equip heavy weapons"+
                      " due to the slave revolts and all the damage it did to the city. Slaves"+
                      " characters require housing but do not expect to keep tips or to be paid"+
                      " any wages. There are no restrictions on inventory access. "+
                      "A slave can be freed for a fee, talk to Stan at the Slave Market.")

                text ("Free characters will take care of their housing situation. Inventory"+
                      " access will be restricted, but extra options will become available"+
                      " at high disposition or with friend/lover statuses. Free characters"+
                      " also have a monopoly on management and guard positions. "+
                      "Free workers expect wages to be paid to them.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 80
                spacing 10
                frame:
                    add pscale("content/gfx/interface/pyp/status_0.webp", 350, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/status_1.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
