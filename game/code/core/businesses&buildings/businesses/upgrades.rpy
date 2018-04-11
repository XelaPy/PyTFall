init -3 python:
    # Sub Upgrades:     # ==========================>>>
    class BBUpgrade(CoreExtension):
        """Building or Business Upgrade core class.
        In case we need one...
        """
        def __init__(self, **kwargs):
            super(BBUpgrade, self).__init__(**kwargs)


    class BuildingUpgrade(BBUpgrade):
        SORTING_ORDER = 0
        #@Review: Inherited from building upgrade before, not sure why.
        """Usually suggests an expansion to a building that modifies some of it's workflow/properties/jobs!
        """
        def __init__(self, **kwargs):
            super(BuildingUpgrade, self).__init__(**kwargs)


    class BusinessUpgrade(BBUpgrade):
        SORTING_ORDER = 0
        #@Review: Inherited from building upgrade before, not sure why.
        """Usually suggests an expansion to a business that modifies some of it's workflow/properties/jobs!
        I want to code a skeleton for this atm.
        """
        COMPATIBILITY = []
        def __init__(self, *args, **kwargs):
            super(BusinessUpgrade, self).__init__(**kwargs)
            self.business = None


    # class Garden(BuildingUpgrade):
    #     def __init__(self, name="Garden", desc="Nice, green place to relax!",
    #                 img="content/buildings/upgrades/garden.webp",
    #                 **kwargs):
    #
    #         super(Garden, self).__init__(name=name, desc=desc,
    #                                      img=img, **kwargs)
    #
    #
    # class MainHall(BuildingUpgrade):
    #     def __init__(self, name="Main Hall", desc="Reception for your customers!",
    #                  img="content/buildings/upgrades/main_hall.webp", **kwargs):
    #
    #         super(MainHall, self).__init__(name=name, desc=desc,
    #                 img=img, **kwargs)
    #
    #
    # class CatWalk(BusinessUpgrade):
    #     # For Strip Club
    #     NAME = "Cat Walk"
    #     def __init__(self, name="Cat Walk",
    #                  desc="Good way to show off your strippers!",
    #                  img="content/buildings/upgrades/catwalk_0.webp",
    #                  **kwargs):
    #
    #         super(CatWalk, self).__init__(name=name, desc=desc,
    #             build_effort=build_effort, **kwargs)
    #
    #
    # class Aquarium(BusinessUpgrade):
    #     # For Bar, Strip Club.
    #     MATERIALS = {"Glass": 10, "Wood": 5}
    #     NAME = "Aquarium"
    #     def __init__(self, name="Aquarium",
    #                  desc="Enhance the entertainment experience of your clients!",
    #                  img="content/buildings/upgrades/aquarium_nq.webp",
    #                  **kwargs):
    #
    #         super(Aquarium, self).__init__(name=name,
    #                     desc=desc, **kwargs)
