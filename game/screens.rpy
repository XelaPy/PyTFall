# This file is in the public domain. Feel free to modify it as a basis
# for your own screens.

##############################################################################
# Say
#
# Screen that's used to display adv-mode dialogue.
# http://www.renpy.org/doc/html/screen_special.html#say
screen say(who, what, side_image=None, two_window=False):
    zorder 10
    # add Transform(Text("PyTFaLL", style="earthkid", color=black, size=50), alpha=.6) align (0.6, 0.9)
    # add Transform(Text("PyTFaLL", style="earthkid", color=azure, size=70), alpha=.5) align (0.1, 0.95)
    # add Transform(Text("PyTFaLL", style="earthkid", color=black, size=50), alpha=.6) align (0.8, 0.98)
    # add Transform(Text("PyTFaLL", style="earthkid", color=black, size=50), alpha=.6) align (0.9, 0.9

    if block_say:
        button:
            background Null()
            xysize (config.screen_width, config.screen_height)
            action Return()

    # Decide if we want to use the one-window or two-window variant.
    if not two_window:

        # The one window variant.
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what"

    else:

        # The two window variant.
        vbox:
            style "say_two_window_vbox"

            if who:
                window:
                    style "say_who_window"

                    text who:
                        id "who"

            window:
                id "window"

                has vbox:
                    style "say_vbox"

                text what id "what"

    # If there's a side image, display it above the text.
    if side_image:
        # In order to have more control over the say screen portraits for Chars we pass instances of Char here:
        if isinstance(side_image, Char):
            if side_image.say_screen_portrait_overlay_mode == "zoom_fast":
                add At(side_image.say_screen_portrait, interactions_zoom(.2)) pos 219, 639 anchor .5, .5
            elif side_image.say_screen_portrait_overlay_mode == "zoom_slow":
                add At(side_image.say_screen_portrait, interactions_zoom(1.2)) pos 219, 639 anchor .5, .5
            elif side_image.say_screen_portrait_overlay_mode == "test_case":
                add side_image.say_screen_portrait pos 219, 639 anchor .5, .5
                # add interactions_surprised_tr pos 150, 650 yanchor 1.0
            else:
                add side_image.say_screen_portrait pos 219, 639 anchor .5, .5


            if side_image.say_screen_portrait_overlay_mode not in [None] + STATIC_CHAR.UNIQUE_SAY_SCREEN_PORTRAIT_OVERLAYS:
                timer .0001 action Function(interactions_portraits_overlay.change, side_image.say_screen_portrait_overlay_mode)
                add interactions_portraits_overlay
        else:
            add side_image xalign 0.138 yalign 0.968
            add interactions_portraits_overlay
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # Use the quick menu.
    use quick_menu

##############################################################################
# Choice
#
# Screen that's used to display in-game menus.
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):

    zorder 15
    modal True

    window:
        style "menu_window"
        align (0.5, 0.5)

        vbox:
            style "menu"
            spacing 2

            $ item = items[0][0]
            if item in menu_extensions:
                for cap, act in menu_extensions.build_choices(item):
                    if act:
                        button:
                            if isinstance(act, (list, tuple)) and "return" in act:
                                action MenuExtensionAction(act, [items[0][1]])
                            else:
                                action act
                            style "menu_choice_button_blue"

                            text cap style "menu_choice"

                    else:
                        text cap style "menu_caption"

            for caption, action, chosen in items:
                if caption in menu_extensions:
                    $ pass
                else:
                    if action:
                        button:
                            action action
                            style "menu_choice_button"

                            text caption style "menu_choice"

                    else:
                        text caption style "menu_caption"


init -2:
    $ config.narrator_menu = True

##############################################################################
# Input
#
# Screen that's used to display renpy.input()
# http://www.renpy.org/doc/html/screen_special.html#input
screen input(prompt=""):
    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

##############################################################################
# Nvl
#
# Screen used for nvl-mode dialogue and menus.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # Display dialogue.
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # Display a menu, if given.
        if items:

            vbox:
                id "menu"

                for caption, action, chosen in items:

                    if action:

                        button:
                            style "nvl_menu_choice_button"
                            action action

                            text caption style "nvl_menu_choice"

                    else:

                        text caption style "nvl_dialogue"

    add SideImage() xalign 0.0 yalign 1.0

    use quick_menu

##############################################################################
# Main Menu
#
# Screen that's used to display the main menu, when Ren'Py first starts
# http://www.renpy.org/doc/html/screen_special.html#main-menu

transform patreon_hover(init_alpha=.25):
    alpha init_alpha additive .4
    on hover:
        linear 1.0 alpha 1.0
    on idle:
        linear 1.0 alpha .25

screen main_menu():
    tag menu

    default prereqs = exist(["content/chars/", "content/rchars/"])

    default map_options = ["content/gfx/bg/locations/map_buttons/dark/", "content/gfx/bg/locations/map_buttons/bright/", "content/gfx/bg/locations/map_buttons/gismo/"]

    # The background of the main menu.
    add "bg_main"

    if not renpy.get_screen("credits"):
        vbox:
            align (.5, .01)
            text "Support us on:":
                at patreon_hover(init_alpha=.4)
                xalign .5
                size 22
                color goldenrod
                drop_shadow [(1, 2)]
                drop_shadow_color black
                antialias True
            hbox:
                spacing 60
                button:
                    at patreon_hover
                    xalign .5
                    xysize (100, 100)
                    background pscale("content/gfx/interface/icons/credits/x_hole_idle.png", 100, 100)
                    hover_background pscale("content/gfx/interface/icons/credits/x_hole_hover.png", 100, 100)
                    action OpenURL('https://www.patreon.com/xelapy')
                    add At(pscale("content/gfx/interface/icons/credits/patreonlogoorange.png", 100, 25, yalign=1.0), patreon_bounce)
                # null width 10
                button:
                    at patreon_hover
                    xalign .5
                    xysize (100, 100)
                    background pscale("content/gfx/interface/icons/credits/dark_hole_idle.png", 100, 100)
                    hover_background pscale("content/gfx/interface/icons/credits/dark_hole_hover.png", 100, 100)
                    action OpenURL('https://www.patreon.com/darkt')
                    add At(pscale("content/gfx/interface/icons/credits/patreonlogoorange.png", 100, 25, yalign=1.0), patreon_bounce)

    # button:
        # background "content/gfx/interface/logos/gibc.png"
        # hover_background im.MatrixColor("content/gfx/interface/logos/gibc.png", im.matrix.brightness(0.10))
        # action OpenURL('https://mega.nz/#!mxAw0Q5b!F-4-An4oK5TbB9BO5e-M0Elslolrim6t3UxBdGolj-8')
        # focus_mask True
        # xysize(350, 342)
    # $ index = map_options.index(persistent.town_path)
    # button:
        # xalign 0
        # yalign 1.0
        # xysize (60, 25)
        # style "blue1"
        # text "<->" color black align (0.5, 0.5) size 15
        # action [SetField(persistent, "town_path", map_options[(index + 1) % len(map_options)]), Jump("_save_reload_game")]

    # $ img = ProportionalScale("content/gfx/interface/icons/arena.png", 60, 60)
    #imagebutton:
        #pos (380, 460)
        #idle (img)
        #hover (im.MatrixColor(img, im.matrix.brightness(0.25)))
        #action Show("credits", transition=ImageDissolve("content/gfx/masks/m02.webp", 3))
    if not prereqs:
        frame:
            background Frame("content/gfx/frame/frame_gp.webp", 40, 40)
            xanchor 0
            xpos 0.50
            xmaximum 300
            yalign 0.5
            text ("Resources are missing, the game won't run without."+
                "At least one unique character with accompanied .json is required "+
                "in the\n{i}game/content/chars/{/i} subdirectory of PyTFall as well as "+
                "one random character .json in the\n"+
                "{i}game/content/{b}r{/b}chars/{/i} directory.") size 15
    # ===== Animation ===== #

    viewport:
        xysize (768, 328)
        pos (514, 100)
        add "mm_clouds" at mm_clouds(768, 0, 50)
        add "mm_clouds" at  mm_clouds(0, -768, 50)

    add "eyes" pos (150, 410)
    # add "logo" pos (980, 250)
    add "anim_logo" pos (980, 250) # static logo
    add "fog" at fog

    # Fire
    viewport:
        xysize (200, 526)
        pos (580, 100)
        # add Transform(Solid(red, xysize=(20, 263)), alpha=1) at mm_fire(366, 0, 30)
        # add Transform(Solid(black, xysize=(20, 263)), alpha=1) at mm_fire(1009, 0, 30)
        add "mm_fire" at mm_fire(263, 0, 1.0, 0, 8)
        add "mm_fire" at mm_fire(526, 263, 0, 1, 8)
        add "mm_fire" at mm_fire(426, 163, 0.5, 0, 8)

    # The main menu buttons.
    vbox:
        align (0.947, 0.87)
        frame:
            background Null()
            style_group "mmenu"
            vbox:
                spacing 4
                textbutton _("New Game") action SensitiveIf(prereqs), Start() xalign 0.5
                null height 4
                textbutton _("Load Game") action SensitiveIf(prereqs), Show("s_menu", s_menu="Load", main_menu=True), With(dissolve)

                textbutton _("Settings") action Show("s_menu", s_menu="Settings", main_menu=True), With(dissolve)
                hbox:
                    xalign 0.5
                    textbutton _("Credits") action Show("credits", transition=ImageDissolve("content/gfx/masks/m02.webp", 1)) xsize 85 text_size 16
                    textbutton _("Help") action Show("discord", transition=ImageDissolve("content/gfx/masks/m02.webp", 1)) xsize 85 text_size 16
                textbutton _("Quit") action Quit(confirm=False) xalign 0.5


screen discord():
    zorder 1
    modal True
    frame:
        background Transform(Frame("content/gfx/frame/frame_dec_1.png", 20, 20), alpha=.7)
        pos(10, 120)
        xysize (900, 580)
        style_group "mmenu"
        textbutton "Hide":
            align(0.5, 0.90)
            action Hide("discord", transition=dissolve)
        vbox:
            xalign .5
            yalign .2
            text "The game is still in development. Support us if you enjoyed it!" align (.45, .1) size 25 color goldenrod drop_shadow [(1, 2)] drop_shadow_color black antialias True style_prefix "proper_stats"
            null height 10
            text "ANY QUESTIONS OR BUGS TO REPORT?" size 35 color goldenrod drop_shadow [(1, 2)] drop_shadow_color black antialias True style_prefix "proper_stats" xalign .5
            text "JOIN OUR COMMUNITY ON:" size 35 color goldenrod drop_shadow [(1, 2)] drop_shadow_color black antialias True style_prefix "proper_stats" xalign .5
        null height 5
        button:
            yalign .6
            xalign .5
            xysize 300, 83
            background Transform("content/gfx/interface/icons/credits/discord.png", zoom=.9, align=(.5, .5))
            hover_background Transform("content/gfx/interface/icons/credits/discord.png", align=(.5, .5))
            action OpenURL("https://discord.gg/4tT4qmW")


screen credits():
    zorder 1 modal True

    frame:
        background Transform(Frame("content/gfx/frame/frame_dec_1.png", 20, 20), alpha=.9)
        pos (10, 10)
        xysize (900, 700)
        style_group "mmenu"

        text "About Us":
            xalign .5 ypos 50
            size 35
            color goldenrod
            drop_shadow [(1, 2)]
            drop_shadow_color black
            antialias True
            style_prefix "proper_stats"

        side "c r":
            area (100, 100, 800, 550)
            viewport id "vp":
                draggable True
                mousewheel True
                vbox:
                    hbox:
                        xalign .52
                        vbox:
                            style_prefix "proper_stats"
                            text "Core Coding" xalign .5 size 22 color goldenrod drop_shadow [(1, 2)] drop_shadow_color black antialias True
                            button:
                                xalign .5
                                xysize (100, 100)
                                background ProportionalScale("content/gfx/interface/icons/credits/x_hole_idle.png", 100, 100)
                                hover_background ProportionalScale("content/gfx/interface/icons/credits/x_hole_hover.png", 100, 100)
                                action OpenURL('https://www.patreon.com/xelapy')
                                add At(pscale("content/gfx/interface/icons/credits/patreonlogoorange.png", 100, 25, yalign=1.0), patreon_bounce)
                            null height 3
                            text " XelaPy " xalign .5 size 30 color goldenrod drop_shadow [(1, 2)] drop_shadow_color black antialias True
                            hbox:
                                spacing 10
                                xalign .5
                                button:
                                    xysize 30, 30
                                    background Frame("content/gfx/interface/icons/credits/twitter.png")
                                    hover_background Frame(im.MatrixColor("content/gfx/interface/icons/credits/twitter.png", im.matrix.brightness(.05)))
                                    action OpenURL('https://twitter.com/XelaPy')
                                button:
                                    xysize 30, 30
                                    background Frame("content/gfx/interface/icons/credits/youtube.png")
                                    hover_background Frame(im.MatrixColor("content/gfx/interface/icons/credits/youtube.png", im.matrix.brightness(.05)))
                                    action OpenURL('https://www.youtube.com/channel/UCWnMQ6MO-KpMytYf4hoFFBA')
                        null width 100
                        vbox:
                            style_prefix "proper_stats"
                            text "Content and Coding":
                                size 22
                                xalign .5
                                color goldenrod
                                drop_shadow [(1, 2)]
                                drop_shadow_color black
                                antialias True
                            button:
                                xalign .5
                                xysize (100, 100)
                                background pscale("content/gfx/interface/icons/credits/dark_hole_idle.png", 100, 100)
                                hover_background pscale("content/gfx/interface/icons/credits/dark_hole_hover.png", 100, 100)
                                action OpenURL('https://www.patreon.com/darkt')
                                add At(pscale("content/gfx/interface/icons/credits/patreonlogoorange.png", 100, 25, yalign=1.0), patreon_bounce)
                            null height 3
                            text " DarkTl ":
                                align .5, 1.0
                                size 30
                                color goldenrod
                                drop_shadow [(1, 2)]
                                drop_shadow_color black
                                antialias True
                            null height 30

                    null height 10

                    text "The game is still in development. Support us if you enjoyed it!":
                        size 25
                        color goldenrod
                        drop_shadow [(1, 2)]
                        drop_shadow_color black
                        antialias True
                        style_prefix "proper_stats"

                    null height 10

                    vbox:
                        style_prefix "proper_stats"
                        text "Special thanks to:":
                            size 22
                            color goldenrod
                            drop_shadow [(1, 2)]
                            drop_shadow_color black
                            antialias True
                        text "All artists and composers for amazing content featured in PyTFall."
                        text "Tom Rothamel for Ren'Py."

                        null height 10
                        text "Many thanks to:":
                            size 22
                            color goldenrod
                            drop_shadow [(1, 2)]
                            drop_shadow_color black
                            antialias True
                        text "TheWorst, Gismo, Picobyte, CherryWood, Xipomus, Lamoli, Thewlis, Rudistoned,"
                        text "Eliont, Matt, Longint, Armegetton, MrKlaus, Krakr, Sysreq, GonDra, Jaeke, Janmaba."

        textbutton "Hide":
            align .5, .90
            action Hide("credits", transition=dissolve)


##############################################################################
# Navigation
#
# Screen that's included in other screens to display the game menu
# navigation and background.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation():

    # The background of the game menu.
    # window:
        # style "gm_root"

    # The various buttons.
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Return") action Return()
        textbutton _("Settings") action Show("s_menu", s_menu="Settings"), With(dissolve) # action ShowMenu("preferences")
        textbutton _("Save Game") action Show("s_menu", s_menu="Save"), With(dissolve) # action ShowMenu("save")
        textbutton _("Load Game") action Show("s_menu", s_menu="Load"), With(dissolve) # action ShowMenu("load")
        textbutton _("Main Menu") action MainMenu()
        # textbutton _("Help") action Help()
        textbutton _("Quit") action Quit()

    key "mousedown_3" action Return()

##############################################################################
# Yes/No Prompt
#
# Screen that asks the user a yes or no question.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt

screen yesno_prompt(message, yes_action, no_action):
    zorder 10000000
    modal True

    # window:
        # style "gm_root"

    add Transform("content/gfx/images/bg_gradient2.webp", alpha=.3)
    frame:
        background Frame (Transform("content/gfx/frame/ink_box.png", alpha=.65), 10, 10)
        style_prefix "dropdown_gm2"
        minimum 550, 200
        margin 10, 10
        padding 10, 10
        align .5, .1
        has vbox:
            align .5, .5
            spacing 30

        label _(message) xalign 0.5 text_text_align 0.5 text_color "#ecc88a" text_font "fonts/TisaOTM.otf" text_size 17 text_outlines [(1, "#3a3a3a", 0, 0)]

        hbox:
            xalign .5
            spacing 100

            textbutton _("Yes") action yes_action
            textbutton _("No") action no_action

    # Right-click and escape answer "no".
    key "game_menu" action no_action
    key "K_RETURN" action yes_action
    key "K_ESCAPE" action no_action


##############################################################################
# Quick Menu
#
# A screen that's included by the default say screen, and adds quick access to
# several useful functions.
screen quick_menu():

    # Add an in-game quick menu.
    hbox:
        style_group "quick"

        #xalign 1.0
        #yalign 1.0
        pos (937,773)

        # textbutton _("Back") action Rollback()
        # textbutton _("Save") action ShowMenu('save')
        textbutton _("Q.Save") action QuickSave()
        textbutton _("Q.Load") action QuickLoad()
        textbutton _("Skip") action Skip()
        textbutton _("F.Skip") action Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        # textbutton _("Prefs") action ShowMenu('preferences')

init: # Default preference menus, replaces by our own versions:
    ##############################################################################
    # Save, Load
    #
    # Screens that allow the user to save and load the game.
    # http://www.renpy.org/doc/html/screen_special.html#save
    # http://www.renpy.org/doc/html/screen_special.html#load

    # Since saving and loading are so similar, we combine them into
    # a single screen, file_picker. We then use the file_picker screen
    # from simple load and save screens.

    screen file_picker():

        frame:
            style "file_picker_frame"

            has vbox

            # The buttons at the top allow the user to pick a
            # page of files.
            hbox:
                style_group "file_picker_nav"

                textbutton _("Previous"):
                    action FilePagePrevious()

                textbutton _("Auto"):
                    action FilePage("auto")

                textbutton _("Quick"):
                    action FilePage("quick")

                for i in range(1, 9):
                    textbutton str(i):
                        action FilePage(i)

                textbutton _("Next"):
                    action FilePageNext()

            $ columns = 2
            $ rows = 4

            # Display a grid of file slots.
            grid columns rows:
                transpose True
                xfill True
                style_group "file_picker"

                # Display ten file slots, numbered 1 - 10.
                for i in range(1, columns * rows + 1):

                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Empty Slot."))
                    $ json_info = FileJson(i, empty= _(""))
                    $ save_name = FileSaveName(i)

                    # Each file slot is a button.
                    button:
                        action  FileAction(i)
                        xfill True

                        has hbox

                        # Add the screenshot.
                        add FileScreenshot(i)

                        vbox:
                            spacing 1
                            text "[file_name]. [file_time!t]\n[save_name!t]" xpos 70
                            hbox:
                                xpos 20
                                spacing 4
                                for key in json_info:
                                    if not key.startswith("_"):
                                        $ val = json_info[key]
                                        text "[key]: [val]"

                        key "save_delete" action FileDelete(i)


    screen save():

        # This ensures that any other menu screen is replaced.
        tag menu

        use navigation
        use file_picker

    screen load():

        # This ensures that any other menu screen is replaced.
        tag menu

        use navigation
        use file_picker

    ##############################################################################
    # Preferences
    #
    # Screen that allows the user to change the preferences.
    # http://www.renpy.org/doc/html/screen_special.html#prefereces

    screen preferences():

        tag menu

        # Include the navigation.
        use navigation

        # Put the navigation columns in a three-wide grid.
        grid 3 1:
            style_group "prefs"
            xfill True

            # The left column.
            vbox:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Display")
                    textbutton _("Window") action Preference("display", "window")
                    textbutton _("Fullscreen") action Preference("display", "fullscreen")

                frame:
                    style_group "pref"
                    has vbox

                    label _("Transitions")
                    textbutton _("All") action Preference("transitions", "all")
                    textbutton _("None") action Preference("transitions", "none")

                frame:
                    style_group "pref"
                    has vbox

                    label _("Text Speed")
                    bar value Preference("text speed")

                frame:
                    style_group "pref"
                    has vbox

                    textbutton _("Joystick...") action Preference("joystick")

            vbox:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Skip")
                    textbutton _("Seen Messages") action Preference("skip", "seen")
                    textbutton _("All Messages") action Preference("skip", "all")

                frame:
                    style_group "pref"
                    has vbox

                    textbutton _("Begin Skipping") action Skip()

                frame:
                    style_group "pref"
                    has vbox

                    label _("After Choices")
                    textbutton _("Stop Skipping") action Preference("after choices", "stop")
                    textbutton _("Keep Skipping") action Preference("after choices", "skip")

                frame:
                    style_group "pref"
                    has vbox

                    label _("Auto-Forward Time")
                    bar value Preference("auto-forward time")

                    if config.has_voice:
                        textbutton _("Wait for Voice") action Preference("wait for voice", "toggle")

            vbox:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Mute")

                    textbutton "Music":
                        action Preference("music mute", "toggle")
                    textbutton "Sound":
                        action Preference("sound mute", "toggle")

                frame:
                    style_group "pref"
                    has vbox

                    label _("Music Volume")
                    bar value Preference("music volume")

                frame:
                    style_group "pref"
                    has vbox

                    label _("Sound Volume")
                    bar value Preference("sound volume")

                    if config.sample_sound:
                        textbutton _("Test"):
                            action Play("sound", config.sample_sound)
                            style "soundtest_button"

                if config.has_voice:
                    frame:
                        style_group "pref"
                        has vbox

                        label _("Voice Volume")
                        bar value Preference("voice volume")

                        textbutton _("Voice Sustain") action Preference("voice sustain", "toggle")
                        if config.sample_voice:
                            textbutton _("Test"):
                                action Play("voice", config.sample_voice)
                                style "soundtest_button"
