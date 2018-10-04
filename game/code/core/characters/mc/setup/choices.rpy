init:
    python:
        main_story = None # Fathers occupation
        sub_story = None # Father specific occupation
        mc_story = None # MCs mother
        mc_substory = None # MCs heritage

    $ mc_stories = OrderedDict() # Main Dictionary

    python hide: # Main options:
        """
        MC Screens are built from this dictionaries and we expect them to have some values,
        even if those values are just the empty dicts and/or images to be grayed out by the screen.

        OrderedDict() is a variation of dictionary that keeps the order of it's members.
        {} or dict() we use when we don't care about the order.
        """

        mc_stories["Merchant"] = temp = {} # Merchant! This is the main branch displayed as the very first thing (four choices).
        temp["img"] = "content/gfx/interface/images/merchant.png" # Path to the icon representing the branch onscreen.
        temp["choices"] = OrderedDict()

        mc_stories["Warrior"] = temp = {}
        temp["img"] = "content/gfx/interface/images/warriorP.png"
        temp["header"] = "Your father was a skilled fighter..."
        # temp["text"] = "Bla bla bla"
        temp["choices"] = OrderedDict(Warrior="content/gfx/interface/images/mc/warrior_m.png",
                                      Knight="content/gfx/interface/images/mc/defender_m.png",
                                      Shooter="content/gfx/interface/images/mc/shooter_m.png",
                                      Assassin="content/gfx/interface/images/mc/assassin_m.png")

        mc_stories["Mage"] = temp = {}
        temp["img"] = "content/gfx/interface/images/magicP.png"
        temp["header"] = "Arcane Artist"
        temp["text"] = "Your father was a powerful mage."
        temp["text"] += set_font_color("\n+ Mage Class", color="green")
        temp["class"] = "Mage"
        temp["choices"] = OrderedDict()

        mc_stories["Noble"] = temp = {}
        temp["img"] = "content/gfx/interface/images/nobleP.png"
        temp["choices"] = OrderedDict()

    python hide: # Warrior options:
        mc_stories["Warrior"]["Warrior"] = {}
        mc_stories["Warrior"]["Warrior"]["class"] = "Warrior"
        temp = []
        temp.append("He was a famous gladiator. Decades of fighting at the arena made him competent with almost every known weapon and brought fame and wealth.")
        temp.append("{color=[green]}+ Warrior Class{/color}")
        temp.append("{color=[green]}+ Arena Permit{/color}")
        mc_stories["Warrior"]["Warrior"]["text"] = "\n".join(temp)
        mc_stories["Warrior"]["Warrior"]["label"] = "mc_setup_warrior_warrior"

        mc_stories["Warrior"]["Assassin"] = {}
        mc_stories["Warrior"]["Assassin"]["class"] = "Assassin"
        temp = []
        temp.append("He was a deadly assassin. Even royalties, diplomats and nobility would perish at the tip of his blade, for the right price.")
        temp.append("{color=[green]}+ Assassin Class{/color}")
        mc_stories["Warrior"]["Assassin"]["text"] = "\n".join(temp)

        mc_stories["Warrior"]["Shooter"] = {}
        mc_stories["Warrior"]["Shooter"]["class"] = "Shooter"
        temp = []
        temp.append("He was a skilled marksman. For many years together with other rangers, he hunted monsters and smugglers.")
        temp.append("{color=[green]}+ Shooter Class{/color}")
        mc_stories["Warrior"]["Shooter"]["text"] = "\n".join(temp)

        mc_stories["Warrior"]["Knight"] = {}
        mc_stories["Warrior"]["Knight"]["class"] = "Knight"
        temp = []
        temp.append("He was an experienced bodyguard. His skills secured him a place in high society, as he provided his service to the nobility and royalty alike.")
        temp.append("{color=[green]}+ Knight Class{/color}")
        mc_stories["Warrior"]["Knight"]["text"] = "\n".join(temp)

        mc_stories["Warrior"]["MC"] = {}
        for key in mc_stories["Warrior"]["choices"]:
            mc_stories["Warrior"]["MC"][key] = {}
            mc_stories["Warrior"]["MC"][key]["choices"] = OrderedDict()

        mc_stories["Warrior"]["MC"]["Knight"]["choices"] = OrderedDict(l="Royal Guard",
                                                                        l_img="content/gfx/interface/images/mc/knight.jpg",
                                                                        l0="Royal Defender",
                                                                        l0_img="content/gfx/interface/images/mc/crown.png",
                                                                        l1="Left-Handed",
                                                                        l1_img="content/gfx/interface/images/mc/left_hand.png",
                                                                        l2="Shield Master",
                                                                        l2_img="content/gfx/interface/images/mc/shield.png",
                                                                        r="Harpy",
                                                                        r_img="content/gfx/interface/images/mc/harpy.jpg",
                                                                        r0="Hollow Bones",
                                                                        r0_img="content/gfx/interface/images/mc/bones.png",
                                                                        r1="Effective Metabolism",
                                                                        r1_img="content/gfx/interface/images/mc/meta.png",
                                                                        r2="Sky Ward",
                                                                        r2_img="content/gfx/interface/images/mc/wind.png"
                                                                        )

        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"] = royal_guard = {}
        royal_guard["header"] = "Royal Guard"
        royal_guard["text"] = "Many years of exemplary service made him the captain of Palace Guard. It was then that he met your future mother, a young knight from a poor but noble family."
        royal_guard["text"] += "\n{color=[green]}+ Better Starting Home{/color}"
        royal_guard["label"] = "mc_setup_warrior_defender_guard"

        royal_guard["Royal Defender"] = temp = {}
        temp["text"] = "You've learned much about armor from your parents. The equipment provides additional defense based on its price."
        temp["text"] += set_font_color("\n+ {a=Armor Expert}Armor Expert Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_defender_guard_armor"

        royal_guard["Left-Handed"] = temp = {}
        temp["text"] = "You are left-handed, just like your mother. Items in your left hand (such as shields) is significantly more powerful, but equipment in your right hand (such as weapons) is less efficient."
        temp["text"] += set_font_color("\n+ {a=Left-Handed}Left-Handed Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_defender_guard_left"

        royal_guard["Shield Master"] = temp = {}
        temp["text"] = "Your mother taught you her fighting style. All shields are a bit more sturdy."
        temp["text"] += set_font_color("\n+ {a=Shield Master}Shield Master Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_defender_guard_shield"

        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"] = harpy = {}
        harpy["header"] = "Harpy"
        harpy["text"] = "One day, he was given a task of guarding an ambassador of the Harpies Empire. Unable to move freely around the city due to her status, she gladly accepted him as the main source of entertainment."
        harpy["text"] += set_font_color("\n+ Shooter Class", "green")
        harpy["text"] += set_font_color("\n+ {a=Harpy Priestess Blood}Harpy Priestess Blood Trait{/a}", "green")
        harpy["text"] += set_font_color("\n+ Air Elemental Alignment", "ivory")
        harpy["text"] += set_font_color("\n+ Air Magic Skill", "ivory")
        harpy["label"] = "mc_setup_warrior_defender_harpy"
        harpy["class"] = "Shooter"

        harpy["Hollow Bones"] = temp = {}
        temp["text"] = "Harpies evolved to have hollow bones making their bodies significantly lighter. It makes you weaker against physical attacks but completely neutralizes any equipment penalties to agility."
        temp["text"] += set_font_color("\n+ {a=Hollow Bones}Hollow Bones Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_defender_harpy_bones"

        harpy["Effective Metabolism"] = temp = {}
        temp["text"] = "Harpies digest food much more efficient than most other races. All consumables (and especially food) restore vitality far more effectively."
        temp["text"] += set_font_color("\n+ {a=Effective Metabolism}Effective Metabolism Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_defender_harpy_meta"

        harpy["Sky Ward"] = temp = {}
        temp["text"] = "Harpies use their mystical connection to the sky to fly. You may not be able to do that without wings, but that heritage is still of great help."
        temp["text"] += set_font_color("\n+ {a=Sky Ward}Sky Ward Trait{/a}", "green")
        temp["text"] += set_font_color("\n+ One Action Point", "green")
        temp["text"] += set_font_color("\n+ Agility", "green")
        temp["label"] = "mc_setup_warrior_defender_harpy_sky"


        mc_stories["Warrior"]["MC"]["Shooter"]["choices"] = OrderedDict(l="Forest Elf",
                                                                        l_img="content/gfx/interface/images/mc/forest_elf.jpg",
                                                                        l0="Sniper",
                                                                        l0_img="content/gfx/interface/images/mc/bow.png",
                                                                        l1="Elven Farsightedness",
                                                                        l1_img="content/gfx/interface/images/mc/aim.png",
                                                                        l2="Elven Ranger",
                                                                        l2_img="content/gfx/interface/images/mc/ranger.png",
                                                                        r="Summer Fay",
                                                                        r_img="content/gfx/interface/images/mc/summer_fay.jpg",
                                                                        r0="Eternality",
                                                                        r0_img="content/gfx/interface/images/mc/infinity.png",
                                                                        r1="Summer Affinity",
                                                                        r1_img="content/gfx/interface/images/mc/sun.png",
                                                                        r2="Life Beacon",
                                                                        r2_img="content/gfx/interface/images/mc/beacon.png"
                                                                        )

        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"] = forest_elf = {}
        forest_elf["header"] = "Forest Elf"
        forest_elf["text"] = "He worked closely together with elven rangers. As time passed, mistrust gave way to friendship and, eventually, to close relationships with one of their ranks."
        # forest_elf["text"] += set_font_color("\n+ Warrior Class", "green")
        forest_elf["text"] += set_font_color("\n+ {a=Forest Elf Blood}Forest Elf Blood Trait{/a}", "green")
        forest_elf["label"] = "mc_setup_warrior_shooter_forest_elf"
        # forest_elf["class"] = "Warrior" # I do not believe it to be reasonable to add Warrior here. It will nerf the effects of shooter.
        # Pure Shooter feels like a perfect fit here.

        forest_elf["Sniper"] = temp = {}
        temp["text"] = "Your mother taught you to use bows, as only the Forest Elves can. All bows are more powerful than usual."
        temp["text"] += set_font_color("\n+ {a=Bow Master}Bow Master Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_shooter_forest_elf_sniper"

        forest_elf["Elven Farsightedness"] = temp = {}
        temp["text"] = "Forest elves reliance on ranged weapons reduced their ability to fight in close combat but made them the best ranged weapon users amongst all races. This trait was passed to you from your mother."
        temp["text"] += set_font_color("\n+ {a=Farsightedness}Farsightedness Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_shooter_forest_elf_farsight"

        forest_elf["Elven Ranger"] = temp = {}
        temp["text"] = "Your mother taught you the ways of elves. Most ranged weapons don't give you penalties to defense."
        temp["text"] += set_font_color("\n+ {a=Elven Ranger}Elven Ranger Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_shooter_forest_elf_ranger"

        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"] = summer_fay = {}
        summer_fay["header"] = "Summer Fay"
        summer_fay["text"] = "For eons, Fae race performs the same functions in Forest Courts, unable to change their fate or even to die."
        summer_fay["text"] += " Summer Fae embody growth and the emergence of life. Making a child with an occasional mortal is one of the ways to fulfill that destiny."
        summer_fay["text"] += set_font_color("\n+ {a=Fae Blood}Fae Blood Trait{/a}", "green")
        summer_fay["text"] += set_font_color("\n+ Light Elemental Alignment", "green")
        summer_fay["text"] += set_font_color("\n+ One Light Elemental Spell", "green")
        summer_fay["label"] = "mc_setup_warrior_shooter_summer_fay"

        summer_fay["Eternality"] = temp = {}
        temp["text"] = "Your body inherited some of your mother's unchangeability. You recover half of max-health every day, but all healing items are less efficient."
        temp["text"] += set_font_color("\n+ {a=Summer Eternality}Summer Eternality Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_shooter_summer_fay_eternal"

        summer_fay["Summer Affinity"] = temp = {}
        temp["text"] = "You inherited some of your mother's mystical powers. Fire and Light elements are less effective against you and deal more damage to enemies."
        temp["text"] += set_font_color("\n+ {a=Summer Affinity}Summer Affinity Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_shooter_summer_fay_affinity"

        summer_fay["Life Beacon"] = temp = {}
        temp["text"] = "Your Fae inheritance gives you the Aura of Life which regenerates some health for you and all characters under your command every day, making them a bit happier."
        temp["text"] += set_font_color("\n+ {a=Life Beacon}Life Beacon Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_shooter_summer_fay_beacon"


        mc_stories["Warrior"]["MC"]["Assassin"]["choices"] = OrderedDict(l="Princess",
                                                                        l_img="content/gfx/interface/images/mc/princess.jpg",
                                                                        l0="Heavy Knight",
                                                                        l0_img="content/items/sweapon/bks.png",
                                                                        l1="Fencer",
                                                                        l1_img="content/items/weapon/og.png",
                                                                        l2="Royal Assassin",
                                                                        l2_img="content/gfx/interface/images/mc/crown.png",
                                                                        r="Drow",
                                                                        r_img="content/gfx/interface/images/mc/drow.jpg",
                                                                        r0="Poison Master",
                                                                        r0_img="content/gfx/interface/images/mc/poison.png",
                                                                        r1="High-Speed Fencer",
                                                                        r1_img="content/items/sweapon/cd.png",
                                                                        r2="Sister Lover",
                                                                        r2_img="content/gfx/interface/images/mc/sister.png")

        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"] = princess = {}
        princess["header"] = "Princess"
        princess["class"] = "Manager"
        princess["text"] = "He was instructed to eliminate a princess from another land while visiting their capital on a diplomatic mission. No one has seen her since then. Except you, her son."
        princess["text"] += " You were taught how to load and manage people and property."
        princess["text"] += set_font_color("\n+ Manager Class", "green")
        princess["text"] += set_font_color("\n+ {a=Royal Blood}Royal Blood Trait{/a}", "green")
        princess["text"] += set_font_color("\n+ 2000 Gold", "gold")
        princess["label"] = "mc_setup_warrior_assassin_princess"
        # princess["class"] = "Knight"

        princess["Heavy Knight"] = temp = {}
        temp["text"] = "Your mother taught you the combat style of Royal Knights, known only to members of the royal families. Defense provided by armor is a bit higher than usual."
        temp["text"] += set_font_color("\n+ {a=Knightly Stance}Knightly Stance Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_assassin_princess_knight"

        princess["Fencer"] = temp = {}
        temp["text"] = "Your mother taught you the fencing style of Royal Knights, known only to members of the royal families. All swords are a bit more powerful than usual."
        temp["text"] += set_font_color("\n+ {a=Sword Master}Sword Master Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_assassin_princess_fencer"

        princess["Royal Assassin"] = temp = {}
        temp["text"] = "Due to your heritage, you got used to the best of equipment. The more expensive your items are, the stronger is their attack."
        temp["text"] += set_font_color("\n+ {a=Royal Assassin}Royal Assassin Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_assassin_princess_royal"

        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"] = drow = {}
        drow["header"] = "Drow"
        drow["text"] = "Carrying out orders, your father often encountered competitors. He'd eliminate them together with the target, but one particularly skilled assassin evaded every one of his deadly strikes. It was your future mother, a lone elf from a distant, underground world."
        drow["text"] += set_font_color("\n+ {a=Drow Blood}Drow Blood Trait{/a}", "green")
        drow["text"] += set_font_color("\n+ Darkness Elemental Alignment", "darkgray")
        drow["text"] += set_font_color("\n+ One Darkness Magic Spell", "darkgray")
        drow["label"] = "mc_setup_warrior_assassin_drow"

        drow["Poison Master"] = temp = {}
        temp["text"] = "You know a lot about poisons from your mother. Toxins are much less effective against you, and your poison attacks are much stronger."
        temp["text"] += set_font_color("\n+ {a=Poison Master}Poison Master Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_assassin_drow_poison"

        drow["High-Speed Fencer"] = temp = {}
        temp["text"]= "You learned from your mother about rare combat style used by drow assassins. All daggers are more powerful than usual."
        temp["text"] += set_font_color("\n+ {a=Dagger Master}Dagger Master Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_assassin_drow_dagger"

        drow["Sister Lover"] = temp = {}
        temp["text"] = "Incest is widespread in drow families, and you know a lot about it from your mother's stories. Characters with the Half-Sister trait will not reject you due to kinship and will have additional disposition bonus."
        temp["text"] += set_font_color("\n+ {a=Sister Lover}Sister Lover Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_assassin_drow_sister"


        mc_stories["Warrior"]["MC"]["Warrior"]["choices"] = OrderedDict(l="Amazon",
                                                                        l_img="content/gfx/interface/images/mc/amazon.jpg",
                                                                        l0="Yuri Expert",
                                                                        l0_img="content/gfx/interface/images/mc/amazon_yuri.png",
                                                                        l1="Muscle",
                                                                        l1_img="content/gfx/interface/images/mc/amazon_const.png",
                                                                        l2="Berserk",
                                                                        l2_img="content/gfx/interface/images/mc/berserk.png",
                                                                        r="Dragon",
                                                                        r_img="content/gfx/interface/images/mc/dragon.jpg",
                                                                        r0="Fire",
                                                                        r0_img="content/gfx/interface/images/mc/fire_dragon.jpg",
                                                                        r1="Stone",
                                                                        r1_img="content/gfx/interface/images/mc/stone_dragon.jpg",
                                                                        r2="Dragon Sight",
                                                                        r2_img="content/gfx/interface/images/mc/dragon_eye.png")

        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"] = amazon = {}
        amazon["header"] = "Amazon"
        amazon["text"] = "It was there that he met your mother, an Amazon from a remote tribe. After defeating her in battle, he took her body instead of taking her life."
        amazon["text"] += set_font_color("\n+ Arena Reputation", "green")
        amazon["text"] += set_font_color("\n+ {a=Amazon Blood}Amazon Blood Trait{/a}", "green")
        amazon["label"] = "mc_setup_warrior_warrior_amazon"

        amazon["Yuri Expert"] = temp = {}
        temp["text"] = "Amazon tribes live without males, so you know a lot about lesbians from your mother's stories. Lesbian characters will not reject you due to your gender, and your oral skill is pretty good too."
        temp["text"] += set_font_color("\n+ {a=Yuri Expert}Yuri Expert Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_warrior_amazon_yuri"

        amazon["Muscle"] = temp = {}
        temp["text"] = "You inherited your mother's strength. Melee weapons deal more damage than usual."
        temp["text"] += set_font_color("\n+ {a=Amazon Musculature}Amazon Musculature Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_warrior_amazon_muscle"

        amazon["Berserk"] = temp = {}
        temp["text"] = "Your mother taught you her fighting style. All defense bonuses from equipment are lower, but all attack bonuses are higher."
        temp["text"] += set_font_color("\n+ {a=Berserk}Berserk Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_warrior_amazon_berserk"

        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"] = dragon = {}
        dragon["header"] = "Dragon"
        dragon["text"] = "It was there that he met your mother, one of the last half-dragons. Being a monster, she was supposed to fight him to the death, but her dislike for clothes changed his mind."
        dragon["text"] += set_font_color("\n+ {a=Dragon Blood}Dragon Blood Trait{/a}", "green")
        dragon["text"] += set_font_color("\n+ Assassin Class", "green")
        dragon["label"] = "mc_setup_warrior_warrior_dragon"
        dragon["class"] = "Assassin"

        dragon["Fire"] = temp = {}
        temp["text"] = "Your body is covered with tiny scales. They are almost unnoticeable, but at extreme temperatures they actively absorb and dissipate heat, making fire and, to some extent, electricity less effective."
        temp["text"] += set_font_color("\n+ {a=Fire Dragon Scales}Fire Dragon Scales Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_warrior_dragon_fire"

        dragon["Stone"] = temp = {}
        temp["text"] = "Your body is covered with tiny scales. They are almost unnoticeable, but upon impact they become as hard as iron, softening the blow (+earth and physical resistance)."
        temp["text"] += set_font_color("\n+ {a=Stone Dragon Scales}Stone Dragon Scales Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_warrior_dragon_stone"

        dragon["Dragon Sight"] = temp = {}
        temp["text"] = "Dragons have perfect vision, and so do you. You are competent with ranged weapons and deal (slightly) increased critical damage."
        temp["text"] += set_font_color("\n+ {a=Dragon Eyesight}Dragon Eyesight Trait{/a}", "green")
        temp["label"] = "mc_setup_warrior_warrior_dragon_sight"

    python hide: # Mage options:
        mc_stories["Mage"]["choices"]["Sorcerer"] = "content/gfx/interface/images/mc/sorc.png"
        mc_stories["Mage"]["choices"]["Researcher"] = "content/gfx/interface/images/mc/researcher.png"
        mc_stories["Mage"]["choices"]["Arcane Knight"] = "content/gfx/interface/images/mc/arc.png"

        mc_stories["Mage"]["Arcane Knight"] = temp = {}
        # temp["class"] = "Mage"
        temp["text"] = "As an Arcane Knight, he specialized in the extermination of dangerous magical creatures who were continually threatening the city."
        # temp["text"] += set_font_color("\n+ Mage Class", "green")

        mc_stories["Mage"]["Sorcerer"] = temp = {}
        # temp["class"] = "Mage"
        temp["text"] = "As a Sorcerer, he dedicated his life to the study of arcane arts."
        # temp["text"] += set_font_color("\n+ Mage Class", "green")

        mc_stories["Mage"]["Researcher"] = temp = {}
        # temp["class"] = "Mage"
        temp["text"] = "As a Researcher, he studied ruins of ancient civilizations in search of forgotten technologies and enchantments."
        # temp["text"] += set_font_color("\n+ Mage Class", "green")

        mc_stories["Mage"]["MC"] = {}
        for key in mc_stories["Mage"]["choices"]:
            mc_stories["Mage"]["MC"][key] = {}
            mc_stories["Mage"]["MC"][key]["choices"] = OrderedDict()


        mc_stories["Mage"]["MC"]["Researcher"]["choices"] = OrderedDict(l="Android",
                                                                      l_img="content/gfx/interface/images/mc/android.jpg",
                                                                      l0="Creature of Electricity",
                                                                      l0_img="content/gfx/interface/images/mc/ele.png",
                                                                      l1="Looped Physiology",
                                                                      l1_img="content/gfx/interface/images/mc/loop.png",
                                                                      l2="Recharge",
                                                                      l2_img="content/gfx/interface/images/mc/recharge.png",
                                                                      r="Slime",
                                                                      r_img="content/gfx/interface/images/mc/slime.jpg",
                                                                      r0="Creature of Water",
                                                                      r0_img="content/gfx/interface/images/mc/water.png",
                                                                      r1="Arcane Archer",
                                                                      r1_img="content/gfx/interface/images/mc/bow.png",
                                                                      r2="Point Resilience",
                                                                      r2_img="content/gfx/interface/images/mc/slime.png"
                                                                      )

        mc_stories["Mage"]["MC"]["Researcher"]["Android"] = android = {}
        android["header"] = "Android"
        android["text"] = "In one of his expeditions, he found an ancient faulty android. He managed to repair and reprogram her to be his 'very' personal assistant."
        android["text"] += set_font_color("\n+ Assassin Class", "green")
        android["text"] += set_font_color("\n+ Electricity Elemental Alignment", "#7df9ff")
        android["text"] += set_font_color("\n+ Special attack you can use when fighting unarmed.", "#7df9ff")
        android["label"] = "mc_setup_mage_researcher_android"
        android["class"] = "Assassin"

        android["Creature of Electricity"] = temp = {}
        temp["text"] = "Electricity spells heal you instead of dealing damage, but your Water spells are almost useless."
        temp["text"] += " You were left small inheritance by your parents."
        temp["text"] += set_font_color("\n+ {a=Master of Electricity}Master of Electricity Trait{/a}", "#7df9ff")
        temp["text"] += set_font_color("\n+ Three Spell Scrolls", "#7df9ff")
        temp["label"] = "mc_setup_mage_researcher_android_ele"

        android["Looped Physiology"] = temp = {}
        temp["text"] = "Healing spells don't affect you, but your vitality can never drop to zero."
        temp["text"] += set_font_color("\n+ {a=Looped Physiology}Looped Physiology Trait{/a}", "green")
        temp["label"] = "mc_setup_mage_researcher_android_loop"

        android["Recharge"] = temp = {}
        temp["text"] = "Most consumables, even those that don't typically increase MP, restore yours when you consume them."
        temp["text"] += set_font_color("\n+ {a=Recharging}Recharging Trait{/a}", "green")
        temp["label"] = "mc_setup_mage_researcher_android_recharge"

        mc_stories["Mage"]["MC"]["Researcher"]["Slime"] = slime = {}
        slime["header"] = "Slime"
        slime["text"] = "Pureblood slimes do not feel pleasure in the same way as non-liquid beings, but they are still interested in mating, especially with creatures of potent magic, like your father."
        slime["text"] += set_font_color("\n+ {a=Liquid Body Structure}Liquid Body Structure Trait{/a}", "#2389da")
        slime["text"] += set_font_color("\n+ Water Elemental Alignment", "#2389da")
        slime["text"] += set_font_color("\n+ Couple of Spells", "#2389da")
        slime["label"] = "mc_setup_mage_researcher_slime"
        slime["class"] = "Shooter"

        slime["Creature of Water"] = temp = {}
        temp["text"] = "Water spells heal you instead of hurting, but your Electricity spells are almost ineffective."
        temp["text"] += set_font_color("\n+ {a=Master of Water}Master of Water Trait{/a}", "#2389da")
        temp["text"] += set_font_color("\n+ Three Spell Scrolls", "#2389da")
        temp["label"] = "mc_setup_mage_researcher_slime_water"

        slime["Arcane Archer"] = temp = {}
        temp["class"] = "Shooter"
        temp["text"] = "Most ranged weapons give a bonus to magic equal to their bonus to attack."
        temp["text"] += set_font_color("\n+ Shooter Class", "green")
        temp["text"] += set_font_color("\n+ {a=Arcane Archer}Arcane Archer Trait{/a}", "green")
        temp["label"] = "mc_setup_mage_researcher_slime_aarcher"

        slime["Point Resilience"] = temp = {}
        temp["text"] = "Ranged attacks are ineffective against you, but melee weapons are more dangerous."
        temp["text"] += set_font_color("\n+ {a=Resilience}Resilience Trait{/a}", "green")
        temp["label"] = "mc_setup_mage_researcher_slime_res"

        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"] = winter_fay = {}
        winter_fay["header"] = "Winter Fay"
        winter_fay["text"] = "Winter Fae are known to be harsh and unyielding, embodying entropy and death in the circle of nature. Therefore the reason behind your birth remains to be discovered."
        winter_fay["text"] += set_font_color("\n+ {a=Fae Blood}Fae Blood Trait{/a}", "green")
        winter_fay["text"] += set_font_color("\n+ Ice Elemental Alignment", "#A5F2F3")
        winter_fay["text"] += set_font_color("\n+ Couple of Spells", "#A5F2F3")
        winter_fay["label"] = "mc_setup_mage_sorcerer_winter"

        winter_fay["Creature of Ice"] = temp = {}
        temp["text"] = "Ice spells heal you instead of dealing damage, but your Fire spells are almost useless."
        temp["text"] += set_font_color("\n+ {a=Master of Ice}Master of Ice Trait{/a}", "#A5F2F3")
        temp["text"] += set_font_color("\n+ Three Spell Scrolls", "#A5F2F3")
        temp["label"] = "mc_setup_mage_sorcerer_winter_ice"

        winter_fay["Immutability"] = temp = {}
        temp["text"] = "Your body inherited some of your mother's unchangeability. You restore a third of maximum MP every day. Items that restore it are less effective."
        temp["text"] += set_font_color("\n+ {a=Winter Eternality}Winter Eternality Trait{/a}", "#A5F2F3")
        temp["label"] = "mc_setup_mage_sorcerer_winter_imm"

        winter_fay["Winter Magician"] = temp = {}
        temp["text"] = "The Winter itself gives you power. You have less MP, but it can never become exhausted."
        temp["text"] += set_font_color("\n+ {a=Winter Magician}Winter Magician Trait{/a}", "#A5F2F3")
        temp["label"] = "mc_setup_mage_sorcerer_winter_win"


        mc_stories["Mage"]["MC"]["Sorcerer"]["choices"] = OrderedDict(l="Kitsune",
                                                                      l_img="content/gfx/interface/images/mc/kitsune.jpg",
                                                                      l0="Fire Fox",
                                                                      l0_img="content/gfx/interface/images/mc/fire.png",
                                                                      l1="Mana Source",
                                                                      l1_img="content/gfx/interface/images/mc/flow.png",
                                                                      l2="Magical Kin",
                                                                      l2_img="content/gfx/interface/images/mc/mana.png",
                                                                      r="Winter Fay",
                                                                      r_img="content/gfx/interface/images/mc/winter.jpg",
                                                                      r0="Creature of Ice",
                                                                      r0_img="content/gfx/interface/images/mc/ice.png",
                                                                      r1="Immutability",
                                                                      r1_img="content/gfx/interface/images/mc/infinity_1.png",
                                                                      r2="Winter Magician",
                                                                      r2_img="content/gfx/interface/images/mc/winter_m.png",
                                                                      )

        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"] = kitsune = {}
        kitsune["header"] = "Kitsune"
        kitsune["text"] = "Kitsunes are intelligent beings from a distant land. They possess potent magical abilities that increase as they grow older."
        kitsune["text"] +=" Your mother, however, was very young and inexperienced when her clan sent her to study arcane arts under the guidance of your father."
        kitsune["text"] += set_font_color("\n+ {a=Kitsune Blood}Kitsune Blood Trait{/a}", "green")
        kitsune["text"] += set_font_color("\n+ Fire Elemental Alignment", "orange")
        kitsune["text"] += set_font_color("\n+ One Fire Spell", "orange")
        kitsune["label"] = "mc_setup_mage_sorcerer_kitsune"

        kitsune["Fire Fox"] = temp = {}
        temp["text"] = "Fire spells heal you instead of hurting, but your Ice spells are almost ineffective."
        temp["text"] += set_font_color("\n+ {a=Master of Fire}Master of Fire Trait{/a}", "orange")
        temp["text"] += set_font_color("\n+ Three Spell Scrolls", "orange")
        temp["label"] = "mc_setup_mage_sorcerer_kitsune_fire"

        kitsune["Mana Source"] = temp = {}
        temp["text"] = "Your magical origins allow you to restore the magical energy of your partners during intimate acts."
        temp["text"] += set_font_color("\n+ {a=Mana Source}Mana Source Trait{/a}", "green")
        temp["label"] = "mc_setup_mage_sorcerer_kitsune_mana"

        kitsune["Magical Kin"] = temp = {}
        temp["text"] = "Consumables, especially alcoholic beverages, restore much more MP."
        temp["text"] += set_font_color("\n+ {a=Magical Kin}Magical Kin Trait{/a}", "green")
        temp["label"] = "mc_setup_mage_sorcerer_kitsune_flow"

        mc_stories["Mage"]["MC"]["Arcane Knight"]["choices"] = OrderedDict(l="Ghost",
                                                                      l_img="content/gfx/interface/images/mc/ghost.jpg",
                                                                      l0="Intangible",
                                                                      l0_img="content/gfx/interface/images/mc/ill.png",
                                                                      l1="Illusive",
                                                                      l1_img="content/gfx/interface/images/mc/illusion.png",
                                                                      l2="Creature of Light",
                                                                      l2_img="content/gfx/interface/images/elements/small_light.png",
                                                                      r="Vampire",
                                                                      r_img="content/gfx/interface/images/mc/vampire.jpg",
                                                                      r0="Creature of Night",
                                                                      r0_img="content/gfx/interface/images/mc/night.png",
                                                                      r1="Blood Master",
                                                                      r1_img="content/gfx/interface/images/mc/blood.png",
                                                                      r2="Perfect Reflexes",
                                                                      r2_img="content/gfx/interface/images/mc/reflexes.png"
                                                                      )

        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"] = ghost = {}
        ghost["header"] = "Ghost"
        ghost["text"] = "While exploring an abandoned temple in an ancient forest, your father found a friendly,"
        ghost["text"] += " lonely spirit of a young priestess. She gladly joined with him, and soon enough they became a family."
        ghost["text"] += set_font_color("\n+ Warrior Class", "green")
        ghost["text"] += set_font_color("\n+ {a=Ghostly Structure}Ghostly Structure Trait{/a}", "green")
        ghost["text"] += set_font_color("\n+ Light Elemental Alignment", "ivory")
        ghost["text"] += set_font_color("\n+ Couple of Spells", "ivory")
        ghost["label"] = "mc_setup_mage_arc_ghost"
        ghost["class"] = "Warrior"

        ghost["Intangible"] = temp = {}
        temp["text"] = "Just as your mother, you are do not entirely belong to the world of the living. All attacks and magic are less effective against you, but your attacks and magic are less efficient as well."
        temp["text"] += set_font_color("\n+ {a=Incorporeal}Incorporeal Trait{/a}", "green")
        temp["label"] = "mc_setup_mage_arc_ghost_intangible"

        ghost["Illusive"] = temp = {}
        temp["text"] = "You exist between the realm of light and darkness. Physical damage is almost ineffective against you, but being ghostly, you can't take girls virginity."
        temp["text"] += set_font_color("\n+ {a=Illusive}Illusive Trait{/a}", "green")
        temp["label"] = "mc_setup_mage_arc_ghost_illusive"

        ghost["Creature of Light"] = temp = {}
        temp["text"] = "Light spells heal you instead of dealing damage, but your Darkness spells are almost ineffective."
        temp["text"] += " You've were left some inheritance."
        temp["text"] += set_font_color("\n+ {a=Master of Light}Master of Light{/a}", "ivory")
        temp["text"] += set_font_color("\n+ Three Spell Scrolls", "ivory")
        temp["label"] = "mc_setup_mage_arc_ghost_light"

        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"] = vampire = {}
        vampire["header"] = "Vampire"
        vampire["text"] = "For decades he hunted vampires, protecting citizens from these nocturnal predators."
        vampire["text"] += " One day, while clearing a nest, he captured a vampire queen, but her seductiveness kept her alive and even gave birth to you."
        vampire["text"] += set_font_color("\n+ Knight Class", "green")
        vampire["text"] += set_font_color("\n+ {a=Vampiric Blood}Vampiric Blood Trait{/a}", "green")
        vampire["text"] += set_font_color("\n+ Darkness Elemental Alignment", "purple")
        vampire["text"] += set_font_color("\n+ Couple of Spells", "purple")
        vampire["label"] = "mc_setup_mage_arc_vampire"
        vampire["class"] = "Knight"

        vampire["Creature of Night"] = temp = {}
        temp["text"] = "Darkness spells heal you instead of dealing damage, but your Light spells are almost ineffective."
        temp["text"] += set_font_color("\n+ {a=Master of Darkness}Master of Darkness{/a}", "purple")
        temp["text"] += set_font_color("\n+ Three Spell Scrolls", "purple")
        temp["label"] = "mc_setup_mage_arc_vampire_night"

        vampire["Blood Master"] = temp = {}
        temp["text"] = "Only true vampires have access to blood magic, but your heritage still gives a few perks. Girls who lose their virginity to you, become more obedient."
        temp["text"] += set_font_color("\n+ {a=Blood Master}Blood Master Trait{/a}", "green")
        temp["label"] = "mc_setup_mage_arc_vampire_blood"

        vampire["Perfect Reflexes"] = temp = {}
        temp["text"] = "You inherited your mother's reflexes, which help to evade attacks. Sadly, mortal body is not suitable for vampire speed, affecting your health."
        temp["text"] += set_font_color("\n+ {a=Perfect Reflexes}Perfect Reflexes Trait{/a}", "green")
        temp["label"] = "mc_setup_mage_arc_vampire_reflex"
