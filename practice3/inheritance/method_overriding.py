class Phone:
    def call(self):
        print("Making a standard voice call...")

class SmartPhone(Phone):
    # Overriding the parent's method
    def call(self):
        print("Making a high-definition video call...")

p1 = Phone()
p1.call() # Standard version

p2 = SmartPhone()
p2.call() # Overridden version