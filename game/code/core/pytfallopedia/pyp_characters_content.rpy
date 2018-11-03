screen pyp_characters():
    # main chars screen.
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        text "Characters Info" align .5, .5

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_stats():
    # main chars screen.
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        text "Stats Info" align .5, .5

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"

screen pyp_skills():
    # main chars screen.
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        text "Skills Info" align .5, .5

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"
