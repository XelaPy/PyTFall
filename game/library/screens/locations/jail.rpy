label city_jail:
    
    # Music related:
    if not "cityjail" in ilists.world_music:
        $ ilists.world_music["cityjail"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("cityjail")]
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_jail"):
            pytfall.world_actions.menu("cells", "Cells")
            pytfall.world_actions.slave_market(pytfall.ra, "Claim an escaped slave by paying off their fine.",
                                               button="Browse Escapees", null_button="No Escapees",
                                               buy_button="Retrieve", buy_tt="Claim this girl by paying her fine of %s Gold.",
                                               index=("cells", "sm_ra"))
            pytfall.world_actions.slave_market(jail, "Acquire the services of a prisoner buy paying their bail.",
                                               button="Browse Prisoners", null_button="No Prisoners",
                                               buy_button="Bail", buy_tt="Acquire this girl by paying her bail of %s Gold.",
                                               index=("cells", "sm_cj"))
            pytfall.world_actions.slave_market(jail, "Acquire the services of a prisoner buy paying their bail.",
                                               button="Browse Prisoners", null_button="No Prisoners",
                                               buy_button="Bail", buy_tt="Acquire this girl by paying her bail of %s Gold.",
                                               index=("cells", "sm_cj"))
            
            pytfall.world_actions.add(("cells", "browse"), "Browse Cells", "browse_jail_cells", label="_no_jail_event")
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_jail
    with dissolve
    
    if not global_flags.flag('visited_city_jail'):
        $ global_flags.set_flag('visited_city_jail')
        "The city jail..."
        "Temporary home of miscreants and law breakers."
        "Not to mention the occasional escaped slave."
    
    show screen city_jail
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    while True:
        $ result = ui.interact()
        if result[0] == "control":
            if result[1] == "return":
                hide screen city_jail
                jump city
        
        hide _tag
        
        
label _no_jail_event:
    $ hero.say(choice(["Nothing to see.",
                       "No ones here.",
                       "Nothing."]))
    return
    

screen city_jail:
    
    use top_stripe(True)
    
    use location_actions("city_jail")
    
