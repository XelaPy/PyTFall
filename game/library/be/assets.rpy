# Assets of the BE:
init -1: # Images and Animations
    $ renpy.audio.music.register_channel("main_gfx_attacks", renpy.config.movie_mixer, loop=False, stop_on_mute=False, movie=True)
    
    # FilmStrips:
    # Attacks:
    python:
        for i in xrange(1, 6):
            renpy.image("melee_%d" % i, FilmStrip('content/gfx/be/filmstrips/melee_%d.png' % i, (192, 192), (5, 2), 0.05, loop=False))
    
    # Casting:
    python:
        for i in ["cast_dark_2", "cast_light_2", "cast_water_2", "cast_air_2", "cast_fire_2", "cast_earth_2", "cast_electricity_2", "cast_ice_2"]:
            renpy.image(i, FilmStrip('content/gfx/be/filmstrips/%s.png' % i, (192, 192), (5, 4), 0.07, loop=False))
    image cast_default_1 = FilmStrip('content/gfx/be/filmstrips/cast_default_1.png', (192, 192), (5, 3), 0.08, loop=False)
    image cast_runes_1 = FilmStrip('content/gfx/be/filmstrips/cast_runes_1.png', (192, 192), (5, 1), 0.15, loop=False)
    
    # Magic:
    # Fire:
    image fire_1 = FilmStrip('content/gfx/be/filmstrips/fire_1.png', (192, 192), (5, 4), 0.1, loop=False)
    image fire_2 = FilmStrip('content/gfx/be/filmstrips/fire_2.png', (192, 192), (5, 4), 0.1, loop=False)
    image fire_3 = FilmStrip('content/gfx/be/filmstrips/fire_3.png', (192, 192), (5, 7), 0.1, loop=False)
    image fire_4 = FilmStrip('content/gfx/be/filmstrips/fire_4.png', (192, 192), (5, 10), 0.1, loop=False)
    image fire_mask = FilmStrip('content/gfx/be/filmstrips/fire_mask.jpg', (240, 180), (5, 5), 0.05, loop=True)
    image flame_bm = FilmStrip('content/gfx/be/filmstrips/fire_mask_bm.png', (240, 180), (5, 5), 0.05, loop=True)
    image cataclysm_webm = MovieLoopedOnce(channel="main_gfx_attacks", play="content/gfx/be/webm/cataclysm.webm", mask="content/gfx/be/webm/cataclysm.webm")
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
        
    image fire_5_1:
        FilmStrip('content/gfx/be/filmstrips/fire_5_1.png', (192, 192), (5, 4), 0.05, loop=False)
        zoom 2.0
        1.0
    image fire_5:
        FilmStrip('content/gfx/be/filmstrips/fire_5.png', (192, 192), (5, 6), 0.05, loop=True)
        rotate 0
        linear 1.5 rotate 360
    image fire_6_1:
        FilmStrip('content/gfx/be/filmstrips/fire_6_1.png', (192, 192), (5, 3), 0.08, loop=False)
        zoom 2.0
        1.2
    image fire_6:
        FilmStrip('content/gfx/be/filmstrips/fire_6.png', (192, 192), (5, 6), 0.05, loop=True)
        rotate 0
        linear 1.5 rotate 360
    image cataclysm_sideways = FilmStrip('content/gfx/be/filmstrips/cataclysm_sideways.png', (481, 453), (5, 4), 0.1, include_frames=range(17), loop=False)

    # Water:
    image water_1 = FilmStrip('content/gfx/be/filmstrips/water_1.png', (192, 192), (5, 3), 0.1, loop=False)
    image water_2 = FilmStrip('content/gfx/be/filmstrips/water_2.png', (192, 192), (5, 4), 0.1, loop=False)
    image water_3 = FilmStrip('content/gfx/be/filmstrips/water_3.png', (192, 192), (5, 5), 0.1, loop=False)
    image water_4 = FilmStrip('content/gfx/be/filmstrips/water_4.png', (192, 192), (5, 9), 0.05, loop=False)
    image water_5 = FilmStrip('content/gfx/be/filmstrips/water_5.png', (192, 192), (5, 6), 0.1, loop=False)
    image water_6 = FilmStrip('content/gfx/be/filmstrips/water_6.png', (192, 192), (5, 10), 0.1, loop=False)
    image rain = FilmStrip('content/gfx/be/filmstrips/rain.png', (192, 192), (5, 10), 0.05, loop=True)
    image water_wave = FilmStrip('content/gfx/be/filmstrips/water_wave.png', (531, 213), (3, 3), 0.15, include_frames=range(7), loop=False)
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
        # It's prolly a better design to work with the displayable directly using contains instead of replacing them with parallel...
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
            
        
    # Earth:
    image earth_1 = FilmStrip('content/gfx/be/filmstrips/earth_1.png', (192, 192), (5, 4), 0.1, loop=False)
    image earth_2 = FilmStrip('content/gfx/be/filmstrips/earth_2.png', (192, 192), (5, 2), 0.1, loop=False)
    image earth_3 = FilmStrip('content/gfx/be/filmstrips/earth_3.png', (192, 192), (5, 3), 0.1, loop=False)
    image earth_4 = FilmStrip('content/gfx/be/filmstrips/earth_4.png', (192, 192), (5, 2), 0.12, loop=False)
    image earth_5 = FilmStrip('content/gfx/be/filmstrips/earth_5.png', (192, 192), (5, 8), 0.07, loop=False)
    image earth_6 = FilmStrip('content/gfx/be/filmstrips/earth_6.png', (192, 192), (5, 4), 0.1, loop=False)
    image magma = FilmStrip('content/gfx/be/filmstrips/magma.png', (192, 192), (5, 8), 0.08, loop=False)
    image crushing_hand = FilmStrip('content/gfx/be/filmstrips/crushing_hand.png', (513, 297), (3, 6), 0.15, loop=False)
    
    # Air:
    image air_1 = FilmStrip('content/gfx/be/filmstrips/air_1.png', (192, 192), (5, 5), 0.06, loop=False)
    image air_2 = FilmStrip('content/gfx/be/filmstrips/air_2.png', (192, 192), (5, 5), 0.06, loop=False)
    image air_3 = FilmStrip('content/gfx/be/filmstrips/air_3.png', (192, 192), (5, 5), 0.06, loop=False)
    image air_4 = FilmStrip('content/gfx/be/filmstrips/air_4.png', (192, 192), (5, 6), 0.05, loop=False)
    image air_6 = FilmStrip('content/gfx/be/filmstrips/air_6.png', (151, 151), (5, 7), 0.06, loop=False, reverse=True)
    image air_webm = MovieLoopedOnce(channel="main_gfx_attacks", play="content/gfx/be/webm/Air_2.webm", mask="content/gfx/be/webm/Air_1t.webm")
    image vortex = FilmStrip('content/gfx/be/filmstrips/vortex.png', (277, 277), (15, 1), 0.1, loop=True)
    image tornado:
        FilmStrip('content/gfx/be/filmstrips/tornado.png', (674, 592), (2, 3), 0.05, loop=True)
        anchor (0.5, 1.0)
        zoom 0.5
        subpixel True
        easeout 1.5 zoom 1.3
        
        on hide:
            alpha 1.0
            linear 0.5 alpha 0
    
    image light_1 = FilmStrip('content/gfx/be/filmstrips/light_1.png', (192, 192), (5, 5), 0.05, loop=False)
    image light_2 = FilmStrip('content/gfx/be/filmstrips/light_2.png', (192, 192), (5, 5), 0.05, loop=False)
    image light_3 = FilmStrip('content/gfx/be/filmstrips/light_3.png', (100, 100), (5, 16), 0.02, loop=False)
    image light_5 = FilmStrip('content/gfx/be/filmstrips/light_5.png', (192, 192), (5, 5), 0.1, loop=False)
    image light_6 = FilmStrip('content/gfx/be/filmstrips/light_6.png', (153, 160), (4, 3), 0.15, loop=False)
    image dawn = FilmStrip('content/gfx/be/filmstrips/dawn.png', (192, 192), (5, 7), 0.1, loop=False)
    image holy_blast = FilmStrip('content/gfx/be/filmstrips/holy_blast_2x_bm.png', (382, 336), (8, 5), 0.1, include_frames=range(36), loop=False)

    # Darkness:
    image darkness_1 = FilmStrip('content/gfx/be/filmstrips/darkness_1.png', (192, 192), (5, 4), 0.05, loop=False)
    image darkness_2 = FilmStrip('content/gfx/be/filmstrips/darkness_2.png', (192, 192), (5, 4), 0.08, loop=False)
    image darkness_3 = FilmStrip('content/gfx/be/filmstrips/darkness_3.png', (192, 192), (5, 6), 0.05, loop=False)
    image darkness_4 = FilmStrip('content/gfx/be/filmstrips/darkness_4.png', (192, 192), (5, 6), 0.05, loop=False)
    image darkness_5 = FilmStrip('content/gfx/be/filmstrips/darkness_5.png', (375, 500), (4, 3), 0.1, loop=False)
    image darkness_6 = FilmStrip('content/gfx/be/filmstrips/darkness_6.png', (192, 192), (5, 3), 0.1, loop=False)
    image darklight = FilmStrip('content/gfx/be/filmstrips/darklight.png', (144, 192), (5, 4), 0.1, loop=False)
    image dominion = Transform(FilmStrip('content/gfx/be/filmstrips/dominion_bm.png', (595, 354), (5, 5), 0.1, loop=False),
                                                      size=(config.screen_width, config.screen_height))

    # Ice Arrow:
    image ice_1 = FilmStrip('content/gfx/be/filmstrips/ice_1.png', (192, 192), (5, 5), 0.08, loop=False)
    image ice_2 = FilmStrip('content/gfx/be/filmstrips/ice_2.png', (192, 192), (5, 5), 0.07, loop=False)
    image ice_3 = FilmStrip('content/gfx/be/filmstrips/ice_3.png', (192, 192), (5, 5), 0.05, loop=False)
    image ice_4 = FilmStrip('content/gfx/be/filmstrips/ice_4.png', (192, 192), (5, 4), 0.04, loop=False)
    image ice_5 = FilmStrip('content/gfx/be/filmstrips/ice_5.png', (192, 192), (5, 6), 0.07, loop=False)
    image ice_6 = FilmStrip('content/gfx/be/filmstrips/ice_6.png', (192, 192), (5, 4), 0.06, loop=False)
    image ice_7 = FilmStrip('content/gfx/be/filmstrips/ice_7.png', (192, 192), (5, 5), 0.08, loop=False, reverse=True)
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
        
    image ice_blast = FilmStrip('content/gfx/be/filmstrips/ice_blast.png', (393, 508), (5, 5), 0.1, include_frames=range(22), loop=False)
    
    image ice_twin_explosion = FilmStrip('content/gfx/be/filmstrips/ice_twin_explosion.png', (358, 312), (2, 4), 0.1, include_frames=range(7), loop=False)
    image ice_strike = FilmStrip('content/gfx/be/filmstrips/ice_strike.png', (581, 511), (3, 4), 0.1, loop=False)
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
    
    
    # Electricity:
    image electricity_1 = FilmStrip('content/gfx/be/filmstrips/electricity_1.png', (192, 192), (5, 2), 0.1, loop=False)
    image electricity_2 = FilmStrip('content/gfx/be/filmstrips/electricity_2.png', (192, 192), (5, 3), 0.08, loop=False)
    image electricity_3 = FilmStrip('content/gfx/be/filmstrips/electricity_3.png', (192, 192), (5, 3), 0.09, loop=False)
    image electricity_4:
        FilmStrip('content/gfx/be/filmstrips/electricity_4.png', (192, 192), (5, 3), 0.04, loop=False)
        zoom 1.5
    image electricity_5 = FilmStrip('content/gfx/be/filmstrips/electricity_5.png', (192, 384), (5, 2), 0.08, loop=True)
    image electricity_6 = FilmStrip('content/gfx/be/filmstrips/electricity_6.png', (192, 192), (5, 16), 0.04, loop=True)
    image ion:
        FilmStrip('content/gfx/be/filmstrips/ion.png', (192, 192), (5, 9), 0.05, loop=True)
        zoom 3.0
    image ion_1:
        FilmStrip('content/gfx/be/filmstrips/ion_1.png', (192, 192), (5, 5), 0.04, loop=True)
        rotate 0
        linear 1.0 rotate 360
    image thunder_storm_2 = FilmStrip('content/gfx/be/filmstrips/thunder_storm_2.png', (354, 389), (4, 4), 0.1, loop=False)
    image thunder_storm_3:
        VBox(Transform(FilmStrip('content/gfx/be/filmstrips/just_frelling_die_2x_bm.png', (507, 253), (2, 17), 0.1, loop=False), crop=(0, 0, 507, 125)),
                  Transform(FilmStrip('content/gfx/be/filmstrips/just_frelling_die_2x_bm.png', (507, 253), (2, 17), 0.1, loop=False), crop=(0, 125, 507, 128), yzoom=3))
    
    image poison_1 = FilmStrip('content/gfx/be/filmstrips/poison_1.png', (192, 192), (5, 6), 0.07, loop=False)
    image poison_2 = FilmStrip('content/gfx/be/filmstrips/poison_2.png', (192, 192), (5, 3), 0.1, loop=False)
    image poison_3 = FilmStrip('content/gfx/be/filmstrips/poison_3.png', (192, 192), (5, 5), 0.06, loop=False)
        
    image heal_1 = FilmStrip('content/gfx/be/filmstrips/heal_1.png', (192, 192), (5, 6), 0.1, loop=False)
    image heal_2 = FilmStrip('content/gfx/be/filmstrips/heal_2.png', (192, 192), (5, 5), 0.1, loop=False)
    image resurrection = FilmStrip('content/gfx/be/filmstrips/resurrection2x.png', (288, 247), (5, 4), 0.1, loop=False)
    image bg test_grid = "content/gfx/bg/maps/map17x6.jpg"
    
    
# Skillz (We do not want to do this in the init so I am making it a label):
label load_battle_skills:
    python:
        # Weapons:
        SimpleAttack("SwordAttack", attributes=["melee"], critpower=0, effect=5, range=1, menuname="Sword", gfx=ProportionalScale("content/gfx/be/swords.png", 150, 150), sfx="content/sfx/sound/be/sword.mp3")
        SimpleAttack("BowAttack", attributes=["ranged"], critpower=0, effect=5, range=3, menuname="Bow", gfx=ProportionalScale("content/gfx/be/bows.png", 150, 150), sfx=["content/sfx/sound/be/bow_attack_1.mp3", "content/sfx/sound/be/bow_attack_2.mp3"])
        SimpleAttack("CrossbowAttack", attributes=["ranged"], critpower=0.2, effect=7, range=4, menuname="Crossbow",  piercing=True, gfx=ProportionalScale("content/gfx/be/crossbows.png", 150, 150), sfx="content/sfx/sound/be/crossbow_attack.mp3")
        SimpleAttack("KnifeAttack", attributes=["melee"], critpower=1.0, effect=4, menuname="Stab", gfx=ProportionalScale("content/gfx/be/knives.png", 150, 150), sfx="content/sfx/sound/be/knife.mp3")
        SimpleAttack("ClawAttack", attributes=["melee"], critpower=0.4, effect=5, menuname="Claws", gfx=ProportionalScale("content/gfx/be/claws.png", 150, 150), sfx="content/sfx/sound/be/claw_attack.mp3")
        SimpleAttack("FistAttack", attributes=["melee"], critpower=-0.4, effect=3, menuname="Fists", gfx=ProportionalScale("content/gfx/be/fists.png", 150, 150), sfx=list("content/sfx/sound/be/fist_attack_%d.mp3"%i for i in xrange(1, 6)))
        SimpleAttack("CannonAttack", attributes=["ranged"], critpower=-0.6, effect=6, range=3, menuname="Cannon", gfx=ProportionalScale("content/gfx/be/cannons.png", 150, 150), sfx=["content/sfx/sound/be/cannon_1.mp3", "content/sfx/sound/be/cannon_2.mp3", "content/sfx/sound/be/cannon_3.mp3"])
        SimpleAttack("RodAttack", attributes=["melee"], critpower=-1.1, effect=2, menuname="Mace", gfx=ProportionalScale("content/gfx/be/rods.png", 150, 150), sfx="content/sfx/sound/be/rod_attack.mp3")
        SimpleAttack("AxeAttack", attributes=["melee"], critpower=-0.2, effect=5, menuname="Axe", gfx=ProportionalScale("content/gfx/be/axes.png", 150, 150), sfx="content/sfx/sound/be/axe_attack.mp3")
        SimpleAttack("BiteAttack", attributes=["melee"], critpower=0.5, effect=3, menuname="Bite", gfx=ProportionalScale("content/gfx/be/bites.png", 150, 150), sfx="content/sfx/sound/be/bite_attack.mp3")
        SimpleAttack("GunAttack", attributes=["ranged"], critpower=0.3, effect=5, menuname="Gun", gfx=ProportionalScale("content/gfx/be/shoots.png", 150, 150), sfx="content/sfx/sound/be/gun_attack.mp3")
        SimpleAttack("ScytheAttack", attributes=["melee"], critpower=0.6, effect=6, menuname="Scythe", gfx=ProportionalScale("content/gfx/be/scythe.png", 150, 150), sfx="content/sfx/sound/be/scythe_attack.mp3")
        SimpleAttack("SprayAttack", attributes=["ranged"], critpower=-0.7, effect=5, menuname="Spray", gfx=ProportionalScale("content/gfx/be/spray.png", 150, 150), sfx="content/sfx/sound/be/spray_attack.mp3")
        SimpleAttack("ThrowAttack", attributes=["ranged"], critpower=-0.1, effect=5, menuname="Throw", gfx=ProportionalScale("content/gfx/be/throw.png", 150, 150), sfx=["content/sfx/sound/be/throwing_attack_1.mp3", "content/sfx/sound/be/throwing_attack_2.mp3"])
        SimpleAttack("WhipAttack", attributes=["melee"], critpower=0.4, effect=4, menuname="Whip", gfx=ProportionalScale("content/gfx/be/whip.png", 150, 150), sfx=["content/sfx/sound/be/whip_attack_1.mp3", "content/sfx/sound/be/whip_attack_2.mp3"])
        
        # Magic:
        # Fire:
        # GFX/SFX Dicts:
        # attacker_action = {"gfx": "step_forward", "sfx": None}
        # attacker_effects = {"gfx": "fire_1", "sfx": "default"}
        # main_effect = {"gfx": "fire_1", "sfx": Transform("content/sfx/sound/be/fire4.mp3", zoom=1.5), "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 50}, "start_at": 0}
        # target_sprite_damage_effect = {"gfx": "shake", "sfx": None, "initial_pause": 0.1, "duration": 0.9}
        # target_damage_effect = {"gfx": "battle_bounce", "sfx": None}
        # target_death_effect = {"gfx": "dissolve", "sfx": None, "initial_pause": 0.1, "duration": 0.9}
        SimpleMagicalAttack(u"Fire", menu_pos=0, attributes=['magic', 'fire'], effect=20, multiplier=1.2, type="all_enemies", cost=5, range=4, desc="Ignites a small plot of land.",
                                           attacker_effects={"gfx": "fire_1", "sfx": "default"},
                                           main_effect={"gfx": Transform("fire_1", zoom=1.7), "sfx": "content/sfx/sound/be/fire4.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 75}},
                                           target_sprite_damage_effect={"gfx": "on_fire", "initial_pause": 0.1, "duration": 1.7},
                                           target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 1.5})
        SimpleMagicalAttack(u"Fira", menu_pos=1, attributes=['magic', 'fire'], effect=30, multiplier=1.2, cost=7, range=4, desc="Ignites the air in a limited area.",
                                           attacker_effects = {"gfx": "fire_1", "sfx": "default"},
                                           main_effect={"gfx": Transform("fire_2", zoom=1.5), "sfx": "content/sfx/sound/be/fire4.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                                           target_sprite_damage_effect={"gfx": "burning", "initial_pause": 0.1, "duration": 1.3},
                                           target_death_effect={"gfx": "dissolve", "initial_pause": 0.7, "duration": 1.2})
        SimpleMagicalAttack(u"Firaga", menu_pos=2, attributes=['magic', 'fire'], effect=25, multiplier=1.2, cost=6, range=4, piercing=True, desc="Creates liquid fire that envelopes the target, causing massive burns.",
                                           attacker_effects={"gfx": "fire_2", "sfx": "default"},
                                           main_effect={"gfx": Transform("fire_4", zoom=1.5), "sfx": "content/sfx/sound/be/fire6.mp3", "duration": 5.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                                           target_sprite_damage_effect={"gfx": "fire", "initial_pause": 1.3, "duration": 3.6},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.3},
                                           target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 1.5})
        SimpleMagicalAttack(u"Firaja", menu_pos=3, attributes=['magic', 'fire'], effect=10, multiplier=1.2, cost=15, range=4, type="all_enemies", piercing=True, desc="Creates a rain of fire that hits all enemies.",
                                           attacker_effects={"gfx": "fire_1", "sfx": "default"},
                                           main_effect={"gfx": Transform("fire_3", zoom=1.5), "sfx": "content/sfx/sound/be/fire5.mp3", "duration": 3.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                                           target_sprite_damage_effect={"gfx": "fire_shake", "initial_pause": 0.2, "duration": 3.0},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.3},
                                           target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 1.5})
        P2P_MagicAttack(u"Fireball", menu_pos=10, attributes=['magic', 'fire'], effect=50, multiplier=1.5, cost=10, range=4, piercing=True,
                                      desc="Launches an exploding fireball at one enemy.",
                                      projectile_effects={"gfx": 'fire_6', "sfx": "content/sfx/sound/be/fire7.mp3", "duration": 1.0},
                                      main_effect={"gfx": Transform("fire_6_1", zoom=1), "sfx": None, "duration": 1.2, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                                      attacker_effects={"gfx": "fire_2", "sfx": "default"},
                                      target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 0.7},
                                      target_death_effect={"gfx": "dissolve", "initial_pause": 0.1, "duration": 0.5})
        P2P_MagicAttack(u"Solar Flash", menu_pos=11, attributes=['magic', 'fire'], effect=65, multiplier=1.5, cost=12, range=4,
                                      desc="Sends towards the target a small piece of solar plazma.",
                                      projectile_effects={"gfx": 'fire_5', "sfx": "content/sfx/sound/be/fire7.mp3", "duration": 1.0},
                                      main_effect={"gfx": Transform("fire_5_1", zoom=1), "duration": 1.5},
                                      attacker_effects={"gfx": "fire_2", "sfx": "default"},
                                      target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 0.7},
                                      target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 0.5})
        MagicArrows(u"Fire Arrow", menu_pos=8, attributes=['magic', 'fire'], effect=100, multiplier=1.8, cost=20, range=4, piercing=True,
                              desc="Creates a bow and arrow of scorching air.",
                              firing_effects={"gfx": 'Fire Arrow cast', "sfx": "content/sfx/sound/be/fire_arrow.mp3"},
                              projectile_effects={"gfx": 'Fire Arrow fly', "sfx": None, "duration": 0.4},
                              attacker_effects={"gfx": "default_1", "sfx": "default"},
                              target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.021},
                              main_effect={"gfx": 'Fire Arrow impact', "sfx": None, "duration": 0.51, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                              target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.01, "duration": 0.4},
                              target_death_effect={"gfx": "shatter", "initial_pause": 0.011, "duration": 0.6})
        SimpleMagicalAttack("Meteor", menu_pos=12, attributes=['magic', 'fire'], effect=70, multiplier=1.8, cost=15, range=4, true_pierce=True, type="se", desc="Summons flaming fragments of meteor.",
                                           attacker_effects={"gfx": "orb", "sfx": "default"},
                                           main_effect={"gfx": Transform('cataclysm_sideways', xzoom=-1), "sfx": "content/sfx/sound/be/fire8.mp3", "duration": 1.8, "aim": {"point": "bc", "anchor": (0.5, 0.1), "xo": 150, "yo": -370}, "hflip": True},
                                           target_sprite_damage_effect={"gfx": "fire", "initial_pause": 1.2, "duration": 0.6},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.3},
                                           target_death_effect={"gfx": "dissolve",  "initial_pause": 1.4, "duration": 0.5})
        ArealMagicalAttack("Cataclysm", menu_pos=13, attributes=['magic', 'fire'], effect=70, multiplier=1.8, cost=15, range=4, true_pierce=True, type="all_enemies", piercing=True,
                                        desc="A larger vesrion of Cataclysm capable of causing desctruction on a much larger scale.",
                                        attacker_effects={"gfx": "orb", "sfx": "default"},
                                        main_effect={"gfx": Transform("cataclysm_webm", zoom=0.85), "sfx": "content/sfx/sound/be/fire2.mp3", "duration": 4.93, "aim": {"anchor": (0.5, 1.0), "xo":-50 ,"yo": 330}},
                                        target_damage_effect={"gfx": "battle_bounce", "initial_pause": 4.8},
                                        target_sprite_damage_effect={"gfx": "shake", "initial_pause": 2, "duration": 2.5},
                                        target_death_effect={"gfx": "hide", "initial_pause": 3.0, "duration": 0.0001},
                                        bg_main_effect={"gfx": "mirrage", "initial_pause": 2.6, "duration": 2})

    
        
        # Water:
        SimpleMagicalAttack(u"Water", menu_pos=0, attributes=['magic', 'water'], effect=10, multiplier=1.2, cost=4, range=4, type="all_enemies", desc="Crushes targets by bubbles of water.",
                                           attacker_effects={"gfx": "water_1", "sfx": "default"},
                                           main_effect={"gfx": Transform('water_1', zoom=1.1), "sfx": "content/sfx/sound/be/water.mp3", "duration": 1.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                                           target_sprite_damage_effect={"gfx": "shake", "sfx": None, "initial_pause": 0.1, "duration": 1.4},
                                           target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                                           target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 0.11, "duration": 0.9})
        SimpleMagicalAttack(u"Watera", menu_pos=1, attributes=['magic', 'water'], effect=30, multiplier=1.2, cost=7, range=4, desc="High pressure water jets pierce through the target.",
                                           attacker_effects={"gfx": "water_1", "sfx": "default"},
                                           main_effect={"gfx": Transform('water_2', zoom=1.4), "sfx": "content/sfx/sound/be/water.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                                           target_sprite_damage_effect={"gfx": "shake", "sfx": None, "initial_pause": 0.1, "duration": 1.4},
                                           target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                                           target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})
        SimpleMagicalAttack(u"Waterga", menu_pos=2, attributes=['magic', 'water'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["water_1", "default"], gfx='water_3', zoom=1.5, pause=2.5, target_damage_gfx=[0.1, "shake", 2.0], sfx="content/sfx/sound/be/water2.mp3", piercing=True,
                                           aim="bc", anchor=(0.5, 1.0), yo=40,
                                           desc="A cloud of water droplets at high speed crashes into the target.")
        SimpleMagicalAttack(u"Waterja", menu_pos=3, attributes=['magic', 'water'], effect=30, multiplier=1.5, cost=8, range=4, casting_effects=["water_2", "default"], gfx='water_4', zoom=1.5, pause=2.25, target_damage_gfx=[0.1, "shake", 2.0], sfx="content/sfx/sound/be/water3.mp3", type="all_enemies", piercing=True,
                                           aim="bc", anchor=(0.5, 1.0), yo=40,
                                           desc="Evaporates some water from targets.")
        SimpleMagicalAttack(u"Geyser", menu_pos=10, attributes=['magic', 'water'], effect=65, multiplier=1.5, cost=12, range=6, casting_effects=["water_2", "default"], gfx='water_5', zoom=1.9, pause=3.0, target_damage_gfx=[0.5, "shake", 2.5], sfx="content/sfx/sound/be/water6.mp3",
                                           aim="bc", anchor=(0.5, 1.0), yo=60,
                                           desc="A powerful stream of water shoots out of the ground directly beneath the target.")
        SimpleMagicalAttack(u"Last Drop", menu_pos=11, attributes=['magic', 'water'], effect=50, multiplier=1.5, cost=10, piercing=True, range=6,
                                           desc="Hits the taget with a massive water blast from above.",
                                           attacker_effects={"gfx": "water_2", "sfx": "default"},
                                           main_effect={"gfx": Transform('water_6', zoom=1.9), "sfx": "content/sfx/sound/be/water5.mp3", "duration": 5.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 60}},
                                           target_sprite_damage_effect={"gfx": "shake", "initial_pause": 1.0, "duration": 3.5},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.1},
                                           target_death_effect={"gfx": "dissolve", "initial_pause": 1.1, "duration": 0.5})
        SimpleMagicalAttack(u"Heavy Rain", menu_pos=12, attributes=['magic', 'water'], effect=70, multiplier=1.8, true_pierce=True, cost=15, range=6, casting_effects=["water_2", "default"], gfx='rain', zoom=2.0, pause=5.0, target_damage_gfx=[0.25, "shake", 4.75], sfx="content/sfx/sound/be/heavy_rain.mp3", type="all_enemies", piercing=True,
                                           aim="bc", anchor=(0.5, 1.0), yo=80,
                                           desc="Summons a rain of extra heavy water from another dimension.")
        ATL_ArealMagicalAttack(u"Water Blast", menu_pos=13, attributes=['magic', 'water'], effect=100, multiplier=3.0, cost=30, piercing=True, range=6, type="all_enemies",
                                                desc="Hits the taget with a massive water blast!",
                                                attacker_effects={"gfx": "orb", "sfx": "default"},
                                                main_effect={"atl": water_combined, "predict": ["water_attack", "water_wave"], "left_args": [1.8, -300], "right_args": [-1.8, 300], "sfx": "content/sfx/sound/be/water7.mp3", "duration": 1.6},
                                                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.6, "duration": 0.9},
                                                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.6},
                                                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})
        
        # Ice:
        MagicArrows("Ice Arrow", menu_pos=8, attributes=['magic', 'ice'], effect=50, multiplier=1.5, cost=10, range=4,
                              desc="Creates a an arrow of ice crystals that pierces through the target.",
                              firing_effects={"gfx": 'Ice Arrow cast', "sfx": "content/sfx/sound/be/ice_arrow.mp3"},
                              projectile_effects={"gfx": 'Ice Arrow fly', "sfx": None, "duration": 0.4},
                              main_effect={"gfx": 'Ice Arrow impact', "sfx": None, "duration": 0.51, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                              attacker_effects={"gfx": "ice_2", "sfx": "default"},
                              target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.021},
                              target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.01, "duration": 0.4},
                              target_death_effect={"gfx": "shatter", "initial_pause": 0.011, "duration": 0.6})   
        SimpleMagicalAttack(u"Blizzard", menu_pos=0, attributes=['magic', 'ice'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["ice_1", "default"], gfx='ice_1', zoom=1.9, pause=2.9, target_damage_gfx=[0.2, "shake", 1.8], sfx="content/sfx/sound/be/ice3.mp3", type="all_enemies",
                                           aim="bc", anchor=(0.5, 1.0), yo=60,
                                           desc="Creates a cloud of sharp ice splinters.")
        SimpleMagicalAttack(u"Blizzara", menu_pos=1, attributes=['magic', 'ice'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["ice_1", "default"], gfx='ice_2', zoom=1.3, pause=1.5, target_damage_gfx=[0.1, "shake", 1.55], sfx="content/sfx/sound/be/ice1.mp3",
                                           aim="bc", anchor=(0.5, 1.0), yo=80,
                                           desc="Ice blades grow out of the ground.")
        SimpleMagicalAttack(u"Blizzarga", menu_pos=2, attributes=['magic', 'ice'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["ice_2", "default"], gfx='ice_4', zoom=1.5, pause=0.8, target_damage_gfx=[0.1, "shake", 0.75], sfx="content/sfx/sound/be/ice2.mp3", piercing=True,
                                           aim="bc", anchor=(0.5, 1.0), yo=40,
                                           desc="Freezes the air itself around the target, creating deadly ice blades.")
        SimpleMagicalAttack(u"Blizzarja", menu_pos=3, attributes=['magic', 'ice'], effect=10, multiplier=1.2, cost=4, range=4, casting_effects=["ice_1", "default"], gfx='ice_3', zoom=1.7, pause=1.25, sfx="content/sfx/sound/be/ice2.mp3", type="all_enemies", piercing=True,
                                           aim="bc", anchor=(0.5, 1.0), yo=60,
                                           target_sprite_damage_effect={"gfx": "frozen", "initial_pause": 0.1, "duration": 1.1},
                                           desc="Quickly draws heat from a small area.")
        SimpleMagicalAttack(u"Zero Prism", menu_pos=10, attributes=['magic', 'ice'], effect=65, multiplier=1.5, cost=12, range=4,
                                           desc="Freezes the target into a solid ice block.",
                                           attacker_effects={"gfx": "ice_2", "sfx": "default"},
                                           main_effect={"gfx": Transform("ice_5", zoom=2.1), "sfx": "content/sfx/sound/be/ice4.mp3", "duration": 2.1, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 110}},
                                           target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.3, "duration": 1.5},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.2},
                                           target_death_effect={"gfx": "shatter", "initial_pause": 1.4, "duration": 0.5})
        SimpleMagicalAttack(u"Ice Shards", menu_pos=11, attributes=['magic', 'ice'], effect=30, multiplier=1.5, cost=8, range=4, piercing=True, type="all_enemies",
                                           desc="Small part of the target immediately freezes and explodes.",
                                           attacker_effects={"gfx": "ice_2", "sfx": "default"},
                                           main_effect={"gfx": Transform("ice_6", zoom=2.0), "sfx": "content/sfx/sound/be/ice2.mp3", "duration": 1.2, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 80}},
                                           target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 0.7},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.2},
                                           target_death_effect={"gfx": "shatter", "initial_pause": 0.2, "duration": 0.5})
        SimpleMagicalAttack("Hailstorm", menu_pos=12, attributes=['magic', 'ice'], effect=100, multiplier=1.8, cost=20, range=4, casting_effects=["orb", "default"], gfx='ice_7', zoom=1.7, pause=2.0, sfx="content/sfx/sound/be/Hailstorm.mp3", piercing=True, true_pierce=True,
                                           aim="bc", anchor=(0.5, 1.0), yo=50,
                                           target_sprite_damage_effect={"gfx": "iced", "initial_pause": 0.2, "duration": 1.8},
                                           desc="Puts the target in a middle of a small, but violent snow storm.")
        SimpleMagicalAttack("Ice Blast", menu_pos=12.5, attributes=['magic', 'ice'], effect=70, multiplier=1.8, cost=15, range=4, true_pierce=True, type="se", desc="Summons frozen fragments of meteor.",
                                           attacker_effects={"gfx": "orb", "sfx": "default"},
                                           main_effect={"gfx": Transform('ice_blast', xzoom=-1), "sfx": "content/sfx/sound/be/ice5.mp3", "duration": 2.3, "aim": {"point": "bc", "anchor": (0.5, 0.1), "xo": 120, "yo": -370}, "hflip": True},
                                           target_sprite_damage_effect={"gfx": "shake", "initial_pause": 1.2, "duration": 1.1},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.3},
                                           target_death_effect={"gfx": "dissolve",  "initial_pause": 1.4, "duration": 0.5})
        ATL_ArealMagicalAttack("Ice Storm", menu_pos=13, attributes=['magic', 'ice'], effect=70, multiplier=1.8, cost=15, range=4, true_pierce=True, type="all_enemies", piercing=True,
                                                desc="Conjures a power ice storm from above!",
                                                attacker_effects={"gfx": "orb", "sfx": "default"},
                                                main_effect={"atl": ice_storm, "predict": ["ice_twin_explosion", "ice_strike"], "sfx": "content/sfx/sound/be/ice2.mp3", "duration": 1.7, "left_args": [(190, 700)], "right_args": [(1035, 700)]},
                                                target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.7},
                                                target_sprite_damage_effect={"gfx": "iced", "initial_pause": 0.6, "duration": 1.0},
                                                target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})
        
        # Earth:
        SimpleMagicalAttack(u"Stone", menu_pos=0, attributes=['magic', 'earth'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["earth_1", "default"], gfx='earth_1', zoom=1.4, pause=2.0, target_damage_gfx=[0.1, "shake", 1.7], sfx="content/sfx/sound/be/earth.mp3", type="all_enemies",
                                           aim="bc", anchor=(0.5, 1.0), yo=40,
                                           desc="Creates cloud of fragments of hardened clay.")
        SimpleMagicalAttack(u"Stonera", menu_pos=1, attributes=['magic', 'earth'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["earth_1", "default"], gfx='earth_2', zoom=1.0, pause=1.5, target_damage_gfx=[0.1, "shake", 0.8], sfx="content/sfx/sound/be/earth.mp3",
                                           aim="bc", anchor=(0.5, 1.0), yo=10,
                                           desc="Creates a spall, yet sharp spike.")
        SimpleMagicalAttack(u"Stonega", menu_pos=2, attributes=['magic', 'earth'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["earth_1", "default"], gfx='earth_3', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.2], sfx="content/sfx/sound/be/earth3.mp3", piercing=True,
                                           aim="bc", anchor=(0.5, 0.5), yo=0,
                                           desc="A small amount of magma moves to the surface, spilling on the target.")
        SimpleMagicalAttack(u"Stoneja", menu_pos=3, attributes=['magic', 'earth'], effect=10, multiplier=1.2, cost=7, range=4, casting_effects=["earth_2", "default"], gfx='earth_4', zoom=1.2, pause=1.2, target_damage_gfx=[0.1, "shake", 0.9], sfx="content/sfx/sound/be/earth2.mp3", piercing=True, type="all_enemies",
                                           aim="bc", anchor=(0.5, 1.0), yo=40,
                                           desc="Small part of the target becomes stone and shatters into a thousand pieces.")
        SimpleMagicalAttack(u"Mudslide", menu_pos=10, attributes=['magic', 'earth'], effect=65, multiplier=1.5, cost=12, range=4,
                                           desc="Dirt, rocks and poisonous gases are pulled out of the ground under high pressure.",
                                           attacker_effects={"gfx": "earth_2", "sfx": "default"},
                                           main_effect={"gfx": Transform('earth_5', zoom=1.5), "sfx": "content/sfx/sound/be/earth4.mp3", "duration": 2.8, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                                           target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 2.7},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.1},
                                           target_death_effect={"gfx": "dissolve", "initial_pause": 2.0, "duration": 0.5})
        SimpleMagicalAttack(u"Transmutation", menu_pos=11, menuname="Transmute", attributes=['magic', 'earth'], effect=50, multiplier=1.5, cost=10, range=4, casting_effects=["earth_2", "default"], gfx='earth_6', zoom=1.5, pause=2.0, target_damage_gfx=[0.2, "shake", 1.8], sfx="content/sfx/sound/be/earth6.mp3", piercing=True,
                                           aim="bc", anchor=(0.5, 1.0), yo=50,
                                           desc="The land itself under the target becomes explosive and detonates.")
        SimpleMagicalAttack(u"Rift Line", menu_pos=12, attributes=['magic', 'earth'], effect=70, multiplier=1.8, cost=15, range=4, type="all_enemies", piercing=True, true_pierce=True,
                                           desc="Brings a small flow of magma to the surface.",
                                           attacker_effects={"gfx": "earth_2", "sfx": "default"},
                                           main_effect={"gfx": Transform('magma', zoom=2.0), "sfx": "content/sfx/sound/be/rift_line.mp3", "duration": 3.2, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 75}},
                                           target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.7, "duration": 2.2},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.8},
                                           target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})
        ArealMagicalAttack("Fist of Bethel", menu_pos=13, menuname="FoB", attributes=['magic', 'earth'], effect=70, multiplier=3, cost=15, range=4, true_pierce=True, type="all_enemies", piercing=True,
                                        desc="Smite your enemies with might of the Earth itself!",
                                        attacker_effects={"gfx": "orb", "sfx": "default"},
                                        main_effect={"gfx": Transform(Transform("crushing_hand", xzoom=-1.0), zoom=2), "sfx": "content/sfx/sound/be/earth7.mp3", "duration": 2.7, "aim": {"anchor": (0.5, 1.0), "xo": 0 ,"yo": 150}, "hflip": True},
                                        target_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.7},
                                        target_sprite_damage_effect={"gfx": "shake", "initial_pause": 1.0, "duration": 1.7},
                                        target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 0.5},
                                        bg_main_effect={"gfx": "black", "initial_pause": 0, "duration": 2.7})
        
        # Air:
        SimpleMagicalAttack(u"Aero", menu_pos=0, attributes=['magic', 'air'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["air_1", "default"], gfx='air_1', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.3], sfx="content/sfx/sound/be/air2.mp3", type="all_enemies",
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="High pressure air cuts through armor and flesh like a hardened blade.")
        SimpleMagicalAttack(u"Aero webm", menu_pos=0, attributes=['magic', 'air'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["air_1", "default"], gfx='air_1', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.3], sfx="content/sfx/sound/be/air2.mp3", type="all_enemies",
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="High pressure air cuts through armor and flesh like a hardened blade.")
        SimpleMagicalAttack(u"Aerora", menu_pos=1, attributes=['magic', 'air'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["air_1", "default"], gfx='air_5', zoom=1.3, pause=0.9, target_damage_gfx=[0.1, "shake", 0.8], sfx="content/sfx/sound/be/air1.mp3",
                                           desc="Causes damage by sand and branches picked up by the wind rather than air itself.")    
        SimpleMagicalAttack(u"Aeroga", menu_pos=2, attributes=['magic', 'air'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["air_1", "default"], gfx='air_2', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.3], sfx="content/sfx/sound/be/air3.mp3", piercing=True,
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="Even for those who don't need to breathe instantaneous air pressure drop is dangerous.")
        SimpleMagicalAttack(u"Aeroja", menu_pos=3, attributes=['magic', 'air'], effect=10, multiplier=1.2, cost=4, range=4, casting_effects=["air_2", "default"], gfx='air_3', zoom=1.4, pause=1.5, target_damage_gfx=[0.1, "shake", 1.2], sfx="content/sfx/sound/be/air2.mp3", piercing=True, type="all_enemies",
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="High pressure air flows cover a small area.")
        SimpleMagicalAttack(u"Air Pressure", menu_pos=10, menuname="Pressure", attributes=['magic', 'air'], effect=50, multiplier=1.5, cost=10, range=4, casting_effects=["air_2", "default"], gfx='air_4', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.3], sfx="content/sfx/sound/be/air3.mp3", type="all_enemies", piercing=True,
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="Pumps air from the target, crushing it by external atmospheric pressure.")
        SimpleMagicalAttack(u"Air Blast", menu_pos=11, attributes=['magic', 'air'], effect=100, multiplier=1.5, cost=20, range=4, casting_effects=["air_2", "default"], gfx='air_6', zoom=1.5, pause=1.5, target_damage_gfx=[0.1, "shake", 1.0], sfx="content/sfx/sound/be/air3.mp3", piercing=True,
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="Pumps air into the target, tearing it from the inside.")
        SimpleMagicalAttack("Vortex", menu_pos=12, attributes=['magic', 'air'], effect=85, multiplier=1.8, cost=18, range=4, casting_effects=["orb", "default"], gfx='vortex', zoom=2.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.4], sfx="content/sfx/sound/be/vortex.mp3", type="all_enemies",
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="Creates a small, but very powerful sphere of hurricane winds around the target.")
        ArealMagicalAttack("Tornado", menu_pos=13, attributes=['magic', 'air'], effect=70, multiplier=1.8, cost=15, range=4, true_pierce=True, type="all_enemies", piercing=True,
                                        desc="Use a magical Tornado to wipe out your enemies!",
                                        attacker_effects={"gfx": "orb", "sfx": "default"},
                                        main_effect={"gfx": "tornado", "sfx": "content/sfx/sound/be/air4.mp3", "duration": 3.5, "aim": {"anchor": (0.5, 1.0), "xo": -80 ,"yo": 150}},
                                        target_damage_effect={"gfx": "battle_bounce", "initial_pause": 4.8},
                                        target_sprite_damage_effect={"gfx": "fly_away", "initial_pause": 0.2, "duration": 5.2},
                                        target_death_effect={"gfx": "shatter", "initial_pause": 4.7, "duration": 0.2})
    
        # Electricity:
        SimpleMagicalAttack(u"Thunder", menu_pos=0, attributes=['magic', 'electricity'], effect=20, multiplier=1.2, cost=5, range=5, casting_effects=["electricity_1", "default"], gfx='electricity_1', zoom=1.5, pause=1.0, target_damage_gfx=[0.2, "shake", 0.6], sfx="content/sfx/sound/be/thunder2.mp3", type="all_enemies",
                                           desc="Shocks targets with static electricity caused by friction of airborne particles.")
        SimpleMagicalAttack(u"Thundara", menu_pos=1, attributes=['magic', 'electricity'], effect=30, multiplier=1.2, cost=7, range=5, casting_effects=["electricity_1", "default"], gfx='electricity_2', zoom=1.7, pause=1.2, target_damage_gfx=[0.1, "shake", 1.1], sfx="content/sfx/sound/be/thunder4.mp3",
                                           desc="Surrounds the target by brief electricity field.", aim="bc", anchor=(0.5, 1.0), yo=50)
        SimpleMagicalAttack(u"Thundaga", menu_pos=2, attributes=['magic', 'electricity'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["electricity_2", "default"], gfx='electricity_4', zoom=1.8, pause=0.6, target_damage_gfx=[0.05, "shake", 1.0], sfx="content/sfx/sound/be/thunder3.mp3", piercing=True,
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="Creates plasma ball of ionized air near the target.")
        SimpleMagicalAttack(u"Thundaja", menu_pos=3, attributes=['magic', 'electricity'], effect=10, multiplier=1.2, cost=4, range=5, casting_effects=["electricity_1", "default"], gfx='electricity_3', zoom=2.2, pause=1.35, target_damage_gfx=[0.2, "shake", 1.0], sfx="content/sfx/sound/be/thunder.mp3", type="all_enemies", piercing=True,
                                           desc="Covers a small area by lightning discharges.", aim="bc", anchor=(0.5, 1.0), yo=50)
        SimpleMagicalAttack(u"Thunderstorm", menu_pos=6, menuname="TS", attributes=['magic', 'electricity'], effect=30, multiplier=1.5, cost=8, range=4, casting_effects=["electricity_2", "default"], gfx='electricity_5', zoom=1.6, pause=1.6, target_damage_gfx=[0.15, "shake", 1.45], sfx="content/sfx/sound/be/thunder5.mp3", type="all_enemies", piercing=True,
                                           aim="tc", anchor=(0.5, 0.5),
                                           desc="Сovers a small area by numerous high-voltage discharges.")
        SimpleMagicalAttack(u"Electromagnetism", menu_pos=10, menuname="EM", attributes=['magic', 'electricity'], effect=40, multiplier=1.5, cost=9, range=4, casting_effects=["electricity_2", "default"], gfx='electricity_6', zoom=1.8, pause=3.2, target_damage_gfx=[0.3, "shake", 2.9], sfx="content/sfx/sound/be/thunder6.mp3", type="all_enemies",
                                           aim="tc", anchor=(0.5, 0.5), yo=15,
                                           desc="Takes control over charged particles inside the target, causing severe internal injuries.")
        P2P_MagicAttack(u"Ion Blast", menu_pos=11, attributes=['magic', 'electricity'], effect=100, multiplier=1.8, cost=20, range=4, piercing=True, true_pierce=True,
                                      type="all_enemies", desc="Hits targets with clouds of charged particles.",
                                      projectile_effects={"gfx": 'ion_1', "sfx": "content/sfx/sound/be/ion_storm.mp3", "duration": 1.0},
                                      main_effect={"gfx": "ion", "sfx": None, "duration": 2.25},
                                      attacker_effects={"gfx": "orb", "sfx": "default"},
                                      target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.3, "duration": 1.4},
                                      target_death_effect={"gfx": "hide", "initial_pause": 0.7, "duration": 0.01})
        P2P_ArealMagicalAttack(u"Ion Storm", menu_pos=7, attributes=['magic', 'electricity'], effect=100, multiplier=1.8, cost=20, range=4, piercing=True, true_pierce=True,
                                                type="all_enemies", desc="Hits all targets with raging cloud of charged particles.",
                                                projectile_effects={"gfx": 'ion_1', "sfx": "content/sfx/sound/be/ion_storm.mp3", "duration": 1.0},
                                                main_effect={"gfx": Transform('ion', zoom=2.0), "sfx": None, "duration": 2.25, "aim": {"anchor": (0.5, 0.5), "xo": 0 ,"yo": 0}},
                                                attacker_effects={"gfx": "orb", "sfx": "default"},
                                                target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.3, "duration": 1.4},
                                                target_death_effect={"gfx": "hide", "initial_pause": 0.7, "duration": 0.01})
        SimpleMagicalAttack("Lighting Wrath", menu_pos=12, menuname="LW", attributes=['magic', 'electricity'], effect=70, multiplier=3.0, cost=15, range=4, true_pierce=True, type="se", piercing=True,
                                        desc="Hits the target with a powerful burst of lightning!",
                                        attacker_effects={"gfx": "orb", "sfx": "default"},
                                        main_effect={"gfx": Transform("thunder_storm_2", xzoom=1.2, yzoom=1.3), "start_at": 0, "sfx": "content/sfx/sound/be/thunder5.mp3", "duration": 1.6, "aim": {"point": "bc", "anchor": (0.5, 1.0), "xo": 0 ,"yo": 30}},
                                        target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.5},
                                        target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.4, "duration": 1.6},
                                        target_death_effect={"gfx": "dissolve", "initial_pause": 0.8, "duration": 0.5},
                                        bg_main_effect={"gfx": "black", "initial_pause": 0, "duration": 2.3})
        ArealMagicalAttack("Might of Zeus", menu_pos=13, menuname="MoZ", attributes=['magic', 'electricity'], effect=70, multiplier=4, cost=15, range=4, true_pierce=True, type="all_enemies", piercing=True,
                                        desc="The most powerful Lighting attack in the World!",
                                        attacker_effects={"gfx": "orb", "sfx": "default"},
                                        main_effect={"gfx": Transform("thunder_storm_3", zoom=1.2), "sfx": "content/sfx/sound/be/thunder7.mp3", "duration": 3.4, "aim": {"anchor": (0.5, 1.0), "xo": -10 ,"yo": 150}},
                                        target_damage_effect={"gfx": "battle_bounce", "initial_pause": 3.4},
                                        target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.9, "duration": 2.5},
                                        target_death_effect={"gfx": "dissolve", "initial_pause": 2.0, "duration": 0.5},
                                        bg_main_effect={"gfx": "black", "initial_pause": 0, "duration": 3.4})
        
        # Light:
        SimpleMagicalAttack(u"Holy", menu_pos=0, attributes=['magic', 'light'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["light_1", "default"], gfx='light_1', zoom=1.5, pause=1.25, target_damage_gfx=[0.1, "shake", 1.1], sfx="content/sfx/sound/be/light1.mp3", type="all_enemies",
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="A flash of energy burns targets from inside.")
        SimpleMagicalAttack(u"Holyra", menu_pos=1, attributes=['magic', 'light'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["light_1", "default"], gfx='light_2', zoom=1.5, pause=1.25, target_damage_gfx=[0.1, "shake", 1.1], sfx="content/sfx/sound/be/light3.mp3",
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="A sphere of light burns the target from all sides.")
        SimpleMagicalAttack(u"Holyda", menu_pos=2, attributes=['magic', 'light'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["light_1", "default"], gfx='light_3', zoom=2.5, pause=1.6, target_damage_gfx=[0.1, "shake", 1.5], sfx="content/sfx/sound/be/light4.mp3", piercing=True,
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="A smallest particle of stellar energy burns the target.")
        SimpleMagicalAttack(u"Holyja", menu_pos=3, attributes=['magic', 'light'], effect=10, multiplier=1.2, cost=4, range=4, piercing=True, type="all_enemies", 
                                           desc="Gathers holy energy around targets and releases it upwards like a pillar of light.",
                                           attacker_effects={"gfx": "light_2", "sfx": "default"},
                                           main_effect={"gfx": Transform("light_4", zoom=1.5), "sfx": "content/sfx/sound/be/light5.mp3", "duration": 2.04, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 60}},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.04},
                                           target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.5, "duration": 1.4},
                                           target_death_effect={"gfx": "hide", "initial_pause": 1.5, "duration": 0.0001})
                                           
        SimpleMagicalAttack(u"Photon Blade", menu_pos=10, menuname="PB", attributes=['magic', 'light'], effect=30, multiplier=1.5, cost=8, range=4, casting_effects=["light_2", "default"], gfx='light_5', zoom=1.9, pause=2.5, target_damage_gfx=[0.5, "shake", 1.4], sfx="content/sfx/sound/be/dawn.mp3", type="all_enemies", piercing=True,
                                           desc="Infinitely thin blades of pure light slices targets.")
        SimpleMagicalAttack(u"Star Light", menu_pos=11, attributes=['magic', 'light'], effect=50, multiplier=1.5, cost=10, range=4, casting_effects=["light_2", "default"], gfx='light_6', zoom=1.4, pause=1.8, target_damage_gfx=[0.1, "shake", 1.7], sfx="content/sfx/sound/be/light2.mp3", piercing=True,
                                           aim="center", anchor=(0.5, 0.5), desc="A powerful and painful flash of star light.")
        SimpleMagicalAttack("Forced Dawn", menu_pos=12, menuname="Dawn", attributes=['magic', 'light'], effect=70, multiplier=1.8, cost=15, range=4, type="all_enemies", piercing=True,
                                           desc="The energy of a whole sunrise quickly covers a small area.",
                                           attacker_effects={"gfx": "circle_3", "sfx": "default"},
                                           main_effect={"gfx": Transform("dawn", zoom=2.5), "sfx": "content/sfx/sound/be/dawn.mp3", "duration": 3.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 50, "xo": -50}},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.7},
                                           target_sprite_damage_effect={"gfx": "shake", "initial_pause": 1.5, "duration": 0.5},
                                           target_death_effect={"gfx": "dissolve", "initial_pause": 1.6, "duration": 1.0})
        ArealMagicalAttack("Holy Blast", menu_pos=13, attributes=['magic', 'light'], effect=70, multiplier=1.8, cost=15, range=4, true_pierce=True, type="all_enemies", piercing=True,
                                        desc="Concentrates all holy energy in the area into one point, forcing it to explode as it reaches critical levels!",
                                        attacker_effects={"gfx": "orb", "sfx": "default"},
                                        main_effect={"gfx": Transform("holy_blast", zoom=2.2), "sfx": "content/sfx/sound/be/light6.mp3", "duration": 3.7, "aim": {"anchor": (0.5, 1.0), "xo":-50 ,"yo": 320}},
                                        target_damage_effect={"gfx": "battle_bounce", "initial_pause": 3.7},
                                        target_sprite_damage_effect={"gfx": "shake", "initial_pause": 1.5, "duration": 2.2},
                                        target_death_effect={"gfx": "dissolve", "initial_pause": 2.7, "duration": 0.5})
                                        # bg_main_effect={"gfx": "mirrage", "initial_pause": 2.9, "duration": 2.4})
        
        # Darkness:
        SimpleMagicalAttack(u"Dark", menu_pos=0, attributes=['magic', 'darkness'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["dark_1", "default"], gfx='darkness_1', zoom=1.3, pause=1.0, target_damage_gfx=[0.1, "shake", 0.9], sfx="content/sfx/sound/be/darkness1.mp3", type="all_enemies",
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="The mere presence of dark energy is dangerous for most creatures.")
        SimpleMagicalAttack(u"Darkra", menu_pos=1, attributes=['magic', 'darkness'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["dark_1", "default"], gfx='darkness_2', zoom=1.4, pause=1.6, target_damage_gfx=[0.1, "shake", 1.4], sfx="content/sfx/sound/be/darkness2.mp3",
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="Darkness envelops the target, slowly killing it.")
        SimpleMagicalAttack(u"Darkga", menu_pos=2, attributes=['magic', 'darkness'], effect=25, multiplier=1.2, cost=6, range=4, target_damage_gfx=[0.9, "shake", 0.6], piercing=True,
                                          desc="Negative energy concentrates in a very small area and then explodes.",
                                          attacker_effects={"gfx": "dark_1", "sfx": "default"},
                                          main_effect={"gfx": Transform("darkness_3", zoom=1.4), "sfx": "content/sfx/sound/be/darkness3.mp3", "duration": 1.5, "aim": {"point": "center", "anchor": (0.5, 0.5)}},
                                          target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.9},
                                          target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.9, "duration": 0.6},
                                          target_death_effect={"gfx": "dissolve", "initial_pause": 1.0, "duration": 0.5})
        SimpleMagicalAttack(u"Darkja", menu_pos=3, attributes=['magic', 'darkness'], effect=10, multiplier=1.2, cost=4, range=4, casting_effects=["dark_2", "default"], gfx='darkness_4', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.2], sfx="content/sfx/sound/be/darkness2.mp3", piercing=True, type="all_enemies",
                                           aim="center", anchor=(0.5, 0.5),
                                           desc="Summons an abnormal and chaotic substances from a dark world that deforms targets.")
        SimpleMagicalAttack(u"Eternal Gluttony", menu_pos=10, menuname="EG", attributes=['magic', 'darkness'], effect=50, multiplier=1.5, cost=10, range=4, casting_effects=["dark_2", "default"], gfx='darkness_5', pause=1.2, target_damage_gfx=[0.1, "shake", 1.1], sfx="content/sfx/sound/be/horny2.mp3", piercing=True, 
                                           desc="Summons a dark creature to devour the target.")
        SimpleMagicalAttack(u"Black Hole", menu_pos=11, attributes=['magic', 'darkness'], effect=30, multiplier=1.5, cost=8, range=4, casting_effects=["dark_2", "default"], gfx='darkness_6', pause=1.5, target_damage_gfx=[0.1, "shake", 1.2], sfx="content/sfx/sound/be/darkness3.mp3", type="all_enemies", piercing=True,
                                           desc="Creates a hole in spaace that leads to a dark dimension.")
        SimpleMagicalAttack("Other Light", menu_pos=12, attributes=['magic', 'darkness'], effect=70, multiplier=1.8, cost=15, range=4, type="all_enemies", piercing=True, true_pierce=True,
                                           desc="Brings an alternative form of light from a dark dimension.",
                                           attacker_effects={"gfx": "orb", "sfx": "default"},
                                           main_effect={"gfx": Transform('darklight', zoom=1.5), "sfx": "content/sfx/sound/be/darklight.mp3", "duration": 2.0, "aim": {"point": "tc", "anchor": (0.5, 0), "yo": -55}},
                                           target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.3, "duration": 1.2},
                                           target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.8},
                                           target_death_effect={"gfx": "dissolve", "initial_pause": 0.8, "duration": 0.5})
        FullScreenCenteredArealMagicalAttack("Dominion", menu_pos=13, attributes=['magic', 'darkness'], effect=70, multiplier=1.8, cost=15, range=4, true_pierce=True, type="all_enemies", piercing=True,
                                                                        desc="Cut the darkness itself!",
                                                                        attacker_effects={"gfx": "orb", "sfx": "default"},
                                                                        main_effect={"gfx": "dominion", "sfx": "content/sfx/sound/be/darkness5.mp3", "duration": 2.5},
                                                                        target_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.5},
                                                                        target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 2.4},
                                                                        target_death_effect={"gfx": "dissolve", "initial_pause": 2, "duration": 0.5},
                                                                        bg_main_effect={"gfx": "black", "initial_pause": 0, "duration": 2.6})
                                           
        # Healing:
        BasicHealingSpell(u"Cure", attributes=['magic', 'healing'], effect=25, cost=8, range=5, type="sa",
                                      desc="Heals superficial wounds and accelerates the healing of internal ones.",
                                      attacker_action={"gfx": None},
                                      attacker_effects={"gfx": "runes_1", "sfx": "default"},
                                      main_effect={"gfx": Transform("heal_1", zoom=1.4), "sfx": "content/sfx/sound/be/heal1.mp3", "duration": 3.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                                      target_sprite_damage_effect={"gfx": None},
                                      target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.0},
                                      target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 1.5})
        BasicHealingSpell(u"Curaga", attributes=['magic', 'healing'], effect=10, cost=10, range=5, type="all_allies", piercing=True, true_pierce=True,
                                      desc="Heals the whole party at once.",
                                      attacker_action={"gfx": None},
                                      attacker_effects={"gfx": "runes_1", "sfx": "default"},
                                      main_effect={"gfx": Transform("heal_2", zoom=1.4), "sfx": "content/sfx/sound/be/heal2.mp3", "duration": 2.5, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": 0}},
                                      target_sprite_damage_effect={"gfx": None},
                                      target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.7},
                                      target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 1.5})
        ReviveSpell(u"Revive", attributes=['magic', 'revive'], effect=10, cost=10, range=5, type="sa", piercing=True, true_pierce=True, target_state="dead",
                             desc="Bring an ally back to the battlefield!",
                             attacker_action={"gfx": None},
                             attacker_effects={"gfx": "runes_1", "sfx": "default"},
                             main_effect={"gfx": Transform("resurrection", zoom=1.75), "sfx": "content/sfx/sound/be/heal2.mp3", "duration": 2.0, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": -150}},
                             target_sprite_damage_effect={"gfx": None},
                             target_damage_effect={"gfx": "battle_bounce", "initial_pause": 2.0},
                             target_death_effect={"gfx": None})
                                      
        # Effects:
        BasicPoisonSpell("Poison", attributes=['status', 'poison'], effect=100, multiplier=1.0, cost=30, range=4,
                                     desc="Poisons the target causing additional damage each turn!",
                                     attacker_effects={"gfx": "runes_1", "sfx": "default"},
                                     main_effect={"gfx": Transform("poison_1", zoom=2.1), "sfx": "content/sfx/sound/be/poison_01.ogg", "duration": 1.0, "aim": {"point": "center", "anchor": (0.5, 0.5), "yo": -25}},
                                     target_sprite_damage_effect={"gfx": None},
                                     target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.2},
                                     target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 0.5})
    return
