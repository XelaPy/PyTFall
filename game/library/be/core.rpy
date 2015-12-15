init -1 python: # Core classes:
    battle_skills = {}
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
            
            logical: Just the calculations, without pause/gfx/sfx. Does not work yet.
            """
            self.teams = list() # Each team represents a faction on the battlefield. 0 index for left team and 1 index for right team.
            self.queue = list() # List of events in BE..
            self.bg = bg # Background we'll use.
                
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
                        # This character is not controled by the player so we call the controller:
                        ev.controller()
                    else:
                        # Controller is the player:
                        # Call the skill choice screen:
                        s = renpy.call_screen("pick_skill", ev)
                        s.source = ev
                        # Ok, so now we got the skll... so we call it.
                        s()
                
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
            """
            Should return True/False to allow event execution.
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
        """
        Basic action class that assumes that there will be targeting of some kind and followup logical and graphical effects.
        """
        def __init__(self, name, range=1, source=None, type="se", piercing=False, multiplier=1, true_pierce=False,
                           menuname=None, critpower=0, menucat="Attacks", sfx=None, gfx=None, attributes=[], effect=0, zoom=None,
                           add2skills=True, td_gfx=None, desc="", death_effect=None, **kwrags):
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
            self.name = name
            if not menuname:
                self.mn = self.name
            else:
                self.mn = menuname
            self.manucat = menucat    
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
            
            self.sfx = sfx # This is for really simple attacks.
            self.gfx = gfx # This is for really simple attacks.
            if td_gfx:
                self.td_gfx = td_gfx # A list of pause --> kind of effect --> end of effect. **If this gets any more complicated, gfx method might have to become at/st funciton.
            else:
                self.td_gfx = [0.1] # This will be used to control damage bounce.
            # Zoom:
            # Zoom factors the size of the main displayable of the attack (if there is one). Use floats, 1.0 represents original size, -1 will invert (flip) the image.
            self.zoom = zoom
            
            self.tags_to_hide = list() # BE effects tags of all kinds, will be hidden when the show gfx method runs it's cource and cleared for the next use.
            
            if add2skills:
                battle_skills[self.name] = self
        
        def get_targets(self, source=None):
            """
            Gets tagets that can be hit with this action.
            Rows go [0, 1, 2, 3] from left to right of the battle-field.
            """
            if source:
                char = source
            else:
                char = self.source
                
            # First figure out all targets within the range:
            # We calculate this by assigning.
            target_rows = range(char.row - self.range, char.row + 1 + self.range)
            in_range = set(f for f in battle.get_fighters() if f.row in target_rows)
                    
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
                                
            # In a perfect world, we're done, however we have to overwrite normal rules if no targets are found and backrow can hit over it's own range (for example):
            if not in_range:
                # Another step is to allow any range > 1 backrow attack and any frontrow attack hitting backrow of the opfor...
                # and... if there is noone if front row, allow longer reach fighters in backrow even if their range normally would not allow it.
                if char.row == 0:
                    # Case: Fighter in backrow and no defenders on opfor.
                    if not battle.get_fighters(rows=[2]) and self.range > 1:
                        # We add everyone in the back row for target practice :)
                        in_range = in_range.union(battle.get_fighters(rows=[3]))
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
                
            # Now the type, we just care about friends and enemies:
            if self.type in ["all_enemies", "se"]:
                in_range = [f for f in in_range if char.allegiance != f.allegiance]
            elif self.type in ["all_allies", "sa"]:
                in_range = [f for f in in_range if char.allegiance == f.allegiance]
                    
            return list(in_range) # So we can support indexing...
            
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
                        damage = damage * -1 * result
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
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            for t in targets:
                if t.health - t.beeffects[0] > 0:
                    t.mod("health", t.beeffects[0] * -1)
                else:
                    if t.can_die:
                        t.health = 0
                    else:
                        t.health = 1
                    battle.end_turn_events.append(RPG_Death(t))
            
        def __call__(self):
            # Call the targeting screen:
            targets = self.get_targets()
            t = renpy.call_screen("target_practice", self, targets)
            self.show_gfx(t)
            
            for tag in self.tags_to_hide:
                renpy.hide(tag)
            self.tags_to_hide= list()
                    
        def show_gfx(self):
            """
            All graphical effects for the action.
            """
            pass
        
        def show_gfx_td(self, target, t, type="shake"):
            """
            This is separated from the show gfx function... Maybe setup for the attack should be separated as well... TODO: Decide!
            Target damage graphical effects.
            t: Time
            type: Which effect to apply.
            """
            if type == "shake":
                renpy.show(target.betag, what=target.besprite, at_list=[damage_shake(0.05, (-10, 10))], zorder=target.besk["zorder"])
        
        def show_gfx_dmg(self, target, type="bb"):
            """
            Easy way to show damage like the bouncing damage effect.
            """
            if type == "bb":
                bbtag = "bb" + str(random.random())
                self.tags_to_hide.append(bbtag)
                txt = Text("%s"%target.beeffects[0], style="content_label", color=getattr(store, target.dmg_font), size=15)
                renpy.show(bbtag, what=txt, at_list=[battle_bounce(battle.get_cp(target, type="tc", yo=-10))], zorder=target.besk["zorder"]+2)
                target.dmg_font = "red"
                
        def get_element(self):
            # Returns (if any) an element bound to spell or attack:
            for t in traits:
                if t.lower() in self.attributes and t.lower() not in ["magic", "melee", "ranged"]:
                    return traits[t]
            # element = set(["fire", "air", "water", "earth", "darkness", "light", "neutral"]) & set(self.attributes)
            # if element:
                # return element.pop()
                
        
                
    class BE_AI(object):
        # Not sure this even needs to be a class...
        def __init__(self, source):
            self.source = source
        
        def __call__(self):
            skills = self.get_skills()
            if skills:
                skill = choice(skills)
                # So we have a skill... not lets pick a taget(s):
                skill.source = self.source
                targets = skill.get_targets()
                if "all" in skill.type:
                    skill.show_gfx(targets)
                else:
                    skill.show_gfx(choice(targets))
                
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
