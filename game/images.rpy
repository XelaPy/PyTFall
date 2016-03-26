# ANIMATION
init:
    image bg_main = "content/gfx/bg/main.jpg"
    
    image eyes:
        zoom 0.7
        additive 1.0
        alpha 0.7
        "content/gfx/animations/main_menu/eyes/eyes1.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes2.png"
        pause 2
        "content/gfx/animations/main_menu/eyes/eyes3.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes4.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes5.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes6.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes7.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes8.png"
        pause 2
        "content/gfx/animations/main_menu/eyes/eyes9.png"
        pause 2
        "content/gfx/animations/main_menu/eyes/eyes10.png"
        pause 2
        "content/gfx/animations/main_menu/eyes/eyes11.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes12.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes13.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes14.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes15.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes16.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes17.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes18.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes19.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes20.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes21.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes22.png"
        pause 2
        "content/gfx/animations/main_menu/eyes/eyes23.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes24.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes25.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes26.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes27.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes28.png"
        pause 0.2
        "content/gfx/animations/main_menu/eyes/eyes29.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes30.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes31.png"
        pause 0.5
        "content/gfx/animations/main_menu/eyes/eyes32.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes33.png"
        pause 0.5
        "content/gfx/animations/main_menu/eyes/eyes34.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes35.png"
        pause 0.5
        "content/gfx/animations/main_menu/eyes/eyes36.png"
        pause 0.5
        "content/gfx/animations/main_menu/eyes/eyes37.png"
        pause 0.5
        "content/gfx/animations/main_menu/eyes/eyes38.png"
        pause 1
        "content/gfx/animations/main_menu/eyes/eyes39.png"
        pause 0.4
        "content/gfx/animations/main_menu/eyes/eyes40.png"
        pause 0.4
        repeat
    
    image logo:
        subpixel True
        additive 0.1
        alpha 0.95
        "content/gfx/animations/main_menu/logo/logo1.png"
        pause 0.3
        "content/gfx/animations/main_menu/logo/logo2.png"
        pause 0.3
        "content/gfx/animations/main_menu/logo/logo3.png"
        pause 0.4
        "content/gfx/animations/main_menu/logo/logo2.png"
        pause 0.3
        "content/gfx/animations/main_menu/logo/logo1.png"
        pause 0.3
        "content/gfx/animations/main_menu/logo/logo5.png"
        pause 0.3
        "content/gfx/animations/main_menu/logo/logo6.png"
        pause 0.4
        "content/gfx/animations/main_menu/logo/logo5.png"
        pause 0.3
        repeat
    
    image fog:
        "content/gfx/animations/main_menu/fog1.png"
        pos (15, 20)
    
    image mm_fire = "content/gfx/animations/main_menu/fire1.png"
       # additive 1.0
       # pause 0.6
       # "content/gfx/animations/main_menu/fire2.png"
       # additive 1.0
       # pause 0.6
       # "content/gfx/animations/main_menu/fire3.png"
       # additive 1.0
       # pause 0.6
       # repeat
    
    image mm_clouds = "content/gfx/animations/main_menu/cloud1.png"
    image mm_cloudstest = im.Scale("content/gfx/animations/main_menu/cloud1.png", 287, 263)
    
    image arena_victory = "content/gfx/images/victory.png"
    image arena_defeat = "content/gfx/images/defeat.png"
    
    image save:
        zoom 0.4
        additive 1.0
        alpha 0.7
        "content/gfx/animations/main_menu/settings/save1.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save2.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save3.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save4.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save5.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save6.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save7.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save8.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save9.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save10.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save11.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/save12.png"
        pause 0.2
        repeat
    
    image slo:
        zoom 0.9
        additive 1.0
        #alpha 0.7
        "content/gfx/animations/main_menu/settings/slo1.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo2.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo3.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo4.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo5.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo6.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo7.png"
        pause 0.2
        "content/gfx/animations/main_menu/settings/slo8.png"
        pause 0.2
        repeat
        
    # Interactions module:
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
