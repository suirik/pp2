# 1. Write a Python program to subtract five days from current date.

from datetime import datetime, timedelta

# Get current date
current_date = datetime.now()
# Subtract 5 days
five_days_ago = current_date - timedelta(days=5)

print("Current Date:", current_date)
print("Five days ago:", five_days_ago)



# 2. Write a Python program to print yesterday, today, tomorrow.
# his involves adding and subtracting a single day from the current time.

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday.strftime('%Y-%m-%d'))
print("Today:", today.strftime('%Y-%m-%d'))
print("Tomorrow:", tomorrow.strftime('%Y-%m-%d'))



# 3. Write a Python program to drop microseconds from datetime.
# The replace() method allows you to modify specific parts of a datetime object.

now = datetime.now()
# Replace microseconds with 0
no_microseconds = now.replace(microsecond=0)

print("With microseconds:", now)
print("Without microseconds:", no_microseconds)



# 4. Write a Python program to calculate two date difference in seconds.
# When you subtract two dates, Python returns a timedelta object, which has a built-in method called total_seconds().

date1 = datetime(2026, 2, 26, 12, 0, 0)
date2 = datetime(2026, 2, 25, 12, 0, 0)

difference = date1 - date2
seconds_diff = difference.total_seconds()

print(f"Difference in seconds: {seconds_diff}")