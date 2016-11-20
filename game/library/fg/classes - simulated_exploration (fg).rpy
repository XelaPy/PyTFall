init -9 python:
    # ======================= (Simulated) Exploration code =====================>>>
    class FG_Area(_object):
        """Dummy class for areas (for now).
        
        Tracks the progess in SE areas as well as storing their data.
        """
        def __init__(self):
            self.stage = 0 # For Sorting.
            self.days = 3
            self.max_days = 15
            self.risk = 50
            self._explored = 0
            self.items = dict()
            self.girls = dict()
            self.main = False
            self.area = ""
            self.mobs = {}
            self.known_mobs = set()
            self.known_items = set()
            self.cash_earned = 0
            self.travel_time = 0
            self.hazard = dict()
            
            # Generated Content:
            self.logs = collections.deque(maxlen=10)
            
        @property
        def explored(self):
            return self._explored
            
        @explored.setter
        def explored(self, value):
            if value >= 100:
                self._explored = 100
            else:
                self._explored = value
