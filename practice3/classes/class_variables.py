class Robot:
    # Class variable (shared by all robots)
    species = "Android"

    def __init__(self, model_name):
        # Instance variable (unique to each robot)
        self.model_name = model_name

# Both robots share the same species but have different names
r1 = Robot("R2-D2")
r2 = Robot("C-3PO")

print(f"{r1.model_name} is an {r1.species}")
print(f"{r2.model_name} is an {r2.species}")