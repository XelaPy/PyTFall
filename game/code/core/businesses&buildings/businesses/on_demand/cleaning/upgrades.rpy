init 5 python:
    class BroomCloset(BusinessUpgrade):
        SORTING_ORDER = 5
        COMPATIBILITY = [Cleaners]

        NAME = "Closet"
        IMG = "content/buildings/upgrades/broom_closet.webp"
        MATERIALS = {"Wood": 20, "Stone": 10,
                     "Steel":5}
        temp = []
        temp.append("Broom Closet!")
        temp.append("Closet full of magical brooms which can be used to speed up cleaning process.")
        temp.append("(+2 Job Power)")
        DESC = "\n".join(temp)
        del temp
        COST = 1000
        IN_SLOTS = 2
        EX_SLOTS = 0
        CAPACITY = 0

        EXP_CAP_IN_SLOTS = 0
        EXP_CAP_EX_SLOTS = 0
        EXP_CAP_COST = 0

        def __init__(self, **kwargs):
            super(BroomCloset, self).__init__(**kwargs)
            self.job_power_mod = 2
            self.expands_capacity = False # Force the matter.
