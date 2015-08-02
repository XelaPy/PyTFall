label build_mc_stories:
    
    python:
        main_story = None # Fathers occupation
        sub_story = None # Father specific occupation
        mc_story = None # MCs occupation
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
        
        # We add the rest of the options:
        mc_stories["Warrior"] = {}
        mc_stories["Warrior"]["img"] = "content/gfx/interface/images/warriorP.png"
        mc_stories["Warrior"]["choices"] = OrderedDict()
        mc_stories["Warrior"]["MC"] = {}
        mc_stories["Scholar"] = {}
        mc_stories["Scholar"]["img"] = "content/gfx/interface/images/magicP.png"
        mc_stories["Scholar"]["choices"] = OrderedDict()
        mc_stories["Noble"] = {}
        mc_stories["Noble"]["img"] = "content/gfx/interface/images/nobleP.png"
        mc_stories["Noble"]["choices"] = OrderedDict()
        
        
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
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Book"] = {}
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Book"]["text"] = "On each halt books were your only friends {color=#1E90FF}({/color}{color=#8470FF} +Intelligence{/color}{color=#1E90FF},{/color}{color=#FFD700}+ Random Books{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Boots"] = {}
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Boots"]["text"] = "The driver of a caravan in sandals - definitely not about you. For your salary you bought good pair of boots {color=#1E90FF}({/color}{color=#00FA9A} +Luck{/color}{color=#1E90FF},{/color}{color=#FFD700}+ Random Boots{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Bag"] = {}
        mc_stories["Merchant"]["MC"]["Caravan"]["Muleteer"]["Bag"]["text"] = "In your bag is always a few bottles of wine, and you often share them on halts. For what your subordinates are always glad to see you {color=#1E90FF}({/color}{color=#FF3E96}+Charisma{/color}{color=#1E90FF},{/color}{color=#FFD700}+ Random Wine Bottles{/color}{color=#1E90FF}){/color}"
        
    return
