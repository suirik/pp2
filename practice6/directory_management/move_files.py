import shutil
import os

# Move sample.txt into the nested directory
os.makedirs("data", exist_ok=True)
if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "data/sample.txt")
    print("File moved to data/ folder.")
