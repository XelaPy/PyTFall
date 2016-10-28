init -9 python:
    ####### Equipment Classes ########
    class Item(_object):
        NOT_USABLE = set(["gift", "quest", "loot", "resources"])
        NOT_TRANSFERABLE = set(["gift", "quest", "loot", "resources"])
        NOT_SELLABLE = set(["quest"])
        CONS_AND_MISC = set(['consumable', 'misc'])
        
        def __init__(self):
            self.desc = ""
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
            
            # BE attributes:
            # self.evasion_bonus = 0 # Needs a int, will be used a percentage (1 = 1%)
            # self.ch_multiplier = 0 # Critical hit multi...
            # self.damage_multiplier = 0
            
            # self.defence_bonus = {} # Delivery! Not damage types!
            # self.defence_multiplier = {}
            # self.delivery_bonus = {} Expects a k/v pair of type: multiplier This is direct bonus added to attack power.
            # self.delivery_multiplier = {}

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
                
            # Gets rid of possible caps:
            self.sex = self.sex.lower()

        def get_stat_eq_bonus(self, char, stat):
            """Simple method that tries to get the real bonus an item can offer for the stat.
            
            This method assumes that item can offer a bonus to the stat!
            Presently used in auto_equip method.
            Does not take traits into concideration, just max/lvl_max and stats.
            """
            stats = char.stats
            if stat in self.max:
                new_max = stats.max[stat] + self.max[stat]
                new_max = min(new_max, stats.lvl_max[stat])
            else:
                new_max = char.get_max(stat)
            new_stat = stats.stats[stat] + stats.imod[stat] + self.mod[stat]
            if new_stat > new_max:
                new_stat = new_max
            return new_stat - stats._get_stat(stat)
            
            
    # Inventory with listing
    # this is used together with a specialized screens/functions
    class Inventory(_object):
        GENDER_FILTERS = {"any": ["unisex", "female", "male"], "male": ["unisex", "male"], "female": ["unisex", "female"]}
        SLOT_FILTERS = {"all": ('weapon', 'smallweapon', 'head', 'body', 'wrist', 'feet', 'cape', 'amulet', 'ring', 'consumable', 'gift', 'misc', 'quest', "resources", "loot"),
                                        "quest": ("quest", "resources", "loot")}
        
        def __init__(self, per_page):
            self.filtered_items = list() # Handles actual filtered items instances.
            self.items = OrderedDict() # Handles item/amount pairs.
            
            # Paging:
            self.set_page_size(per_page)
            self.filter_index = 0
            
            # Filters:
            self.slot_filter = 'all' # Active Slot filter.
            self.gender_filter = self.GENDER_FILTERS["any"]

        # Filters:
        def set_gender_filter(self, filter):
            self.gender_filter = self.GENDER_FILTERS[filter]
            
        @property
        def filters(self):
            # returns a selection of availible filters for the occasion:
            filters = ["all"]
            availible_item_slots = set(item.slot for item in self.items.iterkeys())
            
            # Special cases:
            if "loot" in availible_item_slots:
                availible_item_slots.remove("loot")
                availible_item_slots.add("quest")
            if "resources" in availible_item_slots:
                availible_item_slots.remove("resources")
                availible_item_slots.add("quest")
                
            return filters + list(sorted(availible_item_slots))
        
        def apply_filter(self, direction):
            """Filter for items.
            
            Currently filtered by slot.
            """
            if direction == 'next':
                self.filter_index = (self.filter_index + 1) % len(self.filters)
            elif direction == 'prev':
                self.filter_index = (self.filter_index - 1) % len(self.filters)
            else:
                try: # We try to get the correct filter, but it could be a fail...
                    self.filter_index = self.filters.index(direction)
                except:
                    # Explicitly silenced Exception. We set the index to "all" (0) which is always availible!
                    self.index = 0
                    
            self.slot_filter = self.filters[self.filter_index]
            
            self.filtered_items = list(item for item in self.items.iterkeys() if item.sex in self.gender_filter and item.slot in self.SLOT_FILTERS.get(self.slot_filter, [self.slot_filter]))
            
            self.page = 0

        # Paging:
        @property
        def paged_items(self):
            items = []
            for start in xrange(0, len(self.filtered_items), self.page_size):
                 items.append(self.filtered_items[start:start+self.page_size])
            return items
        
        def set_page_size(self, size):
            self.page_size = size
            self.page = 0
        
        def next(self):
            """Next page.
            """
            if self.page + 1 < self.max_page:
                self.page += 1
 
        def prev(self):
            """Previous page.
            """
            if self.page > 0:
                self.page -= 1

        def first(self):
            """First page.
            """
            self.page = 0

        def last(self):
            """Last page.
            """
            self.page = self.max_page - 1 if self.paged_items else 0

        @property
        def page_content(self):
            """Get content for current page.
            """
            return self.paged_items[self.page] if self.paged_items else []
            
        @property
        def max_page(self):
            return len(self.paged_items)
            
        # Add/Remove/Clear:
        def append(self, item, amount=1):
            """
            Add and item to inv and recalc max page.
            After rescaling, both remove and append methods are overkill.
            In case of game code review, one should prolly be removed.
            """
            if isinstance(item, basestring):
                item = store.items[item]
                
            self.items[item] = self.items.get(item, 0) + amount
            if item not in self.filtered_items:
                self.filtered_items.append(item)

        def remove(self, item, amount=1):
            """Removes given amount of items from inventory.
            
            Returns True if in case of success and False if there aren't enough items.
            """
            if isinstance(item, basestring):
                item = store.items[item]
                
            if self.items.get(item, 0) - amount >= 0:    
                self.items[item] = self.items.get(item, 0) - amount
                if self.items[item] <= 0:
                    del(self.items[item])
                    if item in self.filtered_items:
                        self.filtered_items.remove(item)
                return True
                
            return False

        def clear(self):
            """Removes ALL items from inventory!!!
            """
            self.items = OrderedDict()
            self.filtered_items = list()
            
        # Easy access (special methods):
        def __getitem__(self, item):
            """Returns an amount of specif item in inventory.
            """
            if isinstance(item, basestring):
                item = store.items[item]
            
            return self.items.get(item, 0)

        def __len__(self):
            """Returns total amount of items in the inventory.
            """
            return sum(self.items.values())
            
        def __nonzero__(self):
            return bool(self.items)
            
        def __iter__(self):
            return iter(self.items)

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

            for item in self.inventory:
                if item.infinite:
                    self.inventory.items[item] = 100
                else:
                    x = int(round(item.chance/10.0))
                    self.inventory.items[item] += x

        def next_day(self):
            '''Basic counter to be activated on next day
            '''
            if self.restockday == day:
                self.gold += randint(int(self.normal_gold_amount / 10), int(self.normal_gold_amount / 7))
                if self.gold > self.normal_gold_amount: self.gold = randint(int(self.normal_gold_amount * 1.3), int(self.normal_gold_amount * 1.6))
                self.restock()
                self.restockday += randint(3, 7)
            
            
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
