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
            self.base_stats = {"agility": 30, "constitution": 30}

        def traits_and_effects_effectiveness_mod(self, worker, log):
            """Affects worker's effectiveness during one turn. Should be added to effectiveness calculated by the function below.
               Calculates only once per turn, in the very beginning.
            """
            effectiveness = 0
             # effects always work
            if worker.effects['Food Poisoning']['active']:
                log.append("%s suffers from Food Poisoning, and is very far from her top shape." % worker.name)
                effectiveness -= 50
            elif worker.effects['Down with Cold']['active']:
                log.append("%s is not feeling well due to colds..." % worker.name)
                effectiveness -= 15

            if locked_dice(65): # traits don't always work, even with high amount of traits there are normal days when performance is not affected

                traits = list(i for i in worker.traits if i in ["Adventurous", "Homebody", "Neat", "Messy", "Shy", "Energetic"])
                if traits:
                    trait = random.choice(traits)
                else:
                    return effectiveness

                if trait == "Adventurous":
                    log.append("%s would prefer to explore dungeons and look for treasures rather than clean stuff..." % worker.name)
                    effectiveness -= 25
                elif trait == "Homebody":
                    log.append("%s really enjoys the simple and predictable cleaning task." % worker.name)
                    effectiveness += 25
                elif trait == "Neat":
                    log.append("%s diligently gets rid of even slightest traces of dirt. Refreshing to see someone who truly enjoys her work." % worker.name)
                    effectiveness += 40
                elif trait == "Messy":
                    log.append("%s reluctantly does her job, preferring to hide the dirt instead of cleaning it properly." % worker.name)
                    effectiveness += 40
                elif trait == "Shy":
                    log.append("%s appreciates the chance to have a job where her shyness doesn't get in the way." % worker.name)
                    effectiveness += 15
            return effectiveness

        def calculate_disposition_level(self, char): # calculating the needed level of disposition
            # TODO: Update for beta
            return 0

        def settle_workers_disposition(self, worker, log):
            # TODO: Update for beta
            pass
