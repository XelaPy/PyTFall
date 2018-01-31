screen set_action_dropdown(char, pos=()):
    # Trying to create a drop down screen with choices of actions:
    zorder 3
    modal True

    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    # Get mouse coords:
    python:
        x, y = pos
        xval = 1.0 if x > config.screen_width/2 else .0
        yval = 1.0 if y > config.screen_height/2 else .0

    frame:
        style_prefix "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        has vbox

        if isinstance(char.location, UpgradableBuilding):
            # Jobs:
            $ jobs = char.location.get_valid_jobs(char)
            for i in jobs:
                textbutton "[i.id]":
                    # Without Equipping for the job!
                    action [Function(set_char_to_work, char, char.location, i), Hide("set_action_dropdown")]

        # Other buildings
        elif hasattr(char.location, "actions"):
            for entry in char.location.actions:
                if entry == "Guard":
                    if char.status not in ("slave", "various") and ("Warrior" in char.occupations or char.disposition <= 950):
                        textbutton "[entry]":
                            action [SetField(char, "action", entry), Function(equip_for, char, entry), Hide("set_action_dropdown")]
                elif entry == "Take Course":
                    textbutton "[entry]":
                        action [Hide("set_action_dropdown"), Hide("charslist"), Hide("char_profile"), # Hide the dropdown screen, the chars list and char profile screens
                                SetField(store, "char", char, True), # Ensure that the global var char is set to the current char
                                Jump("char_training")] # Jump to the training screen
                else:
                    textbutton "[entry]":
                            action [SetField(char, "action", entry), Function(equip_for, char, entry), If(char_is_training(char), true=Function(stop_training, char)), Hide("set_action_dropdown")]

        # Prevent none action in schools
        if not hasattr(char.location, "is_school") or not char.location.is_school:
            textbutton "None":
                action [SetField(char, "action", None), If(char_is_training(char), true=Function(stop_training, char)), Hide("set_action_dropdown")]

        textbutton "Rest":
            # TODO: Temporary way to set action to Rest, this needs to be rewritten completely.
            action [SetField(char, "action", Rest()), Hide("set_action_dropdown")]

        textbutton "Close":
            action [Hide("set_action_dropdown")]

    key "K_ESCAPE" action [Hide("set_action_dropdown")]

screen set_location_dropdown(char, pos=()):
    # Trying to create a drop down screen with choices of actions:
    zorder 3
    modal True

    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    # Get mouse coords:
    python:
        x, y = pos
        xval = 1.0 if x > config.screen_width/2 else .0
        yval = 1.0 if y > config.screen_height/2 else .0

    frame:
        style_prefix "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        has vbox
        # Updating to new code: *Ugly code atm, TODO: Fix IT!
        for building in hero.buildings:
            if isinstance(building, UpgradableBuilding):
                if char.action in building.jobs:
                    $ can_keep_action = True
                else:
                    $ can_keep_action = False
                if can_keep_action:
                    textbutton "[building.name]":
                        action [SelectedIf(char.location==building), If(char_is_training(char),
                                true=Function(stop_training, char)), Function(change_location, char, building),
                                Hide("set_location_dropdown")]
                else:
                    textbutton "[building.name]":
                        action [SelectedIf(char.location==building), SetField(char, "action", None),
                                If(char_is_training(char), true=Function(stop_training, char)),
                                Function(change_location, char, building),
                                Hide("set_location_dropdown")]

        textbutton "Home":
            action [If(char_is_training(char), true=Function(stop_training, char)), Function(change_location, char, char.home), Hide("set_location_dropdown")]

        textbutton "Close":
            action Hide("set_location_dropdown")

    key "K_ESCAPE" action Hide("set_location_dropdown")

screen set_home_dropdown(char, pos=()):
    # Trying to create a drop down screen with choices of actions:
    zorder 3
    modal True

    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    # Get mouse coords:
    python:
        x, y = pos
        xval = 1.0 if x > config.screen_width/2 else .0
        yval = 1.0 if y > config.screen_height/2 else .0

    default habitable_locations = [b for b in hero.buildings if (b.habitable and b.vacancies)] + [locations["Streets"]]

    frame:
        style_prefix "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        has vbox

        for loc in habitable_locations:
            textbutton "[loc]":
                selected char.home == loc
                action SetField(char, "home", loc), Hide("set_home_dropdown")
        # for building in hero.buildings:
        #     if isinstance(building, UpgradableBuilding) or building.habitable:
        #         textbutton "[building.name]":
        #             selected char.home == building
        #             action SetField(char, "home", building), Hide("set_home_dropdown")
        # textbutton "Streets":
        #     selected char.home == locations["Streets"]
        #     action SetField(char, "home", ), Hide("set_home_dropdown")
        textbutton "Close":
            action Hide("set_home_dropdown")

    key "K_ESCAPE" action Hide("set_home_dropdown")

screen char_rename(char=None):
    modal True
    zorder 1
    frame:
        if isinstance(char, Player):
            background Frame("content/gfx/frame/post_battle.png", 500, 400)
            xysize(500, 400)
        elif char.status != "slave":
            background Frame("content/gfx/frame/post_battle.png", 500, 300)
            xysize(500, 300)
        else:
            background Frame("content/gfx/frame/post_battle.png", 500, 500)
            xysize(500, 500)
        align (0.5, 0.5)
        vbox:
            style_prefix "wood"
            at fade_in_out()
            align (0.5, 0.5)
            spacing 10
            if isinstance(char, Player) or char.status == "slave":
                text "Name:" size 21 color goldenrod outlines [(2, "#3a3a3a", 0, 0)]
                button:
                    xysize (340, 60)
                    xalign 1.0
                    yalign 0.5
                    text "[char.name]" size 16 color goldenrod
                    action Return(["rename", "name"])
                    padding (10, 10)
            if not(isinstance(char, Player)): # it's weird to give a nickname to yourself. should be handled by ingame events
                text "Nickname:" size 21 color goldenrod outlines [(2, "#3a3a3a", 0, 0)]
                button:
                    xysize (340, 60)
                    xalign 1.0
                    yalign 0.5
                    if char.nickname != char.name:
                        text "[char.nickname]" size 16 color goldenrod
                    else:
                        text "None" size 16 color goldenrod
                    action Return(["rename", "nick"])
                    padding (10, 10)
            if isinstance(char, Player) or char.status == "slave":
                text "Full Name:" size 21 color goldenrod outlines [(2, "#3a3a3a", 0, 0)]
                button:
                    xysize (340, 60)
                    xalign 1.0
                    yalign 0.5
                    text "[char.fullname]" size 16 color goldenrod
                    action Return(["rename", "full"])
                    padding (10, 10)

            null height 20
            button:
                xysize (100, 50)
                xalign 0.5
                yalign 0.5
                text "Back" size 16 color goldenrod
                action Hide("char_rename")
                padding (10, 10)

    key "K_ESCAPE" action Hide("char_rename")

screen character_pick_screen(): # screen to select someone from the MC team
    key "mousedown_3" action Return(False)
    frame:
        align (.5, .5)
        xsize 450
        ysize 310
        padding(2, 2)
        background Frame("content/gfx/frame/frame_dec_1.png")
        label "Select a character" align (0.5, 0.08) text_color "#DAA520" text_size 18
        hbox:
            spacing 45
            align (.5, .4)
            for l in hero.team:
                $ char_profile_img = l.show('portrait', resize=(101, 101), cache=True)
                $ img = "content/gfx/frame/ink_box.png"
                vbox:
                    spacing 1
                    xsize 102
                    imagebutton:
                        xalign .5
                        background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                        idle (char_profile_img)
                        hover (im.MatrixColor(char_profile_img, im.matrix.brightness(0.15)))
                        action Return(l)
                        xysize (102, 102)
                    bar:
                        xalign .5
                        right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                        left_bar im.Scale("content/gfx/interface/bars/hp2.png", 102, 14)
                        value l.health
                        range l.get_max("health")
                        thumb None
                        left_gutter 0
                        right_gutter 0
                        xysize (102, 14)
                    bar:
                        xalign .5
                        right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                        left_bar im.Scale("content/gfx/interface/bars/mp2.png", 102, 14)
                        value l.mp
                        range l.get_max("mp")
                        thumb None
                        left_gutter 0
                        right_gutter 0
                        xysize (102, 14)
                    bar:
                        xalign .5
                        right_bar im.Scale("content/gfx/interface/bars/empty_bar2.png", 102, 14)
                        left_bar im.Scale("content/gfx/interface/bars/vitality2.png", 102, 14)
                        value l.vitality
                        range l.get_max("vitality")
                        thumb None
                        left_gutter 0
                        right_gutter 0
                        xysize (102, 14)
                    frame:
                        xalign .5
                        xsize 102
                        ysize 30
                        padding(2, 2)
                        background Frame("content/gfx/frame/gm_frame.png")
                        $ name = l.name[:8]
                        label "[name]" align (0.5, 0.5) text_color "#DAA520" text_size 16

        vbox:
            style_group "wood"
            align (.5, 0.9)
            button:
                xysize (102, 40)
                yalign 0.5
                action Return(False)
                text "Cancel" size 15 color goldenrod
