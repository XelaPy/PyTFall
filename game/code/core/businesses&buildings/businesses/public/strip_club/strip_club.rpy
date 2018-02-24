init -5 python:
    class StripClub(PublicBusiness):
        COMPATIBILITY = []
        SORTING_ORDER = 4
        MATERIALS = {"Wood": 30, "Bricks": 50, "Glass": 10}
        NAME = "Strip Club"
        DESC = "Exotic Dancers go here!",
        IMG = "content/buildings/upgrades/strip_club.jpg"
        COST = 500
        def __init__(self, **kwargs):
            super(StripClub, self).__init__(**kwargs)

            self.jobs = set([simple_jobs["Striptease Job"]])

        def worker_control(self, worker):
            temp = "{} comes out to do striptease in {}!".format(
                                                worker.name, self.name)
            self.log(temp, True)

            du_working = 35

            # We create the log object here! And start logging to it directly!
            building = self.building
            job, loc = self.job, self.building
            log = NDEvent(job=job, char=worker, loc=loc, business=self)

            log.append("{} is performing Striptease!".format(worker.name))
            log.append("\n")

            difficulty = loc.tier
            effectiveness = job.effectiveness(worker, difficulty, log, False)

            if config.debug:
                log.append("Debug: Her effectiveness: {}! (difficulty: {}, Tier: {})".format(
                                effectiveness, difficulty, worker.tier))

            # Actively serving these clients:
            can_serve = 5 # We consider max of 5
            serving_clients = set() # actively serving these clients
            clients_served = [] # client served during the shift

            while worker.jobpoints > 0 and du_working > 0:
                # Add clients to serve:
                for c in self.clients_waiting.copy():
                    if len(serving_clients) < can_serve:
                        self.clients_waiting.remove(c)
                        self.clients_served.add(c)
                        c.served_by(worker, effectiveness)
                        serving_clients.add(c)
                        clients_served.append(c)
                    else:
                        break

                yield self.env.timeout(1)

                worker.jobpoints -= len(serving_clients)*2 # 2 jobpoints per client?

            if clients_served:
                if config.debug:
                    temp = "{}: Logging {} for {}!".format(self.env.now, self.name, worker.name)
                    self.log(temp)
                job.work_strip_club(worker, loc, log)

                earned = payout(job, effectiveness, difficulty, building, self, worker, clients_served, log)
                temp = "{}: {} earns {} by serving {} clients!".format(self.env.now,
                                                worker.name, earned, self.res.count)
                self.log(temp)

                # Create the job report and settle!
                log.after_job()
                NextDayEvents.append(log)
            else:
                temp = "{}: There were no clients for {} to serve".format(self.env.now, worker.name)
                self.log(temp)

            self.active_workers.remove(worker)
            temp = "{} is done with the job in {} for the day!".format(
                                set_font_color(worker.name, "red"),
                                self.name)
            self.log(temp, True)
