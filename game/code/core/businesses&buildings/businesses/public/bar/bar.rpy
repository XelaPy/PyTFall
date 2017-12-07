init -5 python:
    class Bar(PublicBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 50, "Bricks": 30, "Glass": 5}
        COST = 5000
        ID = "Bar"
        IMG = "content/buildings/upgrades/bar.jpg"

        def __init__(self, name="Bar", instance=None, desc="Serve drinks and snacks to your customers!", img="content/buildings/upgrades/bar.jpg", build_effort=0, materials=None, in_slots=3, cost=500, **kwargs):
            super(Bar, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Bartending"]])
            self.workable = True
            self.type = "public_service"

            self.capacity = in_slots
            self.active_workers = set() # On duty Bartenders.
            self.clients = set() # Clients at the bar.

            # SimPy and etc follows (L33t stuff :) ):
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
                yield request # TODO: WE PROLLY DO NOT NEED A SIMPY RESOURCE HERE...

                # All is well and we create the event:
                temp = "{}: {} enters the {}.".format(self.env.now, client.name, self.name)
                self.clients.add(client)
                self.log(temp)

                while not client.flag("jobs_ready_to_leave"):
                    yield self.env.timeout(1)

                # This stuff should be better conditioned later:
                if self.instance.manager: # add more conditioning:
                    cash = randint(2, 4)
                else:
                    cash = randint(1, 3)
                dirt = randint(2, 3)
                self.earned_cash += cash
                self.log_income(cash)
                self.instance.dirt += dirt

                temp = "{}: {} exits the {} leaving {} Gold and {} Dirt behind.".format(self.env.now,
                                                                client.name, self.name, cash, dirt)
                self.clients.remove(client)
                self.log(temp)
                client.del_flag("jobs_busy")

        def add_worker(self):
            if not self.active_workers or len(self.active_workers) < self.res.count/4:
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
            """
            # See if there are any strip girls, that may be added to Resource at some point of the development:
            counter = 0
            while 1:
                yield self.env.timeout(self.time)

                # Temp code: =====================================>>>
                # TODO: Should be turned into Job Event.
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

                # Handle the earnings:
                # cash = self.res.count*len(self.active_workers)*randint(8, 12)
                # self.earned_cash += cash # Maybe it's better to handle this on per client basis in their own methods? Depends on what modifiers we will use...

                # Manage clients... We send clients on his/her way:
                flag_name = "jobs_spent_in_{}".format(self.name)
                for c in self.clients:
                    c.mod_flag(flag_name, self.time)
                    if c.flag(flag_name) >= self.time*2:
                        c.set_flag("jobs_ready_to_leave")

                if config.debug:
                    temp = "{}: Debug: {} places are currently in use in {} | Total Cash earned so far: {}!".format(self.env.now, set_font_color(self.res.count, "red"), self.name, self.earned_cash)
                    temp = temp + " {} Workers are currently on duty in {}!".format(set_font_color(len(self.active_workers), "red"), self.name)
                    self.log(temp)

                if not self.all_workers and not self.active_workers:
                    break

            # We remove the business from nd if there are no more strippers to entertain:
            temp = "There are no workers available in the {} so it is shutting down!".format(self.name)
            self.log(temp)
            self.instance.nd_ups.remove(self)

        def worker_control(self, worker):
            temp = "{}: {} comes out to serve customers in {}!".format(self.env.now,
                                                            worker.name, self.name)
            self.log(temp)

            # We create the log object here! And start logging to it directly!
            job, loc = self.job, self.instance
            log = NDEvent(job=job, char=worker, loc=loc, business=self)

            log.append("{} is tending the bar at {}!".format(worker.name, self.instance.name))
            log.append("\n")

            difficulty = self.instance.tier
            effectiveness = job.effectiveness(worker, difficulty, log, False)
            if config.debug:
                log.append("Debug: Her effectiveness: {}! (difficulty: {}, worker tier: {})".format(effectiveness, difficulty, worker.tier))

            clients = set() # list of clients this worker is severing
            max_clients = 5 # Come up with a good way to figure out how many clients a worker can serve!
            tips = 0 # Tips the worker is going to get!

            while worker.jobpoints and self.res.count:
                yield self.env.timeout(self.time) # This is a single shift a worker can take for cost of 1 AP.

                # Account for clients that left...
                clients = {c for c in clients if c in self.clients} # There might be a better way to handle this!
                if len(clients) < max_clients: # Find some clients for worker to take care of:
                    temp = [c for c in self.clients if not c.flag("jobs_attended_by")]
                    can_service = max_clients - len(clients)
                    if len(temp) > can_service:
                        temp = random.sample(temp, can_service)
                    for client in temp:
                        client.set_flag("jobs_attended_by", worker)
                    clients = clients.union(temp)

                # Visit counter:
                for client in self.clients:
                    client.up_counter("got_serviced_by" + worker.id)

                worker.jobpoints -= 100
                # TODO Is this worth adjusting to lower base???

                if effectiveness > 200:
                    tips += randint(3, 5) * self.instance.tier
                elif effectiveness > 100:
                    tips += randint(1, 3) * self.instance.tier

                temp = "{}: {} gets {} in tips from {} clients!".format(self.env.now,
                                                worker.name, tips, self.res.count)
                self.log(temp)

            # Once the worker is done, we run the job and create the event:
            if clients:
                if config.debug:
                    temp = "{}: Logging {} for {}!".format(self.env.now, self.name, worker.name)
                    self.log(temp)
                job.bar_task(worker, clients, loc, log)

                # Create the job report and settle!
                log.after_job()
                NextDayEvents.append(log)
            else:
                temp = "{}: There were no clients for {} to serve".format(self.env.now, worker.name)
                self.log(temp)

            # log the tips
            # self.log_income(tips)
            if tips:
                worker.mod_flag("jobs_tips", tips)
                loc.fin.log_logical_income(tips, job.id + " Tips")

            self.active_workers.remove(worker)
            temp = "{}: {} is done with the job in {} for the day!".format(self.env.now,
                                        set_font_color(worker.name, "red"), self.name)
            self.log(temp)
