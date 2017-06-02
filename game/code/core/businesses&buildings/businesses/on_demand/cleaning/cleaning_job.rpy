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
            self.skills = ["cleaning"]
            self.stats = ["agility"]

        def __call__(self, cleaners_original, cleaners, building, dirt, dirt_cleaned):
            self.all_workers = cleaners_original
            workers = cleaners
            self.loc = building
            self.dirt, self.dirt_cleaned = dirt, dirt_cleaned
            self.clean()

        def is_valid_for(self, char):
            if "Service" in worker.traits:
                return True
            if worker.status == 'slave':
                return True

            if worker.disposition >= self.calculate_disposition_level(char):
                return True
            else:
                return False

        def calculate_disposition_level(self, char): # calculating the needed level of disposition
            # sub = check_submissivity(char)
            # if "Shy" in worker.traits:
                # disposition = 800 + 50 * sub
            # else:
                # disposition = 700 + 50 * sub
            # if cgochar(char, "SIW"):
                # disposition -= 500
            # if "Exhibitionist" in worker.traits:
                # disposition -= 200
            # if "Nymphomaniac" in worker.traits:
                # disposition -= 50
            # elif "Frigid" in worker.traits:
                # disposition += 50
            # if check_lovers(char, hero):
                # disposition -= 50
            # elif check_friends(hero, char):
                # disposition -= 25
            # return disposition
            return 500

        def check_occupation(self, char=None):
            """Checks if the worker is willing to do this job.
            """
            return True # Don't want to mess with this atm.

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
