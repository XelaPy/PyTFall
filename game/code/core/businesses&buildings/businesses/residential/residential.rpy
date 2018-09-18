init -6 python:
    # Provides living space, not sure if this or the building should be bound as home locations!
    class SlaveQuarters(Business):
        SORTING_ORDER = 0
        NAME = "Slave Quarters"
        DESC = "Place for slaves to live in"
        IMG = "content/buildings/upgrades/guard_qt.webp"
        def __init__(self, **kwargs):
            super(SlaveQuarters, self).__init__(**kwargs)
            self.habitable = True

        @property
        def daily_modifier(self):
            value = self._daily_modifier
            for u in self.upgrades:
                value += getattr(u, "daily_rejuvenation_modifier", 0)
            return value
