screen pytfallopedia():
    zorder 1000
    modal True

    default show_sub = True
    # variable is responsible for correctly toggling between main and sub cats buttons.
    # without this, returning to main will take an extra click.

    # Top Stripe Frame:
    fixed:
        xysize config.screen_width, 40
        add "content/gfx/frame/top_stripe.png"
        # Buttons:
        python:
            actions = [Hide("pytfallopedia")]
            if pyp.main_screen:
                actions.append(Hide(pyp.main_screen))
            if pyp.sub_screen:
                actions.append(Hide(pyp.sub_screen))
                actions.append(SetField(pyp, "sub_focused", None))
        $ img = im.Scale("content/gfx/interface/buttons/close.png", 35, 35)
        imagebutton:
            align .996, .5
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(.15))
            insensitive_background img
            action actions
            tooltip "Close PyTFallopedia"
            keysym "mousedown_3"

        $ img = im.Scale("content/gfx/interface/buttons/arrow_button_metal_gold_left.png", 35, 35)
        imagebutton:
            align .035, .5
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(.15))
            insensitive im.Sepia(img)
            insensitive_background img
            if pyp.sub_focused:
                action Hide(pyp.sub_screen), Show(pyp.main_screen), SetField(pyp, "sub_focused", None), SetScreenVariable("show_sub", False)
            elif pyp.main_focused:
                action Hide(pyp.main_screen), SetField(pyp, "main_focused", None)
            sensitive pyp.sub_focused or pyp.main_focused
            tooltip "Back"
            keysym "mousedown_2"

    # Right frame with info (Will prolly be a bunch of separate screens in the future)
    frame:
        background Frame("content/gfx/frame/mes11.webp", 2, 2)
        pos 289, 42
        xysize config.screen_width-287, config.screen_height-41
        style_prefix "proper_stats"

    if not pyp.main_focused and not pyp.sub_focused:
        fixed:
            pos 302, 49
            xysize 971, 664
            style_prefix "pyp"

            add "content/gfx/interface/logos/logo9.png" xalign .5 ypos 30

            vbox:
                align .5, .5
                label "Welcome to PyTFallopedia" xalign .5 text_size 40
                null height 100
                text "An in-game encyclopedia that introduces the player to the core game-world and game-play concepts!" xalign .5

    # Left frame with buttons:
    frame:
        pos 4, 42
        background Frame("content/gfx/frame/mes11.webp", 2, 2)
        padding 2, 12
        has side "c l"
        vpgrid:
            id "vp"
            style_prefix "basic"
            xysize 279, config.screen_height-53
            mousewheel 1
            draggable 1
            cols 1
            if pyp.main_focused in pyp.sub and show_sub:
                for name, screen in pyp.sub[pyp.main_focused]:
                    button:
                        xsize 270
                        text name
                        if pyp.sub_focused:
                            action Hide(pyp.sub_screen), SetField(pyp, "sub_focused", (name, screen)), Show(screen)
                        else:
                            action SetField(pyp, "sub_focused", (name, screen)), Hide(pyp.main_screen), Show(screen)
            else:
                for name, screen in pyp.main.items():
                    python:
                        actions = [SetField(pyp, "main_focused", name), Show(screen), SetScreenVariable("show_sub", True)]
                        if pyp.main_screen:
                            actions.insert(0, Hide(pyp.main_screen))
                    button:
                        xsize 270
                        text name
                        action actions
                        selected pyp.main_screen is not None and screen == pyp.main[pyp.main_focused]

        vbar value YScrollValue("vp")

    if not pyp.main_focused and not pyp.sub_focused:
        add "content/gfx/frame/h3.webp"

# DEFAULT positioning blueprint that can be used with any screen pyp info in the future.
screen pyp_default():
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
                text "**Title**" size 30

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            # Images and maybe details:

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
