init:
    # Portrait overlays (for enhancing emotions):
    image angry_pulse = "content/gfx/animations/interactions/angry.png"
    image sweat_drop = "content/gfx/animations/interactions/uncertain.png"
    image scared_lines = "content/gfx/animations/interactions/scared.png"
    image question_mark = "content/gfx/animations/interactions/puzzled.png"
    image exclamation_mark = "content/gfx/animations/interactions/exclamation.png"
    image music_note = "content/gfx/animations/interactions/note.png"
    image shy_blush = "content/gfx/animations/interactions/blush.png"
    image hearts_rise = FilmStrip('content/gfx/animations/interactions/hearts.png', (168, 157), (10, 3), 0.07, loop=True)
    
    image hearts_flow:
        subpixel True
        anchor (.5, 1.0)
        alpha .8
        additive .9
        "content/gfx/animations/interactions/hearts/heart1.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart2.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart3.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart4.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart5.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart6.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart7.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart8.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart9.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart10.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart11.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart12.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart13.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart14.png"
        pause 0.07
        "content/gfx/animations/interactions/hearts/heart15.png"
        pause 0.07
        repeat
    
    transform interactions_angry_pulse_tr:
        "angry_pulse"
        pos (150, 566)
        anchor (0.5, 0.5)
        block:
            linear 0.05 zoom 1.1
            linear 0.05 zoom 0.9
            pause 0.2
            linear 0.05 zoom 1.1
            linear 0.05 zoom 0.9
            pause 0.8
            repeat
            
    transform interactions_puzzled_tr:
        "question_mark"
        pos (130, 546)
        alpha 0.8
        anchor (.0, .0)
        block:
            linear 1 rotate 15 alpha 0.7 zoom 1.1
            linear 1 rotate -15 alpha 0.9 zoom 0.9
            repeat
            
    transform interactions_note_tr:
        "music_note"
        pos (125, 546)
        alpha 0.9
        anchor (.0, .0)
        block:
            linear 1 alpha 1.0 zoom 1.1
            linear 1 alpha 0.8 zoom 0.9
            repeat
            
    transform interactions_blush_tr:
        "shy_blush"
        pos (218, 640)
        anchor (.5, .5)
        yzoom 2.0
        block:
            linear 1.0 zoom 1.1
            linear 1.0 zoom 0.9
            repeat

    transform interactions_surprised_tr:
        "exclamation_mark"
        subpixel True
        pos (157, 650)
        alpha 0.8
        anchor (.5, 1.0)
        block:
            linear 0.4 yzoom 1.1 alpha 0.7
            pause 0.01
            linear 0.4 yzoom 0.9 alpha 0.9
            repeat
            
    transform interactions_sweat_drop_tr:
        pos (137, 575) alpha 0.0
        "sweat_drop"
        easein 1.0 ypos 610 alpha 1.0
        
    transform interactions_scared_lines_tr:
        "scared_lines"
        pos (160, 577)
        alpha 0.0
        linear 1.0 alpha 1.0
        
    transform interactions_zoom(t):
        subpixel True
        anchor (.5, .5)
        block:
            linear t zoom 1.1
            linear t zoom 1


        
    default interactions_portraits_overlay = DisplayableSwitcher(displayable={"angry": interactions_angry_pulse_tr,
                                                                                                                          "sweat": interactions_sweat_drop_tr,
                                                                                                                          "scared": interactions_scared_lines_tr,
                                                                                                                          "puzzled": interactions_puzzled_tr,
                                                                                                                          "note": interactions_note_tr,
                                                                                                                          "surprised": interactions_surprised_tr,
                                                                                                                          "shy": interactions_blush_tr, # probably should be used only as a replacement for missing shy portraits
                                                                                                                          "love": Transform("hearts_flow", pos=(220, 700)),
                                                                                                                          "like": Transform("hearts_rise", pos=(120, 405), anchor=(0.0, 0.0))
                                                                                                                          })