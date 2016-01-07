label test_be:
    python:
        # Prepear the teams:
        enemy_team = Team(name="Enemy Team", max_size=3)
        mob = build_mob(id="Goblin Shaman", level=120)
        mob.apply_trait("Fire")
        mob.front_row = True
        mob.controller = BE_AI(mob)
        if len(enemy_team) != 3:
            enemy_team.add(mob)
        mob = build_mob(id="Goblin Archer", level=100)
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
        # Add new attack types to see how they look on the other side:
        for m in enemy_team:
            m.magic_skills.append(battle_skills["Water Blast"])
            # m.magic_skills.append(battle_skills["Pure Ion Storm"])
            
        
        h = chars["Hinata"] # Changing to Kushina cause Hinata is still in old xml format that cannot add basetraits.
        h.status = "free"
        h.exp += 2000000
        for stat in h.stats:
            h.mod(stat, 1000)
        h.front_row = False
        n = chars["Nami"]
        n.status = "free"
        n.apply_trait("Air")
        for skill in battle_skills.values():
            if isinstance(skill, SimpleAttack):
                if skill not in h.attack_skills:
                    h.attack_skills.append(skill)
                if skill not in n.attack_skills:
                    n.attack_skills.append(skill)
            else:
                if skill not in h.magic_skills:
                    h.magic_skills.append(skill)
                if skill not in n.magic_skills:
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
        battle = BE_Core(Image("content/gfx/bg/be/b_forest_1.png"), music="content/sfx/music/be/battle (14).ogg", start_sfx=get_random_image_dissolve(1.5), end_sfx=dissolve)
        battle.teams.append(hero.team)
        battle.teams.append(enemy_team)

        battle.start_battle()
 
    jump mainscreen
    
label test_be_logical:
    $ tl.timer("Logical BE Scenario with Setup!")
    python:
        # Prepear the teams:
        enemy_team = Team(name="Enemy Team", max_size=3)
        mob = build_mob(id="Goblin Shaman", level=120)
        mob.front_row = True
        mob.apply_trait("Fire")
        mob.controller = BE_AI(mob)
        if len(enemy_team) != 3:
            enemy_team.add(mob)
        mob = build_mob(id="Goblin Archer", level=100)
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
        
        hero.controller = BE_AI(hero)
        h = chars["Hinata"]
        h.status = "free"
        h.controller = BE_AI(h)
        h.exp += 2000000
        for stat in h.stats:
            h.mod(stat, 1000)
        h.front_row = True
        n = chars["Nami"]
        n.status = "free"
        n.controller = BE_AI(n)
        n.apply_trait("Air")
        # for skill in battle_skills.values():
            # if isinstance(skill, SimpleAttack):
                # h.attack_skills.append(skill)
                # n.attack_skills.append(skill)
            # else:
                # h.magic_skills.append(skill)
                # n.magic_skills.append(skill)
        n.front_row = True
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
        battle = BE_Core(Image("content/gfx/bg/be/b_forest_1.png"), music="content/sfx/music/be/battle (14).ogg", start_sfx=get_random_image_dissolve(1.5), end_sfx=dissolve, logical=1)
        battle.teams.append(hero.team)
        battle.teams.append(enemy_team)
        
        tl.timer("Logical BE Scenario without Setup!")
        battle.start_battle()
        tl.timer("Logical BE Scenario without Setup!")
        
        # Reset Controller:
        hero.controller = "player"
        n.controller = "player"
        h.controller = "player"
        
    $ tl.timer("Logical BE Scenario with Setup!")
    
    scene black
    call screen battle_report
 
    jump mainscreen
    
screen battle_report():
    vbox:
        align (0.5, 0.3)
        spacing 10
        frame:
            background Frame("content/gfx/frame/MC_bg3.png", 10, 10)
            style "dropdown_gm_frame"
            has viewport:
                xysize (540, 400)
                scrollbars "vertical"
                has vbox
                for entry in reversed(battle.combat_log):
                    label "%s"%entry style_group "stats_value_text" text_size 14 text_color ivory
                    
        textbutton "Exit":
            xalign 0.5
            action Return()
                
    
