screen pyp_quests_and_events():
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
                text "Quests and Events" size 30

            vbox:
                ypos 80
                label "Quests and Events"
                text ("The game has a system of quests and events. Not all of them are available"+
                      " from the beginning, some require a certain level, high enough day counter or are simply randomized.")
                null height 5
                text "Right now there is not much quests and events, but we hope to add much more in the future!"

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            # Images and maybe details:

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_quests():
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
                text "Quests" size 30

            vbox:
                ypos 80
                text ("Sometimes you can get a quest after discovering something"+
                     " or talking to a character. The game shows a notification"+
                     " each time you get, update or close one.")
                null height 5
                text "You can check all known quests in the quests journal."

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                ypos 80 xalign .5
                spacing 20
                frame:
                    add pscale("content/gfx/interface/pyp/quest_1.webp", 350, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/quest_2.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_events():
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
                text "Events" size 30

            vbox:
                ypos 80
                text ("Sometimes by exploring city and its surroundings you can"+
                      " find small random events. They are not quests, and "+
                      "don't leave any records in the journal.")
                null height 5
                text "However they still offer rewards if completed correctly."

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                ypos 80 xalign .5
                frame:
                    add pscale("content/gfx/interface/pyp/events.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
