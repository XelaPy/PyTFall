init -11 python:
    # Simple Automatic conflict resolver for friendly and enemy parties:
    def s_conflict_resolver(fp, ep, new_results=False):
        """
        Simple conflict resolver, used mainly during job events, stats based.
        fp = friendly party (Team)
        ep = enemy party (Team)
        new_results = Whether to allow the function to return OV and DV results.
        """
        offence = 0
        defence = 0
        luck = 0
        
        for friend in fp:
            offence += friend.attack + friend.defence + friend.agility + friend.health
            if friend.mp > friend.magic/5:
                offence += friend.magic
            
            luck += friend.luck
        
        luck *= choice([0.5, 1, 1, 1, 1.5, 2])
        
        for enemy in ep:
            defence += enemy.attack + enemy.defence + enemy.agility + friend.health
            if enemy.mp > enemy.magic/5:
                defence += enemy.magic
        
        exp = int(defence/10)
        
        # Overwhelming victory
        if defence * 2 <= offence and new_results:
            return "OV", exp
        
        # Desisive victory
        elif defence * 1.5 <= offence and new_results:
            return "DV", exp
        
        # Victory
        elif defence <= offence:
            if new_results: return "V", exp
            else: return "victory", exp
        
        # Lucky victory
        elif defence <= offence + luck:
            if new_results: return  "LV", exp
            else: return "victory", exp
        
        # Overwhelming defeat
        elif defence * 0.6 > offence:
            if new_results: return "OD", exp
            else: return "OD"
        
        # Defeat
        else:
            if new_results: return "D", exp
            else: return "defeat"
    
    
    # @TODO: Absolete code!?!
    def be_bridge_team_setup(team, battle, f_class=None, skip=False, sprite_flip=False):
        """
        Registers skills, stats,  with the battle engine.
        team: container for iteration.
        battle: instance of battleengine to avoid another global
        f_class: fighter class
        skip: enables or disables turn skipping
        sprite_flip: self-explanatory
        """
        # Put leader in the middle if team has three members:
        if len(team) == 3:
            team = [team[1], team[0], team[2]]
            
        for member in team:
            
            if sprite_flip:
                Sprite = BattleSprite(im.Flip(member.show("battle_sprite", resize=(200, 200)), horizontal=True), anchor=(0.5, 0.75), placeMark=(0,-75))
            else:
                Sprite = BattleSprite(member.show('battle_sprite', resize=(200, 200)), anchor=(0.5, 0.75))
                
            Member = f_class(member.name, sprite=Sprite,  attributes=[member.element.split(" ")[0]],
                                          Health=member.health, Speed=member.agility, Attack=member.attack,
                                          Magic=member.magic, Defence=member.defence, MP=member.mp,
                                          Luck=member.luck, Charisma=member.charisma)
  
            Member._baseStats.Luck = member.get_max("luck")
            Member._baseStats.Charisma = member.get_max("charisma")
            Member._baseStats.Health = member.get_max('health')
            Member._baseStats.Magic = member.get_max('magic')
            Member._baseStats.Attack = member.get_max('attack')
            Member._baseStats.Defence = member.get_max('defence')
            Member._baseStats.MP = member.get_max('mp')
            Member._baseStats.Speed = member.get_max('agility')
            if f_class == PlayerFighter:
                for key in itertools.chain(member.battle_skills.keys(), member.magic_skills.keys()):
                    key = key.replace(" ", "")
                    # Crutch until this is fixed in the file:
                    if key == "Claw": key = "ClawAttack"
                    Member.RegisterSkill(Library.Skills.__dict__[key])
            else:
                for key in member.battle_skills:
                    entry = key.replace(" ", "")
                    # Crutch until this is fixed in the file:
                    if entry == "Claw": entry = "ClawAttack"
                    Member.RegisterSkill(Library.Skills.__dict__[entry], member.battle_skills[key])
                for key in member.magic_skills:
                    entry = key.replace(" ", "")
                    Member.RegisterSkill(Library.Skills.__dict__[entry], member.magic_skills[key])
                    
            if skip:
                Member.RegisterSkill(Library.Skills.Skip)
                
            battle.AddFighter(Member)
            
    def be_bridge_fighter_setup(fighter, battle, f_class=None, skip=False, sprite_flip=False):
        """
        Registers skills, stats,  with the battle engine on a high level, prolly better do that in BE itself when I get to know it better.
        battle: instance of battleengine to avoid another global
        f_class: fighter class
        skip: enables or disables turn skipping
        sprite_flip: self-explanatory
        """
        member = fighter
        
        if sprite_flip:
            Sprite = BattleSprite(im.Flip(member.show("battle_sprite", resize=(200, 200)), horizontal=True), anchor=(0.5, 0.75), placeMark=(0,-75))
        else:    
            Sprite = BattleSprite(member.show('battle_sprite', resize=(200, 200)), anchor=(0.5, 0.75))
            
        Member = f_class(member.name, sprite=Sprite,  attributes=[member.element.split(" ")[0]],
                                      Health=member.health, Speed=member.agility, Attack=member.attack,
                                      Magic=member.magic, Defence=member.defence, MP=member.mp,
                                      Luck=member.luck, Charisma=member.charisma)

        Member._baseStats.Luck = member.get_max("luck")
        Member._baseStats.Charisma = member.get_max("charisma")
        Member._baseStats.Health = member.get_max('health')
        Member._baseStats.Magic = member.get_max('magic')
        Member._baseStats.Attack = member.get_max('attack')
        Member._baseStats.Defence = member.get_max('defence')
        Member._baseStats.MP = member.get_max('mp')
        Member._baseStats.Speed = member.get_max('agility')
        if f_class == PlayerFighter:
            for key in itertools.chain(member.battle_skills.keys(), member.magic_skills.keys()):
                key = key.replace(" ", "")
                Member.RegisterSkill(Library.Skills.__dict__[key])
        else:
            for key in member.battle_skills:
                entry = key.replace(" ", "")
                Member.RegisterSkill(Library.Skills.__dict__[entry], member.battle_skills[key])
            for key in member.magic_skills:
                entry = key.replace(" ", "")
                Member.RegisterSkill(Library.Skills.__dict__[entry], member.magic_skills[key])
                
        if skip:        
            Member.RegisterSkill(Library.Skills.Skip)
            
        battle.AddFighter(Member)
                 
    def start_battle(player_team, enemy_team, music=None, background=None, pt_ai=False):
        '''
        Bridge to battle engine, idea is to try and make it as easy as possible.
        player_team/enemy_team: iterables
        music: path to a music file
        background: Displayable
        pt_ai: if AI Fighter is required on player team, should be a list of booleans of same length as player_team (True for AI, False for Player control)
        '''
        if music:
            renpy.music.play(music)
        
        battle = Battle(ActiveSchema())
        battle.SetBattlefield(SimpleBattlefield(background))
        
        # Put leader in the middle if team has three members:
        if isinstance(player_team, Team):
            if len(player_team) == 3:
                player_team = [player_team[1], player_team[0], player_team[2]]
                if pt_ai:
                    pt_ai = [pt_ai[1], pt_ai[0], pt_ai[2]]
            
        if isinstance(enemy_team, Team):
            if len(enemy_team) == 3:
                enemy_team = [enemy_team[1], enemy_team[0], enemy_team[2]]
        
        # Player Faction:
        battle.AddFaction("Player", playerFaction=True)

        for index, fighter in enumerate(player_team):
            # This auto sets sprite flips:
            if isinstance(fighter, (Mob)):
                sprite_flip = True
            else:
                sprite_flip = False
             
            if pt_ai:
                if pt_ai[index]:
                    f_class = SimplerAIFighter
                else:
                    f_class = PlayerFighter
            else:
                f_class = PlayerFighter
                
                be_bridge_fighter_setup(fighter, battle, f_class=f_class, skip=True, sprite_flip=sprite_flip)
        
        # Enemies:
        battle.AddFaction('Enemies', playerFaction=False)
        
        for fighter in enemy_team:
            
            if isinstance(fighter, (Mob)):
                sprite_flip = False
            else:
                sprite_flip = True
            
            be_bridge_fighter_setup(fighter, battle, f_class=SimpleAIFighter, skip=False, sprite_flip=sprite_flip)

        battle.AddExtra(RPGDamage(offset=(0, -75)))
        battle.AddExtra(RPGDeath())
        battle.AddExtra(ActiveDisplay("Player", {"HP":"Health", "Move":"Move", "MP":"MP"}))
        battle.AddExtra(RPGActionBob())
        battle.AddExtra(SimpleWinCondition())
        battle.Start()
        
        renpy.music.stop(fadeout = 1.0)
        
        
        corpses = list()
        if battle.Won == "Player":
            for fighter in battle._fighters:
                for member in player_team:
                    if member.name == fighter._name:
                        if fighter._rawStats.Health >= 1:
                            member.health = fighter._rawStats.Health
                        else:
                            member.health = 1
                        member.mp = fighter._rawStats.MP

                        if fighter in battle._corpses:
                            corpses.append(member)
                            
                for member in enemy_team:
                    if member.name == fighter._name:
                        if fighter._rawStats.Health >= 1:
                            member.health = fighter._rawStats.Health
                        else:
                            member.health = 1
                        member.mp = fighter._rawStats.MP
                        
            return (True, corpses)

        else: # Player lost -->
            for fighter in battle._fighters:
                for member in enemy_team:
                    if member.name == fighter._name:
                        if fighter._rawStats.Health >= 1:
                            member.health = fighter._rawStats.Health
                        else:
                            member.health = 1
                        member.mp = fighter._rawStats.MP
                        
                for member in player_team:
                    if member.name == fighter._name:
                        #statdict = {}
                        if fighter._rawStats.Health >= 1:
                            member.health = fighter._rawStats.Health
                        else:
                            member.health = 1
                        member.mp = fighter._rawStats.MP
                        member.combat_stats = "K.O."
                        
            return (False, corpses)
            

