label graveyard_town:
    $ gm.enter_location(goodtraits=["Undead", "Divine Creature", "Demonic Creature"], badtraits=["Elf", "Android", "Monster", "Human", "Furry"], curious_priority=False)
    
    if not "cemetery" in ilists.world_music:
        $ ilists.world_music["cemetery"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("cemetery")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["cemetery"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")
    

    python:
        # Build the actions
        if pytfall.world_actions.location("graveyard_town"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.finish()
            
    scene bg graveyard_town
    with dissolve
    show screen graveyard_town
    $ number=0
        
    while 1:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ gm.start_gm(result[1])
        if result[0] == 'control':
            $ renpy.hide_screen("graveyard_town")
            if result[1] == 'return':
                $ renpy.music.stop(channel="world")
                hide screen graveyard_town
                jump city
                
label show_dead_list:
    $ dead_list = list(i for i in chars.values() if i.location == "After Life") # list of dead characters
    if dead_list:
        $ random.shuffle(dead_list) # randomizing list every time the screen opens
        show screen cemetry_list_of_dead_chars (dead_list, number)
        with dissolve
        while 1:
            $ result = ui.interact()
    else:
        "You look around, but all tombstones are old and worn out. Nothing interesting."
        jump graveyard_town
        
label show_dead_list_without_shuffle:
    show screen cemetry_list_of_dead_chars (dead_list, number)
    while 1:
        $ result = ui.interact()

screen cemetry_list_of_dead_chars (dead_list, number): # the list should not be empty!
    on "show":
        action Hide("graveyard_town", dissolve)
    # on "hide":
        # action Show("graveyard_town", dissolve)
    frame:
        align (0.5, 0.5)
        xysize (234, 420)
        background Frame("content/gfx/frame/tombstone.png", 234, 420)
        vbox:
            align (0.54, 0.65)
            $ character = dead_list[number]
            if character.has_image('portrait', 'indifferent'):
                $ char_profile_img = character.show('portrait', 'indifferent', resize=(99, 99), cache=True)
            else:
                $ char_profile_img = character.show('portrait', 'happy', resize=(99, 99), cache=True, type="reduce")
            frame:
                background Frame("content/gfx/frame/MC_bg.png")
                add im.Sepia(char_profile_img) align .5, .5
                xalign 0.5
                xysize (102, 102)
            spacing 5
            frame:
                background Frame("content/gfx/frame/namebox3.png")
                xsize 160
                if len(character.name) <= 10:
                    text ([character.name]) xalign 0.5 style "stats_value_text" color silver
                else:
                    text ([character.name]) xalign 0.5 style "stats_value_text" color silver size 12
            frame:
                background Frame("content/gfx/frame/namebox3.png")
                xsize 160
                text ("[character.level] lvl") xalign 0.5 style "stats_value_text" color silver
                
    $ img = "content/gfx/interface/buttons/next.png"
    $ img1 = im.Flip("content/gfx/interface/buttons/next.png", horizontal=True)
    imagebutton:
        align (0.415, 0.62)
        idle (img1)
        hover (im.MatrixColor(img1, im.matrix.brightness(0.15)))
        action [Jump("cemetery_prev_char")]
    imagebutton:
        align (0.59, 0.62)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Jump("cemetery_next_char")]
        
    vbox:
        style_group "wood"
        align (0.9, 0.9)
        button:
            xysize (120, 40)
            yalign 0.5
            action [Hide("cemetry_list_of_dead_chars"), Jump("graveyard_town")]
            text "Exit" size 15
            
label cemetery_prev_char:
    if number > 0:
        $ number -= 1
    else:
        $ number = len(dead_list)-1
    jump show_dead_list_without_shuffle
        
label cemetery_next_char:
    if number < len(dead_list)-1:
        $ number += 1
    else:
        $ number = 0
    jump show_dead_list_without_shuffle
    
screen graveyard_town():

    use top_stripe(True)
    
    use location_actions("graveyard_town")
    
    $ img_cemetery = ProportionalScale("content/gfx/interface/icons/cemetery.png", 80, 80)
    $ img_mausoleum = ProportionalScale("content/gfx/interface/icons/mausoleum.png", 80, 80)
    imagebutton:
        pos(580, 220)
        idle (img_cemetery)
        hover (im.MatrixColor(img_cemetery, im.matrix.brightness(0.15)))
        action [Hide("graveyard_town"), Jump("show_dead_list")]
    imagebutton:
        pos(1090, 180)
        idle (img_mausoleum)
        hover (im.MatrixColor(img_mausoleum, im.matrix.brightness(0.15)))
        action [Hide("graveyard_town"), Jump("enter_dungeon")]

    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show('girlmeets', exclude=["swimsuit", "wildness", "beach", "pool", "urban", "stage", "onsen", "indoors", "indoor"], type="first_default",label_cache=True, resize=(300, 400)), return_value=['jump', entry])
