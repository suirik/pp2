import os

# Task 1: Create nested directories
path = "parent/child/grandchild"
os.makedirs(path, exist_ok=True)

# Task 2: List files and folders
print("Current directory contents:", os.listdir("."))

# Task 3: Find files by extension (e.g., .py)
files = [f for f in os.listdir(".") if f.endswith(".py")]
print("Python files in directory:", files)