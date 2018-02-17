init -5 python:
    class Cleaners(OnDemandBusiness):
        SORTING_ORDER = 1
        COMPATIBILITY = []
        MATERIALS = {"Wood": 2, "Bricks": 2}
        NAME = "Cleaning Block"
        DESC = "Until it shines!"
        IMG = "content/buildings/upgrades/cleaners.jpg"

        def __init__(self, **kwargs):
            super(Cleaners, self).__init__(**kwargs)

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
            building = self.building
            make_nd_report_at = 0 # We build a report every 25 ticks but only if this is True!
            dirt_cleaned = 0 # We only do this for the ND report!

            cleaning = False # set to true if there is active cleaning in process
            using_all_service_workers = False
            using_all_workers = False

            power_flag_name = "ndd_cleaning_power"
            job = simple_jobs["Cleaning"]

            # Pure cleaners, container is kept around for checking during all_on_deck scenarios
            pure_workers = self.get_pure_workers(job, power_flag_name)
            all_workers = pure_workers.copy() # Everyone that cleaned for the report.
            workers = all_workers.copy() # cleaners on active duty

            while 1:
                dirt = building.dirt
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
                        all_workers = self.all_on_deck(workers, job, power_flag_name)
                        workers = all_workers.union(workers)

                    if not make_nd_report_at and dirt:
                        wlen = len(workers)
                        make_nd_report_at = min(self.env.now+25, 100)
                        if self.env and wlen:
                            temp = "{}: {} Workers have started to clean {}!".format(self.env.now,
                                                set_font_color(wlen, "red"), building.name)
                            self.log(temp)
                elif dirt >= 600:
                    if not using_all_workers:
                        using_all_workers = True
                        all_workers = self.all_on_deck(workers, job, power_flag_name)
                        workers = all_workers.union(workers)

                    if not make_nd_report_at:
                        wlen = len(workers)
                        make_nd_report_at = min(self.env.now+25, 100)
                        if self.env and wlen:
                            temp = "{}: {} Workers have started to clean {}!".format(self.env.now,
                                                set_font_color(wlen, "red"), building.name)
                            self.log(temp)
                elif dirt >= 200:
                    if not make_nd_report_at:
                        wlen = len(workers)
                        make_nd_report_at = min(self.env.now+25, 100)
                        if self.env and wlen:
                            temp = "{}: {} Workers have started to clean {}!".format(self.env.now,
                                                set_font_color(wlen, "red"), building.name)
                            self.log(temp)

                # switch back to normal cleaners only
                if dirt <= 200 and using_all_workers:
                    using_all_workers = False
                    for worker in workers.copy():
                        if worker not in pure_workers:
                            workers.remove(worker)
                            building.available_workers.insert(0, worker)

                # Actually handle dirt cleaning:
                if make_nd_report_at and building.dirt > 0:
                    for w in workers.copy():
                        value = w.flag(power_flag_name)
                        dirt_cleaned += value
                        building.clean(value)

                        # Adjust JP and Remove the clear after running out of jobpoints:
                        w.jobpoints -= 5
                        if w.jobpoints <= 0:
                            temp = "{}: {} is done cleaning for the day!".format(self.env.now,
                                                set_font_color(w.nickname, "blue"))
                            self.log(temp)
                            workers.remove(w)

                # Create actual report:
                c0 = make_nd_report_at and dirt_cleaned
                c1 = building.dirt <= 0 or self.env.now == make_nd_report_at
                if c0 and c1:
                    if config.debug:
                        temp = "{}: DEBUG! WRITING CLEANING REPORT! c0: {}, c1: {}".format(self.env.now,
                                            c0, c1)
                        self.log(temp)
                    self.write_nd_report(pure_workers, all_workers, -dirt_cleaned)
                    make_nd_report_at = 0
                    dirt_cleaned = 0

                    # Release none-pure cleaners:
                    if dirt < 600 and using_all_workers:
                        using_all_workers = False
                        for worker in workers.copy():
                            if worker not in pure_workers:
                                workers.remove(worker)
                                building.available_workers.insert(0, worker)

                    # and finally update all cleaners container:
                    all_workers = workers.copy()

                yield self.env.timeout(1)

        def write_nd_report(self, pure_workers, all_workers, dirt_cleaned):
            job, loc = self.job, self.building
            log = NDEvent(job=job, loc=loc, team=all_workers, business=self)

            extra_workers = all_workers - pure_workers

            temp = "{} Cleaning Report!\n".format(loc.name)
            log.append(temp)

            wlen = len(all_workers)
            temp = "{} Workers cleaned the building today.".format(set_font_color(wlen, "red"))
            log.append(temp)

            log.img = Fixed(xysize=(820, 705))
            log.img.add(Transform(loc.img, size=(820, 705)))
            vp = vp_or_fixed(all_workers, ["maid", "cleaning"], {"exclude": ["sex"], "resize": (150, 150), "type": "any"})
            log.img.add(Transform(vp, align=(.5, .9)))

            log.team = all_workers

            if extra_workers:
                temp = "Dirt overwhelmed your building so extra staff was called to clean it! "
                if len(extra_workers) > 1:
                    temp += "{} were pulled off their duties to help out...".format(", ".join([w.nickname for w in extra_workers]))
                else:
                    temp += "{} was pulled off her duty to help out...".format(", ".join([w.nickname for w in extra_workers]))
                log.append(temp)

            workers = all_workers - extra_workers
            temp = "{} worked hard keeping your business clean".format(", ".join([w.nickname for w in workers]))
            if extra_workers:
                temp += " as it is their direct job!"
            else:
                temp += "!"
            log.append(temp)

            dirt_cleaned = int(dirt_cleaned)

            temp = "\nA total of {} dirt was cleaned.".format(set_font_color(dirt_cleaned, "red"))
            log.append(temp)

            # Stat mods
            log.logloc('dirt', dirt_cleaned)

            log.event_type = "jobreport" # Come up with a new type for team reports?

            log.after_job()
            NextDayEvents.append(log)
