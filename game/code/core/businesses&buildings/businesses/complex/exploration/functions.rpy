init python:
    def all_chars_for_se():
        global BUILDING
        global bm_mid_frame_mode

        rv = []

        # collect the set of all idle characters that are set
        # exploration teams but not exploring:
        # This may be an overkill cause we should really remove workers
        # from teams when we change their locations!
        idle_explorers = set(bm_mid_frame_mode.idle_explorers())
        for worker in BUILDING.get_workers():
            if worker in idle_explorers:
                continue
            elif worker.status != "free":
                continue

            rv.append(worker)

        return rv
