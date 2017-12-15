init -3 python:
    # Sub Upgrades:     # ==========================>>>
    class BusinessUpgrade(_object):
        SORTING_ORDER = 0
        #@Review: Inherited from building upgrade before, not sure why.
        """Usually suggests an expansion to a business upgrade that modifies some of it's workflow/properties/jobs!

        I want to code a skeleton for this atm.
        """
        COMPATIBILITY = []
        def __init__(self, *args, **kwargs):
            self.main_upgrade = None

        @property
        def img(self):
            return self.IMG

        @property
        def cost(self):
            return self.COST


    class Garden(BusinessUpgrade):
        def __init__(self, name="Garden", instance=None, desc="Relax!",
                    img="content/buildings/upgrades/garden.jpg", build_effort=0,
                    materials=None, in_slots=0, ex_slots=2, cost=500, **kwargs):
            super(Garden, self).__init__(name=name, instance=instance, desc=desc,
                            img=img, build_effort=build_effort, materials=materials,
                            cost=cost, **kwargs)


    class MainHall(BusinessUpgrade):
        def __init__(self, name="Main Hall", instance=None, desc="Reception!",
                     img="content/buildings/upgrades/main_hall.jpg", build_effort=0,
                     materials=None, in_slots=0, ex_slots=2, cost=500, **kwargs):
            super(MainHall, self).__init__(name=name, instance=instance, desc=desc,
                    img=img, build_effort=build_effort, materials=materials,
                    cost=cost, **kwargs)


    class CatWalk(BusinessUpgrade):
        COMPATIBILITY = [StripClub]
        MATERIALS = {"Wood": 10, "Bricks": 30, "Glass": 2}
        COST = 1000
        ID = "Cat Walk"
        IMG = "content/buildings/upgrades/catwalk_0.jpg"
        def __init__(self, name="Cat Walk", instance=None,
                desc="Good way to show off your strippers!", build_effort=0,
                materials=None, in_slots=2, **kwargs):
            super(CatWalk, self).__init__(name=name, instance=instance, desc=desc,
                build_effort=build_effort, materials=materials, **kwargs)


    class Aquarium(BusinessUpgrade):
        COMPATIBILITY = [StripClub]
        MATERIALS = {"Glass": 10, "Wood": 5}
        COST = 2500
        ID = "Aquarium"
        IMG = "content/buildings/upgrades/aquarium_nq.jpg"
        def __init__(self, name="Aquarium", instance=None,
            desc="Enhance the entertainment experience of your clients!",
            build_effort=0, materials=None, in_slots=4, **kwargs):
            super(Aquarium, self).__init__(name=name, instance=instance,
            desc=desc, build_effort=build_effort, materials=materials, **kwargs)
