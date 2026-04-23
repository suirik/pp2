# The __init__ method is a constructor that runs when a new object is created
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

# Creating objects with specific data
s1 = Student("Saida", 95)
s2 = Student("Alikhan", 88)

print(f"Student 1: {s1.name}, Grade: {s1.grade}")
print(f"Student 2: {s2.name}, Grade: {s2.grade}")