init -5 python:
    class StripClub(PublicBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 30, "Bricks": 50, "Glass": 10}
        COST = 8000
        ID = "Strip Club"
        IMG = "content/buildings/upgrades/strip_club.jpg"

        def __init__(self, name="Strip Club", instance=None, desc="Exotic Dancers go here!",
                     img="content/buildings/upgrades/strip_club.jpg", build_effort=0,
                     materials=None, in_slots=5, cost=500, **kwargs):
            super(StripClub, self).__init__(name=name, instance=instance,
                                            desc=desc, img=img, build_effort=build_effort,
                                            materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Striptease Job"]])
            self.workable = True
            self.type = "public_service"

            self.capacity = in_slots
            self.active_workers = set() # On duty Strippers.
            self.clients = set() # Clients watching the stripshows.

            self.res = None # Restored before every job...
            self.time = 5
            self.is_running = False

            self.earned_cash = 0

        def client_control(self, client):
            """Request for a spot for a client...

            Clients pay for the service here.
            We add dirt here.
            """
            with self.res.request() as request:
                yield request

                self.clients.add(client)
                temp = "{} enters the {}.".format(client.name, self.name)
                self.log(temp, True)

                dirt = 0
                flag_name = "jobs_spent_in_{}".format(self.name)
                du_to_spend_here = self.time*3 # 3 full terns

                while not client.flag("jobs_ready_to_leave"):
                    yield self.env.timeout(self.time)

                    dirt += randint(2, 3) # Move to business_control?

                    if client.flag("jobs_without_service") >= 10:
                        break

                    if client.flag(flag_name) >= du_to_spend_here:
                        break

                self.instance.dirt += dirt

                temp = "{} exits the {} leaving {} dirt behind.".format(
                                        client.name, self.name, dirt)
                self.log(temp, True)
                self.clients.remove(client)
                client.del_flag("jobs_busy")

        def add_worker(self):
            workers = self.instance.available_workers
            # Get all candidates:
            job = self.job
            ws = self.get_workers(job)
            if ws:
                w = ws.pop()
                self.active_workers.add(w)
                workers.remove(w)
                self.env.process(self.worker_control(w))

        def business_control(self):
            """This runs the club as a SimPy process from start to the end.

            I think that in case of a public business, we should handle serving the clients here.
            """

            counter = 0
            building = self.instance
            tier = building.tier

            while 1:
                every_5_du = not self.env.now % 5

                # if every_5_du:
                if True:
                    max_clients_to_service = sum([w.flag("jobs_can_serve_clients") for w in self.active_workers])
                    if len(self.clients) > max_clients_to_service:
                        new_workers_required = max(1, (len(self.clients)-max_clients_to_service)/4)
                        for i in range(new_workers_required):
                            self.add_worker()
                        max_clients_to_service = sum([w.flag("jobs_can_serve_clients") for w in self.active_workers])


                yield self.env.timeout(self.time)

                # Could be flipped to a job Brawl event?:
                if False:
                    if counter < 1 and self.env.now > 20:
                        counter += 1
                        for u in self.instance._upgrades:
                            if u.__class__ == WarriorQuarters:
                                process = u.request_action(building=self.instance, start_job=True, priority=True, any=False, action="patrol")[1]
                                u.interrupt = process # New field to which we can bind a process that can be interrupted.
                                break

                    # testing interruption:
                    if "process" in locals() and (counter == 1 and self.env.now > 40):
                        counter += 1
                        process.interrupt("fight")
                        self.env.process(u.intercept(interrupted=True))
                    #  =====================================>>>

                # Strip for clients (random worker is picked atm):
                workers = list(self.active_workers)
                if workers:
                    w = workers.pop()
                    can_service = w.flag("jobs_can_serve_clients")
                else:
                    w = None
                    can_service = None

                flag_name = "jobs_spent_in_{}".format(self.name)
                for c in self.clients:
                    c.up_counter(flag_name, self.time)

                    if can_service is None:
                        c.up_counter("jobs_without_service", self.time)
                    else:
                        c.del_flag("jobs_without_service")
                        can_service -= 1
                        w.flag("jobs_clients_served").append(c)
                        effectiveness = w.flag("jobs_effectiveness")
                        if effectiveness >= 150:
                            w.up_counter("jobs_tips", tier*randint(2, 3))
                        if effectiveness >= 100:
                            w.up_counter("jobs_tips", tier*randint(1, 2))

                    if can_service == 0:
                        if workers:
                            w = workers.pop()
                            can_service = w.flag("jobs_can_serve_clients")
                        else:
                            w = None
                            can_service = None

                if config.debug:
                    temp = "Debug: {} places are currently in use in {} | Total Cash earned so far: {}!".format(
                            set_font_color(self.res.count, "red"),
                            self.name,
                            self.earned_cash)
                    temp = temp + " {} Workers are currently on duty in {}!".format(
                            set_font_color(len(self.active_workers), "red"),
                            self.name)
                    self.log(temp, True)

                if not self.all_workers and not self.active_workers:
                    break

            # We remove the business from nd if there are no more strippers to entertain:
            temp = "There are no workers available in the {} so it is shutting down!".format(self.name)
            self.log(temp)
            building.nd_ups.remove(self)

        def worker_control(self, worker):
            temp = "{} comes out to do striptease in {}!".format(
                                                worker.name, self.name)
            self.log(temp, True)

            # We create the log object here! And start logging to it directly!
            job, loc = self.job, self.instance
            log = NDEvent(job=job, char=worker, loc=loc, business=self)

            log.append("{} is performing Strip Job!".format(worker.name))
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
                job.strip(worker, loc, log)

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
                temp = "{} gets {} in tips for stripping!".format(worker.name, tips)
                self.log(temp, True)
                loc.fin.log_logical_income(tips, job.id + " Tips")

            self.active_workers.remove(worker)
            temp = "{} is done with the job in {} for the day!".format(
                                set_font_color(worker.name, "red"),
                                self.name)
            self.log(temp, True)
