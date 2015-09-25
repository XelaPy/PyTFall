# after asking people at city streets MC found out about a girl who used to make and sell paper figures but disappeared some time ago.
# he also found out where she lived, and for a fee got a key from the room
init:
    image orig_1 = ProportionalScale("content/items/quest/orig_1.png", 150, 150)
    image orig_2 = ProportionalScale("content/items/quest/orig_2.png", 150, 150)
    image scroll = ProportionalScale("content/items/cons/scr_ice.png", 150, 150)
    image ling = ProportionalScale("content/items/quest/ling.png", 150, 150)
    image protector = ProportionalScale("content/items/quest/konan_protector.png", 150, 150)
label intro_story_konan_room:
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
    
label konan_first_meeting:
    stop music
    stop world
    $ k = chars["Konan"]
    $ k_spr = chars["Konan"].get_vnsprite()
    play world "Theme2.ogg" fadein 2.0 loop
    show bg hiddenvillage_entrance with dissolve
    show expression k_spr at center with dissolve
    "Strolling through the village, you noticed a familiar figure."
    $ k.override_portrait("portrait", "indifferent")
    k.say "Hm? Ah, it's you. As I promised, I helped you to get to the village. I suppose it means we're even now."
    menu:
        "Try to start a neutral conversation":
            $ k.disposition -= 25
            k.say "I'm sorry to say it, but for me your intentions are clear as the sky today."
        "Propose to have sex here and now":
            $ k.override_portrait("portrait", "happy")
            "It's the first time you see her smile."
            $ k.disposition += 15
            k.say "How amusing. Normally men try to pretend they want something else."
        "Tell her about your mission in the village":
            "She nods."
            $ k.disposition += 20
            k.say "I appreciate your honesty. It's a rare gift, especially among kunoichi."
    $ k.override_portrait("portrait", "indifferent")
    k.say "However, I'm not a young, inexperienced girl like others. I'm fulfilling missions of the highest rank for years."
    k.say "The chances of me being captured and raped are nonexistent. One could argue I'm the strongest and the most experienced among remaining kunoichi."
    k.say "Thus your services are not needed."
    $ a = 0
    $ b = 0
    $ c = 0
    label konan_seduce:
    menu:
        "What about love?" if a == 0:
            $ k.override_portrait("portrait", "sad")
            $ a = 1
            k.say "I... loved once. But he's gone long time ago."
            $ k.override_portrait("portrait", "indifferent")
            k.say "This part of my life is behind."
            jump konan_seduce
        "What about sexual pleasure?" if b == 0:
            $ k.override_portrait("portrait", "suggestive")
            $ b = 1
            k.say "Oh? You've never heard of self pleasure, young man? I don't think so."
            $ k.override_portrait("portrait", "indifferent")
            k.say "There is no need for you, or anyone else, to help me with that."
            jump konan_seduce
        "Remind her about events in her room" if c == 0 and (a == 1 or b == 1):
            $ k.override_portrait("portrait", "shy")
            $ c = 1
            k.say "Not so loud! I... I would appreciate if you'll never talk about it with anyone."
            $ k.override_portrait("portrait", "indifferent")
            k.say "I don't want others to know about it. Not before I'll find out that's happened."
            $ k.override_portrait("portrait", "shy")
            "She sighs."
            k.say "You may be right. I might be not as all-powerful as I always thought."
            $ k.override_portrait("portrait", "indifferent")
            k.say "Very well. Let's make a deal. You will never talk about events in my room with anyone, not before I'll let you."
            $ k.override_portrait("portrait", "shy")
            k.say "And in return I'll give you a chance. I can deflower myself without your help if I must. Prove me that it should be you."
            jump konan_seduce
        "Promise to get her fall in love again" if a == 1 and c == 1:
            $ k.override_portrait("portrait", "sad")
            k.say "I don't believe it is possible. But you can try, I'll give you a chance as I promised."
            "We give quest to get her disposition to 600."
        "Promise to make her first time unforgettable and painless" if b == 1 and c == 1:
            $ k.override_portrait("portrait", "shy")
            k.say "W-well, I suppose it's better to avoid pain when possible. I'll give you a chance as I promised."
            "We give quest to rise MC's vaginal and oral sex skills to 300."
    hide expression k_spr with dissolve
    $ k.restore_portrait()
    $ del a
    $ del b
    $ del c
    scene black with dissolve
    stop world
    
label konan_second_meeting_love: # depending on selected quest, there could be two scenes
    stop music
    stop world
    $ k = chars["Konan"]
    $ k_spr = chars["Konan"].get_vnsprite()
    show bg hiddenvillage_entrance with dissolve
    play world "Field1.ogg" fadein 2.0 loop
    show expression k_spr at center with dissolve
    "Once again you met Konan in the village. She wasn't that surly and cold woman that you used to know."
    $ k.override_portrait("portrait", "happy")
    k.say "..."
    "You had a lively discussion about her recent adventures. Her top rank missions are always interesting and complex, making her stories exciting."
    "Even though they are supposed to be classified, she seems to enjoy sharing them with you."
    "Finally, when you was about to say goodbye..."
    $ k.override_portrait("portrait", "shy")
    $ k.disposition += 100
    k.say "Wait, [hero.name]. Do you... Do you remember about your promise?"
    menu:
        "Yes":
            k.say "Well, I just wanted to say that you can stop making so many efforts."
        "What promise?":
            $ k.override_portrait("portrait", "happy")
            k.say "I'm not sure if you're joking or not, but it does not matter."
    $ k.override_portrait("portrait", "shy")
    k.say "Because you won. You... you have proved me that it should be you."
    $ set_lovers(hero, k)
    $ k.override_portrait("portrait", "happy")
    k.say "What is past is past. If you don't mind, I'd like to be with you from now on."
    $ k.override_portrait("portrait", "suggestive")
    "She suddenly leans forward and soundly kisses you."
    k.say "Oh, and we can do whatever you want anytime you want. Just saying." # unlocking sex actions
    $ k.restore_portrait()
    scene black with dissolve
    stop world
    
#label intro_story:
label konan_second_meeting_sex:
    stop music
    stop world
    $ k = chars["Konan"]
    $ k_spr = chars["Konan"].get_vnsprite()
    if k.disposition < 500:
        $ k.disposition = 500
    show bg hiddenvillage_entrance with dissolve
    play world "Field1.ogg" fadein 2.0 loop
    show expression k_spr at center with dissolve
    "Once again you met Konan in the village. But this time you was prepared."
    $ k.override_portrait("portrait", "indifferent")
    k.say "Good day, [hero.name]. Want something?"
    "You explain that you are ready to prove your skill."
    k.say "Your skill..? Ah, you mean 'that' skill. Let's see..."
    "She thinks for a few seconds."
    $ k.override_portrait("portrait", "happy")
    k.say "If you are as skilled as you claim, it shouldn't be a problem for you to make me feel good without irreversible consequences. Follow me."
    show bg girl_room with fade
    "She quickly led into a room in a local small hotel. Despite her cold attitude, she really has no complexes..."
    hide expression k_spr with dissolve
    show expression k.show("sex", "masturbation", "confident", "indoors", "no clothes", resize=(800, 600), type="first_default") as xxx at truecenter
    "She quickly undresses and lays on the floor."
    $ k.override_portrait("portrait", "suggestive")
    k.say "Well? I'm waiting. A word of warning though. If it won't be better than masturbation, we're done now and forever."
    "Looks like to need to work with tongue for a start. You bend down and begin. If she really doesn't have any experience besides her hand, it will be easy."
    k.say "..."
    "At first she remains silent, but you notice how often she breathes now."
    $ k.override_portrait("portrait", "shy")
    k.say "Mmm..."
    "You increase the pace."
    k.say "Ah..."
    "She softly moans now. Good, but you need to try even harder."
    k.say "Aah... H-hey, [hero.name], you... ahh... you can stop now... aaaahhh..."
    "Too bad, too late. You increase the pace even more."
    $ k.override_portrait("portrait", "ecstatic")
    k.say "I-I said... ahh... ahh.. I said you can st... AHH!"
    "She does not attempt to stop you, so maybe it's a roleplay of some kind? Doesn't matter, you are here to prove her your skill, not your chivalry."
    "Last seconds, and..."
    $ k.override_portrait("portrait", "ecstatic")
    k.say "AHHHHH!"
    "...done."
    hide xxx with dissolve
    show bg hiddenvillage_entrance with dissolve
    show expression k_spr at center with dissolve
    "It took her a few minutes to recover. She got dressed and together you left the hotel."
    "Finally she broke the silence."
    $ k.override_portrait("portrait", "indifferent")
    k.say "I suppose I was wrong. I always thought it feels just the same, not matter how... or with who you do it."
    $ k.override_portrait("portrait", "happy")
    k.say "You should be proud of your skills. Normally I do it silently, but I just could not help but moan this time."
    $ k.override_portrait("portrait", "shy")
    k.say "I was afraid someone might hear me and enter the room. But you didn't stopped, so I was considered to attack you with my paper technique..."
    "Oh. That was close."
    $ k.override_portrait("portrait", "happy")
    k.say "But then I thought 'screw it, I'd rather kill anyone who enters the room and interrupts us'."
    "She suddenly leans forward and whispered in your ear."
    $ k.override_portrait("portrait", "suggestive")
    k.say "I can't wait for more. You know where to find me."
    hide expression k_spr with dissolve
    "With these words, she turned around and left. Still waters run deep, huh?" #unlocking sex with her
    $ k.set_flag("allowed_sex", value="True")
    $ k.set_flag("quest_no_sex", value="False")
    $ k.restore_portrait()
    scene black with dissolve
    stop world