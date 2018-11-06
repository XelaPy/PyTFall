screen pyp_quests_and_events():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            label "Quests and Events"
            text "The game has a system of quests and events. Not all of them are available from the beginning, some require a certain level, high enough day counter or are simply randomized."
            null height 5
            text "Right now there is not much quests and events, but we hope to add much more in the future!"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_quests():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            frame:
                align .5, .1
                background Frame("content/gfx/frame/mes11.webp", 10, 10)
                padding 6, 6
                add "content/gfx/interface/pyp/quest_1.webp"
            null height 15
            frame:
                align .5, .1
                background Frame("content/gfx/frame/mes11.webp", 10, 10)
                padding 6, 6
                add "content/gfx/interface/pyp/quest_2.webp"
            label "Quests"
            text "Sometimes you can get a quest after discovering something or talking to a character. The game shows a notification each time you get, update or close one."
            null height 5
            text "You can check all known quests in the quests journal."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_events():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            frame:
                align .5, .1
                background Frame("content/gfx/frame/mes11.webp", 10, 10)
                padding 6, 6
                add "content/gfx/interface/pyp/events.webp"
            label "Events"
            text "Sometimes by exploring city and its surroundings you can find small random events. They are not quests, and don't leave any records in the journal."
            null height 5
            text "However they still offer rewards if completed correctly."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
