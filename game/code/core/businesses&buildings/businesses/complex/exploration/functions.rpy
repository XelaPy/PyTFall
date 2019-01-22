init python:
    # For now a dedicated sorting funcs, maybe this should be turned into something more generic in the future?
    def all_chars_for_se():
        # We expect a global var building to be set for this!

        # collect the set of all idle characters that are set exploration teams but not exploring:
        # This may be an overkill cause we should really remove workers from teams when we change their locations!
        idle_explorers = set()
        for b in hero.buildings:
            if isinstance(b, UpgradableBuilding):
                fg = b.get_business("fg")
                if fg:
                    idle_explorers.update(fg.idle_explorers())

        return [w for w in building.get_workers() if w not in idle_explorers]
