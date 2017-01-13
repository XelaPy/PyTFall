init -6 python:
    class Cleaners(OnDemandBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 2, "Bricks": 2}
        COST = 500
        ID = "Cleaners"
        IMG = "content/buildings/upgrades/cleaners.jpg"
        """This will be the first upgrade that will take care clearing some workload.

        This will have to work differently from any other upgrade... it prolly should have a request method that activates a cleaning routine and searches for willing workers.
        """
        def __init__(self, name="Cleaning Block", instance=None, desc="Until it shines!", img="content/buildings/upgrades/cleaners.jpg", build_effort=0, materials=None, in_slots=0, cost=0, **kwargs):
            super(Cleaners, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Cleaning"]])

        def request_cleaning(self, building=None, start_job=True, priority=True, any=False):
            """This checks if there are idle workers willing/ready to clean in the building.

            This will also start the job by default.
            Priority will call just the real cleaners.
            Any will also add everyone else who might be willing to clean.
            """

            if not building:
                building = self

            job = simple_jobs["Cleaning"]
            # dirt = building.get_dirt()
            cleaners = self.get_workers(job, amount=10, priority=priority, any=any)

            if not cleaners:
                return False # Noone to clean the building so we don't.
            else:
                # Might require optimization so we don't send all the cleaners to once.
                # Update worker lists:
                self.active_workers = cleaners[:]
                self.instance.available_workers = list(i for i in self.instance.available_workers if i not in cleaners)
                self.env.process(self.clean(cleaners, building))
                return True

        def clean(self, cleaners, building):
            """Cleaning the building...
            """
            cleaners_original = cleaners[:]
            power_flag_name = "jobs_cleaning_power"
            for w in cleaners:
                # Set their cleaning capabilities as temp flag:
                value = int(round(1 + w.get_skill("service") * 0.025 + w.agility * 0.3))
                w.set_flag(power_flag_name, value)

            wlen = len(cleaners)
            if self.env:
                t = self.env.now
                temp = "{}: {} Workers have started to clean {}!".format(self.env.now, set_font_color(wlen, "red"), building.name)
                self.log(temp)

            dirt = building.get_dirt()
            dirt_cleaned = 0
            counter = 0 # Just to make sure lines are not printed every du to the general building report.
            while cleaners and dirt - dirt_cleaned >= 10:
                # Job Points:
                flag_name = "_jobs_cleaning_points"
                for w in cleaners[:]:
                    if not w.flag(flag_name) or w.flag(flag_name) <= 0:
                        self.convert_AP(w, cleaners, flag_name)

                    # Cleaning itself:
                    if w in cleaners:
                        dirt_cleaned = dirt_cleaned + w.flag(power_flag_name)
                        w.mod_flag("_jobs_cleaning_points", -1) # 1 point per 1 dp? Is this reasonable...? Prolly, yeah.
                        w.mod_flag("job_cleaning_points_spent", 1) # So we know what to do during the job event buildup and stats application.

                if config.debug and self.env and not counter % 2:
                    wlen = len(cleaners)
                    # We run this once per 2 du and only for debug purposes.
                    temp = "{}: Debug: ".format(self.env.now)
                    temp = temp + " {} Workers are currently cleaning {}!".format(set_font_color(wlen, "red"), building.name)
                    temp = temp + set_font_color(" Cleaned: {} dirt".format(dirt_cleaned), "blue")
                    self.log(temp)

                # We may be running this outside of SimPy...
                if self.env:
                    yield self.env.timeout(1)
                counter = counter + 1

            temp = "{}: Cleaning process of {} is now finished!".format(self.env.now, building.name)
            temp = set_font_color(temp, "red")
            self.log(temp)

            # Once the loop is broken:
            # Restore the lists:
            self.active_workers = list()
            for w in cleaners:
                self.instance.available_workers.append(w)

            # Build the report:
            simple_jobs["Cleaning"](cleaners_original, cleaners, building, dirt, dirt_cleaned)


    class WarriorQuarters(OnDemandBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 15, "Bricks": 30, "Glass": 3}
        COST = 2500
        ID = "Warrior Quarters"
        IMG = "content/buildings/upgrades/guard_qt.jpg"
        def __init__(self, name="Warrior Quarters", instance=None, desc="Place for Guards!", img="content/buildings/upgrades/guard_qt.jpg", build_effort=0, materials=None, in_slots=2, ex_slots=1, cost=500, **kwargs):
            super(WarriorQuarters, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Guarding"]])

        def request_action(self, building=None, start_job=True, priority=True, any=False, action=None):
            """This checks if there are idle workers willing/ready to do an action in the building.

            This will also start the job by default.
            Priority will call just the real warriors.
            Any will also add everyone else who might be willing to act.

            TODO: Once done, see if this can be generalized like the previous two upgrade types!
            """
            if not action:
                raise Exception("Action Must Be provided to .request_action method!")

            if not building:
                building = self.instance

            job = simple_jobs["Guarding"]
            # dirt = building.get_dirt()
            workers = self.get_workers(job, amount=10, priority=priority, any=any)
            process = None
            if not workers:
                return False, process # No workers available
            else:
                # Might require optimization so we don't send all the warriors to once.
                # Update worker lists:
                if start_job:
                    if action == "patrol":
                        self.active_workers = workers[:]
                        self.instance.available_workers = list(i for i in self.instance.available_workers if i not in workers)
                        process = self.env.process(self.patrol(workers, building))
                return True, process

        def patrol(self, workers, building):
            """Patrolling the building...
            """
            workers_original = workers[:]
            power_flag_name = "jobs_guard_power"
            for w in workers:
                # Set their cleaning capabilities as temp flag:
                value = int(round(1 + w.defence * 0.025 + w.agility * 0.3)) # Is defence sound here? We don't have guarding still...
                w.set_flag(power_flag_name, value)

            wlen = len(workers)
            if self.env:
                t = self.env.now
                temp = "{}: {} guards are going to patrol halls of {}!".format(self.env.now, set_font_color(wlen, "red"), building.name)
                self.log(temp)

            counter = 0 # counter for du, lets say that a single patrol run takes 20 du...

            while (workers and counter <= 100) and self.env.now < 99:
                # Job Points:
                try:
                    flag_name = "_jobs_guard_points"
                    for w in workers[:]:
                        if not w.flag(flag_name) or w.flag(flag_name) <= 0:
                            self.convert_AP(w, workers, flag_name)

                        # Cleaning itself:
                        if w in workers:
                            w.mod_flag("_jobs_guard_points", 1) # 1 point per 1 dp? Is this reasonable...? Prolly, yeah.
                            w.mod_flag("job_guard_points_spent", 1) # So we know what to do during the job event buildup and stats application.

                    if config.debug and self.env and not counter % 4:
                        wlen = len(workers)
                        # We run this once per 2 du and only for debug purposes.
                        temp = "{}: Debug: ".format(self.env.now)
                        temp = temp + " {} Guards are currently patrolling {}!".format(set_font_color(wlen, "red"), building.name)
                        temp = temp + set_font_color(" DU spent: {}!".format(counter), "blue")
                        self.log(temp)

                    # We may be running this outside of SimPy... not really? not in this scenario anyway...
                    if self.env:
                        yield self.env.timeout(1)
                    counter = counter + 1

                except simpy.Interrupt as reason:
                    temp = "{}: Debug: ".format(self.env.now)
                    temp = temp + " {} Guards responding to an event ({}), patrol is halted in {}".format(set_font_color(wlen, "red"), reason.cause, building.name)
                    temp = temp + set_font_color("!!!!".format(counter), "crimson")
                    self.log(temp)

                    yield self.env.timeout(5)

                    temp = "{}: Debug: ".format(self.env.now)
                    temp = temp + " {} Guards finished their response to the event, back to patrolling {}".format(set_font_color(wlen, "red"), building.name)
                    temp = temp + set_font_color("....".format(counter), "crimson")
                    self.log(temp)

            temp = "{}: Patrol of {} is now finished! Guards are falling back to their quarters!".format(self.env.now, building.name)
            temp = set_font_color(temp, "red")
            self.log(temp)

            # Once the loop is broken:
            # Restore the lists:
            self.active_workers = list()
            for w in workers:
                self.instance.available_workers.append(w)

            # Build the report:
            simple_jobs["Guarding"](workers_original, workers, building, action="patrol")

        def intercept(self, opfor=None, interrupted=False):
            """This intercepts a bunch of aggressive clients and resolves the issue through combat or intimidation.

            opfor = opposition forces

            TODO:
            - This needs to gather the forces.
            - Return the result and put a hold on the business process if interception had failed.
            - Work with clients instead of props I am planning to use for testing.
            - Check if previous guard action was interrupted and act (look for defenders/restore older process) accordingly.
            """
            job = simple_jobs["Guarding"]
            opfor = list() if opfor is None else opfor

            # gather the response forces:
            defenders = list()
            if interrupted:
                active_workers_backup = self.active_workers[:]
                defenders = self.active_workers[:]
                self.active_workers = list()

            temp = self.get_workers(job, amount=10, match_to_client=None, priority=True, any=True) # Set amount according to opfor/manager:
            defenders = set(defenders + temp)

            temp = "{}: {} Guards are intercepting attack event in {}".format(self.env.now, set_font_color(len(defenders), "red"), building.name)
            self.log(temp)

            if not defenders:
                # If there are no defenders, we're screwed:
                temp = "{}: Noone was able to intercept attack event in {}".format(self.env.now, building.name)
                self.log(temp)
                self.env.exit(False) # TODO: Maybe more options than False and None?
            else:
                temp = "{}: {} Guards are intercepting attack event in {}".format(self.env.now, set_font_color(len(defenders), "red"), building.name)
                self.log(temp)

            # TODO: This should prolly be a function!
            # Prepare the teams:
            enemy_team = Team(name="Enemy Team", max_size=5) # TODO: max_size should be len(opfor)
            mob = build_mob(id="Goblin Shaman", level=30)
            mob.front_row = True
            mob.apply_trait("Fire")
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
            for i in xrange(4): # Testing 5 mobs...
                mob = build_mob(id="Goblin Archer", level=10)
                mob.front_row = False
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)

            defence_team = Team(name="Guardians Of The Galaxy", max_size=len(defenders))
            for i in defenders:
                i.controller = BE_AI(i)
                defence_team.add(i)

            # ImageReference("chainfights")
            global battle
            battle = BE_Core(logical=1)
            battle.teams.append(defence_team)
            battle.teams.append(enemy_team)

            battle.start_battle()

            for i in defenders:
                i.controller = "player"

            yield self.env.timeout(5)

            # We also should restore the list if there was interruption:
            if "active_workers_backup" in locals():
                for i in active_workers_backup:
                    if check_char(i, check_ap=False): # Check if we're still ok to work...
                        self.active_workers.append(i)
                        # TODO: Actual workers list should be here as well, not just the general one...

            # Build a Job report:
            # Create flag object first to pass data to the Job:
            flag = Flags()
            flag.set_flag("result", battle.winner == defence_team)
            flag.set_flag("opfor", opfor)
            job(defenders, defenders, self.instance, action="intercept", flag=flag)

            # decided to add report in debug mode after all :)
            if config.debug:
                self.log(set_font_color("Debug: Battle Starts!", "crimson"))
                for entry in reversed(battle.combat_log):
                    self.log(entry)
                self.log(set_font_color("=== Battle Ends ===", "crimson"))

            if battle.winner == defence_team:
                temp = "{}: Interception Success!".format(self.env.now)
                temp = temp + set_font_color("....", "crimson")
                self.log(temp)
                self.env.exit(True) # return True
            else:
                temp = "{}: Interception Failed, your Guards have been defeated!".format(self.env.now)
                temp = temp + set_font_color("....", "crimson")
                self.log(temp)
                self.env.exit(False)

        def convert_AP(self, w, workers, flag):
            # "Job Points": TODO: Remove this, temp code to help out with testing.
            if w.take_ap(1):
                value = 100
                w.set_flag(flag, value)
            else:
                workers.remove(w)
