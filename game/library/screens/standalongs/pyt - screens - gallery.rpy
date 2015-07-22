label gallery:
    scene bg gallery
    show screen pyt_gallery
    with dissolve
    
    $ pyt_gallery.screen_loop()
    
    hide screen pyt_gallery
    with dissolve
    $ pyt_gallery = None
    jump girl_profile
    
screen pyt_gallery():
    
    default black_bg = True
    
    # Tags + Image:
    vbox:
        style_group "content"
        # Tags:
        frame:
            background Frame("content/gfx/frame/p_frame7.png", 10, 10)
            align (0.5, 0.5)
            xysize (980, 40)
            text "Tags: [pyt_gallery.tags]" align(0.5, 0.5) color ivory
        # Img:
        frame:
            xysize (980, 680)
            background Frame("content/gfx/frame/p_frame7.png", 10, 10)
            xpadding 0
            ypadding 0
            xmargin 0
            ymargin 0
            frame:
                align(0.5, 0.5)
                xpadding 7
                ypadding 7
                xmargin 0
                ymargin 0
                if black_bg:
                    background Frame("content/gfx/frame/MC_bg3.png", 10 ,10)
                else:
                    background Frame(im.Twocolor("content/gfx/frame/MC_bg3.png", white, white), 10 ,10)
                add (pyt_gallery.image) align (0.5, 0.5) 
            if config.developer:
                button:
                    if black_bg:
                        background Solid(white, xysize=(30, 30))
                    else:
                        background Solid(black, xysize=(30, 30))
                    xysize (30, 30)
                    action SetScreenVariable("black_bg", not black_bg)
                    align (1.0, 0)

    # Tags Buttons and controls:
    vbox:
        align (1.0, 0)
        # Tags:
        frame:
            background Frame("content/gfx/frame/p_frame5.png", 15, 15)
            xysize (300, 570)
            has vbox xalign 0.5
            if config.developer:
                $ img = ProportionalScale("content/gfx/interface/logos/logo9.png", 280, 60)
                button:
                    xalign 0.5
                    xysize (280, 60)
                    insensitive_background im.Sepia(img)
                    idle_background img
                    hover_background im.MatrixColor(img, im.matrix.brightness(0.15))
                    action If(pyt_gallery.td_mode == "dev", true=Return(["change_dict", "full"]), false=Return(["change_dict", "dev"]))
            else:
                add ProportionalScale("content/gfx/interface/logos/logo9.png", 280, 60) xalign 0.5
            null height 2
            frame:
                background Frame(Transform("content/gfx/frame/mc_bg.png", alpha=0.5), 5, 5)
                xysize (280, 495)
                xalign 0.5
                # ypos 15
                side "c r":
                    viewport id "g_buttons_vp":
                        xysize (260, 480)
                        style_group "basic"
                        draggable True
                        mousewheel True 
                        vbox:
                            $ pyt_gallery.tagsdict = OrderedDict(sorted(pyt_gallery.tagsdict.items(), key=itemgetter(1), reverse=True))
                            for key in pyt_gallery.tagsdict:
                                hbox:
                                    $ name = key.capitalize()
                                    $ amount = pyt_gallery.tagsdict[key]
                                    if key == pyt_gallery.girl.id:
                                        $ name = "All Images"
                                    button:
                                        xysize (240, 30)
                                        action Return(["tag", key])
                                        fixed:
                                            xysize (230, 28)
                                            text "[name]" xalign 0
                                            text "{color=[blue]}[amount]" xalign 1.0
                    vbar value YScrollValue("g_buttons_vp")

        # Buttons:                
        frame:
            yoffset -3
            background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
            style_group "basic"
            xysize (300, 155)
            has vbox xalign 0.5 spacing 5
            textbutton "SlideShow":
                xalign 0.5
                action Return(["view_trans"])
            hbox:
                xalign 0.5
                spacing 20
                use r_lightbutton(img=im.Scale("content/gfx/interface/buttons/blue_arrow_left.png", 60, 60), return_value =['image', 'previous'])
                use exit_button(size=(45, 45), align=(0.5, 0.5))
                use r_lightbutton(img=im.Scale("content/gfx/interface/buttons/blue_arrow_right.png", 60, 60),return_value =['image', 'next'])
            textbutton "Lets Jig with this girl! :)":
                xalign 0.5
                action Jump("jigsaw_puzzle_start")

                
screen pyt_gallery_trans():
    zorder 5000
    button:
        align (0.5, 0.5)
        background None
        xysize (config.screen_width, config.screen_height)
        xfill True
        yfill True
        action SetVariable("stop_dis_shit", True)
