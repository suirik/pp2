import re

# Task 1: Check for 'a' followed by zero or more 'b's
# The '*' quantifier means the 'b' character is optional and can repeat indefinitely.
pattern1 = r"ab*"
print(f"Task 1 Result: {bool(re.fullmatch(pattern1, 'abbb'))}")

# Task 2: Check for 'a' followed by exactly 2 to 3 'b's
# The '{2,3}' range forces the match to fail if there are fewer than 2 or more than 3 'b's.
pattern2 = r"ab{2,3}"
print(f"Task 2 (2 'b's): {bool(re.fullmatch(pattern2, 'abb'))}")
print(f"Task 2 (3 'b's): {bool(re.fullmatch(pattern2, 'abbb'))}")

# Task 3: Find lowercase sequences connected by an underscore (snake_case)
# [a-z]+ matches one or more lowercase letters.
pattern3 = r"[a-z]+_[a-z]+"
print(f"Task 3 Matches: {re.findall(pattern3, 'hello_world test_case example')}")

# Task 4: Find a single Uppercase letter followed by lowercase letters
# This is useful for finding capitalized words in a sentence.
pattern4 = r"[A-Z][a-z]+"
print(f"Task 4 Matches: {re.findall(pattern4, 'Hello World Python Regex')}")

# Task 5: Match a string starting with 'a', containing anything, and ending with 'b'
# '.*' is a greedy match for any character sequence in the middle.
pattern5 = r"a.*b"
print(f"Task 5 Result: {bool(re.fullmatch(pattern5, 'axxxb'))}")

# Task 6: Replace spaces, commas, or dots with a colon
# The square brackets [ ,.] act as an 'OR' operator for these specific characters.
text = "Hello, world. Python regex"
result = re.sub(r"[ ,\.]", ":", text)
print(f"Task 6 Result: {result}")

# Task 8: Split a string at every capital letter
# (?=[A-Z]) is a 'positive lookahead' that finds the position before an uppercase letter without deleting it.
text_split = "HelloWorldPythonRegex"
print(f"Task 8 Split: {re.split(r'(?=[A-Z])', text_split)[1:]}")

# Task 10: Convert camelCase to snake_case
# We find capital letters, add an underscore before them, then lowercase the entire string.
def camel_to_snake(s):
    return re.sub(r"([A-Z])", r"_\1", s).lower().lstrip("_")

print(f"Task 10 Result: {camel_to_snake('helloWorldExample')}")
