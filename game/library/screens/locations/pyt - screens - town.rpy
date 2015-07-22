label pyt_city:
    
    # Music related:
    if not "pytfall" in ilists.world_music:
        $ ilists.world_music["pytfall"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("pytfall")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["pytfall"])
    $ global_flags.del_flag("keep_playing_music")
    
    # TS Dropdown var:
    $ pytfall.city_dropdown = False
    
    scene bg humans
    show screen pyt_city_screen
    with dissolve
    
    python:
        while 1:
            result = ui.interact()
            if result[0] == 'control':
                if result[1] == 'return':
                    break
            elif result[0] == 'location':
                renpy.hide_screen("pyt_city_screen")
                jump(result[1])
                
    $ global_flags.set_flag("keep_playing_music")            
    hide screen pyt_city_screen
    jump mainscreen


screen pyt_city_screen():
    
    default tt = Tooltip(None)
    
    for key in pytfall.maps['PyTFall']:
            python:
                map_point = pytfall.maps['PyTFall'][key]['attr']
                x = int(map_point['x']) / float(config.screen_width)
                y = int(map_point['y']) / float(config.screen_height)
                if "rx" in map_point:
                    rx = int(map_point["rx"])
                    ry = int(map_point["rx"])
                else:
                    rx = 25
                    ry = 25
                    
            if map_point['image']:
                $ img=ProportionalScale(map_point['image'], rx, ry)
                imagebutton:
                    align(x, y)
                    idle img
                    hover im.MatrixColor(img, im.matrix.brightness(0.25))
                    focus_mask True
                    hovered tt.action(map_point['name'])
                    action Return(['location', key])
            else: # Map-cut-style:
                imagebutton:
                    idle "".join([persistent.town_path, key, ".png"])
                    hover "".join([persistent.town_path, key, "_hover.png"])
                    focus_mask True
                    hovered tt.action(map_point['name'])
                    action Return(['location', key])
                    
    if tt.value:
        frame:
            align (0.6, 0.07)
            background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 3, 3)
            text (u"{=content_text}{size=+7}{color=[ivory]}[tt.value]") xalign 0.5
            
    use pyt_top_stripe(True, use_hide_transform=True, normal_op=False)
            
