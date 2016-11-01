init python:
    q = register_quest("A Fugitive")
    register_event("naruko_first_meeting", quest="A Fugitive", simple_conditions=["hero.level >= 1000", "hero.gold >= 500"], locations=["cafe"], dice=100, restore_priority=0, jump=True, trigger_type="auto") # disabled for testing; TODO before the release: make "hero.level >= 10"
    q1 = register_quest("The Hidden Ones")
    
label naruko_first_meeting:
    $ hero.AP -=1
    if global_flags.flag("waitress_chosen_today") != day:
        $ cafe_waitress_who = choice(["npc cafe_mel_novel", "npc cafe_monica_novel", "npc cafe_chloe_novel"])
        $ global_flags.set_flag("waitress_chosen_today", value=day)
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    $ waitress = Character("Waitress", color=white, what_color=white, show_two_window=True)
    show expression Transform(cafe_waitress_who, zoom=0.7) at center
    show expression n_spr at right
    with dissolve
    
    waitress "Welcome to the Ca... Oh, it's you again."
    $ n.override_portrait("portrait", "angry")
    n.say "What's wrong with you, people? I just want some food!"
    waitress "Like I said, the food is not free. Get a work if you don't have money."
    n.say "But I have money! Look!"
    "She demonstrates a bag of coins. It's clearly not gold."
    waitress "I'm sorry, Naruko, but we only accept gold. These coins are worthless here."
    hide expression Transform(cafe_waitress_who, zoom=0.7) with dissolve
    $ n.override_portrait("portrait", "sad")
    n.say "Man, this sucks... I'm starving..."
    hide n_spr with dissolve
    $ pytfall.world_quests.get("A Fugitive").next_in_label("You've met a weird starving girl near the cafe. Perhaps you could offer help?")
    $ pytfall.world_events.kill_event("naruko_first_meeting", cached=True)
    jump cafe
    
label naruko_first_feeding:
    $ renpy.hide(cafe_waitress_who)
    with dissolve
    $ n = chars["Naruko_Uzumaki"]
    $ n_spr = chars["Naruko_Uzumaki"].get_vnsprite()
    $ waitress = Character("Waitress", color=white, what_color=white, show_two_window=True)
    show expression n_spr at center with dissolve
    if pytfall.world_quests.check_stage("A Fugitive") == 1:
        $ n.override_portrait("portrait", "sad")
        n.say "What is it?"
        hero.say "You ask her if she is in trouble."
        $ n.override_portrait("portrait", "indifferent")
        n.say "Uhh, maybe a little. I have not eaten for four days, and no one wants my money, and this damn city is so big I keep going astray, ha ha..."
        hero.say "You propose to help her with money."
        $ n.override_portrait("portrait", "happy")
        n.say "For real? That's awesome! I'm fine though, I just need some food to restore my strength."
        hero.say "You call the waitress and offer Naruko to make an order."
        $ cost = randint(100, 150)
        if hero.take_money(cost):
            $ name = "content/gfx/images/food/animated/big_" + str(renpy.random.randint(1, 3)) + ".webm"
            show image Movie(channel="main_gfx_attacks", play=name) at truecenter with dissolve
        waitress "It will be [cost] gold, thank you very much!"
        hide image Movie(channel="main_gfx_attacks", play=name) with dissolve
        "It cost you more than you expected. She ate a whole mountain of food."
        n.say "Aaaah, it feels so good... You are a lifesaver!"
        $ n.disposition += 20
        n.say "I'll repay you, I promise. Let's meet here tomorrow, ok?"
        hide expression n_spr with dissolve
        $ pytfall.world_quests.get("A Fugitive").next_in_label("You paid for her food. Perhaps later you will meet her again at the same place.")
        $ n.set_flag("quest_ate_in_cafe", value=day)
    elif pytfall.world_quests.check_stage("A Fugitive") == 2:
        $ n.override_portrait("portrait", "happy")
        n.say "Sup, [hero.name]! Feeling good?"
        $ hero.set_flag("ate_in_cafe", value=day)
        n.say "Yesterday I tried to find a job, but lost and ended up in a huge garden. It was sooo cool! There were those red flowers everywhere, and they smelled so funny! Here, I got one for you too!"
        $ hero.add_item ("Red Rose")
        "She gives you a red rose. There is only one place in the city where they grow in a garden, called royal gardens."
        "Now it's too dangerous to hire her or give her a room since she could be wanted for illegal entry. They will look for her for weeks."
        hide expression our_image with dissolve
        n.say "I wanted to stay there a bit more, but some angry people showed up and chased me away..."
        n.say "Anyway, I'm really hungry! Let's eat!"
        $ cost = randint(40, 60)
        if hero.take_money(cost):
            $ name = "content/gfx/images/food/animated/big_" + str(renpy.random.randint(1, 3)) + ".webm"
            show image Movie(channel="main_gfx_attacks", play=name) at truecenter with dissolve
        "You order some food too, and you eat together as she tells you about her misadventures in the city."
        hide image Movie(channel="main_gfx_attacks", play=name) with dissolve
        waitress "It will be [cost] gold, thank you very much!"
        $ n.disposition += 10
        n.say "Aaaah, so tasty! See ya around!"
        hide expression n_spr with dissolve
        $ n.set_flag("quest_ate_in_cafe", value=day)
        $ pytfall.world_quests.get("A Fugitive").next_in_label("You've met again. She's still broke.")
    elif pytfall.world_quests.check_stage("A Fugitive") == 3:
        $ n.override_portrait("portrait", "happy")
        $ hero.set_flag("ate_in_cafe", value=day)
        n.say "Hey, [hero.name]! Look what I've found!"
        "She handles you a small gem."
        $ hero.add_item ("Amethyst")
        n.say "I've found a really huge river and wanted to swim. But there were big waves, and one of them..."
        "There are no rivers near the city. She must be talking about the ocean."
        $ n.override_portrait("portrait", "shy")
        n.say "Well, it took my bra. I tried to find it, but instead found a small underwater cave with this pretty stone. You can have it."
        $ n.override_portrait("portrait", "happy")
        n.say "Oh well, I can live without it anyway. I still have the remaining clothes. Let's eat."
        $ cost = randint(40, 60)
        $ n.disposition += 10
        if hero.take_money(cost):
            $ name = "content/gfx/images/food/animated/big_" + str(renpy.random.randint(1, 3)) + ".webm"
            show image Movie(channel="main_gfx_attacks", play=name) at truecenter with dissolve
        "You order some food too, and you eat together as she tells you about her misadventures at the beach."
        hide image Movie(channel="main_gfx_attacks", play=name) with dissolve
        waitress "It will be [cost] gold, thank you very much!"
        n.say "Aaaah, so tasty! See ya around!"
        hide expression n_spr with dissolve
        $ n.set_flag("quest_ate_in_cafe", value=day)
        $ pytfall.world_quests.get("A Fugitive").next_in_label("She's lost her bra, but found a gem for you.")
    elif pytfall.world_quests.check_stage("A Fugitive") == 4:
        $ n.override_portrait("portrait", "happy")
        $ hero.set_flag("ate_in_cafe", value=day)
        n.say "[hero.name]! Doing alright?"
        n.say "This place is so big! And it's never boring here, unlike my home."
        hero.say "You ask about her home."
        $ n.override_portrait("portrait", "indifferent")
        n.say "Oh, it's just a small, boring village. Nothing ever happens there, and they don't allow us to leave it too."
        n.say "So, you know, I said 'screw it' and ran away. I'm not gonna waste my life hiding in a bushes when there is a huge, amazing world around."
        $ n.override_portrait("portrait", "happy")
        n.say "No matter. Hey, let's try those cupcakes, they look awesome!"
        $ n.disposition += 10
        $ n.override_portrait("portrait", "happy")
        $ cost = randint(40, 60)
        if hero.take_money(cost):
            $ name = "content/gfx/images/food/animated/big_" + str(renpy.random.randint(1, 3)) + ".webm"
            show image Movie(channel="main_gfx_attacks", play=name) at truecenter with dissolve
        "You order some food too, and you eat together. You trying to find out more about her homeland, but she quickly changes the subject, and bombards you with questions about the city."
        hide image Movie(channel="main_gfx_attacks", play=name) with dissolve
        waitress "It will be [cost] gold, thank you very much!"
        n.say "Mmm, delicious! Hey, we should go to the beach together sometime, what do you say?"
        $ n.override_portrait("portrait", "shy")
        n.say "I mean, after I get another swimsuit..."
        hide expression n_spr with dissolve
        $ n.set_flag("quest_ate_in_cafe", value=day)
        $ pytfall.world_quests.get("A Fugitive").next_in_label("Looks like she ran away from a small village. Although, there are no villages near the city as far as you know.")
    elif pytfall.world_quests.check_stage("A Fugitive") == 5:
        $ n.override_portrait("portrait", "happy")
        $ hero.set_flag("ate_in_cafe", value=day)
        n.say "Hey, you late, [hero.name]! I'm starving!"
        n.say "Let's see, today I want these eggs in tomato sauce, raspberry muffins and..."
        $ k = chars["Kushina_Uzumaki"]
        $ k_spr = chars["Kushina_Uzumaki"].get_vnsprite()
        show expression k_spr at left with dissolve
        $ k.override_portrait("portrait", "happy")
        k.say "Hey guys, mind if I join?"
        $ n.override_portrait("portrait", "indifferent")
        $ n.show_portrait_overlay("surprised", "reset")
        n.say "..!"
        "A woman suddenly approaches you."
        k.say "I just had a little chat with the waitress here, and she told me you two are regular visitors! Who would have thought that I'll find you so fast."
        k.say "I appreciate you concern about my daughter, [hero.name]. Even though a small diet wouldn't hurt in her case, it was a worthy act."
        $ n.override_portrait("portrait", "sad")
        $ n.hide_portrait_overlay()
        n.say "Mom, I..."
        $ k.override_portrait("portrait", "angry")
        k.say "We'll speak at home, darling. Take a good look at these muffins by the way. Then there will be something to remember the next two years on bread and water."
        $ k.override_portrait("portrait", "indifferent")
        k.say "Now, I believe she owns you quite a sum, eh?"
        menu:
            "Indeed":
                k.say "Here, it should cover your expenses and then some more."
                $ hero.add_money(700)
            "Refuse":
                $ k.override_portrait("portrait", "happy")
                $ n.disposition += 10
                $ k.disposition += 20
                k.say "Oh? That's very nice of you."
        $ k.override_portrait("portrait", "angry")
        k.say "Now then, time to return home, Naruko. And don't even try to pull something."
        n.say "...Ok. Bye, [hero.name]."
        hide k_spr
        hide n_spr
        with dissolve
        $ pytfall.world_quests.get("A Fugitive").finish_in_label("Her mother found her and took home. Perhaps you'll see them again in the future.", "complete")
        $ n.del_flag("quest_ate_in_cafe")
        $ n.restore_portrait()
        $ k.restore_portrait()
        $ register_event("quest_to_unlock_village", quest="The Hidden Ones", simple_conditions=["hero.level >= 20"], locations=["main_street"], dice=100, restore_priority=0, jump=True, trigger_type="auto")
    jump main_street
    
label quest_to_unlock_village:
    "As you walked down the street, something landed just before you."
    show expression Image("content/items/quest/orig_1.png") as i with dissolve 
    "It's a bird or something like that made from colored paper."
    hide i with dissolve
    "You picked it up and examined. Suddenly, the bird's head turned, pointing somewhere to the north-west."
    "Perhaps it's worth investigating?" # FOR XELA: until this part the village location is hidden on the map, but at this moment we unlock it.
    $ pytfall.world_quests.get("The Hidden Ones").next_in_label("You found an animated paper figure which points to the north-west. Check the city map to travel there!")
    $ pytfall.world_events.kill_event("quest_to_unlock_village", cached=True)
    jump main_street
    
label first_arrive_to_the_hidden_village:
    scene bg hiddenvillage_entrance with dissolve
    $ k = chars["Konan"]
    $ k_spr = chars["Konan"].get_vnsprite()
    $ k.override_portrait("portrait", "indifferent")
    $ t = chars["Tsunade"]
    $ t_spr = chars["Tsunade"].get_vnsprite()
    $ t.override_portrait("portrait", "indifferent")
    "You always thought that there is nothing but endless forest, but soon enough the paper figure brought you to small village."
    "Once you entered it, the figure stopped moving, and at the next second you felt someone's hand on your shoulder."
    show expression k_spr at center with dissolve
    k.say "Welcome, visitor. Please follow me."
    menu:
        "Ask something":
            k.say "All your questions will be answered by the head of our village."
        "Silently follow her":
            $ pass
    hide expression k_spr with dissolve
    "You decided to follow her for now. The village seems quite peaceful and underpopulated."
    scene bg story cab_2
    show expression k_spr at left
    show expression t_spr at right
    with dissolve
    k.say "Your guest is here, ma'am."
    t.say "Wonderful. You may go now."
    hide expression k_spr with dissolve
    t.say "Welcome to our village, [hero.name]. Make yourself at home. You can call me Tsunade."
    $ i = 1
    while i == 1:
        $ t.override_portrait("portrait", "indifferent")
        menu:
            "Ask about the village":
                t.say "We just call it the hidden village. Once it had another name, but it's meaningless now."
                t.say "We are refugees. Twelve years ago we ran away from a war that is impossible to win. Before he died, our previous leader sent this part of the village as far as he could."
                t.say "This place is different from our homeland. Our enemies, almost invincible there, are powerless here. Therefore there is no need to worry about pursuers."
            "Ask about villagers":
                t.say "It's a village built for ninjas. You probably noticed that we don't have many people here. We tried to attract new people, but it's not that simple."
            "Ask about her":
                t.say "Oh, I'm just a medic. After our last leader passed away, I was the best alternative."
                $ t.override_portrait("portrait", "happy")
                t.say "Don't let it get to your head."
            "Ask why they brought you here":
                $ i = 2
    $ del i
    t.say "Oh, it's very simple. You are the first citizen who offered help to one of our people."
    $ t.override_portrait("portrait", "indifferent")
    t.say "I was looking for a chance to establish a relationship with the city, and you proved yourself to to somewhat trustworthy."
    t.say "Now, let's get down to the business. You must have noticed how Naruko knows next to nothing about your world. This is also true for most other villagers."
    t.say "I visit the city regularly, but they rarely left the village. They don't know how to behave, don't know about the laws."
    t.say "This village is doomed. We don't have enough people to maintain population. The city is our only future."
    t.say "So I propose a deal. The first part is to teach our people about your world and laws. It should be pretty simple for someone who lived in the city the whole life."
    $ t.override_portrait("portrait", "confident")
    t.say "The second part is a bit more... personal. I am the head medic for the village. As such, it is my position to watch over certain... customs."
    t.say "We have an older custom. When a female ninja qualifies for the jobs above a certain clearance, there is a real danger that she gets captured. You probably understand that females do get a 'special treatment', right?"
    t.say "Back in my days, we kept it in the family. Don't look at me like that. You usually had an older member of the family, that liked the young ninja a lot, and that agreed to, you know."
    t.say "That was back then, but now, things are different. We don't have any males left, not to mention that they have all those modern ideas about finding love outside the village."
    t.say "I am not asking you to rape them, or to force yourself on them. If you get idea, it would be a miracle if you survive the attempt."
    t.say "Their first time should be with someone that they trust, someone that has shown them how beautiful a thing this can be. Not some slobbering pimply faced boy that has to drink his courage, pukes all over their dresses, and then can't get it up."
    t.say "I'm talking about a first time that will stay with them forever, and that will shield them against all the bad things they will have. A woman can go through much if she has good memories. Good memories carry you through being imprisoned, captured, and a whole lot more."
    $ t.override_portrait("portrait", "indifferent")
    t.say "I'm sure they will be more than happy to join you after the education is over. You could use a few highly skilled fighters, right?"
    $ t.restore_portrait()
    $ k.restore_portrait()
    "From now on you can use the main village building to teach locals. Over time they will begin to trust you enough to do something else."
    $ pytfall.world_quests.get("The Hidden Ones").finish_in_label("You found a village of ninjas in the forest near the city.", "complete")
    $ global_flags.set_flag('hidden_village_study_icon')
    jump hiddenvillage_entrance
label hidden_village_study: # here MC teaches the villagers about the outside world
    scene bg story study
    if hero.AP > 0:
        $ hero.AP -= 1
    else:
        "You don't have Action Points left. Try again tomorrow."
        jump hiddenvillage_entrance
    if not global_flags.flag('visited_hidden_village_study'):
        $ global_flags.set_flag('visited_hidden_village_study')
        "This is the main building where you can teach multiple villagers at once. Every time after the lesson you can pick one of the characters to spend additional time with her."
        "The outcome however depends on her mood, so pay attention to their portraits."
    python:
        temp = list(i for i in naruto_quest_characters_list if dice(80)) # not everyone may be there every day
        if not(temp):
            temp = naruto_quest_characters_list # a countermeasure against empty list due to dice; if no one is there, then we force everyone to be there
        characters = {}
        for i in temp: # every character gets random mood via a dict based on disposition
            if i.disposition < 50:
                l="indifferent"
            elif i.disposition < 200:
                l=random.choice(["happy", "indifferent"])
            else: # might be a good idea to limit the amount of shy ones even further
                l=random.choice(["happy", "indifferent", "shy"]) 
            if l == "indifferent":
                i.set_flag("village_quest_knowledge_level", value=i.flag("village_quest_knowledge_level")+randint(0,1))
                i.disposition += randint(1, 2)
            elif l == "happy":
                i.set_flag("village_quest_knowledge_level", value=i.flag("village_quest_knowledge_level")+1)
                i.disposition += randint(2, 4)
            else:
                i.disposition += randint(4, 6)
                i.set_flag("village_quest_knowledge_level", value=i.flag("village_quest_knowledge_level")+randint(1,2))
            characters[i]=l

    $ char = q = renpy.call_screen("hidden_village_chars_list", characters)
    $ ff = q.flag("village_quest_knowledge_level") # lines to control how stuff works, should be deleted
    hero.say "her knowledge is [ff]" # lines to control how stuff works, should be deleted
    if characters[q] == "indifferent":
        if dice(50):
            call naruto_pack_image_list(q, "school")
            "Looks like [q.name] has troubles with understanding your lesson. You take your time to explain everything better."
            call interactions_teaching_lines
            $ q.set_flag("village_quest_knowledge_level", value=i.flag("village_quest_knowledge_level")+randint(1,2))
            $ q.disposition += randint(1,3)
        else:
            scene bg hiddenvillage_entrance with dissolve
            call naruto_pack_image_list(q, "talking")
            "You have a small chat with [q.name] after the studies are over."
            call hidden_village_special_chat(q)
            $ q.disposition += randint(3,4)
    elif characters[q] == "happy":
        if not q.flag("village_quest_house_is_visible"):
            call naruto_pack_image_list(q, "school")
            $ q.set_flag("village_quest_house_is_visible")
            call interactions_study_together
            "Now you can visit her house in the exploration mode!"
        else:
            call naruto_pack_image_list(q, "school")
            call interactions_invite_to_sparring
            if dice(50):
                scene bg city_beach_right
                "After short warming up she invites you to the beach."
                call naruto_pack_image_list(q, "beach")
                call interactions_invite_to_beach
                $ q.disposition += randint(5, 20)
            else:
                scene bg forest_1 with dissolve
                call naruto_pack_image_list(q, "sparring")
                "You spent some time helping [q.name] with her training. She really appreciates it."
                $ q.disposition += randint(10, 15)
    elif characters[q] == "shy":
        if dice(50):
            call naruto_pack_image_list(q, "school")
            call interactions_study_sex
            show bg girl_room with fade
            call naruto_pack_image_list(q, "revealing")
            call interactions_study_sex_lines
            $ act = random.choice(["blowjob", "titsjob", "handjob", "footjob"])
            $ picture = get_single_sex_picture_not_for_gm(q, act=act, location="room", hidden_partner=True)
            show expression picture at truecenter with dissolve
            call interactions_guy_cum_alot
        else:
            call naruto_pack_image_list(q, "school")
            call interactions_invite_to_sparring
            scene bg city_beach_right
            "After short warming up she invites you to the beach."
            call naruto_pack_image_list(q, "beach")
            call interactions_alone_together
            $ act = random.choice(["blowjob", "titsjob", "handjob", "footjob"])
            $ picture = get_single_sex_picture_not_for_gm(q, act=act, location="beach", hidden_partner=True)
            show expression picture at truecenter with dissolve
            call interactions_guy_cum_alot
            
        if q.flag("quest_cannot_be_fucked"):
            $ q.del_flag("quest_cannot_be_fucked")
            if not("Open Minded" in q.traits):
                $ q.apply_trait("Open Minded")
            "Now [q.name] can be your sex partner, assuming that she likes you enough of course."
            if not q.flag("village_quest_house_is_visible"):
                $ q.set_flag("village_quest_house_is_visible")
                "You can also visit her house in the exploration mode."
    jump hiddenvillage_entrance

label hidden_village_special_chat(char): # normally we jump to the chat label, but it this case we want call, so I copy part of the interactions chatting code here;
    if char.disposition >= 100:
        if ct("Impersonal") or ct("Dandere") or ct("Shy"):
            $ narrator(choice(["[char.pC] didn't talked much, but [char.pC] enjoyed your company nevertheless.", "You had to do most of the talking, but [char.p] listened you with a smile.", "[char.pC] welcomed the chance to spend some time with you.", "[char.pC] is visibly at ease when talking to you, even though [char.p] didn't talked much."]))
        else:
            $ narrator(choice(["It was quite a friendly chat.", "You gossiped like close friends.", "[char.pC] welcomed the chance to spend some time with you.", "[char.pC] is visibly at ease when talking to you.", "You both have enjoyed the conversation."]))
    elif char.disposition >=50:
        if ct("Impersonal") or ct("Dandere") or ct("Shy"):
            $ narrator(choice(["But there was a lot of awkward silence.", "But you had to do most of the talking.", "There is no sign of [char.op] opening up to you yet.", "But it was kind of one-sided."]))      
        else:
            $ narrator(choice(["It's all a little bit stiff.", "There's some reservation though...", "It's hard to find common ground.", "But it was somewhat forced."]))
    else:
        $ narrator(choice(["Looks like there's a good amount of mistrust between you.", "But it was difficult for both of you.", "Sadly, [char.p] was not very interested in chatting with you.", "It was clearly uncomfortable for [char.op] to speak to you.", "[char.pC] was suspicious of you the entire time and never let [char.op] guard down."]))
    return
screen hidden_village_chars_list(characters): # the screen shows portraits of given characters dict as imagebuttons at the bottom and returns the selected character; the dict is "character: [emotion tag]"
# TODO FOR XELA: portraits are not symmetrical for small groups, the screen will look better if they will always be
    hbox:
        spacing 25
        pos (17, 605)
        for l in characters.keys():
            $ char_profile_img = l.show('portrait', characters[l], resize=(98, 98), cache=True, type="reduce")
            $ img = "content/gfx/frame/ink_box.png"
            imagebutton:
                background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
                idle (char_profile_img)
                hover (im.MatrixColor(char_profile_img, im.matrix.brightness(0.15)))
                action [Return(l), Hide("hidden_village_chars_list")]
                align 0, .5
                xysize (102, 102)

label naruto_pack_image_list(char, location): # this label shows pictures for naruto chars depending on the location; should be called
    if location == "beach":
        $ picture = char.show("sfw", "swimsuit", exclude=["pool", "sleeping", "sad", "angry", "scared"], type="reduce", resize=(800, 600))

    elif location == "school":
        $ picture = char.show("sfw", "girlmeets", "schoolgirl", exclude=["outdoors", "sleeping", "revealing", "formal", "sad", "angry", "scared", "swimsuit"], type="reduce", resize=(800, 600))

    elif location == "sparring":
        $ picture = char.show("sfw", "battle", "outdoors", "nature", exclude=["indoors", "swimsuit"], type="reduce", resize=(800, 600))

    elif location == "talking":
        $ picture = char.show("sfw", "girlmeets", "outdoors", exclude=["wildness", "revealing", "formal", "sad", "angry", "scared", "swimsuit"], type="reduce", resize=(800, 600))
            
    else: # revealing
        $ picture = char.show("nude", "indoors", "living", exclude=["striptease", "sad", "angry", "scared", "swimsuit"], type="reduce", resize=(800, 600))
                
    show expression picture at truecenter with dissolve
    return
    
label hidden_village_hiring_tsunade:
    $ char.override_portrait("portrait", "confident")
    "You ask her to join you."
    char.say "I don't mind, I'm tired of this village as much as others. But I need to pay my gambling debts first. It will be 5000 G."
    if hero.gold >= 5000:
        menu:
            "Pay her 5000 G?"
            "Yes":
                if hero.take_money(5000):
                    char.say "Great, one debt less... I'll meet you outside the village then."
                    $ char.del_flag("event_to_interactions_hidden_village_hiring_tsunade")
                    $ char.del_flag("quest_cannot_be_hired")
                    $ char.del_flag("village_quest_house_is_visible")
                    $ hero.add_char(char)
                    $ char.restore_portrait()
                    jump hiddenvillage_entrance # TODO for XELA: for some reason after I jump to the entrance the girlmeets screen remains; I dunno how to fix it
                else:
                    char.say "Oh, that's too bad. Tell me if you change your mind."
                    $ char.restore_portrait()
                    jump girl_interactions
            "No":
                char.say "Oh, that's too bad. Tell me if you change your mind."
                $ char.restore_portrait()
                jump girl_interactions
    else:
        "Sadly, you don't have so much gold."
        char.say "Oh, that's too bad. The proposition still stands though."
        $ char.restore_portrait()
        jump girl_interactions
                    
label hidden_village_hiring_konan:
    "You ask her to join you."
    $ char.override_portrait("portrait", "indifferent")
    char.say "It's not a problem. However, I an a mercenary. I want 1000 G for my services."
    if hero.gold >= 1000:
        menu:
            "Pay her 1000 G?"
            "Yes":
                if hero.take_money(1000):
                    char.say "In this case, I'm at your service."
                    $ char.del_flag("event_to_interactions_hidden_village_hiring_konan")
                    $ char.del_flag("quest_cannot_be_hired")
                    $ char.del_flag("village_quest_house_is_visible")
                    $ hero.add_char(char)
                    $ char.restore_portrait()
                    jump hiddenvillage_entrance # TODO for XELA: for some reason after I jump to the entrance the girlmeets screen remains; I dunno how to fix it
                else:
                    char.say "Then please return when you will have the money."
                    $ char.restore_portrait()
                    jump girl_interactions
            "No":
                char.say "Then please return when you will have the money."
                $ char.restore_portrait()
                jump girl_interactions
    else:
        "Sadly, you don't have so much gold."
        char.say "Then please return when you will have the money."
        $ char.restore_portrait()
    jump girl_interactions