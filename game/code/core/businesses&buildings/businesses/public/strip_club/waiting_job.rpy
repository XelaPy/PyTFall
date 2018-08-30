init -5 python:
    class Waiting(Job):
        def __init__(self):
            super(Waiting, self).__init__()
            """Dead Job ATM (Beta release)
            """
            self.id = "Waiting Job"
            self.type = "Service"

            # Traits/Job-types associated with this job:
            self.occupations = [] # General Strings likes SIW, Combatant, Server...
            self.occupation_traits = [] # Corresponding traits...
            self.aeq_purpose = 'Service'

            # Relevant skills and stats:
            self.skills = []
            self.stats = []

            workermod = {}
            self.locmod = {}

        def __call__(self, char):
            pass

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
            elif worker.effects['Drunk']['active']:
                log.append("%s is drunk, which affects her coordination. Not the best thing when you need to carry drinks and snacks." % worker.name)
                effectiveness -= 20
            elif worker.effects['Revealing Clothes']['active']:
                log.append("Her revealing clothes get a lot of the wrong kind of attention from drunk customers, interfering with work.")
                effectiveness -= 15

            if locked_dice(65): # traits don't always work, even with high amount of traits there are normal days when performance is not affected

                traits = list(i.id for i in worker.traits if i in ["Abnormally Large Boobs", "Aggressive", "Big Boobs", "Always Hungry", "Clumsy", "Great Arse", "Ill-mannered", "Long Legs", "Vicious", "Nerd", "Shy", "Masochist", "Psychic", "Natural Leader", "Scars", "Elegant", "Natural Follower", "Serious", "Optimist", "Small Boobs"])
                if traits:
                    trait = random.choice(traits)
                else:
                    return effectiveness

                if trait == "Abnormally Large Boobs":
                    log.append("When %s isn't getting hit on for her huge breasts, she is busy accidentally spilling drinks with those massive funbags." % worker.name)
                    effectiveness -= 40
                elif trait == "Aggressive":
                    log.append("A customer tried to hit on her and %s kicked him where it counts. It didn't help with keeping customers." % worker.name)
                    effectiveness -= 20
                elif trait == "Big Boobs":
                    log.append("%s always gets the attention of lecherous old men because of her boobs and hates every minute of it." % worker.name)
                    effectiveness -= 20
                elif trait == "Small Boobs":
                    log.append("Her small chest gets her ignored for the whole shift and %s gets to do her job in peace." % worker.name)
                    effectiveness += 40
                elif trait == "Always Hungry":
                    log.append("%s can't resist the smell of a customers food, biting off pieces in front of them." % worker.name)
                    effectiveness -= 25
                elif trait == "Clumsy":
                    log.append("The sound of shattering glasses and angry customers was heard throughout the shift...")
                    effectiveness -= 20
                elif trait == "Great Arse":
                    log.append("%s spends the entire shift with one customer or another trying to cop a feel of her ass, having trouble getting anything done." % worker.name)
                    effectiveness -= 20
                elif trait == "Long Legs":
                    log.append("Her sexy legs get a lot of the wrong kind of attention from drunk old men.")
                    effectiveness -= 20
                elif trait == "Ill-mannered":
                    log.append("%s constantly gets into an argument with customers over what they ordered, killing the mood." % worker.name)
                    effectiveness -= 20
                elif trait == "Vicious":
                    log.append("%s accidentally broke a glass on a customers face after he groped her." % worker.name)
                    effectiveness -= 20
                elif trait == "Nerd":
                    log.append("%s cannot carry a decent conversation with most of the patrons because she keeps going on about stuff they don't care about." % worker.name)
                    effectiveness -= 15
                elif trait == "Shy":
                    log.append("%s is too nervous to even approach customers for their orders, slowing down the business." % worker.name)
                    effectiveness -= 25
                elif trait == "Masochist":
                    log.append("The customers are especially bad to her today, but looks like %s enjoys it. Being treated like a piece of meat by a drunken customer is her idea of a good time." % worker.name)
                    effectiveness += 25
                elif trait == "Psychic":
                    log.append("%s deflects the customers' sexual harassment with ease and maintains a friendly air with them." % worker.name)
                    effectiveness += 35
                elif trait == "Natural Leader":
                    log.append("The customers are too charmed by her character to consider harassing her.")
                    effectiveness += 10
                elif trait == "Natural Follower":
                    log.append("The customers like %s because she is easy to order around." % worker.name)
                    effectiveness += 20
                elif trait == "Scars":
                    log.append("Her scars make the customers think twice about picking on her.")
                    effectiveness += 15
                elif trait == "Elegant":
                    log.append("%s gracefully evades customers' attempts to grope her.")
                    effectiveness += 20
                elif trait == "Serious":
                    log.append("Being a waitress isn't very fun, but %s makes the most of it and even enjoys talking to a few nice guys." % worker.name)
                    effectiveness += 10
                elif trait == "Optimist":
                    log.append("%s is genuinely fun for the customers to talk to and she plays along with their crude jokes." % worker.name)
                    effectiveness += 15
            return effectiveness

        def club_task(self):
            """
            Solve the job as a waitress.
            """
            clientsmax = self.APr * (2 + (worker.agility * .05 + worker.serviceskill * .05 + worker.refinement * .01))

            if self.loc.servicer['clubclientsleft'] - clientsmax <= 0:
                clientsserved = self.loc.servicer['clubclientsleft']
                log.append("She finished serving drinks and snacks to tables of %d remaining customers. At least she got a break.  \n"%self.loc.servicer['clubclientsleft'])
                self.loc.servicer['clubclientsleft'] -= clientsserved

            elif self.loc.servicer['clubclientsleft'] - clientsmax > 0:
                clientsserved = clientsmax
                log.append("She served snacks and drinks to tables of %d clients. \n"%(clientsmax))
                self.loc.servicer['clubclientsleft'] = self.loc.servicer['clubclientsleft'] - clientsserved

            clubfees = clientsserved * self.loc.rep * .08 + clientsserved * .5 * (worker.refinement * .1 + worker.charisma * .1 + worker.service * .025)
            tips = 0

            log.append("\n")

            # Skill Checks
            if worker.serviceskill > 2000:
                self.locmod['reputation'] += choice([0, 1])
                clubfees = clubfees * 1.5
                tips = clubfees * .10
                log.append("She is an excellent waitress, customers didn't notice how they've just kept spending their money as she offered them more and more house specials. \n")

            elif worker.serviceskill >= 1000:
                self.locmod['reputation'] += choice([0,0,0,1])
                clubfees = clubfees * 1.2
                tips = clubfees * .07
                log.append("Customers were pleased with such a skilled waitress serving them. \n")

            elif worker.serviceskill >= 500:
                tips = clubfees * .03
                self.locmod['reputation'] += choice([0,0,0,0,0,1])
                log.append("She was skillful enough not to mess anything up during her job. \n")

            elif worker.serviceskill >= 100:
                self.locmod['reputation'] += choice([0,0,-1,0,0,-1])
                clubfees = clubfees * .8
                log.append("Her performance was rather poor and it most definitely has cost you income. \n")

            if worker.charisma > 300:
                tips = tips + clubfees*.05
                self.locmod['fame'] += choice([0, 1, 1])
                log.append("Your girl was stunningly pretty, customers couldn't keep their eyes off her. \n")

            elif worker.charisma > 150:
                tips = tips + clubfees*.03
                self.locmod['fame'] += choice([0 ,0, 1])
                log.append("Your girl looked beautiful, this will not go unnoticed. \n")

            elif worker.charisma > 45:
                tips = tips + clubfees*.02
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
            clubfees = round_int(clubfees)
            tips = round_int(tips)

            log.append("{color=[gold]}%s earned %d Gold during this shift"%(worker.nickname, clubfees))

            if tips:
                log.append(" and got %d in tips" % tips)

            log.append(".{/color}\n")

            self.img = worker.show("bunny", "waitress", exclude=["sex"], resize=(740, 685), type="any")

            # Finances:
            worker.fin.log_logical_income(clubfees, "Waitress")
            worker.mod_flag("_jobs_tips", tips)

            self.apply_stats()
            self.finish_job()
