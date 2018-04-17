init 5 python:
    class MainHall(BuildingUpgrade):
        SORTING_ORDER = 5
        COMPATIBILITY = []

        NAME = "Main Hall"
        IMG = "content/buildings/upgrades/main_hall.webp"
        MATERIALS = {"Bricks": 50, "Stone": 50,
                     "Green Marble": 40, "Steel": 10}
        temp = []
        temp.append("Main Hall!")
        temp.append("A lux main hall will attract more clients.")
        temp.append("(+20% Clients)")
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
            super(MainHall, self).__init__(**kwargs)
            self.client_flow_mod = 1.2
            self.expands_capacity = False # Force the matter.


    class Garden(BuildingUpgrade):
        SORTING_ORDER = 5
        COMPATIBILITY = []

        NAME = "Garden"
        IMG = "content/buildings/upgrades/garden.webp"
        MATERIALS = {"Stone": 50,
                     "Green Marble": 10,
                     "Wood": 50}
        temp = []
        temp.append("Main Hall!")
        temp.append("Beautiful garden to calm down your workers and clients.")
        temp.append("(+Chance to increase worker joy)")
        temp.append("(+Reduced threat accumulation from aggressive clients)")
        DESC = "\n".join(temp)
        del temp
        COST = 6000
        IN_SLOTS = 1
        EX_SLOTS = 5
        CAPACITY = 0

        EXP_CAP_IN_SLOTS = 0
        EXP_CAP_EX_SLOTS = 0
        EXP_CAP_COST = 0

        def __init__(self, **kwargs):
            super(Garden, self).__init__(**kwargs)
            self.expands_capacity = False # Force the matter.
