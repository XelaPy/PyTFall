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
            """This checks if there are idle workers willing/ready to clean in the building.
            Cleaning is always active, checked on every tick.
            Cleaners are on call at all times.
            Whenever dirt reaches 200, they start cleaning till it’s 0 or are on standby on idle otherwise.
            If dirt reaches 600 (they cannot coop or there are simply no pure cleaners),
            all “Service Types” that are free help out and they are released when dirt reaches 50 or below.
            If dirt reaches 900, we check for auto-cleaning and do the “magical” thing if player has
            the money and is willing to pay (there is a checkbox for that already).
            If there is no auto-cleaning, we call all workers in the building to clean…
            unless they just refuse that on some principal (trait checks)...
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
            pure_cleaners = self.get_pure_workers(job, power_flag_name)
            all_cleaners = pure_cleaners.copy() # Everyone that cleaned for the report.
            cleaners = all_cleaners.copy() # cleaners on active duty

            while 1:
                dirt = building.get_dirt()
                if config.debug and not self.env.now % 5:
                    temp = "{color=[red]}" + "DEBUG: {0:.2f} DIRT IN THE BUILDING!".format(dirt)
                    self.log(temp, True)

                if dirt >= 900:
                    if building.auto_clean:
                        price = building.get_cleaning_price()
                        if hero.take_money(price):
                            building.dirt = 0
                            dirt = 0
                            temp = "{}: {} Building was auto-cleaned!".format(self.env.now,
                                                building.name)
                            self.log(temp)

                    if not using_all_workers and dirt:
                        using_all_workers = True
                        all_cleaners = self.all_on_deck(cleaners, job, power_flag_name)
                        cleaners = all_cleaners.union(cleaners)

                    if not make_nd_report_at and dirt:
                        wlen = len(cleaners)
                        make_nd_report_at = min(self.env.now+25, 100)
                        if self.env and wlen:
                            temp = "{}: {} Workers have started to clean {}!".format(self.env.now,
                                                set_font_color(wlen, "red"), building.name)
                            self.log(temp)
                elif dirt >= 600:
                    if not using_all_workers:
                        using_all_workers = True
                        all_cleaners = self.all_on_deck(cleaners, job, power_flag_name)
                        cleaners = all_cleaners.union(cleaners)

                    if not make_nd_report_at:
                        wlen = len(cleaners)
                        make_nd_report_at = min(self.env.now+25, 100)
                        if self.env and wlen:
                            temp = "{}: {} Workers have started to clean {}!".format(self.env.now,
                                                set_font_color(wlen, "red"), building.name)
                            self.log(temp)
                elif dirt >= 200:
                    if not make_nd_report_at:
                        wlen = len(cleaners)
                        make_nd_report_at = min(self.env.now+25, 100)
                        if self.env and wlen:
                            temp = "{}: {} Workers have started to clean {}!".format(self.env.now,
                                                set_font_color(wlen, "red"), building.name)
                            self.log(temp)

                # switch back to normal cleaners only
                if dirt <= 200 and using_all_workers:
                    using_all_workers = False
                    for worker in cleaners.copy():
                        if worker not in pure_cleaners:
                            cleaners.remove(worker)
                            self.instance.available_workers.insert(0, worker)

                # Actually handle dirt cleaning:
                if make_nd_report_at and building.dirt > 0:
                    for w in cleaners.copy():
                        value = w.flag(power_flag_name)
                        dirt_cleaned += value
                        building.clean(value)

                        # Adjust JP and Remove the clear after running out of jobpoints:
                        w.jobpoints -= 5
                        if w.jobpoints <= 0:
                            temp = "{}: {} is done cleaning for the day!".format(self.env.now,
                                                set_font_color(w.nickname, "blue"))
                            self.log(temp)
                            cleaners.remove(w)

                # Create actual report:
                c0 = make_nd_report_at and dirt_cleaned
                c1 = building.dirt <= 0 or self.env.now == make_nd_report_at
                if c0 and c1:
                    if config.debug:
                        temp = "{}: DEBUG! WRITING CLEANING REPORT! c0: {}, c1: {}".format(self.env.now,
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
