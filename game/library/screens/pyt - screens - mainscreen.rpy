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
    show screen pyt_mainscreen
    # with pixellate
    
    # Prediction Helpers:
    # TODO: Stop predicions when we've moved to far away from the images!
    python:
        imglist = ["".join([pytfall.map_pattern, key, ".png"]) for key in list(i["id"] for i in pytfall.maps("pytfall"))]
        imglist.extend(["".join([pytfall.map_pattern, key, "_hover.png"])  for key in list(i["id"] for i in pytfall.maps("pytfall"))])
        imglist.append("bg gallery")
        renpy.start_predict(*imglist)
    
    $ pytfall.world_events.next_day() # Get new set of active events
    $ pytfall.world_quests.run_quests("auto") # Unsquelch active quests
    $ pytfall.world_events.run_events("auto") # Run current events
    $ pytfall.world_quests.next_day() # Garbage collect quests
    
    while True:
        $ result = ui.interact()
        
        if len(result) > 1:
            python:
                pytfall.sm.set_index()
                renpy.hide_screen("pyt_mainscreen")
                pytfall.arena.seen_report = True
                jump(result[1])
        elif result[0] == "girls_list":
            stop world
            $ renpy.hide_screen("pyt_mainscreen")
            $ pytfall.arena.seen_report = True
            # scene bg gallery
            # with irisin
            $ jump(result[0])
        elif result[0] == "pyt_city":
            $ global_flags.set_flag("keep_playing_music")
            $ renpy.hide_screen("pyt_mainscreen")
            $ pytfall.arena.seen_report = True
            scene bg humans
            # with irisin
            $ jump(result[0])
        else:
            python:
                renpy.hide_screen("pyt_mainscreen")
                pytfall.arena.seen_report = True
                jump(result[0])


screen pyt_mainscreen():
    
    # Tooltip related:
    default tt = Tooltip("Welcome to PyTFall!\nHave a nice game!!!")
    
    # Main pic:
    add (im.Scale("content/gfx/bg/bg085_rsz.jpg", config.screen_width, config.screen_height-40)) at sfade(0.0, 1.0, 2.0) ypos 40
    # add("rukia_mast") align(0.5, 0.5) # align(0.9999, 0.9999)

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
                # action Return(["girls_list"])
                action Stop("world"), Hide("pyt_mainscreen"), Show("pyt_girlslist", dissolve, source=GuiGirlsList(), page=0, total_pages=1), Jump("girls_list")
                hovered tt.Action('Here you can see a list of all girls you possess, their stats and characteristics.\nIt is also here you can change their equipment and sell them.')
            textbutton "Buildings":
                action Return(["brothel_management"])
                hovered tt.Action('Here you can see a list of all your buildings. \nIt is also here you can you can upgrade your building and advertice them.')
            if fg in hero.buildings or config.developer:
                textbutton "Fighters Guild":
                    action Return(["fg_management"])
                    hovered tt.Action('Fighters Guild can be managed from here!')
            textbutton "Go to the City":
                action Return(["pyt_city"])
                hovered tt.Action('Explore the city.\nIf you are lucky, you may even find something interesting to do there...')
    
            null height 10
            
            textbutton "-Next Day-":
                style "main_screen_4_button"
                hovered tt.action("Begin New day and watch the results.")
                action [Hide("pyt_mainscreen"), Jump("next_day")]
           
    if config.developer:
        vbox:
            style_group "dropdown_gm"
            spacing 1
            align (0.01, 0.5)
            textbutton "Test BE":
                # action Function(renpy.show_screen, "pyt_display_disposition", str(random.random()), 1000, 40, 530, 400, 5)
                action Hide("pyt_mainscreen"), Jump("test_be")
            textbutton "Test Forest Exploration":
                action [Hide("pyt_mainscreen"), Jump("forest_exploration")]
            textbutton "Free Test":
                action Hide("pyt_mainscreen"), Jump("frog_deathfight")
            textbutton "Examples":
                action [Hide("pyt_mainscreen"), Jump("examples")]

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

    use pyt_top_stripe(False)
