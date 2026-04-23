# A list of tuples (Subject, Grade)
grades = [("Math", 88), ("Physics", 95), ("History", 82)]

# Sort by grade (the second element in each tuple)
grades.sort(key=lambda x: x[1])

print("Subjects sorted by grades (lowest to highest):")
print(grades)