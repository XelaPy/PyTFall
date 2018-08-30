label graveyard_town:
    python:
        gm.enter_location(goodtraits=["Undead", "Divine Creature", "Demonic Creature"],
                          badtraits=["Elf", "Android", "Monster", "Human", "Furry"],
                          curious_priority=False)
    $ coords = [[.1, .55], [.5, .84], [.92, .45]]

    if not "cemetery" in ilists.world_music:
        $ ilists.world_music["cemetery"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("cemetery")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["cemetery"]) fadein .5

    $ global_flags.del_flag("keep_playing_music")

    python:
        # Build the actions
        if pytfall.world_actions.location("graveyard_town"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.finish()

    $ dungeon_access = day >= global_flags.get_flag("can_access_cemetery_dungeon", 0)

    scene bg graveyard_town
    with dissolve
    show screen graveyard_town
    $ number = 0

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
    $ dead_list = list(locations["After Life"].inhabitants) # list of dead characters
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

screen cemetry_list_of_dead_chars(dead_list, number): # the list should not be empty!
    on "show":
        action Hide("graveyard_town", dissolve)
    # on "hide":
        # action Show("graveyard_town", dissolve)

    frame:
        align (.5, .5)
        xysize (234, 420)
        background Frame("content/gfx/frame/tombstone.png", 234, 420)
        vbox:
            align (.54, .65)
            $ character = dead_list[number]

            if character.has_image('portrait', 'indifferent'):
                $ char_profile_img = character.show('portrait', 'indifferent', resize=(99, 99), cache=True)
            else:
                $ char_profile_img = character.show('portrait', 'happy', resize=(99, 99), cache=True, type="reduce")

            frame:
                background Frame("content/gfx/frame/MC_bg.png")
                add im.Sepia(char_profile_img) align .5, .5
                xalign .5
                xysize (102, 102)

            spacing 5

            frame:
                background Frame("content/gfx/frame/namebox3.png")
                xsize 160
                if len(character.name) <= 10:
                    text ([character.name]) xalign .5 style "stats_value_text" color silver
                else:
                    text ([character.name]) xalign .5 style "stats_value_text" color silver size 12

            frame:
                background Frame("content/gfx/frame/namebox3.png")
                xsize 160
                text ("[character.level] lvl") xalign .5 style "stats_value_text" color silver

    $ img = "content/gfx/interface/buttons/next.png"
    $ img1 = im.Flip("content/gfx/interface/buttons/next.png", horizontal=True)

    imagebutton:
        align (.415, .62)
        idle (img1)
        hover (im.MatrixColor(img1, im.matrix.brightness(.15)))
        action [Jump("cemetery_prev_char")]

    imagebutton:
        align (.59, .62)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(.15)))
        action [Jump("cemetery_next_char")]

    vbox:
        style_group "wood"
        align (.9, .9)
        button:
            xysize (120, 40)
            yalign .5
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

    if not gm.show_girls:
        $ img_cemetery = ProportionalScale("content/gfx/interface/icons/cemetery.png", 80, 80)
        $ img_mausoleum = ProportionalScale("content/gfx/interface/icons/mausoleum.png", 80, 80)
        imagebutton:
            pos(580, 220)
            idle (img_cemetery)
            hover (im.MatrixColor(img_cemetery, im.matrix.brightness(.15)))
            action [Hide("graveyard_town"), Jump("show_dead_list")]
            tooltip "Graves"
        imagebutton:
            pos(1090, 180)
            idle (img_mausoleum)
            hover (im.MatrixColor(img_mausoleum, im.matrix.brightness(.15)))
            if dungeon_access:
                tooltip "Dungeon\nBeware all who enter here"
                action [Hide("graveyard_town"), Jump("enter_dungeon")]
            else:
                if global_flags.flag("can_access_cemetery_dungeon")-day >= 2:
                    tooltip "You may re-enter in {} days.".format(global_flags.flag("can_access_cemetery_dungeon")-day)
                else:
                    tooltip "You may re-enter tomorrow."
                action NullAction()

    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")
        add "content/gfx/images/bg_gradient.png" yalign .45
        for j, entry in enumerate(gm.display_girls()):
            hbox:
                align (coords[j])
                use rg_lightbutton(img=entry.show('girlmeets',
                        exclude=["swimsuit", "wildness",
                                 "beach", "pool", "urban", "stage",
                                 "onsen", "indoors", "indoor"],
                                 type="first_default", label_cache=True,
                                 resize=(300, 400)),
                                 return_value=['jump', entry])
