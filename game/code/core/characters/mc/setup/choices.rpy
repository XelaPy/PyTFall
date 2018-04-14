label build_mc_stories:

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

        mc_stories["Merchant"] = {} # Merchant! This is the main branch displayed as the very first thing (four choices).
        mc_stories["Merchant"]["img"] = "content/gfx/interface/images/merchant.png" # Path to the icon representing the branch onscreen.
        mc_stories["Merchant"]["choices"] = OrderedDict()

        mc_stories["Warrior"] = {}
        mc_stories["Warrior"]["img"] = "content/gfx/interface/images/warriorP.png"
        mc_stories["Warrior"]["header"] = "Your father was a skilled fighter..."
        mc_stories["Warrior"]["choices"] = OrderedDict(Warrior="content/gfx/interface/images/mc/warrior_m.png",
                                                       Knight="content/gfx/interface/images/mc/defender_m.png",
                                                       Shooter="content/gfx/interface/images/mc/shooter_m.png",
                                                       Assassin="content/gfx/interface/images/mc/assassin_m.png")

        mc_stories["Mage"] = {}
        mc_stories["Mage"]["img"] = "content/gfx/interface/images/magicP.png"
        mc_stories["Mage"]["header"] = "Your father was a powerful mage..."
        mc_stories["Mage"]["choices"] = OrderedDict()

        mc_stories["Noble"] = {}
        mc_stories["Noble"]["img"] = "content/gfx/interface/images/nobleP.png"
        mc_stories["Mage"]["header"] = "Your father was a powerful mage..."
        mc_stories["Noble"]["choices"] = OrderedDict()

    python hide: # Warrior options:
        mc_stories["Warrior"]["Warrior"] = {}
        mc_stories["Warrior"]["Warrior"]["class"] = "Warrior"
        mc_stories["Warrior"]["Warrior"]["text"] = "He was a famous gladiator. Decades of fighting at the arena made him competent with almost every known weapon and brought fame and wealth."
        mc_stories["Warrior"]["Assassin"] = {}
        mc_stories["Warrior"]["Assassin"]["class"] = "Assassin"
        mc_stories["Warrior"]["Assassin"]["text"] = "He was a deadly assassin. Even royalties, diplomats and nobility would perish at the tip of his blade, for the right price."
        mc_stories["Warrior"]["Shooter"] = {}
        mc_stories["Warrior"]["Shooter"]["class"] = "Shooter"
        mc_stories["Warrior"]["Shooter"]["text"] = "He was a skilled marksman. For many years together with other rangers, he hunted monsters and smugglers."
        mc_stories["Warrior"]["Knight"] = {}
        mc_stories["Warrior"]["Knight"]["class"] = "Knight"
        mc_stories["Warrior"]["Knight"]["text"] = "He was an experienced bodyguard. His skills secured him a place in high society, as he provided his service to the nobility and royalty alike."

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

        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"] = {}
        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["header"] = "Royal Guard"
        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["text"] = "Many years of exemplary service made him the captain of Palace Guard. It was then that he met your future mother, a young knight from a poor but noble family."
        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["label"] = "mc_setup_warrior_defender_guard"

        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["Royal Defender"] = {}
        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["Royal Defender"]["text"] = "You've learned much about armor from your parents. The equipment provides additional defense based on its price."
        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["Royal Defender"]["label"] = "mc_setup_warrior_defender_guard_armor"

        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["Left-Handed"] = {}
        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["Left-Handed"]["text"] = "You are left-handed, just like your mother. Items in your left hand (such as shields) is significantly more powerful, but equipment in your right hand (such as weapons) is less efficient."
        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["Left-Handed"]["label"] = "mc_setup_warrior_defender_guard_left"

        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["Shield Master"] = {}
        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["Shield Master"]["text"] = "Your mother taught you her fighting style. All shields are a bit more sturdy."
        mc_stories["Warrior"]["MC"]["Knight"]["Royal Guard"]["Shield Master"]["label"] = "mc_setup_warrior_defender_guard_shield"

        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"] = {}
        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["header"] = "Harpy"
        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["text"] = "One day, he was given a task of guarding an ambassador of the Harpies Empire. Unable to move freely around the city due to her status, she gladly accepted him as the main source of entertainment."
        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["label"] = "mc_setup_warrior_defender_harpy"
        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["class"] = "Shooter"

        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["Hollow Bones"] = {}
        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["Hollow Bones"]["text"] = "Harpies evolved to have hollow bones making their bodies significantly lighter. It makes you weaker against physical attacks but completely neutralizes any equipment penalties to agility."
        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["Hollow Bones"]["label"] = "mc_setup_warrior_defender_harpy_bones"

        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["Effective Metabolism"] = {}
        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["Effective Metabolism"]["text"] = "Harpies digest food much more efficient than most other races. All consumables (and especially food) restore vitality far more effectively."
        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["Effective Metabolism"]["label"] = "mc_setup_warrior_defender_harpy_meta"

        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["Sky Ward"] = {}
        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["Sky Ward"]["text"] = "Harpies use their mystical connection to the sky to fly. You may not be able to do that without wings, but that heritage is still of great help. (+1 Action Point and additional agility)"
        mc_stories["Warrior"]["MC"]["Knight"]["Harpy"]["Sky Ward"]["label"] = "mc_setup_warrior_defender_harpy_sky"


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

        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["header"] = "Forest Elf"
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["text"] = "He worked closely together with elven rangers. As time passed, mistrust gave way to friendship and, eventually, to close relationships with one of their ranks."
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["label"] = "mc_setup_warrior_shooter_forest_elf"
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["class"] = "Warrior"

        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Sniper"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Sniper"]["text"] = "Your mother taught you to use bows, as only the Forest Elves can. All bows are more powerful than usual."
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Sniper"]["label"] = "mc_setup_warrior_shooter_forest_elf_sniper"

        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Farsightedness"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Farsightedness"]["text"] = "Forest elves reliance on ranged weapons reduced their ability to fight in close combat but made them the best ranged weapon users amongst all races. This trait was passed to you from your mother."
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Farsightedness"]["label"] = "mc_setup_warrior_shooter_forest_elf_farsight"

        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Ranger"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Ranger"]["text"] = "Your mother taught you the ways of elves. Most ranged weapons don't give you penalties to defense."
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Ranger"]["label"] = "mc_setup_warrior_shooter_forest_elf_ranger"


        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["header"] = "Summer Fay"
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["text"] = "For eons, Fae race performs the same functions in Forest Courts, unable to change their fate or even to die. Summer Fae embody growth and the emergence of life. Making a child with an occasional mortal is one of the ways to fulfill that destiny."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["label"] = "mc_setup_warrior_shooter_summer_fay"

        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Eternality"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Eternality"]["text"] = "Your body inherited some of your mother's unchangeability. You recover half of max-health every day, but all healing items are less efficient."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Eternality"]["label"] = "mc_setup_warrior_shooter_summer_fay_eternal"

        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Summer Affinity"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Summer Affinity"]["text"] = "You inherited some of your mother's mystical powers. Fire and Light elements are less effective against you and deal more damage to enemies."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Summer Affinity"]["label"] = "mc_setup_warrior_shooter_summer_fay_affinity"

        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Life Beacon"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Life Beacon"]["text"] = "Your Fae inheritance gives you the Aura of Life which regenerates some health for you and all characters under your command every day, making them a bit happier."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Life Beacon"]["label"] = "mc_setup_warrior_shooter_summer_fay_beacon"


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

        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["header"] = "Princess"
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["text"] = "He was instructed to eliminate a princess from another land while visiting their capital on a diplomatic mission. No one has seen her since then. Except you, her son. (+2000 Gold)"
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["label"] = "mc_setup_warrior_assassin_princess"
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["class"] = "Knight"

        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Heavy Knight"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Heavy Knight"]["text"] = "Your mother taught you the combat style of Royal Knights, known only to members of the royal families. Defense provided by armor is a bit higher than usual."
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Heavy Knight"]["label"] = "mc_setup_warrior_assassin_princess_knight"


        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Fencer"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Fencer"]["text"] = "Your mother taught you the fencing style of Royal Knights, known only to members of the royal families. All swords are a bit more powerful than usual."
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Fencer"]["label"] = "mc_setup_warrior_assassin_princess_fencer"

        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Royal Assassin"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Royal Assassin"]["text"] = "Due to your heritage, you got used to the best of equipment. The more expensive your items are, the stronger is their attack."
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Royal Assassin"]["label"] = "mc_setup_warrior_assassin_princess_royal"

        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["header"] = "Drow"
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["text"] = "Carrying out orders, your father often encountered competitors. He'd eliminate them together with the target, but one particularly skilled assassin evaded every one of his deadly strikes. It was your future mother, a lone elf from a distant, underground world."
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["label"] = "mc_setup_warrior_assassin_drow"

        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Poison Master"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Poison Master"]["text"]= "You know a lot about poisons from your mother. Toxins are much less effective against you, and your poison attacks are much stronger."
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Poison Master"]["label"] = "mc_setup_warrior_assassin_drow_poison"

        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["High-Speed Fencer"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["High-Speed Fencer"]["text"]= "You learned from your mother about rare combat style used by drow assassins. All daggers are more powerful than usual."
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["High-Speed Fencer"]["label"] = "mc_setup_warrior_assassin_drow_dagger"

        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Sister Lover"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Sister Lover"]["text"]= "Incest is widespread in drow families, and you know a lot about it from your mother's stories. Characters with the Half-Sister trait will not reject you due to kinship and will have additional disposition bonus."
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Sister Lover"]["label"] = "mc_setup_warrior_assassin_drow_sister"

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




        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["header"] = "Amazon"
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["text"] = "It was there that he met your mother, an Amazon from a remote tribe. After defeating her in battle, he took her body instead of taking her life.  (+ Arena Reputation)"
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["label"] = "mc_setup_warrior_warrior_amazon"

        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Yuri Expert"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Yuri Expert"]["text"] = "Amazon tribes live without males, so you know a lot about lesbians from your mother's stories. Lesbian characters will not reject you due to your gender, and your oral skill is pretty good too."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Yuri Expert"]["label"] = "mc_setup_warrior_warrior_amazon_yuri"

        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Muscle"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Muscle"]["text"] = "You inherited your mother's strength. Melee weapons deal more damage than usual."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Muscle"]["label"] = "mc_setup_warrior_warrior_amazon_muscle"

        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Berserk"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Berserk"]["text"] = "Your mother taught you her fighting style. All defense bonuses from equipment are lower, but all attack bonuses are higher."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Berserk"]["label"] = "mc_setup_warrior_warrior_amazon_berserk"

        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["header"] = "Dragon"
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["text"] = "It was there that he met your mother, one of the last half-dragons. Being a monster, she was supposed to fight him to the death, but her dislike for clothes changed his mind."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["label"] = "mc_setup_warrior_warrior_dragon"
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["class"] = "Assassin"

        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Fire"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Fire"]["text"] = "Your body is covered with tiny scales. They are almost unnoticeable, but at extreme temperatures they actively absorb and dissipate heat, making fire and, to some extent, electricity less effective."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Fire"]["label"] = "mc_setup_warrior_warrior_dragon_fire"

        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Stone"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Stone"]["text"] = "Your body is covered with tiny scales. They are almost unnoticeable, but upon impact they become as hard as iron, softening the blow (+earth and physical resistance)."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Stone"]["label"] = "mc_setup_warrior_warrior_dragon_stone"

        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Dragon Sight"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Dragon Sight"]["text"] = "Dragons have perfect vision, and so do you. You are competent with ranged weapons and deal (slightly) increased critical damage."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Dragon Sight"]["label"] = "mc_setup_warrior_warrior_dragon_sight"



    python hide: # Mage options:
        mc_stories["Mage"]["choices"]["Arcane Knight"] = "content/gfx/interface/images/mc/arc.png"
        mc_stories["Mage"]["choices"]["Sorcerer"] = "content/gfx/interface/images/mc/sorc.png"
        mc_stories["Mage"]["choices"]["Researcher"] = "content/gfx/interface/images/mc/researcher.png"

        mc_stories["Mage"]["Arcane Knight"] = {}
        mc_stories["Mage"]["Arcane Knight"]["class"] = "Mage"
        mc_stories["Mage"]["Arcane Knight"]["text"] = "As an Arcane Knight, he specialized in the extermination of dangerous magical creatures who were continually threatening the city."

        mc_stories["Mage"]["Sorcerer"] = {}
        mc_stories["Mage"]["Sorcerer"]["class"] = "Mage"
        mc_stories["Mage"]["Sorcerer"]["text"] = "As a Sorcerer, he dedicated his life to the study of arcane arts."

        mc_stories["Mage"]["Researcher"] = {}
        mc_stories["Mage"]["Researcher"]["class"] = "Mage"
        mc_stories["Mage"]["Researcher"]["text"] = "As a Researcher, he studied ruins of ancient civilizations in search of forgotten technologies and enchantments."

        mc_stories["Mage"]["MC"] = {}
        for key in mc_stories["Mage"]["choices"]:
            mc_stories["Mage"]["MC"][key] = {}
            mc_stories["Mage"]["MC"][key]["choices"] = OrderedDict()

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

        mc_stories["Mage"]["MC"]["Researcher"]["Android"] = {}
        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["header"] = "Android"
        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["text"] = "In one of his expeditions, he found an ancient faulty android. He managed to repair and reprogram her to be his 'very' personal assistant."
        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["label"] = "mc_setup_mage_researcher_android"
        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["class"] = "Assassin"

        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["Creature of Electricity"] = {}
        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["Creature of Electricity"]["text"] = "Electricity spells heal you instead of dealing damage, but your Water spells are almost useless."
        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["Creature of Electricity"]["label"] = "mc_setup_mage_researcher_android_ele"

        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["Looped Physiology"] = {}
        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["Looped Physiology"]["text"] = "Healing spells don't affect you, but your vitality can never drop to zero."
        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["Looped Physiology"]["label"] = "mc_setup_mage_researcher_android_loop"

        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["Recharge"] = {}
        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["Recharge"]["text"] = "Most consumables, even those that don't typically increase MP, restore yours when you consume them."
        mc_stories["Mage"]["MC"]["Researcher"]["Android"]["Recharge"]["label"] = "mc_setup_mage_researcher_android_recharge"

        mc_stories["Mage"]["MC"]["Researcher"]["Slime"] = {}
        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["header"] = "Slime"
        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["text"] = "Pureblood slimes do not feel pleasure in the same way as non-liquid beings, but they are still interested in mating, especially with creatures of potent magic, like your father."
        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["label"] = "mc_setup_mage_researcher_slime"
        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["class"] = "Shooter"

        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["Creature of Water"] = {}
        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["Creature of Water"]["text"] = "Water spells heal you instead of hurting, but your Electricity spells are almost ineffective."
        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["Creature of Water"]["label"] = "mc_setup_mage_researcher_slime_water"

        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["Point Resilience"] = {}
        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["Point Resilience"]["text"] = "Ranged attacks are ineffective against you, but melee weapons are more dangerous."
        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["Point Resilience"]["label"] = "mc_setup_mage_researcher_slime_res"

        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["Arcane Archer"] = {}
        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["Arcane Archer"]["text"] = "Most ranged weapons give a bonus to magic equal to their bonus to attack."
        mc_stories["Mage"]["MC"]["Researcher"]["Slime"]["Arcane Archer"]["label"] = "mc_setup_mage_researcher_slime_aarcher"

        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"] = {}
        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["header"] = "Winter Fay"
        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["text"] = "Winter Fae are known to be harsh and unyielding, embodying entropy and death in the circle of nature. Therefore the reason behind your birth remains to be discovered."
        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["label"] = "mc_setup_mage_sorcerer_winter"

        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["Creature of Ice"] = {}
        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["Creature of Ice"]["text"] = "Ice spells heal you instead of dealing damage, but your Fire spells are almost useless."
        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["Creature of Ice"]["label"] = "mc_setup_mage_sorcerer_winter_ice"

        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["Immutability"] = {}
        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["Immutability"]["text"] = "Your body inherited some of your mother's unchangeability. You restore a third of maximum MP every day. Items that restore it are less effective."
        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["Immutability"]["label"] = "mc_setup_mage_sorcerer_winter_imm"

        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["Winter Magician"] = {}
        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["Winter Magician"]["text"] = "The Winter itself gives you power. You have less MP, but it can never become exhausted."
        mc_stories["Mage"]["MC"]["Sorcerer"]["Winter Fay"]["Winter Magician"]["label"] = "mc_setup_mage_sorcerer_winter_win"

        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"] = {}
        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["header"] = "Kitsune"
        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["text"] = "Kitsunes are intelligent beings from a distant land. They possess potent magical abilities that increase as they grow older. Your mother, however, was very young and inexperienced when her clan sent her to study arcane arts under the guidance of your father."
        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["label"] = "mc_setup_mage_sorcerer_kitsune"

        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["Fire Fox"] = {}
        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["Fire Fox"]["text"] = "Fire spells heal you instead of hurting, but your Ice spells are almost ineffective."
        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["Fire Fox"]["label"] = "mc_setup_mage_sorcerer_kitsune_fire"

        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["Mana Source"] = {}
        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["Mana Source"]["text"] = "Your magical origins allow you to restore the magical energy of your partners during intimate acts."
        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["Mana Source"]["label"] = "mc_setup_mage_sorcerer_kitsune_mana"

        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["Magical Kin"] = {}
        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["Magical Kin"]["text"] = "Consumables, especially alcoholic beverages, restore much more MP."
        mc_stories["Mage"]["MC"]["Sorcerer"]["Kitsune"]["Magical Kin"]["label"] = "mc_setup_mage_sorcerer_kitsune_flow"

        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["header"] = "Ghost"
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["text"] = "While exploring an abandoned temple in an ancient forest, your father found a friendly, lonely spirit of a young priestess. She gladly joined with him, and soon enough they became a family."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["label"] = "mc_setup_mage_arc_ghost"
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["class"] = "Warrior"

        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["Intangible"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["Intangible"]["text"] = "Just as your mother, you are do not entirely belong to the world of the living. All attacks and magic are less effective against you, but your attacks and magic are less efficient as well."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["Intangible"]["label"] = "mc_setup_mage_arc_ghost_intangible"

        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["Illusive"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["Illusive"]["text"] = "You exist between the realm of light and darkness. Physical damage is almost ineffective against you, but being ghostly, you can't take girls virginity."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["Illusive"]["label"] = "mc_setup_mage_arc_ghost_illusive"

        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["Creature of Light"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["Creature of Light"]["text"] = "Light spells heal you instead of dealing damage, but your Darkness spells are almost ineffective."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Ghost"]["Creature of Light"]["label"] = "mc_setup_mage_arc_ghost_light"

        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["header"] = "Vampire"
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["text"] = "For decades he hunted vampires, protecting citizens from these nocturnal predators. One day, while clearing a nest, he captured a vampire queen, but her seductiveness kept her alive and even gave birth to you."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["label"] = "mc_setup_mage_arc_vampire"
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["class"] = "Knight"

        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Creature of Night"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Creature of Night"]["text"] = "Darkness spells heal you instead of dealing damage, but your Light spells are almost ineffective."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Creature of Night"]["label"] = "mc_setup_mage_arc_vampire_night"

        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Blood Master"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Blood Master"]["text"] = "Only true vampires have access to blood magic, but your heritage still gives a few perks. Girls who lose their virginity to you, become more obedient."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Blood Master"]["label"] = "mc_setup_mage_arc_vampire_blood"

        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Perfect Reflexes"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Perfect Reflexes"]["text"] = "You inherited your mother's reflexes, which help to evade attacks. Sadly, mortal body is not suitable for vampire speed, affecting your health."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Perfect Reflexes"]["label"] = "mc_setup_mage_arc_vampire_reflex"
    return
