init python:
    class SchoolCourse(_object):
        def __init__(self, name, difficulty, duration, days_to_complete,
                     effectiveness, data):
            self.name = name
            # self.trainer = trainer # restore after ST.
            self.difficulty = difficulty
            self.students = []
            self.students_progress = {}
            self.completed = set() # Students that completed this course
            self.duration = self.days_remaining = duration
            self.days_to_complete = days_to_complete # 25 or about 80% of duration is normal.
            self.effectiveness = effectiveness

            self.data = data

            self.set_image()
            self.set_price()

        def set_price(self):
            price = get_average_wage()
            price = price + price*self.difficulty
            self.price = round_int(price)

        def set_image(self):
            images = []
            folder = "content/schools/" + self.data["image"]
            for fn in renpy.list_files():
                if folder in fn and fn.endswith(IMAGE_EXTENSIONS):
                    images.append(fn)

            if not images:
                self.img = renpy.displayable("no_image")
            else:
                img = choice(images)
                self.img = renpy.displayable(img)

        def get_status(self, char):
            if char in self.students:
                return "Active!"

            days_to_complete = self.days_to_complete
            duration = self.duration

            if days_to_complete < duration*.65:
                dtc = " and Fast"
            elif days_to_complete < duration*.75:
                dtc = ""
            else:
                dtc = " and Slow"

            if self.difficulty >= char.tier+2:
                temp = "Great"
            elif self.difficulty >= char.tier:
                temp = "Good"
            else:
                temp = "Bad"

            return temp + dtc

        @property
        def tooltip(self):
            tt = self.data.get("desc", "No Description Available")

            temp = []
            for s in self.students:
                temp.append(s.nickname)

            if temp:
                tt += "\nStudents: "
                tt += ", ".join(temp)

            return tt

        def add_student(self, student):
            if student not in self.students:
                self.students.append(student)
            if student not in self.students_progress:
                self.students_progress[student] = 0
            student.action = self

        def remove_student(self, student):
            if student in self.students:
                self.students.remove(student)
            student.workplace = None
            student.action = None

        def next_day(self):
            self.days_remaining -= 1

            students = [s for s in self.students if s.AP > 0]
            if not students:
                return

            if len(students) >= 3 and dice(25):
                best_student = choice(students)
            else:
                best_student = None

            for char in self.students[:]:
                txt = [] # Append all events we want to relay to the player.
                flag_green = False

                temp = "{} is taking a {} Course!".format(char.fullname,
                                                          self.name)
                txt.append(temp)

                # Pay for the class:
                if hero.take_money(self.price, reason="-PyTFall Educators-"):
                    char.fin.log_logical_expense(self.price, "-PyTFall Educators-")
                    temp = "You've covered a fee of {color=[gold]}%s Gold!{/color}" % self.price
                    txt.append(temp)
                else:
                    self.remove_student(char)
                    temp = "\nYou failed to cover the fee of {color=[gold]}%d Gold!{/color}." % self.price
                    temp += " The student has been kicked from the class!"
                    txt.append(temp)

                    self.build_nd_report(char, type="failed_to_pay", txt=txt)
                    continue

                completed = self.days_to_complete - self.students_progress.get(char, 0) <= 0

                self.students_progress[char] += 1
                days_to_complete = self.days_to_complete # Mod on traits?
                ap_spent = char.AP
                char.AP = 0

                primary_stats = []
                secondary_stats = []

                primary_skills = []
                secondary_skills = []

                for s in self.data["primary"]:
                    if char.stats.is_stat(s):
                        if getattr(char, s) < char.get_max(s):
                            primary_stats.append(s)
                    elif char.stats.is_skill(s):
                        primary_skills.append(s)
                    else:
                        raise Exception("{} is not a valid stat/skill for {} course.".format(
                                s, self.name
                        ))

                for s in self.data["secondary"]:
                    if char.stats.is_stat(s):
                        if getattr(char, s) < char.get_max(s):
                            secondary_stats.append(s)
                    elif char.stats.is_skill(s):
                        secondary_skills.append(s)
                    else:
                        raise Exception("{} is not a valid stat/skill for {} course.".format(
                                s, self.name
                        ))

                stats = primary_stats*3 + secondary_stats
                skills = primary_skills*3 + secondary_skills
                exp = exp_reward(char, self.difficulty,
                                 ap_used=ap_spent)
                charmod = defaultdict(int) # Dict of changes of stats and skills for ND

                # Add stats/skills/exp mods.
                points = max(1, self.difficulty-char.tier)
                if char == best_student:
                    temp = "%s has been a perfect student today and went every extra mile she could." % char.name
                    temp += " {color=[lawngreen]}+50% Stats/Skills/EXP Bonus!{/color}"
                    flag_green = True
                    txt.append(temp)
                    points *= 1.5
                    exp *= 1.5

                if completed and char not in self.completed:
                    self.completed.add(char)
                    points *= 2
                    exp *= 2
                    temp = "%s has completed the course today!" % char.nickname
                    temp += " {color=[lawngreen]}+100% Stats/Skills/EXP Bonus!{/color}"
                    flag_green = True
                    txt.append(temp)
                elif char in self.completed:
                    points *= .8
                    exp *= .8
                    temp = "%s has already finished this course!" % char.nickname
                    temp += " {color=[red]}-20% Stats/Skills/EXP Bonus!{/color}"
                    txt.append(temp)

                # Effectiveness mod (simple)
                effectiveness = self.effectiveness/100.0
                points *= effectiveness

                stats_pool = round_int(points*ap_spent)
                skills_pool = round_int(points*2*ap_spent)

                exp = round_int(exp)
                char.exp += exp
                charmod["exp"] = exp

                if stats:
                    for i in xrange(stats_pool):
                        stat = choice(stats)
                        char.mod_stat(stat, 1)
                        charmod[stat] += 1
                if skills:
                    for i in xrange(skills_pool):
                        skill = choice(skills)
                        char.mod_skill(skill, 1)
                        charmod[skill] += 1

                if self.days_remaining <= 0:
                    txt.append("This Course has ended, all students have been sent back home.")
                    self.remove_student(char)

                self.build_nd_report(char, charmod=charmod,
                                     flag_green=flag_green, txt=txt)

        def build_nd_report(self, char, charmod=None, type="normal",
                            txt=None, flag_green=False):
            if txt is None:
                txt = str(self.name) + " Testing string."
            else:
                txt = "\n".join(txt)

            if type == "normal":
                evt = NDEvent()
                evt.type = "course_nd_report"
                evt.charmod = charmod
                evt.red_flag = False
                evt.green_flag = flag_green
                evt.loc = schools["-PyTFall Educators-"]
                evt.char = char
                evt.txt = txt
                # Get char image from data:
                tags = self.data.get("imageTags", ["profile"])
                mode = self.data.get("imageMode", "reduce")
                kwargs = dict(exclude=self.data.get("noImageTags", []),
                              resize=(820, 705), type=mode, add_mood=False)
                evt.img = char.show(*tags, **kwargs)

                NextDayEvents.append(evt)
            elif type == "failed_to_pay":
                evt = NDEvent()
                evt.type = "course_nd_report"
                # evt.charmod = charmod
                evt.red_flag = True
                evt.loc = schools["-PyTFall Educators-"]
                evt.char = char
                evt.img = self.img # TODO Replace with char image?
                evt.txt = ""
                NextDayEvents.append(evt)


    class School(BaseBuilding):
        def __init__(self, id="-PyTFall Educators-",
                     img="content/schools/school.webp"):
            super(School, self).__init__(id=id, name=id)
            self.img = renpy.displayable(img)
            self.courses = []

        @property
        def is_school(self):
            """
            Whether or not this building is a school. Used in training screen.
            """
            return True

        def add_courses(self):
            forced = max(0, 12-len(self.courses))
            for i in range(forced):
                self.create_course()

            if dice(50) and len(self.courses) < 20:
                self.create_course()

            if dice(10) and len(self.courses) < 30:
                self.create_course()

        def remove_course(self, course):
            if course in self.courses:
                self.courses.remove(course)

        def create_course(self):
            id = choice(school_courses.keys())

            v0 = max(0, hero.tier - 1)
            v1 = min(10, hero.tier + 3)
            difficulty = randint(v0, v1)

            duration = randint(20, 40)
            days_to_complete = round_int(duration*random.uniform(.5, .75))
            effectiveness = randint(60, 100)
            data = school_courses[id]

            course = SchoolCourse(id, difficulty, duration,
                                  days_to_complete, effectiveness,
                                  data)
            self.courses.append(course)

        def next_day(self):
            for c in self.courses[:]:
                c.next_day()
                if c.days_remaining <= 0:
                    self.remove_course(c)

            self.add_courses()
            self.build_nd_report()

        def build_nd_report(self):
            txt = []
            type = "school_nd_report"

            temp = "{} Report: \n".format(self.name)
            txt.append(temp)

            students = self.get_all_chars()

            if not students:
                txt.append("Excellent courses are available here today! Remember our Motto: Education is Gold!")
            else:
                temp = choice(["You currently have %d students training with us!" % len(students),
                               "Excellent courses are available today! Remember our Motto: Education is Gold!"])
                txt.append(temp)

            if students:
                txt.append("\n")
                txt.append("Students:")
                for s in students:
                    txt.append("  {}".format(s.name))

            img = pscale(self.img, 820, 705)
            txt = "\n".join(txt)

            evt = NDEvent(type=type, txt=txt, img=img)
            NextDayEvents.append(evt)


    def stop_course(char):
        course = char.action
        course.remove_student(char)
