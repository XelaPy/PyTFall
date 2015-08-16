label test_matrix:
    $ result = check_polymatrix("library/events/StoryI/coordinates.json")
    "Result: [result]"
    show bg story dark_room with dissolve
    menu:
        "Try Again":
            jump test_matrix
        "Start Game":
            return
