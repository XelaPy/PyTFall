init 5 python:
    class StatueOfSexGoddess(BusinessUpgrade):
        SORTING_ORDER = 5
        COMPATIBILITY = [BrothelBlock]

        MATERIALS = {"Bricks": 100, "Stone": 200,
                     "Green Marble": 100, "Steel": 50}
        COST = 10000
        IN_SLOTS = 2
        EX_SLOTS = 4
        CAPACITY = 0

        EXP_CAP_IN_SLOTS = 0
        EXP_CAP_EX_SLOTS = 0
        EXP_CAP_COST = 0

        def __init__(self, name="Statue",
                     img="content/buildings/upgrades/statue_sexgoddess.jpg",
                     **kwargs):
            self.job_effectiveness_mod = 50

            temp = []
            temp.append("Statue Of The Sex Goddess!")
            temp.append("A large statue with mystical properties to stand outside of the Brothel.")
            temp.append("(+50 Job Effectiveness)")
            self.desc = temp.join("\n")
