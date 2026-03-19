import shutil
import os

# Task 4: Copy and back up files
shutil.copy("sample.txt", "sample_backup.txt")
print("Backup created.")

# Task 5: Delete files safely
if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")
    print("Backup deleted safely.")