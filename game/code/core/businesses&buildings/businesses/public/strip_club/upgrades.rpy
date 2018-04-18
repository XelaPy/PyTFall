init 5 python:
    class Catwalk(BusinessUpgrade):
        SORTING_ORDER = 5
        COMPATIBILITY = [StripClub]

        NAME = "Catwalk"
        IMG = "content/buildings/upgrades/catwalk_2.webp"
        MATERIALS = {"Bricks": 20,
                     "Wood": 50,
                     "Glass": 20}
        temp = []
        temp.append("Catwalk!")
        temp.append("A podium with strip poles to increase the effectiveness of your workers.")
        temp.append("(+20 Job Effectiveness)")
        DESC = "\n".join(temp)
        del temp
        COST = 2000
        IN_SLOTS = 2
        EX_SLOTS = 0
        CAPACITY = 0

        EXP_CAP_IN_SLOTS = 0
        EXP_CAP_EX_SLOTS = 0
        EXP_CAP_COST = 0

        def __init__(self, **kwargs):
            super(Catwalk, self).__init__(**kwargs)
            self.job_effectiveness_mod = 20
            self.expands_capacity = False # Force the matter.
