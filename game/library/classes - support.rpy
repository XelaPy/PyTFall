# Support classes

init -9 python:
    ######## Game logic classes ########
    class PyTFallWorld(_object):
        '''This class will guide all AI/Logic inside of the world that is not controlled by the player.
        This really looks like this should be a function at the moment, but we will add more relevant methods in the future.
        '''
        def __init__(self):
            # Maps
            # self.maps = xml_to_dict(content_path('db/maps.xml'))
            # for key in self.maps:
                # if "attr" in self.maps[key]:
                    # del self.maps[key]["attr"]
            self.map_pattern = "content/gfx/bg/locations/map_buttons/gismo/"
            self.maps = OnScreenMap()
            
            # GUI
            self.city_dropdown = False
            self.it = None  # Items Transfer
            self.sm = SlaveMarket()
            self.hp = GuiHeroProfile()
            # self.gs = GuiGirlsList()
            
            # Teams
            # self.pt = Team(implicit = [hero])
            
            # Exploration
            # self.tiles = load_tiles()
            # self.forest_1 = object()
            
            # Events:
            self.world_events = WorldEventsManager(world_events)
            
            # Quests:
            self.world_quests = WorldQuestManager(world_quests)
            
            # Actions:
            self.world_actions = WorldActionsManager()
            
            # Runaways:
            self.ra = RunawayManager()
            
            # We use this for the message in the main screen:
            self.temp_text = list() # We add reports from the game here, that don't fit in the next day reports.
            self.ms_text = ""
            self.show_text = False
            self.todays_first_view = True
            
        def init_shops(self):
            # Shops:
            self.shops = ['General Store', 'Cafe', 'Work Shop', 'Witches Hut', 'Tailor Store']
            self.general_store = GeneralStore('General Store', 18, ['General Store'])
            self.cafe = ItemShop('Cafe', 18, ['Cafe'], sells=["food"])
            self.workshop = ItemShop('Work Shop', 18, ['Work Shop'], sells=["armor", "dagger", "fists", "rod", "claws", "sword", "bow"])
            self.witches_hut = ItemShop('Witches Hut', 18, ['Witches Hut'], sells=["amulet", "restore", "smallweapon"])
            self.tailor_store = ItemShop('Tailor Store', 18, ['Tailor Store'], sells=["dress"])
            self.hidden_village_shop = ItemShop("Ninja Tools Shop", 18, ["Ninja Shop"], gold=1000, sells=["armor", "dagger", "fists", "rod", "claws", "sword", "bow", "amulet", "smallweapon", "restore", "dress"], sell_margin=0.85, buy_margin=3.0)
        
        # World AI ----------------------------->
        @staticmethod
        def restore_all_chars():
            """
            Heals, restores AP and MP for non player characters that may have been exposed to world events.
            """
            characters = [girl for girl in chars.itervalues() if girl not in hero.girls]
            
            for girl in characters:
                girl.health = girl.get_max("health")
                girl.mp = girl.get_max("mp")
                girl.vitality = girl.get_max("vitality")
                
                # Resets and Counters
                girl.restore_ap()
                # girl.rt_trait(traits)
                girl.item_counter()
                girl.img_cache = list()
                girl.cache = list()
                for key in girl.effects:
                    if girl.effects[key]['active']:
                        girl.apply_effects(key)
                girl.effects['Food Poisoning']['activation_count'] = 0
                
            # Same for Arena Fighters:
            for fighter in pytfall.arena.arena_fighters:
                fighter.cache = list()
                fighter.health = fighter.get_max("health")
                fighter.mp = fighter.get_max("mp")
                fighter.vitality = fighter.get_max("vitality")
        
        @staticmethod        
        def add_random_girls():
            l = list(girl for girl in chars.values() if girl.__class__ == rChar and not girl.arena_active and girl not in hero.girls)
            amount = randint(45, 60)
            if len(l) < amount:
                for __ in xrange((amount+5) - len(l)):
                    build_rc()
            
        # ----------------------------------------->    
        def next_day(self):
            '''Next day logic for our PyTFall World
            '''
            self.ms_text = ""
            
            # Shops and SlaveMarket:
            self.general_store.next_day()
            self.cafe.next_day()
            self.workshop.next_day()
            self.witches_hut.next_day()
            self.tailor_store.next_day()
            self.sm.next_day()
            self.ra.next_day()
            store.jail.next_day()
            
            # Girlsmeets:
            # Termination:
            cells = gm.girlcells
            for cell in cells.keys():
                if cells[cell].termination_day <= day:
                    del cells[cell]
            
            # Arena:
            self.arena.next_day()
            
            # Girls, Buildings income and Hero:
            for char in chars.values():
                char.next_day()
            
            businesses = [b for b in hero.buildings if isinstance(b, NewStyleUpgradableBuilding)]
            for b in businesses:
                b.nd_log_income()
            
            hero.next_day()
            
            # Restoring world girls:
            self.restore_all_chars()
            if not day%14:
                self.add_random_girls()
                
            # Last we construct the main screen report:
            self.ms_text = "\n".join(self.temp_text)
            self.temp_text = list()
            self.ms_text = self.ms_text + "\n\n"
            self.ms_text = self.ms_text + self.arena.daily_report # Arena*
            self.todays_first_view = True
        
    
    class Difficulties(_object):
        """
        Adjusts gameplay values based on the difficulty setting.
        """
        def __init__(self):
            self.difficulty = "normal"
            
            self.easy = dict()
            self.normal = dict()
            self.hard = dict()
            
            self.easy["income_tax_1000+"] = 5
            self.normal["income_tax_1000+"] = 10
            self.hard["income_tax_1000+"] =  15
        
        def set_difficulty(self, difficulty):
            """
            Sets up difficulty values throughout the game.
            """
            self.difficulty = difficulty
            for i in self.__dict__[difficulty]:
                setattr(self, i, self.__dict__[difficulty][i])
    
    class ListHandler(_object):
        # Most of this class is obsolete at this point of development
        # Note: We should cut it to it's bare minimum and kill it later :)
        def __init__(self):
            self.BrtlUpList = ['bar', 'garden', 'stripclub', 'casinofloor', 'viprooms']
            self.BrtlAdList = ['sign', 'flyers', 'magazine', 'billboard', 'girl', 'celeb']
            self.LocList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'brothel', "-PyTFall Educators-"]
            self.clientCastes = ['None', 'Peasant', 'Merchant', 'Nomad', 'Wealthy Merchant', 'Clerk', 'Noble', 'Royal']
            self.battlestats = ['health', 'mp', 'attack', 'magic', 'defence', 'agility', "luck", "charisma"]
            self.herostats = ['libido', 'constitution', 'reputation', 'fame', 'charisma', 'sex', 'alignment', 'vitality', 'intelligence', 'luck']
            
            # get a list of all battle tracks:
            self.battle_tracks = list()
            path = content_path("sfx/music/be")
            for track in os.listdir(path):
                if track.startswith("battle"):
                    self.battle_tracks.append("/".join([path, track]))
                    
            # Dict for music locations ( :0 )
            self.world_music = dict()
        
    
    class Calendar(object):
        '''
        Cheers to Rudi for mooncalendar calculations.
        '''
        def __init__(self, day=1, month=1, year=1, leapyear=False):
            """
            Expects day/month/year as they are numbered in normal calender.
            If you wish to add leapyear, specify a number of the first Leap year to come.
            """
            self.day = day
            self.month = month - 1
            self.year = year
            if not leapyear:
                self.leapyear = self.year + 4
            else:
                self.leapyear = leapyear
            
            self.daycount_from_gamestart = 0
            
            self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            self.month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                               'August', 'September', 'October', 'November', 'December']
            self.days_count = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            
            self.mooncycle = 29
            self.newmoonday = 1
            
        def game_day(self):
            """
            Returns amount of days player has spent in game.
            Counts first day as day 1.
            """
            return self.daycount_from_gamestart + 1
            
        def string(self):
            return "%s %d %d"%(self.month_names[self.month], self.day, self.year)
            
        def next(self, days=1):
            """
            Next day counter.
            Now supports skipping.
            """
            global day
            self.daycount_from_gamestart += days
            day = self.daycount_from_gamestart + 1
            while days:
                self.day += 1
                days -= 1
                if self.leapyear == self.year and self.month == 1:
                    if self.day > self.days_count[self.month] + 1:
                        self.month += 1
                        self.day = 1
                        self.leapyear += 4
                elif self.day > self.days_count[self.month]:
                    self.month += 1
                    self.day = 1
                    if self.month > 11: 
                        self.month = 0
                        self.year += 1
                        

        def weekday(self):
            '''Returns the name of the current day according to daycount.'''
            daylistidx = self.daycount_from_gamestart % len(self.days)
            return self.days[daylistidx]

        def week(self):
            '''Returns the number of weeks, starting at 1 for the first week.
            '''
            weekidx = self.daycount_from_gamestart / len(self.days)
            return weekidx + 1

        def lunarprogress(self):
            '''Returns the progress in the lunar cycle since new moon as percentage.
            '''
            newmoonidx = self.newmoonday - 1
            dayidx = self.daycount_from_gamestart - newmoonidx
            moonidx = dayidx % self.mooncycle
            moondays = moonidx + 1
            percentage = moondays * 100.0 / self.mooncycle
            return int(round(percentage))

        def moonphase(self):
            '''Returns the lunar phase according to daycount.

            Phases:
            new moon -> waxing crescent -> first quater -> waxing moon ->
                full moon -> waning moon -> last quarter -> waning crescent -> ...
            '''
            # calculate days into the cycle
            newmoonidx = self.newmoonday - 1
            dayidx = self.daycount_from_gamestart - newmoonidx
            moonidx = dayidx % self.mooncycle
            moondays = moonidx + 1
            # substract the number of named days
            unnamed_days = self.mooncycle - 4
            # calculate the days per quarter
            quarter = unnamed_days / 4.0
            # determine phase
            if moonidx<1:
                phase = "new moon"
            elif moonidx<(quarter+1):
                phase = "waxing crescent"
            elif moonidx<(quarter+2):
                phase = "first quarter"
            elif moonidx<(2*quarter+2):
                phase = "waxing moon"
            elif moonidx<(2*quarter+3):
                phase = "full moon"
            elif moonidx<(3*quarter+3):
                phase = "waning moon"
            elif moonidx<(3*quarter+4):
                phase = "last quarter"
            else:
                phase = "waning crescent"
            return phase

    class NDEvent(_object):
        """Next Day Report. Logs in a single event to be read in next_day label.

        The load_image method will always return the same image. If you want to
        do another search, you have to set the 'img' attribute to 'None'.
        """
        def __init__(self, type='', txt='', img='', char=None, charmod={}, loc=None, locmod={}, red_flag=False, green_flag=False, team=None, **kwargs):
            # describes the type of event
            self.type = type
            # the description of the event
            self.txt = txt
            # information on the event image or a displayable
            self.img = img
            # the character involved in the event (optional)
            self.char = char
            # Team, this overrides char property in the ND reports and is used for team events:
            self.team = team
            # Same as above, just for stats:
            if team:
                self.team_charmod = charmod.copy()
                self.charmod = None
            else:
                # stat changes of a char (optional)
                self.charmod = charmod.copy()
                self.team_charmod = None
            # the location of the event (optional)
            self.loc = loc
            # stat changes of that location (optional)
            self.locmod = locmod.copy()
            
            self.kind = kwargs.get("kind", None)
            
            self.green_flag = green_flag
            self.red_flag = red_flag
            
        def load_image(self):
            """
            Returns a renpy image showing the event.
            
            The image is selected based on the event type and the character.
            """
            
            # select/load an image according to img
            width = 820
            height = 705
            
            size = (width, height)
            d = self.img
            # Try to analyze self.img in order to figure out what it represents:
            if isinstance(d, renpy.display.core.Displayable):
                return d
            if isinstance(d, basestring):
                if not d:
                    raise Exception("Basetring Supplied as img: Ev.type: {}, Ev.loc.name: {}".format(self.type, self.loc.name if self.loc else "Unknown"))
                elif "." in d:
                    return ProportionalScale(d, width, height)
                else:
                    return self.char.show(self.img, resize=size, cache=True)
            devlog.warning("Unknown Image Type: {} Provided to Event (Next Day Events class)".format(self.img))
            return ProportionalScale("content/gfx/interface/images/no_image.png", width, height)
            
            
    class OnScreenMap(_object):
        """
        Loads data from JSON, builds a map.
        To be used with screens.
        It either builds the map from cut out peaces or by placing icons on in.
        """
        def __init__(self):
            in_file = content_path("db/maps.json")
            with open(in_file) as f:
                data = json.load(f)
                
            for i in data:
                setattr(self, i, data[i])
                
        def __call__(self, map):
            return getattr(self, map)
            
        def unlock(self, map, loc):
            for l in self(map):
                if l["id"] == loc:
                    l["hidden"] = False
                    break
            else:
                notify("Could not find location: {} in map: {} to unlock.".format(map, loc))
                
        def appearing(self, map, loc):
            for l in self(map):
                if l["id"] == loc:
                    if l.get("appearing", False):
                        return True
            return False
                
        def lock(self, map, loc):
            for l in self(map):
                if l["id"] == loc:
                    l["hidden"] = True
                    break
            else:
                notify("Could not find location: {} in map: {} to lock.".format(map, loc))
                
    
    # Menu extensions:
    class MenuExtension(_dict):
        """Smarter Dictionary...
        """
        def add_extension(self, ext, matrix):
            self[ext].append(matrix)
            
        def remove_extension(self, ext, name):
            matrix = None
            for m in self[ext]:
                if m[0] == name:
                    matrix = m
                    break
            else:
                devlog.warning("Removal of matrix named: {} from Menu Extensions failed!".format(name))
            if matrix:
                self[ext].remove(matrix)
            
        def build_choices(self, ext):
            choices = []
            for i in self[ext]:
                # check if we have a condition in the matrix (2nd index)
                if len(i) == 3:
                    if eval(i[2]):
                        # We need to remove the second index because screens expects just the two:
                        i = i[:2]
                        choices.append(i)
                else:
                    choices.append(i)
            return choices
