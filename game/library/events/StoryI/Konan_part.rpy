# after asking people at city streets MC found out about a girl who used to make and sell paper figures but disappeared some time ago.
# he also found out where she lived, and for a fee got a key from the room
init:
    image orig_1 = ProportionalScale("content/items/quest/orig_1.png", 150, 150)
    image orig_2 = ProportionalScale("content/items/quest/orig_2.png", 150, 150)
    image scroll = ProportionalScale("content/items/cons/scr_ice.png", 150, 150)
    image ling = ProportionalScale("content/items/quest/ling.png", 150, 150)
    image protector = ProportionalScale("content/items/quest/konan_protector.png", 150, 150)
    image blossoms = SnowBlossom("content/items/quest/paper.png", count=125,  border=50, xspeed=(20, 50), yspeed=(100, 200), start=0, horizontal=True)
label intro_story_konan:
    stop music
    stop world
    $ k = chars["Konan"]
    $ k_spr = chars["Konan"].get_vnsprite()
    $ konan_orig = 0
    $ konan_ling = 0
    $ konan_protector = 0
    $ a = 0
    $ b = 0
    $ c = 0
    $ d = 0
    $ e = 0
    $ f = 0
    $ sc = 0
    hide screen pyt_city_screen
    play world "Dungeon2.ogg" fadein 2.0 loop
    scene bg story dark_room with dissolve
    "This is the place where lived the kunoichi, a small room in a dirty, old hotel. You should examine it, maybe there are some clues left."
    label konan_room_search:
    call screen poly_matrix("library/events/StoryI/coordinates.json", show_exit_button=(1.0, 1.0))
    if not _return:
        jump konan_go_on
    if _return == "Curtains":
        "You look at the gap between the curtains."
        show bg story street with dissolve
        "An ordinary street. She used to sell her paper handicrafts across the street."
        "You wonder if it was just a cover for some mission or something."
        scene bg story dark_room with dissolve
        jump konan_room_search
    elif _return == "Basket":
        "There is a small trash can in the corner. You look inside."
        "It's filled with paper."
        menu:
            "Rummaging in the garbage":
                if konan_orig == 0:
                    show orig_2 at truecenter with dissolve
                    "At the very bottom you found another paper figure. It most likely confirms that the kunoichi lived here at least for some time."
                    hide orig_2 with dissolve
                    $ konan_orig = 1
                    jump konan_room_search
                else:
                    "Nothing but crumpled paper."
                    jump konan_room_search
            "Leave it alone":
                jump konan_room_search
    elif _return == "Table":
        "An old, tacky empty coffee table."
        jump konan_room_search
    elif _return == "Pillow":
        "Unlike other furniture, it doesn't look like hotel property. Ino and Sakura use such pillows to sit at home too. Why kunoichi dislike chairs?"
        jump konan_room_search
    elif _return == "Box_1":
        "An empty box."
        jump konan_room_search
    elif _return == "Box_2":
        "A box with basic cosmetics. Smell of perfume."
        jump konan_room_search
    elif _return == "Calendar":
        "You take a closer look at the calendar. It's for the current year, and there are many strange, small marks next to the days."
        "The last mark was made about three weeks ago."
        jump konan_room_search
    elif _return == "Bookshelf":
        "The bookshelf is filled with old fiction books. You have no idea if they belong to the hotel or not."
        if b == 1:
            "In the note there was something about books. You very carefully check the bookshelf."
            "One book stands out. It looks newer, and it's not an ordinary fiction book. It's a short treatise about the art of summoning practiced by the ancient tribes in the area even before the construction of the city."
            "One paragraph draws your attention. It says that the summoner should use a part of his body, usually blood, to make the ritual work."
            $ c = 1
        jump konan_room_search
    elif _return == "Drawer_1":
        play events2 "events/drawer.mp3"
        "Writing utensils, a few dishes. Nothing interesting."
        jump konan_room_search
    elif _return == "Drawer_2":
        play events2 "events/drawer.mp3"
        "Sheets of paper, dozens of them. Why there is so much paper here anyway?"
        jump konan_room_search
    elif _return == "Drawer_3":
        play events2 "events/drawer.mp3"
        "Bingo. The drawer is full of lingerie."
        label konan_lingerie:
        menu:
            "Examine it":
                "You rummaging through lingerie. It's all black, and most of it is lacy. Probably belongs to a mature woman."
                jump konan_lingerie
            "Take something" if konan_ling == 0:
                "Hmmm..."
                show ling at truecenter with dissolve
                "Looks good enough. Might be useful in different circumstances."
                hide ling with dissolve
                $ konan_ling = 1
                jump konan_lingerie
            "Close the drawer":
                jump konan_room_search
        jump konan_room_search
    elif _return == "Drawer_4":
        play events2 "events/drawer.mp3"
        "Empty."
        jump konan_room_search
    elif _return == "Drawer_5":
        play events2 "events/drawer.mp3"
        "A straw mattress. There is no bed in the room, so she probably slept on the floor."
        if a == 1 and sc == 0:
            "The straw in the bottom drawer probably belongs to it. Maybe there is something inside of it instead of that straw? You need something sharp."
        elif a == 1 and sc == 1:
            "Using the scissors, you carefully cut the mattress."
            play events2 "events/scissors.mp3"
            "There is straw, lots of it... "
            play events2 "events/scissors.mp3"
            "Hm? A note?"
            show scroll at truecenter with dissolve
            "'a private thing, a drop of blood, books'"
            "What is that supposed to mean?"
            hide scroll with dissolve
            $ b = 1
            jump konan_room_search
        jump konan_room_search
    elif _return == "Drawer_6":
        play events2 "events/drawer.mp3"
        "A lot of paper and a pair of metal scissors."
        if a == 1 and b == 0:
            $ sc = 1
            "The scissors might be useful."
        elif b == 1:
            "A ripped mattress. Nothing else."
        jump konan_room_search
    elif _return == "Drawer_7":
        play events2 "events/drawer.mp3"
        if konan_protector == 0:
            show protector at truecenter with dissolve
            "A head protector, like the ones used by your familiar kunoichi, but with a different symbol."
            menu:
                "Take it":
                    "Might be useful."
                    $ konan_protector = 1
                    hide protector with dissolve
                    jump konan_room_search
                "Leave it alone":
                    hide protector with dissolve
                    jump konan_room_search
        else:
            "Empty."
            jump konan_room_search
    elif _return == "Drawer_8":
        play events2 "events/drawer.mp3"
        "Is it... straw? The drawer is full of straw. How strange."
        $ a = 1
        jump konan_room_search
    label konan_go_on:
    menu:
        "Continue to examine the room":
            jump konan_room_search
        "Leave the room":
            "There is no point to leave until you find something useful. You have to find that kunoichi."
            jump konan_go_on
        "Examine the figure" if konan_orig == 1:
            show orig_2 at truecenter with dissolve
            "You take the paper figure you found in the room. For some reason it feels a little warm."
            label konan_paper_figure:
            menu:
                "Take a closer look":
                    "It looks similar to the figure you got from Ino, but made a bit differently."
                "Smell it":
                    "It smells like... blood. That explains the color."
                "Leave it alone":
                    hide orig_2 with dissolve
                    jump konan_go_on
        "Examine the lingerie" if konan_ling == 1:
            show ling at truecenter with dissolve
            "It's a black lace lingerie."
            hide ling with dissolve
            jump konan_go_on
        "Read the note again" if b == 1:
            show scroll at truecenter with dissolve
            "'a private thing, a drop of blood, books'"
            "What is that supposed to mean?"
            hide scroll with dissolve
            jump konan_go_on
        "Try the summon ritual" if c == 1:
            if konan_orig == 0:
                "You need to find some blood."
                jump konan_go_on
            if konan_ling == 0 and konan_protector == 0:
                "You need to find a personal thing."
                jump konan_go_on
            "You have the components. You begin to arrange them in accordance with the book."
            menu:
                "A personal thing is..."
                
                "Lingerie" if konan_ling == 1:
                    $ d = 1
                    $ k.disposition -= 50
                "Head protector" if konan_protector == 1:
                    $ d = 2
                "Stop the ritual":
                    jump konan_go_on
            label konan_fluids:
            menu:
                "Now a part of your body"
                
                "Sweat?":
                    "Unfortunately, it's pretty cold in the room. That won't work."
                    jump konan_fluids
                "Blood?":
                    "It will be painful. But it's probably the best idea. Do it?"
                    menu:
                        "Yes":
                            $ e = 1
                        "No":
                            jump konan_fluids
                "Sperm?":
                    "You wonder if it's a good idea. That will be messy for sure. Do it?"
                    menu:
                        "Yes":
                            $ e = 2
                        "No":
                            jump konan_fluids
                "Saliva?":
                    "This is probably the less risky way. Do it?"
                    menu:
                        "Yes":
                            $ e = 3
                        "No":
                            jump konan_fluids
                "Stop the ritual":
                    jump konan_go_on
            if e == 1:
                "You make a deep cut on the hand with the scissors. It hurts as hell, but the blood flows down onto the figure."
            elif e == 2:
                "Too bad you can't ask someone to help here. You recall your night with Sakura and quickly get viscous, white fluid flowing down onto the figure."
            else:
                "You gain some saliva and copiously irrigate the figure."
    stop world fadeout 2.0
    "Something is going on."
    play world "Field2.ogg" fadein 2.0 loop
    "Numerous sheets of paper in the room begin to move around you."
    $ temp = Transform("content/items/quest/paper.png", zoom=0.3)
    show expression Vortex(temp, amount=150, radius=400, adjust_radius=(-20, 20), time=(0.5, 2.5), circles=(0.5, 5)) as vortex
    show expression k.show("nude", "no clothes", "no bg", resize=(800, 600), type="first_default") as xxx at truecenter with dissolve
    pause
    hide vortex
    "After some time they stick together in a human figure. It's a naked girl. She looks confused and embarrassed."
    $ k.override_portrait("portrait", "shy")
    k.say "Where am I? What's going on? Who are you? W-why am I naked?!"
    "Out of her mouth flows a trickle of fluid. She puts a hand to her mouth."
    if e == 1:
        "It's blood. Is it yours or hers? You are not sure."
        "A whole range of emotions passes over her face as she realizes the situation looking at you and the red figure on the floor."
        "She looks at you and notices your bleeding hand and slightly turns pale."
        k.say "You shouldn't use so much blood, a couple drops would be enough!"
        $ k.disposition += 200
        $ hero.constitution -= 10
        $ hero.vitality -= 100
    elif e == 2:
        "It's a viscous, white fluid. Suddenly you have a guess what it might be."
        $ k.override_portrait("portrait", "ecstatic")
        "The girl, however, looks confused. She sniffs the liquid and licks lips, probably trying to identify it."
        "A whole range of emotions passes over her face as she realizes the situation looking at you and the red figure on the floor."
        "She blushes even more, jumps up and quickly hides in the bathroom. That wasn't the reaction you expected..."
        $ k.disposition += 50
        $ hero.constitution -= 5
    else:
        "It's a transparent, viscous liquid. Probably saliva."
        "A whole range of emotions passes over her face as she realizes the situation looking at you and the red figure on the floor."
        $ k.override_portrait("portrait", "ecstatic")
        k.say "It tastes... strange. Um, could you turn away? I have to get dressed."
        $ k.disposition += 50
    stop world fadeout 2.0
    hide xxx with dissolve
    show black with dissolve 
    pause 1.0
    play world "Theme3.ogg" fadein 2.0 loop
    hide black with dissolve
    show expression k_spr at center with dissolve
    "When the girl came to her senses and dressed, you introduced yourself and briefly told her why are you here."
    $ k.override_portrait("portrait", "indifferent")
    k.say "I see. You have my gratitude, [hero.name]."
    k.say "My name is Konan."
    "She's still embarrassed, but keeps her feeling under control."
    label konan_saved:
    menu:
        "What just happened?":
            $ k.override_portrait("portrait", "indifferent")
            $ a = 1
            k.say "I cannot say. I prepared this technique in case if something will happen to me. I don't remember what happened though."
            jump konan_saved
        "Praise her lingerie" if konan_ling == 1:
            $ k.override_portrait("portrait", "shy")
            k.say "I'm sorry? Ah, you had to take my underwear summon me. L-let's not talk about it any more."
            $ k.disposition += 20
            $ konan_ling = 0
            jump konan_saved
        "Ask her to help you":
            $ k.override_portrait("portrait", "happy")
            k.say "You want to get to our village? I understand. You will have my approval, it is the least I can do."
            k.say "I will contact others and send you my paper plane when we'll be ready to take you there."
            "A paper plane? Really?.."
    hide expression k_spr with dissolve
    play sound "content/sfx/sound/events/door_open.mp3"
    show bg story street with dissolve
    "Saying goodbye to her, you going home. With the third kunoichi you will be able to get to their village very soon."
    $ k.restore_portrait()
    $ del a
    $ del b
    $ del c
    $ del d
    $ del e
    $ del f
    $ del sc
    $ del konan_orig
    $ del konan_ling
    $ del konan_protector
    scene black with dissolve
    stop world