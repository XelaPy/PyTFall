init -5 python:
    class Bar(PublicBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 50, "Bricks": 30, "Glass": 5}
        COST = 5000
        ID = "Bar"
        IMG = "content/buildings/upgrades/bar.jpg"

        def __init__(self, name="Bar", instance=None, desc="Serve drinks and snacks to your customers!",
                     img="content/buildings/upgrades/bar.jpg", build_effort=0, materials=None,
                     in_slots=3, cost=500, **kwargs):
            super(Bar, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Bartending"]])
            self.workable = True
            self.type = "public_service"

            self.active_workers = set() # On duty Bartenders.
            self.clients = set() # Clients at the bar.

            # SimPy and etc follows (L33t stuff :) ):
            self.res = None # Restored before every job...
            self.time = 5
            self.is_running = False

        def worker_control(self, worker):
            temp = "{} comes out to tend bar in {}!".format(
                                                worker.name, self.name)
            self.log(temp, True)

            # We create the log object here! And start logging to it directly!
            job, loc = self.job, self.instance
            log = NDEvent(job=job, char=worker, loc=loc, business=self)

            log.append("{} is working the bar!".format(worker.name))
            log.append("\n")

            difficulty = loc.tier
            effectiveness = job.effectiveness(worker, difficulty, log, False)
            # Come up with a good way to figure out how many clients a worker can serve!
            can_serve_clients = 5
            if config.debug:
                log.append("Debug: Her effectiveness: {}! (difficulty: {}, Tier: {})".format(
                                effectiveness, difficulty, worker.tier))

            worker.set_flag("jobs_effectiveness", effectiveness)
            worker.set_flag("jobs_can_serve_clients", can_serve_clients)
            # Must be a list in case of doubles:
            worker.set_flag("jobs_clients_served", list())

            while worker.jobpoints > 0: #  and self.res.count:
                yield self.env.timeout(self.time)

                worker.jobpoints -= 100

            clients = worker.flag("jobs_clients_served")
            # Once the worker is done, we run the job and create the event:
            if clients:
                if config.debug:
                    temp = "{}: Logging {} for {}!".format(self.env.now, self.name, worker.name)
                    self.log(temp)
                job.work_bar(worker, clients, loc, log)

                earned = payout(job, effectiveness, difficulty, building, self, worker, clients, log)
                temp = "{}: {} earns {} by serving {} clients!".format(self.env.now,
                                                worker.name, earned, self.res.count)
                self.log(temp)

                # Create the job report and settle!
                log.after_job()
                NextDayEvents.append(log)
            else:
                temp = "{}: There were no clients for {} to serve".format(self.env.now, worker.name)
                self.log(temp)

            # log the tips:
            tips = worker.flag("jobs_tips")
            if tips:
                temp = "{} gets {} in tips in the bar!".format(worker.name, tips)
                self.log(temp, True)
                loc.fin.log_logical_income(tips, job.id + " Tips")

            self.active_workers.remove(worker)
            temp = "{} is done with the job in {} for the day!".format(
                                set_font_color(worker.name, "red"),
                                self.name)
            self.log(temp, True)
