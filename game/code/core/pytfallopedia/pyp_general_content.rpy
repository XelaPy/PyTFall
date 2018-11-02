# DEFAULT positioning blueprint that can be used with any screen pyp info in the future.
screen pyp_default():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.png"
