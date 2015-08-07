init:

    image bg bloodscene = im.MatrixColor("content/events/Intro/sky1.jpg", im.matrix.colorize(red, black))
label intro_storyt:
    stop world
    stop music
    scene black
    "After a few days you received a message from kunoichi leaders. They will meet you after midnight in an old building outside the city. You have to come alone."
    play music "content/sfx/music/events/Theme2.ogg" fadein 2.0 loop
    show event oldhouse with dissolve
    "Afraid of being late, you arrived a few hours earlier. Nevertheless, you barely found the road in the dark."
    label menuone:
    menu:
        "Inspect the building":
            "It looks like an old tavern. The building seems to have been abandoned for some time."
            jump menuone
        "Look around":
            "The building is situated at the crossroads, an hour's walk from the city walls."
            jump menuone
        "Enter":
            "You o"
    
    return
