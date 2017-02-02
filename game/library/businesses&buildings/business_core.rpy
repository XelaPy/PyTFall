init -12 python:
    #################################################################
    """Thoughts:

    - Here is the continuation of SimPy land, which starts at the main building and calls/activates methods gtom workable upgrades.
    - It may be a good idea to create a Flags object here and pass it to the Jobs which create ND reports. It makes sense (at least) for the team jobs.
    - This needs to get a lot more generic, especially newer addons.
    """
    # BUILDING UPGRADE CLASSES:
    class Business(_object):
        """BaseClass for any building expansion! (aka Business)
        """
        MATERIALS = {}
        COST = 0 # in Gold.
        CONSTRUCTION_EFFORT = 0
        IN_SLOTS = 1
        EX_SLOTS = 1
        COST = 100

        def __init__(self, name="", instance=None, desc="", img="", build_effort=0, materials=None, in_slots=1, ex_slots=0, cost=0, **kwargs):
            self.name = name # name, a string.
            self.instance = instance # Building this upgrade belongs to.
            self.desc = desc # description, a string.

            # Weird code... we prolly set img somewhere in child classes prior to running this method. I need to normalize how we handle images for upgrades.
            if not hasattr(self, "img"):
                self.img = img # Ren'Py path leading the an image, a string.
            if not hasattr(self, "cost"):
                self.cost = cost

            self.jobs = set() # Jobs this upgrade can add. *We add job instances here!  # It may be a good idea to turn this into a direct job assignment instead of a set...
            self.workers = set() # List of on duty characters.

            self._rep = 0

            self.show = True # Display to the player...

            self.habitable = False
            self.workable = False
            self.active = True # If not active, business is not executed and is considered "dead", we run "inactive" method with a corresponding simpy process in this case.

            self.in_slots = in_slots
            self.ex_slots = ex_slots

            self.clients = set() # Local clients, this is used during next day and reset on when that ends.

            # @Review: From Business class which seemed useless to me...
            self.blocked_upgrades = kwargs.get("blocked_upgrades", list())
            self.allowed_upgrades = kwargs.get("allowed_upgrades", list())
            self.in_construction_upgrades = list()
            self.upgrades = list()
            self.expects_clients = True # If False, no clients are expected. If all businesses in the building have this set to false, no client stream will be generated at all.

        def get_client_count(self):
            # Returns amount of clients we expect to come here.
            return 2 + int(self._rep*0.01*len(self.all_workers))

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

        def log(self, item):
            # Logs the text for next day event...
            self.instance.nd_events_report.append(item)

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

        def get_workers(self, job, amount=1, match_to_client=None, priority=True, any=True):
            """Tries to find workers for any given job.

            - Tries to get a perfect match where action == job first.
            - Tries to get any match trying to match any occupation at all.

            @param: match_to_client: Will try to find the a good match to client, expects a client (or any PytC instance with .likes set) object.
            """
            workers = list()

            if priority:
                priorityw = self.action_priority_workers(job)
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
            if job.check_occupation(worker):
                if config.debug:
                    temp = set_font_color("{}: Debug: {} worker (Occupations: {}) with action: {} is doing {}.".format(self.env.now, worker.nickname, ", ".join(list(str(t) for t in worker.occupations)), worker.action, job.id), "lawngreen")
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
            if check_char(worker):
                return True
            else:
                if worker in self.instance.available_workers:
                    self.instance.available_workers.remove(worker)
                temp = set_font_color('{}: {} is done working for the day.'.format(self.env.now, worker.name), "aliceblue")
                self.log(temp)
                return False

        def convert_AP(self, w, workers, flag, remove=True):
            # Converts AP to "Job Points".
            # Removes w from workers list if remove is True.
            # Returns False if no AP was left, True otherwise
            if w.take_ap(1):
                value = int(round(7 + w.agility * 0.1))
                w.set_flag(flag, value)
                return True
            else:
                if remove:
                    workers.remove(w)
                return False

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
            self.instance.fin.log_work_income(amount, reason)

        def post_nd_reset(self):
            # Resets all flags and variables after next day calculations are finished.
            pass

        def inactive_process(self):
            temp = "{} is currently inactive, no actions will be conducted here!".format(self.name)
            self.log(temp)
            yield self.env.timeout(100)

        # @Review: From MainUpgrade class which seemed useless to me...
        # SimPy:
        def business_control(self):
            """SimPy business controller.
            """
            while 1:
                yield self.env.timeout(100)

        # Business MainUpgrade related:
        def add_upgrade(self, upgrade):
            upgrade.instance = self
            self.main_upgrade = self.instance
            self.upgrades.append(upgrade)

        def has_upgrade(self, upgrade_class):
            return upgrade_class in [u.__class__ for u in self.upgrades]

        def check_upgrade_compatibility(self, upgrade):
            return self.__class__ in upgrade.COMPATIBILITY

        def check_upgrade_allowance(self, upgrade):
            return upgrade.__class__ in self.allowed_upgrades


    class PrivateBusiness(Business):
        def __init__(self, name="Private Business", instance=None, desc="Client is always right!?!", img=None, build_effort=0, materials=None, in_slots=2, cost=500, **kwargs):
            img = Null() if img is None else img
            super(PrivateBusiness, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.capacity = in_slots
            self.type = "personal_service"
            self.jobs = set()
            self.workable = True

            # SimPy and etc follows:
            self.res = None # Restored before every job...
            self.time = 5 # Same
            self.is_running = False # Is true when the business is running, this is being set to True at the start of the ND and to False on it's end.

        def get_client_count(self):
            # Returns amount of workers we expect to come here.
            # We may not use this at all and handle everything on level of the main building instead!
            return int(round(2 + self._rep*0.01*max(len(self.all_workers), self.capacity)))

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

        def request_room(self, client, char):
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
        """Public Business Upgrade.

        This usually assumes the following:
        - Clients are handled in one general pool.
        - Workers randomly serve them.
        """
        def __init__(self, name="Public Default", instance=None, desc="Client is always right!?!", img=None, build_effort=0, materials=None, in_slots=3, cost=500, **kwargs):
            img = Null() if img is None else img
            super(PublicBusiness, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set() # Job bound to this update.
            self.workable = True
            self.type = "public_service"

            self.capacity = in_slots
            self.active_workers = set() # On duty Workers.
            self.clients = set() # Clients.

            # SimPy and etc follows (L33t stuff :) ):
            self.res = None # Restored before every job... Resource Instance that may not be useful here...
            self.time = 5 # Time for a single shift.
            self.is_running = False # Active/Inactive.

            self.earned_cash = 0 # Cash earned (total)

        def get_client_count(self):
            # Returns amount of clients we expect to come here.
            return int(round(3 + self._rep*0.05*max(len(self.all_workers), self.capacity)))

        def pre_nd(self):
            # Whatever we need to do at start of Next Day calculations.
            self.res = simpy.Resource(self.env, self.capacity)

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

                temp = "{}: {} exits the {} leaving {} Gold and {} Dirt behind.".format(self.env.now, client.name, self.name, cash, dirt)
                self.clients.remove(client)
                self.log(temp)
                client.del_flag("jobs_busy")

        def worker_control(self):
            if not self.active_workers or len(self.active_workers) < self.res.count/4:
                workers = self.instance.available_workers
                # Get all candidates:
                job = self.job
                ws = self.get_workers(job)
                if ws:
                    w = ws.pop()
                    self.active_workers.add(w)
                    workers.remove(w)
                    self.env.process(self.use_worker(w))

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

        def use_worker(self, worker):
            temp = "{}: {} comes out to serve customers in {}!".format(self.env.now, worker.name, self.name)
            self.log(temp)
            while worker.AP and self.res.count:
                yield self.env.timeout(self.time) # This is a single shift a worker can take for cost of 1 AP.
                worker.set_union("jobs_bar_clients", self.clients) # TODO: Maybe limit clients to worker routines?

                # Visit counter:
                for client in self.clients:
                    client.up_counter("got_serviced_by" + worker.id)

                worker.AP -= 1
                tips = randint(1, 2) * self.res.count
                self.log_income(tips)
                worker.mod_flag("jobs_" + self.job.id + "_tips", tips)
                temp = "{}: {} gets {} in tips from {} clients!".format(self.env.now, worker.name, tips, self.res.count)
                self.log(temp)

            # Once the worker is done, we run the job and create the event:
            if worker.flag("jobs_bar_clients"):
                if config.debug:
                    temp = "{}: Logging {} for {}!".format(self.env.now, self.name, worker.name)
                    self.log(temp)
                self.job(worker) # better bet to access Class directly...
            else:
                temp = "{}: There were no clients for {} to serve".format(self.env.now, worker.name)
                self.log(temp)

            self.active_workers.remove(worker)
            temp = "{}: {} is done with the job in {} for the day!".format(self.env.now, set_font_color(worker.name, "red"), self.name)
            self.log(temp)

        def post_nd_reset(self):
            self.res = None
            self.is_running = False
            self.active_workers = set()
            self.clients = set()
            self.earned_cash = 0


    class OnDemandBusiness(Business):
        def __init__(self, name="On Demand Default", instance=None, desc="Does something on request!", img=None, build_effort=0, materials=None, in_slots=0, cost=0, **kwargs):
            img = Null() if img is None else img
            super(OnDemandBusiness, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.capacity = in_slots
            self.type = "on_demand_service"
            self.jobs = set()
            self.workable = False
            self.active_workers = list()
            self.action = None # Action that is currently running! For example guard that are presently on patrol should still respond to act
                                          # of violence by the customers, even thought it may appear that they're busy (in code).

            # SimPy and etc follows:
            self.res = None # Restored before every job...
            self.time = 1 # Same.
            self.is_running = False # Is true when the business is running, this is being set to True at the start of the ND and to False on it's end.
            self.interrupt = None # We can bind an active process here if it can be interrupted. I'ma an idiot... This needs to be reset.
            self.expects_clients = False # See Business.__init__

        def post_nd_reset(self):
            # Resets all flags and variables after next day calculations are finished.
            self.interrupt = None


    class TaskBusiness(Business):
        """Base class upgrade for businesses that just need to complete a task, like FG, crafting and etc.
        """
        # For lack of a better term... can't come up with a better name atm.
        def __init__(self, name="Task Default", instance=None, desc="Completes given task!", img=None, build_effort=0, materials=None, in_slots=0, cost=0, **kwargs):
            img = Null() if img is None else img
            super(TaskBusiness, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)

            self.res = None #*Throws an error?
