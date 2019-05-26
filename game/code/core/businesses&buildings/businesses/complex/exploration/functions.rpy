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
            if isinstance(worker, Player):
                continue
            elif worker in idle_explorers:
                continue
            elif worker.status != "free":
                continue

            rv.append(worker)

        return rv

    def rebuild_se_dd():
        global bm_mid_frame_mode
        global workers
        global fg_filters
        global guild_teams
        if isinstance(bm_mid_frame_mode, ExplorationGuild):
            # Looks pretty ugly... this might be worth improving upon just for the sake of esthetics.
            workers = CoordsForPaging(all_chars_for_se(), columns=6, rows=3,
                    size=(80, 80), xspacing=10, yspacing=10, init_pos=(56, 11))
            fg_filters = CharsSortingForGui(all_chars_for_se)
            fg_filters.occ_filters.add("Combatant")
            fg_filters.target_container = [workers, "content"]
            fg_filters.filter()

            guild_teams = CoordsForPaging(bm_mid_frame_mode.idle_teams(clear_by_workplace=True), columns=3, rows=3,
                            size=(208, 83), xspacing=0, yspacing=5, init_pos=(4, 340))
