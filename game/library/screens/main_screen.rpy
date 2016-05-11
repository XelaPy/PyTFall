label mainscreen:
    
    # Music related:
    # First Run (Fadeout added)
    if global_flags.flag("game_start"):
        $ global_flags.del_flag("game_start")
        $ fadein = 15
    else:
        $ fadein = 0
            
    if not "pytfall" in ilists.world_music:
        $ ilists.world_music["pytfall"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("pytfall")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["pytfall"]) fadein fadein
    $ global_flags.del_flag("keep_playing_music")
    
    scene black
    show screen mainscreen
    # with pixellate
    
    # Prediction Helpers:
    # TODO: Stop predicions when we've moved to far away from the images!
    python:
        imglist = ["".join([pytfall.map_pattern, key, ".png"]) for key in list(i["id"] for i in pytfall.maps("pytfall"))]
        imglist.extend(["".join([pytfall.map_pattern, key, "_hover.png"])  for key in list(i["id"] for i in pytfall.maps("pytfall"))])
        imglist.extend("".join(["content/gfx/interface/buttons/locations/", key, ".png"]) for key in ["main_street",
                               "arena_outside", "slave_market", "city_jail", "tavern_town",
                               "city_parkgates", "academy_town", "mages_tower",
                               "graveyard_town", "city_beach", "forest_entrance", "hiddenvillage_entrance"])
        imglist.append("bg gallery")
        imglist.append("content/gfx/images/m_1.png")
        imglist.append("content/gfx/frame/h2.png")
        imglist.append("content/gfx/interface/buttons/compass.png")
        imglist.append("content/gfx/images/m_2.png")
        renpy.start_predict(*imglist)
    
    $ pytfall.world_events.next_day() # Get new set of active events
    $ pytfall.world_quests.run_quests("auto") # Unsquelch active quests
    $ pytfall.world_events.run_events("auto") # Run current events
    $ pytfall.world_quests.next_day() # Garbage collect quests
    
    while 1:
        $ result = ui.interact()
        
        if len(result) > 1:
            python:
                pytfall.sm.set_index()
                renpy.hide_screen("mainscreen")
                pytfall.arena.seen_report = True
                jump(result[1])
                
        elif result[0] == "chars_list":
            stop world
            $ renpy.hide_screen("mainscreen")
            $ pytfall.arena.seen_report = True
            # scene bg gallery
            # with irisin
            $ jump(result[0])
            
        elif result[0] == "city":
            $ global_flags.set_flag("keep_playing_music")
            $ renpy.hide_screen("mainscreen")
            $ pytfall.arena.seen_report = True
            scene bg humans
            # with irisin
            $ jump(result[0])
            
        else:
            python:
                renpy.hide_screen("mainscreen")
                pytfall.arena.seen_report = True
                jump(result[0])


screen mainscreen():
    
    # Tooltip related:
    default tt = Tooltip("Welcome to PyTFall!\nHave a nice game!!!")
    
    # Main pic:
    add im.Scale("content/gfx/bg/bg085_rsz.jpg", config.screen_width, config.screen_height-40) at fade_from_to(0.0, 1.0, 2.0) ypos 40

    frame:
        align (0.995, 0.88)
        background Frame("content/gfx/frame/window_frame2.png", 30, 30)
        xysize (255, 670)
        xfill True
        yfill True
        
        add "".join(["content/gfx/interface/images/calendar/","cal ", calendar.moonphase(), ".png"]) xalign 0.485 ypos 83
        
        text "{font=fonts/TisaOTM.otf}{k=-1}{color=#FFEC8B}{size=18}%s" % calendar.weekday() xalign 0.5 ypos 210

        text "{font=fonts/TisaOTM.otf}{k=-0.5}{color=#FFEC8B}{size=18}%s" % calendar.string() xalign 0.5 ypos 250

        vbox:
            style_group "main_screen_3"
            xalign 0.5
            ypos 305
            spacing 15
            textbutton "Girls":
                action Stop("world"), Hide("mainscreen"), Jump("chars_list")
                hovered tt.Action('Here you can see a list of all girls you possess, their stats and characteristics.\nIt is also here you can change their equipment and sell them.')
            textbutton "Buildings":
                action Return(["building_management"])
                hovered tt.Action('Here you can see a list of all your buildings. \nIt is also here you can you can upgrade your building and advertice them.')
            if config.developer:
                textbutton "Fighters Guild":
                    action Return(["fg_management"])
                    hovered tt.Action('Fighters Guild can be managed from here!')
            textbutton "Go to the City":
                action Return(["city"])
                hovered tt.Action('Explore the city.\nIf you are lucky, you may even find something interesting to do there...')
    
            null height 10
            
            textbutton "-Next Day-":
                style "main_screen_4_button"
                if day > 1:
                    hovered tt.action("Begin New day and watch the results. Click RMB to review reports")
                    action [Hide("mainscreen"), Jump("next_day")]
                    alternate SetVariable("just_view_next_day", True), Hide("mainscreen"), Jump("next_day")
                else:
                    hovered tt.action("Begin New day and watch the results.")
                    action [Hide("mainscreen"), Jump("next_day")]
           
    if config.developer:
        vbox:
            style_group "dropdown_gm"
            spacing 1
            align (0.01, 0.5)
            textbutton "Arena Inside":
                action Hide("mainscreen"), Jump("arena_inside")
            textbutton "Test BE":
                action Hide("mainscreen"), Jump("test_be")
            textbutton "Test BE Logical":
                action Hide("mainscreen"), Jump("test_be_logical")
            textbutton "Test Forest Exploration":
                action [Hide("mainscreen"), Jump("forest_exploration")]
            textbutton "Free Test":
                action Hide("mainscreen"), Jump("frog_deathfight")
            textbutton "Examples":
                action [Hide("mainscreen"), Jump("examples")]

    showif pytfall.ms_text and pytfall.todays_first_view:
        frame:
            pos (500, 95)
            xysize (500, 500)
            background Frame(Transform(("content/gfx/frame/arena_d.png"), alpha=0.7), 30, 30)
            text "%s"%pytfall.ms_text align (0.5, 0.5) style "content_text" color ivory
            timer 15 action ToggleField(pytfall, "todays_first_view")
            
    # Tooltip related:
    frame:
        background Frame("content/gfx/frame/window_frame1.png", 10, 10)
        align(0.5, 0.997)
        xysize (750, 100)
        text (u"{=content_text}{size=24}{color=[ivory]}%s" % tt.value) align(0.5, 0.5)

    use top_stripe(False)
