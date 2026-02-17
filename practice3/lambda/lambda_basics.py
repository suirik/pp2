# Regular function
def add(a, b):
    return a + b

# Equivalent Lambda function
# Syntax: lambda arguments: expression
add_lambda = lambda a, b: a + b

print(f"Regular function result: {add(5, 3)}")
print(f"Lambda function result: {add_lambda(5, 3)}")