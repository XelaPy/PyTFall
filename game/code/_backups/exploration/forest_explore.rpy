label forest_exploration:
    show screen forest_exploration
    with dissolve
    
    $ pytfall.forest_1.screen_loop()
    
    hide screen forest_exploration
    jump mainscreen


screen forest_exploration:
    
    add(pytfall.forest_1.map[pytfall.forest_1.player_tile[0]][pytfall.forest_1.player_tile[1]].bg)
    
    use r_lightbutton(img=im.Scale("content/gfx/interface/buttons/shape69.png", 40, 40), return_value=['control', 'return'], align=(0.99, 0))
    
    # Team stats ---------------------------------------------->
    frame:
        align (0,0)
        background (Solid((255,255,255,100)))
        maximum(700, 125)
        minimum(700, 125)

        
        hbox:
            spacing 20
            for member in hero.team:
                hbox:
                    spacing 10
                    xmaximum 250
                    add(member.show("portrait", cache=True, resize=(100, 100))) yalign 0.5
                    vbox:
                        spacing 2
                        vbox:
                            text("{size=-8}HP:")
                            bar:
                                value member.health
                                range member.get_max("health")
                                left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 110, 20), red, red)
                                right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 110, 20), red, red)
                                thumb None
                                xmaximum 110
                                ymaximum 20
                        vbox:
                            text("{size=-8}MP:")
                            bar:
                                value member.mp
                                range member.get_max("mp")
                                left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 110, 20), green, green)
                                right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 110, 20), green, green)
                                thumb None
                                xmaximum 110
                                ymaximum 20
                        vbox:
                            text("{size=-8}Vitality:")
                            bar:
                                value member.vitality
                                range member.get_max("vitality")
                                left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 110, 20), blue, blue)
                                right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 110, 20), blue, blue)
                                thumb None
                                xmaximum 110
                                ymaximum 20
                
    # Tile Map ---------------------------------------------->
    frame:
        align (0.999, 0.999)
        maximum(200, 200)
        minimum(200, 200)
        xfill True
        yfill True
        hbox:
            align (0.5, 0.5)
            box_wrap True
            maximum(162, 82)
            minimum(162, 82)
            for y in range(pytfall.forest_1.map_dimensions[1]):
                    for x in range(pytfall.forest_1.map_dimensions[0]):
                        frame:
                            minimum (8, 8)
                            maximum (8, 8)
                            xfill True
                            yfill True
                            background pytfall.forest_1.map[x][y].color


    text("Player Coords: %d, %d"% (pytfall.forest_1.player_tile[0], pytfall.forest_1.player_tile[1])) align (0.75, 0.95)
    
    
    # Directional Buttons ---------------------------------------------->
    vbox:
        align (0.5, 0.9)
        spacing 10
        hbox:
            xalign 0.5
            use r_lightbutton(img=im.Scale("content/gfx/interface/buttons/blue_arrow_up.png", 60, 60),return_value =['move','up'])
        hbox:
            xalign 0.5
            spacing 5
            use r_lightbutton(img=im.Scale("content/gfx/interface/buttons/blue_arrow_left.png", 60, 60),return_value =['move','left'])
            use r_lightbutton(img=im.Scale(im.Flip("content/gfx/interface/buttons/blue_arrow_up.png", vertical=True), 60, 60),return_value =['move','down'])
            use r_lightbutton(img=im.Scale("content/gfx/interface/buttons/blue_arrow_right.png", 60, 60),return_value =['move','right'])
            
            
    # Action Buttons ---------------------------------------------->
    vbox:
        align (0.01, 0.5)
        spacing 10
        if pytfall.forest_1.show_encounter_button():
            textbutton "Battle":
                action Return(['fight', 'simple_battle'])
