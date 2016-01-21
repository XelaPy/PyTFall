init python:
    renpy.image("nami_looking", animate("/library/events/moneybitch_event/img/nami_looking", loop=True))
    
    # # Unsure about copyright etc. Perhaps necessarily to remove images.
     
    renpy.image("pitfall_idea", "library/events/moneybitch_event/img/pitfall_idea.png") # http://sakuramo-chi.deviantart.com/art/Sticking-pitfall-245601225
    renpy.image("pitfall", "library/events/moneybitch_event/img/pitfall.png") # http://dlminecraft.net/hungry-animals-mod/
    renpy.image("beach_cave", "library/events/moneybitch_event/img/beach_cave.jpg") # http://www.mobiletoones.com/browse/free-mobile-wallpapers/s43-nature-wallpapers/f68762-beach-cave.html
     
    # # used in composite image.
    # # renpy.image("pitfall", "library/events/moneybitch_event/img/chest-clipart-vector-88534402.jpg")  # http://www.clipartpanda.com/categories/treasure-chest-clipart
    renpy.image("nami_beach_sex_treasure", "library/events/moneybitch_event/img/nami_treasure_thoughts.png")
  
    # Since this quest has some content which isn't save for work its perhaps better to add a tag for it??
    register_quest("Treasure Seeker")
    if config.developer:
        register_event("show_nami_looking", screen=True, quest="Treasure Seeker", locations=["city_beach_right"], trigger_type="auto", restore_priority=1, priority=300, start_day=1, jump=True, dice=100, max_runs=20)
    else:
        register_event("show_nami_looking", screen=True, quest="Treasure Seeker", locations=["city_beach_right"], trigger_type="auto", restore_priority=1, priority=300, start_day=choice([15, 25, 35]), jump=True, dice=65, max_runs=20)
    
    # Dev Note: I've added screen attribute to WorldEvent class so the useless labels below are no longer required.
    # This doesn't change much for this event but in other places it will mean a much smoother gameplay.
    
screen show_nami_looking():
    zorder 10
    if renpy.get_screen("city_beach_right"):
        imagebutton:
            pos (800, 440)
            idle Transform("nami_looking", zoom=1) 
            hover Transform("nami_looking", zoom=1.1, alpha=1.1)
            action Jump("nami_discover_event")
    else:
        timer 0.01 action Hide("show_nami_looking")
        

label nami_discover_event:
    hide screen city_beach_right
    with dissolve
    "Walking on the beach enjoying the sight of many hot girls, you notice a very peculiar behaviour from one of them."
    
    menu:
        "Follow her.":
            jump nami_personality_event
        "Your time is too precious...":
            "Not interested in this strange girl you leave her alone."
            $ pytfall.world_quests.get("Treasure Seeker").finish_in_label("You ignored the strange girl.")
            $ pytfall.world_events.kill_event("show_nami_looking")
            jump city_beach_right

label nami_personality_event():
    
        "You spent a large portion of your day following the girl, you discover that she is obsessed with money and treasure hunting."
        "Given her fondness for money you think that it might be possible to convince her to work for you."
        $ hero.take_ap(1)
        
        menu:
            "Approach her":
                jump nami_treasure_seeker
            "Leave the little gold digger alone":
                # "Deciding that having someone who is overly obsessed with money work for you would be troublesome you leave her alone."
                "Well... that is as for as it goes..."
                $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You leave the little treasure seeker alone for now")
                $ pytfall.world_events.kill_event("show_nami_looking")
                jump nami_add_slave_path_event
                

label nami_treasure_seeker:
    $ nami = chars["Nami"]
    
    show expression nami.get_vnsprite() as nami_sprite with dissolve
    hero.say "Hi! I couldn't help but notice you."
    nami.say "Hello."
    hero.say "This is perhaps a bit sudden and presumptuous but I would like to talk to you about an opportunity to earn some cash."
    nami.say "Uhm... I wouldn't mind, but your not some kind of treasure seeker are you?"
    
    menu:
        "Claim that your a treasure seeker":
            # "You notice Nami's face turning dark"
            $ nami.override_portrait("portrait", "angry")
            nami.say "Don't take this personal but I really don't like competition."
            nami.say "PERVERT!"
            nami.say "PERVERT!!" 
            nami.say "Don't let him get away!!!"
            $ nami.restore_portrait()
            
            if hero.reputation > 75: # should be replaced by fame/reputation statement.
                "By using your fame and reputation you mange to calm the crowd."
                "Unfortunately you are still made to leave the beach."
                $ hero.take_ap(1)
                jump nami_add_slave_path_event
            else:
                "You see no other option and quickly withdraw."
                $ hero.take_ap(2)
                jump nami_add_slave_path_event
            
            $ pytfall.world_events.kill_event("show_nami_looking")
            $ pytfall.world_quests.get("Treasure Seeker").next_in_label("Believing that you're a treasure hunter she doesn't want to talk to you any more.")
                
        "Nope, just a business owner":
            $ nami.override_portrait("portrait", "happy")
            nami.say "Aaah, that's good. Competition should really stay the hell away from me or they'd be sorry!"
            $ nami.restore_portrait()
            jump nami_convincing_event

    
label nami_convincing_event:
    $ loop = True
    
    hero.say "As I was saying I'm a business owner. If you are interested in earning some serious money regardless of what you have to do you have what it takes to become one of my employees?"
    nami.say "Oh, I don't know. I'm quite flexible when it come to earning money but still there are something a girl shouldn't do, so what kind of business are you running?"
    
    hero.say "Nothing special, its just something where an flexible young woman is always welcome."
    hero.say "The pay is exceptionally good, although some people may find it a bit immoral."
    
    if hero.fame > 75:  # Replace again with fame/reputation
        nami.say "Oh, something dirty comes to mind. But it can't be that you're running a brothel?"
        nami.say "Offering my body to lecherous men to use, I'm not sure that I could do such work."
        nami.say "Uhm... Perhaps if they were rich?"
        "You have the impression that this girl would be willing to work for you for the right kind of money."
        while loop:
            menu:
                "Upfront fee: 500 Gold":
                    nami.say "It's a bit low don't you think, can't let my body be used by men for such a pitiable amount"
                    
                "Upfront fee: 2500 Gold":
                    nami.say "It's a bit low don't you think, can't let my body be used by men for such a pitiable amount"
                    
                "Upfront fee: 5000 Gold":
                    nami.say "It's a bit low don't you think, can't let my body be used by men for such a pitiable amount"
                    
                "Upfront fee: 10000 Gold"  if hero.gold >= 10000:
                    nami.say "Ooh that's some serious cash."
                    $ loop = False
                    $ hero.take_money(10000, reason="Other")
                    $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You spend 10 000 gold on her.")
                    jump nami_excited_event
                    
                "Upfront fee: 25000 Gold"  if hero.gold >= 25000:
                    nami.say "Ooh that's some serious cash."
                    $ loop = False
                    $ hero.take_money(25000, reason="Other")
                    $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You spend 25 000 gold on her.")
                    jump nami_excited_event
                    
                "Upfront fee: 50000 Gold"  if hero.gold >= 50000:
                    nami.say "Ooh that's some serious cash."
                    $ loop = False
                    $ hero.take_money(50000, reason="Other")
                    $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You spend 50 000 gold on her.")
                    jump nami_excited_event
                    
                "I'm low on cash, will catch you another time":
                   $ loop = False;
                   $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You didn't make her an good enough offer, perhaps there is another way.")
                   jump nami_add_slave_path_event
            
    else:
        nami.say "Oh, I'm pretty familiar with most business owners."
        nami.say "And I sure as hell don't recall you being one of the more successful business owners."
        nami.say "Don't think I'm some stupid broad who will fall from some empty talk about serious money."
        $ pytfall.world_events.kill_event("show_nami_looking")
        $ pytfall.world_quests.get("Treasure Seeker").next_in_label("She doesn't believe your a successful business owner, probably because your fame is too low")
        jump nami_add_slave_path_event
        
label nami_excited_event:
    nami.say "Uhm..."
    hide nami_sprite
    show expression nami.show("nude", "beach", "suggestive", "girlmeets", resize=(800, 600)) at truecenter as xxx with dissolve
    nami.say "I'm feeling a bit... all this cash is making me uhh ..."
    nami.say "Perhaps you help me and check if I'm up for the task?"
    "You find it a bit odd that this girl is making such lewd remarks. But seeing how excited Nami is right now you see no reason to object."
    hide xxx with dissolve
    
    show expression nami.show("nude", "stripping", "simple bg", "happy", "revealing", resize=(800, 600)) at truecenter as xxx with dissolve
    "Before you know it she is lying naked in the middle of the beach ready to be fucked."
    "Your starting to feel a bit uneasy. How come this young woman right now is behaving exactly like an easy beach whore."
    hide xxx with dissolve
    
    show expression nami.show("sex", "partnerhidden", "ecstatic", "straight", "2c vaginal", "normalsex", "onside", "outdoors", "swimsuit", resize=(800, 600)) at truecenter as xxx with dissolve
    "Realizing you have been played, you angrily start to fuck her hard."
    
    "Despite fucking her hard, you notice she is not all that into it. Not really enjoying the pounding you are giving her."
    "You could make this pleasurable for the both of you."
    
    menu:
        "Whisper in her ears about money and gold":
            "Slowly she starts to moan, telling her about the fantastic treasures you own, you feel her excitement grow."
            "About ready to cum, you want to make her cum as well. Enlightened by a flash of inspiration you whisper into her ear, that you wish to shove a fist sized diamond up her cunt."
            "All of a sudden she tightens, feeling powerful muscles grip your dick you orgasm. Blasting jets of cum into her gold-digging cunt."
            hide xxx with dissolve
            show expression nami.show("sex", "partnerhidden", "ecstatic", "straight", "2c vaginal", "normalsex", "onside", "outdoors", "swimsuit", resize=(800, 600)) at truecenter as xxx with dissolve
            
        "You don't care":
            "You increase your pace even more. It's starting to hurt her but you don't care. Finally you cum, filling her gold-digging cunt with your cum."
            hide xxx with dissolve
            show expression nami.show("sex", "outdoor", "2c vaginal", "normalsex", "partnerhidden", "missionary", "ecstatic", "nature", resize=(800, 600)) at truecenter as xxx with dissolve
            
    $ hero.vaginal += 1
    "Besides being angry that she had tricked you, you realize that without a large amount of gold she is an incredible boring fuck. Given the salary and her hiring fee its unlikely you will ever see a return on your investment. What will you do with her?"
    hide xxx with dissolve
    
    menu:
        "Fire her":
            hero.say "Don't bother showing up, your fired..."
            $ pytfall.world_events.kill_event("show_nami_looking")
            $ pytfall.world_quests.get("Treasure Seeker").next_in_label("You fired her, if only there was some way to get some revenge.")
            jump nami_add_slave_path_event
        "Keep her":
            hero.say "Dammit, little trickster you better be there to tomorrow. No way I'm going to let you get away, I'll work you till your an old bag of bones."
            # Add code to add nami to your girls list.
            # With a salary of 100g and a pretty low tumble price (10 <-> 25 g or so?)
            $ pytfall.world_events.kill_event("show_nami_looking")
            $ pytfall.world_quests.get("Treasure Seeker").finish_in_label("You decide to hire her, despite her obvious flaws.")

label nami_add_slave_path_event:
        # Works, doesn't always show up because u can only have one event per map per visit???
        $ register_event_in_label("start_nami_pitfall", screen=True, locations=["forest_entrance"], trigger_type="auto", restore_priority=1, priority=300, start_day=day, jump=True, dice=100, max_runs=100)
        jump city_beach_right  # return to beach where nami was discovered.
        # Its probably best to replace this with some code which will add it as a random option to the look around choice in the forest. As the text is more or less written for it.
        # For not this is just a place holder so you can start the with the 'profitable' ending. 
        
screen start_nami_pitfall():
    zorder 10
    if renpy.get_screen("forest_entrance"):
        imagebutton:
            pos (400, 440)
            idle Transform("nami_looking", zoom=1) 
            hover Transform("nami_looking", zoom=1.1, alpha=1.1)
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
                nami.say "You, You dirty treasure thief. Trying to take what's is mine."
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