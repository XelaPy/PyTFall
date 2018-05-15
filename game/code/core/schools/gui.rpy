label school_training:
    $ school = schools.values().pop()
    show screen school_training

    while 1:
        $ result = ui.interact()

        if result[0] == "set_course":
            pass

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
        temp.append("The Beautiful educational facilities in PyTFall offer any")
        temp.append("training one may require for free citizens,")
        temp.append("foreigners and slaves alike. Century old traditions will make sure")
        temp.append("that no girl taking classes here will ever be sad or unhappy.")
        temp.append("Nothing in this world is free however, so courses here")
        temp.append("might cost you a dime and if you wish to be trained")
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
            add ProportionalScale(school.img, 450, 300) xalign .5
        null height 8
        default desc = school_desc_string()
        text "[desc]" color ivory
        null height 3
        text "Girls currently taking courses here:" color ivory
        null height 3
        viewport:
            xsize 580
            draggable False
            mousewheel True
            scrollbars "vertical"
            vbox:
                xmaximum 610
                spacing 10
                for c in list(c for c in chain.from_iterable(course.students for course in school.courses)):
                    hbox:
                        fixed:
                            xsize 180
                            text (u"[c.fullname]:") color ivory
                        text (u"[c.action]") color ivory
                for i in range(100):
                    add Solid("F00", xysize=(400, 10))

    frame:
        style_prefix "content"
        background Frame("content/gfx/frame/mes11.jpg", 10, 10)
        xpos 1280-8 xanchor 1.0 ypos 48
        padding 10, 10
        xysize (750, 666)

    use top_stripe(True)
