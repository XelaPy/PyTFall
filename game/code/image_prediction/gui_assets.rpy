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
                         "content/gfx/frame/rank_frame.png",
                         "content/gfx/images/m_1.webp",
                         "content/gfx/images/m_2.webp",
                         "content/gfx/images/fishy.png",
                         "content/gfx/interface/buttons/IT2.png",
                         "content/gfx/interface/buttons/sl_idle.png",
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
                         ))
    renpy.start_predict(*gui_predict)

init python hide:
    bg_predict = []
    bg_predict.append('content/gfx/bg/main_brothel.webp')
    bg_predict.append("bg gallery")


    renpy.start_predict(*bg_predict)

init python hide:
    main_scr_predict = ["city_screen", "chars_list", "top_stripe"]
    for scr in main_scr_predict:
        renpy.start_predict_screen(scr)
