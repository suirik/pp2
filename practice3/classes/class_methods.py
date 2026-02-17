class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    # A method to describe the car
    def start_engine(self):
        print(f"The {self.color} {self.brand} engine is now running!")

# Using the method
my_car = Car("Toyota", "Red")
my_car.start_engine()