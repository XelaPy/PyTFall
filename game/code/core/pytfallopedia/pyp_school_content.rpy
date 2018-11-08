screen pyp_school():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "-PyTFall Educators-" size 30

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            # Images and maybe details:

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

# screen pyp_courses():
#     zorder 1001
#
#     fixed:
#         pos 302, 49
#         xysize config.screen_width-309, config.screen_height-56
#         style_prefix "proper_stats"
#
#         # Screen Content goes here!
#
#     # ForeGround frame (should be a part of every screen with Info):
#     add "content/gfx/frame/h3.webp"
#
# screen pyp_courses():
#     zorder 1001
#
#     fixed:
#         pos 302, 49
#         xysize config.screen_width-309, config.screen_height-56
#         style_prefix "proper_stats"
#
#         # Screen Content goes here!
#
#     # ForeGround frame (should be a part of every screen with Info):
#     add "content/gfx/frame/h3.webp"
