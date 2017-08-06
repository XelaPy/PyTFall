init -5 python:
    class Waiting(Job):
        def __init__(self):
            super(Waiting, self).__init__()
            self.id = "Waiting Job"
            self.type = "Service"

            # Traits/Job-types associated with this job:
            self.occupations = [] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [] # Corresponding traits...

            # Relevant skills and stats:
            self.skills = []
            self.stats = []

            workermod = {}
            self.locmod = {}

        def club_task(self):
            """
            Solve the job as a waitress.
            """
            clientsmax = self.APr * (2 + (worker.agility * 0.05 + worker.serviceskill * 0.05 + worker.refinement * 0.01))

            if self.loc.servicer['clubclientsleft'] - clientsmax <= 0:
                clientsserved = self.loc.servicer['clubclientsleft']
                log.append("She finished serving drinks and snacks to tables of %d remaining customers. At least she got a break.  \n"%self.loc.servicer['clubclientsleft'])
                self.loc.servicer['clubclientsleft'] -= clientsserved

            elif self.loc.servicer['clubclientsleft'] - clientsmax > 0:
                clientsserved = clientsmax
                log.append("She served snacks and drinks to tables of %d clients. \n"%(clientsmax))
                self.loc.servicer['clubclientsleft'] = self.loc.servicer['clubclientsleft'] - clientsserved

            clubfees = clientsserved * self.loc.rep * 0.08 + clientsserved * 0.5 * (worker.refinement * 0.1 + worker.charisma * 0.1 + worker.service * 0.025)
            tips = 0

            log.append("\n")

            # Skill Checks
            if worker.serviceskill > 2000:
                self.locmod['reputation'] += choice([0, 1])
                clubfees = clubfees * 1.5
                tips = clubfees * 0.10
                log.append("She is an excellent waitress, customers didn't notice how they've just kept spending their money as she offered them more and more house specials. \n")

            elif worker.serviceskill >= 1000:
                self.locmod['reputation'] += choice([0,0,0,1])
                clubfees = clubfees * 1.2
                tips = clubfees * 0.07
                log.append("Customers were pleased with such a skilled waitress serving them. \n")

            elif worker.serviceskill >= 500:
                tips = clubfees * 0.03
                self.locmod['reputation'] += choice([0,0,0,0,0,1])
                log.append("She was skillful enough not to mess anything up during her job. \n")

            elif worker.serviceskill >= 100:
                self.locmod['reputation'] += choice([0,0,-1,0,0,-1])
                clubfees = clubfees * 0.8
                log.append("Her performance was rather poor and it most definitely has cost you income. \n")

            if worker.charisma > 300:
                tips = tips + clubfees*0.05
                self.locmod['fame'] += choice([0, 1, 1])
                log.append("Your girl was stunningly pretty, customers couldn't keep their eyes off her. \n")

            elif worker.charisma > 150:
                tips = tips + clubfees*0.03
                self.locmod['fame'] += choice([0 ,0, 1])
                log.append("Your girl looked beautiful, this will not go unnoticed. \n")

            elif worker.charisma > 45:
                tips = tips + clubfees*0.02
                self.locmod['fame'] += choice([0, 0, 0, 1])
                log.append("Your girl was easy on the eyes, not bad for a bartender. \n")

            elif worker.charisma > 0:
                self.locmod['fame'] += choice([0, -1, -1])
                log.append("Customers did not appreciate a hag serving them. Consider sending this girl to a beauty school. \n")

            log.append("\n")

            # Stat Mods
            workermod['vitality'] -= clientsserved * 5
            workermod['service'] += choice([0, 0, 1]) * self.APr
            workermod['agility'] += choice([0, 0, 1]) * self.APr
            workermod['exp'] += self.APr * randint(15, 25)

            self.locmod['dirt'] += clientsserved * 6

            # Integers:
            clubfees = int(round(clubfees))
            tips = int(round(tips))

            log.append("{color=[gold]}%s earned %d Gold during this shift"%(worker.nickname, clubfees))

            if tips:
                log.append(" and got %d in tips" % tips)

            log.append(".{/color}\n")

            self.img = worker.show("bunny", "waitress", exclude=["sex"], resize=(740, 685), type="any")

            # Finances:
            worker.fin.log_logical_income(clubfees, "Waitress")
            worker.mod_flag("jobs_tips", tips)
            self.loc.fin.log_logical_income(clubfees + tips, "Waitress")

            self.apply_stats()
            self.finish_job()
