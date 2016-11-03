init -9 python:
    def load_schools():
        """
        Creates the valid schools.
        """
        schools = load_training("school", School)
        
        # Load the hero's dungeon
        # school = TrainingDungeon(load_training("training", PytTraining))
        # schools[school.name] = school
        
        # Creates courses
        for school in schools:
            if schools[school].is_school:
                for _ in range(7):
                    schools[school].create_course()
        
        return schools
    
    def load_training(type, clazz):
        """
        Load all the training information from the json files in content/db.
        type = The type of file to load. "(school)_*.json", "(training)_*.json", etc.
        clazz = The class to parse the json objects with.
        """
        dir = content_path("db")
        dirlist = os.listdir(dir)
        training = dict()
        
        for file in dirlist:
            if file.startswith(type) and file.endswith(".json"):
                file = os.path.join(dir, file)
                with open(file) as f:
                    tr = json.load(f)
                    if not isinstance(tr, list): tr = [tr] # Ensure list
                    
                    for i in tr:
                        ptr = clazz(file=str(file), **i)
                        
                        if ptr.name not in training: training[ptr.name] = ptr
                        else:
                            devlog.warning("Duplicate training option \"%s\" was found in %s. Original from %s."%(ptr.name, ptr.file, training[ptr.name].file))
        
        return training
    
    def in_training_location(girl):
        """
        Checks whether a girl is currently in a location that offers training.
        girl = The girl to check.
        """
        return girl.location in schools or girl.location in schools.values()
    
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
    
    # The store for relay proxies for easy access.
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
            trait = The name of a trait to add when the flag is above 0.
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
        
    
    def girl_is_broken(girl):
        """
        Whether the girl has the broken trait.
        girl = The girl to check.
        """
        return "Broken" in girl.traits
    
    # RelayProxy for escape events.
    guard_escape_event = PytRelayProxy("escape_event", use_against=True)
    
    # RelayProxy for obey events.
    trainer_obey_event = PytRelayProxy("obey_event")
    
    # RelayProxy for disobey events.
    trainer_disobey_event = PytRelayProxy("disobey_event", use_against=True)
    
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
            # TODO: May not be upgraded to modern code properly:
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
                    if file.endswith((".png", ".jpg", ".jpeg")):
                        images.append("schools/%s/%s"%(p, file))
            
            # Overwrite image so its used for rest of session
            if len(images) > 0: self.image = choice(images)
            else: self.image = "gfx/interface/images/no_image.png"
            
            return 'content/'+self.image
        
        def get_options(self, girl, hero, one_off_only=None):
            """
            The options that the girl can partake in for the class.
            """
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
            
            # If we have tags
            if self.imageTags:
                # Check and return
                if girl.has_image(*self.imageTags, **kwargs): return girl.show(*self.imageTags, **kwargs)
            
            # Else return profile
            return girl.show("profile", "happy", **kwargs)
        
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
                devlog.error("No response for PytTrainingLesson(%s, %s).get_label(%s)"%(self.type, self.name, state))
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
                    if file.endswith((".png", ".jpg", ".jpeg")):
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
            
            if isinstance(self.based, str):
                if hasattr(store, self.based): f = getattr(store, self.based)(girl)
                else:
                    devlog.error("No scaling function found for PytTrainingScaling \"%s\"."%self.based)
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
                        devlog.warning(str("Attempt to access \"%s\" in STATS and SKILLS for %s in TrainingLesson.get_scaling."%(i, girl.fullname)))
                
                f = float(s)/float(m) # Ensure float
            
            if self.scale == PytTrainingLesson.POS_EFFECT: return f
            elif self.scale == PytTrainingLesson.NEG_EFFECT: return 1-f
            elif self.scale == PytTrainingLesson.POS_TILL_CHECK:
                if isinstance(self.check, str):
                    if hasattr(store, self.check):
                        if getattr(store, self.check)(girl): return f
                        else: return 0
                        
                    else:
                        devlog.error("No check function found for PytTrainingLesson \"%s\"."%self.check)
                        return f
                
                else:
                    if self.check(girl): return f
                    else: return 0
            
            elif self.scale == PytTrainingLesson.NEG_TILL_CHECK:
                if isinstance(self.check, str):
                    if hasattr(store, self.check):
                        if getattr(store, self.check)(girl): return 1-f
                        else: return 0
                        
                    else:
                        devlog.error("No check function found for PytTrainingLesson \"%s\"."%self.check)
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
                    devlog.warning(str("Tried to access \"%s\" in STATS and SKILLS for %s."%(i, hero.fullname)))
            
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
                    s += hero.stats.get_skill(i) * 0.75
                    m += hero.stats.get_skill(i)
                    
                else:
                    devlog.warning(str("Tried to access \"%s\" in STATS and SKILLS for %s."%(i, hero.fullname)))
            
            if s == 0 or m == 0: return 0
            else: return int(s/m) * 100
        
        def trainerStatus(self, girl, hero):
            """
            Returns a description of how well a trainer would teach this lesson for the girl.
            Calculated as:
                H = The the difference between girls knowledge and the trainers knoweldge as a percentage of the trainers knowledge.
                    eg: trainer = 100, girl = 75, result = 0.25
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
                devlog.warning("PytStatChanges encountered a multiplier out of traditional bounds. Mult: %s"%str(mult))
            
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
                            setattr(girl, k, int(v*mult))
            
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
                    else: devlog.warning("Attempt to set non-existant flag in StatChanges: %s = %s"(k, v))
            
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
                    else: devlog.warning("Attempt to call non-existent function in global store \"%s\"."%k)
        
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
                    if not getattr(store, i)(girl): return False
                
                else:
                    devlog.warning("Attempt to call non-existant function in global store \"%s\"."%i)
            
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
                devlog.warning("Tried to access \"%s\" in SKILLS or STATS for %s in StatCheck."%(key, girl.fullname))
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
                            devlog.warning("Attempt to access a non-existant property in PytStatCheck: %s"%str(k))
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
    
    class RunawayManager(_object):
        """
        The class that handles runawawy logic.
        """
        
        STATUS_STATS = ["vitality", "intelligence", "agility"]
        
        ACTION = "Hiding"
        LOCATION = "Unknown"
        
        CAUGHT = "caught"
        DEFEATED = "defeated"
        FOUGHT = "fought"
        ESCAPED = "escaped"
        
        def __init__(self):
            """
            Creates a new RunawwayManager.
            """
            self.girls = dict()
            self.jail_cache = dict()
            self.look_cache = dict()
            
            self.retrieve_jail = False
            
            # Slavemarket stuff
            self.girl = None
            self.index = 0
        
        def __contains__(self, girl):
            """
            Checks whether a girl has runaway.
            """
            return girl in self.girls
        
        def add(self, girl, jail=False):
            """
            Adds a girl that has runaway.
            girl = The girl to add.
            jail = Whether to add straight to jail.
            """
            if girl not in self:
                self.girls[girl] = 0
                girl.action = RunawayManager.ACTION
                girl.location = RunawayManager.LOCATION
                if girl in hero.team: hero.team.remove(girl)
                girl_disobeys(girl, 10)
                
                if jail:
                    self.jail_cache[girl] = [4, False]
                    if self.girl is None:
                        self.girl = girl
                        self.index = 0
        
        def buy_girl(self):
            """
            Buys an escaped girl from the jail.
            """
            if hero.take_ap(1):
                if hero.take_money(self.get_price(), reason="Slave Repurchase"):
                    renpy.play("content/sfx/sound/world/purchase_1.ogg")
                    self.retrieve(self.girl)
                
                else:
                    renpy.call_screen('message_screen', "You don't have enough money for this purchase!")
            
            else:
                renpy.call_screen('message_screen', "You don't have enough AP left for this action!!")
            
            if not self.chars_list:
                renpy.hide_screen("slave_shopping")
        
        def can_escape(self, girl, location, guards=None, girlmod=None, pos_traits=None, neg_traits=["Restrained"], use_be=True, simulate=True, be_kwargs=None):
            """
            Calculates whether a girl can the location.
            girl = The girl check.
            location = The location to check, or None to ignore security and go straight to combat.
            guards = A list of guards to use in combat. If None guards/warriors are pulled from the locaiton.
            girlmod = A dict to use to record the girls stats.
            pos_traits = A list of trait names that increase the girls chance.
            neg_trats = A list of trait names that decrease the girls chance.
            use_be = Whether to require a BE simulation at high security levels.
            simulate = Whether to simulate the battle or use the BE.
            be_kwargs = Keyword arguments to pass to the BE.
            """
            # Ensure stats in girlmod
            if girlmod:
                if "health" not in girlmod: girlmod["health"] = 0
                if "vitality" not in girlmod: girlmod["vitality"] = 0
                if "joy" not in girlmod: girlmod["joy"] = 0
                if "disposition" not in girlmod: girlmod["dosposition"] = 0
                if "exp" not in girlmod: girlmod["exp"] = 0
            
            be_kwargs = dict() if be_kwargs is None else be_kwargs
            # Get traits
            p = 0
            if pos_traits:
                for i in pos_traits:
                    p += girl_training_trait_mult(girl, i)
            
            n = 0
            if neg_traits:
                for i in neg_traits:
                    n += girl_training_trait_mult(girl, i)
            
            # Get security
            if location:
                sec = self.location_security(location)
                runaway = (self.location_runaway(location) + p) < (sec - n)
                
            else:
                sec = 1
                runaway = True
            
            if runaway:
                # If no BE or low security
                if not use_be or sec < 0.5:
                    # Girl escaped without fighting
                    return True, self.ESCAPED
                
                # If girl is too injured to fight
                elif girl.health < 40 or girl.vitality < 40:
                    # Girl was caight without fighting
                    return False, self.CAUGHT
                
                # BE simultaion
                else:
                    # If we need guards
                    if not guards:
                        
                        # If we have no location, girl walks out
                        if not location:
                            return True, self.ESCAPED
                        
                        else:
                            # Get guards if available action
                            if hasattr(location, "actions") and "Guard" in location.actions:
                                guards = [g for g in location.get_girls("Guard") if g.AP > 0 and g.health > 40 and g.vitality > 40]
                            
                            # Get warriors
                            else:
                                guards = [g for g in location.get_girls(occupation="Warrior") if g.AP > 0 and g.health > 40 and g.vitality > 40]
                            
                            if girl in guards: guards.remove(girl)
                            
                            # Force simulation if hero not available
                            if not simulate: simulate = hero.location is not location
                            
                            # If we are simulating
                            if simulate:
                                # Get amount according to location
                                gam = max(int(len(guards) * ((sec-0.5) * 2)), 1)
                                while len(guards) > gam: guards.remove(choice(guards))
                                
                                # Add hero
                                if hero.location is location: guards.append(hero)
                            
                            # Else we are BE
                            else:
                                # If we have more then 2, get the player and 2 random guards
                                if len(guards) > 2:
                                    g = randint(0, len(guards)-1)
                                    guards = [hero, guards[g], guards[g+1]]
                                    pt_ai = [False, True, True]
                                
                                else:
                                    guards.insert(0, hero)
                                    pt_ai = [True for i in guards]
                                    pt_ai[0] = False
                    
                    # If we want to simulate
                    if simulate:
                        
                        # If we end up with no guards
                        if not guards:
                            return True, self.ESCAPED
                        
                        result, exp = s_conflict_resolver(guards, [girl], new_results=True)
                        
                        # Remove hero from guards to avoid event
                        if hero in guards: guards.remove(hero)
                        
                        # Overwhelming victory
                        # Girl was caught without fighting
                        if result == "OV":
                            for g in guards:
                                guard_escape_event.count(g, 1)
                                guard_escape_event.against(g, [girl])
                                guard_escape_event.stats(g, dict(exp=randint(15, 25)))
                                guard_escape_event.win(g, 1)
                            
                            return False, self.CAUGHT
                        
                        # Desisive victory
                        # Girl was caught easily while fighting
                        elif result == "DV":
                            for g in guards:
                                guard_escape_event.count(g, 1)
                                guard_escape_event.against(g, [girl])
                                guard_escape_event.stats(g, dict(health=randint(-10, -20),
                                                                 vitality=randint(-10, -20),
                                                                 exp=exp
                                                                 ))
                                guard_escape_event.win(g, 1)
                            
                            if girlmod:
                                girlmod["health"] -= randint(20, 30)
                                girlmod["vitality"] -= randint(20, 30)
                                girlmod["joy"] -= choice([0,2,2,4,6])
                            
                            else:
                                girl.health -= randint(20, 30)
                                girl.vitality -= randint(20, 30)
                                girl.joy -= choice([0,2,2,4,6])
                            
                            return False, self.DEFEATED
                        
                        # Victory
                        # Girl was caught while fighting
                        elif result == "V":
                            for g in guards:
                                guard_escape_event.count(g, 1)
                                guard_escape_event.against(g, [girl])
                                guard_escape_event.stats(g, dict(health=randint(-10, -20),
                                                                 vitality=randint(-10, -20),
                                                                 exp=exp
                                                                 ))
                                guard_escape_event.win(g, 1)
                            
                            if girlmod:
                                girlmod["health"] -= randint(10, 20)
                                girlmod["vitality"] -= randint(10, 20)
                                girlmod["joy"] -= choice([0,1,1,2,3])
                            
                            else:
                                girl.health -= randint(10, 20)
                                girl.vitality -= randint(10, 20)
                                girl.joy -= choice([0,1,2,2,3])
                            
                            return False, self.DEFEATED
                        
                        # Lucky victory
                        # Girl was bearly caught while fighting
                        elif result == "LV":
                            for g in guards:
                                guard_escape_event.count(g, 1)
                                guard_escape_event.against(g, [girl])
                                guard_escape_event.stats(g, dict(health=randint(-20, -30),
                                                                 vitality=randint(-20, -30),
                                                                 ))
                                guard_escape_event.win(g, 1)
                            
                            if girlmod:
                                girlmod["health"] -= randint(10, 20)
                                girlmod["vitality"] -= randint(10, 20)
                                girlmod["exp"] += exp
                            
                            else:
                                girl.health -= randint(10, 20)
                                girl.vitality -= randint(10, 20)
                                girl.exp += exp
                            
                            return False, self.DEFEATED
                        
                        # Defeat
                        # Girl was able to escape while fighting
                        elif result == "D":
                            for g in guards:
                                guard_escape_event.count(g, 1)
                                guard_escape_event.against(g, [girl])
                                guard_escape_event.stats(g, dict(health=randint(-20, -30),
                                                                 vitality=randint(-20, -30),
                                                                 ))
                                guard_escape_event.loss(g, 1)
                            
                            if girlmod:
                                girlmod["health"] -= randint(10, 20)
                                girlmod["vitality"] -= randint(10, 20)
                                girlmod["exp"] += exp
                                girlmod["joy"] += choice([0,1,1,2,3])
                            
                            else:
                                girl.health -= randint(10, 20)
                                girl.vitality -= randint(10, 20)
                                girl.exp += exp
                                girl.joy += choice([0,1,1,2,3])
                            
                            return True, self.FOUGHT
                        
                        # Overwhelming defeat
                        # Girl was able to escape without fighting
                        elif result == "OD":
                            for g in guards:
                                guard_escape_event.count(g, 1)
                                guard_escape_event.against(g, [girl])
                                guard_escape_event.loss(g, 1)
                            
                            if girlmod:
                                girlmod["exp"] += exp
                                girlmod["joy"] += choice([0,2,2,4,6])
                            
                            else:
                                girl.exp += exp
                                girl.joy += choice([0,2,2,4,6])
                            
                            return True, self.ESCAPED
                    
                    else:
                        # Fight!
                        # TODO (Alex) Check out what this is/does:
                        result, dead = start_battle(guards, [girl], pt_ai=pt_ai, **be_kwargs)
                        
                        exp = (girl.attack + girl.defence + girl.agility + girl.magic) / 10
                        
                        # Remove hero from guards to avoid event
                        if hero in guards: guards.remove(hero)
                        
                        # If the guards won
                        if result:
                            for g in guards:
                                guard_escape_event.count(g, 1)
                                guard_escape_event.against(g, [girl])
                                guard_escape_event.stats(g, dict(vitality=-randint(-10, -20),
                                                                 exp=exp
                                                                 ))
                                guard_escape_event.win(g, 1)
                            
                            if girlmod:
                                girlmod["vitality"] -= randint(10, 20)
                                girlmod["joy"] -= choice([0,1,1,2,3])
                            
                            else:
                                girl.health -= randint(10, 20)
                                girl.joy -= choice([0,1,1,2,3])
                            
                            return True, self.DEFEATED
                        
                        # Else the girl won
                        else:
                            for g in guards:
                                guard_escape_event.count(g, 1)
                                guard_escape_event.against(g, [girl])
                                guard_escape_event.stats(g, dict(vitality=-randint(-10, -20),
                                                                 exp=exp
                                                                 ))
                                guard_escape_event.loss(g, 1)
                            
                            if girlmod:
                                girlmod["vitality"] -= randint(10, 20)
                                girlmod["exp"] += exp
                                girlmod["joy"] += choice([0,1,1,2,3])
                            
                            else:
                                girlmod.vitality -= randint(10, 20)
                                girlmod.exp += exp
                                girl.joy += choice([0,1,1,2,3])
                            
                            return False, self.FOUGHT
            
            else:
                return False
        
        def get_look_around_girl(self, event):
            """
            Gets the girl for the event.
            event = The event to return the girl for.
            """
            return self.look_cache.pop(event.name, None)
        
        def get_price(self):
            """
            Returns the price to retieve the girl.
            """
            # In case non-slaves escape, use 3000 as base price
            base = self.girl.fin.get_price() or 3000
            time = float(self.jail_cache[self.girl][0])
            return int(base * (0.75 - (0.125 * time)))
        
        def get_whore_price(self):
            """
            Return the whore cost for the girl.
            """
            return self.girl.fin.get_whore_price()
        
        def get_upkeep(self):
            """
            Return the upkeep cost for the girl.
            """
            return self.girl.fin.get_upkeep()
        
        @property
        def girlfin(self):
            """
            The property to return the proper financial data for the girl.
            """
            return self
        
        @property
        def chars_list(self):
            """
            The list to use for the slavemarket interface.
            """
            if self.jail_cache: return self.jail_cache.keys()
            else: return []
        
        def location_runaway(self, location, sutree=None):
            """
            Returns a runaway chance for the location.
            location = The location to calculate the chance for.
            sutree = The name of the security upgrade tree to use if not default.
            
            Calculates the chance using:
            - The mod_runaway function if it exists.
            - The sutree current / total, if it exists.
            - The amount of guards in the location, if the action exists.
            - The amount of warriors in the location
            
            Returns:
            0 = high chance.
            1 = low chance
            """
            # Get runaway modifier
            mod = 0
            
            # If location has own function, use it
            if hasattr(location, "mod_runaway"):
                mod = location.mod_runaway()
            
            # Else if location is upgradable, use its sutree
            elif isinstance(location, UpgradableBuilding):
                if sutree is None: sutree = location.security_upgrade_tree
                mod = self.get_upgrade_mod(sutree) / len(self.upgrades[sutree])
            
            # Else if has guard action, use amount over total
            elif hasattr(location, "actions") and "Guard" in location.actions:
                girls = [g for g in hero.chars if g.location == location]
                if girls:
                    mod = float(len(location.get_girls("Guard"))) / float(len(girls))
                else:
                    mod = 0
            
            # Else use warriors over total
            else:
                girls = [g for g in hero.chars if g.location == location]
                if girls:
                    mod = float(len(location.get_girls(occupation="Warrior"))) / float(len(girls))
                else:
                    mod = 0
            
            return mod
        
        def location_security(self, location, modifier=1):
            """
            Returns the security modifier for the location.
            location = The location to get the modifier for.
            modifier = A multiplier for the final modifier.
            
            Returns:
            1 = low chance
            2 = high chance
            """
            return (renpy.random.random() * (2 - location.security_mult())) * modifier
        
        def next_day(self):
            """
            Solves the next day logic for the girls.
            """
            girls = self.girls.keys()
            cdb = config.developer
            type = "schoolndreport"
            txt = ["Escaped girls:"]
            
            # Replace with better code to prevent mass-creation/destruction of events?
            # Clean look_cache
            for i in self.look_cache.keys():
                pytfall.world_events.kill_event(i, cached=True)
                del self.look_cache[i]
            
            # Clean jail_cache
            for i in self.jail_cache.keys():
                if self.jail_cache[i][0] == 0:
                    del self.jail_cache[i]
                
                else:
                    self.jail_cache[i][0] -= 1
            
            # Loop through girls
            while girls:
                girl = choice(girls)
                girls.remove(girl)
                cdb = config.developer
                txt.append("    %s"%girl.fullname)
                
                # Increase girls escape time
                self.girls[girl] += 1
                
                # Get status
                status = self.status(girl)
                if cdb: txt.append("{color=[blue]}        status: %s{/color}"%status)    
                
                # If girl is free
                if girl not in self.jail_cache:
                    # Chance to escape for good
                    if self.girls[girl] > 20:
                        if dice(status) and dice(self.girls[girl]):
                            del self.girls[girl]
                            hero.remove_char(girl)
                            
                            if cdb: txt.append("{color=[blue]}        escaped for good{/color}")
                            continue
                    
                    # Chance to go to jail
                    if self.girls[girl] > 10:
                        if dice(status) and len(self.jail_cache) < 10:
                            self.jail_cache[girl] = [4, False]
                            
                            if cdb: txt.append("{color=[blue]}        sent to jail for 4 days (%s days till escape){/color}"%(20-self.girls[girl]))
                            continue
                    
                    # Chance to find in look_around
                    if dice(status) and len(self.look_cache) < 5:
                        ev = "runaway_look_around_%s"%str(girl)
                        self.look_cache[ev] = girl
                        # Add event for girl (do we want high priority?)
                        register_event_in_label(ev, label=girl.runaway_look_event, trigger_type="look_around", locations=["all"], dice=status, max_runs=1, start_day=day+1, priority=999)
                        
                        if cdb: txt.append("{color=[blue]}        in look around (%s days till escape){/color}"%(20-self.girls[girl]))
                        continue
                    
                    if cdb: txt.append("{color=[blue]}        %s days till escape{/color}"%(20-self.girls[girl]))
                
                # Else if girl is jailed
                else:
                    # If we know they're in jail
                    if self.jail_cache[girl][1]:
                        txt.append("    %s, in jail for %s days"%(girl.fullname, self.jail_cache[girl][0]))
                        if cdb: txt.append("{color=[blue]}    (%s days till escape){/color}"%(20-self.girls[girl]))
                    
                    # Else
                    else:
                        txt.append("    %s"%girl.fullname)
                        if cdb: txt.append("{color=[blue]}        in jail for %s days (%s days till escape){/color}"%(self.jail_cache[girl], (20-self.girls[girl])))
            
            # Slavemarket update
            self.index = 0
            if self.jail_cache:
                self.girl = self.chars_list[0]
            
            # If we have escaped girls, post the event
            if self.girls:
                ev = NDEvent()
                ev.type = type
                ev.char = None
                ev.img = im.Scale("content/gfx/bg/locations/city_jail.jpg", int(config.screen_width*0.6), int(config.screen_height*0.8))
                ev.txt = "\n".join(txt)
                NextDayEvents.append(ev)
        
        def next_index(self):
            """
            Sets the next index for the slavemarket.
            """
            self.index = (self.index+1) % len(self.chars_list)
            self.girl = self.chars_list[self.index]
        
        def previous_index(self):
            """
            Sets the previous index for the slavemarket.
            """
            self.index = (self.index-1) % len(self.chars_list)
            self.girl = self.chars_list[self.index]
        
        def retrieve(self, girl):
            """
            Returns a girl to the player.
            girl = The girl to return.
            """
            if girl in self:
                del self.girls[girl]
                
                ev = "runaway_look_around_%s"%str(girl)
                if ev in self.look_cache:
                    del self.look_cache[ev]
                    pytfall.world_events.kill_event(ev)
                
                if girl in self.jail_cache:
                    del self.jail_cache[girl]
                    
                    if self.jail_cache:
                        self.index %= len(self.jail_cache)
                        self.girl = self.chars_list[self.index]
                    
                    else:
                        self.index = 0
                        self.girl = None
                
                girl.action = None
                
                if schools[TrainingDungeon.NAME] in hero.buildings:
                    girl.location = schools[TrainingDungeon.NAME]
                
                else:
                    girl.location = hero
        
        def set_girl(self, girl):
            """
            Sets the girl to be the index for the slavemarket.
            girl = The girl to set.
            """
            if self.chars_list and girl in self.chars_list:
                self.girl = girl
                self.index = self.chars_list.index(self.girl)
        
        def status(self, girl):
            """
            Returns the "runaway status" of the girl.
            girl = The girl to get the status for.
            """
            a = 0
            b = 0
            for i in self.STATUS_STATS:
                a += girl.stats[i]
                b += girl.stats.max[i]
            
            status = (float(a) / float(b)) * 100
            status *= girl_training_trait_mult(girl, "Restrained")
            if girl.status == "slave": status *= 0.75
            
            return 100-status
        
    
