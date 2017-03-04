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
    perfect_middle_xr = BDP["r0"][1][0] + (BDP["r1"][1][0] - BDP["r0"][1][0])
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
        def __init__(self, bg=Null(), music=None, row_pos=None, start_sfx=None, end_sfx=None, logical=False, quotes=False, max_skill_lvl=float("inf")):
            """Creates an instance of BE scenario.

            logical: Just the calculations, without pause/gfx/sfx.
            """
            self.teams = list() # Each team represents a faction on the battlefield. 0 index for left team and 1 index for right team.
            self.queue = list() # List of events in BE..

            self.bg = ConsitionSwitcher("default", {"default": bg, "black": Solid("#000000"), "mirage": Mirage(bg, resize=get_size(bg), amplitude=0.04, wavelength=10, ycrop=10)}) # Background we'll use.

            if music == "random":
                self.music = choice(ilists.battle_tracks)
            else:
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
            self.start_turn_events = list() # Events we execute on start of the turn.
            self.mid_turn_events = list() # Events we execute on the end of the turn.
            self.end_turn_events = list() # Events to execute after controller was set.
            self.terminate = False

            self.logical = logical
            self.logical_counter = 0
            self.quotes = quotes # Decide if we run quotes at the start of the battle.

            self.start_sfx = start_sfx
            self.end_sfx = end_sfx

            self.max_skill_lvl = max_skill_lvl

        def log(self, report):
            if config.debug:
                devlog.info(report)
            self.combat_log.append(report)

        def get_faction(self, char):
            # Since factions are simply teams:
            for team in self.teams:
                if char in team:
                    return team

        def main_loop(self):
            """
            Handles events on the battlefield until something that can break the loop is found.
            """
            while 1:
                # We run events queued at the start of the turn first:
                for event in self.start_turn_events[:]:
                    if event():
                        self.start_turn_events.remove(event)

                fighter = self.controller = self.next_turn()

                for event in self.mid_turn_events[:]:
                    if event():
                        self.mid_turn_events.remove(event)

                # If the controller was killed off during the mid_turn_events:
                if fighter not in self.corpses:
                    if fighter.controller != "player":
                        # This character is not controled by the player so we call the (AI) controller:
                        fighter.controller()
                    else:
                        # Controller is the player:
                        # Call the skill choice screen:
                        s = None
                        t = None

                        # making known whos turn it is:
                        w, h = fighter.besprite_size
                        renpy.show("its_my_turn", at_list=[Transform(additive=.6, alpha=.7, size=(int(w*1.5), h/3), pos=battle.get_cp(fighter, type="bc", yo=20), anchor=(.5, 1.0))], zorder=fighter.besk["zorder"]+1)

                        while not (s and t):
                            s = renpy.call_screen("pick_skill", fighter)
                            s.source = fighter

                            # Unique check for Skip Skill:
                            if isinstance(s, BE_Skip):
                                break

                            # Call the targeting screen:
                            targets = s.get_targets()

                            t = renpy.call_screen("target_practice", s, fighter, targets)

                        # We don't need to see status icons during skill executions!
                        if not self.logical:
                            renpy.hide_screen("be_status_overlay")
                            renpy.hide("its_my_turn")
                        s(t=t) # This actually executes the skill!
                        if not self.logical:
                            renpy.show_screen("be_status_overlay")

                if not self.logical:
                    renpy.hide_screen("pick_skill")
                    renpy.hide_screen("target_practice")

                # End turn events, Death (Usually) is added here for example.
                for event in self.end_turn_events[:]:
                    if event():
                        self.end_turn_events.remove(event)

                self.logical_counter += 1

                if config.debug and self.logical:
                    temp = "Debug: Loop: %d, TLeft: %d, TRight: %d"%(self.logical_counter, len(self.get_fighters(state="dead", rows=(0, 1))),  len(self.get_fighters(state="dead", rows=(2, 3))))
                    temp += ", ".join([str(i.health) for i in self.teams[0]])
                    self.log(temp)

                for event in self.get_all_events():
                    if hasattr(event, "activated_this_turn"):
                        event.activated_this_turn = False

                # We check the conditions for terminating the BE scenario, this should prolly be end turn event as well, but I've added this before I've added events :)
                if self.check_break_conditions():
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
                renpy.show_screen("battle_overlay", self)
                renpy.show_screen("be_status_overlay")
                if self.start_sfx: # Special Effects:
                    renpy.with_statement(self.start_sfx)

                if self.quotes:
                    self.start_turn_events.append(RunQuotes(self.teams[0]))

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
                renpy.hide_screen("be_status_overlay")
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
                    # i.besprite_size = None
                    i.status_overlay = [] # Clear the overlay.

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
            # char.besprite_size = sprite.true_size()

            # We'll assign "indexes" from 0 to 3 from left to right [0, 1, 3, 4] to help calculating attack ranges.
            team_index = team.position
            char_index = char.beinx
            if team_index:
                if char.__class__ == Mob:
                    if isinstance(sprite, ProportionalScale):
                        char.besprite = im.Flip(sprite, horizontal=True)
                    else:
                        char.besprite = Transform(sprite, xzoom=-1)
                else:
                    char.besprite = sprite

                # We're going to land the character at the default position from now on, with centered buttom of the image landing directly on the position!
                # This makes more sense for all purposes:
                char.dpos = self.row_pos[team_index + str(int(char.front_row))][char_index]
                char.cpos = char.dpos

            if team_index == "r":
                if char.__class__ != Mob:
                    if isinstance(sprite, ProportionalScale):
                        char.besprite = im.Flip(sprite, horizontal=True)
                    else:
                        char.besprite = Transform(sprite, xzoom=-1)
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
            sopos: This is tc of default character position. Used to place status overlay icons.
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

                if type == "sopos":
                    xpos = char.dpos[0] + char.besprite_size[0] / 2
                    ypos = char.dpos[1] + yo

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

        def check_break_conditions(self):
            # Checks if any specific condition is reached.
            # Should prolly be turned into a function when this gets complicated, for now it's just fighting until one of the party are "corpses".
            # For now this assumes that team indexed 0 is player team.
            if self.terminate:
                return True
            if self.logical and self.logical_counter >= 1000:
                self.winner = self.teams[1]
                self.log("Battle went on for far too long! %s is concidered the winner!" % self.winner.name)
                return True
            if len(self.teams[0]) == len(self.get_fighters(state="dead", rows=(0, 1))):
                self.winner = self.teams[1]
                self.log("%s is victorious!" % self.winner.name)
                return True
            if len(self.teams[1]) == len(self.get_fighters(state="dead", rows=(2, 3))):
                self.winner = self.teams[0]
                self.log("%s is victorious!" % self.winner.name)
                return True

        def get_all_events(self):
            # returns a list of all events on this battle field:
            return self.start_turn_events + self.mid_turn_events + self.end_turn_events


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
        DELIVERY = set(["magic", "ranged", "melee", "status"]) # Damage/Effects Delivery Methods!
        DAMAGE = {"physical": "{image=physical_be_viewport}", "fire": "{image=fire_element_be_viewport}", "water": "{image=water_element_be_viewport}",
                  "ice": "{image=ice_element_be_viewport}", "earth": "{image=earth_element_be_viewport}", "air": "{image=air_element_be_viewport}",
                  "electricity": "{image=ele_element_be_viewport}", "light": "{image=light_element_be_viewport}", "darkness": "{image=darkness_element_be_viewport}",
                  "healing": "{image=healing_be_viewport}", "poison": "{image=poison_be_viewport}"} # Damage (Effect) types...
        DAMAGE_20 = {"physical": "{image=physical_be_size20}", "fire": "{image=fire_element_be_size20}", "water": "{image=water_element_be_size20}",
                     "ice": "{image=ice_element_be_size20}", "earth": "{image=earth_element_be_size20}", "air": "{image=air_element_be_size20}",
                     "electricity": "{image=ele_element_be_size20}", "light": "{image=light_element_be_size20}", "darkness": "{image=darkness_element_be_size20}",
                     "healing": "{image=healing_be_size20}", "poison": "{image=poison_be_size20}"}

        def __init__(self, name, mp_cost=0, health_cost=0, vitality_cost=0, kind="assault",
                           range=1, source=None, type="se", piercing=False, multiplier=1, true_pierce=False,
                           menuname=None, critpower=0, sfx=None, gfx=None, attributes=[], effect=0, zoom=None,
                           add2skills=True, desc="", pause=0, target_state="alive", menu_pos=0,
                           attacker_action={},
                           attacker_effects={},
                           main_effect={},
                           dodge_effect={},
                           target_sprite_damage_effect={},
                           target_damage_effect={},
                           target_death_effect={},
                           bg_main_effect={},
                           event_class = None, # If a class, instance of this even will be created and placed in the queue. This envokes special checks in the effects method.
                           **kwargs):
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
            self.kind = kind
            self.menu_pos = menu_pos # Skill level might be a better name.
            if not menuname:
                self.mn = self.name
            else:
                self.mn = menuname

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
            self.desc = desc
            self.target_state = target_state

            self.event_class = event_class

            try:
                self.delivery = self.DELIVERY.intersection(self.attributes).pop()
            except:
                self.delivery = ""

            self.damage = [d for d in self.attributes if d in self.DAMAGE]

            self.tags_to_hide = list() # BE effects tags of all kinds, will be hidden when the show gfx method runs it's cource and cleared for the next use.

            if add2skills:
                battle_skills[self.name] = self

            # GFX/SFX + Dicts:
            self.timestamps = {} # We keep all gfx effects here!

            # Normalize:
            self.attacker_action = attacker_action.copy()
            self.attacker_action["gfx"] = self.attacker_action.get("gfx", "step_forward")
            self.attacker_action["sfx"] = self.attacker_action.get("sfx", None)

            self.attacker_effects = attacker_effects.copy()
            self.attacker_effects["gfx"] = attacker_effects.get("gfx", None)
            self.attacker_effects["sfx"] = attacker_effects.get("sfx", None)

            dp = deepcopy(main_effect)
            self.main_effect = dp
            self.main_effect["gfx"] = main_effect.get("gfx", None)
            self.main_effect["sfx"] = main_effect.get("sfx", None)
            self.main_effect["start_at"] = main_effect.get("start_at", 0)
            self.main_effect["aim"] = dp.get("aim", {})
            if self.delivery in ["melee", "ranged"]:
                self.main_effect["duration"] = main_effect.get("duration", .1)
            else:
                self.main_effect["duration"] = main_effect.get("duration", .5)

            self.dodge_effect = dodge_effect.copy()
            self.dodge_effect["gfx"] = dodge_effect.get("gfx", "dodge")

            self.target_sprite_damage_effect = target_sprite_damage_effect.copy()
            self.target_sprite_damage_effect["gfx"] = target_sprite_damage_effect.get("gfx", "shake")
            self.target_sprite_damage_effect["duration"] = target_sprite_damage_effect.get("duration", self.main_effect["duration"])
            self.target_sprite_damage_effect["sfx"] = target_sprite_damage_effect.get("sfx", None)
            if self.delivery in ["melee", "ranged"]:
                self.target_sprite_damage_effect["initial_pause"] = target_sprite_damage_effect.get("initial_pause", 0.1)
            else:
                self.target_sprite_damage_effect["initial_pause"] = target_sprite_damage_effect.get("initial_pause", 0.2)

            self.target_damage_effect = target_damage_effect.copy()
            self.target_damage_effect["gfx"] = target_damage_effect.get("gfx", "battle_bounce")
            self.target_damage_effect["sfx"] = target_damage_effect.get("sfx", None)
            if not self.delivery in ["melee", "ranged"]:
                self.target_damage_effect["initial_pause"] = self.target_damage_effect.get("initial_pause", .21)

            self.target_death_effect = target_death_effect.copy()
            self.target_death_effect["gfx"] = target_death_effect.get("gfx", "dissolve")
            self.target_death_effect["duration"] = self.target_death_effect.get("duration", 0.5)
            self.target_death_effect["sfx"] = target_death_effect.get("sfx", None)
            if self.delivery in ["melee", "ranged"]:
                self.target_death_effect["initial_pause"] = target_death_effect.get("initial_pause", .2)
            else:
                self.target_death_effect["initial_pause"] = target_death_effect.get("initial_pause", self.target_sprite_damage_effect["initial_pause"] + 0.1)

            self.bg_main_effect = bg_main_effect.copy()
            self.bg_main_effect["gfx"] = bg_main_effect.get("gfx", None)
            if self.bg_main_effect["gfx"]:
                self.bg_main_effect["initial_pause"] = self.bg_main_effect.get("initial_pause", self.main_effect["start_at"])
                self.bg_main_effect["duration"] = self.bg_main_effect.get("duration", main_effect.get("duration", .4))

            # Cost of the attack:
            self.mp_cost = mp_cost
            if not(isinstance(health_cost, int)) and health_cost > 0.9:
                self.health_cost = 0.9
            else:
                self.health_cost = health_cost
            self.vitality_cost = vitality_cost

        def __call__(self, ai=False, t=None):
            self.effects_resolver(t)
            died = self.apply_effects(t)

            if not isinstance(died, (list, set, tuple)):
                died = list()

            if not battle.logical:
                self.time_gfx(t, died)

                for tag in self.tags_to_hide:
                    renpy.hide(tag)
                self.tags_to_hide= list()

            # Clear (maybe move to separate method if this ever gets complicated), should be moved to core???
            for f in battle.get_fighters(state="all"):
                f.beeffects= []

        # Targeting/Conditioning.
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
            if not in_range: # <== We need to run "frenemy" code prior to this!
                # Another step is to allow any range > 1 backrow attack and any frontrow attack hitting backrow of the opfor...
                # and... if there is noone if front row, allow longer reach fighters in backrow even if their range normally would not allow it.
                if char.row == 0:
                    # Case: Fighter in backrow and there is no defender on own team:
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
            """Checks if the source can manage the attack."""
            char = source if source else self.source

            # Indoor check:
            if self.menu_pos >= battle.max_skill_lvl:
                return False

            # Check if attacker has enought resources for the attack:
            if not isinstance(self.mp_cost, int):
                mp_cost = int(char.get_max("mp")*self.mp_cost)
            else:
                mp_cost = self.mp_cost

            if not isinstance(self.health_cost, int):
                health_cost = int(char.get_max("health")*self.health_cost)
            else:
                health_cost = self.health_cost

            if not isinstance(self.vitality_cost, int):
                vitality_cost = int(char.get_max("vitality")*self.vitality_cost)
            else:
                vitality_cost = self.vitality_cost

            # We need to make sure that we have enough resources for this one:
            # Making sure we cannot kill the source by taking off all the health:
            if (char.mp - mp_cost >= 0) and (char.health - health_cost > 0) and (char.vitality - vitality_cost >= 0):
                if self.get_targets(char):
                    return True

        # Logical Effects:
        def effects_resolver(self, targets):
            """Logical effect of the action.

            - For normal attacks, it calculates the damage.
            Expects a list or tuple with targets.
            This should return it's results through PytCharacters property called damage so the show_gfx method can be adjusted accordingly.
            But it is this method that writes to the log to be displayed later... (But you can change even this :D)
            """
            # prepare the variables:
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]

            a = self.source
            attributes = self.attributes

            attacker_items = a.eq_items()

            # Get the attack power:
            attack = self.get_attack()
            name = self.name

            # DAMAGE Mods:
            if self.damage:
                attack = attack/len(self.damage)

            for t in targets:
                # effect list must be cleared here first thing... preferebly in the future, at the end of each skill execution...
                effects = t.beeffects

                defense = self.get_defense(t)
                if self.damage:
                    defense = defense/len(self.damage)

                # We get the multiplier and any effects that those may bring.
                multiplier = 1.0
                total_damage = 0

                # Critical Strike and Evasion checks:
                if self.delivery in ["melee", "ranged"]:
                    # Critical Hit Chance:
                    ch = max(35, (a.luck - t.luck + 10) * .75) # No more than 35% chance? Dark: we can add items/traits field capable to increase the max chance of crit hit

                    # Items bonuses:
                    m = .0
                    for i in attacker_items:
                        if hasattr(i, "ch_multiplier"):
                            m += i.ch_multiplier
                    ch += 100*m

                    # Traits bonuses:
                    m = .0
                    for i in a.traits:
                        if hasattr(i, "ch_multiplier"):
                            m += i.ch_multiplier
                    ch += 100*m

                    if dice(ch):
                        multiplier += 1.5 + self.critpower
                        effects.append("critical_hit")
                    elif ("inevitable" not in attributes): # inevitable attribute makes skill/spell undodgeable/unresistable
                        ev = min(t.agility*.05-a.agility*.05, 15) + max(0, min(t.luck-a.luck, 15)) # Max 15 for agility and luck each...

                        # Items bonuses:
                        temp = 0
                        for i in t.eq_items():
                            if hasattr(i, "evasion_bonus"):
                                temp += i.evasion_bonus
                        ev += temp

                        # Traits Bonuses:
                        temp = 0
                        for i in t.traits:
                            if hasattr(i, "evasion_bonus"):
                                # Reference: (minv, maxv, lvl)
                                minv, maxv, lvl = i.evasion_bonus
                                if lvl <= 0:
                                    lvl = 1
                                if lvl >= t.level:
                                    temp += maxv
                                else:
                                    temp += max(minv, float(t.level)*maxv/lvl)
                        ev += temp

                        if t.health <= t.get_max("health")*0.25:
                            ev += randint(1,5) # very low health provides additional random evasion, 1-5%

                        if dice(ev):
                            effects.append("missed_hit")
                            self.log_to_battle(effects, 0, a, t, message=None)
                            continue

                # Rows Damage:
                if self.row_penalty(t):
                    multiplier *= .5
                    effects.append("backrow_penalty")

                for type in self.damage:

                    result = self.damage_modifier(t, attack, type) # Can return a number or "resisted" string

                    # Resisted:
                    if result == "resisted":
                        effects.append((type, result))
                        continue

                    # We also check for absorbsion:
                    absorb_ratio = self.check_absorbtion(t, type)
                    if absorb_ratio:
                        result = -(absorb_ratio)*result
                        # We also set defence to 1, no point in defending against absorbtion:
                        temp_def = 1
                    else:
                        temp_def = defense

                    # Get the damage:
                    result = self.damage_calculator(t, result, temp_def, multiplier, attacker_items)

                    effects.append((type, result))
                    total_damage += result

                if self.event_class:
                    # Check if event is in play already:
                    # Check for resistance first:
                    temp = self.event_class(a, t, total_damage)
                    if temp.type in t.resist or self.check_absorbtion(t, temp.type):
                        pass
                    else:
                        for event in store.battle.mid_turn_events:
                            if (isinstance(event, self.event_class) and t == event.target): # TODO: Add field to event that would allow being hit multiple times?
                                # battle.log("%s is already poisoned!" % (t.nickname)) # TODO: Add reports to events? So they make sense?
                                break
                        else:
                            battle.mid_turn_events.append(temp)

                # Finally, log to battle:
                self.log_to_battle(effects, total_damage, a, t, message=None)

        def row_penalty(self, t):
            # It's always the normal damage except for rows 0 and 3 (unless everyone in the front row are dead :) ).
            # Adding true_piece there as well:
            if t.row == 3:
                if battle.get_fighters(rows=[2]) and not self.true_pierce:
                    return True
            if t.row == 0:
                if battle.get_fighters(rows=[1]) and not self.true_pierce:
                    return True

        def check_absorbtion(self, t, type):
            # Get all absorption capable traits:
            l = list(trait for trait in t.traits if trait.el_absorbs)

            # # Get ratio:
            ratio = []
            for trait in l:
                if type in trait.el_absorbs:
                    ratio.append(trait.el_absorbs[type])
            if ratio:
                return sum(ratio) / len(ratio)
            else:
                return None

        def get_attack(self):
            """
            Very simple method to get to attack power.
            """
            a = self.source

            if "melee" in self.attributes:
                attack = (a.attack*0.75 + a.agility*.5 + self.effect) * self.multiplier
            elif "ranged" in self.attributes:
                attack = (a.agility*0.7 + a.attack*.5 + (a.luck+50)*.5 + self.effect) * self.multiplier
            elif "magic" in self.attributes:
                attack = (a.magic*0.75 + a.intelligence*.5 + self.effect) * self.multiplier
            elif "status" in self.attributes:
                attack = (a.intelligence*0.75 + a.attack*.25 + a.agility*.25 + self.effect) * self.multiplier

            delivery = self.delivery

            # Items bonuses:
            m = 1.0
            items = a.eq_items()
            for i in items:
                if hasattr(i, "delivery_bonus"):
                    attack = attack + i.delivery_bonus.get(delivery, 0)
                if hasattr(i, "delivery_multiplier"):
                    m = m + i.delivery_multiplier.get(delivery, 0)
            attack = attack * m

            # Trait Bonuses:
            m = 1.0
            for i in a.traits:
                if hasattr(i, "delivery_bonus"):
                    # Reference: (minv, maxv, lvl)
                    if self.delivery in i.delivery_bonus:
                        minv, maxv, lvl = i.delivery_bonus[self.delivery]
                        if lvl <= 0:
                            lvl = 1
                        if lvl >= a.level:
                            attack += maxv
                        else:
                            attack += max(minv, float(a.level)*maxv/lvl)
                if hasattr(i, "delivery_multiplier"):
                    m = m + i.delivery_multiplier.get(self.delivery, 0)
            attack *= m

            # Simple randomization factor?:
            # attack *= random.uniform(.90, 1.10) # every time attack is random from 90 to 110% Alex: Why do we do this? Dark: we make damage calculations unpredictable (within reasonable limits); many games use much more harsh ways to add randomness to BE.

            # Decreasing based of current health:
            # healthlevel=(1.0*a.health)/(1.0*a.get_max("health"))*0.5 # low health decreases attack power, down to 50% at close to 0 health.
            # attack *= (0.5+healthlevel)

            return int(attack) if attack >= 1 else 1

        def get_defense(self, target):
            """
            A method to get defence value vs current attack.
            """
            if "melee" in self.attributes:
                defense = round(target.defence*.8 + target.constitution*.4)
            elif "ranged" in self.attributes:
                defense = round(target.defence*.8 + target.constitution*.2 + target.agility*.2)
            elif "magic" in self.attributes:
                defense = round(target.defence*.5 + target.magic*.5 + target.intelligence*.2)
            elif "status" in self.attributes:
                defense = round(target.defence*.6 + target.magic*.3 + target.intelligence*.3)

            # Items bonuses:
            items = target.eq_items()
            m = 1.0
            for i in items:
                if hasattr(i, "defence_bonus"):
                    defense = defense + i.defence_bonus.get(self.delivery, 0)
                if hasattr(i, "defence_multiplier"):
                    m = m + i.defence_multiplier.get(self.delivery, 0)
            defense *= m

            # Trait Bonuses:
            m = 1.0
            for i in target.traits:
                if hasattr(i, "defence_bonus"):
                    # Reference: (minv, maxv, lvl)
                    if self.delivery in i.defence_bonus:
                        minv, maxv, lvl = i.defence_bonus[self.delivery]
                        if lvl <= 0:
                            lvl = 1
                        if lvl >= target.level:
                            defense += maxv
                        else:
                            defense += max(minv, float(target.level)*maxv/lvl)
                if hasattr(i, "defence_multiplier"):
                    if i in target.traits.basetraits and len(target.traits.basetraits)==1:
                        m = m + 2*i.defence_multiplier.get(self.delivery, 0)
                    else:
                        m = m + i.defence_multiplier.get(self.delivery, 0)
            defense *= m

            # Testing status mods through be skillz:
            m = 1.0
            d = 0
            for event in battle.get_all_events():
                if event.target == target:
                    if hasattr(event, "defence_bonus"):
                        d += event.defence_bonus.get(self.delivery, 0)
                        event.activated_this_turn = True
                    if hasattr(event, "defence_multiplier"):
                        m = m + event.defence_multiplier.get(self.delivery, 0)
                        event.activated_this_turn = True

            if d or m != 1.0:
                target.beeffects.append("magic_shield")
                defense += d
                defense *= m

            # defense *= random.uniform(.90, 1.10)

            return defense if defense > 0 else 1

        def damage_calculator(self, t, attack, defense, multiplier, attacker_items=[]):
            """Used to calc damage of the attack.
            Before multipliers and effects are apllied.
            """
            a = self.source

            damage = multiplier*attack**2/(attack+3*defense)

            # Items Bonus:
            m = 1.0
            for i in attacker_items:
                if hasattr(i, "damage_multiplier"):
                    m = m + i.damage_multiplier
            damage *= m

            # Traits Bonus:
            m = 1.0
            for i in a.traits:
                if hasattr(i, "damage_multiplier"):
                    m = m + i.damage_multiplier
            damage *= m

            return int(round(damage))

        def damage_modifier(self, t, damage, type):
            """
            This calculates the multiplier to use with effect of the skill.
            d: Damage (number per type)
            type: Damage Type
            """
            effects = list()
            a = self.source
            m = 1.0

            if type in t.resist:
                return "resisted"

            # Get multiplier from traits:
            # We decided that any trait could influence this:
            # damage = 0
            # defence = 0

            # Damage first:
            for trait in a.traits:
                if type in trait.el_damage:
                    m += trait.el_damage[type]

            # Defence next:
            for trait in t.traits:
                if type in trait.el_defence:
                     m -= trait.el_defence[type]

            damage *= m

            return damage

        # To String methods:
        def log_to_battle(self, effects, total_damage, a, t, message=None):
            # Logs effects to battle, target...
            effects.insert(0, total_damage)

            # Log the effects:
            t.beeffects = effects

            # String for the log:
            s = list()
            if not message:
                s.append("{color=[teal]}%s{/color} attacks %s with %s!" % (a.nickname, t.nickname, self.name))
            else:
                s.append(message)

            s = s + self.effects_to_string(t)

            battle.log("".join(s))

        def set_dmg_font_color(self, t, attributes, to_string=True, color="red"):
            """
            Sets up the color for damage graphics and returns a correct string for the log if to_string is True
            color: default to use if none found.
            attributes: list of effects to go through
            """
            effects = t.beeffects

            # Get the color for damage font based on elemental damage:
            l = list(e for e in store.traits.itervalues() if e.id.lower() in attributes)
            if l:
                # Just need one (if by some future design there is more)
                e = l[0]
                if e.font_color:
                    color = e.font_color
            # We do not color battle bounce anymore:
            # t.dmg_font = color # Set the font to pass it to show_damage_effect method, where it is reset back to red.

            # We do not want to show damage in the log if the attack missed:
            if to_string and "missed_hit" in effects:
                gfx = self.dodge_effect.get("gfx", "dodge")
                if gfx == "dodge":
                    return ""

            # return "{color=[%s]} DMG: %d {/color}" % (color, t.beeffects[0])
            # Simpler now, no special colors:
            return " DMG: %d" % (t.beeffects[0])

        def color_string_by_DAMAGE_type(self, s, type):
            # Takes a string "s" and colors it based of damage "type".
            # If type is not an element, color will be red or some preset (in this method) default.

            type_to_color_map = {e.id.lower(): e.font_color for e in tgs.elemental}
            type_to_color_map["poison"] = "green"
            type_to_color_map["healing"] = "lightgreen"

            color = type_to_color_map.get(type, "red")

            return "{color=[%s]} %s {/color}" % (color, s)

        def effects_to_string(self, t, default_color="red"):
            """Adds information about target to the list and returns it to be written to the log later.

            - We assume that all tuples in effects are damages by type!
            - At times also calls set_dmg_font_color.
            """
            # String for the log:
            effects = t.beeffects
            attributes = self.attributes
            damage_attrs = [i for i in effects if isinstance(i, tuple)]
            s = list()

            for effect in effects:
                if isinstance(effect, tuple):
                    temp = " %s:%s "%(self.DAMAGE[effect[0]], effect[1])
                    s.append(self.color_string_by_DAMAGE_type(temp, effect[0]))
                    # if effect[0] == "damage_mod":
                        # damage = round(float(effect[1]), 1)
                        # if damage > 0:
                            # s.append(" {color=[lawngreen]}⚔+ (%s){/color} "%damage)
                        # elif damage < 0:
                            # s.append(" {color=[red]}⚔- (%s){/color} "%-damage)

                    # elif effect[0] == "defence_mod":
                        # defence = round(float(effect[1]), 1)
                        # if defence > 0:
                            # s.append(" {color=[red]}☗+ (%s){/color} "%defence)
                        # elif defence < 0:
                            # s.append(" {color=[lawngreen]}☗- (%s){/color} "%-defence)

                else: # it's a string...
                    if effect == "backrow_penalty":
                        # Damage halved due to the target being in the back row!
                        s.append(" {color=[red]}1/2 DMG (Back-Row) {/color}")
                    elif effect == "critical_hit":
                        s.append(" {color=[lawngreen]}Critical Hit {/color}")
                    elif effect == "magic_shield":
                        s.append(" {color=[lawngreen]}☗+{/color} ")
                    elif effect == "missed_hit":
                        gfx = self.dodge_effect.get("gfx", "dodge")
                        if gfx == "dodge":
                            s.append(" {color=[lawngreen]}Attack Missed {/color}")
                        # else:
                            # s.append(" {color=[lawngreen]}Spell Resisted (-⅓ damage) {/color}")
                    # elif effect == "absorbed":
                        # s.append(" {color=[lawngreen]}Absorbed DMG{/color}")
                        # s.append(self.set_dmg_font_color(t, attributes, color="green"))
                    else:
                        if len(damage_attrs) > 1:
                            s.append(self.set_dmg_font_color(t, attributes, color=default_color))

            return s

        def apply_effects(self, targets):
            """This is a  final method where all effects of the attacks are being dished out on the objects.
            """

            # Not 100% for that this will be required...
            # Here it is simple since we are only focusing on damaging health:
            # prepare the variables:
            died = list()
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            for t in targets:
                if t.health - t.beeffects[0] > 0:
                    t.mod_stat("health", -t.beeffects[0])
                else:
                    t.health = 1
                    battle.end_turn_events.append(RPG_Death(t))
                    died.append(t)

            self.settle_cost()
            return died

        def settle_cost(self):
            # Here we need to take of cost:
            if not(isinstance(self.mp_cost, int)):
                mp_cost = int(self.source.get_max("mp")*self.mp_cost)
            else:
                mp_cost = self.mp_cost
            if not(isinstance(self.health_cost, int)):
                health_cost = int(self.source.get_max("health")*self.health_cost)
            else:
                health_cost = self.health_cost
            if not(isinstance(self.vitality_cost, int)):
                vitality_cost = int(self.source.get_max("vitality")*self.vitality_cost)
            else:
                vitality_cost = self.vitality_cost

            self.source.mp -= mp_cost
            self.source.health -= health_cost
            self.source.vitality -= vitality_cost

        # Game/Gui Assists:
        def get_element(self):
            # This may have to be expanded if we permit multi-elemental attacks in the future.
            # Returns first (if any) an element bound to spell or attack:
            if len(tgs.el_names.intersection(self.attributes)) > 1:
                return "me"

            for t in tgs.elemental:
                element = t.id
                if element.lower() in self.attributes:
                    return t

        # GFX/SFX:
        def time_gfx(self, targets, died):
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
            last_time_stamp = 0
            for index, stamp in enumerate(time_stamps):
                pause = stamp-last_time_stamp
                if pause > 0.02:
                    renpy.pause(pause)
                self.timestamps[stamp]()

                last_time_stamp = stamp

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
                renpy.show("casting", what=what,  at_list=[Transform(pos=battle.get_cp(attacker, type="center", yo=-50), align=(0.5, 0.5))], zorder=attacker.besk["zorder"]+1)
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
                pause = 0.96
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
            loop_sfx = self.main_effect.get("loop_sfx", False)

            # SFX:
            if isinstance(sfx, (list, tuple)):
                if not loop_sfx:
                    sfx = choice(sfx)

            if sfx:
                renpy.music.play(sfx, channel='audio')

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

            for target in [t for t in targets if not "missed_hit" in t.beeffects]:
                at_list = []

                if type == "shake":
                    what = target.besprite
                    at_list = [damage_shake(0.05, (-10, 10))]
                elif type == "true_dark": # not used atm! will need decent high level spells for this one!
                    what = AlphaBlend(Transform(target.besprite, alpha=.8), target.besprite, Transform("fire_logo", size=target.besprite_size), alpha=True)
                elif type == "true_water":
                    what = AlphaBlend(Transform(target.besprite, alpha=.6), target.besprite, Transform("water_overlay_test", size=target.besprite_size), alpha=True)
                elif type == "vertical_shake":
                    what = target.besprite
                    at_list = [vertical_damage_shake(0.1, (-5, 5))]
                elif type == "fly_away":
                    what = target.besprite
                    at_list = [fly_away]
                elif type == "on_air":
                    what = target.besprite
                    at_list = [blowing_wind()]
                elif type.startswith("iced"):
                    child = Transform("content/gfx/be/frozen.jpg", size=target.besprite_size)
                    mask = target.besprite
                    what = AlphaMask(child, mask)
                    if type.endswith("shake"):
                        at_list = [damage_shake(0.05, (-10, 10))]
                elif type.startswith("on_darkness"):
                    size = int(target.besprite_size[0]*1.5), 60
                    what = Fixed(target.besprite, Transform("be_dark_mask", size=size, anchor=(0.5, 0.3), align=(.5, 1.0), alpha=0.8), xysize=(target.besprite_size))
                    if type.endswith("shake"):
                        at_list = [damage_shake(0.05, (-10, 10))]
                elif type.startswith("on_light"):
                    size = int(target.besprite_size[0]*2.5), int(target.besprite_size[1]*2.5)
                    what = Fixed(target.besprite, Transform("be_light_mask", size=size, align=(.5, 1.0), alpha=0.6), xysize=(target.besprite_size))
                    if type.endswith("shake"):
                        at_list = [damage_shake(0.05, (-10, 10))]
                elif type == "on_death":
                    what = AlphaBlend(Transform(target.besprite, alpha=.5), target.besprite, dark_death_color(*target.besprite_size), alpha=True)
                elif type.startswith("on_dark"):
                    child = Transform("content/gfx/be/darken.jpg", size=target.besprite_size)
                    mask = target.besprite
                    what = AlphaMask(child, mask)
                    if type.endswith("shake"):
                        at_list = [damage_shake(0.05, (-10, 10))]
                elif type.startswith("frozen"): # shows a big block of ice around the target sprite
                    size = (int(target.besprite_size[0]*1.5), int(target.besprite_size[1]*1.5))
                    what = Fixed(target.besprite, Transform("content/gfx/be/frozen_2.png", size=size, offset=(-30, -50)))
                    t = self.target_sprite_damage_effect.get("duration", 1)
                    at_list=[fade_from_to_with_easeout(start_val=1.0, end_val=0.2, t=t)]
                    if type.endswith("shake"):
                        at_list = [damage_shake(0.05, (-10, 10))]
                elif type.startswith("burning"): # looks like more dangerous flame, should be used for high level spells
                    child = Transform("fire_mask", size=target.besprite_size)
                    mask = target.besprite
                    what = AlphaMask(child, mask)
                    if type.endswith("shake"):
                        at_list = [damage_shake(0.05, (-10, 10))]
                elif type.startswith("on_fire"):
                    what = AlphaBlend(Transform(target.besprite, alpha=.8), target.besprite, fire_effect_color(*target.besprite_size), alpha=True)
                    if type.endswith("shake"):
                        at_list = [damage_shake(0.05, (-10, 10))]
                elif type.startswith("on_water"):
                    sprite = target.besprite
                    sprite_size = target.besprite_size
                    mask = Transform("be_water_mask", size=sprite_size)
                    what = Fixed(xysize=sprite_size)
                    what.add(sprite)
                    what.add(AlphaMask(mask, sprite))
                    if type.endswith("shake"):
                        at_list = [damage_shake(0.05, (-10, 10))]
                elif type.startswith("on_ele"):
                    sprite = target.besprite
                    sprite_size = target.besprite_size
                    mask = Transform("be_electro_mask", size=sprite_size)
                    what = Fixed(xysize=sprite_size)
                    what.add(sprite)
                    what.add(AlphaMask(mask, sprite))
                    if type.endswith("shake"):
                        at_list = [damage_shake(0.05, (-10, 10))]
                elif type.startswith("poisoned"): # ideally we could use animated texture of green liquid, but it's hard to find for free...
                        what = AlphaBlend(Transform(target.besprite, alpha=.8), target.besprite, poison_effect_color(*target.besprite_size), alpha=True)
                        if type.endswith("shake"):
                            at_list = [damage_shake(0.05, (-10, 10))]
                elif isinstance(type, basestring) and type.startswith("being_healed"):
                        what = AlphaBlend(Transform(target.besprite, alpha=.9, additive=.4),
                                          target.besprite, healing_effect_color(*target.besprite_size),
                                          alpha=True)

                if "what" in locals():
                    renpy.show(target.betag, what=what, at_list=at_list, zorder=target.besk["zorder"])

            if self.target_sprite_damage_effect.get("master_shake", False):
                renpy.layer_at_list([damage_shake(0.05, (-5, 5))], layer='master')

        def hide_target_sprite_damage_effect(self, targets, died):
            # Hides damage effects applied to targets:
            if self.target_sprite_damage_effect.get("master_shake", False):
                renpy.layer_at_list([], layer='master')

            type = self.target_sprite_damage_effect.get("gfx", "shake")
            if type == "frozen":
                for target in targets:
                    if target not in died:
                        renpy.hide(target.betag)
                        renpy.show(target.betag, what=target.besprite, at_list=[Transform(pos=target.cpos), fade_from_to(0.3, 1, 0.3)], zorder=target.besk["zorder"])
            elif type in ["shake"] and self.target_death_effect["gfx"] == "shatter":
                for target in targets:
                    renpy.hide(target.betag)
                    renpy.show(target.betag, what=target.besprite, at_list=[Transform(pos=target.cpos)], zorder=target.besk["zorder"])
            else:
                for target in targets:
                    if target not in died:
                        renpy.hide(target.betag)
                        renpy.show(target.betag, what=target.besprite, at_list=[Transform(pos=target.cpos)], zorder=target.besk["zorder"])

        def time_target_damage_effect(self, targets, died, start):
            default =  self.main_effect["duration"] * .75 # Used to be .2 but it is a better idea to show it after the attack gfx effects are finished if no value was specified directly.
            damage_effect_start = start + self.target_damage_effect.get("initial_pause", default)

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
                            gfx = self.dodge_effect.get("gfx", "dodge")
                            if gfx == "dodge":
                                s = "Missed"
                                color = getattr(store, target.dmg_font)
                            else:
                                s = "▼ "+"%s"%target.beeffects[0]
                                color = getattr(store, target.dmg_font)
                        else:
                            s = "%s"%target.beeffects[0]
                            if "critical_hit" in target.beeffects:
                                s = "\n".join([s, "Critical hit!"])
                            color = getattr(store, target.dmg_font)
                        txt = Text(s, style="TisaOTM", min_width=200, text_align=0.5, color=color, size=18)
                        renpy.show(tag, what=txt, at_list=[battle_bounce(battle.get_cp(target, type="tc", yo=-30))], zorder=target.besk["zorder"]+2)
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

            if gfx in ["mirage"]:
                battle.bg.change(gfx)
            if gfx in ["black"]:
                renpy.with_statement(None)
                renpy.show("bg", what=Solid("#000000"))
                renpy.with_statement(dissolve)
                # renpy.pause(0.5)

        def hide_bg_main_effect(self):
            gfx = self.bg_main_effect["gfx"]
            if gfx in ["mirage"]:
                battle.bg.change("default")
            if gfx in ["black"]:
                renpy.with_statement(None)
                renpy.show("bg", what=battle.bg)
                renpy.with_statement(dissolve)

        def time_dodge_effect(self, targets, attacker, start):
            # effect_start = start - .3
            # if effect_start < 0:
                # effect_start = 0

            # Ok, so since we'll be using it for all kinds of attacks now, we need better timing controls:
            effect_start = self.dodge_effect.get("initial_pause", None)
            if effect_start is None:
                effect_start = start - .3
                if effect_start < 0:
                    effect_start = 0
            else:
                effect_start = effect_start + start

            if effect_start in self.timestamps:
                effect_start = effect_start + random.uniform(0.001, 0.002)
            self.timestamps[effect_start] = renpy.curry(self.show_dodge_effect)(attacker, targets)

            # Hiding timing as well in our new version:
            delay = effect_start + self.main_effect["duration"]
            if delay in self.timestamps:
                delay = delay + random.uniform(0.001, 0.002)

            self.timestamps[delay] = renpy.curry(self.hide_dodge_effect)(targets)

        def show_dodge_effect(self, attacker, targets):
            # This also handles shielding... which might not be appropriate and future safe...

            gfx = self.dodge_effect.get("gfx", "dodge")
            # gfx = self.dodge_effect["gfx"]
            # sfx = self.dodge_effect.get("sfx", None)

            # if sfx:
                # renpy.sound.play(sfx)

            for index, target in enumerate(targets):
                if "missed_hit" in target.beeffects:
                    if gfx == "dodge":
                        xoffset = -100 if battle.get_cp(attacker)[0] > battle.get_cp(target)[0] else 100

                        # Figure out the pause:
                        pause = self.main_effect["duration"]
                        if pause < .5:
                            pause = 0
                        else:
                            pause = pause - .5

                        renpy.show(target.betag, what=target.besprite, at_list=[be_dodge(xoffset, pause)], zorder=target.besk["zorder"])

                elif "magic_shield" in target.beeffects:
                    # Get GFX:
                    for event in battle.get_all_events():
                        if isinstance(event, DefenceBuff):
                            if event.target == target:
                                if event.activated_this_turn:
                                    gfx = event.gfx_effect
                                    break
                    else:
                        raise devlog.warning("No Effect GFX detected for magic_shield dodge_effect!")

                    # We need to find out if it's reasonable to show shields at all based on damage effects!
                    tsde = self.target_sprite_damage_effect.get("gfx", None)
                    # This should ensure that we do not show the shield for major damage effects, it will not look proper.
                    if tsde not in ["fly_away"]:
                        # Else we just show the shield:
                        if gfx == "default":
                            tag = "dodge" + str(index)
                            renpy.show(tag, what=ImageReference("resist"), at_list=[Transform(size=(300, 300), pos=battle.get_cp(target, type="center"), anchor=(.5, .5))], zorder=target.besk["zorder"]+1)
                        elif gfx == "gray_shield":
                            # raise Exception("M")
                            tag = "dodge" + str(index)
                            renpy.show(tag, what=AlphaBlend(ImageReference("resist"), ImageReference("resist"), gray_shield(300, 300), alpha=True), at_list=[Transform(size=(300, 300), pos=battle.get_cp(target, type="center"), anchor=(.5, .5))], zorder=target.besk["zorder"]+1)
                        elif gfx == "air_shield":
                            tag = "dodge" + str(index)
                            renpy.show(tag, what=AlphaBlend(ImageReference("ranged_shield_webm"), ImageReference("ranged_shield_webm"), green_shield(350, 300), alpha=True), at_list=[Transform(size=(350, 300), pos=battle.get_cp(target, type="center"), anchor=(.5, .5))], zorder=target.besk["zorder"]+1)
                        elif gfx == "solid_shield":
                            tag = "dodge" + str(index)
                            renpy.show(tag, what=ImageReference("shield_2"), at_list=[Transform(size=(400, 400), pos=battle.get_cp(target, type="center"), anchor=(.5, .5))], zorder=target.besk["zorder"]+1)

        def hide_dodge_effect(self, targets):
            # gfx = self.dodge_effect.get("gfx", "dodge")
            for index, target in enumerate(targets):
                if "magic_shield" in target.beeffects:
                    tag = "dodge" + str(index)
                    renpy.hide(tag)


    class BE_AI(object):
        # Not sure this even needs to be a class...
        def __init__(self, source):
            self.source = source

        def __call__(self):
            skills = self.get_availible_skills()
            if skills:
                skill = choice(skills)
                # So we have a skill... now lets pick a target(s):
                skill.source = self.source
                targets = skill.get_targets() # Get all targets in range.
                targets = targets if "all" in skill.type else choice(targets) # We get a correct amount of targets here.

                skill(ai=True, t=targets)

            else:
                BE_Skip(source=self.source)()

        def get_availible_skills(self):
            allskills = list(self.source.attack_skills) + list(self.source.magic_skills)
            return [s for s in allskills if s.check_conditions(self.source)]


    class Complex_BE_AI(BE_AI):
        """This one does a lot more "thinking".

        Possible options (Copied from GitHub Issue):
            Elemental affinities.
            Personalities (of AI).
            Intelligence (How smart it actually should be).
            Healing/Reviving.
            Favorite attacks/spells?
            Test multiple scenarios to see if we get infinite loops anywhere.
        """
        def __init__(self, source):
            super(Complex_BE_AI, self).__init__(source=source)

        def __call__(self):
            skills = self.get_availible_skills()
            if not skills:
                BE_Skip(source=self.source)()
                return

            # Split skills in containers:
            attack_skills = [s for s in skills if s.kind == "assault"]
            healing_skills = [s for s in skills if s.kind == "healing"]
            buffs = [s for s in skills if s.kind == "buffs"]
            revival_skills = [s for s in skills if s.kind == "revival"]

            # Reviving first:
            if revival_skills and dice(50):
                for skill in revival_skills:
                    targets = skill.get_targets(source=self.source)
                    if targets:
                        skill.source = self.source
                        targets = targets if "all" in skill.type else choice(targets)
                        skill(ai=True, t=targets)
                        return

            if healing_skills and dice(70):
                for skill in healing_skills:
                    targets = skill.get_targets(source=self.source)
                    for a in targets:
                        if a.health < a.get_max("health")*.5:
                            skill.source = self.source
                            targets = targets if "all" in skill.type else a
                            skill(ai=True, t=targets)
                            return

            if buffs and dice(10):
                for skill in buffs:
                    targets = skill.get_targets(source=self.source)
                    if targets:
                        skill.source = self.source
                        targets = targets if "all" in skill.type else a
                        skill(ai=True, t=targets)
                        return

            if attack_skills:
                # Sort skills by menu_pos:
                attack_skills.sort(key=attrgetter("menu_pos"))
                total_skills = len(attack_skills)
                while attack_skills:
                    # Most powerful skill has 70% chance to trigger.
                    # If not tirggered, next skill have slightly lower chance.
                    # Last skill in the list will execute!
                    chance = 70.0*len(attack_skills)/total_skills
                    skill = attack_skills.pop()
                    if not attack_skills or dice(chance):
                        skill.source = self.source
                        targets = skill.get_targets()
                        targets = targets if "all" in skill.type else a
                        skill(ai=True, t=targets)
                        return

            # In case we did not pick any specific skill:
            BE_Skip(source=self.source)()


    def get_char_with_lowest_attr(chars, attr="hp"):
        chars.sort(key=attrgetter(attr))
        return chars[0]


    class Slave_BE_AI(BE_AI): # for slaves involved in combat, skips every turn since they are not allowed to fight.
        def __init__(self, source):
            super(Slave_BE_AI, self).__init__(source=source)
        def __call__(self):
            Slave_BE_Skip(source=self.source)()
