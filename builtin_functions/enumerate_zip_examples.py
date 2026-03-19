# Task 3: enumerate() and zip()
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

print("--- Zip and Enumerate ---")
for index, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{index}. {name} scored {score}")

# Task 4: Type checking and conversions
val = "100"
if isinstance(val, str):
    num = int(val)
    print(f"Converted {type(val)} to {type(num)}")