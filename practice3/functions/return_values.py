# A function that calculates and returns a result
def multiply_numbers(a, b):
    return a * b

# Storing the returned value in a variable
result = multiply_numbers(10, 5)
print(f"The result of the multiplication is: {result}")

# Using return in a conditional
def check_even(number):
    if number % 2 == 0:
        return True
    return False

print(f"Is 8 even? {check_even(8)}")