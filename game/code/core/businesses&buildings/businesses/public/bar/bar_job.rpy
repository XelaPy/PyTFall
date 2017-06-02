init -5 python:
    class BarJob(Job):
        def __init__(self):
            super(BarJob, self).__init__()
            self.id = "Bartending"
            self.type = "Service"

            # Traits/Job-types associated with this job:
            self.occupations = ["Server"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Bartender"]] # Corresponding traits...

            self.disposition_threshold = 750 # Any worker with disposition this high will be willing to do the job even without matched traits.

            # Relevant skills and stats:
            self.base_skills = {"bartending": 100}
            self.base_stats = {"charisma": 100}

        def traits_and_effects_effectiveness_mod(self, worker, log):
            # TODO, UPDATE FOR BETA!
            return 0

        def effectiveness(self, worker, difficulty, log):
            """
            difficulty is used to counter worker tier.
            100 is considered a score where worker does the task with acceptable performance.
            """
            base_effectiveness = super(BarJob, self).effectiveness(worker, difficulty, log)

            # Do whatever has to be done for the job:
            effectiveness = base_effectiveness + 0

            return effectiveness

        def calculate_disposition_level(self, worker):
            """
            calculating the needed level of disposition;
            since it's whoring we talking about, values are really close to max,
            or even higher than max in some cases, making it impossible
            """
            # TODO: UPDATE FOR BETA!
            sub = check_submissivity(worker)
            if "Shy" in worker.traits:
                disposition = 800 + 50 * sub
            else:
                disposition = 700 + 50 * sub
            if cgochar(worker, "SIW"):
                disposition -= 500
            if "Exhibitionist" in worker.traits:
                disposition -= 200
            if "Nymphomaniac" in worker.traits:
                disposition -= 50
            elif "Frigid" in worker.traits:
                disposition += 50
            if check_lovers(hero, worker):
                disposition -= 50
            elif check_friends(hero, worker):
                disposition -= 25
            return disposition

        def settle_workers_disposition(self, worker, log):
            """
            handles penalties in case of wrong job
            """
            # Formerly check_occupation
            # TODO: UPDATE FOR BETA! (This version lools really old)
            if not [t for t in self.all_occs if t in worker.occupations]:
                if worker.status == 'slave':
                    temp = choice(["%s has no choice but to agree to tend the bar."%worker.fullname,
                                            "She'll tend the bar for customer, does not mean she'll enjoy it.",
                                            "%s is a slave so she'll do as she is told. However you might want to consider giving her work fit to her profession."%worker.name])
                    worker.set_flag("jobs_barintro", temp)
                    worker.set_flag("jobs_introjoy", -3)

                elif worker.disposition < 800:
                    temp = choice(["%s refused to serve! It's not what she wishes to do in life."%worker.name,
                                             "%s will not work as a Service Girl, find better suited task for her!"%worker.fullname])
                    temp = set_font_color(temp, "red")
                    log.append(temp)

                    worker = char
                    self.loc = worker.location
                    self.event_type = "jobreport"

                    log.logws('disposition', -50)
                    self.img = worker.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                    worker.action = None

                    # self.apply_stats()
                    # self.finish_job()
                    # return False

                else: # worker.disposition > 800:
                    temp = "%s reluctantly agreed to be a servicer. It's not what she wishes to do in life but she admires you to much to refuse. " % worker.name
                    worker.set_flag("jobs_barintro", temp)

            else:
                temp = choice(["%s will work as a Bartender!"%worker.name,
                                         "Tending the Bar:"])
                worker.set_flag("jobs_barintro", temp)
            return True

        def check_occupation(self, char):
            """Checks the workers occupation against the job.
            """
            if not [t for t in self.all_occs if t in worker.occupations]:
                if worker.status == 'slave':
                    temp = choice(["%s has no choice but to agree to tend the bar."%worker.fullname,
                                            "She'll tend the bar for customer, does not mean she'll enjoy it.",
                                            "%s is a slave so she'll do as she is told. However you might want to consider giving her work fit to her profession."%worker.name])
                    worker.set_flag("jobs_barintro", temp)
                    worker.set_flag("jobs_introjoy", -3)

                elif worker.disposition < 800:
                    temp = choice(["%s refused to serve! It's not what she wishes to do in life."%worker.name,
                                             "%s will not work as a Service Girl, find better suited task for her!"%worker.fullname])
                    temp = set_font_color(temp, "red")
                    log.append(temp)

                    worker = char
                    self.loc = worker.location
                    self.event_type = "jobreport"

                    log.logws('disposition', -50)
                    self.img = worker.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                    worker.action = None

                    self.apply_stats()
                    self.finish_job()
                    return False

                else: # worker.disposition > 800:
                    temp = "%s reluctantly agreed to be a servicer. It's not what she wishes to do in life but she admires you to much to refuse. " % worker.name
                    worker.set_flag("jobs_barintro", temp)

            else:
                temp = choice(["%s will work as a Bartender!"%worker.name,
                                         "Tending the Bar:"])
                worker.set_flag("jobs_barintro", temp)
            return True

        def bar_task(self, worker, clients, loc, log):

            len_clients = len(clients)

            serviceskill = worker.get_skill("bartending")
            charisma = worker.charisma

            # Skill checks
            if serviceskill > 2000:
                log.logloc('reputation', choice([0, 1, 2]))
                log.append("She was an excellent bartender, customers kept spending their money just for the pleasure of her company. \n")

            elif serviceskill >= 1000:
                log.logloc('reputation', choice([0, 1]))
                log.append("Customers were pleased with her company and kept asking for more booze. \n")

            elif serviceskill >= 500:
                log.logloc('reputation', choice([0, 0, 0, 0, 0, 1]))
                log.append("She was skillful enough not to mess anything up during her job. \n")

            elif serviceskill >= 100:
                log.logloc('reputation', -1)
                log.append("Her performance was rather poor and it most definitely has cost you income. \n")

            else:
                log.logloc('reputation', -2)
                log.append("She is a very unskilled bartender, this girl definitely needs training \n")

            if charisma > 300:
                log.logloc('fame', choice([0,1,1]))
                log.append("Your girl was stunningly pretty, customers couldn't keep their eyes off her. \n")

            elif charisma > 150:
                log.logloc('fame', choice([0,0,1]))
                log.append("Your girl looked beautiful, this will not go unnoticed. \n")

            elif charisma > 45:
                log.logloc('fame', choice([0, 0, 0, 1]))
                log.append("Your girl was easy on the eyes, not bad for a bartender. \n")

            else:
                log.logloc('fame', -2)
                log.append("Customers did not appreciate a hag serving them. Consider sending this girl to a beauty school. \n")

            log.append("\n")

            #Stat Mods
            log.logws('exp', randint(15, 25))
            log.logws('bartending', choice([1, 2]))
            log.logws('refinement', choice([0, 0, 0, 1]))
            log.logws('vitality', len_clients * -3)

            # Integers:
            # barfees = int(round(worker.earned_cash))
            # tips = int(round(worker.flag("jobs_" + self.id + "_tips")))
            #
            # if tips:
            #     log.append("She got %d in tips! " % tips)

            if worker.has_image("waitress", exclude=["sex"]):
                log.img = worker.show("waitress", exclude=["sex"], resize=(740, 685))
            elif worker.has_image("maid", exclude=["sex"]):
                log.img = worker.show("maid", exclude=["sex"], resize=(740, 685))
            else:
                log.img = worker.show("profile", exclude=["sex", "nude"], resize=(740, 685))

            # Finances:
            # worker.fin.log_logical_income(barfees, "Barmaid")
            # if tips:
            #     worker.mod_flag("jobs_tips", tips)

            # self.loc.fin.log_logical_income(tips, "Barmaid")
            #
            # self.apply_stats()
            # self.finish_job()
