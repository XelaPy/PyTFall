screen pyp_traits():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        label "Traits Info" align .5, .025 text_size 30

        vbox:
            spacing 8
            align .1, .5
            text "The character is defined by his or her traits. Some of the traits are mandatory, like body type. Some of them are optional, like Smart. Traits can affect many things: stats and skills, combat efficiency, random events, and dialogues. \n\n A number of traits can be obtained or removed, permanently or temporally, by using or equipping a particular item. Others can be obtained only during character creation, and stay forever."
        # Screen Content goes here!

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_classes():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            spacing 8
            align .1, .5

            label "Classes" text_size 25
            hbox:
                spacing 2
                viewport:
                    draggable 1
                    mousewheel 1
                    scrollbars "vertical"
                    xysize 674, 420
                    has vbox spacing 8

                    text "Technically close to traits, Classes are characters talents and occupations. They define the jobs character can and willing to do. They always give certain bonuses to stats and skills useful for the corresponding jobs. \n\n At the moment Class cannot be changed after character creation. It's possible to have two Classes, in which case each of the classes gives only a half of its bonuses. \n\n"
                    vbox:
                        label "Prostitute and Stripper"
                        text "The base classes for your brothels. Strippers may be more reluctant when asked for sex, but not much."
                    vbox:
                        label "Cleaner"
                        text "Keeps your buildings clean. All types of businesses generate dirt, and high dirt discourages customers from visiting your buildings."
                    vbox:
                        label "Barmaid"
                        text "Serves drinks and food in a bar, if you have any."
                    vbox:
                        label "Maid"
                        text "A universal service class who can perform many tasks with high efficiency, but also requires much more training. Capable of replacing Cleaners and Barmaids."
                    vbox:
                        label "Manager"
                        text "Helps other workers to perform their duties better, resolves conflicts with customers and in general improves the efficiency of your businesses. Each building can have only one Manager. Free characters only."
                    vbox:
                        label "Mage"
                        text "A combat class focused on magic. Can work as a guard in your buildings. Free characters only."
                    vbox:
                        label "Healer"
                        text "A combat class focused on magic, with less damage output but much more effective healing spells. Can work as a guard in your buildings. Free characters only."
                    vbox:
                        label "Warrior"
                        text "A combat class focused on melee fights. Can work as a guard in your buildings. Free characters only."
                    vbox:
                        label "Knight"
                        text "A combat class focused on melee fights. Has relatively weak attack, but great defence. Can work as a guard in your buildings. Free characters only."
                    vbox:
                        label "Shooter"
                        text "A combat class focused on ranged fights. Can fight in melee combat too, but not for long as defence is not high enough for that. Can work as a guard in your buildings. Free characters only."
                    vbox:
                        label "Assassin"
                        text "A combat class focused on high damage output, critical hits, and evasion. Has low defence. Can work as a guard in your buildings. Free characters only."
                frame:
                    yalign .5
                    background Frame("content/gfx/frame/mes11.webp", 10, 10)
                    padding 6, 6
                    add "content/gfx/interface/pyp/core_traits.webp"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_fixed_traits():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"
        vbox:
            spacing 8
            align .1, .5
            label "Fixed Traits" text_size 25
            text "Some traits are mandatory. They define the core characteristics, and cannot be changed after the character creation. \n\n All fixed traits provide lots of bonuses and penalties of different kind, so they are very important for defying a character."
            hbox:
                spacing 2
                viewport:
                    draggable 1
                    mousewheel 1
                    scrollbars "vertical"
                    xysize 674, 420
                    has vbox spacing 8


                    vbox:
                        label "Class"
                        text "Every character should have one or two classes. For more information, see Classes section."
                    vbox:
                        label "Personality (female only at the moment)"
                        text "Defines character personality, profoundly affects all dialogues and decides what the character likes and dislikes in general. The used personalities are based on a number of Japanese archetypes, such as Tsundere, Kuudere, etc. The list of races can be found in content/db/traits/traits_personality.json file in the game folders. Personalities have big icons in the top left corner of the character profiles."
                    vbox:
                        label "Body type (female only at the moment)"
                        text "General body constitution. While in real life one can change it by visiting a gym or overeating fast-food, we are limited by pictures base. Therefore body type is set in stone. Can be Lolita, Slim, Chubby, Athletic."
                    vbox:
                        label "Boobs size (female only of course)"
                        text "The size of character boobs, something significant in a brothel or strip club. Can be Abnormally Large, Big, Average and Small."
                    vbox:
                        label "Race"
                        text "Used in the fantasy meaning of the word, such as Elf, Undead, Android, etc. Sometimes provides many unique effects. Each race has a corresponding icon. The list of races can be found in content/db/traits/traits_races.json file in the game folders."
                vbox:
                    frame:
                        yalign .5
                        background Frame("content/gfx/frame/mes11.webp", 10, 10)
                        padding 6, 6
                        add "content/gfx/interface/pyp/fixed_traits.webp"
                    null height 10
                    frame:
                        yalign .5
                        background Frame("content/gfx/frame/mes11.webp", 10, 10)
                        padding 6, 6
                        add "content/gfx/interface/pyp/pers_traits.webp"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_elements():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"
        vbox:
            spacing 8
            align .1, .5
            label "Elements" text_size 25
            text "Elemental traits define the attack and defence in combat in relation to different elements. One character can be weak to fire spells and attacks but strong against Ice ones. A mage could use Darkness spells effectively but suck at Water magic. \n\n There are two kinds of elemental traits, base, and general. Note that not only spells, but also many attacks have elemental components, so it's important not only for mages."
            hbox:
                spacing 2
                viewport:
                    draggable 1
                    mousewheel 1
                    scrollbars "vertical"
                    xysize 674, 420
                    has vbox spacing 8


                    vbox:
                        label "Base Elemental Traits"
                        text "The base elemental traits are elements themselves. The full list is: Fire, Water, Air, Earth, Electricity, Ice, Light, Darkness. Each of them buffs some elemental attacks and defences and reduces others, for instance, Fire gives +25% to fire damage and 15% to fire and air defences, but reduces ice spells damage by 25% and lowers water defence by 30%. One character can even have all elements at once, but since they all have pros and cons it's very unwise, as it gives no positive effect. Instead, it's better to focus on a few elements."
                    vbox:
                        label "General Elemental Traits"
                        text "Unlike base elemental traits, general traits may not present at all, or be temporally, but they affect elements in one way or another: Immunity traits protect against element completely, Absorption traits not only protect but also restore character health if attacked by the corresponding element. Others provide bonuses to attack or defence of a specific element. Some of these traits can be obtained by equipping an item, others available only during character creation. Some can only be used by monsters."
                    vbox:
                        label "Neutral Element"
                        text "When a character has no base elemental traits, he/she automatically gets a Neutral trait. It provides a solid defence against most elements, but gives significant penalties to the elemental damage. Making it a good choice only for characters who don't rely on elemental damage of any kind."
                    vbox:
                        label "Changing your element"
                        text "While it's possible to set up base elements during character creation, they can be added or removed mid-game. Without spoiling too much, try to visit the Mages Tower once your level is high enough."
                    vbox:
                        label "Sources of Damage"
                        text "While each element has its own source of damage used in combat, not all sources of damage have their base elements. The remaining sources are Healing, Physical and Poison (could be more in the future). However, there are general elemental traits that affect them, for example, protect from physical damage or make immune to healing spells (the latter is mostly used by undead monsters)."
                vbox:
                    frame:
                        yalign .5
                        background Frame("content/gfx/frame/mes11.webp", 10, 10)
                        padding 6, 6
                        add "content/gfx/interface/pyp/neu_el.webp"
                    null height 10
                    frame:
                        yalign .5
                        background Frame("content/gfx/frame/mes11.webp", 10, 10)
                        padding 6, 6
                        add "content/gfx/interface/pyp/multi_el.webp"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_effects():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            spacing 8
            align .1, .5
            label "Effects" text_size 25
            text "Effects are unique conditions with special logic. Some of them accompany a particular trait, others are independent. The difference between trait and effect is that trait can do a limited number of things (like change max stat), while effect can do pretty much anything and even require special conditions of obtaining and removing it. The list of existing effects is below. Most of them are female-only at the moment."

            viewport:
                draggable 1
                mousewheel 1
                scrollbars "vertical"
                xysize 974, 420
                has vbox spacing 8

                vbox:
                    label "Poisoned"
                    text "Health decreases over time until the effect is removed by a potion."
                vbox:
                    label "Slow Learner/Fast Learner"
                    text "Tied to certain traits, -10%/+10% to experience."
                vbox:
                    label "Introvert/Extrovert"
                    text "Tied to certain personality traits. Harder/easier to increase and decrease disposition."
                vbox:
                    label "Insecure"
                    text "Tied to certain personality trait. Significant changes in disposition also affect joy."
                vbox:
                    label "Sibling"
                    text "Tied to a certain trait. If the disposition is low enough, it gradually increases over time."
                vbox:
                    label "Assertive/Diffident"
                    text "Tied to a certain personality traits. If a character stat is high/low enough, it slowly decreases/increases over time."
                vbox:
                    label "Food Poisoning"
                    text "Intemperance in eating or low-quality food often lead to problems. Reduces health, vitality, and joy every day, cannot consume any more food."
                vbox:
                    label "Down with Cold"
                    text "Causes weakness and aches, will be held in a week or two. Has a great impact on vitality and health."
                vbox:
                    label "Unstable"
                    text "Tied to certain personality traits. From time to time joy randomly changes."
                vbox:
                    label "Optimist/Pessimist"
                    text "Tied to certain traits. Joy increases/decreases over time."
                vbox:
                    label "Composure"
                    text "Tied to certain traits. Over time joy decreases if it's too high and increases if it's too low."
                vbox:
                    label "Kleptomaniac"
                    text "Tied to a certain trait. Randomly increases character gold."
                vbox:
                    label "Drowsy"
                    text "Tied to a certain trait. Rest restores more vitality than usual if unspent APs left."
                vbox:
                    label "Loyal"
                    text "Tied to a certain trait. Harder to decrease disposition."
                vbox:
                    label "Lactation"
                    text "Tied to a certain trait. Girl's breasts produce milk. If she's your slave or lover, you will get a free sample every day."
                vbox:
                    label "Vigorous"
                    text "Tied to a certain trait. If vitality is too low, it slowly increases over time."
                vbox:
                    label "Silly/Intelligent"
                    text "Tied to certain traits.  Intelligence decreases/increases over time."
                vbox:
                    label "Fast Metabolism"
                    text "Tied to certain traits. Any food is more effective than usual, giving more bonuses."
                vbox:
                    label "Drunk"
                    text "Appears after too much alcohol was consumed. -1AP for every next drink."
                vbox:
                    label "Depression"
                    text "Appears if joy is too low for some time. -1AP."
                vbox:
                    label "Elation"
                    text "Appears if joy is maxed out for some time. 10% chance of +1AP at the beginning of the day."
                vbox:
                    label "Drinker"
                    text "Tied to a certain trait. Neutralizes the AP penalty of Drunk effect."
                vbox:
                    label "Injured"
                    text "Appears if too much damage was inflicted in battle. Gives heavy penalties until healed."
                vbox:
                    label "Exhausted"
                    text "Appears if character has low vitality for some time. Gives penalties until proper rest."
                vbox:
                    label "Impressible/Calm"
                    text "Tied to certain traits. Easier/harder to decrease and increase joy."
                vbox:
                    label "Regeneration"
                    text "Restores some health every day."
                vbox:
                    label "MP Regeneration"
                    text "Restores some mp every day."
                vbox:
                    label "Blood Connection"
                    text "Disposition increases and character decreases every day. Appears after character gave her virginity to Main Hero in case if he has a certain trait."
                vbox:
                    label "Horny"
                    text "Character is in the mood for sex. Increases the chance of success for sex interactions, provides bonuses and penalties for some jobs. Appears randomly deepening on character traits."
                vbox:
                    label "Chastity"
                    text "Special enchantment preserves virginity intact. Can be obtained by equipping a certain item."
                vbox:
                    label "Revealing Clothes"
                    text "Can be obtained by equipping some items. Provides bonuses and penalties for some jobs."
                vbox:
                    label "Fluffy Companion"
                    text "Main Hero only. Helps to increase disposition during interactions. Can be obtained by equipping a unique item obtained in a quest."
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
