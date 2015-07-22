label mc_setup:
    python:
        # Get the images:
        mc_pics = load_mc_images()
        mc_class = "Warrior"
        total_points = 0
        
        main_story = None # Fathers occupation
        sub_story = None # Father specific occupation
        mc_story = None # MCs occupation
        mc_substory = None # MCs "Hobby"
        
        mc_stories = {} # Main Dictionary
        
        mc_stories["Merchant"] = {} # Merchant:
        mc_stories["Merchant"]["header"] = "Your father was a great merchant"
        mc_stories["Merchant"]["Caravan"] = "\n Maybe he didn't have own shop, but his caravan provides the city all necessary goods. Luck was on his side, he amassed considerable wealth, grateful friends, but also powerful enemies.\n Anticipating trouble, he left you at home. And on this day, luck deserted him. Caravan was looted. All people were killed and the father was gone.\n {color=#1E90FF}({/color}{color=#FFD700}+15k gold{/color}{color=#1E90FF},{/color}{color=#8470FF} +Intelligence{/color}{color=#1E90FF},{/color}{color=#DEB887} +Constitution{/color}{color=#1E90FF},{/color}{color=#00FA9A} +Luck{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["choices"] = OrderedDict(Caravan="content/gfx/interface/images/story/caravan/wagon35.png",
                                                                                       Farm="content/gfx/interface/images/hay35.png",
                                                                                       Ranch="content/gfx/interface/images/ranch35.png",
                                                                                       Mine="content/gfx/interface/images/Mine37.png",
                                                                                       Shopkeeper="content/gfx/interface/images/shop36.png",
                                                                                       Smuggler="content/gfx/interface/images/smuggler35.png",
                                                                                       Shipmaster="content/gfx/interface/images/shipmaster35.png",
                                                                                       Moneychanger="content/gfx/interface/images/coin30.png")
        
        mc_stories["Merchant"]["MC"] = {} # Merchant Family MC personal choices:
        for key in mc_stories["Merchant"]["choices"]: # We create new dicts for all keys to avoid errors:
            mc_stories["Merchant"]["MC"][key] = {}
            mc_stories["Merchant"]["MC"][key]["choices"] = OrderedDict()
        mc_stories["Merchant"]["MC"]["Caravan"]["choices"] = OrderedDict(l="Defender",
                                                                                                                   l_img="content/gfx/interface/images/story/caravan/Warrior2.png",
                                                                                                                   l0="Sword",
                                                                                                                   l0_img="content/gfx/interface/images/story/caravan/sword1.bmp",
                                                                                                                   l1="Woman",
                                                                                                                   l1_img="content/gfx/interface/images/story/caravan/woman2.png",
                                                                                                                   l2="Money Bag",
                                                                                                                   l2_img="content/gfx/interface/images/story/caravan/money_bag3.png",
                                                                                                                   r="Caravan",
                                                                                                                   r_img="content/gfx/interface/images/story/caravan/caravan.png",
                                                                                                                   r0="Book",
                                                                                                                   r0_img="content/gfx/interface/images/story/caravan/book1.png",
                                                                                                                   r1="Boots",
                                                                                                                   r1_img="content/gfx/interface/images/story/caravan/boots1.png",
                                                                                                                   r2="Bag",
                                                                                                                   r2_img="content/gfx/interface/images/story/caravan/bag2.png")
        mc_stories["Merchant"]["MC"]["Defender"] = {} # Sub sub choices, Main: Caravan (Could theoretically be anything), sub = Defender
        mc_stories["Merchant"]["MC"]["Defender"]["header"] = "Defender of the caravan"
        mc_stories["Merchant"]["MC"]["Caravan"]["header"] = "Muleteer"
        mc_stories["Merchant"]["MC"]["Caravan"]["text"] = "You personally ruled one of vans in the father's caravan. Because of a sedentary life you lose in a constitution a little, but in conversations you don't have the equal {color=#1E90FF}({/color}{color=#DEB887} -- Constitution{/color}{color=#1E90FF},{/color}{color=#8470FF} +Intelligence{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Defender"]["text"] = "Acting as a security guard at the father's caravan, you have gained some experience in the weapons handling. You become a little bit stronger and hardier {color=#1E90FF}({/color}{color=#E9967A}+Defence{/color}{color=#1E90FF},{/color}{color=#DEB887} + Constitution{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Defender"]["Sword"] = "You cut down many heads with your favourite sword 'Bettie' {color=#1E90FF}({/color}{color=#FFD700}+Sword{/color}{color=#1E90FF},{/color} {color=#CD5C5C}+Attack{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Defender"]["Woman"] = "During his travels, you become skilled in love games, when staying in various taverns {color=#1E90FF}({/color} {color=#FFAEB9}+Sex{/color}{color=#1E90FF},{/color}{color=#FF3E96}+Charisma{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Defender"]["Money Bag"] = "You didn't spend on drink the honestly earned money after each campaign, unlike the subordinates {color=#1E90FF}({/color}{color=#8470FF}+Intelligence{/color}{color=#1E90FF},{/color}{color=#FFD700}+1500 Gold{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Book"] = "On each halt books were your only friends {color=#1E90FF}({/color}{color=#8470FF} +Intelligence{/color}{color=#1E90FF},{/color}{color=#FFD700}+ Random Books{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Boots"] = "The driver of a caravan in sandals - definitely not about you. For your salary you bought good pair of boots {color=#1E90FF}({/color}{color=#00FA9A} +Luck{/color}{color=#1E90FF},{/color}{color=#FFD700}+ Random Boots{/color}{color=#1E90FF}){/color}"
        mc_stories["Merchant"]["MC"]["Caravan"]["Bag"] = "In your bag is always a few bottles of wine, and you often share them on halts. For what your subordinates are always glad to see you {color=#1E90FF}({/color}{color=#FF3E96}+Charisma{/color}{color=#1E90FF},{/color}{color=#FFD700}+ Random Wine Bottles{/color}{color=#1E90FF}){/color}"
        
        mc_stories["Warrior"] = {}
        mc_stories["Warrior"]["choices"] = OrderedDict()
        mc_stories["Warrior"]["MC"] = {}
        mc_stories["Scholar"] = {}
        mc_stories["Scholar"]["choices"] = OrderedDict()
        mc_stories["Noble"] = {}
        mc_stories["Noble"]["choices"] = OrderedDict()
        
        # mc
        
    scene bg mc_setup
    show screen mc_setup
    with dissolve
    
    $ global_flags.set_flag("game_start")
    
    python:
        while 1:
            result = ui.interact()
            
            if result[0] == "control":
                if result[1] == "return":
                    break
                if result[1] == "build_mc":
                    hero.stats.max = mc_max
                    hero.stats.lvl_max = mc_lvl_max
                    hero.occupation = mc_class
                    for stat in mc_stats:
                        setattr(hero, stat, mc_stats[stat])
                        
                    if not hero.img_db:
                        renpy.call_screen("pyt_message_screen", "Please select a battle sprite for the MC!")
                    else:
                        hs()
                        # renpy.pause(0.5)
                        "Meow"
                        for key in mc_pics.keys():
                            if mc_pics[key] == hero.img_db:
                                del mc_pics[key]
                        af_pics = mc_pics # Mooore AFs :)
                        del mc_pics
                        del total_points
                        del mc_class
                        del mc_stats
                        del mc_max
                        del mc_lvl_max
                        hero.say = Character(hero.nickname, color=ivory, show_two_window=True, show_side_image=hero.show("portrait", resize=(140, 140)), window_left_padding=230)
                        if hasattr(renpy.store, "neow"):
                            del neow
                        hero.restore_ap()
                        hero.log_stats()
                        
                        break
                     
            elif result[0] == "rename":
                if result[1] == "name":
                    hero.name = renpy.call_screen("pyt_input", hero.name, "Enter Name", 20)
                    hero.nickname = hero.name
                    hero.fullname = hero.name
                if result[1] == "nick":
                    hero.nickname = renpy.call_screen("pyt_input", hero.name, "Enter Nick-Name", 20)
                if result[1] == "full":
                    hero.fullname = renpy.call_screen("pyt_input", hero.name, "Enter Full-Name", 20)
                        
            elif result[0] == "adjust_stat":
                stat = result[2]
                if result[1] == "+":
                    if total_points:
                        if mc_stats[stat] < min(mc_max[stat], mc_lvl_max[stat]):
                            mc_stats[stat] += 1
                            total_points -= 1
                        else:
                            renpy.call_screen("pyt_message_screen", "You cannot increase %s over the maxumum allowed!"%stat)
                elif result[1] == "-":
                    if stat == "luck":
                        if mc_stats[stat] > 0:
                            mc_stats[stat] -= 1
                            total_points += 1
                        else:
                            renpy.call_screen("pyt_message_screen", "It cannot go lower than this!")
                    else:
                        if not hasattr(renpy.store, "neow"):
                            neow = copy.copy(mc_stats)
                        if mc_stats[stat] > min(neow[stat], round(hero.stats.min[stat] + min(mc_max[stat], mc_lvl_max[stat])*0.6)):
                            mc_stats[stat] -= 1
                            total_points += 1
                        else:
                            renpy.call_screen("pyt_message_screen", "It cannot go lower than this!")
                    
            elif result[0] == "change_class":
                mc_class = result[1]
                total_points = 0
                if result[1] == "Warrior":
                    mc_max = {
                    'libido': 100,
                    'constitution': 60,
                    'reputation': 100,
                    'health': 100,
                    'fame': 100,
                    'alignment': 1000,
                    'vitality': 300,
                    'intelligence': 100,
                    'charisma': 60,
                    'sex': 170,
    
                    'luck': 50,
    
                    'attack': 70,
                    'magic': 50,
                    'defence': 60,
                    'agility': 55,
                    'mp': 40}
                
                    mc_lvl_max = {
                    'libido': 100,
                    'constitution': 40,
                    'reputation': 100,
                    'health': 200,
                    'fame': 100,
                    'alignment': 1000,
                    'vitality': 300,
                    'intelligence': 60,
                    'charisma': 35,
                    'sex': 120,
    
                    'luck': 50,
    
                    'attack': 50,
                    'magic': 35,
                    'defence': 40,
                    'agility': 45,
                    'mp': 30}
                    
                    mc_stats = {
                    'constitution': 30,
                    'intelligence': 10,
                    'charisma': 10,
                    'sex': 30,
    
                    'luck': 10,
    
                    'attack': 40,
                    'magic': 25,
                    'defence': 30,
                    'agility': 35}
                    
                if result[1] == "Casanova":
                    mc_max = {
                    'libido': 100,
                    'constitution': 50,
                    'reputation': 100,
                    'health': 100,
                    'fame': 100,
                    'alignment': 1000,
                    'vitality': 300,
                    'intelligence': 100,
                    'charisma': 80,
                    'sex': 250,
    
                    'luck': 50,
    
                    'attack': 50,
                    'magic': 40,
                    'defence': 50,
                    'agility': 45,
                    'mp': 30}
                
                    mc_lvl_max = {
                    'libido': 100,
                    'constitution': 30,
                    'reputation': 100,
                    'health': 200,
                    'fame': 100,
                    'alignment': 1000,
                    'vitality': 300,
                    'intelligence': 60,
                    'charisma': 60,
                    'sex': 200,
    
                    'luck': 50,
    
                    'attack': 40,
                    'magic': 25,
                    'defence': 30,
                    'agility': 35,
                    'mp': 30}
                    
                    mc_stats = {
                    'constitution': 20,
                    'intelligence': 10,
                    'charisma': 35,
                    'sex': 45,
    
                    'luck': 10,
    
                    'attack': 25,
                    'magic': 20,
                    'defence': 20,
                    'agility': 20}
                
                    
    hide screen mc_stories
    hide screen mc_texts
    hide screen mc_sub_stories
    hide screen mc_sub_texts
    hide screen mc_setup
    return
 
screen mc_stories(choices=OrderedDict()): # This is the fathers SUB occupation choice.
    tag mc_sub
    hbox:
        pos(0, 145)
        style_group "mcsetup"
        box_wrap True
        xsize 360
        $ img_choices = choices["choices"]
        for key in img_choices:
            python:
                if choices["MC"][key].get("choices", ""):
                    # greycolor = False
                    sepia = False
                else:
                    # greycolor = True
                    sepia = True
                img = im.Sepia(img_choices[key]) if sepia else img_choices[key]
            button:
                if img_choices.keys().index(key) % 2:
                    text key align (1.0, 0.52)
                        # if greycolor:
                            # color grey
                    add img align (0.0, 0.5)
                else:
                    text key align (0.0, 0.52)
                        # if greycolor:
                            # color grey
                    add img align (1.0, 0.5)
                action SensitiveIf(not sepia), SelectedIf(store.sub_story==key), If(store.sub_story==key, false=[Hide("mc_sub_texts"), Hide("mc_texts"),
                              SetVariable("mc_story", None), SetVariable("mc_substory", None), SetVariable("sub_story", key),
                              Show("mc_texts", transition=dissolve),
                              Show("mc_sub_stories", transition=dissolve, choices=mc_stories[main_story]["MC"][key]["choices"])])
                
screen mc_texts():
    tag mc_texts
    frame:
        pos (0, 350)
        background Frame(Transform("content/gfx/frame/MC_bg.png", alpha=1), 30, 30)
        xysize(350, 370)
        vbox:
            xalign 0.5
            if main_story in mc_stories:
                if "header" in mc_stories[main_story]:
                    text ("{font=fonts/DeadSecretary.ttf}{size=22}%s" % mc_stories[main_story]["header"]) xalign 0.5
                else:
                    text "Add 'header' to [main_story] story!" xalign 0.5
                null height 15
                vbox:
                    if sub_story in mc_stories[main_story]:
                        text ("%s" % mc_stories[main_story][sub_story]) xalign 0.5 style "garamond" size 18
            else:
                text "No [main_story] story found!!!" align (0.5, 0.5)
                
screen mc_sub_stories(choices=OrderedDict()): # This is the MC occupation choice.
    if choices:
        hbox:
            pos(870, 145)
            spacing 10
            for i in ["l", "r"]:
                if choices.get(i, ""):
                    vbox:
                        spacing 2
                        $ img = ProportionalScale(choices["".join([i, "_img"])], 150, 150, align=(0.5, 0.5))
                        button:
                            xalign 0.5
                            xysize (165, 165)
                            background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                            idle_foreground img
                            hover_foreground im.MatrixColor(img, im.matrix.brightness(0.10), align=(0.5, 0.5))
                            activate_sound "content/sfx/sound/sys/hooah.ogg"
                            action [Hide("mc_sub_texts"), SetVariable("mc_story", choices[i]), Show("mc_sub_texts", transition=dissolve), Return(["change_class", "Warrior"])]
                        hbox:
                            xalign 0.5
                            spacing 1
                            style_group "sqstory"
                            for sub in xrange(3):
                                $ sub = str(sub)
                                if choices.get(i + sub, ""):
                                    $ img = ProportionalScale(choices["".join([i, sub, "_img"])], 46, 46, align=(0.5, 0.5))
                                    button:
                                        # foreground img
                                        # idle_foreground im.Sepia(img, align=(0.5, 0.5))
                                        # hover_foreground im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
                                        background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                                        idle_foreground im.Sepia(img, align=(0.5, 0.5))
                                        hover_foreground im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
                                        selected_foreground img
                                        action If(mc_story == choices[i], true=[Hide("mc_sub_texts"),
                                                     SetVariable("mc_substory", choices[i + sub]), Show("mc_sub_texts", transition=dissolve)])
                            
screen mc_sub_texts():
    tag mc_subtexts
    frame:
        background Frame(Transform("content/gfx/frame/MC_bg.png", alpha=1), 30, 30)
        anchor (1.0, 1.0)
        pos (1280, 723)
        xysize (450, 335)
        # xmargin 20
        has vbox xmaximum 430 xfill True xalign 0.5
        $ texts = mc_stories[main_story]["MC"][mc_story]
        if "header" in texts:
            text ("{font=fonts/DeadSecretary.ttf}{size=28}%s" % texts["header"]) xalign 0.5
        else:
            text "Add Header text!"
        null height 10
        if "text" in texts:
            text ("%s" % texts["text"]) style "garamond" size 18
        else:
            text "Add Main Text!"
        null height 20    
        if mc_substory in texts:
            text ("{font=fonts/DeadSecretary.ttf}{size=23}%s" % mc_substory) xalign 0.5
            null height 5
            text ("%s" % texts[mc_substory]) style "garamond" size 18
                
screen mc_setup():
    
    default sprites = mc_pics.keys()
    default index = 0
    default left_index = -1
    default right_index = 1
    
    # Rename and start buttons:
    if all([hero.img_db, hasattr(store, "mc_stats"), (hasattr(store, "mc_substory") and store.mc_substory)]):
        textbutton "{size=40}{color=[white]}{font=fonts/TisaOTB.otf}Start Game" at fade_in_out():
            background Transform(Frame("content/gfx/interface/images/story12.png", 5, 5), alpha=1)
            hover_background Transform(Frame(im.MatrixColor("content/gfx/interface/images/story12.png", im.matrix.brightness(0.15)), 5, 5), alpha=1)
            align (0.46, 0.93)
            activate_sound "content/sfx/sound/events/start_2.mp3"
            action [Execute(renpy.music.stop), Return(["control", "build_mc"])]
    textbutton "{size=24}{font=fonts/TisaOTM.otf}{color=[white]}[hero.name]":
        background Transform(Frame("content/gfx/interface/images/story12.png", 5, 5), alpha=0.8)
        hover_background Transform(Frame(im.MatrixColor("content/gfx/interface/images/story12.png", im.matrix.brightness(0.15)), 5, 5), alpha=1)
        xpadding 12
        ypadding 8
        align (0.37, 0.10)
        action Show("chr_rename", chr=hero)
    
    # Text:
    # text ("{size=80}{font=fonts/earthkid.ttf}PyTFall") antialias True vertical True align (0.51, 0.65)
                
    # MC Sprites:
    if hasattr(store, "mc_pics"):
        hbox:
            spacing 4
            align (0.463, 0.71)
            $ img = ProportionalScale("content/gfx/interface/buttons/blue_arrow_left.png", 40, 40)
            imagebutton:
                idle img
                hover im.MatrixColor(img, im.matrix.brightness(0.20))
                activate_sound "content/sfx/sound/sys/hover_2.wav"
                action [SetScreenVariable("index", (index - 1) % len(sprites)),
                           SetScreenVariable("left_index", (left_index - 1) % len(sprites)),
                           SetScreenVariable("right_index", (right_index - 1) % len(sprites)),
                           SetField(hero, "img_db", mc_pics[sprites[(index - 1) % len(sprites)]])]
            $ img = ProportionalScale("content/gfx/interface/buttons/blue_arrow_right.png", 40, 40)
            imagebutton:
                idle img
                hover im.MatrixColor(img, im.matrix.brightness(0.20))
                activate_sound "content/sfx/sound/sys/hover_2.wav"
                action [SetScreenVariable("index", (index + 1) % len(sprites)),
                           SetScreenVariable("left_index", (left_index + 1) % len(sprites)),
                           SetScreenVariable("right_index", (right_index + 1) % len(sprites)),
                           SetField(hero, "img_db", mc_pics[sprites[(index + 1) % len(sprites)]])]
        frame:
            align (0.328, 0.53)  
            xysize (160, 220)
            background Frame("content/gfx/frame/MC_bg3.png", 40, 40)
            add im.Sepia(ProportionalScale(mc_pics[sprites[left_index]]["battle_sprite"][0], 140, 190)) align (0.5, 0.4)
        frame:
            align (0.586, 0.53)
            xysize (160, 220)
            background Frame("content/gfx/frame/MC_bg3.png", 40, 40)
            add im.Sepia(ProportionalScale(mc_pics[sprites[right_index]]["battle_sprite"][0], 140, 190)) align (0.5, 0.4)
        frame:
            align (0.457, 0.36)
            xysize (160, 220)
            background Frame("content/gfx/frame/MC_bg3.png", 40, 40)
            add ProportionalScale(mc_pics[sprites[index]]["battle_sprite"][0], 150, 200) align (0.5, 0.4)
            frame:
                align (0.995, -0.74)
                anchor (1, 1) 
                background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                add ProportionalScale(mc_pics[sprites[index]]["portrait"][0], 100, 100)
            
    # Stats: @ Review, disabled for now!
    # if hasattr(store, "mc_stats") and hasattr(store, "total_points"):
        # frame:
            # background Frame(Transform("content/gfx/frame/MC_bg.png", alpha=1), 30, 30)
            # xanchor 1.0
            # pos (1280, 10)
            # vbox:
                # spacing 4
                # xysize (438, 250)
                # text ("{font=fonts/DeadSecretary.ttf}{size=22}attributes") xalign 0.5 yalign 0.4
                # vbox:
                    # xalign 0.5
                    # spacing 4
                    # for stat in mc_stats:
                        # hbox:
                            # hbox:
                                # hbox:
                                    # xminimum 340
                                    # xmaximum 340
                                    # xanchor -0.06
                                    # xfill True
                                    # text ("{font=fonts/agrevue.ttf}{size=17}%s"%stat.capitalize())
                                # hbox:
                                    # xminimum 100
                                    # xmaximum 100
                                    # xanchor -0.3
                                    # xfill True
                                    # text ("{=myriadpro_reg}{size=17}%d I %d"%(mc_stats[stat], min(mc_max[stat], mc_lvl_max[stat])))
                             
                            # # Buttons:
                            # #hbox:
                                # #spacing 4
                                # #xanchor 0.2
                                # #$ img = ProportionalScale("content/gfx/interface/buttons/blue_arrow_left.png", 15, 15)
                                # #imagebutton:    
                                    # #idle img
                                    # #hover im.MatrixColor(img, im.matrix.brightness(0.20))
                                    # #activate_sound "content/sfx/sound/sys/hover_2.wav"
                                    # #action Return(["adjust_stat", "-", stat])
                                     
                                # #$ img = ProportionalScale("content/gfx/interface/buttons/blue_arrow_right.png", 15, 15)
                                # #imagebutton:    
                                    # #idle img
                                    # #hover im.MatrixColor(img, im.matrix.brightness(0.20))
                                    # #activate_sound "content/sfx/sound/sys/hover_2.wav"
                                    # #action Return(["adjust_stat", "+", stat])
                            

    ### Background Story ###
    add "content/gfx/interface/images/story1.png" align (0.002, 0.09)
    
    frame: ## Text frame for Main Story (Merchant, Warrior, Scholar and Noble)
        text ("{size=20}{font=fonts/TisaOTm.otf}[main_story]") align (0.53, 0.4)
        background Frame(Transform("content/gfx/interface/images/story12.png", alpha=0.8), 10, 10)
        pos(102, 15)
        xysize(150, 20)
        
    hbox: # Fathers Main occupation:
        style_group "sqstory"
        pos (30, 65)
        spacing 17
        $ ac_list = [Hide("mc_stories"), Hide("mc_sub_stories"), Hide("mc_sub_texts"),
                          SetVariable("sub_story", None), SetVariable("mc_story", None), SetVariable("mc_substory", None)]
        $ img = im.Scale("content/gfx/interface/images/merchant.png", 50, 50, align=(0.5, 0.5))
        # TODO: This bit needs to be recoded in "for loop" format.
        button: ## Merchant ##
            foreground im.Sepia(img, align=(0.5, 0.5))
            selected_foreground img
            idle_foreground im.Sepia(img, align=(0.5, 0.5))
            hover_foreground im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
            if mc_stories["Merchant"].get("header", ""):
                action SelectedIf(main_story == "Merchant"), If(store.main_story == "Merchant",
                              false=ac_list + [SetVariable("main_story", "Merchant"),
                                                       Show("mc_stories", transition=dissolve, choices=mc_stories["Merchant"])])
        $ img = im.Scale("content/gfx/interface/images/warriorP.png", 50, 50, align=(0.5, 0.5))
        button: ## Warrior ##
            foreground im.Sepia(img, align=(0.5, 0.5))
            selected_foreground img
            idle_foreground im.Sepia(img, align=(0.5, 0.5))
            hover_foreground im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
            if mc_stories["Warrior"].get("header", ""):
                action SelectedIf(main_story == "Warrior"), If(store.main_story == "Warrior",
                              false=ac_list + [SetVariable("main_story", "Warrior"),
                                                       Show("mc_stories", transition=dissolve, choices=mc_stories["Warrior"])])
        $ img = im.Scale("content/gfx/interface/images/magicP.png", 50, 50, align=(0.5, 0.5))
        button: ## Scholar ##
            foreground im.Sepia(img, align=(0.5, 0.5))
            selected_foreground img
            idle_foreground im.Sepia(img, align=(0.5, 0.5))
            hover_foreground im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
            if mc_stories["Scholar"].get("header", ""):
                action SelectedIf(main_story == "Scholar"), If(store.main_story == "Scholar",
                          false=ac_list + [SetVariable("main_story", "Scholar"),
                                                   Show("mc_stories", transition=dissolve, choices=mc_stories["Scholar"])])
        $ img = im.Scale("content/gfx/interface/images/nobleP.png", 50, 50, align=(0.5, 0.5))
        button: ## Noble ##
            foreground im.Sepia(img, align=(0.5, 0.5))
            selected_foreground img
            idle_foreground im.Sepia(img, align=(0.5, 0.5))
            hover_foreground im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
            if mc_stories["Noble"].get("header", ""):
                action SelectedIf(main_story == "Noble"), If(store.main_story == "Noble",
                          false=ac_list + [SetVariable("main_story", "Noble"),
                                                   Show("mc_stories", transition=dissolve, choices=mc_stories["Noble"])])
