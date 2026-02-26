# 1.Create a generator that generates the squares of numbers up to some number N.
# This generator calculates squares on the fly, which is more memory-efficient than creating a full list.

def square_generator(N):
    for i in range(N + 1):
        yield i ** 2

# Example usage:
# for sq in square_generator(5):
#     print(sq)



# 2.Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.
# This task requires taking input from the console and formatting the generator output as a string.

def even_generator(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)

n = int(input("Enter a number for even sequence: "))
gen = even_generator(n)
print(",".join(gen))





# 3. Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.
# A number divisible by both 3 and 4 is essentially divisible by 12.

def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# Example usage:
# for num in divisible_by_3_and_4(50):
#     print(num)





# 4. Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.
# This allows you to define a specific range rather than starting from zero.
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

# Testing with a for loop
print("Squares from 3 to 7:")
for val in squares(3, 7):
    print(val)





# 5. Implement a generator that returns all numbers from (n) down to 0.
# This uses a downward range to return numbers in reverse order.

def countdown(n):
    while n >= 0:
        yield n
        n -= 1

# Example usage:
# for num in countdown(5):
#     print(num)