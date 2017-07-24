init -1 python:
    register_event("found_sad_cat_1", locations=["main_street"], run_conditions=["dice(100)"], priority=5000, dice=0, start_day=1, restore_priority=0, jump=True)

label found_sad_cat_1:
    hide screen main_street
    scene bg street_alley
    $ temp = npcs["sad_cat"].show("profile", "tired", resize = (295, 340))
    show expression temp at left
    with dissolve
    hero.say "Oh. There is a cat in that narrow alley. It looks exhausted."
    menu:
        "Pet it":
            hide temp
            $ temp = npcs["sad_cat"].show("profile", "scared", resize = (295, 340))
            show expression temp at left
            "The cat is frightened as you approach, and quickly runs away."
            hide expression temp with dissolve
            hero.say "Maybe a treat of some kind will help? I suppose cats like fish..."
            $ pytfall.world_events.kill_event("found_sad_cat_1")
            $ register_event_in_label("found_sad_cat_2", locations=["main_street"], run_conditions=["dice(100)"], priority=5000, dice=0, start_day=1, restore_priority=0, jump=True)
        "Ignore it":
            "There are plenty of cats in the city. No need to pay any attention."
        "Drive it away":
            hide temp
            $ temp = npcs["sad_cat"].show("profile", "scared", resize = (295, 340))
            show expression temp at left
            "The cat is frightened as you approach, and quickly runs away."
            $ pytfall.world_events.kill_event("found_sad_cat_1")
    $ global_flags.set_flag("keep_playing_music")
    jump main_street
    
label found_sad_cat_2:
    hide screen main_street
    scene bg street_alley
    $ temp = npcs["sad_cat"].show("profile", "tired", resize = (295, 340))
    show expression temp at left
    with dissolve
    $ fish = list(i for i in hero.inventory if i.type == "fish" and i.price >= 3)
    if not(fish):
        hero.say "This cat again. Sorry, I have nothing for you."
    else:
        hero.say "This cat again. I have some fish, maybe it will like it?"
        menu:
            "Give some fish to the cat":
                hide temp
                $ temp = npcs["sad_cat"].show("profile", "indifferent", resize = (295, 340))
                show expression temp at left
                "The cat snatches the fish from your hands and runs away."
                hide temp with dissolve
                hero.say "What an ungrateful animal..."
                $ hero.remove_item(random.choice(fish).id)
                $ pytfall.world_events.kill_event("found_sad_cat_2")
                $ register_event_in_label("found_sad_cat_3", locations=["main_street"], run_conditions=["dice(100)"], priority=5000, dice=0, start_day=1, restore_priority=0, jump=True)
            "Maybe later":
                hero.say "I have a more important business to attend right now."
                hide temp with dissolve
            "Drive it away":
                hide temp
                $ temp = npcs["sad_cat"].show("profile", "scared", resize = (295, 340))
                show expression temp at left
                "The cat is frightened as you approach, and quickly runs away."
                $ pytfall.world_events.kill_event("found_sad_cat_2")
    $ global_flags.set_flag("keep_playing_music")
    jump main_street
    
label found_sad_cat_3:
    hide screen main_street
    scene bg street_alley
    $ temp = npcs["sad_cat"].show("profile", "tired", resize = (295, 340))
    show expression temp at left
    with dissolve
    $ fish = list(i for i in hero.inventory if i.type == "fish" and i.price >= 3)
    if not(fish):
        hero.say "This cat again. Sorry, I have nothing for you."
    else:
        hero.say "This cat again. I have some fish too."
        menu:
            "Give some fish to the cat":
                hide temp
                $ temp = npcs["sad_cat"].show("profile", "confident", resize = (295, 340))
                show expression temp at left
                "The cat cautiously approaches and sniffs you, then snatches the fish and runs away."
                hide temp with dissolve
                hero.say "It wasn't as frightened today... I guess."
                $ hero.remove_item(random.choice(fish).id)
                $ pytfall.world_events.kill_event("found_sad_cat_3")
                $ register_event_in_label("found_sad_cat_4", locations=["main_street"], run_conditions=["dice(100)"], priority=5000, dice=0, start_day=1, restore_priority=0, jump=True)
            "Maybe later":
                hero.say "I have a more important business to attend right now."
                hide temp with dissolve
            "Drive it away":
                hide temp
                $ temp = npcs["sad_cat"].show("profile", "scared", resize = (295, 340))
                show expression temp at left
                "The cat is frightened as you approach, and quickly runs away."
                $ pytfall.world_events.kill_event("found_sad_cat_3")
    $ global_flags.set_flag("keep_playing_music")
    jump main_street
            
label found_sad_cat_4:
    hide screen main_street
    scene bg street_alley
    $ temp = npcs["sad_cat"].show("profile", "tired", resize = (295, 340))
    show expression temp at left
    with dissolve
    $ fish = list(i for i in hero.inventory if i.type == "fish" and i.price >= 3)
    if not(fish):
        hero.say "This cat again. Sorry, I have nothing for you."
    else:
        hero.say "This cat again. I bet it won't refuse more fish."
        menu:
            "Give some fish to the cat":
                hide temp
                $ temp = npcs["sad_cat"].show("profile", "indifferent", resize = (295, 340))
                show expression temp at left
                "The cat approaches and sniffs you, then takes the fish and goes away."
                hide temp with dissolve
                hero.say "It doesn't fear me as much as before. Maybe I could pet it the next time."
                $ hero.remove_item(random.choice(fish).id)
                $ pytfall.world_events.kill_event("found_sad_cat_4")
                # $ register_event_in_label("found_sad_cat_5", locations=["main_street"], run_conditions=["dice(100)"], priority=5000, dice=0, start_day=1, restore_priority=0, jump=True)
            "Maybe later":
                hero.say "I have a more important business to attend right now."
                hide temp with dissolve
            "Drive it away":
                hide temp
                $ temp = npcs["sad_cat"].show("profile", "scared", resize = (295, 340))
                show expression temp at left
                "The cat is frightened as you approach, and quickly runs away."
                $ pytfall.world_events.kill_event("found_sad_cat_4")
    $ global_flags.set_flag("keep_playing_music")
    jump main_street