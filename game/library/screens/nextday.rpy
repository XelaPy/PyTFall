label next_day:
    scene bg profile_2
    
    $ FilteredList=list()
    
    if global_flags.flag("nd_music_play"):
        $ global_flags.del_flag("nd_music_play")
        if not "pytfall" in ilists.world_music:
            $ ilists.world_music["pytfall"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("pytfall")]
        play world choice(ilists.world_music["pytfall"])
    
    python:
        global_flags.set_flag("keep_playing_music")
        tl.timer("Next Day")
        devlog.info("Day: %s, Girls (Player): %s, Girls (Game): %s" % (day, len(hero.girls), len(chars)))
        NextDayList = list()
        
        ################## Restore before the jobs ##################
        tl.timer("Char.restore for all MC girls")
        list(girl.restore() for girl in list(g for g in hero.girls if g.action != "Exploring"))
        tl.timer("Char.restore for all MC girls")
        
        ################## Building events Start ##################
        """
        Complete Rewrite! This should become a manager for jobs! Preferably partly in Ren'Py script!
        """
    $ tl.timer("Buildings")
    # Ren'Py script:
    $ nd_buildings = list(b for b in hero.buildings if isinstance(b, NewStyleUpgradableBuilding))
    
    $ tl.timer("Rest (1)")
    $ ndr_chars = list(c for c in hero.girls if c.location != "Exploring" and (isinstance(c.action, Rest) or isinstance(c.action, AutoRest))) # Next Day Resting Chars
    # $ ndr_chars2 = list(c for c in hero.girls if not check_char(c)) # Revice this for characters who are set to work till the drop???
    while ndr_chars:
        $ resting_char = ndr_chars.pop()
        $ resting_char.action(resting_char) # <--- Looks odd and off?
    $ tl.timer("Rest (1)")
    
    while nd_buildings:
        $ building = nd_buildings.pop()
        $ building.run_nd()
        
        # Old jobs:
        python:
            if False:
                ###### Let Strippers do their thing #######
                tl.timer("StripJob")
                girls = strippers
                if strippers:
                    building.servicer['strippers'] = len(strippers)
                
                while strippers:
                    girl = choice(strippers)
                    StripJob(girl, building, strippers, clients)
                
                tl.timer("StripJob")
                
                ##### First round of Service Girls is next #####
                tl.timer("ServiceJob(1)")
                girls = service_girls
                while service_girls:
                    girl = choice(service_girls)
                    ServiceJob(girl, building, service_girls, clients)
                
                tl.timer("ServiceJob(1)")
                
                ###### Whores do their thing! #######
                tl.timer("WhoreJob")
                girls = whores
                while whores and clients and not stop_whore_job:
                    client = clients.pop()
                    whore = None
                    for girl in whores:
                        if client.favtraits and client.favtraits & set(girl.traits):
                            whore = girl
                            client.traitmatched = True
                            break
                    
                    else:
                        whore = choice(whores)
                    
                    WhoreJob(whore, client, building, whores, clients)
                
                tl.timer("WhoreJob")
                
                ##### Second round for Service Girls (Just cleaning this time) #####
                tl.timer("ServiceJob(2)")
                service_girls = list(girl for girl in hero.girls if girl.location == building and girl.action == 'ServiceGirl')
                girls = service_girls
                building.servicer['second_round'] = True
                while service_girls:
                    girl = choice(service_girls)
                    ServiceJob(girl, building, service_girls, clients)
                
                tl.timer("ServiceJob(2)")
                
                ##### Guard Job events and reports #####
                tl.timer("GuardJob")
                guards = list(girl for girl in hero.girls if girl.location == building and girl.action == 'Guard')
                girls = guards
                while guards:
                    girl = choice(guards)
                    GuardJob(girl, building, guards)
                
                tl.timer("GuardJob")
                
                ###### Rest job in buildings #######
                tl.timer("RestJob")
                resting = list(girl for girl in hero.girls if girl.location == building and girl.action in ['Rest', 'AutoRest'])
                girls = resting
                for girl in resting:
                    Rest(girl, building, resting)
                
                tl.timer("RestJob")
                
    python:
        # Append building report to the list
        tl.timer("Building.next_day")
        building.next_day()
        tl.timer("Building.next_day")
            
    $ tl.timer("Buildings")
        ################## Building events END ##################
        #   
        #
        ################## Training events Start ##################
    python:
        tl.timer("Training")
        for school in schools:
            school = schools[school]
            if not school.available: continue
            
            girls = school.get_girls("Course")
            guards = school.get_girls("Guard")
            trainers = school.get_girls("Training")
            
            # Girls first so disobey/runaway/obey events and trainer ap can be calculated
            tl.timer("TrainingJob")
            while girls:
                TrainingJob(choice(girls), school, girls)
            tl.timer("TrainingJob")
            
            # Guards go next for runaway events
            tl.timer("SchoolGuardJob")
            while guards:
                SchoolGuardJob(choice(guards), school, guards)
            tl.timer("SchoolGuardJob")
            
            # Trainers last for disobey events
            tl.timer("TrainerJob")
            while trainers:
                TrainerJob(choice(trainers), school, trainers)
            tl.timer("TrainerJob")
            
            if school.is_school:
                tl.timer("School.next_day")
                school.next_day()
                tl.timer("School.next_day")
            
            else:
                tl.timer("TrainingDungeon.next_day")
                school.next_day()
                tl.timer("TrainingDungeon.next_day")
        
        tl.timer("Training")
        ################## Training events End ##################
        #
        #
        ################## Searching events Start ####################
        tl.timer("Searching")
        for building in hero.buildings:
            girls = building.get_girls("Search")
            while girls:
                EscapeeSearchJob(choice(girls), building, girls)
        
        tl.timer("Searching")
        ################## Searching events End ####################
        #
        #
        ################## Exploration ########################
        tl.timer("Fighers Guild")
        if fg in hero.buildings:
            fg.next_day()
        
        tl.timer("Fighers Guild")    
        ################## Logic #############################
        tl.timer("pytfall + calender.next_day")
        pytfall.next_day()
        calendar.next() # day + 1 is here.
        
        tl.timer("pytfall + calender.next_day")
        
        tl.timer("Next Day")
        #Setting index and picture
        FilteredList = NextDayList * 1
        if FilteredList:
            event = FilteredList[0]
            gimg = event.load_image()
    
    ####### - - - - - #######
    call next_day_controls

    # Lets free some memory...
    if not day%50:
        $ renpy.free_memory()
    
    $ girls = None
    hide screen next_day
    jump mainscreen

label next_day_controls:
    scene bg profile_2
    show screen next_day
    with dissolve
    
    while 1:
        $ result = ui.interact()
        
        if result[0] == 'filter':
            
            if result[1] == 'all':
                python:
                    FilteredList = NextDayList * 1
                    event = FilteredList[0]
                    index = FilteredList.index(event)
                    # raise Exception, [event, type(event), event.__class__, event.__dict__]
                    gimg = event.load_image()
                
            if result[1] == 'red_flags':
                python:
                    FilteredList = list()
                    for event in NextDayList:
                        if event.red_flag:
                            FilteredList.append(event)
                    event = FilteredList[0]
                    index = FilteredList.index(event)
                    # raise Exception, [event, type(event), event.__class__, event.__dict__]
                    gimg = event.load_image()
                
            elif result[1] == 'mc':
                python:
                    FilteredList = []
                    for entry in NextDayList:
                        if entry.type == 'mcndreport':
                            FilteredList.append(entry)
                    event = FilteredList[0]
                    index = FilteredList.index(event)
                    gimg = event.load_image()
            
            elif result[1] == 'school':
                python:
                    FilteredList = []
                    for entry in NextDayList:
                        if entry.type == 'schoolndreport':
                            FilteredList.insert(0, entry)
                        if entry.type == 'schoolreport':
                            FilteredList.append(entry)
                    event = FilteredList[0]
                    index = FilteredList.index(event)
                    gimg = event.load_image()
                        
            elif result[1] == 'gndreports': # Girl Next Day Reports
                python:
                    FilteredList = []
                    for entry in NextDayList:
                        if entry.type == 'girlndreport':
                            FilteredList.append(entry)
                    
                # Preventing Index Exception on empty filter
                python:
                    if FilteredList:
                        event = FilteredList[0]
                        index = FilteredList.index(event)
                        gimg = event.load_image()
                    else:
                        FilteredList = NextDayList
                        
            elif result[1] == 'building':
                python:
                    building = result[2]
                    FilteredList = []
                    for entry in NextDayList:
                        if entry.type == 'buildingreport' and entry.loc == building:
                            FilteredList.insert(0, entry)
                        elif entry.type == "jobreport" and entry.loc == building:
                            FilteredList.append(entry)
                    event = FilteredList[0]
                    index = FilteredList.index(event)
                    gimg = event.load_image()
                
            elif result[1] == "fighters_guild":
                python:
                    FilteredList = []
                    for entry in NextDayList:
                        if entry.type == "fg_report":
                            FilteredList.insert(0, entry)
                        elif entry.type == "exploration_report":
                            FilteredList.insert(1, entry)
                        elif entry.type == 'fg_job':
                            FilteredList.append(entry)
                    event = FilteredList[0]
                    index = FilteredList.index(event)
                    gimg = event.load_image()

        if result[0] == 'control':
            if result[1] == 'left':
                python:
                    index = FilteredList.index(event)
                    if index > 0:
                        event = FilteredList[index-1]
                        gimg = event.load_image()

            elif result[1] == 'right':
                python:
                    index = FilteredList.index(event)
                    if index < len(FilteredList)-1:
                        event = FilteredList[index+1]
                        gimg = event.load_image()
                    
            elif result[1] == 'return':
                return

screen next_day():

    default tt = Tooltip("Review days events here!")
    default show_summary = True
    default summary_filter = "buildings" # Not applicable atm
    default report_stats = False

    key "mousedown_3" action [Return(['control', 'return'])]
    
    if show_summary:
        # Here summary screen is build and constructed, most of the required logic is done directly here:
        # Right info/Filters frame:
        frame:
            background Frame (Transform("content/gfx/frame/p_frame6.png", alpha=0.98), 10, 10)
            xysize (581, 683)
            ypos 37
            xalign 1.0
            
            vbox:
                xalign 0.38
                # Prepear the data:
                python:
                    strippers = list()
                    whores = list()
                    sgs = list()
                    guards = list()
                    
                    for girl in hero.girls:
                        if traits["Stripper"] in girl.occupations:
                            strippers.append(girl)
                        elif traits["Prostitute"] in girl.occupations:
                            whores.append(girl)
                        elif "Server" in girl.occupations:
                            sgs.append(girl)
                        elif "Warrior"in girl.occupations:
                            guards.append(girl)
                
                frame: 
                    style_group "content"
                    xalign 0.5
                    ypos 5
                    xysize (330, 50)
                    background Frame("content/gfx/frame/namebox5.png", 10, 10)
                    label (u"Buildings") text_size 23 text_color ivory align(0.5, 0.6)
                    add ProportionalScale("content/gfx/images/birds1.png", 548, 115) pos (-100, 5)
                
                null height 80
                # ALL:
                frame:
                    xalign 0.5
                    xysize (515, 134)
                    background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                    hbox:
                        null width 3
                        $ img = "content/gfx/frame/MC_bg3.png"
                        button:
                            xysize (95, 95)
                            yalign 0.5
                            idle_background Frame(img, 5 ,5)
                            hover_background Frame(im.MatrixColor(img ,im.matrix.brightness(0.20)), 5, 5)
                            text "All" align (0.5, 0.5) style "stats_label_text" size 32
                            action [Return(['filter', 'all']), SetScreenVariable("show_summary", None)]
                            hovered tt.action(u"Show full report tree!")
                        
                        null width 5
                        frame:
                            align(0.5, 0.5)
                            xysize (300, 130)
                            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 5, 5)
                            vbox:
                                style_group "stats"
                                yfill True
                                spacing -7
                            
                                # Active (Numeric Info):
                                hbox:
                                    xpos 2
                                    spacing 2
                                    hbox:
                                        frame:
                                            xysize (285, 33)
                                            text "Active" yalign 0.5 xpos 3
                                            text ("%d" % len(list(girl for girl in strippers if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 115 yalign 0.6
                                            text ("%d" % len(list(girl for girl in whores if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 155 yalign 0.6
                                            text ("%d" % len(list(girl for girl in sgs if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 195 yalign 0.6
                                            text ("%d" % len(list(girl for girl in guards if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 235 yalign 0.6
                                
                                # Resting:
                                hbox:
                                    xpos 2
                                    spacing 2
                                    hbox:
                                        frame:
                                            xysize (285, 33)
                                            text "Resting" pos (3, -3)
                                            text ("%d" % len(list(girl for girl in strippers if girl.action in ("Rest", "AutoRest"))))  style "stats_value_text" xpos 115 yalign 0.6
                                            text ("%d" % len(list(girl for girl in whores if girl.action in ("Rest",  "AutoRest"))))  style "stats_value_text" xpos 155 yalign 0.6
                                            text ("%d" % len(list(girl for girl in sgs if girl.action in ("Rest",  "AutoRest"))))  style "stats_value_text" xpos 195 yalign 0.6
                                            text ("%d" % len(list(girl for girl in guards if girl.action in ("Rest", "AutoRest"))))  style "stats_value_text" xpos 235 yalign 0.6
                                 
                                # Events: 
                        
                                frame:
                                    xpos 2
                                    xysize (285, 33)
                                    text "Events" yalign 0.5 xpos 3
                        
                                    # Prepear the data:
                                    python:
                                        strippers = list()
                                        whores = list()
                                        sgs = list()
                                        guards = list()
                                
                                        for __ in NextDayList:
                                            if isinstance(__.char, Char):
                                                if traits["Stripper"] in __.char.occupations:
                                                    strippers.append(__)
                                                elif traits["Prostitute"] in __.char.occupations:
                                                    whores.append(__)
                                                elif "Server" in __.char.occupations:
                                                    sgs.append(__)
                                                elif "Warrior" in __.char.occupations:
                                                    guards.append(__)
                                                    
                                    hbox:
                                        xpos 115
                                        xmaximum 40
                                        text ("%d" % len(strippers)) style "stats_value_text" yalign 0.6
                                        python:
                                            red_flag = False
                                            green_flag = False
                                            for __ in strippers:
                                                if __.red_flag:
                                                    red_flag = True
                                                if __.green_flag:
                                                    green_flag = True
                                                if red_flag and green_flag:
                                                    break

                                        if red_flag:
                                            button:
                                                xpadding 1
                                                ypadding 1
                                                background Null()
                                                text "{color=[red]}!" style "next_day_summary_text"
                                                action NullAction()

                                        if green_flag:
                                            button:
                                                xpadding 1
                                                ypadding 1
                                                background Null()
                                                text "{color=[green]}!" style "next_day_summary_text"
                                                action NullAction()

                                        
                                    hbox:
                                        xpos 155
                                        xmaximum 40
                                        text ("%d" % len(whores)) style "stats_value_text" yalign 0.6
                                        python:
                                            red_flag = False
                                            green_flag = False
                                            for __ in whores:
                                                if __.red_flag:
                                                    red_flag = True
                                                if __.green_flag:
                                                    green_flag = True
                                                if red_flag and green_flag:
                                                    break

                                        if red_flag:
                                            button:
                                                xpadding 1
                                                ypadding 1
                                                background Null()
                                                text "{color=[red]}!" style "next_day_summary_text"
                                                action NullAction()

                                        if green_flag:
                                            button:
                                                xpadding 1
                                                ypadding 1
                                                background Null()
                                                text "{color=[green]}!" style "next_day_summary_text"
                                                action NullAction()

                                
                                    hbox:
                                        xpos 195
                                        xmaximum 40
                                        text ("%d" % len(sgs)) style "stats_value_text" yalign 0.6
                                        python:
                                            red_flag = False
                                            green_flag = False
                                            for __ in sgs:
                                                if __.red_flag:
                                                    red_flag = True
                                                if __.green_flag:
                                                    green_flag = True
                                                if red_flag and green_flag:
                                                    break

                                        if red_flag:
                                            button:
                                                xpadding 1
                                                ypadding 1
                                                background Null()
                                                text "{color=[red]}!" style "next_day_summary_text"
                                                action NullAction()

                                        if green_flag:
                                            button:
                                                xpadding 1
                                                ypadding 1
                                                background Null()
                                                text "{color=[green]}!" style "next_day_summary_text"
                                                action NullAction()

                                    hbox:
                                        xpos 235
                                        xmaximum 40
                                        text ("%d" % len(guards)) style "stats_value_text" yalign 0.6
                                        python:
                                            red_flag = False
                                            green_flag = False
                                            for __ in guards:
                                                if __.red_flag:
                                                    red_flag = True
                                                if __.green_flag:
                                                    green_flag = True
                                                if red_flag and green_flag:
                                                    break

                                        if red_flag:
                                            button:
                                                xpadding 1
                                                ypadding 1
                                                background Null()
                                                text "{color=[red]}!" style "next_day_summary_text"
                                                action NullAction()

                                        if green_flag:
                                            button:
                                                xpadding 1
                                                ypadding 1
                                                background Null()
                                                text "{color=[green]}!" style "next_day_summary_text"
                                                action NullAction()

                                frame:
                                    xpos 2
                                    xysize (285, 33)
                                    text "Customers:" yalign 0.5 xpos 3
                                    python:
                                        clients = 0
                                        businesses = [b for b in hero.buildings if isinstance(b, NewStyleUpgradableBuilding)]
                                        for b in businesses:
                                            clients = clients + b.total_clients
                                    hbox:
                                        xpos 115
                                        xmaximum 40
                                        text "[clients]" style "stats_value_text" ypos 1
                                
                        null width 4
                        # View all red flagged events:
                        python:
                            red_flags = False
                            for __ in NextDayList:
                                if __.red_flag:
                                    red_flags = True
                                    break
                                
                        if red_flags:
                            button:
                                yalign 0.5
                                xysize (90, 90)
                                idle_background Frame("content/gfx/frame/p_frame5.png", 5 ,5)
                                hover_background Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(0.10)), 5, 5)
                                text "!" align (0.5, 0.5) color red size 60 style "stats_text"
                                action [Return(['filter', 'red_flags']), SetScreenVariable("show_summary", None)]
                                hovered tt.action(u"View All events flagged Red!!")
                        else:
                            button:
                                yalign 0.5
                                xysize (90, 90)
                                idle_background Frame("content/gfx/frame/p_frame5.png", 5 ,5)
                                hover_background Frame("content/gfx/frame/p_frame5.png", 5 ,5)
                                action NullAction()
                    
                    
            side "c r":
                xalign 0.5
                ypos 285
                viewport id "Reports":
                    xysize (580, 365)
                    child_size (600, 10000)
                    draggable True
                    mousewheel True
                    vbox:
                        if summary_filter == "buildings":
                        
                            # Buildings ------------------------------------------------>>>
                            # FightersGuild ------------------------------------------>>>
                            if fg in hero.buildings:
                                # Prepear the data:
                                python:
                                    strippers = list()
                                    whores = list()
                                    sgs = list()
                                    guards = list()
                                    
                                    for girl in hero.girls:
                                        if girl.location == fg:
                                            if  traits["Stripper"] in girl.occupations:
                                                strippers.append(girl)
                                            elif traits["Prostitute"] in girl.occupations:
                                                whores.append(girl)
                                            elif "Server" in girl.occupations:
                                                sgs.append(girl)
                                            elif "Warrior" in girl.occupations:
                                                guards.append(girl)
                                                
                                # Image/Name
                                null height 5
                                hbox:
                                    null width 10
                                    text ("%s" % fg.name) style "stats_label_text"
                                null height 5
                                frame:
                                    xalign 1.0
                                    xysize (555, 134)
                                    background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                                    hbox:
                                        yalign 0.5
                                        null width 10
                                        frame:
                                            yalign 0.5
                                            xysize (95, 95)
                                            background Frame("content/gfx/frame/MC_bg3.png", 5 , 5)
                                            $ img = im.Scale(fg.img, 95, 95)
                                            imagebutton:
                                                align (0.5, 0.5)
                                                idle (img)
                                                hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
                                                action [Return(['filter', 'fighters_guild']), SetScreenVariable("show_summary", None)]
                                                hovered tt.action(u"View Events in FightersGuild!")
                                            if fg.flag_red:
                                                button:
                                                    align (0.95, 0.95)
                                                    background Null()
                                                    text "!" color red size 40 italic True
                                                    action NullAction()
                                                    hovered tt.action(u"There are building related events flagged Red!")
                                            elif fg.flag_green:
                                                button:
                                                    align (0.95, 0.95)
                                                    background Null()
                                                    text "!" color green size 40 italic True
                                                    action NullAction()
                                                    hovered tt.action(u"There are building related events flagged Green!")
                                            
                                        null width 6
                                        
                                        # Stats:
                                        frame:
                                            align(0.5, 0.5)
                                            xysize (410, 130)
                                            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 5, 5)
                                            vbox:
                                                style_group "stats"
                                                yfill True
                                                spacing -7
                                        
                                                # Active:
                                                hbox:
                                                    xpos 2
                                                    spacing 2
                                                    hbox:
                                                        frame:
                                                            xysize (405, 33)
                                                            text "Active" yalign 0.5 xpos 3
                                                            text ("%d" % len(list(girl for girl in strippers if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 115 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in whores if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 155 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in sgs if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 195 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in guards if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 235 yalign 0.7
                                                            text "Dirt" yalign 0.5 xpos 275
                                                            text ("%d%%" % fg.get_dirt_percentage()[0]) style "stats_value_text" xalign 1.0 yalign 0.9
                                              
                                                # Rest:
                                                hbox:
                                                    xpos 2
                                                    spacing 2
                                                    hbox:
                                                        frame:
                                                            xysize (405, 33)
                                                            text "Resting" yalign 0.5 xpos 3
                                                            text ("%d" % len(list(girl for girl in strippers if girl.action in ("Rest", "AutoRest")))) style "stats_value_text" xpos 115 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in whores if girl.action in ("Rest",  "AutoRest")))) style "stats_value_text" xpos 155 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in sgs if girl.action in ("Rest",  "AutoRest")))) style "stats_value_text" xpos 195 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in guards if girl.action in ("Rest", "AutoRest")))) style "stats_value_text" xpos 235 yalign 0.7
                                                            text "Fame" yalign 0.5 xpos 275
                                                            text ("%d/%d" % (fg.fame, fg.maxfame)) style "stats_value_text" xalign 1.0 yalign 0.9
                                                
                                                # Events:
                                                frame:
                                                    xpos 2
                                                    xysize (405, 33)
                                                    text "Events" yalign 0.5 xpos 3
                                            
                                                    # Prepear the data:
                                                    python:
                                                        strippers = list()
                                                        whores = list()
                                                        sgs = list()
                                                        guards = list()
                                                
                                                        for __ in NextDayList:
                                                            if isinstance(__.char, Char) and __.char.location == fg:
                                                                if traits["Stripper"] in __.char.occupations:
                                                                    strippers.append(__)
                                                                elif traits["Prostitute"] in __.char.occupations:
                                                                    whores.append(__)
                                                                elif "Server" in __.char.occupations:
                                                                    sgs.append(__)
                                                                elif "Warrior" in __.char.occupations:
                                                                    guards.append(__)
                                                        
                                                    hbox:
                                                        xpos 115
                                                        xmaximum 40
                                                        text ("%d" % len(strippers)) style "stats_value_text" yalign 0.6 
                                                        python:
                                                            red_flag = False
                                                            green_flag = False
                                                            for __ in strippers:
                                                                if __.red_flag:
                                                                    red_flag = True
                                                                if __.green_flag:
                                                                    green_flag = True
                                                                if red_flag and green_flag:
                                                                    break
    
                                                        if red_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[red]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                        if green_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[green]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                        
                                                    hbox:
                                                        xpos 155
                                                        xmaximum 40
                                                        text ("%d" % len(whores)) style "stats_value_text" yalign 0.6
                                                        python:
                                                            red_flag = False
                                                            green_flag = False
                                                            for __ in whores:
                                                                if __.red_flag:
                                                                    red_flag = True
                                                                if __.green_flag:
                                                                    green_flag = True
                                                                if red_flag and green_flag:
                                                                    break
    
                                                        if red_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[red]}!" style "next_day_summary_text"
                                                                action NullAction()
                                                        
                                                        if green_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[green]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                    hbox:
                                                        xpos 195
                                                        xmaximum 40
                                                        text ("%d" % len(sgs)) style "stats_value_text" yalign 0.6
                                                        python:
                                                            red_flag = False
                                                            green_flag = False
                                                            for __ in sgs:
                                                                if __.red_flag:
                                                                    red_flag = True
                                                                if __.green_flag:
                                                                    green_flag = True
                                                                if red_flag and green_flag:
                                                                    break
    
                                                        if red_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[red]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                        if green_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[green]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                    hbox:
                                                        xpos 235
                                                        xmaximum 40
                                                        text ("%d" % len(guards)) style "stats_value_text" yalign 0.6
                                                        python:
                                                            red_flag = False
                                                            green_flag = False
                                                            for __ in guards:
                                                                if __.red_flag:
                                                                    red_flag = True
                                                                if __.green_flag:
                                                                    green_flag = True
                                                                if red_flag and green_flag:
                                                                    break
    
                                                        if red_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[red]}!" style "next_day_summary_text"
                                                                action NullAction()
                                                        
                                                        if green_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[green]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                    hbox:
                                                        yalign 0.5
                                                        xpos 275
                                                        xmaximum 48
                                                        text "Rep."
                                                    hbox:
                                                        yalign 0.5
                                                        xalign 1.0
                                                        xmaximum 100
                                                        text ("%d/%d" % (fg.rep, fg.maxrep)) style "stats_value_text" yalign 0.9
                                            
                                                frame:
                                                    xpos 2
                                                    xysize (405, 33)
                                                # hbox: Not applicable
                                                    # text "Customers:" style "next_day_summary_text"
                                                    # null width 8
                                                    # text ("%d" % building.get_clients()) style "next_day_summary_text"
                    
                            # Buildings ------------------------------------------------->>>
                            $ buildings = [b for b in hero.buildings if isinstance(b, NewStyleUpgradableBuilding)]
                            for building in buildings:
                                
                                # Prepear the data:
                                python:
                                    strippers = list()
                                    whores = list()
                                    sgs = list()
                                    guards = list()
                                    
                                    for girl in hero.girls:
                                        if girl.location == building:
                                            if traits["Stripper"] in girl.occupations:
                                                strippers.append(girl)
                                            elif traits["Prostitute"] in girl.occupations:
                                                whores.append(girl)
                                            elif "Server" in girl.occupations:
                                                sgs.append(girl)
                                            elif "Warrior" in girl.occupations:
                                                guards.append(girl)
                                                
                                # Image/Name
                                null height 5
                                hbox:
                                    null width 10
                                    text "[building.name]" style "stats_label_text"
                                null height 5
                                frame:
                                    xalign 1.0
                                    xysize (555, 134)
                                    background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
                                    hbox:
                                        yalign 0.5
                                        null width 10
                                        frame:
                                            yalign 0.5
                                            xysize (95, 95)
                                            background Frame("content/gfx/frame/MC_bg3.png", 5 ,5)
                                            $ img = im.Scale(building.img, 95, 95)
                                            imagebutton:
                                                align (0.5, 0.5)
                                                idle (img)
                                                hover (im.MatrixColor(img ,im.matrix.brightness(0.15)))
                                                action [Return(['filter', 'building', building]), SetScreenVariable("show_summary", None)]
                                                hovered tt.action(u"View Events in %s building." % building.name)
                                            if building.flag_red:
                                                button:
                                                    align (0.95, 0.95)
                                                    background Null()
                                                    text "!" color red size 40 italic True
                                                    action NullAction()
                                                    hovered tt.action(u"There are building related events flagged Red!")
                                        
                                        null width 6
                                        
                                        # Stats:
                                        frame:
                                            align(0.5, 0.5)
                                            xysize (410, 130)
                                            background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 5, 5)
                                            vbox:
                                                style_group "stats"
                                                #yfill true
                                                spacing -7
                                        
                                                # Active:
                                                hbox:
                                                    xpos 2
                                                    spacing 2
                                                    hbox:
                                                        frame:
                                                            xysize (405, 33)
                                                            text "Active" yalign 0.5 xpos 3
                                                            text ("%d" % len(list(girl for girl in strippers if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 115 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in whores if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 155 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in sgs if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 195 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in guards if girl.action not in ("Rest", "AutoRest", None)))) style "stats_value_text" xpos 235 yalign 0.6
                                                            text "Dirt" yalign 0.5 xpos 275
                                                            text ("%d%%" % building.get_dirt_percentage()[0]) style "stats_value_text" xalign 1.0 yalign 0.9
                                          
                                                # Rest:
                                                hbox:
                                                    xpos 2
                                                    spacing 2
                                                    hbox:
                                                        frame:
                                                            xysize (405, 33)
                                                            text "Resting" yalign 0.5 xpos 3
                                                            text ("%d" % len(list(girl for girl in strippers if girl.action in ("Rest", "AutoRest")))) style "stats_value_text" xpos 115 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in whores if girl.action in ("Rest",  "AutoRest")))) style "stats_value_text" xpos 155 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in sgs if girl.action in ("Rest",  "AutoRest")))) style "stats_value_text" xpos 195 yalign 0.6
                                                            text ("%d" % len(list(girl for girl in guards if girl.action in ("Rest", "AutoRest")))) style "stats_value_text" xpos 235 yalign 0.6
                                                            text "Fame" yalign 0.5 xpos 275
                                                            text ("%d/%d" % (building.fame, building.maxfame)) style "stats_value_text" xalign 1.0 yalign 0.9
                                             
                                                # Events:
                                                frame:
                                                    xpos 2
                                                    xysize (405, 33)
                                                    text "Events" yalign 0.5 xpos 3
                                                
                                                    # Prepear the data:
                                                    python:
                                                        strippers = list()
                                                        whores = list()
                                                        sgs = list()
                                                        guards = list()
                                                    
                                                        for __ in NextDayList:
                                                            if isinstance(__.char, Char) and __.char.location == building:
                                                                if traits["Stripper"] in __.char.occupations:
                                                                    strippers.append(__)
                                                                elif traits["Prostitute"] in __.char.occupations:
                                                                    whores.append(__)
                                                                elif "Server" in __.char.occupations:
                                                                    sgs.append(__)
                                                                elif "Warrior" in __.char.occupations:
                                                                    guards.append(__)
                                                            
                                                    hbox:
                                                        xpos 115
                                                        xmaximum 40
                                                        text ("%d" % len(strippers)) style "stats_value_text" yalign 0.6
                                                        python:
                                                            red_flag = False
                                                            green_flag = False
                                                            for __ in strippers:
                                                                if __.red_flag:
                                                                    red_flag = True
                                                                if __.green_flag:
                                                                    green_flag = True
                                                                if red_flag and green_flag:
                                                                    break
    
                                                        if red_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[red]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                        if green_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[green]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                            
                                                    hbox:
                                                        xpos 155
                                                        xmaximum 40
                                                        text ("%d" % len(whores)) style "stats_value_text" yalign 0.6
                                                        python:
                                                            red_flag = False
                                                            green_flag = False
                                                            for __ in whores:
                                                                if __.red_flag:
                                                                    red_flag = True
                                                                if __.green_flag:
                                                                    green_flag = True
                                                                if red_flag and green_flag:
                                                                    break
    
                                                        if red_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[red]}!" style "next_day_summary_text"
                                                                action NullAction()
                                                            
                                                        if green_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[green]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                    
                                                    hbox:
                                                        xpos 195
                                                        xmaximum 40
                                                        text ("%d" % len(sgs)) style "stats_value_text" yalign 0.6
                                                        python:
                                                            red_flag = False
                                                            green_flag = False
                                                            for __ in sgs:
                                                                if __.red_flag:
                                                                    red_flag = True
                                                                if __.green_flag:
                                                                    green_flag = True
                                                                if red_flag and green_flag:
                                                                    break
    
                                                        if red_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[red]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                        if green_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[green]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                    
                                                    hbox:
                                                        xpos 235
                                                        xmaximum 40
                                                        text ("%d" % len(guards)) style "stats_value_text" yalign 0.6
                                                        python:
                                                            red_flag = False
                                                            green_flag = False
                                                            for __ in guards:
                                                                if __.red_flag:
                                                                    red_flag = True
                                                                if __.green_flag:
                                                                    green_flag = True
                                                                if red_flag and green_flag:
                                                                    break
    
                                                        if red_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[red]}!" style "next_day_summary_text"
                                                                action NullAction()
                                                        
                                                        if green_flag:
                                                            button:
                                                                xpadding 1
                                                                ypadding 1
                                                                background Null()
                                                                text "{color=[green]}!" style "next_day_summary_text"
                                                                action NullAction()

                                                        
                                                    hbox:
                                                        yalign 0.5
                                                        xpos 275
                                                        xmaximum 48
                                                        text "Rep."
                                                    hbox:
                                                        yalign 0.5
                                                        xalign 1.0
                                                        xmaximum 100
                                                        text ("%d/%d" % (fg.rep, fg.maxrep)) style "stats_value_text" yalign 0.9
                                            
                                                hbox:
                                                    frame:
                                                        xpos 2
                                                        xysize (405, 33)
                                                        text "Customers:" yalign 0.5 xpos 3
                                                        text "[building.total_clients]" style "stats_value_text" ypos 1 xpos 115
                                    
                vbar value YScrollValue("Reports")
        
        # Buttons will be drawn over the frame +==============================>>>
        if summary_filter == "buildings":
            $ start_pos = 844
            for i in ("Strippers", "Whores", "Service G.", "Warriors"):
                $ start_pos = start_pos + 42
                frame:
                    at rotate_by(45)
                    pos (start_pos, 95)
                    xysize (90, 30)
                    background Frame("content/gfx/interface/buttons/button_wood_right_hover.png", 3, 3)
                    text "[i]" size 12 bold True xalign 0.1
                
        # Mid frame:
        frame:
            pos (275, 250)
            xysize (430, 349)
            background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
            vbox:
                xalign 0.5
                # Hero Filter/Portrait:
                frame:
                    xalign 0.5
                    xysize (414, 120)
                    background Frame("content/gfx/frame/ink_box.png", 10 ,10)
                    $ img = hero.show("portrait", resize=(95, 95), cache=True)
                    frame:
                        background Frame("content/gfx/frame/MC_bg3.png", 10 ,10)
                        align (0.25, 0.8)
                        imagebutton:
                            idle (img)
                            hover (im.MatrixColor(img ,im.matrix.brightness(0.15)))
                            action [Return(['filter', 'mc']), SetScreenVariable("show_summary", None)]
                            hovered tt.action(u"Show personal MC report!")
                    frame:
                        style_group "stats"
                        yalign 0.5
                        xpos 178
                        xysize (148, 105)
                        background Frame(Transform("content/gfx/frame/P_frame2.png", alpha=0.6), 10, 10)
                        vbox:
                            label "[hero.name]":
                                text_size 16
                                text_bold True
                                xpos 38
                                yalign 0.03
                                text_color ivory
                            fixed: # HP
                                xysize (150, 25)
                                xanchor -8
                                bar:
                                    yalign 0.5
                                    left_bar ProportionalScale("content/gfx/interface/bars/hp1.png", 150, 20)
                                    right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                    value hero.health
                                    range hero.get_max("health")
                                    thumb None
                                    xysize (150, 20)
                                text "HP" size 14 color ivory bold True yalign 0.1 xpos 8
                                if hero.health <= hero.get_max("health")*0.2:
                                    text "[hero.health]" size 14 color red bold True style "stats_value_text" yoffset -3 xpos 102
                                else:
                                    text "[hero.health]" size 14 color ivory bold True style "stats_value_text" yoffset -3 xpos 102
                    
                            fixed: # MP
                                xysize (150, 25)
                                xanchor -5
                                bar:
                                    yalign 0.2
                                    left_bar ProportionalScale("content/gfx/interface/bars/mp1.png", 150, 20)
                                    right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                    value hero.mp
                                    range hero.get_max("mp")
                                    thumb None
                                    xysize (150, 20)
                                text "MP" size 14 color ivory bold True yalign 0.8 xpos 7
                                if hero.mp <= hero.get_max("mp")*0.2:
                                    text "[hero.mp]" size 14 color red bold True style "stats_value_text" yoffset 2 xpos 99
                                else:
                                    text "[hero.mp]" size 14 color ivory bold True style "stats_value_text" yoffset 2 xpos 99
                    
                            fixed: # VIT
                                xysize (150, 25)
                                xanchor -2
                                bar:
                                    yalign 0.5
                                    left_bar ProportionalScale("content/gfx/interface/bars/vitality1.png", 150, 20)
                                    right_bar ProportionalScale("content/gfx/interface/bars/empty_bar1.png", 150, 20)
                                    value hero.vitality
                                    range hero.get_max("vitality")
                                    thumb None
                                    xysize (150, 20)
                                text "VP" size 14 color ivory bold True yalign 0.8 xpos 7
                                if hero.vitality <= hero.get_max("vitality")*0.2:
                                    text "[hero.vitality]" size 14 color red bold True style "stats_value_text" yoffset 2 xpos 99
                                else:
                                    text "[hero.vitality]" size 14 color ivory bold True style "stats_value_text" yoffset 2 xpos 99
                                add ProportionalScale("content/gfx/images/c1.png", 123, 111) pos (-42, 55)
            
        # MC (extra info) -------------------------------------------->>>
                # Prepearing info:
                python:
                    for __ in NextDayList:
                        if __.type == "mcndreport":
                            report = __
            
                if  __.red_flag:
                    button:
                        anchor (-196, 50)
                        yalign 1.0
                        background Frame("content/gfx/frame/p_frame5.png", 5 ,5)
                        text "!" color red size 40 style "stats_text"
                        action NullAction()
                        hovered tt.action(u"Red flag in MC's Report!")
            
            # School:
            frame:
                align (0, 1.0)
                xysize (95, 95)
                background Frame("content/gfx/frame/MC_bg3.png", 5, 5)
                $ img = im.Scale(schools["-PyTFall Educators-"].img, 95, 95)
                imagebutton:
                    align (0.5, 0.5)
                    idle (img)
                    hover (im.MatrixColor(img ,im.matrix.brightness(0.15)))
                    action [Return(['filter', 'school']), SetScreenVariable("show_summary", None)]
                    hovered tt.action(u"View School and School Events!")
                    
            # Girlz:
            frame:
                align (1.0, 1.0)
                xysize (95, 95)
                background Frame("content/gfx/frame/MC_bg3.png", 5, 5)
                $ img = im.Scale("content/gfx/bg/gallery.jpg", 95, 95)
                imagebutton:
                    align (0.5, 0.5)
                    idle (img)
                    hover (im.MatrixColor(img ,im.matrix.brightness(0.15)))
                    action [Return(['filter', 'gndreports']), SetScreenVariable("show_summary", None)]
                    hovered tt.action(u"Show personal girl reports!")
            
            vbox:
                align (0.5, 0.85)
                spacing 3
                # Getting data:
                python:
                    free = 0
                    slaves = 0
                    for girl in hero.girls:
                        if girl.status == "slave":
                            slaves = slaves + 1
                        else:
                            free = free + 1
                            
                hbox:
                    spacing 5
                    add ProportionalScale("content/gfx/interface/icons/slave.png", 50, 50)
                    text ("%d" % slaves) style "agrevue"
                    null width 240
                    text ("%d" % free) style "agrevue"
                    add ProportionalScale("content/gfx/interface/icons/free.png", 50, 50)
                    
                null height 90
                
                # Data:
                python:
                    unas = list()
                    for girl in hero.girls:
                        if not girl.action:
                            unas.append(girl)
                if unas:
                    text ("{color=[red]}Unassigned: %d" % len(unas)) style "agrevue"
                else:
                    text ("{color=[green]}Unassigned: -") style "agrevue"
        
        # School (extra info) ---------------------------------------->>>         
            # Prepearing info:
            python:
                for school in NextDayList:
                    if school.type == "schoolndreport":
                        break
            
            if  "We inform you about fresh courses starting today." in school.txt:
                button:
                    yalign 0.5
                    xalign 0
                    background Frame("content/gfx/frame/p_frame5.png", 5 ,5)
                    text "+" color green size 40 style "stats_text"
                    action NullAction()
                    hovered tt.action(u"New Cources availible!")
            hbox:
                yalign 0.5
                xalign 0
                if "has successfully completed" in school.txt:
                    button:
                        background Frame("content/gfx/frame/p_frame5.png", 5 ,5)
                        text "!" color yellow size 40 style "stats_text"
                        action NullAction()
                        hovered tt.action(u"One of your girls has successfully completed her cource (this doesn't mean that a cource has ended)!")
                if "is attending is at it's end" in school.txt:
                    button:
                        background Frame("content/gfx/frame/p_frame5.png", 5 ,5)
                        text "!" color yellow size 40 style "stats_text"
                        action NullAction()
                        hovered tt.action(u"A course one of your girls attended has ended!")
        
                        
        # Girlz (extra info) ------------------------------------------->>>
            # Prepearing info:
            python:
                red_flags = False
                for __ in NextDayList:
                    if __.type == "girlndreport" and __.red_flag:
                        red_flags = True
            
            if  red_flags:
                button:
                    yalign 0.7
                    xalign 0.61
                    background Frame("content/gfx/frame/p_frame5.png", 5 ,5)
                    text "!" color red size 40 style "stats_text"
                    action NullAction()
                    hovered tt.action(u"Red flag in Girlz personal Reports!")
                        
                        
        # Left Box ==========================================================================>>>>            
        # Fin:
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
            xysize (277, 560)
            pos(2, 37)
            
            # Day Total ===========================================>>>
            $ fin_inc = hero.fin.game_fin_log[str(day-1)][0]["private"]
            $ fin_exp = hero.fin.game_fin_log[str(day-1)][1]["private"]
            
            frame:
                background Frame (Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 10, 10)
                xysize (270, 550)
                xanchor 5
                yanchor 2
                frame:
                    style_group "content"
                    align (0.5, 0.015)
                    xysize (210, 40)
                    background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.6), 10, 10)
                    label (u"Daily Balance") text_size 23 text_color ivory align(0.55, 0.03)
                vbox:
                    style_group "stats"
                    hbox:
                        yfill True
                        ypos 53
                        vbox:
                            spacing -7
                            xanchor 0
                            xmaximum 140
                            xfill True
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            frame:
                                xsize 260
                                text("")
                            add ProportionalScale("content/gfx/images/magic2.png", 120, 120) pos (150, -50)
                        hbox:
                            vbox:
                                spacing 5
                                yanchor -5
                                xanchor 130
                                xmaximum 185
                                xfill True
                                for key in fin_inc:
                                    text("[key]") color green
                                for key in fin_exp:
                                    text("[key]") color red
                            vbox:
                                yanchor -9
                                spacing 9
                                xfill True
                                xanchor 110
                                xminimum 108
                                xmaximum 108
                                for key in fin_inc:
                                    $ val = fin_inc[key]
                                    text("[val]") color green style "stats_value_text" xalign (1.0)
                                for key in fin_exp:
                                    $ val = fin_exp[key]
                                    text("[val]") color red style "stats_value_text" xalign (1.0)
                        
                    python:
                        total_income = 0
                        total_expenses = 0
                    
                        for key in fin_inc:
                            total_income += fin_inc[key]
                        for key in fin_exp:
                            total_expenses += fin_exp[key]
                        
                        total = total_income - total_expenses
                
                    if total > 0:
                        hbox:
                            yfill True
                            vbox:
                                yalign (1.0)
                                xmaximum 90
                                xfill True
                                text "-------------------------------------------------" color green anchor (-8, -13)
                                frame:
                                    xsize 260
                                    text("Total") color green size 24 xpos 2 yanchor 7
                                    text "-------------------------------------------------" color green anchor (-2, -6)
                            vbox:
                                yalign 1.0
                                xfill True
                                xminimum 160
                                xmaximum 160
                                text("[total]") color green size 20 style "stats_value_text" xalign 1.0
                    else:
                        hbox:
                            yfill True
                            vbox:
                                yalign (1.0)
                                xmaximum 90
                                xfill True
                                text "------------------------------------------------" color red anchor (-8, -13)
                                frame:
                                    xsize 260
                                    text("Total") color red size 24 xpos 2 yanchor 7
                                    text "------------------------------------------------" color red anchor (-2, -6)
                            vbox:
                                yalign 1.0
                                xfill True
                                xminimum 160
                                xmaximum 160
                                text("[total]") color red size 20 style "stats_value_text" xalign 1.0
                        
        # Game Total!    =============================================>>>
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
            xysize (429, 220)
            pos(276, 37)
            style_group "content"
            frame: 
                ypos 6
                xalign 0.5
                xysize (380, 50)
                background Frame("content/gfx/frame/namebox5.png", 10, 10)
                label (u"Game Total") text_size 23 text_color ivory align(0.5, 0.6) #text_outlines [(2, "#424242", 0, 0)]
            null height 1
            frame:
                align(0.5, 0.95)
                xysize (414, 150)
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.6), 5, 5)
                add ProportionalScale("content/gfx/images/jp1.png", 68, 101) pos (325, 5)
                add ProportionalScale("content/gfx/images/jp2.png", 73, 103) pos (12, 5)
                python:
                    income = dict()
                    for _day in hero.fin.game_fin_log:
                        for key in hero.fin.game_fin_log[_day][0]["private"]:
                            income[key] = income.get(key, 0) + hero.fin.game_fin_log[_day][0]["private"][key]
                    expenses = dict()
                    for _day in hero.fin.game_fin_log:
                        for key in hero.fin.game_fin_log[_day][1]["private"]:
                            expenses[key] = expenses.get(key, 0) + hero.fin.game_fin_log[_day][1]["private"][key]
                            
                    game_total = 0
                    total_income = sum(income.values())
                    total_expenses = sum(expenses.values())
                    game_total = total_income - total_expenses
                                
                hbox:
                    style_group "stats"
                    yfill True
                    vbox:
                        spacing -7
                        yanchor -24
                        xanchor -82
                        xmaximum 75
                        xfill True
                        frame:
                            xsize 240
                            text("Earnings") color green
                        frame:
                            xsize 240
                            text("Expences") color red
                    vbox:
                        yanchor -34
                        spacing 9
                        xfill True
                        xanchor -82
                        xminimum 158
                        xmaximum 158
                        text("[total_income]") color green style "stats_value_text" xalign (1.0)
                        text("[total_expenses]") color red style "stats_value_text" xalign (1.0)
                        
                    
                if game_total > 0:
                    hbox:
                        style_group "stats"
                        yfill True
                        vbox:
                            yalign (1.0)
                            xmaximum 90
                            xfill True
                            text "------------------------------------------------------------------------------" color green anchor (-8, -13)
                            frame:
                                xsize 404
                                text("Total") color green size 24 xpos 60 yanchor 7
                                text "------------------------------------------------------------------------------" color green anchor (-2, -6)
                        vbox:
                            yalign 1.0
                            xfill True
                            xminimum 240
                            xmaximum 240
                            text("[game_total]") color green size 20 style "stats_value_text" xalign 1.0
                else:
                    hbox:
                        style_group "stats"
                        yfill True
                        vbox:
                            yalign (1.0)
                            xmaximum 90
                            xfill True
                            text "------------------------------------------------------------------------------" color red anchor (-8, -13)
                            frame:
                                xsize 404
                                text("Total") color red size 24 xpos 60 yanchor 7
                                text "------------------------------------------------------------------------------" color red anchor (-2, -6)
                        vbox:
                            yalign 1.0
                            xfill True
                            xminimum 240
                            xmaximum 240
                            text("[game_total]") color red size 20 style "stats_value_text" xalign 1.0
                            
        # Tooltip Frame       
        frame background Frame("content/gfx/frame/mes12.jpg", 10, 10):
            xysize (700, 125)
            xpadding 10
            pos (3, 594)
            text(u"{size=20}{color=[ivory]}%s" % tt.value) yalign 0.1
                   
        use top_stripe(True)
            
    #  Reports  =============================================================================>>>>
    else:
        
        key "mousedown_4" action Return(['control', 'right'])
        key "mousedown_5" action Return(['control', 'left'])
        
        # Image frame:
        frame:
            pos (0, 0)
            xysize (835, 720)
            background Frame("content/gfx/frame/p_frame7.png", 10, 10)
            xpadding 0
            ypadding 0
            xmargin 0
            ymargin 0
            frame:
                align(0.5, 0.5)
                xpadding 7
                ypadding 7
                xmargin 0
                ymargin 0
                background Frame("content/gfx/frame/MC_bg3.png", 10 ,10)
                add gimg align (0.5, 0.5)
        
        # Stat Frames:
        showif report_stats:
            # Girls Stats Frame:
            frame background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10):
                at slide(so1=(136, 0), eo1=(0, 0), t1=0.4,
                             so2=(0, 0), eo2=(136, 0), t2=0.3)
                pos (690, -2)
                viewport id "nextdaygsf_vp":
                    xysize (136, 400)
                    # draggable True
                    # mousewheel True
                    # if event.type in ["jobreport", "schoolreport", "girlndreport", "mcndreport", "exploration_report"]: # <-- Not usefull???
                    if event.charmod:    
                        vbox:
                            null height 25
                            frame:
                                style_group "content"
                                xalign 0.5
                                xysize (136, 40)
                                background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.7), 10, 10)
                                label (u"Char Stats:") text_size 18 text_color ivory align (0.5, 0.5)
                            null height 10
                            vbox:
                                spacing -7
                                style_group "stats"
                                xmaximum 140
                                for key in event.charmod:
                                    if event.charmod[key] != 0:
                                        vbox:
                                            frame:
                                                background Frame(Transform("content/gfx/frame/stat_box.png", alpha=0.7), 5, 5)
                                                xsize 136
                                                text (u"{size=-1}%s:"%str(key).capitalize()) pos (3, -4)
                                                if event.charmod[key] > 0:
                                                    label (u"{size=-5}{color=[lawngreen]}%d"%event.charmod[key]) style "stats_value_text" align (1.0, 0.5)
                                                else:
                                                    label (u"{size=-5}{color=[red]}%d"%event.charmod[key]) style "stats_value_text" align (1.0, 0.5)
                                                        
            
            # Buildings Stats Frame:
            frame background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10):
                at slide(so1=(136, 0), eo1=(0, 0), t1=0.4,
                             so2=(0, 0), eo2=(136, 0), t2=0.3)
                pos (690, 406)
                viewport id "nextdaybsf_vp":
                    xysize (136, 305)
                    #draggable False
                    #mousewheel True
                    if event.type=="jobreport":
                        vbox:
                            null height 5
                            frame:
                                style_group "content"
                                xalign 0.5
                                xysize (136, 40)
                                background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.7), 10, 10)
                                label (u"Building Stats:") text_size 18 text_color ivory align(0.5, 0.5)
                            null height 10
                            vbox:
                                spacing -7
                                style_group "stats"
                                xmaximum 140
                                for key in event.locmod:
                                    if event.locmod[key] != 0:
                                        vbox:
                                            frame:
                                                background Frame (Transform("content/gfx/frame/stat_box.png", alpha=0.7), 5, 5)
                                                xsize 136
                                                if key == "reputation":
                                                    $ hkey = "Rep"
                                                else:
                                                    $ hkey = key
                                                text (u"{size=-1} %s:"%hkey.capitalize()) pos (1, -4)
                                                label (u"{size=-5}%d"%event.locmod[key]) style "stats_value_text" align (1.0, 0.5)
                
        # Text Frame + Stats Reports Mousearea:
        frame background Frame("content/gfx/frame/p_frame5.png", 15, 15):
            xysize (449, 609)
            pos (834, -2)
            vbox:
                frame:
                    ypos 10
                    style_group "content"
                    xalign 0.5
                    xysize (330, 60)
                    background Frame("content/gfx/frame/namebox5.png", 10, 10)
                    label (u"Description:") text_size 23 text_color ivory align(0.5, 0.6)
                frame:
                    background Frame(Transform("content/gfx/frame/mc_bg.png", alpha=0.5), 5, 5)
                    xysize (435, 520)
                    ypos 15
                    side "c l":
                        ypos 5
                        xalign 0.5
                        viewport id "nextdaytxt_vp":
                            xysize (400, 500)
                            draggable True
                            mousewheel True
                            has vbox
                            null height 10
                            text u"{}".format(event.txt) style "TisaOTMolxm" size 20
                        vbar value YScrollValue("nextdaytxt_vp")
                 
        mousearea:
            area (834, -2, 449, 609)
            hovered SetScreenVariable("report_stats", True)
            unhovered SetScreenVariable("report_stats", False)
        # Bottom Buttons:
        frame:
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
            pos (834, 603)
            xysize (449, 120)
            vbox:
                align (0.5, 0.5)
                spacing 8
                hbox:
                    align (0.5, 0.5)
                    spacing 20
                    button:
                        xysize (120, 40)
                        style "left_wood_button"
                        action Return(['control', 'left'])
                        hovered tt.action("<== View Previous Event")
                        text "Previous Event" style "wood_text" xalign(0.6) size 10
                    frame:
                        align (0.5, 0.5)
                        background Frame (Transform("content/gfx/frame/p_frame5.png", alpha=0.9), 5, 5)
                        xysize (90, 40)
                        text(u'Act: %d/%d'%(FilteredList.index(event)+1, len(FilteredList))) align (0.5, 0.5) size 16 style "stats_text"
                    button:
                        xysize (120, 40)
                        style "right_wood_button"
                        action Return(['control', 'right'])
                        hovered tt.action("View Next Event ==>")
                        text "Next Event" style "wood_text" xalign(0.4) size 10
                hbox:
                    align (0.5, 0.5)
                    spacing 20
                    textbutton "-Next Day-":
                        style "main_screen_4_button"
                        hovered tt.action("Begin New day and watch the results.")
                        action [Hide("mainscreen"), Jump("next_day")]
                        text_size 16
                        xysize (150, 20)
                    
                    $ img = im.Scale("content/gfx/interface/buttons/close.png", 40, 40)
                    imagebutton:
                        align (0.5, 0.5)
                        idle img
                        hover im.MatrixColor(img, im.matrix.brightness(0.25))
                        action Return(['control', 'return'])
                        hovered tt.Action("Return to previous screen!")
                
                    textbutton "-Summary-":
                        style "main_screen_4_button"
                        hovered tt.action("Back to ND Summary!")
                        action SetScreenVariable("show_summary", True)
                        text_size 16
                        xysize (150, 20)
