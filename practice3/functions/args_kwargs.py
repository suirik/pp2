# Simple example of *args and **kwargs

# *args: Accepts any number of items
def make_pizza(*toppings):
    print(f"Making a pizza with: {toppings}")

make_pizza("cheese")
make_pizza("cheese", "pepperoni", "mushrooms")

# **kwargs: Accepts any number of named details
def user_info(**details):
    print(f"User details: {details}")

user_info(name="Samatkyzy", age=20)
user_info(city="Almaty", job="Student", level="Gold")