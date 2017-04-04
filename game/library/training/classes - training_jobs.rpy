init python:
    ##################################################################################################
    # Training Jobs
    # Presently used mostly in schools. Normal Jobs will be recoded before Beta, these jobs will be updated soon afterwards...
    class TrainingJobParent(_object):
        """ Baseclass for jobs and other next day actions with some defaults.

        - Older class used with Schools and Training.
        """
        def __init__(self, girl=None, girls=None, loc=None, event_type="jobreport"):
            """Creates a new Job.

            girl = The girl doing the job.
            girls = A container with all the girls. (May not be useful anymore)
            """
            self.id = "Base Job"
            self.girls = girls
            self.girl = girl
            self.girlmod = {} # Logging all stats/skills changed during the job.

            self.loc = loc
            self.locmod = {}

            # Traits/Job-types associated with this job:
            self.occupations = list() # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = list() # Corresponing traits...

            self.txt = list()
            self.img = ""
            self.finished = False

            self.flag_red = False
            self.flag_green = False

            self.event_type = event_type

        def __call__(self, girl, girls, loc=None, event_type="jobreport"):
            self.girl = girl
            self.girls = girls
            self.loc = loc
            self.event_type = event_type

            self.finished = False

        def __str__(self):
            return str(self.id)

        def reset(self):
            self.girl = None
            self.loc = None
            self.client = None
            self.event_type = None
            self.finished = False
            self.txt = list()
            self.img = ""

            self.flag_red = False
            self.flag_green = False

            self.girlmod = {}
            self.locmod = {}


        @property
        def all_occs(self):
            # All Occupations:
            return set(self.occupations + self.occupation_traits)

        def get_clients(self):
            # This returns a correct amount of clients used for the job
            return 0

        def create_event(self):
            """
            Returns an event depicting the current state of this job.
            """
            if isinstance(self.txt, (list, tuple)):
                try:
                    self.txt = "".join(self.txt)
                except TypeError:
                    self.txt = "".join(str(i) for i in self.txt)

            return NDEvent(type=self.event_type,
                                 img=self.img,
                                 txt=self.txt,
                                 char=self.girl,
                                 charmod=self.girlmod,
                                 loc=self.loc,
                                 locmod=self.locmod,
                                 green_flag=self.flag_green,
                                 red_flag=self.flag_red)

        def check_occupation(self, char=None):
            """
            Checks the girls occupation.
            """
            return True

        def check_life(self):
            """
            Checks whether the girl is alive.
            Might be deprecated, needs updating.
            """
            if not self.girl.alive:
                self.txt.append("%s is dead. \n"%self.girl.fullname)
                self.girls.remove(self.girl)
                self.img = im.Sepia(self.girl.show('profile'), resize=(740, 685))
                self.finish_job()

        def finish_job(self):
            """
            Finish the job and adds it to NextDayEvents.
            """
            self.finished = True
            NextDayEvents.append(self.create_event())

            # Reset all attrs:
            # Redundant?
            self.girlmod = {}
            self.locmod = {}
            self.txt = list()
            self.img = ""
            self.flag_red = False
            self.flag_green = False

        def check_injury(self):
            """Checks whether the girl is injured and sets her to auto rest.
            """
            if self.girl.health < self.girl.get_max("health")*0.25:
                self.txt.append("%s is injured and in need of medical attention! "%self.girl.name)
                self.img = self.girl.show("profile", "sad", resize=(740, 685))

                if self.girl.autocontrol['Rest']:
                    self.girl.previousaction = self.girl.action
                    self.girl.action = 'AutoRest'
                    self.txt.append("She is going to take few days off to heal her wounds. ")

                self.girls.remove(self.girl)
                self.finish_job()

        def check_vitality(self):
            """
            Checks whether the girl is tired and sets her to auto rest.
            """
            if self.girl.vitality < 30:
                self.txt.append("%s is to tired to work today! "%self.girl.name)
                self.img = self.girl.show("profile", "sad", resize=(740, 685))

                if self.girl.autocontrol['Rest']:
                    self.girl.previousaction = self.girl.action
                    self.girl.action = 'AutoRest'
                    self.txt.append("She's going to take few days off to recover her stamina. ")

                self.girls.remove(self.girl)
                self.finish_job()

        def apply_stats(self):
            """
            Applies the stat changes generated by this job to the girl.
            """
            for stat in self.girlmod:
                if stat == "exp":
                    self.girlmod[stat] = self.girl.adjust_exp(self.girlmod[stat])
                    self.girl.exp += self.girlmod[stat]

                # After a long conversation with Dark and CW, we've decided to prevent girls dieing during jobs
                # I am leaving the code I wrote before that decision was reached in case
                # we change our minds or add jobs like exploration where it makes more sense.
                # On the other hand just ignoring it is bad, so let's at least reduce some stuff, pretending that she lost consciousness for example.
                elif stat == 'health' and (self.girl.health + self.girlmod[stat]) <= 0:
                    self.girl.health = 1
                    if self.girl.constitution > 5:
                        self.girl.constitution -= 5

                else:
                    if self.girl.stats.is_stat(stat):
                        self.girl.mod_stat(stat, self.girlmod[stat])

                    elif self.girl.stats.is_skill(stat):
                        self.girl.mod_stat(stat, self.girlmod[stat])

            for stat in self.locmod:
                if stat == 'fame':
                    self.loc.modfame(self.locmod[stat])

                elif stat == 'dirt':
                    if self.locmod[stat] < 0:
                        self.loc.clean(-self.locmod[stat])

                    else:
                        self.loc.dirt += self.locmod[stat]

                elif stat == 'reputation':
                    self.loc.modrep(self.locmod[stat])

                else:
                    raise Exception("Stat: {} does not exits for Businesses".format(stat))

        def auto_clean(self):
            """
            Auto cleans the building if needed.
            """
            if isinstance(self.loc, DirtyBuilding):
                if self.loc.auto_clean and self.loc.get_dirt_percentage()[0] > 80:
                    price = self.loc.get_cleaning_price()
                    if hero.take_money(price, reason="Pro-Cleaning"):
                        self.loc.fin.log_expense(price, "Pro-Cleaning")
                        self.loc.dirt = 0
                        self.txt.append("Cleaners were hired to tidy up your building. Cost: {color=[gold]} %s Gold.{/color}\n\n"%price)

                    else:
                        self.txt.append("You did not have enough funds to pay for the professional cleaning service (%d Gold).\n\n"%price)

        def check_dirt(self):
            """
            Checks the dirt for the building and reports it.
            """
            if isinstance(self.loc, DirtyBuilding):
                if self.loc.get_dirt_percentage()[0] > 80:
                    self.txt.append(choice(["Your building looks like a pigstall, fix this or keep losing your clients!",
                                                         "Your building is to dirty to do business!",
                                                         "Clean your damn establishment or keep losing money and rep!"]))

                    if dice(self.loc.get_dirt_percentage()[0]):
                        self.locmod["reputation"] -= randint(2, 5)

                    self.apply_stats()
                    self.img = self.girl.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                    self.finish_job()

                    return True

                else:
                    return False

            else:
                return False

        def loggs(self, s, value):
            # Logs girls stat/skill to a dict:
            self.girlmod[s] = self.girlmod.get(s, 0) + value

        def logloc(self, s, value):
            # Logs a stat for the building:
            self.locmod[s] = self.girlmod.get(s, 0) + value


    class SchoolGuardJob(TrainingJobParent):
        """
        A job for girls that are guarding a school or dungeon.
        """

        def __init__(self, girl, loc, girls):
            """
            Creates a new SchoolGuardJob.
            girl = The girl that is doing the guarding.
            loc = The location of the training (school, house, etc).
            girls = The list of girls guarding in total.
            """
            super(SchoolGuardJob, self).__init__(girl, girls, loc=loc, event_type="schoolreport")

            self.girlmod["attack"] = 0
            self.girlmod["defence"] = 0
            self.girlmod["joy"] = 0
            self.girlmod["exp"] = 0
            self.girlmod["vitality"] = 0

            # Can we guard?
            self.check_life()
            if not self.finished: self.check_injury()
            if not self.finished: self.check_vitality()

            # Successfuly guarding?
            if not self.finished: self.check_success()

            # Do job
            if not self.finished:
                self.get_events()
                self.post_job_activities()

                self.apply_stats()
                self.girls.remove(self.girl)
                self.finish_job()

        def check_success(self):
            """
            Whether the girl can guard.
            """
            if self.girl.AP == 0:
                self.txt.append("%s was exhausted and couldn't do any guarding today! \n"%self.girl.name)
                self.flag_red = True
                self.girls.remove(self.girl)
                self.finish_job()

            else:
                # Catch all incase of no events
                self.txt.append("%s spent her day guarding. \n"%self.girl.name)

        def get_events(self):
            """
            Reponds to events generated by the girls.
            """
            amount = guard_escape_event.count(self.girl)
            if amount:
                self.txt.append("%d %s tried to escape today. \n"%(amount, plural("slave", amount)))

                win = guard_escape_event.win(self.girl)
                loss = guard_escape_event.loss(self.girl)

                self.girlmod = guard_escape_event.stats(self.girl)

                if win:
                    ww = "was" if win == 1 else "were"
                    self.txt.append("{color=[green]}%d %s %s successfully stopped with %s's help. {/color}\n"%(win, plural("slave", win), ww, self.girl.nickname))

                if loss:
                    self.txt.append("{color=[red]}%s and the rest of the guards were unable to prevent %d %s from escaping. {/color}\n"%(loss, plural("slave", loss), self.girl.nickname))

                guard_escape_event.reset(self.girl)

        def post_job_activities(self):
            """
            General activities for excess AP.
            """
            if self.loc.get_upgrade_mod("Security") >= 3:
                if dice(50):
                    self.txt.append("%s spent the remainder of her time relaxing in the Guard House. \n"%self.girl.name)
                    self.girlmod['vitality'] = randint(15, 20) * self.girl.AP

                else:
                    self.txt.append("%s spent the remainder of her time doing some simple training in the Guard House. \n"%self.girl.name)
                    self.girlmod['attack'] = choice([0,0,0,0,1])
                    self.girlmod['defence'] = choice([0,0,0,0,1])
                    self.girlmod['joy'] = choice([0,1,1,1])
                    self.girlmod['exp'] = randint(15, 25)
                    self.girlmod['vitality'] = randint(15, 20)

            self.girl.AP = 0


    class TrainerJob(TrainingJobParent):
        """
        A job for girls that are training others.
        """

        def __init__(self, girl, loc, girls):
            """
            Creates a new TrainerJob.
            girl = The girl that is doing the training.
            loc = The location of the training (school, house, etc).
            girls = The list of girls being trained in total.
            """
            super(TrainerJob, self).__init__(girl, girls, loc=loc, event_type="schoolreport")

            # Are we the player?
            self.you = girl is hero

            # The amount of AP we spent today
            self.girlAP = trainer_ap_for_girl(self.girl)

            # Whether we can train
            self.check_success()

            # Do training
            if not self.finished:
                # Clear flags
                trainer_obey_event.reset(self.girl)
                trainer_disobey_event.reset(self.girl)
                training_ap_cost.clear(self.girl)

                self.get_events()
                self.post_job_activities()

                self.apply_stats()
                self.girls.remove(self.girl)
                self.finish_job()

        def check_success(self):
            """
            Whether the girl can perform her job.
            """
            if self.girlAP < 0:
                if self.you: self.txt.append("{color=[red]}You couldn't train everyone you wanted as your workload is too high!{/color} \n")
                else: self.txt.append("{color=[red]}%s couldn't train everyone assigned to her as her workload is too high!{/color} \n"%self.girl.name)
                self.red_flag = True

            else:
                if self.you: self.txt.append("You spent the day training your girls. \n")
                else: self.txt.append("%s spent the day training your girls. \n"%self.girl.name)

        def get_events(self):
            """
            Responds to events generated by the girls.
            """
            yw = "you were" if self.you else "%s was"%self.girl.nickname

            girls = girls_training_with(self.girl)
            ogn = len(girls)

            # If we have obey events
            if trainer_obey_event.count(self.girl):
                ogirls = trainer_obey_event.helped(self.girl)

                if len(ogirls) == 1:
                    self.txt.append("{color=[lawngreen]}With the help of the facilities %s able to get %s to be obedient and pay attention.{/color} \n"%(yw, ogirls[0].fullname))

                else:
                    self.txt.append("{color=[lawngreen]}With the help of the facilities %s able to get the following girls to be obedient and pay attention:{/color} \n"%yw)

                    if len(ogirls) == 2:
                        self.txt.append("%s and %s. \n"%(ogirls[0].fullname, ogirls[1].fullname))

                    else:
                        for g in ogirls[:-1]:
                            self.txt.append("%s, "%g.fullname)

                        self.txt.append("and %s. \n"%ogirls[-1].fullname)

                self.txt.append("\n")

                for g in ogirls:
                    girls.remove(g)

            # If we have disobey events
            if trainer_disobey_event.count(self.girl):
                girls = trainer_diboey_event.against(self.girl)

                self.txt.append("%d of the girls trained attempted to disobey during their trainind. \n"%len(ogirls))

                if trainer_disobey_event.win(self.girl) > 0:
                    if trainer_disobey_event.loss(self.girl) > 0:
                        self.txt.append("{color=[red]}%s not able to prevent %d{/color}, {color=[lawngreen]}but managed to stop %d.{/color} \n"%(yw,
                                                                                                                                                 trainer_disobey_event.win(self.girl),
                                                                                                                                                 trainer_disobey_event.loss(self.girl)))

                    else:
                        self.txt.append("{color=[lawngreen]}%s able to prevent them.{/color} \n"%yw)

                else:
                    if trainer_disobey_event.loss(self.girl) > 0:
                        self.txt.append("{color=[red]}%s not able to prevent them.{/color} \n"%yw)

                if len(ogirls) == 1:
                    self.txt.append("%s disobeyed. \n"%ogirls[0].fullname)

                elif len(ogirls) == 2:
                    self.txt.append("%s and %s disobeyed. \n"%ogirls[0].fullname, ogirls[1].fullname)

                else:
                    self.txt.append("The following girls disobeyed: \n")

                    if len(ogirls) == 2:
                        for g in ogirls[:-1]:
                            self.txt.append("%s, "%g.fullname)

                        self.txt.append("and %s. \n"%ogirls[-1].fullname)

                self.txt.append("\n")

                for g in ogirls:
                    girls.remove(g)

            # Left overs
            if girls:
                yw = "You" if self.you else self.girl.pronoun

                if ogn != len(girls): self.txt.append("%s also trained "%yw)
                else: self.txt.append("%s trained "%yw)

                if len(girls) == 1:
                    self.txt.append("%s. \n"%girls[0].fullname)

                elif len(girls) == 2:
                    self.txt.append("%s and %s. \n"%(girls[0].fullname, girls[1].fullname))

                else:
                    for g in girls[-1]:
                        self.txt.append("%s, "%g.fullname)

                    self.txt.append("and %s."%girls[-1].fullname)

                self.txt.append("\n")

        def post_job_activities(self):
            """
            General activities for excess AP.
            """
            if not self.you:
                if self.loc.get_upgrade_mod("Punishments") >= 3 and self.stopped > 0:
                    self.txt.append("%s blew off some steam by using the disobedient girls for her own pleasure. \n"%self.girl.name)
                    self.girlmod["joy"] += choice([1,1,1,2,2,3])

                if self.loc.get_upgrade_mod("Trainers") >= 1 and self.girlAP >= 0:
                    self.txt.append("%s spent the remainder of her time resting in her personal room."%self.girl.name)
                    self.girlmod['vitality'] = randint(15, 25) * self.girl.AP

                else:
                    self.girlmod["vitality"] = -(randint(15, 25) * self.girl.AP)

            self.girlmod["exp"] = self.girl.AP * randint(15, 25)
            self.girl.AP = 0


    class TrainingJobFlags(_object):
        """
        Class that contains the check_success flags.
        """

        # Flag for when the training went normally.
        NORMAL = "normal"

        # Flag for when the girl obeyed.
        OBEY = "obey"

        # Flag for when the girl disobeyed.
        DISOBEY = "disobey"

        # Flag for when the girl refuses the trainer.
        STOP = "stop"

        # Flag for when the girl runs away.
        RUNAWAY = "runaway"

        # Flag for when the girl has no ap to complete the course.
        GIRL_AP = 0

        # Flag for when the trainer has no ap to complete the course.
        HERO_AP = 1

        # Flag for when the hero can't afford the gold.
        NO_GOLD = 2

        # Flag for when the trainer isn't good (not used outside of Job classes).
        BAD_TRAINER = 3


    class TrainingJob(TrainingJobParent):
        """
        A job for girls that are training, either in schools or with assigned trainers.
        """

        def __init__(self, girl, loc, girls, course=None, trainer=None):
            """
            Creates a new TrainingJob.
            girl = The girl that is doing the training.
            loc = The location of the training (school, house, etc).
            girls = The list of girls being trained in total.
            """
            super(TrainingJob, self).__init__(girl, girls, loc=loc, event_type="schoolreport")

            # Get needed stats
            self.course = course or char_is_training(self.girl)
            self.trainer = trainer or girl_training_with(self.girl)

            # The chance that the girl will get an effect from the training
            self.teachingchance = self.course.trainerSkill(self.trainer)

            # The maximum skill/stat can be raised to
            self.maxskill = self.course.trainerKnowledge(self.trainer)

            # If dungeon, get upgrades
            if not self.loc.is_school:
                # rewards upgrades / total
                # 0   > chance = low chance
                # 0.5 > chance = medium chance
                # 1   > chance = high chance
                #
                self.obey = self.loc.mod_obey() + girl_training_trait_mult(self.girl, "Easy to Reward")

                # punishments upgrades / total
                # 0   < chance = high chance
                # 0.5 < chance = medium chance
                # 1   < chance = low chance
                #
                self.disobey = self.loc.mod_disobey() + girl_training_trait_mult(self.girl, "Easy to Punish")

                # security upgrades / total
                # 0   < chance = high chance
                # 0.5 < chance = medium chance
                # 1   < chance = low chance
                #
                self.runaway = pytfall.ra.location_runaway(self.loc) # girl_training_trait_mult done in can_escape call

                # security_rating / 1000
                # 2 - 0   = 2, high chance
                # 2 - 0.5 = 1.5, medium chance
                # 2 - 1   = 1, low chance
                #
                self.chance = pytfall.ra.location_security(self.loc)

                # equipment upgrades / total
                self.expmod = self.loc.mod_exp()

                # trainer upgrades / total
                self.teachingchance += (self.teachingchance*0.25) * self.loc.mod_skill()
                self.maxskill += (self.maxskill*0.25) * self.loc.mod_skill()

            # If school, ignore
            else:
                self.obey = 0
                self.disobey = 0
                self.runaway = 0
                self.expmod = 0
                self.chance = 0


            # Debugging info
            if config.developer and False:
                self.txt.extend(["{color=[blue]}",
                                 "Girl: %s\n"%self.girl,
                                 "Trainer: %s\n"%("You" if self.trainer is hero else self.trainer),
                                 "Course: %s - %s\n"%(self.course.type, self.course.name),
                                 "Security: %s\n"%(self.loc.security_mult() if not self.loc.is_school else "n/a"),
                                 "Chance: %s\n"%self.chance,
                                 "Obey: %s (%s)\n"%(self.obey, girl_training_trait_mult(self.girl, "Easy to Reward")),
                                 "Disobey: %s (%s)\n"%(self.disobey, girl_training_trait_mult(self.girl, "Easy to Punish")),
                                 "Runaway: %s (%s)\n"%(self.runaway, girl_training_trait_mult(self.girl, "Restrained")),
                                 "{/color}"])

            # Check for refusals first:
            self.check_success()

            # Now go to courses
            if not self.finished:
                self.do_course(self.course.doNum)
                self.loc.log_income(self.girl, self.course.gold)

                exp = self.course.get_exp(self.trainer)
                exp += (exp*0.25) * self.expmod

                self.girlmod["exp"] = self.girl.adjust_exp(exp)

                self.apply_stats()
                self.rg()
                self.finish_job()

            try:
                self.course.chars[str(self.girl)] += 1

            except KeyError:
                devlog.error("TrainingJob.__init__ cannot increase girl (%s) training amount in course %s."%(self.girl.id, self.course.action))

        def check_success(self):
            """
            Checks that the girl succeeded at the training.
            """
            ##### AP AND GOLD

            # Check for girl AP
            if self.course.AP > 0:
                if self.girl.AP < self.course.AP:
                    self.txt.append("%s couldn't attend the %s as she didn't have enough AP! \n"%(self.girl.name, self.course.action))
                    self.rg()
                    self.finish_job()
                    return TrainingJobFlags.GIRL_AP

            # Check for trainer AP
            if self.trainer is not None:
                # Lower trainer AP
                training_ap_cost.set(self.trainer, self.trainer.baseAP if self.course.heroAP == -1 else self.course.heroAP, True)

                # If there is no AP left
                if trainer_ap_for_girl(self.trainer) < 0:
                    self.txt.append("%s couldn't attend the %s as her trainer %s didn't have enough AP! \n"%(self.girl.name, self.course.action, self.trainer.name))
                    self.rg()
                    self.finish_job()
                    return TrainingJobFlags.HERO_AP

            elif not self.course.is_schooling:
                # This catch is for if non-school lessons don't have trainers
                self.txt.append("%s couldn't attend the %s as she didn't have a trainer assigned! \n"%(self.girl.name, self.course.action))
                self.rg()
                self.finish_job()
                return TrainingJobFlags.HERO_AP

            # Check for gold
            if hero.gold < self.course.gold:
                self.txt.append("%s couldn't attend the %s as you couldn't afford to send her! \n"%(self.girl.name, self.course.action))
                self.rg()
                self.finish_job()
                return TrainingJobFlags.NO_GOLD

            ##### BAD TRAINERS
            bad = False

            # Schools don't have assigned trainers
            if not self.course.is_schooling:
                # If the girl isn't broken
                if not girl_is_broken(self.girl):

                    # Check for trainer/girl slave/free relationship
                    if self.trainer.status == "slave":
                        if not girl_is_broken(self.girl) and self.girl.disposition < 500:
                            self.txt.append("%s was too disgusted at %s's mental state to be eager to train. \n"%(self.girl.name, self.trainer.name))
                            bad = True

                    if not bad and self.trainer is not hero:
                        ownSkill = self.course.trainerSkill(self.girl) * 0.8
                        ownMax = self.course.trainerKnowledge(self.girl) * 0.8

                        # If the girl is better then the trainer
                        if ownSkill > self.teachingchance and ownMax > self.maxskill:
                            self.txt.append("%s wasn't happy that she already know more then her trainer, %s. \n"%(self.girl.name, self.trainer.name))
                            bad = True

            # If the trainer is bad
            if bad:
                flag = TrainingJobFlags.BAD_TRAINER

                if TrainingJobFlags.BAD_TRAINER in self.course.succeed:
                    _, message = self.course.succeed[TrainingJobFlags.BAD_TRAINER]

                else:
                    message = None

            else:
                # Get the success
                flag, message = self.course.get_success(self.girl)
                if flag is None: flag = TrainingJobFlags.NORMAL

                # Debugging info
                if config.developer and False:
                    self.txt.append("{color=[blue]}Flag: %s\n{/color}"%str(flag))

            ##### SUCCESS STATE

            # Post message
            if message is not None:
                if "%s" in message: message = message.replace("%s", self.girl.name) # Fuzzy interpolation
                if message.endswith("\n"): self.txt.append(message)
                else: self.txt.append(message + "\n")

            # Generic failure, (triggers disobey)
            if flag == TrainingJobFlags.DISOBEY:
                # If girl successfully disobeys
                if self.disobey < self.chance:
                    # Girl, trainer and school flags
                    girl_disobeys.set(self.girl, 1, True)
                    self.loc.events_relay["disobey"][0] += 1
                    if self.trainer is not None:
                        trainer_disobey_event.count(self.trainer, 1)
                        trainer_disobey_event.against(self.trainer, [self.girl])
                        trainer_disobey_event.loss(self.trainer, 1)

                    # End
                    self.rg()
                    self.finish_job()
                    return TrainingJobFlags.DISOBEY

                # Else, continue lesson
                else:
                    self.txt.append("However she was stopped by the trainer thanks to the equipment and facilities, and her lesson continued. \n")

                    # Girl, trainer and school flags
                    girl_disobeys.set(self.girl, 1, True)
                    self.loc.events_relay["disobey"][1] += 1
                    if self.trainer is not None:
                        trainer_disobey_event.count(self.trainer, 1)
                        trainer_disobey_event.against(self.trainer, [self.girl])
                        trainer_disobey_event.win(self.trainer, 1)

                    # Stats
                    self.girlmod["joy"] = -2
                    self.girlmod["disposition"] = -10

                    return TrainingJobFlags.NORMAL

            # Critial failure for free girls, (stop course)
            elif flag == TrainingJobFlags.STOP or (flag == TrainingJobFlags.BAD_TRAINER and self.girl.status == "free"):
                # Auto-success
                girl_disobeys.set(self.girl, 1, True)
                self.loc.events_relay["runaway"][0] += 1

                # End
                stop_training(self.girl)
                self.rg()
                self.finish_job()
                return flag

            # Critical failure for slave girls, (runaway)
            elif flag == TrainingJobFlags.RUNAWAY or (flag == TrainingJobFlags.BAD_TRAINER and self.girl.status == "slave"):
                result, by = pytfall.ra.can_escape(self.girl, self.loc, self.girlmod, use_be=self.girl.status == "slave")

                if by == RunawayManager.CAUGHT: self.txt.append("She surrendered to the guards when they chanellenged her. \n")
                elif by == RunawayManager.DEFEATED: self.txt.append("She was captured by the guards after a brief fight. \n")
                elif by == RunawayManager.FOUGHT: self.txt.append("She managed to escape after defeating the guards in a fight! \n")
                elif by == RunawayManager.ESCAPED: self.txt.append("She managed to slip out undetected! \n")

                # If girl successfully runs away
                if result:
                    pytfall.ra.add(self.girl)
                    self.loc.events_relay["runaway"][0] += 1

                    # End
                    stop_training(self.girl)
                    self.rg()
                    self.finish_job()
                    return flag

                # Else, continue lesson
                else:
                    # Girl and school flags
                    girl_disobeys.set(self.girl, 2, True)
                    self.loc.events_relay["runaway"][1] += 1

                    # Stats
                    self.girlmod["joy"] = -3
                    self.girlmod["disposition"] = -10

                    return TrainingJobFlags.NORMAL

            # Generic success, (triggers obey)
            elif flag == TrainingJobFlags.OBEY:
                girl_obeys.set(self.girl, 1, True)
                self.loc.events_relay["obey"][0] += 1
                if self.trainer is not None:
                    trainer_obey_event.count(self.trainer, 1)
                    trainer_obey_event.helped(self.trainer, [self.girl])

                return TrainingJobFlags.OBEY

            # If no flag
            elif flag == TrainingJobFlags.NORMAL:
                # If girl successfully obeys
                if self.obey > self.chance:
                    self.txt.append("%s did extra well today thanks to the equipment and facilities. \n"%self.girl.name)

                    # Girl and school flags
                    girl_obeys.set(self.girl, 1, True)
                    self.loc.events_relay["obey"][1] += 1

                    # Stats
                    self.girlmod["joy"] = 2
                    self.girlmod["disposition"] = 10

                    return TrainingJobFlags.OBEY

                else:
                    return TrainingJobFlags.NORMAL

        def do_course(self, amount=0):
            """
            Solves all the training logic.
            amount = The amount of times to 'do' the training. 0 = till the girl has no ap left.
            """
            self.txt.append("%s attended %s %s! \n"%(self.girl.name, aoran(self.course.action, "xxx"), self.course.action))

            # Get actual amount
            if amount == 0: amount = self.girl.AP

            if config.developer and False:
                self.txt.append("{color=[red]}do_course solved %s times.{/color} \n"%int(amount/self.course.AP))

            while amount >= self.course.AP:
                # Trainer primary
                # Based on dice roll using teachingchance + girls AP*2
                self.course.primary(self.girl, chance=self.teachingchance + self.girl.AP*2, mult=self.course.get_scaling(self.girl), girlmod=self.girlmod)

                # Trainer secondary
                # Based on dice roll using 1/2 teachingchance + girls AP
                self.course.secondary(self.girl, chance=int(self.teachingchance*0.5)+self.girl.AP, mult=self.course.get_scaling(self.girl), girlmod=self.girlmod)

                # Maxes for primes (applied to stats normally, trippled for skills)
                if self.course.primary.mod is not None:
                    if dice(round(1+(self.teachingchance*0.05))):
                        statmod = choice(self.course.primary.mod.keys())
                        if self.girl.stats.is_stat(statmod):
                            self.girl.stats.max[statmod] += 1

                        elif self.girl.stats.is_skill(statmod):
                            setattr(self.girl, statmod, 1) # Action
                            setattr(self.girl, statmod.capitalize(), 1) # Training

                        self.txt.append("Your girl got an {color=[lawngreen]}extra bonus{/color} in %s with the help of her trainer, this is a rare feat, you should be proud of her! \n"%statmod)

                # Self primary
                # Based on dice roll using random num between 1 and 20 + girls AP*2
                self.course.primary(self.girl, random=(1,20), chance=self.girl.AP*2, mult=self.course.get_scaling(self.girl), girlmod=self.girlmod)

                # Self secondary
                # Based on dice roll using random num between 1 and 20 + girls AP
                self.course.secondary(self.girl, random=(1,10), chance=self.girl.AP, mult=self.course.get_scaling(self.girl), girlmod=self.girlmod)

                # Decrease amount
                amount -= self.course.AP

            # Acknowledge max stats / lesson limitations
            for stat in self.girlmod:
                if self.girlmod[stat] > 0:
                    # Are we a stat (skills have no max)?
                    if self.girl.stats.is_stat(stat):
                        # If we have hit the girls max
                        if self.girl.stats[stat] + self.girlmod[stat] >= self.girl.get_max(stat):
                            self.txt.append("{color=[red]}This girl has reached her limits in %s! {/color} \n"%stat)

                            if self.girl.stats[stat] >= self.girl.get_max(stat): self.girlmod[stat] = 0

                        # If we have hit the teachers max
                        elif self.girl.stats[stat] + self.girlmod[stat] >= self.maxskill:
                            self.txt.append("{color=[red]}Your girl can no longer improve her %s under this teachers guidance!{/color} \n"%stat)

                            if self.girl.stats[stat] >= self.maxskill: self.girlmod[stat] = 0

            # Check we can still do the training
            if not self.course.reqs(self.girl):
                stop_training(self.girl)
                self.txt.append("%s is no longer eligable to attend this course! \n"%self.girl.name)
                self.loc.events_relay["finish"][1] += 1

            # Basic stat changes
            self.girlmod["vitality"] = randint(18,28)

            # Reduce girls AP
            self.girl.AP -= self.course.AP

            # Get images
            self.img = self.course.get_image(self.girl, resize=(740, 685))

        def rg(self):
            """
            Removes the girl from the girls list, if possible.
            """
            if self.girls is not None:
                self.girls.remove(self.girl)


    class OneOffTrainingJob(TrainingJob):
        """
        TrainingJob subclass that solves one-off-event training, as they happen outside the normal next day logic.
        """

        def __init__(self, girl, loc, course, trainer):
            """
            Creates a new OneOffTrainingJob.
            girl = The girl who is being trained.
            loc = The location where the training is happening.
            trainer = Thr trainer who is doing the training.
            course = The course that is being trained.
            """
            # Do non-standard inheritance
            Job.__init__(self, girl, None, loc=loc, event_type="schoolreport")

            # Get needed stats
            self.course = course
            self.trainer = trainer
            self.teachingchance = self.course.trainerSkill(self.trainer)
            self.maxskill = self.course.trainerKnowledge(self.trainer)

            # If dungeon, get upgrades
            if not self.loc.is_school:
                # rewards upgrades / total
                # 0   > chance = low chance
                # 0.5 > chance = medium chance
                # 1   > chance = high chance
                #
                self.obey = self.loc.mod_obey()

                # punishments upgrades / total
                # 0   < chance = high chance
                # 0.5 < chance = medium chance
                # 1   < chance = low chance
                #
                self.disobey = self.loc.mod_disobey()

                # security upgrades / total
                # 0   < chance = high chance
                # 0.5 < chance = medium chance
                # 1   < chance = low chance
                #
                self.runaway = pytfall.ra.location_runaway(self.loc)

                # security_rating / 1000
                # 2 - 0   = 2, high chance
                # 2 - 0.5 = 1.5, medium chance
                # 2 - 1   = 1, low chance
                #
                self.chance = pytfall.ra.location_security(self.loc)

                # equipment upgrades / total
                self.expmod = self.loc.mod_exp()

                # trainer upgrades / total
                self.teachingchance += (self.teachingchance*0.25) * self.loc.mod_skill()
                self.maxskill += (self.maxskill*0.25) * self.loc.mod_skill()

            # If school, ignore
            else:
                self.obey = 0
                self.disobey = 0
                self.runaway = 0
                self.expmod = 0
                self.chance = 0

            # Debugging info
            # if config.developer:
                # self.txt.extend(["{color=[blue]}",
                                 # "Girl: %s\n"%self.girl,
                                 # "Trainer: %s\n"%("You" if self.trainer is hero else self.trainer),
                                 # "Course: %s - %s\n"%(self.course.type, self.course.name),
                                 # "Security: %s\n"%(self.loc.security_mult() if not self.loc.is_school else "n/a"),
                                 # "Chance: %s\n"%self.chance,
                                 # "Obey: %s\n"%self.obey,
                                 # "Disobey: %s\n"%self.disobey,
                                 # "Runaway: %s\n"%self.runaway,
                                 # "{/color}"])

            # Label and obey status
            self.label, self.does_obey = self.course.get_label(self.girl, self.check_success())

        def __call__(self):
            """
            Does the actual training and expenses.
            """
            if not self.finished:
                self.do_course(1) # Override with only 1 resolution
                self.loc.log_income(self.girl, self.course.gold)

                exp = self.course.get_exp(self.trainer)
                exp += (exp*0.25) * self.expmod

                self.girlmod["exp"] = self.girl.adjust_exp(exp)
                self.girl.exp += exp

                self.finish_job()

        def finish_job(self):
            """
            Override to add the event to the locations one_off_events list.
            """
            self.finished = True
            self.loc.one_off_events.append(self.create_event())


    class EscapeeSearchJob(TrainingJobParent):
        """
        A job for girls that search for escaped slaves.
        """

        def __init__(self, girl, loc, girls):
            """
            Creates a new EscapeeSearchJob.
            girl = The girl the job is for.
            loc = The location the girl is in.
            girls = The list the girl belongs to.
            """
            super(EscapeeSearchJob, self).__init__(girl, girls, loc=loc, event_type="schoolndreport")

            # Get search chance
            self.chance = pytfall.ra.status(self.girl)
            if  "Warrior" not in self.girl.occupations: self.chance *= 0.8

            self.slave = None
            self.capture = False
            self.cost = None

            self.check_ap()
            if not self.finished: self.check_search()
            if not self.finished:
                if self.capture: self.capture()
                else: self.jail()

                self.apply_stats()
                self.girls.remove(self.girl)
                self.finish_job()

        def capture(self):
            """
            Checks whether the girl is able to catch the escapee.
            """
            caught, result = pytfall.ra.can_escape(self.slave, None, guards=[self.girl])

            # Set girlmod to the escape event stats generated by can_escape
            self.girlmod = guard_escape_event.stats(self.girl)

            # If the girl is caught
            if caught:
                pytfall.ra.retrieve(self.slave)

            if result == RunawayManager.CAUGHT:
                self.txt.append("%s proved to be the better runner and was able to catch %s before she could run. \n"%(self.girl.nickname, self.slave.fullname))

            elif result == RunawayManager.DEFEATED:
                self.txt.append("%s proved to be the better figher and was able to defeat %s and return her to you. \n"%(self.girl.nickname, self.slave.fullname))

            elif result == RunawayManager.FOUGHT:
                self.txt.append("Unfortunately %s proved too strong for %s and was able to defeat her and escape while she was incapacitated. \n"%(self.slave.fullname, self.girl.nickname))

            elif result == RunawayManager.ESCAPED:
                self.txt.append("Unfortunately %s proved too nimble for %s and was able to escape into %s. \n"%(self.slave.fullname,
                                                                                                              self.girl.nickname,
                                                                                                              choice(["a croud.",
                                                                                                                      "a back alley.",
                                                                                                                      "the darkness.",
                                                                                                                      "the trees."])
                                                                                                              ))

        def check_ap(self):
            """
            Checks that the girl is capable of performing the job.
            """
            if self.girl.AP < 2:
                self.txt.append("%s was unable to search for any escapees as she was too tired! \n"%self.girl.nickname)
                self.girls.remove(self.girl)
                self.finish_job()

            elif self.girl.health < 40 or self.girl.vitality < 40:
                self.txt.append("%s was unable to search for any escapees as she was too hurt to do so! \n"%self.girl.nickname)
                self.girls.remove(self.girl)
                self.finish_job()

            else:
                self.txt.append("%s went out to search for your escapees. \n"%self.girl.nickname)

        def check_search(self):
            """
            Checks the search chance and returns figures out whether a girl is found.
            """
            escapees = False

            # If there are girls free
            if pytfall.ra.look_cache:
                escapees = True

                girls = pytfall.ra.look_cache.items()
                l = len(girls)

                while girls:
                    _,g = girls.pop(randint(0, l))

                    if pytfall.ra.status(g) < self.chance:
                        self.slave = g
                        self.capture = True
                        self.txt.append("While searching %s was able to spot %s and gave chase! \n"%(self.girl.nickname, self.slave.fullname))
                        return

            # If there are girls in jail
            if pytfall.ra.jail_cache:
                escapees = True

                # If we are successful
                if dice(self.chance):
                    # Get a girl
                    self.slave = choice(pytfall.ra.jail_cache.keys())
                    pytfall.ra.set_girl(self.slave)
                    self.cost = pytfall.ra.get_price()

                    self.txt.append("%s checked the local jail and found that %s had been captured! "%(self.girl.nickname, self.slave.fullname))
                    return

            # Not slaves / none found
            if not escapees: self.txt.append("But there weren't any girls to find! \n")
            else: self.txt.append("But was unable to find anyone. \n")
            self.girls.remove(self.girl)
            self.finish_job()

        def jail(self):
            # If we can bail and afford
            if pytfall.ra.retrieve_jail and hero.take_money(self.cost, reason="Slave Bail"):
                # Retrieve the girl
                pytfall.ra.retrieve(self.slave)
                self.girlmod["exp"] = randint(25, 50)

                self.txt.append("She was able to bail her out and bring her back for {color=[gold]}%d Gold{/color}!"%cost)

            else:
                # If couldn't afford
                if pytfall.ra.retrieve_jail:
                    self.txt.append("Unfortunately %s wasn't able to afford her bail. \n"%self.girl.nickname)

                # Log her location
                pytfall.ra.jail_cache[self.slave][1] = True
                self.girlmod["exp"] = randint(1, 25)
