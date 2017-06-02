init -1 python:
    register_event("simple_beach_event", locations=["city_beach", "city_beach_left", "city_beach_right"], restore_priority=1, dice=50, max_runs=50)
    register_event("creatures_beach_event", locations=["city_beach_right"], restore_priority=2, dice=40, max_runs=3)

label simple_beach_event(event):
    python:
        n = Character(" ")
        img = get_random_event_image("simple_beach")
        renpy.show("event", what=img, at_list=[center])
        renpy.with_statement(dissolve)
        n(choice(["This looks like fun!", "Damn, don't you wish could join them...", "Fun on the beach :)", "Awesome!", "... speachless", "Cute!"]))
    return

label creatures_beach_event(event):
    python:
        n = Character(" ")
        img = get_random_event_image("creatures_beach")
        renpy.show("event", what=img, at_list=[center])
        renpy.with_statement(dissolve)
        n(choice(["This looks like fun!", "Monster Girls are the best?", "What the hell?", "What are they called???"]))
    return
