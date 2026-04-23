# for loop with break

for i in range(10):
    if i == 6:
        break
    print(i)

# Stop when negative number appears
nums = [3, 5, 7, -1, 9]
for n in nums:
    if n < 0:
        break
    print(n)

# Break after finding number
for i in range(1, 20):
    if i == 10:
        print("Found 10")
        break
 
