init -9 python:
    # ======================= (Simulated) Exploration code =====================>>>
    class FG_Area(_object):
        """Dummy class for areas (for now).
        
        Tracks the progess in SE areas as well as storing their data. This can prolly remain the same or similar to this plain design.
        """
        def __init__(self):
            self.days = 3
            self.max_days = 15
            self.risk = 50
            self._explored = 0
            self.items = dict()
            self.girls = dict()
            self.known_mobs = set()
            self.known_items = set()
            self.cash_earned = 0
            self.travel_time = 0
            self.hazard = dict()
            
        @property
        def explored(self):
            return self._explored
            
        @explored.setter
        def explored(self, value):
            if value >= 100:
                self._explored = 100
            else:
                self._explored = value
            
        
    class FG_Drags(_object):
        """
        Handles the drags coords and info.
        Might be I'll just use this in the future to handle the whole thing.
        For now, this will be used in combination with screen language.
        *Adaptation of Roman's Inv code!
        """
        
        # Do we even still need this???
        
        def __init__(self):
            # Should be changes to location in the future:    
            self.content = list(girl for girl in fg.get_girls() if girl.action not in ["Exploring"])
            self.page = 0
            self.page_size = 10
            self.max_page = len(self.content) / self.page_size if len(self.content) % self.page_size not in [0, self.page_size] else (len(self.content) - 1) / self.page_size

            self.pos = list()
            x = 0
            y = 0
            for i in xrange(5):
                self.pos.append((x, y))
                y = y + 70
            x = 70
            y = 0
            for i in xrange(5):
                self.pos.append((x, y))
                y = y + 70
                
        # Next page
        def next(self):
            if self.page < self.max_page:
                self.page += 1

        # Previous page
        def prev(self):
            if self.page > 0:
                self.page -= 1
                
        def get_page_content(self):
            start = self.page * self.page_size
            end = (self.page+1) * self.page_size
            
            return self.content[start:end]
            
        # Get an item
        # Items coordinates: page number * page size + displacement from the start of the current page
        def getitem(self, i):
            return self.content[self.page * self.page_size + i]
            
        # group of methods realizing the interface of common listing
        # remove and add an element
        # with recalc of current page
        def append(self, girl):
            if girl not in self.content:
                self.content.append(girl)
            self.max_page = len(self.content) / self.page_size if len(self.content) % self.page_size not in [0, self.page_size] else (len(self.content) - 1) / self.page_size

        def remove(self, girl):
            if girl in self.content:
                self.content.remove(girl)
                self.max_page = len(self.content) / self.page_size if len(self.content) % self.page_size not in [0, self.page_size] else (len(self.content) - 1) / self.page_size
