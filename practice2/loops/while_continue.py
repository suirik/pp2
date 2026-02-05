# while loop with continue

i = 0
while i < 6:
    i += 1
    if i == 3:
        continue
    print(i)

# Skip odd numbers
j = 0
while j < 10:
    j += 1
    if j % 2 != 0:
        continue
    print(j)

# Skip negative inputs
while True:
    x = int(input("Number: "))
    if x == 0:
        break
    if x < 0:
        continue
    print(x)
  
