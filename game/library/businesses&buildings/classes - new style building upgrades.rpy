init -9 python:
    #################################################################
    # BUILDING UPGRADE CLASSES
    class BuildingUpgrade(_object):
        """
        BaseClass for any building expansion!
        """
        def __init__(self, name="", instance=None, desc="", img="", build_effort=0, materials=None, in_slots=1, ex_slots=0, cost=0):
            self.name = name # name, a string.
            self.instance = instance # Building this upgrade belongs to.
            self.desc = desc # description, a string.
            self.img = img # Ren'Py path leading the an image, a string.
            
            self.build_effort = build_effort # Effort it takes to build this upgrade. 0 for instant.
            if not materials:
                self.materials = {} # Materials required to build this upgrade. Empty dict for none.
            else:
                self.materials = materials
            self.in_slots = in_slots # Internal slots
            self.ex_slots = ex_slots # External slots
            self.cost = cost # Price in gold.
            
            self.jobs = set() # Jobs this upgrade can add. *We add job instances here!  # It may be a good idea to turn this into a direct job assignment instead of a set...
            self.workers = set() # List of on duty characters.
            
            self._rep = 0
            
            self.habitable = False
            self.workable = False
            
            self.clients = set() # Local clients, this is used during next day and reset on when that ends.
        
        def get_client_count(self):
            # Returns amount of workers we expect to come here.
            return 2 + self._rep*0.01*self.all_workers
            
        @property
        def job(self):
            # This may not be required if we stick to a single job per business scenario:
            if self.jobs:
                return random.sample(self.jobs, 1).pop()
            
        # Reputation:
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
            # Logs the text to log...
            self.instance.nd_events_report.append(item)
            
        def has_workers(self, amount=1):
            # Checks if there is a worker(s) availible.
            return False
            
        def get_workers(self, amount=1):
            # Finds a best match for workers and returns them...
            return None
            
        @property
        def all_workers(self):
            return list(i for i in self.instance.workers if self.all_occs & i.occupations)
            
        def action_priority_workers(self, job):
            return list(i for i in self.instance.workers if i.action == job)
            
        def get_workers(self, job, amount=1, match_to_client=None):
            """Tries to find workers for any given job.
            
            - Tries to get a perfect match where action == job first.
            - Tries to get any match trying to match any occupaiton at all.
            
            @param: match_to_client: Will try to find the a good match to client, expects a client (or any PytC instance with .likes set) object.
            """
            workers = list()
            
            priority = self.action_priority_workers(job)
            shuffle(priority)
            anyw = list(i for i in self.all_workers if i not in priority)
            shuffle(anyw)
            while len(workers) < amount and (priority or anyw):
                while priority and len(workers) < amount:
                    if match_to_client:
                        w = self.find_best_match(match_to_client, priority) # This is not ideal as we may end up checking a worker who will soon be removed...
                    else:
                        w = priority.pop()
                    if self.check_worker_capable(w) and self.check_worker_willing(w, job):
                        workers.append(w)
                        
                while anyw and len(workers) < amount:
                    if match_to_client:
                        w = self.find_best_match(match_to_client, anyw) # This is not ideal as we may end up checking a worker who will soon be removed...
                    else:
                        w = anyw.pop()
                    if self.check_worker_capable(w) and self.check_worker_willing(w, job):
                        workers.append(w)
                        
            return workers
            
        def find_best_match(self, client, workers):
            """Attempts to match a client to the best worker.
            
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
            """
            Returns True if this upgrade requires a Worker to run this job.
            Example: Building
            Strip Club on the other hand may nor require one or one would be requested later.
            It may be a better bet to come up with request_worker method that evaluates the same ealier, we'll see.
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
                if worker in self.instance.workers:
                    self.instance.workers.remove(worker)
                    
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
                if worker in self.instance.workers:
                    self.instance.workers.remove(worker)
                temp = set_font_color('{}: {} is done working for the day.'.format(self.env.now, worker.name), "aliceblue")
                self.log(temp)
                return False
                
        def pre_nd(self):
            # Runs at the very start of execusion of SimPy loop during the next day.
            return
            
        @property
        def all_occs(self):
            s = set()
            for j in self.jobs:
                s = s | j.all_occs
            return s
        
        def post_nd_reset(self):
            # Resets all flags and variables after next day calculations are finished.
            pass
        
        
    class MainUpgrade(BuildingUpgrade):
        """
        Usually suggests a business of some kind and unlocks jobs and other upgrades!
        """
        def __init__(self, *args, **kwargs):
            super(MainUpgrade, self).__init__(*args, **kwargs)
            
            
    class BrothelBlock(MainUpgrade):
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
            
        def get_client_count(self):
            # Returns amount of workers we expect to come here.
            return int(round(2 + self._rep*0.01*max(len(self.all_workers), self.capacity)))
            
        def has_workers(self):
            return list(i for i in self.instance.workers if self.all_occs & i.occupations)
            
        def requires_workers(self, amount=1):
            return True
            
        def pre_nd(self):
            self.res = simpy.Resource(self.env, self.capacity)
            
        def request_room(self, client, char):
            with self.res.request() as request:
                yield request
                        
                # All is well and we create the event
                temp = "{}: {} and {} enter the room.".format(self.env.now, client.name, char.name)
                self.log(temp)
                
                yield self.env.process(self.run_job(client, char))
                
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
            
            # Execute the job:
            self.job(char, client)
            
            # We return the char to the nd list:
            self.instance.workers.insert(0, char)
            
        def post_nd_reset(self):
            self.res = None
            self.is_running = False
            
            
    class StripClub(MainUpgrade):
        def __init__(self, name="Strip Club", instance=None, desc="Exotic Dancers go here!", img="content/buildings/upgrades/strip_club.jpg", build_effort=0, materials=None, in_slots=5, cost=500, **kwargs):
            super(StripClub, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Striptease Job"]])
            self.workable = True
            self.type = "public_service"
            
            self.capacity = in_slots
            self.active_workers = set() # On duty Strippers.
            self.clients = set() # Clients watching the stripshows.
            
            # SimPy and etc follows (L33t stuff :) ):
            self.res = None # Restored before every job...
            self.time = 5
            self.is_running = False
            
            self.earned_cash = 0
            
        def get_client_count(self):
            # Returns amount of workers we expect to come here.
            return int(round(3 + self._rep*0.05*max(len(self.all_workers), self.capacity)))
            
        def pre_nd(self):
            self.res = simpy.Resource(self.env, self.capacity)
            
        def request_spot(self, client):
            """Request for a spot for a client in the club is being made here.
            """
            with self.res.request() as request:
                yield request
                
                # All is well and we create the event:
                temp = "{}: {} enters the Strip Club.".format(self.env.now, client.name)
                self.clients.add(client)
                self.log(temp)
                
                while not client.flag("jobs_ready_to_leave"):
                    yield self.env.timeout(1)
                
                temp = "{}: {} leaves the Club.".format(self.env.now, client.name)
                self.clients.remove(client)
                self.log(temp)
                client.del_flag("jobs_busy")
                
        def send_in_workers(self):
            if not self.active_workers or len(self.active_workers) < self.res.count/4:
                workers = self.instance.workers
                # Get all candidates:
                job = self.job
                ws = self.get_workers(job)
                if ws:
                    w = ws.pop()
                    self.active_workers.add(w)
                    workers.remove(w)
                    self.env.process(self.use_worker(w))
                
        def run_business(self, end):
            """This runs the club as a SimPy process from start to the end.
            
            Called once for a building and yields self.time timeouts writing reports.
            """
            # See if there are any strip girls, that may be added to Resource at some point of the development:
            while 1:
                yield self.env.timeout(self.time)
                
                # Handle the earnings:
                # It's prolly better to handle earnings in clients methods (Since they do the actual paying)
                cash = self.res.count*len(self.active_workers)*randint(8, 12)
                self.earned_cash += cash
                
                # Manage clients...
                for c in self.clients:
                    c.mod_flag("jobs_seen_strip_for", self.time)
                    if c.flag("jobs_seen_strip_for") >= self.time*2:
                        c.set_flag("jobs_ready_to_leave")
                
                if config.debug:
                    temp = "{}: Debug: {} places are currently in use in StripClub | Cash earned: {}, Total: {}!".format(self.env.now, set_font_color(self.res.count, "red"), cash, self.earned_cash)
                    temp = temp + " {} Workers are currently doing streaptease!".format(set_font_color(len(self.active_workers), "red"))
                    self.log(temp)
                    
                if not self.all_workers and not self.active_workers:
                    break
                    
            # We remove the business from nd if there are no more strippers to entertain:
            temp = "There are no Strippers available to entertain in {} so club is shutting down!".format(self.name)
            self.log(temp)
            self.instance.nd_ups.remove(self)
            
        def use_worker(self, worker):
            temp = "{}: {} comes out to do a stripshow!".format(self.env.now, worker.name)
            self.log(temp)
            while worker.AP and self.res.count:
                yield self.env.timeout(self.time) # This is a single shift a worker can take for cost of 1 AP.
                worker.set_union("jobs_strip_clients", self.clients)
                worker.AP -= 1
                tips = randint(4, 7) * self.res.count
                worker.mod_flag("jobs_" + self.job.id + "_tips", tips)
                temp = "{}: {} gets {} in tips from {} clients!".format(self.env.now, worker.name, tips, self.res.count)
                self.log(temp)
                
            if worker.flag("jobs_strip_clients"):
                temp = "{}: Logging StripJob for {}!".format(self.env.now, worker.name)
                self.log(temp)
                simple_jobs["Striptease Job"](worker) # better bet to access Class directly...
            else:
                temp = "{}: No clients came to see {}".format(self.env.now, worker.name)
                self.log(temp)
                
            self.active_workers.remove(worker)
            temp = "{}: {} is done entertaining for the day!".format(self.env.now, set_font_color(worker.name, "red"))
            self.log(temp)
            
        def post_nd_reset(self):
            self.res = None
            self.is_running = False
            self.active_workers = set()
            self.clients = set()
            self.earned_cash = 0
            
            
    class Bar(MainUpgrade):
        """Bar Main Upgrade.
        """
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
            
        def get_client_count(self):
            # Returns amount of workers we expect to come here.
            return int(round(3 + self._rep*0.05*max(len(self.all_workers), self.capacity)))
            
        def pre_nd(self):
            self.res = simpy.Resource(self.env, self.capacity)
            
        def request_spot(self, client):
            """Request for a spot for a client in thebar is being made here.
            
            Clients pay for the service here.
            We add dirt here.
            """
            with self.res.request() as request:
                yield request
                
                # All is well and we create the event:
                temp = "{}: {} enters the {}.".format(self.env.now, client.name, self.name)
                self.clients.add(client)
                self.log(temp)
                
                while not client.flag("jobs_ready_to_leave"):
                    yield self.env.timeout(1)
                    
                # This stuff should be better conditioned later:
                cash = randint(8, 12)
                dirt = randint(5, 7)
                self.earned_cash += cash
                self.instance.dirt += dirt
                
                temp = "{}: {} exits the Bar leaving {} Gold and {} Dirt behind.".format(self.env.now, client.name, cash, dirt)
                self.clients.remove(client)
                self.log(temp)
                client.del_flag("jobs_busy")
                
        def send_in_workers(self):
            if not self.active_workers or len(self.active_workers) < self.res.count/4:
                workers = self.instance.workers
                # Get all candidates:
                job = self.job
                ws = self.get_workers(job)
                if ws:
                    w = ws.pop()
                    self.active_workers.add(w)
                    workers.remove(w)
                    self.env.process(self.use_worker(w))
                
        def run_business(self, end):
            """This runs the club as a SimPy process from start to the end.
            """
            # See if there are any strip girls, that may be added to Resource at some point of the development:
            while 1:
                yield self.env.timeout(self.time)
                
                # Handle the earnings:
                # cash = self.res.count*len(self.active_workers)*randint(8, 12)
                # self.earned_cash += cash # Maybe it's better to handle this on per client basis in their own methods? Depends on what modifiers we will use...
                
                # Manage clients...
                for c in self.clients:
                    c.mod_flag("jobs_spent_in_bar", self.time)
                    if c.flag("jobs_spent_in_bar") >= self.time*2:
                        c.set_flag("jobs_ready_to_leave")
                
                if config.debug:
                    temp = "{}: Debug: {} places are currently in use in Bar | Total Cash earned so far: {}!".format(self.env.now, set_font_color(self.res.count, "red"), self.earned_cash)
                    temp = temp + " {} Workers are currently tending the bar!".format(set_font_color(len(self.active_workers), "red"))
                    self.log(temp)
                    
                if not self.all_workers and not self.active_workers:
                    break
                    
            # We remove the business from nd if there are no more strippers to entertain:
            temp = "There are no bartenders available in the {} so it is shutting down!".format(self.name)
            self.log(temp)
            self.instance.nd_ups.remove(self)
            
        def use_worker(self, worker):
            temp = "{}: {} comes out to serve customers!".format(self.env.now, worker.name)
            self.log(temp)
            while worker.AP and self.res.count:
                yield self.env.timeout(self.time) # This is a single shift a worker can take for cost of 1 AP.
                worker.set_union("jobs_bar_clients", self.clients)
                worker.AP -= 1
                tips = randint(4, 7) * self.res.count
                worker.mod_flag("jobs_" + self.job.id + "_tips", tips)
                temp = "{}: {} gets {} in tips from {} clients!".format(self.env.now, worker.name, tips, self.res.count)
                self.log(temp)
                
            if worker.flag("jobs_bar_clients"):
                temp = "{}: Logging {} for {}!".format(self.env.now, self.name, worker.name)
                self.log(temp)
                simple_jobs["Bartending"](worker) # better bet to access Class directly...
            else:
                temp = "{}: No clients bought drinks from {}".format(self.env.now, worker.name)
                self.log(temp)
                
            self.active_workers.remove(worker)
            temp = "{}: {} is done bar tending for the day!".format(self.env.now, set_font_color(worker.name, "red"))
            self.log(temp)
            
        def post_nd_reset(self):
            self.res = None
            self.is_running = False
            self.active_workers = set()
            self.clients = set()
            self.earned_cash = 0
            
            
    class Cleaners(MainUpgrade):
        """This will be the first upgrade that will take care clearing some workload.
        """
        pass
            
            
    class Garden(MainUpgrade):
        def __init__(self, name="Garden", instance=None, desc="Relax!", img="content/buildings/upgrades/garden.jpg", build_effort=0, materials=None, in_slots=0, ex_slots=2, cost=500, **kwargs):
            super(Garden, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            
            
    class MainHall(MainUpgrade):
        def __init__(self, name="Main Hall", instance=None, desc="Reception!", img="content/buildings/upgrades/main_hall.jpg", build_effort=0, materials=None, in_slots=0, ex_slots=2, cost=500, **kwargs):
            super(MainHall, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set()
            
            
    class WarriorQuarters(MainUpgrade):
        def __init__(self, name="Warrior Quarters", instance=None, desc="Place for Guards!", img="content/buildings/upgrades/guard_qt.jpg", build_effort=0, materials=None, in_slots=2, ex_slots=1, cost=500, **kwargs):
            super(WarriorQuarters, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set(["Guard"])
            
            
    class SlaveQuarters(MainUpgrade):
        def __init__(self, name="Slave Quarters", instance=None, desc="Place for slaves to live in!", img="content/buildings/upgrades/guard_qt.jpg", build_effort=0, materials=None, in_slots=2, ex_slots=0, cost=500, **kwargs):
            super(SlaveQuarters, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.rooms = in_slots
            
    # UPGRADES = [Bar(), BrothelBlock(), StripClub(), Garden(), MainHall(), WarriorQuarters(), SlaveQuarters()]
            
