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
