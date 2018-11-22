screen pyp_general():
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
                text "PyTFall" size 30

            vbox:
                ypos 80
                label "Open World H/Sim Game"
                null height 20
                text ("PyTFall is an open source, turn-based Sim game with a Hentai twist"+
                      " developed to serve as a next-generation of WM and SimBro focusing on "+
                      "gathering a team of workers, managing businesses, leveling up "+
                      "the MC and other characters and Date-Sim Elements, "+
                      "RPG Style Combat and Exploration, Interactions and etc.")
                null height 10
                text ("Events of PyTFall take place in the same universe as those of WM"+
                      " (Whore Master). The world itself poses barely any rules or"+
                      " guidelines to it. The WM's original City (CrossGate) still "+
                      "exists in the time frame of PyTFall and is described as "+
                      "'the slave capital of the World'.")
                null height 10
                text ("In the future, we're hoping to expand it with many more cities, businesses, gang-fighting, "+
                      "Politics that have a direct effect on game world rules (such as slavery being forbidden, slaves not"+
                      " being able to part-take in combat, prostitution banned and etc.), Economy, Religions, World Events, and much more.")


        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                align .5, .5
                spacing 7
                add pscale("content/gfx/interface/logos/logo9.png", 250, 250):
                    xalign .5
                frame:
                    add pscale("content/gfx/interface/pyp/pf.webp", 350, 1000)
                add pscale("content/gfx/interface/logos/logo9.png", 250, 250):
                    xalign .5

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_game_settings():
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
                text "Game Settings" size 30

            vbox:
                ypos 80
                text "Before you begin, the game has important settings in the Game tab of main menu. It's important to understand them for better gaming experience."
                null height 10
                vbox:
                    label "Panic Screen"
                    text "If it's enabled enabled, by pressing Q on keyboard you replace everything on a screen with a sfw picture. The only way to get hid of it is to press Q again. Useful if you want to hide NSFW content when someone enters your room."
                vbox:
                    label "Battle Results"
                    text "If enabled, shows screen with battle results after every battle. Doesn't affect the arena, works in location like Forest. You can disable it to speed up gameplay a bit."
                vbox:
                    label "Combat Targeting"
                    text "Toggles between two types of interface during the battle. The difference is visible when you select a target for your attack. Use the one you like the most."
                vbox:
                    label "Auto Saves"
                    text "If enabled, the game makes an auto save each time you close Next Day screen. It may slow down gameplay since it takes a few seconds, especially without SSD."
                vbox:
                    label "Quest Pop-Ups"
                    text "If enabled, displays a big notification window when you progress in a quest."
                vbox:
                    label "Tooltips"
                    text "If enabled, shows tooltips for most elements of game interface."
                    
        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add "content/gfx/interface/pyp/settings.webp"
                
    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_time_flow():
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
                text "Time Progression" size 30

            vbox:
                ypos 80
                text ("One turn of the game corresponds to one day, in which the Player"+
                      " can take actions, perform tasks, jobs and date-sim to his/her heart's content.")
                null height 10
                text ("There is presently no concept of daytimes (Morning/Day/Evening/Night)"+
                      " in PyTFall, although we develop with a presence of those in mind. A large amount of"+
                      " extra content (mostly backgrounds) that would be required is scary and not reasonable to mess"+
                      " around with at this development stage.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            add pscale("content/gfx/interface/icons/clock.png", 250, 250):
                xalign .5 ypos 50

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_action_points():
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
                text "Action Points" size 30

            text ("Actions Points decide how many actions "+
                  "the Player and other Characters can take per one game turn (Day). "+
                  " The amount of AP depends on stats (constitution) and Traits."+
                  " When performing Jobs during the Next Day, 'AP' is converted to Job Points (1 AP = 100 JP)"+
                  " that can be affected by Upgrades and Manager effects. For Interactions,"+
                  " AP is converted into Interaction Points (1 AP = 3 IP)."):
                      ypos 80


        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/ap.webp", 250, 100)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_next_day():
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
                text "Next Day" size 30

            vbox:
                ypos 80
                text ("Next Day starts execution of businesses, training and some events"+
                      " pushing the game to the next day.")
                null height 10
                text ("For any Character (including the Player itself), Next Day will execute whatever 'Action'"+
                      " they are set to perform and spend the remaining amount of Action Points performing it. "+
                      " At the end of such a cycle, you will be able to review detailed reports of everything that has happened "+
                      " as those actions and events were performed.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 80
                spacing 20
                frame:
                    xalign .5
                    add pscale("content/gfx/interface/pyp/next_day_button.webp", 350, 1000)
                frame:
                    xalign .5
                    add pscale("content/gfx/interface/pyp/next_day_screen.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_controls():
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
                text "Controls Info" size 30

            text ("Most actions in PyTFall are performed with LMB (Left Mouse Button). RMB "+
                  "(Right Mouse Button), is also of great use as it will attempt to 'return' "+
                  "you to the previous screen or close the current one. Mousewheel is used in "+
                  "viewports and for paging.\n\nIn rare cases, RMB will trigger an alternative action,"+
                  " tooltips are used to hint at where. There are also a number of shortkeys ('a' for Arena,"+
                  " 'f' for Forest Entrance, 'm' for Slave Market, 'p' for Main Street, 'i' for MC's Equipment Screen),"+
                  " most of them lead to specific locations and will be activated after the player visits"+
                  " the corresponding location at least once. Such shortkeys are available from main-screen."+
                  " 'q' will work everywhere and will call up a so-called 'panic screen',"+
                  " 's' will take a screenshot of the game and place it in the root folder of the game.\n\n"+
                  "A number of controls and behavior can be adjusted under 'Game' options in preferences."):
                      ypos 80

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            vbox:
                xalign .5 ypos 80
                spacing 10
                frame:
                    add pscale("content/gfx/interface/pyp/actions_0.webp", 350, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/actions_1.webp", 350, 1000)
                frame:
                    add pscale("content/gfx/interface/pyp/actions_2.webp", 350, 1000)

screen pyp_gazette():
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
                text "PyTFall GAZETTE" size 30

            vbox:
                ypos 80
                text ("Gazzete reports on major events in the city!")
                null height 10
                text ("It will be significantly expanded once we have World Events, "+
                      "Politics, and Economy. For now, you will know about the events at the Arena, "+
                      " shop and slave market restocks and new workers submitting their applications to"+
                      " the Employment agency!")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add "content/gfx/interface/pyp/gazette.webp" align .5, .05

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
