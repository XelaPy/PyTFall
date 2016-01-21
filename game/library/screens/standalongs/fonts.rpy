label fonts:
    python:
        fonts = list()
        for font in os.listdir(renpy.loader.transfn("fonts")):
            fonts.append("fonts/" + font)
    call screen fonts(fonts)        
            
screen fonts(fonts):
    
    zorder 1000
    
    default index = 0
    
    add Solid(black)
    
    vbox:
        align (0.5, 0.1)
        vbox:
            text fonts[index].strip("fonts/")
            text u"Hyūga Hinata" font fonts[index]
            hbox:
                text "Charisma" font fonts[index]
                null width 30
                text "1590" font fonts[index]
            text u" & * + # %"  font fonts[index]
            text u" & * + # %"  font fonts[index]
            text u" ¼ ½  ¾"  font fonts[index]
            text u"❤ ☀ ☆ ☂ ☻ ♞ ☯ ☭ ☢ € → ☎ ❄ ♫ ✂ ▷ ✇ ♎ ⇧ ☮ ⌘"  font fonts[index]
        # null height 10
        # vbox:
            # text u"Hyūga Hinata"
            # text u""
            # text u""
            # text u""
    
    # vbox:
        # spacing 5
        # xysize (config.screen_width, 700)
        # box_wrap True
        # for font in os.listdir(renpy.loader.transfn("fonts")):
            # $ path = "fonts/" + font
            # text ("{size=30}{font=[path]}%s" % font)
            
    hbox:
        align (0.5, 0.8)
        textbutton "<--" action SetScreenVariable("index", (index - 1) % len(fonts))
        null width 10
        textbutton "-->" action SetScreenVariable("index", (index + 1) % len(fonts))
        
    textbutton "Close":
        align (0.5, 1.0)
        action Hide("fonts"), Jump("mainscreen")
