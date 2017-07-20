init -5 python:
    class Cleaners(OnDemandBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 2, "Bricks": 2}
        COST = 500
        ID = "Cleaners"
        IMG = "content/buildings/upgrades/cleaners.jpg"
        def __init__(self, name="Cleaning Block", instance=None, desc="Until it shines!",
                     img="content/buildings/upgrades/cleaners.jpg", build_effort=0,
                     materials=None, in_slots=0, cost=0, **kwargs):
            super(Cleaners, self).__init__(name=name, instance=instance,
                  desc=desc, img=img, build_effort=build_effort,
                  materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Cleaning"]])

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

            power_flag_name = "_ndr_cleaning_power"
            job = simple_jobs["Cleaning"]

            # Pure cleaners, container is kept around for checking during all_on_deck scenarios
            pure_cleaners = self.get_pure_cleaners(job, power_flag_name)
            all_cleaners = pure_cleaners.copy() # Everyone that cleaned for the report.
            cleaners = all_cleaners.copy() # cleaners on active duty

            while 1:
                dirt = building.get_dirt()
                if config.debug:
                    temp = "{color=[red]}" + "{}: DEBUG: {} DIRT IN THE BUILDING!".format(self.env.now,
                                        dirt)
                    self.log(temp)

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
                        if self.env:
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
                        if self.env:
                            temp = "{}: {} Workers have started to clean {}!".format(self.env.now,
                                                set_font_color(wlen, "red"), building.name)
                            self.log(temp)
                elif dirt >= 200:
                    if not make_nd_report_at:
                        wlen = len(cleaners)
                        make_nd_report_at = min(self.env.now+25, 100)
                        if self.env:
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
                condition0 = make_nd_report_at and self.env.now == make_nd_report_at
                condition1 = make_nd_report_at and building.dirt <= 0
                if condition0 or condition1:
                    if config.debug:
                        temp = "{}: DEBUG! WRITING CLEANING REPORT! c0: {}, c1: {}".format(self.env.now,
                                            condition0, condition1)
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
                self.calc_job_effectiveness(cleaners, job, power_flag_name)

            return cleaners

        def all_on_deck(self, cleaners, job, power_flag_name):
            # calls everyone in the building to clean it
            new_cleaners = self.get_workers(job, amount=float("inf"),
                            match_to_client=None, priority=True, any=True)

            if new_cleaners:
                # Do Disposition checks:
                job.settle_workers_disposition(new_cleaners, self, all_on_deck=True)
                # Do Effectiveness calculations:
                self.calc_job_effectiveness(new_cleaners, job, power_flag_name)

            return cleaners.union(new_cleaners)

        def calc_job_effectiveness(self, cleaners, job, power_flag_name, remove_from_available_workers=True):
            difficulty = self.instance.tier
            for w in cleaners:
                if not w.flag(power_flag_name):
                    effectiveness = job.effectiveness(w, difficulty)
                    effectiveness += job.traits_and_effects_effectiveness_mod(w)

                    relative_ability = job.relative_ability(w, difficulty)

                    if config.debug:
                        devlog.info("Cleaning Job Effectiveness: {}: {}".format(w.nickname, effectiveness))
                    value = -int(round(3 + w.get_skill("service") * 0.025 + w.agility * 0.03))
                    w.set_flag(power_flag_name, value)

                    # Remove from active workers:
                    if remove_from_available_workers:
                        self.instance.available_workers.remove(w)

        def write_nd_report(self, pure_cleaners, all_cleaners, dirt_cleaned):
            job, loc = self.job, self.instance
            log = NDEvent(job=job, loc=loc, team=all_cleaners, business=self)

            extra_cleaners = all_cleaners - pure_cleaners

            temp = "{} Cleaning Report!\n".format(loc.name)
            log.append(temp)

            wlen = len(all_cleaners)
            temp = "{} Workers cleaned the building today.".format(set_font_color(wlen, "red"))
            log.append(temp)

            log.img = Fixed(xysize=(820, 705))
            log.img.add(Transform(loc.img, size=(820, 705)))
            vp = vp_or_fixed(pure_cleaners, ["maid", "cleaning"], {"exclude": ["sex"], "resize": (150, 150), "type": "any"})
            log.img.add(Transform(vp, align=(.5, .9)))

            log.team = all_cleaners

            if extra_cleaners:
                temp = "Dirt overwhelmed your building so extra staff was called to clean it! "
                if len(extra_cleaners) > 1:
                    temp += "{} were pulled off their duties to help out...".format(", ".join([w.nickname for w in extra_cleaners]))
                else:
                    temp += "{} was pulled off ger duty to help out...".format(", ".join([w.nickname for w in extra_cleaners]))
                log.append(temp)

            cleaners = all_cleaners - extra_cleaners
            temp = "{} worked hard keeping your business clean".format(", ".join([w.nickname for w in cleaners]))
            if extra_cleaners:
                temp += " as it is their direct job!"
            else:
                temp += "!"
            log.append(temp)

            temp = "\nA total of {} dirt was cleaned.".format(set_font_color(dirt_cleaned, "red"))
            log.append(temp)

            # Stat mods
            log.logloc('dirt', dirt_cleaned)

            log.event_type = "jobreport" # Come up with a new type for team reports?

            log.after_job()
            NextDayEvents.append(log)
