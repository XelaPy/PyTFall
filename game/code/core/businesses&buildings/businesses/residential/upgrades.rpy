init 5 python:
    class SQLandscape(BusinessUpgrade):
        SORTING_ORDER = 5
        COMPATIBILITY = [BrothelBlock]

        NAME = "Garden"
        IMG = "content/buildings/upgrades/landscape.webp"
        MATERIALS = {"Stone": 20,
                     "Wood": 20,
                     "Green Marble": 5}
        temp = []
        temp.append("Beautiful Garden!")
        temp.append("A large and beautiful garden to put your slaves at ease.")
        temp.append("(+25% Overnight restoration for slaves in this building!)")
        DESC = "\n".join(temp)
        del temp
        COST = 3000
        IN_SLOTS = 2
        EX_SLOTS = 5
        CAPACITY = 0

        EXP_CAP_IN_SLOTS = 0
        EXP_CAP_EX_SLOTS = 0
        EXP_CAP_COST = 0

        def __init__(self, **kwargs):
            super(SQLandscape, self).__init__(**kwargs)
            self.daily_rejuvenation_modifier = .25
