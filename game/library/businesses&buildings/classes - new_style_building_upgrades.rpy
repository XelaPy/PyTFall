init -5 python:
    #################################################################
    """Thoughts:
    
    - Here is the continuation of SimPy land, which starts at the main building and calls/activates methods gtom workable upgrades.
    - It may be a good idea to create a Flags object here and pass it to the Jobs which create ND reports. It makes sense (at least) for the team jobs.
    - This needs to get a lot more generic, especially newer addons.
    """
    # BUILDING UPGRADE CLASSES:
    class BuildingUpgrade(_object):
        """BaseClass for any building expansion! (aka Business)
        """
        MATERIALS = {}
        COST = 0 # in Gold.
        CONSTRUCTION_EFFORT = 0
        IN_SLOTS = 1
        EX_SLOTS = 1
        COST = 100
        
        def __init__(self, name="", instance=None, desc="", img="", build_effort=0, materials=None, in_slots=1, ex_slots=0, cost=0):
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

        
    class MainUpgrade(BuildingUpgrade):
        """Usually suggests a business of some kind and unlocks jobs and other upgrades!
        """
        def __init__(self, *args, **kwargs):
            super(MainUpgrade, self).__init__(*args, **kwargs)
            
            self.blocked_upgrades = kwargs.get("blocked_upgrades", list())
            self.allowed_upgrades = kwargs.get("allowed_upgrades", list())
            self.in_construction_upgrades = list()
            self.upgrades = list()
            self.expects_clients = True # If False, no clients are expected. If all businesses in the building have this set to false, no client stream will be generated at all.
            
        def business_control(self):
            """SimPy business controller.
            """
            while 1:
                yield self.env.timeout(100)
            
        # SubUpgrade related:
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
            
            
    class PrivateBusinessUpgrade(MainUpgrade):
        def __init__(self, name="Private Business", instance=None, desc="Client is always right!?!", img=Null(), build_effort=0, materials=None, in_slots=2, cost=500, **kwargs):
            super(PrivateBusinessUpgrade, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
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
            
            
    class PublicBusinessUpgrade(MainUpgrade):
        """Public Business Upgrade.
        
        This usually assumes the following:
        - Clients are handled in one general pool.
        - Workers randomly serve them.
        """
        def __init__(self, name="Public Default", instance=None, desc="Client is always right!?!", img=Null(), build_effort=0, materials=None, in_slots=3, cost=500, **kwargs):
            super(PublicBusinessUpgrade, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
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
            
            
    class OnDemandUpgrade(MainUpgrade):
        def __init__(self, name="On Demand Default", instance=None, desc="Does something on request!", img=Null(), build_effort=0, materials=None, in_slots=0, cost=0, **kwargs):
            super(OnDemandUpgrade, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
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
            self.expects_clients = False # See MainUpgrade.__init__
            
        def post_nd_reset(self):
            # Resets all flags and variables after next day calculations are finished.
            self.interrupt = None
            
    class TaskUpgrade(MainUpgrade):
        """Base class upgrade for businesses that just need to complete a task, like FG, crafting and etc.
        """
        # For lack of a better term... can't come up with a better name atm.
        def __init__(self, name="Task Default", instance=None, desc="Completes given task!", img=Null(), build_effort=0, materials=None, in_slots=0, cost=0, **kwargs):
            super(TaskUpgrade, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            
            self.res = None #*Throws an error?
            
    class BrothelBlock(PrivateBusinessUpgrade):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 70, "Bricks": 30, "Glass": 5}
        COST = 10000
        ID = "Brothel"
        IMG = "content/buildings/upgrades/room.jpg"
        def __init__(self, name="Brothel", instance=None, desc="Rooms to freck in!", img="content/buildings/upgrades/room.jpg", build_effort=0, materials=None, in_slots=2, cost=500, **kwargs):
            super(BrothelBlock, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.capacity = in_slots
            self.type = "personal_service"
            self.jobs = set([simple_jobs["Whore Job"]])
            self.workable = True
            
            # SimPy and etc follows:
            self.res = None # Restored before every job...
            self.time = 5 # Same
            self.is_running = False # Is true when the business is running, this is being set to True at the start of the ND and to False on it's end.
            
            
    class StripClub(PublicBusinessUpgrade):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 30, "Bricks": 50, "Glass": 10}
        COST = 8000
        ID = "Strip Club"
        IMG = "content/buildings/upgrades/strip_club.jpg"
        
        def __init__(self, name="Strip Club", instance=None, desc="Exotic Dancers go here!", img="content/buildings/upgrades/strip_club.jpg", build_effort=0, materials=None, in_slots=5, cost=500, **kwargs):
            super(StripClub, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
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
            
            
    class Bar(PublicBusinessUpgrade):
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
            
            
    class Cleaners(OnDemandUpgrade):
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
                value = int(round(1 + w.serviceskill * 0.025 + w.agility * 0.3))
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
            
            
    class Garden(MainUpgrade):
        def __init__(self, name="Garden", instance=None, desc="Relax!", img="content/buildings/upgrades/garden.jpg", build_effort=0, materials=None, in_slots=0, ex_slots=2, cost=500, **kwargs):
            super(Garden, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            
            
    class MainHall(MainUpgrade):
        def __init__(self, name="Main Hall", instance=None, desc="Reception!", img="content/buildings/upgrades/main_hall.jpg", build_effort=0, materials=None, in_slots=0, ex_slots=2, cost=500, **kwargs):
            super(MainHall, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set()
            
            
    class WarriorQuarters(OnDemandUpgrade):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 15, "Bricks": 30, "Glass": 3}
        COST = 2500
        ID = "Warrior Quarters"
        IMG = "content/buildings/upgrades/guard_qt.jpg"
        def __init__(self, name="Warrior Quarters", instance=None, desc="Place for Guards!", img="content/buildings/upgrades/guard_qt.jpg", build_effort=0, materials=None, in_slots=2, ex_slots=1, cost=500, **kwargs):
            super(WarriorQuarters, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Guarding"]])
            
        def request_action(self, building=None, start_job=True, priority=True, any=False, action=None):
            """This checks if there are idle workers willing/ready to do an action in the building.
            
            This will also start the job by default.
            Priority will call just the real warriors.
            Any will also add everyone else who might be willing to act.
            
            TODO: Once done, see if this can be generalized like the previous two upgrade types!
            """
            if not action:
                raise Exception("Action Must Be provided to .request_action method!")
            
            if not building:
                building = self.instance
                
            job = simple_jobs["Guarding"]
            # dirt = building.get_dirt()
            workers = self.get_workers(job, amount=10, priority=priority, any=any)
            process = None
            if not workers:
                return False, process # No workers available
            else:
                # Might require optimization so we don't send all the warriors to once.
                # Update worker lists:
                if start_job:
                    if action == "patrol":
                        self.active_workers = workers[:]
                        self.instance.available_workers = list(i for i in self.instance.available_workers if i not in workers)
                        process = self.env.process(self.patrol(workers, building))
                return True, process
                
        def patrol(self, workers, building):
            """Patrolling the building...
            """
            workers_original = workers[:]
            power_flag_name = "jobs_guard_power"
            for w in workers:
                # Set their cleaning capabilities as temp flag:
                value = int(round(1 + w.defence * 0.025 + w.agility * 0.3)) # Is defence sound here? We don't have guarding still...
                w.set_flag(power_flag_name, value)
                
            wlen = len(workers)
            if self.env:
                t = self.env.now
                temp = "{}: {} guards are going to patrol halls of {}!".format(self.env.now, set_font_color(wlen, "red"), building.name)
                self.log(temp)
                
            counter = 0 # counter for du, lets say that a single patrol run takes 20 du...
            
            while (workers and counter <= 100) and self.env.now < 99:
                # Job Points:
                try:
                    flag_name = "_jobs_guard_points"
                    for w in workers[:]:
                        if not w.flag(flag_name) or w.flag(flag_name) <= 0:
                            self.convert_AP(w, workers, flag_name)
                            
                        # Cleaning itself:
                        if w in workers:
                            w.mod_flag("_jobs_guard_points", 1) # 1 point per 1 dp? Is this reasonable...? Prolly, yeah.
                            w.mod_flag("job_guard_points_spent", 1) # So we know what to do during the job event buildup and stats application.
                            
                    if config.debug and self.env and not counter % 4:
                        wlen = len(workers)
                        # We run this once per 2 du and only for debug purposes.
                        temp = "{}: Debug: ".format(self.env.now)
                        temp = temp + " {} Guards are currently patrolling {}!".format(set_font_color(wlen, "red"), building.name)
                        temp = temp + set_font_color(" DU spent: {}!".format(counter), "blue")
                        self.log(temp)
                        
                    # We may be running this outside of SimPy... not really? not in this scenario anyway...
                    if self.env:
                        yield self.env.timeout(1)
                    counter = counter + 1
                    
                except simpy.Interrupt as reason:
                    temp = "{}: Debug: ".format(self.env.now)
                    temp = temp + " {} Guards responding to an event ({}), patrol is halted in {}".format(set_font_color(wlen, "red"), reason.cause, building.name)
                    temp = temp + set_font_color("!!!!".format(counter), "crimson")
                    self.log(temp)

                    yield self.env.timeout(5)

                    temp = "{}: Debug: ".format(self.env.now)
                    temp = temp + " {} Guards finished their response to the event, back to patrolling {}".format(set_font_color(wlen, "red"), building.name)
                    temp = temp + set_font_color("....".format(counter), "crimson")
                    self.log(temp)
                
            temp = "{}: Patrol of {} is now finished! Guards are falling back to their quarters!".format(self.env.now, building.name)
            temp = set_font_color(temp, "red")
            self.log(temp)
            
            # Once the loop is broken:
            # Restore the lists:
            self.active_workers = list()
            for w in workers:
                self.instance.available_workers.append(w)
                
            # Build the report:
            simple_jobs["Guarding"](workers_original, workers, building, action="patrol")
            
        def intercept(self, opfor=list(), interrupted=False):
            """This intercepts a bunch of aggressive clients and resolves the issue through combat or intimidation.
            
            opfor = opposition forces
            
            TODO:
            - This needs to gather the forces.
            - Return the result and put a hold on the business process if interception had failed.
            - Work with clients instead of props I am planning to use for testing.
            - Check if previous guard action was interrupted and act (look for defenders/restore older process) accordingly.
            """
            job = simple_jobs["Guarding"]
            
            # gather the response forces:
            defenders = list()
            if interrupted:
                active_workers_backup = self.active_workers[:]
                defenders = self.active_workers[:]
                self.active_workers = list()
                
            temp = self.get_workers(job, amount=10, match_to_client=None, priority=True, any=True) # Set amount according to opfor/manager:
            defenders = set(defenders + temp)
            
            temp = "{}: {} Guards are intercepting attack event in {}".format(self.env.now, set_font_color(len(defenders), "red"), building.name)
            self.log(temp)
            
            if not defenders:
                # If there are no defenders, we're screwed:
                temp = "{}: Noone was able to intercept attack event in {}".format(self.env.now, building.name)
                self.log(temp)
                self.env.exit(False) # TODO: Maybe more options than False and None?
            else:
                temp = "{}: {} Guards are intercepting attack event in {}".format(self.env.now, set_font_color(len(defenders), "red"), building.name)
                self.log(temp)
                
            # TODO: This should prolly be a function!
            # Prepare the teams:
            enemy_team = Team(name="Enemy Team", max_size=5) # TODO: max_size should be len(opfor)
            mob = build_mob(id="Goblin Shaman", level=30)
            mob.front_row = True
            mob.apply_trait("Fire")
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
            for i in xrange(4): # Testing 5 mobs...
                mob = build_mob(id="Goblin Archer", level=10)
                mob.front_row = False
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
            
            defence_team = Team(name="Guardians Of The Galaxy", max_size=len(defenders))
            for i in defenders:
                i.controller = BE_AI(i)
                defence_team.add(i)
                
            # ImageReference("chainfights")
            global battle
            battle = BE_Core(logical=1)
            battle.teams.append(defence_team)
            battle.teams.append(enemy_team)
            
            battle.start_battle()
            
            for i in defenders:
                i.controller = "player"
                
            yield self.env.timeout(5)
                
            # We also should restore the list if there was interruption:
            if "active_workers_backup" in locals():
                for i in active_workers_backup:
                    if check_char(i, check_ap=False): # Check if we're still ok to work...
                        self.active_workers.append(i)
                        # TODO: Actual workers list should be here as well, not just the general one...
            
            # Build a Job report:
            # Create flag object first to pass data to the Job:
            flag = Flags()
            flag.set_flag("result", battle.winner == defence_team)
            flag.set_flag("opfor", opfor)
            job(defenders, defenders, self.instance, action="intercept", flag=flag)
                        
            # decided to add report in debug mode after all :)
            if config.debug:
                self.log(set_font_color("Debug: Battle Starts!", "crimson"))
                for entry in reversed(battle.combat_log):
                    self.log(entry)
                self.log(set_font_color("=== Battle Ends ===", "crimson"))
            
            if battle.winner == defence_team:
                temp = "{}: Interception Success!".format(self.env.now)
                temp = temp + set_font_color("....", "crimson")
                self.log(temp)
                self.env.exit(True) # return True
            else:
                temp = "{}: Interception Failed, your Guards have been defeated!".format(self.env.now)
                temp = temp + set_font_color("....", "crimson")
                self.log(temp)
                self.env.exit(False)
            
        def convert_AP(self, w, workers, flag):
            # "Job Points": TODO: Remove this, temp code to help out with testing.
            if w.take_ap(1):
                value = 100
                w.set_flag(flag, value)
            else:
                workers.remove(w)
            
            
    class SlaveQuarters(MainUpgrade):
        def __init__(self, name="Slave Quarters", instance=None, desc="Place for slaves to live in!", img="content/buildings/upgrades/guard_qt.jpg", build_effort=0, materials=None, in_slots=2, ex_slots=0, cost=500, **kwargs):
            super(SlaveQuarters, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.rooms = in_slots
            
            
    def launch_exploration_run(team, area):
        # Making sure that the team can explore the area.
        # Ask if player wants to send the team exploring:
        # I think this needs to be moved somewhere... it's a good fit for the class:
        if not renpy.call_screen("yesno_prompt",
                                 message="Are you sure that you wish to send %s exploring?" % team.name,
                                 yes_action=Return(True),
                                 no_action=Return(False)):
            return
        
        # I think that the game should be rigged in such a way that this is impossible:
        # for char in team:
            # if char.action == "Exploring":
                # renpy.show_screen("message_screen", "Team Member: %s is already on exploration run!" % char.name)
                # return
        
        for char in team:
            char.action = "Exploring" # We effectively remove char from the game so this is prolly ok.
            char.set_flag("loc_backup", char.location)
            if char in hero.team:
                hero.team.remove(char)
                
            # TODO: Remove char from every possible team setup in any of the buildings?
            for t in fg.teams:
                if t != team:
                    for char in team:
                        for c in t:
                            if c == char:
                                t.remove(char)
            
    # Temporary I'll Put Exploration code here:
    class ExplorationTracker(Job):
        # Added inheritance for Job so we can use the required methods,
        """The class that stores data for an exploration job.
        
        *Not really a Job, it stores data and doesn't write any reports to ND. **Maybe it should create ND report once the run is done!
        Adapted from old FG, not sure what we can keep here..."""
        def __init__(self, team, area):
            """Creates a new ExplorationJob.
            
            team = The team that is exploring.
            area = The area that is being explored.
            """
            
            # We do this because this data needs to be tracked separately and area object can only be updated once team has returned.
            # There is a good chance that some of these data must be updated in real time.
            # TODO: Keep this confined to copy of an area? Feels weird and useless to copy all of these properties.
            self.area = deepcopy(area)
            self.team = team
            
            self.mobs = self.area.mobs
            self.risk = self.area.risk
            self.cash_limit = self.area.cash_limit
            self.items_limit = self.area.items_limit
            self.hazard = self.area.hazard
            
            # Is this it? We should have area items???
            self.items = list(item.id for item in items.values() if "Exploration" in item.locations and item.price < self.items_limit)
            
            # Traveling to and from + Status flags:
            self.distance = self.area.travel_time * 25 # We may be setting this directly in the future. Distance in KM as units. 25 is what we expect the team to be able to travel in a day. This may be offset through traits and stats/skills.
            # We assume that it's never right outside of the freaking city walls, so we do this:
            if not self.distance:
                self.distance = randint(4, 10)
                
            self.traveled = 0 # Distance traveled in "KM"...
            
            self.arrived = False # Set to True upon arrival to the location.
            self.finished_exploring = False # Set to True after exploration is finished.
            
            self.points = 0 # Combined exploration points from the whole team. Replaces AP.
            self.power = 0 # Power, ability might be a better name.
            self.tp = 0 # travel point we use during traveling to offset ep sorrectly.
            
            self.state = "traveling to" # Instead of a bunch of properties, we'll use just the state as string and set it accordingly.
            self.captured_chars = list()
            self.found_items = list()
            self.cash = list()
            
            self.day = 0 # Day since start.
            self.total_days = 0 # Total days, travel times included!
            self.days = self.area.days # Days team is expected to be exploring (without travel times)!
            
            # TODO: Stats here need to be personal for each of the team members.
            self.unlocks = dict()
            for key in self.area.unlocks:
                self.unlocks[key] = 0
            
            self.flag_red = False
            self.flag_green = False
            self.stats = dict(attack=0,
                              defence=0,
                              agility=0,
                              magic=0,
                              exp=0)
            
            self.logs = list() # List of all log object we create for this exploration run.
            
            # And we got to make copies of chars stat dicts so we can show changes in ND after the exploration run is complete!
            self.init_stats = dict()
            for i in self.team:
                self.init_stats[i] = i.stats.stats.copy()
            
            # fg.exploring.append(self) # TODO: Add to the proper list! Maybe not here but in fg gui.
            renpy.show_screen("message_screen", "Team %s was sent out on %d days exploration run!" % (team.name, area.days))
            # jump("fg_management")
            
        def log(self, txt, name="", nd_log=True, ui_log=False):
            obj = ExLog(name, txt, nd_log, ui_log)
            self.logs.append(obj)
            return obj
            
        def build_nd_report(self):
            # Build one major report for next day!
            txt = [] # Not sure if this is required... we can add log objects and build reports from them in realtime instead of replicating data we already have.
            event_type = "jobreport"
            
            # Build an image combo for the report:
            vp = self.vp_or_fixed(self.all_workers, ["fighting"], {"exclude": ["sex"], "resize": (150, 150)}, xmax=820)
            img.add(Transform(vp, align=(.5, .9)))
            
            # We need to create major report for nd to keep track of progress:
            for log in self.logs:
                if log.nd_log:
                    self.txt.append("\n".join(log.txt))
            
            return NDEvent(type=event_type,
                                      img=simg,
                                      txt=txt,
                                      char=self.worker,
                                      team=self.team,
                                      charmod=self.workermod,
                                      loc=self.loc,
                                      locmod=self.locmod,
                                      green_flag=self.flag_green,
                                      red_flag=self.flag_red)
    
            
    class ExLog(Action):
        """Stores resulting text and data for SE.
        
        Also functions as a screen action for future buttons. Maybe...
        """
        def __init__(self, name="", txt="", nd_log=True, ui_log=False):
            """
            nd_log: Printed in next day report upon arrival.
            ui_log: Only reports worth of ui interface in FG.
            """
            self.name = name # Name of the event, to be used as a name of a button in gui.
            self.txt = [] # I figure we use list to store text.
            if txt:
                self.txt.append(txt)
            self.battle_log = [] # Used to log the event.
            self.battle_won = False
            self.found_items = []
            
        def __call__(self):
            renpy.show_screen("...") # Whatever the pop-up screen with info in gui is gonna be.
            
        def is_sensitive(self):
            # Check if the button has an action.
            return self.battle_log or self.found_items
            
    
    class ExplorationGuild(TaskUpgrade):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 70, "Bricks": 50, "Glass": 5}
        COST = 10000
        ID = "ExplorationGuild"
        IMG = "content/gfx/bg/buildings/Chorrol_Fighters_Guild.png"
        def __init__(self, name="Exploration Guild", instance=None, desc="Travel to exotic places, meet new monsters and people... and take their shit!", img="content/gfx/bg/buildings/Chorrol_Fighters_Guild.png", build_effort=0, materials=None, in_slots=0, cost=0, **kwargs):
            super(ExplorationGuild, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            
            # Global Values that have effects on the whole business.
            self.teams = list() # List to hold all the teams formed in this guild. We should add at least one team or the guild will be useless...
            self.explorers = list() # List to hold all the (active) exploring trackers.

            self.teams.append(Team("Avengers", free=1))
            if config.debug:
                for i in range(5):
                    self.teams.append(Team(str(i), free=1))
                    
            self.workable = True
            self.focus_team = None
            self.team_to_launch_index = 0
            self.capture_chars = False # Do we capture chars during exploration in this building. # Move to Areas?
            
        # Teams control methods:
        def teams_to_launch(self):
            # Returns a list of teams that can be launched on an exploration run.
            # Must have at least one member and NOT already running exploration!
            return [t for t in self.teams_for_setup() if t]
            
        def prev_team_to_launch(self):
            teams = self.teams_to_launch()
            index = self.team_to_launch_index
            
            index = (index-1) % len(teams)
            
            self.team_to_launch_index = index
            self.focus_team = teams[index]
        
        def next_team_to_launch(self):
            teams = self.teams_to_launch()
            index = self.team_to_launch_index
            
            index = (index+1) % len(teams)
            
            self.team_to_launch_index = index
            self.focus_team = teams[index]
            
        def exploring_teams(self):
            # Teams that are busy with exploration runs.
            return [tracker.team for tracker in self.explorers]
        
        def teams_for_setup(self):
            # Teams avalible for setup in order to set them on exploration runs.
            return [t for t in self.teams if t not in self.exploring_teams()]
            
        # SimPy methods:
        def business_control(self):
            """SimPy business controller.
            """
            for tracker in self.explorers:
                self.env.process(self.exploration_controller(tracker))
                
            while 1:
                yield self.env.timeout(100)
                
        def launch_team(self, area, _team=None):
            # Moves the team to appropriate list, removes from main one and makes sure everything is setup right from there on out:
            team = self.focus_team if not _team else _team
            # self.teams.remove(team) # We prolly do not do this?
            
            tracker = ExplorationTracker(team, area)
            self.explorers.append(tracker)
            
            if not _team:
                self.focus_team = None
                self.team_to_launch_index = 0
            
        def exploration_controller(self, tracker):
            # Controls the exploration by setting up proper simpy processes.
            
            # Convert AP to exploration points:
            self.convert_AP(tracker)
            
            # Set the state to traveling back if we're done:
            if tracker.day > tracker.days:
                tracker.state = "traveling back"
            
            while self.env.now < 99:
                if tracker.state == "traveling to":
                    yield self.env.process(self.travel_to(tracker))
                    # Testing mode, we can plainly build a report to see what's happening:
                    tracker.build_nd_report() # Report methods needs moar luv, this is not gonna fly atm. Gonna try making it work tonight.
                    
                # elif tracker.state == "exploring":
                    # yield self.env.process(self.explore(tracker))
                # elif tracker.state == "camping":
                    # yield self.env.process(self.camping(tracker))
                # elif tracker.state == "traveling back":
                    # yield self.env.process(self.travel_back(tracker))
                
            if config.debug:
                tracker.log("The day has come to an end for {}.".format(tracker.team.name))
            tracker.day += 1
            
            
                    
        def travel_to(self, tracker):
            # Env func that handles the travel to routine.
            
            # Figure out how far we can travel in 5 du:
            # Understanding here is that any team can travel 25 KM per day on average. This can be offset by traits and stats in the future.
            tacker.tp = int(round(tracker.ep / 20.0))
            
            while 1:
                yield self.env.timeout(5) # We travel...
                
                raise Exception("meow")
                
                tracker.ep -= tracker.tp
                tracker.traveled += 1.25
                
                # Team arrived:
                if tracker.traveled <= tracker.distance:
                    temp = "{} arrived to {}!".format(tracker.team.name, tracker.area.id)
                    if tracker.day > 0:
                        temp = temp + " It took {} {} to get there.".format(tracker.day, plural("day", tracker.day))
                    tracker.log(temp, name="Arrival")
                
                if self.evn.now == 99: # We couldn't make it there before the days end...
                    temp = "{} spent the entire day on route to {}! ".format(tracker.team.name, tracker.area.id)
                    tracker.log(temp)
                    # self.env.exit("not there yet") Not needed?
                
        def travel_back(self, tracker):
            # Env func that handles the travel to routine.
            
            # Figure out how far we can travel in 5 du:
            # Understanding here is that any team can travel 25 KM per day on average. This can be offset by traits and stats in the future.
            tacker.tp = int(round(tracker.ep / 20.0))
            
            while 1:
                yield self.env.timeout(5) # We travel...
                
                tracker.ep -= tracker.tp
                tracker.traveled += 1.25
                
                # Team arrived:
                if tracker.traveled <= tracker.distance:
                    temp = "{} came back to the guild from {}!".format(tracker.team.name, tracker.area.id)
                    if tracker.day > 0:
                        temp = temp + " It took {} {} to get back.".format(tracker.day, plural("day", tracker.day))
                    tracker.log(temp, name="Return")
                    # Leads to building a report
                
                if self.evn.now == 99: # We couldn't make it there before the days end...
                    temp = "{} spent the entire day going back to the guild from {}! ".format(tracker.team.name, tracker.area.id)
                    tracker.log(temp)
                    self.env.exit("on the way back")
                    
        def camping(self, tracker):
            """Camping will allow restoration of health/mp/agility and so on. Might be forced on low health.
            """
            team = tracker.team
            keep_camping = True
            
            temp = "{} (in {}) setup a camp to get some rest and recover!".format(tracker.team.name, tracker.area.id)
            tracker.log(temp)
            
            while keep_camping:
                yield self.env.timeout(5) # We camp...
                
                for c in team:
                    c.health += randint(5, 6)
                    c.mp += randint(5, 6)
                    c.vitality += randint(8, 12)
                    
                for c in team:
                    if c.health <= c.get_max("health")*.9:
                        break
                    if c.mp <= c.get_max("mp")*.9:
                        break
                    if c.vitality <= c.get_max("vitality"):
                        break
                else:
                    temp = "{} are now ready for more action in {}! ".format(tracker.team.name, tracker.area.id)
                    tracker.log(temp)
                    self.env.exit("restored after camping")
                    
        def overnight(self, tracker):
            # overnight: More effective heal. Spend the night resting.
            # Do we run this? This prolly doesn't need to be a simpy process... or maybe schedual this to run at 99.
            
            team = tracker.team
            
            temp = "{} are done with exploring for the day and will now rest and recover! ".format(tracker.team.name)
            tracker.log(temp)
            
            for c in team:
                c.health += randint(60, 70)
                c.mp += randint(60, 70)
                c.vitality += randint(8, 12)
        
        def explore(self, tracker):
            """SimPy process that handles the exploration itself.
            
            Idea is to keep as much of this logic as possible and adapt it to work with SimPy...
            """
            items = list()
            area = tracker.area
            fought_mobs = 0
            encountered_opfor = 0
            
            # Points (ability) Convertion:
            for char in tracker.team:
                # Set their cleaning capabilities as temp flag:
                tracker.power += int(round(1 + w.agility * 0.1)) # Exploration Points...? How do we calculate?
            
            # AP Convertion:
            self.convert_AP(tracker)
            
            #Day 1 Risk 1 = 0.213, D 15 R 1 = 0.287, D 1 R 50 = 0.623, D 15 R 50 = 0.938, D 1 R 100 = 1.05, D 15 R 100 = 1.75
            risk_a_day_multiplicator = int(round(((0.2 + (area.risk*0.008))*(1 + tracker.day*(0.025*(1+area.risk/100))))*0.05)) # For now, I'll just devide the damn thing by 20...
            
            while 1:
                yield self.env.timeout(5) # We'll go with 5 du per one iteration of "exploration loop".
                
                # Hazzard:
                if area.hazard:
                    temp = "{color=[blue]}Hazardous area!{/color} The team has been effected."
                    tracker.log(temp)
                    for char in tracker.team:
                        for stat in area.hazard:
                            # value, because we calculated effects on daily base in the past...
                            var = max(1, int(round(area.hazard[stat]*.05)))
                            char.mod(stat, -var) # TODO: Change to log + direct application.
                            
                if tracker.items and dice(area.risk*0.2 + tracker.day *3):
                    items.append(choice(tracker.items))
                
                # Second round of items for those specifically specified for this area:
                for i in area.items:
                    if dice((area.items[i]*risk_a_day_multiplicator)): # TODO: Needs to be adjusted to SimPy (lower the probability!)
                        temp = "{color=[blue]}Found an item {}!{/color}.".format(i.name)
                        tracker.log("Found Item", temp, ui_log=True)
                        
                        items.append(i)
                        # break   #too hard to calculate chances for json with that
                
                if dice(area.risk + self.day*2):
                    cash += randint(int(tracker.cash_limit/50*self.day), int(tracker.cash_limit/15*tracker.day))
                
                #  =================================================>>>
                # Girls capture (We break off exploration run in case of success):
                if tracker.capture_chars:
                    for g in area.girls:
                        if g in chars and dice(area.girls[g] + tracker.day*0.1) and g.location == "se":
                            tracker.captured_girl = None # chars[g] # TODO: Properly create the rchar...
                            self.env.exit("captured char")
                            
                        # TODO: g in rchars looks like broken code! This also need to be updated and reviewed.
                        elif g in rchars and dice(area.girls[g] + self.day*0.1):
                            new_random_girl = build_rc()
                            self.captured_girl = build_rc()
                            self.env.exit("captured rchar")
                
                if not fought_mobs:
                    mob = None
                    
                    for key in tracker.mobs:
                        encounter_chance = dice(((tracker.mobs[key][0]*risk_a_day_multiplicator)/(ap/2)))*0.05 # Needs a rework... what is ap here?
                        if encounter_chance: # Needs a review, we don't have ap here anymore.
                            enemies = choice(tracker.mobs[key][2]) # Amount if mobs on opfor team!
                            mob = key
                            temp = "{} were attacked by ".format(team.name)
                            temp = temp + "%d %s!" % (enemies, plural(mob, enemies))
                            log = tracker.log("Engagement", temp, ui_log=True)
                            break
                            
                    if mob:
                        self.combat_mobs(tracker, mob, enemies, log)
        
                if items and cash:
                    self.txt.append("The team has found: %s %s" % (", ".join(items), plural("item", len(items))))
                    self.found_items.extend(items)
                    self.txt.append(" and {color=[gold]}%d Gold{/color} in loot" % cash)
                    self.cash.append(cash)
                
                if cash and not items:
                    self.txt.append("The team has found: {color=[gold]}%d Gold{/color} in loot" % cash)
                    self.cash.append(cash)
                
                if items or cash:
                    self.txt.append("!\n")
                
                if not items and not cash:
                    self.txt.append("It was a quite day of exploration, nothing of interest happened...")
                
                self.stats["agility"] += randrange(2)
                self.stats["exp"] += randint(5, max(15, self.risk/4))
                
                inv = list(g.inventory for g in self.team)
                
                for g in self.team:
                    l = list()
                    
                    if g.health < 75:
                        l.extend(g.auto_equip(["health"], source=inv))
                    
                    if g.vitality < 100:
                        l.extend(g.auto_equip(["vitality"], source=inv))
                    
                    if g.mp < 30:
                        l.extend(g.auto_equip(["mp"], source=inv))
                    
                    if l:
                        self.txt.append("\n%s used: {color=[blue]}%s %s{/color} to recover!\n" % (g.nickname, ", ".join(l), plural("item", len(l))))
                
                if not stop and self.day == self.days:
                    self.txt.append("\n\n {color=[green]}The party has finished their exploration run!{/color}")
                    stop = True
                
                if not stop:
                    for member in self.team:
                        if member.health <= (member.get_max("health") / 100.0 * (100 - self.risk)) or member.health < 15:
                            temp = "{color=[blue]}Your party falls back to base due to risk factors!{/color}"
                            tracker.log(temp)
                            
            
        def combat_mobs(self, tracker, mob, amount, log):
            # amount of mobs*
            # log is the exlog object we add be report to!
            
            team = tracker.team
            opfor = Team(name="Enemy Team", max_size=amount)
            
            # Get a level... for now, I am keeping it plain and simple:
            level = tracker.mobs[mob][0]
            mob_id = mob
            
            for i in xrange(amount):
                mob = build_mob(id=mob, level=level)
                mob.controller = BE_AI(mob)
                opfor.add(mob)
            
            # Logical battle scenario:
            battle = BE_Core(logical=1)
            store.battle = battle # Making it global... I need to make sure this is not needed.
            battle.teams.append(team)
            battle.teams.append(opfor)
            battle.start_battle()
            
            # Add the battle report to log!:
            log.battle_log = reversed(battle.combat_log)
            
            if battle.winner == team:
                log.battle_won = True
                for member in team:
                    member.attack += randrange(3)
                    member.defence + randrange(3)
                    member.agility += randrange(3)
                    member.magic += randrange(3)
                    member.exp += level*10 # Adjust for levels? ! TODO:
                
                # Death needs to be handled based off risk factor: TODO:
                # for member in self.team:
                    # damage = randint(3, 10)
                    # if member.health - damage <= 0:
                        # if self.risk > 75:
                            # self.txt.append("\n{color=[red]}%s has died during this skirmish!{/color}\n" % member.name)
                            # stop = True
                            # member.health -= damage
                        # else:
                            # self.txt.append("\n{color=[red]}%s nearly died during this skirmish... it's time for the party to fall back!{/color}\n")
                            # stop = True
                            # member.health = 1
                    # else:
                        # member.health -= damage
                    # member.mp -= randint(3, 7)
            
            if result[0] == "defeat": # Defeat here...
                # self.stats["attack"] += randrange(2)
                # self.stats["defence"] += randrange(2)
                # self.stats["agility"] += randrange(2)
                # self.stats["magic"] += randrange(2)
                # self.stats["exp"] += mob_power/15
                
                self.txt.append("{color=[red]}Exploration Party was defeated!{/color}\n")
                
        
        def convert_AP(self, tracker):
            # Convert teams AP to Job points:
            # The idea here is that teammates will help each other to carry out any task and act as a unit, so we don't bother tracking individual AP.
            team = tracker.team
            AP = 0
            for m in team:
                AP + m.AP
            tracker.points = AP * 100
            
    # Sub Upgrades
    class SubUpgrade(BuildingUpgrade):
        """Usually suggests an expansion to a business upgrade that modifies some of it's workflow/properties/jobs!
        
        I want to code a skeleton for this atm.
        """
        COMPATIBILITY = []
        def __init__(self, *args, **kwargs):
            super(SubUpgrade, self).__init__(*args, **kwargs)
            
            self.main_upgrade = None
            
        @property
        def img(self):
            # We return IMG instead of the usual img here.
            return self.IMG
            
        @property
        def cost(self):
            # We return IMG instead of the usual img here.
            return self.COST
            
    class CatWalk(SubUpgrade):
        COMPATIBILITY = [StripClub]
        MATERIALS = {"Wood": 10, "Bricks": 30, "Glass": 2}
        COST = 1000
        ID = "Cat Walk"
        IMG = "content/buildings/upgrades/catwalk_0.jpg"
        def __init__(self, name="Cat Walk", instance=None, desc="Good way to show off your strippers!", build_effort=0, materials=None, in_slots=2, **kwargs):
            super(CatWalk, self).__init__(name=name, instance=instance, desc=desc, build_effort=build_effort, materials=materials, **kwargs)
            
            
            # ??? Think of a way to generalize bonuses? Maybe a system with clear mechanics is needed...
            
            
    class Aquarium(SubUpgrade):
        COMPATIBILITY = [StripClub]
        MATERIALS = {"Glass": 10, "Wood": 5}
        COST = 2500
        ID = "Aquarium"
        IMG = "content/buildings/upgrades/aquarium_nq.jpg"
        def __init__(self, name="Aquarium", instance=None, desc="Enhance the entertainment experience of your clients!", build_effort=0, materials=None, in_slots=4, **kwargs):
            super(Aquarium, self).__init__(name=name, instance=instance, desc=desc, build_effort=build_effort, materials=materials, **kwargs)
            
