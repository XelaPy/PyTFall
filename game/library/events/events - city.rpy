init python:
    register_event("city_events_thugs_robbery", locations=["main_street"], dice=100, trigger_type = "look_around", priority = 50, start_day=1, jump=True, times_per_days=(1,7))

label city_events_thugs_robbery:
    scene
    $ renpy.scene(layer="screens")
    show bg street_alley with dissolve
    "As you walking down the alley, a shady man approaches you."
    show expression npcs["street_thug"].get_vnsprite() as npc with dissolve
    $ t = npcs["street_thug"].say
    t "A word, my friend!"
    t "These streets are unsafe, if you know what I mean. But I can ensure your safety. 200 G per week. The price is pretty reasonable, right?"
    if hero.gold < 200:
        "Unfortunately, you don't have so much money."
        t "Hard times, eh... Well, there you go then."
        "He tosses you a few coins."
        t "My mother always told me to help those in need, heh. See ya."
        $ hero.gold += randint(10,50)
        hide npc with dissolve
    else:
        menu:
            "Give him 200 G?"
            "Yes":
                t "Thank you kindly. Worry not, no one will bother you. For now."
                $ pytfall.world_events.kill_event("city_events_thugs_robbery_attack")
                $ register_event("city_events_thugs_robbery", locations=["main_street"], dice=100, trigger_type = "look_around", priority = 50, start_day=day+7, jump=True, times_per_days=(1,3))
                $ hero.gold -= 200
            "No":
                t "It's your choice. Don't blame me if something will happen."
                $ register_event("city_events_thugs_robbery_attack", locations=["main_street"], dice=100, trigger_type = "look_around", priority = 1000, start_day=day+1, times_per_days=(1,2))
    "He walks away."
    jump main_street
            
label city_events_thugs_robbery_attack(event):
    $ scr = pytfall.world_events.get("city_events_thugs_robbery_attack").label_cache
    "A group of men suddenly surrounds you!"
    scene
    python:
        back = interactions_pick_background_for_fight(scr)
        your_team = Team(name="Your Team")
        for member in hero.team:
            your_team.add(member)
        for member in your_team:
            if member <> hero:
                if member.status == "slave":
                    member.controller = Slave_BE_AI(member)
        enemy_team = Team(name="Enemy Team", max_size=3)
        for i in xrange(3):
            mob = build_mob("Thug", level=1)
            enemy_team.add(mob)
        battle = BE_Core(Image(back), start_sfx=get_random_image_dissolve(1.5), music="random", end_sfx=dissolve, quotes=True)
        battle.teams.append(your_team)
        battle.teams.append(enemy_team)
        battle.start_battle()
        your_team.reset_controller()
        if battle.winner != your_team:
            hero.health = 0
        else:
            for member in your_team:
                member.exp += adjust_exp(member, 100)
                if member in battle.corpses:
                    member.health = 1
    scene expression "bg " + event.label_cache
    $ renpy.scene(layer="screens")
    "You found some gold in their pockets."
    $ hero.gold += randint(10,40)
    jump expression scr