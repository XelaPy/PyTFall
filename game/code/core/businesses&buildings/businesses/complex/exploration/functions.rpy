init python:
    # For now a dedicated sorting funcs, maybe this should be turned into something more generic in the future?
    def all_chars_for_se():
        # We expect a global var building to be set for this!
        return [w for w in building.get_workers() if w not in all_idle_explorers()]

    def all_idle_explorers():
        # returns a list of all idle characters that are set exploration teams but not exploring:
        # This may be an overkill cause we should really remove workers from teams when we change their locations!
        idle_explorers = set()
        for building in hero.buildings:
            if isinstance(building, UpgradableBuilding):
                fg = building.get_business("fg")
                if fg:
                    idle_explorers = idle_explorers.union(fg.idle_explorers())
        return idle_explorers
