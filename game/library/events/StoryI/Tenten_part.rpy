init python:
    questtenten = register_quest("Weapons Specialist", manual=True)

label tenten_first_meeting:
    scene black
    $ ten = chars["Tenten"]
    $ ten_spr = chars["Tenten"].get_vnsprite()
    $ tem = chars["Temari"]
    $ tem_spr = chars["Temari"].get_vnsprite()
    show bg hiddenvillage_entrance with dissolve
    show expression ten_spr at mid_right
    show expression tem_spr at mid_left
    with dissolve
    "Passing through the village, you hear Temari talking with a girl."
    $ ten.override_portrait("portrait", "angry")
    $ tem.override_portrait("portrait", "indifferent")
    tem.say "...happened?"
    ten.say "I digress for a moment, and they used a sleeping gas bomb to knock me out."
    tem.say "And?"
    ten.say "They took everything I had! My scrolls, my money, my clothes, everything..."
    tem.say "Did they... did something with you? I mean..."
    ten.say "That's the worst part! I was there, naked and helpless, and they did nothing! Those penisless jerks! When I'll catch them, they will regret that they were born!"
    $ tem.override_portrait("portrait", "confident")
    tem.say "Wouldn't you need your scrolls and weapons to do it?"
    $ ten.override_portrait("portrait", "happy")
    ten.say "Yes, about that... Can you lend me money for new equipment? Please?"
    tem.say "No way. I cannot afford to buy several hundreds ninja weapons that were sealed in your scrolls. You better start to save money, Tenten."
    $ ten.override_portrait("portrait", "angry")
    ten.say "I swear, I'll kill them with my bare hands..."
    hide expression ten_spr at mid_left
    hide expression tem_spr at mid_right 
    with dissolve
    $ ten.restore_portrait()
    $ tem.restore_portrait()
    "Looks like a severe case. The best approach would be to find her equipment for a start."
    $ pytfall.world_quests.get("Weapons Specialist").next_in_label("You met Tenten, a tomboyish kunoichi who lost her weapon scrolls. Here we give a quest find them in SE -_-")
    $ del ten
    $ del ten_spr
    $ del tem
    $ del tem_spr
    scene black with dissolve
    jump hiddenvillage_entrance
    
label tenten_second_meeting: # after finding the summon scroll
    scene black
    $ b = Character("Bandit", color=white, what_color=white, show_two_window=True)
    $ ten = chars["Tenten"]
    $ ten_spr = chars["Tenten"].get_vnsprite()
    $ tem = chars["Temari"]
    $ tem_spr = chars["Temari"].get_vnsprite()
    show bg hiddenvillage_entrance with dissolve
    "Armed with ninja scrolls, you carefully approach the girl."
    $ ten.override_portrait("portrait", "angry")
    show expression ten_spr at center with dissolve
    ten.say "Who are you? What do you need?"
    $ ten.disposition += 200
    "She seems to be not in the mood. The best approach would be..."
    menu:
        "Be a gentleman, call her a lady and politely offer the scroll":
            $ ten.override_portrait("portrait", "indifferent")
            ten.say "Hm? Who are you talking to?"
            $ ten.override_portrait("portrait", "shy")
            ten.say "W-wait, you mean me? L-lady?"
        "There is no time to beat around the bush. Scroll for virginity.":
            $ ten.override_portrait("portrait", "indifferent")
            ten.say "Say what? You want to take my..."
            $ ten.override_portrait("portrait", "shy")
            ten.say "I don't know what to say... I mean, no one had ever offered me to..."
    show expression tem_spr at mid_left with dissolve
    $ tem.override_portrait("portrait", "confident")
    tem.say "Hello Tenten, hello [hero.name]! <she notices Tenten blush> Oh? Did I interrupted something interesting?"
    $ tem.override_portrait("portrait", "happy")
    tem.say "Are you guys on a date or something? Well done, Tenten! I told you you will find someone sooner or later."
    ten.say "Wait, Temari, he... Um, [hero.name] just gave my my scrolls back and..."
    tem.say "Good timing! I wanted to help too, so I tracked the bandits. I'm sure it's the same guys who robbed you."
    $ ten.override_portrait("portrait", "indifferent")
    ten.say "How do you know?"
    $ tem.override_portrait("portrait", "confident")
    tem.say "Simple. One of them is wearing your clothes."
    ten.say "Huh? Why would he wanted to wear women's clothing?"
    tem.say "Well, if I have to guess, to them it looks similar enough to men's clothing, so..."
    $ ten.override_portrait("portrait", "angry")
    ten.say "Where are they?!"
    $ tem.override_portrait("portrait", "happy")
    tem.say "Not far from the village. Come on, I'll show you. Want to tag along, [hero.name]? Come on, it will be fun!"
    $ ten.override_portrait("portrait", "indifferent")
    ten.say "I don't mind. Don't worry, if something happens, we will cover you."
    "Looks like a good chance to see kunoichi at work without being killed."
    hide expression ten_spr
    hide expression tem_spr
    with dissolve
    show bg story training_ground with dissolve
    "Very soon Temari brought you to the village outskirts. You see a group of men ahead."
    $ ten.override_portrait("portrait", "indifferent")
    ten.say "Hey, do you remember me, criminals?"
    b "What is it, boy? We don't have time right now, so get lost."
    $ tem.override_portrait("portrait", "confident")
    tem.say "Ouch. You better step back, [hero.name]."
    $ ten.override_portrait("portrait", "angry")
    ten.say "Boy? BOY?! I will rape your corpse, you bastard!" 
    hide expression ten_spr
    hide expression tem_spr
    with dissolve
    $ enemy_team = Team(name="Enemy Team", max_size=3)
    $ your_team = Team(name="Your Team", max_size=3)
    $ tem.front_row = True
    $ ten.front_row = True
    $ hero.front_row = False
    $ mob_1 = build_mob("Warrior", level=20)
    $ mob_2 = build_mob("Warrior", level=25)
    $ mob_3 = build_mob("Archer", level=15)
    $ enemy_team.add(mob_1)
    $ enemy_team.add(mob_2)
    $ enemy_team.add(mob_3)
    $ your_team.add(tem)
    $ your_team.add(ten)
    python:
        for member in your_team:
            member.controller = BE_AI(member)
    $ your_team.add(hero)
    $ battle = BE_Core(Image("content/gfx/bg/be/b_forest_1.png"), music="content/sfx/music/be/battle (14).ogg", start_sfx=get_random_image_dissolve(1.5), end_sfx=dissolve)
    $ battle.teams.append(your_team)
    $ battle.teams.append(enemy_team)
    $ battle.start_battle()
    $ your_team.reset_controller()
    if battle.winner != your_team:
        jump game_over
    show bg story training_ground with dissolve
    show expression ten_spr at mid_right
    show expression tem_spr at mid_left
    ten.say "How about that, lowlife? How about that?"
    tem.say "Calm down, Tenten. They cannot hear you anymore."
    "Poor bandits were no match for two kunoichi."
    $ ten.override_portrait("portrait", "indifferent")
    ten.say "<panting> I'll just take back my equipment, and we can go back."
    hide expression ten_spr with dissolve
    $ tem.override_portrait("portrait", "confident")
    tem.say "...Try to not hurt her feeling, [hero.name]. For your own safety."
    tem.say "As you can see, she is not very popular among men. Some men like tomboys, but her case is... extreme."
    show expression ten_spr at mid_right
    $ ten.override_portrait("portrait", "confident")
    ten.say "Alright, I'm done. Let's go."
    "Together you come back to the village. You can't help but notice how Tenten tries to keep close to you. Poor girl is ready to jump on the first available guy..."
    $ ten.restore_portrait()
    $ tem.restore_portrait()
    $ ten.set_flag("quest_cannot_be_lover", value=False)
    $ ten.set_flag("quest_cannot_be_fucked", value=False)
    $ pytfall.world_quests.get("Weapons Specialist").next_in_label("You managed to get closer to her. Now it's up to your charisma.")
    $ del ten
    $ del ten_spr
    $ del tem
    $ del tem_spr
    $ del b
    scene black with dissolve
    jump hiddenvillage_entrance

label tenten_finish_quest:
    "Tenten was the easiest target ever. It's hard to be a tomboy..."
    $ pytfall.world_quests.get("Weapons Specialist").finish_in_label("You took care of Tenten's virginity.", "complete")
    jump hiddenvillage_entrance
    
label tenten_bonus_scene: # random scene after doing it with both temari and tenten
    stop music
    stop world
    play world "park.mp3" fadein 2.0 loop
    scene black
    $ ten = chars["Tenten"]
    $ tem = chars["Temari"]
    show bg story training_ground with dissolve
    $ ten.override_portrait("portrait", "suggestive")
    $ tem.override_portrait("portrait", "sad")
    "Walking through the outskirts of the village, you heard a strange noise."
    "Driven by curiosity, you carefully venturing into the woods. Sounds become closer..."
    show expression ten.show("sex", "gay", "nature", "indifferent", "scissors", resize=(600, 800), type="first_default") as xxx at truecenter with dissolve
    tem.say "Ah... Mmm... Tenten, I..."
    ten.say "Quite, Temari. Someone might hear us. You know how Tsunade disapproves these things!"
    "You immediately recall how Temari said something about someone that she had an eye for. You thought it's a man, but looks like Tenten is manly enough for her."
    "It's not safe to stay, so you quickly leave before they will notice (and probably kill) you."
    $ ten.restore_portrait()
    $ tem.restore_portrait()
    $ del ten
    $ del tem
    scene black with dissolve
    stop world