init -6 python:
    class StripClub(PublicBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 30, "Bricks": 50, "Glass": 10}
        COST = 8000
        ID = "Strip Club"
        IMG = "content/buildings/upgrades/strip_club.jpg"
        
        def __init__(self, name="Strip Club", instance=None, desc="Exotic Dancers go here!", img="content/buildings/upgrades/strip_club.jpg", build_effort=0, materials=None, in_slots=5, cost=500, **kwargs):
            super(StripClub, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Striptease Job"]])
            self.workable = True
            self.type = "public_service"
            
            self.capacity = in_slots
            self.active_workers = set() # On duty Strippers.
            self.clients = set() # Clients watching the stripshows.
            
            self.res = None # Restored before every job...
            self.time = 5
            self.is_running = False
            
            self.earned_cash = 0
            
            
    class Bar(PublicBusiness):
        COMPATIBILITY = []
        MATERIALS = {"Wood": 50, "Bricks": 30, "Glass": 5}
        COST = 5000
        ID = "Bar"
        IMG = "content/buildings/upgrades/bar.jpg"
        
        def __init__(self, name="Bar", instance=None, desc="Serve drinks and snacks to your customers!", img="content/buildings/upgrades/bar.jpg", build_effort=0, materials=None, in_slots=3, cost=500, **kwargs):
            super(Bar, self).__init__(name=name, instance=instance, desc=desc, img=img, build_effort=build_effort, materials=materials, cost=cost, **kwargs)
            self.jobs = set([simple_jobs["Bartending"]])
            self.workable = True
            self.type = "public_service"
            
            self.capacity = in_slots
            self.active_workers = set() # On duty Bartenders.
            self.clients = set() # Clients at the bar.
            
            # SimPy and etc follows (L33t stuff :) ):
            self.res = None # Restored before every job...
            self.time = 5
            self.is_running = False
            
            self.earned_cash = 0
