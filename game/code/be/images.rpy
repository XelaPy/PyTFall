# Assets of the BE:
init -1: # Images and Animations
    transform crosshair_red():
        subpixel True
        anchor (.5, .5)
        zoom .5 alpha .9
        "content/gfx/interface/images/crosshair_red.webp"
        parallel:
            rotate 0
            linear 3.0 rotate 360
            repeat
        parallel:
            zoom .5
            easein .5 zoom .6
            easeout .5 zoom .5
            easein .5 zoom .4
            easeout .5 zoom .5
            repeat

    transform patreon_bounce():
        xoffset 0
        on hover:
            pause .1
            easein .4 xoffset 40
            easeout .3  xoffset 0
            easein .3 xoffset 25
            easeout .2  xoffset 0
            easein .1 xoffset 10
            easeout .1  xoffset 0
        on idle:
            linear .1 xoffset 0

    transform dark_death_color(w, h):
        Solid("#222222", xysize=(w, h))
        .1
        Solid("#111111", xysize=(w, h))
        .1
        repeat

    transform healing_effect_color(w, h):
        Solid("#8CD9B3", xysize=(w, h))
        .05
        Solid("#85E0B3", xysize=(w, h))
        .05
        Solid("#7DE8B3", xysize=(w, h))
        .05
        Solid("#75F0B3", xysize=(w, h))
        .05
        Solid("#7DE8B3", xysize=(w, h))
        .05
        Solid("#85E0B3", xysize=(w, h))
        .05
        repeat

    transform gray_shield(w, h):
        Solid("#B2B2B2", xysize=(w, h))

    transform green_shield(w, h):
        Solid("#5CD699", xysize=(w, h))

    transform fire_effect_color(w, h):
        Solid("#D98026", xysize=(w, h))
        .05
        Solid("#E68019", xysize=(w, h))
        .05
        Solid("#F2800D", xysize=(w, h))
        .05
        Solid("#FF8000", xysize=(w, h))
        .05
        Solid("#F2800D", xysize=(w, h))
        .05
        Solid("#E68019", xysize=(w, h))
        .05
        repeat

    transform poison_effect_color(w, h):
        Solid("#178217", xysize=(w, h))
        .05
        Solid("#0F8A0F", xysize=(w, h))
        .05
        Solid("#089108", xysize=(w, h))
        .05
        Solid("#009900", xysize=(w, h))
        .05
        Solid("#089108", xysize=(w, h))
        .05
        Solid("#0F8A0F", xysize=(w, h))
        .05
        repeat

    # To be moved to transforms file:
    transform multi_strike(d, offset, t, duration, af):
        # A Single instance of simple attack for the BE.
        pause t
        alpha 1.0
        d
        offset offset
        linear duration alpha af

    transform double_strike(d1, d2, d2_offset, delay):
        parallel:
            alpha 1.0
            d1
            pause .2
            linear .3 alpha .0
        parallel:
            pause delay
            alpha 1.0
            d2
            offset d2_offset
            pause .2
            linear .3 alpha .0

    transform triple_strike(d1, d2, d3, d2_offset, d3_offset, delay):
        parallel:
            alpha 1.0
            d1
            pause .2
            linear .3 alpha .0
        parallel:
            pause delay
            alpha 1.0
            d2
            offset d2_offset
            pause .2
            linear .3 alpha .0
        parallel:
            pause delay*2
            alpha 1.0
            d3
            offset d3_offset
            pause .2
            linear .3 alpha .0

    $ renpy.audio.music.register_channel("main_gfx_attacks", renpy.config.movie_mixer, loop=False, stop_on_mute=False, movie=True)

    # filmstrip for spray simple attack:
    image simple_spray_attack = Transform(FilmStrip("content/gfx/be/filmstrips/spray.webp", (192, 192), (5, 8), .03, loop=False), zoom=1.2)

    python:
        for i in xrange(1, 6):
            renpy.image("melee_%d" % i, FilmStrip("content/gfx/be/filmstrips/melee_%d.webp" % i, (192, 192), (5, 2), .05, loop=False))
    # Casting:
    python:
        # be_dark_mask = Transform(Movie(channel="main_gfx_bow", play="content/gfx/autowebm/be_dark_mask inf main_gfx_bow/movie.webm", mask="content/gfx/autowebm/be_dark_mask inf main_gfx_bow/mask.webm"), zoom=1.2, alpha=.8)
        for i in ["cast_dark_2", "cast_light_2", "cast_water_2", "cast_air_2", "cast_fire_2", "cast_earth_2", "cast_electricity_2", "cast_ice_2"]:
            renpy.image(i, FilmStrip("content/gfx/be/filmstrips/%s.webp" % i, (192, 192), (5, 4), .07, loop=False))
    image cast_default_1 = FilmStrip("content/gfx/be/filmstrips/cast_default_1.webp", (192, 192), (5, 3), .08, loop=False)
    image cast_runes_1 = FilmStrip("content/gfx/be/filmstrips/cast_runes_1.webp", (192, 192), (5, 1), .15, loop=False)

    ########### Magic:
    ########### Fire:
    image fire_1 = FilmStrip("content/gfx/be/filmstrips/fire_1.webp", (192, 192), (5, 4), .1, loop=False)
    image fire_2 = FilmStrip("content/gfx/be/filmstrips/fire_2.webp", (192, 192), (5, 4), .1, loop=False)
    image fire_3 = FilmStrip("content/gfx/be/filmstrips/fire_3.webp", (192, 192), (5, 7), .1, loop=False)
    image fire_4 = FilmStrip("content/gfx/be/filmstrips/fire_4.webp", (192, 192), (5, 10), .1, loop=False)
    image fire_mask = FilmStrip("content/gfx/be/filmstrips/fire_mask.webp", (240, 180), (5, 5), .05, loop=True)

    image fire_5_1:
        FilmStrip("content/gfx/be/filmstrips/fire_5_1.webp", (192, 192), (5, 4), .05, loop=False)
        zoom 2.0
        1.0
    image fire_5:
        FilmStrip("content/gfx/be/filmstrips/fire_5.webp", (192, 192), (5, 6), .05, loop=True)
        rotate 0
        linear 1.5 rotate 360
    image fire_6_1:
        FilmStrip("content/gfx/be/filmstrips/fire_6_1.webp", (192, 192), (5, 3), .08, loop=False)
        zoom 2.0
        1.2
    image fire_6:
        FilmStrip("content/gfx/be/filmstrips/fire_6.webp", (192, 192), (5, 6), .05, loop=True)
        rotate 0
        linear 1.5 rotate 360
    image cataclysm_sideways = FilmStrip("content/gfx/be/filmstrips/cataclysm_sideways.webp", (481, 453), (5, 4), .1, include_frames=range(17), loop=False)

    ########### Water:
    image water_1 = FilmStrip("content/gfx/be/filmstrips/water_1.webp", (192, 192), (5, 3), .1, loop=False)
    image water_2 = FilmStrip("content/gfx/be/filmstrips/water_2.webp", (192, 192), (5, 4), .1, loop=False)
    image water_3 = FilmStrip("content/gfx/be/filmstrips/water_3.webp", (192, 192), (5, 5), .1, loop=False)
    image water_4 = FilmStrip("content/gfx/be/filmstrips/water_4.webp", (192, 192), (5, 9), .05, loop=False)
    image water_5 = FilmStrip("content/gfx/be/filmstrips/water_5.webp", (192, 192), (5, 6), .1, loop=False)
    image water_6 = FilmStrip("content/gfx/be/filmstrips/water_6.webp", (192, 192), (5, 10), .1, loop=False)
    image rain = FilmStrip("content/gfx/be/filmstrips/rain.webp", (192, 192), (5, 10), .05, loop=True)
    image water_wave = FilmStrip("content/gfx/be/filmstrips/water_wave.webp", (531, 213), (3, 3), .15, include_frames=range(7), loop=False)

    transform water_combined(xz, xo):
        # It"s prolly a better design to work with the displayable directly using contains instead of replacing them with parallel...
        contains:
            "water_attack"
            xalign .5
            ypos 600
            yanchor 1.0

        contains:
            pause .6
            "water_wave"
            xalign .5
            ypos 650
            yanchor 1.0
            xzoom xz
            xoffset xo
            yzoom 1.8

    ########### Earth:
    image earth_1 = FilmStrip("content/gfx/be/filmstrips/earth_1.webp", (192, 192), (5, 4), .1, loop=False)
    image earth_2 = FilmStrip("content/gfx/be/filmstrips/earth_2.webp", (192, 192), (5, 2), .1, loop=False)
    image earth_3 = FilmStrip("content/gfx/be/filmstrips/earth_3.webp", (192, 192), (5, 3), .1, loop=False)
    image earth_4 = FilmStrip("content/gfx/be/filmstrips/earth_4.webp", (192, 192), (5, 2), .12, loop=False)
    image earth_6 = FilmStrip("content/gfx/be/filmstrips/earth_6.webp", (192, 192), (5, 4), .1, loop=False)
    image magma = FilmStrip("content/gfx/be/filmstrips/magma.webp", (192, 192), (5, 8), .08, loop=False)
    image crushing_hand = FilmStrip("content/gfx/be/filmstrips/crushing_hand.webp", (513, 297), (3, 6), .15, loop=False)

    ########### Air:
    image air_1 = FilmStrip("content/gfx/be/filmstrips/air_1.webp", (192, 192), (5, 5), .06, loop=False)
    image air_2 = FilmStrip("content/gfx/be/filmstrips/air_2.webp", (192, 192), (5, 5), .06, loop=False)
    image air_3 = FilmStrip("content/gfx/be/filmstrips/air_3.webp", (192, 192), (5, 5), .06, loop=False)
    image air_4 = FilmStrip("content/gfx/be/filmstrips/air_4.webp", (192, 192), (5, 6), .05, loop=False)
    image air_6 = FilmStrip("content/gfx/be/filmstrips/air_6.webp", (151, 151), (5, 7), .04, loop=False, reverse=True)
    image vortex = FilmStrip("content/gfx/be/filmstrips/vortex.webp", (277, 277), (15, 1), .1, loop=True)
    image tornado:
        FilmStrip("content/gfx/be/filmstrips/tornado.webp", (674, 592), (2, 3), .05, loop=True)
        anchor (.5, 1.0)
        zoom .5
        subpixel True
        easeout 1.5 zoom 1.3

        on hide:
            alpha 1.0
            linear .5 alpha 0

    ########### Light:
    image light_1 = FilmStrip("content/gfx/be/filmstrips/light_1.webp", (192, 192), (5, 5), .05, loop=False)
    image light_2 = FilmStrip("content/gfx/be/filmstrips/light_2.webp", (192, 192), (5, 5), .05, loop=False)
    image light_3 = FilmStrip("content/gfx/be/filmstrips/light_3.webp", (100, 100), (5, 16), .02, loop=False)
    image light_5 = FilmStrip("content/gfx/be/filmstrips/light_5.webp", (192, 192), (5, 5), .1, loop=False)
    image dawn = FilmStrip("content/gfx/be/filmstrips/dawn.webp", (192, 192), (5, 7), .1, loop=False)
    image holy_blast = FilmStrip("content/gfx/be/filmstrips/holy_blast_2x_bm.webp", (382, 336), (8, 5), .1, include_frames=range(36), loop=False)

    ########### Darkness:
    image darkness_1 = FilmStrip("content/gfx/be/filmstrips/darkness_1.webp", (192, 192), (5, 4), .05, loop=False)
    image darkness_2 = FilmStrip("content/gfx/be/filmstrips/darkness_2.webp", (192, 192), (5, 4), .08, loop=False)
    image darkness_3 = FilmStrip("content/gfx/be/filmstrips/darkness_3.webp", (192, 192), (5, 6), .05, loop=False)
    image darkness_4 = FilmStrip("content/gfx/be/filmstrips/darkness_4.webp", (192, 192), (5, 6), .05, loop=False)
    image darkness_5 = FilmStrip("content/gfx/be/filmstrips/darkness_5.webp", (375, 500), (4, 3), .1, loop=False)
    image darkness_6 = FilmStrip("content/gfx/be/filmstrips/darkness_6.webp", (192, 192), (5, 3), .1, loop=False)
    image darklight = FilmStrip("content/gfx/be/filmstrips/darklight.webp", (144, 192), (5, 4), .1, loop=False)
    image dominion = Transform(FilmStrip("content/gfx/be/filmstrips/dominion_bm.webp", (595, 354), (5, 5), .1, loop=False),
                                                      size=(config.screen_width, config.screen_height))

    ########### Ice:
    image ice_1 = FilmStrip("content/gfx/be/filmstrips/ice_1.webp", (192, 192), (5, 5), .08, loop=False)
    image ice_2 = FilmStrip("content/gfx/be/filmstrips/ice_2.webp", (192, 192), (5, 5), .07, loop=False)
    image ice_3 = FilmStrip("content/gfx/be/filmstrips/ice_3.webp", (192, 192), (5, 5), .05, loop=False)
    image ice_4 = FilmStrip("content/gfx/be/filmstrips/ice_4.webp", (192, 192), (5, 4), .04, loop=False)
    image ice_5 = FilmStrip("content/gfx/be/filmstrips/ice_5.webp", (192, 192), (5, 6), .07, loop=False)
    image ice_6 = FilmStrip("content/gfx/be/filmstrips/ice_6.webp", (192, 192), (5, 4), .06, loop=False)
    image ice_7 = FilmStrip("content/gfx/be/filmstrips/ice_7.webp", (192, 192), (5, 5), .08, loop=False, reverse=True)
    image ice_blast = FilmStrip("content/gfx/be/filmstrips/ice_blast.webp", (393, 508), (5, 5), .1, include_frames=range(22), loop=False)
    image ice_twin_explosion = FilmStrip("content/gfx/be/filmstrips/ice_twin_explosion.webp", (358, 312), (2, 4), .1, include_frames=range(7), loop=False)
    image ice_strike = FilmStrip("content/gfx/be/filmstrips/ice_strike.webp", (581, 511), (3, 4), .1, loop=False)
    transform ice_storm(pos):
        contains:
            "ice_strike"
            pos pos
            anchor (.5, 1.0)
            pause 1.2
            Null()
        contains:
            pause .6
            "ice_twin_explosion"
            pos pos
            anchor (.5, 1.0)
            offset (-120, -10)
            pause .7
            Null()
        contains:
            pause .8
            "ice_twin_explosion"
            pos pos
            anchor (.5, 1.0)
            offset (100, -60)
            pause .7
            Null()
        contains:
            pause .95
            "ice_twin_explosion"
            pos pos
            anchor (.5, 1.0)
            offset (60, -140)
            pause .7
            Null()
        contains:
            pause 1.0
            "ice_twin_explosion"
            pos pos
            anchor (.5, 1.0)
            offset (-60, -170)
            pause .7
            Null()
        contains:
            pause 1.0
            "ice_twin_explosion"
            pos pos
            anchor (.5, 1.0)
            offset (40, -80)
            pause .7
            Null()

    ########### Electricity:
    image electricity_1 = FilmStrip("content/gfx/be/filmstrips/electricity_1.webp", (192, 192), (5, 2), .1, loop=False)
    image electricity_2 = FilmStrip("content/gfx/be/filmstrips/electricity_2.webp", (192, 192), (5, 3), .08, loop=False)
    image electricity_3 = FilmStrip("content/gfx/be/filmstrips/electricity_3.webp", (192, 192), (5, 3), .09, loop=False)
    image electricity_4:
        FilmStrip("content/gfx/be/filmstrips/electricity_4.webp", (192, 192), (5, 3), .04, loop=False)
        zoom 1.5
    image electricity_5 = FilmStrip("content/gfx/be/filmstrips/electricity_5.webp", (192, 384), (5, 2), .08, loop=True)
    image electricity_6 = FilmStrip("content/gfx/be/filmstrips/electricity_6.webp", (192, 192), (5, 16), .04, loop=True)
    image ion:
        FilmStrip("content/gfx/be/filmstrips/ion.webp", (192, 192), (5, 9), .05, loop=True)
        zoom 3.0
    image ion_1:
        FilmStrip("content/gfx/be/filmstrips/ion_1.webp", (192, 192), (5, 5), .04, loop=True)
        rotate 0
        linear 1.0 rotate 360
    image thunder_storm_2 = FilmStrip("content/gfx/be/filmstrips/thunder_storm_2.webp", (354, 389), (4, 4), .1, loop=False)
    image moz_stretch:
        VBox(Transform("moz_webm", crop=(0, 0, 1199, 320)),
                  Transform("moz_webm", crop=(0, 320, 1199, 278), yzoom=2))
    ########### Poison:
    image poison_1 = FilmStrip("content/gfx/be/filmstrips/poison_1.webp", (192, 192), (5, 6), .05, loop=False)
    image poison_2 = FilmStrip("content/gfx/be/filmstrips/poison_2.webp", (192, 192), (5, 3), .1, loop=False)
    image poison_3 = FilmStrip("content/gfx/be/filmstrips/poison_3.webp", (192, 192), (5, 5), .1, loop=False)
    ########### Healing:
    image heal_1 = FilmStrip("content/gfx/be/filmstrips/heal_1.webp", (192, 192), (5, 6), .1, loop=False)
    image heal_2 = FilmStrip("content/gfx/be/filmstrips/heal_2.webp", (192, 192), (5, 5), .1, loop=False)
    image heal_3 = FilmStrip("content/gfx/be/filmstrips/heal_3.webp", (360, 360), (1, 42), .05, loop=False)
    image resurrection = FilmStrip("content/gfx/be/filmstrips/resurrection2x.webp", (288, 247), (5, 4), .1, loop=False)
    ########### Magic Shields:
    image shield_1 = FilmStrip("content/gfx/be/filmstrips/shield_1.webp", (192, 192), (5, 4), .05, loop=False)
    image shield_2:
        "content/gfx/be/solid_shield.webp"
        alpha 0
        linear .4 alpha .7
        block:
            linear .5 alpha .9
            linear .5 alpha .7
            repeat
    ########### Weapons-only attacks
    # fire bow:
    image Fire Arrow cast:
        "content/gfx/be/animations/flame_arrow/FlameArrow_1.webp"
        pause .06
        "content/gfx/be/animations/flame_arrow/FlameArrow_2.webp"
        pause .06
        "content/gfx/be/animations/flame_arrow/FlameArrow_3.webp"
        pause .06
        "content/gfx/be/animations/flame_arrow/FlameArrow_4.webp"
        pause .06
        "content/gfx/be/animations/flame_arrow/FlameArrow_5.webp"
        pause .06
        "content/gfx/be/animations/flame_arrow/FlameArrow_6.webp"
        pause .06
        "content/gfx/be/animations/flame_arrow/FlameArrow_7.webp"
        pause .06
        "content/gfx/be/animations/flame_arrow/FlameArrow_8.webp"
        pause .09
        "content/gfx/be/animations/flame_arrow/FlameArrow_9.webp"
        pause .09
        "content/gfx/be/animations/flame_arrow/FlameArrow_10.webp"
        pause .12
        "content/gfx/be/animations/flame_arrow/FlameArrow_11.webp"
        pause .12
        "content/gfx/be/animations/flame_arrow/FlameArrow_12.webp"
        pause .12
        "content/gfx/be/animations/flame_arrow/FlameArrow_13.webp"
        pause .12

    image Fire Arrow fly:
        "content/gfx/be/animations/flame_arrow/FlameArrow.webp"
        pause .3

    image Fire Arrow impact:
        "content/gfx/be/animations/flame_arrow/FlameArrow_I1.webp"
        pause .12
        "content/gfx/be/animations/flame_arrow/FlameArrow_I2.webp"
        pause .12
        "content/gfx/be/animations/flame_arrow/FlameArrow_I3.webp"
        pause .12
        "content/gfx/be/animations/flame_arrow/FlameArrow_I4.webp"
        pause .12
        "content/gfx/be/animations/flame_arrow/FlameArrow_I5.webp"
        pause .13
        "content/gfx/be/animations/flame_arrow/FlameArrow_I6.webp"
    # ice bow:
    image Ice Arrow cast:
        "content/gfx/be/animations/ice_arrow/Ice Arrow_1.webp"
        pause .09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_2.webp"
        pause .09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_3.webp"
        pause .09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_4.webp"
        pause .09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_5.webp"
        pause .09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_6.webp"
        pause .09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_7.webp"
        pause .06
        "content/gfx/be/animations/ice_arrow/Ice Arrow_8.webp"
        pause .12
        "content/gfx/be/animations/ice_arrow/Ice Arrow_9.webp"
        pause .12
        "content/gfx/be/animations/ice_arrow/Ice Arrow_10.webp"
        pause .12
        "content/gfx/be/animations/ice_arrow/Ice Arrow_11.webp"
        pause .12
        "content/gfx/be/animations/ice_arrow/Ice Arrow_12.webp"
        pause .12

    image Ice Arrow fly:
        "content/gfx/be/animations/ice_arrow/Ice Arrow.webp"
        pause .3

    image Ice Arrow impact:
        "content/gfx/be/animations/ice_arrow/IceArrow_I1.webp"
        pause .10
        "content/gfx/be/animations/ice_arrow/IceArrow_I2.webp"
        pause .10
        "content/gfx/be/animations/ice_arrow/IceArrow_I3.webp"
        pause .12
        "content/gfx/be/animations/ice_arrow/IceArrow_I4.webp"
        pause .12
        "content/gfx/be/animations/ice_arrow/IceArrow_I5.webp"
        pause .12
        "content/gfx/be/animations/ice_arrow/IceArrow_I6.webp"
        pause .12
        "content/gfx/be/animations/ice_arrow/IceArrow_I7.webp"
        pause .12
        "content/gfx/be/animations/ice_arrow/IceArrow_I8.webp"

    image ice_dagger = FilmStrip("content/gfx/be/filmstrips/ice_dagger.webp", (192, 192), (5, 3), .05, loop=False)
