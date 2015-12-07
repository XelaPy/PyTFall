init -9 python:
    ####### Equipment Classes ########
    class Item(_object):
        NOT_USABLE = set(["gift", "quest", "loot"])
        NOT_TRANSFERABLE = set(["gift", "quest", "loot"])
        NOT_SELLABLE = set(["quest"])
        CONS_AND_MISC = set(['consumable', 'misc'])

        def __init__(self):
            self.desc = ''
            self.slot = "consumable"
            self.mod = {}
            self.mod_skills = {}
            self.max = {}
            self.min = {}
            self.addtraits = []
            self.removetraits = []
            self.add_be_spells = []
            self.remove_be_spells = []
            self.addeffects = []
            self.removeeffects = []
            self.goodtraits = set()
            self.badtraits = set()

            # Rules:
            self.usable = None
            self.transferable = None
            self.sellable = None
            
            self.hidden = True # Not used atm, decides if we should hide the effects.
            self.jump_to_label = ""
            self.price = 0
            self.sex = 'unisex'
            self.unique = "" # Should be girls id in case of unique item.
            self.bg_color = "" # only value atm is dark, otherwise brighter background will be used.
            self.statmax = False
            self.skillmax = False
            self.infinite = False
            self.locations = []
            self.chance = 50
            self.badness = 0

        def init(self):
            # Rules:
            if self.usable is None:
                if self.slot in self.NOT_USABLE:
                    self.usable = False
                else:
                    self.usable = True
                    
            if self.transferable is None:
                if self.slot in self.NOT_TRANSFERABLE:
                    self.transferable = False
                else:
                    self.transferable = True
                    
            if self.sellable is None:
                if self.slot in self.NOT_SELLABLE:
                    self.sellable = False
                else:
                    self.sellable = True
            
            if not hasattr(self, "eqchance"):
                self.eqchance = self.badness
                
            if not hasattr(self, 'type'):
                self.type = self.slot

            if self.slot == 'consumable':
                if not hasattr(self, 'cblock'):
                    self.cblock = False

                if not hasattr(self, 'ctemp'):
                    self.ctemp = False
                # Disabling maxes if ctemp is active:
                if self.ctemp:
                    self.skillmax = False
                    self.statmax = False
                    
                if not hasattr(self, 'ceffect'):
                    self.ceffect = False

            if self.slot == 'misc':
                if not hasattr(self, 'mtemp'):
                    self.mtemp = 10
                if not hasattr(self, 'mdestruct'):
                    self.mdestruct = False
                if not hasattr(self, 'mreusable'):
                    self.mreusable = False

            # Ensures normal behaviour:     
            if (self.statmax or self.skillmax) and self.slot not in self.CONS_AND_MISC:
                self.statmax = False
                self.skillmax = False
                
            if self.sex == "Male": self.sex = 'male'
            if self.sex == "Female": self.sex = 'female'
            if self.sex == "Unisex": self.sex = 'unisex'

    # Inventory with listing
    # this is used together with a specialized screens/functions
    class Inventory(_object):
        def __init__(self, per_page):
            self.items = list() # Handles actual filtered items instances
            self.content = OrderedDict() # Handles item.id/amount pairs
            
            # Paging:
            self.page = 0
            self.page_size = per_page
            self.set_max_page()
            
            # Filters:
            self.filter = 'all'
            self.male_filter = False # Filters out female only items
            self.female_filter = False
            self.ALL_FILTERS = ['all', 'weapon', 'smallweapon', 'head', 'body', 'wrist', 'feet', 'cape', 'amulet', 'ring', 'consumable', 'gift', 'misc', 'quest']
            self.GEQ_FILTERS = ['all', 'weapon', 'smallweapon', 'consumable', 'head', 'body', 'wrist', 'feet', 'cape', 'amulet', 'ring', 'misc', 'quest']
            self.FILTERS = self.ALL_FILTERS

        def set_page_size(self, size):
            self.page_size = size
            self.page = 0
            self.set_max_page()
            
        def apply_filter(self, direction):
            """
            Filter for items
            Currently filtered by slot
            """
            # if last_label in ("girl_profile", "char_equip", "items_transfer"):
            if last_label in ("items_transfer"):
                self.FILTERS = self.GEQ_FILTERS
            else:
                self.FILTERS = self.ALL_FILTERS
            
            index = self.FILTERS.index(self.filter)
            if direction == 'next':
                index = (index + 1) % len(self.FILTERS)
            elif direction == 'prev':
                index = (index - 1) % len(self.FILTERS)
            else:
                index = self.FILTERS.index(direction)

            filter = self.FILTERS[index]
            items = store.items
            if filter == 'all':
                if self.male_filter:
                    self.items = list(items[item] for item in self.content.iterkeys() if items[item].sex != "female")
                elif last_label in ("char_equip", "items_transfer") or self.female_filter:
                    self.items = list(items[item] for item in self.content.iterkeys() if items[item].sex != "male" and items[item].slot in self.FILTERS)
                else:
                    self.items = list(items[item] for item in self.content.iterkeys())
            else:
                if self.male_filter:
                    self.items = list(items[item] for item in self.content.iterkeys() if items[item].slot == filter and items[item].sex != 'female')
                elif last_label in ("char_equip", "items_transfer") or self.female_filter:
                    self.items = list(items[item] for item in self.content.iterkeys() if items[item].slot == filter and items[item].sex != 'male')
                else:    
                    self.items = list(items[item] for item in self.content.iterkeys() if items[item].slot == filter)

            self.page = 0
            self.set_max_page()
            self.filter = filter

        def next(self):
            """
            Next page
            """
            if self.page < self.max_page:
                self.page += 1
 
        def prev(self):
            """
            Previous page
            """
            if self.page > 0:
                self.page -= 1

        def first(self):
            """
            First page
            """
            self.page = 0

        def last(self):
            """
            Last page
            """
            self.page = self.max_page

        def getpage(self):
            """
            Get content of a page
            It's a cut-off from the whole
            """
            start = self.page * self.page_size
            end = (self.page+1) * self.page_size
            items = store.items
            return self.items[start:end]
            
        def set_max_page(self):
            """
            Calculates the max page.
            """
            self.max_page = len(self.items) / self.page_size if len(self.items) % self.page_size not in [0, self.page_size] else (len(self.items) - 1) / self.page_size

        def getitem(self, i):
            """
            Returns an item.
            Items coordinates: page number * page size + displacement from the start of the current page.
            """
            return self.items[self.page * self.page_size + i]

        def get_item_count(self, item):
            """
            Returns total amount of any particular item in the inventory.
            """
            if isinstance(item, Item):
                item = item.id
            if item in self.content:
                return self.content[item]
            
        def append(self, item, amount=1):
            """
            Add and item to inv and recalc max page.
            After rescaling, both remove and append methods are overkill.
            In case of game code review, one should prolly be removed.
            """
            if isinstance(item, basestring):
                item = store.items[item]
            self.content[item.id] = self.content.get(item.id, 0) + amount
            if item not in self.items:
                self.items.append(item)
            self.set_max_page()

        def remove(self, item, amount=1):
            """
            Removes given amount of items from inventory.
            Returns True if in case of success and False if there aren't enough items.
            """
            if isinstance(item, basestring):
                item = store.items[item]
            if self.content.get(item.id, 0) - amount >= 0:    
                self.content[item.id] = self.content.get(item.id, 0) - amount
                if self.content[item.id] <= 0:
                    del(self.content[item.id])
                    if item in self.items:
                        self.items.remove(item)
                self.set_max_page()
                return True
            return False

        def clear(self):
            """
            Removes ALL items from inventory!!!
            """
            self.content = OrderedDict()
            self.items = list()
            
        # Easy access:
        def __getitem__(self, key):
            """
            Returns an instance of an item if item is in the inventory.
            """
            if isinstance(key, Item):
                key = item.id
            if key in self.content:
                return self.content[key]

        def __len__(self):
            """
            Returns total amount of items in the inventory.
            """
            return sum(self.content.values())
            
        def __nonzero__(self):
            return bool(self.content)
            
        def __iter__(self):
            return iter(self.content)

    # Shops Classes:
    class ItemShop(_object):
        '''Any shop that sells items ;)
        '''
        def __init__(self, name, inv_length, locations=[], gold=10000, visible=True, sells=None, sell_margin=0.8, buy_margin=1.2):
            """Takes:
            locations = must be a list of item location fields ["general_shop", "cafe"] for example
            int_length = lenght of inventory field as arguments (must be an integer)
            gold = amount of gold shop has on start-up (int)
            visible = If the shop is visible to the player (bool), false is not used at the moment
            sells = list of all the item types this shop should trade.
            """
            self.name = name
            self.locations = set(locations)
            self.inventory = Inventory(inv_length)
            self.gold = gold
            self.normal_gold_amount = gold
            self.sell_margin = sell_margin
            self.buy_margin = buy_margin
            # self.target = None # Forgot what the hell tis is supposed to be
            self.visible = visible 
            self.restockday = randint(3, 5)
            if not sells:
                self.sells = set()
            else:
                self.sells = set(sells)

            self.restock()

        def restock(self):
            '''Restock this shop
            Chance for an item appearing and amount of items are taken from the Item class
            '''
            items = store.items
            for item in items.itervalues():
                for loc in self.locations:
                    if loc in item.locations:
                        if dice(item.chance):
                            self.inventory.append(item)

            for item in self.inventory.content:
                item = items[item]
                if item.infinite:
                    self.inventory.content[item.id] = 100
                else:
                    x = int(round(item.chance/10.0))
                    self.inventory.content[item.id] += x

        def next_day(self):
            '''Basic counter to be activated on next day
            '''
            if self.restockday == day:
                self.gold += randint(int(self.normal_gold_amount / 10), int(self.normal_gold_amount / 7))
                if self.gold > self.normal_gold_amount: self.gold = randint(int(self.normal_gold_amount * 1.3), int(self.normal_gold_amount * 1.6))
                self.restock()
                self.restockday += randint(3, 7)

        def get(self, id):
            return self.inventory.pop(id)
            
            
    class GeneralStore(ItemShop):
        '''General Store (sells basic items)
        '''
        def __init__(self, name, inv_length, locations, *args, **kwargs):
            ItemShop.__init__(self, name, inv_length, locations, *args, **kwargs)
            
        def next_day(self):
            '''Basic counter to be activated on next day
            '''
            if self.restockday == day:
                self.gold += randint(int(self.normal_gold_amount / 10), int(self.normal_gold_amount / 7))
                if self.gold > self.normal_gold_amount: self.gold = randint(int(self.normal_gold_amount * 1.3), int(self.normal_gold_amount * 1.6))
                self.restock()
                self.restockday += randint(3, 7)
            else:
                if self.gold < 15000:
                    self.gold += randint(16000, 25000)
