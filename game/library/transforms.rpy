init -997: # Transforms:
    # Basic transforms:
    
    # First, More default positions:
    transform mid_right:
        align (0.75, 1.0)
        
    transform mid_left:
        align (0.25, 1.0)
    
    # Other Transforms:
        
    transform move_to_pos_with_offset(pos, t):
        linear t offset pos
    
    transform move_from_to_pos_with_ease(start_pos=(0, 0), end_pos=(config.screen_width, config.screen_height), t=1.0, wait=0):
        # Moves the child from start position to end position in t seconds
        subpixel True
        pos start_pos
        pause wait
        ease t pos end_pos
        
    transform move_from_to_pos_with_easeout(start_pos=(0, 0), end_pos=(config.screen_width, config.screen_height), t):
        # Move by pos with easeOut:
        subpixel True
        pos start_pos
        easeout t pos end_pos
        
    transform move_from_to_align_with_linear(start_align=(0, 0), end_align=(1.0, 1.0), t=1.0):
        # Move_by_align_with_linear
        subpixel True
        align start_align
        linear t align end_align
        
    transform move_from_to_align_with_easein(start_align=(0, 0), end_align=(1.0, 1.0), t=1.0):
        # Move_by_align_with_linear
        subpixel True
        align start_align
        easein t align end_align
        
    transform move_from_to_offset_with_ease(start_offset=(-640, -400), end_offset=(0, 0), t=1.0):
        # move_from_to_offset_with_ease
        subpixel True
        offset start_offset
        ease t offset end_offset
        
    transform slide(so1=(-1000, 0), eo1=(0, 0), t1=1.0,
                             so2=(0, 0), eo2=(-1000, 0), t2=1.0):
        # Slides in on show
        # Slide out in show
        on show:
            move_from_to_offset_with_ease(so1, eo1, t1)
        on hide:
            move_from_to_offset_with_ease(so2, eo2, t2)
            
    transform auto_slide(init_pos=(0, -40), show_pos=(0, 0), t1=0.25, hide_pos=(0, -40), t2=0.25):
        # Auto-Slide, default values are for the top_stripe
        # This is used instead of a normal slide as it doesn't reset in the middle of a motion when switching between show/hide
        pos init_pos
        on show:
            linear t1 pos show_pos
        on hide:
            linear t2 pos hide_pos
            
    transform fade_from_to(start_val=1.0, end_val=0.0, t=1.0, wait=0):
        # Setup as a fade out, reverse the values for the fade in
        # simple_fade (fade is reserved...)
        subpixel True
        alpha start_val
        pause wait
        linear t alpha end_val
        
    transform fade_from_to_with_easeout(start_val=1.0, end_val=0.0, t=1.0, wait=0):
        # Setup as a fade out, reverse the values for the fade in
        # simple_fade (fade is reserved...)
        subpixel True
        alpha start_val
        pause wait
        easeout t alpha end_val
        
    transform fade_in_out(sv1=0.0, ev1=1.0, t1=1.0,
                                        sv2=1.0, ev2=0.0, t2=1.0):
        on show:
            fade_from_to(sv1, ev1, t1)
        on hide:
            fade_from_to(sv2, ev2, t2)
        
    transform rotate_by(degrees):
        # When used with x/ycenter in SL, this will (or at leastshould) be positioned correctly!
        rotate degrees
        rotate_pad True
        transform_anchor True
        subpixel True
        
    transform repeated_rotate(start_val=0, end_val=360, t=1.0):
        rotate start_val
        linear t rotate end_val
        rotate_pad True
        transform_anchor True
        subpixel True
        repeat
        
    transform simple_zoom_from_to_with_linear(start_val=1.0, end_val=0.0, t=1.0):
        # Simple zoom...
        subpixel True
        anchor (0.5, 0.5)
        zoom start_val
        linear t zoom end_val
        
    transform simple_zoom_from_to_with_easein(start_val=1.0, end_val=0.0, t=1.0):
        # Simple zoom...
        subpixel True
        anchor (0.5, 0.5)
        zoom start_val
        easein t zoom end_val
        
    # Complex transforms(*):
    transform pers_effect():
        subpixel True
        parallel:
            fade_from_to(0.98, 1.05, 1.0)
            fade_from_to(1.05, 0.98, 2.2)
        parallel:
            simple_zoom_from_to_with_linear(0.98, 1.05, 1.0)
            simple_zoom_from_to_with_linear(1.05, 0.98, 2.2)
        repeat    
    
    transform arena_stats_slide:
        parallel:
            move_from_to_offset_with_ease(start_offset=(0, 0), end_offset=(0, -200), t=8.0)
        parallel:
            4.0
            fade_from_to(t=4)
    
    transform elements:
        subpixel True
        parallel:
            block:
                parallel:
                    fade_from_to(0.3, 1.0, 5.0)
                parallel:
                    simple_zoom_from_to_with_linear(1.2, 0.8, 5.0)
            block:
                parallel:
                    fade_from_to(1.0, 0.3, 5.0)
                parallel:    
                    simple_zoom_from_to_with_linear(0.8, 1.2, 5.0)
            repeat
        parallel:
            repeated_rotate(t=30.0)
            
    transform arena_textslide:
        # Slider for arena Vicroty/Defeat texts
        on show:
            parallel:
                fade_from_to(0.3, 1.0, 0.5)
            parallel:
                xoffset 500
                ease 0.5 xoffset -400
                ease 0.5 xoffset -100
            linear 3.0 zoom 1.3 
        on hide:
            fade_from_to(t=0.5)
    
    # Interactions:
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
        pos (145, 575) alpha 0.0
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
            
    # Also used for gm:    
    transform found_cash(x, y, t):
        subpixel True
        parallel:
            alpha 0.5 zoom 0.5
            linear t alpha 1.0 zoom 1.6
        parallel:
            pos(x, y)
            linear t pos(x, (y-200))
          
            
    # BE Transforms:
    transform damage_color(img): # Note: Testing case, this should become a DD/UDD with moar options at some point.
        im.MatrixColor(img, im.matrix.saturation(1))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.1))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.2))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.3))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.4))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.5))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.6))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.7))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.8))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.7))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.6))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.5))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.4))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.3))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.2))
        0.05
        im.MatrixColor(img, im.matrix.saturation(1.1))
        0.05
        repeat
    
    transform damage_shake(t, random_range, delay=0):
        subpixel True
        offset (0, 0)
        pause delay
        choice:
            linear t offset(renpy.random.randint(*random_range), renpy.random.randint(*random_range))
        choice:
            linear t offset(renpy.random.randint(*random_range), renpy.random.randint(*random_range))
        choice:
            linear t offset(renpy.random.randint(*random_range), renpy.random.randint(*random_range))
        choice:
            linear t offset(renpy.random.randint(*random_range), renpy.random.randint(*random_range))
        choice:
            linear t offset(renpy.random.randint(*random_range), renpy.random.randint(*random_range))
        repeat
        
    transform battle_bounce(pos):
        alpha 1
        pos pos # Initial position.
        xanchor 0.5
        easein_circ 0.3 yoffset -100
        easeout_circ 0.3 yoffset 0
        easein_circ 0.3 yoffset -70
        easeout_circ 0.3 yoffset 0
        linear 0.3 alpha 0
        
    transform be_stats_slideout():
        on hover:
            linear 0.3 xoffset 100
        on idle:
            linear 0.3 xoffset 300
        
    transform be_dodge(xoffset):
        easein 0.5 xoffset xoffset
        linear 0.5 xoffset 0
            
    # GUI ===>>>    
    transform circle_around(t=10, around=(config.screen_width/2, config.screen_height/2), angle=0, radius=200):
        subpixel True
        anchor (0.5, 0.5)
        around around
        angle angle
        radius radius
        linear t clockwise circles 1
        repeat

    transform mm_clouds(start, end, t):
        subpixel True
        additive 1.0
        xpos start
        linear t xpos end
        repeat
    
    transform mm_fire(yps, ype, ast, ae, t):
        additive 0.9
        ypos yps
        alpha ast
        linear t ypos ype alpha ae
        repeat
        
    transform flashing:
        additive 1.0 alpha 0.4
        block:
            linear 1.0 alpha 0.1
            linear 1.0 alpha 0.4
            repeat
    
    transform fog:
        linear 1.0 alpha 0.2
        linear 1.0 alpha 0.3
        linear 1.0 alpha 0.4
        linear 1.0 alpha 0.5
        linear 1.0 alpha 0.4
        linear 1.0 alpha 0.3
        repeat
        
    # UDD ===>>>    
    transform vortex_particle(displayable, t=10, around=(config.screen_width/2, config.screen_height/2), angle=0, start_radius=200, end_radius=0, circles=3):
        displayable
        subpixel True
        around around
        angle angle
        radius start_radius
        easeout t radius end_radius clockwise circles circles
        Null()
        
    transform vortex_particle_2(displayable, t=10, around=(config.screen_width/2, config.screen_height/2), angle=0, start_radius=200, circles=3):
        # This one keeps the radius constant
        displayable
        subpixel True
        around around
        angle angle
        radius start_radius
        linear t clockwise circles 1
        Null()
        repeat circles
        
    # This bit is required for the Snowing effect:
    transform snowlike_particle(d, delay, startpos, endpos, speed):
        d
        pause delay
        subpixel True
        pos startpos
        linear speed pos endpos
        
    transform particle(d, delay, speed=1.0, around=(config.screen_width/2, config.screen_height/2), angle=0, radius=200):
        d
        pause delay
        subpixel True
        around around
        radius 0
        linear speed radius radius angle angle
        
    transform fly_away():
        easeout_bounce 1.5 yoffset -1000
        pause 2.0
        easeout_bounce 1.0 yoffset 0
        parallel:
            easeout_bounce 0.1 yzoom 0.95
            easeout_bounce 0.1 yzoom 1.0
        parallel:
            easeout_bounce 0.1 yoffset 10
            easeout_bounce 0.1 yoffset 0
        
    transform shake(dt=.4, dist=128):
        function renpy.curry(_shake_function)(dt=dt,dist=dist)
