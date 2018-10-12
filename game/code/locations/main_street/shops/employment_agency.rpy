label employment_agency:
    jump main_street

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

    # $ g = npcs["Rose_estate"].say

    if not global_flags.has_flag("visited_employment_agency") and not config.developer:
        $ global_flags.set_flag("visited_employment_agency")
        # $ ea = Character(None, kind=nvl)

        # show expression npcs["Rose_estate"].get_vnsprite() at center as rose with dissolve:
        #     yoffset 100
        #
        # g "Welcome to Rose Real Estates."
        # extend " My name is Rose. I'm the owner and the realtor."
        # g "Please have a seat and take a look at some of our offers."
    else:
        show expression npcs["Rose_estate"].get_vnsprite() at right as rose with dissolve
            # yoffset -100

    # Added the next three lines to disable this feature without crashing the game   --fenec250

    $ market_buildings = sorted(set(chain(businesses.values(), buildings.values())) - set(hero.buildings), key = lambda x: x.id)
    $ focus = None

    # if not market_buildings:
    #     npcs["Rose_estate"].say "I'm sorry, we don't have anything for sale at the moment."
    # show screen realtor_agency

    while 1:

        $ result = ui.interact()

        # if result[0] == 'buy':
        #     if hero.AP > 0 and hero.take_money(result[1].price, reason="Property"):
        #         $ hero.AP -= 1
        #         $ renpy.play("content/sfx/sound/world/purchase_1.ogg")
        #         $ hero.add_building(result[1])
        #         $ market_buildings.remove(result[1])
        #         $ focus = None
        #
        #         if hero.AP <= 0:
        #             $ Return(["control", "return"])()
        #     else:
        #         if hero.AP <= 0:
        #             $ renpy.call_screen('message_screen', "You don't have enough Action Points!")
        #         else:
                    # $ renpy.call_screen('message_screen', "You don't have enough Gold!")

        if result[0] == 'control':
            if result[1] == 'return':
                jump employment_agency_exit

label employment_agency_exit:
    $ renpy.music.stop(channel="world")
    hide screen employment_agency
    jump main_street


screen employment_agency():
    modal True
    zorder 1
