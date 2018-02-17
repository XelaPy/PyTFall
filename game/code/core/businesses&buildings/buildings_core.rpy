init -10 python:
    #################################################################
    # CORE BUILDING CLASSES
    # BaseBuilding = Base class, needed if no other.
    # FamousBuilding = Adds fame and reputation mechanics to the building.
    # BuildingStats = Adds dirt and cleaning to the building.
    # UpgradableBuilding = Adds upgrades  to the building.
    #
    # Examples:
    # class CityJail(Building): <-- Just a building6
    # class Brothel(UpgradableBuilding, BuildingStats, FamousBuilding): <-- A building will upgrade, dirt and fame mechanics.
    #
    """Core order for SimPy jobs loop:
    ***Needs update after restructuring/renaming.

    BUILDING:
        # Holds Businesses and data/properties required for operation.
        run_nd():
            # Setups and starts the simulation.
            *Generates Clients if required.
            *Builds worker lists.
            *Logs the init data to the building report.
            *Runs pre_day for all businesses.
            *Creates SimPy Environment and runs it (run_jobs being the main controlling process)
            *Runs the post_nd.
        building_manager():
            SimPy process that manages the building as a whole.
            # Main controller for all businesses.
            *Builds a list of all workable businesses.
            *Starts business_manager for each building.
        clients_manager():
            SimPy Process that supplies clients to the businesses within the building as required.
            *Adds a steady/conditioned stream of clients to the appropriate businesses and manages that stream:
            *Kicks clients if nothing could be arranged for them.

    BUSINESS:
        # Hold all data/methods required for business to operate.
        *Personal Service:
            - Finds best client match using update.get_workers()
            - Runs the job.
        *Public Service:
            - Simply sends client to business.
            - Sends in Workers to serve/entertain the clients.
        *OnDemand Service:
            - Includes some form of "on demand" service, like cleaning or guarding (defending).
            - May also have a continued, "automatic" service like Guard-patrol.

        *workers = On duty characters.
        *habitable/workable = self-explanotory.
        *clients = clients used locally (maybe useful only for the public service?)
        *capacity = cap of the building such as amount of rooms/workspace.
        *jobs = only for businesses
        *get_workers:
            - Checks if a char is capable.
            - Checks if a char is willing.
            - Can also try to match find the best client for the job.

        # This may be obsolete after refactoring... to be rewritten or deleted after a steady system is in place.
        SimPy Land:
            *res = Resource
            *time = cycle
            *is_running = May be useless

        *Personal Service:
            *find_best_match = finds a best client/worker combination.
            *request_resource:
                - requests a room for worker/client.
                - adds a run_job process to Env
                - logs it all to building log
            *run_job:
                - Waits for self.time delay
                - Calls the job so it can form an NDEvent

        *Public Service:
            *active_workers = Does this not simply double the normal workers?
            *request = plainly adds a client and keeps it in the business based on "ready_to_leave" flag set directly to the client.
            *add_worker:
                # Adds workers to business to serve clients.
                - Checks willingness to do the job.
                - Adds workers as required.
                - self.env.process(self.worker_control(worker)) Possible the most important part, this adds a process to Env.
                - Removes worker from building in order to reserve her for this business
            *run_job:
                # main method/SimPy event that manages the job from start to end.
                - Runs for as long there are active workers
                - Waits for self.time delay
                - Manages clients in the business
            *worker_control:
                # Env Process, manages each individual worker.
                - Runs while there are clients and worker has AP in self.time delays.
                - Logs all active clients as flags to a worker.
                - Logs tips to the worker.
                - Runs the Job once AP had been exhausted or there are no more clients availible.
                - Removes the worker from active workers

    Job:
        Has been completely restructured to server as an object to keep track
        of what character is doing what by direct binding and hosting loose
        functions.
    """


    class BaseBuilding(HabitableLocation, Flags):
        """The super class for all Building logic.
        """
        def __init__(self, id=None, name=None, desc=None,
                     price=100, mod=1, **kwargs):
            """Creates a new building.

            id = The id of the building.
            name = The name of the building.
            desc = The description of the building.
            price = The price of the building.
            mod = The modifier for the building.
            **kwargs = Excess arguments.
            """
            super(BaseBuilding, self).__init__(id=id)
            self.name = name
            self.desc = desc
            self.price = price

            self.jobs = set()
            self.building_jobs = set()

            # Flagging:
            self.flag_red = False
            self.flag_green = False
            self.highlighted = False

            # Rooms
            self.mod = mod

            # Security:
            self.security_rating = 0
            self.security_presence = 0

            self.tier = 0

            # ND Report
            self.txt = ""

        def __str__(self):
            if self.name:
                return str(self.name)
            return super(BaseBuilding, self).__str__()

        def get_price(self):
            # Returns our best guess for price of the Building
            # Needed for buying, selling the building or for taxation.
            # **We may want to take reputation and fame into account as well.
            price = self.price

            if hasattr(self, "_upgrades"):
                for u in self._upgrades:
                    price += u.get_price()
            if hasattr(self, "_businesses"):
                for b in self._businesses:
                    price += b.get_price()
            return price

        def get_workers(self):
            # I may want better handing for this...
            # Returns a list of all chars in heros service that have their workplaces set to this building.
            return [c for c in hero.chars if c.workplace==self and c.is_available]

        def get_all_chars(self):
            all_chars = set()

            for c in hero.chars:
                if not c.is_available:
                    continue
                if c.home == self:
                    all_chars.add(c)
                    continue
                if c.workplace == self:
                    all_chars.add(c)

            return all_chars

        def get_girls(self, action=undefined, occupation=undefined, nott=False):
            """
            The girls that are in this location.
            action = The type of action the girls are doing.
            occupation = The occupation of the girls.
            nott = Whether to negate the selection.

            Note: undefined is used as an alternative to None, as a girl can have no action.
            Used by School, should be refactored out of all modern code now.
            """
            # Get all girls
            if action is undefined:
                g = [girl for girl in hero.chars if girl.location is self]

            # Only get girls that (don't) match action list
            elif isinstance(action, (list,tuple)):
                g = [girl for girl in hero.chars if girl.location is self and (girl.action in action) != nott]

            # Only get girls that are training
            elif action == "Course":
                g = [girl for girl in hero.chars if girl.location is self and isinstance(girl.action, basestring) and girl.action.endswith("Course") != nott]

            # Only get girls with specific action
            else:
                g = [girl for girl in hero.chars if girl.location is self and (girl.action == action) != nott]

            # Get all girls
            if occupation is undefined:
                return g

            # Only get girls that (don't) match occupation list
            elif isinstance(occupation, (list,tuple)):
                return [girl for girl in g if [tr for tr in girl.occupations if tr in occupation] != nott]

            # Only get girls with specific occupation
            else:
                return [girl for girl in g if (occupation in girl.occupations) != nott]


    class FamousBuilding(BaseBuilding):
        """
        A Building that has Fame and Reputation properties.
        """

        def __init__(self, *args, **kwargs):
            """
            Creates a new FamousBuilding.
            minfame = The minimum amount of fame the building can have.
            maxfame = The maximum amount of fame the building can have.
            minrep = The minimum amount of reputation the building can have.
            maxrep = The maximum amount of reputation the building can have.
            """
            super(FamousBuilding, self).__init__(*args, **kwargs)

            self.minfame = kwargs.pop("minfame", 0)
            self.maxfame = kwargs.pop("maxfame", 0)
            self.fame = self.minfame

            self.minrep = kwargs.pop("minrep", 0)
            self.maxrep = kwargs.pop("maxrep", 0)
            self.rep = self.minrep

        def modfame(self, value):
            """
            Changes how famous this building is.
            value = The amount to change.
            """
            if self.fame+value > self.maxfame:
                self.fame = self.maxfame
                return

            if value < 0:
                if self.fame+value < self.minfame:
                    self.fame = self.minfame
                    return

            self.fame += value

        def modrep(self, value):
            """
            Changes how reputable this building is.
            value = The amount to change.
            """
            if self.rep+value > self.maxrep:
                self.rep = self.maxrep
                return

            if value < 0:
                if self.rep+value < self.minrep:
                    self.rep = self.minrep
                    return

            self.rep += value


    class BuildingStats(_object):
        """
        A building that has stats (dirt/security) and underlying mechanics.
        """

        DIRT_STATES = dict(Immaculate=(0, 10), Sterile=(10, 20),
                           Spotless=(20, 30), Clean=(30, 40),
                           Tidy=(40, 50), Messy=(50, 60),
                           Dirty=(60, 70), Grimy=(70, 80),
                           Filthy=(80, 90), Disgusting=(90, 100))

        def __init__(self):
            """
            Creates a new BuildingStats.
            # sq_meters = The m^2 that each room takes up.
            """
            self.stats = {"dirt": 0, "threat": 0}
            self.max_stats = {"dirt": 1000, "threat": 1000}
            self.auto_clean = False

        def __setattr__(self, key, value):
            stats = self.__dict__.get("stats", {})
            if key in stats:
                max_val = self.__dict__["max_stats"][key]
                if value > max_val:
                    stats[key] = max_val
                elif value < 0:
                    stats[key] = 0
                else:
                    stats[key] = value
            else:
                super(BuildingStats, self).__setattr__(key, value)

        def __getattr__(self, item):
            stats = self.__dict__.get("stats", {})
            if item in stats:
                return stats[item]
            raise AttributeError("%s object has no attribute named %r" %
                                (self.__class__.__name__, item))

        def get_cleaning_price(self):
            """
            How much it costs to clean this building.
            """
            dirt = self.dirt
            price = 10 + dirt + dirt
            return round_int(price)

        def get_dirt_percentage(self):
            """
            Returns percentage of dirt in the building as (percent, description).
            """
            if self.dirt < 0:
                self.dirt = 0
            dirt = self.dirt * 100 / self.max_stats["dirt"]
            if dirt > 100:
                dirt = 100

            dirt_string = ""
            for key in self.DIRT_STATES:
                if dirt >= self.DIRT_STATES[key][0] and dirt <= self.DIRT_STATES[key][1]:
                    dirt_string = key

            if not dirt_string:
                raise Exception, "No valid string for dirt percentage of %s was found!" % self.id

            return round_int(dirt), dirt_string

        def clean(self, value):
            result = self.dirt + value
            self.dirt = result
            if config.debug and self.env:
                devlog.info("{}: Clean Function: result: {}, self.dirt: {}".format(self.env.now, result, self.dirt))


    class AdvertableBuilding(_object):
        def add_adverts(self, adverts):
            self._adverts = adverts

            for adv in self._adverts:

                adv['active'] = False

                if not 'price' in adv:
                    adv['price'] = 0

                if not 'upkeep' in adv:
                    adv['upkeep'] = 0

        @property
        def adverts(self):
            return self._adverts

        @property
        def can_advert(self):
            return len(self._adverts) != 0

        def toggle_advert(self, advert):
            """
            toggle advertation, returns whether it worked
            """

            if self._adverts[advert]['active']:
                self._adverts[advert]['active'] = False
                return True

            if hero.gold < advert['price'] + advert['upkeep']:
                return False

            self._adverts[advert]['active'] = True
            return True

        def advertising(self, advert):
            return self._adverts[advert]['active']

        def use_adverts(self):
            """Whether this building has any adverts.
            """
            return len(self._adverts) > 0


    class UpgradableBuilding(BaseBuilding):
        def __init__(self, *args, **kwargs):
            """
            @ Last review:
            Alex: I've moved everything except adverts and methods from Building class here.
            """
            super(UpgradableBuilding, self).__init__(*args, **kwargs)
            self._upgrades = list()
            self.allowed_upgrades = []
            self._businesses = list()
            self.allowed_businesses = []

            # And new style upgrades:
            self.in_slots = 0 # Interior Slots
            self.in_slots_max = kwargs.pop("in_slots_max", 100)
            self.ex_slots = 0 # Exterior Slots
            self.ex_slots_max = kwargs.pop("ex_slots_max", 100)

            # We keep maximum amounts of workers of specific types that this business can hold in this dict.
            # They are kept as k/v pairs of Job(): amount.
            # If absent for any job available at the building, we assume that worker can be added endlessly.
            self.worker_slots_max = {}

            # BAD Code?, right now all jobs are kept in .jobs attribute...
            # if this is not a useful distinction, we remove this and just work with the jobs set.
            if hasattr(self, "building_jobs"):
                self.building_jobs = self.building_jobs.union(self.building_jobs)

            if kwargs.get("needs_management", False):
                self.add_job(simple_jobs["Manager"])
                self.worker_slots_max[simple_jobs["Manager"]] = 1
                self.normalize_jobs()

            # Clients:
            self.all_clients = set() # All clients of this building are maintained here.
            self.regular_clients = set() # Subset of self.all_clients.
            self.clients = set() # Local clients, this is used during next day and reset on when that ends.

            # Chars:
            # Note: We also use .inhabitants set inherited from all the way over location.
            self.manager = None
            self.manager_effectiveness = 0
            self.all_workers = list() # All workers presently assigned to work in this building.
            self.available_workers = list() # This is built and used during the next day.

            # Upgrades:
            self.nd_ups = list() # Upgrades active during the next day...

            # SimPy and etc follows:
            self.env = None
            # self.maxrank = kwargs.pop("maxrank", 0) # @Useless property...

            self.logged_clients = False
            # This is the amount of clients that will visit the brothel,
            # this is set by get_client_count method.
            self.total_clients = 0
            self.mod = 1

            self.fin = Finances(self)

        def get_client_count(self, write_to_nd=False):
            """Get the amount of clients that will visit the brothel the next day.
            """

            if not (self.fame or self.rep or any(a['name'] == 'Sign' and a['active'] for a in self.adverts)):
                if write_to_nd:
                    self.log("{}".format(set_font_color("Noone came to your unknown establishment that doesn't have as much as a sign!", "red")))
                    self.flag_red = True
                return 0

            clients = self.baseclients*round_int(self.mod*1.5)
            if write_to_nd:
                self.log("{} clients came to brothel just because its there!".format(set_font_color(clients, "green")))

            if config.debug:
                debug_add = 10
                if write_to_nd:
                    self.log("Debug Mode adding {} clients!".format(set_font_color(debug_add, "red")))
                clients = clients + debug_add

            # Generated by upgrades:
            for u in [u for u in self._businesses if u.workable]:
                temp = u.get_client_count()
                if write_to_nd and config.debug:
                    self.log("Debug: {} upgrade is adding {} clients!".format(u.name, set_font_color(temp, "red")))
                clients = clients + temp

            add_clients = int(self.fame*0.2)
            if add_clients and write_to_nd:
                self.log("{} clients came due to {} renoun!".format(add_clients, self.name))
            clients = clients + add_clients

            self.total_clients = clients if clients > 0 else 0

        def log(self, item, add_time=False):
            # Logs the item (text) to the Building log...
            if add_time and self.env:
                item = "{}: ".format(self.env.now) + item
            self.nd_events_report.append(item)
            if config.debug and True:
                devlog.info(item)

        def add_job(self, job):
            # Adds Job to the BUILDING! and normalizes it.
            self.building_jobs.add(job)
            self.normalize_jobs()

        def normalize_jobs(self):
            self.jobs = self.jobs.union(self.building_jobs)
            for up in self._businesses:
                self.jobs = self.jobs.union(up.jobs)

        def get_valid_jobs(self, char):
            """Returns a list of jobs available for the building that the character might be willing to do.

            Returns an empty list if no jobs is available for the character.
            """
            jobs = []

            for job in self.jobs:
                # We need to check if there are any slots for a worker are left:
                if job in self.worker_slots_max:
                    # we get a list of all workers that are assigned for this job:
                    temp = [w for w in self.all_workers if w.action == job or w.previousaction == job]
                    # This isn't bulletproof... we prolly want to access building.manager here...
                    if len(temp) >= self.worker_slots_max[job]:
                        continue
                if job.is_valid_for(char):
                    jobs.append(job)

            return jobs

        # Building of Upgrades:
        # This should be part of the main BUILDING!!! (So it's this one :) )
        def check_resources(self, upgrade):
            # checks if the player has enough resources to build an upgrade:
            return True

        def check_space(self, upgrade):
            # Checks if the main building has enough space to add this upgrade:
            return True

        def start_construction(self, upgrade):

            # Take the metarials (if we got here, it is assumed that player has enough of everything)
            for r in upgrade.MATERIALS:
                pass

            # Cash...
            hero.take_money(upgrade.cost, "Building Upgrades")

            # adds the upgrade to in construction buildings:
            self.in_construction_upgrades.append(upgrade)

        def get_extension_cost(self, extension, **ec_kwargs):
            # We figure out what it would take to add this extension (building or business)
            # using it's class attributes to figure out the cost and the materials required.
            tier = self.tier or 1

            if inspect.isclass(extension):
                ext = extension(**ec_kwargs)
            else:
                ext = extension
            if ext.building is None:
                ext.building = self

            cap = ext.capacity

            cost = ext.cost * tier
            cost += cap*ext.exp_cap_cost

            materials = ext.materials.copy()
            for k, v in materials.items():
                materials[k] = round_int(v*min(tier, 4))

            in_slots = ext.in_slots + cap*ext.exp_cap_in_slots
            ex_slots = ext.ex_slots * cap*ext.exp_cap_ex_slots

            return cost, materials, in_slots, ex_slots

        def eval_extension_build(self, extension_class, price=None):
            # If price is not None, we expect a tuple with requirements to build
            # Check if we can build an upgrade:
            if price is None:
                cost, materials, in_slots, ex_slots = self.get_extension_cost(extension_class)
            else:
                cost, materials, in_slots, ex_slots = price

            if (self.in_slots_max - self.in_slots) < in_slots or (self.ex_slots_max - self.ex_slots) < ex_slots:
                return False

            if self.has_extension(upgrade):
                return False

            if hero.gold < cost:
                return False

            for i, a in materials.iteritems():
                if hero.inventory[i] < a:
                    return False

            return True

        def add_business(self, business, normalize_jobs=True):
            """Add business to the building.
            """
            cost, materials, in_slots, ex_slots = self.get_extension_cost(business)
            self.in_slots += in_slots
            self.ex_slots += ex_slots

            business.building = self
            self._businesses.append(business)
            self._businesses.sort(key=attrgetter("SORTING_ORDER"), reverse=True)

            if normalize_jobs:
                self.normalize_jobs()

        def add_upgrade(self, upgrade):
            cost, materials, in_slots, ex_slots = self.get_extension_cost(upgrade)
            self.in_slots += in_slots
            self.ex_slots += ex_slots

            upgrade.building = self
            self._upgrades.append(upgrade)
            self._upgrades.sort(key=attrgetter("SORTING_ORDER"), reverse=True)

        def all_possible_extensions(self):
            # Returns a list of all possible extensions (businesses and upgrades)
            return self.allowed_businesses + self.allowed_upgrades

        def all_extensions(self):
            return self._businesses + self._upgrades

        def has_extension(self, extension, include_business_upgrades=False):
            if not inspect.isclass(extension):
                extension = extension.__class__

            for ex in self.all_extensions():
                if isinstance(ex, extension):
                    return True

            if include_business_upgrades:
                for ex in self.all_extensions():
                    if ex.has_extension(extension):
                        return True

            return False

        def get_business(self, up):
            # Takes a string as an argument
            if up == "fg":
                temp = [u for u in building._businesses if u.__class__ == ExplorationGuild]
                if temp:
                    return temp[0]
                else:
                    return False

        def convert_AP(self, worker):
            worker.jobpoints = worker.AP*100
            worker.AP = 0

        @property
        def habitable(self):
            # Overloads property of Location core class to serve the building.
            return any(i.habitable for i in self._businesses)

        @property
        def vacancies(self):
            # check if there is place to live in this building.
            if not self.habitable:
                return 0

            habitable = [i for i in self._businesses if i.habitable]
            capacity = sum([i.capacity for i in habitable])
            rooms = capacity - len(self.inhabitants)
            if rooms < 0:
                rooms = 0
            return rooms

        @property
        def workable(self):
            """Returns True if this building has upgrades that are businesses.
            """
            return any(i.workable for i in self._businesses)

        @property
        def expects_clients(self):
            return any(i.expects_clients for i in self._businesses)

        # SimPy:
        def run_nd(self):
            """This method is ran for buildings during next day
            - Gets list of workable businesses and available workers
            - Creates SimPy Environment
            """
            tl.timer("Temp Jobs Loop")
            # Setup and start the simulation
            self.flag_red = False

            self.log(set_font_color("===================", "lawngreen"))
            self.log("{}".format(set_font_color("Starting the simulation:", "lawngreen")))
            self.log("--- Testing {} Building ---".format(set_font_color(self.name, "lawngreen")))

            # All workers and workable businesses:
            self.available_workers = list(c for c in self.all_workers if
                                          c.is_available and
                                          c.workplace == self and
                                          c.action in self.jobs)
            for w in self.all_workers:
                self.convert_AP(w)

            # Get businesses we wish SimPy to manage! business_manager method is expected here.
            self.nd_ups = list(up for up in self._businesses if up.workable)

            # Clients:
            tl.timer("Generating clients")
            self.get_client_count(write_to_nd=True)
            clnts = self.total_clients
            # TODO B&B-clients: Generate and add regulars!
            # ALSO: We at the moment randomly pick a business for a client to like, that may need to be adjusted.
            if self.available_workers and len(self.all_clients) < clnts:
                if self.nd_ups:
                    for i in xrange(clnts - len(self.all_clients)):
                        if dice(80):
                            self.all_clients.add(build_client(likes=[choice(self.nd_ups)]))
                        else:
                            self.all_clients.add(build_client(gender="female", likes=[choice(self.nd_ups)]))
            self.clients = self.all_clients.copy()
            self.log("Total of {} clients are expected to visit this establishment!".format(set_font_color(len(self.clients), "lawngreen")))
            tl.timer("Generating clients")

            # Create an environment and start the setup process:
            self.env = simpy.Environment()
            for up in self._businesses:
                up.pre_nd()

            self.env.process(self.building_manager(end=101))
            self.env.run(until=101) # 101 will run events at 100 which it is more intuitive to manage.
            self.log("{}".format(set_font_color("Ending the simulation:", "red")))

            # We can run it for a bit more, as matrons option!?!
            # self.env.run(until=110)
            # self.log("{}".format(set_font_color("Ending the second stage of simulation:", "red")))

            self.log("\nA total of {} Gold was earned here today!".format(set_font_color(str(self.fin.get_logical_income()), "red")))
            self.log("{}".format(set_font_color("===================", "red")))
            self.log("\n\n")
            tl.timer("Temp Jobs Loop")

            self.post_nd_reset()

        def building_manager(self, end=100):
            """This is the main process that manages everything that is happening in the building!
            """
            # TODO B&B-clients: Improve the function and add possibilities for "Rush hours"
            for u in self.nd_ups:
                # Trigger all public businesses:
                if not u.active: # building is not active:
                    self.env.process(self.inactive_process())
                else: # Business as usual:
                    self.env.process(u.business_control())

                if u.has_workers():
                    u.is_running = True

            if self.expects_clients:
                self.env.process(self.clients_dispatcher(end=end))

            while 1:
                yield self.env.timeout(100)

        def clients_dispatcher(self, end=100):
            """This method provides stream of clients to the building following it's own algorithm.
            """
            # TODO B&B-clients: This can plainly be done better... i ii iii
            i = 0
            ii = 0
            if self.clients and len(self.clients) > 60:
                iii = randint(3, len(self.clients)/20)
            else:
                iii = 0

            while self.clients and self.nd_ups:
                if ii > iii:
                    delay = randint(1, 3)
                    yield self.env.timeout(delay)
                    # Ensure a steady stream if clients:
                    ii = 0
                    if len(self.clients) > end - self.env.now:
                        iii = (len(self.clients) / (end - self.env.now))
                i += 1
                ii += 1
                client = self.clients.pop()
                self.env.process(self.client_manager(client))

        def client_manager(self, client):
            """Manages a client using SimPy.

            - Picks a business
            - Tries other businesses if the original choice fails
            - Kicks the client if all fails

            So this basically sends the client into the businesses within this building or keeps them waiting/rotating.
            Once in, client is handled and managed by the Business itself until control is returned here!
            Once this method is terminated, client has completely left the building!
            """
            # Register the fact that client arrived at the building:
            temp = '{} arrives at the {}.'.format(client.name, self.name)
            self.log(temp, True)

            if self.dirt >= 800:
                yield self.env.timeout(1)
                temp = "Your building is as clean a pig stall. {} storms right out.".format(client.name)
                self.log(temp)
                self.env.exit()
            if self.threat >= 800:
                yield self.env.timeout(1)
                temp = "Your building is as safe as a warzone. {} runs away from it.".format(client.name)
                self.log(temp)
                self.env.exit()

            # Visit counter:
            client.up_counter("visited_building" + str(self.id))

            # Prepare data:
            # @Review: This is wrong as not every business deals with clients...
            businesses = [b for b in self.nd_ups if not isinstance(b, (TaskBusiness,
                                                                       OnDemandBusiness))]
            shuffle(businesses)

            fav_business = client.likes.intersection(self._businesses)

            if not fav_business: # Case where clients fav business was removed from the building, client to react appropriately.
                self.all_clients.remove(client)
                temp = "{}: {} storms out of the building pissed off as his favorite business was removed!".format(self.env.now, client.name)
                self.log(temp)
                self.env.exit()
            else:
                fav_business = fav_business.pop()

            visited = 0 # Amount of businesses client has successfully visited.
            while businesses: # Manager effects should be a part of this loop as well!
                # Here we pick an upgrade if a client has one in preferences:
                if not visited and fav_business in businesses:
                    # On the first run we'd want to pick the clients fav.
                    business = fav_business
                    businesses.remove(business)
                else:
                    business = businesses.pop()

                # Matron case:
                # Wait for the business to open in case of a favorite:
                if self.manager and business == fav_business:
                    timer = 0
                    if business.res.count < business.capacity:
                        while timer < 7 and business.res.count < business.capacity: # Max wait time
                            timer += 1
                            yield self.env.timeout(1)

                if business.type == "personal_service" and business.res.count < business.capacity:
                    # Personal Service (Brothel-like):
                    job = business.job
                    workers = business.get_workers(job, amount=1, match_to_client=client)

                    if not workers:
                        continue # Send to the next update.
                    else:
                        # We presently work just with the one char only, so:
                        worker = workers.pop()
                        if worker in self.available_workers:
                            self.available_workers.remove(worker)

                        # We bind the process to a flag and wait until it is interrupted:
                        visited += 1
                        self.env.process(business.request_resource(client, worker))
                        client.set_flag("jobs_busy")
                        while client.flag("jobs_busy"):
                            yield self.env.timeout(1)

                # Jobs like the Club:
                elif business.type == "public_service" and business.res.count < business.capacity:
                    self.env.process(business.client_control(client))
                    visited += 1
                    client.set_flag("jobs_busy")
                    while client.flag("jobs_busy"):
                        yield self.env.timeout(1)

            if not visited:
                temp = "{}: There is not much for the {} to do...".format(self.env.now, client.name)
                self.log(temp)
                temp = "{}: So {} leaves your establishment cursing...".format(self.env.now, client.name)
                self.log(temp)
                yield self.env.timeout(0) # To make sure this is a generator :)
            else:
                temp = '{}: {} is leaving after visiting {} businesses.'.format(self.env.now, client.name, visited)
                self.log(temp)

        def post_nd_reset(self):
            self.env = None
            self.nd_ups = list()

            for _ in self._businesses:
                _.post_nd_reset()

            for c in self.all_clients:
                for f in c.flags.keys():
                    if f.startswith("jobs"):
                        c.del_flag(f)
