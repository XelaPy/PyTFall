# Manager stuff goes here, will prolly be only one function but it doesn't fit anywhere else.
# This process should be ran first!
init python:
    def manager_process(env, manager, building):
        effectiveness = building.manager_effectiveness

        # Special bonus to JobPoints (aka pep talk) :D
        mp_init_jp_bonus(manager, building, effectiveness)

        while 1:
            yield env.timeout(1)

    def mp_init_jp_bonus(manager, building, effectiveness):
        # Special bonus to JobPoints (aka pep talk) :D
        init_jp_bonus = (effectiveness-95.0)/100
        if init_jp_bonus < 0:
            init_jp_bonus = None
        elif init_jp_bonus > .3: # Too much power otherwise...
            init_jp_bonus = .3
        elif init_jp_bonus < .05: # Less than 5% is absurd...
            init_jp_bonus = .05

        if init_jp_bonus:
            init_jp_bonus += 1.0

            # Bonus to the maximum amount of workers:
            max_workers = round_int((manager.jobpoints*.5)/5)

            workers = building.active_workers
            if len(workers) > max_workers:
                workers = random.sample(workers, max_workers)
