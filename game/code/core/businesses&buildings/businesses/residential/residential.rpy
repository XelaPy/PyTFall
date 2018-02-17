init -6 python:
    # Provides living space, not sure if this or the building should be bound as home locations!
    class SlaveQuarters(Business):
        SORTING_ORDER = 0
        NAME = "Slave Quarters"
        DESC = "Place for slaves to live in!"
        IMG = "content/buildings/upgrades/guard_qt.jpg"
        def __init__(self, **kwargs):
            super(SlaveQuarters, self).__init__(**kwargs)
            self.habitable = True
