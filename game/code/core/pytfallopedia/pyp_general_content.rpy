screen pyp_default():
    zorder 999

    frame:
        background Frame("content/gfx/frame/mes11.webp", 2, 2)
        pos 300, 40
        padding 2, 2
        has viewport scrollbars "vertical" mousewheel 1 draggable 1
        add Solid("F00")



screen pyp_general():
    add Null()
