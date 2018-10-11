# Manager stuff goes here, will prolly be only one function but it doesn't fit anywhere else.
# This process should be ran first!
init -50 python:
    class ManagerData(object):
        def __init__(self):
            self.init_pep_talk = True
            self.cheering_up = True
            self.asks_clients_to_wait = True
            self.help_ineffective_workers = True # Bad performance still may get a payout.
            self.works_other_jobs = False

            # TODO Before some major release that breaks saves, move manager and effectiveness fields here.
            self.mlog = None # Manager job log

        @property
        def mjp(self):
            if self.manager:
                return self.manager.jobpoints
            else:
                return 0
        @mjp.setter
        def mjp(self, value):
            if self.manager:
                self.manager.jobpoints = value

init -5 python:
    class Manager(Job):
        """This is the manager Job, so far it just creates the instance we can use to assign the job.

        - Later we may use this to do mod stats and level up Managers somehow...
        """
        def __init__(self):
            super(Manager, self).__init__()
            self.id = "Manager"
            self.type = "Management"

            # Traits/Job-types associated with this job:
            self.occupations = ["Specialist"] # General Strings likes SIW, Combatant, Server...
            self.occupation_traits = [traits["Manager"]] # Corresponding traits...
            self.aeq_purpose = 'Manager'
            self.desc = "Manages your business, helping workers in various ways and improving their performance."

            self.base_skills = {"management": 80, "refinement": 20}
            self.base_stats = {"character": 40, "intelligence": 60}

            self.allowed_status = ["free"]


    def manager_process(env, building):
        manager = building.manager
        effectiveness = building.manager_effectiveness
        init_jp = manager.jobpoints

        job = simple_jobs["Manager"]
        building.mlog = log = NDEvent(job=job, char=manager, loc=building)
        temp = "{} is overseeing the building!".format(manager.name)
        log.append(temp)
        log.append("")

        # Special bonus to JobPoints (aka pep talk) :D
        if building.init_pep_talk and effectiveness > 95 and manager.jobpoints >= 10:
            mp_init_jp_bonus(manager, building, effectiveness, log)

        while 1:
            yield env.timeout(1)

            # Special direct bonus to tired/sad characters
            if building.cheering_up and not env.now % 5 and all([
                    manager.jobpoints > 10,
                    dice(effectiveness-50)]):
                workers = [w for w in building.available_workers if
                               check_stat_perc(w, "joy", .5) or
                               check_stat_perc(w, "agility", .3)]

                if workers:
                    worker = choice(workers)
                    if check_stat_perc(w, "joy", .5):
                        handle = "tired"
                    else:
                        handle = "sad"
                    temp0 = "\n{} noticed that {} looks a bit {}.".format(manager.nickname,
                                                    worker.nickname, handle)
                    temp1 = " Your manager cheered her up. {}".format(
                        set_font_color("(+10% Joy, +15% Vitality)", "lawngreen"))
                    log.append(temp0+temp1)

                    building.log("Your manager cheered up {}.".format(w.name))

                    mod_by_max(worker, "joy", .1)
                    mod_by_max(worker, "vitality", .15)
                    manager.jobpoints -= 10

            if env.now == 102:
                break

        points_used = init_jp-manager.jobpoints

        # Handle stats:
        if points_used > 100:
            log.logws("management", randint(1, 2))
            log.logws("intelligence", randrange(2))
            log.logws("refinement", 1)
            log.logws("character", 1)

            ap_used = (points_used)/100.0
            log.logws("exp", exp_reward(manager, building.tier, ap_used=ap_used))

        # finalize the log:
        log.img = manager.show("profile", resize=ND_IMAGE_SIZE, add_mood=True)
        log.event_type = "jobreport"
        log.after_job()
        NextDayEvents.append(log)

        building.mlog = None

    def mp_init_jp_bonus(manager, building, effectiveness, log):
        # Special bonus to JobPoints (aka pep talk) :D
        init_jp_bonus = (effectiveness-95.0)/100
        if init_jp_bonus < 0:
            init_jp_bonus = 0
        elif init_jp_bonus > .3: # Too much power otherwise...
            init_jp_bonus = .3
        elif init_jp_bonus < .05: # Less than 5% is absurd...
            init_jp_bonus = .05

        workers = building.available_workers
        if init_jp_bonus and workers:
            # Bonus to the maximum amount of workers:
            max_job_points = manager.jobpoints*.5
            per_worker = 10
            max_workers = round_int(max_job_points/per_worker)

            if len(workers) > max_workers:
                workers = random.sample(workers, max_workers)

            temp = "{} gave a nice motivational speech and approached some of the workers individually! ".format(manager.name)
            temp += ", ".join([w.name for w in workers])
            temp += " responded positively! "
            temp_p = "(+{}% Job Points)".format(round_int(init_jp_bonus*100))
            temp += set_font_color(temp_p, "lawngreen")
            log.append(temp)
            building.log("{} gave a motivational speech!".format(manager.name))

            init_jp_bonus += 1.0
            for w in workers:
                w.jobpoints = round_int(w.jobpoints*init_jp_bonus)
            manager.jobpoints -= len(workers)*per_worker
