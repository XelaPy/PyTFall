init -5 python:
    class BarBusiness(PublicBusiness):
        COMPATIBILITY = []
        SORTING_ORDER = 4
        MATERIALS = {"Wood": 50, "Bricks": 30, "Glass": 5}
        NAME = "Bar"
        IMG = "content/buildings/upgrades/bar.webp"
        DESC = "Allows to serve drinks and snacks to your customers"
        COST = 500
        IN_SLOTS = 3
        def __init__(self, **kwargs):
            super(BarBusiness, self).__init__(**kwargs)

            self.jobs = set([simple_jobs["Bartending"]])

            # For now, before we'll have to split the method.
            self.intro_string = "{color=[pink]}%s{/color} comes out to tend the Bar!"
            self.log_intro_string = "{color=[pink]}%s{/color} is working the bar!"
            self.job_method = "work_bar"
