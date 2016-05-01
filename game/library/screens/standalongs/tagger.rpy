# Tagger
label tagger:
    call load_json_tags from _call_load_json_tags
    python:
        alltags = list(sorted(tags_dict.values()))
        all_char = {k:v for k, v in chars.iteritems() if v.__class__ == Char}
        # Broken code? TODO: But this module is not likely to be used ever again.
        all_chars.update(rchar)
        pic = None
        if not hasattr(store, "tagchar"):
            tagchar = choice(all_chars.values())
        images = tagdb.get_imgset_with_tag(tagchar.id)
        images = list(images)
        images.sort()
        images = [images[i:i+40] for i in range(0, len(images), 40)]
        imagespage = 0
        tagz = set()
        oldtagz = set()
        
    python:
        renpy.show_screen("tagger")
        renpy.with_statement(dissolve)
        
    python:    
        while 1:
            result = ui.interact()
            if not isinstance(result, list):
                continue
            if result[0] == "update_pic":
                # Update Database
                if pic and tagz != oldtagz:
                    oldtagz = oldtagz - tagz
                    for tag in oldtagz:
                        tagdb.tagmap[tag].remove(pic)
                    for tag in tagz:
                        tagdb.tagmap[tag].add(pic)
                tagz = tagdb.get_tags_per_path(result[1])
                oldtagz = tagz.copy()
                pic = result[1]
                
            if result[0] == "tagchar":
                if result[1] == "show":
                    renpy.show_screen("pick_tagchar", renpy.get_mouse_pos())
                if result[1] == "pick":
                    if renpy.call_screen("yesno_prompt", message="Did you save your tagging?", yes_action=Return(True), no_action=Return(False)):
                        pic = None
                        tagchar = result[2]
                        images = tagdb.get_imgset_with_tag(tagchar.id)
                        images = list(images)
                        images.sort()
                        images = [images[i:i+40] for i in range(0, len(images), 40)]
                        imagespage = 0
                        
            if result[0] == "images":
                if result[1] == "next":
                    try:
                        imagespage = (imagespage + 1) % len(images)
                    except ZeroDevisionError:
                        pass
                elif result[1] == "previous":
                    try:
                        imagespage = (imagespage - 1) % len(images)
                    except ZeroDevisionError:
                        pass
                    
            if result[0] == "tags":
                if result[1] == "json_to_fn":
                    if renpy.call_screen("yesno_prompt", message="This will convert any loaded json tags into filenames!\n\n Are you Sure?", yes_action=Return(True), no_action=Return(False)):
                        if renpy.call_screen("yesno_prompt", message="This process can take quite a while!\n\nDo not turn your PC off and be sure to back your old packs up!\n\n Are you Sure?", yes_action=Return(True), no_action=Return(False)):
                            renpy.call("convert_json_to_filenames")
                if result[1] == "write_to_fn":
                    if renpy.call_screen("yesno_prompt", message="This will write all tags to filenames!\n\n Are you Sure?", yes_action=Return(True), no_action=Return(False)):
                        nums = "".join(list(str(i) for i in range(10)))
                        pool = list("".join([string.ascii_lowercase, nums]))
                        inverted = {v:k for k, v in tags_dict.iteritems()}
                        # Carefully! We write a script to rename the image files...
                        alltagz = set(tags_dict.values())
                        for img in tagdb.get_imgset_with_tag(tagchar.id):
                            # Normalize the path:
                            f = normalize_path("".join([gamedir, "/", img]))
                            # Gets the tags:
                            tags = list(alltagz & tagdb.get_tags_per_path(img))
                            if not tags:
                                devlog.warning("Found no tags for image during renaming: %s" % f)
                                continue
                            tags.sort()
                            tags = list(inverted[tag] for tag in tags)
                            # New filename string:
                            fn = "".join(["-".join(tags), "-", "".join(list(choice(pool) for i in range(4)))])
                            if img.endswith(".png"):
                                fn = fn + ".png"
                            elif img.endswith(".jpg"):
                                fn = fn + ".jpg"
                            elif img.endswith(".jpeg"):
                                fn = fn + ".jpeg"
                            elif img.endswith(".gif"):
                                fn = fn + ".gif"
                            oldfilename = f.split(os.sep)[-1]
                            if oldfilename.split("-")[:-1] == fn.split("-")[:-1]:
                                continue
                            else:    
                                newdir = f.replace(oldfilename, fn)
                                os.rename(f, newdir)
                        del alltagz
                        del nums
                        del inverted
                        renpy.show_screen("message_screen", "Please check devlog.txt for any errors during the process!!")  
            if result[0] == "control":
                if result[1] == "return":
                    break
                
    hide screen tagger
    with dissolve
    jump mainscreen
    
screen pick_tagchar(pos=()):
    zorder 3
    modal True
    
    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()
    
    python:
        x, y = pos
        if x > 1000:
            xval = 1.0
        else:
            xval = 0.0
        if y > 500:
            yval = 1.0
        else:
            yval = 0.0
    frame:
        style_group "dropdown"
        xysize (1100, 700)
        pos (x, y)
        anchor (xval, yval)
        vbox:
            box_wrap True
            # text "Equip For:" style "black_serpent"
            null height 5
            for g in all_chars.values():
                textbutton "{size=10}[g.id]":
                    xsize 100
                    action [Hide("pick_tagchar"), Return(["tagchar", "pick", g])]
        textbutton "Close":
            align (0.5, 1.0)
            action Hide("pick_tagchar")

screen tagger():
    # on "show" action Hide("debugTools")
    # on "hide" action Show("debugTools")
    
    # images:
    hbox:
        xysize (150, 45)
        xfill True
        pos(0, 0)
        $ img = im.Scale("content/gfx/interface/buttons/blue_arrow_left.png", 40, 40)
        imagebutton:
            align (0, 0.5)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
            action Return(['images', 'previous'])
        text "[imagespage]" style "agrevue" color blue align (0.5, 0.5)
        $ img = im.Scale("content/gfx/interface/buttons/blue_arrow_right.png", 40, 40)
        imagebutton:
            align (1.0, 0.5)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
            action Return(['images', 'next'])
    frame:
        pos(0, 40)
        xysize (145, config.screen_height)
        viewport:
            vbox:
                ysize 750
                box_wrap True
                if images:
                    for img in images[imagespage]:
                        if "/" in img:
                            $ fn = img.split("/")[-1]
                        else:
                            $ fn = img.split("\\")[-1]
                        button:
                            ysize(18)
                            idle_background Text("%s" % fn, size=15)
                            background Text("%s" % fn, size=15, color=red)
                            #button_text
                           # text ["{size=15}[fn]"]
                        #textbutton "{size=15}[fn]":
                            action If(img==pic, false=Return(["update_pic", img]))
        
    # Tagz:
    vbox:
        ysize config.screen_height
        box_wrap True
        pos (155, 0)
        for tag in alltags:
            if tag in tagz:
                textbutton "{color=[red]}[tag]":
                    style "white_cry_button"
                    action Function(tagz.remove, tag)
            else:
                textbutton "[tag]":
                    style "white_cry_button"
                    action Function(tagz.add, tag)
        
    # Picture:
    if pic:
        add ProportionalScale(pic, 500, 500) align(1.0, 0)
        
    # Controls:
    vbox:
        align (1.0, 1.0)
        textbutton "Tag filenames!":
            action Return(["tags", "write_to_fn"])
        textbutton "Pick Char":
            action Return(["tagchar", "show"])
        textbutton "{color=[red]}JSON --> FN":
            action Return(["tags", "json_to_fn"])
    use exit_button
        
    
        
