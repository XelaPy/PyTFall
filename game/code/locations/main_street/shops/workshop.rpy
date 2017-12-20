label workshop:

    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5

    hide screen main_street

    scene bg workshop
    with dissolve

    show expression npcs["Katia_workshop"].get_vnsprite() as katia
    $ k = npcs["Katia_workshop"].say
    with dissolve

    if global_flags.flag('visited_workshop'):
        "Welcome back!"
    else:
        $ global_flags.set_flag('visited_workshop')
        k "Welcome to PyTFall's Workshop!"
        k "The best place to go for Weapons and Armor!"
        k "Please take a look at our selection: "

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    $ jump('workshop_shopping')

label workshop_shopping:

    python:
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.workshop
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)

    show screen shopping(left_ref=hero, right_ref=shop)
    with dissolve

    call shop_control from _call_shop_control

    $ global_flags.del_flag("keep_playing_music")
    hide screen shopping
    with dissolve
    jump main_street
