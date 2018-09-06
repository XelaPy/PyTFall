init -12 python:
    #################################################################
    # BUILDING UPGRADE CLASSES:
    class CoreExtension(_object):
        """BaseClass for any building expansion! (aka Business)
        """
        # Class attributes serve as default, they are fed to a method of UpgradableBuilding,
        # adjusted and displayed to the player. In most of the cases, Extension will be created
        # using these (alt is from JSON/Custom data):
        NAME = "Extension"
        DESC = "Core Extension."
        IMG = "no_image"
        SORTING_ORDER = 0
        MATERIALS = {}
        COST = 100
        IN_SLOTS = 2
        EX_SLOTS = 0
        CAPACITY = 0

        EXP_CAP_IN_SLOTS = 1
        EXP_CAP_EX_SLOTS = 0
        EXP_CAP_COST = 100

        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.name = kwargs.get("name", self.NAME)
            self.desc = kwargs.get("desc", self.DESC)
            self.img = renpy.displayable(kwargs.get("img", self.IMG))

            self.building = kwargs.get("building", None) # Building this upgrade belongs to.

            self.cost = kwargs.pop("cost", self.COST)
            self.in_slots = kwargs.pop("in_slots", self.IN_SLOTS)
            self.ex_slots = kwargs.pop("ex_slots", self.EX_SLOTS)
            self.materials = kwargs.pop("materials", self.MATERIALS)

            # This means that we can add capacity to this business.
            # Slots/Cost are the cost of a single expansion!
            self.capacity = kwargs.get("capacity", self.CAPACITY)
            self.expands_capacity = kwargs.get("expands_capacity", True)
            self.exp_cap_in_slots = kwargs.pop("exp_cap_in_slots", self.EXP_CAP_IN_SLOTS)
            self.exp_cap_ex_slots = kwargs.pop("exp_cap_ex_slots", self.EXP_CAP_EX_SLOTS)
            self._exp_cap_cost = kwargs.pop("exp_cap_cost", self.EXP_CAP_COST)

        @property
        def exp_cap_cost(self):
            # Does not scale! If scaled, update the building/business cost methods!
            building = self.building
            return self._exp_cap_cost * (building.tier or 1)

        def can_extend_capacity(self):
            building = self.building

            if not self.expands_capacity:
                return False
            if (building.in_slots + self.exp_cap_in_slots) > building.in_slots_max:
                return False
            if (building.ex_slots + self.exp_cap_ex_slots) > building.ex_slots_max:
                return False
            if hero.gold < self.exp_cap_cost:
                return False

            return True

        def expand_capacity(self, value=1):
            self.in_slots += self.exp_cap_in_slots
            self.building.in_slots += self.exp_cap_in_slots
            self.ex_slots += self.exp_cap_ex_slots
            self.building.ex_slots += self.exp_cap_ex_slots

            hero.take_money(self.exp_cap_cost, "Business Expansion")
            self.capacity += 1

        def get_price(self):
            # Returns our best guess for price of the business
            # Needed for buying, selling the building or for taxation.
            price = self.cost * (self.building.tier or 1)
            price += self.capacity*self.exp_cap_cost
            return price


    class Business(CoreExtension):
        """BaseClass for any building expansion! (aka Business)
        """
        NAME = "Business"
        DESC = "Business"
        CAPACITY = 2
        def __init__(self, **kwargs):
            super(Business, self).__init__(**kwargs)

            # Jobs this upgrade can add. *We add job instances here!
            # It may be a good idea to turn this into a direct job assignment instead of a set...
            self.jobs = set()
            self.workers = set() # List of on duty characters.
            self.clients = set() # Local clients, this is used during next day and reset on when that ends.

            # If False, no clients are expected.
            # If all businesses in the building have this set to false, no client stream will be generated at all.
            self.expects_clients = False
            self.habitable = False
            self.workable = False
            # If not active, business is not executed and is considered "dead",
            # we run "inactive" method with a corresponding simpy process in this case.
            self.active = True

            # @Review: From Business class which seemed useless to me...
            self.blocked_upgrades = kwargs.get("blocked_upgrades", list())
            self.allowed_upgrades = kwargs.get("allowed_upgrades", list())
            self.in_construction_upgrades = list() # Not used yet!
            self.upgrades = list()

        def get_client_count(self):
            """Returns amount of clients we expect to come here.

            Right now we base our best guess on time and cap.
            """
            # .7 is just 70% of absolute max (to make upgrades meaningful).
            # 101.0 is self.env duration.
            # self.time is amount of time we expect to spend per client.
            if not self.time:
                raise Exception("Zero Modulo Division Detected #02")
            amount = round_int(((101.0/self.time)*self.capacity)*.7)

            return amount

        @property
        def job(self):
            # This may not be required if we stick to a single job per business scenario:
            if self.jobs:
                return random.sample(self.jobs, 1).pop()

        # Reputation:
        # Prolly not a good idea to mess with this on per business basis, at least at first...
        # @property
        # def rep(self):
        #     return self._rep
        #
        # @rep.setter
        # def rep(self, value):
        #     self._rep = self._rep + value
        #     if self._rep > 1000:
        #         self._rep = 1000
        #     elif self._rep < -1000:
        #         self._rep = -1000

        @property
        def env(self):
            return self.building.env

        def log(self, item, add_time=False):
            # Logs the text for next day event...
            self.building.log(item, add_time=add_time)

        # Worker methods:
        def has_workers(self, amount=1):
            # Checks if there is a worker(s) available.
            return False

        @property
        def all_workers(self):
            # This may be a poor way of doing it because different upgrades could have workers with the same job assigned to them.
            # Basically what is needed is to allow setting a business to a worker as well as the general building if required...
            # And this doesn't work? workers are never populated???
            return list(i for i in self.building.available_workers if self.all_occs & i.occupations)

        def action_priority_workers(self, job):
            return list(i for i in self.building.available_workers if i.action == job)

        def get_workers(self, job, amount=1, match_to_client=None,
                        priority=True, any=True, use_slaves=True):
            """Tries to find workers for any given job.

            priority: Tries to get a perfect match where action == job first.
            any: Tries to get any match trying to match any occupation at all.

            @param: match_to_client: Will try to find the a good match to client, expects a client (or any PytC instance with .likes set) object.
            """
            workers = list()

            if priority:
                priorityw = self.action_priority_workers(job)
                if not use_slaves:
                    priorityw = [w for w in priorityw if w.status != "slave"]

                shuffle(priorityw)
                while len(workers) < amount and priorityw:
                    if match_to_client:
                        w = self.find_best_match(match_to_client, priorityw) # This is not ideal as we may end up checking a worker who will soon be removed...
                    else:
                        w = priorityw.pop()
                    if self.check_worker_capable(w) and self.check_worker_willing(w, job):
                        workers.append(w)

            if any:
                anyw = list(i for i in self.all_workers if i not in priorityw) if priority else self.all_workers[:]
                if not use_slaves:
                    anyw = [w for w in anyw if w.status != "slave"]

                shuffle(anyw)
                while len(workers) < amount and anyw:
                    if match_to_client:
                        w = self.find_best_match(match_to_client, anyw) # This is not ideal as we may end up checking a worker who will soon be removed...
                    else:
                        w = anyw.pop()
                    if self.check_worker_capable(w) and self.check_worker_willing(w, job):
                        workers.append(w)

            return workers

        def find_best_match(self, client, workers):
            """Attempts to match a client to a worker.

            This intersects worker traits with clients likes and acts accordingly.
            Right now it will not try to find the very best match and instead will break on the first match found.
            Returns a worker at random if that fails.
            """
            for w in workers[:]:
                likes = client.likes.intersection(w.traits)
                if likes:
                    slikes = ", ".join([str(l) for l in likes])
                    temp0 = '{} liked {} for {} {}.'.format(
                        set_font_color(client.name, "beige"),
                        set_font_color(w.nickname, "pink"),
                        slikes, plural("trait", len(likes)))
                    temp1 = '{} found {} {} in {} very appealing.'.format(
                        set_font_color(client.name, "beige"),
                        slikes, plural("trait", len(likes)),
                        set_font_color(w.nickname, "pink"))
                    self.log(choice([temp0, temp1]))
                    worker = w
                    workers.remove(w)
                    client.set_flag("jobs_matched_traits", likes)
                    break
            else:
                worker = workers.pop()
            return worker

        def check_worker_willing(self, worker, job):
            """Checks if the worker is willing to do the job.

            Removes worker from instances master list.
            Returns True is yes, False otherwise.
            """
            building = self.building

            if job.is_valid_for(worker):
                if DSNBR:
                    temp = set_font_color("Debug: {} worker (Occupations: {}) with action: {} is doing {}.".format(
                                          worker.nickname, ", ".join(list(str(t) for t in worker.occupations)), worker.action, job.id), "lawngreen")
                    self.log(temp, True)
                return True
            else:
                if worker in building.available_workers:
                    building.available_workers.remove(worker)

                if DSNBR:
                    temp = set_font_color('Debug: {} worker (Occupations: {}) with action: {} refuses to do {}.'.format(
                            worker.nickname, ", ".join(list(str(t) for t in worker.occupations)),
                            worker.action, job.id), "red")
                    self.log(temp)
                else:
                    temp = set_font_color('{} is refuses to do {}!'.format(worker.name, job.id), "red")
                    self.log(temp)

                return False

        def check_worker_capable(self, worker):
            """Checks if the worker is capable of doing the job.

            Removes worker from instances master list.
            Returns True is yes, False otherwise.
            """
            building = self.building

            if can_do_work(worker):
                return True
            else:
                if worker in building.available_workers:
                    building.available_workers.remove(worker)
                temp = set_font_color('{} is done working for the day.'.format(worker.name), "cadetblue")
                self.log(temp)
                return False

        def convert_AP(self, worker):
            self.building.convert_AP(worker)

        # Runs before ND calcs stats for this building.
        def pre_nd(self):
            # Runs at the very start of execution of SimPy loop during the next day.
            return

        @property
        def all_occs(self):
            s = set()
            for j in self.jobs:
                s = s | j.all_occs
            return s

        def log_income(self, amount, reason=None):
            # Plainly logs income to the main building finances.
            if not reason:
                reason = self.name
            self.building.fin.log_logical_income(amount, reason)

        def post_nd_reset(self):
            # Resets all flags and variables after next day calculations are finished.
            pass

        def inactive_process(self):
            temp = "{} is currently inactive, no actions will be conducted here!".format(self.name)
            self.log(temp)
            yield self.env.timeout(100)

        # SimPy:
        def business_control(self):
            """SimPy business controller.
            """
            while 1:
                yield self.env.timeout(100)

        # Business MainUpgrade related:
        def add_upgrade(self, upgrade, pay=False):
            building = self.building

            cost, materials, in_slots, ex_slots = building.get_extension_cost(upgrade)
            building.in_slots += in_slots
            building.ex_slots += ex_slots

            if pay:
                building.pay_for_extension(cost, materials)

            upgrade.building = building
            upgrade.business = self
            self.upgrades.append(upgrade)
            self.upgrades.sort(key=attrgetter("SORTING_ORDER"), reverse=True)

        def all_possible_extensions(self):
            # Named this was to conform to GUI (same as for Buildings)
            return self.allowed_upgrades

        def has_extension(self, upgrade_class):
            # Named this was to conform to GUI (same as for Buildings)
            return upgrade_class in [u.__class__ for u in self.upgrades]

        def check_upgrade_compatibility(self, upgrade):
            return self.__class__ in upgrade.COMPATIBILITY # How is this different from allowed?

        def check_upgrade_allowance(self, upgrade):
            return upgrade.__class__ in self.allowed_upgrades


    class PrivateBusiness(Business):
        SORTING_ORDER = 3
        NAME = "Private Business"
        DESC = "Client is always right!?!"
        def __init__(self, **kwargs):
            super(PrivateBusiness, self).__init__(**kwargs)

            self.type = "personal_service"
            self.workable = True
            self.expects_clients = True

            # SimPy and etc follows:
            self.res = None # Restored before every job...
            self.time = 10 # Same
            self.is_running = False

        def has_workers(self):
            return list(i for i in self.building.available_workers if
                                              self.all_occs & i.occupations)

        def pre_nd(self):
            self.res = simpy.Resource(self.env, self.capacity)

        def business_control(self):
            while 1:
                yield self.env.timeout(self.time)

                if self.res.count == 0 and not self.has_workers():
                    break

            # We remove the business from nd if there are no more strippers to entertain:
            temp = "There are no workers available in the {} so it is shutting down!".format(self.name)
            self.log(temp)
            self.building.nd_ups.remove(self)

        def request_resource(self, client, char):
            """Requests a room from Sim'Py, under the current code, this will not be called if there are no rooms available...
            """
            raise Exception("request_resource method/process must be implemented")
            with self.res.request() as request:
                yield request

        def run_job(self, client, char):
            """Waits for self.time delay and calls the job...
            """
            raise Exception("Run Job method/process must be implemented")

        def post_nd_reset(self):
            self.res = None
            self.is_running = False


    class PublicBusiness(Business):
        SORTING_ORDER = 2
        NAME = "Public Business"
        DESC = "Clients are always right!?!"
        """Public Business Upgrade.

        This usually assumes the following:
        - Clients are handled in one general pool.
        - Workers randomly serve them.
        """
        def __init__(self, **kwargs):
            super(PublicBusiness, self).__init__(**kwargs)
            self.workable = True
            self.expects_clients = True
            self.type = "public_service"

            # If this is set to self.env.now in client manager, we send in workers (bc).
            self.send_in_worker = False

            self.active_workers = set() # On duty Workers.
            self.clients_waiting = set() # Clients waiting to be served.
            self.clients_being_served = set() # Clients that we serve.

            # SimPy and etc follows (L33t stuff :) ):
            self.res = None # Restored before every job... Resource Instance that may not be useful here...
            self.time = 10 # Time for a single shift.
            self.is_running = False # Active/Inactive.

        def client_control(self, client):
            """Request for a spot for a client...
            We add dirt here.
            """
            building = self.building
            tier = building.tier or 1

            with self.res.request() as request:
                yield request

                self.clients_waiting.add(client)
                temp = "{color=[beige]}%s{/color} enters the %s." % (client.name, self.name)
                self.log(temp, True)

                dirt = 0
                flag_name = "jobs_spent_in_{}".format(self.name)
                du_to_spend_here = self.time
                du_spent_here = 0
                client.du_without_service = 0

                while 1:
                    simpy_debug("Entering PublicBusiness({}).client_control iteration at {}".format(self.name, self.env.now))

                    if client in self.clients_waiting:
                        simpy_debug("Client {color=[beige]}%s{/color} will wait to be served." % client.name)
                        yield self.env.timeout(1)
                        du_spent_here += 1
                        client.du_without_service += 1
                    else:
                        client.du_without_service = 0

                        simpy_debug("Client {color=[beige]}%s{/color} is about to be served." % client.name)
                        yield self.env.timeout(3)
                        du_spent_here += 3
                        self.clients_being_served.remove(client)
                        self.clients_waiting.add(client)
                        dirt += randint(2, 3) # Move to business_control?

                        # Tips:
                        worker, effectiveness = client.served_by
                        client.served_by = ()
                        if effectiveness >= 150:
                            tips = tier*randint(2, 3)
                        elif effectiveness >= 100:
                            tips = tier*randint(1, 2)
                        else:
                            tips = 0
                        if tips:
                            for u in self.upgrades:
                                if isinstance(u, TapBeer) and dice(75):
                                    tips += 1*tier
                            worker.up_counter("_jobs_tips", tips)

                        # And remove client from actively served clients by the worker:
                        if client in worker.serving_clients:
                            worker.serving_clients.remove(client)

                    if client.du_without_service >= 2 and not self.send_in_worker:
                        # We need a worker ASAP:
                        self.send_in_worker = True

                    if du_spent_here >= du_to_spend_here:
                        break

                    if client.du_without_service >= 5:
                        temp = "{color=[beige]}%s{/color} spent too long waiting for service!" % client.name
                        self.log(temp, True)
                        break

                building.dirt += dirt

                temp = "{} exits the {} leaving {} dirt behind.".format(
                                        set_font_color(client.name, "beige"), self.name, dirt)
                self.log(temp, True)

                if client in self.clients_being_served:
                    self.clients_being_served.remove(client)
                if client in self.clients_waiting:
                    self.clients_waiting.remove(client)
                client.del_flag("jobs_busy")

                simpy_debug("Exiting PublicBusiness({}).client_control iteration at {}".format(self.name, self.env.now))

        def add_worker(self):
            simpy_debug("Entering PublicBusiness({}).add_worker at {}".format(self.name, self.env.now))
            building = self.building
            workers = building.available_workers
            # Get all candidates:
            job = self.job
            ws = self.get_workers(job)
            if ws:
                w = ws.pop()
                self.active_workers.add(w)
                workers.remove(w)
                self.env.process(self.worker_control(w))
            simpy_debug("Exiting PublicBusiness({}).add_worker at {}".format(self.name, self.env.now))

        def business_control(self):
            """This runs the club as a SimPy process from start to the end.
            """
            counter = 0
            building = self.building
            tier = building.tier

            while 1:
                simpy_debug("Entering PublicBusiness({}).business_control iteration at {}".format(self.name, self.env.now))
                every_5_du = not self.env.now % 5

                if self.send_in_worker: # Sends in workers when needed!
                    new_workers_required = max(1, len(self.clients_waiting)/5)
                    if DSNBR:
                        temp = "Adding {} workers to {}!".format(
                                set_font_color(new_workers_required, "green"),
                                self.name)
                        temp = temp + " ~ self.send_in_worker == {}".format(
                                    set_font_color(self.send_in_worker, "red"))
                        self.log(temp, True)
                    for i in range(new_workers_required):
                        self.add_worker()
                    self.send_in_worker = False

                yield self.env.timeout(1)

                # Could be flipped to a job Brawl event?:
                # if False:
                #     if counter < 1 and self.env.now > 20:
                #         counter += 1
                #         for u in building._businesses:
                #             if u.__class__ == WarriorQuarters:
                #                 process = u.request_action(building=building, start_job=True, priority=True, any=False, action="patrol")[1]
                #                 u.interrupt = process # New field to which we can bind a process that can be interrupted.
                #                 break
                #
                #     # testing interruption:
                #     if "process" in locals() and (counter == 1 and self.env.now > 40):
                #         counter += 1
                #         process.interrupt("fight")
                #         self.env.process(u.intercept(interrupted=True))
                # =====================================>>>

                if every_5_du:
                    if DSNBR:
                        temp = "Debug: {} capacity is currently in use.".format(
                                set_font_color(self.res.count, "red"))
                        temp = temp + " {} Workers are currently on duty in {}!".format(
                                set_font_color(len(self.active_workers), "blue"),
                                self.name)
                        siw_workers = len([w for w in building.available_workers if set(w.gen_occs).intersection(self.job.occupations)])
                        temp = temp + " {} (gen_occ) workers are available in the Building for the job!".format(
                                set_font_color(siw_workers, "green"))
                        self.log(temp, True)

                    if not self.all_workers and not self.active_workers:
                        break

                simpy_debug("Exiting PublicBusiness({}).business_control iteration at {}".format(self.name, self.env.now))

            # We remove the business from nd if there are no more strippers to entertain:
            temp = "There are no workers available in the {} so it is shutting down!".format(self.name)
            self.log(temp)
            building.nd_ups.remove(self)

        def worker_control(self, worker):
            self.log(self.intro_string % (worker.name), True)

            du_working = 35

            # We create the log object here! And start logging to it directly!
            building = self.building
            job, loc = self.job, self.building
            log = NDEvent(job=job, char=worker, loc=loc, business=self)

            log.append(self.log_intro_string % (worker.name))
            log.append("\n")

            difficulty = loc.tier
            effectiveness = job.effectiveness(worker, difficulty, log, False,
                                manager_effectiveness=building.manager_effectiveness)

            # Upgrade mods:
            # Move to Job method?
            eff_mod = 0
            for u in self.upgrades:
                eff_mod += getattr(u, "job_effectiveness_mod", 0)
            effectiveness += eff_mod

            if DSNBR:
                log.append("Debug: Her effectiveness: {}! (difficulty: {}, Tier: {})".format(
                                effectiveness, difficulty, worker.tier))

            # Actively serving these clients:
            can_serve = 5 # We consider max of 5
            worker.serving_clients = set() # actively serving these clients
            clients_served = [] # client served during the shift (all of them, for the report)

            while worker.jobpoints > 0 and du_working > 0:
                simpy_debug("Entering PublicBusiness({}).worker_control iteration at {}".format(self.name, self.env.now))

                # Add clients to serve:
                for c in self.clients_waiting.copy():
                    if len(worker.serving_clients) < can_serve:
                        self.clients_waiting.remove(c)
                        self.clients_being_served.add(c)
                        c.du_without_service = 0 # Prevent more worker from being called on duty.
                        c.served_by = (worker, effectiveness)
                        worker.serving_clients.add(c)
                        clients_served.append(c)
                    else:
                        break

                yield self.env.timeout(1)
                du_working -= 1

                worker.jobpoints -= len(worker.serving_clients)*2 # 2 jobpoints per client?

                simpy_debug("Exiting PublicBusiness({}).worker_control iteration at {}".format(self.name, self.env.now))

            if clients_served:
                if DSNBR:
                    temp = "Logging {} for {}!".format(self.name, worker.name)
                    self.log(temp, True)
                # Weird way to call job method but it may help with debugging somehow.
                work_method = getattr(job, self.job_method)
                work_method(worker, clients_served, effectiveness, log)

                earned = payout(job, effectiveness, difficulty, building,
                                self, worker, clients_served, log)
                temp = "{} earns {} by serving {} clients!".format(
                                worker.name, earned, self.res.count)
                self.log(temp, True)

                worker.serving_clients = set() # Clean-up.

                # Create the job report and settle!
                log.after_job()
                NextDayEvents.append(log)
            else:
                temp = "There were no clients for {} to serve".format(worker.name)
                self.log(temp, True)

            self.active_workers.remove(worker)
            temp = "{} is done with the job in {} for the day!".format(
                                worker.name,
                                self.name)
            temp = set_font_color(temp, "cadetblue")
            self.log(temp, True)

            simpy_debug("Leaving PublicBusiness({}).worker_control at {}".format(self.name, self.env.now))

        def pre_nd(self):
            # Whatever we need to do at start of Next Day calculations.
            self.res = simpy.Resource(self.env, self.capacity)

        def post_nd_reset(self):
            self.res = None
            self.is_running = False
            self.send_in_worker = False
            self.active_workers = set()
            self.clients = set()


    class OnDemandBusiness(Business):
        SORTING_ORDER = 2
        NAME = "On Demand Business"
        DESC = "Are we gonna work hard!?!"
        def __init__(self, **kwargs):
            super(OnDemandBusiness, self).__init__(**kwargs)

            self.type = "on_demand_service"
            self.workable = True
            self.active_workers = list()
            self.action = None # Action that is currently running! For example guard that are presently on patrol should still respond to act
                                          # of violence by the customers, even thought it may appear that they're busy (in code).

            # SimPy and etc follows:
            self.time = 1 # Same.
            # We can bind an active process here if
            # it can be interrupted. I'ma an idiot... This needs to be reset.
            self.interrupt = None
            self.expands_capacity = False

        def get_pure_workers(self, job, power_flag_name, use_slaves=True):
            workers = set(self.get_workers(job, amount=float("inf"),
                           match_to_client=None, priority=True,
                           any=False, use_slaves=use_slaves))

            if workers:
                # Do Disposition checks:
                job.settle_workers_disposition(workers, self)
                # Do Effectiveness calculations:
                self.calc_job_power(workers, job, power_flag_name)

            return workers

        def all_on_deck(self, workers, job, power_flag_name, use_slaves=True):
            # calls everyone in the building to clean it
            new_workers = self.get_workers(job, amount=float("inf"),
                            match_to_client=None, priority=True,
                            any=True, use_slaves=use_slaves)

            if new_workers:
                # Do Disposition checks:
                job.settle_workers_disposition(new_workers, self, all_on_deck=True)
                # Do Effectiveness calculations:
                self.calc_job_power(new_workers, job, power_flag_name)
            workers = workers.union(new_workers)

            # Throw in the manager:
            manager = self.building.manager
            if manager:
                workers.add(manager)

            return workers

        def calc_job_power(self, workers, job, power_flag_name,
                                remove_from_available_workers=True):
            building = self.building
            difficulty = building.tier

            for w in workers:
                if not w.flag(power_flag_name):
                    effectiveness_ratio = job.effectiveness(w, difficulty,
                            manager_effectiveness=building.manager_effectiveness)

                    if DEBUG_SIMPY:
                        devlog.info("{} Effectiveness: {}: {}".format(job.id,
                                            w.nickname, effectiveness_ratio))
                    value = -(5 * effectiveness_ratio)

                    for u in self.upgrades:
                        value += getattr(u, "job_power_mod", 0)

                    w.set_flag(power_flag_name, value)

                    # Remove from active workers:
                    if remove_from_available_workers:
                        building.available_workers.remove(w)

        def post_nd_reset(self):
            # Resets all flags and variables after next day calculations are finished.
            self.interrupt = None


    class TaskBusiness(Business):
        SORTING_ORDER = 6
        NAME = "Task Business"
        DESC = "Complete given tasks!"
        """Base class upgrade for businesses that just need to complete a task, like FG, crafting and etc.
        """
        # For lack of a better term... can't come up with a better name atm.
        def __init__(self, **kwargs):
            super(TaskBusiness, self).__init__(**kwargs)
            self.workable = True
            self.res = None #*Throws an error?
