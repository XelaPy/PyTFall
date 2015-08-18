label test_matrix:
    $ result = check_polymatrix("library/events/StoryI/coordinates.json")
    "Result: [result]"
    show bg story dark_room with dissolve
    screen ask_are_you_sure:
        fixed:
            textbutton "Yes" xalign 0.33 yalign 0.5 action Return(True)
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
    return
