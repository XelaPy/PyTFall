init -9 python:
    ####### Equipment Classes ########
    class Item(_object):
        NOT_USABLE = set(["gift", "quest", "loot", "resources"])
        NOT_TRANSFERABLE = set(["gift", "quest", "resources"])
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
            self.pref_class = []

            # Rules:
            self.usable = None
            self.transferable = None
            self.sellable = None
            self.be = False # could be used in battle engine

            # mostly not used atm, decides if we should hide the item effects;
            # does hide effects for gifts which have not been used at least once, becoming False afterwards
            self.hidden = True
            self.jump_to_label = ""
            self.price = 0
            self.sex = 'unisex'
            self.unique = "" # Should be girls id in case of unique item.
            self.statmax = False
            self.skillmax = False
            self.infinite = False
            self.locations = []
            self.chance = 50
            self.badness = 0

            self.tier = None # Tier of an item to match class tier, 0 - 4 is the range.
            # self.level = 0 We're using tiers for now.
            # Level is how an item compares to it's relatives
            # I'd like this to be set for all items one days
            # Excalibur for example is 10, the shittiest sword is 1
            # Same can be done for food, scrolls and practically any item in the game.
            # Groups may even start at high values, if items are really good and/or expensive
            # And no shit item exists within the same group
            # Basically, you when we check for level, we want to know how the item
            # is valued in the game on scale from 0 - 10.

            # BE attributes:
            # self.evasion_bonus = 0 # Needs a int, will be used a percentage (1 = 1%)
            # self.ch_multiplier = 0 # Critical hit multi...
            # self.damage_multiplier = 0

            # self.defence_bonus = {} # Delivery! Not damage types!
            # self.defence_multiplier = {}
            # self.delivery_bonus = {} Expects a k/v pair of type: multiplier This is direct bonus added to attack power.
            # self.delivery_multiplier = {}
            # why is it commented out though? BE attributes are widely used by items...

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
                if self.slot in self.NOT_SELLABLE or self.price == 0:
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

            if self.slot == 'misc':
                if not hasattr(self, 'mtemp'):
                    self.mtemp = 10
                if not hasattr(self, 'mdestruct'):
                    self.mdestruct = False
                if not hasattr(self, 'mreusable'):
                    self.mreusable = False

            # Ensures normal behavior:
            if (self.statmax or self.skillmax) and self.slot not in self.CONS_AND_MISC:
                self.statmax = False
                self.skillmax = False

            # Gets rid of possible caps:
            self.sex = self.sex.lower()

        def get_stat_eq_bonus(self, char_stats, stat):
            """Simple method that tries to get the real bonus an item can offer for the stat.

            This method assumes that item can offer a bonus to the stat!
            Presently used in auto_equip method.
            Does not take traits into consideration, just max/lvl_max and stats.
            """
            if stat in self.max:
                new_max = char_stats.max[stat] + self.max[stat]
                new_max = min(new_max, char_stats.lvl_max[stat])
            else:
                new_max = char_stats.get_max(stat)
            new_stat = char_stats.stats[stat] + char_stats.imod[stat] + (self.mod[stat] if stat in self.mod else 0)
            if new_stat > new_max:
                new_stat = new_max
            return new_stat - char_stats._get_stat(stat)


    # Inventory with listing
    # this is used together with a specialized screens/functions
    class Inventory(_object):
        GENDER_FILTERS = {"any": ["unisex", "female", "male"],
                          "male": ["unisex", "male"],
                          "female": ["unisex", "female"]}
        SLOT_FILTERS = {"all": ('weapon', 'smallweapon', 'head', 'body', 'wrist',
            'feet', 'cape', 'amulet', 'ring', 'consumable', 'gift', 'misc', 'quest',
            "resources", "loot"),
            "quest": ("quest", "resources", "loot")}

        def __init__(self, per_page):
            self.filtered_items = list() # Handles actual filtered items instances.
            self.items = OrderedDict() # Handles item/amount pairs.

            # Paging:
            self.set_page_size(per_page)
            self.filter_index = 0

            # Filters:
            self.slot_filter = 'all' # Active Slot filter.
            self.final_sort_filter = ("id", False) # We feel second arg to reverse of sort!
            self.gender_filter = "any"

        # Filters:
        @property
        def filters(self):
            """Returns a selection of available filters for the occasion"""
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

        def update_sorting(self, final_sort_filter=None, gender=None):
            if final_sort_filter is not None:
                self.final_sort_filter = final_sort_filter
            if gender is not None:
                self.gender_filter = gender

            # Genders:
            gf = self.GENDER_FILTERS[self.gender_filter]
            self.filtered_items = [i for i in self.filtered_items if i.sex in gf]

            # Complex:
            key, reverse = self.final_sort_filter
            if self.final_sort_filter[0] in ["id", "price"]:
                self.filtered_items.sort(key=attrgetter(key), reverse=reverse)
            elif self.final_sort_filter[0] == "amount":
                sorted_items = {}
                for item in self.filtered_items:
                    sorted_items[item] = self.items[item]
                sorted_items = OrderedDict(sorted(sorted_items.items(),
                                key=itemgetter(1), reverse=self.final_sort_filter[1]))
                self.filtered_items = sorted_items.keys()

        def apply_filter(self, direction, gender=None):
            """Filter for items.

            Presently filtered by slot.
            """
            filters = self.filters

            if direction in set(self.SLOT_FILTERS["all"]).union(self.SLOT_FILTERS.keys()):
                self.slot_filter = direction
            else:
                if direction == 'next':
                    self.filter_index = (self.filter_index + 1) % len(filters)
                elif direction == 'prev':
                    self.filter_index = (self.filter_index - 1) % len(filters)
                else:
                    try: # We try to get the correct filter, but it could be a fail...
                        self.filter_index = filters.index(self.slot_filter)
                    except:
                        # Explicitly silenced Exception. We set the index to "all" (0) which is always available!
                        self.filter_index = 0
                self.slot_filter = filters[self.filter_index]

            self.filtered_items = list(item for item in self.items.iterkeys() if item.slot in self.SLOT_FILTERS.get(self.slot_filter, [self.slot_filter]))

            self.update_sorting(gender=gender)

            self.page = 0 # min(max(0, self.max_page-1), self.page)

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
            """Next page"""
            if self.max_page > 0:
                self.page = (self.page + 1) % self.max_page
            else:
                self.page = 0

        def prev(self):
            """Previous page"""
            if self.max_page > 0:
                self.page = (self.page - 1) % self.max_page
            else:
                self.page = 0

        def first(self):
            """First page"""
            self.page = 0

        def last(self):
            """Last page"""
            self.page = self.max_page - 1 if self.paged_items else 0

        @property
        def page_content(self):
            """Get content for current page"""
            items = self.paged_items

            try:
                return items[self.page]
            except IndexError:
                if self.page - 1 >= 0:
                    self.page -= 1
                    return items[self.page]
                else:
                    self.page = 0
                    return []

        @property
        def max_page(self):
            return len(self.paged_items)

        # Add/Remove/Clear:
        def append(self, item, amount=1):
            """
            Add an item to inv and recalc max page.
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
        def __contains__(self, item):
            if isinstance(item, basestring):
                item = store.items.get(item, None)
            return item in self.items

        def __getitem__(self, item):
            """Returns an amount of specific item in inventory.
            """
            if isinstance(item, basestring):
                item = store.items.get(item, None)
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
        def __init__(self, name, inv_length, locations=[], gold=10000, visible=True, sells=None, sell_margin=.8, buy_margin=1.2):
            """Takes:
            locations = must be a list of item location fields ["general_shop", "cafe"] for example
            int_length = length of inventory field as arguments (must be an integer)
            gold = amount of gold shop has on start-up (int)
            visible = If the shop is visible to the player (bool), false is not used at the moment
            sells = list of all the item types this shop should trade.
            """
            self.total_items_price = 0 # 25% of items price sold to shop goes to shop's gold on next gold update
            self.name = name
            self.locations = set(locations)
            self.inventory = Inventory(inv_length)
            self.gold = gold
            self.normal_gold_amount = gold
            self.sell_margin = sell_margin
            self.buy_margin = buy_margin
            # self.target = None # Forgot what the hell tis is supposed to be
            self.visible = visible
            self.restockday = locked_random("randint", 3, 5)
            if not sells:
                self.sells = set()
            else:
                self.sells = set(sells)

            self.restock()

        def restock(self):
            '''Restock this shop
            Chance for an item appearing and amount of items are taken from the Item class
            '''
            self.inventory.clear()

            items = store.items
            for item in items.itervalues():
                if self.locations.intersection(item.locations) and dice(item.chance):
                    if item.infinite:
                        x = 100
                    else:
                        x = 1 + round_int(item.chance/10.0)
                    self.inventory.append(item=item, amount=x)

            # Gazette:
            if self in pytfall.__dict__.values():
                msg = [
                "{} Restocked!".format(self.name),
                "New merchandise arrived at {}.".format(self.name),
                "Check out the new arrivals at {}.".format(self.name)
                ]
                gazette.shops.append(choice(msg))


        def next_day(self):
            '''Basic counter to be activated on next day
            '''
            if self.restockday == day:
                self.gold += randint(int(self.normal_gold_amount / 10), int(self.normal_gold_amount / 7))
                if self.gold > self.normal_gold_amount: self.gold = randint(int(self.normal_gold_amount * 1.3), int(self.normal_gold_amount * 1.6))
                self.restock()
                if self.total_items_price > 0:
                    self.gold += int(self.total_items_price * .35)
                self.total_items_price = 0
                self.restockday += locked_random("randint", 3, 7)


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
                    self.gold += locked_random("randint", 16000, 25000)
