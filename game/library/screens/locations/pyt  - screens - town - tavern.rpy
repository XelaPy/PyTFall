label tavern_town:
    $ gm.enter_location(goodtraits=["Adventurer", "Heavy Drinker"], badtraits=["Lolita", "Artificial Body", "Shy", "Elegant"])
    
    python:
        # Build the actions
        if pytfall.world_actions.location("tavern_town"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg tavern
    with dissolve
    show screen pyt_tavern_town
        
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    python:

        while True:

            result = ui.interact()

            if result[0] == 'jump':
                gm.start_gm(result[1])
            if result[0] == 'control':
                if result[1] == 'return':
                    break
            elif result[0] == 'location':
                renpy.music.stop(channel="world")
                jump(result[1])        
                    
    hide screen pyt_tavern_town
    jump pyt_city
    
                
screen pyt_tavern_town:

    use pyt_top_stripe(True)
    
    use location_actions("tavern_town")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in gm.display_girls():
           
                    use rg_lightbutton(img=entry.show("girlmeets",  exclude=["swimsuit", "wildness", "beach", "pool","onsen", "indoors"], type="first_default", label_cache=True, resize=(300, 400)), return_value=['jump', entry])

    for key in pytfall.maps['Tavern']:
        python:
            map_point = pytfall.maps['Tavern'][key]['attr']
            x = int(map_point['x']) / float(config.screen_width)
            y = int(map_point['y']) / float(config.screen_height)
        use r_lightbutton(img=im.Scale(map_point['image'], 60, 60), return_value=['location',key], align=(x,y))
        frame background Solid((0,0,0,128)) align (x,y+0.05):
            text (u"{size=-4}%s"%(map_point['name']))                