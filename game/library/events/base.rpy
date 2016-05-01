# Events File

init -1 python:
    if config.debug:
        register_event("meet_beggar_event", locations=["city_parkgates"], priority=1, restore_priority=8, dice=100, max_runs=7)
    else:
        register_event("meet_beggar_event", locations=["city_parkgates"], priority=1, restore_priority=8, dice=25, max_runs=7)
    register_event("simple_beach_event", locations=["city_beach", "city_beach_left", "city_beach_right"], restore_priority=1, dice=50, max_runs=50)
    register_event("creatures_beach_event", locations=["city_beach_right"], restore_priority=2, dice=40, max_runs=3)
    register_event("found_money_event", locations=["all"], run_conditions=["dice(max(5, int(hero.luck/5)))"], priority=50, dice=0, restore_priority=0)
    register_event("found_item_event", locations=["all"], run_conditions=["dice(max(3, int(hero.luck/6)))"], priority=50, dice=0, restore_priority=0)

   
label meet_beggar_event(event):

    $ beggar = Character('Beggar', color="#c8ffc8", show_two_window=True)

    'You see a girl who comes close to you.'
    show npc beggar_girl_novel
    with dissolve
    
    $ beggar(choice(['Hello, mister! Please, could you spare some coin for hungry beggar?',
                                'Hello, mister! Please, could you spare some coin?',
                                'Hi! Could you buy me something?',
                                'Please, could you spare some coin for hungry beggar?']))

    menu:
        'WTF? Who are you?':
            python:
                random_place = choice([u'library', u'tailor store', u'cafe', u'world peace', u'my sweet home'])
                for steal_amount in [5000, 500, 100, 50, 25, 5]:
                    if hero.take_money(steal_amount, reason="Theft"):
                        break
            beggar 'Oh, I`m just searching my way to [random_place]! I guess it`s there? Thank you, have a nice day!'
            "Somehow your pockets feel a bit lighter..."
            
        'Go buy some food. (-5 gold)':
            if hero.take_money(5, reason="Charity"):
                show npc beggar_girl_smile_novel
                with dissolve
                beggar 'Thanks! ^_^'
            else:
                beggar 'Empty pockets? Too bad. :`('
        'NO!':
            $ beggar(choice(["You're a meanie! >:-(",
                                        "That's too bad...",
                                        "And you looked so promising..."]))

    hide npc
    with dissolve

    return
    

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
    
label found_money_event(event):
    python:
        amount = randint(10, 100) + hero.level*2 + max(10, hero.luck*4)
        renpy.show("_tag", what=Text("%d"%amount, style="back_serpent", color=gold, size=40, bold=True), at_list=[found_cash(150, 600, 4)])
        hero.say(choice(["Yey! Some money!", "Free Gold, lucky!", "I will not let this go to waste!"]))
        hero.add_money(amount, "Events")
    return
     
label found_item_event(event):
    python:
        # amount = max(200, (randint(10, 100) + hero.level*2 + max(10, hero.luck*4)))
        items_pool = list(item for item in items.values() if "Look around" in item.locations)
        found_item = choice(items_pool)
        renpy.show("_tag", what=ProportionalScale(found_item.icon, 100, 100), at_list=[found_cash(150, 600, 4)])
        hero.say(choice(["Yey! Found something! ([found_item.id])", "[found_item.id] Might be useful!", "[found_item.id]! Lucky?", "-[found_item.id]- Never look a gift horse in the mouth :)"]))
        hero.inventory.append(found_item)
    return
        
