label city_map_predict:
    python hide:
        city_map_predict = [item for sl in (("".join([pytfall.map_pattern, key, ".webp"]),
                                        "".join([pytfall.map_pattern, key, "_hover.webp"]),
                                        "".join(["content/gfx/interface/buttons/locations/", key, ".png"]))
                                        for key in (i["id"] for i in pytfall.maps("pytfall")))
                                        for item in sl]
        city_map_predict.append("content/gfx/interface/buttons/compass.png")

        renpy.start_predict(*city_map_predict)
    return

label items_ptedict:
    python hide:
        items_predict = []
        for item in items.values():
            items_predict.append(item.icon)
        renpy.start_predict(*items_predict)
    return


init python hide:
    gui_predict = []
    # gui_predict.append()
    # gui_predict.append()
    # gui_predict.append()
    # gui_predict.append()
    # gui_predict.append()
    # gui_predict.append()
    # gui_predict.append()

    gui_predict.extend(("content/gfx/frame/h2.webp",
                         "content/gfx/frame/p_frame.png",
                         "content/gfx/interface/buttons/sl_idle.png",
                         "content/gfx/frame/rank_frame.png",
                         "content/gfx/images/m_1.webp",
                         "content/gfx/images/m_2.webp",
                         "content/gfx/images/fishy.png",
                         "content/gfx/interface/buttons/IT2.png",
                         "content/gfx/interface/icons/exp.webp",
                         "content/gfx/interface/icons/gold.png",
                         "content/gfx/interface/images/work.webp",
                         "content/gfx/interface/buttons/journal1.png",
                         "content/gfx/frame/frame_ap.webp",
                         "content/gfx/interface/buttons/blue3.png",
                         'content/gfx/interface/buttons/f1.png',
                         'content/gfx/interface/buttons/op3.png',
                         'content/gfx/frame/window_frame2.webp',
                         'content/gfx/interface/buttons/choice_buttons1.png',
                         'content/gfx/interface/buttons/close.png',
                         'content/gfx/interface/icons/checkbox_checked.png',
                         'content/gfx/interface/icons/checkbox_unchecked.png',
                         "content/gfx/interface/buttons/close2.png",
                         "content/gfx/interface/buttons/close2_h.png",
                         "content/gfx/interface/buttons/blue_arrow.png",
                         "content/gfx/interface/buttons/close4.png",
                         "content/gfx/interface/buttons/close4_h.png"
                         ))

    gui_predict.extend(("content/gfx/interface/images/elements/ice.png",
                        "content/gfx/interface/images/elements/fire.png",
                        "content/gfx/interface/images/elements/air.png",
                        "content/gfx/interface/images/elements/darkness.png",
                        "content/gfx/interface/images/elements/earth.png",
                        "content/gfx/interface/images/elements/electricity.png",
                        "content/gfx/interface/images/elements/healing.png",
                        "content/gfx/interface/images/elements/hover.png",
                        "content/gfx/interface/images/elements/light.png",
                        "content/gfx/interface/images/elements/multi.png",
                        "content/gfx/interface/images/elements/neutral.png",
                        "content/gfx/interface/images/elements/physical.png",
                        "content/gfx/interface/images/elements/poison.png",
                        "content/gfx/interface/images/elements/small_air.png",
                        "content/gfx/interface/images/elements/small_darkness.png",
                        "content/gfx/interface/images/elements/small_earth.png",
                        "content/gfx/interface/images/elements/small_electricity.png",
                        "content/gfx/interface/images/elements/small_fire.png",
                        "content/gfx/interface/images/elements/small_ice.png",
                        "content/gfx/interface/images/elements/small_light.png",
                        "content/gfx/interface/images/elements/small_water.png",
                        "content/gfx/interface/images/elements/water.png",
                        ))

    renpy.start_predict(*gui_predict)

init python hide:
    bg_predict = []
    bg_predict.append('content/gfx/bg/main_brothel.webp')
    bg_predict.append("bg gallery")
    bg_predict.append("bg pytfall")


    renpy.start_predict(*bg_predict)

init python hide:
    gfx_overlay_predict = []
    gfx_overlay_predict.extend(["fight_0", "fight_1", "fight_2"])
    gfx_overlay_predict.append("hearts_flow")
    gfx_overlay_predict.append("shy_blush")
    gfx_overlay_predict.append("content/gfx/interface/images/money_bag3.png")
    gfx_overlay_predict.append("content/gfx/interface/icons/gold.png")
    gfx_overlay_predict.append("content/gfx/interface/images/work.webp")

    renpy.start_predict(*gfx_overlay_predict)

init python hide:
    main_scr_predict = ["city_screen", "chars_list", "top_stripe"]
    for scr in main_scr_predict:
        renpy.start_predict_screen(scr)
