import re
import json

# Load the raw data from the text file
# Using encoding='utf-8' is essential to read the Cyrillic (Kazakh/Russian) characters correctly.
with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Extract Monetary Values
# This pattern matches digits, an optional space (thousand separator), and a comma decimal.
# It captures values like '308,00' and '1 200,00'.
prices = re.findall(r"\d+\s?\d*,\d{2}", text)

# 2. Extract Product Names
# We look for a line starting with a number and dot (e.g., '1.') and grab the text on the next line.
# '.+' captures the entire product name string.
products = re.findall(r"\d+\.\n(.+)", text)

# 3. Extract the Total Sum
# We search for the keyword 'ИТОГО:' (TOTAL) and capture the numerical value immediately below it.
total = re.search(r"ИТОГО:\n([\d\s,]+)", text)
total_amount = total.group(1).strip() if total else "Not found"

# 4. Extract Date and Time
# Finds the word 'Время:' and extracts the date (DD.MM.YYYY) and time (HH:MM:SS) that follow.
datetime = re.search(r"Время:\s([\d\.]+\s[\d:]+)", text)
datetime_value = datetime.group(1) if datetime else "Not found"

# 5. Extract Payment Method
# Searches specifically for the phrase 'Банковская карта' (Bank card).
payment = re.search(r"(Банковская карта)", text)
payment_method = payment.group(1) if payment else "Cash or Other"

# Create a clean dictionary to store our results
data = {
    "items_purchased": products,
    "all_detected_prices": prices,
    "total_bill": total_amount,
    "transaction_time": datetime_value,
    "payment_type": payment_method
}

# Output the result as a pretty-printed JSON string
# ensure_ascii=False allows the Cyrillic text to remain readable in the output.
print(json.dumps(data, ensure_ascii=False, indent=4))
