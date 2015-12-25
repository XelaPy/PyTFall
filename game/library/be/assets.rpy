# Assets of the BE:
init -1: # Images and Animations
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
    image fire_1 = FilmStrip('content/gfx/be/filmstrips/fire_1.png', (192, 192), (5, 4), 0.1, loop=False)
    image fire_2 = FilmStrip('content/gfx/be/filmstrips/fire_2.png', (192, 192), (5, 4), 0.1, loop=False)
    image fire_3 = FilmStrip('content/gfx/be/filmstrips/fire_3.png', (192, 192), (5, 7), 0.1, loop=False)
    image fire_4 = FilmStrip('content/gfx/be/filmstrips/fire_4.png', (192, 192), (5, 10), 0.1, loop=False)
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

    image water_1 = FilmStrip('content/gfx/be/filmstrips/water_1.png', (192, 192), (5, 3), 0.1, loop=False)
    image water_2 = FilmStrip('content/gfx/be/filmstrips/water_2.png', (192, 192), (5, 4), 0.1, loop=False)
    image water_3 = FilmStrip('content/gfx/be/filmstrips/water_3.png', (192, 192), (5, 5), 0.1, loop=False)
    image water_4 = FilmStrip('content/gfx/be/filmstrips/water_4.png', (192, 192), (5, 9), 0.05, loop=False)
    image water_5 = FilmStrip('content/gfx/be/filmstrips/water_5.png', (192, 192), (5, 6), 0.1, loop=False)
    image water_6 = FilmStrip('content/gfx/be/filmstrips/water_6.png', (192, 192), (5, 10), 0.1, loop=False, reverse=True)
    image rain = FilmStrip('content/gfx/be/filmstrips/rain.png', (192, 192), (5, 10), 0.05, loop=True)

    image earth_1 = FilmStrip('content/gfx/be/filmstrips/earth_1.png', (192, 192), (5, 4), 0.1, loop=False)
    image earth_2 = FilmStrip('content/gfx/be/filmstrips/earth_2.png', (192, 192), (5, 2), 0.1, loop=False)
    image earth_3 = FilmStrip('content/gfx/be/filmstrips/earth_3.png', (192, 192), (5, 3), 0.1, loop=False)
    image earth_4 = FilmStrip('content/gfx/be/filmstrips/earth_4.png', (192, 192), (5, 2), 0.12, loop=False)
    image earth_5 = FilmStrip('content/gfx/be/filmstrips/earth_5.png', (192, 192), (5, 8), 0.07, loop=False)
    image earth_6 = FilmStrip('content/gfx/be/filmstrips/earth_6.png', (192, 192), (5, 4), 0.1, loop=False)
    image magma = FilmStrip('content/gfx/be/filmstrips/magma.png', (192, 192), (5, 8), 0.08, loop=False)
    
    image air_1 = FilmStrip('content/gfx/be/filmstrips/air_1.png', (192, 192), (5, 5), 0.06, loop=False)
    image air_2 = FilmStrip('content/gfx/be/filmstrips/air_2.png', (192, 192), (5, 5), 0.06, loop=False)
    image air_3 = FilmStrip('content/gfx/be/filmstrips/air_3.png', (192, 192), (5, 5), 0.06, loop=False)
    image air_4 = FilmStrip('content/gfx/be/filmstrips/air_4.png', (192, 192), (5, 6), 0.05, loop=False)
    image air_6 = FilmStrip('content/gfx/be/filmstrips/air_6.png', (151, 151), (5, 7), 0.06, loop=False, reverse=True)
    image vortex = FilmStrip('content/gfx/be/filmstrips/vortex.png', (277, 277), (15, 1), 0.1, loop=True)
    
    image light_1 = FilmStrip('content/gfx/be/filmstrips/light_1.png', (192, 192), (5, 5), 0.05, loop=False)
    image light_2 = FilmStrip('content/gfx/be/filmstrips/light_2.png', (192, 192), (5, 5), 0.05, loop=False)
    image light_3 = FilmStrip('content/gfx/be/filmstrips/light_3.png', (100, 100), (5, 16), 0.02, loop=False)
    image light_5 = FilmStrip('content/gfx/be/filmstrips/light_5.png', (192, 192), (5, 5), 0.1, loop=False)
    image light_6 = FilmStrip('content/gfx/be/filmstrips/light_6.png', (153, 160), (4, 3), 0.15, loop=False)
    image dawn = FilmStrip('content/gfx/be/filmstrips/dawn.png', (192, 192), (5, 7), 0.1, loop=False)

    image darkness_1 = FilmStrip('content/gfx/be/filmstrips/darkness_1.png', (192, 192), (5, 4), 0.05, loop=False)
    image darkness_2 = FilmStrip('content/gfx/be/filmstrips/darkness_2.png', (192, 192), (5, 4), 0.08, loop=False)
    image darkness_3 = FilmStrip('content/gfx/be/filmstrips/darkness_3.png', (192, 192), (5, 6), 0.05, loop=False)
    image darkness_4 = FilmStrip('content/gfx/be/filmstrips/darkness_4.png', (192, 192), (5, 6), 0.05, loop=False)
    image darkness_5 = FilmStrip('content/gfx/be/filmstrips/darkness_5.png', (375, 500), (4, 3), 0.1, loop=False)
    image darkness_6 = FilmStrip('content/gfx/be/filmstrips/darkness_6.png', (192, 192), (5, 3), 0.1, loop=False)
    image darklight = FilmStrip('content/gfx/be/filmstrips/darklight.png', (144, 192), (5, 4), 0.1, loop=False)

    image poison_1 = FilmStrip('content/gfx/be/filmstrips/poison_1.png', (192, 192), (5, 6), 0.07, loop=False)
    image poison_2 = FilmStrip('content/gfx/be/filmstrips/poison_2.png', (192, 192), (5, 3), 0.1, loop=False)
    image poison_3 = FilmStrip('content/gfx/be/filmstrips/poison_3.png', (192, 192), (5, 5), 0.06, loop=False)

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
    image heal_1 = FilmStrip('content/gfx/be/filmstrips/heal_1.png', (192, 192), (5, 6), 0.1, loop=False)
    image heal_2 = FilmStrip('content/gfx/be/filmstrips/heal_2.png', (192, 192), (5, 5), 0.1, loop=False)
    image bg test_grid = "content/gfx/bg/maps/map17x6.jpg"

# Skillz:
init 2 python:
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
    SimpleMagicalAttack(u"Fire", attributes=['magic', 'fire'], effect=20, multiplier=1.2, type="all_enemies", cost=5, range=4, desc="Ignites a small plot of land.",
                                       attacker_effects={"gfx": "fire_1"},
                                       main_effect={"gfx": Transform("fire_1", zoom=1.7), "sfx": "content/sfx/sound/be/fire4.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 50}},
                                       target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 0.9},
                                       target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 1.5})
    SimpleMagicalAttack(u"Fira", attributes=['magic', 'fire'], effect=30, multiplier=1.2, cost=7, range=4, desc="Ignites the air in a limited area.",
                                       attacker_effects = {"gfx": "fire_1"},
                                       main_effect={"gfx": Transform("fire_2", zoom=1.5), "sfx": "content/sfx/sound/be/fire4.mp3", "duration": 2.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                                       target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.1, "duration": 1.3},
                                       target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 1.5})
    SimpleMagicalAttack(u"Firaga", attributes=['magic', 'fire'], effect=25, multiplier=1.2, cost=6, range=4, piercing=True, desc="Creates liquid fire that envelopes the target, causing massive burns.",
                                       attacker_effects={"gfx": "fire_2"},
                                       main_effect={"gfx": Transform("fire_4", zoom=1.5), "sfx": "content/sfx/sound/be/fire6.mp3", "duration": 5.0, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                                       target_sprite_damage_effect={"gfx": "shake", "initial_pause": 1.3, "duration": 3.2},
                                       target_damage_effect={"gfx": "battle_bounce", "initial_pause": 1.3},
                                       target_death_effect={"gfx": "dissolve", "initial_pause": 1.5, "duration": 1.5})
    SimpleMagicalAttack(u"Firaja", attributes=['magic', 'fire'], effect=10, multiplier=1.2, cost=15, range=4, type="all_enemies", piercing=True, desc="Creates a rain of fire that hits all enemies.",
                                       attacker_effects={"gfx": "fire_1"},
                                       main_effect={"gfx": Transform("fire_3", zoom=1.5), "sfx": "content/sfx/sound/be/fire5.mp3", "duration": 3.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}},
                                       target_sprite_damage_effect={"gfx": "shake", "initial_pause": 0.2, "duration": 1.4},
                                       target_damage_effect={"gfx": "battle_bounce", "initial_pause": 0.3},
                                       target_death_effect={"gfx": "dissolve", "initial_pause": 0.3, "duration": 1.5})
    # TODO:
    P2P_MagicAttack(u"Fireball", attributes=['magic', 'fire'], effect=50, multiplier=1.5, cost=10, range=4, casting_effects=["fire_2", "default"], gfx='fire_6', gfx2='fire_6_1', pause=1.0, pause2=1.2, sfx="content/sfx/sound/be/fire7.mp3", piercing=True,
                                       desc="Launches an exploding fireball at one enemy.")
    P2P_MagicAttack(u"Solar Flash", attributes=['magic', 'fire'], effect=65, multiplier=1.5, cost=12, range=4, casting_effects=["fire_2", "default"], gfx='fire_5', gfx2='fire_5_1', pause=1.5, pause2=1, sfx="content/sfx/sound/be/fire7.mp3",
                                       desc="Sends towards the target a small piece of solar plazma.")
    MagicArrows(u"Fire Arrow", attributes=['magic', 'fire'], effect=100, multiplier=1.8, cost=20, range=4, casting_effects=["default_1", "default"], gfx='Fire Arrow cast', gfx2='Fire Arrow fly', gfx3='Fire Arrow impact', sfx="content/sfx/sound/be/fire_arrow.mp3", piercing=True,
                                       desc="Creates a bow and arrow of scorching air.")
    
    SimpleMagicalAttack("Cataclysm", attributes=['magic', 'fire'], effect=70, multiplier=1.8, cost=15, range=4, true_pierce=True, type="all_enemies", desc="Summons flaming fragments of meteor from the atmosphere directly above the target.",
                                       attacker_effects={"gfx": "orb", "sfx": "default"},
                                       main_effect={"gfx": Transform('cataclysm', yzoom=1.2, xzoom=1.2), "sfx": "content/sfx/sound/be/fire2.mp3", "duration": 5.5, "aim": {"point": "bc", "anchor": (0.5, 0.8), "yo": 0}, "start_at": 0},
                                       target_sprite_damage_effect={"gfx": "shake", "sfx": None, "initial_pause": 2.0, "duration": 2.5},
                                       target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                                       target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 0.1, "duration": 0.9})
    # TODO:
    ArealMagicalAttack("Pure Cataclysm", attributes=['magic', 'fire'], effect=70, multiplier=1.8, cost=15, range=4, casting_effects=["orb", "default"], true_pierce=True, gfx='cataclysm', zoom=2.2, pause=5.5, target_damage_gfx=[2.0, "shake", 2.5], sfx="content/sfx/sound/be/fire2.mp3", type="all_enemies", piercing=True,
                                    aim="bc", anchor=(0.5, 1.0), xo=-50, yo=320,
                                    desc="Summons flaming fragments of meteors from the atmosphere directly above the target.")


    
    # Water:
    SimpleMagicalAttack(u"Water", attributes=['magic', 'water'], effect=10, multiplier=1.2, cost=4, range=4, type="all_enemies", desc="Crushes targets by bubbles of water.",
                                       attacker_effects={"gfx": "water_1", "sfx": "default"},
                                       main_effect={"gfx": Transform('water_1', zoom=1.1), "sfx": "content/sfx/sound/be/water.mp3", "duration": 1.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                                       target_sprite_damage_effect={"gfx": "shake", "sfx": None, "initial_pause": 0.1, "duration": 1.4},
                                       target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                                       target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 0.1, "duration": 0.9})
    SimpleMagicalAttack(u"Watera", attributes=['magic', 'water'], effect=30, multiplier=1.2, cost=7, range=4, desc="High pressure water jets pierce through the target.",
                                       attacker_effects={"gfx": "water_1", "sfx": "default"},
                                       main_effect={"gfx": Transform('water_1', zoom=1.1), "sfx": "content/sfx/sound/be/water.mp3", "duration": 1.5, "aim": {"point": "bc", "anchor": (0.5, 1.0), "yo": 40}, "start_at": 0},
                                       target_sprite_damage_effect={"gfx": "shake", "sfx": None, "initial_pause": 0.1, "duration": 1.4},
                                       target_damage_effect={"gfx": "battle_bounce", "sfx": None},
                                       target_death_effect={"gfx": "dissolve", "sfx": None, "initial_pause": 0.1, "duration": 0.9})
    SimpleMagicalAttack(u"Watera", attributes=['magic', 'water'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["water_1", "default"], gfx='water_2', zoom=1.4, pause=2.0, target_damage_gfx=[0.1, "shake", 1.5], sfx="content/sfx/sound/be/water.mp3",
                                       aim="bc", anchor=(0.5, 1.0), yo=40,
                                       desc="High pressure water jets pierce through the target.")
    SimpleMagicalAttack(u"Waterga", attributes=['magic', 'water'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["water_1", "default"], gfx='water_3', zoom=1.5, pause=2.5, target_damage_gfx=[0.1, "shake", 2.0], sfx="content/sfx/sound/be/water2.mp3", piercing=True,
                                       aim="bc", anchor=(0.5, 1.0), yo=40,
                                       desc="A cloud of water droplets at high speed crashes into the target.")
    SimpleMagicalAttack(u"Waterja", attributes=['magic', 'water'], effect=30, multiplier=1.5, cost=8, range=4, casting_effects=["water_2", "default"], gfx='water_4', zoom=1.5, pause=2.25, target_damage_gfx=[0.1, "shake", 2.0], sfx="content/sfx/sound/be/water3.mp3", type="all_enemies", piercing=True,
                                       aim="bc", anchor=(0.5, 1.0), yo=40,
                                       desc="Evaporates some water from targets.")
    SimpleMagicalAttack(u"Geyser", attributes=['magic', 'water'], effect=65, multiplier=1.5, cost=12, range=6, casting_effects=["water_2", "default"], gfx='water_5', zoom=1.9, pause=3.0, target_damage_gfx=[0.5, "shake", 2.5], sfx="content/sfx/sound/be/water6.mp3",
                                       aim="bc", anchor=(0.5, 1.0), yo=60,
                                       desc="A powerful stream of water shoots out of the ground directly beneath the target.")
    SimpleMagicalAttack(u"Last Drop", attributes=['magic', 'water'], effect=50, multiplier=1.5, cost=10, range=6, casting_effects=["water_2", "default"], gfx='water_6', zoom=2.1, pause=5.0, target_damage_gfx=[0.5, "shake", 3], sfx="content/sfx/sound/be/water5.mp3", piercing=True,
                                       aim="bc", anchor=(0.5, 1.0), yo=60,
                                       desc="Evaporates a great deal of water from the target.")
    SimpleMagicalAttack(u"Heavy Rain", attributes=['magic', 'water'], effect=70, multiplier=1.8, true_pierce=True, cost=15, range=6, casting_effects=["water_2", "default"], gfx='rain', zoom=2.0, pause=5.0, target_damage_gfx=[0.25, "shake", 4.75], sfx="content/sfx/sound/be/heavy_rain.mp3", type="all_enemies", piercing=True,
                                       aim="bc", anchor=(0.5, 1.0), yo=80,
                                       desc="Summons a rain of extra heavy water from another dimension.")


    # Ice:
    MagicArrows("Ice Arrow", attributes=['magic', 'ice'], effect=50, multiplier=1.5, cost=10, range=4, casting_effects=["ice_2", "default"], gfx='Ice Arrow cast', gfx2='Ice Arrow fly', gfx3='Ice Arrow impact', sfx="content/sfx/sound/be/ice_arrow.mp3",
                                       desc="Creates a an arrow of ice crystals that pierces through the target.")
    SimpleMagicalAttack(u"Blizzard", attributes=['magic', 'ice'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["ice_1", "default"], gfx='ice_1', zoom=1.9, pause=2.9, target_damage_gfx=[0.2, "shake", 1.8], sfx="content/sfx/sound/be/ice3.mp3", type="all_enemies",
                                       aim="bc", anchor=(0.5, 1.0), yo=60,
                                       desc="Creates a cloud of sharp ice splinters.")
    SimpleMagicalAttack(u"Blizzara", attributes=['magic', 'ice'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["ice_1", "default"], gfx='ice_2', zoom=1.3, pause=1.5, target_damage_gfx=[0.1, "shake", 1.55], sfx="content/sfx/sound/be/ice1.mp3",
                                       aim="bc", anchor=(0.5, 1.0), yo=80,
                                       desc="Ice blades grow out of the ground.")
    SimpleMagicalAttack(u"Blizzarga", attributes=['magic', 'ice'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["ice_2", "default"], gfx='ice_4', zoom=1.5, pause=0.8, target_damage_gfx=[0.1, "shake", 0.75], sfx="content/sfx/sound/be/ice2.mp3", piercing=True,
                                       aim="bc", anchor=(0.5, 1.0), yo=40,
                                       desc="Freezes the air itself around the target, creating deadly ice blades.")
    SimpleMagicalAttack(u"Blizzarja", attributes=['magic', 'ice'], effect=10, multiplier=1.2, cost=4, range=4, casting_effects=["ice_1", "default"], gfx='ice_3', zoom=1.7, pause=1.25, target_damage_gfx=[0.1, "shake", 1.1], sfx="content/sfx/sound/be/ice2.mp3", type="all_enemies", piercing=True,
                                       aim="bc", anchor=(0.5, 1.0), yo=60,
                                       desc="Quickly draws heat from a small area.")
    SimpleMagicalAttack(u"Zero Prism", attributes=['magic', 'ice'], effect=65, multiplier=1.5, cost=12, range=4, casting_effects=["ice_2", "default"], gfx='ice_5', zoom=2.1, pause=2.1, target_damage_gfx=[0.3, "shake", 1.5], sfx="content/sfx/sound/be/ice4.mp3",
                                       aim="bc", anchor=(0.5, 1.0), yo=110, death_effect="shatter",
                                       desc="Freezes the target into a solid ice block.")
    SimpleMagicalAttack(u"Ice Shards", attributes=['magic', 'ice'], effect=30, multiplier=1.5, cost=8, range=4, casting_effects=["ice_2", "default"], gfx='ice_6', zoom=2.0, pause=1.2, target_damage_gfx=[0.1, "shake", 0.7], sfx="content/sfx/sound/be/ice2.mp3", piercing=True, type="all_enemies",
                                       aim="bc", anchor=(0.5, 1.0), yo=80,
                                       desc="Small part of the target immediately freezes and explodes.")
    SimpleMagicalAttack("Hailstorm", attributes=['magic', 'ice'], effect=100, multiplier=1.8, cost=20, range=4, casting_effects=["orb", "default"], gfx='ice_7', zoom=1.7, pause=2.0, target_damage_gfx=[0.1, "shake", 1.9], sfx="content/sfx/sound/be/Hailstorm.mp3", piercing=True, true_pierce=True,
                                       aim="bc", anchor=(0.5, 1.0), yo=50,
                                       desc="Puts the target in a middle of a small, but violent snow storm.")
    # Earth:
    SimpleMagicalAttack(u"Stone", attributes=['magic', 'earth'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["earth_1", "default"], gfx='earth_1', zoom=1.4, pause=2.0, target_damage_gfx=[0.1, "shake", 1.7], sfx="content/sfx/sound/be/earth.mp3", type="all_enemies",
                                       aim="bc", anchor=(0.5, 1.0), yo=40,
                                       desc="Creates cloud of fragments of hardened clay.")
    SimpleMagicalAttack(u"Stonera", attributes=['magic', 'earth'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["earth_1", "default"], gfx='earth_2', zoom=1.0, pause=1.5, target_damage_gfx=[0.1, "shake", 0.8], sfx="content/sfx/sound/be/earth.mp3",
                                       aim="bc", anchor=(0.5, 1.0), yo=10,
                                       desc="Creates a spall, yet sharp spike.")
    SimpleMagicalAttack(u"Stonega", attributes=['magic', 'earth'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["earth_1", "default"], gfx='earth_3', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.2], sfx="content/sfx/sound/be/earth3.mp3", piercing=True,
                                       aim="bc", anchor=(0.5, 0.5), yo=0,
                                       desc="A small amount of magma moves to the surface, spilling on the target.")
    SimpleMagicalAttack(u"Stoneja", attributes=['magic', 'earth'], effect=10, multiplier=1.2, cost=7, range=4, casting_effects=["earth_2", "default"], gfx='earth_4', zoom=1.2, pause=1.2, target_damage_gfx=[0.1, "shake", 0.9], sfx="content/sfx/sound/be/earth2.mp3", piercing=True, type="all_enemies",
                                       aim="bc", anchor=(0.5, 1.0), yo=40,
                                       desc="Small part of the target becomes stone and shatters into a thousand pieces.")
    SimpleMagicalAttack(u"Mudslide", attributes=['magic', 'earth'], effect=65, multiplier=1.5, cost=12, range=4, casting_effects=["earth_2", "default"], gfx='earth_5', zoom=1.5, pause=2.8, target_damage_gfx=[0.1, "shake", 2.6], sfx="content/sfx/sound/be/earth4.mp3",
                                       aim="bc", anchor=(0.5, 1.0), yo=40,
                                       desc="Dirt, rocks and poisonous gases are pulled out of the ground under high pressure.")
    SimpleMagicalAttack(u"Transmutation", attributes=['magic', 'earth'], effect=50, multiplier=1.5, cost=10, range=4, casting_effects=["earth_2", "default"], gfx='earth_6', zoom=1.5, pause=2.0, target_damage_gfx=[0.2, "shake", 1.8], sfx="content/sfx/sound/be/earth6.mp3", piercing=True,
                                       aim="bc", anchor=(0.5, 1.0), yo=50,
                                       desc="The land itself under the target becomes explosive and detonates.")
    SimpleMagicalAttack(u"Rift Line", attributes=['magic', 'earth'], effect=70, multiplier=1.8, cost=15, range=4, casting_effects=["earth_2", "default"], gfx='magma', zoom=2.0, pause=3.2, target_damage_gfx=[0.5, "shake", 2.2], sfx="content/sfx/sound/be/rift_line.mp3", type="all_enemies", piercing=True, true_pierce=True,
                                       aim="bc", anchor=(0.5, 1.0), yo=50,
                                       desc="Brings a small flow of magma to the surface.")

    
    # Air:
    SimpleMagicalAttack(u"Aero", attributes=['magic', 'air'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["air_1", "default"], gfx='air_1', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.3], sfx="content/sfx/sound/be/air2.mp3", type="all_enemies",
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="High pressure air cuts through armor and flesh like a hardened blade.")
    SimpleMagicalAttack(u"Aerora", attributes=['magic', 'air'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["air_1", "default"], gfx='air_5', zoom=1.3, pause=0.9, target_damage_gfx=[0.1, "shake", 0.8], sfx="content/sfx/sound/be/air1.mp3",
                                       desc="Causes damage by sand and branches picked up by the wind rather than air itself.")    
    SimpleMagicalAttack(u"Aeroga", attributes=['magic', 'air'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["air_1", "default"], gfx='air_2', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.3], sfx="content/sfx/sound/be/air3.mp3", piercing=True,
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="Even for those who don't need to breathe instantaneous air pressure drop is dangerous.")
    SimpleMagicalAttack(u"Aeroja", attributes=['magic', 'air'], effect=10, multiplier=1.2, cost=4, range=4, casting_effects=["air_2", "default"], gfx='air_3', zoom=1.4, pause=1.5, target_damage_gfx=[0.1, "shake", 1.2], sfx="content/sfx/sound/be/air2.mp3", piercing=True, type="all_enemies",
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="High pressure air flows cover a small area.")
    SimpleMagicalAttack(u"Air Pressure", attributes=['magic', 'air'], effect=50, multiplier=1.5, cost=10, range=4, casting_effects=["air_2", "default"], gfx='air_4', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.3], sfx="content/sfx/sound/be/air3.mp3", type="all_enemies", piercing=True,
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="Pumps air from the target, crushing it by external atmospheric pressure.")
    SimpleMagicalAttack(u"Air Blast", attributes=['magic', 'air'], effect=100, multiplier=1.5, cost=20, range=4, casting_effects=["air_2", "default"], gfx='air_6', zoom=1.5, pause=1.5, target_damage_gfx=[0.1, "shake", 1.0], sfx="content/sfx/sound/be/air3.mp3", piercing=True,
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="Pumps air into the target, tearing it from the inside.")
    SimpleMagicalAttack("Vortex", attributes=['magic', 'air'], effect=85, multiplier=1.8, cost=18, range=4, casting_effects=["orb", "default"], gfx='vortex', zoom=2.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.4], sfx="content/sfx/sound/be/vortex.mp3", type="all_enemies",
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="Creates a small, but very powerful sphere of hurricane winds around the target.")

    # Electricity:
    SimpleMagicalAttack(u"Thunder", attributes=['magic', 'electricity'], effect=20, multiplier=1.2, cost=5, range=5, casting_effects=["electricity_1", "default"], gfx='electricity_1', zoom=1.5, pause=1.0, target_damage_gfx=[0.2, "shake", 0.6], sfx="content/sfx/sound/be/thunder2.mp3", type="all_enemies",
                                       desc="Shocks targets with static electricity caused by friction of airborne particles.")
    SimpleMagicalAttack(u"Thundara", attributes=['magic', 'electricity'], effect=30, multiplier=1.2, cost=7, range=5, casting_effects=["electricity_1", "default"], gfx='electricity_2', zoom=1.7, pause=1.2, target_damage_gfx=[0.1, "shake", 1.1], sfx="content/sfx/sound/be/thunder4.mp3",
                                       desc="Surrounds the target by brief electricity field.", aim="bc", anchor=(0.5, 1.0), yo=50)
    SimpleMagicalAttack(u"Thundaga", attributes=['magic', 'electricity'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["electricity_2", "default"], gfx='electricity_4', zoom=1.8, pause=0.6, target_damage_gfx=[0.05, "shake", 1.0], sfx="content/sfx/sound/be/thunder3.mp3", piercing=True,
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="Creates plasma ball of ionized air near the target.")
    SimpleMagicalAttack(u"Thundaja", attributes=['magic', 'electricity'], effect=10, multiplier=1.2, cost=4, range=5, casting_effects=["electricity_1", "default"], gfx='electricity_3', zoom=2.2, pause=1.35, target_damage_gfx=[0.2, "shake", 1.0], sfx="content/sfx/sound/be/thunder.mp3", type="all_enemies", piercing=True,
                                       desc="Covers a small area by lightning discharges.", aim="bc", anchor=(0.5, 1.0), yo=50)
    SimpleMagicalAttack(u"Thunderstorm", attributes=['magic', 'electricity'], effect=30, multiplier=1.5, cost=8, range=4, casting_effects=["electricity_2", "default"], gfx='electricity_5', zoom=1.6, pause=1.6, target_damage_gfx=[0.15, "shake", 1.45], sfx="content/sfx/sound/be/thunder5.mp3", type="all_enemies", piercing=True,
                                       aim="tc", anchor=(0.5, 0.5),
                                       desc="Сovers a small area by numerous high-voltage discharges.")
    SimpleMagicalAttack(u"Electromagnetism", attributes=['magic', 'electricity'], effect=40, multiplier=1.5, cost=9, range=4, casting_effects=["electricity_2", "default"], gfx='electricity_6', zoom=1.8, pause=3.2, target_damage_gfx=[0.3, "shake", 2.9], sfx="content/sfx/sound/be/thunder6.mp3", type="all_enemies",
                                       aim="tc", anchor=(0.5, 0.5), yo=15,
                                       desc="Takes control over charged particles inside the target, causing severe internal injuries.")

    P2P_MagicAttack(u"Ion Storm", attributes=['magic', 'electricity'], effect=100, multiplier=1.8, cost=20, range=4, casting_effects=["orb", "default"], gfx='ion_1', gfx2='ion', pause=1, pause2=1, sfx="content/sfx/sound/be/ion_storm.mp3", piercing=True, true_pierce=True,
                                  desc="Sends towards the target a raging cloud of charged particles.")
    P2P_ArealMagicalAttack(u"Pure Ion Storm", attributes=['magic', 'electricity'], effect=100, multiplier=1.8, cost=20, range=4, casting_effects=["orb", "default"], gfx='ion_1', gfx2=Transform('ion', zoom=2.5), pause=1, pause2=1, sfx="content/sfx/sound/be/ion_storm.mp3", piercing=True, true_pierce=True,
                                            type="all_enemies", desc="Sends towards the target a raging cloud of charged particles.")
    # Light:
    SimpleMagicalAttack(u"Holy", attributes=['magic', 'light'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["light_1", "default"], gfx='light_1', zoom=1.5, pause=1.25, target_damage_gfx=[0.1, "shake", 1.1], sfx="content/sfx/sound/be/light1.mp3", type="all_enemies",
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="A flash of energy burns targets from inside.")
    SimpleMagicalAttack(u"Holyra", attributes=['magic', 'light'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["light_1", "default"], gfx='light_2', zoom=1.5, pause=1.25, target_damage_gfx=[0.1, "shake", 1.1], sfx="content/sfx/sound/be/light3.mp3",
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="A sphere of light burns the target from all sides.")
    SimpleMagicalAttack(u"Holyda", attributes=['magic', 'light'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["light_1", "default"], gfx='light_3', zoom=2.5, pause=1.6, target_damage_gfx=[0.1, "shake", 1.5], sfx="content/sfx/sound/be/light4.mp3", piercing=True,
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="A smallest particle of stellar energy burns the target.")
    SimpleMagicalAttack(u"Holyja", attributes=['magic', 'light'], effect=10, multiplier=1.2, cost=4, range=4, casting_effects=["light_2", "default"], gfx='light_4', zoom=1.5, pause=2.04, target_damage_gfx=[0.5, "shake", 1.4], sfx="content/sfx/sound/be/light5.mp3", piercing=True, type="all_enemies", 
                                       aim="bc", anchor=(0.5, 1.0), yo=70,
                                       desc="Gathers light around targets and then instantly releases it in the form of light beams.")
    SimpleMagicalAttack(u"Photon Blade", attributes=['magic', 'light'], effect=30, multiplier=1.5, cost=8, range=4, casting_effects=["light_2", "default"], gfx='light_5', zoom=1.9, pause=2.5, target_damage_gfx=[0.5, "shake", 1.4], sfx="content/sfx/sound/be/dawn.mp3", type="all_enemies", piercing=True,
                                       desc="Infinitely thin blades of pure light slices targets.")
    SimpleMagicalAttack(u"Star Light", attributes=['magic', 'light'], effect=50, multiplier=1.5, cost=10, range=4, casting_effects=["light_2", "default"], gfx='light_6', zoom=1.4, pause=1.8, target_damage_gfx=[0.1, "shake", 1.7], sfx="content/sfx/sound/be/light2.mp3", piercing=True,
                                       aim="center", anchor=(0.5, 0.5), desc="A powerful and painful flash of star light.")
    SimpleMagicalAttack("Forced Dawn", attributes=['magic', 'light'], effect=70, multiplier=1.8, cost=15, range=4, casting_effects=["circle_3", "default"], gfx='dawn', zoom=2.5, pause=3.5, target_damage_gfx=[1.7, "shake", 1.2], sfx="content/sfx/sound/be/dawn.mp3", type="all_enemies", piercing=True,
                                       aim="bc", anchor=(0.5, 1.0), yo=40,
                                       desc="The energy of a whole sunrise quickly covers a small area.")
    
    # Darkness:
    SimpleMagicalAttack(u"Dark", attributes=['magic', 'darkness'], effect=20, multiplier=1.2, cost=5, range=4, casting_effects=["dark_1", "default"], gfx='darkness_1', zoom=1.3, pause=1.0, target_damage_gfx=[0.1, "shake", 0.9], sfx="content/sfx/sound/be/darkness1.mp3", type="all_enemies",
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="The mere presence of dark energy is dangerous for most creatures.")
    SimpleMagicalAttack(u"Darkra", attributes=['magic', 'darkness'], effect=30, multiplier=1.2, cost=7, range=4, casting_effects=["dark_1", "default"], gfx='darkness_2', zoom=1.4, pause=1.6, target_damage_gfx=[0.1, "shake", 1.4], sfx="content/sfx/sound/be/darkness2.mp3",
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="Darkness envelops the target, slowly killing it.")
    SimpleMagicalAttack(u"Darkga", attributes=['magic', 'darkness'], effect=25, multiplier=1.2, cost=6, range=4, casting_effects=["dark_1", "default"], gfx='darkness_3', zoom=1.4, pause=1.5, target_damage_gfx=[0.9, "shake", 0.6], sfx="content/sfx/sound/be/darkness3.mp3", piercing=True,
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="Negative energy concentrates in a very small area and then explodes.")
    SimpleMagicalAttack(u"Darkja", attributes=['magic', 'darkness'], effect=10, multiplier=1.2, cost=4, range=4, casting_effects=["dark_2", "default"], gfx='darkness_4', zoom=1.2, pause=1.5, target_damage_gfx=[0.1, "shake", 1.2], sfx="content/sfx/sound/be/darkness2.mp3", piercing=True, type="all_enemies",
                                       aim="center", anchor=(0.5, 0.5),
                                       desc="Summons an abnormal and chaotic substances from a dark world that deforms targets.")
    SimpleMagicalAttack(u"Eternal Gluttony", attributes=['magic', 'darkness'], effect=50, multiplier=1.5, cost=10, range=4, casting_effects=["dark_2", "default"], gfx='darkness_5', pause=1.2, target_damage_gfx=[0.1, "shake", 1.1], sfx="content/sfx/sound/be/horny2.mp3", piercing=True, 
                                       desc="Summons a dark creature to devour the target.")
    SimpleMagicalAttack(u"Black Hole", attributes=['magic', 'darkness'], effect=30, multiplier=1.5, cost=8, range=4, casting_effects=["dark_2", "default"], gfx='darkness_6', pause=1.5, target_damage_gfx=[0.1, "shake", 1.2], sfx="content/sfx/sound/be/darkness3.mp3", type="all_enemies", piercing=True,
                                       desc="Creates a hole in spaace that leads to a dark dimension.")
    SimpleMagicalAttack("Other Light", attributes=['magic', 'darkness'], effect=70, multiplier=1.8, cost=15, range=4, casting_effects=["orb", "default"], gfx='darklight', zoom=1.3, pause=2.0, target_damage_gfx=[0.2, "shake", 1.2], sfx="content/sfx/sound/be/darklight.mp3", type="all_enemies", piercing=True, true_pierce=True,
                                       aim="tc", anchor=(0.5, 0), yo=-25,
                                       desc="Brings an alternative form of light from a dark dimension.")
                                       
                                       
    # Healing:
    BasicHealingSpell(u"Light Heal", attributes=['magic', 'healing'], effect=25, cost=8, range=5, casting_effects=["runes_1", "default"], gfx='heal_1', zoom=1.4, pause=3.0, sfx="content/sfx/sound/be/heal1.mp3",
                                  yo=25,
                                       desc="Heals superficial wounds and accelerates the healing of internal ones.")
    BasicHealingSpell(u"Light Mass Heal", attributes=['magic', 'healing'], effect=10, cost=10, range=5, casting_effects=["runes_1", "default"], gfx='heal_2', zoom=1.4, pause=2.5, sfx="content/sfx/sound/be/heal2.mp3", type="all_allies", piercing=True, true_pierce=True,
                                  yo=25,
                                       desc="Heals the whole party at once.")
                                  
    # Effects:
    BasicPoisonSpell("Poison", attributes=['status', 'poison'], effect=100, multiplier=1.0, cost=30, range=4, casting_effects=["runes_1", "default"], gfx='poison_1', zoom=2.1, pause=1.0, sfx="content/sfx/sound/be/poison_01.ogg",
                                       aim="center", anchor=(0.5, 0.5))
