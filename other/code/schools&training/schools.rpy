init python:
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
                            # devlog.warning("Duplicate training option \"%s\" was found in %s. Original from %s."%(ptr.name, ptr.file, training[ptr.name].file))
                            pass

        return training

    class School(BaseBuilding):
        """
        Building that represents the school.

        Convert to SimPy?

        Issues:
            Courses are infinite.
            Too much EXP.
            Courses may not correspond to modern jobs.
        """

        #"primary": [1,1,1,0,1,1,1,1,1,1,1,1,2,0],
        #"secondary": [0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,2],
        #"tprimary": [1,1,1,0,1,1,1,1,1,1,1,1,2,3],
        #"tsecondary": [0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,2,2],
        #"sprimary": [1,1,0,0,1,1,1,1,1,1,0,1,0,2],
        #"ssecondary": [0,0,0,1,0,1,0,0,1,0,0,0,1,1,1,1,0,0,0,0,1,2],

        def __init__(self, id="-PyTFall Educators-", image="content/schools/school.webp",
                     primary=0, secondary=0, skillPrimary=None, skillSecondary=None,
                     options=None, file=None):
            """
            Creates a new schoool.
            id = The name of the school.
            image = The image for the school.
            primary = The primary stat increase.
            secondary = The secondary stat increase.
            options = The courses available.
            file = The json file this school was loaded from.
            """
            super(School, self).__init__(id=id, name=id)

            self.img = image

            self.primary = primary
            self.secondary = secondary
            self.skill_primary = skillPrimary or primary
            self.skill_secondary = skillSecondary or secondary

            self.fin = Finances(self)
            self.income = 0

            # Dict
            self.all_courses = options

            # List
            self.courses = []

            self.income = 0

            self.events_relay = {
                "runaway": [0, 0], # successful, prevented
                "disobey": [0, 0], # successful, prevented
                "obey": [0, 0], # from training success, random
                "finish": [0, 0] # end of course, no longer eligible
            }

            # For one off events
            self.one_off_events = list()

            # For debugging purposes
            self.file = None

        @property
        def available(self):
            """
            Whether this building is available.
            """
            return True

        def create_course(self):
            """
            Creates a random course from the courses dictionary.
            """
            key = choice(self.all_courses.keys())
            course = deepcopy(self.all_courses[key])

            x = dict()
            for i in course["primary"]:
                if i in PytCharacter.SKILLS: x[i] = self.skill_primary
                else: x[i] = self.primary

            course["primary"] = PytStatChanges(mod=x)

            x = dict()
            for i in course["secondary"]:
                if i in PytCharacter.SKILLS: x[i] = self.skill_secondary
                else: x[i] = self.secondary

            course["secondary"] = PytStatChanges(mod=x)

            course = SchoolLesson(key, **course)

            self.courses.append(course)

        @property
        def is_school(self):
            """
            Whether or not this building is a school.
            """
            return True

        def log_income(self, char, value):
            """
            Logs the schools income.
            char = The character who the income is being spent for.
            value = The amount being spent.
            """
            hero.take_money(value, reason=self.name)
            self.income += value
            char.fin.log_logical_expense(value, "Training")

        def next_day(self):
            """
            Solves the next day notifications for schooling.
            """
            # Logic
            type = "schoolndreport"
            img = im.Scale(self.img, int(config.screen_width*0.6), int(config.screen_height*0.8))
            txt = "%s Report: \n"%self.name
            evtlist = []
            char = None

            girls = [girl for girl in hero.chars if girl.location == self.name]

            if not girls:
                txt += "Excellent courses are available today! Remember our Motto: Education is Gold! \n"
            else:
                txt += choice(["You currently have %d girls training with us! \n" % len(girls),
                               "Excellent courses are available today! Remember our Motto: Education is Gold! \n"])

            # Add courses
            tempval = len(self.courses)
            if len(self.courses) < 10:
                self.create_course()

            if dice(50):
                if len(self.courses) < randint(10, 20):
                    self.create_course()

            if dice(10):
                if len(self.courses) < 30:
                    self.create_course()

            if tempval < len(self.courses):
                txt += "We inform you about fresh courses starting today. Please check in with us if you are interested. \n"

            # Checking if girl has completed the course:
            for course in self.courses:
                for girl in girls:
                    if str(girl) in course.chars:
                        cdays = int(course.duration*.7)

                        if course.chars[str(girl)] >= cdays:
                            if str(girl) in course.complete:
                                pass
                            else:
                                course.complete[str(girl)] = True
                                self.events_relay["finish"][0] += 1

                                # Final increase
                                course.primary(girl, mult=course.get_scaling(girl))
                                course.secondary(girl, mult=course.get_scaling(girl))

                                if dice(20):
                                    for stat in course.primary.mod:
                                        girl.stats.max[stat] += choice([0, 1])

                                txt += "\n\n{color=[lawngreen]}%s has successfully completed %s and got a nice extra bonus to her stats! \n{/color}"%(girl.name, course.action)

            # Day Count
            for course in self.courses:
                course._daysLeft -= 1

            # End courses and remove girls
            for course in self.courses:
                if course._daysLeft <= 0:
                    for girl in girls:
                        if girl_course_id(girl) == course.id:
                            txt += "Course that %s is attending is at it's end! "%girl.name
                            stop_training(girl)

                    self.courses.remove(course)

            # Event summery
            for i in self.events_relay:
                j, k = self.events_relay[i]
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

            evt = NDEvent(type=type, txt=txt, img=img, char=char)
            NextDayEvents.append(evt)
