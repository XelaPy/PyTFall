label build_mc_stories:
    
    python:
        main_story = None # Fathers occupation
        sub_story = None # Father specific occupation
        mc_story = None # MCs mother
        mc_substory = None # MCs heritage
        
    $ mc_stories = OrderedDict() # Main Dictionary
    
    python:
        """
        MC Screens are built from this dictionaries and we expect them to have some values, 
        even if those values are just the empty dicts and/or images to be grayed out by the screen.
        
        OrderedDict() is a variation of dictionary that keeps the order of it's members.
        {} or dict() we use when we don't care about the order.
        """
        mc_stories["Merchant"] = {} # Merchant! This is the main branch displayed as the very first thing (four choices).
        mc_stories["Merchant"]["img"] = "content/gfx/interface/images/merchant.png" # Path to the icon representing the branch onscreen.
        mc_stories["Merchant"]["header"] = "Your father was a great merchant" # Header for the branch. Without a header, option is grayed out.
        mc_stories["Merchant"]["label"] = "mc_setup_merchant" # This decides a label to jump to in order to apply the effects.
        mc_stories["Merchant"]["class"] = "Mage" # As agreed, we will be adding a class to choices without clear descriptions.

        # Each from the subchoices should have it's own branch, since (in theory) we may wish to use different choices.
        # We simply iterate over the choices dictionary created ealier to make sure that all branches have defaults:

        # The following creates subchoices for Merchant such as Shopkeeper, Farm, Mone and etc:
        # This creates the buttons, they will be greyed out if no content exists for an option.
        mc_stories["Merchant"]["choices"] = OrderedDict(Caravan="content/gfx/interface/images/story/caravan/wagon35.png",
                                                                                       Farm="content/gfx/interface/images/hay35.png",
                                                                                       Ranch="content/gfx/interface/images/ranch35.png",
                                                                                       Mine="content/gfx/interface/images/Mine37.png",
                                                                                       Shopkeeper="content/gfx/interface/images/shop36.png",
                                                                                       Smuggler="content/gfx/interface/images/smuggler35.png",
                                                                                       Shipmaster="content/gfx/interface/images/shipmaster35.png",
                                                                                       Moneychanger="content/gfx/interface/images/coin30.png")
        
        # And finally we add text for these options, these names obviously have to match teh once provided in choices:
        mc_stories["Merchant"]["Caravan"] = {}
        mc_stories["Merchant"]["Caravan"]["text"] = "\n Maybe he didn't have own shop, but his caravan provides the city all necessary goods. Luck was on his side, he amassed considerable wealth, grateful friends, but also powerful enemies.\n Anticipating trouble, he left you at home. And on this day, luck deserted him. Caravan was looted. All people were killed and the father was gone.\n {color=#1E90FF}({/color}{color=#FFD700}+15k gold{/color}{color=#1E90FF},{/color}{color=#8470FF} +Intelligence{/color}{color=#1E90FF},{/color}{color=#DEB887} +Constitution{/color}{color=#1E90FF},{/color}{color=#00FA9A} +Luck{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["Caravan"]["label"] =  "mc_setup_merchant_caravan" # This decides a label to jump to in order to apply the effects.
        # This creates the other branch used on the right side of the screen:
        mc_stories["Merchant"]["MC"] = {} # Declare the main dictionary for the branch!
        
        # Each from the subchoices should have it's own branch, since (in theory) we may wish to use different choices.
        # We simply iterate over the choices dictionary created ealier to make sure that all branches have defaults:
        for key in mc_stories["Merchant"]["choices"]: # We create new dicts for all keys to avoid errors:
            mc_stories["Merchant"]["MC"][key] = {}
            mc_stories["Merchant"]["MC"][key]["choices"] = OrderedDict()
            
        """
        This is the dict with all of the options for MC for Merchant/Caravan branch!
        This also decided if the said options are shown or not, for example Commenting out:
        
        # l="Defender",
        
        Will remove defender MC choice and commenting out:
        
        # r0="Book",
        
        Will remove book option from Caravan MC choice.
        """
        mc_stories["Merchant"]["MC"]["Caravan"]["choices"] = OrderedDict(l="Defender",
                                                                                                                   l_img="content/gfx/interface/images/story/caravan/Warrior2.png",
                                                                                                                   l0="Sword",
                                                                                                                   l0_img="content/gfx/interface/images/story/caravan/sword1.bmp",
                                                                                                                   l1="Woman",
                                                                                                                   l1_img="content/gfx/interface/images/story/caravan/woman2.png",
                                                                                                                   l2="Money Bag",
                                                                                                                   l2_img="content/gfx/interface/images/story/caravan/money_bag3.png",
                                                                                                                   r="Muleteer",
                                                                                                                   r_img="content/gfx/interface/images/story/caravan/caravan.png",
                                                                                                                   r0="Book",
                                                                                                                   r0_img="content/gfx/interface/images/story/caravan/book1.png",
                                                                                                                   r1="Boots",
                                                                                                                   r1_img="content/gfx/interface/images/story/caravan/boots1.png",
                                                                                                                   r2="Bag",
                                                                                                                   r2_img="content/gfx/interface/images/story/caravan/bag2.png")
        
        # Texts for the said options:
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"] = {} 
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["header"] = "Defender of the caravan"
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["text"] = "Acting as a security guard at the father's caravan, you have gained some experience in the weapons handling. You become a little bit stronger and hardier {color=#1E90FF}({/color}{color=#E9967A}+Defence{/color}{color=#1E90FF},{/color}{color=#DEB887} + Constitution{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["label"] = "mc_setup_merchant_mc_defender"
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["class"] = "Warrior" # As agreed, we will be adding a class to choices without clear descriptions.
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["Sword"] = {}
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["Sword"]["text"] = "You cut down many heads with your favourite sword 'Bettie' {color=#1E90FF}({/color}{color=#FFD700}+Sword{/color}{color=#1E90FF},{/color} {color=#CD5C5C}+Attack{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["Sword"]["label"] = "mc_setup_merchant_mc_defender_sword"
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["Woman"] = {}
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["Woman"]["text"] = "During his travels, you become skilled in love games, when staying in various taverns {color=#1E90FF}({/color} {color=#FFAEB9}+Sex{/color}{color=#1E90FF},{/color}{color=#FF3E96}+Charisma{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["Money Bag"] = {}
        mc_stories["Merchant"]["MC"]["Caravan"]["Defender"]["Money Bag"]["text"] = "You didn't spend on drink the honestly earned money after each campaign, unlike the subordinates {color=#1E90FF}({/color}{color=#8470FF}+Intelligence{/color}{color=#1E90FF},{/color}{color=#FFD700}+1500 Gold{/color}{color=#1E90FF}){/color}"
        
        # Second part of the same:
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"] = {} 
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["header"] = "Muleteer"
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["text"] = "You personally ruled one of vans in the father's caravan. Because of a sedentary life you lose in a constitution a little, but in conversations you don't have the equal {color=#1E90FF}({/color}{color=#DEB887} -- Constitution{/color}{color=#1E90FF},{/color}{color=#8470FF} +Intelligence{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["class"] = "Manager" # As agreed, we will be adding a class to choices without clear descriptions.
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Book"] = {}
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Book"]["text"] = "On each halt books were your only friends {color=#1E90FF}({/color}{color=#8470FF} +Intelligence{/color}{color=#1E90FF},{/color}{color=#FFD700}+ Random Books{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Boots"] = {}
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Boots"]["text"] = "The driver of a caravan in sandals - definitely not about you. For your salary you bought good pair of boots {color=#1E90FF}({/color}{color=#00FA9A} +Luck{/color}{color=#1E90FF},{/color}{color=#FFD700}+ Random Boots{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Bag"] = {}
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Bag"]["text"] = "In your bag is always a few bottles of wine, and you often share them on halts. For what your subordinates are always glad to see you {color=#1E90FF}({/color}{color=#FF3E96}+Charisma{/color}{color=#1E90FF},{/color}{color=#FFD700}+ Random Wine Bottles{/color}{color=#1E90FF}){/color}"

        mc_stories["Warrior"] = {}
        mc_stories["Warrior"]["img"] = "content/gfx/interface/images/warriorP.png"
        mc_stories["Warrior"]["header"] = "Your father was a skilled fighter..."
        mc_stories["Warrior"]["choices"] = OrderedDict(Warrior="content/gfx/interface/images/mc/warrior_m.png",
                                                       Defender="content/gfx/interface/images/mc/defender_m.png",
                                                       Shooter="content/gfx/interface/images/mc/shooter_m.png",
                                                       Assassin="content/gfx/interface/images/mc/assassin_m.png")
        mc_stories["Warrior"]["Warrior"] = {}
        mc_stories["Warrior"]["Warrior"]["class"] = "Warrior"
        mc_stories["Warrior"]["Warrior"]["text"] = "He was a famous gladiator. Decades of fighting at the arena made him competent with almost every known weapon, and brought fame and wealth."
        mc_stories["Warrior"]["Assassin"] = {}
        mc_stories["Warrior"]["Assassin"]["class"] = "Assassin"
        mc_stories["Warrior"]["Assassin"]["text"] = "He was a deadly assassin. Not even royalties were safe from his blade, if the price was right of course."
        mc_stories["Warrior"]["Shooter"] = {}
        mc_stories["Warrior"]["Shooter"]["class"] = "Shooter"
        mc_stories["Warrior"]["Shooter"]["text"] = "He was a skilled marksman. For many years he, together with other rangers, hunted monsters and smugglers."
        mc_stories["Warrior"]["Defender"] = {}
        mc_stories["Warrior"]["Defender"]["class"] = "Defender"
        mc_stories["Warrior"]["Defender"]["text"] = "He was an experienced bodyguard. His skills secured him a place in high society, where he guarded royalties."
        
        mc_stories["Warrior"]["MC"] = {}
        for key in mc_stories["Warrior"]["choices"]:
            mc_stories["Warrior"]["MC"][key] = {}
            mc_stories["Warrior"]["MC"][key]["choices"] = OrderedDict()

        mc_stories["Warrior"]["MC"]["Defender"]["choices"] = OrderedDict(l="Royal Guard",
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
                                                                        
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"] = {} 
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["header"] = "Royal Guard"
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["text"] = "Many years of exemplary service made him the captain of the palace guards. It was then that he met your future mother, a young novice knight from a poor, but noble family."
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["label"] = "mc_setup_warrior_defender_guard"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Royal Defender"] = {}
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Royal Defender"]["text"] = "You know a lot about armor from your parents. Equipment gives additional defense based on its price."
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Royal Defender"]["label"] = "mc_setup_warrior_defender_guard_armor"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Left-Handed"] = {}
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Left-Handed"]["text"] = "You are left-handed, just like your mother. Equipment in your left hand (such as shields) is significantly more powerful, but equipment in your right hand (such as weapons) is less effective."
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Left-Handed"]["label"] = "mc_setup_warrior_defender_guard_left"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Shield Master"] = {}
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Shield Master"]["text"] = "Your mother taught you here fighting style. All shields are a bit more powerful than usual."
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Shield Master"]["label"] = "mc_setup_warrior_defender_guard_shield"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"] = {} 
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["header"] = "Harpy"
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["text"] = "Eventually he was given the task to guard a harpy priestess who was also the ambassador of her race at that time. Unable to move freely around the city due to her status, she gladly accepted him as the main source of entertainment, what led to your birth."
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["label"] = "mc_setup_warrior_defender_harpy"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Hollow Bones"] = {}
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Hollow Bones"]["text"] = "Evolution gave harpies hollow bones which make their bodies significantly lighter. It makes you weaker against physical attacks, but completely neutralizes any equipment penalties to agility."
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Hollow Bones"]["label"] = "mc_setup_warrior_defender_harpy_bones"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Effective Metabolism"] = {}
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Effective Metabolism"]["text"] = "To have enough energy for flight harpies should very quickly digest food without residues. All consumables that restore vitality are more effective, especially food."
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Effective Metabolism"]["label"] = "mc_setup_warrior_defender_harpy_meta"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Sky Ward"] = {}
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Sky Ward"]["text"] = "Due to their mystical connection with the sky, harpies are one of the fastest flyers in the world. You cannot be as fast without wings, but it still helps (+ 1 Action Point and additional agility)."
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Sky Ward"]["label"] = "mc_setup_warrior_defender_harpy_sky"
        

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
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["text"] = "Over the years he had to work together with elven rangers. In time, mistrust gave way to friendship and, eventually, to close relationships with one of them."
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["label"] = "mc_setup_warrior_shooter_forest_elf"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Sniper"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Sniper"]["text"] = "Your mother taught you to use bows like forest elves do. All bows are a bit more powerful than usual."
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Sniper"]["label"] = "mc_setup_warrior_shooter_forest_elf_sniper"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Farsightedness"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Farsightedness"]["text"] = "Due to specialization in shooting, over time some forest elves lost the ability to effectively fight in close combat, but became even better shooters."
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Farsightedness"]["label"] = "mc_setup_warrior_shooter_forest_elf_ranger"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Ranger"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Ranger"]["text"] = "Your mother taught you the ways of elves. Most ranged weapons don't give you penalties to defense."
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Ranger"]["label"] = "mc_setup_warrior_shooter_forest_elf_ranger"
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Ranger"]["class"] = "Assassin"

        
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"] = {} 
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["header"] = "Summer Fay"
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["text"] = "Century after century Fae fulfill the same functions in their forest Courts, unable to change their roles or even die once and for all. Summer Fae represent growth and the emergence of life, and making children with other races proves it like nothing else."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["label"] = "mc_setup_warrior_shooter_summer_fay"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Eternality"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Eternality"]["text"] = "Your body inherited some of your mother's unchangeability. You body restores third of max health every day, but healing items are almost ineffective."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Eternality"]["label"] = "mc_setup_warrior_shooter_summer_fay_eternal"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Summer Affinity"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Summer Affinity"]["text"] = "You inherited some of your mother's mystic powers. You can use Summer Arrow skill in battle, and Fire and Light are not very effective against you."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Summer Affinity"]["label"] = "mc_setup_warrior_shooter_summer_fay_affinity"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Life Beacon"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Life Beacon"]["text"] = "Your Fae inheritance gives you aura of life which regenerates some health for all characters under your command every day and makes them a bit happier."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Life Beacon"]["label"] = "mc_setup_warrior_shooter_summer_fay_beacon"
            
                                                                        
        mc_stories["Warrior"]["MC"]["Assassin"]["choices"] = OrderedDict(l="Princess",
                                                                        l_img="content/gfx/interface/images/mc/princess.jpg",
                                                                        l0="Knight",
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
                                                                        r2="Inhuman Flexibility",
                                                                        r2_img="content/gfx/interface/images/mc/flex.png")
                                                                        
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"] = {} 
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["header"] = "Princess"
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["text"] = "Once someone hired him to eliminate a foreign princess visiting the city on a diplomatic mission. No one has seen them since then. Except you, their son."
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["label"] = "mc_setup_warrior_assassin_princess"

        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Knight"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Knight"]["text"] = "You learned from your mother about knightly combat style, usually available only for members of the royal families. Defense given by armor is a bit higher than usual."
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Knight"]["label"] = "mc_setup_warrior_assassin_princess_knight"
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Knight"]["class"] = "Defender"
        
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Fencer"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Fencer"]["text"] = "You learned from your mother about fencing style, usually available only for members of the royal families. All swords are a bit more powerful than usual."
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Fencer"]["label"] = "mc_setup_warrior_assassin_princess_fencer"
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Fencer"]["class"] = "Warrior"
        
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Royal Assassin"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Royal Assassin"]["text"] = "Due to your heritage, you used to use only the best equipment. The more expensive equipped items, the more attack you get."
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Royal Assassin"]["label"] = "mc_setup_warrior_assassin_princess_royal"
        
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"] = {} 
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["header"] = "Drow"
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["text"] = "During assassinations your father often encountered competitors. Usually he eliminated them along with the target, but one particularly skilled assassin kept evading his deadly strikes. It was your future mother, alone elf from the distant underground world. Impressed by the skill of each other, they joined forces."
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["label"] = "mc_setup_warrior_assassin_drow"
        
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Poison Master"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Poison Master"]["text"]= "You know a lot about poisons from your mother. Poisons are much less effective against you, and your poison attacks much are stronger."
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Poison Master"]["label"] = "mc_setup_warrior_assassin_drow_poison"
        
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["High-Speed Fencer"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["High-Speed Fencer"]["text"]= "You learned from your mother about rare combat style used by drow assassins. All daggers are a bit more powerful than usual."
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["High-Speed Fencer"]["label"] = "mc_setup_warrior_assassin_drow_dagger"
        
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Inhuman Flexibility"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Inhuman Flexibility"]["text"]= "You inherited all your mother's flexibility. It helps to evade attacks and also, to some extent, helps in bed."
        mc_stories["Warrior"]["MC"]["Assassin"]["Drow"]["Inhuman Flexibility"]["label"] = "mc_setup_warrior_assassin_drow_flex"
            
        mc_stories["Warrior"]["MC"]["Warrior"]["choices"] = OrderedDict(l="Amazon",
                                                                        l_img="content/gfx/interface/images/mc/amazon.jpg",
                                                                        l0="Training",
                                                                        l0_img="content/items/misc/std.png",
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
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["text"] = "It was there that he met your mother, an amazon from a remote tribe. After defeating her in battle, he took her body instead of taking her life."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["label"] = "mc_setup_warrior_warrior_amazon"

        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Training"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Training"]["text"] = "Your mother watched over your training since childhood. As a result, your body is in a great condition (+ vitality and health)."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Training"]["label"] = "mc_setup_warrior_warrior_amazon_training"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Muscle"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Muscle"]["text"] = "You inherited your mother's strength. Melee weapons deal more damage than usual."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Muscle"]["label"] = "mc_setup_warrior_warrior_amazon_muscle"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Berserk"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Berserk"]["text"] = "Your mother taught you here fighting style. All defense bonuses from equipment are lower, but all attack bonuses are higher."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Berserk"]["label"] = "mc_setup_warrior_warrior_amazon_berserk"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"] = {} 
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["header"] = "Dragon"
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["text"] = "It was there that he met your mother, one of the last representatives of a dying race of half-dragons. Being a monster, she was supposed to fight him to the death in the Beast Fights, but her dislike for clothes changed his mind."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["label"] = "mc_setup_warrior_warrior_dragon"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Fire"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Fire"]["text"] = "Your body is covered with tiny flakes. They are almost inconspicuous, but at higher temperatures they actively absorb and dissipate heat, making fire and, to some extent, electricity ineffective."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Fire"]["label"] = "mc_setup_warrior_warrior_dragon_fire"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Stone"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Stone"]["text"] = "Your body is covered with tiny flakes. They are almost inconspicuous, but upon impact they become solid as stone, softening the blow (+earth and physical resistance)."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Stone"]["label"] = "mc_setup_warrior_warrior_dragon_stone"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Dragon Sight"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Dragon Sight"]["text"] = "Dragons have perfect distance vision, and so do you. You are competent with ranged weapons and have slightly increased critical damage."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Dragon Sight"]["label"] = "mc_setup_warrior_warrior_dragon_sight"
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Dragon Sight"]["class"] = "Shooter"
        
        
        # We add the rest of the options:
        mc_stories["Mage"] = {}
        mc_stories["Mage"]["img"] = "content/gfx/interface/images/magicP.png"
        mc_stories["Mage"]["header"] = "Your father was a powerful mage..."
        mc_stories["Mage"]["choices"] = OrderedDict()
        
        mc_stories["Mage"]["choices"]["Arcane Knight"] = "content/gfx/interface/images/mc/arc.png"
        mc_stories["Mage"]["choices"]["Steam"] = "content/gfx/interface/images/mc/fi.png"
                                                       
        mc_stories["Mage"]["Arcane Knight"] = {}
        mc_stories["Mage"]["Arcane Knight"]["class"] = "Defender"
        mc_stories["Mage"]["Arcane Knight"]["text"] = "As an Arcane Knight, he specialized in extermination of dangerous magical creatures which constantly threaten the city."
        
        mc_stories["Mage"]["Steam"] = {}
        mc_stories["Mage"]["Steam"]["class"] = "Mage"
        mc_stories["Mage"]["Steam"]["text"] = "He chose to learn the secrets of fire and ice."
                                                       
        mc_stories["Mage"]["MC"] = {}
        for key in mc_stories["Mage"]["choices"]:
            mc_stories["Mage"]["MC"][key] = {}
            mc_stories["Mage"]["MC"][key]["choices"] = OrderedDict()
            
        mc_stories["Mage"]["MC"]["Steam"]["choices"] = OrderedDict(l="Lampad",
                                                                   l_img="content/gfx/interface/images/mc/fire.jpg"
                                                                      )
            
        mc_stories["Mage"]["MC"]["Arcane Knight"]["choices"] = OrderedDict(l="Angel",
                                                                      l_img="content/gfx/interface/images/mc/angel.jpg",
                                                                      l0="Intangible",
                                                                      l0_img="content/gfx/interface/images/mc/illusion_1.png",
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
                                                                      
        mc_stories["Mage"]["MC"]["Steam"]["Lampad"] = {} 
        mc_stories["Mage"]["MC"]["Steam"]["Lampad"]["header"] = "Lampad"
        mc_stories["Mage"]["MC"]["Steam"]["Lampad"]["text"] = "Lampads are immortal nymphs from the elemental plane of Fire. Friendly and flirty, they like to travel between worlds in search of entertainment, rarely staying in one place for more than one year."
        mc_stories["Mage"]["MC"]["Steam"]["Lampad"]["label"] = "mc_setup_mage_steam_lampad"
                                                                      
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"] = {} 
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["header"] = "Angel"
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["text"] = "Most high angels don't care about carnal pleasures. And when they do, they get banished to the world of mortals. Being one of them, your mother decided to destroy the world of mortals to earn forgiveness of the Heaven, but your father with a group of adventurers ruined her plans and taught her the ways of mortals."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["label"] = "mc_setup_mage_shadow_angel"
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["class"] = "Mage"
        
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["Intangible"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["Intangible"]["text"] = "You are not entirely suitable for the world of mortals, just like your mother. All attacks and magic are less effective against you, but all your attacks and magic are less effective too."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["Intangible"]["label"] = "mc_setup_mage_shadow_angel_intangible"
        
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["Illusive"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["Illusive"]["text"] = "Due to your heritage, you exist between the realm of light and mortal reality. Physical damage is not a big problem for you, but it leads to unusual results during intimacy."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["Illusive"]["label"] = "mc_setup_mage_shadow_angel_illusive"
        
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["Creature of Light"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["Creature of Light"]["text"] = "Light spells now heal you instead of hurting, but your Water and Ice spells are a bit less effective."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Angel"]["Creature of Light"]["label"] = "mc_setup_mage_shadow_angel_light"
        
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"] = {} 
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["header"] = "Vampire"
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["text"] = "For decades he with other knights hunted vampires, protecting citizens from the nocturnal predators. Eventually he even captured the local vampire queen, but her seductiveness kept her alive and even gave birth to you."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["label"] = "mc_setup_mage_shadow_vampire"
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["class"] = "Mage"
        
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Creature of Night"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Creature of Night"]["text"] = "Darkness spells now heal you instead of hurting, but your Fire and Electricity spells are a bit less effective."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Creature of Night"]["label"] = "mc_setup_mage_shadow_vampire_night"
        
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Blood Master"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Blood Master"]["text"] = "Only pure vampires have access to blood magic, but your heritage still gives a few perks when blood is involved. Girls whose virginity was taken by you are more obedient."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Blood Master"]["label"] = "mc_setup_mage_shadow_vampire_blood"
        
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Perfect Reflexes"] = {}
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Perfect Reflexes"]["text"] = "You inherited your mother's reflexes, which helps to evade attacks. Sadly, mortal body is not suitable for vampire speed, which affected you health."
        mc_stories["Mage"]["MC"]["Arcane Knight"]["Vampire"]["Perfect Reflexes"]["label"] = "mc_setup_mage_shadow_vampire_reflex"
                                                       
        mc_stories["Noble"] = {}
        mc_stories["Noble"]["img"] = "content/gfx/interface/images/nobleP.png"
        mc_stories["Noble"]["choices"] = OrderedDict()
        
    return
