# Events File

init -9 python:    
    register_event("simple_tavern_event", trigger_type="Stay", restore_priority=0, dice=100, max_runs=999999)
  

label simple_tavern_event(event):
    
    define n = Character(" ")
    
    python:
        img = get_random_event_image("simple_beach")
        renpy.show("event", what=img, at_list=[center])
        renpy.with_statement(dissolve)
        n(choice(["This looks like fun!", "Damn, don't you wish could join them...", "Fun on the beach :)", "Awesome!", "... speachless", "Cute!"]))
    return    
   
