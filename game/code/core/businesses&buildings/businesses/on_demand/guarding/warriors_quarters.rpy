init -5 python:
    class WarriorQuarters(OnDemandBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 15, "Bricks": 30, "Glass": 3}
        COST = 2500
        ID = "Warrior Quarters"
        IMG = "content/buildings/upgrades/guard_qt.jpg"
        def __init__(self, name="Warrior Quarters", instance=None, desc="Place for Guards!",
                     img="content/buildings/upgrades/guard_qt.jpg", build_effort=0,
                     materials=None, in_slots=2, ex_slots=1, cost=500, **kwargs):
            super(WarriorQuarters, self).__init__(name=name, instance=instance, desc=desc,
                                                  img=img, build_effort=build_effort,
                                                  materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Guarding"]])

        def business_control(self):
            """Handles normally guarding as a process.
            Basically we just wait for a combat even to occur or idle wait for it to happen.

            Only characters who are set to Guard are used for this purpose. If an event requires more,
            we get other workers involved in it as well.
            """
            building = self.instance
            make_nd_report_at = 0 # We build a report every 25 ticks but only if this is True!
            dirt_cleaned = 0 # We only do this for the ND report!

            cleaning = False # set to true if there is active cleaning in process
            using_all_service_workers = False
            using_all_workers = False

            power_flag_name = "ndd_cleaning_power"
            job = simple_jobs["Cleaning"]

            # Pure cleaners, container is kept around for checking during all_on_deck scenarios
            pure_cleaners = self.get_pure_cleaners(job, power_flag_name)
            all_cleaners = pure_cleaners.copy() # Everyone that cleaned for the report.
            cleaners = all_cleaners.copy() # cleaners on active duty

            while 1:

                c0 = make_nd_report_at
                c1 = self.env.now == make_nd_report_at
                if c0 and c1:
                    if config.debug:
                        temp = "{}: DEBUG! WRITING Guarding REPORT! c0: {}, c1: {}".format(self.env.now,
                                            c0, c1)
                        self.log(temp)
                    self.write_nd_report(pure_cleaners, all_cleaners, -dirt_cleaned)
                    make_nd_report_at = 0
                    dirt_cleaned = 0

                    # Release none-pure cleaners:
                    if dirt < 600 and using_all_workers:
                        using_all_workers = False
                        for worker in cleaners.copy():
                            if worker not in pure_cleaners:
                                cleaners.remove(worker)
                                self.instance.available_workers.insert(0, worker)

                    # and finally update all cleaners container:
                    all_cleaners = cleaners.copy()

                yield self.env.timeout(1)

        def get_pure_cleaners(self, job, power_flag_name):
            cleaners = set(self.get_workers(job, amount=float("inf"),
                           match_to_client=None, priority=True, any=False))

            if cleaners:
                # Do Disposition checks:
                job.settle_workers_disposition(cleaners, self)
                # Do Effectiveness calculations:
                self.calc_job_power(cleaners, job, power_flag_name)

            return cleaners

        def all_on_deck(self, cleaners, job, power_flag_name):
            # calls everyone in the building to clean it
            new_cleaners = self.get_workers(job, amount=float("inf"),
                            match_to_client=None, priority=True, any=True)

            if new_cleaners:
                # Do Disposition checks:
                job.settle_workers_disposition(new_cleaners, self, all_on_deck=True)
                # Do Effectiveness calculations:
                self.calc_job_power(new_cleaners, job, power_flag_name)

            return cleaners.union(new_cleaners)

        def calc_job_power(self, cleaners, job, power_flag_name, remove_from_available_workers=True):
            difficulty = self.instance.tier

            for w in cleaners:
                if not w.flag(power_flag_name):
                    effectiveness_ratio = job.effectiveness(w, difficulty)
                    if config.debug:
                        devlog.info("Cleaning Job Effectiveness: {}: {}".format(w.nickname, effectiveness_ratio))
                    # TODO It feels like this is handled in the effectiveness method already, kinda weird that it's done twice.
                    value = -((3 + w.get_skill("service") * .025 + w.agility * .03) * effectiveness_ratio)
                    w.set_flag(power_flag_name, value)

                    # Remove from active workers:
                    if remove_from_available_workers:
                        self.instance.available_workers.remove(w)


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
                # Set their defence capabilities as temp flag:
                value = round((1 + w.defence * 0.025 + w.agility * 0.3), 2) # Is defence sound here? We don't have guarding still...
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
                        # if not w.flag(flag_name) or w.flag(flag_name) <= 0:
                        #     self.convert_AP(w, workers, flag_name)

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
            self.write_nd_report(workers_original, workers)
            # simple_jobs["Guarding"](workers_original, workers, building, action="patrol")

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
                    if can_do_work(i, check_ap=False): # Check if we're still ok to work...
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

        def write_nd_report(self, pure_guards, all_guards):
            job, loc = self.job, self.instance
            log = NDEvent(job=job, loc=loc, team=pure_guards, business=self)

            pure_guards = set(pure_guards)
            all_guards = set(all_guards)

            extra_guards = all_guards - pure_guards

            temp = "{} Security Report!\n".format(loc.name)
            log.append(temp)

            wlen = len(all_guards)
            temp = "{} Workers kept your businesses safe today.".format(set_font_color(wlen, "red"))
            log.append(temp)

            log.img = Fixed(xysize=(820, 705))
            log.img.add(Transform(loc.img, size=(820, 705)))
            vp = vp_or_fixed(all_guards, ["fighting"], {"exclude": ["sex"], "resize": (150, 150)}, xmax=820)
            log.img.add(Transform(vp, align=(.5, .9)))

            log.team = all_guards

            if extra_guards:
                temp = "Security was lacking so your workers had to protect themselves! "
                if len(extra_cleaners) > 1:
                    temp += "{} were pulled off their duties to help out...".format(", ".join([w.nickname for w in extra_guards]))
                else:
                    temp += "{} was pulled off ger duty to help out...".format(", ".join([w.nickname for w in extra_guards]))
                log.append(temp)

            guards = all_guards - extra_guards
            temp = "{} worked hard keeping your businesses secure".format(", ".join([w.nickname for w in guards]))
            if extra_guards:
                temp += " as per their job assignment!"
            else:
                temp += "!"
            log.append(temp)

            # temp = "\nA total of {} dirt was cleaned.".format(set_font_color(dirt_cleaned, "red"))
            # log.append(temp)

            # Stat mods
            # log.logloc('dirt', dirt_cleaned)

            log.event_type = "jobreport" # Come up with a new type for team reports?

            log.after_job()
            NextDayEvents.append(log)
