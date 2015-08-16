label test_matrix:
    $ result = check_polymatrix("library/events/StoryI/coordinates.json")
    "Result: [result]"
    show bg story dark_room with dissolve
    menu:
        "Try Again":
            jump test_matrix
        "Start Game":
            return
            
label test_vortex:
    show expression Vortex(Solid("F00", xysize=(20, 20))) as vortex
    pause
    hide vortex
    show expression Vortex(Solid("F00", xysize=(10, 10)), amount=150, radius=400, adjust_radius=(-20, 20), time=(0.5, 2.5), circles=(0.5, 5)) as vortex
    pause
    hide vortex
    return
