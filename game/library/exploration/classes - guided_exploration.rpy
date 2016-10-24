init -9 python:
    # Trying to set up some logic for forest encounter system (*Very old code):
    class Tile(_object):
        def __init__(self):
            # Defaults
            
            self.name = "Nameless"
            self.id = ""

            
            # Ememy related
            self.attack_skills = []
            self.magic_skills = []
            self.hostile = False
            self.enemy_enounters = 0
            self.max_enemy_enounters = 5
            self.enemy_stats = {}
            self.force_enemy_party_count = False
            self.enemy_sprite = ""
            self.encounter_track = ""
            
            
            # Mechanics/Display related
            self.blocked = False # Impassible tile
            self.fow = True # Fog Of War (explored vs unexplored)
            self.color = blank # Color of a tile on a map
            self.bg = None # Backgound to display
            self.player = False

                
        def init(self):
            if self.bg:
                self.bg = im.Scale(self.bg, config.screen_width, config.screen_height)
                
            if self.player:
                self.color = red
            elif self.fow:
                self.color = black
            elif self.blocked:
                self.color = white
            else:
                self.color = green
                
                
        def update_tile(self):
            if self.player:
                self.color = red
            elif self.fow:
                self.color = black
            elif self.blocked:
                self.color = white
            else:
                self.color = green

    
    class Exploration(_object):
        def __init__(self, max_encounters = 20):
            self.encounters = 0
            self.max_encounters = max_encounters
            
            # map assests
            self.map_dimensions = 20, 10
            self.map = [[ copy.deepcopy(pytfall.tiles["forest_1"])
                                 for y in range(self.map_dimensions[1])]
                                 for x in range(self.map_dimensions[0])]
            
            self.player_tile = [5, 9]
            self.map[self.player_tile[0]][self.player_tile[1]].fow = False
            self.map[self.player_tile[0]][self.player_tile[1]].player = True
            self.map[3][3].blocked = pytfall.tiles["blocked"]
            self.map[3][6].blocked = pytfall.tiles["blocked"]
            self.map[3][5].blocked = pytfall.tiles["blocked"]
            
            for y in range(self.map_dimensions[1]):
                    for x in range(self.map_dimensions[0]):
                            self.map[x][y].update_tile()
            
            
        def screen_loop(self):
            while True:
                result = ui.interact()
                
                if result[0] == 'control':
                    if result[1] == 'return':
                        break
                        
                if result[0] == "move":
                    self.player_move(result[1])
                if result[0] == "fight":
                    if result[1] == "simple_battle":
                        self.start_simple_encounter()
                    

                        
        def player_move(self, direction):
            self.map[self.player_tile[0]][self.player_tile[1]].player = False
            
            if direction == "up":
                if self.player_tile[1] - 1 >=  0:
                    if not self.map[self.player_tile[0]][self.player_tile[1]-1].blocked:
                        self.player_tile[1] -= 1
                        self.map[self.player_tile[0]][self.player_tile[1]].fow = False
                    else:
                        self.map[self.player_tile[0]][self.player_tile[1]-1].fow = False
                
            elif direction == "down":
                if self.player_tile[1] + 1 <= self.map_dimensions[1] - 1:
                    if not self.map[self.player_tile[0]][self.player_tile[1]+1].blocked:
                        self.player_tile[1] += 1
                        self.map[self.player_tile[0]][self.player_tile[1]].fow = False
                    else:
                        self.map[self.player_tile[0]][self.player_tile[1]+1].fow = False

            elif direction == "left":
                if self.player_tile[0] - 1 >= 0:
                    if not self.map[self.player_tile[0]-1][self.player_tile[1]].blocked:
                        self.player_tile[0] -= 1
                        self.map[self.player_tile[0]][self.player_tile[1]].fow = False
                    else:
                        self.map[self.player_tile[0]-1][self.player_tile[1]].fow = False
                
            elif direction == "right":
                if self.player_tile[0] + 1 <= self.map_dimensions[0] - 1:
                    if not self.map[self.player_tile[0]+1][self.player_tile[1]].blocked:
                        self.player_tile[0] += 1
                        self.map[self.player_tile[0]][self.player_tile[1]].fow = False
                    else:
                        self.map[self.player_tile[0]+1][self.player_tile[1]].fow = False

            self.map[self.player_tile[0]][self.player_tile[1]].player = True
                    
            for y in range(self.map_dimensions[1]):
                    for x in range(self.map_dimensions[0]):
                            self.map[x][y].update_tile()
                            
        def show_encounter_button(self):
            if self.map[self.player_tile[0]][self.player_tile[1]].hostile:
                return True
                
        def start_simple_encounter(self):
            renpy.hide_screen("forest_exploration")
            if self.map[self.player_tile[0]][self.player_tile[1]].encounter_track:
                renpy.music.play(self.map[self.player_tile[0]][self.player_tile[1]].encounter_track, fadein=0.5)
            
            battle = Battle(ActiveSchema())
            battle.SetBattlefield(SimpleBattlefield(BattlefieldSprite(self.map[self.player_tile[0]][self.player_tile[1]].battle_bg)))
            battle.AddFaction("Player", playerFaction=True)
            for member in hero.team:
                MemberSprite = BattleSprite(member.show('battle_sprite', resize=(200,220)), anchor=(0.5, 0.75))
                Member = PlayerFighter(member.name, Health=member.health,  Speed = member.agility, Attack = member.attack, Magic = member.magic, Defence = member.defence, MP = member.mp, sprite=MemberSprite)
                Member._baseStats.Health = member.max['health']
                Member._baseStats.Magic = member.max['magic']
                Member._baseStats.Attack = member.max['attack']
                Member._baseStats.Defence = member.max['defence']
                Member._baseStats.MP = member.max['mp']
                Member._baseStats.Speed = member.max['agility']
                for entry in member.attack_skills:
                    if entry == 'Fist Attack':
                        Member.RegisterSkill(Library.Skills.FistAttack)
                    if entry == 'Sword Attack':
                        Member.RegisterSkill(Library.Skills.SwordAttack)
                    if entry == 'KnifeAttack':
                        Member.RegisterSkill(Library.Skills.KnifeAttack)
                    if entry == 'Claw Attack':
                        Member.RegisterSkill(Library.Skills.SwordAttack)
                    if entry == 'Cannon Attack':
                        Member.RegisterSkill(Library.Skills.CannonAttack)                        
                for entry in member.magic_skills:
                    if entry == 'Fire 1':
                        Member.RegisterSkill(Library.Skills.Fire1)
                    if entry == 'Fire 2':
                        Member.RegisterSkill(Library.Skills.Fire2)
                    if entry == 'Water 1':
                        Member.RegisterSkill(Library.Skills.Water1)
                    if entry == 'Water 2':
                        Member.RegisterSkill(Library.Skills.Water2)
                    if entry == 'Earth 1':
                        Member.RegisterSkill(Library.Skills.Earth1)
                    if entry == 'Earth 2':
                        Member.RegisterSkill(Library.Skills.Earth2)
                    if entry == 'Windwhirl':
                        Member.RegisterSkill(Library.Skills.Windwhirl)
                    if entry == 'Ice Arrow':
                        Member.RegisterSkill(Library.Skills.IceArrow)
                    if entry == 'Fire Arrow':
                        Member.RegisterSkill(Library.Skills.FireArrow)                        
                Member.RegisterSkill(Library.Skills.Skip)
                battle.AddFighter(Member)
                
                
            battle.AddFaction('Enemies', playerFaction=False)
            for enemy in range(1):
                EnemySprite = BattleSprite(self.map[self.player_tile[0]][self.player_tile[1]].enemy_sprite, anchor=(0.5, 0.75), placeMark=(0,-75))
                #EnemySprite = BattleSprite(im.Flip(hero.show("battle_sprite", resize=(200, 200)), horizontal=true), anchor=(0.5, 0.75), placeMark=(0,-75))
                Enemy = SimpleAIFighter(self.map[self.player_tile[0]][self.player_tile[1]].enemy_stats["name"],
                                                          Speed=self.map[self.player_tile[0]][self.player_tile[1]].enemy_stats["speed"],
                                                          Attack=self.map[self.player_tile[0]][self.player_tile[1]].enemy_stats["attack"],
                                                          Defence=self.map[self.player_tile[0]][self.player_tile[1]].enemy_stats["defence"],
                                                          Magic=self.map[self.player_tile[0]][self.player_tile[1]].enemy_stats["magic"],
                                                          MP=self.map[self.player_tile[0]][self.player_tile[1]].enemy_stats["mp"],
                                                          sprite=EnemySprite)
                
                if self.map[self.player_tile[0]][self.player_tile[1]].attack_skills:
                    for entry in self.map[self.player_tile[0]][self.player_tile[1]].attack_skills:
                        if entry == 'Fist Attack':
                            Enemy.RegisterSkill(Library.Skills.FistAttack, 1)
                        if entry == 'Sword Attack':
                            Enemy.RegisterSkill(Library.Skills.SwordAttack, 1)
                        if entry == 'KnifeAttack':
                            Enemy.RegisterSkill(Library.Skills.KnifeAttack, 1)
                        if entry == 'Claw Attack':
                            Enemy.RegisterSkill(Library.Skills.SwordAttack, 1)
                        
                if self.map[self.player_tile[0]][self.player_tile[1]].magic_skills:
                    for entry in self.map[self.player_tile[0]][self.player_tile[1]].magic_skills:
                        if entry == 'Fire 1':
                            Enemy.RegisterSkill(Library.Skills.Fire1, 1)
                        if entry == 'Fire 2':
                            Enemy.RegisterSkill(Library.Skills.Fire2, 1)
                        if entry == 'Water 1':
                            Enemy.RegisterSkill(Library.Skills.Water1, 1)
                        if entry == 'Water 2':
                            Enemy.RegisterSkill(Library.Skills.Water2, 1)
                        if entry == 'Earth 1':
                            Enemy.RegisterSkill(Library.Skills.Earth1, 1)
                        if entry == 'Earth 2':
                            Enemy.RegisterSkill(Library.Skills.Earth2, 1)
                        if entry == 'Windwhirl':
                            Enemy.RegisterSkill(Library.Skills.Windwhirl, 1)
                        if entry == 'Ice Arrow':
                            Enemy.RegisterSkill(Library.Skills.IceArrow, 1)
                        if entry == 'Fire Arrow':
                            Enemy.RegisterSkill(Library.Skills.FireArrow, 1)                
                battle.AddFighter(Enemy)
                
            battle.AddExtra(RPGDamage(offset=(0, -75)))
            battle.AddExtra(RPGDeath())
            battle.AddExtra(ActiveDisplay("Player", {"HP": "Health", "Move": "Move", "MP":"MP"}))
            battle.AddExtra(RPGActionBob())
            battle.AddExtra(SimpleWinCondition())
            battle.Start()
            
            renpy.music.stop(fadeout = 1.0)
            if battle.Won == "Player":
                #raise Exception, battle._fighters[0]._name
                for member in hero.team:
                    for fighter in battle._fighters:
                        if member.name == fighter._name:
                            member.health = fighter._rawStats.Health
                            member.mp = fighter._rawStats.MP
                            member.mod_stat('attack', randint(0,2))
                            member.mod_stat('magic', randint(0,2))
                            member.mod_stat('agility', randint(0,2))
            else:
                raise Exception, "Game Over!!!"
    
            renpy.show_screen("forest_exploration")
            
    # Attempt to load tiles from Tiled into Jake's BE:
    class TileMap(_object):
        """
        Prototype to import and build of maps from Tiled.
        For now using a single tileset (can be updated to using infinite amount)
        """
        def __init__(self, path):
            self.data = load_json(path)
            
            # Map:
            self.map = self.data["layers"][0]["data"]
            self.height = self.data["layers"][0]["height"]
            self.width = self.data["layers"][0]["width"]
            
            # Tileset:
            # If this works out, I'll have to account for mupliple tilesets in the future.
            # self.imageheight = self.data["tilesets"]["imageheight"]
            # self.imagewidth = self.data["tilesets"]["imagewidth"]
            self.image = "content/gfx/tilesets/tmw_desert_spacing.png" # + self.data["tilesets"][0]["image"]
            self.ts_name = self.data["tilesets"][0]["name"]
            self.tileproperties = self.data["tilesets"][0]["tileproperties"]
            self.col = [int(key) + 1 for key in self.tileproperties.keys()]
            
        def get_args_for_composite(self):
            """
            Returns a list of arguments to be unpacked for Composite
            """
            args = list()
            for y in xrange(self.height):
                for x in xrange(self.width):
                    args.append((x*96, y*96))
                    args.append(self.ts_name + str(self.map[y*(self.height+(self.width-self.height)) + x]))
            return args
            
        def build_map(self):
            """
            Builds the map and returns it as RenPy Image
            """
            # Register the times as images first:
            t = 1
            # Margins + Spacing
            for y in xrange(6):
                for x in xrange(8):
                    _x = x + 1
                    _y = y + 1
                    renpy.image(self.ts_name + "%d"%t, im.Scale(im.Crop(self.image, (x*32+_x, y*32+_y, 32, 32)), 96, 96))
                    t += 1
                    
            # Build the map into single image and return it:
            args = self.get_args_for_composite()
            return LiveComposite((3840, 2400), *args)
