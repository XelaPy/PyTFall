label school_training:
    $ school = schools.values().pop()
    show screen school_training

    # Make sure we set char to the_chosen (means we came from listing in Pico's code)
    # if we came from char listings and just have the one char,
    # normal functionality of the screen can be permitted:
    if the_chosen:
        $ char = the_chosen
    if not isinstance(char, PytCharacter) and len(char) == 1:
        $ char = char.pop()

    while 1:
        $ result = ui.interact()

        if result[0] == "set_course":
            $ course = result[1]
            $ course_type = course.data.get("type", None)

            if isinstance(char, PytCharacter):
                $ students = [char]
            else:
                $ students = list(char)

            python:
                for s in students:
                    if s.workplace == school:
                        s.action.remove_student(s)

                    # Blocks bad matches between student and course:
                    # Slaves can't do combat:
                    if course_type == "combat" and s.status == "slave":
                        renpy.notify("Slaves cannot take combat courses")
                        continue

                    # Free girls without naughty basetraits won't do xxx
                    c0 = course_type == "xxx"
                    c1 = s.status == "free"
                    c2 = "SIW" not in s.gen_occs
                    if all([c0, c1, c2]):
                        renpy.notify("Free non whores won't take XXX courses")
                        continue

                    s.workplace = school
                    course.add_student(s)

        if result == ["control", "return"]:
            jump return_from_school_training

label return_from_school_training:
    hide screen school_training

    if the_chosen == None:
        jump char_profile
    else:
        jump chars_list

init python:
    def school_desc_string():
        temp = []
        temp.append("The Beautiful educational facilities in PyTFall offer")
        temp.append("training for free citizens,")
        temp.append("foreigners and slaves alike. Centuries old traditions will make certain")
        temp.append("that no student taking classes here will ever be sad or unhappy.")
        temp.append("Nothing in this world is free and courses here")
        temp.append("will cost you a dime and if you wish to be trained")
        temp.append("by the Masters, a small fortune.")
        rv = " ".join(temp)

        return rv

screen school_training():
    # School info:
    frame:
        style_prefix "content"
        background Frame("content/gfx/frame/mes12.jpg", 10, 10)
        pos 8, 48
        padding 10, 10
        xysize (500, 666)
        has vbox
        null height 3
        label ("[school.name]") xalign .5 text_color ivory text_size 25
        null height 3
        frame:
            xalign .5
            background Null()
            foreground Frame("content/gfx/frame/MC_bg2.png", 10, 10)
            add ProportionalScale(school.img, 450, 300)
        null height 8
        default desc = school_desc_string()
        text "[desc]" color ivory
        null height 5
        text "Girls currently taking courses here:" color ivory
        null height 3
        viewport:
            xsize 480
            draggable False
            mousewheel True
            scrollbars "vertical"
            $ sch = schools["-PyTFall Educators-"]
            vbox:
                spacing 10
                for c in sch.courses:
                    if c.students:
                        vbox:
                            xsize 450
                            text ("[c.name] Course:") color goldenrod xalign .0
                            for s in c.students:
                                hbox:
                                    xalign .05
                                    xsize 450
                                    text ("[s.fullname]") color lawngreen
                                    if s in c.completed:
                                        text "(Completed)" color goldenrod
                                    else:
                                        $ days_left = c.days_to_complete - c.students_progress.get(s, 0)
                                        $ can_complete = c.days_remaining >= days_left
                                        if can_complete:
                                            text "([days_left] days to complete)" color ivory xalign 1.0
                                        else:
                                            text "(can't complete)" color ivory xalign 1.0

    frame:
        style_prefix "content"
        background Frame("content/gfx/frame/mes11.webp", 10, 10)
        xpos 1280-8 xanchor 1.0 ypos 48
        padding 10, 10
        xysize (760, 666)
        has viewport draggable 1 mousewheel 1 scrollbars "vertical"
        hbox:
            xsize 720 box_wrap 1
            for course in school.courses:
                button:
                    style "mmenu1_button"
                    margin 2, 2
                    padding 5, 5
                    xysize 180, 350
                    action Return(["set_course", course])
                    tooltip course.tooltip
                    vbox:
                        xalign .5
                        spacing 2
                        text course.name + " Course" xalign .5 color ivory style "dropdown_gm2_button_value_text"
                        frame:
                            xalign .5
                            background Null()
                            foreground Frame("content/gfx/frame/MC_bg2.png", 10, 10)
                            add ProportionalScale(course.img, 150, 150)
                    text "---------------------------------":
                        xalign .5
                        color ivory
                        ypos 190
                    vbox:
                        ypos 205
                        xalign .5
                        style_prefix "proper_stats"
                        frame:
                            xysize (160, 20)
                            xalign .5
                            text "Days Left":
                                xalign .02
                                color "#79CDCD"
                                hover_color ivory
                                size 15
                            text "[course.days_remaining]/[course.duration]":
                                style_suffix "value_text"
                                hover_color green
                                size 14
                                xalign .99 yoffset -1
                        frame:
                            xysize (160, 20)
                            xalign .5
                            text "Days to Complete":
                                xalign .02
                                color "#79CDCD"
                                hover_color ivory
                                size 15
                            if isinstance(char, PytCharacter):
                                $ days_left = course.days_to_complete - course.students_progress.get(char, 0)
                                text "[days_left]/[course.days_to_complete]":
                                    style_suffix "value_text"
                                    if days_left <= course.days_remaining:
                                        hover_color green
                                    else:
                                        hover_color red
                                    size 14
                                    xalign .99 yoffset -1
                            else:
                                text "--/[course.days_to_complete]":
                                    style_suffix "value_text"
                                    size 14
                                    xalign .99 yoffset -1

                        frame:
                            xysize (160, 20)
                            xalign .5
                            text "Tier":
                                xalign .02
                                color "#79CDCD"
                                hover_color ivory
                                size 15
                            text "[course.difficulty]":
                                style_suffix "value_text"
                                if isinstance(char, PytCharacter):
                                    if char.tier <= course.difficulty:
                                        hover_color green
                                    else:
                                        hover_color red
                                size 14
                                xalign .99 yoffset -1
                        frame:
                            xysize (160, 20)
                            xalign .5
                            text "Effectiveness":
                                xalign .02
                                color "#79CDCD"
                                hover_color ivory
                                size 15
                            text "[course.effectiveness]":
                                style_suffix "value_text"
                                hover_color green
                                size 14
                                xalign .99 yoffset -1
                        frame:
                            xysize (160, 20)
                            xalign .5
                            text "Price":
                                xalign .02
                                color "#79CDCD"
                                hover_color ivory
                                size 15
                            text "[course.price]":
                                style_suffix "value_text"
                                hover_color green
                                size 14
                                xalign .99 yoffset -1
                        frame:
                            xysize (160, 20)
                            xalign .5
                            text "Status":
                                xalign .02
                                color "#79CDCD"
                                hover_color ivory
                                size 15
                            if isinstance(char, PytCharacter):
                                $ status = course.get_status(char)
                                text "[status]":
                                    style_suffix "value_text"
                                    hover_color green size 14
                                    xalign .99 yoffset -1
                            else:
                                text "N/A":
                                    style_suffix "value_text"
                                    hover_color green size 14
                                    xalign .99 yoffset -1

                    if char in course.completed:
                        add pscale("content/gfx/interface/images/completed_stamp.webp", 130, 130):
                            xalign .5 ypos 210



    use top_stripe(True, show_lead_away_buttons=False)
