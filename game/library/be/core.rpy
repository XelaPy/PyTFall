init -1 python: # Core classes:
    """
    This is our version of turnbased BattleEngine.
    I think that we can use zorders on master layer instead of messing with multiple layers.
    """
    
    BDP = {} # BE DEFAULT POSITIONS *Postions are tuples in lists that go from top to bottom.
    BDP["l0"] = [(160, 360), (120, 410), (80, 460)] # Left (Usually player) teams backrow default positions.
    BDP["l1"] = [(260, 360), (220, 410), (180, 460)] # Left (Usually player) teams frontrow default positions.
    BDP["r0"] = list((config.screen_width-t[0], t[1]) for t in BDP["l0"]) # BackRow, Right (Usually enemy).
    BDP["r1"] = list((config.screen_width-t[0], t[1]) for t in BDP["l1"]) # FrontRow, Right (Usually enemy).
    
    # We need to get perfect middle positioning:
    # Get the perfect middle x:
    perfect_middle_xl = BDP["l0"][1][0] + (BDP["l1"][1][0] - BDP["l0"][1][0])
    perfect_middle_yl = BDP["l0"][1][1] + (BDP["l1"][1][0] - BDP["l0"][1][0])
    perfect_middle_xr = BDP["r1"][1][0] + (BDP["r1"][1][0] - BDP["r0"][1][0])
    perfect_middle_yr = perfect_middle_yl
    BDP["perfect_middle_right"] = (perfect_middle_xl, perfect_middle_yl)
    BDP["perfect_middle_left"] = (perfect_middle_xr, perfect_middle_yr)
    del perfect_middle_xl
    del perfect_middle_yl
    del perfect_middle_xr
    del perfect_middle_yr
    
    class BE_Core(object):
        """Main BE attrs, data and the loop!
        """
        def __init__(self, bg, music=None, row_pos=None, start_sfx=None, end_sfx=None, logical=False):
            """Creates an instance of BE scenario.
            
            logical: Just the calculations, without pause/gfx/sfx.
            """
            self.teams = list() # Each team represents a faction on the battlefield. 0 index for left team and 1 index for right team.
            self.queue = list() # List of events in BE..
            self.bg = ConsitionSwitcher("default", {"default": bg, "black": Solid("#000000"), "mirrage": Mirage(bg, amplitude=0.04, wavelength=10, ycrop=10)}) # Background we'll use.
            # self.miragebg = Mirage(bg, amplitude=0.04, wavelength=10, ycrop=10)
                
            self.music = music
            self.corpses = set() # Anyone died in the BE.
            
            if not row_pos:
                self.row_pos = BDP
            else:
                self.row_pos = row_pos
                
            self.controller = None # Whatever controls the current queue of the loop is the controller. Usually it's player or AI combatants.
            self.winner = None
            self.combat_log = list()
            
            # Events:
            self.end_turn_events = list() # Events we execute on start of the turn.
            self.start_turn_events = list() # Events we execute on the end of the turn.
            self.mid_turn_events = list() # Events to execute after controller was set.
            
            self.logical = logical
            
            self.start_sfx = start_sfx
            self.end_sfx = end_sfx
            
        def log(self, report):
            if config.debug:
                devlog.info(report)
            self.combat_log.append(report)
            
        def get_faction(self, char):
            # Since factions are simply teams:
            for team in self.teams:
                if char in team:
                    return team.name # Maybe this should be an instance of the team? Concider this for the future when this might really matter.
            
        def main_loop(self):
            """
            Handles events on the battlefield until something that can break the loop is found.
            """
            while 1:
                # We run events queued at the start of the turn first:
                for event in self.start_turn_events[:]:
                    if event():
                        self.start_turn_events.remove(event)
                        
                ev = self.next_turn() # This is a character (Maybe it's not a good idea to call it event? We'll figure this out in the future when I know for sure if we'll have to put events in the main queue as well.)
                self.controller = ev
                
                for event in self.mid_turn_events[:]:
                    if event():
                        self.mid_turn_events.remove(event)
                
                # If the controller was killed off during the mid_turn_events:
                if ev not in self.corpses:
                    if ev.controller != "player":
                        # This character is not controled by the player so we call the (AI) controller:
                        ev.controller()
                    else:
                        # Controller is the player:
                        # Call the skill choice screen:
                        s = None
                        t = None
                        while not (s and t):
                            s = renpy.call_screen("pick_skill", ev)
                            s.source = ev
                            
                            # Unique check for Skip Skill:
                            if isinstance(s, BE_Skip):
                                break
                            
                            # Call the targeting screen:
                            targets = s.get_targets()
                            
                            t = renpy.call_screen("target_practice", s, targets)
                            
                        s(t=t)
                
                if not self.logical:
                    renpy.hide_screen("pick_skill")
                    renpy.hide_screen("target_practice")
                    
                # if config.developer:
                    # renpy.show_screen("be_test", ev) # If I need to know whats going on atm, I am using this in the dev mode...
                
                # End turn events, Death (Usually) is added here for example.
                for event in self.end_turn_events[:]:
                    if event():
                        self.end_turn_events.remove(event)
                
                # We check the conditions for terminating the BE scenario, this should prolly be end turn event as well, but I've added this before I've added events :)       
                if self.check_conditions():
                    break
            
            self.end_battle()
        
        def start_battle(self):
            
            self.prepear_teams()
            
            if not self.logical:
                
                renpy.maximum_framerate(30)
                
                if self.music:
                    renpy.music.stop()
                    renpy.music.stop(channel="world")
                    renpy.music.play(self.music)
                    
                # Show the BG:
                renpy.scene()
                
                # Lets render the teammembers:
                # First the left team:
                team = self.teams[0]
                for i in team:
                    self.show_char(i, at_list=[Transform(pos=self.get_icp(team, i))])
                    
                team = self.teams[1]
                for i in team:
                    self.show_char(i, at_list=[Transform(pos=self.get_icp(team, i))])
                    
                renpy.show("bg", what=self.bg)
                renpy.show_screen("battle_overlay")
                if self.start_sfx: # Special Effects:
                    renpy.with_statement(self.start_sfx)
                    
            # After we've set the whole thing up, we've launch the main loop:
            self.main_loop()
            
        def prepear_teams(self):
            # Plainly sets allegiance of chars to their teams. Allegiance may change during the fight (confusion skill for example once we have one).
            # I've also included part of team/char positioning logic here. 
            for team in self.teams:
                team.position = "l" if not self.teams.index(team) else "r"
                for char in team:
                    # Position:
                    char.beteampos = team.position
                    char_index = team.members.index(char)
                    if len(team) == 3 and char_index < 2:
                        char_index = not int(bool(char_index))
                    char.beinx = char_index
                    if team.position == "l":
                        char.row = int(char.front_row)
                    else: # Case "r"
                        char.row = 2 if char.front_row else 3
                    
                    # Allegiance:
                    char.allegiance = team.name
            
            
        def end_battle(self):
            """Ends the battle, trying to normalize any variables that may have been used during the battle.
            """
            if not self.logical:
                # We'll have to reset any attributes of the charcters classes:
                renpy.hide_screen("be_test")
                renpy.hide_screen("target_practice")
                renpy.hide_screen("pick_skill")
                renpy.hide_screen("battle_overlay")
                renpy.scene()
                if self.end_sfx:
                    renpy.with_statement(self.end_sfx)
    
                if self.music:
                    renpy.music.stop()
                
            for team in self.teams:
                for i in team:
                    i.betag = None
                    i.besk = None
                    i.besprite_size = None
                    
        def next_turn(self):
            """
            Returns the next battle events to the game.
            (Re)Calculates the queue of events.
            Currently we're calculating one turn where everyone gets to go once.
            Last index is the next in line.
            """
            if not self.queue:
                l = self.get_fighters()
                l = list(i for i in itertools.chain.from_iterable(self.teams) if i not in self.corpses)
                l.sort(key=attrgetter("agility"))
                self.queue = l
            return self.queue.pop()
            
        def get_icp(self, team, char):
            """Get Initial Character Position
            
            Basically this is what sets the characters up at the start of the battle-round.
            Returns inicial position of the character based on row/team!
            Positions should always be retrieved using this method or errors may occur.
            """
            # We want different behavior for 3 member teams putting the leader in the middle:
            char.besk = dict()
            # Supplied to the show method.
            char.betag = str(random.random())
            # First, lets get correct sprites:
            sprite = char.show("battle_sprite", resize=char.get_sprite_size("battle_sprite"))
            char.besprite_size = sprite.true_size()
            
            # We'll assign "indexes" from 0 to 3 from left to right [0, 1, 3, 4] to help calculating attack ranges.
            team_index = team.position
            char_index = char.beinx
            if team_index:
                if char.__class__ == Mob:
                    char.besprite = im.Flip(sprite, horizontal=True)
                else:
                    char.besprite = sprite
                    
                # We're going to land the character at the default position from now on, with centered buttom of the image landing directly on the position!
                # This makes more sense for all purposes:
                char.dpos = self.row_pos[team_index + str(int(char.front_row))][char_index]
                char.cpos = char.dpos
                
            if team_index == "r":
                if char.__class__ != Mob:
                    char.besprite = im.Flip(sprite, horizontal=True)
                else:
                    char.besprite = sprite
                    
                pos = self.row_pos[team_index + str(int(char.front_row))][char_index]
                # Now the offset:
                xpos = pos[0] - char.besprite_size[0]
                char.dpos = (xpos, pos[1])
                char.cpos = char.dpos
                
                
            char.besk["what"] = char.besprite
            # Zorder defaults to characters (index + 1) * 100
            char.besk["zorder"] = (char_index + 1) * 100
            
            # ---------------------------------------------------->>>
            return char.dpos
             
        def show_char(self, char, *args, **kwargs):
            for key in char.besk:
                if key not in kwargs: # We do not want to overwrite!
                    kwargs[key] = char.besk[key]
            renpy.show(char.betag, *args, **kwargs)
            
        def move(self, char, pos, t, pause=True):
            """
            Move character to new position...
            """
            renpy.hide(char.betag)
            renpy.show(char.betag, what=char.besprite, at_list=[move_from_to_pos_with_ease(start_pos=char.cpos, end_pos=pos, t=t)], zorder=char.besk["zorder"])
            char.cpos = pos
            if pause:
                renpy.pause(t)
            
        def get_cp(self, char, type="pos", xo=0, yo=0, override=False):
            """I am not sure how this is supposed to work yet in the grand scheme of things.
            
            Old Comment: For now it will report initial position + types:
            **Updated to using Current Position + Types.
            pos: Character position (pos)
            center: center of the charcters image
            tc: top center of the characters image
            bc: bottom center of the characters image
            fc: front center (Special per row instruction (for offset) applies)
            
            xo = offset for x
            yo = offset for y
            """
            if not override:
                if not char.cpos or not char.besprite_size:
                    raise Exception([char.cpos, char.besprite_size])
                if type == "pos":
                    xpos = char.cpos[0]
                    ypos = char.cpos[1] + yo
                elif type == "center":
                    xpos = char.cpos[0] + char.besprite_size[0] / 2
                    ypos = char.cpos[1] + char.besprite_size[1] / 2 + yo
                elif type == "tc":
                    xpos = char.cpos[0] + char.besprite_size[0] / 2
                    ypos = char.cpos[1] + yo
                elif type == "bc":
                    xpos = char.cpos[0] + char.besprite_size[0] / 2
                    ypos = char.cpos[1] + char.besprite_size[1] + yo
                elif type == "fc":
                    if char.row in [0, 1]:
                        xpos = char.cpos[0] + char.besprite_size[0]
                        ypos = char.cpos[1] + char.besprite_size[1] / 2 + yo
                    else:
                        xpos = char.cpos[0]
                        ypos = char.cpos[1] + char.besprite_size[1] / 2 + yo
                        
            # in case we do not care about position of a target/caster and just provide "overwrite" we should use instead:
            else:
                xpos, ypos = override
                if yo:
                    ypos = ypos + yo # Same as for comment below (Maybe I just forgot how offsets work and why...)
                
            # While yoffset is the same, x offset depends on the team position: @REVIEW: AM I TOO WASTED OR DOES THIS NOT MAKE ANY SENSE???
            if char.row in [0, 1]:
                xpos = xpos + xo
            else:
                xpos = xpos - xo # Is this a reasonable approach instead of providing correct (negative/positive) offsets? Something to concider during the code review...
                    
            return xpos, ypos
                    
        def get_fighters(self, state="alive", rows=None):
            """
            Returns a list of all fighters from the team.
            states:
            - alive: All active member on the battlefield.
            - all: Everyone dead or alive.
            - dead: Everyone dead in the battlefied.
            rows: If provided, should be an iterable in range of 0 - 3. Only fighters in the row will be returned.
            """
            if state == "all":
                l = list(i for i in itertools.chain.from_iterable(self.teams))
            elif state == "alive":
                l =  list(i for i in itertools.chain.from_iterable(self.teams) if i not in self.corpses)
            elif state == "dead":
                l = list(self.corpses)
                
            if rows:
                l = list(i for i in l if i.row in rows)
                
            return l
            
        def check_conditions(self):
            # Checks if any specific condition is reached.
            # Should prolly be turned into a function when this gets complicated, for now it's just fighting until one of the party are "corpses".
            # For now this assumes that team indexed 0 is player team.
            if len(self.teams[0]) == len(self.get_fighters(state="dead", rows=(0, 1))):
                self.winner = self.teams[1]
                return True
            if len(self.teams[1]) == len(self.get_fighters(state="dead", rows=(2, 3))):
                self.winner = self.teams[0]
                return True
                
                
    class BE_Event(object):
        """
        Anything that happens in the BE.
        Can be executed in RT or added to queues where it will be called.
        This is just to show off the structure...
        """
        def __init__(self, **kwargs):
            pass
        
        def __call__(self, *args, **kwargs):
            """
            Sets the pause and logic to allow event to be executed.
            """
            if self.check_conditions():
                self.apply_effects()
                return self.kill()
                
        def __str__(self):
            return str(self.name)
                
        def check_conditions(self):
            """Should return True/False to allow event execution.
            """
            pass
        
        def kill(self):
            """
            Decides if event should be killed or not (should return True for yes and False for keeping it alive)
            """
            pass
        
        def apply_effects(self, targets=None):
            pass
            
        
    class BE_Action(BE_Event):
        """Basic action class that assumes that there will be targeting of some kind and followup logical and graphical effects.
        """
        def __init__(self, name, range=1, source=None, type="se", piercing=False, multiplier=1, true_pierce=False,
                           menuname=None, critpower=0, menucat="Attacks", sfx=None, gfx=None, attributes=[], effect=0, zoom=None,
                           add2skills=True, desc="", pause=0, target_state="alive", menu_pos=0,
                           attacker_action={},
                           attacker_effects={},
                           main_effect={},
                           dodge_effect={},
                           target_sprite_damage_effect={},
                           target_damage_effect={},
                           target_death_effect={},
                           bg_main_effect={},
                           **kwrags):
            """
            range: range of the spell, 1 is minimum.
            damage_effect: None is default, character is dissolved with the death effect in gfx method in special cases
            type: type of the attack, types are:
            *all: Everyone in the range. *This doesn't work yet
            *all_enemies: All enemies within the range.
            *all_allies: All allies within the range.
            *se: Single enemy within range.
            *sa: Single ally within range.
            """
            # Naming/Sorting:
            self.name = name
            if not menuname:
                self.mn = self.name
            else:
                self.mn = menuname
            self.manucat = menucat
            
            # Logic:
            self.range = range
            self.source = source
            self.type = type
            self.critpower = critpower
            self.piercing = piercing
            self.true_pierce = true_pierce # Does full damage to back rows.
            self.attributes = attributes
            self.effect = effect
            self.multiplier = multiplier
            self.death_effect = death_effect
            self.desc = desc
            self.target_state = target_state
            self.menu_pos = menu_pos
            
            self.tags_to_hide = list() # BE effects tags of all kinds, will be hidden when the show gfx method runs it's cource and cleared for the next use.
            
            if add2skills:
                battle_skills[self.name] = self
                
            # GFX/SFX + Dicts:
            self.timestamps = {} # We keep all gfx effects here!
            
            self.attacker_action = attacker_action.copy()
            self.attacker_effects = attacker_effects.copy()
            self.attacker_effects["gfx"] = attacker_effects.get("gfx", None)
            self.attacker_effects["sfx"] = attacker_effects.get("sfx", None)
            
            dp = deepcopy(main_effect)
            self.main_effect = dp
            self.main_effect["gfx"] = main_effect.get("gfx", None)
            self.main_effect["sfx"] = main_effect.get("sfx", None)
            self.main_effect["start_at"] = main_effect.get("start_at", 0)
            self.main_effect["aim"] = dp.get("aim", {})
            
            self.dodge_effect = dodge_effect.copy()
            self.dodge_effect["gfx"] = dodge_effect.get("gfx", True)
            
            self.target_sprite_damage_effect = target_sprite_damage_effect.copy()
            self.target_sprite_damage_effect["gfx"] = target_sprite_damage_effect.get("gfx", None)
            self.target_sprite_damage_effect["sfx"] = target_sprite_damage_effect.get("sfx", None)
            
            self.target_damage_effect = target_damage_effect.copy()
            self.target_damage_effect["gfx"] = target_damage_effect.get("gfx", "battle_bounce")
            self.target_damage_effect["sfx"] = target_damage_effect.get("sfx", None)
            
            self.target_death_effect = target_death_effect.copy()
            self.target_death_effect["gfx"] = target_death_effect.get("gfx", "dissolve")
            self.target_death_effect["sfx"] = target_death_effect.get("sfx", None)
            
            self.bg_main_effect = bg_main_effect.copy()
            self.bg_main_effect["gfx"] = bg_main_effect.get("gfx", None)
            if self.bg_main_effect["gfx"]:
                self.bg_main_effect["initial_pause"] = self.bg_main_effect.get("initial_pause", self.main_effect["start_at"])
                self.bg_main_effect["duration"] = self.bg_main_effect.get("duration", main_effect.get("duration", 0.4))
            
            if sfx:
                self.main_effect["sfx"] = sfx # This is for really simple attacks. ==> Now declared differently for ALL NORMAL ATTACK TYPES!
            if gfx:
                # Zoom:
                # Zoom factors the size of the main displayable of the attack (if there is one). Use floats, 1.0 represents original size, -1 will invert (flip) the image.
                # I am reluctant of supporting this in the future as it can be plainly added to declaration with a Transform...
                self.main_effect["gfx"] = Transform(gfx, zoom=zoom) if zoom else gfx # This is for really simple attacks. ==> Now declared differently for ALL NORMAL ATTACK TYPES!
            if pause:
                self.main_effect["duration"] = pause
            
        
        def get_targets(self, source=None):
            """
            Gets tagets that can be hit with this action.
            Rows go [0, 1, 2, 3] from left to right of the battle-field.
            """
            char = source if source else self.source
            
            # First figure out all targets within the range:
            # We calculate this by assigning.
            target_rows = range(char.row - self.range, char.row + 1 + self.range)
            all_targets = battle.get_fighters(self.target_state)
            in_range = set(f for f in all_targets if f.row in target_rows)
            
            if any(t for t in in_range if isinstance(t, basestring)):
                raise Exception(in_range)
            
            # Lets handle the piercing (Or not piercing since piercing attacks incude everyone in range already):
            if not self.piercing:
                if char.row in [0, 1]:
                    # Source is on left team:
                    # We need to check if there is at least one member on the opposing front row and if true, remove everyone in the back.
                    if battle.get_fighters(rows=[2]):
                        # opfor has a defender:
                        # we need to remove everyone from the back row:
                        in_range = [f for f in in_range if f.row != 3]
                else:
                    if battle.get_fighters(rows=[1]):
                        in_range = [f for f in in_range if f.row != 0]
                             
            # Now the type, we just care about friends and enemies:
            if self.type in ["all_enemies", "se"]:
                in_range = set([f for f in in_range if char.allegiance != f.allegiance])
            elif self.type in ["all_allies", "sa"]:
                in_range = set([f for f in in_range if char.allegiance == f.allegiance])
                
            # In a perfect world, we're done, however we have to overwrite normal rules if no targets are found and backrow can hit over it's own range (for example):
            if not in_range: # <== We need to run "frenemy code prior to this!"
                # Another step is to allow any range > 1 backrow attack and any frontrow attack hitting backrow of the opfor...
                # and... if there is noone if front row, allow longer reach fighters in backrow even if their range normally would not allow it.
                if char.row == 0:
                    # Case: Fighter in backrow and no defenders on opfor.
                    if not battle.get_fighters(rows=[2]) and self.range > 1:
                        # We add everyone in the back row for target practice :)
                        in_range = in_range.union(battle.get_fighters(rows=[3])) # TODO: Union is prolly utterly useless here, confirm and remove!
                    # Case: Fighter in backrow and there is no defender on own team,
                    if not battle.get_fighters(rows=[1]):
                        # but there is at least one on the opfor:
                        if battle.get_fighters(rows=[2]):
                            in_range = in_range.union(battle.get_fighters(rows=[2]))
                        # else, there is are no defenders at all anywhere...
                        else:
                            in_range = in_range.union(battle.get_fighters(rows=[3]))
                elif char.row == 1:
                    if not battle.get_fighters(rows=[2]):
                        # We add everyone in the back row for target practice :)
                        in_range = in_range.union(battle.get_fighters(rows=[3]))
                elif char.row == 2:
                    if not battle.get_fighters(rows=[1]):
                        # We add everyone in the back row for target practice :)
                        in_range = in_range.union(battle.get_fighters(rows=[0]))
                elif char.row == 3:
                    if not battle.get_fighters(rows=[1]) and self.range > 1:
                        # We add everyone in the back row for target practice :)
                        in_range = in_range.union(battle.get_fighters(rows=[0]))
                    # Case: Fighter in backrow and there is no defender on own team,
                    if not battle.get_fighters(rows=[2]):
                        # but there is at least one on the opfor:
                        if battle.get_fighters(rows=[1]):
                            in_range = in_range.union(battle.get_fighters(rows=[1]))
                        # else, there is are no defenders at all anywhere...
                        else:
                            in_range = in_range.union(battle.get_fighters(rows=[0]))
            
            # And we need to check for dead people again... better code is needed to avoid cr@p like this in the future:
            in_range = [i for i in in_range if i in all_targets]
            
            return in_range # List: So we can support indexing...
            
        def check_conditions(self, source=None):
            if source:
                char = source
            else:
                char = self.source
            if self.get_targets(char):
                return True
                
        def effects_resolver(self, targets):
            """
            Logical effect of the action. More often than not, it calculates the damage.
            Expects a list or tuple with targets.
            This should return it's results through PytCharacters property called damage so the show_gfx method can be adjusted accordingly.
            But it is this method that writes to the log to be displayed later... (But you can change even this :D)
            """
            # prepare the variables:
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            a = self.source
            attributes = self.attributes
            
            # Get the attack power:
            attack = self.get_attack()
            name = self.name
            
            for t in targets:
                # If character does NOT resists the attack:
                if not self.check_resistance(t):
                    # We get the mupliplier and any effects that those may bring.
                    effects, multiplier = self.get_attributes_multiplier(t, attributes)
                    
                    # Get the damage:
                    defense = self.get_defense(t)
                    damage = self.default_damage_calculator(t, attack, defense, multiplier)
                    
                    # Rows Damage:
                    effects_append, damage = self.get_row_damage(t, damage)
                    effects = effects + effects_append
                            
                    # Lets check the absobtion:
                    result = self.check_absorbtion(t)
                    if result:
                        damage = -damage * result
                        effects.append("absorbed")
                else: # resisted
                    damage = 0
                    effects = list()
                    effects.append("resisted")
                    
                effects.insert(0, damage)
                
                # log the effects:
                t.beeffects = effects
            
                # String for the log:
                s = list()
                s.append("{color=[teal]}%s{/color} attacks %s with %s!" % (a.nickname, t.nickname, self.name))
                
                s = s + self.effects_for_string(t)
                
                battle.log("".join(s))
        
        def effects_for_string(self, t, default_color="red"):
            # String for the log:
            effects = t.beeffects
            attributes = self.attributes
            s = list()
            if "resisted" not in effects:
                if "elemental_damage_bonus" in effects:
                    # Elemental Damage Bonus, means attacker caused extra damage due to a spell aligning (positevely) with one or more if the attackers elements:
                    s.append(" {color=[lawngreen]}ElDmg+! {/color}")
                if "elemental_damage_penatly" in effects:
                    # The opposite of the above
                    s.append(" {color=[red]}ElDmg-! {/color}")
                if "elemental_defence_bonus" in effects:
                    # Elemental Damage Bonus, means attacker caused extra damage due to a spell aligning (negatevely) with one or more if the defenders elements
                    s.append(" {color=[lawngreen]}ElDef- {/color}")
                if "elemental_defence_penalty" in effects:
                    # The opposite of the above
                    s.append(" {color=[red]}ElDef+ {/color}")
                if "backrow_penalty" in effects:
                    # Damage halved due to the target being in the back row!
                    s.append(" {color=[red]}1/2 DMG (Back-Row) {/color}")
                if "critical_hit" in effects:
                    s.append(" {color=[lawngreen]}Critical Hit {/color}")
                if "missed_hit" in effects:
                    s.append(" {color=[lawngreen]}Attack Missed {/color}")
                if "absorbed" in effects:
                    s.append(" {color=[lawngreen]}Absorbed DMG{/color}")
                    s.append(self.set_dmg_font_color(t, attributes, color="green"))
                else:
                    s.append(self.set_dmg_font_color(t, attributes, color=default_color))    
            else: # If resisted:
                s.append(" {color=[crimson]}Resisted the attack{/color}")
                s.append(self.set_dmg_font_color(t, attributes, color="green"))
                
            return s
                
        def default_damage_calculator(self, t, attack, defense, multiplier):
            damage = 0
            # Calculate damage same as usual
            if (defense < 1):
                damage = attack * 1.5
            else:
                damage = (attack/defense) + 0.5
                
            # Get a random number between 0.8 and 1.2
            rand = (random.random() * 0.4) + 0.8
            damage = int(float(damage) * multiplier * 10 * rand)
            return damage
                
        def get_row_damage(self, t, damage):
            # It's always the normal damage except for rows 0 and 3 (unless everyone in the front row are dead :) ).
            # Adding true_piece there as well:
            effects = list()
            if t.row == 3:
                if battle.get_fighters(rows=[2]) and not self.true_pierce:
                    damage = damage / 2
                    effects.append("backrow_penalty")
            if t.row == 0:
                if battle.get_fighters(rows=[1]) and not self.true_pierce:
                    damage = damage / 2
                    effects.append("backrow_penalty")
            return effects, damage        
                
        def check_absorbtion(self, t):
            # Get all absorption capable traits:
            l = list(trait for trait in t.traits if trait.el_absorbs)
            # Get ratio:
            d = dict()
            if l:
                for attr in self.attributes:
                    for trait in l:
                        if attr in trait.el_absorbs:
                            d[trait.id] = trait.el_absorbs[attr]
                if d:
                    ratio = sum(d.values()) / len(d)
                    return ratio
                    
        def check_resistance(self, t):
            if list(i for i in self.attributes if i in t.resist):
                return True
                
        def get_attack(self):
            """
            Very simple method to get to attack power.
            """
            a = self.source
            if any(list(i for i in ["melee", "ranged"] if i in self.attributes)):
                attack = (a.attack + self.effect) * self.multiplier  # TODO: ADD WEAPONS EFFECTS IF THIS IS A WEAPON SKILLS.
            elif "magic" in self.attributes:
                attack = (a.magic + self.effect) * self.multiplier
            else:
                attack = self.effect + 20
            return attack    
            
        def get_defense(self, target):
            """
            A method to get defence value vs current attack.
            """
            if any(list(i for i in ["melee", "ranged"] if i in self.attributes)):
                defense = round(target.defence + target.constitution*0.2)
            elif "magic" in self.attributes:
                defense = round(target.magic*0.4 + target.defence*0.4 + target.constitution*0.2 + target.intelligence*0.2)
            else:
                defense = target.defence
            return defense if defense != 0 else 1
                
        def get_attributes_multiplier(self, t, attributes):
            """
            This calculates the multiplier to use with damage.
            """
            multiplier = 1.0
            effects = list()
            a = self.source
            if any(list(i for i in ["melee", "ranged"] if i in attributes)): 
                evasion_chance = round (0.5*t.level + t.agility - 0.5*a.level - a.agility)
                if evasion_chance > 0: # evasion
                    if evasion_chance > 90:
                        evasion_chance = 90
                    if dice(evasion_chance):
                        multiplier = 0
                        effects.append("missed_hit")
                elif (a.luck >= t.luck): # Critical hit, cannot be done now on higher level or too agile targets
                    if dice(round(((a.luck+50)-(t.luck+50))*0.35)):
                        multiplier += 1.5 + self.critpower # different weapons have different power of crit
                        effects.append("critical_hit")
            # Magic/Attribute alignment:
            for al in attributes:
                # Damage first:
                i = {}
                # @Review: We decided that any trait should influence this:
                for e in a.traits:
                    if al in e.el_damage:
                        i[e.id] = e.el_damage[al]
                if i:
                    i = sum(i.values()) / len(i)
                    if i > 0.15 or i < 0.15:
                        if i > 0:
                            effects.append("elemental_damage_bonus")
                        elif i < 0:
                            effects.append("elemental_damage_penalty")
                    multiplier += i
                    
                # Defence next:
                i = {}
                for e in t.traits:
                    if al in e.el_defence:
                        i[e.id] = e.el_defence[al]
                if i:
                    i = sum(i.values()) / len(i)
                    # From the perspective of the attacker...
                    if i > 0.15 or i < 0.15:
                        if i > 0:
                            effects.append("elemental_defence_penalty")
                        elif i < 0:
                            effects.append("elemental_defence_bonus")
                    multiplier -= i
                    
            return effects, multiplier
                
        def set_dmg_font_color(self, t, attributes, to_string=True, color="red"):
            """
            Sets up the color for damage graphics and returns a correct string for the log if to_string is True
            color: default to use if none found.
            attributes: list of effects to go through
            """
            # Get the color for damage font based on elemental damage:
            l = list(e for e in store.traits.itervalues() if e.id.lower() in attributes)
            if l:
                # Just need one (if by some future design there is more)
                e = l[0]
                if e.font_color:
                    color = e.font_color
            t.dmg_font = color # Set the font to pass it to show_damage_effect method, where it is reset back to red.
            return "{color=[%s]} DMG: %d {/color}" % (color, t.beeffects[0])
            
        def apply_effects(self, targets):
            # Not 100% for that this will be required...
            # Here it is simple since we are only focusing on damaging health:
            # prepare the variables:
            died = list()
            
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            for t in targets:
                if t.health - t.beeffects[0] > 0:
                    t.mod("health", -t.beeffects[0])
                else:
                    died.append(t)
                    # if t.can_die:
                        # t.health = 0 # This prolly should be moved to end routine to prevent major fuckups with teams!:
                    # else:
                    t.health = 1
                    battle.end_turn_events.append(RPG_Death(t))
                    
            return died
            
        def __call__(self, ai=False, t=None):
            self.effects_resolver(t)
            died = self.apply_effects(t)
            
            if not isinstance(died, (list, set, tuple)):
                died = list()
            
            if not battle.logical:
                self.show_gfx(t, died)
            
                for tag in self.tags_to_hide:
                    renpy.hide(tag)
                self.tags_to_hide= list()
                
        def get_element(self):
            # Returns (if any) an element bound to spell or attack:
            for t in traits:
                if t.lower() in self.attributes and t.lower() not in ["magic", "melee", "ranged"]:
                    return traits[t]
                
        # GFX/SFX:
        def show_gfx(self, targets, died):
            """Executes GFX part of an attack. Diregarded during logical combat.
            
            Usually, this has the following order:
                - Intro (attacker sprite manipulation) + Effect (attacker_effects)
                - Attack itself. (main_effects) = which is usually impact effect!
                - Visual damage effect to the target(s) (sprites shaking for example). (target_sprite_gamage_effects)
                - Some form of visual representation of damage amount (like battle bounce). (target_damage_effects)
                - Events such as death (GFX Part, event itself can be handled later). (death_effect)
                
            Through complex system currently in design we handle showing gfx/hiding gfx and managing sfx (also here).
            """
            # Try to predict the images:
            if self.attacker_effects["gfx"]:
                renpy.start_predict(self.get_attackers_first_effect_gfx())
            if self.main_effect["gfx"]:
                renpy.start_predict(self.main_effect["gfx"])
                
            # Simple effects for the magic attack:
            attacker = self.source
            battle = store.battle
            
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            
            # We need to build a dict of pause timespamp: func to call.
            self.timestamps = {}
            
            if self.attacker_action["gfx"] or self.attacker_action["sfx"]:
                delay = self.time_attackers_first_action(battle, attacker)
            
            # Next is the "casting effect":
            # Here we need to start checking for overlapping time_stamps so we don't overwrite:
            if self.attacker_effects["gfx"] or self.attacker_effects["sfx"]:
                effects_delay = self.time_attackers_first_effect(battle, attacker)
                    
            # Next is the main GFX/SFX effect! ==> We calc the start in any case because we'll need it later...            
            if "effects_delay" in locals(): # We start as effects gfx is finished.
                start = effects_delay + self.main_effect.get("start_at", 0)
            elif "delay" in locals(): # We start after atackers first action is finished.
                start = delay + self.main_effect["start_at"]
            else: # We plainly start at timestamp...
                start = self.main_effect["start_at"]
            
            # Main Effects!:
            if self.main_effect["gfx"] or self.main_effect["sfx"]:
                self.time_main_gfx(battle, attacker, targets, start)
                
            # Dodging:
            if self.dodge_effect["gfx"]: # <== Presently always True...
                self.time_dodge_effect(targets, attacker, start)
                
            # Now the damage effects to targets (like shaking):
            if self.target_sprite_damage_effect["gfx"] or self.target_sprite_damage_effect["sfx"]:
                self.time_target_sprite_damage_effect(targets, died, start)
                
            # Damage effect (battle bounce type):
            if self.target_damage_effect["gfx"] or self.target_damage_effect["sfx"]:
                self.time_target_damage_effect(targets, died, start)
                
            # And Death Effect:
            if died and (self.target_death_effect["gfx"] or self.target_death_effect["sfx"]):
                self.time_target_death_effect(died, start)
                
            # And possible BG effects:
            if self.bg_main_effect["gfx"]:
                self.time_bg_main_effect(start)
                
            time_stamps = sorted(self.timestamps.keys())
            for index, stamp in enumerate(time_stamps):
                self.timestamps[stamp]()
                try:
                    pause = time_stamps[index + 1] - stamp
                    # We do not want to pause for a super small period cause it will not work properly anyway...
                    if pause > 0.02:
                        renpy.pause(pause)
                except: # If we run out of indexes I guess...
                    pass
                
            self.timestamps = {}
            # Try to predict the images:
            if self.attacker_effects["gfx"]:
                renpy.stop_predict(self.get_attackers_first_effect_gfx())
            if self.main_effect["gfx"]:
                renpy.stop_predict(self.main_effect["gfx"])
        
        def time_attackers_first_action(self, battle, attacker):
            # Lets start with the very first part (attacker_action):
            self.timestamps[0] = renpy.curry(self.show_attackers_first_action)(battle, attacker)
            delay = self.get_show_attackers_first_action_duration() + self.get_attackers_first_effect_pause(battle, attacker)
            hide_first_action = delay + self.attacker_action.get("keep_alive_delay", 0)
            self.timestamps[hide_first_action] = renpy.curry(self.hide_attackers_first_action)(battle, attacker)
            return delay
                
        def show_attackers_first_action(self, battle, attacker):
            if self.attacker_action["gfx"] == "step_forward":
                battle.move(attacker, battle.get_cp(attacker, xo=50), 0.5, pause=False)
            
            sfx = self.attacker_action.get("sfx", None)
            if sfx:
                renpy.sound.play(sfx)
                
        def get_show_attackers_first_action_duration(self):
            if self.attacker_action["gfx"] == "step_forward":
                return 0.5
            else:
                return 0
                
        def hide_attackers_first_action(self, battle, attacker):
            if self.attacker_action["gfx"] == "step_forward":
                battle.move(attacker, attacker.dpos, 0.5, pause=False)
            
        def time_attackers_first_effect(self, battle, attacker):
            start = self.get_show_attackers_first_action_duration()
            if start in self.timestamps:
                start = start + random.uniform(0.001, 0.002)
            self.timestamps[start] = renpy.curry(self.show_attackers_first_effect)(battle, attacker)
            
            if self.attacker_effects["gfx"]:
                effects_delay = start + self.get_attackers_first_effect_pause(battle, attacker)
                if effects_delay in self.timestamps:
                    effects_delay = effects_delay + random.uniform(0.001, 0.002)
                self.timestamps[effects_delay] = renpy.curry(self.hide_attackers_first_effect)(battle, attacker)
                return effects_delay
                
            return 0
            
        def get_attackers_first_effect_gfx(self):
            gfx = self.attacker_effects["gfx"]
            if gfx == "orb":
                what=Transform("cast_orb_1", zoom=1.85)
            elif gfx in ["dark_1", "light_1", "water_1", "air_1", "fire_1", "earth_1", "electricity_1", "ice_1"]:
                what=Transform("cast_" + gfx, zoom=1.5)
            elif gfx in ["dark_2", "light_2", "water_2", "air_2", "fire_2", "earth_2", "ice_2", "electricity_2"]:
                what=Transform("cast_" + gfx, zoom=0.9)
            elif gfx == "default_1":
                what=Transform("cast_default_1", zoom=1.6)
            elif gfx == "circle_1":
                what=Transform("cast_circle_1", zoom=1.9)
            elif gfx == "circle_2":
                what=Transform("cast_circle_2", zoom=1.8)
            elif gfx == "circle_3":
                what=Transform("cast_circle_3", zoom=1.8)
            elif gfx == "runes_1":
                what=Transform("cast_runes_1", zoom=1.1)
            else:
                what=Null()
                
            return what
            
        def show_attackers_first_effect(self, battle, attacker):
            gfx, sfx = self.attacker_effects["gfx"], self.attacker_effects["sfx"]
            what = self.get_attackers_first_effect_gfx()
            
            if sfx == "default":
                sfx="content/sfx/sound/be/casting_1.mp3"
        
            if gfx == "orb":
                renpy.show("casting", what=what,  at_list=[Transform(pos=battle.get_cp(attacker, type="center"), align=(0.5, 0.5))], zorder=attacker.besk["zorder"]+1)
            elif gfx in ["dark_1", "light_1", "water_1", "air_1", "fire_1", "earth_1", "electricity_1", "ice_1"]:
                renpy.show("casting", what=what,  at_list=[Transform(pos=battle.get_cp(attacker, type="bc", yo=-75), align=(0.5, 0.5))], zorder=attacker.besk["zorder"]+1)
            elif gfx in ["dark_2", "light_2", "water_2", "air_2", "fire_2", "earth_2", "ice_2", "electricity_2"]:
                renpy.show("casting", what=what,  at_list=[Transform(pos=battle.get_cp(attacker, type="center"), align=(0.5, 0.5))], zorder=attacker.besk["zorder"]+1)
            elif gfx == "default_1":
                renpy.show("casting", what=what,  at_list=[Transform(pos=battle.get_cp(attacker, type="bc"), align=(0.5, 0.5))], zorder=attacker.besk["zorder"]-1)
            elif gfx == "circle_1":
                renpy.show("casting", what,  at_list=[Transform(pos=battle.get_cp(attacker, type="bc", yo=-10), align=(0.5, 0.5))], zorder=attacker.besk["zorder"]-1)
            elif gfx == "circle_2":
                renpy.show("casting", what=what,  at_list=[Transform(pos=battle.get_cp(attacker, type="bc", yo=-100), align=(0.5, 0.5))], zorder=attacker.besk["zorder"]+1)
            elif gfx == "circle_3":
                renpy.show("casting", what=what,  at_list=[Transform(pos=battle.get_cp(attacker, type="bc", yo=-100), align=(0.5, 0.5))], zorder=attacker.besk["zorder"]+1)
            elif gfx == "runes_1":
                renpy.show("casting", what=what,  at_list=[Transform(pos=battle.get_cp(attacker, type="bc", yo=-50), align=(0.5, 0.5))], zorder=attacker.besk["zorder"]-1)
            
            if sfx:
                renpy.sound.play(sfx)
        
        def get_attackers_first_effect_pause(self, battle, attacker):
            gfx = self.attacker_effects["gfx"]
            if gfx == "orb":
                pause = 0.84
            elif gfx in ["dark_1", "light_1", "water_1", "air_1", "fire_1", "earth_1", "electricity_1", "ice_1"]:
                pause = 0.84
            elif gfx in ["dark_2", "light_2", "water_2", "air_2", "fire_2", "earth_2", "ice_2", "electricity_2"]:
                pause = 1.4
            elif gfx == "default_1":
                pause = 1.12
            elif gfx == "circle_1":
                pause = 1.05
            elif gfx == "circle_2":
                pause = 1.1
            elif gfx == "circle_3":
                pause = 1.03
            elif gfx == "runes_1":
                pause = 0.75
            else:
                pause = 0
                
            return pause
            
        def hide_attackers_first_effect(self, battle, attacker):
            # For now we just hide the tagged image here:
            renpy.hide("casting")
        
        def time_main_gfx(self, battle, attacker, targets, start):
            if start in self.timestamps:
                start = start + random.uniform(0.001, 0.002)
            self.timestamps[start] = renpy.curry(self.show_main_gfx)(battle, attacker, targets)
            
            pause = start + self.main_effect["duration"]
            
            if pause in self.timestamps:
                pause = pause + random.uniform(0.001, 0.002)
            self.timestamps[pause] = renpy.curry(self.hide_main_gfx)(targets)
            
        def show_main_gfx(self, battle, attacker, targets):
            # Shows the MAIN part of the attack and handles appropriate sfx.
            gfx = self.main_effect["gfx"]
            sfx = self.main_effect["sfx"]
            
            # SFX:
            sfx = choice(sfx) if isinstance(sfx, (list, tuple)) else sfx
            if sfx:
                renpy.sound.play(sfx)
            
            # GFX:
            if gfx:
                # Flip the attack image if required:
                if self.main_effect.get("hflip", None):
                    gfx = Transform(gfx, xzoom=-1) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else gfx
                
                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (0.5, 0.5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)
                
                for index, target in enumerate(targets):
                    gfxtag = "attack" + str(index)
                    renpy.show(gfxtag, what=gfx, at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo), anchor=anchor)], zorder=target.besk["zorder"]+1)
                
        def hide_main_gfx(self, targets):
            for i in xrange(len(targets)):
                gfxtag = "attack" + str(i)
                renpy.hide(gfxtag)
            
        def time_target_sprite_damage_effect(self, targets, died, start):
            # We take previous start as baseppoint for execution:
            damage_effect_start = start + self.target_sprite_damage_effect["initial_pause"]
            
            if damage_effect_start in self.timestamps:
                damage_effect_start = damage_effect_start + random.uniform(0.001, 0.002)
            self.timestamps[damage_effect_start] = renpy.curry(self.show_target_sprite_damage_effect)(targets)
            
            delay = damage_effect_start + self.target_sprite_damage_effect["duration"]
            if delay in self.timestamps:
                delay = delay + random.uniform(0.001, 0.002)
            
            self.timestamps[delay] = renpy.curry(self.hide_target_sprite_damage_effect)(targets, died)
                
        def show_target_sprite_damage_effect(self, targets):
            """Target damage graphical effects.
            """
            type = self.target_sprite_damage_effect.get("gfx", "shake")
            # We want to overwrite any damage to sprite in case of a miss!
            
            for target in targets:
                if type == "shake":
                    what = target.besprite
                    at_list = [damage_shake(0.05, (-10, 10))]
                elif type == "fly_away":
                    what = target.besprite
                    at_list = [fly_away]
                elif type == "iced":
                    child = Transform("content/gfx/be/frozen.jpg", size=target.besprite_size)
                    mask = target.besprite
                    what = AlphaMask(child, mask)
                    at_list=[]
                elif type == "frozen":
                    size = (int(target.besprite_size[0]*1.5), int(target.besprite_size[1]*1.5))
                    what = Fixed(target.besprite, Transform("content/gfx/be/frozen_2.png", size=size, offset=(-30, -50)))
                    t = self.target_sprite_damage_effect.get("duration", 1)
                    at_list=[fade_from_to_with_easeout(start_val=1.0, end_val=0.2, t=t)]
                elif type == "burning":
                    child = Transform("fire_mask", size=target.besprite_size)
                    mask = target.besprite
                    what = AlphaMask(child, mask)
                    at_list=[]
                elif type == "on_fire":
                    size = (int(target.besprite_size[0]*1.1), int(target.besprite_size[1]*1.0))
                    child = damage_color(im.MatrixColor(target.besprite, im.matrix.tint(0.9, 0.2, 0.2)))
                    mask = Transform("flame_bm", size=size)
                    what = AlphaMask(child, mask)
                    at_list=[]
                elif isinstance(type, basestring) and type.startswith("fire"):
                    what = damage_color(im.MatrixColor(target.besprite, im.matrix.tint(0.9, 0.2, 0.2)))
                    if type == "fire":
                        at_list = []
                    elif type == "fire_shake":
                        at_list=[damage_shake(0.05, (-10, 10))]
                
                if "what" in locals() and not "missed_hit" in target.beeffects:
                    renpy.show(target.betag, what=what, at_list=at_list, zorder=target.besk["zorder"])
                    
        def hide_target_sprite_damage_effect(self, targets, died):
            # Hides damage effects applied to targets:
            type = self.target_sprite_damage_effect.get("gfx", "shake")
            if type == "frozen":
                for target in targets:
                    if target not in died:
                        renpy.hide(target.betag)
                        renpy.show(target.betag, what=target.besprite, at_list=[Transform(pos=target.cpos), fade_from_to(0.3, 1, 0.3)], zorder=target.besk["zorder"])
            else:
                for target in targets:
                    if target not in died:
                        renpy.hide(target.betag)
                        renpy.show(target.betag, what=target.besprite, at_list=[Transform(pos=target.cpos)], zorder=target.besk["zorder"])
            
        def time_target_damage_effect(self, targets, died, start):
            damage_effect_start = start + self.target_damage_effect.get("initial_pause", 0.2)
            
            if damage_effect_start in self.timestamps:
                damage_effect_start = damage_effect_start + random.uniform(0.001, 0.002)
            self.timestamps[damage_effect_start] = renpy.curry(self.show_target_damage_effect)(targets, died)
            
            delay = damage_effect_start + self.get_target_damage_effect_duration()
            if delay in self.timestamps:
                delay = delay + random.uniform(0.001, 0.002)
            
            self.timestamps[delay] = renpy.curry(self.hide_target_damage_effect)(targets, died)
                    
        def show_target_damage_effect(self, targets, died):
            """Easy way to show damage like the bouncing damage effect.
            """
            type = self.target_damage_effect.get("gfx", "battle_bounce")
            force = self.target_damage_effect.get("force", False)
            if type == "battle_bounce":
                for index, target in enumerate(targets):
                    if target not in died or force:
                        tag = "bb" + str(index)
                        if "missed_hit" in target.beeffects:
                            s = "Missed"
                            color = getattr(store, target.dmg_font)
                        else:
                            s = "%s"%target.beeffects[0]
                            if "critical_hit" in target.beeffects:
                                s = "\n".join([s, "Critical hit!"])
                            color = getattr(store, target.dmg_font)
                        txt = Text(s, style="TisaOTM", min_width=200, text_align=0.5, color=color, size=18)
                        renpy.show(tag, what=txt, at_list=[battle_bounce(battle.get_cp(target, type="tc", yo=-20))], zorder=target.besk["zorder"]+2)
                        target.dmg_font = "red"
            
        def get_target_damage_effect_duration(self):
            type = self.target_damage_effect.get("gfx", "battle_bounce")
            if type == "battle_bounce":
                delay = 1.5
            else:
                delay = 0
                
            return delay
             
        def hide_target_damage_effect(self, targets, died):
            for index, target in enumerate(targets):
                if target not in died:
                    tag = "bb" + str(index)
                    renpy.hide(tag)
            
        def time_target_death_effect(self, died, start):
            death_effect_start = start + self.target_death_effect["initial_pause"]
            
            if death_effect_start in self.timestamps:
                death_effect_start = death_effect_start + random.uniform(0.001, 0.002)
            self.timestamps[death_effect_start] = renpy.curry(self.show_target_death_effect)(died)
            
            delay = death_effect_start + self.target_death_effect["duration"]
            if delay in self.timestamps:
                delay = delay + random.uniform(0.001, 0.002)
            
            self.timestamps[delay] = renpy.curry(self.hide_target_death_effect)(died)
                    
        def show_target_death_effect(self, died):
            gfx = self.target_death_effect["gfx"]
            sfx = self.target_death_effect["sfx"]
            duration = self.target_death_effect["duration"]
            
            if sfx:
                renpy.sound.play(sfx)
                
            if gfx == "dissolve":
                for t in died:
                    renpy.show(t.betag, what=t.besprite, at_list=[fade_from_to(start_val=1.0, end_val=0.0, t=duration)], zorder=t.besk["zorder"])
            elif gfx == "shatter":
                for target in died:
                    renpy.show(target.betag, what=HitlerKaputt(target.besprite, 20), zorder=target.besk["zorder"])
                
        def hide_target_death_effect(self, died):
            for target in died:
                renpy.hide(target.betag)
            
        def time_bg_main_effect(self, start):
            effect_start = start + self.bg_main_effect["initial_pause"]
            
            if effect_start in self.timestamps:
                effect_start = effect_start + random.uniform(0.001, 0.002)
            self.timestamps[effect_start] = self.show_bg_main_effect
            
            delay = effect_start + self.bg_main_effect["duration"]
            if delay in self.timestamps:
                delay = delay + random.uniform(0.001, 0.002)
            
            self.timestamps[delay] = self.hide_bg_main_effect
                    
        def show_bg_main_effect(self):
            gfx = self.bg_main_effect["gfx"]
            sfx = self.bg_main_effect.get("sfx", None)
            
            if sfx:
                renpy.sound.play(sfx)
                
            if gfx in ["mirrage"]:
                battle.bg.change(gfx)
            if gfx in ["black"]:
                renpy.with_statement(None)
                renpy.show("bg", what=Solid("#000000"))
                renpy.with_statement(dissolve)
                # renpy.pause(0.5)
                
        def hide_bg_main_effect(self):
            gfx = self.bg_main_effect["gfx"]
            if gfx in ["mirrage"]:
                battle.bg.change("default")
            if gfx in ["black"]:
                renpy.with_statement(None)
                renpy.show("bg", what=battle.bg)
                renpy.with_statement(dissolve)
            
            
        def time_dodge_effect(self, targets, attacker, start):
            effect_start = start - 0.3
            if effect_start < 0:
                effect_start = 0
            
            if effect_start in self.timestamps:
                effect_start = effect_start + random.uniform(0.001, 0.002)
            self.timestamps[effect_start] = renpy.curry(self.show_dodge_effect)(attacker, targets)
            
            # delay = effect_start + self.bg_main_effect["duration"]
            # if delay in self.timestamps:
                # delay = delay + random.uniform(0.001, 0.002)
            
            # self.timestamps[delay] = self.hide_bg_main_effect
                    
        def show_dodge_effect(self, attacker,  targets):
            # gfx = self.dodge_effect["gfx"]
            # sfx = self.dodge_effect.get("sfx", None)
            
            # if sfx:
                # renpy.sound.play(sfx)
                
            for target in targets:
                if "missed_hit" in target.beeffects:
                    xoffset = -100 if battle.get_cp(attacker)[0] > battle.get_cp(target)[0] else 100
                    renpy.show(target.betag, what=target.besprite, at_list=[be_dodge(xoffset)], zorder=target.besk["zorder"])
                
        def hide_dodge_effect(self):
            pass
            
            
    class BE_AI(object):
        # Not sure this even needs to be a class...
        def __init__(self, source):
            self.source = source
        
        def __call__(self):
            skills = self.get_skills()
            if skills:
                skill = choice(skills)
                # So we have a skill... now lets pick a taget(s):
                skill.source = self.source
                targets = skill.get_targets() # Get all targets in range.
                targets = targets if "all" in skill.type else choice(targets) # We get a correct amount of targets here.
                
                skill(ai=True, t=targets)
                
            else:
                skill = BE_Skip(source=self.source)
                skill()
        
        def get_skills(self):
            allskills = self.source.attack_skills + self.source.magic_skills
            skills = [s for s in allskills if s.check_conditions(self.source)]
            
            # for skill in allskills:
                # t = skill.get_targets(source=self.source)
                # if t:
                    # skills.append(skill)
                     
            # for skill in skills[:]:
                # skill.source = self.source
                # if not skill.check_conditions():
                    # skills.remove(skill)
            return skills
