# if – elif – else examples

score = int(input("Score: "))
if score >= 90:
    print("Excellent")
elif score >= 75:
    print("Good")
elif score >= 60:
    print("Satisfactory")
else:
    print("Fail")

day = int(input("Day (1–7): "))
if day == 1:
    print("Monday")
elif day == 2:
    print("Tuesday")
elif day == 3: 
    print("Wednesday")
elif day == 4:
    print("Thursday")
elif day == 5:
    print("Friday")
else:
    print("Weekend")
