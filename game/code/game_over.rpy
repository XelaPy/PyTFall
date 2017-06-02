label game_over:
    stop music
    stop world
    show screen game_over
    with dissolve
    play sound "content/sfx/sound/world/game_over.mp3"
    $ renpy.pause(1)
    return

screen game_over:
    zorder 100**9
    modal True

    add "bg game_over"
    timer 6.0 action MainMenu(confirm=False)
