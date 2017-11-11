init -1 python:
    if config.debug:
        register_event("meet_beggar_event", locations=["city_parkgates"], priority=1, restore_priority=8, dice=100, max_runs=7)
    else:
        register_event("meet_beggar_event", locations=["city_parkgates"], priority=1, restore_priority=8, dice=25, max_runs=7)

label meet_beggar_event(event):

    $ beggar = npcs["beggar"].say

    'You see a girl who comes close to you.'
    show expression npcs["beggar"].show("indifferent", resize=(600, 700)) as npc
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
                show expression npcs["beggar"].show("happy", resize=(600, 700)) as npc
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
