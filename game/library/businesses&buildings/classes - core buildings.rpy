init -9 python:
    #################################################################
    # CORE BUILDING CLASSES
    # Building = Base class, needed if no other.
    # FamousBuilding = Adds fame and reputation mechanics to the building.
    # DirtyBuilding = Adds dirt and cleaning to the building.
    # UpgradableBuilding = Adds upgrades and adverts to the building.
    #
    # Examples:
    # class CityJail(Building): <-- Just a building
    # class TraningDungeon(UpgradableBuilding): <-- A Building that can be upgraded.
    # class Brothel(UpgradableBuilding, DirtyBuilding, FamousBuilding): <-- A building will upgrade, dirt and fame mechanics.
    #
    class Building(Location, Flags):
        """
        The super class for all Building logic.
        """
        def __init__(self, id=None, name=None, desc=None, price=1, minrooms=0, maxrooms=1, roomprice=250, mod=1, **kwargs):
            """
            Creates a new building.
            id = The id of the building.
            name = The name of the building.
            desc = The description of the building.
            price = The price of the building.
            minrooms = The minimum amount of rooms the building can have.
            maxrooms = The maximum amount of rooms the building can have.
            roomprice = The amount each room costs.
            mod = The modifier for the building.
            **kwargs = Excess arguments.
            """
            super(Building, self).__init__()
            self.id = id
            self.name = name
            self.desc = desc
            self.price = price
            self.jobs = set()
            self.building_jobs = set()
            
            # Flagging
            self.flag_red = False
            self.flag_green = False
            self.highlighted = False
            
            # Rooms
            self.rooms = minrooms
            self.minrooms = minrooms
            self.maxrooms = maxrooms
            self.roomprice = roomprice
            self.mod = mod
            
            # Security
            self.security_rating = 0
            self.security_presence = 0
            
            # ND Report
            self.txt = ""
        
        def free_rooms(self):
            """
            The amount of rooms that aren't being used.
            """
            return self.rooms - len(self.get_girls())
        
        def get_girls(self, action=undefined, occupation=undefined, nott=False):
            """
            The girls that are in this location.
            action = The type of action the girls are doing.
            occupation = The occupation of the girls.
            nott = Whether to negate the selection.
            
            Note: undefined is used as an alternative to None, as a girl can have no action.
            """
            # Get all girls
            if action is undefined:
                g = [girl for girl in hero.girls if girl.location is self]
            
            # Only get girls that (don't) match action list
            elif isinstance(action, (list,tuple)):
                g = [girl for girl in hero.girls if girl.location is self and (girl.action in action) != nott]
            
            # Only get girls that are training
            elif action == "Course":
                g = [girl for girl in hero.girls if girl.location is self and girl.action is not None and girl.action.endswith("Course") != nott]
            
            # Only get girls with specific action
            else:
                g = [girl for girl in hero.girls if girl.location is self and (girl.action == action) != nott]
            
            # Get all girls
            if occupation is undefined:
                return g
            
            # Only get girls that (don't) match occupation list
            # TODO: NOT SURE IF THIS IS CORRECT AFTER THE REVIEW!
            elif isinstance(occupation, (list,tuple)):
                return [girl for girl in g if [tr for tr in girl.occupation if tr in occupation] != nott]
            
            # Only get girls with specific occupation
            else:
                return [girl for girl in g if (occupation in girl.occupations) != nott]
        
        def modrooms(self, value):
            """
            Modifies the amount of rooms the dungeon has.
            value = The amount to modify by.
            """
            if value > 0:
                if self.rooms + value > self.maxrooms: self.rooms = self.maxrooms
                else: self.rooms += value
            
            elif self.rooms + value < self.minrooms: self.rooms = self.minrooms
            else: self.rooms -= value
        
        def security_mult(self):
            """
            Get the multiplier caused by security presence.
            """
            return float(self.security_rating) / 1000.0
        
    
    class FamousBuilding(Building):
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
        
    
    class DirtyBuilding(Building):
        """
        A building that has Dirt and Cleaning mechanics.
        """
        
        DIRT_STATES = dict(Immaculate=(0, 10), Sterile=(10, 20), Spotless=(20, 30), Clean=(30, 40), Tidy=(40, 50), Messy=(50, 60), Dirty=(60, 70), Grimy=(70, 80), Filthy=(80, 90), Disgusting=(90, 100))
        
        def __init__(self, *args, **kwargs):
            """
            Creates a new DirtyBuilding.
            sq_meters = The m^2 that each room takes up.
            """
            super(DirtyBuilding, self).__init__(*args, **kwargs)
            
            self.dirt = 0
            self.auto_clean = False
            self.sq_meters = kwargs.pop("sq_meters", 0)
        
        def get_max_dirt(self):
            """
            The total amount of dirt this building can have.
            """
            rooms = float(self.rooms) / self.maxrooms
            return int(self.sq_meters*0.8*rooms)
        
        def get_dirt(self):
            """
            The amount of dirt this building has.
            """
            if self.dirt > self.get_max_dirt():
                return self.get_max_dirt()
            
            else:
                return self.dirt
        
        def get_cleaning_price(self):
            """
            How much it costs to clean this building.
            """
            dirt = self.get_dirt()
            price = 10 + dirt + dirt
            return int(round(price))
        
        def get_dirt_percentage(self):
            """
            Returns percentage of dirt in the building as (percent, description).
            """
            dirt = self.dirt * 100 / self.get_max_dirt()
            if dirt > 100:
                dirt = 100
            
            dirt_string = ""    
            for key in self.DIRT_STATES:
                if dirt >= self.DIRT_STATES[key][0] and dirt <= self.DIRT_STATES[key][1]:
                    dirt_string = key
            
            if not dirt_string:
                raise Error, "No valid string for dirt percentage of %s was found!" % self.id
            
            return int(round(dirt)), dirt_string
        
        def clean(self, value):
            """
            Cleans the building of the given amount of dirt.
            value = The amount to clean.
            """ 
            if self.dirt > self.get_max_dirt():
                self.dirt = self.get_max_dirt()
            
            if self.dirt - value > 0:
                self.dirt -= value
            
            elif self.dirt - value <= 0:
                self.dirt = 0
        
    
    class UpgradableBuilding(Building):
        """
        An extension to Buildings that allows them to be upgradable.
        """
        # The flag for an upgrade that increases the room price
        ROOM_UPGRADE = "room_upgrade"
        
        # The flag for an upgrade that increases the security rating
        SECURITY_UPGRADE = "security_bonus"
        
        # The flag for an upgrade that increases the whore cost.
        WHORE_MULTIPLIER = "whore_mult"
        
        def __init__(self, *args, **kwargs):
            """
            Creates the necessary data for building information.
            """
            super(UpgradableBuilding, self).__init__(*args, **kwargs)
            
            self.upgrade_slots = kwargs.pop("upgrade_slots", 0)
            self.upgrades = OrderedDict()
            self.used_upgrade_slots = 0
            
            self.adverts = OrderedDict()
            
            # Runaway Manager modifier for runaway chances.
            self.security_upgrade_tree = kwargs.pop("sutree", "Security")
        
        def get_room_price(self):
            """
            Get the price of a new room.
            """
            return self.roomprice * self.mod + self.get_upgrade_flag("room_upgrade")
        
        def get_upgrade_flag(self, name):
            """
            Gets the total of a specific flag for those upgrades that are active.
            name = The name of the flag.
            """
            f = 0
            for i in self.upgrades:
                i = self.upgrades[i]
                for j in i:
                    if name in i[j] and i[j]["active"]: f += i[j][name]
            
            return f
        
        def get_upgrade_mod(self, name):
            """
            Gets the modifier for the upgrades.
            name = The name of the group.
            """
            if name not in self.upgrades: return 0
            
            f = 0
            for i in xrange(1, len(self.upgrades[name])+1):
                if self.has_upgrade(name, i): f += 1
            
            return f
        
        def get_upgrade_price(self, dict):
            """
            Get the price to upgrade the location.
            dict = The upgrade to price.
            """
            if "room_dependant" in dict:
                return dict["price"] + dict["price"]/10*self.rooms
            
            else:
                return dict["price"] * self.mod
        
        def gui_security_bar(self):
            """
            Returns a tuple of (Show security bar, Max value).
            """
            return [len(self.get_girls("Guard")) > 0, 20 + self.get_upgrade_flag("security_bonus")]
        
        def has_upgrade(self, name, index):
            """
            Gets whether an upgrade is installed or not.
            name = The name of the group.
            index = The index or name of upgrade.
            """
            if name in self.upgrades:
                up = self.upgrades[name]
                
                if isinstance(index, int):
                    for i in up:
                        if up[i]["id"] == index:
                            return up[i]["active"]
                    
                    else:
                        return False
                
                else:
                    if index in up:
                        return up[index]["active"]
                    
                    else:
                        for i in up:
                            if up[i]["name"] == index:
                                return up[i]["active"]
                        
                        else:
                            return False
            
            else:
                return False
        
        def init(self):
            """
            Activate any upgrades from plain properties in the instance, then remove them.
            Meant for json completion.
            """
            for key in self.upgrades:
                if hasattr(self, key):
                    amount = getattr(self, key)
                    
                    for ukey in self.upgrades[key]:
                        if self.upgrades[key][ukey]["id"] <= amount: self.upgrades[key][ukey]['available'] = True
                    
                    delattr(self, key)
        
        @property
        def use_adverts(self):
            """
            Whether this building has any adverts.
            """
            return len(self.adverts) > 0
        
        @property
        def use_upgrades(self):
            """
            Whether this building has any upgrades.
            """
            return len(self.upgrades) > 0
        
    class NewStyleUpgradableBuilding(Building):
        def __init__(self, *args, **kwargs):
            """
            @ Last review:
            Alex: I've moved everything except adverts and methods from Brothel class here.
            Soon Brothel class needs to die off...
            """
            super(NewStyleUpgradableBuilding, self).__init__(*args, **kwargs)
            self._upgrades = list() #  New style Upgrades!
            
            # And new style upgrades:
            self.in_slots = 100 # Interior Slots
            self.ex_slots = 100 # Exterior Slots
            
            if hasattr(self, "building_jobs"):
                self.building_jobs = self.building_jobs.union(self.building_jobs)
                
            # Clients:
            self.all_clients = set() # All clients of this building are maintained here.
            self.regular_clients = set() # Subset of self.all_clients.
            self.clients = set() # Local clients, this is used during next day and reset on when that ends.
            # Chars:
            self.chars = list() # All Workers...
                
            # SimPy and etc follows (L33t stuff :) ):
            self.env = None
            self.maxrank = kwargs.pop("maxrank", 0) # @Useless property...
            
            self.logged_clients = False
            self.mod = 1
            
            self.fin = Finances(self)
            
        def run_nd(self):
            tl.timer("Temp Jobs Loop")
            # Setup and start the simulation
            self.flag_red = False
            # self.clients = nd_clients
            
            self.log("\n\n")
            self.log(set_font_color("===================", "lawngreen"))
            self.log("{}".format(set_font_color("Starting the simulation:", "lawngreen")))
            self.log("--- Testing {} Building ---".format(set_font_color(self.name, "lawngreen")))
            
            clnts = self.get_client_count(write_to_nd=True)
            # TODO: Generate and add regulars!
            if len(self.all_clients) < clnts:
                for i in xrange(clnts - len(self.all_clients)):
                    self.all_clients.add(build_client())
            self.clients = self.all_clients.copy() # should be union with samples from regulars in the future.
            self.log("Total of {} clients are expected to visit this establishment!".format(set_font_color(len(self.clients), "lawngreen")))
            
            # All workers:
            self.chars = list(g for g in hero.girls if g.location == self)
            
            # Create an environment and start the setup process:
            self.env = simpy.Environment()
            for up in self._upgrades:
                up.run_nd()
            
            # store.env = self.env
            
            self.env.process(self.setup(end=100))
            self.env.run(until=100)
            self.log("{}".format(set_font_color("Ending the First Stage:", "red")))
            self.env.run(until=110)
            self.log("{}".format(set_font_color("Ending the simulation:", "red")))
            self.log("{}".format(set_font_color("===================", "red")))
            self.log("\n\n")
            tl.timer("Temp Jobs Loop")
            
            self.post_nd_reset()
            
        def get_client_count(self, write_to_nd=False):
            """
            Get the amount of clients that will visit the brothel the next day.
            """
            
            if not self.fame and not self.rep and not self.adverts['sign']['active']:
                if write_to_nd:
                    self.log("{}".format(set_font_color("Noone came to your unknown establishment that doesn't have as much as a sign!", "red")))
                    self.flag_red = True
                return 0
            
            clients = self.baseclients*int(round(self.mod*1.5))
            if write_to_nd:
                self.log("{} clients came to brothel just because its there!".format(set_font_color(clients, "green")))
            
            if config.debug:
                debug_add = 10
                if write_to_nd:
                    self.log("Debug Mode adding {} clients!".format(set_font_color(debug_add, "red")))
                clients = clients + debug_add
            
            # Generated by upgrades:
            # TODO: Generate a special return in write_to_nd mode?
            for u in [u for u in self._upgrades if u.workable]:
                temp = u.get_client_count()
                if write_to_nd and config.debug:
                    self.log("Debug: {} upgrade is adding {} clients!".format(u.name, set_font_color(temp, "red")))
                clients = clients + temp
            
            add_clients = int(self.fame*0.2)
            if add_clients and write_to_nd:
                self.log("{} clients came due to {} renoun!".format(add_clients, self.name))
            clients = clients + add_clients
                
                # Adding bonuses for girls in this brothel
                # TODO: Review the code below:
                # gfamebonus = 0
                # for girl in self.get_girls(["Guard", "AutoRest", "Rest"], True): gfamebonus += 1 + int(girl.fame/20)
                # if not self.logged_clients and gfamebonus:
                    # self.txt += "and another %d attracted by your girlz :) \n" % gfamebonus
                
               #  clients = clients + gfamebonus
               
            #TODO: Add girl's customer-magnet traits.
            if clients > 0:
                return clients
            else:
                return 0
            
        def log(self, item):
            # Logs the text to log...
            self.nd_events_report.append(item)
            
        def normalize_jobs(self):
            self.jobs = self.jobs.union(self.building_jobs)
            for up in self._upgrades:
                self.jobs = self.jobs.union(up.jobs)
                
        def can_add_upgrade(self, upgrade, build=False):
            # Check if building has enough space to add this upgrade
            if self.in_slots < upgrade.in_slots or self.ex_slots < self.ex_slots:
                return
                
            # Check is there is already this type of an upgrade:
            if list(up for up in self.upgrades if up.__class__ == upgrade.__class__):
                return
                
            # If we want to build the upgrade as well:
            if build:
                self.add_upgrade(upgrade)
                self.normalize_jobs()
                
            return True
                
        def add_upgrade(self, upgrade):
            """
            Add upgrade to the building.
            """
            upgrade.instance = self
            self._upgrades.append(upgrade)
            
        @property
        def habitable(self):
            """
            Returns True if this buildings has upgrades with free living space.
            """
            return any(i.habitable for i in self._upgrades)
            
        @property
        def workable(self):
            """
            Returns True if this building has upgrades that are businesses.
            """
            return any(i.workable for i in self._upgrades)
            
        # SimPy:
        def kick_client(self, client):
            """
            Gets rid of this client...
            """
            temp = "There is not much for the {} to do...".format(client.name)
            self.log(temp)
            yield self.env.timeout(1)
            temp = "So {} leaves the hotel cursing...".format(client.name)
            self.log(temp)
            
        def setup(self, end=40):
            upgrades = list(up for up in self._upgrades if up.workable)
            i = 0
            while self.clients:
                if self.env.now + 5 <= end: # This is a bit off... should we decide which action should be taken first?
                    if i > 4:
                        yield self.env.timeout(random.randint(1, 3))
                    i += 1
                    store.client = self.clients.pop()
                    store.client.name = "Client {}".format(i)
                    
                    # Register the fact that client arrived at the building:
                    temp = '{} arrives at the {} at {}.'.format(client.name, self.name, self.env.now)
                    self.log(temp)
                    
                    # Take an action!
                    ups = upgrades[:]
                    shuffle(ups)
                    for upgrade in ups:
                        # TODO: Brothel block check needs to be worked out of here.
                        if isinstance(upgrade, BrothelBlock) and upgrade.res.count < upgrade.capacity and upgrade.has_workers():
                            # Assumes a single worker at this stage... This part if for upgrades like Brothel.
                            if upgrade.requires_workers():
                                char = None
                                while self.chars: 
                                    
                                    # Here we should attempt to find the best match for the client!
                                    char = upgrade.get_workers()
                                    
                                    if not char:
                                        break
                                   
                                    # First check is the char is still well and ready:
                                    if not check_char(char):
                                        if char in self.chars:
                                            self.chars.remove(char)
                                        temp = set_font_color('{} is done with this job for the day.'.format(char.name), "aliceblue")
                                        self.log(temp)
                                        continue
                                    
                                    if hasattr(char.action, "id"): # TODO: MAKE DAMN SURE NO CHAR WITHOUT ACTION MAKES IT THIS FAR!
                                        # We to make sure that the girl is willing to do the job:
                                        temp = char.action.id
                                        if not char.action.check_occupation(char):
                                            if char in self.chars:
                                                self.chars.remove(char)
                                            temp = set_font_color('{} is not willing to do {}.'.format(char.name, temp), "red")
                                            self.log(temp)
                                            continue
                                    else:
                                        temp = set_font_color('{} char with action: {} made it this far due to bad coding.'.format(char.name, char.action), "red")
                                        self.log(temp)
                                        if char in self.chars:
                                            self.chars.remove(char)
                                        continue
                                        
                                    break # Breaks the while loop.
                            
                                if char:
                                    if char in self.chars:
                                        self.chars.remove(char)
                                    store.client = client
                                    self.env.process(upgrade.request(client, char))
                                    break
                                else:
                                    continue
                        # Jobs like the Club:
                        elif isinstance(upgrade, StripClub) and upgrade.res.count < upgrade.capacity:
                            self.env.process(upgrade.request(client))
                            break
                            
                    else: # If nothing was found, kick the client:
                        self.env.process(self.kick_client(client))
                else:
                    break
            
        def post_nd_reset(self):
            self.env = None
            
            for _ in self._upgrades:
                _.post_nd_reset()
