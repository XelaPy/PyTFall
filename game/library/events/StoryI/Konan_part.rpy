# after asking people at city streets MC found out about a girl who used to make and sell paper figures but disappeared some time ago.
# he also found out where she lived, and for a fee got a key from the room
init:
    image orig_1 = ProportionalScale("content/items/quest/orig_1.png", 150, 150)
    image orig_2 = ProportionalScale("content/items/quest/orig_2.png", 150, 150)
    image scroll = ProportionalScale("content/items/misc/mm.png", 150, 150)
    image ling = ProportionalScale("content/items/quest/ling.png", 150, 150)
    image protector = ProportionalScale("content/items/quest/konan_protector.png", 150, 150)
label intro_story:
    stop music
    stop world
    play world "Dungeon2.ogg" fadein 2.0 loop
    show bg story dark_room with dissolve
    "This is the place where lived the kunoichi, a small room in a dirty, old hotel. You should examine it, maybe there are some clues left."
    $ a = 0
    $ b = 0
    $ c = 0
    $ d = 0
    $ chars["Konan"].set_flag("lingerie", value="False")
    $ chars["Konan"].set_flag("orig", value="False")
    label konan_room:
    menu:
        "Look out the window":
            "You look at the gap between the curtains."
            show bg story street with dissolve
            "An ordinary street. She used to sell her paper handicrafts across the street."
            "You wonder if it was just a cover for some mission or something."
            show bg story dark_room with dissolve
            jump konan_room
        "Explore the trash can":
            "There is a small trash can in the corner. You look inside."
            "It's filled with paper."
            if chars["Konan"].flag("orig") == "False":
                show orig_2 at truecenter with dissolve
                "At the very bottom you found another paper figure. It most likely confirms that the kunoichi lived here at least for some time."
                hide orig_2 with dissolve
                $ chars["Konan"].set_flag("orig", value="True")
                jump konan_room
            else:
                "Nothing more here."
                jump konan_room
                
        "Explore table":
            "It's an old, tacky empty coffee table."
            label konan_table:
            menu:
                "Look under the table":
                    "Nothing, except a huge layer of dust."
                    jump konan_table
                "Look at the pillow nearby":
                    "Unlike the table, it doesn't look like hotel property. Ino and Sakura use such pillows to sit at home too. Maybe kunoichi dislike chairs?"
                    jump konan_table
                "Leave the table alone":
                    "Let's see what else you can find."
                    jump konan_room
        "Examine calendar on the wall":
            "You take a closer look at the calendar. It's for the current year, and there are many strange, small marks next to the days."
            "The last mark was made about three weeks ago. A few days before the kunoichi disappeared."
            jump konan_room
        "Examine the bookshelf":
            "The bookshelf is filled with books."
            label konan_books:
            menu:
                "Examine books":
                    "You see various old fiction books. They belong to the hotel."
                    jump konan_books
                "Check behind books":
                    "You remove the books one by one. Nothing."
                    jump konan_books
                "Enough with the bookshelf":
                    jump konan_room
        "Examine closet":
            "Another old piece of furniture. It has eight drawers."
            label konan_closet:
            menu:
                "First drawer":
                    play events2 "events/drawer.mp3"
                    "Writing utensils, a few dishes. Nothing interesting."
                    jump konan_closet
                "Second drawer":
                    play events2 "events/drawer.mp3"
                    "Sheets of paper, dozens of them. Why there is so much paper here anyway?"
                    jump konan_closet
                "Third drawer":
                    play events2 "events/drawer.mp3"
                    "Bingo. The drawer is full of lingerie."
                    label konan_lingerie:
                    menu:
                        "Examine it":
                            "You rummaging through lingerie. It's all black, and most of it is lacy. Probably belongs to a mature woman."
                            jump konan_lingerie
                        "Take something" if chars["Konan"].flag("lingerie") == "False":
                            "Hmmm..."
                            show ling at truecenter with dissolve
                            "Looks good enough. Might be useful in different circumstances."
                            hide ling with dissolve
                            $ chars["Konan"].set_flag("lingerie", value="True")
                            jump konan_lingerie
                        "Close the drawer":
                            jump konan_closet
                "Fourth drawer":
                    play events2 "events/drawer.mp3"
                    "Empty."
                    jump konan_closet
                "Fifth drawer":
                    play events2 "events/drawer.mp3"
                    if b == 0:
                        "A mattress. There is no bed in the room, so she probably slept on the floor."
                        jump konan_closet
                    elif b == 1 and c == 0:
                        "You check the mattress. It stuffed with straw. Maybe there is something inside of it instead of that straw in the last drawer?"
                        jump konan_closet
                    elif d == 0:
                        "Ok, hopefully she won't be angry. You carefully cut the mattress."
                        play events2 "events/scissors.mp3"
                        "There is straw, lots of it... "
                        play events2 "events/scissors.mp3"
                        "Hm? A book or something?"
                        show scroll at truecenter with dissolve
                        "You examine it. It looks like a complex handwritten manual for making paper figures, with many pictures but little text."
                        $ d = 1
                        show scroll with dissolve
                        jump konan_closet
                    else:
                        "A ripped mattress. Nothing else."
                        jump konan_closet
                "Sixth drawer":
                    play events2 "events/drawer.mp3"
                    if b == 0:
                        "More paper and a pair of metal scissors."
                    elif c == 0:
                        "More paper and a pair of metal scissors."
                        "Looks like scissors will be useful. You take them."
                        $ c = 1
                    else:
                        "More paper."
                    jump konan_closet
                "Seventh drawer":
                    play events2 "events/drawer.mp3"
                    if a == 0:
                        show protector at truecenter with dissolve
                        "A head protector, like the ones used by your familiar kunoichi, but with a different symbol. This will be useful, you take it."
                        $ a = 1
                        hide protector with dissolve
                        jump konan_closet
                    else:
                        "Empty."
                        jump konan_closet
                "Eighth drawer":
                    play events2 "events/drawer.mp3"
                    "Is it... straw? The drawer is full of straw. How strange."
                    $ b = 1
                    jump konan_closet
                "Enough with closet":
                    jump konan_room
        "Examine the manual" if d == 1:
            show scroll with dissolve
            "You examine the manual"