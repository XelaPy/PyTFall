init python:
    register_event("city_events_thugs_robbery", locations=["main_street"], dice=100,
                    trigger_type = "look_around", priority=50, start_day=1,
                    jump=True, times_per_days=(1,7))

label city_events_thugs_robbery:
    scene
    $ renpy.scene(layer="screens")
    show bg street_alley with dissolve
    "As you walking down the alley, a shady man approaches you."
    show expression npcs["street_thug"].get_vnsprite() as npc with dissolve
    $ t = npcs["street_thug"].say
    t "A word, my friend!"
    t "These streets are unsafe if you know what I mean. But I can ensure your safety. 200 G per week. The price is pretty reasonable, right?"
    if hero.gold < 200:
        "Unfortunately, you don't have enough money."
        t "Hard times, eh... Well, there you go then."
        "He tosses you a few coins."
        t "My mother always told me to help those in need, heh. See ya."
        $ hero.add_money(randint(2, 5), reason="Charity")
        hide npc with dissolve
        jump main_street
    else:
        menu:
            "Give him 200 G?"
            "Yes":
                t "Thank you kindly. Worry not, no one will bother you. For now."
                $ pytfall.world_events.kill_event("city_events_thugs_robbery_attack")
                $ register_event("city_events_thugs_robbery", locations=["main_street"], dice=100, trigger_type = "look_around", priority = 50, start_day=day+7, jump=True, times_per_days=(1,3))
                $ hero.take_money(200, reason="Robbery")
                jump main_street
            "No":
                t "It's your choice. Don't blame me if something will happen."
                $ register_event("city_events_thugs_robbery_attack", locations=["main_street", "city_parkgates", "graveyard_town"], dice=100, trigger_type = "look_around", priority = 1000, start_day=day+1, times_per_days=(1,2), jump=True)
                jump main_street
            "Attack him":
                t "Oho, you have guts, I like it. Let's see what you can do against my boys!"
                python:
                    back = interactions_pick_background_for_fight("city")
                    enemy_team = Team(name="Enemy Team", max_size=3)
                    for i in xrange(3):
                        mob = build_mob("Thug", level=45)
                        enemy_team.add(mob)
                    result = run_default_be(enemy_team, slaves=True, background=back)
                    if result is True:
                        for member in hero.team:
                            member.exp += exp_reward(member, enemy_team)
                        renpy.jump("city_events_thugs_robbery_win")
                    else:
                        renpy.jump("city_events_thugs_robbery_lost")

label city_events_thugs_robbery_win:
    show bg street_alley
    show expression npcs["street_thug"].get_vnsprite() as npc with dissolve
    t "Nice moves! Fair enough, [hero.name]. My guys won't bother you any longer. See ya."
    $ pytfall.world_events.kill_event("city_events_thugs_robbery_attack")
    $ pytfall.world_events.kill_event("city_events_thugs_robbery")
    "He walks away."
    jump main_street

label city_events_thugs_robbery_lost:
    show bg street_alley
    show expression npcs["street_thug"].get_vnsprite() as npc with dissolve
    t "Huuh? That's it?!"
    if hero.gold > 0:
        t "I'm taking your gold to give you a lesson: don't start a battle you can't win, idiot."
    $ g = randint (500, 800)
    if hero.gold < g:
        $ hero.take_money(hero.gold, reason="Robbery")
    else:
        $ hero.take_money(g, reason="Robbery")
    "He walks away."
    jump main_street

label city_events_thugs_robbery_attack:
    $ scr = pytfall.world_events.get("city_events_thugs_robbery_attack").label_cache
    "A group of men suddenly surrounds you!"
    scene
    $ renpy.scene(layer="screens")
    python:
        back = interactions_pick_background_for_fight(scr)
        enemy_team = Team(name="Enemy Team", max_size=3)
        lvl = min(hero.level, 25)
        for i in xrange(3):
            mob = build_mob("Thug", level=lvl)
            enemy_team.add(mob)
        result = run_default_be(enemy_team, slaves=True, background=back)

        if result is True:
            for member in your_team:
                member.exp += exp_reward(member, enemy_team)
            renpy.jump("city_events_thugs_robbery_attack_win")
        else:
            g = min(hero.gold, randint (200, 400))
            hero.take_money(g, reason="Robbery")
            renpy.jump("city_events_thugs_robbery_attack_lost")

label city_events_thugs_robbery_attack_lost:
    scene expression "bg " + scr
    $ renpy.scene(layer="screens")
    "After beating you, they took some gold and disappeared before City Guards arrived."
    jump expression scr

label city_events_thugs_robbery_attack_win:
    scene expression "bg " + scr
    "You found some gold in their pockets before handing them over to the City Guards."
    $ hero.add_money(randint(10,40), reason="Events")
    jump expression scr
