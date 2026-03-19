from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# Task 1: map() and filter()
squared = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Task 2: reduce() (Aggregation - Summing the list)
total_sum = reduce(lambda a, b: a + b, numbers)

print(f"Squared: {squared}")
print(f"Evens: {evens}")
print(f"Total Sum: {total_sum}")