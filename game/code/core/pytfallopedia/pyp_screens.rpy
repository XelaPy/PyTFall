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
            insensitive_background im.Sepia(img)
            action Hide("pytfallopedia")
            tooltip "Close PyTFollopedia"
            keysym "mousedown_3"

    # Left frame with buttons:
    side "c l":
        ypos 40
        vpgrid:
            id "vp"
            style_prefix "basic"
            xysize 300, config.screen_height-40
            mousewheel 1
            draggable 1
            cols 1
            for i in range(100):
                button:
                    xsize 280
                    text "Meow"
                    action NullAction()

        vbar value YScrollValue("vp")

    # Right frame with info (Will prolly be a bunch of separate screens in the future)
    viewport:
        pos 300, 40
        scrollbars "vertical"
        mousewheel 1
        draggable 1
        add Solid("F00")

    add "content/gfx/frame/h3.png"
