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
            self.desc = "Manages your business, helping workers in various ways and improving their performance"

            self.base_skills = {"management": 80, "refinement": 20}
            self.base_stats = {"character": 40, "intelligence": 60}

            self.allowed_status = ["free"]
