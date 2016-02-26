label mc_setup:
    $ mc_pics = load_mc_images()
    # We set the first dict to serve as MCs image base:
    $ hero.img_db = mc_pics[mc_pics.keys()[0]]
    
    call build_mc_stories

    scene bg mc_setup
    show screen mc_setup
    with dissolve
    
    $ global_flags.set_flag("game_start")
    
    while 1:
        $ result = ui.interact()
        
        if result[0] == "control":
            if result[1] == "build_mc":
                python:
                    for key in mc_pics.keys():
                        if mc_pics[key] == hero.img_db:
                            del mc_pics[key]
                        
                $ af_pics = mc_pics # Mooore AFs :)
                
                # python:
                $ del mc_pics
                    # del total_points
                    # del mc_class
                    # del mc_stats
                    # del mc_max
                    # del mc_lvl_max
                    
                $ hero.say = Character(hero.nickname, color=ivory, show_two_window=True, show_side_image=hero.show("portrait", resize=(120, 120)))
                
                if hasattr(renpy.store, "neow"):
                    $ del neow
                $ hero.restore_ap()
                $ hero.log_stats()
                jump mc_setup_end
                 
        elif result[0] == "rename":
            if result[1] == "name":
                $ hero.name = renpy.call_screen("pyt_input", hero.name, "Enter Name", 20)
                $ hero.nickname = hero.name
                $ hero.fullname = hero.name
            if result[1] == "nick":
                $ hero.nickname = renpy.call_screen("pyt_input", hero.name, "Enter Nick-Name", 20)
            if result[1] == "full":
                $ hero.fullname = renpy.call_screen("pyt_input", hero.name, "Enter Full-Name", 20)
                        
            # elif result[0] == "adjust_stat":
                # stat = result[2]
                # if result[1] == "+":
                    # if total_points:
                        # if mc_stats[stat] < min(mc_max[stat], mc_lvl_max[stat]):
                            # mc_stats[stat] += 1
                            # total_points -= 1
                        # else:
                            # renpy.call_screen("message_screen", "You cannot increase %s over the maxumum allowed!"%stat)
                # elif result[1] == "-":
                    # if stat == "luck":
                        # if mc_stats[stat] > 0:
                            # mc_stats[stat] -= 1
                            # total_points += 1
                        # else:
                            # renpy.call_screen("message_screen", "It cannot go lower than this!")
                    # else:
                        # if not hasattr(renpy.store, "neow"):
                            # neow = copy.copy(mc_stats)
                        # if mc_stats[stat] > min(neow[stat], round(hero.stats.min[stat] + min(mc_max[stat], mc_lvl_max[stat])*0.6)):
                            # mc_stats[stat] -= 1
                            # total_points += 1
                        # else:
                            # renpy.call_screen("message_screen", "It cannot go lower than this!")
                     
            # elif result[0] == "change_class":
                # mc_class = result[1]
                # total_points = 0
                # if result[1] == "Warrior":
                    # mc_max = {
                    # 'libido': 100,
                    # 'constitution': 60,
                    # 'reputation': 100,
                    # 'health': 100,
                    # 'fame': 100,
                    # 'alignment': 1000,
                    # 'vitality': 300,
                    # 'intelligence': 100,
                    # 'charisma': 60,
                    # 'sex': 170,
     
                    # 'luck': 50,
     
                    # 'attack': 70,
                    # 'magic': 50,
                    # 'defence': 60,
                    # 'agility': 55,
                    # 'mp': 40}
                 
                    # mc_lvl_max = {
                    # 'libido': 100,
                    # 'constitution': 40,
                    # 'reputation': 100,
                    # 'health': 200,
                    # 'fame': 100,
                    # 'alignment': 1000,
                    # 'vitality': 300,
                    # 'intelligence': 60,
                    # 'charisma': 35,
                    # 'sex': 120,
     
                    # 'luck': 50,
     
                    # 'attack': 50,
                    # 'magic': 35,
                    # 'defence': 40,
                    # 'agility': 45,
                    # 'mp': 30}
                 
                    # mc_stats = {
                    # 'constitution': 30,
                    # 'intelligence': 10,
                    # 'charisma': 10,
                    # 'sex': 30,
 
                    # 'luck': 10,
 
                    # 'attack': 40,
                    # 'magic': 25,
                    # 'defence': 30,
                    # 'agility': 35}
                
                # if result[1] == "Casanova":
                    # mc_max = {
                    # 'libido': 100,
                    # 'constitution': 50,
                    # 'reputation': 100,
                    # 'health': 100,
                    # 'fame': 100,
                    # 'alignment': 1000,
                    # 'vitality': 300,
                    # 'intelligence': 100,
                    # 'charisma': 80,
                    # 'sex': 250,
 
                    # 'luck': 50,

                    # 'attack': 50,
                    # 'magic': 40,
                    # 'defence': 50,
                    # 'agility': 45,
                    # 'mp': 30}
              
                    # mc_lvl_max = {
                    # 'libido': 100,
                    # 'constitution': 30,
                    # 'reputation': 100,
                    # 'health': 200,
                    # 'fame': 100,
                    # 'alignment': 1000,
                    # 'vitality': 300,
                    # 'intelligence': 60,
                    # 'charisma': 60,
                    # 'sex': 200,
 
                    # 'luck': 50,
   
                    # 'attack': 40,
                    # 'magic': 25,
                    # 'defence': 30,
                    # 'agility': 35,
                    # 'mp': 30}
                     
                    # mc_stats = {
                    # 'constitution': 20,
                    # 'intelligence': 10,
                    # 'charisma': 35,
                    # 'sex': 45,
     
                    # 'luck': 10,
     
                    # 'attack': 25,
                    # 'magic': 20,
                    # 'defence': 20,
                    # 'agility': 20}
               
label build_mc:
    # We build the MC here. First we get the classes player picked in the choices screen and add those to MC:
    $ temp = {traits[t] for t in [mc_stories[main_story]["class"],mc_stories[main_story]["MC"][sub_story][mc_story]["class"]]}
    $ hero.traits.basetraits = temp
    python:
        for t in temp:
            hero.apply_trait(t)
            
    # Now that we have our setup, max out all fixed max stats and set all normal stats to 35% of their maximum:
    python:
        for s in ['libido', 'constitution', 'intelligence', 'charisma', 'attack', 'magic', 'defence', 'agility']:
            setattr(hero, s, int(round(hero.get_max(s)*0.35)))
    python:
        for s in ["health", "mp", "vitality"]:
            setattr(hero, s, hero.get_max(s))
    return
                    
label mc_setup_end:
    hide screen mc_stories
    hide screen mc_texts
    hide screen mc_sub_stories
    hide screen mc_sub_texts
    hide screen mc_setup
    scene black
    
    call build_mc
    
    # Call all the labels:
    python:
        """
        main_story: Merchant
        substory: Caravan
        mc_story: Defender
        mc_substory: Sword
        """
    $ temp = mc_stories[main_story]
    if "label" in temp and renpy.has_label(temp["label"]):
        call expression temp["label"]
        
    $ temp = mc_stories[main_story][sub_story]
    if "label" in temp and renpy.has_label(temp["label"]):
        call expression temp["label"]
        
    $ temp = mc_stories[main_story]["MC"][sub_story][mc_story]
    if "label" in temp and renpy.has_label(temp["label"]):
        call expression temp["label"]
        
    $ temp = mc_stories[main_story]["MC"][sub_story][mc_story][mc_substory]
    if "label" in temp and renpy.has_label(temp["label"]):
        call expression temp["label"]
        
    python:
        del temp
        del mc_stories
        del main_story
        del sub_story
        del mc_story
        del mc_substory
    
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
                        text ("%s" % mc_stories[main_story][sub_story]["text"]) xalign 0.5 style "garamond" size 18
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
                            action [Hide("mc_sub_texts"), SetVariable("mc_story", choices[i]), Show("mc_sub_texts", transition=dissolve)]
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
        $ texts = mc_stories[main_story]["MC"][sub_story][mc_story]
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
            text ("%s" % texts[mc_substory]["text"]) style "garamond" size 18
                
screen mc_setup():
    
    default sprites = mc_pics.keys()
    default index = 0
    default left_index = -1
    default right_index = 1
    
    # Rename and Start buttons + Classes are now here as well!!!:
    if all([hero.img_db, (hasattr(store, "mc_substory") and store.mc_substory)]):
        textbutton "{size=40}{color=[white]}{font=fonts/TisaOTB.otf}Start Game" at fade_in_out():
            background Transform(Frame("content/gfx/interface/images/story12.png", 5, 5), alpha=1)
            hover_background Transform(Frame(im.MatrixColor("content/gfx/interface/images/story12.png", im.matrix.brightness(0.15)), 5, 5), alpha=1)
            align (0.46, 0.93)
            activate_sound "content/sfx/sound/events/start_2.mp3"
            action [Stop("music"), Return(["control", "build_mc"])]
            
    textbutton "{size=24}{font=fonts/TisaOTM.otf}{color=[white]}[hero.name]":
        background Transform(Frame("content/gfx/interface/images/story12.png", 5, 5), alpha=0.8)
        hover_background Transform(Frame(im.MatrixColor("content/gfx/interface/images/story12.png", im.matrix.brightness(0.15)), 5, 5), alpha=1)
        xpadding 12
        ypadding 8
        align (0.37, 0.10)
        action Show("char_rename", char=hero)
        
    if store.main_story:
        python:
            try:
                bc = mc_stories[main_story]["class"]
            except:
                bc = "Error: No Class Specified!"
        textbutton "[bc]":
            align (0.32, 0.06)
            action NullAction()
            
    if store.mc_story and mc_stories[main_story]["class"] != mc_stories[main_story]["MC"][sub_story][mc_story]["class"]:
        python:
            try:
                bc = mc_stories[main_story]["MC"][sub_story][mc_story]["class"]
            except:
                bc = "Error: No Class Specified!"
        textbutton "[bc]":
            align (0.42, 0.17)
            action NullAction()
    
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
            
    # Stats: @ Review, disabled for now! or forever?
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
        for branch in mc_stories:
            $ img = im.Scale(mc_stories[branch]["img"], 50, 50, align=(0.5, 0.5))
            button: ## Merchant ##
                foreground im.Sepia(img, align=(0.5, 0.5))
                selected_foreground img
                idle_foreground im.Sepia(img, align=(0.5, 0.5))
                hover_foreground im.MatrixColor(img, im.matrix.brightness(0.15), align=(0.5, 0.5))
                if mc_stories[branch].get("header", ""):
                    action SelectedIf(main_story == branch), If(store.main_story == branch,
                              false=ac_list + [SetVariable("main_story", branch),
                               Show("mc_stories", transition=dissolve, choices=mc_stories[branch])])
