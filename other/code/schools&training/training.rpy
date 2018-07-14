init python:
    class TrainingDungeon(UpgradableBuilding, BuildingStats):
        """
        Building that represents the hero's dungeon to train girls in.
        Presently unused...
        """

        NAME = "Training Dungeon"

        def __init__(self, courses):
            """
            Creates a new TrainingDungeon.
            """
            super(TrainingDungeon, self).__init__(id=self.NAME, name=self.NAME, desc="A personal dungeon for training and punishing slaves.",
                                                  price=7500, minrooms=5, maxrooms=50, roomprice=500, upgrade_slots=18)

            self.img = "content/buildings/dungeon.webp"

            self.actions = ["Guard", "Train", "Take Course", "Search"]

            self.fin = Finances(self)
            self.income = 0

            # Dict
            self.all_courses = courses

            # List
            self.courses = [courses[i] for i in courses]

            self.events_relay = {
                "runaway": [0, 0], # successful, prevented
                "disobey": [0, 0], # successful, prevented
                "obey": [0, 0], # from training success, random
                "finish": [0, 0] # end of course, no longer eligible
            }

            self.one_off_events = list()

        @property
        def can_advert(self):
            return False

        @property
        def available(self):
            """
            Whether this building is available. Used in training screen.
            """
            return self in hero.buildings

        def get_girls(self, type=None):
            """
            Override get_girls to include proper trainer support.
            """
            if type == "Training":
                return [girl_training_with(girl) for girl in super(TrainingDungeon, self).get_girls("Course")]
            else:
                return super(TrainingDungeon, self).get_girls(type)

        def get_upkeep(self):
            """
            The upkeep cost of the building.
            """
            pass

        @property
        def is_school(self):
            """
            Whether or not this building is a school. Used in training screen.
            """
            return False

        def log_income(self, char, value):
            """
            Logs the training cost.
            char = The character who the income is being spent for.
            value = The amount being spent.
            """
            hero.take_money(value, reason=self.name)
            self.income += value
            char.fin.log_logical_expense(value, "Training")

        def mod_disobey(self):
            """
            The modifier for disobeying.
            """
            return self.get_upgrade_mod("Punishments") # / len(self.upgrades["Punishments"])

        def mod_exp(self):
            """
            The modifier for experience.
            """
            return self.get_upgrade_mod("Equipment") # / len(self.upgrades["Equipment"])

        def mod_housing(self):
            """
            The modifier for the hero's AP.
            """
            return self.get_upgrade_mod("Housing") # / len(self.upgrades["Housing"])

        def mod_obey(self):
            """
            The modifier for obeying.
            """
            return self.get_upgrade_mod("Rewards") # / len(self.upgrades["Rewards"])

        def mod_runaway(self):
            """
            The modifier for running away.
            """
            return self.get_upgrade_mod("Security") # / len(self.upgrades["Security"])

        def mod_skill(self):
            """
            The modifier for trainer ability.
            """
            return self.get_upgrade_mod("Trainers") # / len(self.upgrades["Trainers"])

        def next_day(self):
            """
            Solves the next day logic for the training girls.
            """
            # Logic
            type = "schoolndreport"
            img = im.Scale(self.img, int(config.screen_width*0.6), int(config.screen_height*0.8))
            txt = "%s Report: \n"%self.name
            evtlist = []
            char = None

            girls = self.get_girls("Course")

            if not girls:
                txt += "Your dungeon is currently going unused, maybe some of your girls require training? \n"
            else:
                txt += "You currently have %d %s training in your dungeon. \n"%(len(girls), plural("girl", len(girls)))

            # Checking if girls have completed their courses
            for girl in girls:
                course = char_is_training(girl)
                trainer = girl_training_with(girl)

                if course.daysLeft(girl) > 0:
                    girl_training_left.set(girl, -1, True) # Decrease
                else:
                    stop_training(girl)
                    self.events_relay["finish"][0] += 1

                    # Final stat increase
                    course.primary(girl, mult=course.get_scaling(girl))
                    course.secondary(girl, mult=course.get_scaling(girl))

                    # Bonus stat increase
                    if dice(20) and course.primary.mod is not None:
                        for stat in course.primary.mod:
                            girl.stats.max[stat] += choice([0, 1])

                    txt += "\n\n{color=[lawngreen]}%s has completed her %s training. \n{/color}"%(girl.name, course.type)

            # Security
            self.security_rating -= len(girls) * (1+self.mod_runaway())
            if self.security_rating < 0: self.security_rating = 0

            security_power = 0
            guards = self.get_girls("Guard")
            for guard in guards: security_power += (guard.attack + guard.defence + guard.magic) / 3

            self.security_rating += int(security_power * ((self.security_presence/10)+1))

            if self.security_rating < 0: self.security_rating = 0
            elif self.security_rating > 1000: self.security_rating = 1000

            txt += "Security Rating is now %d out of 1000, you currently have %d guards on duty with security presence of %d%%. \n\n"% (self.security_rating, len(guards), self.security_presence)

            # Event summery
            for i in self.events_relay:
                j,k = self.events_relay[i]

                if i == "obey":
                    if j > 0: txt += "%d %s obeyed their trainers perfectly. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s did extra well because of the facilities and equipment. \n"%(k, plural("girl", k))
                elif i == "disobey":
                    if j > 0: txt += "%d %s disobeyed their trainers without punishment. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s disobeyed their trainers and were punished for it. \n"%(k, plural("girl", k))
                elif i == "runaway":
                    if j > 0: txt += "%d %s ran away from their lessons, wasting their day. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s tried to run away, but were caught and punished. \n"%(k, plural("girl", k))
                elif i == "finish":
                    if j > 0: txt += "%d %s have completed their training. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s are no longer eligible for their training. \n"%(k, plural("girl", k))

                self.events_relay[i][0] = 0
                self.events_relay[i][1] = 0

            # Do one off events
            while self.one_off_events:
                NextDayEvents.append(self.one_off_events.pop())

            evt = NDEvent()
            evt.type = type
            evt.char = char
            evt.img = img
            evt.txt = txt
            NextDayEvents.append(evt)


    pytRelayProxyStore = list()
    class PytRelayProxy(_object):
        """
        A class that acts as a proxy for character event relays.
        """

        def __init__(self, event, relay="guard_relay", use_against=False):
            """
            Creates a new PytRelayProxy.
            event = The event to access.
            relay = The relay to access the event in.
            use_against = Whether to use the against list instead of helped.
            """
            self.event = event
            self._relay = relay
            self.use_against = use_against

            # Add to store
            pytRelayProxyStore.append(self)

    def girl_is_broken(girl):
        """
        Whether the girl has the broken trait.
        girl = The girl to check.
        """
        return "Broken" in girl.traits

    training_screen_current = None
    training_screen_course = None
    training_screen_trainer = None

    # Done as action to allow for easy sensitivity detection
    class TrainingSwitchAction(Action):

        def __init__(self, current):
            self.current = current

        def __call__(self):
            global training_screen_current
            global training_screen_course

            training_screen_current = schools[self.current]
            training_screen_course = None

            renpy.restart_interaction()

        def get_sensitive(self):
            return training_screen_current != schools[self.current]


    def get_all_courses(no_school=False, real=False):
        """
        Returns the list of all courses from all schools.
        """
        if real: courses = dict()
        else: courses = list()

        for i in schools.itervalues():
            if not no_school or not i.is_school:
                for j in i.all_courses:
                    if real:
                        courses[j] = i.all_courses[j]

                    else:
                        courses.append((j, i.all_courses[j].action if not i.is_school else j + " Course"))

        return courses

        def against(self, girl, add=None, clear=False):
            """
            Accesses the against property.
            girl = The girl the relay should proxy.
            add = Items to add to the property.
            clear = Whether to clear the list (first).
            """
            r = self.relay(girl)
            if clear:
                r["against"] = list()

            if add:
                for a in add:
                    r["against"].append(add)

            return r["against"]

        def count(self, girl, to=None, relative=True):
            """
            Accesses the count property.
            girl = The girl the relay should proxy.
            to = The value to set to.
            relative = Whether to set the value relative to the current.
            """
            r = self.relay(girl)
            if to is not None:
                if relative: r["count"] += to
                else: r["count"] = to

            return r["count"]

        def has(self, girl, property):
            """
            Checks whether a property is in the relay.
            girl = The girl the relay should proxy.
            property = The property to check for.
            """
            return property in self.relay(girl)

        def helped(self, girl, add=None, clear=False):
            """
            Accesses the helped property.
            girl = The girl the relay should proxy.
            add = Items to add to the property.
            clear = Whether to clear the list (first).
            """
            r = self.relay(girl)
            if clear:
                r["helped"] = list()

            if add:
                for a in add:
                    r["helped"].append(add)

            return r["helped"]

        def loss(self, girl, to=None, relative=True):
            """
            Accesses the count property.
            girl = The girl the relay should proxy.
            to = The value to set to.
            relative = Whether to set the value relative to the current.
            """
            r = self.relay(girl)
            if to is not None:
                if relative: r["loss"] += to
                else: r["loss"] = to

            return r["loss"]

        def relay(self, girl):
            """
            Returns the relay for the girl.
            girl = The girl to proxy.
            """
            return getattr(girl, self._relay)[self.event]

        def reset(self, girl):
            """
            Resets the relay.
            girl = The girl to proxy.
            """
            if self.event not in getattr(girl, self._relay):
                getattr(girl, self._relay)[self.event] = dict()

            self.count(girl, 0, False)

            if self.has(girl, "helped") or not self.use_against:
                self.helped(girl, clear=True)

            if self.has(girl, "against") or self.use_against:
                self.against(girl, clear=True)

            self.stats(girl, clear=True)
            self.win(girl, 0, False)
            self.loss(girl, 0, False)

        def stats(self, girl, merge=None, clear=False):
            """
            Accesses the stats property.
            girl = The girl the relay should proxy.
            merge = A dictionary to merge with.
            clear = Whether to clear the dictionary (first).
            """
            r = self.relay(girl)
            if clear:
                r["stats"] = dict()

            if merge:
                for k,v in merge.iteritems():
                    if k in r["stats"]: r["stats"][k] += v
                    else: r["stats"][k] = v

            return r["stats"]

        def win(self, girl, to=None, relative=True):
            """
            Accesses the count property.
            girl = The girl the relay should proxy.
            to = The value to set to.
            relative = Whether to set the value relative to the current.
            """
            r = self.relay(girl)
            if to is not None:
                if relative: r["win"] += to
                else: r["win"] = to

            return r["win"]

    # RelayProxy for escape events.
    # guard_escape_event = PytRelayProxy("escape_event", use_against=True)

    # RelayProxy for obey events.
    # trainer_obey_event = PytRelayProxy("obey_event")

    # RelayProxy for disobey events.
    # trainer_disobey_event = PytRelayProxy("disobey_event", use_against=True)

    # FlagProxy for the course the girl is currently taking.
    char_is_training = PytFlagProxy("training_course", None)

    # FlagProxy for who is currently training the girl.
    girl_training_with = PytFlagProxy("training_with", None)

    # FlagProxy for how long the training will last.
    girl_training_left = PytFlagProxy("training_left", 0)

    # FlagProxy for the girls obedience with training.
    girl_obeys = PytFlagProxy("obey", 0, trait="Obedient").register_for_relative_training()

    # FlagProxy for the girls disobedience with training.
    girl_disobeys = PytFlagProxy("disobey", 0, trait="Disobedient").register_for_relative_training()

    # FlagProxy for the
    training_ap_cost = PytFlagProxy("training_ap", 0)

    def trainer_total_ap_cost(trainer):
        """
        Returns the total amount of AP it will cost to train the assigned girls.
        trainer = The trainer to check for.
        """
        i = 0
        for girl in girls_training_with(trainer):
            i += char_is_training(girl).heroAP

        return i

    def trainer_ap_for_girl(trainer):
        """
        Returns the ap that the trainer has for training a girl.
        trainer = The trainer to check for.
        """
        return trainer.get_free_ap() - training_ap_cost(trainer)

    def trainers_at_location(location):
        """
        Returns the girls that are assigned as trainers at the location.
        location = The location to check.
        """
        tr = [g for g in hero.chars if g.location is location and g.action == "Train"]
        # Hero always available
        tr.insert(0, hero)
        return tr

    def girls_training_with(trainer):
        """
        Returns the girls that are training with the trainer.
        trainer = The trainer to check for.
        """
        return [girl for girl in hero.chars if girl_training_with(girl) is trainer]

    def girl_training_trait_mult(girl, trait):
        """
        Returns the multiplier for the trait using training specific logic.
        girl = The girl to return the multiplier for.
        trait = The trait to return the multiplier for.
        """
        t = 0
        if trait in traits:
            if trait in girl.traits:
                return float(girl.itemtraits[trait]) / float(getattr(traits[trait], "trEffMax", len(girl.eqslots)))

        return 0

    def stop_training(girl):
        """
        Stops a girl from training.
        """
        char_is_training.clear(girl)
        girl_training_with.clear(girl)
        girl_training_left.clear(girl)
        girl.action = None
        girl.location = hero


    class PytTraining(_object):
        """
        The class that parses and holds a training course.
        """

        def __init__(self, id, image=None, desc="", jobs=None, status=None, succeed=None, options={}, file=None):
            """
            Creates a new PytTraining option.
            id = The name of the training course.
            image = The image to use.
            desc = The description of the course.
            jobs = A list of valid occupations that can take this course. Accepts all if None.
            status = A list of valid status' that can take this course. Accepts all if None.
            succeed = Global success state for all lessons, overridden by lesson specific flags.
            options = A dict of PytTrainingLesson instances, or json objects to make into Lessons.
            file = The original file path that the training came from.
            """
            self.name = id
            self.image = image
            self.desc = desc
            self.jobs = jobs
            self.status = status
            self.options = list()
            self.file = file

            self.succeed = PytStatSwitch(succeed) if succeed is not None else empty_stat_switch

            # Create Lessons from json
            for k,v in options.iteritems():
                if isinstance(v, PytTrainingLesson): v.course = self
                else: v = PytTrainingLesson(self, k, **v)

                self.options.append(v)

        @property
        def action(self):
            return self.name + " Course"

        def can_train(self, girl, hero, one_off_only=None):
            """
            Whether this course is available for the girl.
            """
            if isinstance(girl, list):
                return any(self.can_train(g, hero, one_off_only) for g in girl)
            # TODO lt training: May not be upgraded to modern code properly:
            # f self.jobs is not None and girl.occupation not in self.jobs: return False
            if self.jobs is not None and girl.occupations.intersection(self.jobs): return False
            if self.status is not None and  girl.status not in self.status: return False

            # Only show if at least 1 option is available
            return len(self.get_options(girl, hero, one_off_only)) > 0

        def get_girls(self):
            """
            Returns the girls that are doing this course.
            """
            return [girl for girl in hero.chars if girl.action == self.action]

        def get_lesson_image(self):
            """
            Returns an image for the lesson.
            """
            # Do we have an image
            if self.image is not None:
                # Is the last character not a slash
                if self.image[-1] != "/":
                    if not "schools/" in self.image:
                        self.image = "schools/"+self.image
                    return 'content/'+self.image
                p = self.image[:-1]
            else:
                # Else use name for random folder
                p = self.name

            images = list()
            if p in os.listdir(content_path("schools")):
                for file in os.listdir(content_path("schools/%s"%p)):
                    if check_image_extension(file):
                        images.append("schools/%s/%s"%(p, file))

            # Overwrite image so its used for rest of session
            if len(images) > 0: self.image = choice(images)
            else: self.image = "gfx/interface/images/no_image.png"

            return 'content/'+self.image

        def get_options(self, girl, hero, one_off_only=None):
            """
            The options that the girl can partake in for the class.
            """
            if isinstance(girl, list):
                return [i for i in self.options if any(i.can_train(g, hero) for g in girl) and (one_off_only is None or i.is_one_off_event == one_off_only)]

            return [i for i in self.options if i.can_train(girl, hero) and (one_off_only is None or i.is_one_off_event == one_off_only)]


    class PytTrainingLesson(_object):
        """
        The class that parses and holds a training lesson.
        """

        POS_FLAGS = ("pos", "poseffect", "p", "true", "yes", "on", "1", "positive", "+", "+ve")
        NEG_FLAGS = ("neg", "negeffect", "n", "false", "no", "off", "0", "negative", "-", "-ve")
        POS_CHECK_FLAGS = ("posc", "poscheck", "pc", "post", "postill", "pt")
        NEG_CHECK_FLAGS = ("negc", "negcheck", "nc", "negt", "negtill", "pt")

        NO_EFFECT = "noEffect"
        POS_EFFECT = "posEffect"
        NEG_EFFECT = "negEffect"
        POS_TILL_CHECK = "posTillCheck"
        NEG_TILL_CHECK = "negTillCheck"
        FUNCTION = "function"

        def __init__(self, course, id, image=None, imageMode="normal", imageTags=None, noImageTags=None, desc="",
                     scale=None, check=None, based=None, skill=None, knowledge=None,
                     reqs=None, hero=None, succeed=None, AP=1, heroAP=1, gold=0, duration=0, labels=None,
                     primary=None, secondary=None, doNum=0):
            """
            Creates a new PytTrainingLesson.
            course = The course this lesson belongs to.
            id = The name of the lesson.
            image = The image to use.
            imageMode = The mode to look up images for girls by.
            imageTags = A list of tags to use to get an image for a girl.
            noImageTags = A list of tags to use to not get an image for a girl.
            desc = The description of the lesson.

            scale = How numeric modifications for this method scale.
            check = A PytStatCheck instance, json object or function name to check incase the scale is limited.
            based = A list of stats to base the multiplier off of, or a function name.
            skill = A list of stats to calculate the training chance for. Default is Intelligence.
            knowledge = A list of stats to calculate the training max for. Default is Intelligence.

            reqs = A PytStatCondition, PytStatCheck or json object that the girl needs to meet to take the lesson.
            hero = A PytStatCondition, PytStatCheck or json object that the trainer needs to meet to teach the lesson.
            succeed = A PytStatSwitch to solve the success state of the training.

            AP = The amount of AP this lesson costs the girl.
            heroAP = The amount of AP this lesson costs the trainer. Set to -1 to cost all AP.
            gold = The amount of gold this less on costs.
            duration = The amount of days that the course takes.
            labels = The labels to jump to for the training. Overrides duration as a one-off training event.

            primary = A PytStatChanges instance or json object for the primary changes to a character.
            secondary = A PytStatChanges instance of json object for the secondary changes to a character.
            doNum = The number of times that TrainingJob.do_course should solve the primary and secondary objects.
            """
            self.course = course
            self.name = id
            self.image = image
            self.desc = desc

            self.imageMode = imageMode
            self.imageTags = list()
            self.noImageTags = list()

            if imageTags is not None:
                for i in imageTags:
                    self.imageTags.append(i)

            if noImageTags is not None:
                for i in noImageTags:
                    self.noImageTags.append(i)

            if scale is not None:
                if scale in PytTrainingLesson.POS_FLAGS: self.scale = PytTrainingLesson.POS_EFFECT
                elif scale in PytTrainingLesson.NEG_FLAGS: self.scale = PytTrainingLesson.NEG_EFFECT
                elif scale in PytTrainingLesson.POS_CHECK_FLAGS: self.scale = PytTrainingLesson.POS_TILL_CHECK
                elif scale in PytTrainingLesson.NEG_CHECK_FLAGS: self.scale = PytTrainingLesson.NEG_TILL_CHECK
                else: self.scale = PytTrainingLesson.NO_EFFECT

            else:
                self.scale = PytTrainingLesson.NO_EFFECT

            if isinstance(check, (str, unicode, PytStatCondition, PytStatCheck)): self.check = check
            elif isinstance(check, (dict, list)): self.check = BuildStatRequirement(check)
            else: self.check = None

            self.based = based

            self.reqs = BuildStatRequirement(reqs) if not isinstance(reqs, (PytStatCondition, PytStatCheck)) else reqs
            self.hero = BuildStatRequirement(hero) if not isinstance(hero, (PytStatCondition, PytStatCheck)) else reqs

            self.succeed = PytStatSwitch(succeed) if succeed is not None else empty_stat_switch

            self.skill = skill or ["TEACHING"]
            self.knowledge = knowledge or ["TEACHING"]

            self.AP = AP
            self.heroAP = heroAP
            self.gold = gold

            self.duration = duration
            self.labels = labels

            if isinstance(primary, PytStatChanges): self.primary = primary
            elif isinstance(primary, dict): self.primary = PytStatChanges(**primary)
            else: self.primary = empty_stat_changes

            if isinstance(secondary, PytStatChanges): self.secondary = secondary
            elif isinstance(secondary, dict): self.secondary = PytStatChanges(**secondary)
            else: self.secondary = empty_stat_changes

            self.doNum = doNum

            # Get unique id
            self.id = str(random.random())

            self.chars = dict()

        @property
        def action(self):
            """
            The action this training assigns to a girl.
            """
            return self.type + " Course"

        def can_train(self, girl, hero):
            """
            Whether the girl and hero/trainer meets the requirements for this method.
            """
            if isinstance(girl, list):
                return any(self.can_train(g, hero) for g in girl)
            # If we are a one-off training event
            if self.is_one_off_event:
                # Check for AP as well
                if girl.AP < self.AP or hero.AP < self.heroAP: return False

            return self.reqs(girl) and self.hero(hero)

        def daysLeft(self, girl):
            """
            Returns the amount of days the girl has left at the course.
            """
            return girl_training_left(girl)

        def get_exp(self, hero):
            """
            Calculates the amount of xp generated for this lesson.
            hero = The trainer.
            """
            return int(randint(10, 25) + (self.trainerSkill(hero) + self.trainerKnowledge(hero)) / 5)

        def get_girls(self):
            """
            Returns the girls that are doing this course.
            """
            return [girl for girl in hero.chars if char_is_training(girl) is self]

        def get_image(self, girl, **kwargs):
            """
            Returns an image from the girl for the training.
            girl = The girl to get an image from.
            kwargs = Extra arguments to pass to the show function.
            """
            # Set image mode
            kwargs["type"] = self.imageMode
            # Add excluded tags, if any
            if self.noImageTags: kwargs["exclude"] = self.noImageTags

            # If we have tags:
            if self.imageTags:
                img = girl.show(*self.imageTags, **kwargs)

            # Else return profile
            return img or girl.show("profile", "happy", **kwargs)

        def get_label(self, girl, state):
            """
            Returns the label for the success state.
            girl = The girl to get the label for.
            state = The state to get the label for.
            """
            if state in self.labels:
                l = self.labels[state]
                o = state == TrainingJobFlags.OBEY

            elif state == TrainingJobFlags.OBEY:
                l = self.labels[TrainingJobFlags.NORMAL]
                o = True

            elif state == TrainingJobFlags.DISOBEY:
                l = "training_event_disobey"
                o = False

            elif state == TrainingJobFlags.STOP:
                l = "training_event_stop"
                o = False

            elif state == TrainingJobFlags.RUNAWAY:
                l = "training_event_runaway"
                o = False

            elif state == TrainingJobFlags.GIRL_AP:
                l = "training_event_girl_ap"
                o = False

            elif state == TrainingJobFlags.HERO_AP:
                l = "training_event_hero_ap"
                o = False

            elif state == TrainingJobFlags.NO_GOLD:
                l = "training_event_no_gold"
                o = False

            else:
                # devlog.error("No response for PytTrainingLesson(%s, %s).get_label(%s)"%(self.type, self.name, state))
                l = self.labels[TrainingJobFlags.NORMAL]
                o = False

            u = "%s_%s"%(l, girl.id)
            if renpy.has_label(u): return u, o
            else: return l, o

        def get_lesson_image(self):
            """
            Returns an image for the lesson.
            """
            # Do we have an image
            if self.image is not None:
                if self.image[-1] != "/":
                    if not "schools/" in self.image:
                        self.image = "schools/"+self.image
                    return 'content/'+self.image
                p = self.image[:-1]
            else:
                # Else use name for random folder
                p = self.type

            images = list()
            if p in os.listdir(content_path("schools")):
                for file in os.listdir(content_path("schools/%s"%p)):
                    if check_image_extension(file):
                        images.append("schools/%s/%s"%(p, file))

            # Overwrite image so its used for rest of session
            if len(images) > 0: self.image = choice(images)
            else: self.image = "gfx/interface/images/no_image.png"

            return 'content/'+self.image

        def get_scaling(self, girl):
            """
            Returns the scaling based on the stats or functions given.
            """
            if self.scale == PytTrainingLesson.NO_EFFECT:
                return 1.0

            if isinstance(self.based, basestring):
                if hasattr(store, self.based): f = getattr(store, self.based)(girl)
                else:
                    # devlog.error("No scaling function found for PytTrainingScaling \"%s\"."%self.based)
                    f = 1.0

            else:
                s = 0
                m = 0
                for i in self.based:
                    if girl.stats.is_stat(i):
                        s += girl.stats._get_stat(i)
                        m += girl.stats.max[i]
                    elif girl.stats.is_skill(i):
                        s += girl.stats.get_skill(i)
                        m += girl.stats.get_skill(i)
                    else:
                        pass
                        # devlog.warning(str("Attempt to access \"%s\" in STATS and SKILLS for %s in TrainingLesson.get_scaling."%(i, girl.fullname)))

                f = float(s)/float(m) # Ensure float

            if self.scale == PytTrainingLesson.POS_EFFECT: return f
            elif self.scale == PytTrainingLesson.NEG_EFFECT: return 1-f
            elif self.scale == PytTrainingLesson.POS_TILL_CHECK:
                if isinstance(self.check, basestring):
                    if hasattr(store, self.check):
                        if getattr(store, self.check)(girl): return f
                        else: return 0

                    else:
                        # devlog.error("No check function found for PytTrainingLesson \"%s\"."%self.check)
                        return f

                else:
                    if self.check(girl): return f
                    else: return 0

            elif self.scale == PytTrainingLesson.NEG_TILL_CHECK:
                if isinstance(self.check, basestring):
                    if hasattr(store, self.check):
                        if getattr(store, self.check)(girl): return 1-f
                        else: return 0

                    else:
                        # devlog.error("No check function found for PytTrainingLesson \"%s\"."%self.check)
                        return f

                else:
                    if self.check(girl): return 1-f
                    else: return 0

            else:
                return 0

        def get_success(self, girl):
            """
            Returns the success state for this lesson.
            girl = The girl to return the state for.
            """
            if self.is_schooling: return self.succeed(girl)
            else:
                flag, m = self.succeed(girl)

                if flag is None:
                    flag, m = self.course.succeed(girl)

                    if flag in self.succeed:
                        return None, None

                return flag, m

        @property
        def is_one_off_event(self):
            return self.labels is not None and TrainingJobFlags.NORMAL in self.labels

        @property
        def is_schooling(self):
            """
            Whether this lesson is schooling or training.
            """
            return False

        def set_training(self, girl, location, hero):
            """
            Sets a girl and hero combo for training.
            """
            if isinstance(girl, list):
                for g in girl:
                    if self.can_train(g, hero):
                        self.set_training(g, location, hero)
                return

            char_is_training(girl, self)
            girl_training_with(girl, hero)
            girl_training_left(girl, self.duration+1)

            girl.action = self.action
            girl.location = location

            # Add to training counter
            self.chars[str(girl)] = 0

        def trainerKnowledge(self, hero, **kwargs):
            """
            The maximum that a skill/stat can be raised to during the training.
            Calculated as the mean of all skills and stats in the knowledge array.
            hero = The trainer.
            """
            s = 0

            for i in self.knowledge:
                if hero.stats.is_stat(i): s += hero.stats._get_stat(i.lower())
                elif hero.stats.is_skill(i): s += hero.stats.get_skill(i)
                else:
                    # devlog.warning(str("Tried to access \"%s\" in STATS and SKILLS for %s."%(i, hero.fullname)))
                    pass

            return int(s/len(self.knowledge))

        def trainerSkill(self, hero):
            """
            The chances of a girl receiving an effect from the training.
            Calculated as the mean of (all skills*0.8 and stats) / (all skills and max-stats).
            This means a trainerSkill that only uses skills will have a 100% chance, as they don't have totals.
            hero = The trainer.
            """
            s = 0
            m = 0
            for i in self.skill:
                if hero.stats.is_stat(i):
                    s += hero.stats._get_stat(i.lower())
                    m += hero.stats.max[i.lower()]
                elif hero.stats.is_skill(i):
                    s += hero.stats.get_skill(i) * .75
                    m += hero.stats.get_skill(i)
                else:
                    # devlog.warning(str("Tried to access \"%s\" in STATS and SKILLS for %s."%(i, hero.fullname)))
                    pass

            if s == 0 or m == 0: return 0
            else: return int(s/m) * 100

        def trainerStatus(self, girl, hero):
            """
            Returns a description of how well a trainer would teach this lesson for the girl.
            Calculated as:
                H = The the difference between girls knowledge and the trainers knoweldge as a percentage of the trainers knowledge.
                    eg: trainer = 100, girl = 75, result = .25
                S = The trainers skill.

                H <= 0: "Worthless"
                H < 20: "Bad"
                H < 40: "Poor"
                H < 60: "Average"
                H < 80: "Good"
                Else  : "Great"

                S < 33: "Slow"
                S < 66: n/a
                Else  : "Fast"

            girl = The girl being taught.
            hero = The trainer.
            """
            g = float(self.trainerKnowledge(girl, is_girl=True))
            h = float(self.trainerKnowledge(hero))
            s = self.trainerSkill(hero)

            if g <= 0: h = 100
            elif h <= 0: h = 0
            else: h = (1 - (g / h)) * 100

            g = 0

            if h < 40:
                g = -1
                if h <= 0: r = "Worthless"
                elif h < 20: r = "Bad"
                else: r = "Poor"

            elif h < 60:
                r = "Average"

            else:
                g = 1
                if h < 80: r = "Good"
                else: r = "Great"

            if s < 33: r += (" and " if g < 1 else " but ") + "Slow"
            elif s > 65: r += (" and " if g > 0 else " but ") + "Fast"

            return r

        @property
        def type(self):
            if isinstance(self.course, (str, unicode)): return self.course
            else: return self.course.name


    class OneOffTrainingAction(Action):
        """
        Screen action for the easy execution of OneOffTrainingJobs.
        """

        def __init__(self, mode, lesson):
            """
            Creates a new OneOffTrainingAction.
            mode = How the action should work.
            lesson = The lesson the action is for.
            """
            self.mode = mode
            self.lesson = lesson

        def __call__(self):
            """
            Functions this action.
            If mode = "action": Functions the training interaction and jumps to the label.
            If mode = "menu": Returns whether any option in the training course can be used.
            If mode = "condition": Returns whether the course can be used.
            """
            if self.mode == "action":
                if in_training_location(char):
                    global gm_job

                    # Build the job
                    gm_job = OneOffTrainingJob(char, char.location, self.lesson, hero)

                    # Report
                    gm.show_menu = False
                    gm.jump_cache = gm_job.label

                    # Jump
                    renpy.jump(gm_job.label)

                else:
                    renpy.show_screen("message_screen", "%s cannot be trained in her current location!"%char.nickname)

            elif self.mode == "menu":
                return self.lesson.can_train(char, hero, one_off_only=True)

            elif self.mode == "condition":
                return self.lesson.can_train(char, hero)


    class SchoolLesson(PytTrainingLesson):
        """
        A training lesson specially set up to use a 'school' instead of an assigned trainer.
        """

        def __init__(self, id, **kwargs):
            """
            Creates a new SchoolLesson.
            Accepts all the same arguments as PytTrainingLesson, except 'type', which will be the same as 'id'.
            """
            super(SchoolLesson, self).__init__(id, id, **kwargs)

            self.skill = randint(30, 100)
            self.knowledge = randint(40, 300)

            self.duration = randint(14, 29)
            self._daysLeft = self.duration + 1

            self.complete = dict()

            if self.gold <= 0:
                self.gold = int(self.skill*0.3)

                if self.knowledge >= 250: self.gold += self.knowledge*2
                elif self.knowledge >= 200: self.gold += int(self.knowledge*1.5)
                elif self.knowledge >= 150: self.gold += int(self.knowledge*1.3)
                elif self.knowledge >= 100: self.gold += int(self.knowledge*0.5)
                elif self.knowledge >= 50: self.gold += int(self.knowledge*0.5)
                else: self.gold += int(self.knowledge*0.3)

        def daysLeft(self, girl=None):
            """
            Whether the girl and hero/trainer meets the requirements for this method.
            """
            return self._daysLeft

        def get_exp(self, hero=None):
            """
            Calculates the amount of xp generated for this lesson.
            """
            return int(randint(10, 25) + (self.trainerSkill(hero) + self.trainerKnowledge(hero)) / 5)

        @PytTrainingLesson.is_schooling.getter
        def is_schooling(self):
            """
            Whether this lesson is schooling or training.
            """
            return True

        def set_training(self, girl, location, hero=None):
            """
            Sets a girl and hero combo for training.
            """
            if isinstance(girl, list):
                for g in girl:
                    if self.can_train(g, hero):
                        self.set_training(g, location, hero)
                return

            char_is_training(girl, self)
            girl_training_with(girl, None)

            girl.action = self.action
            girl.location = location

            # Add to training counter
            self.chars[str(girl)] = 0

        def trainerKnowledge(self, hero=None, is_girl=False, **kwargs):
            """
            How much "knowledge" the trainer has in this subject.
            hero = The character to return the skill of.
            is_girl = Whether the character passed is the girl being trained.
            """
            if isinstance(hero, list):
                l = [self.trainerKnowledge(h, is_girl, **kwargs) for h in hero]
                return sum(l) / len(l) if len(l) else 0# return the average

            # Are we the girl
            if is_girl:
                s = 0

                for i in self.primary.mod:
                    if hero.stats.is_stat(i): s += hero.stats._get_stat(i)
                    elif hero.stats.is_skill(i): s += hero.stats._raw_skill(i)

                return int(s / len(self.primary.mod))

            # Else, return the stored knowledge
            else: return self.knowledge

        def trainerSkill(self, hero=None):
            """
            How much "skill" the trainer has in this subject.
            """
            return self.skill


    class PytStatChanges(_object):
        """
        The class that parses and holds girl-stat change logic.
        """

        def __init__(self, mod=None, min=None, max=None, props=None, flags=None, traits=None, noTraits=None, effect=None, noEffect=None, funcs=None):
            """
            Creates a new PytStatChanges object.
            mod = An object of {"stat": number} formatting to add the numbers to the stats or skills.
            min = An object of {"stat": number} formatting to add the numbers to the stat minimums.
            max = An object of {"stat": number} formatting to add the numbers to the stat maximums.
            props = An object of {"variable": value} formatting to set properties in the main girl class.
            flags = An object of {"flag": value} formatting to set flags in the girl's Flag instance.
            traits = A list of traits to add.
            noTraits = A list of traits to remove.
            effect = A list of effects to add.
            noEffect = A list of effects to remove.
            funcs = A list of function names to call. Passes (girl, boolean) as arguments.
            """
            self.mod = mod
            self.min = min
            self.max = max
            self.props = props
            self.flags = flags
            self.traits = traits
            self.noTraits = noTraits
            self.effect = effect
            self.noEffect = noEffect
            self.funcs = funcs

        def __call__(self, girl, random=None, chance=0, mult=1.0, girlmod=None):
            """
            Applies the changes contained in this instance to the girl.
            girl = The girl to apply the changes to.
            random = A tuple of 2 integers to return a random number between. Added to chance.
            chance = A number to pass to a dice call to check if a stat should be modified. Only affects mod, min and max.
            mult = The multiplier for the changes.
            girlmod = An object to update with the stat changes (only works with mod) instead of the girl. Used for Job logic.
            """
            # Skip if no changes
            if mult == 0: return

            if mult < 0 or mult > 1:
                # devlog.warning("PytStatChanges encountered a multiplier out of traditional bounds. Mult: %s"%str(mult))
                pass

            if random is not None: can = lambda: dice(randint(*random)+chance)
            elif chance > 0: can = lambda: dice(chance)
            else: can = lambda: True

            if self.mod is not None:
                for k,v in self.mod.iteritems():
                    # If a stat
                    if girl.stats.is_stat(k) and can():
                        if isinstance(v, (list,tuple)):
                            if len(v) == 1: v = randint(0,v[0])
                            elif len(v) == 2: v = randint(*v)
                            else: v = choice(v)

                        if girlmod is not None:
                            girlmod[k] = girlmod.get(k, 0) + int(v*mult)

                        else:
                            girl.mod_stat(k, int(v*mult))

                    # If a skill
                    elif girl.stats.is_skill(k) and can():
                        if isinstance(v, (list,tuple)):
                            if len(v) == 1: v = randint(0,v[0])
                            elif len(v) == 2: v = randint(*v)
                            else: v = choice(v)

                        if girlmod is not None:
                            girlmod[k] = girlmod.get(k, 0) + int(v*mult)
                        else:
                            girl.mod_skill(k, int(v*mult))
                            # setattr(girl, k, int(v*mult))

            if self.min is not None:
                for k,v in self.min.iteritems():
                    if girl.stats.is_stat(k) and can():
                        if isinstance(v, (list,tuple)):
                            if len(v) == 1: v = randint(0,v[0])
                            elif len(v) == 2: v = randint(*v)
                            else: v = choice(v)

                        v = int(v*mult)

                        # Prevent negative minimum
                        if (girl.stats.min[k] + v) > 0:
                            girl.stats.min[k] += v
                            # Ensure below max
                            if girl.stats.max[k] <= girl.stats.min[k]: girl.stats.max[k] = girl.stats.min[k]+1

                        else: girl.stats.min[k] = 0

                        # Update data
                        if girl.stats._get_stat(k) < girl.stats.min[k]: girl.mod_stat(k, girl.stats.min[k] - girl.stats.get_skill(k))

            if self.max is not None:
                for k,v in self.max.iteritems():
                    if girl.stats.is_stat(k) and can():
                        if isinstance(v, (list,tuple)):
                            if len(v) == 1: v = randint(0,v[0])
                            elif len(v) == 2: v = randint(*v)
                            else: v = choice(v)

                        v = int(v*mult)

                        # Prevent negative maximum
                        if (girl.stats.max[k] + v) > 0:
                            girl.stats.max[k] += v
                            # Ensure above min
                            if girl.stats.min[k] >= girl.stats.max[k]: girl.stats.min[k] = girl.stats.max[k]-1

                        else:
                            girl.stats.max[k] = 1
                            girl.stats.min[k] = 0

                        # Update data
                        if girl.stats._get_stat(k) > girl.stats.max[k]: girl.mod_stat(k, girl.stats.max[k] - girl.stats.get_skill(k))

            if self.props is not None:
                for k,v in self.props.iteritems():
                    if isinstance(v, (list,tuple)):
                        if len(v) == 1: v = randint(0,v[0])
                        elif len(v) == 2: v = randint(*v)
                        else: v = choice(v)

                    if isinstance(v, int): v = int(v*mult)
                    elif isinstance(v, float): v = v*mult

                    if hasattr(girl, k): setattr(girl, k, v)
                    else:
                        # devlog.warning("Attempt to set non-existant flag in StatChanges: %s = %s"(k, v))
                        pass

            if self.flags is not None:
                for k, v in self.flags.iteritems():
                    if isinstance(v, (list, tuple)):
                        if len(v) == 1: v = randint(0, v[0])
                        elif len(v) == 2: v = randint(*v)
                        else: v = choice(v)

                    if k in pytFlagProxyStore: pytFlagProxyStore[k].set(girl, v, True)
                    else: girl.set_flag(k, v)

            if self.traits is not None:
                for k in iter(self.traits):
                    if isinstance(k, (list,tuple)): k = choice(v)

                    if k in traits: girl.apply_trait(traits[k])

            if self.noTraits is not None:
                for k in iter(self.noTraits):
                    if isinstance(k, (list,tuple)): k = choice(v)

                    if k in traits: girl.remove_trait(traits[k])

            if self.effect is not None:
                for k in iter(self.effect):
                    if isinstance(k, (list,tuple)): k = choice(v)

                    girl.enable_effect(k)

            if self.noEffect is not None:
                for k in iter(self.noEffect):
                    if isinstance(k, (list,tuple)): k = choice(v)

                    girl.disable_effect(k)

            if self.funcs is not None:
                for k in iter(self.funcs):
                    if hasattr(store, k): getattr(store, k)(girl, can())
                    else:
                        # devlog.warning("Attempt to call non-existent function in global store \"%s\"."%k)
                        pass

        def __str__(self):
            s = "PytStatChanges:"
            if self.mod is not None: s += "\n\tmod:" + self._str(self.mod)
            if self.min is not None: s += "\n\tmin:" + self._str(self.min)
            if self.max is not None: s += "\n\tmax:" + self._str(self.max)
            if self.props is not None: s += "\n\tprops:" + self._str(self.props)
            if self.flags is not None: s += "\n\tflags:" + self._str(self.flags)
            if self.traits is not None: s += "\n\ttraits:" + self._strh(self.traits)
            if self.noTraits is not None: s += "\n\tnoTraits:" + self._strh(self.noTraits)
            if self.effect is not None: s += "\n\teffect:" + self._strh(self.effect)
            if self.noEffect is not None: s += "\n\tnoEffect:" + self._strh(self.noEffect)
            if self.funcs is not None: s += "\n\tfuncs:" + self._strh(self.funcs)
            return s

        def _str(self, sub):
            s = ""
            for i in sub.iteritems(): s += " %s + %s"%i
            return s

        def _strh(self, sub):
            return " " + ", ".join(sub)


    def BuildStatRequirement(dets):
        """
        Creates the appropriate PytStatCondition/Check based on whether its given a list/array or dict/object.
        Returns the contents of "empty_stat_check" if None is passed.

        dets = The object imported from a "training*.json" file containing the information.
        """
        if isinstance(dets, list): return PytStatCondition(dets)
        elif isinstance(dets, dict): return PytStatCheck(**dets)
        elif dets is None: return empty_stat_check
        else:
            raise PytStatParseException("Malformed Requirement statement. Encountered neither list nor object.\n\t\"%s\""%str(dets))


    class PytStatSwitch(_object):
        """
        The class that parses and holds character stat/trait checks as a switch condition.
        """

        def __init__(self, checks=None):
            """
            Creates a new PytStatSwitch instance.
            checks = A list of dicts containing the return flag and a list, PytStatCheck instance or json object.
            """
            self.cases = list()
            self.default = (None, None)

            if checks is not None:
                for i in checks:
                    if i[1] == True:
                        if len(i) > 2: self.default = i[0], i[2]
                        else: self.default = i[0], None

                    else:
                        if len(i) > 2: self.cases.append( (i[0], BuildStatRequirement(i[1]), i[2]) )
                        else: self.cases.append( (i[0], BuildStatRequirement(i[1]), None) )

        def __call__(self, girl):
            """
            Checks the character against the logic within this instance.
            """
            for r,c,m in self.cases:
                if c(girl): return r,m

            else:
                return self.default

        def __contains__(self, flag):
            """
            Whether a case is in this switch.
            """
            for r,c,m in self.cases:
                if r == flag: return True

            else:
                return False

        def __getitem__(self, case):
            """
            Returns the condition, message for the case.
            """
            if case in self:
                return self.cases[case][1], self.cases[case][2]

            else:
                return None, None

        def __str__(self):
            return "PytStatSwitch\n\tdefault: %s\n\t\t%s\n\t%s"%(self.default[0], self.default[1], ("\n".join(["%s: %s\n\t\t%s"%(r,str(c),m) for r,c,m in self.cases])).replace("\n", "\n\t"))


    class PytStatCondition(_object):
        """
        The class that parses and holds the chatacter stat/trait checks as an if condition.
        """

        AND = "and"
        OR = "or"
        XOR = "xor"

        def __init__(self, checks, mode="or"):
            """
            Creates a new PytStatCondition instance.
            checks = A list of lists, PytStatCheck instances or json objects.
                     The first instance can be a string to set the mode.
            mode = The condition mode for the checks. Overridden by the first index of checks if a string.
            """
            self.checks = list()

            if isinstance(checks[0], (str, unicode)):
                self.mode = str(checks[0])
                start = 1

            else:
                self.mode = mode
                start = 0

            for i in checks[start:]:
                if isinstance(i, list): self.checks.append(PytStatCondition(i))
                else: self.checks.append(PytStatCheck(**i))

        def __call__(self, girl):
            """
            Checks the character against the logic within this instance.
            """
            if self.mode == PytStatCondition.AND:
                for i in self.checks:
                    if not i(girl): return False

                else:
                    return True

            elif self.mode == PytStatCondition.OR:
                for i in self.checks:
                    if i(girl): return True

                else:
                    return False

            elif self.mode == PytStatCondition.XOR:
                ht = False
                for i in self.checks:
                    if i(girl):
                        if ht: return False
                        else: ht = True

                return ht

        def __str__(self):
            return "PytStatCondition(%s)\n\t%s"%(self.mode, ("\n".join([str(i) for i in self.checks])).replace("\n", "\n\t"))


    class PytStatCheck(_object):
        """
        The class that parses and holds the character stat/trait logic.
        """

        def __init__(self, mod=None, min=None, max=None, props=None, flags=None, traits=None, noTraits=None, effect=None, noEffect=None, funcs=None):
            """
            Creates a new PytStatCheckCheck instance.
            mod = A condition dict to match stats or skills.
            min = A condition dict to match minimum stats.
            max = A condition dict to match maximum stats.
            props = A condition dict to match character properties.
            flags = A condition dict to match flags.
            traits = A list of traits needed.
            noTraits = A list of traits that aren't wanted.
            effect = A list of effects needed.
            noEffect = A list of effects that aren't watned.
            funcs = A list of functions to call.

            mod, min, max, props and flags shoud be formatted as:
            {
            "lt": An object of {"stat": number} keys to match a < condition.
            "le": An object of {"stat": number} keys to match a <= condition.
            "eq": An object of {"stat": number} keys to match a == condition.
            "ne": An object of {"stat": number} keys to match a != condition.
            "ge": An object of {"stat": number} keys to match a >= condition.
            "gt": An object of {"stat": number} keys to match a > condition.

            "stat": A number to check stat against. Uses a >= condition (== condition for props and flags).
            }
            """
            self.mod = mod
            self.min = min
            self.max = max
            self.props = props
            self.flags = flags
            self.traits = traits
            self.noTraits = noTraits
            self.effect = effect
            self.noEffect = noEffect
            self.funcs = funcs

        def __call__(self, girl):
            """
            Checks the character against the logic within this instance.
            """
            if self.mod is not None and not self.meet(self.mod, girl): return False
            if self.min is not None and not self.meet(self.min, girl, "min"): return False
            if self.max is not None and not self.meet(self.max, girl, "max"): return False
            if self.props is not None and not self.meetf(self.props, girl): return False
            if self.flags is not None and not self.meetf(self.flags, girl, True): return False
            if self.traits is not None and not self.has(self.traits, girl): return False
            if self.noTraits is not None and not self.has(self.noTraits, girl, True): return False
            if self.effect is not None and not self.hase(self.effect, girl): return False
            if self.noEffect is not None and not self.hase(self.noEffect, girl, True): return False
            if self.funcs is not None and not self.call(self.funcs, girl): return False
            return True

        def __str__(self):
            s = "PytStatCheck:"
            if self.mod is not None: s += "\n\tmod:" + self._str(self.mod)
            if self.min is not None: s += "\n\tmin:" + self._str(self.min)
            if self.max is not None: s += "\n\tmax:" + self._str(self.max)
            if self.props is not None: s += "\n\tprops:" + self._str(self.props)
            if self.flags is not None: s += "\n\tflags:" + self._str(self.flags)
            if self.traits is not None: s += "\n\ttraits:" + self._strh(self.traits)
            if self.noTraits is not None: s += "\n\tnoTraits:" + self._strh(self.noTraits)
            if self.effect is not None: s += "\n\teffect:" + self._strh(self.effect)
            if self.noEffect is not None: s += "\n\tnoEffect:" + self._strh(self.noEffect)
            if self.funcs is not None: s += "\n\tfuncs:" + self._strh(self.funcs)
            return s

        def call(self, sub, girl):
            """
            Function to check the girl using functions.
            sub = The list of function names to check with.
            girl = The girl to check.
            """
            for i in sub:
                if hasattr(store, i):
                    if not getattr(store, i)(girl):
                        return False
                else:
                    # devlog.warning("Attempt to call non-existant function in global store \"%s\"."%i)
                    pass

            return True

        def girl_get(self, girl, key):
            """
            Function to return the skill or stat from the character.
            girl = The character to return the value from.
            key = The stat or skill to return.
            """
            if girl.stats.is_stat(key): return girl.stats._get_stat(key.lower())
            elif girl.stats.is_skill(key): return girl.get_skill(key)
            else:
                # devlog.warning("Tried to access \"%s\" in SKILLS or STATS for %s in StatCheck."%(key, girl.fullname))
                return 0

        def has(self, sub, girl, nott=False):
            """
            Function to check girl for traits.
            sub = The dict to check with.
            girl = The girl to check.
            nott = Whether to check for a lack of traits.
            """
            for i in sub:
                if nott:
                    if i in girl.traits: return False

                else:
                    if i not in girl.traits: return False

            return True

        def hase(self, sub, girl, nott=False):
            """
            Function to check for effects.
            sub = The dict to check with.
            girl = The girl to check.
            nott = Whether to check for a lack of effects.
            """
            for i in sub:
                if nott:
                    if i in girl.effects and girl.effects[i]["active"]: return False
                else:
                    if i in girl.effects and not girl.effects[i]["active"]: return False

            return True

        def meet(self, sub, girl, type="mod"):
            """
            Function to check for stats.
            sub = The dict to check with.
            access = The function to access the stats with.
            """
            for g,s in sub.iteritems():
                for k,v in s.iteritems():
                    if type == "mod": a = self.girl_get(girl, k)
                    elif type == "min": a = girl.stats.min[k]
                    elif type == "max": a = girl.stats.max[k]
                    elif type == "per": a = (girl.stats._get_stat(k) / girl.stats.max[k]) * 100

                    if g == "lt":
                        if a >= v: return False

                    elif g == "le":
                        if a > v: return False

                    elif g == "eq":
                        if a != v: return False

                    elif g == "ne":
                        if a == v: return False

                    elif g == "ge":
                        if a < v: return False

                    elif g == "gt":
                        if a <= v: return False

                    # Those without grouping are assumed to be >=
                    else:
                        if a < s: return False

            return True

        def meetf(self, sub, girl, flags=False):
            """
            Function to check for general variables.
            sub = The dict to check with.
            girl = The girl to check.
            flags = Whether we are checking flags or variables.
            """
            for g,s in sub.iteritems():
                for k,v in s.iteritems():
                    if flags:
                        if k in pytFlagProxyStore: a = pytFlagProxyStore[k].get(girl)
                        elif hasattr(girl.flags, k): a = getattr(girl.flags, k)
                        else: a = 0

                    else:
                        if hasattr(girl, k): a = getattr(girl, k);
                        else:
                            # devlog.warning("Attempt to access a non-existant property in PytStatCheck: %s"%str(k))
                            a = 0


                    if g == "lt":
                        if a >= v: return False

                    elif g == "le":
                        if a > v: return False

                    elif g == "eq":
                        if a != v: return False

                    elif g == "ne":
                        if a == v: return False

                    elif g == "ge":
                        if a < v: return False

                    elif g == "gt":
                        if a <= v: return False

                    # Assume ==
                    else:
                        if a != v: return False

            return True

        def _str(self, sub, flag=False):
            s = ""
            for g,z in sub.iteritems():
                if s != "": s += " and"

                if g == "lt":
                    for i in z.iteritems(): s += " %s < %s"%i

                elif g == "le":
                    for i in z.iteritems(): s += " %s <= %s"%i

                elif g == "eq":
                    for i in z.iteritems(): s += " %s == %s"%i

                elif g == "ne":
                    for i in z.iteritems(): s += " %s != %s"%i

                elif g == "ge":
                    for i in z.iteritems(): s += " %s >= %s"%i

                elif g == "gt":
                    for i in z.iteritems(): s += " %s > %s"%i

                elif flag:
                    s += "%s == %s"%(g,z)

                else:
                    s += "%s >= %s"%(g,z)

            return s

        def _strh(self, sub):
            return " " + ", ".join(sub)


    # Empty changes for when no changes are needed, but an instance still is.
    empty_stat_changes = PytStatChanges()

    # Empty check for when no requirements are needed, but an instance sill is.
    empty_stat_check = PytStatCheck()

    # Empty switch for when no requirements are needed, but an instance still is.
    empty_stat_switch = PytStatSwitch()


    # The store for flag proxies for easy access.
    pytFlagProxyStore = dict()

    class PytFlagProxy(_object):
        """
        A class that acts as an easy accessor/mutator/deletor for character flags.
        """

        def __init__(self, flag, default=False, min=1, max=10, trait=None):
            """
            Creates a new proxy
            flag = The flag to proxy.
            default = The value to return if the flag doesn't exist.
            min = The minimum value for the flag if a number.
            max = The maximum value for the flag if a number.
            trait = The name of a trait to add when the flag is above .
            """
            self.flag = flag
            self.default = default
            self.min = min
            self.max = max
            self.trait = trait

        def __call__(self, girl, to=undefined, relative=False):
            """
            Gets/sets the flag for the girl.
            girl = The girl to access the flag for.
            to = The value to set the flag to, pass BLANK to ignore.
            relative = Whether to set the flag relative to its current value.
            """
            if to is not undefined: self.set(girl, to, relative)
            return self.get(girl)

        def clear(self, girl):
            """
            Deletes the flag from the girl.
            girl = The girl to delete the flag from.
            """
            girl.del_flag(self.flag)
            if self.trait is not None and self.trait in girl.traits:
                girl.apply_trait(traits[self.trait])

        def get(self, girl):
            """
            Returns the flag for the girl.
            girl = The girl to access the flag for.
            """
            if not self.has(girl): return self.default
            else: return girl.flag(self.flag)

        def has(self, girl):
            """
            Check whether the flag exists.
            girl = The girl to check for.
            """
            return girl.has_flag(self.flag)

        def register_for_relative_training(self):
            """
            Registers this proxy as being used in PytStatChanges for relative adjustment of a flag, instead of normal setting.
            """
            pytFlagProxyStore[self.flag] = self
            return self

        def set(self, girl, to, relative=False):
            """
            Sets the flag to a new value.
            girl = The girl to set the flag for.
            to = The value to set the flag to.
            relative = Whether to set the flag relative to its current value.
            """
            if isinstance(to, (int, float)):
                if relative: to += self.get(girl)
                else: to = to

            if to < self.min: self.clear(girl)
            else:
                girl.set_flag(self.flag, to)
                if self.trait is not None and self.trait not in girl.traits:
                    girl.apply_trait(traits[self.trait])


label girl_training:
    show screen girl_training
    with dissolve

    python:
        char = PytGroup(the_chosen) if the_chosen else char
        # Ensure valid school
        if training_screen_current is None:
            for i in schools:
                if schools[i].available:
                    training_screen_current = schools[i]
                    break

        # Ensure valid trainer
        if training_screen_trainer is None:
            training_screen_trainer = hero

        # Ensure valid course if selected
        if training_screen_course is not None:
            if not training_screen_course.can_train(char, training_screen_trainer):
                training_screen_course = None

        while True:
            result = ui.interact()

            if result[0] == "trainer":
                training_screen_trainer = result[1]

            elif result[0] == "open":
                training_screen_course = result[1]

            elif result[0] == "setto":
                # Schooling
                if training_screen_current.is_school:
                    # Slave and combat incompatibility
                    if result[1].type == "Combat" and char.status in ("slave", "various"):
                        renpy.call_screen("message_screen", "Slaves cannot be trained as Warriors!")

                    else:
                        result[1].set_training(char, training_screen_current)

                # Normal training
                else:
                    result[1].set_training(char, training_screen_current, training_screen_trainer)

                break

            # Exit
            elif result[0] == "control" and result[1] == "return":
                break

    hide screen girl_training
    if the_chosen == None:
        jump char_profile
    else:
        jump chars_list



screen girl_training:

    default tt = Tooltip("Perfection is impossible, there are always improvements to be made.")

    # Selection
    vbox:
        style_group "basic"
        null height 44
        hbox:
            for i in schools:
                if schools[i].available:
                    textbutton schools[i].name action TrainingSwitchAction(i)

    # Sub-screen
    if training_screen_current is None:
        null

    elif training_screen_current.is_school:
        use girl_training_schooling

    else:
        use girl_training_trainer

    # Tooltip related:
    frame:
        background Frame("content/gfx/frame/window_frame1.png", 10, 10)
        align(0.5, 0.997)
        xysize (1000, 100)
        xpadding 10
        ypadding 10
        text (u"{=content_text}{color=[ivory]}%s" % tt.value)

    use top_stripe(True)

# Personal sub-screen
screen girl_training_trainer:

    # Trainers:
    frame:
        style_group "content"
        background Frame("content/gfx/frame/arena_d.png", 10, 10)
        area(0, 76, 385, 617)
        has vbox
        null height 3
        frame:
            background Frame("content/gfx/frame/p_frame2.png", 10, 10)
            xysize (365, 25)
            label u"- Trainers -" align (0.5, 0.5) text_size 25 text_color ivory
        null height 3
        side "c r":
            viewport id "trainer_vp":
                area (0, 0, 385, 545)
                draggable False
                mousewheel True
                has vbox
                for trainer in trainers_at_location(training_screen_current):
                    frame:
                        background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                        xysize (358, 75)
                        hbox:
                            null width 5
                            $ girl_image_show = trainer.show("profile", resize=(70, 70), cache=True)
                            imagebutton:
                                align (0, 0.5)
                                idle girl_image_show
                                hover im.MatrixColor(girl_image_show, im.matrix.brightness(0.15))
                                action Return(["trainer", trainer])
                                hovered tt.action("Train girls with %s.\nCurrently training: %s"%(trainer.name, ", ".join([str(g) for g in girls_training_with(hero)])))

                            null width 5

                            vbox:
                                yalign 0.5
                                label (u"[trainer.name]"):
                                    text_size 20
                                    if training_screen_trainer is trainer:
                                        text_color red
                                    else:
                                        text_color ivory
                                null height 5
                                hbox:
                                    text (u"Girls: %d"%len(girls_training_with(trainer))) color ivory size 18
                                    null width 5
                                    text (u"AP: %d"%trainer_total_ap_cost(trainer)) color ivory size 18

            vbar value YScrollValue("trainer_vp")

    # Courses:
    frame:
        background Frame("content/gfx/frame/arena_d.png", 10, 10)
        area (395, 76, 415, 617)
        style_group "content"
        has vbox
        null height 3
        frame:
            background Frame("content/gfx/frame/p_frame2.png", 10, 10)
            xysize (385, 25)
            label u"- Courses -" align (0.5, 0.5) text_size 25 text_color ivory
        null height 3
        side "c r":
            viewport id "course_vp":
                area (0, 0, 420, 545)
                draggable False
                mousewheel True
                hbox:
                    xsize 415
                    box_wrap True
                    spacing 5
                    for course in sorted(training_screen_current.courses):
                        if course.can_train(char, hero, one_off_only=False):
                            frame:
                                background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                                xysize (190, 190)
                                vbox:
                                    xalign 0.5
                                    null height 5
                                    label (u"[course.name]") xalign 0.5
                                    null height 5
                                    frame:
                                        xysize (170, 170)
                                        imagebutton:
                                            align (0.5, 0.5)
                                            idle ProportionalScale(course.get_lesson_image(), 155, 155)
                                            hover im.MatrixColor(ProportionalScale(course.get_lesson_image(), 155, 155), im.matrix.brightness(0.15))
                                            action Return(["open", course])
                                            hovered tt.action(u"%s"%course.desc)
                                    null height 5
            vbar value YScrollValue("course_vp")

    # Course details
    frame:
        background Frame("content/gfx/frame/arena_d.png", 10, 10)
        area (820, 76, 460, 610)
        style_group "content"
        has vbox
        if training_screen_course is not None:
            null height 3
            frame:
                background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                xysize (427, 25)
                label u"- %s -"%training_screen_course.name align (0.5, 0.5) text_size 25 text_color ivory
            null height 3
            side "c r":
                viewport id "lesson_vp":
                    area (0, 0, 440, 545)
                    draggable False
                    mousewheel True
                    hbox:
                        xsize 440
                        box_wrap True
                        spacing 7
                        for course in training_screen_course.get_options(char, training_screen_trainer, one_off_only=False):
                            frame:
                                background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                                xysize (210, 145)
                                use girl_training_lesson(course, tt, False)

                vbar value YScrollValue("lesson_vp")


screen girl_training_lesson(course, tt, show_image):
    vbox:
        style_group "content"
        xalign 0.5
        null height 2

        # Do we have an image
        if show_image:
            # Use plain title
            if course.is_schooling:
                label (u"[course.action]") xalign 0.5 text_color ivory
            else:
                label (u"[course.name]") xalign 0.5 text_color ivory

            null height 2

            # Image is button
            frame:
                xysize (190, 190)
                imagebutton:
                    align (0.5, 0.5)
                    idle ProportionalScale(course.get_lesson_image(), 175, 175)
                    hover im.MatrixColor(ProportionalScale(course.get_lesson_image(), 175, 175), im.matrix.brightness(0.15))
                    action Return(["setto", course])
                    hovered tt.action(u"%s\nGirls being trained: %s"%(course.desc, ", ".join([girl.fullname for girl in hero.chars if char_is_training(girl) is course])))

            null height 3

        # Else
        else:
            # Use title as button
            vbox:
                style_group "basic"
                xalign 0.5

                null height 3

                textbutton (u"[course.%s]"%("action" if course.is_schooling else "name")):
                    xsize 185
                    action Return(["setto", course])
                    hovered tt.action(u"%s\nGirls being trained: %s"%(course.desc, ", ".join([girl.fullname for girl in hero.chars if char_is_training(girl) is course])))

                null height 3

        vbox:
            xalign 0.5
            hbox:
                xalign 0.5
                vbox:
                    xmaximum 120
                    xfill True

                    if not course.is_one_off_event:
                        text "Days:"
                    else:
                        text "Girls AP:"

                    if course.is_schooling:
                        text "Days Left:"

                    else:
                        text "Trainer AP:"

                    text "Daily Fee:"

                    text "Status:"

                vbox:
                    if not course.is_one_off_event:
                        text (u"%s"%(course.duration))

                    else:
                        text (u"%s"%(course.AP))

                    if course.is_schooling:
                        text (u"%s"%(course.daysLeft()))

                    else:
                        text (u"%s"%(course.heroAP))

                    text (u"%s"%(course.gold))

            text (u"%s"%(course.trainerStatus(char, training_screen_trainer)))


# Schools sub-screen
screen girl_training_schooling:
    # Course viewport
    frame:
        background Frame("content/gfx/frame/arena_d.png", 10, 10)
        area (620, 71, 660, 622)
        side "c r":
            viewport id "course_vp":
                area (0, 0, 660, 610)
                draggable False
                mousewheel True
                hbox:
                    xsize 660
                    box_wrap True
                    spacing 7
                    for course in training_screen_current.courses:
                        frame:
                            background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                            xysize (210, 330)
                            xpadding 5
                            ypadding 5
                            use girl_training_lesson(course, tt, True)
            vbar value YScrollValue("course_vp")

    # Detail viewport
    frame:
        style_group "content"
        background Frame("content/gfx/frame/mes11.jpg", 10, 10)
        align (0, 0.7)
        xpadding 10
        ypadding 10
        xysize (610, 610)
        has vbox
        null height 3
        label ("[training_screen_current.name]") xalign 0.5 text_color ivory text_size 25
        null height 3
        add (ProportionalScale("content/schools/school.jpg", 585, 400)) xalign 0.5
        null height 8
        text "The Beautiful educational facilities in PyTFall offer any training one may require for free citizens, foreigners and slaves alike. Century old traditions will make sure that no girl taking classes here will ever be sad or unhappy. Nothing in this world is free however, so courses here might cost you a dime and if you wish to be trained by the Masters, a small fortune." color ivory
        null height 5
        side "c r":
            viewport id "school_vp":
                xsize 580
                draggable False
                mousewheel True
                vbox:
                    xmaximum 610
                    spacing 10
                    text "Girls currently taking courses here:" color ivory
                    for entry in [girl for girl in hero.chars if girl.location == training_screen_current]:
                        hbox:
                            vbox:
                                xmaximum 180
                                xfill True
                                text (u"[entry.fullname]:") color ivory
                            vbox:
                                text (u"[entry.action]") color ivory

            vbar value YScrollValue("school_vp")
