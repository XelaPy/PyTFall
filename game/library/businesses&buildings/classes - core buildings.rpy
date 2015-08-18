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
    class Building(Location):
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
            self.id = id
            self.name = name
            self.desc = desc
            self.price = price
            self.jobs = set()
            self.building_jobs = set()
            
            # Flagging
            self.flags = Flags()
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
        
        def set_flag(self, par, value=True):
            """
            Sets a flag for this building.
            par = The flag.
            value = The value.
            """
            self.flags.set_flag(par, value)
        
        def has_flag(self, par):
            """
            Whether this building as a flag.
            par = The flag.
            """
            return self.flags.has_flag(par)
        
        def del_flag(self, par):
            """
            Deletes a flag from this building.
            par = The flag.
            """
            self.flags.del_flag(par)
        
        def flag(self, par):
            """
            Returns a flag for this building.
            par = The flag.
            """
            return self.flags.flag(par)
        
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
            super(NewStyleUpgradableBuilding, self).__init__(*args, **kwargs)
            self._upgrades = list() #  New style Upgrades!
            
            # And new style upgrades:
            self.in_slots = 100 # Interior Slots
            self.ex_slots = 100 # Exterior Slots
            
            if hasattr(self, "building_jobs"):
                self.building_jobs = self.building_jobs.union(self.building_jobs)
                
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
            
