init -5 python:
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
