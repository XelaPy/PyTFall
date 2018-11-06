screen pyp_city():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        # Screen Content goes here!

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_interactions():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        # Screen Content goes here!

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_mc_jobs():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        # Screen Content goes here!

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_mc_actions():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            label "Actions in the City"
            text "In the City you can spend your Action Points on various minigames and other activities, getting various rewards for it. All minigames have their own tutorials once you discover them."
            null height 15
            label "Fishing"
            text "On the beach you can try to catch some fish. Sometimes you get something more valuable."
            null height 5
            label "Diving"
            text "You can inspect the ocean floor to discover long sunken treasures."
            null height 5
            label "Wood Cutting"
            text "With an axe you can cut some trees in the forest and the sell them or use for upgrades."
            null height 5
            label "Exploring"
            text "You can explore cemetery ruins or the forest around the City to find enemies and treasures."
            null height 5
            label "Gambling"
            text "In the tavern you can play dices if you are feeling lucky."
            null height 15
            text "And there are many other things you can do, try to find them all!"
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_slave_market():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        # Screen Content goes here!

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_npcs():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        vbox:
            align .5, .5
            add "content/gfx/interface/pyp/npc.webp" align .5, .05
            label "Non Playable Characters"
            text "Many locations have key NPCs providing different services. Some of them are hidden, and should be discovered first."
            null height 5
            text "Try to look around in different locations. Note that some NPCs require high enough level or stats before you can find them."
            null height 5
            text "The NPCs can train you or other characters for a price, or sell you items you won't find anywhere else."

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

# screen pyp_look_around():
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

screen pyp_arena():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        # Screen Content goes here!

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_main_street():
    zorder 1001

    fixed:
        pos 302, 49
        xysize config.screen_width-309, config.screen_height-56
        style_prefix "proper_stats"

        # Mention Realtor and EA

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
