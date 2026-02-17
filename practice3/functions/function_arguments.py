# Function with a parameter (name)
def greet_user(name):
    print(f"Hello, {name}! Glad to see you here.")

# Calling the function with an argument
greet_user("suiriksamatkyzy")

# Function with a default parameter
def power_info(device="Laptop"):
    print(f"The {device} is currently powered on.")

power_info() # Uses default
power_info("Smartphone") # Overrides default