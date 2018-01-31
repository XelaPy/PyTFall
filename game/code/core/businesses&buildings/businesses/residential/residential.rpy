init -6 python:
    # Provides living space, not sure if this or the building should be bound as home locations!
    class SlaveQuarters(Business):
        SORTING_ORDER = 0
        def __init__(self, name="Slave Quarters",
                     desc="Place for slaves to live in!",
                     img="content/buildings/upgrades/guard_qt.jpg",
                     **kwargs):
            super(SlaveQuarters, self).__init__(name=name,
                  desc=desc, img=img, **kwargs)
            self.habitable = True
