init -1: # Transforms:
    # Basic transforms:
    
    # First, More default positions:
    transform mid_right:
        align (0.75, 1.0)
        
    transform mid_left:
        align (0.25, 1.0)
    
    # Other Transforms:
        
    transform just_move_with_offset(pos, t):
        linear t offset pos
    
    transform move_bpwe(start_pos=(0, 0), end_pos=(config.screen_width, config.screen_height), t=1.0):
        # move_by_pos_with_ease
        # Moves the child from start position to end position in t sexconds
        subpixel True
        pos start_pos
        ease t pos end_pos
        
    transform move_bawl(start_align=(0, 0), end_align=(1.0, 1.0), t=1.0):
        # Move_by_align_with_linear
        subpixel True
        align start_align
        linear t align end_align
        
    transform move_bowe(start_offset=(-640, -400), end_offset=(0, 0), t=1.0):
        # move_by_offset_with_ease
        subpixel True
        offset start_offset
        ease t offset end_offset
        
    transform slide(so1=(-1000, 0), eo1=(0, 0), t1=1.0,
                             so2=(0, 0), eo2=(-1000, 0), t2=1.0):
        # Slides in on show
        # Slide out in show
        on show:
            move_bowe(so1, eo1, t1)
        on hide:
            move_bowe(so2, eo2, t2)
            
    transform auto_slide(init_pos=(0, -40), show_pos=(0, 0), t1=0.25, hide_pos=(0, -40), t2=0.25):
        # Auto-Slide, default values are for the top_stripe
        # This is used instead of a normal slide as it doesn't reset in the middle of a motion when switching between show/hide
        pos init_pos
        on show:
            linear t1 pos show_pos
        on hide:
            linear t2 pos hide_pos
            
    transform sfade(start_val=1.0, end_val=0.0, t=1.0):
        # Setup as a fade out, reverse the values for the fade in
        # simple_fade (fade is reserved...)
        subpixel True
        alpha start_val
        linear t alpha end_val
        
    transform fade_in_out(sv1=0.0, ev1=1.0, t1=1.0,
                                        sv2=1.0, ev2=0.0, t2=1.0):
        on show:
            sfade(sv1, ev1, t1)
        on hide:
            sfade(sv2, ev2, t2)
        
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
        
    transform szoom(start_val=1.0, end_val=0.0, t=1.0):
        # Simple zoom...
        anchor (0.5, 0.5)
        zoom start_val
        linear t zoom end_val
       
    # Complex transforms(*):
    transform pers_effect():
        subpixel True
        parallel:
            sfade(0.9, 1.1, 2.0)
            sfade(1.1, 0.9, 2.0)
        parallel:
            szoom(0.9, 1.1, 2.0)
            szoom(1.1, 0.9, 2.0)
        repeat    
    
    transform arena_stats_slide:
        parallel:
            move_bowe(start_offset=(0, 0), end_offset=(0, -200), t=8.0)
        parallel:
            4.0
            sfade(t=4)
    
    transform elements:
        subpixel True
        parallel:
            block:
                parallel:
                    sfade(0.3, 1.0, 5.0)
                parallel:
                    szoom(1.2, 0.8, 5.0)
            block:        
                parallel:
                    sfade(1.0, 0.3, 5.0)
                parallel:    
                    szoom(0.8, 1.2, 5.0)
            repeat
        parallel:
            repeated_rotate(t=30.0)
            
    transform arena_textslide:
        # Slider for arena Vicroty/Defeat texts
        on show:
            parallel:
                sfade(0.3, 1.0, 0.5)
            parallel:
                xoffset 500
                ease 0.5 xoffset -400
                ease 0.5 xoffset -100
            linear 3.0 zoom 1.3 
        on hide:
            sfade(t=0.5)
    
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
    transform damage_shake(t, random_range):
        subpixel True
        offset (0, 0)
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
        easein 0.3 yoffset -60
        easeout 0.3 yoffset 0
        easein 0.3 yoffset -35
        easeout 0.3 yoffset 0
        linear 0.5 alpha 0
        
    transform be_stats_slideout():
        on hover:
            linear 0.3 xoffset 100
        on idle:
            linear 0.3 xoffset 300
        
    transform move_bpweo(start_pos=(0, 0), end_pos=(config.screen_width, config.screen_height), t):
        # Move by pos with easeOut:
        subpixel True
        pos start_pos
        easeout t pos end_pos
        
    transform circle_around(t=10, around=(config.screen_width/2, config.screen_height/2), angle=0, radius=200):
        subpixel True
        anchor (0.5, 0.5)
        around around
        angle angle
        radius radius
        linear t clockwise circles 1
        repeat

    transform mm_clouds(start, end, t):
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
