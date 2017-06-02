init python:
    
    # Add quest
    # Alex: We've changed manual to True to be used as a default setting for all quests.
    q = register_quest("Strange Idol", manual=None)
    
    # Add first event
    # q.condition(stage, strict, *flags) allows for run conditions based on the current status of the quest
    # stage=What stage the quest is at
    # strict=Whether to check == or >= for the stage
    # flags=Flags to check for as well 
    #
    # (Yes, setting dice to 100 would have worked as well, but I wanted to show off the condition function)
    register_event("strange_idol1", quest="Strange Idol", locations=["main_street"], dice=None, run_conditions=[q.condition(0, True)], max_runs=1)
    

label strange_idol1(event):
    hero.say "Huh?"
    "You bend down to pick something up off the floor."
    $ pytfall.world_quests.get(event.quest).next_in_label("You found a piece of an idol! How strange.", "piece1") # Can access the quest straight in the event.
    hero.say "Its... part of a statue?"
    "You try to place the piece aside, but after fighting against your impulses you decide to take it with you."
    # Advance quest
    # q.next(prompt, *flags, to=None) moves the quest forwards
    # prompt=The prompt to add to the quest log. Set to None for no addition
    # flags=Flags to add to the quest, used for more complex monitoring then just a number
    # to=The stage to jump to. If left as None adds 1 to the current stage
    # Remove event
    $ pytfall.world_events.kill_event("strange_idol1")
    
    # Create second part of quest
    $ register_event_in_label("strange_idol2", quest=event.quest, locations=["main_street"], dice=100, max_runs=2, restore_priority=1)
    
    return

label strange_idol2(event):
    hero.say "Huh?"
    "You bend down to pick something up off the floor."
    
    python:
        # Use in syntax for easy flag checking
        if "piece2" in pytfall.world_quests.get(event.quest):
            pytfall.world_quests.get(event.quest).next_in_label("You found another piece of the idol! I think its complete.", "piece3")
            
            # Remove event
            pytfall.world_events.kill_event("strange_idol2")
            
            # Create third part of quest
            register_event_in_label("strange_idol3", quest=event.quest, locations=["mainscreen"], trigger_type="auto", dice=100, max_runs=1, start_day=day+1)
        
        else:
            pytfall.world_quests.get(event.quest).next_in_label("You found another piece of the idol! I wonder how many there are?", "piece2")
    hero.say "Its... another part of that statue!"
    "You take the piece with you, wondering how many there are."
    return

label strange_idol3(event):
    "As you wake you feel a strange sensation move through you, almost as if your very soul was being caressed."
    "Suddenly a bright flash makes you bolt out of bed, staring towards its source."
    # Use the finish command to end the quest. Works the same as next() (but no 'to' param)
    $ pytfall.world_quests.get(event.quest).finish_in_label("You completed the idol! It disappeared though.", "complete")
    "The place where you stored those pieces of the strange idol is slightly scorched, the pieces themselves no where to be found."
    "Worriedly you continue with your morning feeling... {i}better{/i}."
    

    
    # Remove event
    $ pytfall.world_events.kill_event("strange_idol3")
    
    # Improve sex?
    $ hero.sex += 10
    return
