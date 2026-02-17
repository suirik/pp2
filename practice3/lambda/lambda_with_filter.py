ages = [12, 18, 25, 15, 30, 8, 21]

# Filter list to keep only adults (age 18 and over)
adults = list(filter(lambda age: age >= 18, ages))

print(f"All ages: {ages}")
print(f"Adults: {adults}")