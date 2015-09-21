label test_be():
    python:
        # Prepear the teams:
        enemy_team = Team(name="Enemy Team", max_size=3)
        mob = build_mob(id="Goblin Shaman", level=120)
        mob.apply_trait("Fire")
        mob.controller = BE_AI(mob)
        if len(enemy_team) != 3:
            enemy_team.add(mob)
        mob = build_mob(id="Goblin Archer", level=100)
        mob.apply_trait("Freak")
        mob.front_row = False
        mob.attack_skills.append("SwordAttack")
        if len(enemy_team) != 3:
            enemy_team.add(mob)
        mob = build_mob(id="Goblin Archer", level=100)
        mob.front_row = False
        mob.attack_skills.append("BowAttack")
        mob.apply_trait("Air")
        if len(enemy_team) != 3:
            enemy_team.add(mob)
        
        h = chars["Hinata"] # Changing to Kushina cause Hinata is still in old xml format that cannot add basetraits.
        h.status = "free"
        h.exp += 2000000
        for stat in h.stats:
            h.mod(stat, 1000)
        h.front_row = False
        n = chars["Nami"]
        h.status = "free"
        n.apply_trait("Air")
        for skill in battle_skills.values():
            if isinstance(skill, SimpleAttack):
                h.attack_skills.append(skill)
                n.attack_skills.append(skill)
            else:
                h.magic_skills.append(skill)
                n.magic_skills.append(skill)
        n.front_row = False
        n.exp += 2000000
        
        for i in hero.team:
            i.besk = None
        
        for stat in n.stats:
            n.mod(stat, 1000)
        if len(hero.team) != 3 and h not in hero.team:
            hero.team.add(h)
        h.AP = 6
        if len(hero.team) != 3 and n not in hero.team:
            hero.team.add(n)
        n.AP = 6
        # ImageReference("chainfights")
        battle = BE_Core(Image("content/gfx/bg/be/b_forest_1.png"), music="content/sfx/music/be/battle (14).ogg", start_sfx=dissolve, end_sfx=dissolve)
        battle.teams.append(hero.team)
        battle.teams.append(enemy_team)

        battle.start_battle()
 
    jump mainscreen
