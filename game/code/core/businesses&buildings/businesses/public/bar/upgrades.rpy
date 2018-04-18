init 5 python:
    class TapBeer(BusinessUpgrade):
        SORTING_ORDER = 5
        COMPATIBILITY = [BarBusiness]

        NAME = "Tap Beer"
        IMG = "content/buildings/upgrades/beer.webp"
        MATERIALS = {"Wood": 2,
                     "Glass": 5}
        temp = []
        temp.append("Serve Fresh Tap Beer!")
        temp.append("Best brew in the city will keep your customers drunk and happy.")
        temp.append("(+10 Job Effectiveness)")
        temp.append("(+Small chance to get extra tips)")
        DESC = "\n".join(temp)
        del temp
        COST = 500
        IN_SLOTS = 1
        EX_SLOTS = 0
        CAPACITY = 0

        EXP_CAP_IN_SLOTS = 0
        EXP_CAP_EX_SLOTS = 0
        EXP_CAP_COST = 0

        def __init__(self, **kwargs):
            super(TapBeer, self).__init__(**kwargs)
            self.job_effectiveness_mod = 10
            self.expands_capacity = False # Force the matter.
