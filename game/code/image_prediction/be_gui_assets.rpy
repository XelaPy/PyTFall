init python hide:
    be_predict = []

    be_predict.append("content/gfx/interface/bars/empty_bar1.png")
    be_predict.append("content/gfx/interface/bars/hp1.png")
    be_predict.append("content/gfx/interface/bars/mp1.png")
    be_predict.append("content/gfx/interface/bars/vitality1.png")
    be_predict.append("content/gfx/interface/images/crosshair_red.webp")
    # be_predict.append()
    # be_predict.append()
    # be_predict.append()
    # be_predict.append()
    # be_predict.append()
    # be_predict.append()
    # be_predict.append()

    be_predict.extend((
        "fire_element_be_viewport",
        "water_element_be_viewport",
        "earth_element_be_viewport",
        "darkness_element_be_viewport",
        "ice_element_be_viewport",
        "air_element_be_viewport",
        "ele_element_be_viewport",
        "light_element_be_viewport",
        "healing_be_viewport",
        "poison_be_viewport",
        "physical_be_viewport",

        "fire_element_be_size20",
        "water_element_be_size20",
        "earth_element_be_size20",
        "darkness_element_be_size20",
        "ice_element_be_size20",
        "air_element_be_size20",
        "ele_element_be_size20",
        "light_element_be_size20",
        "healing_be_size20",
        "poison_be_size20",
        "physical_be_size20",
    ))

    renpy.start_predict(*be_predict)
