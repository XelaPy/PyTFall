init -9 python: # FG Area
    class FG_Area(_object):
        """Dummy class for areas (for now).

        Tracks the progress in SE areas as well as storing their data.
        """
        def __init__(self):
            self.stage = 0 # For Sorting.
            self.tier = .2 # Difficulty
            self.days = 3
            self.max_days = 15
            self.risk = 45
            self._explored = 0
            self.last_explored = 0 # we check this to reduce exploration in ND

            # Controls the rate of exploration:
            self.exploration_multiplier = 1.0

            self.main = False
            self.area = None

            self.unlocks = {}

            self.travel_time = 0
            self.hazard = dict()
            self.items = dict()
            self.mobs = dict()

            # Special fields for quests, keys are chars or items and values are
            # exploration progress required to get them. Later we might add
            # some complex conditions instead, like fighting mobs.
            self.special_items = dict()
            self.special_chars = dict()

            # Chars capture:
            self.capture_chars = False
            self.chars = dict() # id: [explored, chance_per_day]
            self.rchars = dict() # id can be 'any' here, meaning any rChar.

            # All general items tagged with "Exploration" location are cut off by this value.
            self.items_price_limit = 0

            # Use dicts instead of sets as we want counters:
            self.mobs_defeated = dict()
            self.found_items = dict()
            self.chars_captured = 0
            self.cash_earned = 0

            # Flags for exploration tasks on "area" scope.
            self.camp = None
            self.building_camp = False
            self.camp_build_points_current = 0
            self.camp_build_points_required = 1000

            # Generated Content:
            self.logs = collections.deque(maxlen=19)

            # Trackers exploring the area at any given time, this can be used for easy access!
            self.trackers = set()

        @property
        def img(self):
            try:
                return self._img
            except: # Return from main:
                return store.fg_areas[self.area]._img

        @img.setter
        def img(self, value):
            self._img = value

        @property
        def distance_from_city(self):
            # 5 KM is minimum.
            distance = round_int(self.travel_time*25)
            return distance or 5

        @property
        def camp_build_status(self):
            return "%d%%" % (100.0*self.camp_build_points_current/self.camp_build_points_required)

        @property
        def teams(self):
            # Teams presently exploring this area:
            return [t.team for t in self.trackers]

        @property
        def explored(self):
            return self._explored

        @explored.setter
        def explored(self, value):
            if value >= 100:
                self._explored = 100
            elif value <= 0:
                self._explored = 0
            else:
                self._explored = value


init -6 python: # Guild, Tracker and Log.
    # ======================= (Simulated) Exploration code =====================>>>
    class ExplorationTracker(Job):
        # Added inheritance for Job so we can use the required methods.
        """The class that stores data for an exploration job.

        *Not really a Job, it stores data and doesn't write any reports to ND. **Maybe it should create ND report once the run is done!
        Adapted from old FG, not sure what we can keep here..."""
        def __init__(self, team, area, guild):
            """Creates a new ExplorationJob.

            team = The team that is exploring.
            area = The area that is being explored.
            """
            super(ExplorationTracker, self).__init__()
            self.id = "Exploration"
            self.type = "Combat"

            # Traits/Job-types associated with this job:
            self.occupations = ["Combatant"] # General Strings likes SIW, Combatant, Server...
            self.occupation_traits = [traits["Warrior"], traits["Mage"]] # Corresponding traits...

            self.base_stats = {"attack": 20, "defence": 20,
                               "agility": 60, "magic": 20}
            self.base_skills = {"exploration": 100}

            self.desc = "Explore the world, find new places, meet new people... and take their shit!"

            # We do this because this data needs to be tracked separately and
            # area object can only be updated once team has returned.
            # There is a good chance that some of these data must be updated in real time.
            self.team = team
            self.guild = guild # Guild this tracker was initiated from...

            # We do not want to deepcopy areas...
            # We can just write required info to this namespace:
            self.encounter_chance = getattr(area, "encounter_chance", 45) # 45% base encounter chance
            self.risk = area.risk
            self.capture_chars = area.capture_chars
            self.area = area

            # Features:
            self.basecamp = False
            self.base_camp_health = 0 # We call it health in case we allow it to be attacked at some point...

            # This is the general items that can be found at any exploration location,
            # Limited by price:
            self.exploration_items = dict([(item.id, item.chance) for item in store.items.values() if
                                          "Exploration" in item.locations and
                                          area.items_price_limit >= item.price])

            # Traveling to and from + Status flags:
            # We may be setting this directly in the future.
            # Distance in KM as units. 25 is what we expect the
            # team to be able to travel in a day.
            # This may be offset through traits and stats/skills.
            self.distance = area.distance_from_city

            self.traveled = 0 # Distance traveled in "KM"...
            self.arrived = False # Set to True upon arrival to the location.
            self.finished_exploring = False # Set to True after exploration is finished.

            # Exploration:
            self.points = 0 # Combined JP. Replaces AP, but we get this from the whole team.
            # Used to be effectiveness, but that would collide with a method of parent class
            self.ability = 0 # How well the team can perform any given exploration task.
            self.travel_points = 0 # travel point we use during traveling to offset JP correctly.

            # Instead of a bunch of properties, we'll use just the state as string and set it accordingly.
            self.state = "traveling to"
            # Use dicts instead of sets as we want counters:
            self.mobs_defeated = defaultdict(int)
            self.found_items = list()
            self.captured_chars = list()
            self.cash = list()
            self.unlocked_areas = list()

            self.daily_items = None

            self.day = 1 # Day since start (total of everything).
            # Days team is expected to be exploring (without travel times)!
            self.days = self.area.days
            if self.days < 3:
                self.days = 3
            self.days_traveled = 0 # Days team spent traveling to/from the locations
            self.days_explored = 0 # Days team spent exploring the location (includes camping and etc.)
            # As exploration loop can be interrupted and/or resumed, we need some way to fix it.
            # This just contains all (global) days team spent 'exploring'
            self.days_explored_tracker = set()
            # Simple counter for the amount of days team is spending at camp.
            # This is set back to 0 when team recovers inside of the camping method.
            self.days_in_camp = 0

            self.flag_red = False
            self.flag_green = False
            self.logs = list() # List of all log object we create during this exploration run.
            self.died = list()

            # And we got to make copies of chars stat dicts so we can show
            # changes in ND after the exploration run is complete!
            self.init_stats = dict()
            for char in self.team:
                self.init_stats[char] = char.stats.stats.copy()
                self.init_stats[char]["exploration"] = char.explorationskill
                self.init_stats[char]["exp"] = char.exp

            if not DEBUG:
                renpy.show_screen("message_screen", "Team %s was sent out on %d days exploration run!" % (team.name, area.days))

        @property
        def mobs(self):
            return self.area.mobs

        @property
        def cash_limit(self):
            return self.area.cash_limit

        @property
        def hazard(self):
            return self.area.hazard

        def log(self, txt, name="", nd_log=True, ui_log=False, **kwargs):
            if DEBUG_SE:
                msg = "{}: {} at {}\n    {}".format(self.area.name,
                                    self.team.name, self.guild.env.now, txt)
                se_debug(msg, mode="info")

            obj = ExplorationLog(name, txt, nd_log, ui_log, **kwargs)
            self.logs.append(obj)
            return obj

        def calc_ability(self):
            # Effectiveness (Ability):
            # New concept is as follows:
            # 300 effectiveness or 100 ability is needed to do this job right.
            # This will remove the need to mess with the size of the team
            # when calculating the results during the exploration.
            area = self.area
            team = self.team

            abilities = list()
            # Difficulty is tier of the area explored + 1/10 of the same value / 100 * risk.
            difficulty = area.tier+(area.tier*.001*self.risk)
            for char in team:
                # Set their exploration capabilities as temp flag
                a = self.effectiveness(char, difficulty, log=None, return_ratio=False)
                abilities.append(a)
            self.ability = sum(abilities)/3.0

            if DEBUG_SE:
                msg = "@ {} ability!".format(self.ability)
                se_debug(msg, mode="info")

        def finish_exploring(self):
            """
            Build one major report for next day!
            Log all the crap to Area and Main Area!
            Make sure that everything is cleaned up.
            """
            global fg_areas
            global items
            area = self.area
            building = self.guild.building
            team = self.team

            # Handle the no one returned to base case...
            if self.state == "full_death":
                self.guild.explorers.remove(self)
                area.trackers.remove(self)

                temp = "No one from {} returned back to the guild... we may as well assume the worse.".format(team.name)
                temp = set_font_color(temp, "red")
                txt = [temp]
                event_type = "explorationndreport"

                # Build an image combo for the report:
                img = pscale(area.img, *ND_IMAGE_SIZE)

                evt = NDEvent(type=event_type,
                              img=img,
                              txt=txt,
                              char=None,
                              team=None,
                              charmod={},
                              loc=self.guild.building,
                              locmod={},
                              green_flag=self.flag_green,
                              red_flag=self.flag_red)
                NEXT_DAY_EVENTS.append(evt)

                return

            if self.guild.has_extension(HealingSprings):
                temp = choice(["The team visited the Healing Springs on their way back to the Guild.",
                               "The team took some time off to visit the Onsen on their way back"])
                self.log(temp)
                for char in self.team:
                    mod_by_max(char, "health", .25)
                    mod_by_max(char, "mp", .25)
                    mod_by_max(char, "vitality", .25)

            # Log in the return:
            temp = "{} returned to the guild!".format(self.team.name)
            self.log(temp, name="Return")

            # Main and Sub Area Stuff:
            area.logs.extend([l for l in self.logs if l.ui_log])
            area.trackers.remove(self)

            found_items = collections.Counter(self.found_items)
            cash_earned = sum(self.cash)
            chars_captured = len(self.captured_chars)

            area.mobs_defeated = add_dicts(area.mobs_defeated, self.mobs_defeated)
            area.found_items = add_dicts(area.found_items, found_items)
            area.cash_earned += cash_earned
            area.chars_captured += chars_captured

            main_area = fg_areas[area.area]
            main_area.mobs_defeated = add_dicts(main_area.mobs_defeated, self.mobs_defeated)
            main_area.found_items = add_dicts(main_area.found_items, found_items)
            main_area.cash_earned += cash_earned
            main_area.chars_captured += chars_captured

            for a in self.unlocked_areas:
                a.unlocked = True

            # Restore Chars and Remove from guild:
            self.guild.explorers.remove(self)
            now = self.guild.env.now
            for char in self.team:
                char.action = None
                # Give the AP back if team returned early:
                char.AP = round_int(now*.01*char.setAP)

            # Next Day Stuff:
            # Not sure if this is required... we can add log objects and build
            # reports from them in real-time instead of replicating data we already have.
            txt = []
            images = []
            event_type = "explorationndreport"

            # Build an image combo for the report:
            bg = pscale(area.img, *ND_IMAGE_SIZE)
            images.append(bg)
            imgs = vp_or_fixed(self.team, ["fighting"],
                              {"exclude": ["sex"], "resize": (1000, 200)})
            images.extend(imgs)

            # We need to create major report for nd to keep track of progress:
            for log in [l for l in self.logs if l.nd_log]:
                txt.append("\n".join(log.txt))

            # Team stats for ND:
            team_charmod = {}
            for char, data in self.init_stats.items():
                if char in self.team: # Don't do this for dead explorers
                    if char not in team_charmod:
                        team_charmod[char] = {}
                        target = team_charmod[char]

                    for s, value in data.items():
                        if value < 1:
                            continue

                        if s in ("health", "mp", "vitality"):
                            continue

                        if s == "exploration":
                            temp = char.explorationskill - value
                            if temp:
                                target[s] = temp
                        elif s == "exp":
                            temp = char.exp - value
                            if temp:
                                target[s] = temp
                        else:
                            temp = char.stats.stats[s] - value
                            if temp:
                                target[s] = temp

            # handle the loot of all kinds:
            # Cash first:
            if cash_earned:
                hero.add_money(cash_earned, "Exploration Guild")
                building.fin.log_logical_income(cash_earned, "Exploration Guild")

            # Items:
            for item in self.found_items:
                hero.add_item(item)

            # Chars:
            for char in self.captured_chars:
                jail.add_prisoner(char, "SE_capture")

            evt = NDEvent(type=event_type,
                          img=images,
                          txt=txt,
                          team=self.team,
                          charmod=team_charmod,
                          loc=self.guild.building,
                          locmod={},
                          green_flag=self.flag_green,
                          red_flag=self.flag_red)
            NEXT_DAY_EVENTS.append(evt)


    class ExplorationLog(Action):
        """Stores resulting text and data for SE.

        Also functions as a screen action for future buttons. Maybe...
        """
        def __init__(self, name="", txt="", nd_log=True, ui_log=False, item=None):
            """
            nd_log: Printed in next day report upon arrival.
            ui_log: Only reports worth of ui interface in FG.
            """
            self.name = name # Name of the event, to be used as a name of a button in gui. (maybe...)
            self.suffix = "" # If there is no special condition in the screen, we add this to the right side of the event button!

            self.nd_log = nd_log
            self.ui_log = ui_log
            self.txt = [] # I figure we use list to store text.
            if txt:
                self.txt.append(txt)

            self.battle_log = [] # Used to log the event.
            self.found_items = []
            self.item = item # Item object for the UI log if one was found!

        def add(self, text, newline=True):
            # Adds a text to the log.
            self.txt.append(text)

        def __call__(self):
            renpy.show_screen("...") # Whatever the pop-up screen with info in gui is gonna be.

        def is_sensitive(self):
            # Check if the button has an action.
            return self.battle_log or self.found_items


    class ExplorationGuild(TaskBusiness):
        SORTING_ORDER = 10
        COMPATIBILITY = []
        MATERIALS = {"Wood": 70, "Bricks": 50, "Glass": 5}
        NAME = "Exploration Guild"
        IMG = "content/gfx/bg/buildings/the_guild.webp"
        DESC = "Travel to exotic places, meet new monsters and people... and take their shit!"

        CAPACITY = 0

        EXP_CAP_IN_SLOTS = 3
        EXP_CAP_EX_SLOTS = 0
        EXP_CAP_COST = 5000

        def __init__(self, **kwargs):
            super(ExplorationGuild, self).__init__(**kwargs)

            # Global Values that have effects on the whole business.
            self.teams = list() # List to hold all the teams formed in this guild. We should add at least one team or the guild will be useless...
            self.explorers = list() # List to hold all the (active) exploring trackers.

            self.workable = True
            self.focus_team = None
            self.team_to_launch_index = 0

        def expand_capacity(self, name="", mod_gui=None):
            if not name:
                name = get_team_name()

            team = self.new_team(name)
            if mod_gui is not None:
                mod_gui.add(team)

            super(ExplorationGuild, self).expand_capacity()

        def reduce_capacity(self, team=None, mod_gui=False):
            if team is None:
                team = self.teams.pop()
            else:
                self.teams.remove(team)

            if mod_gui:
                workers, guild = mod_gui
                for i in team:
                    workers.add(i)
                guild.remove(team)

            super(ExplorationGuild, self).reduce_capacity()

        # Business MainUpgrade related:
        def add_upgrade(self, upgrade, pay=False):
            if isinstance(upgrade, TheEye):
                store.the_eye_upgrade_active = True
            super(ExplorationGuild, self).add_upgrade(upgrade, pay=pay)

        def can_be_sold(self):
            if self.explorers:
                return False
            else:
                return True

        # Teams control/sorting/grouping methods:
        def new_team(self, name):
            team = Team(name, free=True)
            self.teams.append(team)
            return team

        def remove_team(self, t):
            self.teams.remove(t)

        def teams_to_launch(self):
            # Returns a list of teams that can be launched on an exploration run.
            # Must have at least one member and NOT already running exploration!
            return [t for t in self.idle_teams() if t]

        def prev_team_to_launch(self):
            teams = self.teams_to_launch()
            index = self.team_to_launch_index

            index = (index-1) % len(teams)

            self.team_to_launch_index = index
            self.focus_team = teams[index]

        def next_team_to_launch(self):
            teams = self.teams_to_launch()
            index = self.team_to_launch_index

            index = (index+1) % len(teams)

            self.team_to_launch_index = index
            self.focus_team = teams[index]

        def exploring_teams(self):
            # Teams that are busy with exploration runs.
            return [tracker.team for tracker in self.explorers]

        def idle_teams(self, clear_by_workplace=False):
            # Teams available for setup in order to set them on exploration runs.
            teams = [t for t in self.teams if t not in self.exploring_teams()]

            if clear_by_workplace:
                wp = self.building
                for team in teams:
                    for fighter in team:
                        if fighter.workplace != wp:
                            team.remove(fighter)

            return teams

        def idle_explorers(self):
            # Returns a list of idle explorers:
            return list(chain.from_iterable(t.members for t in self.idle_teams()))

        def launch_team(self, area, _team=None):
            # Moves the team to appropriate list, removes from main one and makes sure everything is setup right from there on out:
            team = self.focus_team if not _team else _team
            # self.teams.remove(team) # We prolly do not do this?

            for c in team:
                if check_for_impairments(c):
                    return c
                if c.workplace == schools["-PyTFall Educators-"]:
                    return c

            # Setup Explorers:
            for char in team:
                # We effectively remove char from the game so this is prolly ok.
                char.action = "Exploring"
                for t in hero.teams:
                    if char in t:
                        t.remove(char)

            # Remove Explorers from other teams:
            for t in self.teams:
                if t != team:
                    for char in team:
                        if char in t:
                            t.remove(char)

            tracker = ExplorationTracker(team, area, self)
            area.trackers.add(tracker)
            self.explorers.append(tracker)

            if not _team:
                self.focus_team = None
                self.team_to_launch_index = 0

            return True

        # SimPy methods:
        def business_control(self):
            """SimPy business controller.
            """
            for tracker in self.explorers:
                self.env.process(self.exploration_controller(tracker))

            while 1:
                yield self.env.timeout(100)

        def exploration_controller(self, tracker):
            # Controls the exploration by setting up proper simpy processes.
            # handle full death:
            if tracker.state == "full_death":
                temp = ("{color=[green]}Day: %d{/color} | "+
                        "{color=[green]}%s{/color} are still dead..."+
                        "\n") % (tracker.day, tracker.team.name)
                tracker.log(temp)

                yield self.env.timeout(50)

                # Add a couple of days on top so we don't 'jump to conclusions'
                if tracker.days_explored >= tracker.days+5:
                    tracker.finish_exploring()
                else:
                    tracker.days_explored += 1
                self.env.exit("full_death")

            tracker.area.last_explored = store.day

            # Prep aliases:
            process = self.env.process
            area = tracker.area
            team = tracker.team
            global_day = store.day

            # Convert AP to exploration points:
            self.convert_AP(tracker)

            if DEBUG_SE:
                msg = "Entered exploration controller for {}.".format(team.name)
                se_debug(msg, mode="info")

            # Log the day:
            if tracker.day == 1:
                temp = ("{color=[green]}Day: %d{/color} | "+
                        "{color=[green]}%s{/color} are on exploration run of %s!") % \
                        (tracker.day, tracker.team.name, tracker.area.name)
            else:
                temp = "\n{color=[green]}Day %d:{/color}" % tracker.day
            tracker.log(temp)

            # Ability:
            tracker.calc_ability()

            while 1:
                # Additional .state control:
                if tracker.state is None:
                    # just arrived to the location -> decide what to do
                    if area.building_camp:
                        tracker.state = "setting_up_basecamp"
                    else:
                        tracker.state = "exploring"
                # Set the state to traveling back if we're done:
                elif tracker.days_explored >= tracker.days:
                    tracker.state = "traveling back"

                # Day counter:
                temp = global_day not in tracker.days_explored_tracker
                if temp and tracker.state in ("exploring", "camping", "setting_up_basecamp"):
                    tracker.days_explored_tracker.add(global_day)
                    tracker.days_explored += 1

                if tracker.state == "traveling to":
                    # The team is not there yet, keep tracking
                    result = yield process(self.travel_to(tracker))
                    if result == "arrived":
                        tracker.state = None
                        # And reset the distance counter:
                        tracker.traveled = 0
                elif tracker.state == "exploring":
                    result = yield process(self.explore(tracker))
                    if result in ("retreat_to_camp", "defeat"):
                        tracker.state = "camping"
                    elif str(result).startswith(("captured", "got", "fallback", "unlocked")):
                        # We found something special or captured a char.
                        self.update_loot(tracker)
                        tracker.state = "traveling back"
                    elif result == "full_death":
                        tracker.state = "full_death"
                        self.env.exit("full_death")
                elif tracker.state == "camping":
                    result = yield process(self.camping(tracker))
                    if result == "restored":
                        tracker.state = "exploring"
                elif tracker.state == "traveling back":
                    result = yield process(self.travel_back(tracker))
                    if result == "back2guild":
                        tracker.finish_exploring() # Build the ND report!
                        self.env.exit() # We're done...
                elif tracker.state == "setting_up_basecamp":
                    yield process(self.setup_basecamp(tracker))

                if self.env.now >= 99:
                    break

            # if DEBUG_SE:
                # tracker.log("Debug: The day has come to an end for {}.".format(tracker.team.name))
            self.overnight(tracker)
            tracker.day += 1

        def set_travel_speed(self, tracker, log=True):
            if self.has_extension(GuildStables):
                if log:
                    temp = choice(["The Stables turned out to be a great investment after all. Team travels at 2x the speed!",
                                   "The team is traveling at 2x the pace! Stables Rule!"])
                    tracker.log(temp)
                speed = 2.5
            else:
                speed = 1.25

            speed = self.rewards_mod(tracker, speed, mb_ability=True, min_val=.75)

            return speed

        def travel_to(self, tracker):
            # Env func that handles the travel to routine.
            team = tracker.team
            area = tracker.area

            # It should be safe to just add a day here as this method can't be terminated
            # until traveling is done.
            tracker.days_traveled += 1

            if DEBUG_SE:
                msg = "{} are traveling to {}.".format(team.name, area.name)
                se_debug(msg, mode="info")

            # Figure out how far we can travel in steps of 5 DU:
            # Understanding here is that any team can travel 25 KM per day on average. This can be offset by traits and stats in the future.
            # tacker.tp = int(round(tracker.points / 20.0))
            travel_points = round_int(tracker.points / 20.0) # local variable just might do the trick...

            if not tracker.traveled:
                temp = "=> "
                temp = set_font_color(temp, "green")
                temp += "{} are on route to {}!".format(tracker.team.name, tracker.area.name)
                tracker.log(temp)

            speed = self.set_travel_speed(tracker, log=True)

            while 1:
                yield self.env.timeout(5) # We travel...

                tracker.points -= tracker.travel_points
                tracker.traveled += speed

                # Team arrived:
                if tracker.traveled >= tracker.distance:
                    if DEBUG_SE:
                        msg = "{} arrived at {} ({}).".format(team.name, area.name, area.id)
                        se_debug(msg, mode="info")

                    temp = "{} arrived at {}!".format(team.name, area.name)
                    if tracker.day > 1:
                        temp = temp + " It took {} {} to get there.".format(tracker.day, plural("day", tracker.day))
                    else:
                        temp = temp + " The trip took less then one day!"
                    tracker.log(temp, name="Arrival")
                    self.env.exit("arrived")

                if self.env.now >= 99: # We couldn't make it there before the days end...
                    temp = "{} spent the rest of the day on route to {}! ".format(team.name, area.name)
                    tracker.log(temp)
                    if DEBUG_SE:
                        se_debug(temp, mode="info")
                    self.env.exit("not_arrived")

        def travel_back(self, tracker):
            # Env func that handles the travel to routine.
            team = tracker.team

            if DEBUG_SE:
                msg = "{} are traveling back.".format(team.name)
                se_debug(msg, mode="info")

            # Figure out how far we can travel in 5 du:
            # Understanding here is that any team can travel 25 KM per day on average.
            # This can be offset by traits and stats in the future.
            # tacker.tp = int(round(tracker.points / 20.0))
            travel_points = round_int(tracker.points / 20.0) # local variable just might do the trick...

            speed = self.set_travel_speed(tracker, log=False)

            if not tracker.traveled:
                temp = "<= "
                temp = set_font_color(temp, "green")
                temp += choice(["{} are traveling back home.".format(tracker.team.name),
                               "The team is on route back the {}.".format(self.building.name),
                               "{} are on route back home.".format(tracker.team.name)])
                tracker.log(temp)

            while 1:
                yield self.env.timeout(5) # We travel...

                tracker.points -= tracker.travel_points
                tracker.traveled += speed

                # Team arrived:
                if tracker.traveled >= tracker.distance:
                    self.env.exit("back2guild")

                if self.env.now >= 99: # We couldn't make it there before the days end...
                    temp = "{} spent the rest of the day traveling back to the guild from {}! ".format(tracker.team.name, tracker.area.name)
                    tracker.log(temp)
                    self.env.exit("on the way back")

        def camping(self, tracker):
            """Camping will allow restoration of health/mp/agility and so on.
            Might be forced on low health.

            One day of camping (without item use) is meant to restore about 40%
                with tent and 80% with a camp at 100% ability.
            """
            team = tracker.team
            area = tracker.area
            # We don't want to run over autoequip on every iteration, two times is enough.
            auto_equip_counter = 0

            if DEBUG_SE:
                msg = "{} is Camping. State: {}".format(team.name, tracker.state)
                se_debug(msg, mode="info")

            mod = self.rewards_mod(tracker, .4, mb_ability=True, mb_risk=None,
                            mb_exploration_day=None, mb_explored=None,
                            min_val=.1)
            if area.camp:
                mod *= 2

            if not tracker.days_in_camp:
                if not area.camp:
                    temp = "{} setup a tent to get some rest and recover!".format(team.name)
                    tracker.log(temp)
                else:
                    temp = "{} retreated to camp to recover!".format(team.name)
                    temp += " Their downtime will be twice as effective as resting in a tent!"
                    tracker.log(temp)

            while 1:
                yield self.env.timeout(20) # We camp...

                # Base stats:
                for char in team:
                    mod_by_max(char, "health", mod*.2)
                    mod_by_max(char, "mp", mod*.2)
                    mod_by_max(char, "vitality", mod*.2)

                # Apply items:
                if auto_equip_counter < 2:
                    invlist = list(c.inventory for c in team)
                    random.shuffle(invlist)
                    for explorer in team:
                        l = list()
                        if explorer.health <= explorer.get_max("health")*.8:
                            for inv in invlist:
                                l.extend(explorer.auto_equip(["health"], inv=inv))
                        if explorer.vitality <= explorer.get_max("vitality")*.8:
                            for inv in invlist:
                                l.extend(explorer.auto_equip(["vitality"], inv=inv))
                        if explorer.mp <= explorer.get_max("mp")*.8:
                            for inv in invlist:
                                l.extend(explorer.auto_equip(["mp"], inv=inv))
                        if l:
                            temp = "%s used: {color=[lawngreen]}%s %s{/color} to recover!\n" % (explorer.nickname, ", ".join(l), plural("item", len(l)))
                            self.log(temp)
                    auto_equip_counter += 1

                for c in team:
                    if c.health <= c.get_max("health")*.9:
                        break
                    if c.mp <= c.get_max("mp")*.9:
                        break
                    if c.vitality <= c.get_max("vitality")*.8:
                        break
                else:
                    tracker.days_in_camp = 0
                    temp = "{} are now ready for more action in {}! ".format(team.name, area.name)
                    tracker.log(temp)
                    self.env.exit("restored")

                if self.env.now >= 99:
                    tracker.days_in_camp += 1

                    if DEBUG_SE:
                        msg = "{} exiting camping. (Day Ended)".format(team.name)
                        se_debug(msg, mode="info")

                    self.env.exit("still camping")

                # if not stop:
                    # for member in self.team:
                        # if member.health <= (member.get_max("health") / 100.0 * (100 - self.risk)) or member.health < 15:
                            # temp = "{color=[blue]}Your party falls back to base due to risk factors!{/color}"
                            # tracker.log(temp)

        def overnight(self, tracker):
            # overnight: More effective heal. Spend the night resting.
            # Do we run this? This prolly doesn't need to be a simpy process...
            # or maybe schedule this to run at 99.
            team = tracker.team

            if DEBUG_SE:
                msg = "{} is overnighting. State: {}".format(team.name, tracker.state)
                se_debug(msg, mode="info")

            self.update_loot(tracker)

            if DEBUG_SE:
                msg = "{} has finished an exploration scenario. (Day Ended)".format(team.name)
                se_debug(msg, mode="info")

            if tracker.state == "exploring":
                temp = "{} are done with exploring for the day and will now rest and recover! ".format(team.name)
                tracker.log(temp)
            elif tracker.state == "camping":
                temp = "{} cozied up in their camp for the night! ".format(team.name)
                tracker.log(temp)

            for c in team:
                c.health += round_int(c.get_max("health")*.1)
                c.mp += round_int(c.get_max("mp")*.1)
                c.vitality += round_int(c.get_max("vitality")*.1)

        def update_loot(self, tracker):
            # Updates items and gold and logs in the same!
            if tracker.daily_items is not None:
                # This basically means that team spent some time on exploring -> create a summary
                items = tracker.daily_items
                cash = tracker.daily_cash
                if items and cash:
                    tracker.log("The team has found: %s %s and {color=[gold]}%d Gold{/color} in loot!" % (", ".join(items), plural("item", len(items)), cash))
                    tracker.found_items.extend(items)
                    tracker.cash.append(cash)
                elif cash and not items:
                    tracker.log("The team has found: {color=[gold]}%d Gold{/color} in loot." % cash)
                    tracker.cash.append(cash)
                elif items and not cash:
                    tracker.log("The team has found: %s %s" % (", ".join(items), plural("item", len(items))))
                    tracker.found_items.extend(items)
                elif not items and not cash:
                    tracker.log("Your team has not found anything of interest...")

                tracker.daily_items = None

        def explore(self, tracker):
            """SimPy process that handles the exploration itself.

            Idea is to keep as much of this logic as possible and adapt it to work with SimPy...
            """
            if tracker.daily_items is None:
                tracker.daily_items = list()
                tracker.daily_cash = 0

            items = tracker.daily_items
            area = tracker.area
            team = tracker.team
            encountered_opfor = 1.0

            if DEBUG_SE:
                msg = "{} is starting an exploration scenario.".format(team.name)
                se_debug(msg, mode="info")

            # Let's run the expensive item calculations once and just give
            # items as we explore.
            # Get the max number of items that can be found in one day (base: 3):
            max_items = self.rewards_mod(tracker, 3, mb_ability=True,
                            mb_risk=True,
                            mb_exploration_day=True, mb_explored=True,
                            min_val=0)
            max_items = round_int(max_items)
            if DEBUG_SE:
                msg = "Max Items ({}) to be found on Day: {}!".format(max_items, tracker.day)
                se_debug(msg, mode="info")

            chosen_items = [] # Picked items
            local_items = [] # Local Items
            if max_items:
                for i, d in area.items.iteritems():
                    if dice(d):
                        local_items.append(i)

                area_items = []
                for i, d in tracker.exploration_items.iteritems():
                    if dice(d):
                        area_items.append(i)

                if DEBUG_SE:
                    msg = "Local Items: {}|Area Items: {}".format(len(local_items), len(area_items))
                    se_debug(msg, mode="info")

                while len(chosen_items) < max_items and (area_items or local_items):
                    # always pick from local item list first!
                    if local_items:
                        chosen_items.append(choice(local_items))

                    if area_items and len(chosen_items) < max_items:
                        chosen_items.append(choice(area_items))

                if DEBUG_SE:
                    msg = "({}) Items were picked for choice!".format(len(chosen_items))
                    se_debug(msg, mode="info")

            # Max cash to be found this day:
            max_cash = self.rewards_mod(tracker, tracker.cash_limit, mb_ability=True,
                            mb_risk=True,
                            mb_exploration_day=True, mb_explored=False,
                            min_val=0)

            # Exploration speed:
            exploration_rate = self.rewards_mod(tracker, 2, mb_ability=True,
                                    mb_risk=True,
                                    mb_exploration_day=False, mb_explored=False,
                                    min_val=.2)
            exploration_rate *= area.exploration_multiplier
            if self.has_extension(CartographyLab):
                temp = choice(["The team is making notes about the area to be used in the lab when they get back.",
                               "Your explorers are doing the boring work of mapping the area (+50% exploration rate from the Lab)"])
                tracker.log(temp)
                exploration_rate *= 1.5

            if DEBUG_SE:
                msg = "Exploration rate: {}".format(exploration_rate)
                se_debug(msg, mode="info")

            while 1:
                yield self.env.timeout(5) # We'll go with 5 du per one iteration of "exploration loop".

                # record the exploration
                # risk and multiplier added now
                # +/- 10 points per day for a competent team.
                if not self.env.now % 25:
                    area.explored += exploration_rate

                    temp = choice(["-Looking around.",
                                   "-Exploring the area!",
                                   "-Trying to find something useful.",
                                   "-Is there something useful around here?"])
                    tracker.log(temp)

                    for member in team:
                        if dice(50):
                            ss_reward(member, area.tier, {"exploration": 1}, apply=True)

                    for a, value in area.unlocks.items():
                        area_to_unlock = store.fg_areas[a]
                        if area.explored >= value and area_to_unlock.unlocked is False:
                            area_to_unlock.unlocked = "standby"
                            tracker.unlocked_areas.append(area_to_unlock)
                            temp = "Your team has uncovered a location of a new area to explore!"
                            temp += "\n {} is now unlocked!".format(a)
                            temp += "\n They are falling back to the base to report the finding."
                            temp = set_font_color(temp, "green")
                            tracker.log(temp)
                            self.env.exit("unlocked area")

                    # Hazard:
                    if area.hazard:
                        dead = []
                        temp = "{color=[yellow]}Hazardous area!{/color} The team was effected."
                        tracker.log(temp)

                        for char in team:
                            for stat, value in area.hazard.items():
                                # value, because we calculated effects on daily base in the past...
                                val = max(1, round_int(value*.25))
                                if stat == "health" and char.health-val <= 0:
                                    dead.append(char)
                                else:
                                    char.mod_stat(stat, -val)

                        if dead:
                            _result = self.death(tracker, dead=dead, kind='hazard')
                            if _result == "full_death":
                                self.env.exit(_result)
                            elif _result == "fallback_to_guild":
                                self.env.exit(_result)

                        if self.assess_exploration_risk(tracker):
                            self.env.exit("back2camp")

                # Items:
                # Handle the special items (must be done here so it doesn't collide with other teams)
                special_items = []
                if area.special_items:
                    for item, explored in area.special_items.items():
                        if area.explored >= explored:
                            special_items.append(item)

                if (chosen_items or special_items) and not self.env.now % 5:
                    if self.env.now < 50:
                        chance = self.env.now/5
                    elif self.env.now < 80:
                        chance = self.env.now
                    else:
                        chance = 100

                    if dice(chance):
                        if special_items:
                            item = special_items.pop()

                            if DEBUG_SE:
                                msg = "{} Found a special item {}!".format(team.name, item)
                                se_debug(msg, mode="info")

                            temp = "Found a special item %s!" % item
                            temp = set_font_color(temp, "orange")
                            tracker.log(temp, "Item", ui_log=True, item=store.items[item])

                            # And delete special item from area so it can't be discovered again or by another team:
                            del(area.special_items[item])

                            if DEBUG_SE:
                                msg = "{} has finished an exploration scenario. (Captured a special item {})".format(team.name, item)
                                se_debug(msg, mode="info")

                            self.env.exit("got special item")
                        else:
                            item = chosen_items.pop()
                            temp = "Found an item %s!" % item
                            temp = set_font_color(temp, "lawngreen")
                            tracker.log(temp, "Item", ui_log=True, item=store.items[item])
                            if DEBUG_SE:
                                msg = "{} Found an item {}!".format(team.name, item)
                                se_debug(msg, mode="info")
                        items.append(item)

                # Cash:
                if max_cash > 0 and not self.env.now % 20:
                    give = round_int(max_cash/5.0)
                    if give > 0:
                        max_cash -= give
                        tracker.daily_cash += give

                        temp = "{color=[gold]}Found %d Gold!{/color}" % give
                        tracker.log(temp)
                        if DEBUG_SE:
                            msg = "{} Found {} Gold!".format(team.name, give)
                            se_debug(msg, mode="info")

                # Chars Capture:
                if tracker.capture_chars and not self.env.now % 30:
                    # Special Chars:
                    if area.special_chars:
                        for char, explored in area.special_chars.items():
                            if area.explored >= explored:
                                del(area.special_chars[char])
                                tracker.captured_chars.append(char)

                                temp = "Your team has captured a 'special' character: {}!".format(char.name)
                                temp = set_font_color(temp, "orange")
                                tracker.log(temp)
                                if DEBUG_SE:
                                    msg = "{} has finished an exploration scenario. (Captured a special char {})".format(team.name, char.id)
                                    se_debug(msg, mode="info")

                                self.env.exit("captured char")

                    # uChars (also from Area):
                    if area.chars:
                        for id, data in area.chars.items():
                            explored, chance = data
                            chance = self.rewards_mod(tracker, chance, mb_ability=True,
                                            mb_risk=True,
                                            mb_exploration_day=True, mb_explored=True,
                                            min_val=None)
                            if area.explored >= explored and dice(chance*.33):
                                del(area.chars[id])

                                char = store.chars[id]
                                tracker.captured_chars.append(char)
                                temp = "Your team has captured a character: {}!".format(char.name)
                                temp = set_font_color(temp, "lawngreen")
                                tracker.log(temp)
                                if DEBUG_SE:
                                    msg = "{} has finished an exploration scenario. (Captured a uChar {})".format(team.name, char.id)
                                    se_debug(msg, mode="info")

                                self.env.exit("captured char")

                    # rChars:
                    if area.rchars:
                        for id, data in area.rchars.items():
                            explored, chance = data
                            chance = self.rewards_mod(tracker, chance, mb_ability=True,
                                            mb_risk=True,
                                            mb_exploration_day=True, mb_explored=True,
                                            min_val=None)
                            if area.explored >= explored and dice(chance*.33):
                                # Get tier:
                                if area.tier == 0:
                                    tier = random.uniform(.1, .3)
                                else:
                                    tier = random.uniform(area.tier*.8, area.tier*1.2)
                                tier = min(.1, tier)
                                tier = max(8, tier) # never build rChars over tier 8?

                                kwargs = {"tier": tier, "set_status": True}
                                if id != "any":
                                    kwargs["id"] = id

                                char = build_rc(**kwargs)
                                tracker.captured_chars.append(char)
                                temp = "Your team has captured a character: {}!".format(char.name)
                                temp = set_font_color(temp, "lawngreen")
                                tracker.log(temp)
                                if DEBUG_SE:
                                    msg = "{} has finished an exploration scenario. (Captured an rChar {})".format(team.name, char.id)
                                    se_debug(msg, mode="info")

                                self.env.exit("captured char")

                # Mobs Combat:
                if tracker.mobs and not self.env.now % 30:
                    ec = tracker.encounter_chance*.33/encountered_opfor
                    if dice(ec):
                        encountered_opfor += 1

                        if isinstance(tracker.mobs, list):
                            mob = choice(tracker.mobs)
                        elif isinstance(tracker.mobs, (set, dict)):
                            mob = choice(tracker.mobs.keys())
                        else:
                            mob = tracker.mobs

                        min_enemies = 2
                        max_ememies = 4
                        enemies = randint(min_enemies, max_ememies)

                        temp = "\n{} were attacked by ".format(team.name)
                        temp = temp + "%d %s!" % (enemies, plural(mob, enemies))
                        temp = set_font_color(temp, "orange")
                        log = tracker.log(temp, "Combat!", ui_log=True)

                        result, battle = self.combat_mobs(tracker, mob, enemies, log)
                        dead = set(team).intersection(battle.corpses)
                        if dead:
                            _result = self.death(tracker, dead=dead, kind='combat')
                            if _result == "full_death":
                                self.env.exit(_result)
                            elif _result == "fallback_to_guild":
                                self.env.exit(_result)

                        if self.assess_exploration_risk(tracker):
                            self.env.exit("retreat_to_camp")

                if self.env.now >= 99:
                    self.env.exit()

        def assess_exploration_risk(self, tracker):
            """Evals the risk to health.
            Returns True if the team has to fall back to camp.
            """
            team = tracker.team

            for member in team:
                if (member.health <= (member.get_max("health") / 100.0 * (100 - tracker.risk))) or check_stat_perc(member, "health", .15):
                    temp = "{color=[blue]}The team falls back to base due to risk factors!{/color}"
                    tracker.log(temp)
                    return True
            return False

        def combat_mobs(self, tracker, mob, opfor_team_size, log):
            # log is the Exploration Log object we add be reports to!
            # Do we really need to pass team size to this method instead of figuring everything out here?
            team = tracker.team
            opfor = Team(name="Enemy Team", max_size=opfor_team_size)

            if DEBUG_SE:
                msg = "{} is stating a battle scenario.".format(team.name)
                se_debug(msg, mode="info")

            # Get a level we'll set the mobs to:
            level = tracker.area.tier*20
            minl = max(1, level-3)
            maxl = max(5, level+3+tracker.day)
            level = randint(minl, maxl)

            # raise Exception(mob, tracker.area.mobs)
            for i in xrange(opfor_team_size):
                temp = build_mob(id=mob, level=level)
                temp.be.controller = BE_AI(temp)
                opfor.add(temp)

            for i in team:
                i.be.controller = BE_AI(i)

            # Logical battle scenario:
            battle = BE_Core(logical=True)
            store.battle = battle # Making battle global... I need to make sure this is not needed.
            battle.teams.append(team)
            battle.teams.append(opfor)
            battle.start_battle()

            # Add the battle report to log!:
            log.battle_log = list(reversed(battle.combat_log))

            # Reset the controllers:
            team.reset_controller()
            opfor.reset_controller()

            tracker.points -= 100*len(team)

            for mob in opfor:
                if mob in battle.corpses:
                    tracker.mobs_defeated[mob.id] += 1

            if battle.winner == team:
                log.suffix = "{color=[lawngreen]}Victory{/color}"
                for member in team:
                    if member in battle.corpses:
                        continue
                    temp = {"attack": randrange(3),
                            "agility": randrange(3),
                            "defence": randrange(3),
                            "magic": randrange(3)}
                    ss_reward(member, opfor, temp, apply=True)
                    member.exp += exp_reward(member, opfor)
                temp = "{color=[lawngreen]}Your team won!!{/color}\n"
                log.add(temp)

                if DEBUG_SE:
                    msg = "{} finished a battle scenario. Result: victory".format(team.name)
                    se_debug(msg, mode="info")

                return ("victory", battle)
            else: # Defeat here...
                log.suffix = "{color=[red]}Defeat{/color}"
                temp = "{color=[red]}Your team got their asses kicked!!{/color}\n"
                log.add(temp)

                if DEBUG_SE:
                    msg = "{} finished a battle scenario. Result: defeat".format(team.name)
                    se_debug(msg, mode="info")

                return ("defeat", battle)

        def setup_basecamp(self, tracker):
            # New type of shit, trying to get teams to coop here...
            area = tracker.area
            team = tracker.team
            teams = [t.team for t in area.trackers if t.state == "setting_up_basecamp"]

            if DEBUG_SE:
                msg = "Team {} is setting up basecamp.".format(team.name)
                se_debug(msg, mode="info")

            # TODO (se): Make sure this is adapted to building skill(s) once we have it!
            build_power = max(3, tracker.ability*.03)

            if len(teams) > 1:
                temp = "Teams: {} are setting up basecamp!".format(", ".join([t.name for t in teams]))
            else:
                temp = "Team {} is setting up basecamp!".format(teams[0].name)
            tracker.log(temp)

            while 1:
                if area.camp_build_points_current >= area.camp_build_points_required:
                    # Team done setting up the encampment:
                    temp = "Encampment is finished! Team is moving onto exploration!"
                    area.camp = True
                    tracker.state = "exploring"
                    tracker.log(temp)
                    self.env.exit()

                area.camp_build_points_current += build_power
                yield self.env.timeout(5) # We build...

                if not self.env.now % 25:
                    temp = "Basecamp is {} complete!".format(area.camp_build_status)
                    tracker.log(temp)

                if self.env.now >= 99:
                    self.env.exit()

            if DEBUG_SE:
                msg = "Team {} finished setting up basecamp.".format(team.name)
                se_debug(msg, mode="info")

        def death(self, tracker, dead=(), kind='combat'):
            """Handles death in the SE.
               Based mostly of risk factor.
               Death can occur with risk of 50+
            """
            risk = tracker.risk
            team = tracker.team
            tracker.flag_red = True

            # Set health to 1 (required when we don't kill anyone)
            for char in dead:
                char.health = 1
                char.enable_effect("Injured", duration=3)

            if risk <= 50:
                # We terminate the exploration but prevent death!
                if len(dead) == 1:
                    temp = "A fighter of {} was".format(tracker.team.name)
                else:
                    temp = "Fighters of {} were".format(tracker.team.name)
                if kind == 'combat':
                    temp = "{} badly injured in combat and are near death!".format(temp)
                elif kind == 'hazard':
                    temp = "{} badly injured by hazards and are near death!".format(temp)
                temp = set_font_color(temp, "orange")
                tracker.log(temp)

                return "fallback_to_guild"
            elif risk <= 90:
                if kind == 'combat':
                    temp = "{} were badly injured in combat!".format(tracker.team.name)
                elif kind == 'hazard':
                    temp = "{} were badly injured by hazard!".format(tracker.team.name)
                temp = set_font_color(temp, "orange")
                tracker.log(temp)
                for fighter in dead:
                    if dice(risk):
                        result = kill_char(fighter)
                        if result:
                            temp = "{} died...".format(fighter.name)
                            temp = set_font_color(temp, "red")
                            tracker.log(temp)

                            tracker.died.append(fighter)
                            team.remove(fighter)
                        else:
                            temp = "{} cannot die!".format(fighter.name)
                            temp = set_font_color(temp, "gray")
                            tracker.log(temp)
                    else:
                        temp = "{} is near death...".format(fighter.name)
                        temp = set_font_color(temp, "orange")
                        tracker.log(temp)

                if not len(team): # everyone died...
                    return "full_death"
                else:
                    return "fallback_to_guild"
            else: # risk 90+
                if kind == 'combat':
                    temp = "{} were badly injured in combat!".format(tracker.team.name)
                elif kind == 'hazard':
                    temp = "{} were badly injured by hazard!".format(tracker.team.name)
                temp = set_font_color(temp, "orange")
                temp += " But the stakes are high and risk is high so the team keeps on exploring..."
                tracker.log(temp)
                for fighter in dead:
                    result = kill_char(fighter)
                    if result:
                        temp = "{} died...".format(fighter.name)
                        temp = set_font_color(temp, "red")
                        tracker.log(temp)

                        tracker.died.append(fighter)
                        team.remove(fighter)
                    else:
                        temp = "{} cannot die!"
                        temp = set_font_color(temp, "gray")
                        tracker.log(temp)

            if not len(team): # everyone died...
                return "full_death"

        def rewards_mod(self, tracker, value, mb_ability=None, mb_risk=None,
                        mb_exploration_day=None, mb_explored=None,
                        min_val=None):
            """Takes a value, modifies it by SE concepts that might affect it and
            returns it.
            ability: Combination of team size and effectiveness considerations.
            risk: Risk at which the team operates at the area.
            exploration_day: 3 - 15 right now, it's the duration of a single exploration run.
            explored: how much of the area has already been explored. Usually high values increase
                the rewards.

            mb_ = mod by
            """
            area = tracker.area
            team = tracker.team

            risk = tracker.risk
            ability = tracker.ability
            eday = tracker.day
            explored = area.explored

            # Ability from base of 100:
            if mb_ability:
                value = value/100.0*ability

            # Risk from base of 100:
            if mb_risk:
                value = value/100.0*(risk+10)

            # eday with bonus of 100% the rewards from day 5 - 15:
            if mb_exploration_day and eday >= 5:
                bonus = eday - 5
                bonus /= 10.0
                if bonus <= .1:
                    bonus = .1

                value += value*bonus

            if mb_explored and explored > 50:
                value += value/100.0*(explored-50)

            if min_val and min_val > value:
                value = min_val

            return value

        # AP:
        def convert_AP(self, tracker):
            # Convert teams AP to Job points:
            # The idea here is that teammates will help each other to carry out
            # any task and act as a unit, so we don't bother tracking individual AP.
            team = tracker.team
            AP = 0
            for m in team:
                AP += m.AP
                m.AP = 0
            tracker.points = AP * 100
