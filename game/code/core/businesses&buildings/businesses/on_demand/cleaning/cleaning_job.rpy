init -5 python:
    class CleaningJob(Job):
        def __init__(self):
            super(CleaningJob, self).__init__()
            self.id = "Cleaning"
            self.type = "Service"

            # Traits/Job-types associated with this job:
            self.occupations = ["Service"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Maid"]] # Corresponding traits...

            # Relevant skills and stats:
            self.base_skills = {"cleaning": 100}
            self.base_stats = {"agility": 100}

        def __call__(self, cleaners_original, cleaners, building, dirt, dirt_cleaned):
            self.all_workers = cleaners_original
            workers = cleaners
            self.loc = building
            self.dirt, self.dirt_cleaned = dirt, dirt_cleaned
            self.clean()

        def traits_and_effects_effectiveness_mod(self, worker, log):
            """Affects worker's effectiveness during one turn. Should be added to effectiveness calculated by the function below.
               Calculates only once per turn, in the very beginning.
            """
            # TODO: Update for beta
            return 0

        def calculate_disposition_level(self, char): # calculating the needed level of disposition
            # TODO: Update for beta
            return 0

        def settle_workers_disposition(self, worker, log):
            # TODO: Update for beta
            pass

        def clean(self):
            """Build a report for cleaning team effort.
            (Keep in mind that a single worker is also a posisbility here) <== Important when building texts.

            This one is simpler... it just logs the stats, picks an image and builds a report...
            """
            self.img = Fixed(xysize=(820, 705))
            self.img.add(Transform(self.loc.img, size=(820, 705)))
            vp = vp_or_fixed(self.all_workers, ["maid", "cleaning"], {"exclude": ["sex"], "resize": (150, 150), "type": "any"})
            self.img.add(Transform(vp, align=(.5, .9)))

            self.team = self.all_workers

            log = ["{} cleaned {} today!".format(", ".join([w.nickname for w in self.all_workers]), self.loc.name)]

            # Stat mods
            self.logloc('dirt', -self.dirt_cleaned)
            for w in self.all_workers:
                log.logws('vitality', -randint(15, 25), w)  # = ? What to do here?
                log.logws('exp', randint(15, 25), w) # = ? What to do here?
                if dice(33):
                    log.logws('service', 1, w) # = ? What to do here?
            # ... We prolly need to log how much dirt each individual worker is cleaning or how much wp is spent...
            self.event_type = "jobreport" # Come up with a new type for team reports?
            self.apply_stats()
            self.finish_job()
