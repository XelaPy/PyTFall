init -5 python:
    class WarriorQuarters(OnDemandBusiness):
        SORTING_ORDER = 2
        COMPATIBILITY = []
        MATERIALS = {"Wood": 15, "Bricks": 30, "Glass": 3}
        COST = 300
        NAME = "Warrior Quarters"
        IMG = "content/buildings/upgrades/guard_qt.webp"
        DESC = "Serve and Protect!"
        def __init__(self, **kwargs):
            super(WarriorQuarters, self).__init__(**kwargs)
            self.jobs = set([simple_jobs["Guarding"]])

        def business_control(self):
            """We decided for this to work similarly (or the same as cleaning routines)

            For now, goal is to get this to work reliably.
            """
            building = self.building
            make_nd_report_at = 0 # We build a report every 25 ticks but only if this is True!
            threat_cleared = 0 # We only do this for the ND report!

            guarding = False # set to true if there is active cleaning in process
            using_all_service_workers = False
            using_all_workers = False

            power_flag_name = "ndd_guarding_power"
            job = simple_jobs["Guarding"]

            # Upgrades:
            EnforcedOrder_active = False
            SparringQuarters_active = False
            for u in self.upgrades:
                if isinstance(u, EnforcedOrder):
                    EnforcedOrder_active = True
                elif isinstance(u, EnforcedOrder):
                    SparringQuarters_active = True

            # Brawl event:
            had_brawl_event = False

            # Pure workers, container is kept around for checking during all_on_deck scenarios
            pure_workers = self.get_pure_workers(job, power_flag_name, use_slaves=False)
            all_workers = pure_workers.copy() # Everyone that cleaned for the report
            workers = all_workers.copy() # workers on active duty

            while 1:
                simpy_debug("Entering WarriorQuarters.business_control at {}".format(self.env.now))

                threat = building.threat
                if DSNBR and not self.env.now % 5:
                    temp = "{color=[red]}" + "DEBUG: {0:.2f} Threat to THE BUILDING!".format(threat)
                    self.log(temp, True)

                if threat >= 900:
                    if True: # Add a condition similar to auto-cleaning? Or should this be forced?
                        price = 500*building.get_max_client_capacity()*(building.tier or 1)
                        price = min(hero.gold, price)
                        if hero.take_money(price, "Police"):
                            building.threat = 0
                            threat = 0
                            temp = "Police arrived at {}!".format(building.name)
                            temp += " You paid {} in penalty fees for allowing things to get this out of hand.".format(price)
                            temp += " {} reputation also took a very serious hit!".format(building.name)
                            building.modrep(-(50*min(1, building.tier)))
                            self.log(temp, True)

                    if not using_all_workers and threat:
                        using_all_workers = True
                        all_workers = self.all_on_deck(workers, job,
                                                power_flag_name, use_slaves=False)
                        workers = all_workers.union(workers)

                    if not make_nd_report_at and threat:
                        wlen = len(workers)
                        make_nd_report_at = min(self.env.now+25, 100)
                        if self.env and wlen:
                            temp = "{}: {} Workers have started to guard {}!".format(self.env.now,
                                                set_font_color(wlen, "red"), building.name)
                            self.log(temp)
                elif threat >= 700:
                    if not using_all_workers:
                        using_all_workers = True
                        all_workers = self.all_on_deck(workers, job,
                                            power_flag_name, use_slaves=False)
                        workers = all_workers.union(workers)

                    if not make_nd_report_at:
                        wlen = len(workers)
                        make_nd_report_at = min(self.env.now+25, 100)
                        if self.env and wlen:
                            temp = "{}: {} Workers have started to guard {}!".format(self.env.now,
                                                set_font_color(wlen, "red"), building.name)
                            self.log(temp)
                elif threat >= 200:
                    if not make_nd_report_at:
                        wlen = len(workers)
                        make_nd_report_at = min(self.env.now+25, 100)
                        if self.env and wlen:
                            temp = "{}: {} Workers have started to guard {}!".format(self.env.now,
                                                set_font_color(wlen, "red"), building.name)
                            self.log(temp)

                # switch back to normal workers only
                if threat <= 200 and using_all_workers:
                    using_all_workers = False
                    for worker in workers.copy():
                        if worker not in pure_workers:
                            workers.remove(worker)
                            building.available_workers.insert(0, worker)

                # Actually handle threat cleared:
                if make_nd_report_at and building.threat > 0:
                    for w in workers.copy():
                        value = w.flag(power_flag_name)
                        threat_cleared += value
                        building.threat += value

                        # Adjust JP and Remove the clear after running out of jobpoints:
                        w.jobpoints -= 5
                        w.up_counter("jobs_points_spent", 5)
                        if w.jobpoints <= 0:
                            temp = "{} is done guarding for the day!".format(
                                                w.nickname)
                            temp = set_font_color(temp, "cadetblue")
                            self.log(temp)
                            workers.remove(w)

                if EnforcedOrder_active and self.env.now > 0 and not self.env.now % 50:
                    self.log("Enforced order is making your civilian workers uneasy...")
                    for w in building.all_workers:
                        if not "Combatant" in w.gen_occs:
                            w.disposition -= 1
                            if dice(50):
                                w.joy -= 1

                # Create actual report:
                c0 = make_nd_report_at and threat_cleared
                c1 = building.threat <= 0 or self.env.now == make_nd_report_at
                if c0 and c1:
                    if DSNBR:
                        temp = "DEBUG! WRITING GUARDING REPORT! c0: {}, c1: {}".format(c0, c1)
                        self.log(temp, True)

                    c0 = self.env.now > 0 and not self.env.now % 25
                    if all([SparringQuarters_active, c0, threat < 500]):
                        use_SQ = True
                    else:
                        use_SQ = False
                    self.write_nd_report(pure_workers, all_workers,
                                         -threat_cleared, use_SQ=use_SQ)
                    make_nd_report_at = 0
                    threat_cleared = 0

                    # Release none-pure workers:
                    if threat < 700 and using_all_workers:
                        using_all_workers = False
                        for worker in workers.copy():
                            if worker not in pure_workers:
                                workers.remove(worker)
                                building.available_workers.insert(0, worker)

                    # and finally update all workers container:
                    all_workers = workers.copy()

                simpy_debug("Exiting WarriorQuarters.business_control at {}".format(self.env.now))
                if not EnforcedOrder_active and threat >= 500 and not had_brawl_event:
                    self.intercept(workers, power_flag_name)
                    had_brawl_event = True
                    yield self.env.timeout(5)
                else:
                    yield self.env.timeout(1)

        def write_nd_report(self, pure_workers, all_workers, threat_cleared, **kwargs):
            simpy_debug("Entering WarriorQuarters.write_nd_report at {}".format(self.env.now))
            job, loc = self.job, self.building
            log = NDEvent(job=job, loc=loc, team=all_workers, business=self)

            extra_workers = all_workers - pure_workers

            temp = "{} Security Report!\n".format(loc.name)
            log.append(temp)

            wlen = len(all_workers)
            temp = "{} Workers kept your businesses safe today.".format(set_font_color(wlen, "red"))
            log.append(temp)

            log.img = Fixed(xysize=ND_IMAGE_SIZE)
            log.img.add(Transform(loc.img, size=ND_IMAGE_SIZE))
            vp = vp_or_fixed(all_workers, ["fighting"],
                    {"exclude": ["sex"], "resize": (150, 150)}, xmax=ND_IMAGE_SIZE[0])
            log.img.add(Transform(vp, align=(.5, .9)))

            log.team = all_workers

            if extra_workers:
                temp = "Security threat became too high that non-combatant workers were called to mitigate it! "
                if len(extra_workers) > 1:
                    temp += "{} were pulled off their duties to help out...".format(", ".join([w.nickname for w in extra_workers]))
                else:
                    temp += "{} was pulled off her duty to help out...".format(", ".join([w.nickname for w in extra_workers]))
                log.append(temp)

            workers = all_workers - extra_workers
            temp = "{} worked hard keeping your business safe".format(", ".join([w.nickname for w in workers]))
            if extra_workers:
                temp += " as it is their direct job!"
            else:
                temp += "!"
            log.append(temp)

            threat_cleared = int(threat_cleared)

            temp = "\nA total of {} threat was removed.".format(set_font_color(threat_cleared, "red"))
            log.append(temp)

            if kwargs.get("use_SQ", False):
                log.append("Your guards managed to sneak in a friendly sparring match between their patrol duties!")
                for w in pure_workers:
                    ap_used = w.get_flag("jobs_points_spent", 0)/100.0
                    if dice(25):
                        log.logws("security", 1, char=w)
                        log.logws("attack", 1, char=w)
                        log.logws("agility", 1, char=w)
                        log.logws("defence", 1, char=w)
                        log.logws("magic", 1, char=w)
                        if dice(10):
                            log.logws("constitution", 1, char=w)
                        log.logws("exp", exp_reward(w, loc.tier, value=10,
                                                    ap_used=ap_used), char=w)

                        log.logws("vitality", -5, char=w)
                        if dice(20): # Small chance to get hurt.
                            log.logws("health", round_int(-w.get_max("health")*.2), char=w)

            if not len(all_workers):
                raise Exception("Zero Modulo Division Detected #01")
            # exp = threat_cleared/len(all_workers)
            for w in pure_workers:
                ap_used = w.get_flag("jobs_points_spent", 0)/100.0
                log.logws("security", randint(1, 3), char=w)
                if dice(30):
                    log.logws("attack", 1, char=w)
                if dice(30):
                    log.logws("defence", 1, char=w)
                if dice(30):
                    log.logws("magic", 1, char=w)
                if dice(30):
                    log.logws("agility", 1, char=w)
                if dice(10):
                    log.logws("constitution", 1, char=w)
                log.logws("exp", exp_reward(w, loc.tier, ap_used=ap_used), char=w)
                w.del_flag("jobs_points_spent")
            for w in extra_workers:
                ap_used = w.get_flag("jobs_points_spent", 0)/100.0
                log.logws("security", 1, char=w)
                if dice(10):
                    log.logws("attack", 1, char=w)
                if dice(10):
                    log.logws("defence", 1, char=w)
                if dice(10):
                    log.logws("magic", 1, char=w)
                if dice(10):
                    log.logws("agility", 1, char=w)
                if dice(10):
                    log.logws("constitution", 1, char=w)
                # Same imperfection as with Cleaning.
                log.logws("exp", exp_reward(w, loc.tier,
                                        ap_used=ap_used, final_mod=.5), char=w)
                w.del_flag("jobs_points_spent")

            # Stat mods
            log.logloc('threat', threat_cleared)

            log.event_type = "jobreport" # Come up with a new type for team reports?

            log.after_job()
            NextDayEvents.append(log)

            simpy_debug("Exiting WarriorQuarters.write_nd_report at {}".format(self.env.now))

        def intercept(self, workers, power_flag_name, interrupted=False):
            """This intercepts a bunch of aggressive clients and
                    resolves the issue through combat or intimidation.

            For beta, this is a simple function we trigger when threat
                level is high from the business_control method.

            Ideally, this should interrupt other processes but that is
                very time-costly to setup and is not required atm.

            We will also make it a separate report for the time being.
            """
            simpy_debug("Entering WarriorQuarters.intercept at {}".format(self.env.now))

            building = self.building
            job = simple_jobs["Guarding"]

            # gather the response forces:
            defenders = list()

            all_workers = self.all_on_deck(workers, job,
                                power_flag_name, use_slaves=False)
            defenders = all_workers.union(workers)

            # temp = "{}: {} Guards are intercepting attack event in {}".format(self.env.now, set_font_color(len(defenders), "red"), building.name)
            # self.log(temp)

            temp = "{color=[red]}A number of clients got completely out of hand!{/color}"
            self.log(temp, True)

            if not defenders:
                # If there are no defenders, we're screwed:
                temp = "No one was available to put them down"
                dirt = 400
                threat = 500
                temp += "\n  +{} Dirt and +{} Threat!".format(dirt, threat)
                self.log(temp)

                building.dirt += dirt
                building.threat += threat

                self.env.exit(False)
            else:
                temp = "{} Guards and employees are responding!".format(set_font_color(len(defenders), "red"), building.name)
                self.log(temp)

            # Prepare the teams:
            # Enemies:
            capacity = building.get_max_client_capacity()
            enemies = capacity/5
            enemies = min(10, max(enemies, 1)) # prolly never more than 10 enemies...

            # Note: We could draw from client pool in the future, for now,
            # we'll just generate offenders.
            enemy_team = Team(name="Hooligans", max_size=enemies)
            for e in range(enemies):
                enemy = build_client(gender="male", caste="Peasant", name="Hooligan",
                                 last_name="{}".format(e+1),
                                 pattern=["Combatant"], tier=building.tier+2.0)
                                 # Tier + 1.5 cause we don't give them any items so it's a brawl!
                enemy.front_row = True
                enemy.apply_trait("Fire")
                enemy.controller = BE_AI(enemy)
                enemy_team.add(enemy)

            defence_team = Team(name="Guardians Of The Galaxy", max_size=len(defenders))
            for i in defenders:
                i.controller = BE_AI(i)
                defence_team.add(i)

            # ImageReference("chainfights")
            global battle
            battle = BE_Core(logical=True, max_skill_lvl=6,
                        max_turns=(enemies+len(defenders))*4)
            battle.teams.append(defence_team)
            battle.teams.append(enemy_team)

            battle.start_battle()

            for i in defenders:
                i.controller = "player"

            # We also should restore the list if there was interruption:
            # if "active_workers_backup" in locals():
            #     for i in active_workers_backup:
            #         if can_do_work(i, check_ap=False): # Check if we're still ok to work...
            #             self.active_workers.append(i)

            # Build a Job report:
            # Create flag object first to pass data to the Job:
            # flag = Flags()
            # flag.set_flag("result", battle.winner == defence_team)
            # flag.set_flag("opfor", opfor)
            # job(defenders, defenders, building, action="intercept", flag=flag)

            # decided to add report in debug mode after all :)
            self.log(set_font_color("Battle Starts!", "crimson"))
            for entry in battle.combat_log:
                self.log(entry)
            self.log(set_font_color("=== Battle Ends ===", "crimson"))

            if battle.winner == defence_team:
                temp = "Interception is a Success!"
                temp = set_font_color(temp, "lawngreen")
                # temp = temp + set_font_color("....", "crimson")
                self.log(temp)
                building.threat -= 200
                building.dirt += 35*enemies
                # self.env.exit(True) # return True
            else:
                temp = "Interception Failed, your Guards have been defeated!"
                temp = set_font_color(temp, "crimson")
                # temp = temp + set_font_color("....", "crimson")
                self.log(temp)
                building.threat += 100
                building.dirt += 60*enemies
                # self.env.exit(False)

            simpy_debug("Exiting WarriorQuarters.intercept at {}".format(self.env.now))
