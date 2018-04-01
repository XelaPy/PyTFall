init 5 python:
    class MainHall(BuildingUpgrade):
        SORTING_ORDER = 5
        COMPATIBILITY = [BrothelBlock]

        NAME = "Main Hall"
        IMG = "content/buildings/upgrades/main_hall.jpg"
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
