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
            self.students.append(student)
            if student not in self.students_progress:
                self.students_progress[student] = 0

        def remove_student(self):
            self.students.remove(student)

        def next_day(self):
            self.days_remaining -= 1

            students = [s for s in self.students if s.AP > 0]
            if not students:
                return

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


    class School(BaseBuilding):
        def __init__(self, id="-PyTFall Educators-",
                     img="content/schools/school.webp"):
            super(School, self).__init__(id=id, name=id)
            self.img = renpy.displayable(img)
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

            v0 = max(0, hero.tier - 1)
            v1 = min(10, hero.tier + 3)
            difficulty = randint(v0, v1)

            duration = randint(20, 40)
            days_to_complete = round_int(duration*random.uniform(.5, .85))
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
                    self.courses.remove(c)

            self.add_courses()
