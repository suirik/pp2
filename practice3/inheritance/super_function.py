class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, graduation_year):
        # super() links the child to the parent's constructor
        super().__init__(name)
        self.graduation_year = graduation_year

    def info(self):
        print(f"{self.name} will graduate in {self.graduation_year}")

s = Student("Ali", 2026)
s.info()