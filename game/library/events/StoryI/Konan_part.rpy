# after asking people at city streets MC found out about a girl who used to make and sell paper figures but disappeared some time ago.
# he also found out where she lived, and for a fee got a key from the room
init:
    image orig_1 = ProportionalScale("content/items/quest/orig_1.png", 150, 150)
    image orig_2 = ProportionalScale("content/items/quest/orig_2.png", 150, 150)
    image scroll = ProportionalScale("content/items/misc/mm.png", 150, 150)
    image ling = ProportionalScale("content/items/quest/ling.png", 150, 150)
    image protector = ProportionalScale("content/items/quest/konan_protector.png", 150, 150)
    image blossoms = SnowBlossom("content/items/quest/paper.png", count=125,  border=50, xspeed=(20, 50), yspeed=(100, 200), start=0, horizontal=True)
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
    $ e = 0
    $ f = 0
    $ konan_ling = 0
    $ konan_orig = 0
    $ body = 0
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
            if konan_orig == 0:
                show orig_2 at truecenter with dissolve
                "At the very bottom you found another paper figure. It most likely confirms that the kunoichi lived here at least for some time."
                hide orig_2 with dissolve
                $ konan_orig = 1
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
                        "Take something" if konan_ling == 0:
                            "Hmmm..."
                            show ling at truecenter with dissolve
                            "Looks good enough. Might be useful in different circumstances."
                            hide ling with dissolve
                            $ konan_ling = 1
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
                        hide scroll with dissolve
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
                        "A head protector, like the ones used by your familiar kunoichi, but with a different symbol."
                        $ a = 1
                        hide protector with dissolve
                        jump konan_closet
                    else:
                        show protector at truecenter with dissolve
                        "Nothing except the head protector."
                        hide protector with dissolve
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
            "You examine the manual."
            hide scroll with dissolve
            label konan_manual:
            menu:
                "Flip through the book":
                    "You see dozens of various methods to make stuff from paper. It could take days to read it and years to master all the tricks."
                    jump konan_manual
                "Find something about the blue figure":
                    show orig_1 at truecenter with dissolve
                    "A piece of paper given to you by Ino. Most of figures in the manual are strictly white, so you found the blue one quickly."
                    "It's a key of some sort that disables traps made from paper. That explains why nothing bad happened so far."
                    hide orig_1 with dissolve
                    jump konan_manual
                "Find something about the red figure" if konan_orig == 1:
                    show orig_2 at truecenter with dissolve
                    "A piece of paper you just found in the room. After some time you found notes about on the last page."
                    "Looks like it was green originally, but became red after something happened to the one who created it."
                    "Below are instructions how to 'open' it correctly. The manual doesn't explain what opening means in this case."
                    hide orig_2 with dissolve
                    $ e = 1
                    jump konan_manual
                "Read the instructions for red figure" if e == 1:
                    "To open it you need a piece of body of the one who created it and a body fluid mixed together. That's... a bit strange, to say at least."
                    $ f = 1
                    jump konan_manual
                "Leave the manual alone":
                    jump konan_room
        "Try to 'open the figure'" if f == 1:
            if konan_ling == 1:
                show ling at truecenter with dissolve
                "You quickly check your recent catch. Yes, looks like here is a small hair left on the reverse side."
                jump konan_ritual
            else:
                "You need to find a piece of body of the one who created all paper figures first."
                jump konan_room
    label konan_ritual:
    "Ok, now a body fluid."
    label konan_fluids:
    menu:
        "Sweat?":
            "Unfortunately, it's pretty cold in the room. That won't work."
            jump konan_fluids
        "Urine?":
            "That might work. Probably. Though you wonder if it's a good idea. Do it?"
            menu:
                "Yes":
                    $ body = 1
                "No":
                    jump konan_fluids
        "Blood?":
            "It will be painful. But it's probably the best idea. Do it?"
            menu:
                "Yes":
                    $ body = 2
                "No":
                    jump konan_fluids
        "Sperm?":
            "That will be messy for sure. Do it?"
            menu:
                "Yes":
                    $ body = 3
                "No":
                    jump konan_fluids
        "Saliva?":
            "This is probably the less risky way. Do it?"
            menu:
                "Yes":
                    $ body = 4
                "No":
                    jump konan_fluids
    if body == 1:
        "You put the figure and the lingerie on the ground and, whistling, moisturize it."
    elif body == 2:
        "You put the figure and the lingerie on the ground and make on your hand a deep cut with a knife. It hurts as hell, but the blood flows down onto the figure."
    elif body == 3:
        "Too bad you can't ask someone to help here. You recall your night with Sakura and quickly get viscous, white fluid flowing down onto the figure and the lingerie."
    else:
        "You put the figure and the lingerie on the ground, gain some saliva and copiously irrigate it."
    hide ling with dissolve
    stop world fadeout 2.0
    play world "Field2.ogg" fadein 2.0 loop
    "Something is going on."
    show blossoms with dissolve
    "Numerous sheets of paper in the room begin to move around you."
    "After some time they begin to stick together in a human figure!"
    $ k = chars["Konan"]
    $ k_spr = chars["Konan"].get_vnsprite()
    show expression k.show("nude", "no clothes", "no bg", resize=(800, 600), type="first_default") as xxx at truecenter with dissolve
    "It's a naked girl. She looks confused and embarrassed."
    $ k.override_portrait("portrait", "shy")
    k.say "Where am I? What's going on? Who are you? W-why am I naked?!"
    "Out of her mouth flows a trickle of fluid. She puts a hand to her mouth."
    if body == 1:
        "Suddenly you have a guess what it might be. Oops."
        k.say "What? W-what is that? It smells like..."
        "A whole range of emotions passes over her face as she realizes the situation looking at you and the red figure on the floor."
        k.say "You... You used THAT is a fluid? YOU JERK!"
        $ k.disposition -= 50
        $ hero.constitution += 5
        hide xxx with dissolve
        "She jumps up and runs to the bathroom. You glad that you managed to not laugh or smile before her, she would kill you on spot."
    elif body == 2:
        "It's blood. Is it yours or hers? You are not sure."
        "A whole range of emotions passes over her face as she realizes the situation looking at you and the red figure on the floor."
        "She looks at you and notices your bleeding hand and slightly turns pale."
        k.say "You shouldn't use so much blood, a couple drops would be enough!"
        $ k.disposition += 200
        $ hero.constitution -= 10
        $ hero.vitality -= 100
        "Forgetting her nakedness, she jumps up and drags you to the bathroom to treat the wound."
    elif body == 3:
        "It's a viscous, white fluid. Suddenly you have a guess what it might be."
        $ k.override_portrait("portrait", "ecstatic")
        "The girl, however, looks confused. She sniffs the liquid and licks lips, probably trying to identify it."
        "A whole range of emotions passes over her face as she realizes the situation looking at you and the red figure on the floor."
        k.say "Is it... Is it yours..."
        "She blushes even more, jumps up and quickly hides in the bathroom. That wasn't the reaction you expected..."
        $ k.disposition += 50
        $ hero.constitution -= 5
    else:
        "It's a transparent, viscous liquid. Probably saliva."
        "A whole range of emotions passes over her face as she realizes the situation looking at you and the red figure on the floor."
        $ k.override_portrait("portrait", "ecstatic")
        k.say "It tastes... strange. Um, could you turn away? I have to get dressed, it's pretty cold here."
        $ k.disposition += 50
    stop world fadeout 2.0
    hide xxx with dissolve
    hide blossoms with dissolve
    show black with dissolve 
    pause 2.0
    play world "Theme3.ogg" fadein 2.0 loop
    hide black with dissolve
    show expression k_spr at center with dissolve
    "When the girl came to her senses and dressed, you introduced yourself and briefly told her why are you here."
    $ k.override_portrait("portrait", "indifferent")
    k.say "I see. You have my gratitude, [hero.name]. I would be in trouble if someone would not opened the bound origami soon."
    k.say "My name is Konan."
    if body == 1:
        "You can see that she's still displeased, but keeps her feeling under control."
    elif body == 2:
        $ k.override_portrait("portrait", "shy")
        k.say "Please be careful in the future. It's dangerous to give so much blood to any technique."
    elif body == 3:
        "You can see that she's still embarrassed, but keeps her feeling under control."
    k.say "If there is something I could do in return..."
    $ a = 0
    $ b = 0
    
    label konan_saved:
    menu:
        "What just happened?" if a == 0:
            $ k.override_portrait("portrait", "indifferent")
            $ a = 1
            k.say "I cannot say for sure. This technique is supposed to hide me when I'm in grave danger. But it damages memory, so I have no idea what happened to me either."
            jump konan_saved
        "Praise her lingerie" if b == 0:
            $ k.override_portrait("portrait", "shy")
            k.say "I'm sorry? Ah, you had to take my underwear to open my origami. T-thanks, I guess. Let's not talk about it any more."
            $ k.disposition += 5
            $ b = 1
            jump konan_saved
        "Ask her to help you":
            $ k.override_portrait("portrait", "happy")
            k.say "You want to get to our village? I understand. You will have my approval, it is the least I can do."
            k.say "I will contact others and send you my paper plane when we'll be ready to take you there."
            "A paper plane? Really?.."
            $ k.override_portrait("portrait", "indifferent")
            k.say "Now, if you excuse me, I have many things to do. My house is not safe anymore, we shouldn't stay here any longer."
    hide expression k_spr with dissolve
    play sound "content/sfx/sound/events/door_open.mp3"
    show bg story street with dissolve
    "Saying goodbye to her, you going home. With the third kunoichi you will be able to get to their village very soon."
    $ k.restore_portrait()
    scene black with dissolve
    stop world