# Assets of the BE:
init -1: # Images and Animations
    # Test of an alternative damge overlay concept:
    transform dark_death_color(w, h):
        Solid("#222222", xysize=(w, h))
        0.1
        Solid("#111111", xysize=(w, h))
        0.1
        repeat

    transform healing_effect_color(w, h):
        Solid("#8CD9B3", xysize=(w, h))
        0.05
        Solid("#85E0B3", xysize=(w, h))
        0.05
        Solid("#7DE8B3", xysize=(w, h))
        0.05
        Solid("#75F0B3", xysize=(w, h))
        0.05
        Solid("#7DE8B3", xysize=(w, h))
        0.05
        Solid("#85E0B3", xysize=(w, h))
        0.05
        repeat

    transform gray_shield(w, h):
        Solid("#B2B2B2", xysize=(w, h))

    transform green_shield(w, h):
        Solid("#5CD699", xysize=(w, h))

    transform fire_effect_color(w, h):
        Solid("#D98026", xysize=(w, h))
        0.05
        Solid("#E68019", xysize=(w, h))
        0.05
        Solid("#F2800D", xysize=(w, h))
        0.05
        Solid("#FF8000", xysize=(w, h))
        0.05
        Solid("#F2800D", xysize=(w, h))
        0.05
        Solid("#E68019", xysize=(w, h))
        0.05
        repeat

    transform poison_effect_color(w, h):
        Solid("#178217", xysize=(w, h))
        0.05
        Solid("#0F8A0F", xysize=(w, h))
        0.05
        Solid("#089108", xysize=(w, h))
        0.05
        Solid("#009900", xysize=(w, h))
        0.05
        Solid("#089108", xysize=(w, h))
        0.05
        Solid("#0F8A0F", xysize=(w, h))
        0.05
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

    # simplest single weapon attacks; after certain BE changes they require these simple alts to gradually disappear
    image simple_sword_attack:
        ProportionalScale("content/gfx/be/swords.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_bow_attack:
        ProportionalScale("content/gfx/be/bows.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_crossbow_attack:
        ProportionalScale("content/gfx/be/crossbows.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_dagger_attack:
        ProportionalScale("content/gfx/be/knives.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_claw_attack:
        ProportionalScale("content/gfx/be/claws.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_fist_attack:
        ProportionalScale("content/gfx/be/fists.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_cannon_attack:
        ProportionalScale("content/gfx/be/cannons.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_blunt_attack:
        ProportionalScale("content/gfx/be/rods.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_axe_attack:
        ProportionalScale("content/gfx/be/axes.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_bite_attack:
        ProportionalScale("content/gfx/be/bites.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_gun_attack:
        ProportionalScale("content/gfx/be/shoots.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_scythe_attack:
        ProportionalScale("content/gfx/be/scythe.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_spray_attack:
        ProportionalScale("content/gfx/be/spray.png", 150, 150)
        alpha 1.0
        linear 1.0 alpha 0

    image simple_throw_attack:
        ProportionalScale("content/gfx/be/throw.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    image simple_whip_attack:
        ProportionalScale("content/gfx/be/whip.png", 150, 150)
        alpha 1.0
        linear 0.5 alpha 0

    python:
        for i in xrange(1, 6):
            renpy.image("melee_%d" % i, FilmStrip("content/gfx/be/filmstrips/melee_%d.png" % i, (192, 192), (5, 2), 0.05, loop=False))
    # Casting:
    python:
        # be_dark_mask = Transform(Movie(channel="main_gfx_bow", play="content/gfx/autowebm/be_dark_mask inf main_gfx_bow/movie.webm", mask="content/gfx/autowebm/be_dark_mask inf main_gfx_bow/mask.webm"), zoom=1.2, alpha=0.8)
        for i in ["cast_dark_2", "cast_light_2", "cast_water_2", "cast_air_2", "cast_fire_2", "cast_earth_2", "cast_electricity_2", "cast_ice_2"]:
            renpy.image(i, FilmStrip("content/gfx/be/filmstrips/%s.png" % i, (192, 192), (5, 4), 0.07, loop=False))
    image cast_default_1 = FilmStrip("content/gfx/be/filmstrips/cast_default_1.png", (192, 192), (5, 3), 0.08, loop=False)
    image cast_runes_1 = FilmStrip("content/gfx/be/filmstrips/cast_runes_1.png", (192, 192), (5, 1), 0.15, loop=False)

    ########### Magic:
    ########### Fire:
    image fire_1 = FilmStrip("content/gfx/be/filmstrips/fire_1.png", (192, 192), (5, 4), 0.1, loop=False)
    image fire_2 = FilmStrip("content/gfx/be/filmstrips/fire_2.png", (192, 192), (5, 4), 0.1, loop=False)
    image fire_3 = FilmStrip("content/gfx/be/filmstrips/fire_3.png", (192, 192), (5, 7), 0.1, loop=False)
    image fire_4 = FilmStrip("content/gfx/be/filmstrips/fire_4.png", (192, 192), (5, 10), 0.1, loop=False)
    image fire_mask = FilmStrip("content/gfx/be/filmstrips/fire_mask.jpg", (240, 180), (5, 5), 0.05, loop=True)
    image flame_bm = FilmStrip("content/gfx/be/filmstrips/fire_mask_bm.png", (240, 180), (5, 5), 0.05, loop=True)

    image fire_5_1:
        FilmStrip("content/gfx/be/filmstrips/fire_5_1.png", (192, 192), (5, 4), 0.05, loop=False)
        zoom 2.0
        1.0
    image fire_5:
        FilmStrip("content/gfx/be/filmstrips/fire_5.png", (192, 192), (5, 6), 0.05, loop=True)
        rotate 0
        linear 1.5 rotate 360
    image fire_6_1:
        FilmStrip("content/gfx/be/filmstrips/fire_6_1.png", (192, 192), (5, 3), 0.08, loop=False)
        zoom 2.0
        1.2
    image fire_6:
        FilmStrip("content/gfx/be/filmstrips/fire_6.png", (192, 192), (5, 6), 0.05, loop=True)
        rotate 0
        linear 1.5 rotate 360
    image cataclysm_sideways = FilmStrip("content/gfx/be/filmstrips/cataclysm_sideways.png", (481, 453), (5, 4), 0.1, include_frames=range(17), loop=False)

    ########### Water:
    image water_1 = FilmStrip("content/gfx/be/filmstrips/water_1.png", (192, 192), (5, 3), 0.1, loop=False)
    image water_2 = FilmStrip("content/gfx/be/filmstrips/water_2.png", (192, 192), (5, 4), 0.1, loop=False)
    image water_3 = FilmStrip("content/gfx/be/filmstrips/water_3.png", (192, 192), (5, 5), 0.1, loop=False)
    image water_4 = FilmStrip("content/gfx/be/filmstrips/water_4.png", (192, 192), (5, 9), 0.05, loop=False)
    image water_5 = FilmStrip("content/gfx/be/filmstrips/water_5.png", (192, 192), (5, 6), 0.1, loop=False)
    image water_6 = FilmStrip("content/gfx/be/filmstrips/water_6.png", (192, 192), (5, 10), 0.1, loop=False)
    image rain = FilmStrip("content/gfx/be/filmstrips/rain.png", (192, 192), (5, 10), 0.05, loop=True)
    image water_wave = FilmStrip("content/gfx/be/filmstrips/water_wave.png", (531, 213), (3, 3), 0.15, include_frames=range(7), loop=False)
    image water_attack:
        "content/gfx/be/animations/water_attack/00.png"
        pause 0.1
        "content/gfx/be/animations/water_attack/01.png"
        pause 0.1
        "content/gfx/be/animations/water_attack/02.png"
        pause 0.1
        "content/gfx/be/animations/water_attack/03.png"
        pause 0.1
        "content/gfx/be/animations/water_attack/04.png"
        pause 0.1
        "content/gfx/be/animations/water_attack/05.png"
        pause 0.1
        "content/gfx/be/animations/water_attack/06.png"
        pause 0.1
        "content/gfx/be/animations/water_attack/07.png"
        pause 0.1
        "content/gfx/be/animations/water_attack/08.png"
        pause 0.1
        Null()

    transform water_combined(xz, xo):
        # It"s prolly a better design to work with the displayable directly using contains instead of replacing them with parallel...
        contains:
            "water_attack"
            xalign 0.5
            ypos 600
            yanchor 1.0

        contains:
            pause 0.6
            "water_wave"
            xalign 0.5
            ypos 650
            yanchor 1.0
            xzoom xz
            xoffset xo
            yzoom 1.8

    ########### Earth:
    image earth_1 = FilmStrip("content/gfx/be/filmstrips/earth_1.png", (192, 192), (5, 4), 0.1, loop=False)
    image earth_2 = FilmStrip("content/gfx/be/filmstrips/earth_2.png", (192, 192), (5, 2), 0.1, loop=False)
    image earth_3 = FilmStrip("content/gfx/be/filmstrips/earth_3.png", (192, 192), (5, 3), 0.1, loop=False)
    image earth_4 = FilmStrip("content/gfx/be/filmstrips/earth_4.png", (192, 192), (5, 2), 0.12, loop=False)
    image earth_6 = FilmStrip("content/gfx/be/filmstrips/earth_6.png", (192, 192), (5, 4), 0.1, loop=False)
    image magma = FilmStrip("content/gfx/be/filmstrips/magma.png", (192, 192), (5, 8), 0.08, loop=False)
    image crushing_hand = FilmStrip("content/gfx/be/filmstrips/crushing_hand.png", (513, 297), (3, 6), 0.15, loop=False)

    ########### Air:
    image air_1 = FilmStrip("content/gfx/be/filmstrips/air_1.png", (192, 192), (5, 5), 0.06, loop=False)
    image air_2 = FilmStrip("content/gfx/be/filmstrips/air_2.png", (192, 192), (5, 5), 0.06, loop=False)
    image air_3 = FilmStrip("content/gfx/be/filmstrips/air_3.png", (192, 192), (5, 5), 0.06, loop=False)
    image air_4 = FilmStrip("content/gfx/be/filmstrips/air_4.png", (192, 192), (5, 6), 0.05, loop=False)
    image air_6 = FilmStrip("content/gfx/be/filmstrips/air_6.png", (151, 151), (5, 7), 0.04, loop=False, reverse=True)
    image vortex = FilmStrip("content/gfx/be/filmstrips/vortex.png", (277, 277), (15, 1), 0.1, loop=True)
    image tornado:
        FilmStrip("content/gfx/be/filmstrips/tornado.png", (674, 592), (2, 3), 0.05, loop=True)
        anchor (0.5, 1.0)
        zoom 0.5
        subpixel True
        easeout 1.5 zoom 1.3

        on hide:
            alpha 1.0
            linear 0.5 alpha 0

    ########### Light:
    image light_1 = FilmStrip("content/gfx/be/filmstrips/light_1.png", (192, 192), (5, 5), 0.05, loop=False)
    image light_2 = FilmStrip("content/gfx/be/filmstrips/light_2.png", (192, 192), (5, 5), 0.05, loop=False)
    image light_3 = FilmStrip("content/gfx/be/filmstrips/light_3.png", (100, 100), (5, 16), 0.02, loop=False)
    image light_5 = FilmStrip("content/gfx/be/filmstrips/light_5.png", (192, 192), (5, 5), 0.1, loop=False)
    image dawn = FilmStrip("content/gfx/be/filmstrips/dawn.png", (192, 192), (5, 7), 0.1, loop=False)
    image holy_blast = FilmStrip("content/gfx/be/filmstrips/holy_blast_2x_bm.png", (382, 336), (8, 5), 0.1, include_frames=range(36), loop=False)

    ########### Darkness:
    image darkness_1 = FilmStrip("content/gfx/be/filmstrips/darkness_1.png", (192, 192), (5, 4), 0.05, loop=False)
    image darkness_2 = FilmStrip("content/gfx/be/filmstrips/darkness_2.png", (192, 192), (5, 4), 0.08, loop=False)
    image darkness_3 = FilmStrip("content/gfx/be/filmstrips/darkness_3.png", (192, 192), (5, 6), 0.05, loop=False)
    image darkness_4 = FilmStrip("content/gfx/be/filmstrips/darkness_4.png", (192, 192), (5, 6), 0.05, loop=False)
    image darkness_5 = FilmStrip("content/gfx/be/filmstrips/darkness_5.png", (375, 500), (4, 3), 0.1, loop=False)
    image darkness_6 = FilmStrip("content/gfx/be/filmstrips/darkness_6.png", (192, 192), (5, 3), 0.1, loop=False)
    image darklight = FilmStrip("content/gfx/be/filmstrips/darklight.png", (144, 192), (5, 4), 0.1, loop=False)
    image dominion = Transform(FilmStrip("content/gfx/be/filmstrips/dominion_bm.png", (595, 354), (5, 5), 0.1, loop=False),
                                                      size=(config.screen_width, config.screen_height))

    ########### Ice:
    image ice_1 = FilmStrip("content/gfx/be/filmstrips/ice_1.png", (192, 192), (5, 5), 0.08, loop=False)
    image ice_2 = FilmStrip("content/gfx/be/filmstrips/ice_2.png", (192, 192), (5, 5), 0.07, loop=False)
    image ice_3 = FilmStrip("content/gfx/be/filmstrips/ice_3.png", (192, 192), (5, 5), 0.05, loop=False)
    image ice_4 = FilmStrip("content/gfx/be/filmstrips/ice_4.png", (192, 192), (5, 4), 0.04, loop=False)
    image ice_5 = FilmStrip("content/gfx/be/filmstrips/ice_5.png", (192, 192), (5, 6), 0.07, loop=False)
    image ice_6 = FilmStrip("content/gfx/be/filmstrips/ice_6.png", (192, 192), (5, 4), 0.06, loop=False)
    image ice_7 = FilmStrip("content/gfx/be/filmstrips/ice_7.png", (192, 192), (5, 5), 0.08, loop=False, reverse=True)
    image ice_blast = FilmStrip("content/gfx/be/filmstrips/ice_blast.png", (393, 508), (5, 5), 0.1, include_frames=range(22), loop=False)
    image ice_twin_explosion = FilmStrip("content/gfx/be/filmstrips/ice_twin_explosion.png", (358, 312), (2, 4), 0.1, include_frames=range(7), loop=False)
    image ice_strike = FilmStrip("content/gfx/be/filmstrips/ice_strike.png", (581, 511), (3, 4), 0.1, loop=False)
    transform ice_storm(pos):
        contains:
            "ice_strike"
            pos pos
            anchor (0.5, 1.0)
            pause 1.2
            Null()
        contains:
            pause 0.6
            "ice_twin_explosion"
            pos pos
            anchor (0.5, 1.0)
            offset (-120, -10)
            pause 0.7
            Null()
        contains:
            pause 0.8
            "ice_twin_explosion"
            pos pos
            anchor (0.5, 1.0)
            offset (100, -60)
            pause 0.7
            Null()
        contains:
            pause 0.95
            "ice_twin_explosion"
            pos pos
            anchor (0.5, 1.0)
            offset (60, -140)
            pause 0.7
            Null()
        contains:
            pause 1.0
            "ice_twin_explosion"
            pos pos
            anchor (0.5, 1.0)
            offset (-60, -170)
            pause 0.7
            Null()
        contains:
            pause 1.0
            "ice_twin_explosion"
            pos pos
            anchor (0.5, 1.0)
            offset (40, -80)
            pause 0.7
            Null()

    ########### Electricity:
    image electricity_1 = FilmStrip("content/gfx/be/filmstrips/electricity_1.png", (192, 192), (5, 2), 0.1, loop=False)
    image electricity_2 = FilmStrip("content/gfx/be/filmstrips/electricity_2.png", (192, 192), (5, 3), 0.08, loop=False)
    image electricity_3 = FilmStrip("content/gfx/be/filmstrips/electricity_3.png", (192, 192), (5, 3), 0.09, loop=False)
    image electricity_4:
        FilmStrip("content/gfx/be/filmstrips/electricity_4.png", (192, 192), (5, 3), 0.04, loop=False)
        zoom 1.5
    image electricity_5 = FilmStrip("content/gfx/be/filmstrips/electricity_5.png", (192, 384), (5, 2), 0.08, loop=True)
    image electricity_6 = FilmStrip("content/gfx/be/filmstrips/electricity_6.png", (192, 192), (5, 16), 0.04, loop=True)
    image ion:
        FilmStrip("content/gfx/be/filmstrips/ion.png", (192, 192), (5, 9), 0.05, loop=True)
        zoom 3.0
    image ion_1:
        FilmStrip("content/gfx/be/filmstrips/ion_1.png", (192, 192), (5, 5), 0.04, loop=True)
        rotate 0
        linear 1.0 rotate 360
    image thunder_storm_2 = FilmStrip("content/gfx/be/filmstrips/thunder_storm_2.png", (354, 389), (4, 4), 0.1, loop=False)
    image moz_stretch:
        VBox(Transform("moz_webm", crop=(0, 0, 1199, 320)),
                  Transform("moz_webm", crop=(0, 320, 1199, 278), yzoom=2))
    ########### Poison:
    image poison_1 = FilmStrip("content/gfx/be/filmstrips/poison_1.png", (192, 192), (5, 6), 0.07, loop=False)
    image poison_2 = FilmStrip("content/gfx/be/filmstrips/poison_2.png", (192, 192), (5, 3), 0.1, loop=False)
    image poison_3 = FilmStrip("content/gfx/be/filmstrips/poison_3.png", (192, 192), (5, 5), 0.06, loop=False)
    ########### Healing:
    image heal_1 = FilmStrip("content/gfx/be/filmstrips/heal_1.png", (192, 192), (5, 6), 0.1, loop=False)
    image heal_2 = FilmStrip("content/gfx/be/filmstrips/heal_2.png", (192, 192), (5, 5), 0.1, loop=False)
    image heal_3 = FilmStrip("content/gfx/be/filmstrips/heal_3.png", (360, 360), (1, 42), 0.05, loop=False)
    image resurrection = FilmStrip("content/gfx/be/filmstrips/resurrection2x.png", (288, 247), (5, 4), 0.1, loop=False)
    ########### Magic Shields:
    image shield_1 = FilmStrip("content/gfx/be/filmstrips/shield_1.png", (192, 192), (5, 4), 0.05, loop=False)
    image shield_2:
        "content/gfx/be/solid_shield.png"
        alpha 0
        linear 0.4 alpha 0.7
        block:
            linear 0.5 alpha 0.9
            linear 0.5 alpha 0.7
            repeat
    ########### Weapons-only attacks
    image simple_poison_dagger_attack:
        im.Recolor("content/gfx/be/knives.png", 0, 255, 0, 255) # green attack for poison dagger
        alpha 1.0
        linear 0.5 alpha 0

    image simple_bow_fire_attack:
        im.Recolor("content/gfx/be/bows.png", 255, 45, 10, 255) # orange attack for fire bow
        alpha 1.0
        linear 0.5 alpha 0

    image simple_bow_ice_attack:
        im.Recolor("content/gfx/be/bows.png", 0, 173, 233, 255) # blue attack for ice bow
        alpha 1.0
        linear 0.5 alpha 0

    # fire bow:
    image Fire Arrow cast:
        "content/gfx/be/animations/flame_arrow/FlameArrow_1.png"
        pause 0.06
        "content/gfx/be/animations/flame_arrow/FlameArrow_2.png"
        pause 0.06
        "content/gfx/be/animations/flame_arrow/FlameArrow_3.png"
        pause 0.06
        "content/gfx/be/animations/flame_arrow/FlameArrow_4.png"
        pause 0.06
        "content/gfx/be/animations/flame_arrow/FlameArrow_5.png"
        pause 0.06
        "content/gfx/be/animations/flame_arrow/FlameArrow_6.png"
        pause 0.06
        "content/gfx/be/animations/flame_arrow/FlameArrow_7.png"
        pause 0.06
        "content/gfx/be/animations/flame_arrow/FlameArrow_8.png"
        pause 0.09
        "content/gfx/be/animations/flame_arrow/FlameArrow_9.png"
        pause 0.09
        "content/gfx/be/animations/flame_arrow/FlameArrow_10.png"
        pause 0.12
        "content/gfx/be/animations/flame_arrow/FlameArrow_11.png"
        pause 0.12
        "content/gfx/be/animations/flame_arrow/FlameArrow_12.png"
        pause 0.12
        "content/gfx/be/animations/flame_arrow/FlameArrow_13.png"
        pause 0.12

    image Fire Arrow fly:
        "content/gfx/be/animations/flame_arrow/FlameArrow.png"
        pause 0.3

    image Fire Arrow impact:
        "content/gfx/be/animations/flame_arrow/FlameArrow_I1.png"
        pause 0.12
        "content/gfx/be/animations/flame_arrow/FlameArrow_I2.png"
        pause 0.12
        "content/gfx/be/animations/flame_arrow/FlameArrow_I3.png"
        pause 0.12
        "content/gfx/be/animations/flame_arrow/FlameArrow_I4.png"
        pause 0.12
        "content/gfx/be/animations/flame_arrow/FlameArrow_I5.png"
        pause 0.13
        "content/gfx/be/animations/flame_arrow/FlameArrow_I6.png"
    # ice bow:
    image Ice Arrow cast:
        "content/gfx/be/animations/ice_arrow/Ice Arrow_1.png"
        pause 0.09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_2.png"
        pause 0.09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_3.png"
        pause 0.09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_4.png"
        pause 0.09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_5.png"
        pause 0.09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_6.png"
        pause 0.09
        "content/gfx/be/animations/ice_arrow/Ice Arrow_7.png"
        pause 0.06
        "content/gfx/be/animations/ice_arrow/Ice Arrow_8.png"
        pause 0.12
        "content/gfx/be/animations/ice_arrow/Ice Arrow_9.png"
        pause 0.12
        "content/gfx/be/animations/ice_arrow/Ice Arrow_10.png"
        pause 0.12
        "content/gfx/be/animations/ice_arrow/Ice Arrow_11.png"
        pause 0.12
        "content/gfx/be/animations/ice_arrow/Ice Arrow_12.png"
        pause 0.12

    image Ice Arrow fly:
        "content/gfx/be/animations/ice_arrow/Ice Arrow.png"
        pause 0.3

    image Ice Arrow impact:
        "content/gfx/be/animations/ice_arrow/IceArrow_I1.png"
        pause 0.10
        "content/gfx/be/animations/ice_arrow/IceArrow_I2.png"
        pause 0.10
        "content/gfx/be/animations/ice_arrow/IceArrow_I3.png"
        pause 0.12
        "content/gfx/be/animations/ice_arrow/IceArrow_I4.png"
        pause 0.12
        "content/gfx/be/animations/ice_arrow/IceArrow_I5.png"
        pause 0.12
        "content/gfx/be/animations/ice_arrow/IceArrow_I6.png"
        pause 0.12
        "content/gfx/be/animations/ice_arrow/IceArrow_I7.png"
        pause 0.12
        "content/gfx/be/animations/ice_arrow/IceArrow_I8.png"

    image ice_dagger = FilmStrip("content/gfx/be/filmstrips/ice_dagger.png", (192, 192), (5, 3), 0.05, loop=False)

# Skillz (We do not want to do this in the init so I am making it a label):
label load_battle_skills:
    python:
        # Weapons:
        # Sword attacks:
        BE_Action("Sword Slash", attributes=["melee", "physical"], critpower=0, effect=5, multiplier=0.5, range=1, vitality_cost=1, menu_pos=0,
                desc="Attacking with a blade.",
                main_effect={"gfx": "simple_sword_attack", "sfx": "content/sfx/sound/be/sword.mp3", "duration": .5},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        MultiAttack("Sword Slash 2X", attributes=["melee", "physical"], critpower=.02, multiplier=0.65, effect=10, range=1, vitality_cost=2, menu_pos=0.1,
                desc="Two quick attacks with a blade.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/swords.png", 150, 150), "sfx": "content/sfx/sound/be/sword.mp3", "duration": .6},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .55},
                target_death_effect={"gfx": "dissolve", "initial_pause": .6, "duration": .5})
        MultiAttack("Sword Slash 4X", attributes=["melee", "physical"], critpower=.04, multiplier=0.8, effect=25, range=1, vitality_cost=4, menu_pos=0.2,
                desc="Four quick attacks with a blade.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/swords.png", 150, 150), "sfx": "content/sfx/sound/be/sword.mp3", "duration": 1.2, "times": 4},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .85},
                target_death_effect={"gfx": "dissolve", "initial_pause": .8, "duration": .5})
        MultiAttack("Sword Slash 6X", attributes=["melee", "physical"], critpower=.06, multiplier=0.9, effect=50, range=1, vitality_cost=8, menu_pos=0.3,
                desc="Six quick attacks with a blade.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/swords.png", 150, 150), "sfx": "content/sfx/sound/be/sword.mp3", "duration": 1.5, "times": 6, "interval": .25},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": 1.2},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.25, "duration": .5})
        MultiAttack("Sword Slash 10X", attributes=["melee", "physical"], critpower=.1, multiplier=1.0, effect=80, range=1, vitality_cost=8, menu_pos=0.5,
                desc="Ten quick attacks with a blade.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/swords.png", 150, 150), "sfx": "content/sfx/sound/be/sword.mp3", "duration": 2.0, "times": 10, "interval": .2},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": 1.95},
                target_death_effect={"gfx": "dissolve", "initial_pause": 2.0, "duration": .5})
        BE_Action(u"Moon Slash", range=1, attributes=["melee", "ice", "light", "physical"], critpower=.2, effect=50, multiplier=0.9, vitality_cost=5, menu_pos=1.0,
                desc="Attacking with the moon powered sword.",
                main_effect={"gfx": "moon_hit_webm", "sfx": "content/sfx/sound/be/moon_attack.ogg", "duration": 0.37, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.01, "duration": 0.3},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .4})
        P2P_Skill(u"Moon Projective Slash", menu_pos=1.1, range=3, attributes=["ranged", "light", "ice"], critpower=.3, effect=40, piercing=True, menuname="M Projective", multiplier=0.85, vitality_cost=10, mp_cost=0.1,
                desc="The inner powers of the weapon allow to perform attacks even at great distance.",
                projectile_effects={"gfx": "moon_proj_webm", "sfx": "content/sfx/sound/be/pr_sl.mp3", "duration": 0.37, "aim": {"point": "center", "anchor": (.5, .5)}},
                main_effect={"gfx": "moon_hit_webm", "sfx": "content/sfx/sound/be/moon_attack.ogg", "duration": 0.37, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.01, "duration": 0.3},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .15},
                dodge_effect={"initial_pause": 0.005})
        BE_Action(u"Moon Slice", menu_pos=1.5, range=3, attributes=["melee", "light", "ice", "electricity"], critpower=.4, effect=85, multiplier=1.2, vitality_cost=20, mp_cost=0.15,
                desc="Uses the rotation energy of the Moon to perform a deadly strike.",
                main_effect={"gfx": Transform("moon_slash_webm", zoom=1.1), "sfx": "content/sfx/sound/be/moon.ogg", "duration": 0.77, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_light", "initial_pause": .1, "duration": .6},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.6, "duration": .2})
        BE_Action(u"Dark Slash", range=1, attributes=["melee", "physical", "darkness"], critpower=.4, multiplier=1.15, effect=100, vitality_cost=8, menu_pos=1.5,
                desc="Attacking with a dark sword.",
                main_effect={"gfx": Transform("demon_sword_webm", zoom=1.1), "sfx": "content/sfx/sound/be/demon_sword.ogg", "duration": 0.27, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .1, "duration": .25},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .4})
        P2P_Skill(u"Dark Projective Slash", menu_pos=1.6, range=3, attributes=["ranged", "physical", "darkness"], critpower=.1, piercing=True, menuname="D Projective", effect=60, multiplier=1.05, vitality_cost=10, mp_cost=0.1,
                desc="Dark inner powers of the weapon allow to perform attacks even at great distance.",
                projectile_effects={"gfx": "dark_projective_webm", "sfx": "content/sfx/sound/be/pr_sl.mp3", "duration": 0.55, "aim": {"point": "center", "anchor": (.5, .5)}},
                main_effect={"gfx": Null(), "sfx": None, "duration": 0.01, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                target_sprite_damage_effect={"gfx": "on_darkness", "initial_pause": 0.01, "duration": 0.2},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .15},
                dodge_effect={"initial_pause": 0.005})
        BE_Action(u"Demonic Core", menu_pos=2, range=1, attributes=["melee", "physical", "darkness", "fire", "inevitable"], critpower=1.0, effect=150, multiplier=1.35, vitality_cost=35, health_cost=0.15,
                desc="Concentrates inner powers of the weapon to perform a powerful attack. Critical strikes are especially dangerous.",
                main_effect={"gfx": Transform("demon_slash_webm", zoom=1.1), "sfx": "content/sfx/sound/be/demon_core.ogg", "duration": 1.6, "aim": {"point": "tc", "anchor": (.5, .5), "xo": 80}, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_dark_with_shake", "initial_pause": .3, "duration": 1.0},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": .5})
        BE_Action(u"Light Slash", range=1, attributes=["melee", "physical", "light"], critpower=.3, effect=100, multiplier=1.15, vitality_cost=8, menu_pos=1.5,
                desc="Attacking with a light sword.",
                main_effect={"gfx": Transform("angel_sword_webm", zoom=1.1), "sfx": "content/sfx/sound/be/light3.mp3", "duration": 0.35, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .1, "duration": .25},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .4})
        ArealSkill(u"Light Field", range=3, attributes=["ranged", "light", "inevitable"], critpower=.2, menu_pos=1.6, effect=150, multiplier=0.95, vitality_cost=25, mp_cost=0.15, type="all_enemies", piercing=True,
                desc="Countless cascading blades of pure light leave no place for escape.",
                main_effect={"gfx": Transform("holy_sword_webm", zoom=1.2), "sfx": "content/sfx/sound/be/light_field.mp3", "duration": 2.7, "aim": {"anchor": (0.6, 0.8), "xo": 0, "yo":0}, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_light", "initial_pause": 1.3, "duration": 1.3},
                target_death_effect={"gfx": "dissolve", "initial_pause": 2.3, "duration": .5})
        BE_Action(u"Angelic Rain", menu_pos=2, range=2, attributes=["ranged", "physical", "light"], critpower=.5,  effect=100, multiplier=1.35, vitality_cost=35, mp_cost=0.2,
                desc="Concentrates inner powers of the weapon to summon blades of light upon the target.",
                main_effect={"gfx": Transform("angel_swords_webm", zoom=1.3), "sfx": "content/sfx/sound/be/light_rain.ogg", "duration": 0.97, "aim": {"point": "tc", "anchor": (0.5, 0.5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_light", "initial_pause": .3, "duration": .6},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.7, "duration": .5})
        BE_Action(u"Chop Rush", menu_pos=0.6, range=1, attributes=["melee", "physical"], effect=90, critpower=0.7, multiplier=1.05, vitality_cost=20,
                desc="A deadly combination of heavy sharp blade and high speed. Critical hits are especially dangerous.",
                main_effect={"gfx": Transform("weapon_chopper_webm", zoom=1.1), "sfx": "content/sfx/sound/be/chop_1.ogg", "duration": 1.17, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 1.0},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.1, "duration": .4})
        BE_Action(u"Ice Slash", menu_pos=0.31, range=1, attributes=["melee", "ice", "physical"], effect=80, multiplier=0.85, vitality_cost=6, mp_cost=1,
                desc="Attacking with an ice blade.",
                main_effect={"gfx": Transform("ice_dagger", zoom=1.6), "sfx": "content/sfx/sound/be/knife_ice.mp3", "duration": 0.75, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "iced_with_shake", "initial_pause": .3, "duration": .5},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": .5})
        MultiAttack("Ice Slash 4X", attributes=["melee", "physical", "ice"], menu_pos=0.32, critpower=0.15, mp_cost=3, multiplier=0.95, effect=85, vitality_cost=10, range=1,
                desc="Four quick strikes with an ice sword.",
                main_effect={"gfx": Transform("ice_dagger", zoom=1.1), "sfx": "content/sfx/sound/be/knife_ice.mp3", "duration": 1.8, "times": 4, "interval": .5, "alpha_fade": 1.0, "sd_duration": .75},
                target_sprite_damage_effect={"gfx": "iced_with_shake", "initial_pause": .05, "duration": 1.5},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": .5})
        BE_Action(u"Big Ice Break", range=2, attributes=["ranged", "ice"], menu_pos=1.4, effect=110, multiplier=1.25, critpower=0.3, vitality_cost=20, mp_cost=10,
                desc="Released inner powers of the dagger send a sharp ice formation towards the target.",
                main_effect={"gfx": Transform("ice_dagger_webm", zoom=1.4), "sfx": "content/sfx/sound/be/knife_ice.mp3", "duration": 0.88, "aim": {"point": "center", "anchor": (.5, .5), "xo":140}, "hflip": True},
                target_sprite_damage_effect={"gfx": "frozen", "initial_pause": .3, "duration": .4},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": .5})
        BE_Action(u"Excalibur Slash", range=1, attributes=["melee", "light", "darkness", "physical"], critpower=.2, effect=150, multiplier=1.35, vitality_cost=15, menu_pos=2, mp_cost=0.05,
                desc="Even a normal attack draws in the power of elements as a result of microcracks in the space itself.",
                main_effect={"gfx": Transform("omni_sword_webm", zoom=1.1), "sfx": "content/sfx/sound/be/excal.ogg", "duration": 0.27, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .1, "duration": .25},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .4})
        # to do post beta: unique target_sprite_damage_effect for superior multielemental weapons like Excalibur
        BE_Action(u"Full Power Slash", menu_pos=3, range=2, attributes=["melee", "physical", "light", "darkness", "earth", "fire", "air"], critpower=0.3, effect=200, multiplier=1.8, vitality_cost=30, mp_cost=0.1,
                desc="Power of the weapon distorts space on the path of the blade, causing powerful shockwave.",
                main_effect={"gfx": Transform("planet_slash_webm", zoom=1.1), "sfx": "content/sfx/sound/be/exc_bl.ogg", "duration": 1.2, "aim": {"point": "tc", "anchor": (.5, .5), "xo": 80}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .5, "duration": .6, "master_shake": True},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": .5})
        ArealSkill(u"Consecutive Slashes", range=3, attributes=["melee", "physical", "light", "darkness", "ice", "electricity", "inevitable"], critpower=0.4, menu_pos=5, effect=250, multiplier=2.0, vitality_cost=50, mp_cost=0.2, health_cost=5, type="all_enemies", piercing=True,
                desc="Multiple rapid attacks cause local space collapsing.",
                main_effect={"gfx": Transform("universe_slash_webm", zoom=0.9), "sfx": "content/sfx/sound/be/exc_full.ogg", "duration": 1.7, "aim": {"anchor": (0.5, 0.5), "xo": 100, "yo":-100}, "hflip": True, "webm_size": (1000,800)},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 1.5, "master_shake": True},
                target_death_effect={"gfx": "shatter", "initial_pause": 1.75, "duration": 0.7},
                bg_main_effect={"gfx": "mirage", "initial_pause": 0.1, "duration": 1.3})
        BE_Action(u"Soul Blade", menu_pos=1.4, range=1, attributes=["melee", "physical"], effect=30, multiplier=0.8, critpower=.3, vitality_cost=8, mp_cost=0.05, piercing=True,
                desc="Projects a huge blade made from the user's soul energy towards the target.",
                main_effect={"gfx": Transform("soul_sword_webm", zoom=1.1), "sfx": "content/sfx/sound/be/soul_sword.mp3", "duration": 0.5, "aim": {"point": "center", "anchor": (.5, .5), "xo": 80}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .3, "duration": .5},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": .5})
        BE_Action(u"Weapon Dance", menu_pos=1.8, range=3, attributes=["melee", "physical"], effect=65, multiplier=1.0, critpower=-0.2, vitality_cost=25, type="all_enemies",
                desc="Multiple elegant strikes in quick succession.",
                main_effect={"gfx": Transform("weapon_dance_webm", zoom=1.1), "sfx": "content/sfx/sound/be/multi.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .1, "duration": 1.3},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.2, "duration": .3})
        BE_Action(u"Solar Incision", menu_pos=1.3, range=2, attributes=["melee", "fire", "physical"], effect=100, critpower=.2, multiplier=1.25, vitality_cost=15, mp_cost=15,
                desc="A small artificial sun explodes in front of the target.",
                main_effect={"gfx": Transform("fire_sword_webm"), "sfx": "content/sfx/sound/be/fire_sword.mp3", "duration": 1.1, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_fire_with_shake", "initial_pause": 0.4, "duration": 0.7},
                target_death_effect={"gfx": "dissolve", "initial_pause": .4, "duration": .5})
        P2P_Skill(u"Projective Slash", menu_pos=1.0, range=3, attributes=["ranged", "physical"], critpower=.1, effect=20, multiplier=0.8, vitality_cost=10, mp_cost=5, piercing=True,
                desc="With special enchantment even simplest blades can be used to send cutting waves at a distance.",
                projectile_effects={"gfx": "simple_projective_webm", "sfx": "content/sfx/sound/be/pr_sl.mp3", "duration": 0.55, "aim": {"point": "center", "anchor": (.5, .5)}},
                main_effect={"gfx": Null(), "sfx": None, "duration": 0.01, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.01, "duration": 0.2},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .15},
                dodge_effect={"initial_pause": -.01})


        # Rapier attacks:
        BE_Action(u"Steel Flourish", range=1, attributes=["melee", "physical"], critpower=0.6, effect=70, multiplier=1.05, vitality_cost=12, mp_cost=6, menu_pos=1,
                desc="Quick consecutive slashes form an ancient rune capable to increase critical damage.",
                main_effect={"gfx": Transform("steel_flourish_webm", zoom=1.1), "sfx": "content/sfx/sound/be/chop.ogg", "duration": 0.97, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .15, "duration": .8},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": .4})
        BE_Action(u"Toxic Core", range=1, attributes=["melee", "physical", "poison"], critpower=0.2, effect=100, multiplier=0.95, vitality_cost=5, health_cost=5, menu_pos=1.1,
                desc="Inner layers of the weapon produce natural toxins which could be released during attack if necessary.",
                main_effect={"gfx": Transform("elven_rapier_webm", zoom=0.9), "sfx": "content/sfx/sound/be/sword.mp3", "duration": 0.47, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "poisoned_with_shake", "initial_pause": .15, "duration": .8},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": .4})
        BE_Action(u"Air Assault", range=1, attributes=["melee", "physical", "air"], critpower=.1, effect=30, vitality_cost=20,  multiplier=1.0, health_cost=15, menu_pos=1.2, type="all_enemies",
                desc="Countless quick slashes rip the air itself, sending rapid shockwaves.",
                main_effect={"gfx": Transform("elven_combo_webm", zoom=1.1), "sfx": "content/sfx/sound/be/elven_combo.mp3", "duration": 1.4, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_air", "initial_pause": .1, "duration": 1.2},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.9, "duration": .3})
        # Bow Attacks:
        BE_Action("Bow Shot", attributes=["ranged", "physical"], critpower=0, effect=5, range=3, vitality_cost=1, menu_pos=0, multiplier=0.5,
                desc="Shooting an arrow.",
                main_effect={"gfx": "simple_bow_attack", "sfx": "content/sfx/sound/be/bow_attack.mp3", "duration": .5,},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        MultiAttack("Bow Shot 2X", attributes=["ranged", "physical"], critpower=.02, multiplier=0.65, effect=20, range=3, vitality_cost=2, menu_pos=0.1,
                desc="Shooting two arrows in quick succession.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/bows.png", 150, 150), "sfx": "content/sfx/sound/be/bow_attack.mp3", "duration": .6},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .55},
                target_death_effect={"gfx": "dissolve", "initial_pause": .6, "duration": .5})
        MultiAttack("Bow Shot 4X", attributes=["ranged", "physical"], critpower=.04, multiplier=0.8, effect=50, range=4, vitality_cost=5, menu_pos=0.2,
                desc="Shooting four arrows in quick succession.",
                 main_effect={"gfx": ProportionalScale("content/gfx/be/bows.png", 150, 150), "sfx": "content/sfx/sound/be/bow_attack.mp3", "duration": 1.2, "times": 4},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": 1.1},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": .5})
        BE_Action(u"Light Shot", range=4, attributes=["ranged", "physical", "light"], critpower=.2, multiplier=0.9, effect=60, vitality_cost=5, menu_pos=1.0,
                desc="Shooting an arrow made of light.",
                main_effect={"gfx": Transform("angel_bow_attack_webm", zoom=1.1), "sfx": "content/sfx/sound/be/light3.mp3", "duration": 0.96, "aim": {"point": "center", "anchor": (.5, .5)}},
                target_sprite_damage_effect={"gfx": "on_light", "initial_pause": .1, "duration": .25},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .4})
        BE_Action(u"Dark Shot", range=4, attributes=["ranged", "physical", "darkness"], critpower=.4, multiplier=0.95, effect=70, vitality_cost=4, health_cost=2, menu_pos=1.0,
                desc="Shooting an arrow made of darkness.",
                main_effect={"gfx": Transform("demon_bow_attack_webm", zoom=1.1), "sfx": "content/sfx/sound/be/demon_sword.ogg", "duration": 0.96, "aim": {"point": "center", "anchor": (.5, .5)}},
                target_sprite_damage_effect={"gfx": "on_darkness", "initial_pause": .1, "duration": .25},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .4})
        BE_Action("Poison Arrow", attributes=["ranged", "physical", "poison"], critpower=0, multiplier=0.8, effect=15, range=4, vitality_cost=4, menu_pos=1.5, piercing=True,
                desc="Shooting a poisonous arrow.",
                main_effect={"gfx": Transform("green_hit_webm", zoom=1.1), "sfx": "content/sfx/sound/be/elf_arrow.ogg", "duration": 0.56, "hflip": True},
                target_sprite_damage_effect={"gfx": "poisoned_with_shake", "initial_pause": .1, "duration": .4})
        ArrowsSkill(u"Emerald Arrow", menu_pos=1.6, attributes=["ranged", "air", "earth"], critpower=.3, effect=55, multiplier=0.95, vitality_cost=12, mp_cost=3, range=4, piercing=True,
                desc="Shooting an arrow empowered with the nature itself.",
                firing_effects={"gfx": "emerald_bow_webm", "sfx": "content/sfx/sound/be/elf_bow.ogg", "duration": 0.86},
                projectile_effects={"gfx": "emerald_bow_arrow_webm", "sfx": None, "duration": 0.76},
                attacker_effects={"gfx": "earth_2", "sfx": "default"},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.021},
                main_effect={"gfx": "emerald_bow_hit_webm", "sfx": "content/sfx/sound/be/elf_arrow.ogg", "duration": 0.46, "aim": {"anchor": (.5, .5)}},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .01, "duration": .3},
                target_death_effect={"gfx": "dissolve", "initial_pause": .3, "duration": .5},
                dodge_effect={"initial_pause": .1})
        ArrowsSkill(u"Trinity Arrow", menu_pos=2, attributes=["ranged", "light"], effect=95, critpower=.3, multiplier=1.3, vitality_cost=30, mp_cost=5, range=4, piercing=True,
                desc="Shooting triple arrow made of highly concentrated light.",
                firing_effects={"gfx": Transform("angel_bow_webm", zoom=1.3), "sfx": "content/sfx/sound/be/elf_bow.ogg", "duration": 1.2},
                projectile_effects={"gfx": "angel_bow_arrow_webm", "sfx": None, "duration": 0.46},
                attacker_effects={"gfx": "light_2", "sfx": "default"},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.021},
                main_effect={"gfx": Transform("angel_bow_hit_webm", zoom=1.5), "sfx": "content/sfx/sound/be/light3.mp3", "duration": 0.36, "aim": {"anchor": (.5, .5)}},
                target_sprite_damage_effect={"gfx": "on_light", "initial_pause": .01, "duration": .3},
                target_death_effect={"gfx": "dissolve", "initial_pause": .3, "duration": .5},
                dodge_effect={"initial_pause": .1})
        P2P_Skill(u"Midnight Arrow", menu_pos=2, range=3, attributes=["ranged", "physical", "darkness"], effect=100, multiplier=1.3, vitality_cost=20, health_cost=10, critpower=.3,
                desc="Releases explosive arrow made of dark energy.",
                projectile_effects={"gfx": "demon_bow_arrow_webm", "sfx": "content/sfx/sound/be/elf_bow.ogg", "duration": 0.56, "aim": {"point": "center", "anchor": (.5, .5)}},
                main_effect={"gfx": "demon_bow_hit_webm", "sfx":"content/sfx/sound/be/demon_core.ogg", "duration": 0.36, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_dark_with_shake", "initial_pause": 0.01, "duration": 0.2},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .15},
                dodge_effect={"initial_pause": 0.005})
        BE_Action("Fire Shot", attributes=["ranged", "physical", "fire"], critpower=0.1, multiplier=0.85, effect=30, range=3, vitality_cost=3, menu_pos=1.0,
                desc="Shooting a fire arrow.",
                main_effect={"gfx": Transform("simple_bow_fire_attack", zoom=0.8), "sfx": "content/sfx/sound/be/bow_attack.mp3", "duration": 0.5},
                target_sprite_damage_effect={"gfx": "on_fire_with_shake", "initial_pause": .05, "duration": .5})
        BE_Action("Ice Shot", attributes=["ranged", "physical", "ice"], critpower=0.1, multiplier=0.85, effect=30, range=3, vitality_cost=3, menu_pos=1.0,
                desc="Shooting an ice arrow.",
                main_effect={"gfx": Transform("simple_bow_ice_attack", zoom=0.8), "sfx": "content/sfx/sound/be/bow_attack.mp3", "duration": 0.5},
                target_sprite_damage_effect={"gfx": "iced_with_shake", "initial_pause": .05, "duration": .5})
        ArrowsSkill(u"Fire Arrow", menu_pos=1.2, attributes=["ranged", "fire", "air"], effect=45, multiplier=1.0, critpower=.2, mp_cost=5, vitality_cost=10, range=4, piercing=True,
                desc="Shooting an arrow of scorching air.",
                firing_effects={"gfx": "Fire Arrow cast", "sfx": "content/sfx/sound/be/fire_arrow.mp3"},
                projectile_effects={"gfx": "Fire Arrow fly", "sfx": None, "duration": 0.4},
                attacker_effects={"gfx": "default_1", "sfx": "default"},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.021},
                main_effect={"gfx": "Fire Arrow impact", "sfx": None, "duration": 0.51, "aim": {"anchor": (.5, .5)}},
                target_sprite_damage_effect={"gfx": "burning_with_shake", "initial_pause": .01, "duration": .3},
                target_death_effect={"gfx": "dissolve", "initial_pause": .3, "duration": .5},
                dodge_effect={"initial_pause": .1})

        ArrowsSkill("Ice Arrow", menu_pos=1.2, attributes=["ranged", "ice", "water"], effect=45, multiplier=1.0, critpower=.2, mp_cost=5, vitality_cost=10, range=4, piercing=True,
                desc="Shooting an arrow of frozen water.",
                firing_effects={"gfx": "Ice Arrow cast", "sfx": "content/sfx/sound/be/ice_arrow.mp3"},
                projectile_effects={"gfx": "Ice Arrow fly", "sfx": None, "duration": 0.4},
                main_effect={"gfx": "Ice Arrow impact", "sfx": None, "duration": 0.51, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                attacker_effects={"gfx": "ice_2", "sfx": "default"},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.021},
                target_sprite_damage_effect={"gfx": "frozen_with_shake", "initial_pause": .01, "duration": .3},
                target_death_effect={"gfx": "dissolve", "initial_pause": .3, "duration": .5},
                dodge_effect={"initial_pause": .1})
        BE_Action(u"Arc Strike", menu_pos=1.0, range=3, attributes=["ranged", "physical"], effect=35, multiplier=0.9, critpower=0.15, vitality_cost=10, mp_cost=5, type="all_enemies",
                desc="Countless enchanted arrows are coming from above.",
                main_effect={"gfx": Transform("magic_bow_webm", zoom=1.1), "sfx": "content/sfx/sound/be/enc_arrows.ogg", "duration": 0.67, "aim": {"point": "center", "anchor": (.5, .5)}},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .1, "duration": .5},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": .5})
        # Crossbow Attacks:
        BE_Action("Crossbow Shot", attributes=["ranged", "physical"], critpower=0.1, multiplier=0.55, effect=10, range=4, vitality_cost=1, menu_pos=0,
                desc="Shooting a bolt.",
                main_effect={"gfx": "simple_crossbow_attack", "sfx": "content/sfx/sound/be/crossbow_attack.mp3", "duration": 0.5},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        BE_Action(u"Penetrating Bolt", range=3, attributes=["ranged", "physical"], critpower=.5, multiplier=0.65, piercing=True, effect=20, vitality_cost=6, menu_pos=1,
                desc="Releases special high-density bolt with high critical damage.",
                main_effect={"gfx": Transform("crossbow_hit_webm", zoom=1.3), "sfx": "content/sfx/sound/be/crossbow_1.ogg", "duration": 0.56, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .1, "duration": 1.8},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": 0.8})
        # Daggers Attacks:
        BE_Action("Dagger Strike", attributes=["melee", "physical"], critpower=0.05, effect=1, range=1, vitality_cost=1, menu_pos=0, multiplier=0.5,
                desc="Attacking with a dagger.",
                main_effect={"gfx": "simple_dagger_attack", "sfx": "content/sfx/sound/be/knife.mp3", "duration": .5, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        MultiAttack("Dagger Strike 4X", attributes=["melee", "physical"], critpower=.075, multiplier=0.75, effect=20, vitality_cost=5, range=1,
                desc="Four quick strikes with a dagger.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/knives.png", 150, 150), "sfx": "content/sfx/sound/be/dagger_attack_2.mp3", "duration": 1.2, "times": 4, "interval": .2},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .55},
                target_death_effect={"gfx": "dissolve", "initial_pause": .6, "duration": .5})
        BE_Action(u"Rapid Strikes", range=1, attributes=["melee", "physical"], effect=30, menu_pos=0.5, multiplier=0.85, critpower=.2, vitality_cost=15, type="all_enemies",
                desc="Special enchantments can temporally decrease weapon weight and momentum, allowing to perform rapid succession of strikes.",
                main_effect={"gfx": Transform("speed_dagger_webm", zoom=1.1), "sfx": "content/sfx/sound/be/multi_dagger.mp3", "duration": 0.5, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .1, "duration": .4},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": .2})
        BE_Action(u"Ice Strike", menu_pos=0.31, range=1, attributes=["melee", "ice", "physical"], effect=60, critpower=.15, multiplier=0.8, vitality_cost=5, mp_cost=1,
                desc="Stabbing with an ice dagger.",
                main_effect={"gfx": Transform("ice_dagger", zoom=1.1), "sfx": "content/sfx/sound/be/knife_ice.mp3", "duration": 0.75, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "iced_with_shake", "initial_pause": .3, "duration": .5},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": .5})

        MultiAttack("Ice Strike 3X", attributes=["melee", "physical", "ice"], menu_pos=0.32, multiplier=0.9, critpower=0.25, effect=80, vitality_cost=7, mp_cost=2, range=1,
                desc="Three quick strikes with an ice dagger.",
                main_effect={"gfx": Transform("ice_dagger", zoom=1.1), "sfx": "content/sfx/sound/be/knife_ice.mp3", "duration": 1.5, "times": 3, "interval": .5, "alpha_fade": 1.0, "sd_duration": .75},
                target_sprite_damage_effect={"gfx": "iced_with_shake", "initial_pause": .05, "duration": 1.5},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": .5})
        BE_Action(u"Ice Break", range=2, attributes=["ranged", "ice"], menu_pos=1.4, effect=90, multiplier=1.1, critpower=0.35, vitality_cost=15, mp_cost=7,
                desc="Released inner powers of the dagger send a sharp ice formation towards the target.",
                main_effect={"gfx": Transform("ice_dagger_webm", zoom=0.8), "sfx": "content/sfx/sound/be/knife_ice.mp3", "duration": 0.88, "aim": {"point": "center", "anchor": (.5, .5), "xo":140}, "hflip": True},
                target_sprite_damage_effect={"gfx": "frozen", "initial_pause": .3, "duration": .4},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": .5})
        BE_Action("Poisoned Dagger", attributes=["melee", "physical", "poison"], critpower=0.2, effect=20, range=1, vitality_cost=2, menu_pos=0.2, multiplier=0.6,
                desc="Stabbing with a poisoned dagger.",
                main_effect={"gfx": Transform("simple_poison_dagger_attack", zoom=0.9), "sfx": "content/sfx/sound/be/knife.mp3", "duration": 0.5, "hflip": True},
                target_sprite_damage_effect={"gfx": "poisoned_with_shake", "initial_pause": .05, "duration": .5})
        BasicPoisonSpell(u"Poisonous Rune", range=2, attributes=["status", "poison"], effect=55, menuname = "P Rune", menu_pos=0.7, multiplier=1.0, vitality_cost=20, mp_cost=0.1,
                desc="Blade enchantment materializes a good deal of poison above the target.",
                main_effect={"gfx": Transform("poison_dagger_webm", zoom=1.1), "sfx": "content/sfx/sound/be/poison_cloud.mp3", "duration": 1.8, "aim": {"point": "tc", "anchor": (.5, .5)}, "hflip": True},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.0},
                target_sprite_damage_effect={"gfx": "poisoned_with_shake", "initial_pause": 1.0, "duration": .8},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": .4})
        P2P_Skill("Shadow Kunai", attributes=["ranged", "darkness", "physical"], menu_pos=1.5, effect=70, vitality_cost=20, multiplier=1.0, critpower=.3, mp_cost=0.1, range=4, piercing=True,
                desc="Creates an explosive shadow copy of the weapon which can be thrown at the target.",
                projectile_effects={"gfx": "kunai_throw_webm", "sfx": "content/sfx/sound/be/kunai_throw.mp3", "duration": 0.75},
                main_effect={"gfx": Transform("kunai_exp_webm", zoom=1), "sfx": "content/sfx/sound/be/kunai_exp.mp3", "duration": 0.55, "aim": {"anchor": (0.5, 0.5)}},
                target_sprite_damage_effect={"gfx": "on_dark_with_shake", "initial_pause": 0.1, "duration": 0.4},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.1, "duration": 0.4},
                dodge_effect={"initial_pause": 0.01})
        ArealSkill(u"Shadow Contract", range=2, attributes=["melee", "darkness", "physical", "poison"], menu_pos=1.8, effect=100, critpower=.4, multiplier=1.2, vitality_cost=30, mp_cost=0.2, type="all_enemies", piercing=True,
                desc="Establishes spiritual connection between shadow scrolls and targets body parts. All that remains is to destroy the said scrolls.",
                main_effect={"gfx": Transform("kunai_bomb_webm", zoom=1.2), "sfx": "content/sfx/sound/be/shadow_contract.ogg", "duration": 1.46, "aim": {"anchor": (0.5, 0.5), "xo": 180, "yo":-70}, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_dark_with_shake", "initial_pause": .2, "duration": 1.2},
                target_death_effect={"gfx": "dissolve", "initial_pause": .7, "duration": .5},
                bg_main_effect={"gfx": "mirage", "initial_pause": 0.7, "duration": 0.3},
                dodge_effect={"initial_pause": 0.7})
        # Claw Attacks:
        BE_Action("Claw Slash", attributes=["melee", "physical"], critpower=0.1, effect=15, range=1, vitality_cost=1, menu_pos=0, multiplier=0.5,
                desc="Ripping with claws.",
                main_effect={"gfx": "simple_claw_attack", "sfx": "content/sfx/sound/be/claw_attack.mp3", "duration": .5, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        MultiAttack("Claw Slash 2X", attributes=["melee", "physical"], critpower=.1,  effect=30, range=1, vitality_cost=2, menu_pos=0.1, multiplier=0.65,
                desc="Two quick attacks with claws.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/claws.png", 150, 150), "sfx": "content/sfx/sound/be/claw_attack.mp3", "duration": 0.6, "times": 2},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .55},
                target_death_effect={"gfx": "dissolve", "initial_pause": .3, "duration": .3})
        MultiAttack("Claw Slash 4X", attributes=["melee", "physical"], critpower=.1, multiplier=0.8, effect=45, range=1, vitality_cost=5, menu_pos=0.2,
                desc="Four quick attacks with claws.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/claws.png", 150, 150), "sfx": "content/sfx/sound/be/claw_attack.mp3", "duration": 1.2, "times": 4},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": 1.05},
                target_death_effect={"gfx": "dissolve", "initial_pause": .7, "duration": .3})
        # Fist Attacks:
        BE_Action("Fist Attack", attributes=["melee", "physical"], critpower=-0.2, effect=5, range=1, menu_pos=0, multiplier=0.4,
                desc="Attacking with bare hands.",
                main_effect={"gfx": "simple_fist_attack", "sfx": list("content/sfx/sound/be/fist_attack_%d.mp3"%i for i in xrange(1, 6)), "duration": .5},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        MultiAttack("Fist Attack 2X", attributes=["melee", "physical"], critpower=-0.2, effect=5, range=1, vitality_cost=1, menu_pos=0.1,  multiplier=0.5,
                desc="Two quick attacks with bare hands.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/fists.png", 150, 150), "sfx": "content/sfx/sound/be/fist_attack_5.mp3", "duration": 0.6, "times": 2},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .55},
                target_death_effect={"gfx": "dissolve", "initial_pause": .3, "duration": .3})
        MultiAttack("Fist Attack 4X", attributes=["melee", "physical"], critpower=-.2, multiplier=0.6, effect=5, range=1, vitality_cost=2, menu_pos=0.2,
                desc="Two quick attacks with bare hands.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/fists.png", 150, 150), "sfx": "content/sfx/sound/be/fist_attack_5.mp3", "duration": 1.2, "times": 4},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": 1.05},
                target_death_effect={"gfx": "dissolve", "initial_pause": .6, "duration": .3})
        BE_Action(u"Fire Barrage", menu_pos=0.5, range=1, attributes=["melee", "fire", "physical"], effect=40, critpower=.1, multiplier=0.9, vitality_cost=5,
                desc="A high-speed combination of attacks, fast enough to set air around the target ablaze.",
                main_effect={"gfx": "multi_fist_webm", "sfx": "content/sfx/sound/be/fire_barrage.ogg", "duration": 0.46, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_fire_with_shake", "initial_pause": 0.1, "duration": 0.36},
                target_death_effect={"gfx": "dissolve", "initial_pause": .2, "duration": .4})
        # Cannon Attacks:
        BE_Action("Cannon Shot", attributes=["ranged", "physical"], critpower=0.3, effect=50, range=3, vitality_cost=3, menu_pos=0, multiplier=0.55,
                desc="Shooting a large caliber.",
                main_effect={"gfx": "simple_cannon_attack", "sfx": list("content/sfx/sound/be/cannon_%d.mp3"%i for i in xrange(1, 4)), "duration": .5, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        # Blunt Attacks:
        BE_Action("Blunt Strike", attributes=["melee", "physical"],  effect=35, range=1, vitality_cost=1, menu_pos=0.1, multiplier=0.5,
                desc="Hitting with a blunt weapon.",
                main_effect={"gfx": "simple_blunt_attack", "sfx": "content/sfx/sound/be/rod_attack.mp3", "duration": .5, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        BE_Action(u"Ground Shockwave", menu_pos=0.6, range=1, attributes=["melee", "earth", "physical"], effect=100, critpower=0.25, multiplier=1.15, vitality_cost=20,
                desc="Sends a shock wave powerful enough to cause a local earthquake.",
                main_effect={"gfx": "earth_hammer_webm", "sfx": "content/sfx/sound/be/earth_hammer.mp3", "duration": 0.9, "aim": {"point": "bc", "anchor": (.5, 1.0), "xo": 160}, "hflip": True},
                target_sprite_damage_effect={"gfx": "vertical_shake", "initial_pause": 0.5, "duration": 0.6, "master_shake": True},
                target_death_effect={"gfx": "dissolve", "initial_pause": .4, "duration": .5})
        # Axes Attack:
        BE_Action("Axe Strike", attributes=["melee", "physical"], critpower=.1, effect=10, range=1, vitality_cost=2, menu_pos=0, multiplier=0.55,
                desc="Cutting through with an axe.",
                main_effect={"gfx": "simple_axe_attack", "sfx": "content/sfx/sound/be/axe_attack.mp3", "duration": .5, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        MultiAttack("Axe Strike 2X", attributes=["melee", "physical"], critpower=.15, multiplier=0.7, effect=15, range=1, vitality_cost=4, menu_pos=0.1,
                desc="Two quick attacks with an axe.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/axes.png", 150, 150), "sfx": "content/sfx/sound/be/axe_attack.mp3", "duration": .6},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .55},
                target_death_effect={"gfx": "dissolve", "initial_pause": .6, "duration": .5})
        MultiAttack("Axe Strike 4X", attributes=["melee", "physical"], critpower=.2, multiplier=0.85, effect=35, range=1, vitality_cost=7, menu_pos=0.2,
                desc="Four quick attacks with an axe.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/axes.png", 150, 150), "sfx": "content/sfx/sound/be/axe_attack.mp3", "duration": 1.2, "times": 4},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .85},
                target_death_effect={"gfx": "dissolve", "initial_pause": .8, "duration": .5})
        BE_Action(u"Ice Axe Strike", menu_pos=1, range=1, critpower=.2, attributes=["melee", "ice", "physical"], effect=50, multiplier=0.95, vitality_cost=12, mp_cost=4,
                desc="Attack with an ice axe.",
                main_effect={"gfx": "Ice Arrow impact", "sfx": "content/sfx/sound/be/ice_axe.mp3", "duration": 0.7, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "iced_with_shake", "initial_pause": 0.2, "duration": 0.4},
                target_death_effect={"gfx": "dissolve", "initial_pause": .4, "duration": .4})
        # Bite Attacks:
        BE_Action("Bite", attributes=["melee", "physical"], critpower=.3, effect=1, range=1, vitality_cost=1, menu_pos=0, multiplier=0.5,
                desc="Biting with fangs.",
                main_effect={"gfx": "simple_bite_attack", "sfx": "content/sfx/sound/be/bite_attack.mp3", "duration": .5},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        # Gun Attacks:
        BE_Action("Gun Shot", attributes=["ranged", "physical"], critpower=.3, effect=50, range=3, vitality_cost=2, menu_pos=0, multiplier=0.5,
                desc="Shooting a bullet.",
                main_effect={"gfx": "simple_gun_attack", "sfx": "content/sfx/sound/be/gun_attack.mp3", "duration": .5},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        # Scythe Attacks:
        BE_Action("Scythe Slash", attributes=["melee", "physical"], critpower=.5, effect=10, range=1, vitality_cost=2, menu_pos=0, multiplier=0.5,
                desc="Shredding with a scythe.",
                main_effect={"gfx": "simple_scythe_attack", "sfx": "content/sfx/sound/be/scythe_attack.mp3", "duration": .5, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        MultiAttack("Scythe Slash 2X", attributes=["melee", "physical"], critpower=.5, multiplier=0.65, effect=25, range=1, vitality_cost=4, menu_pos=0.1,
                desc="Two quick attacks with a scythe.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/scythe.png", 150, 150), "sfx": "content/sfx/sound/be/scythe_attack.mp3", "duration": 0.6, "times": 2},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .55},
                target_death_effect={"gfx": "dissolve", "initial_pause": .3, "duration": .3})
        MultiAttack("Scythe Slash 4X", attributes=["melee", "physical"], critpower=.5, multiplier=0.8, effect=40, range=1, vitality_cost=6, menu_pos=0.2,
                desc="Four quick attacks with a scythe.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/scythe.png", 150, 150), "sfx": "content/sfx/sound/be/scythe_attack.mp3", "duration": 1.2, "times": 4},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .85},
                target_death_effect={"gfx": "dissolve", "initial_pause": .8, "duration": .5})
        BE_Action(u"Steel Assault", type="all_enemies", range=1, attributes=["melee", "physical"], critpower=0.2, multiplier=1.05, effect=70, vitality_cost=20, menu_pos=1.7,
                desc="Quick consecutive slashes capable to attack multiple enemies.",
                main_effect={"gfx": Transform("chain_scythe_webm", zoom=1.1), "sfx": "content/sfx/sound/be/chop.ogg", "duration": 0.76, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .15, "duration": .7},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": .4})
        ArealSkill(u"Harvesting Time", range=2, attributes=["melee", "darkness", "physical", "poison", "inevitable"], menu_pos=5, critpower=1.0, effect=150, multiplier=1.8, vitality_cost=40, mp_cost=0.1, health_cost=0.1, type="all_enemies",
                desc="By sacrificing some life energy a small piece of the Death powers can be summoned to join the battle.",
                main_effect={"gfx": Transform("death_scythe_webm", zoom=1.2), "sfx": "content/sfx/sound/be/death_skythe.ogg", "duration": 1.46, "aim": {"anchor": (0.5, 0.5), "xo": 180, "yo":-70}, "hflip": True},
                target_death_effect={"gfx": "dissolve", "initial_pause": .6, "duration": .3},
                bg_main_effect={"gfx": "black", "initial_pause": 0, "duration": 1.5},
                target_sprite_damage_effect={"gfx": "on_death", "initial_pause": .3, "duration": 1.25})
        # Spray Attacks:
        BE_Action("Spray", attributes=["ranged", "poison"], critpower=-0.3, effect=100, range=2, vitality_cost=3, menu_pos=0, multiplier=0.5,
                desc="Spraying a dangerous substance.",
                main_effect={"gfx": "simple_spray_attack", "sfx": "content/sfx/sound/be/spray_attack.mp3", "duration": 1.0, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .5, "duration": .5})
        # Throw attacks:
        BE_Action("Throw", attributes=["ranged", "physical"], effect=5, range=3, vitality_cost=1, menu_pos=0, multiplier=0.5,
                desc="Throwing a projectile.",
                main_effect={"gfx": "simple_throw_attack", "sfx": list("content/sfx/sound/be/throwing_attack_%d.mp3"%i for i in xrange(1, 3)), "duration": .5, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        ArrowsSkill("Shadow Shuriken", menu_pos=0.5, attributes=["ranged", "darkness"], effect=60, critpower=.5, multiplier=0.95, mp_cost=.05, vitality_cost=15, range=4, piercing=True,
                desc="Throwing explosive shadow projectile.",
                firing_effects={"gfx": "shuriken_throw_webm", "sfx": "content/sfx/sound/be/kunai_throw.mp3"},
                projectile_effects={"gfx": "shuriken_fly_webm", "sfx": None, "duration": 0.4},
                main_effect={"gfx": "shuriken_hit_webm", "sfx": "content/sfx/sound/be/kunai_exp.mp3", "duration": 0.51, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.021},
                target_sprite_damage_effect={"gfx": "on_dark_with_shake", "initial_pause": .01, "duration": .3},
                target_death_effect={"gfx": "dissolve", "initial_pause": .3, "duration": .5},
                dodge_effect={"initial_pause": .05, "duration": 1.5})
        BE_Action(u"Cloud of Knives", range=3, attributes=["ranged", "physical"], critpower=.4, effect=100, multiplier=1.05, vitality_cost=15, menu_pos=0.5,
                desc="Throwing multiple knives in quick succession.",
                main_effect={"gfx": Transform("throwing_knives_webm", zoom=1.3), "sfx": "content/sfx/sound/be/knives_cloud.mp3", "duration": 1.96, "aim": {"point": "center", "anchor": (.5, .5)}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .1, "duration": 1.8},
                target_death_effect={"gfx": "dissolve", "initial_pause": .5, "duration": 0.8})
        # Whip Attacks:
        BE_Action("Whip Strike", attributes=["melee", "physical"], critpower=.1, effect=4, range=1, vitality_cost=1, menu_pos=0, multiplier=0.5,
                desc="Lashing with a whip.",
                main_effect={"gfx": "simple_whip_attack", "sfx": list("content/sfx/sound/be/whip_attack_%d.mp3"%i for i in xrange(1, 3)), "duration": .5, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .5})
        MultiAttack("Whip Strike 2X", attributes=["melee", "physical"], critpower=.1, multiplier=0.6, effect=15, range=1, menu_pos=0.1, vitality_cost=3,
                desc="Two quick attacks with a whip.",
                main_effect={"gfx": ProportionalScale("content/gfx/be/whip.png", 150, 150), "sfx": "content/sfx/sound/be/whip_attack_1.mp3", "duration": 0.6, "times": 2},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": .05, "duration": .55},
                target_death_effect={"gfx": "dissolve", "initial_pause": .3, "duration": .3})
        BE_Action(u"Shocker Whip", menu_pos=1.4, range=1, attributes=["melee", "electricity", "physical"], effect=70, critpower=.5, multiplier=1.1, vitality_cost=8, mp_cost=0.1,
                desc="A whip attack charged with electricity. Double pleasure, double pain.",
                main_effect={"gfx": "shock_whip_webm", "sfx": "content/sfx/sound/be/shock_whip.ogg", "duration": 1.36, "aim": {"point": "center", "anchor": (.5, .5), "xo": 180}, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.5, "duration": 0.5},
                target_death_effect={"gfx": "dissolve", "initial_pause": .7, "duration": .5})



    ##### Magic:
        # Fire:
        BE_Action(u"Fire", menu_pos=0, attributes=["magic", "fire"], effect=10, multiplier=1.0, type="all_enemies", mp_cost=10, range=4,
                desc="Ignites a small plot of land.",
                attacker_effects={"gfx": "fire_1", "sfx": "default"},
                main_effect={"gfx": Transform("fire_1", zoom=1.7), "sfx": "content/sfx/sound/be/fire4.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 75}},
                target_sprite_damage_effect={"gfx": "on_fire_with_shake", "initial_pause": 0.1, "duration": 1.7},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 1.5})
        BE_Action(u"Fira", menu_pos=0.1, attributes=["magic", "fire"], effect=10, multiplier=1.1, mp_cost=8, range=4,
                desc="Ignites the air in a limited area.",
                attacker_effects = {"gfx": "fire_1", "sfx": "default"},
                main_effect={"gfx": Transform("fire_2", zoom=1.5), "sfx": "content/sfx/sound/be/fire4.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                target_sprite_damage_effect={"gfx": "on_fire_with_shake", "initial_pause": 0.1, "duration": 1.3},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.7, "duration": 1.2})
        BE_Action(u"Firaga", menu_pos=0.2, attributes=["magic", "fire"], effect=10, multiplier=0.9, mp_cost=12, range=4, piercing=True,
                desc="Creates liquid fire that envelopes the target, causing massive burns.",
                attacker_effects={"gfx": "fire_1", "sfx": "default"},
                main_effect={"gfx": Transform("fire_4", zoom=1.5), "sfx": "content/sfx/sound/be/fire6.mp3", "duration": 5.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                target_sprite_damage_effect={"gfx": "on_fire_with_shake", "initial_pause": 1.3, "duration": 3.6},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.3},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 1.5})
        BE_Action(u"Firaja", menu_pos=0.3, attributes=["magic", "fire"], effect=6, multiplier=0.8, mp_cost=15, range=4, type="all_enemies", piercing=True,
                desc="Creates a rain of fire that hits all enemies.",
                attacker_effects={"gfx": "fire_1", "sfx": "default"},
                main_effect={"gfx": Transform("fire_3", zoom=1.5), "sfx": "content/sfx/sound/be/fire5.mp3", "duration": 3.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                target_sprite_damage_effect={"gfx": "on_fire_with_shake", "initial_pause": 0.2, "duration": 3.0},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.3},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 1.5})
        P2P_Skill(u"Fireball", menu_pos=0.5, attributes=["magic", "fire"], effect=50, multiplier=1.3, mp_cost=30, range=4, piercing=True,
                desc="Launches an exploding fireball at one enemy.",
                projectile_effects={"gfx": "fire_6", "sfx": "content/sfx/sound/be/fire7.mp3", "duration": 1.0},
                main_effect={"gfx": Transform("fire_6_1", zoom=1), "sfx": None, "duration": 1.2, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                attacker_effects={"gfx": "fire_2", "sfx": "default"},
                target_sprite_damage_effect={"gfx": "burning_with_shake", "initial_pause": 0.1, "duration": 0.7},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.1, "duration": 0.5},
                dodge_effect={"initial_pause": .1})
        P2P_Skill(u"Self-Division", menu_pos=0.5, attributes=["magic", "fire"], effect=50, multiplier=1.2, mp_cost=1, range=4, piercing=True, # should be unavailable for player, made specially for a boss
                desc="Launches an exploding fireball filled with twisted energy at one enemy.",
                projectile_effects={"gfx": "Blazing_Star_fireball_webm", "sfx": "content/sfx/sound/be/fire7.mp3", "duration": 0.667},
                main_effect={"gfx": Transform("fire_6_1", zoom=1), "sfx": None, "duration": 1.2, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                target_sprite_damage_effect={"gfx": "burning_with_shake", "initial_pause": 0.1, "duration": 0.7},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.1, "duration": 0.5},
                dodge_effect={"initial_pause": .1})
        P2P_Skill(u"Solar Flash", menu_pos=1, attributes=["magic", "fire"], effect=50, multiplier=1.4, mp_cost=50, range=4,
                desc="Sends towards the target a small piece of solar plasma.",
                projectile_effects={"gfx": "fire_5", "sfx": "content/sfx/sound/be/fire7.mp3", "duration": 1.0},
                main_effect={"gfx": Transform("fire_5_1", zoom=1), "duration": 1.5},
                attacker_effects={"gfx": "fire_2", "sfx": "default"},
                target_sprite_damage_effect={"gfx": "burning_with_shake", "initial_pause": 0.1, "duration": 0.7},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 0.5},
                dodge_effect={"initial_pause": .1})
        BE_Action("Meteor", menu_pos=5, attributes=["magic", "fire"], effect=50, multiplier=1.2, mp_cost=70, range=4, type="all_enemies",
                desc="Summons flaming fragments of meteor.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": Transform("cataclysm_sideways", xzoom=-1), "sfx": "content/sfx/sound/be/fire8.mp3", "duration": 1.8, "aim": {"point": "bc", "anchor": (0.5, 0.1), "xo": 150, "yo": -370}, "hflip": True},
                target_sprite_damage_effect={"gfx": "burning_with_shake", "initial_pause": 1.2, "duration": 0.6, "master_shake": True},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.3},
                target_death_effect={"gfx": "dissolve",  "initial_pause": 1.4, "duration": 0.5},
                dodge_effect={"initial_pause": .8})
        ArealSkill("Flame Vortex", menu_pos=8, attributes=["magic", "fire", "air", "inevitable"], effect=75, multiplier=1.35, mp_cost=0.2, vitality_cost=25, range=4, type="all_enemies",
                desc="Sizzling hot air flow burns everything on the way.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": "flame_vortex_webm", "sfx": "content/sfx/sound/be/fire9.mp3", "duration": 1.367, "aim": {"anchor": (0.5, 1.0), "xo": 300 ,"yo": 150}, "hflip": True},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.7},
                target_sprite_damage_effect={"gfx": "burning_with_shake", "initial_pause": 0.2, "duration": 1.0},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.2, "duration": 0.16})
        ArealSkill("Cataclysm", menu_pos=9, attributes=["magic", "fire", "inevitable"], effect=100, multiplier=1.5, mp_cost=100, range=4, type="all_enemies", piercing=True,
                desc="A massive spontaneous air combustion capable of causing destruction on a large scale.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": Transform("cataclysm_webm", zoom=0.85), "sfx": "content/sfx/sound/be/fire2.mp3", "duration": 4.93, "aim": {"anchor": (0.5, 1.0), "yo": 330}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 4.8},
                target_sprite_damage_effect={"gfx": "burning_with_shake", "initial_pause": 2, "duration": 2.5, "master_shake": True},
                target_death_effect={"gfx": "hide", "initial_pause": 3.0, "duration": 0.0001},
                bg_main_effect={"gfx": "mirage", "initial_pause": 2.6, "duration": 2})
        # Water:
        BE_Action(u"Water", menu_pos=0, attributes=["magic", "water"], effect=10, multiplier=1.0, mp_cost=10, range=4, type="all_enemies",
                desc="Crushes targets by bubbles of water.",
                attacker_effects={"gfx": "water_1", "sfx": "default"},
                main_effect={"gfx": Transform("water_1", zoom=1.1), "sfx": "content/sfx/sound/be/water.mp3", "duration": 1.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "true_water", "sfx": None, "initial_pause": 0.1, "duration": 1.4},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 0.11, "duration": 0.9})
        BE_Action(u"Watera", menu_pos=0.1, attributes=["magic", "water"], effect=10, multiplier=1.1, mp_cost=8, range=4,
                desc="High pressure water jets pierce through the target.",
                attacker_effects={"gfx": "water_1", "sfx": "default"},
                main_effect={"gfx": Transform("water_2", zoom=1.4), "sfx": "content/sfx/sound/be/water.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "true_water", "sfx": None, "initial_pause": 0.1, "duration": 1.4},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})
        BE_Action(u"Waterga", menu_pos=0.2, attributes=["magic", "water"], effect=10, multiplier=0.9, mp_cost=12, range=4,
                desc="A cloud of water droplets at high speed crashes into the target.",
                attacker_effects={"gfx": "water_1", "sfx": "default"},
                main_effect={"gfx": Transform("water_3", zoom=1.5), "sfx": "content/sfx/sound/be/water2.mp3", "duration": 2.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "true_water", "sfx": None, "initial_pause": 0.1, "duration": 1.9},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})
        BE_Action(u"Waterja", menu_pos=0.3, attributes=["magic", "water"], effect=10, multiplier=0.8, mp_cost=15, range=4, type="all_enemies", piercing=True,
                desc="Creates a powerful burst of water and steam from the ground.",
                attacker_effects={"gfx": "water_1", "sfx": "default"},
                main_effect={"gfx": Transform("water_4", zoom=1.5), "sfx": "content/sfx/sound/be/water3.mp3", "duration": 2.25, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_water", "sfx": None, "initial_pause": 0.3, "duration": 1.9},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None, "initial_pause": 2.2},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.2, "duration": .5})
        BE_Action(u"Last Drop", menu_pos=0.5, attributes=["magic", "water"], effect=50, multiplier=1.3, mp_cost=30, piercing=True, range=6,
                desc="Hits the target with a massive water blast from above.",
                attacker_effects={"gfx": "water_2", "sfx": "default"},
                main_effect={"gfx": Transform("water_6", zoom=1.9), "sfx": "content/sfx/sound/be/water5.mp3", "duration": 5.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 60}},
                target_sprite_damage_effect={"gfx": "on_water", "initial_pause": 1.0, "duration": 3.5},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.1},
                target_death_effect={"gfx": "dissolve", "initial_pause": 4.5, "duration": 0.5})
        BE_Action(u"Geyser", menu_pos=1, attributes=["magic", "water"], effect=50, multiplier=1.4, mp_cost=50, range=6,
                desc="A powerful stream of water shoots out of the ground directly beneath the target.",
                attacker_effects={"gfx": "water_2", "sfx": "default"},
                main_effect={"gfx": Transform("water_5", zoom=1.9), "sfx": "content/sfx/sound/be/water6.mp3", "duration": 3.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 60}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "true_water", "sfx": None, "initial_pause": 0.5, "duration": 2.5},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None, "initial_pause": 2.2},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.2, "duration": .5})
        BE_Action(u"Heavy Rain", menu_pos=5, attributes=["magic", "water"], effect=50, multiplier=1.2, mp_cost=70, type="all_enemies", range=6,
                desc="Summons a rain of extra heavy water from another dimension.",
                attacker_effects={"gfx": "water_2", "sfx": "default"},
                main_effect={"gfx": Transform("rain", zoom=2.0), "sfx": "content/sfx/sound/be/heavy_rain.mp3", "duration": 5.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 80}, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 1.0, "duration": 3.8, "master_shake": True},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 4.5},
                target_death_effect={"gfx": "dissolve", "initial_pause": 4.5, "duration": 0.5})
        ATL_ArealSkill(u"High Tide", menu_pos=9, attributes=["magic", "water", "inevitable"], effect=100, multiplier=1.5, mp_cost=100, piercing=True, range=6, type="all_enemies",
                desc="A huge tidal wave instantly crashes all enemies.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"atl": water_combined, "predict": ["water_attack", "water_wave"], "left_args": [1.8, -300], "right_args": [-1.8, 300], "sfx": "content/sfx/sound/be/water7.mp3", "duration": 1.6},
                target_sprite_damage_effect={"gfx": "on_water_with_shake", "initial_pause": .6, "duration": .9},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.6},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})

        # Ice:
        BE_Action(u"Blizzard", menu_pos=0, attributes=["magic", "ice"], effect=10, multiplier=1.0, mp_cost=10, range=4, type="all_enemies",
                desc="Creates a cloud of sharp ice splinters.",
                attacker_effects={"gfx": "ice_1", "sfx": "default"},
                main_effect={"gfx": Transform("ice_1", zoom=1.9), "sfx": "content/sfx/sound/be/ice3.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 60}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.2, "duration": 1.8},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.5, "duration": 0.4})
        BE_Action(u"Blizzara", menu_pos=0.1, attributes=["magic", "ice"], effect=10, multiplier=1.1, mp_cost=8, range=4,
                desc="Ice blades grow out of the ground.",
                attacker_effects={"gfx": "ice_1", "sfx": "default"},
                main_effect={"gfx": Transform("ice_2", zoom=1.3), "sfx": "content/sfx/sound/be/ice1.mp3", "duration": 1.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 80}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "iced_with_shake", "initial_pause": 0.1, "duration": 1.35},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.0, "duration": 0.4})
        BE_Action(u"Blizzarga", menu_pos=0.2, attributes=["magic", "ice"], effect=10, multiplier=0.9, mp_cost=12, range=4,
                desc="Freezes the air itself around the target, creating deadly ice blades.",
                attacker_effects={"gfx": "ice_1", "sfx": "default"}, piercing=True,
                main_effect={"gfx": Transform("ice_4", zoom=1.5), "sfx": "content/sfx/sound/be/ice2.mp3", "duration": 0.8, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "iced_with_shake", "initial_pause": 0.1, "duration": 0.7},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 0.6, "duration": 0.3})
        BE_Action(u"Blizzarja", menu_pos=0.3, attributes=["magic", "ice"], effect=10, multiplier=0.9, mp_cost=15, range=4,
                desc="Quickly draws heat from a small area.",
                attacker_effects={"gfx": "ice_1", "sfx": "default"}, piercing=True, type="all_enemies",
                main_effect={"gfx": Transform("ice_3", zoom=1.7), "sfx": "content/sfx/sound/be/ice2.mp3", "duration": 1.25, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 60}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "frozen", "initial_pause": 0.1, "duration": 1.1},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 0.6, "duration": 0.3})
        BE_Action("Ice Blast", menu_pos=0.5, attributes=["magic", "ice"], effect=50, multiplier=1.3, mp_cost=30, range=4, piercing=True, type="se",
                desc="Summons frozen fragments of meteor.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": Transform("ice_blast", xzoom=-1), "sfx": "content/sfx/sound/be/ice5.mp3", "duration": 2.3, "aim": {"point": "bc", "anchor": (0.5, 0.1), "xo": 120, "yo": -370}, "hflip": True},
                target_sprite_damage_effect={"gfx": "iced_with_shake", "initial_pause": 1.6, "duration": 0.5},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.5},
                target_death_effect={"gfx": "dissolve",  "initial_pause": 2.0, "duration": 0.5},
                dodge_effect={"initial_pause": .8})
        BE_Action(u"Zero Prism", menu_pos=1, attributes=["magic", "ice"], effect=50, multiplier=1.4, mp_cost=50, range=4,
                desc="Freezes the target into a solid ice block.",
                attacker_effects={"gfx": "ice_2", "sfx": "default"},
                main_effect={"gfx": Transform("ice_5", zoom=2.1), "sfx": "content/sfx/sound/be/ice4.mp3", "duration": 2.1, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 110}},
                target_sprite_damage_effect={"gfx": "frozen", "initial_pause": 0.3, "duration": 1.5},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.2},
                target_death_effect={"gfx": "shatter", "initial_pause": 1.4, "duration": 0.5})
        BE_Action(u"Ice Shards", menu_pos=2, attributes=["magic", "ice"], effect=65, multiplier=1.25, mp_cost=70, range=4, type="all_enemies",
                desc="Small part of the target immediately freezes and explodes.",
                attacker_effects={"gfx": "ice_2", "sfx": "default"},
                main_effect={"gfx": Transform("ice_6", zoom=2.0), "sfx": "content/sfx/sound/be/ice2.mp3", "duration": 1.2, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 80}},
                target_sprite_damage_effect={"gfx": "iced", "initial_pause": 0.1, "duration": 1.1},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.2},
                target_death_effect={"gfx": "shatter", "initial_pause": 0.5, "duration": 0.2})
        BE_Action(u"Hailstorm", menu_pos=5, attributes=["magic", "ice"], effect=50, multiplier=1.35, mp_cost=60, range=4, piercing=True, type="all_enemies",
                desc="Puts targets in a middle of a small, but violent snow storm.",
                attacker_effects={"gfx": "ice_2", "sfx": "default"},
                main_effect={"gfx": Transform("ice_7", zoom=1.7), "sfx": "content/sfx/sound/be/Hailstorm.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 50}, "hflip": True},
                target_sprite_damage_effect={"gfx": "iced", "initial_pause": 0.2, "duration": 1.8},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.2},
                target_death_effect={"gfx": "shatter", "initial_pause": 1.9, "duration": 0.5})
        ATL_ArealSkill("Ice Storm", menu_pos=9, attributes=["magic", "ice", "inevitable"], effect=100, multiplier=1.5, mp_cost=100, range=4, type="all_enemies", piercing=True,
                desc="Conjures a power ice storm from a remote ice planet.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"atl": ice_storm, "predict": ["ice_twin_explosion", "ice_strike"], "sfx": "content/sfx/sound/be/ice2.mp3", "duration": 1.7, "left_args": [(190, 700)], "right_args": [(1035, 700)]},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.7},
                target_sprite_damage_effect={"gfx": "iced_with_shake", "initial_pause": 0.6, "duration": 1.0, "master_shake": True},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})
        # Earth:
        BE_Action(u"Stone", menu_pos=0, attributes=["magic", "earth"], effect=10, multiplier=1.0, mp_cost=10, range=4, type="all_enemies",
                desc="Creates cloud of fragments of hardened clay.",
                attacker_effects={"gfx": "earth_1", "sfx": "default"},
                main_effect={"gfx": Transform("earth_1", zoom=1.4), "sfx": "content/sfx/sound/be/earth.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "vertical_shake", "initial_pause": 0.1, "duration": 1.7},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.5, "duration": 0.5})
        BE_Action(u"Stonera", menu_pos=0.1, attributes=["magic", "earth"], effect=10, multiplier=1.1, mp_cost=8, range=4,
                desc="Creates a sharp stone spike.",
                attacker_effects={"gfx": "earth_1", "sfx": "default"},
                main_effect={"gfx": "earth_2", "sfx": "content/sfx/sound/be/earth.mp3", "duration": 1.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 10}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "vertical_shake", "initial_pause": 0.1, "duration": 0.8},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 0.6, "duration": 0.5})
        BE_Action(u"Stonega", menu_pos=0.2, attributes=["magic", "earth"], effect=10, multiplier=0.9, mp_cost=12, range=4, piercing=True,
                desc="A small amount of magma moves to the surface, spilling on the target.",
                attacker_effects={"gfx": "earth_1", "sfx": "default"},
                main_effect={"gfx": Transform("earth_3", zoom=1.2), "sfx": "content/sfx/sound/be/earth3.mp3", "duration": 1.5, "aim": {"point": "bc", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "vertical_shake", "initial_pause": 0.1, "duration": 1.2},
                target_damage_effect={"gfx": "battle_bounce"},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.2, "duration": 0.3})
        BE_Action(u"Stoneja", menu_pos=0.3, attributes=["magic", "earth"], effect=10, multiplier=0.8, mp_cost=15, range=4, piercing=True, type="all_enemies",
                desc="Small part of the target becomes stone and shatters into a thousand pieces.",
                attacker_effects={"gfx": "earth_1", "sfx": "default"},
                main_effect={"gfx": Transform("earth_4", zoom=1.2), "sfx": "content/sfx/sound/be/earth2.mp3", "duration": 1.2, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 0.9},
                target_damage_effect={"gfx": "battle_bounce"},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.9, "duration": 0.3})
        BE_Action(u"Breach", menu_pos=0.5, attributes=["magic", "earth"], effect=50, multiplier=1.3, mp_cost=30, range=4, piercing=True,
                desc="Hot dust and poisonous gases are pulled out of the ground under high pressure.",
                attacker_effects={"gfx": "earth_2", "sfx": "default"},
                main_effect={"gfx": Transform("earth_5_webm", zoom=1.5), "sfx": "content/sfx/sound/be/earth4.mp3", "duration": 0.86, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 0}},
                target_sprite_damage_effect={"gfx": "vertical_shake", "initial_pause": 0.1, "duration": 0.8},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.7},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.7, "duration": 0.15})
        BE_Action(u"Transmutation", menu_pos=1, attributes=["magic", "earth"], effect=50, multiplier=1.4, mp_cost=50, range=4,
                desc="The land itself under the target becomes explosive and detonates.",
                attacker_effects={"gfx": "earth_2", "sfx": "default"},
                main_effect={"gfx": Transform("earth_6", zoom=1.5), "sfx": "content/sfx/sound/be/earth4.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 50}},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.2, "duration": 1.8},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.7},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.7, "duration": 0.3},
                dodge_effect={"initial_pause": .2})
        BE_Action(u"Rift Line", menu_pos=5, attributes=["magic", "earth"], effect=50, multiplier=1.2, mp_cost=65, range=4, type="all_enemies",
                desc="Brings a small flow of magma to the surface.",
                attacker_effects={"gfx": "earth_2", "sfx": "default"},
                main_effect={"gfx": Transform("magma", zoom=2.0), "sfx": "content/sfx/sound/be/rift_line.mp3", "duration": 3.2, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 75}},
                target_sprite_damage_effect={"gfx": "vertical_shake", "master_shake": True, "initial_pause": 0.7, "duration": 2.2},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.8},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})
        ArealSkill("Fist of Bethel", menu_pos=9, menuname="FoB", attributes=["magic", "earth", "inevitable"], effect=100, multiplier=1.5, mp_cost=100, range=4, type="all_enemies", piercing=True,
                desc="The fist of an ancient underground deity crashes all enemies.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": Transform(Transform("crushing_hand", xzoom=-1.0), zoom=2), "sfx": "content/sfx/sound/be/earth7.mp3", "duration": 2.7, "aim": {"anchor": (0.5, 1.0), "xo": 0 ,"yo": 150}, "hflip": True},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.7},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 1.0, "duration": 1.7, "master_shake": True},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 0.5},
                bg_main_effect={"gfx": "black", "initial_pause": 0, "duration": 2.7})
        # Air:
        BE_Action(u"Aero", menu_pos=0, attributes=["magic", "air"], effect=10, multiplier=1.0, mp_cost=10, range=4, type="all_enemies",
                desc="High pressure air cuts through armor and flesh like a hardened blade.",
                attacker_effects={"gfx": "air_1", "sfx": "default"},
                main_effect={"gfx": Transform("air_1", zoom=1.2), "sfx": "content/sfx/sound/be/air2.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 1.3},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.2, "duration": 0.3})
        BE_Action(u"Aerora", menu_pos=0.1, attributes=["magic", "air"], effect=10, multiplier=1.1, mp_cost=8, range=4,
                desc="Causes damage by sand and branches picked up by the wind rather than air itself.",
                attacker_effects={"gfx": "air_1", "sfx": "default"},
                main_effect={"gfx": Transform("air_5", zoom=1.3), "sfx": "content/sfx/sound/be/air1.mp3", "duration": 0.9, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_air", "initial_pause": 0.1, "duration": 0.8},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 0.7, "duration": 0.2})
        BE_Action(u"Aeroga", menu_pos=0.2, attributes=["magic", "air"], effect=10, multiplier=0.9, mp_cost=12, range=4, piercing=True,
                desc="Even for those who don't need to breathe instantaneous air pressure drop is dangerous.",
                attacker_effects={"gfx": "air_1", "sfx": "default"},
                main_effect={"gfx": Transform("air_2", zoom=1.2), "sfx": "content/sfx/sound/be/air3.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 1.3},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.0, "duration": 0.3})
        BE_Action(u"Aeroja", menu_pos=0.3, attributes=["magic", "air"], effect=10, multiplier=0.8, mp_cost=15, range=4, piercing=True, type="all_enemies",
                desc="High pressure air flows cover a small area.",
                attacker_effects={"gfx": "air_1", "sfx": "default"},
                main_effect={"gfx": Transform("air_3", zoom=1.4), "sfx": "content/sfx/sound/be/air2.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 1.2},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.0, "duration": 0.3})
        BE_Action(u"Pressure", menu_pos=0.5, attributes=["magic", "air"], effect=50, multiplier=1.3, mp_cost=30, range=4,piercing=True,
                desc="Pumps air from the target, crushing it by external atmospheric pressure.",
                attacker_effects={"gfx": "air_2", "sfx": "default"},
                main_effect={"gfx": Transform("air_4", zoom=1.2), "sfx": "content/sfx/sound/be/air3.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_air", "initial_pause": 0.1, "duration": 1.3},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.0, "duration": 0.3})
        BE_Action(u"Air Blast", menu_pos=1, attributes=["magic", "air"], effect=50, multiplier=1.4, mp_cost=50, range=4,
                desc="Pumps air into the target, tearing it from the inside.",
                attacker_effects={"gfx": "air_2", "sfx": "default"},
                main_effect={"gfx": Transform("air_6", zoom=1.5), "sfx": "content/sfx/sound/be/air3.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 1.3},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.0},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.0, "duration": 0.3})
        BE_Action(u"Vortex", menu_pos=2, attributes=["magic", "air"], effect=50, multiplier=1.2, mp_cost=70, range=4, type="all_enemies",
                desc="Creates a small, but very powerful sphere of hurricane winds around the target.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": Transform("vortex", zoom=2.2), "sfx": "content/sfx/sound/be/vortex.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                 target_sprite_damage_effect={"gfx": "on_air", "initial_pause": 0.1, "duration": 1.4, "master_shake": True},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.0},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 1.0, "duration": 0.3})
        ArealSkill("Northern Flow", menu_pos=4.2, attributes=["magic", "air", "ice"], effect=120, multiplier=1.2, mp_cost=60, range=4, type="all_enemies", piercing=True, true_pierce=True,
                desc="Summons a flow of frozen air from the upper atmosphere. Ignores back row damage reduction.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": "north_webm", "sfx": "content/sfx/sound/be/air5.mp3", "duration": 3.8, "aim": {"anchor": (.5, .5)}, "hflip": True},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.1, "duration": 0.1},
                target_sprite_damage_effect={"gfx": "iced", "initial_pause": 0.1, "duration": 3.7},
                target_death_effect={"gfx": "dissolve",  "initial_pause": 3.7, "duration": 0.2})
        ArealSkill("Tornado", menu_pos=9, attributes=["magic", "air", "inevitable"], effect=100, multiplier=1.5, mp_cost=100, range=4, type="all_enemies", piercing=True,
                desc="Conjures a full-fledged but short-lived tornado to wipe out all enemies.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": "tornado", "sfx": "content/sfx/sound/be/air4.mp3", "duration": 3.5, "aim": {"anchor": (0.5, 1.0), "yo": 150}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 4.8},
                target_sprite_damage_effect={"gfx": "fly_away", "initial_pause": 0.2, "duration": 5.1},
                target_death_effect={"gfx": "shatter", "initial_pause": 4.7, "duration": 0.2})
        # Electricity:
        BE_Action(u"Thunder", menu_pos=0, attributes=["magic", "electricity"], effect=10, multiplier=1.0, mp_cost=10, range=4, type="all_enemies",
                desc="Shocks targets with static electricity caused by friction of airborne particles.",
                attacker_effects={"gfx": "electricity_1", "sfx": "default"},
                main_effect={"gfx": Transform("electricity_1", zoom=1.5), "sfx": "content/sfx/sound/be/thunder2.mp3", "duration": 1.0, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.2, "duration": 0.6},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 0.3, "duration": 0.6})
        BE_Action(u"Thundara", menu_pos=0.1, attributes=["magic", "electricity"], effect=10, multiplier=1.1, mp_cost=8, range=4,
                desc="Surrounds the target by brief electricity field.",
                attacker_effects={"gfx": "electricity_1", "sfx": "default"},
                main_effect={"gfx": Transform("electricity_2", zoom=1.7), "sfx": "content/sfx/sound/be/thunder4.mp3", "duration": 1.2, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 50}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.1, "duration": 1.1},
                target_damage_effect={"gfx": "battle_bounce"},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.9, "duration": 0.3})
        BE_Action(u"Thundaga", menu_pos=0.2, attributes=["magic", "electricity"], effect=10, multiplier=0.9, mp_cost=12, range=4,
                desc="Creates a plasma ball of ionized hot air near the target.",
                attacker_effects={"gfx": "electricity_1", "sfx": "default"}, piercing=True,
                main_effect={"gfx": Transform("electricity_4", zoom=1.8), "sfx": "content/sfx/sound/be/thunder3.mp3", "duration": 0.6, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.05, "duration": 0.7},
                target_damage_effect={"gfx": "battle_bounce"},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.4, "duration": 0.3})
        BE_Action(u"Thundaja", menu_pos=0.3, attributes=["magic", "electricity"], effect=10, multiplier=0.8, mp_cost=15, range=4,
                desc="Covers a small area by lightning discharges.",
                attacker_effects={"gfx": "electricity_1", "sfx": "default"}, piercing=True, type="all_enemies",
                main_effect={"gfx": Transform("electricity_3", zoom=2.2), "sfx": "content/sfx/sound/be/thunder.mp3", "duration": 1.35, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 50}, "start_at": 0, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.2, "duration": 1.0},
                target_damage_effect={"gfx": "battle_bounce"},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.2})
        P2P_Skill(u"Ion Blast", menu_pos=0.5, attributes=["magic", "electricity"], effect=50, multiplier=1.3, mp_cost=30, range=4, piercing=True,
                desc="Hits target with cloud of charged particles.",
                projectile_effects={"gfx": "ion_1", "sfx": "content/sfx/sound/be/ion_storm.mp3", "duration": 1.0},
                main_effect={"gfx": "ion", "sfx": None, "duration": 2.25},
                attacker_effects={"gfx": "orb", "sfx": "default"},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.3, "duration": 1.4},
                target_death_effect={"gfx": "hide", "initial_pause": 0.7, "duration": 0.01},
                dodge_effect={"initial_pause": .1})
        BE_Action(u"Electromagnetism", menu_pos=1, attributes=["magic", "electricity"], menuname="EM", effect=50, multiplier=1.4, mp_cost=50, range=4,
                desc="Takes control over charged particles inside the target, causing severe internal injuries.",
                attacker_effects={"gfx": "electricity_2", "sfx": "default"}, dodge_effect={"initial_pause": .2},
                main_effect={"gfx": Transform("electricity_6", zoom=1.8), "sfx": "content/sfx/sound/be/thunder6.mp3", "duration": 3.2, "aim": {"point": "tc", "anchor": (0.5, 0.5), "yo": 15}, "start_at": 0, "hflip": True},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.3, "duration": 2.9},
                target_damage_effect={"gfx": "battle_bounce"},
                target_death_effect={"gfx": "dissolve", "initial_pause": 3.0, "duration": 0.2})
        BE_Action(u"Thunderstorm", menu_pos=2, attributes=["magic", "electricity"], menuname="TStorm", effect=50, multiplier=1.2, mp_cost=70, range=4,
                desc="Covers a small area by numerous high-voltage discharges.",
                attacker_effects={"gfx": "electricity_2", "sfx": "default"}, type="all_enemies", dodge_effect={"initial_pause": .2},
                main_effect={"gfx": Transform("electricity_5", zoom=1.6), "sfx": "content/sfx/sound/be/thunder5.mp3", "duration": 1.6, "aim": {"point": "tc", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.15, "duration": 1.45},
                target_damage_effect={"gfx": "battle_bounce"},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.2})
        P2P_ArealSkill(u"Ion Storm", menu_pos=5, attributes=["magic", "electricity"], effect=50, multiplier=1.1, mp_cost=60, range=4, piercing=True, type="all_enemies",
                desc="Hits the targets with raging cloud of charged particles.",
                projectile_effects={"gfx": "ion_1", "sfx": "content/sfx/sound/be/ion_storm.mp3", "duration": 1.0},
                main_effect={"gfx": Transform("ion", zoom=2.0), "sfx": None, "duration": 2.25, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                attacker_effects={"gfx": "orb", "sfx": "default"},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.3, "duration": 1.4},
                target_death_effect={"gfx": "hide", "initial_pause": 0.7, "duration": 0.01},
                dodge_effect={"initial_pause": .1})
        BE_Action("Full Discharge", menuname="F Discharge", menu_pos=4.3, attributes=["magic", "electricity", "water"], effect=75, multiplier=1.35, mp_cost=80, range=4, piercing=True, true_pierce=True,
                desc="Hits the target with magically concentrated and amplified burst of atmospheric electricity. Ignores back row damage reduction.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": Transform("thunder_storm_2", xzoom=1.2, yzoom=1.3), "start_at": 0, "sfx": "content/sfx/sound/be/thunder5.mp3", "duration": 1.6, "aim": {"point": "bc", "anchor": (0.5, 1.0), "xo": 0 ,"yo": 30}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.5},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.4, "duration": 1.2, "master_shake": True},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.8, "duration": 0.4},
                bg_main_effect={"gfx": "black", "initial_pause": 0, "duration": 2.3},
                dodge_effect={"initial_pause": .3})
        ArealSkill("Thunderstorm Front", menu_pos=9, menuname="T Front", attributes=["magic", "electricity", "inevitable"], effect=100, multiplier=1.5, mp_cost=100, range=4, type="all_enemies", piercing=True,
                desc="Releases a full-scale thunderstorm incinerating enemies with countless lightnings.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": Transform("moz_stretch", zoom=.7), "sfx": "content/sfx/sound/be/thunder7.mp3", "duration": 3.4, "aim": {"anchor": (0.5, 1.0), "yo": 150}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 3.4},
                target_sprite_damage_effect={"gfx": "on_ele_with_shake", "initial_pause": 0.5, "duration": 2.5, "master_shake": True},
                target_death_effect={"gfx": "dissolve", "initial_pause": 2.4, "duration": 0.5})
        # Light:
        BE_Action(u"Holy", menu_pos=0, attributes=["magic", "light"], effect=15, multiplier=1.0, mp_cost=12, range=4, type="all_enemies",
                desc="A flash of light energy burns targets from inside.",
                attacker_effects={"gfx": "light_1", "sfx": "default"},
                main_effect={"gfx": Transform("light_1", zoom=1.5), "sfx": "content/sfx/sound/be/light1.mp3", "duration": 1.25, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_light_with_shake", "initial_pause": 0.1, "duration": 1.1},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause":0.9, "duration": 0.2})
        BE_Action(u"Holyra", menu_pos=0.1, attributes=["magic", "light"], effect=15, multiplier=1.1, mp_cost=10, range=4,
                desc="A sphere of light energy burns the target from all sides.",
                attacker_effects={"gfx": "light_1", "sfx": "default"},
                main_effect={"gfx": Transform("light_2", zoom=1.5), "sfx": "content/sfx/sound/be/light3.mp3", "duration": 1.25, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_light_with_shake", "initial_pause": 0.1, "duration": 1.1},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause":0.9, "duration": 0.2})
        BE_Action(u"Holyda", menu_pos=0.2, attributes=["magic", "light"], effect=15, multiplier=0.9, mp_cost=14, range=4,
                desc="A smallest particle of stellar energy burns the target.",
                attacker_effects={"gfx": "light_1", "sfx": "default"}, piercing=True,
                main_effect={"gfx": Transform("light_3", zoom=2.5), "sfx": "content/sfx/sound/be/light4.mp3", "duration": 1.6, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_light_with_shake", "initial_pause": 0.1, "duration": 1.5},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause":1.3, "duration": 0.2})
        BE_Action(u"Holyja", menu_pos=0.3, attributes=["magic", "light"], effect=15, multiplier=0.8, mp_cost=17, range=4, piercing=True, type="all_enemies",
                desc="Gathers holy energy around targets and releases it upwards like a pillar of light.",
                attacker_effects={"gfx": "light_1", "sfx": "default"},
                main_effect={"gfx": Transform("light_4_webm", zoom=1.5), "sfx": "content/sfx/sound/be/light5.mp3", "duration": 2.23, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 70}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.1},
                target_sprite_damage_effect={"gfx": "on_light_with_shake", "initial_pause": 0.5, "duration": 1.4},
                target_death_effect={"gfx": "hide", "initial_pause": 1.5, "duration": 0.0001})
        BE_Action(u"Star Light", menu_pos=0.5, attributes=["magic", "light"], effect=60, multiplier=1.3, mp_cost=35, range=4,
                desc="A powerful and painful flash of star light.",
                attacker_effects={"gfx": "light_2", "sfx": "default"}, piercing=True,
                main_effect={"gfx": Transform("light_6_webm", zoom=1.4), "sfx": "content/sfx/sound/be/light2.mp3", "duration": 0.96, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_light_with_shake", "initial_pause": 0.1, "duration": 0.8},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.3},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause":1.0, "duration": 0.4})
        BE_Action(u"Photon Blade", menu_pos=1, attributes=["magic", "light"], effect=60, multiplier=1.4, mp_cost=55, range=4,
                desc="Infinitely thin blades of pure light slices target.",
                attacker_effects={"gfx": "light_2", "sfx": "default"},
                main_effect={"gfx": Transform("light_5", zoom=1.9), "sfx": "content/sfx/sound/be/dawn.mp3", "duration": 2.5, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0, "hflip": True},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.5, "duration": 1.4},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.6},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause":2.0, "duration": 0.4})
        BE_Action("Forced Dawn", menu_pos=5, menuname="Dawn", attributes=["magic", "light"], effect=60, multiplier=1.2, mp_cost=75, range=4, type="all_enemies",
                desc="The energy of a whole sunrise quickly covers a small area.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": Transform("dawn", zoom=2.5), "sfx": "content/sfx/sound/be/dawn.mp3", "duration": 3.3, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 50, "xo": -50}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.7},
                target_sprite_damage_effect={"gfx": "on_light", "initial_pause": 1.5, "duration": 0.5},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.6, "duration": 1.0},
                dodge_effect={"initial_pause": 1.2})
        ArealSkill("Holy Blast", menu_pos=9, attributes=["magic", "light", "inevitable"], effect=120, multiplier=1.5, mp_cost=110, range=4, type="all_enemies", piercing=True,
                desc="Concentrates all holy energy in the area into one point, forcing it to explode as it reaches critical levels.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": Transform("holy_blast", zoom=2.2), "sfx": "content/sfx/sound/be/light6.mp3", "duration": 3.7, "aim": {"anchor": (0.5, 1.0), "yo": 320}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 3.7},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 1.5, "duration": 2.2},
                target_death_effect={"gfx": "dissolve", "initial_pause": 2.7, "duration": 0.5})
        # Darkness:
        BE_Action(u"Dark", menu_pos=0, attributes=["magic", "darkness"], effect=15, multiplier=1.0, mp_cost=12, range=4, type="all_enemies",
                desc="The mere presence of dark energy is dangerous for most creatures.",
                attacker_effects={"gfx": "dark_1", "sfx": "default"},
                main_effect={"gfx": Transform("darkness_1", zoom=1.3), "sfx": "content/sfx/sound/be/darkness1.mp3", "duration": 1.0, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_darkness", "initial_pause": 0.1, "duration": 0.9},
                target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause":0.8, "duration": 0.2})
        BE_Action(u"Darkra", menu_pos=0.1, attributes=["magic", "darkness"], effect=15, multiplier=1.1, mp_cost=10, range=4,
                desc="Darkness envelops the target, slowly killing it.",
                attacker_effects={"gfx": "dark_1", "sfx": "default"},
                main_effect={"gfx": Transform("darkness_2", zoom=1.6), "sfx": "content/sfx/sound/be/darkness2.mp3", "duration": 1.6, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}, "start_at": 0},
                target_sprite_damage_effect={"gfx": "on_darkness", "initial_pause": 0.3, "duration": 1.3},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.4},
                target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause":0.8, "duration": 0.2})
        BE_Action(u"Darkga", menu_pos=0.2, attributes=["magic", "darkness"], effect=15, multiplier=0.9, mp_cost=14, range=4, piercing=True,
                desc="Negative energy concentrates in a very small area and then explodes.",
                attacker_effects={"gfx": "dark_1", "sfx": "default"},
                main_effect={"gfx": Transform("darkness_3", zoom=1.4), "sfx": "content/sfx/sound/be/darkness3.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5)}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.9},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.9, "duration": 0.6},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})
        BE_Action(u"Darkja", menu_pos=0.3, attributes=["magic", "darkness"], effect=15, multiplier=0.8, mp_cost=17, range=4, piercing=True, type="all_enemies",
                desc="Summons an abnormal and chaotic substances from a dark world that deforms targets.",
                attacker_effects={"gfx": "dark_1", "sfx": "default"},
                main_effect={"gfx": Transform("darkness_4", zoom=1.2), "sfx": "content/sfx/sound/be/darkness2.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5)}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.1},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 1.2},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.4})
        BE_Action(u"Eternal Gluttony", menu_pos=0.5, attributes=["magic", "darkness"], effect=60, multiplier=1.3, mp_cost=35, range=4, piercing=True,
                desc="Summons a dark creature from the world of darkness to devour the target.",
                attacker_effects={"gfx": "dark_2", "sfx": "default"},
                main_effect={"gfx": Transform("darkness_5", zoom=1.2), "sfx": "content/sfx/sound/be/horny2.mp3", "duration": 1.2, "aim": {"point": "center", "anchor": (0.5, 0.5)}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.5},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.5, "duration": 0.7},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.9, "duration": 0.2})
        BE_Action(u"Black Hole", menu_pos=1, attributes=["magic", "darkness"], effect=60, multiplier=1.2, mp_cost=75, range=4, type="all_enemies",
                desc="Creates holes in space itself that lead to the dark dimension.",
                attacker_effects={"gfx": "dark_2", "sfx": "default"},
                main_effect={"gfx": Transform("darkness_6", zoom=1.1), "sfx": "content/sfx/sound/be/darkness3.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5)}},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.1},
                target_sprite_damage_effect={"gfx": "on_darknes_with_shake", "initial_pause": 0.1, "duration": 1.2},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.9, "duration": 0.2})
        BE_Action("Other Light", menu_pos=4, attributes=["magic", "darkness", "light"], effect=75, multiplier=1.25, mp_cost=45, range=4, piercing=True, true_pierce=True,
                desc="Brings an alternative form of light from a dark dimension. Ignores back row damage reduction.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": Transform("darklight", zoom=1.5), "sfx": "content/sfx/sound/be/darklight.mp3", "duration": 2.0, "aim": {"point": "tc", "anchor": (0.5, 0), "yo": -55}},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.3, "duration": 1.2},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.8},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.8, "duration": 0.5},
                dodge_effect={"initial_pause": .2})
        FullScreenCenteredArealSkill("Dominion", menu_pos=9, attributes=["magic", "darkness", "inevitable"], effect=100, multiplier=1.5, mp_cost=110, range=4, type="all_enemies", piercing=True,
                desc="Conjures primary darkness tearing apart all living things.",
                attacker_effects={"gfx": "orb", "sfx": "default"},
                main_effect={"gfx": "dominion", "sfx": "content/sfx/sound/be/darkness5.mp3", "duration": 2.5},
                arget_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.5},
                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 2.4},
                target_death_effect={"gfx": "dissolve", "initial_pause": 2, "duration": 0.5},
                bg_main_effect={"gfx": "black", "initial_pause": 0, "duration": 2.6})
        # Healing:
        # effect should be from 0 to 1, heals the max health*effect
        BasicHealingSpell(u"Life Wind", menu_pos=-3, attributes=["magic", "healing", "air"], kind="healing", effect=0.1, mp_cost=50, range=5, type="all_allies",
                desc="Healing wind restores health for the whole party (+10%).",
                attacker_action={"gfx": None},
                attacker_effects={"gfx": "runes_1", "sfx": "default"},
                main_effect={"gfx": Transform("heal_3", zoom=1.4), "sfx": "content/sfx/sound/be/heal3.mp3", "duration": 2.1, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}},
                target_sprite_damage_effect={"gfx": "being_healed"},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.0},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 1.5})
        BasicHealingSpell(u"Curer", menu_pos=-2, attributes=["magic", "healing", "water"], kind="healing", effect=0.25, mp_cost=20, range=5, type="sa",
                desc="Heals superficial wounds and accelerates the healing of internal ones (+25%).",
                attacker_action={"gfx": None},
                attacker_effects={"gfx": "runes_1", "sfx": "default"},
                main_effect={"gfx": Transform("heal_2", zoom=2.4), "sfx": "content/sfx/sound/be/heal2.mp3", "duration": 2.5, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}},
                target_sprite_damage_effect={"gfx": "being_healed"},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.7},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 1.5})
        BasicHealingSpell(u"Restoration", menu_pos=-1, attributes=["magic", "healing", "light"], kind="healing", effect=0.5, mp_cost=40, range=5, type="sa", piercing=True, true_pierce=True,
                desc="Concentrated flow of positive energy quickly regenerates even severe wounds (+50%).",
                attacker_action={"gfx": None},
                attacker_effects={"gfx": "runes_1", "sfx": "default"},
                main_effect={"gfx": Transform("heal_1", zoom=2.0), "sfx": "content/sfx/sound/be/heal1.mp3", "duration": 3.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                target_sprite_damage_effect={"gfx": "being_healed"},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.0},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 1.5})
        if config.debug: # spell for killing allies for testing; available only in debug mode
            BE_Action(u"DarkTouch", menu_pos=-99, attributes=["magic", "darkness"], effect=999999999, mp_cost=10, range=5,
                type="sa", piercing=True, true_pierce=True,
                desc="Sacrifices a party member in the name of an ancient dark creature from another dimension.",
                attacker_action={"gfx": None},
                attacker_effects={"gfx": "runes_1", "sfx": "default"},
                main_effect={"gfx": Transform("heal_2", zoom=1.4), "sfx": "content/sfx/sound/be/heal2.mp3", "duration": 2.5, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}},
                target_sprite_damage_effect={"gfx": None},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.7},
                target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 1.5})
            FullScreenCenteredArealSkill("Get Rekt", menu_pos=0, attributes=["magic", "darkness", "fire", "ice", "water", "inevitable"], effect=10000, multiplier=100, mp_cost=1, range=4, type="all_enemies", piercing=True, # testing spell for killing enemy team on spot
                    desc="«Instant death! Instant death, unavoidable! I was dodging, and still got instantly killed!»",
                    attacker_effects={"gfx": "orb", "sfx": "default"},
                    main_effect={"gfx": "dominion", "sfx": "content/sfx/sound/be/darkness5.mp3", "duration": 2.5},
                    arget_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.5},
                    target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 2.4},
                    target_death_effect={"gfx": "dissolve", "initial_pause": 2, "duration": 0.5},
                    bg_main_effect={"gfx": "black", "initial_pause": 0, "duration": 2.6})
        # Reviving:
        ReviveSpell(u"Revive", attributes=["magic", "light"], kind="revival", menu_pos=-1, effect=10, mp_cost=35, health_cost=0.3, range=5, type="sa", piercing=True, true_pierce=True, target_state="dead",
                desc="Brings an unconscious ally back to the battlefield by sharing some life energy.",
                attacker_action={"gfx": None},
                attacker_effects={"gfx": "circle_3", "sfx": "default"},
                main_effect={"gfx": Transform("resurrection", zoom=1.75), "sfx": "content/sfx/sound/be/heal2.mp3", "duration": 2.0, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": -150}},
                target_sprite_damage_effect={"gfx": None},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.0},
                target_death_effect={"gfx": None})

    ##### Effects:
        # Poison:
        # effect should be from 0 to 1, ie part of max health the poison takes every turn
        BasicPoisonSpell("Poison", menu_pos=-5, attributes=["status", "poison", "darkness"], effect=0.1, multiplier=1.0, mp_cost=30, range=4, kind="damage_over_time",
                desc="Poisons the target causing additional damage each turn.",
                attacker_effects={"gfx": "default_1", "sfx": "default"},
                main_effect={"gfx": Transform("poison_1", zoom=2.1), "sfx": "content/sfx/sound/be/poison_01.ogg", "duration": 1.0, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": -25}},
                target_sprite_damage_effect={"gfx": None},
                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.2},
                target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 0.5})
        # Buffs:
        DefenceBuffSpell("Aery Field", menu_pos=-1, attributes=["status", "air"], kind="buff", defence_multiplier={"ranged": 1.5}, buff_group="ranged shield", buff_icon=ProportionalScale("content/gfx/be/buffs/ranged_def.png", 30, 30), mp_cost=0.1, vitality_cost=0.3, range=4, type="sa", defence_gfx="air_shield",
                desc="Creates a force field around the target, reducing damage from ranged attacks.",
                main_effect={"gfx": Transform(AlphaBlend(ImageReference("ranged_shield1_webm"), ImageReference("ranged_shield1_webm"), green_shield(350, 300), alpha=True), size=(350, 300)), "sfx": "content/sfx/sound/be/m_shield.ogg", "duration": 0.967, "aim": {"point": "center", "anchor": (.5, .5), "yo": 0}},
                target_sprite_damage_effect={"gfx": None},
                target_damage_effect={"gfx": None},
                target_death_effect={"gfx": None})
        DefenceBuffSpell("Aery Shield", menu_pos=-1, attributes=["status", "air"], kind="buff", defence_multiplier={"ranged": 3.0}, buff_group="ranged shield", buff_icon=ProportionalScale("content/gfx/be/buffs/big_ranged_def.png", 30, 30), mp_cost=0.2, vitality_cost=0.5, range=4, type="sa", defence_gfx="air_shield",
                desc="Creates a powerful force field around the target, reducing damage from ranged attacks.",
                main_effect={"gfx": Transform(AlphaBlend(ImageReference("ranged_shield1_webm"), ImageReference("ranged_shield1_webm"), green_shield(350, 300), alpha=True), size=(350, 300)), "sfx": "content/sfx/sound/be/m_shield.ogg", "duration": 0.967, "aim": {"point": "center", "anchor": (.5, .5), "yo": 0}},
                target_sprite_damage_effect={"gfx": None},
                target_damage_effect={"gfx": None},
                target_death_effect={"gfx": None})
        DefenceBuffSpell("Arcane Field", menu_pos=-1, attributes=["status", "darkness"], kind="buff", defence_multiplier={"magic": 1.5}, buff_group="spell shield", buff_icon=ProportionalScale("content/gfx/be/buffs/mag_def.png", 30, 30), mp_cost=0.3, vitality_cost=0.1, range=4, type="sa",
                desc="Sets up a force field around the target, partly shielding from magical damage.",
                main_effect={"gfx": Transform("magic_shield_webm", zoom=1.1), "sfx": "content/sfx/sound/be/m_shield.ogg", "duration": 1.27, "aim": {"point": "center", "anchor": (.5, .5), "yo": 0}},
                target_sprite_damage_effect={"gfx": None},
                target_damage_effect={"gfx": None},
                target_death_effect={"gfx": None})
        DefenceBuffSpell("Arcane Shield", menu_pos=-1, attributes=["status", "darkness"], kind="buff", defence_multiplier={"magic": 3.0}, buff_group="spell shield", vitality_cost=0.2, mp_cost=0.5, buff_icon=ProportionalScale("content/gfx/be/buffs/big_mag_def.png", 30, 30), range=4, type="sa",
                desc="Sets up a powerful force field around the target, shielding from magical damage.",
                main_effect={"gfx": Transform("magic_shield_webm", zoom=1.1), "sfx": "content/sfx/sound/be/m_shield.ogg", "duration": 1.27, "aim": {"point": "center", "anchor": (.5, .5), "yo": 0}},
                target_sprite_damage_effect={"gfx": None},
                target_damage_effect={"gfx": None},
                target_death_effect={"gfx": None})
        DefenceBuffSpell("Solid Field", menu_pos=-1, attributes=["status", "earth"], kind="buff", defence_multiplier={"melee": 1.5}, buff_group="melee shield", buff_icon=ProportionalScale("content/gfx/be/buffs/melee_def.png", 30, 30), mp_cost=0.2, vitality_cost=0.4, range=4, type="sa", defence_gfx="solid_shield",
                desc="Sets up a force field around the target, partly shielding from melee damage.",
                main_effect={"gfx": Transform("shield_1", size=(400, 400)), "sfx": "content/sfx/sound/be/m_shield.ogg", "duration": 1.0, "aim": {"point": "center", "anchor": (.5, .5), "yo": 0}},
                target_sprite_damage_effect={"gfx": None},
                target_damage_effect={"gfx": None},
                target_death_effect={"gfx": None})
        DefenceBuffSpell("Solid Shield", menu_pos=-1, attributes=["status", "earth"], kind="buff", defence_multiplier={"melee": 3.0}, buff_group="melee shield", vitality_cost=0.7, mp_cost=0.2, buff_icon=ProportionalScale("content/gfx/be/buffs/big_melee_def.png", 30, 30), range=4, type="sa", defence_gfx="solid_shield",
                desc="Sets up a powerful force field around the target, shielding from melee damage.",
                main_effect={"gfx": Transform("shield_1", size=(400, 400)), "sfx": "content/sfx/sound/be/m_shield.ogg", "duration": 1.0, "aim": {"point": "center", "anchor": (.5, .5), "yo": 0}},
                target_sprite_damage_effect={"gfx": None},
                target_damage_effect={"gfx": None},
                target_death_effect={"gfx": None})
        DefenceBuffSpell("Gray Shield", menu_pos=-1, attributes=["status", "darkness", "light"], kind="buff",
                defence_multiplier={"melee": 3.0, "magic": 3.0, "ranged": 3.0}, buff_group="melee shield",
                vitality_cost=1.0, mp_cost=0.5, buff_icon=ProportionalScale("content/gfx/be/buffs/gray.png", 30, 30),
                range=4, type="sa", defence_gfx="gray_shield",
                desc="The apathy of the Gray Ring denies the existence of most incoming attacks, decreasing their power, because it's such a bother to deal with them...",
                main_effect={"gfx": AlphaBlend("magic_shield_webm", "magic_shield_webm", gray_shield(340, 330), alpha=True), "sfx": "content/sfx/sound/be/m_shield.ogg", "duration": 1.27, "aim": {"point": "center", "anchor": (.5, .5), "yo": 0}},
                target_sprite_damage_effect={"gfx": None},
                target_damage_effect={"gfx": None},
                target_death_effect={"gfx": None})
    return
