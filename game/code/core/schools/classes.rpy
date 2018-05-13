init python:
    class SchoolCourseNew(_object):
        def __init__(self, trainer):
            self.trainer = trainer
            self.students = []
            self.students_progress = {}
            self.completed = set() # Students that completed this course
            self.duration = 30

            self.stats = {}
            self.skills = {}

        def add_student(self, student):
            self.students.append(student)
            if student not in self.students_progress:
                self.students_progress[student] = 0

        def remove_student(self):
            self.students.remove(student)

        def next_day(self):
            pass


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
            pass

        def next_day(self):
            pass
