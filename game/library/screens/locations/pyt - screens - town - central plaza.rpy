label city_plaza:
    
    #python:
        # Build the actions
        #pytfall.world_actions.location("city_plaza")
        #pytfall.world_actions.finish()
    
    hide screen pyt_city_screen
    show screen pyt_city_plaza
    with irisout
    
    if global_flags.flag('visited_central_plaza'):
        "..."
    else:
        $global_flags.set_flag('visited_central_plaza')
        "Central Plaza! Amongst many useful things, you will find a questboard here. "
        "But we have nothing so far..."
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
        
    python:
        while True:
            result = ui.interact()
            if result[0] == 'control':
                if result[1] == 'return':
                    break
            elif result[0] == 'location':
                jump(result[1])
    hide screen pyt_city_plaza
    jump pyt_city
    
    
    
screen pyt_city_plaza:

    add(im.Scale("content/gfx/bg/locations/city_plaza.jpg", config.screen_width, config.screen_height))
    
    use pyt_top_stripe(True)
