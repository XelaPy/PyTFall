label test_matrix:
    stop music
    stop world
    show bg hidden_village with dissolve
    call screen poly_matrix("library/events/StoryI/coordinates_hidden_village.json", show_exit_button=(0.9, 0.9))
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
    return
