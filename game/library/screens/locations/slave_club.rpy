label slave_market_club: 
    
    python:
        # Build the actions
        if pytfall.world_actions.location("slave_market_club"):
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg slave_market_club
    show screen slavemarket_club
    with fade
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    while 1:
        $ result = ui.interact()
        
        if result[0] == 'control':
            if result[1] == 'return': 
                $ global_flags.set_flag("came_from_sc")
                hide screen slavemarket_club
                jump slave_market
                
                
screen slavemarket_club():
    
    use top_stripe(True)
    
    use location_actions("slave_market_club")
    
