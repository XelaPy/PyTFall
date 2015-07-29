init python:
    # The dice value for gm scenes
    gm_dice = 100
    
    # The disposition multiplier for gm scenes
    gm_disp_mult = 1
    
    # Whether the gm scene was successful
    gm_last_success = False
    
    # List for possible about her text
    gm_abouther_list = None
    
    # The background for the date fight
    gm_fight_bg = None
    
    # The job for the GT mode
    gm_job = None
    

label girl_interactions:
    python:
        # Hide all images, show background
        renpy.scene()
        renpy.show(gm.bg_cache)
        
        # Hide last screen
        hs()
        
        # Set characters
        g = Character(char.name, color="#c8ffc8", show_two_window=True)
        h = Character(hero.name, color="#c8ffc8", show_two_window=True)
        nvl_gm = Character(None, kind=nvl)
        
        # Run quests and events
        pytfall.world_quests.run_quests("auto")
        pytfall.world_events.run_events("auto")
        
        # Hide menus till greeting
        gm.show_menu = False
        gm.show_menu_givegift = False
        
        # Show screen
        renpy.show_screen("pyt_girl_interactions")
        renpy.with_statement(dissolve)
    
    # Show greeting
    if gm.see_greeting:
        $ gm.see_greeting = False
        
        if renpy.has_label("%s_greeting"%gm.mode):
            call expression ("%s_greeting"%gm.mode) from _call_expression
    
    python:
        # Show menu
        gm.show_menu = True
        
        # GM labels can now be of the following formats (where %l is the label and %g is the girl's id):
        # girl_meets_%l_%g
        # girl_meets_%l
        # girl_interactions_%l_%g
        # girl_interactions_%l
        # girl_trainings_%l_%g
        # girl_trainings_%g
        # interaction_%l_%g
        # interaction_%l
        #
        # The GM system will pick the most specific available label. Possible choices can be restricted by setting the follow arguments as False:
        # allow_gm
        # allow_int
        # allow_tr
        # allow_unique
        #
        # Note, the above doesn't work for actions generated through the ST module, although they will use girl-specific labels if available.
        #
        # You can limit what action is available under what mode by setting the mode argument to:
        # girl_meets = When meeting free girls in the city.
        # girl_interactions = When interacting with girls under your employ.
        # girl_training = When training slaves.
        #
        # If you wish to limit an entire menu you need to set condition to either _gm_mode, _gi_mode or _gt_mode for girl_meets, girl_interactions or girl_trainings respectively.
        #
        
        # Create actions
        if pytfall.world_actions.location("girl_meets"):
            _gm_mode = Iff(S((gm, "mode")), "==", "girl_meets")
            _gi_mode = Iff(S((gm, "mode")), "==", "girl_interactions")
            _gt_mode = Iff(S((gm, "mode")), "==", "girl_trainings")
            
            _not_gm_mode = IffOr(_gi_mode, _gt_mode)
            _not_gi_mode = IffOr(_gm_mode, _gt_mode)
            _not_gt_mode = IffOr(_gm_mode, _gi_mode)
            
            # CHAT
            m = 0
            pytfall.world_actions.menu(m, "Chat")
            pytfall.world_actions.gm_choice("General", index=(m, 0))
            pytfall.world_actions.gm_choice("About Job", mode="girl_interactions", index=(m, 1))
            pytfall.world_actions.gm_choice("How She Feels", mode="girl_interactions", index=(m, 2))
            pytfall.world_actions.gm_choice("About Her", index=(m, 3))
            pytfall.world_actions.gm_choice("About Occupation", mode="girl_meets", index=(m, 4))
            pytfall.world_actions.gm_choice("Interests", index=(m, 5))
            pytfall.world_actions.gm_choice("Romance", index=(m, 6))
            
            
            # TRAINING
            m = 1
            n = 0
            pytfall.world_actions.menu(m, "Training", condition=_gt_mode)
            
            # Loop through all courses that don't belong to a school, and return the real dict
            #for k,c in get_all_courses(no_school=True, real=True).iteritems():
            
            # Loop through all courses in the training dungeon
            for k,c in schools[TrainingDungeon.NAME].all_courses.iteritems():
                # Get the lessons that are one off events 
                ev = [l for l in c.options if l.is_one_off_event]
                
                if ev:
                    # Create the menu for the course
                    pytfall.world_actions.menu((m, n), k, condition=OneOffTrainingAction("menu", c))
                    
                    for l in range(len(ev)):
                        # Add the lesson
                        pytfall.world_actions.add((m, n, l), ev[l].name, OneOffTrainingAction("action", ev[l]), condition=OneOffTrainingAction("condition", ev[l]))
                    
                    n += 1
            
            # PRAISE
            m = 2
            pytfall.world_actions.menu(m, "Praise",  condition="not(char in hero.girls)")
            pytfall.world_actions.gm_choice("Clever", mode="girl_meets", index=(m, 0))
            pytfall.world_actions.gm_choice("Strong", mode="girl_meets", index=(m, 1))
            pytfall.world_actions.gm_choice("Cute", mode="girl_meets", index=(m, 2))
            
          
            # GIVE MONEY
            m = 3
            pytfall.world_actions.menu(m, "Give Money")
            pytfall.world_actions.gm_choice("25G", label="gm25g", index=(m, 0))
            pytfall.world_actions.gm_choice("50G", label="gm50g", index=(m, 1))
            pytfall.world_actions.gm_choice("100G", label="gm100g", index=(m, 2))
            pytfall.world_actions.gm_choice("500G", label="gm500g", index=(m, 3))
            
            # GIVE GIFT
            m = 4
            pytfall.world_actions.add(m, "Give Gift", Return(["gift", True]))
            
            # GO OUT
           # m = 6
           # pytfall.world_actions.menu(m, "Go Out")
           # pytfall.world_actions.gm_choice("Beach", index=(m, 0))
           # pytfall.world_actions.gm_choice("Shopping", index=(m, 1)) # In shopping file instead of go out
            
            # PROPOSITION
            m = 5
            pytfall.world_actions.menu(m, "Propose", condition="not(char in hero.girls) or not(check_friends(char, hero)) or not(check_lovers(char, hero))")
            pytfall.world_actions.gm_choice("Friends", condition="not check_friends(char, hero)", index=(m, 0))
            pytfall.world_actions.gm_choice("Girlfriend", condition="not check_lovers(char, hero)", index=(m, 1))
            pytfall.world_actions.gm_choice("Hire", condition="not(char in hero.girls)", index=(m, 2))
            
            # INTIMACY
            m = 6
            pytfall.world_actions.menu(m, "Intimacy")
            pytfall.world_actions.gm_choice("Hug", index=(m, 0))
            pytfall.world_actions.gm_choice("Slap Butt", index=(m, 1))
            pytfall.world_actions.gm_choice("Grab Breasts", index=(m, 2))
            pytfall.world_actions.gm_choice("Kiss", index=(m, 3))
            pytfall.world_actions.gm_choice("Sex", index=(m, 4))
            pytfall.world_actions.gm_choice("Become Fr", index=(m, 5))
            pytfall.world_actions.gm_choice("Become Lv", index=(m, 6))
            pytfall.world_actions.gm_choice("Disp", index=(m, 7))
            
           
            # Back
            pytfall.world_actions.add("zzz", "Leave", Return(["control", "back"]))
            
            # Developer mode switches
            if config.developer:
                pytfall.world_actions.menu("dev", "Developer")
                pytfall.world_actions.add(("dev", "gm"), "GM", Return(["test", "GM"]), condition=_not_gm_mode)
                pytfall.world_actions.add(("dev", "gi"), "GI", Return(["test", "GI"]), condition=_not_gi_mode)
                pytfall.world_actions.add(("dev", "gt"), "GT", Return(["test", "GT"]), condition=_not_gt_mode)
            
            pytfall.world_actions.finish()
    
    jump girl_interactions_control

label girl_interactions_end:
    python:
        # Music flag
        # This causes an issue when run from interactions, trying to fix:
        if renpy.music.get_playing(channel='world'):
            global_flags.set_flag("keep_playing_music")
        
        # Reset GM counters
        gm_disp_mult = 1
        
        # Reset scene
        renpy.scene()
        renpy.hide_screen("pyt_girl_interactions")
        
        # End the GM
        gm.end()
        
label girl_interactions_control:
    while 1:
        $ result = ui.interact()
        
        # Testing
        if result[0] == "test":
            python:
                gm.end(safe=True)
                
                # Girls Meets
                if result[1] == "GM":
                    # Include img as coming from int and tr prevents the "img from last location" from working
                    gm.start_gm(char, img=char.show("profile", exclude=["nude", "bikini", "swimsuit", "beach", "angry", "scared", "ecstatic"]))
                
                # Interactions
                elif result[1] == "GI":
                    gm.start_int(char)
                
                # Training
                elif result[1] == "GT":
                    gm.start_tr(char)
        
        # Gifts
        elif result[0] == "gift":
            python:
                # Show menu
                if result[1] is True:
                    gm.show_menu = False
                    gm.show_menu_givegift = True
                
                # Hide menu
                elif result[1] is None:
                    gm.show_menu = True
                    gm.show_menu_givegift = False
            
                # Give gift
                else:
                    item = result[1]
                    dismod = 0
                    if (hasattr(item, "traits") and any(trait in char.traits for trait in item.traits)) or (hasattr(item, "occupations") and char.occupation in item.occupations):
                        if hasattr(item, "traits"):
                            for key in item.traits:
                                if key in char.traits:
                                    dismod += item.traits[key]
                         
                        if hasattr(item, "occupations"):
                            for key in item.occupations:
                                if key == char.occupation:
                                    dismod += item.occupations[key]
                     
                    else:
                        dismod = item.dismod
                     
                    hero.inventory.remove(item)
                    char.disposition += dismod
                    setattr(gm, "show_menu", True)
                    setattr(gm, "show_menu_givegift", False)
                     
                    if dismod < 0:
                        gm.jump("badgift")
                     
                    elif 50 < dismod >= 0:
                        gm.jump("goodgift")
                     
                    else:
                        gm.jump("perfectgift")
        
        # Controls
        elif result[0] == "control":
            # Return / Back
            if result[1] in ("back", "return"):
                jump girl_interactions_end
    

screen pyt_girl_interactions():
    
    # BG
    add "content/gfx/images/bg_gradient.png" yalign 0.2
    
    # Disposition bar
    vbox:
        align (0.95, 0.31)
        
        vbar:
            top_gutter 13
            bottom_gutter 0 
            value AnimatedValue(value=gm.char.disposition, range=gm.char.get_max("disposition"), delay=4.0)
            bottom_bar "content/gfx/interface/bars/progress_bar_full1.png"
            top_bar "content/gfx/interface/bars/progress_bar_1.png"
            thumb None
            xysize(22, 175)
        
        python:
            # Trying to invert the values (bar seems messed up with negative once):
            if gm.char.disposition < 0:
                inverted_disposition = gm.char.disposition * -1
            else:
                inverted_disposition = 0
        
        vbar:
            bar_invert True
            top_gutter 12
            bottom_gutter 0
            value AnimatedValue(value=inverted_disposition, range=gm.char.stats.min["disposition"]*-1, delay=4.0)
            bottom_bar im.Flip("content/gfx/interface/bars/progress_bar_1.png", vertical=True)
            top_bar "content/gfx/interface/bars/bar_mine.png"
            thumb None
            xysize(22, 175)
    
    # Girl image
    hbox:
        xanchor 0
        xpos 0.22
        yalign 0.22
        
        frame:
            background Frame("content/gfx/frame/MC_bg.png", 10, 10)
            if isinstance(gm.img, im.ImageBase):
                add ProportionalScale(gm.img, 515, 515)
            else:
                add renpy.easy.displayable(gm.img)
        
        if config.developer:
            null width 15
            
            vbox:
                null height 60
                text "{color=[white]}Mode: [gm.mode]"
                text "{color=[white]}Label: [gm.jump_cache]"
                text ("{color=[white]}Girl.AP: [gm.char.AP] / %s"%gm.char.get_ap())
                text "{color=[white]}Points: [gm.gm_points]"
    
    # Actions
    if gm.show_menu:
        use location_actions("girl_meets", gm.char, pos=(1180, 315), anchor=(1.0, 0.5), style="main_screen_3")
    
    # Give gift interface
    if gm.show_menu_givegift:
        vbox:
            align (0.75, 0.5)
            
            viewport:
                maximum(400, 400)
                scrollbars "vertical"
                mousewheel True
                 
                vbox:
                    xalign 0.5
                     
                    for item in hero.inventory:
                        $ item = items[item]
                        if item.slot == "gift":
                            button:
                                xysize(350, 90)
                                hbox:
                                    add LiveComposite((90, 90), (0, 0), im.Scale(item.icon, 90, 90), (0, 0), Text(str(hero.inventory.content[item.id])))
                                    null width 10
                                    text "[item.id]" yalign 0.5
                                 
                                action If(hero.AP > 0, Return(["gift", item]))
            
            null height 10
            textbutton "Back" action Return(["gift", None]) minimum(220, 30) xalign 0.5
    
    use pyt_top_stripe(False)
    

screen pyt_girl_interactions_old:
    
    # Controls
    frame:
        pos (860, 50)
        xysize (420, 560)
        background "content/gfx/frame/frame12.png"
        style_group "interactions"
         
        text "TALK" xalign 0.49 ypos 130 size 22 color white
         
        text "SEX" xalign 0.49 ypos 260 size 22 color white
         
        text "GO OUT" xalign 0.49 ypos 380 size 22 color white
         
        hbox:
            xalign 0.47
            ypos 150
            button:
                xysize (78, 30)
                action gi_action("chat")
                text "Chat"
             
            null width 65
             
            button:
                xysize (78, 30)
                action gi_action("praise")
                text "Praise"
         
        button:
            xalign 0.48
            ypos 192
            xysize (78, 30)
            action gi_action("scold")
            text "Scold"
         
        button:
            xalign 0.195
            ypos 285
            xysize (78, 30)
            action gi_action("fuck")
            text "Fuck"
         
        button:
            xalign 0.493
            ypos 285
            xysize (110, 30)
            action gi_action("blowjob")
            text "Blowjob"
         
        button:
            xalign 0.79
            ypos 285
            xysize (78, 30)
            action gi_action("anal")
            text "Anal"
         
        button:
            xalign 0.488
            ypos 325
            xysize (160, 30)
            action gi_action("lesbo")
            text "Lesbo Action"
         
        button:
            xalign 0.193
            ypos 394
            xysize (78, 30)
            action gi_action("date")
            text "Date"
         
        button:
            xalign 0.493
            ypos 394
            xysize (110, 30)
            action gi_action("shopping")
            text "Shopping"
         
        button:
            xalign 0.79
            ypos 394
            xysize (78, 30)
            action gi_action("other")
            text "Other"
         
        button:
            xalign 0.484
            ypos 435
            xysize (170, 30)
            action gi_action("entertainment")
            text "Entertainment"
     
    # Move to General GM
    if config.developer:
        textbutton "Test GM":
            align (0.5, 0.1)
            action Return(['test_gm'])
     
    # Girl image
    frame:
        background Frame("content/gfx/frame/FrameGP.png", 40, 40)
        xanchor 0
        xpos 0.05
        yalign 0.2
        add ProportionalScale(gm.img, 900, 530)
    
    use pyt_top_stripe(True)
    
