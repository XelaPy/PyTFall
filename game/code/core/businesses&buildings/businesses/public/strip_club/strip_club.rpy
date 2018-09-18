init -5 python:
    class StripClub(PublicBusiness):
        COMPATIBILITY = []
        SORTING_ORDER = 4
        MATERIALS = {"Wood": 30, "Bricks": 50, "Glass": 10}
        NAME = "Strip Club"
        DESC = "Allows to use strippers to make customers hornier and get occasional tips"
        IMG = "content/buildings/upgrades/strip_club.webp"
        COST = 500
        def __init__(self, **kwargs):
            super(StripClub, self).__init__(**kwargs)

            self.jobs = set([simple_jobs["Striptease Job"]])
            # For now, before we'll have to split the method.
            self.intro_string = "{color=[pink]}%s{/color} comes out to do striptease!"
            self.log_intro_string = "{color=[pink]}%s{/color} is performing Striptease!"
            # Looks weird but until we have a better way to debug SimPy :(
            self.job_method = "work_strip_club"
