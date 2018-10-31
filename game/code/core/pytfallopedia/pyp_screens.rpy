screen pytfallopedia():
    zorder 1000
    modal True

    # Top Stripe Frame:
    fixed:
        xysize config.screen_width, 40
        add "content/gfx/frame/top_stripe.png"
        # Buttons:
        $ img = im.Scale("content/gfx/interface/buttons/close.png", 35, 35)
        imagebutton:
            align .996, .5
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(.15))
            insensitive_background img
            action Hide("pytfallopedia")
            tooltip "Close PyTFollopedia"
            keysym "mousedown_3"

        $ img = im.Scale("content/gfx/interface/buttons/arrow_button_metal_gold_left.png", 35, 35)
        imagebutton:
            align .03, .5
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(.15))
            insensitive_background img
            action NullAction()
            tooltip "Back"
            keysym "mousedown_2"

    # Right frame with info (Will prolly be a bunch of separate screens in the future)
    frame:
        background Frame("content/gfx/frame/mes11.webp", 2, 10)
        pos 286, 42
        padding 14, 2
        has viewport xsize config.screen_width-296 scrollbars "vertical" mousewheel 1 draggable 1
        add Solid("F00")
        vbox:
            xsize config.screen_width-290
            text "MOWN11112121221212122121212212121221221212121221211212121211212121212121212121212121212212121212122133333333333333333333333666666666666666666666666666666666"


    # Left frame with buttons:
    frame:
        pos 4, 42
        background Frame("content/gfx/frame/mes11.webp", 2, 2)
        padding 2, 12
        has side "c l"
        vpgrid:
            id "vp"
            style_prefix "basic"
            xysize 279, config.screen_height-51
            mousewheel 1
            draggable 1
            cols 1
            for i in range(100):
                button:
                    xsize 270
                    text "Meow #" + str(i)
                    action NullAction()

        vbar value YScrollValue("vp")



    add "content/gfx/frame/h3.png"
