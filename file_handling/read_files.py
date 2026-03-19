# Task 2: Read and print file contents
# Task 3: Append new lines and verify content

filename = "sample.txt"

# Appending first
with open(filename, "a") as file:
    file.write("This line was appended later.\n")

# Reading and verifying
with open(filename, "r") as file:
    print("--- File Content ---")
    print(file.read())