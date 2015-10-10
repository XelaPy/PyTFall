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
            
            self.jobs = set() # Jobs this upgrade can add. *We add job instances here!
            self.workers = set() # List of on duty characters.
            
            self._rep = 0
            
            self.habitable = False
            self.workable = False
            
            self.clients = set() # Local clients, this is used during next day and reset on when that ends.
        
        def get_client_count(self):
            # Returns amount of workers we expect to come here.
            return 2 + self._rep*0.01*self.all_workers
            
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
            
        def requires_workers(self, amount=1):
            """
            Returns True if this upgrade requires a Worker to run this job.
            Example: Building
            Strip Club on the other hand may nor require one or one would be requested later.
            It may be a better bet to come up with request_worker method that evaluates the same ealier, we'll see.
            """
            return False
            
        def pre_nd(self):
            # Runs at the very start of execusion of SimPy loop during the next day.
            return
            
        @property
        def all_occs(self):
            s = set()
            for i in self.jobs:
                s = s | i.all_occs
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
            self.type = "personal_type"
            self.jobs = set([simple_jobs["Whore Job"]])
            self.workable = True
            
            # SimPy and etc follows (L33t stuff :) ):
            self.res = None # Restored before every job...
            self.time = 5 # Same
            
        def get_client_count(self):
            # Returns amount of workers we expect to come here.
            return int(round(2 + self._rep*0.01*max(len(self.all_workers), self.capacity)))
            
        def has_workers(self):
            return list(i for i in self.instance.workers if self.all_occs & i.occupations)
            
        def requires_workers(self, amount=1):
            return True
            
        def get_workers(self, client, amount=1):
            """This is quite possibly an overkill for this stage of the game development.
            
            For now we just work with one clients.
            """
            workers = list()
            
            # TODO: Left off here, ALL SIW Occupations make it, this needs to be narrowed down somehow to return only a proper occupation.
            # First gets the workers assigned directly to this upgrade as a priority.
            priority = list(i for i in self.instance.workers if i.workplace == self and self.all_occs & i.occupations)
            for i in xrange(amount):
                try:
                    w = self.find_best_match(client, workers)
                    if w:
                        workers.append(w)
                    else:
                        workers.append(priority.pop())
                except:
                    break
            
            if len(workers) < amount:
                # Next try to get anyone availible:
                anyw = list(i for i in self.instance.workers if self.all_occs & i.occupations)
                for i in xrange(amount-len(workers)):
                    try:
                        w = self.find_best_match(client, workers)
                        if w:
                            workers.append(w)
                        else:
                            workers.append(anyw.pop())
                    except:
                        break
                        
            if len(workers) == amount:
                if len(workers) == 1:
                    return workers.pop()
            # When we'll have jobs that require moar than one worker, we'll add moar code here.
            
        def find_best_match(self, client, workers):
            worker = None
            for w in workers:
                likes = client.likes.intersection(w.traits)
                if likes:
                    if len(likes) == 1:
                        likes = likes.pop()
                    else:
                        likes = ", ".join(likes)
                    temp = '{} liked {} for {}.'.format(client.name, w.nickname, likes)
                    self.instance.log(temp)
                    worker = w
                    break
            return worker
            
        def pre_nd(self):
            self.res = simpy.Resource(self.env, self.capacity)
            
        def request(self, client, char):
            with self.res.request() as request:
                yield request
                        
                # All is well and we create the event
                temp = "{} and {} enter the room at {}".format(client.name, char.name, self.env.now)
                self.log(temp)
                
                yield self.env.process(self.run_job(client, char))
                
                temp = "{} leaves at {}".format(client.name, self.env.now)
                self.log(temp)
                
        def run_job(self, client, char):
            """
            This should be a job...
            """
            yield self.env.timeout(self.time)
            if config.debug:
                temp = "Debug: {} Building Resource in use!".format(set_font_color(self.res.count, "red"))
                self.log(temp)
            
            temp = "{} and {} did their thing!".format(set_font_color(char.name, "pink"), client.name)
            self.log(temp)
            char.action(char, client)
            
            # We return the char to the nd list:
            self.instance.workers.insert(0, char)
            
        def post_nd_reset(self):
            self.res = None
            
            
    class StripClub(MainUpgrade):
        def __init__(self, name="Strip Club", instance=None, desc="Exotic Dancers go here!", img="content/buildings/upgrades/strip_club.jpg", build_effort=0, materials=None, in_slots=5, cost=500, **kwargs):
            super(StripClub, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Striptease Job"]])
            self.workable = True
            self.type = "club_type"
            
            self.capacity = in_slots
            self.active = set() # On duty Strippers.
            self.clients = set() # Clients watching the stripshows.
            
            # SimPy and etc follows (L33t stuff :) ):
            self.res = None # Restored before every job...
            self.time = 5 # Same
            self.is_running = False
            
            self.earned_cash = 0
            
        def get_client_count(self):
            # Returns amount of workers we expect to come here.
            return int(round(3 + self._rep*0.05*max(len(self.all_workers), self.capacity)))
            
        def pre_nd(self):
            self.res = simpy.Resource(self.env, self.capacity)
            
        def request(self, client):
            with self.res.request() as request:
                yield request
                
                # All is well and we create the event
                temp = "{} enters the Strip Club at {}".format(client.name, self.env.now)
                self.clients.add(client)
                self.log(temp)
                
                # TODO: LEFT OFF HERE, THIS IS A MESS.
                while not client.flag("jobs_ready_to_leave"):
                    yield self.env.timeout(2)
                # yield self.env.process(self.run_job(client))
                
                temp = "{} leaves the Club at {}".format(client.name, self.env.now)
                self.clients.remove(client)
                self.log(temp)
                
        def run_job(self, end):
            # See if there are any strip girls, that may be added to Resource at some point of the development:
            while 1:
                if not self.active or len(self.active) < self.res.count/3:
                    workers = self.instance.workers
                    # Get all candidates:
                    aw = self.all_workers
                    if aw:
                        shuffle(aw)
                        worker = aw.pop()
                        self.active.add(worker)
                        workers.remove(worker)
                        self.env.process(self.use_worker(worker))
                    
                yield self.env.timeout(self.time)
                
                # Handle the cash/tips:
                cash = self.res.count*len(self.active)*randint(8, 12)
                self.earned_cash += cash
                
                # Manage clients...
                for c in self.clients:
                    c.mod_flag("jobs_seen_strip_for", self.time)
                    if c.flag("jobs_seen_strip_for") >= self.time*2:
                        c.set_flag("jobs_ready_to_leave")
                
                if config.debug:
                    temp = "Debug: {} places are currently in use in StripClub | Cash earned: {}, Total: {}!".format(set_font_color(self.res.count, "red"), cash, self.earned_cash)
                    self.log(temp)
            
        def use_worker(self, worker):
            temp = "{} comes out to do a stripshow!".format(worker.name)
            self.log(temp)
            while worker.AP and self.res.count:
                yield self.env.timeout(5) # This is a single shift a worker can take for cost of 1 AP.
                worker.set_union("jobs_strip_clients", self.clients)
                worker.AP -= 1
                tips = randint(4, 7) * self.res.count
                worker.mod_flag("jobs_" + worker.action.id + "_tips", tips)
                temp = "{} gets {} in tips from {} clients!".format(worker.name, tips, self.res.count)
                self.log(temp)
                
            if worker.flag("jobs_strip_clients"):
                simple_jobs["Striptease Job"](worker, self) # BETTER BET TO ACCESS Class directly...
            else:
                temp = "No clients came to see {}".format(worker.name)
                self.log(temp)
            self.active.remove(worker)
            temp = "{} is done entertaining for the day!".format(set_font_color(worker.name, "red"))
            self.log(temp)
            
        def post_nd_reset(self):
            self.res = None
            self.is_running = False
            self.active = set()
            self.clients = set()
            self.earned_cash = 0
            
            
    class Bar(MainUpgrade):
        """
        Bar Main Upgrade.
        """
        def __init__(self, name="Bar", instance=None, desc="Serve drinks and snacks to your customers!", img="content/buildings/upgrades/bar.jpg", build_effort=0, materials=None, in_slots=3, cost=500, **kwargs):
            super(Bar, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set(["Waitress"])
            self.workable = True
            
            
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
            
