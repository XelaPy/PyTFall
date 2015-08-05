init python:
    renpy.image("nami_looking", animate("/library/events/moneybitch_event/img/nami_looking"))


    #Images from darkTI's onepiece pack.
    renpy.image("nami_approach", "library/events/moneybitch_event/img_darkti/0111-nn-e2-cb-l3-pr-pa.jpg")
    renpy.image("nami_face_wondering", "library/events/moneybitch_event/img_darkti/0004-po-ee.jpg")
    renpy.image("nami_face_excited", "library/events/moneybitch_event/img_darkti/0007-po-e9.jpg")
    
    renpy.image("nami_beach_undressing", "library/events/moneybitch_event/img_darkti/005E-nd-ec-cb-l5-pr-pa.jpg")
    renpy.image("nami_beach_ready", "library/events/moneybitch_event/img_darkti/013E-nd-e5-c4-l2-a1.jpg")
    renpy.image("nami_beach_sex", "library/events/moneybitch_event/img_darkti/013D-sx-e4-cb-l3-ns-p3-s4-sj-sm-p2.jpg")
    
    renpy.image("nami_beach_sex_forced", "library/events/moneybitch_event/img_darkti/00A8-sx-e4-l3-lc-ns-p3-s3-sj-p2.jpg");
    renpy.image("nami_beach_sex_happy", "library/events/moneybitch_event/img_darkti/00BC-sx-e4-e5-cb-l5-ns-p3-sj-p2.jpg");

    #Unsure about copyright etc. Perhaps necessarily to remove images.
    
    renpy.image("pitfall_idea", "library/events/moneybitch_event/img/pitfall_idea.png") # http://sakuramo-chi.deviantart.com/art/Sticking-pitfall-245601225
    renpy.image("pitfall", "library/events/moneybitch_event/img/pitfall.png") #http://dlminecraft.net/hungry-animals-mod/
    renpy.image("beach_cave", "library/events/moneybitch_event/img/beach_cave.jpg") #http://www.mobiletoones.com/browse/free-mobile-wallpapers/s43-nature-wallpapers/f68762-beach-cave.html
    
    # used in composite image.
    #renpy.image("pitfall", "library/events/moneybitch_event/img/chest-clipart-vector-88534402.jpg")  #http://www.clipartpanda.com/categories/treasure-chest-clipart
    renpy.image("nami_beach_sex_treasure", "library/events/moneybitch_event/img/nami_treasure_thoughts.png")
  
    #Since this quest has some content which isn't save for work its perhaps better to add a tag for it??
    register_quest("Treasure Seeker")
    if config.developer:
        register_event("show_nami_looking", screen=True, quest="Treasure Seeker", locations=["city_beach_right"], trigger_type="auto", restore_priority=1, priority=300, start_day=1, jump=True, dice=100, max_runs=20)
    else:
        register_event("show_nami_looking", screen=True, quest="Treasure Seeker", locations=["city_beach_right"], trigger_type="auto", restore_priority=1, priority=300, start_day=choice([15, 25, 35]), jump=True, dice=65, max_runs=20)
    
    # Dev Note: I've added screen attribute to WorldEvent class so the useless labels below are no longer required.
    # This doesn't change much for this event but in other places it will mean a much smoother gameplay.
    
screen show_nami_looking:
    zorder 10
    if renpy.get_screen("pyt_city_beach_right"):
        $ img = Transform("nami_looking", zoom=1)
        imagebutton:
            pos (800, 440) #was 400
            idle Transform("nami_looking", zoom=1) 
            hover Transform("nami_looking", zoom=1)
            action Jump("nami_discover_event")
    else:
        timer 0.01 action Hide("show_nami_looking")
        

label nami_discover_event:
    hide screen pyt_city_beach_right
    with dissolve
    "Walking on the beach enjoying the sight of many hot girls, you notice the strange behaviour of this attractive girl."
    
    menu:
        "You decide to follow the girl to see what she is doing.":
            jump nami_personality_event
        "My time is too precious, I like continue starting at the girls on the beach.":
            "Not interested in this strange girl you leave her alone."
            $ pytfall.world_quests.get("Treasure Seeker").finish_in_label("You ignored the strange girl.")
            $ pytfall.world_events.kill_event("show_nami_looking")
            jump city_beach_right

label nami_personality_event():
    
        "You spent a large portion of your day following the girl, you discover that she is really obsessed with money and finding treasures"
        "Given her fondness for money you think that it might be possible to convince her to come work for you as one of your whores"
        $ hero.ap = 0
        
        menu:
            "Approach her":
                jump nami_treasure_seeker
            "Leave the little gold digger alone":
                "Deciding that having someone who is overly obsessed with money work for you would be troublesome you leave her alone."
                $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You leave the little treasure seeker alone for now")
                $ pytfall.world_events.kill_event("show_nami_looking")
                jump nami_add_slave_path_event
                


label nami_treasure_seeker:
    define f1 = Character("Nami", color=orange, what_color=orange, show_two_window=True, image="nami_face_wondering")
    define f2 = Character("Nami", color=orange, what_color=orange, show_two_window=True, image="nami_face_excited")
    
        # Nami has some face pictures but no idea how to add them to the Character.
    
    show nami_approach #image is too large for screen, should be made to fit?
        
    hero.say "Hi I couldn't help but notice you."
    f1 "Hello."
    hero.say "This is perhaps a bit sudden and presumptuous but I would like to talk to you about an opportunity to earn some cash."
    f1 "Uhm... I wouldn't mind, but your not some kind of treasure seeker are you?"
    
    menu:
        "Confess that your a treasure seeker":
            "You notice Nami's face turning dark"
            f1 "Don't take this personal but I really don't like competition."
            f1 "PERVERT!"
            f1 "PERVERT!!" 
            f1 "Don't let him get away!!!"
            
            if hero.reputation > 75:        #should be replaced by fame/reputation statement.
                "By using your fame and reputation you mange to calm the crowd."
                "Unfortunately you are still made to leave the beach"
                $ hero.take_ap(1)
                jump nami_add_slave_path_event
            else:
                "You see no other option, and start to run away."
                $ hero.take_ap(3)
                jump nami_add_slave_path_event
            
            $ pytfall.world_events.kill_event("show_nami_looking")
            $ pytfall.world_quests.get("Treasure Seeker").next_in_label("Mistakenly believing your a treasure hunter she doesn't want to talk to you any more.")
                
        "Nope, just a business owner":
            f1 "Aaah, that's good. It's just that I really can't stand people trying to find treasures in my territory."
            jump nami_convincing_event

    
label nami_convincing_event:
    $ loop = True
    
    hero.say "As I was saying I'm a business owner. If you are interested in earning some serious money regardless of what you have to do you have what it takes to become one of my employees?"
    f1 "Oh, I don't know. I'm quite flexible when it come to earning money but still there are something a girl shouldn't do, so kind Sir what kind of business are you running?"
    
    hero.say "Nothing special, its just something where an flexible young woman is always welcome."
    hero.say "The pay is exceptionally good, although some people may find it a bit immoral."
    
    if hero.fame > 75:  #replace again with fame/reputation
        f1 "Oh, something dirty comes to mind. But it can't be that you're running a brothel?"
        f1 "Offering my body to lecherous men to use, I'm not sure that I could do such work."
        f1 "Uhm... Perhaps if they were rich?"
        "You have the impression that this girl would be willing to work for you for the right kind of money."
        while loop:
            menu:
                "Starting fee:   500 Gold, 100 Gold upkeep":
                    f1 "It's a bit low don't you think, can't let my body be used by men for such a pitiable amount"
                    
                "Starting fee:  2500 Gold, 100 Gold upkeep":
                    f1 "It's a bit low don't you think, can't let my body be used by men for such a pitiable amount"
                    
                "Starting fee:  5000 Gold, 100 Gold upkeep":
                    f1 "It's a bit low don't you think, can't let my body be used by men for such a pitiable amount"
                    
                "Starting fee: 10000 Gold, 100 Gold upkeep"  if hero.gold >= 10000:
                    f2 "Ooh that's some serious cash."
                    $ loop = False
                    $ hero.take_money(10000, reason="Other")
                    $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You spend 10 000 gold on her.")
                    jump nami_excited_event
                    
                "Starting fee: 25000 Gold, 100 Gold upkeep"  if hero.gold >= 25000:
                    f2 "Ooh that's some serious cash."
                    $ loop = False
                    $ hero.take_money(25000, reason="Other")
                    $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You spend 25 000 gold on her.")
                    jump nami_excited_event
                    
                "Starting fee: 50000 Gold, 100 Gold upkeep"  if hero.gold >= 50000:
                    f2 "Ooh that's some serious cash."
                    $ loop = False
                    $ hero.take_money(50000, reason="Other")
                    $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You spend 50 000 gold on her.")
                    jump nami_excited_event
                    
                "I'm low on cash, will catch you another time":
                   $ loop = False;
                   $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You didn't make her an good enough offer, perhaps there is another way.")
                   jump nami_add_slave_path_event
            
    else:
        f1 "Oh, I'm pretty familiar with most business owners."
        f1 "And I sure as hell don't recall you being one of the more successful business owners."
        f1 "Don't think I'm some stupid broad who will fall from some empty talk about serious money."
        $ pytfall.world_events.kill_event("show_nami_looking")
        $ pytfall.world_quests.get("Treasure Seeker").next_in_label("She doesn't believe your a successful business owner, probably because your fame is too low")
        jump nami_add_slave_path_event
        
label nami_excited_event:
    f2 "Uhm..."
    hide nami_approach
    show nami_beach_undressing
    f2 "I'm feeling a bit..., its the money I gets me ..."
    f2 "Perhaps you help me and check if I'm up for the task?"
    "You find it a bit odd that this girl is making such lewd remarks. But seeing how excited Nami is right now you see no reason to object."
    hide nami_beach_undressing
    show nami_beach_ready
    "Before you know it she is lying naked in the middle of the beach ready to be fucked."
    "Your starting to feel a bit uneasy. How come this young woman right now is behaving exactly like an easy beach whore"
    hide nami_beach_ready
    show nami_beach_sex
    "Realizing you have been played, you angrily start to fuck her hard."
    hide nami_beach_sex
    show nami_beach_sex_treasure
    "Despite fucking her hard, you notice she is quite obviously fantasying about something else. Not really enjoying the pounding you are giving her."
    "You could make this pleasurable for the both of you."
    
    menu:
        "Whisper in her ears about money and gold":
            "Slowly she starts to moan, telling her about the fantastic treasures you own, you feel her excitement grow."
            "About ready to cum, you want to make her cum as well. Enlightened by a flash of inspiration you whisper into her ear, that you wish to shove a fist sized diamond up her cunt."
            "All of a sudden she tightens, feeling powerful muscles grip your dick you orgasm. Blasting jets of cum into her gold-digging cunt."
            
            hide nami_beach_sex_treasure
            show nami_beach_sex_happy
            #hero.sex? + something.
            
        "You don't care":
            "You increase your pace even more. It's starting to hurt her but you don't care. Finally you cum, filling her gold-digging cunt with your cum."
            hide nami_beach_sex_treasure
            show nami_beach_sex_forced
    
    "Besides being angry that she had tricked you, you realize that without a large amount of gold she is an incredible boring fuck. Given the salary and her hiring fee its unlikely you will ever see a return on your investment. What will you do with her?"
    
    menu: 
        "Fire her":
            hero.say "Crap, I can't believe I was tricked like that. Don't bother showing up, your fired"
            $ pytfall.world_events.kill_event("show_nami_looking")
            $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You fired her, if only there was some way to get some revenge.")
            jump nami_add_slave_path_event
        "Keep her":
            hero.say "Dammit, little trickster you better be there to tomorrow. No way I'm going to let you get away, I'll work you till your an old bag of bones."
            #Add code to add nami to your girls list.
            #With a salary of 100g and a pretty low tumble price (10 <-> 25 g or so?)
            $ pytfall.world_events.kill_event("show_nami_looking")
            $ pytfall.world_quests.get("Treasure Seeker").finish_in_label("You decide to hire her, despite her obvious flaws.")

label nami_add_slave_path_event:
        #works, doesn't always show up because u can only have one event per map per visit???
        $ register_event_in_label("start_nami_pitfall", screen=True, locations=["forest_entrance"], trigger_type="auto", restore_priority=1, priority=300, start_day=day, jump=True, dice=100, max_runs=100)
        jump city_beach_right  # return to beach where nami was discovered
        
        
        #Its probably best to replace this with some code which will add it as a random option to the look around choice in the forest. As the text is more or less written for it.
        #For not this is just a place holder so you can start the with the 'profitable' ending. 
screen start_nami_pitfall:
    zorder 10
    if renpy.get_screen("pyt_forest_entrance"):
        $ img = Transform("nami_looking", zoom=1)  
        imagebutton:
            pos (400, 440) #was 400
            idle Transform("nami_looking", zoom=1) 
            hover Transform("nami_looking", zoom=1)
            action Jump("nami_discovered_pitfall")
    else:
        timer 0.01 action Hide("start_nami_pitfall")
        
label nami_discovered_pitfall:
        show pitfall
        "Strolling through the forest in the hope of finding something interesting you happen to come across an square whole in the ground."
        "Wondering why someone would dig such an odd looking hole in the middle of nowhere, you suddenly hear a dog whining. Carefully looking over the edge into the whole you notice a dog next to a particularly large bone."
        "Ha ha, someone made a mighty big trap just to catch a stray dog."
        "It's a pity something like that can't be used to catch me some slaves. Uh... Wait a sec, that greedy bitch would definitely be too distracted to notice it."
        hide pitfall
        show pitfall_idea
        "Surely that will work to capture that treasure seeking bitch, although it will take a bit of time and effort."
        
        menu: 
            "Prepare to capture Nami (will require {color=[gold]}5000 Gold{/color})":
                "Having decided to build a pitfall trap to capture Nami you now need acquire enough gold and find a suitable location."
                "A secluded spot on the beach where you first met her would be ideal."
                $ pytfall.world_events.kill_event("start_nami_pitfall")
                $ pytfall.world_quests.get("Treasure Seeker").next_in_label("Having a good idea how you can capture Nami, you now need to find a suitable location. (on the beach were you met her first)")
                jump nami_add_capture_location_event
            "She's not worth the effort.":
                $ pytfall.world_events.kill_event("start_nami_pitfall")
                $ pytfall.world_quests.get("Treasure Seeker").finish_in_label("You decide to hire her, despite her obvious flaws.")
                jump forest_entrance
            
label nami_add_capture_location_event:

        $ register_event_in_label("nami_capture_event", screen=False, locations=["city_beach_right"], trigger_type="auto", restore_priority=1, priority=300, start_day=day, jump=True, dice=100, max_runs=100)
        jump forest_entrance  # return to beach where nami was discovered
        
label nami_capture_event:
        show beach_cave
        "Walking on the beach, you discover a cave hidden from direct view. This location seems perfect to dig a pitfall trap and capture Nami."
        "Do you start digging?"
        
        menu: 
            "No, I made other plans":
                "Today is really bad for me. Lets do it tomorrow."
                $ pytfall.world_events.kill_event("nami_capture_event")
                
            "Yes, Dig the trap and leave a money trail. (invest 5500 gold)" if hero.gold > 5500:
                "Realizing the cave is really well hidden you spend 500 gold leaving a trail towards it. Piling up the rest of the 5500 gold you invested behind the pitfall."
                "After hiding behind the gold you piled up for a while you see Nami walking into the cave carrying a heavy sack full with gold coins. (yours probably)"
                "Almost tossing away the sack of gold coins you see an ecstatic Nami rushing towards you."
                "CRASH"  #play the sound of someone crashing into a pit?
                "Filled with joy you leave your hiding place to take a look at your prey"
                "Carefully looking over the edge you see Nami, slowly getting up."
                f1 "You, You dirty treasure thief. Trying to take what's is mine."
                "Crap, you notice Nami going berserk. With strength far surpassing her limits she jumps out of your pitfall trap."
                "Seeing Nami, come at you with berserker rage your only choice is to fight her now."
                jump nami_battle_event
                
            "Yes, Dig the trap. (invest 5000 gold)" if hero.gold > 5000: 
                "You wait the whole day patiently for Nami to show up."
                "As it begins to get dark you feel the water rising. In you hurry to leave before the cave is flooded you only manage to retrieved 4378 gold."
                $ pytfall.world_events.kill_event("nami_capture_event")
                $ hero.take_ap(3) #should be all ap.
                # hero.gold = hero.gold - 622 #reduce the gold not recovered.
                jump city_beach_right
            
            
label nami_battle_event:
        "Your battle with Nami starts"  #Setup fight....
        # hero.gold = hero.gold - 1472 #reduce the gold not recovered.
        jump city_beach_right