# 1. Write a Python program to convert degree to radian.
# To convert degrees to radians, you use the formula Radian=Degree×(π/180) or the built-in math.radians() function.

import math

degree = float(input("Input degree: "))
radian = math.radians(degree)
print(f"Output radian: {radian:.6f}")



# 2. Write a Python program to calculate the area of a trapezoid.
# The formula is Area=(base1+base2)​/ 2 × height.

height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area = ((base1 + base2) / 2) * height
print(f"Expected Output: {area}")



# 3. Write a Python program to calculate the area of regular polygon.

import math

n_sides = int(input("Input number of sides: "))
side_length = float(input("Input the length of a side: "))

area = (n_sides * side_length**2) / (4 * math.tan(math.pi / n_sides))
print(f"The area of the polygon is: {int(area)}")



# 4. Write a Python program to calculate the area of a parallelogram.
# The formula is Area=base×height.

base_length = float(input("Length of base: "))
height_para = float(input("Height of parallelogram: "))

area_para = base_length * height_para
print(f"Expected Output: {area_para}")