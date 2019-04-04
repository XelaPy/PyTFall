init -1 python: # Core classes:
    """
    This is our version of turn based BattleEngine.
    I think that we can use zorders on master layer instead of messing with multiple layers.
    """

    BDP = {} # BE DEFAULT POSITIONS *positions are tuples in lists that go from top to bottom.
    BDP["l0"] = [(230, 540), (190, 590), (150, 640)] # Left (Usually player) teams backrow default positions.
    BDP["l1"] = [(360, 540), (320, 590), (280, 640)] # Left (Usually player) teams frontrow default positions.
    BDP["r0"] = list((config.screen_width-t[0], t[1]) for t in BDP["l0"]) # BackRow, Right (Usually enemy).
    BDP["r1"] = list((config.screen_width-t[0], t[1]) for t in BDP["l1"]) # FrontRow, Right (Usually enemy).

    # We need to get perfect middle positioning:
    # Get the perfect middle x:
    perfect_middle_xl = BDP["l0"][1][0] + round_int((BDP["l1"][1][0] - BDP["l0"][1][0])*.5)
    perfect_middle_yl = perfect_middle_yr = BDP["l1"][1][1] - 100
    perfect_middle_xr = BDP["r0"][1][0] + round_int((BDP["r1"][1][0] - BDP["r0"][1][0])*.5)
    BDP["perfect_middle_right"] = (perfect_middle_xl, perfect_middle_yl)
    BDP["perfect_middle_left"] = (perfect_middle_xr, perfect_middle_yr)
    del perfect_middle_xl
    del perfect_middle_yl
    del perfect_middle_xr
    del perfect_middle_yr


    class BE_Core(_object):
        """Main BE attrs, data and the loop!
        """
        def __init__(self, bg=Null(), music=None, row_pos=None, start_sfx=None,
                     end_sfx=None, logical=False, quotes=False,
                     max_skill_lvl=float("inf"), max_turns=1000, give_up=None,
                     use_items=False):
            """Creates an instance of BE scenario.

            logical: Just the calculations, without pause/gfx/sfx.
            """
            self.teams = list() # Each team represents a faction on the battlefield. 0 index for left team and 1 index for right team.
            self.queue = list() # List of events in BE..
            self.give_up = give_up # allows to avoid battle in one way or another
            self.use_items = use_items # allows use of items during combat.
            self.combat_status = None # general status of the battle, used to run away from BF atm.

            self.max_turn = max_turns

            if not logical:
                # Background we'll use.
                self.bg = ConsitionSwitcher("default", {"default": bg,
                                                        "black": Solid("#000000"),
                                                        "mirage": Mirage(bg, resize=get_size(bg),
                                                        amplitude=.04, wavelength=10, ycrop=10)})

                if music == "random":
                    self.music = get_random_battle_track()
                else:
                    self.music = music

            self.corpses = set() # Anyone died in the BE.

            if not row_pos:
                self.row_pos = BDP
            else:
                self.row_pos = row_pos

            # Whatever controls the current queue of the loop is the controller.
            # Usually it's player or AI combatants.
            self.controller = None
            self.winner = None
            self.win = None # We set this to True if left team wins and to False if right.
            self.combat_log = list()
            # We may want to delay logging something to the end of turn.
            self.delayed_log = list()

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

            self.generate_type_to_color_map()

        def generate_type_to_color_map(self):
            type_to_color_map = {e.id.lower(): e.font_color for e in tgs.elemental}
            type_to_color_map["poison"] = "green"
            type_to_color_map["healing"] = "lightgreen"

            self.type_to_color_map = type_to_color_map

        def log(self, report, delayed=False):
            # be_debug(report)
            if delayed:
                self.delayed_log.append(report)
            else:
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
            s = None # Clear this on first BE review.

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
                    if fighter.be.controller is not None:
                        # This character is not controlled by the player so we call the (AI) controller:
                        fighter.be.controller()
                    else: # Controller is the player:
                        # making known whose turn it is:
                        w, h = fighter.besprite_size
                        renpy.show("its_my_turn", at_list=[Transform(additive=.6, alpha=.7, size=(int(w*1.5), h/3),
                                                           pos=battle.get_cp(fighter, type="bc", yo=20),
                                                           anchor=(.5, 1.0))],
                                                           zorder=fighter.be.show_kwargs["zorder"]+1)

                        while 1:
                            skill = None
                            targets = None

                            rv = renpy.call_screen("pick_skill", fighter)

                            # Unique check for Skip/Escape Events:
                            if isinstance(rv, BESkip):
                                if rv() == "break":
                                    break
                            else: # Normal Skills:
                                if isinstance(rv, Item):
                                    skill = ConsumeItem()
                                    skill.item = rv
                                else:
                                    skill = rv

                                skill.source = fighter
                                targets = skill.get_targets()
                                targets = renpy.call_screen("target_practice", skill, fighter, targets)
                                if targets:
                                    break

                        # We don't need to see status icons during skill executions!
                        if not self.logical:
                            renpy.hide_screen("be_status_overlay")
                            renpy.hide("its_my_turn")

                        # This actually executes the skill!
                        if skill is not None:
                            if isinstance(targets, PytCharacter):
                                targets = [targets]
                            skill(targets=targets)

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

                # if DEBUG_BE and self.logical:
                #     temp = "Debug: Loop: %d, TLeft: %d, TRight: %d"%(self.logical_counter, len(self.get_fighters(state="dead", rows=(0, 1))),  len(self.get_fighters(state="dead", rows=(2, 3))))
                #     temp += ", ".join([str(i.health) for i in self.teams[0]])
                #     self.log(temp)

                for event in self.get_all_events():
                    if hasattr(event, "activated_this_turn"):
                        event.activated_this_turn = False

                if not self.logical:
                    for c in self.get_fighters("all"):
                        c.stats.update_delayed()

                self.combat_log.extend(self.delayed_log)
                self.delayed_log = list()

                # We check the conditions for terminating the BE scenario, this should prolly be end turn event as well, but I've added this before I've added events :)
                if self.check_break_conditions():
                    break

            self.end_battle()

        def start_battle(self):

            self.prepear_teams()

            if not self.logical:

                renpy.maximum_framerate(60)

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
                    if not i.attack_skills:
                        # we never allow hero team members to have zero attacks
                        i.attack_skills.append("Fist Attack")

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
                gfx_overlay.notify(type="fight")
                renpy.pause(.6)
                # renpy.pause(.35)

            self.main_loop()

        def prepear_teams(self):
            # Plainly sets allegiance of chars to their teams.
            # Allegiance may change during the fight (confusion skill for example once we have one).
            # I've also included part of team/char positioning logic here.
            pos = "l"
            for team in self.teams:
                team.position = pos
                size = len(team)
                for idx, char in enumerate(team.members):
                    # Clear the data (to be safe):
                    char.be.clear(controller=False)

                    # Position:
                    char.be.teampos = pos
                    if size == 3 and idx < 2:
                        idx = 1 - idx
                    char.be.index = idx
                    if pos == "l":
                        char.be.row = int(char.be.front_row)
                    else: # Case "r"
                        char.be.row = 2 if char.be.front_row else 3

                    # Allegiance:
                    char.be.allegiance = team.name or team

                    if not self.logical:
                        char.stats.update_delayed()

                pos = "r"

        def end_battle(self):
            """Ends the battle, trying to normalize any variables that may have been used during the battle.
            """
            if not self.logical:
                if self.win is True:
                    gfx_overlay.notify("You Win!")
                elif self.win is False:
                    tkwargs = {"color": blue,
                               "outlines": [(1, cyan, 0, 0)]}
                    gfx_overlay.notify("You Lose!", tkwargs=tkwargs)

                renpy.pause(1.0) # Small pause before terminating the engine.

                renpy.scene(layer='screens')
                renpy.scene()

                if self.end_sfx:
                    renpy.with_statement(self.end_sfx)

                if self.music:
                    renpy.music.stop()

            for f in self.get_fighters("all"):
                for s in list(f.magic_skills)+list(f.attack_skills):
                    s.source = None

                f.be.clear()

        def next_turn(self):
            """
            Returns the next battle events to the game.
            (Re)Calculates the queue of events.
            Currently we're calculating one turn where everyone gets to go once.
            Last index is the next in line.
            """
            if not self.queue:
                l = self.get_fighters()
                l.sort(key=attrgetter("agility"))
                self.queue = l
            return self.queue.pop()

        def get_icp(self, team, char):
            """Get Initial Character Position

            Basically this is what sets the characters up at the start of the battle-round.
            Returns initial position of the character based on row/team!
            Positions should always be retrieved using this method or errors may occur.
            """
            # We want different behavior for 3 member teams putting the leader in the middle:
            char.be.show_kwargs = dict()
            # Supplied to the show method.
            char.be.tag = str(random.random())
            # First, lets get correct sprites:
            if "Grim Reaper" in char.traits:
                sprite = Image("content/gfx/images/reaper.png")
            else:
                sprite = char.show("battle_sprite", resize=char.get_sprite_size("battle_sprite"))
            # char.besprite_size = sprite.true_size()

            # We'll assign "indexes" from 0 to 3 from left to right [0, 1, 3, 4] to help calculating attack ranges.
            team_index = team.position
            char_index = char.be.index
            # Sprite Flips:
            if team_index == "r":
                if char.__class__ != Mob:
                    if isinstance(sprite, ProportionalScale):
                        char.be.sprite = im.Flip(sprite, horizontal=True)
                    else:
                        char.be.sprite = Transform(sprite, xzoom=-1)
                else:
                    char.be.sprite = sprite
            else:
                if char.__class__ == Mob:
                    if isinstance(sprite, ProportionalScale):
                        char.be.sprite = im.Flip(sprite, horizontal=True)
                    else:
                        char.be.sprite = Transform(sprite, xzoom=-1)
                else:
                    char.be.sprite = sprite

            # We're going to land the character at the default position from now on,
            # with centered bottom of the image landing directly on the position!
            # This makes more sense for all purposes:
            x, y = self.row_pos[team_index + str(int(char.be.front_row))][char_index]
            w, h = char.besprite_size
            xpos = round_int(x-w*.5)
            ypos = round_int(y-h)
            char.be.default_pos = char.be.current_pos = (xpos, ypos)

            char.be.show_kwargs["what"] = char.be.sprite
            # Zorder defaults to characters (index + 1) * 100
            char.be.show_kwargs["zorder"] = (char_index + 1) * 100

            # ---------------------------------------------------->>>
            return char.be.default_pos

        def show_char(self, char, *args, **kwargs):
            for key in char.be.show_kwargs:
                if key not in kwargs: # We do not want to overwrite!
                    kwargs[key] = char.be.show_kwargs[key]
            renpy.show(char.be.tag, *args, **kwargs)

        def move(self, char, pos, t, pause=True):
            """
            Move character to new position...
            """
            renpy.hide(char.be.tag)
            renpy.show(char.be.tag, what=char.be.sprite, at_list=[move_from_to_pos_with_ease(start_pos=char.be.current_pos, end_pos=pos, t=t)], zorder=char.be.show_kwargs["zorder"])
            char.be.current_pos = pos
            if pause:
                renpy.pause(t)

        def get_cp(self, char, type="pos", xo=0, yo=0, override=False,
                   use_absolute=False):
            """I am not sure how this is supposed to work yet in the grand scheme of things.

            Old Comment: For now it will report initial position + types:
            **Updated to using Current Position + Types.
            pos: Character position (pos)
            sopos: This is tc of default character position. Used to place status overlay icons.
            center: center of the characters image
            tc: top center of the characters image
            bc: bottom center of the characters image
            fc: front center (Special per row instruction (for offset) applies)

            xo = offset for x
            yo = offset for y

            absolute: convert to absolute for subpixel positioning.
            """
            if not override:
                if not char.be.current_pos or not char.besprite_size:
                    raise Exception([char.be.current_pos, char.besprite_size])

                if type == "sopos":
                    xpos = char.be.default_pos[0] + char.besprite_size[0] / 2
                    ypos = char.be.default_pos[1] + yo

                if type == "pos":
                    xpos = char.be.current_pos[0]
                    ypos = char.be.current_pos[1] + yo
                elif type == "center":
                    xpos = char.be.current_pos[0] + char.besprite_size[0] / 2
                    ypos = char.be.current_pos[1] + char.besprite_size[1] / 2 + yo
                elif type == "tc":
                    xpos = char.be.current_pos[0] + char.besprite_size[0] / 2
                    ypos = char.be.current_pos[1] + yo
                elif type == "bc":
                    xpos = char.be.current_pos[0] + char.besprite_size[0] / 2
                    ypos = char.be.current_pos[1] + char.besprite_size[1] + yo
                elif type == "fc":
                    if char.be.row in [0, 1]:
                        xpos = char.be.current_pos[0] + char.besprite_size[0]
                        ypos = char.be.current_pos[1] + char.besprite_size[1] / 2 + yo
                    else:
                        xpos = char.be.current_pos[0]
                        ypos = char.be.current_pos[1] + char.besprite_size[1] / 2 + yo

            # in case we do not care about position of a target/caster and just provide "overwrite" we should use instead:
            else:
                xpos, ypos = override
                if yo:
                    ypos = ypos + yo # Same as for comment below (Maybe I just forgot how offsets work and why...)

            # While yoffset is the same, x offset depends on the team position: @REVIEW: AM I TOO WASTED OR DOES THIS NOT MAKE ANY SENSE???
            if char.be.row in [0, 1]:
                xpos = xpos + xo
            else:
                xpos = xpos - xo # Is this a reasonable approach instead of providing correct (negative/positive) offsets? Something to consider during the code review...

            if use_absolute:
                return absolute(xpos), absolute(ypos)
            else:
                return xpos, ypos

        def get_fighters(self, state="alive", rows=None):
            """
            Returns a list of all fighters from the team.
            states:
            - alive: All active member on the battlefield.
            - all: Everyone dead or alive.
            - dead: Everyone dead in the battlefield.
            rows: If provided, should be an iterable in range of 0 - 3. Only fighters in the row will be returned.
            """
            if state == "all":
                l = list(i for i in itertools.chain.from_iterable(self.teams))
            elif state == "alive":
                l =  list(i for i in itertools.chain.from_iterable(self.teams) if i not in self.corpses)
            elif state == "dead":
                l = list(self.corpses)

            if rows:
                l = list(i for i in l if i.be.row in rows)

            return l

        def check_break_conditions(self):
            # Checks if any specific condition is reached.
            # Should prolly be turned into a function when this gets complicated, for now it's just fighting until one of the party are "corpses".
            # For now this assumes that team indexed 0 is player team.
            if self.terminate:
                return True
            if self.combat_status in ("escape", "surrender"):
                self.win = False
                self.winner = self.teams[1]
                return True
            if self.logical and self.logical_counter >= self.max_turn:
                self.winner = self.teams[1]
                self.log("Battle went on for far too long! %s is considered the winner!" % self.winner.name)
                return True
            team0 = len(self.teams[0])
            team1 = len(self.teams[1])
            for c in self.corpses:
                if c.be.row < 2:
                    team0 -= 1
                else:
                    team1 -= 1
            if team0 == 0:
                self.winner = self.teams[1]
                self.win = False
                self.log("%s is victorious!" % self.winner.name)
                return True
            if team1 == 0:
                self.winner = self.teams[0]
                self.win = True
                self.log("%s is victorious!" % self.winner.name)
                return True

        def get_all_events(self):
            return itertools.chain(self.start_turn_events, self.mid_turn_events, self.end_turn_events)


    class BE_Event(_object):
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

        # ported from Action class as we need this for Events as well:
        def assess_resistance(self, target, type):
            if not type in target.be.damage:
                target.be.damage[type] = {}

            target.be.damage[type]["resisted"] = type in target.resist

        def assess_elemental(self, attacker, target, type):
            if not type in target.be.damage:
                target.be.damage[type] = {}

            # Get multiplier from traits
            # We decided that any trait could influence this
            # Damage first:
            m = 0
            for trait in attacker.traits:
                m += trait.el_damage.get(type, 0)
            target.be.damage[type]["elemental_damage_multiplier"] = m

            # Defence next:
            m = 0
            for trait in target.traits:
                m -= trait.el_defence.get(type, 0)
            target.be.damage[type]["elemental_defence_multiplier"] = m

        def assess_damage_multipliers(self, attacker, target, type, attacker_items=None):
            if not type in target.be.damage:
                target.be.damage[type] = {}

            if attacker_items is None:
                attacker_items = attacker.eq_items()

            # Items Bonus:
            m = 0
            for i in attacker_items:
                m += getattr(i, "damage_multiplier", 0)
            target.be.damage[type]["items_damage_multiplier"] = m

            # Traits Bonus:
            m = 0
            for t in attacker.traits:
                m += getattr(t, "damage_multiplier", 0)
            target.be.damage[type]["traits_damage_multiplier"] = m


    class BE_Action(BE_Event):
        """Basic action class that assumes that there will be targeting
            of some kind and follow-up logical and graphical effects.
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

        def __init__(self):
            # Naming/Sorting:
            self.name = self.mn = None
            self.kind = "assault"
            self.menu_pos = 0 # Skill level might be a better name.
            self.tier = None

            # Logic:
            self.range = 1
            self.source = None
            self.type = "se"
            self.critpower = 0
            self.piercing = False
            self.true_pierce = False # Does full damage to back rows.
            self.attributes = []
            self.effect = 0
            self.multiplier = 1
            self.desc = ""
            self.target_state = "alive"

            self.event_class = None # If a class, instance of this even will be created and placed in the queue. This invokes special checks in the effects method.):

            # GFX/SFX:
            self.attacker_action = { "gfx" : "step_forward", "sfx" : None }
            self.attacker_effects = { "gfx" : None, "sfx" : None }
            self.main_effect = { "gfx" : None, "sfx" : None, "start_at" : 0, "aim": {}, "duration": None }
            self.dodge_effect = { "gfx": "dodge" }
            self.target_sprite_damage_effect = { "gfx" : "shake", "sfx" : None, "duration": None, "initial_pause": None }
            self.target_damage_effect = { "gfx" : "battle_bounce", "sfx" : None, "initial_pause": None }
            self.target_death_effect = { "gfx" : "dissolve", "sfx" : None, "duration": .5, "initial_pause": None }
            self.bg_main_effect = { "gfx" : None, "initial_pause" : None, "duration": None }

            # Cost of the attack:
            self.mp_cost = 0
            self.health_cost = 0
            self.vitality_cost = 0

        def init(self):
            # set default values
            if not self.mn:
                self.mn = self.name

            try:
                self.delivery = self.DELIVERY.intersection(self.attributes).pop()
            except:
                self.delivery = ""

            self.damage = [d for d in self.attributes if d in self.DAMAGE]

            # Dicts:
            self.tags_to_hide = list() # BE effects tags of all kinds, will be hidden when the show gfx method runs it's course and cleared for the next use.
            self.timestamps = {} # Container for the timed gfx effects

            if self.main_effect["duration"] is None:
                self.main_effect["duration"] = (.1 if self.delivery in ["melee", "ranged"] else .5)

            if self.target_sprite_damage_effect["duration"] is None:
                self.target_sprite_damage_effect["duration"] = self.main_effect["duration"]

            if self.target_sprite_damage_effect["initial_pause"] is None:
                self.target_sprite_damage_effect["initial_pause"] = .1 if self.delivery in ["melee", "ranged"] else .2

            if self.target_damage_effect["initial_pause"] is None:
                self.target_damage_effect["initial_pause"] = (self.main_effect["duration"] * .75) if self.delivery in ["melee", "ranged"] else .21

            if self.target_death_effect["initial_pause"] is None:
                self.target_death_effect["initial_pause"] = (.2 if self.delivery in ["melee", "ranged"] else (self.target_sprite_damage_effect["initial_pause"] + .1))

            if self.bg_main_effect["initial_pause"] is None:
                self.bg_main_effect["initial_pause"] = self.main_effect["start_at"]

            if self.bg_main_effect["duration"] is None:
                self.bg_main_effect["duration"] = self.main_effect["duration"]

        def __call__(self, ai=False, targets=None):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            attacker = self.source

            self.assess_logical_effects(attacker, targets)
            died = self.apply_effects(targets)

            if not isinstance(died, (list, set, tuple)):
                died = list()

            if not battle.logical:
                self.time_gfx(targets, died)

                for tag in self.tags_to_hide:
                    renpy.hide(tag)
                self.tags_to_hide = list()

            # Clear data
            for f in battle.get_fighters(state="all"):
                f.be.clear_skill_data()

        # Targeting/Conditioning.
        def get_targets(self, source=None):
            """
            Gets tagets that can be hit with this action.
            Rows go [0, 1, 2, 3] from left to right of the battle-field.
            """
            char = source if source else self.source

            # First figure out all targets within the range:
            # We calculate this by assigning.
            all_targets = battle.get_fighters(self.target_state)
            left_front_row_empty = not any(f for f in all_targets if f.be.row == 1)
            right_front_row_empty = not any(f for f in all_targets if f.be.row == 2)
            range = self.range
            if left_front_row_empty:
                # 'move' closer because of an empty row
                range += 1
            elif char.be.row == 0 and self.range == 1:
                # allow to reach over a teammate
                range += 1
            if right_front_row_empty:
                # 'move' closer because of an empty row
                range += 1
            elif char.be.row == 3 and self.range == 1:
                # allow to reach over a teammate
                range += 1

            rows_from, rows_to = char.be.row - range, char.be.row + range
            in_range = [f for f in all_targets if rows_from <= f.be.row <= rows_to]

            #if DEBUG_BE:
            #    if any(t for t in in_range if isinstance(t, basestring)):
            #        raise Exception(in_range)

            # Lets handle the piercing (Or not piercing since piercing attacks include everyone in range already):
            if not self.piercing:
                if char.be.row < 2:
                    # Source is on left team:
                    # We need to check if there is at least one member on the opposing front row and if true, remove everyone in the back.
                    if not right_front_row_empty:
                        # opfor has a defender:
                        # we need to remove everyone from the back row:
                        in_range = [f for f in in_range if f.be.row != 3]
                else:
                    if not left_front_row_empty:
                        in_range = [f for f in in_range if f.be.row != 0]

            # Now the type, we just care about friends and enemies:
            if self.type in ("all_enemies", "se"):
                in_range = [f for f in in_range if char.be.allegiance != f.be.allegiance]
            elif self.type in ("all_allies", "sa"):
                in_range = [f for f in in_range if char.be.allegiance == f.be.allegiance]

            # In a perfect world, we're done, however we have to overwrite normal
            # rules if no targets are found and backrow can hit over it's own range (for example):
            #if not in_range: # <== We need to run "frenemy" code prior to this!
            #    # Another step is to allow any range > 1 backrow attack and any frontrow attack hitting backrow of the opfor...
            #    # and... if there is noone if front row, allow longer reach fighters in backrow even if their range normally would not allow it.
            #    if char.row == 0:
            #        # Case: Fighter in backrow and there is no defender on own team:
            #        if not battle.get_fighters(rows=[1]):
            #            # but there is at least one on the opfor:
            #            in_range = battle.get_fighters(rows=[2])
            #            if not in_range:
            #                # else, there is are no defenders at all anywhere...
            #                in_range = battle.get_fighters(rows=[3])
            #    elif char.row == 1:
            #        if not battle.get_fighters(rows=[2]):
            #            # We add everyone in the back row for target practice :)
            #            in_range = battle.get_fighters(rows=[3])
            #    elif char.row == 2:
            #        if not battle.get_fighters(rows=[1]):
            #            # We add everyone in the back row for target practice :)
            #            in_range = battle.get_fighters(rows=[0])
            #    elif char.row == 3:
            #        if not battle.get_fighters(rows=[1]) and self.range > 1:
            #            # We add everyone in the back row for target practice :)
            #            in_range = battle.get_fighters(rows=[0])
            #        # Case: Fighter in backrow and there is no defender on own team,
            #        if not battle.get_fighters(rows=[2]):
            #            # but there is at least one on the opfor:
            #            if battle.get_fighters(rows=[1]):
            #                in_range = battle.get_fighters(rows=[1])
            #            # else, there is are no defenders at all anywhere...
            #            else:
            #                in_range = battle.get_fighters(rows=[0])

            #    # And we need to check for dead people again... better code is needed to avoid cr@p like this in the future:
            #    in_range = [i for i in in_range if i in all_targets]

            # @Review: Prevent AI from casting the same Buffs endlessly:
            # Note that we do not have a concrete setup for buffs yet so this
            # is coded to be safe.
            if char.be.controller is not None:
                # a character controller by an AI
                buff_group = getattr(self, "buff_group", None)
                if buff_group is not None:
                    for target in in_range[:]:
                        for ev in store.battle.get_all_events():
                            if target == ev.target and getattr(ev, "group", "no_group") == buff_group:
                                in_range.remove(target)
                                break

            return in_range # List: So we can support indexing...

        def check_conditions(self, source=None):
            """Checks if the source can manage the attack."""
            char = source if source else self.source

            # Indoor check:
            if self.menu_pos >= battle.max_skill_lvl:
                return False

            # Check if attacker has enough resources for the attack:
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
        def assess_logical_effects(self, attacker, targets, log=True):
            """Logical effect of the action.

            - This is basically the controller that calls other methods.
            - For normal attacks, it calculates the damage.
            Expects a list or tuple with targets.
            This should return it's results through PytCharacters property called
                damage so the show_gfx method can be adjusted accordingly.
            But it is this method that writes to the log to be displayed later...
            """
            # prepare the variables:
            attributes = self.attributes
            attacker_items = attacker.eq_items()

            # Get the attack:
            self.assess_attack(attacker)

            for target in targets:
                self.assess_defence(target)
                self.assess_row_penalty(target)

                # Critical Strike and Evasion checks:
                if self.delivery in ["melee", "ranged"]:
                    self.assess_critical_hit(attacker, target, attacker_items)
                    self.assess_evasion(attacker, target)

                for type in self.damage:
                    target.be.damage[type] = {}
                    self.assess_resistance(target, type)
                    self.assess_elemental(attacker, target, type)
                    self.assess_absorbtion(target, type)
                    self.assess_damage_multipliers(attacker, target, type, attacker_items=attacker_items)
                    self.assess_damage(attacker, target, type)

                if log:
                    self.log_to_battle(attacker, target)

                # Write data:
                if DEBUG_BE:
                    devlog.info("======>")
                    devlog.info("{} attacks {} with {}.".format(attacker.name, target.name, self.name))
                    if attacker.be.attack:
                        temp = {k: v for k, v in attacker.be.attack.items() if v is not 0}
                        devlog.info("Attack: {}".format(temp))
                    if target.be.defence:
                        temp = {k: v for k, v in target.be.defence.items() if v is not 0}
                        devlog.info("Defence: {}".format(temp))
                    if attacker.be.critical_hit:
                        temp = {k: v for k, v in attacker.be.critical_hit.items() if v is not 0}
                        devlog.info("Critical: {}".format(temp))
                    if target.be.evasion:
                        temp = {k: v for k, v in target.be.evasion.items() if v is not 0}
                        devlog.info("Evasion: {}".format(temp))
                    if target.be.damage:
                        devlog.info("Damage:")
                        for type, data in target.be.damage.items():
                            data = {k: v for k, v in data.items() if v is not 0}
                            devlog.info("{}: {}".format(type, data))
                    devlog.info("Row Penalty: {}".format(target.be.row_penalty))
                    devlog.info("Total Damage: {}".format(target.be.total_damage))

        def assess_attack(self, attacker):
            """
            - Called from the effects resolver controller.

            Very simple method to get to attack power.
            """
            delivery = self.delivery

            if "melee" in self.attributes:
                attack = (attacker.attack*.7 + attacker.agility*.3 + self.effect) * self.multiplier
            elif "ranged" in self.attributes:
                attack = (attacker.attack*.7 + attacker.intelligence*.3 + self.effect) * self.multiplier
            elif "magic" in self.attributes:
                attack = (attacker.magic*.7 + attacker.intelligence*.3 + self.effect) * self.multiplier
            elif "status" in self.attributes:
                attack = (attacker.intelligence*.7 + attacker.agility*.3 + self.effect) * self.multiplier
            attacker.be.attack["base"] = round(attack, 1)

            # Items bonuses:
            bonus = 0
            m = 0
            items = attacker.eq_items()
            for i in items:
                if hasattr(i, "delivery_bonus"):
                    bonus += i.delivery_bonus.get(delivery, 0)
                if hasattr(i, "delivery_multiplier"):
                    m += i.delivery_multiplier.get(delivery, 0)
            attacker.be.attack["items_delivery_bonus"] = bonus
            attacker.be.attack["items_delivery_multiplier"] = m

            # Trait Bonuses:
            bonus = 0
            m = 0
            for i in attacker.traits:
                if hasattr(i, "delivery_bonus"):
                    # Reference: (minv, maxv, lvl)
                    if delivery in i.delivery_bonus:
                        minv, maxv, lvl = i.delivery_bonus[delivery]
                        if lvl <= 0:
                            lvl = 1
                        if lvl <= attacker.level:
                            bonus += maxv
                        else:
                            bonus += max(minv, float(attacker.level)*maxv/lvl)
                if hasattr(i, "delivery_multiplier"):
                    m += i.delivery_multiplier.get(delivery, 0)
            attacker.be.attack["traits_delivery_bonus"] = bonus
            attacker.be.attack["traits_delivery_multiplier"] = m

            # Finally:
            # Base value (stats + skill effect + skill multiplier)
            rv = attacker.be.attack["base"]

            # Direct bonuses from traits and items:
            rv += attacker.be.attack["items_delivery_bonus"]
            rv += attacker.be.attack["traits_delivery_bonus"]

            # Multipliers from traits and items:
            a = attacker.be.attack["items_delivery_multiplier"]
            b = attacker.be.attack["traits_delivery_multiplier"]
            multi = sum([1.0, a, b])
            rv *= multi

            rv = max(1, round(rv, 1))
            attacker.be.attack["result"] = rv

        def assess_defence(self, target):
            """
            - Called from the effects resolver controller.

            A method to get defence value vs current attack.
            """
            if "melee" in self.attributes:
                defence = round(target.defence*.7 + target.constitution*.3)
            elif "ranged" in self.attributes:
                defence = round(target.defence*.7 + target.agility*.3)
            elif "magic" in self.attributes:
                defence = round(target.defence*.4 + target.magic*.2 + target.intelligence*.4)
            elif "status" in self.attributes:
                defence = round(target.defence*.4 + target.intelligence*.3 + target.constitution*.3)
            target.be.defence["base"] = round(defence, 1)

            # Items bonuses:
            items = target.eq_items()
            bonus = 0
            m = 0
            for i in items:
                if hasattr(i, "defence_bonus"):
                    bonus += i.defence_bonus.get(self.delivery, 0)
                if hasattr(i, "defence_multiplier"):
                    m += i.defence_multiplier.get(self.delivery, 0)
            target.be.defence["items_defence_bonus"] = bonus
            target.be.defence["items_defence_multiplier"] = m

            # Trait Bonuses:
            bonus = 0
            m = 0
            for i in target.traits:
                if hasattr(i, "defence_bonus"):
                    # Reference: (minv, maxv, lvl)
                    if self.delivery in i.defence_bonus:
                        minv, maxv, lvl = i.defence_bonus[self.delivery]
                        if lvl <= 0:
                            lvl = 1
                        if lvl <= target.level:
                            bonus += maxv
                        else:
                            bonus += max(minv, float(target.level)*maxv/lvl)
                if hasattr(i, "defence_multiplier"):
                    if i in target.traits.basetraits and len(target.traits.basetraits) == 1:
                        m += 2*i.defence_multiplier.get(self.delivery, 0)
                    else:
                        m += i.defence_multiplier.get(self.delivery, 0)
            target.be.defence["traits_defence_bonus"] = bonus
            target.be.defence["traits_defence_multiplier"] = m

            # Testing status mods through be skillz:
            m = 0
            bonus = 0
            for event in battle.get_all_events():
                if event.target == target:
                    if hasattr(event, "defence_bonus"):
                        bonus += event.defence_bonus.get(self.delivery, 0)
                        event.activated_this_turn = True
                    if hasattr(event, "defence_multiplier"):
                        m += event.defence_multiplier.get(self.delivery, 0)
                        event.activated_this_turn = True
            target.be.defence["events_defence_bonus"] = bonus
            target.be.defence["events_defence_multiplier"] = m
            if bonus or m:
                target.be.defence["magic_shield"] = True

            # Finally
            # base value (stats)
            rv = target.be.defence["base"]

            # Direct bonuses:
            rv += target.be.defence["items_defence_bonus"]
            rv += target.be.defence["traits_defence_bonus"]
            rv += target.be.defence["events_defence_bonus"]

            # Multipliers:
            a = target.be.defence["traits_defence_multiplier"]
            b = target.be.defence["items_defence_multiplier"]
            c = target.be.defence["events_defence_multiplier"]
            multi = sum([1.0, a, b, c])
            rv *= multi

            rv = max(1, round(rv, 1))
            target.be.defence["result"] = rv

        def assess_damage(self, attacker, target, type):
            # Calculations:
            attack = attacker.be.attack["result"] / max(1, len(self.damage))
            defence = target.be.defence["result"] / max(1, len(self.damage))

            # Base:
            damage = attack*(75.0/(75+defence))
            target.be.damage[type]["base"] = damage

            # Direct and Elemental multipliers:
            a = target.be.damage[type]["items_damage_multiplier"]
            b = target.be.damage[type]["traits_damage_multiplier"]
            c = target.be.damage[type]["elemental_damage_multiplier"]
            d = target.be.damage[type]["elemental_defence_multiplier"]
            multi = sum([1.0, a, b, c, d])
            damage *= multi

            # Critical Hit:
            if attacker.be.critical_hit.get("result", False):
                damage *= 1.1+self.critpower

            # rng factors:
            damage *= uniform(.95, 1.05)

            # Absorption:
            absorbed = target.be.damage[type]["absorbed"]
            if absorbed:
                damage = -damage*absorbed

            # Row:
            if target.be.row_penalty:
                damage *= .5

            # Resistance:
            if target.be.damage[type]["resisted"]:
                damage = 0

            damage = round_int(damage)
            target.be.damage[type]["result"] = damage
            target.be.total_damage += damage

        def assess_row_penalty(self, target):
            """
            It's always the normal damage except for rows 0 and 3
            (unless everyone in the front row are dead).
            Account for true_piece here as well.
            """
            if target.be.row == 3:
                if battle.get_fighters(rows=[2]) and not self.true_pierce:
                    target.be.row_penalty = True
            elif target.be.row == 0:
                if battle.get_fighters(rows=[1]) and not self.true_pierce:
                    target.be.row_penalty = True

        def assess_absorbtion(self, target, type):
            """
            - Called from the effects resolver controller.

            Check all absorption capable traits.
            """
            absorbs = list(t for t in target.traits if t.el_absorbs)

            # # Get ratio:
            ratio = []
            for trait in absorbs:
                if type in trait.el_absorbs:
                    ratio.append(trait.el_absorbs[type])

            if ratio:
                rv = get_mean(ratio)
            else:
                rv = False

            target.be.damage[type]["absorbed"] = rv

        def assess_critical_hit(self, attacker, target, attacker_items):
            # Stats base:
            base = max(0, min((attacker.luck-target.luck), 20))
            attacker.be.critical_hit["base"] = base

            # Items bonuses:
            m = 0
            for i in attacker_items:
                m += getattr(i, "ch_multiplier", 0)
            attacker.be.critical_hit["items_multiplier"] = m

            # Traits bonuses:
            m = 0
            for i in attacker.traits:
                m += getattr(i, "ch_multiplier", 0)
            attacker.be.critical_hit["traits_multiplier"] = m

            # Finally:
            ch = base
            a = attacker.be.critical_hit["items_multiplier"]
            b = attacker.be.critical_hit["traits_multiplier"]
            ch += 100*(a+b)

            attacker.be.critical_hit["result"] = dice(ch)

        def assess_evasion(self, attacker, target):
            # Stats base:
            agility = min(15, target.agility*.05-attacker.agility*.05)
            luck = min(15, target.luck-attacker.luck)
            base = max(0, agility+luck)
            target.be.evasion["base"] = base

            # Items bonuses:
            bonus = 0
            for i in target.eq_items():
                bonus += getattr(i, "evasion_bonus", 0)
            target.be.evasion["item_bonus"] = bonus

            # Traits Bonuses:
            bonus = 0
            for i in target.traits:
                if hasattr(i, "evasion_bonus"):
                    # Reference: (minv, maxv, lvl)
                    minv, maxv, lvl = i.evasion_bonus
                    if lvl <= 0:
                        lvl = 1
                    if lvl <= target.level:
                        bonus += maxv
                    else:
                        bonus += max(minv, float(target.level)*maxv/lvl)
            target.be.evasion["traits_bonus"] = bonus

            # Health bonus:
            bonus = 0
            if target.health <= target.get_max("health")*.25:
                bonus = randint(1, 5) # very low health provides additional random evasion, 1-5%
            target.be.evasion["health_bonus"] = bonus

            # Calculations:
            ev = target.be.evasion["base"]

            a = target.be.evasion["item_bonus"]
            b = target.be.evasion["traits_bonus"]
            ev = max(0, a+b)

            ev += target.be.evasion["health_bonus"]

            if "inevitable" in self.attributes:
                target.be.evasion["result"] = False
                target.be.evasion["inevitable"] = True
            else:
                target.be.evasion["result"] = dice(ev)

        # To String methods:
        def log_to_battle(self, a, t, message=None):
            # String for the log:
            s = list()
            total_damage = t.be.total_damage
            if not message:
                if total_damage >= 0:
                    s.append("{color=[teal]}%s{/color} attacks %s with %s" % (a.nickname, t.nickname, self.name))
                else:
                    temp = randint(0, 1)
                    if temp == 0:
                        s.append("{color=[teal]}%s{/color} attacks %s with %s, but %s absorbs it" % (a.nickname, t.nickname, self.name, t.nickname))
                    else:
                        s.append("%s absorbs damage from {color=[teal]}%s{/color}'s %s attack" % (t.nickname, a.nickname, self.name))
            else:
                s.append(message)

            s = s + self.effects_to_string(a, t)

            battle.log(" ".join(s), delayed=True)

        def color_string_by_DAMAGE_type(self, type, value, return_for="log"):
            # Takes a string "s" and colors it based of damage "type".
            # If type is not an element, color will be red or some preset (in this method) default.
            if value < 0:
                value = -value
                color = battle.type_to_color_map["healing"]
            else:
                color = battle.type_to_color_map.get(type, "red")

            if return_for == "log":
                s = "%s: %s" % (self.DAMAGE.get(type, type), value)
                return "{color=[%s]}%s{/color}" % (color, s)
            elif return_for == "bb": # battle bounce
                return value, color
            else:
                return "Unknown Return For DAMAGE type!"

        def effects_to_string(self, attacker, target, default_color="red"):
            """Adds information about target to the list and returns it to be written to the log later.

            - We assume that all tuples in effects are damages by type!
            """
            # String for the log:
            damage = target.be.damage
            total_damage = target.be.total_damage
            rv = list()

            # First add the str effects:
            if target.be.evasion.get("result", False):
                gfx = self.dodge_effect.get("gfx", "dodge")
                if gfx == "dodge":
                    rv.append("{color=[lawngreen]}Attack Evaded{/color}")
                return rv
            else:
                if target.be.row_penalty:
                    rv.append("{color=[red]}1/2 DMG (Back-Row){/color}")
                if attacker.be.critical_hit.get("result", False):
                    rv.append("{color=[lawngreen]}Critical Hit{/color}")
                if target.be.defence.get("magic_shield", False):
                    rv.append("{color=[lawngreen]}☗+{/color}")

            # Next damage by type:
            for type, data in damage.items():
                temp = self.color_string_by_DAMAGE_type(type, data["result"])
                rv.append(temp)

            # And finally, combined damage for multi-type attacks:
            if len(damage) > 1:
                temp = self.color_string_by_DAMAGE_type("DGM", total_damage)
                rv.append(temp)

            return rv

        def apply_effects(self, targets):
            """This is a final method where all effects of the
                  attacks are being dished out on the objects.
            """
            died = list()
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]

            for t in targets:
                if t.be.evasion.get("result", False):
                    continue

                damage = t.be.total_damage
                if t.health - damage > 0:
                    t.mod_stat("health", -damage)

                    if self.event_class:
                        # First check resistance, then check if event is already in play:
                        type = self.buff_group
                        if not (type in t.resist or t.be.damage[type].get("absorbs", False)):
                            for event in store.battle.mid_turn_events:
                                if t == event.target and event.type == type:
                                    battle.log("%s is already effected by %s!" % (t.nickname, type))
                                    break
                            else:
                                duration = getattr(self, "event_duration", 3)
                                temp = self.event_class(attacker, t, self.effect, duration=duration)
                                battle.mid_turn_events.append(temp)
                                # We also add the icon to targets status overlay:
                                t.be.status_overlay.append(temp.icon)
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
            self.source.health = max(1, self.source.health - health_cost)
            self.source.vitality -= vitality_cost

            if not battle.logical:
                self.source.stats.update_delayed()

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
            """Executes GFX part of an attack. Disregarded during logical combat.

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
                renpy.start_predict(self.get_main_gfx())

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
            # calculate start time in any case, because we'll need it later
            start = self.main_effect["start_at"]
            if self.attacker_effects["gfx"] or self.attacker_effects["sfx"]:
                # We start as effects gfx is finished.
                start += self.time_attackers_first_effect(battle, attacker, targets)

            #  We start after attackers first action is finished.
            elif "delay" in locals():
                start += delay
            #else: # We plainly start at timestamp...

            # Next is the main GFX/SFX effect!:
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

            # Doesn't feel conceptually correct to put this here,
            # but it's likely the safest solution atm.
            gfx_overlay.be_taunt(attacker, self)

            time_stamps = sorted(self.timestamps.keys())
            st = time.time()
            for stamp in time_stamps:
                func = self.timestamps[stamp]
                # devlog.info("Func: {}".format(func.__dict__["callable"]))

                real_passed_time = time.time()-st
                # devlog.info("New iteration at: {}".format(round(real_passed_time, 2)))

                if real_passed_time < stamp:
                    pause = stamp-real_passed_time
                    if pause-.05 > 0:
                        # devlog.info("Paused for: {}".format(round(pause, 2)))
                        # ui.pausebehavior(pause, False)
                        # ui.interact(mouse='pause', type='pause', roll_forward=None)
                        renpy.pause(pause)

                # devlog.info("Function called at: {} (perfect time to call: {})".format(round(time.time()-st, 2), round(stamp, 2)))
                func()
                # devlog.info("Leaving iteration at: {}".format(round(time.time()-st, 2)))

            self.timestamps = {}
            # Try to predict the images:
            if self.attacker_effects["gfx"]:
                renpy.stop_predict(self.get_attackers_first_effect_gfx())
            if self.main_effect["gfx"]:
                renpy.stop_predict(self.get_main_gfx())

        # First attacker action (usually step forward)
        def time_attackers_first_action(self, battle, attacker):
            # Lets start with the very first part (attacker_action):
            self.timestamps[0] = renpy.curry(self.show_attackers_first_action)(battle, attacker)
            delay = self.get_show_attackers_first_action_initial_pause() + self.attacker_effects.get("duration", 0)
            hide_first_action = delay + self.attacker_action.get("keep_alive_delay", 0)
            self.timestamps[hide_first_action] = renpy.curry(self.hide_attackers_first_action)(battle, attacker)
            return delay

        def show_attackers_first_action(self, battle, attacker):
            if self.attacker_action["gfx"] == "step_forward":
                battle.move(attacker, battle.get_cp(attacker, xo=50), .5, pause=False)

            sfx = self.attacker_action.get("sfx", None)
            if sfx:
                renpy.sound.play(sfx)

        def get_show_attackers_first_action_initial_pause(self):
            if self.attacker_action["gfx"] == "step_forward":
                return .5
            else:
                return 0

        def hide_attackers_first_action(self, battle, attacker):
            if self.attacker_action["gfx"] == "step_forward":
                battle.move(attacker, attacker.be.default_pos, .5, pause=False)

        # First attacker effect (usually casting animation or similar)
        def time_attackers_first_effect(self, battle, attacker, targets):
            start = self.get_show_attackers_first_action_initial_pause()
            if start in self.timestamps:
                start = start + uniform(.001, .002)
            self.timestamps[start] = renpy.curry(self.show_attackers_first_effect)(battle, attacker, targets)

            if self.attacker_effects["gfx"]:
                effects_delay = start + self.attacker_effects.get("duration", 0)
                if effects_delay in self.timestamps:
                    effects_delay = effects_delay + uniform(.001, .002)
                self.timestamps[effects_delay] = renpy.curry(self.hide_attackers_first_effect)(battle, attacker)
                return effects_delay

            return 0

        def get_attackers_first_effect_gfx(self):
            gfx = self.attacker_effects["gfx"]
            zoom = self.attacker_effects.get("zoom", None)

            if zoom is not None:
                gfx = Transform(gfx, zoom=zoom)

            return gfx

        def show_attackers_first_effect(self, battle, attacker, targets):
            gfx = self.attacker_effects["gfx"]
            if gfx:
                what = self.get_attackers_first_effect_gfx()

                cast = self.attacker_effects.get("cast", {})
                point = cast.get("point", "center")
                align = cast.get("align", (.5, .5))
                xo = cast.get("xo", 0)
                yo = cast.get("yo", 0)
                zorder = 1 if cast.get("ontop", True) else -1

                # Flip the attack image if required:
                if self.attacker_effects.get("hflip", None) and battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0]:
                    what = Transform(what, xzoom=-1)
                    align = (1.0 - align[0], align[1])

                renpy.show("casting", what=what,  at_list=[Transform(pos=battle.get_cp(attacker, type=point, xo=xo, yo=yo), align=align)], zorder=attacker.be.show_kwargs["zorder"]+zorder)

            sfx = self.attacker_effects["sfx"]
            if sfx:
                if sfx == "default":
                    sfx="content/sfx/sound/be/casting_1.mp3"
                renpy.sound.play(sfx)

        def hide_attackers_first_effect(self, battle, attacker):
            # For now we just hide the tagged image here:
            renpy.hide("casting")

        # Main graphics, the effects of the skill
        def time_main_gfx(self, battle, attacker, targets, start):
            if start in self.timestamps:
                start = start + uniform(.001, .002)
            self.timestamps[start] = renpy.curry(self.show_main_gfx)(battle, attacker, targets)

            pause = start + self.main_effect["duration"]
            # Kind of a shitty way of trying to handle attacks that come.
            # With their own pauses in time_main_gfx method.
            pause += getattr(self, "firing_effects", {}).get("duration", 0)
            pause += getattr(self, "projectile_effects", {}).get("duration", 0)
            if pause in self.timestamps:
                pause = pause + uniform(.001, .002)

            self.timestamps[pause] = renpy.curry(self.hide_main_gfx)(targets)

        def get_main_gfx(self):
            gfx = self.main_effect["gfx"]

            # use AlphaBlend
            blend = self.main_effect.get("blend", None)
            if blend is not None:
                alpha = blend.get("alpha", None)
                if alpha is not None:
                    gfx = Transform(gfx, alpha=alpha)
                effect = getattr(store, blend.get("effect", None), None)
                if effect is not None:
                    size = blend["size"]
                    gfx = AlphaBlend(gfx, gfx, effect(*size), alpha=True)

            # Zoom if requested
            xzoom = self.main_effect.get("xzoom", 1.0)
            yzoom = self.main_effect.get("yzoom", 1.0)
            zoom = self.main_effect.get("zoom", None)
            if zoom is not None:
                xzoom *= zoom
                yzoom *= zoom
            if xzoom != 1.0 or yzoom != 1.0:
                gfx = Transform(gfx, xzoom=xzoom, yzoom=yzoom)

            # Scale if requested
            scale = self.main_effect.get("scale", None)
            if scale is not None:
                gfx = ProportionalScale(gfx, *scale)

            return gfx

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
                what = self.get_main_gfx()

                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (.5, .5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)

                # Flip the attack image if required:
                if self.main_effect.get("hflip", None) and battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0]:
                    what = Transform(what, xzoom=-1)

                for index, target in enumerate(targets):
                    gfxtag = "attack" + str(index)
                    renpy.show(gfxtag, what=what, at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo), anchor=anchor)], zorder=target.be.show_kwargs["zorder"]+1)

        def hide_main_gfx(self, targets):
            for i in xrange(len(targets)):
                gfxtag = "attack" + str(i)
                renpy.hide(gfxtag)

        # Effect of the main attack on the target(s), like shaking
        def time_target_sprite_damage_effect(self, targets, died, start):
            # We take previous start as basepoint for execution:
            damage_effect_start = start + self.target_sprite_damage_effect["initial_pause"]

            if damage_effect_start in self.timestamps:
                damage_effect_start = damage_effect_start + uniform(.001, .002)
            self.timestamps[damage_effect_start] = renpy.curry(self.show_target_sprite_damage_effect)(targets)

            delay = damage_effect_start + self.target_sprite_damage_effect["duration"]
            if delay in self.timestamps:
                delay = delay + uniform(.001, .002)

            self.timestamps[delay] = renpy.curry(self.hide_target_sprite_damage_effect)(targets, died)

        def show_target_sprite_damage_effect(self, targets):
            """Target damage graphical effects.
            """
            gfx = self.target_sprite_damage_effect["gfx"]

            if gfx:
                for target in targets:
                    if target.be.evasion.get("result", False):
                        continue

                    at_list = []

                    what = target.be.sprite
                    if gfx == "shake":
                        at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx == "true_dark": # not used atm! will need decent high level spells for this one!
                        what = AlphaBlend(Transform(what, alpha=.8), what, Transform("fire_logo", size=target.besprite_size), alpha=True)
                    elif gfx == "true_water":
                        what = AlphaBlend(Transform(what, alpha=.6), what, Transform("water_overlay_test", size=target.besprite_size), alpha=True)
                    elif gfx == "vertical_shake":
                        at_list = [vertical_damage_shake(.1, (-5, 5))]
                    elif gfx == "fly_away":
                        at_list = [fly_away]
                    elif gfx == "on_air":
                        at_list = [blowing_wind()]
                    elif gfx.startswith("iced"):
                        child = Transform("content/gfx/be/frozen.webp", size=target.besprite_size)
                        what = AlphaMask(child, what)
                        if gfx.endswith("shake"):
                            at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx.startswith("on_darkness"):
                        size = int(target.besprite_size[0]*1.5), 60
                        what = Fixed(what, Transform("be_dark_mask", size=size, anchor=(.5, .3), align=(.5, 1.0), alpha=.8), xysize=(target.besprite_size))
                        if gfx.endswith("shake"):
                            at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx.startswith("on_light"):
                        size = int(target.besprite_size[0]*2.5), int(target.besprite_size[1]*2.5)
                        what = Fixed(what, Transform("be_light_mask", size=size, align=(.5, 1.0), alpha=.6), xysize=(target.besprite_size))
                        if gfx.endswith("shake"):
                            at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx == "on_death":
                        what = AlphaBlend(Transform(what, alpha=.5), what, dark_death_color(*target.besprite_size), alpha=True)
                    elif gfx.startswith("on_dark"):
                        child = Transform("content/gfx/be/darken.webp", size=target.besprite_size)
                        what = AlphaMask(child, what)
                        if gfx.endswith("shake"):
                            at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx.startswith("frozen"): # shows a big block of ice around the target sprite
                        size = (int(target.besprite_size[0]*1.5), int(target.besprite_size[1]*1.5))
                        what = Fixed(what, Transform("content/gfx/be/frozen_2.webp", size=size, offset=(-30, -50)))
                        t = self.target_sprite_damage_effect.get("duration", 1)
                        at_list=[fade_from_to_with_easeout(start_val=1.0, end_val=.2, t=t)]
                        if gfx.endswith("shake"):
                            at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx.startswith("burning"): # looks like more dangerous flame, should be used for high level spells
                        child = Transform("fire_mask", size=target.besprite_size)
                        what = AlphaMask(child, what)
                        if gfx.endswith("shake"):
                            at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx.startswith("on_fire"):
                        what = AlphaBlend(Transform(what, alpha=.8), what, fire_effect_color(*target.besprite_size), alpha=True)
                        if gfx.endswith("shake"):
                            at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx.startswith("on_water"):
                        sprite_size = target.besprite_size
                        child = Transform("be_water_mask", size=sprite_size)
                        what = Fixed(what, AlphaMask(child, what), xysize=sprite_size)
                        if gfx.endswith("shake"):
                            at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx.startswith("on_ele"):
                        sprite_size = target.besprite_size
                        child = Transform("be_electro_mask", size=sprite_size)
                        what = Fixed(what, AlphaMask(child, what), xysize=sprite_size)
                        if gfx.endswith("shake"):
                            at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx.startswith("poisoned"): # ideally we could use animated texture of green liquid, but it's hard to find for free...
                            what = AlphaBlend(Transform(what, alpha=.8), what, poison_effect_color(*target.besprite_size), alpha=True)
                            if gfx.endswith("shake"):
                                at_list = [damage_shake(.05, (-10, 10))]
                    elif gfx == "being_healed":
                            what = AlphaBlend(Transform(what, alpha=.9, additive=.4),
                                              what, healing_effect_color(*target.besprite_size),
                                              alpha=True)
                    else:
                        be_debug("Unknown target_sprite_damage_effect-gfx '%s' defined in %s" % (gfx, self.name))
                        continue

                    renpy.show(target.be.tag, what=what, at_list=at_list, zorder=target.be.show_kwargs["zorder"])

            if self.target_sprite_damage_effect.get("master_shake", False):
                renpy.layer_at_list([damage_shake(.05, (-5, 5))], layer='master')

        def hide_target_sprite_damage_effect(self, targets, died):
            # Hides damage effects applied to targets:
            if self.target_sprite_damage_effect.get("master_shake", False):
                renpy.layer_at_list([], layer='master')

            type = self.target_sprite_damage_effect.get("gfx", "shake")
            if type == "frozen":
                for target in targets:
                    if target not in died:
                        renpy.hide(target.be.tag)
                        renpy.show(target.be.tag, what=target.be.sprite, at_list=[Transform(pos=target.be.current_pos), fade_from_to(.3, 1, .3)], zorder=target.be.show_kwargs["zorder"])
            elif type == "shake" and self.target_death_effect["gfx"] == "shatter":
                for target in targets:
                    renpy.hide(target.be.tag)
                    renpy.show(target.be.tag, what=target.be.sprite, at_list=[Transform(pos=target.be.current_pos)], zorder=target.be.show_kwargs["zorder"])
            else:
                for target in targets:
                    if target not in died:
                        renpy.hide(target.be.tag)
                        renpy.show(target.be.tag, what=target.be.sprite, at_list=[Transform(pos=target.be.current_pos)], zorder=target.be.show_kwargs["zorder"])

        # This is the effect of damage amount or similar
        # Number bouncing is the usual default
        def time_target_damage_effect(self, targets, died, start):
            # Used to be .2 but it is a better idea to show
            # it after the attack gfx effects are finished
            # if no value was specified directly.
            damage_effect_start = start + self.target_damage_effect["initial_pause"]

            if damage_effect_start in self.timestamps:
                damage_effect_start = damage_effect_start + uniform(.001, .002)
            self.timestamps[damage_effect_start] = renpy.curry(self.show_target_damage_effect)(targets, died)

            delay = damage_effect_start + self.get_target_damage_effect_duration()
            if delay in self.timestamps:
                delay = delay + uniform(.001, .002)

            self.timestamps[delay] = renpy.curry(self.hide_target_damage_effect)(targets, died)

        def show_target_damage_effect(self, targets, died):
            """Easy way to show damage like the bouncing damage effect.
            """
            attacker = self.source
            type = self.target_damage_effect.get("gfx", "battle_bounce")
            force = self.target_damage_effect.get("force", False)
            if type == "battle_bounce":
                for index, target in enumerate(targets):
                    if target not in died or force:
                        tag = "bb" + str(index)
                        value = target.be.total_damage

                        if target.be.evasion.get("result", False):
                            gfx = self.dodge_effect.get("gfx", "dodge")
                            if gfx == "dodge":
                                s = "Missed"
                                color = getattr(store, target.be.damage_font)
                            else:
                                s = "▼ "+"%s" % value
                                color = getattr(store, target.be.damage_font)
                        else:
                            types = target.be.damage.keys()

                            if len(types) == 1:
                                type = types.pop()
                                value, color = self.color_string_by_DAMAGE_type(type, value, return_for="bb")
                            else:
                                value, color = self.color_string_by_DAMAGE_type("DMG", value, return_for="bb")
                            s = "%s" % value
                            color = getattr(store, color)
                                # if value < 0:
                                #     s = "%s" % -value
                                #     color = store.lightgreen
                                # else:
                                #     s = "%s" % value
                                #     color = getattr(store, target.be.damage_font)

                        if attacker.be.critical_hit.get("result", False):
                            s = "\n".join([s, "Critical hit!"])
                        txt = Text(s, style="TisaOTM", min_width=200,
                                   text_align=.5, color=color, size=18)
                        renpy.show(tag, what=txt,
                                   at_list=[battle_bounce(battle.get_cp(target,
                                                                        type="tc",
                                                                        yo=-30))],
                                   zorder=target.be.show_kwargs["zorder"]+2)

                        target.be.damage_font = "red"

        def get_target_damage_effect_duration(self):
            type = self.target_damage_effect.get("gfx", "battle_bounce")
            if type == "battle_bounce":
                duration = 1.5
            else:
                duration = 0

            # Kind of a shitty way of trying to handle attacks that come
            # With their own pauses in time_main_gfx method.
            firing = hasattr(self, "firing_effects")
            if hasattr(self, "firing_effects"):
                duration += getattr(self, "firing_effects", {}).get("duration", 0)
                duration += self.main_effect.get("duration")
            duration += getattr(self, "projectile_effects", {}).get("duration", 0)

            return duration

        def hide_target_damage_effect(self, targets, died):
            for index, target in enumerate(targets):
                if target not in died:
                    tag = "bb" + str(index)
                    renpy.hide(tag)

        # Death effect...
        def time_target_death_effect(self, died, start):
            death_effect_start = start + self.target_death_effect["initial_pause"]

            if death_effect_start in self.timestamps:
                death_effect_start = death_effect_start + uniform(.001, .002)
            self.timestamps[death_effect_start] = renpy.curry(self.show_target_death_effect)(died)

            delay = death_effect_start + self.target_death_effect["duration"]
            if delay in self.timestamps:
                delay = delay + uniform(.001, .002)

            self.timestamps[delay] = renpy.curry(self.hide_target_death_effect)(died)

        def show_target_death_effect(self, died):
            gfx = self.target_death_effect["gfx"]
            sfx = self.target_death_effect["sfx"]
            duration = self.target_death_effect["duration"]

            if sfx:
                renpy.sound.play(sfx)

            if gfx == "dissolve":
                for t in died:
                    renpy.show(t.be.tag, what=t.be.sprite, at_list=[fade_from_to(start_val=1.0, end_val=.0, t=duration)], zorder=t.be.show_kwargs["zorder"])
            elif gfx == "shatter":
                for t in died:
                    renpy.show(t.be.tag, what=HitlerKaputt(t.be.sprite, 20), zorder=t.be.show_kwargs["zorder"])

        def hide_target_death_effect(self, died):
            for target in died:
                renpy.hide(target.be.tag)

        # Effect over the whole background, like distortion
        def time_bg_main_effect(self, start):
            effect_start = start + self.bg_main_effect["initial_pause"]

            if effect_start in self.timestamps:
                effect_start = effect_start + uniform(.001, .002)
            self.timestamps[effect_start] = self.show_bg_main_effect

            delay = effect_start + self.bg_main_effect["duration"]
            if delay in self.timestamps:
                delay = delay + uniform(.001, .002)

            self.timestamps[delay] = self.hide_bg_main_effect

        def show_bg_main_effect(self):
            gfx = self.bg_main_effect["gfx"]
            sfx = self.bg_main_effect.get("sfx", None)

            if sfx:
                renpy.sound.play(sfx)

            if gfx == "mirage":
                battle.bg.change(gfx)
            elif gfx == "black":
                renpy.with_statement(None)
                renpy.show("bg", what=Solid("#000000"))
                renpy.with_statement(dissolve)
                # renpy.pause(.5)

        def hide_bg_main_effect(self):
            gfx = self.bg_main_effect["gfx"]
            if gfx == "mirage":
                battle.bg.change("default")
            elif gfx == "black":
                renpy.with_statement(None)
                renpy.show("bg", what=battle.bg)
                renpy.with_statement(dissolve)

        # Dodging effect usually movement of the target sprite.
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
                effect_start = effect_start + uniform(.001, .002)
            self.timestamps[effect_start] = renpy.curry(self.show_dodge_effect)(attacker, targets)

            # Hiding timing as well in our new version:
            delay = effect_start + self.main_effect["duration"]
            if delay in self.timestamps:
                delay = delay + uniform(.001, .002)

            self.timestamps[delay] = renpy.curry(self.hide_dodge_effect)(targets)

        def show_dodge_effect(self, attacker, targets):
            # This also handles shielding... which might not be appropriate and future safe...
            gfx = self.dodge_effect.get("gfx", "dodge")
            # gfx = self.dodge_effect["gfx"]
            # sfx = self.dodge_effect.get("sfx", None)

            # if sfx:
                # renpy.sound.play(sfx)

            for index, target in enumerate(targets):
                if target.be.evasion.get("result", False):
                    if gfx == "dodge":
                        xoffset = -100 if battle.get_cp(attacker)[0] > battle.get_cp(target)[0] else 100

                        # Figure out the pause:
                        pause = self.main_effect["duration"]
                        if pause < .5:
                            pause = 0
                        else:
                            pause = pause - .5

                        renpy.show(target.be.tag, what=target.be.sprite, at_list=[be_dodge(xoffset, pause)], zorder=target.be.show_kwargs["zorder"])
                # We need to find out if it's reasonable to show shields at all based on damage effects!
                # This should ensure that we do not show the shield for major damage effects, it will not look proper.
                elif target.be.defence.get("magic_shield", False) and self.target_sprite_damage_effect["gfx"] != "fly_away":
                    # Get GFX:
                    for event in battle.get_all_events():
                        if isinstance(event, DefenceBuff):
                            if event.target == target:
                                if event.activated_this_turn:
                                    what = event.gfx_effect
                                    break
                    else:
                        be_debug("No Effect GFX detected for magic_shield dodge_effect!")
                        continue

                    # we just show the shield:
                    if what == "default":
                        what, size = "resist", (300, 300)
                    elif what == "gray_shield":
                        what = AlphaBlend("resist", "resist", gray_shield(300, 300), alpha=True)
                        size = (300, 300)
                    elif what == "air_shield":
                        what = AlphaBlend("ranged_shield_webm", "ranged_shield_webm", green_shield(350, 300), alpha=True)
                        size = (350, 300)
                    elif what == "solid_shield":
                        what, size = "shield_2", (400, 400)
                    else:
                        be_debug("The defence_gfx '%s' is not recognized. Should be one of ('default', 'gray_shield', 'air_shield', 'solid_shield')" % what)
                        continue
                    tag = "dodge" + str(index)
                    renpy.show(tag, what=what, at_list=[Transform(size=size, pos=battle.get_cp(target, type="center"), anchor=(.5, .5))], zorder=target.be.show_kwargs["zorder"]+1)

        def hide_dodge_effect(self, targets):
            # gfx = self.dodge_effect.get("gfx", "dodge")
            for index, target in enumerate(targets):
                if target.be.defence.get("magic_shield", False):
                    tag = "dodge" + str(index)
                    renpy.hide(tag)


    class BE_AI(_object):
        # Not sure this even needs to be a class...
        def __init__(self, source):
            self.source = source

        def __call__(self):
            skip = BESkip(source=self.source)

            skills = self.get_available_skills()
            if skills:
                skill = choice(skills)
                # So we have a skill... now lets pick a target(s):
                skill.source = self.source
                targets = skill.get_targets() # Get all targets in range.
                targets = targets if "all" in skill.type else choice(targets) # We get a correct amount of targets here.

                skill(ai=True, targets=targets)
            else:
                skip()

        def get_available_skills(self):
            # slaves should not battle
            if self.source.status == "slave":
                return

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
            skip = BESkip(source=self.source)

            temp = self.get_available_skills()
            if not temp:
                skip()
                return

            # Split skills in containers:
            skills = {}
            for s in temp:
                skills.setdefault(s.kind, []).append(s)

            # Reviving first:
            revival_skills = skills.get("revival", None)
            if revival_skills and dice(50):
                for skill in revival_skills:
                    targets = skill.get_targets(source=self.source)
                    if targets:
                        skill.source = self.source
                        targets = targets if "all" in skill.type else choice(targets)
                        skill(ai=True, targets=targets)
                        return

            healing_skills = skills.get("healing", None)
            if healing_skills and dice(70):
                for skill in healing_skills:
                    targets = skill.get_targets(source=self.source)
                    for t in targets:
                        if t.health < t.get_max("health")*.5:
                            skill.source = self.source
                            targets = targets if "all" in skill.type else t
                            skill(ai=True, targets=targets)
                            return

            buffs = skills.get("buffs", None)
            if buffs and dice(10):
                for skill in buffs:
                    targets = skill.get_targets(source=self.source)
                    if targets:
                        skill.source = self.source
                        targets = targets if "all" in skill.type else random.choice(targets)
                        skill(ai=True, targets=targets)
                        return

            attack_skills = skills.get("assault", None)
            if attack_skills:
                # Sort skills by menu_pos:
                attack_skills.sort(key=attrgetter("menu_pos"))
                while attack_skills:
                    # Most powerful skill has 70% chance to trigger.
                    # Last skill in the list will execute!
                    skill = attack_skills.pop()
                    if not attack_skills or dice(70):
                        skill.source = self.source
                        targets = skill.get_targets()
                        targets = targets if "all" in skill.type else random.choice(targets)
                        skill(ai=True, targets=targets)
                        return

            # In case we did not pick any specific skill:
            skip()

    #def get_char_with_lowest_attr(chars, attr="hp"):
    #    chars.sort(key=attrgetter(attr))
    #    return chars[0]
