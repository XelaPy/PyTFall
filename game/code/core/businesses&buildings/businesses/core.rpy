init -12 python:
    #################################################################
    # BUILDING UPGRADE CLASSES:
    class Business(_object):
        """BaseClass for any building expansion! (aka Business)
        """
        ID = "Business"
        SORTING_ORDER = 0
        MATERIALS = {}

        def __init__(self, name="", instance=None, desc="", img="",
                     expands_capacity=True, **kwargs):
            self.name = name # name, a string.
            self.instance = instance # Building this upgrade belongs to.
            self.desc = desc # description, a string.

            self.img = img

            # Jobs this upgrade can add. *We add job instances here!
            # It may be a good idea to turn this into a direct job assignment instead of a set...
            self.jobs = set()
            self.workers = set() # List of on duty characters.

            # self._rep = 0

            self.show = True # Display to the player...

            self.habitable = False
            self.workable = False
            # If not active, business is not executed and is considered "dead",
            # we run "inactive" method with a corresponding simpy process in this case.
            self.active = True

            self.cost = kwargs.pop("cost", 0)
            self.in_slots = kwargs.pop("in_slots", 0)
            self.ex_slots = kwargs.pop("ex_slots", 0)

            self.clients = set() # Local clients, this is used during next day and reset on when that ends.

            # @Review: From Business class which seemed useless to me...
            self.blocked_upgrades = kwargs.get("blocked_upgrades", list())
            self.allowed_upgrades = kwargs.get("allowed_upgrades", list())
            self.in_construction_upgrades = list()
            self.upgrades = list()

            # If False, no clients are expected.
            # If all businesses in the building have this set to false, no client stream will be generated at all.
            self.expects_clients = True

            # This means that we can add capacity to this business.
            self.capacity = kwargs.pop("capacity", 1)
            self.expands_capacity = kwargs.pop("expands_capacity", True)

        def get_client_count(self):
            # Returns amount of clients we expect to come here.
            return self.capacity

        def expand_capacity(self, value=1):
            self.capacity += 1

            self.in_slots += 1
            self.instance.in_slots += 1

        @property
        def job(self):
            # This may not be required if we stick to a single job per business scenario:
            if self.jobs:
                return random.sample(self.jobs, 1).pop()

        # Reputation:
        # Prolly not a good idea to mess with this on per business basis, at least at first...
        @property
        def rep(self):
            return self._rep

        @rep.setter
        def rep(self, value):
            self._rep = self._rep + value
            if self._rep > 1000:
                self._rep = 1000
            elif self._rep < -1000:
                self._rep = -1000

        @property
        def env(self):
            # SimPy and etc follows (L33t stuff :) ):
            return self.instance.env

        def log(self, item, add_time=False):
            # Logs the text for next day event...
            self.instance.log(item, add_time=add_time)

        # Worker methods:
        def has_workers(self, amount=1):
            # Checks if there is a worker(s) available.
            return False

        @property
        def all_workers(self):
            # This may be a poor way of doing it because different upgrades could have workers with the same job assigned to them.
            # Basically what is needed is to allow setting a business to a worker as well as the general building if required...
            # And this doesn't work? workers are never populated???
            return list(i for i in self.instance.available_workers if self.all_occs & i.occupations)

        def action_priority_workers(self, job):
            return list(i for i in self.instance.available_workers if i.action == job)

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
                    temp = '{}: {} liked {} for {}.'.format(self.env.now, client.name, w.nickname, slikes)
                    self.log(temp)
                    worker = w
                    workers.remove(w)
                    client.set_flag("jobs_matched_traits", likes)
                    break
            else:
                worker = workers.pop()
            return worker

        def requires_workers(self, amount=1):
            # TODO: Get rid of this?
            """Returns True if this upgrade requires a Worker to run this job.

            Example: Building
            Strip Club on the other hand may nor require one or one would be requested later.
            It may be a better bet to come up with request_worker method that evaluates the same earlier, we'll see.
            """
            return False

        def check_worker_willing(self, worker, job):
            """Checks if the worker is willing to do the job.

            Removes worker from instances master list.
            Returns True is yes, False otherwise.
            """
            if job.is_valid_for(worker):
                if config.debug:
                    temp = set_font_color("{}: Debug: {} worker (Occupations: {}) with action: {} is doing {}.".format(self.env.now,
                                          worker.nickname, ", ".join(list(str(t) for t in worker.occupations)), worker.action, job.id), "lawngreen")
                    self.log(temp)
                return True
            else:
                if worker in self.instance.available_workers:
                    self.instance.available_workers.remove(worker)

                if config.debug:
                    temp = set_font_color('{}: Debug: {} worker (Occupations: {}) with action: {} refuses to do {}.'.format(self.env.now, worker.nickname, ", ".join(list(str(t) for t in worker.occupations)), worker.action, job.id), "red")
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
            if can_do_work(worker):
                return True
            else:
                if worker in self.instance.available_workers:
                    self.instance.available_workers.remove(worker)
                temp = set_font_color('{}: {} is done working for the day.'.format(self.env.now, worker.name), "aliceblue")
                self.log(temp)
                return False

        def convert_AP(self, worker):
            self.instance.convert_AP(worker)

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
            self.instance.fin.log_logical_income(amount, reason)

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
        def add_upgrade(self, upgrade):
            upgrade.instance = self
            upgrade.building = self.instance
            self.upgrades.append(upgrade)

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
        def __init__(self, name="Private Business", instance=None,
                     desc="Client is always right!?!",
                     img=None, **kwargs):

            img = Null() if img is None else img

            super(PrivateBusiness, self).__init__(name=name, instance=instance,
                            desc=desc, img=img, **kwargs)

            self.type = "personal_service"
            self.jobs = set()
            self.workable = True

            # SimPy and etc follows:
            self.res = None # Restored before every job...
            self.time = 5 # Same
            self.is_running = False # Is true when the business is running, this is being set to True at the start of the ND and to False on it's end.

        def has_workers(self):
            # Check if the building still has someone availbile to do the job.
            # We just check this for
            return list(i for i in self.instance.available_workers if self.all_occs & i.occupations)

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
            self.instance.nd_ups.remove(self)

        def request_resource(self, client, char):
            """Requests a room from Sim'Py, under the current code, this will not be called if there are no rooms available...
            """
            with self.res.request() as request:
                yield request

                # All is well and the client enters:
                temp = "{}: {} and {} enter the room.".format(self.env.now, client.name, char.name)
                self.log(temp)

                # This line will make sure code halts here until run_job ran it's course...
                yield self.env.process(self.run_job(client, char))

                # Action (Job) ran it's course and client is leaving...
                temp = "{}: {} leaves the {}.".format(self.env.now, client.name, self.name)
                self.log(temp)
                # client.flag("jobs_busy").interrupt()
            client.del_flag("jobs_busy")

        def run_job(self, client, char):
            """Waits for self.time delay and calls the job...
            """
            yield self.env.timeout(self.time)
            if config.debug:
                temp = "{}: Debug: {} Building Resource in use!".format(self.env.now, set_font_color(self.res.count, "red"))
                self.log(temp)

            temp = "{}: {} and {} did their thing!".format(self.env.now, set_font_color(char.name, "pink"), client.name)
            self.log(temp)

            # Visit counter:
            client.up_counter("got_serviced_by" + char.id)

            # Execute the job:
            self.job(char, client)

            # We return the char to the nd list:
            self.instance.available_workers.insert(0, char)

        def post_nd_reset(self):
            self.res = None
            self.is_running = False


    class PublicBusiness(Business):
        SORTING_ORDER = 2
        """Public Business Upgrade.

        This usually assumes the following:
        - Clients are handled in one general pool.
        - Workers randomly serve them.
        """
        def __init__(self, name="Public Default", instance=None,
                     desc="Client is always right!?!", img=None,
                     **kwargs):

            img = Null() if img is None else img

            super(PublicBusiness, self).__init__(name=name, instance=instance,
                            desc=desc, img=img, **kwargs)
            self.jobs = set() # Job bound to this update.
            self.workable = True
            self.type = "public_service"

            self.active_workers = set() # On duty Workers.
            self.clients = set() # Clients.

            # SimPy and etc follows (L33t stuff :) ):
            self.res = None # Restored before every job... Resource Instance that may not be useful here...
            self.time = 5 # Time for a single shift.
            self.is_running = False # Active/Inactive.

            self.earned_cash = 0 # Cash earned (total)

        def pre_nd(self):
            # Whatever we need to do at start of Next Day calculations.
            self.res = simpy.Resource(self.env, self.capacity)

        def client_control(self, client):
            """Request for a spot for a client...
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
                        for u in self.instance._businesses:
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
                    temp = "Debug: {} places are currently in use in {}!".format(
                            set_font_color(self.res.count, "red"),
                            self.name)
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
            raise Exception("worker_control method must be implemented")

        def post_nd_reset(self):
            self.res = None
            self.is_running = False
            self.active_workers = set()
            self.clients = set()
            self.earned_cash = 0


    class OnDemandBusiness(Business):
        SORTING_ORDER = 2
        def __init__(self, name="On Demand Default", instance=None,
                     desc="Does something on request!", img=None,
                     **kwargs):

            img = Null() if img is None else img

            super(OnDemandBusiness, self).__init__(name=name, instance=instance,
                        desc=desc, img=img, **kwargs)

            self.type = "on_demand_service"
            self.jobs = set()
            self.workable = True
            self.active_workers = list()
            self.action = None # Action that is currently running! For example guard that are presently on patrol should still respond to act
                                          # of violence by the customers, even thought it may appear that they're busy (in code).

            # SimPy and etc follows:
            self.res = None # Restored before every job...
            self.time = 1 # Same.
            self.is_running = False # Is true when the business is running, this is being set to True at the start of the ND and to False on it's end.
            self.interrupt = None # We can bind an active process here if it can be interrupted. I'ma an idiot... This needs to be reset.
            self.expects_clients = False # See Business.__init__

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

            return workers.union(new_workers)

        def calc_job_power(self, workers, job, power_flag_name,
                                remove_from_available_workers=True):
            difficulty = self.instance.tier

            for w in workers:
                if not w.flag(power_flag_name):
                    effectiveness_ratio = job.effectiveness(w, difficulty)
                    if config.debug:
                        devlog.info("{} Effectiveness: {}: {}".format(job.id,
                                            w.nickname, effectiveness_ratio))
                    value = -(5 * effectiveness_ratio)
                    w.set_flag(power_flag_name, value)

                    # Remove from active workers:
                    if remove_from_available_workers:
                        self.instance.available_workers.remove(w)

        def post_nd_reset(self):
            # Resets all flags and variables after next day calculations are finished.
            self.interrupt = None


    class TaskBusiness(Business):
        SORTING_ORDER = 6
        """Base class upgrade for businesses that just need to complete a task, like FG, crafting and etc.
        """
        # For lack of a better term... can't come up with a better name atm.
        def __init__(self, name="Task Default", desc="Completes given task!",
                     img=None, **kwargs):

            img = Null() if img is None else img

            super(TaskBusiness, self).__init__(name=name, instance=instance, desc=desc,
                                               img=img, **kwargs)

            self.res = None #*Throws an error?
