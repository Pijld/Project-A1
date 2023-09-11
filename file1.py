class group:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def sayhello(self):
        print(f"hello, my name is {self.name} and i am {self.age} years old.")

s1 = group("Sam", 20)
s2 = group("Pam", 18)

s1.sayhello()