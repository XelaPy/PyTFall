label realtor_agency:

    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5

    hide screen main_street

    scene bg realtor_agency
    with dissolve

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")

    $ g = Character("{color=[rosybrown]}Rose", color=rosybrown, show_two_window=True)

    if not global_flags.has_flag("visited_ra"):

        $ nvl_ra = Character(None, kind=nvl)
        nvl_ra "After entering the real-estate office the first thing that hit you was the brightness."
        nvl_ra "It was far brighter then the outside world. Your eyes quickly adapted and you noticed the source of the light."
        nvl_ra "This medium size room, without windows, probably was a part of a bigger apartment, have been highly illuminated with a large chandelier, hanging from the ceiling over the central part of the room and a standing lamp near the desk."
        nvl_ra "On the left side, there were two couches opposing each other separated with a coffee table."
        extend " On the right side, there was a cupboard and a door that probably leading further inside the house."
        nvl_ra "In the middle, under the chandelier was standing a desk with a single chair. There were also multiple painting hanging on the walls."
        nvl_ra "But that all have been showed into the background when you noticed the owner."
        nvl_ra "She was a mature type woman with glasses, that surely wasn't ashamed of her female attributes."
        nvl_ra "Blouse and skirt that she wore was well fitted, and stick really tightly to her body emphasizing her breasts and hips."
        nvl_ra "The black stockings that she was wearing also matched her perfectly, underlining her beautiful legs. The finishing touch was her shoes with little, cute roses on the toes, that you almost didn't notice."

        show npc rose at right with dissolve

        g "Welcome to Rose Real Estates."
        extend " My name is Rose. I'm the owner and the realtor."
        g "Please have a seat and take a look at some of our offers."

        $ global_flags.set_flag("visited_ra")

    else:
        "Room is still bright and filled with the same sweet scent."
        show npc rose


    # Added the next three lines to disable this feature without crashing the game   --fenec250

    $ market_buildings = sorted(set(chain(businesses.values(), buildings.values())) - set(hero.buildings), key = lambda x: x.id)
    $ focus = None

    show screen realtor_agency
    with fade

    while 1:

        $ result = ui.interact()

        if result[0] == 'buy':
            if hero.take_ap(1):
                if hero.take_money(result[1].price, reason="Property"):
                    $ renpy.play("content/sfx/sound/world/purchase_1.ogg")
                    $ hero.add_building(result[1])
                    $ market_buildings.remove(result[1])
                    $ focus = None
                else:
                    $ renpy.call_screen('message_screen', "You don't have enough Gold!!")
            else:
                $ renpy.call_screen('message_screen', "You don't have enough AP left for this action!!")

        if result[0] == 'control':
            if result[1] == 'return':
                jump realtor_exit

label realtor_exit:
    $ renpy.music.stop(channel="world")
    hide screen realtor_agency
    jump city


screen realtor_agency():
    modal True
    zorder 1


    default tt = Tooltip("Please take a look at some of our offers!")

    if market_buildings:
        frame:
            style_group "content"
            background Frame("content/gfx/frame/p_frame53.png", 10, 10)
            xalign 0.997
            ypos 42
            xysize (420, 675)
            side "c r":
                viewport id "brothelmarket_vp":
                    xysize (410, 645)
                    draggable True
                    mousewheel True
                    has vbox
                    for building in market_buildings:
                        vbox:
                            xfill True
                            xysize (395, 320)
                            frame:
                                background Frame (Transform("content/gfx/frame/MC_bg3.png", alpha=0.6), 5, 5)
                                xysize (395, 320)
                                null height 15
                                vbox:
                                    xalign 0.5
                                    null height 5
                                    frame:
                                        style_group "content"
                                        xalign 0.5
                                        xysize (340, 50)
                                        background Frame("content/gfx/frame/p_frame5.png", 10, 10)
                                        label (u"[building.name]") text_size 23 text_color ivory align(0.5, 0.5)
                                    null height 5
                                    frame:
                                        background Frame("content/gfx/frame/mes11.jpg", 5, 5)
                                        xpadding 5
                                        ypadding 5
                                        xalign 0.5
                                        $ img = ProportionalScale(building.img, 300, 220)
                                        imagebutton:
                                            idle (img)
                                            hover (im.MatrixColor(img, im.matrix.brightness(0.25)))
                                            action SetVariable("focus", building)
                vbar value YScrollValue("brothelmarket_vp")

    if focus:
        frame:
            style_group "content"
            background Frame("content/gfx/frame/p_frame53.png", 10, 10)
            xalign 0.003
            ypos 42
            xysize (420, 675)
            side "c l":
                viewport id "info_vp":
                    xysize (410, 645)
                    draggable True
                    mousewheel True
                    vbox:
                        xsize 400
                        xfill True
                        null height 50
                        frame:
                            style_group "content"
                            xalign 0.5
                            xysize (350, 60)
                            background Frame("content/gfx/frame/namebox5.png", 10, 10)
                            label (u"[focus.name]") text_size 23 text_color ivory align(0.5, 0.8)
                        null height 50
                        hbox:
                            style_group "proper_stats"
                            frame:
                                xpadding 12
                                ypadding 12
                                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=0.98), 10, 10)
                                vbox:
                                    spacing -1
                                    frame:
                                        xysize 380, 24
                                        text "{color=[gold]}Price:" yalign 0.5
                                        label (u"{color=[gold]}%d"%(focus.price)) align (1.0, 0.5)
                                    frame:
                                        xysize 380, 24
                                        text "Rooms:" yalign 0.5
                                        label (u"{color=[ivory]}%s/%s" % (focus.rooms, focus.maxrooms)) align (1.0, 0.5)
                                    if isinstance(focus, FamousBuilding):
                                        frame:
                                            xysize 380, 24
                                            text "Fame:" yalign 0.5
                                            label (u"%s/%s" % (focus.fame, focus.maxfame)) align (1.0, 0.5)
                                        frame:
                                            xysize 380, 24
                                            text "Reputation:" yalign 0.5
                                            label (u"%s/%s" % (focus.rep, focus.maxrep)) align (1.0, 0.5)

                                    if isinstance(focus, Building):
                                        frame:
                                            xysize 380, 24
                                            text "Max Rank:" yalign 0.5
                                            label (u"%s" % (focus.maxrank)) align (1.0, 0.5)

                        null height 50

                        frame:
                            background Frame("content/gfx/frame/ink_box.png", 10, 10)
                            xalign 0.5
                            xysize (400, 100)
                            xpadding 10
                            ypadding 10
                            text ("{=content_text}{color=[ivory]}[focus.desc]")

                        null height 100

                        button:
                            xalign 0.5
                            style "blue1"
                            xpadding 15
                            ypadding 10
                            text "Buy" align (0.5, 0.5) style "black_serpent" color ivory hover_color red
                            action Return(['buy', focus])
    use top_stripe(True)
