init python:
    class SchoolCourseNew(_object):
        def __init__(self, name, difficulty, data):
            self.name = name
            # self.trainer = trainer # restore after ST.
            self.difficulty = difficulty
            self.students = []
            self.students_progress = {}
            self.completed = set() # Students that completed this course
            self.duration = self.days_remaining = 30

            self.data = data

        def add_student(self, student):
            self.students.append(student)
            if student not in self.students_progress:
                self.students_progress[student] = 0

        def remove_student(self):
            self.students.remove(student)

        def next_day(self):
            self.days_remaining -= 1


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

            course = SchoolCourseNew(id, difficulty, data)
            self.courses.append(course)

        def next_day(self):
            for c in self.courses[:]:
                c.next_day()
                if c.days_remaining <= 0:
                    self.courses.remove(c)
