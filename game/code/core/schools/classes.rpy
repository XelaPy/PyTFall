init python:
    class SchoolCourseNew(_object):
        def __init__(self, name, difficulty, duration, days_to_complete,
                     effectiveness, base_price, data):
            self.name = name
            # self.trainer = trainer # restore after ST.
            self.difficulty = difficulty
            self.students = []
            self.students_progress = {}
            self.completed = set() # Students that completed this course
            self.duration = self.days_remaining = 30
            self.days_to_complete = days_to_complete # 25 or about 80% of duration is normal.
            self.effectiveness = effectiveness

            self.data = data

        @property
        def price(self):
            # For implementation:
            # Average Wage vs difficulty.
            return 100

        def status(self, char):
            days_to_complete = self.days_to_complete
            duration = self.duration

            if days_to_complete < duration*.65:
                dtc = "fast"
            elif days_to_complete < duration*.75:
                dtc = ""
            else:
                dtc = "slow"

            # Add

        def add_student(self, student):
            self.students.append(student)
            if student not in self.students_progress:
                self.students_progress[student] = 0

        def remove_student(self):
            self.students.remove(student)

        def next_day(self):
            self.days_remaining -= 1

            students = [s for s in self.students if s.AP > 0]

            if len(students) >= 3 and dice(25):
                best_student = choice(students)
            else:
                best_student = None

            for char in self.students:
                self.students_progress[char] += 1
                days_to_complete = self.days_to_complete # Mod on traits?
                ap_spent = char.AP

                if char == best_student:
                    pass

                # Add stats/skills/exp mods.

                char.AP = 0


    class SchoolNew(BaseBuilding):
        ID = "-PyTFall Educators-"
        IMG = "content/schools/school.webp"

        def __init__(self):
            super(School, self).__init__(id=ID, name=IMG)
            self.courses = []

        def add_cources(self):
            forced = max(0, 12-len(self.courses))
            for i in range(forced):
                self.create_course()

            if dice(50) and len(self.courses) < 20:
                self.create_course()

            if dice(10) and len(self.courses) < 30:
                self.create_course()

        def create_course(self):
            id = choice(school_courses.keys())
            data = school_courses[id]

            v0 = max(0, hero.tier - 1)
            v1 = min(10, hero.tier + 3)
            difficulty = randint(v0, v1)

            duration = randint(20, 40)
            days_to_complete = round_int(duration*random.uniform(.5, .85))

            course = SchoolCourseNew(id, difficulty, duration,
                                     days_to_complete, effectiveness,
                                     base_price, data)
            self.courses.append(course)

        def next_day(self):
            for c in self.courses[:]:
                c.next_day()
                if c.days_remaining <= 0:
                    self.courses.remove(c)

            self.add_courses()
