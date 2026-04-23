# for loop with continue

for i in range(1, 8):
    if i == 4:
        continue
    print(i)

# Skip multiples of 3
for i in range(1, 11):
    if i % 3 == 0:
        continue
    print(i)

# Skip negative numbers
nums = [2, -1, 4, -3, 6]
for n in nums:
    if n < 0:
        continue
    print(n)
 
