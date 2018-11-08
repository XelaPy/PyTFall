screen pyp_school():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "-PyTFall Educators-" size 30

            vbox:
                ypos 100
                spacing 12
                vbox:
                    label "School"
                    text ("The school allows training of characters. They attend courses, "+
                          "and each session can increase stats and skills, as well as to "+
                          "gain experience. The school does not limit the number of students"+
                          " that can attend as long as you can afford the classes.")
                vbox:
                    label "Courses"
                    text ("Courses teach stats and skills. Each class focuses on a"+
                          " number of primary and secondary stats and has a duration"+
                          " in days.  They also have a tier and effectiveness, it pays"+
                          " off to pick a course with the same or higher tier than the"+
                          " student. A student can complete the course in a number of "+
                          "days that is usually lower than the duration. Upon completion,"+
                          " the student is awarded significant bonuses, and the course"+
                          " becomes less effective for the student after it was completed.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            # Images and maybe details:
            frame:
                xalign .5
                add pscale("content/gfx/interface/pyp/school.webp", 360, 1000)

        hbox:
            align 1.0, 1.0
            spacing 4
            frame:
                add pscale("content/gfx/interface/pyp/courses.webp", 262, 1000)
            frame:
                add pscale("content/gfx/interface/pyp/courses_1.webp", 264, 1000)

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
