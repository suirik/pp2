# Task 1: Create a text file and write sample data
filename = "sample.txt"
content = "Hello! This is sample data.\nPython file handling is useful.\n"

with open(filename, "w") as file:
    file.write(content)
print(f"{filename} created successfully.")
