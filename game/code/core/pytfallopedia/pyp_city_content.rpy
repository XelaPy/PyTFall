screen pyp_city():
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
                text "City" size 30

            vbox:
                ypos 80
                spacing 20
                text ("The City has three Quarters, Richford, Midtown and Flee Bottom. There are"+
                      "many locations available with different events, quests, and possible actions.")

                text ("You will find many characters hanging around in most locations, as the game progresses,"+
                      " new characters will appear. The city is home for many NPCs who can help you with the game,"+
                      " and here you can also find friends and workers for your businesses or teammates to do"+
                      " battle in the Arena or to explore the Dark Forest.")

                text ("Many shops sell all kinds of items. You can buy spell scrolls or "+
                      "receive unique types of training from NPCs (some of which must be found first).")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                ypos 80
                add "content/gfx/interface/pyp/city.webp"

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_interactions():
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
                text "Interactions" size 30

            viewport:
                draggable 1
                mousewheel 1
                scrollbars "vertical"
                ypos 80 ysize 580
                has vbox spacing 8
                label "Interactions"
                text "In order to run a business or fight in a team you need workers. You can buy slaves at the slave market (see its section), but in order to get free characters you need to find them and hire."
                null height 5
                text "In most locations you will see a button in the bottom right corner called «Meet Girls». It allows to search the area for possible candidates. Then you can pick one of them and start interaction."
                null height 5
                text "During interactions you can speak to characters about different things, give gifts or money, hire or even romance them. Your goal is to increase disposition, as it makes all actions more successful. You can see the disposition bar all the time during interactions. Be careful though, some actions may decrease disposition. If you upset a character, she will refuse to talk to you for a few days."
                null height 5
                label "Gifts"
                text "Some items can be used as gifts. The effect of the gift is based on character personality, and remains the same. However some time should pass before you can use the same gift again."
                text "A character may dislike a particular gift. As you try new gifts, hints for them become available in the gifts menu, showing their effect for the current character."
                null height 5
                label "Hiring"
                text "You can't hire a character whose tier is much higher than the tier of the Main Character. But you still can romance them if you wish to."
                text "You can interact with the characters you hired from their profiles, but some options will be different for them."
                null height 5
                label "Friends List"
                frame:
                    align .5, .5
                    add "content/gfx/interface/pyp/interactions_1.webp"
                text "In hero profile screen you can find a list of all not hired characters you know closely. From there you can start interactions with them any time."

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/interactions.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_mc_actions():
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
                text "Actions" size 30

            viewport:
                draggable 1
                mousewheel 1
                scrollbars "vertical"
                ypos 80 ysize 580
                has vbox spacing 8
                label "Actions in the City"
                text ("In the City you can spend your Action Points on various minigames and "+
                      "other activities, getting various rewards for it. All minigames have their own tutorials once you discover them.")
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
                null height 5
                label "Work"
                text ("You can work at the Slave Market and make a quick buck. Either"+
                      " all Action Point or One Action point can be used at the time.")
                null height 15
                text "And there are many other things you can do, try to find them all!"

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            # Images and maybe details:

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_slave_market():
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
                text "Slave Market" size 30

            vbox:
                ypos 80
                spacing 20
                text ("In the Slave Market, you can buy slaves, work for a bit of cash and some stats"+
                      " and skills bonuses. Here you can also free a slave for a hefty fee if you so wish.")

                text ("New slave lots will arrive at the slave market as the game progresses."+
                      " The quality of such depends on Players tier, but there is always a chance"+
                      " of getting a high-quality option (if you can afford the price of course).")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 80
                spacing 10
                frame:
                    add pscale("content/gfx/interface/pyp/slave_market_0.webp", 350, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/slave_market_1.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_npcs():
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
                text "Non Playable Characters" size 30

            vbox:
                ypos 80
                text ("Many locations have key NPCs providing different services. "+
                      "Some of them are hidden, and should be discovered first.")
                null height 5
                text ("Try to look around in different locations. Note that some NPCs"+
                      " require high enough level or stats before you can find them.")
                null height 5
                text ("The NPCs can train you or other characters for a price, "+
                      "or sell you items you won't find anywhere else.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/npc.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_arena():
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
                text "Arena" size 30

            vbox:
                ypos 80
                spacing 20
                text ("Arena is a great place to do battle in a controlled environment. "+
                      "Unless it's a very specific match, stage-wide magical spells will prevent deadly blows.")

                text ("You can fight weird creatures in the Survival mode, where you are expected"+
                      " to get six wins in a row and challenge the Leader of the pack at turn seven.")

                text ("In Dogfights you can challenge other Arena Fighters to a friendly"+
                      " sparring match. In actual Matches, you can fight one on one or "+
                      "team vs. team for a place in the Arena Ladders, which is the most"+
                      " prestigious ranking available. Arena Fighters are also ranked by"+
                      " Arena Reputation, but that matters less as far as the spectators"+
                      " are concerned.")

                text ("You may get items (also unique items), arena reputation and Gold "+
                      "when winning at the Arena. It can be a decent source of income"+
                      " if running a business is not your cup of tea.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                ypos 80 xalign .5
                add pscale("content/gfx/interface/pyp/arena.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_main_street():
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
                text "Main Street" size 30

            vbox:
                ypos 80
                text ("Main Steet is where you'll find the most shops in the game, "+
                      "but more importantly, Real Estate Agency where you can buy "+
                      "buildings (fixed at this stage of development) and the "+
                      "Employment Agency where you can hire free workers.")

                text ("Some shops have unique actions available. You can take your"+
                      " friends out for lunch at the Café and improve on some items at the Tailors.")


        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                ypos 80 xalign .5
                add pscale("content/gfx/interface/pyp/main_street.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
