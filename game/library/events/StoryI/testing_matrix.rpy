label test_matrix:
    stop music
    stop world
    scene bg story prison
    show scroll at truecenter with dissolve
    show blueprint at truecenter with dissolve
    call screen poly_matrix("library/events/StoryI/coordinates_1.json", show_exit_button=(1.0, 1.0))
    "Result: [_return]"
    
    menu:
        "Try Again":
            jump test_matrix
        "Start Game":
            return
            
label test_vortex:
    scene black
    show expression Vortex(Solid("F00", xysize=(20, 20))) as vortex
    pause
    hide vortex
    $ temp = Transform("content/items/quest/paper.png", zoom=0.3)
    show expression Vortex(temp, amount=150, radius=400, adjust_radius=(-20, 20), time=(0.5, 2.5), circles=(0.5, 5)) as vortex
    pause
    hide vortex
    $ temp = Transform("content/items/quest/paper.png", zoom=0.3)
    show expression Vortex(temp, amount=150, radius=400, adjust_radius=(-20, 20), time=(0.5, 2.5), reverse=True, circles=(0.5, 5)) as vortex
    pause
    hide vortex
    $ temp = Transform("content/items/quest/paper.png", zoom=0.2, rotate=45)
    show expression Vortex(temp, amount=50, radius=400, limit_radius=60, adjust_radius=(-20, 20), constant_radius=True,  time=(5, 7), circles=5) as vortex
    pause
    hide vortex
    return
