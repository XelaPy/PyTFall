init python:
    q = register_quest("Settling in the city")
    register_event("reflection_quest_part_one", quest="Settling in the city", dice=None, trigger_type="auto", max_runs=1)
init:
    image carstein = ProportionalScale("content/events/StoryI/Eric Carstein.png", 1700, 500)
    $ ec_neutral = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_neutral.png")
    $ ec_sad = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_sad.png")
    $ ec_scared = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_scared.png")
    $ ec_happy = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_happy.png")
    $ ec_angry = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_angry.png")
    $ ec_d = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_d.png")
    image bag = ProportionalScale("content/items/quest/bag.png", 150, 150)
    image clocks = ProportionalScale("content/items/quest/cl2.png", 150, 150)
    image letter = ProportionalScale("content/items/quest/letter.png", 150, 150)
    image box = ProportionalScale("content/items/quest/box.png", 150, 150)


label reflection_quest_part_one:
    stop world
    stop music
    scene black with dissolve
    play world "cemetery.ogg" fadein 2.0 loop
    show expression Text("City Cemetery", style="TisaOTM", align=(0.5, 0.33), size=40) as txt1:
        alpha 0
        linear 3.5 alpha 1.0
    pause 2.5
    hide txt1
    show bg cemetery with dissolve
    "You found the cemetery very soon with the help of locals. It does not look abandoned, but you are almost alone here."
    "..."
    "But after two hours of searching you found nothing."
    show bg story tombstone with dissolve
    show carstein at center with dissolve
    ec_sad "..."
    "On the very edge you see an old man standing next to a tombstone. Maybe he is the author of the letter? You come closer with caution."
    ec_happy "Well hello there youngster."
    "His voice is low and raspy."
    ec_happy "Not many people come to this place these days. Do you have some business with me?"
    $ cem = 0
    label reflection_quest_diag_one:
    menu:
        "Look at the tombstone next to him":
            "Nope, it's not your father. You can not make out the name, but the surname is 'Carstein'."
            jump reflection_quest_diag_one
        "Ask about the cemetery":
            ec_neutral  "Ah yes, you see, after the riot there were too many dead bodies to bury, so we started to burn them." 
            ec_neutral  "Over time it has become a tradition, and cemeteries are almost no longer used as before."
            ec_neutral "That's why not many people come here these days. <he glances at the tombstone nearby>"
            jump reflection_quest_diag_one
        "Ask what is he doing here":
            ec_happy "<he laughs softly> The same thing as you, I presume. Pay tribute to the fallen."
            jump reflection_quest_diag_one
        "Ask about your father's grave":
            ec_d "Oh, so you are looking for HIM. I'm afraid he is not here. I don't know where he is. Maybe nobody knows."
            $ cem = 1
            jump reflection_quest_diag_one
        "Leave" if cem == 1:
            "You turning around, going to leave this place. Obviously, the letter was someone's joke."
            ec_neutral "But if you looking for anyone else, we can help each other, [hero.name]."
    "You stop. Does he know you?"
    ec_neutral "Allow me to introduce myself, boy. I am Eric Carstein, retired militia officer."
    ec_neutral "I used to know your father. Now I'm just a tired old man, but I still have some connections with military."
    label reflection_quest_diag_two:
    menu:
        "Ask about the papers of your father":
            ec_d "<he doesn't look interested> Ah yes, he used to work on something. I don't know what it was, and I don't want to know too."
            ec_neutral "I already know enough to sleep bad at night. <he winks at you> Let's not worsen the situation."
            jump reflection_quest_diag_two
        "Ask about your father":
            ec_neutral "We were friends from childhood. Always wanted to make a military career."
            ec_sad "And we both succeeded in killing people. I was on the battlefield, your father was in the laboratory."
            jump reflection_quest_diag_two
        "Show him your letter":
            show letter at center with dissolve
            "You show him the letter you received two weeks ago."
            ec_neutral "Ah yes, I sent it. You see, I don't know the details, but I know that some dangerous people trying to find you right now."
            ec_neutral "They don't expect you to be right in the city thanks to my warning, so we have some time."
            hide letter with dissolve
    ec_neutral "I believe we can be helpful to each other. If you help me to understand something, I will help you the best I can in return."
    ec_neutral "Buy yourself a house. Find a job. Gather some money."
    ec_neutral "<he gives you address> This is where I live. Meet me there when you will be ready. Until then..."
    hide carstein with dissolve
    "He left. After a short while you go back to the city."
    $ pytfall.world_quests.get("Settling in the city").next_in_label("Your new acquaintance Carstein wants you to buy a house in the city and gather 3000 gold before you can continue.")
    $ pytfall.world_events.kill_event("reflection_quest_part_one")
    stop world fadeout 2.0
    $ register_event_in_label("reflection_quest_part_two", quest="Settling in the city", locations=["mainscreen"], run_conditions=["hero.gold >= 3000"], dice=100, max_runs=1)
    scene black
    jump city
    
label reflection_quest_part_two:
    stop music
    stop world
    scene black with dissolve
    play world "Town5.ogg" fadein 2.0 loop
    show bg story cab with dissolve
    show carstein at center with dissolve
    "You managed to settle a bit for the last days. You came to Carstein as he asked and told that you are ready."
    ec_neutral "Good, very good. During this time I learned something new about our... case."
    "You sit on a luxury sofa. It's very comfortable and most likely worth more than your house."
    label last_carst:
    menu:
        "Ask about your father's grave":
            ec_happy "Ah, you see, nobody knows where is he. At least no one alive in the city. <he grins slightly>"
            jump last_carst
        "Ask about the letter":
            ec_neutral "Nothing new here. It's the same paper, the same inks, the same handwriting."
            ec_neutral "But letters are identical to each other. Yet the force pressing the paper is different, so it shouldn't be written by a machine."
            ec_sad "<sigh> ...Or at least my connections think so."
            jump last_carst
        "Ask about new clues":
            ec_neutral "Yes, yes. <he looks at you> Do you know what happened in 3596?"
            $ a = 0
            $ b = 0
            $ c = 0
            label last_carst1:
            menu:
                "My father died" if a == 0:
                    $ a = 1
                    ec_sad "Yes, indeed. A tragedy, but just one of many. There are witnesses of his death, but no one saw what happened to his body after."
                    jump last_carst1
                "The city was wiped out" if b == 0:
                    $ b = 1
                    ec_neutral "Close, but not truth. We lost a quarter of the city. Mainly the slave army was affected, because we managed to gather rebels in one place."
                    jump last_carst1
                "Slaves rebellion" if c == 0:
                    $ c = 1
                    ec_neutral "Indeed, but they happened almost every year back then. Although it was a big one, perhaps the biggest one."
                    ec_sad "<you are alone in the room, but he lowers his voice anyway> They say someone helped them. Someone gave them weapons and magic to fight back."
                    ec_sad "But in the end they were manipulated by someone. The riot was a consequence, not a cause."
                    jump last_carst1
                "Enough with history" if a == 1 or b == 1 or c == 1:
                    ec_happy "<he makes a short laugh> As you say, young man. After all, if you want to know the official history, you can go to the library."
                    ec_neutral "Unfortunately, the red flash that vaporized the army of slaves also destroyed most of the clues. The official story for the most part consists of assumptions and propaganda."
                    ec_neutral "And the user of the weapon lost his mind, so he is useless to us..."
    ec_happy "However, I have an idea where we should start looking."
    ec_neutral "The weapon used during the riot was found in ruins not very far from the city. They say an itinerant historian came to the city and told us where to find it."
    ec_neutral "<sigh> And everything he said was true. The riot ended with a single flash. The city has grown and become rich."
    ec_neutral "And he never told us about the consequences for one who used it. So technically, he did not lie in anything."
    ec_sad "<he frowns> Very convenient. But there is more. Nobody remembers how he looked. Initially I had hoped to find him, and questioned eyewitnesses for many years."
    ec_neutral "So now I want you to send an expedition to the ruins he mentioned. This is the best clue I have. The information about its location is classified, so most likely nobody was there after Terumi."
    ec_neutral "See if you can find something. Anything."
    "You get up to leave."
    ec_sad "...And be careful. Do not tell anyone about our conversation."
    # And so we give a quest to find ruins deep in SE. When the group will return, MC will know that ruins were sealed by impenetrable stone wall.
    # At the wall there is the same symbol you saw at Sakura's equipment.
    scene black with dissolve
    stop music fadeout 2.0
    
label intro_story_ff:
    stop music # after ruins were opened and expedition returned
    stop world
    scene black with dissolve
    play world "Town5.ogg" fadein 2.0 loop
    show bg story cab with dissolve
    show carstein at center with dissolve
    ec_sad "Well, I can't say I'm surprised. Do not be upset, young man."
    "Despite the assistance of kunoichi, the result of the expedition wasn't satisfactory."
    ec_neutral "I don't quite understand why they sealed the ruins in the first place. Perhaps it was done to slow us down, and in this case it worked perfectly."
    "Your last expedition has found some monsters and trinkets in the ruins, but nothing about the ancient weapon."
    ec_neutral "The description of the ruins made by your expedition does not match at all the description made by the first expedition. There are many ways to explain it, but I have no idea which one is the best in this case..."
    menu:
        "The first expedition?":
            ec_neutral "Yes, it took the weapon from the ruins. Only one of its members is still alive."
        "What should we do now?":
            ec_neutral "I have an idea. One member of the first expedition is still alive."
    ec_neutral "Terumi, the ex captain of the city's Intelligence Department. He brought us the weapon, and he used it against the riot. Which appears to have some devastating affect on him."
    ec_neutral "Currently he is contained in a special underground section of the Department. It's like a prison for special cases."
    ec_neutral "I did not see him personally. but they say he lost hid mind and will."
    ec_happy "I bet you wonder how can we get information from him. Your new ninja friends will help us."
    menu:
        "How do know about it?":
            ec_happy "I told you, I have good connections."
        "Are you spying on me?":
            ec_happy "I told you, I have good connections. You had a lot of fun recently, don't you?"
        "How?":
            $ pass
    ec_neutral "I heard many things about their healing techniques. I believe some of them are powerful enough to return Terumi his mind."
    ec_neutral "I cannot be sure, so you better ask your ninja friends about it. If they want money, tell them I'm willing to cover the bill."
    "You get up to leave."
    ec_sad "[hero.name], do not trust Terumi. If possible, do not let him free."
    scene black with dissolve
    stop music fadeout 2.0