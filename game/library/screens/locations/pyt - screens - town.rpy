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
    
    for key in pytfall.maps("pytfall"):
        if "img" in key:
            $ rx = int(key["rx"]) if "rx" in key else 25
            $ ry = int(key["ry"]) if "ry" in key else 25
            $ img = ProportionalScale(key["img"], rx, ry)
            imagebutton:
                pos (key["x"], key["y"])
                idle img
                hover im.MatrixColor(img, im.matrix.brightness(0.25))
                focus_mask True
                hovered tt.action(key['name'])
                action Return(['location', key["id"]])
        else: # Map-cut-style:
            imagebutton:
                idle "".join([pytfall.map_pattern, key["id"], ".png"])
                hover "".join([pytfall.map_pattern, key["id"], "_hover.png"])
                focus_mask True
                hovered tt.action(key['name'])
                action Return(['location', key["id"]])
                    
    if tt.value:
        frame:
            align (0.6, 0.07)
            background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.5), 3, 3)
            text (u"{=content_text}{size=+7}{color=[ivory]}[tt.value]") xalign 0.5
            
    use pyt_top_stripe(True, use_hide_transform=True, normal_op=False)
            
