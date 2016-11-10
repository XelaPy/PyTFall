label build_mc_stories:
    
    python:
        main_story = None # Fathers occupation
        sub_story = None # Father specific occupation
        mc_story = None # MCs mother
        mc_substory = None # MCs "Hobby"
        
    $ mc_stories = OrderedDict() # Main Dictionary
    
    python:
        """
        MC Screens are built from this dictionaries and we expect them to have some values, 
        even if those values are just the empty dicts and/or images to be greyed out by the screen.
        
        OrderedDict() is a variation of dictionary that keeps the order of it's members.
        {} or dict() we use when we don't care about the order.
        """
        mc_stories["Merchant"] = {} # Merchant! This is the main branch displayed as the very first thing (four choices).
        mc_stories["Merchant"]["img"] = "content/gfx/interface/images/merchant.png" # Path to the icon representing the branch onscreen.
        mc_stories["Merchant"]["header"] = "Your father was a great merchant" # Header for the branch. Without a header, option is greyed out.
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
        mc_stories["Warrior"]["label"] = "mc_setup_warrior"
        
        mc_stories["Warrior"]["choices"] = OrderedDict(Warrior="content/gfx/interface/images/mc/warrior_m.png",
                                                       Defender="content/gfx/interface/images/mc/defender_m.png",
                                                       Shooter="content/gfx/interface/images/mc/shooter_m.png",
                                                       Assassin="content/gfx/interface/images/mc/assassin_m.png")
        mc_stories["Warrior"]["Warrior"] = {}
        mc_stories["Warrior"]["Warrior"]["class"] = "Warrior"
        mc_stories["Warrior"]["Warrior"]["text"] = "He was a famous gladiator. Decades of fighting at the arena made him competent with almost every known weapon, and brought fame and wealth."
        mc_stories["Warrior"]["Warrior"]["label"] = "mc_setup_warrior_warrior"
        mc_stories["Warrior"]["Assassin"] = {}
        mc_stories["Warrior"]["Assassin"]["class"] = "Assassin"
        mc_stories["Warrior"]["Assassin"]["text"] = "He was a deadly assassin. Not even royalties were safe from his blade, if the price was right of course."
        mc_stories["Warrior"]["Assassin"]["label"] = "mc_setup_warrior_assassin"
        mc_stories["Warrior"]["Shooter"] = {}
        mc_stories["Warrior"]["Shooter"]["class"] = "Shooter"
        mc_stories["Warrior"]["Shooter"]["text"] = "He was a skilled marksman. For many years he, together with other rangers, hunted monsters and smugglers."
        mc_stories["Warrior"]["Shooter"]["label"] = "mc_setup_warrior_shooter"
        mc_stories["Warrior"]["Defender"] = {}
        mc_stories["Warrior"]["Defender"]["class"] = "Defender"
        mc_stories["Warrior"]["Defender"]["text"] = "He was an experienced bodyguard. His skills secured him a place in high society, where he guarded royalties."
        mc_stories["Warrior"]["Defender"]["label"] = "mc_setup_warrior_defender"
        
        mc_stories["Warrior"]["MC"] = {}
        for key in mc_stories["Warrior"]["choices"]:
            mc_stories["Warrior"]["MC"][key] = {}
            mc_stories["Warrior"]["MC"][key]["choices"] = OrderedDict()

        mc_stories["Warrior"]["MC"]["Defender"]["choices"] = OrderedDict(l="Royal Guard",
                                                                        l_img="content/gfx/interface/images/mc/knight.jpg",
                                                                        l0="Armor Expert",
                                                                        l0_img="content/items/body/mail.png",
                                                                        l1="Left-Handed",
                                                                        l1_img="content/gfx/interface/images/mc/left_hand.png",
                                                                        l2="Big Heritage",
                                                                        l2_img="content/gfx/interface/images/mc/divider.png",
                                                                        r="Harpy",
                                                                        r_img="content/gfx/interface/images/mc/harpy.jpg",
                                                                        r0="Hollow Bones",
                                                                        r0_img="content/gfx/interface/images/mc/bones.png"
                                                                        )
                                                                        
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"] = {} 
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["header"] = "Royal Guard"
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["text"] = "Many years of exemplary service made him the captain of the palace guards. It was then that he met your future mother, a young novice knight from a poor, but noble family."
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["label"] = "mc_setup_warrior_defender_guard"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Armor Expert"] = {}
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Armor Expert"]["text"] = "You know a lot about armor from your parents. All armor bonuses to stats are a bit more effective than usual."
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Armor Expert"]["label"] = "mc_setup_warrior_defender_guard_armor"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Left-Handed"] = {}
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Left-Handed"]["text"] = "You are left-handed, just like your mother. Equipment in your left hand (such as shields) is significantly more powerful, but equipment in your right hand (such as weapons) is less effective."
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Left-Handed"]["label"] = "mc_setup_warrior_defender_guard_left"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Big Heritage"] = {}
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Big Heritage"]["text"] = "Your mother's family may be poor, but they have good genes. Due to your ancestry, the certain part of your body is a bit thicker than than that of most people. That makes anal sex much harder, but gives you unmatched performance in the other hole."
        mc_stories["Warrior"]["MC"]["Defender"]["Royal Guard"]["Big Heritage"]["label"] = "mc_setup_warrior_defender_guard_big"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"] = {} 
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["header"] = "Harpy"
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["text"] = "Eventually he was given the task to guard a harpy priestess who was also the ambassador of her race at that time. Unable to move freely around the city due to her status, she gladly accepted him as the main source of entertainment, what led to your birth."
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["label"] = "mc_setup_warrior_defender_harpy"
        
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Hollow Bones"] = {}
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Hollow Bones"]["text"] = "Evolution gave harpies hollow bones which make their bodies significantly lighter. It makes you weaker against physical attacks, but completely neutralizes any equipment penalties to agility."
        mc_stories["Warrior"]["MC"]["Defender"]["Harpy"]["Hollow Bones"]["label"] = "mc_setup_warrior_defender_harpy_bones"

        mc_stories["Warrior"]["MC"]["Shooter"]["choices"] = OrderedDict(l="Forest Elf",
                                                                        l_img="content/gfx/interface/images/mc/forest_elf.jpg",
                                                                        l0="Sniper",
                                                                        l0_img="content/items/weapon/eb.png",
                                                                        l1="Ranger",
                                                                        l1_img="content/gfx/interface/images/mc/ranger.png",
                                                                        l2="Elven Features",
                                                                        l2_img="content/gfx/interface/images/mc/divider.png",
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
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Ranger"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Ranger"]["text"] = "You know a lot about surviving outside of the city from your parents. Your exploration skills are second to none." # we don't have SE atm. When we will, it will give something special too
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Ranger"]["label"] = "mc_setup_warrior_shooter_forest_elf_ranger"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Features"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Features"]["text"] = "Due to your ancestry, the certain part of your body is a bit thinner than you would like. Although, not as thin as that of pureblood male elves. That makes anal sex easier, but you have to try harder in the other hole."
        mc_stories["Warrior"]["MC"]["Shooter"]["Forest Elf"]["Elven Features"]["label"] = "mc_setup_warrior_shooter_forest_elf_features"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"] = {} 
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["header"] = "Summer Fay"
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["text"] = "Century after century Fae fulfill the same functions in their forest Courts, unable to change their roles or even die once and for all. Summer Fae represent growth and the emergence of life, and making children with other races proves it like nothing else."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["label"] = "mc_setup_warrior_shooter_summer_fay"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Eternality"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Eternality"]["text"] = "Your body inherited some of your mother's unchangeability. You body restores third of max health every day, but healing items are almost ineffective."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Eternality"]["label"] = "mc_setup_warrior_shooter_summer_fay_eternal"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Summer Affinity"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Summer Affinity"]["text"] = "You inherited some of your mother's mystic powers. You can use Summer Arrow skill in battle, and Fire and Light are not very effective against you. On the other hand, Ice and Darkness are bad news."
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Summer Affinity"]["label"] = "mc_setup_warrior_shooter_summer_fay_affinity"
        
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Life Beacon"] = {}
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Life Beacon"]["text"] = "Your Fae inheritance gives you aura of life which strengthens the instinct of reproduction. Virgins will never refuse to let you in during intimacy, and all girls will be happier and healthier after intercourse." # might add more if we'll have pregnancy in the future
        mc_stories["Warrior"]["MC"]["Shooter"]["Summer Fay"]["Life Beacon"]["label"] = "mc_setup_warrior_shooter_summer_fay_beacon"
            
                                                                        
        mc_stories["Warrior"]["MC"]["Assassin"]["choices"] = OrderedDict(l="Princess",
                                                                        l_img="content/gfx/interface/images/mc/princess.jpg",
                                                                        l0="Knight",
                                                                        l0_img="content/items/sweapon/bks.png",
                                                                        l1="Fencer",
                                                                        l1_img="content/items/weapon/og.png",
                                                                        l2="Sister Lover",
                                                                        l2_img="content/gfx/interface/images/mc/sister.png",
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
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Knight"]["text"] = "You learned from your mother about knightly combat style, usually available only for members of the royal families. All defense given by equipment is a bit higher than usual."
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Knight"]["label"] = "mc_setup_warrior_assassin_princess_knight"
        
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Fencer"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Fencer"]["text"] = "You learned from your mother about fencing style, usually available only for members of the royal families. All swords are a bit more powerful than usual."
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Fencer"]["label"] = "mc_setup_warrior_assassin_princess_fencer"
        
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Sister Lover"] = {}
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Sister Lover"]["text"] = "Incest is extremely common in royal families, and you know a lot about it from your mother stories. Characters with Half-Sister trait will not reject you due to kinship and have more starting disposition."
        mc_stories["Warrior"]["MC"]["Assassin"]["Princess"]["Sister Lover"]["label"] = "mc_setup_warrior_assassin_princess_sister"
        
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
                                                                        l2="Yuri",
                                                                        l2_img="content/gfx/interface/images/mc/amazon_yuri.png",
                                                                        r="Dragon",
                                                                        r_img="content/gfx/interface/images/mc/dragon.jpg",
                                                                        r0="Fire",
                                                                        r0_img="content/gfx/interface/images/mc/fire_dragon.jpg",
                                                                        r1="Stone",
                                                                        r1_img="content/gfx/interface/images/mc/stone_dragon.jpg",
                                                                        r2="Defiler",
                                                                        r2_img="content/gfx/interface/images/mc/defiler_dragon.jpg")
                                                                        

                                                                        
                                                                        
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"] = {} 
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["header"] = "Amazon"
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["text"] = "It was there that he met your mother, an amazon from a remote tribe. After defeating her in battle, he took her body instead of taking her life."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["label"] = "mc_setup_warrior_warrior_amazon"

        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Training"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Training"]["text"] = "Your mother watched over your training since childhood. As a result, your body is in a great condition (+ max vitality)."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Training"]["label"] = "mc_setup_warrior_warrior_amazon_training"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Muscle"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Muscle"]["text"] = "You inherited your mother's strength. Melee weapons deal more damage than usual."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Muscle"]["label"] = "mc_setup_warrior_warrior_amazon_muscle"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Yuri"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Yuri"]["text"] = "You know a lot about lesbians from your Amazon mother. Lesbian characters will not reject you due to your gender, and your oral skill is pretty good."
        mc_stories["Warrior"]["MC"]["Warrior"]["Amazon"]["Yuri"]["label"] = "mc_setup_warrior_warrior_amazon_yuri"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"] = {} 
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["header"] = "Dragon"
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["text"] = "It was there that he met your mother, one of the last representatives of a dying race of half-dragons. Being a monster, she was supposed to fight him to the death in the Beast Fights, but her dislike for clothes changed his mind."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["label"] = "mc_setup_warrior_warrior_dragon"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Fire"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Fire"]["text"] = "Your body is covered with tiny flakes. They are almost inconspicuous, but at higher temperatures they actively absorb and dissipate heat, making fire ineffective."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Fire"]["label"] = "mc_setup_warrior_warrior_dragon_fire"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Stone"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Stone"]["text"] = "Your body is covered with tiny flakes. They are almost inconspicuous, but upon impact they become solid as stone, softening the blow."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Stone"]["label"] = "mc_setup_warrior_warrior_dragon_stone"
        
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Defiler"] = {}
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Defiler"]["text"] = "Your body is covered with tiny flakes. They are almost inconspicuous, but they can make certain parts of your skin scabrous, which helps during intimacy."
        mc_stories["Warrior"]["MC"]["Warrior"]["Dragon"]["Defiler"]["label"] = "mc_setup_warrior_warrior_dragon_defiler"
        
        
        # We add the rest of the options:
       

        mc_stories["Scholar"] = {}
        mc_stories["Scholar"]["img"] = "content/gfx/interface/images/magicP.png"
        mc_stories["Scholar"]["choices"] = OrderedDict()
        mc_stories["Noble"] = {}
        mc_stories["Noble"]["img"] = "content/gfx/interface/images/nobleP.png"
        mc_stories["Noble"]["choices"] = OrderedDict()
        
    return
