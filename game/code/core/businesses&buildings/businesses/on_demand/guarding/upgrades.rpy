init 5 python:
    class SparringQuarters(BusinessUpgrade):
        SORTING_ORDER = 5
        COMPATIBILITY = [WarriorQuarters]

        NAME = "Sparring Quarters"
        IMG = "content/buildings/upgrades/sparring_qt.webp"
        MATERIALS = {"Wood": 20,
                     "Stone": 5,
                     "Steel": 10}
        temp = []
        temp.append("Sparring Quarters!")
        temp.append("Quarters where guards can do some training between their patrol shifts.")
        temp.append("+Chance to earn extra combat stats, skills and experience.")
        temp.append("-Small chance to get hurt while training.")
        DESC = "\n".join(temp)
        del temp
        COST = 2000
        IN_SLOTS = 2
        EX_SLOTS = 2
        CAPACITY = 0

        EXP_CAP_IN_SLOTS = 0
        EXP_CAP_EX_SLOTS = 0
        EXP_CAP_COST = 0

        def __init__(self, **kwargs):
            super(SparringQuarters, self).__init__(**kwargs)
            # We just check for instance and award stats.
            # It's prolly more confusing to add modifier here unless logic changes.
            self.expands_capacity = False # Force the matter.

    class EnforcedOrder(BusinessUpgrade):
        SORTING_ORDER = 5
        COMPATIBILITY = [WarriorQuarters]

        NAME = "Enforced Order"
        IMG = "content/buildings/upgrades/training_qt.webp"
        MATERIALS = {"Wood": 5,
                     "Stone": 20,
                     "Steel": 30}
        temp = []
        temp.append("Enforced Order!")
        temp.append("Set of decorations and tools in order to over-secure your building.")
        temp.append("But your workers feel 'out of place'.")
        temp.append("+5 Job Power points. Brawl event is blocked.")
        temp.append("-Joy and Disposition for civilians working the building.")
        DESC = "\n".join(temp)
        del temp
        COST = 5000
        IN_SLOTS = 5
        EX_SLOTS = 1
        CAPACITY = 0

        EXP_CAP_IN_SLOTS = 0
        EXP_CAP_EX_SLOTS = 0
        EXP_CAP_COST = 0

        def __init__(self, **kwargs):
            super(EnforcedOrder, self).__init__(**kwargs)
            self.job_power_mod = kwargs.get("job_power_mod", 5)
            self.expands_capacity = False # Force the matter.
            # We just check for instance and award stats.
            # It's prolly more confusing to add modifier here unless logic changes.
