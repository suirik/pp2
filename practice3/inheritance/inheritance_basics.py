# Parent class
class Animal:
    def breathe(self):
        print("This animal is breathing.")

# Child class (inherits from Animal)
class Dog(Animal):
    def bark(self):
        print("The dog says: Woof!")

# Creating a Dog object
my_dog = Dog()
my_dog.breathe()  # Inherited method
my_dog.bark()     # Child's own method