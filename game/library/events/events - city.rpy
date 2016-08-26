init python:
    register_event("city_events_thugs_robbery", locations=["main_street"], dice=100, trigger_type = "look_around", priority=50, start_day=1, jump=True, times_per_days=(1,7))

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
                jump main_street
            "No":
                t "It's your choice. Don't blame me if something will happen."
                $ register_event("city_events_thugs_robbery_attack", locations=["main_street", "city_parkgates", "graveyard_town"], dice=100, trigger_type = "look_around", priority = 1000, start_day=day+1, times_per_days=(1,2), jump=True)
                jump main_street
            "Attack him":
                t "Oho, you have guts, I like it. Let's see what you can do against my boys!"
                python:
                    back = interactions_pick_background_for_fight("city")
                    your_team = Team(name="Your Team")
                    for member in hero.team:
                        your_team.add(member)
                    for member in your_team:
                        if member <> hero:
                            if member.status == "slave":
                                member.controller = Slave_BE_AI(member)
                    enemy_team = Team(name="Enemy Team", max_size=3)
                    for i in xrange(3):
                        mob = build_mob("Thug", level=45)
                        enemy_team.add(mob)
                    battle = BE_Core(Image(back), start_sfx=get_random_image_dissolve(1.5), music="random", end_sfx=dissolve, quotes=True)
                    battle.teams.append(your_team)
                    battle.teams.append(enemy_team)
                    battle.start_battle()
                    your_team.reset_controller()
                    if battle.winner != your_team:
                        for member in your_team:
                            if member in battle.corpses:
                                member.health = 1
                        renpy.jump("city_events_thugs_robbery_lost")
                    else:
                        for member in your_team:
                            member.exp += adjust_exp(member, 50)
                            if member in battle.corpses:
                                member.health = 1
                        renpy.jump("city_events_thugs_robbery_win")
label city_events_thugs_robbery_win:
    show bg street_alley
    show expression npcs["street_thug"].get_vnsprite() as npc with dissolve
    t "Nice moves! Fair enough, [hero.name], my guys won't bother you any longer. See ya."
    $ pytfall.world_events.kill_event("city_events_thugs_robbery_attack")
    $ pytfall.world_events.kill_event("city_events_thugs_robbery")
    "He walks away."
    jump main_street
label city_events_thugs_robbery_lost:
    show bg street_alley
    show expression npcs["street_thug"].get_vnsprite() as npc with dissolve
    t "Huuh? That's it?!"
    if hero.gold > 0:
        t "I'm taking you gold to give you a lesson: don't start a battle you can't win, idiot."
    $ g = randint (500, 800)
    if hero.gold < g:
        $ hero.gold = 0
    else:
        $ hero.gold -= g
    "He walks away."
    jump main_street
            
label city_events_thugs_robbery_attack:
    $ scr = pytfall.world_events.get("city_events_thugs_robbery_attack").label_cache
    "A group of men suddenly surrounds you!"
    scene
    $ renpy.scene(layer="screens")
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
        if hero.level < 20:
            lvl = hero.level
        else:
            lvl = 25
        for i in xrange(3):
            mob = build_mob("Thug", level=lvl)
            enemy_team.add(mob)
        battle = BE_Core(Image(back), start_sfx=get_random_image_dissolve(1.5), music="random", end_sfx=dissolve, quotes=True)
        battle.teams.append(your_team)
        battle.teams.append(enemy_team)
        battle.start_battle()
        your_team.reset_controller()
        if battle.winner != your_team:
            for member in your_team:
                if member in battle.corpses:
                    member.health = 1
            g = randint (200, 400)
            if hero.gold < g:
                hero.gold = 0
            else:
                hero.gold -= g
            renpy.jump("city_events_thugs_robbery_attack_lost")
        else:
            for member in your_team:
                member.exp += adjust_exp(member, 10)
                if member in battle.corpses:
                    member.health = 1
            renpy.jump("city_events_thugs_robbery_attack_win")
label city_events_thugs_robbery_attack_lost:
    scene expression "bg " + scr
    $ renpy.scene(layer="screens")
    "After beating you they took some gold and disappeared before City Guards arrived."
    jump expression scr
label city_events_thugs_robbery_attack_win:
    scene expression "bg " + scr
    "You found some gold in their pockets before handing them over to the City Guards."
    $ hero.gold += randint(10,40)
    jump expression scr