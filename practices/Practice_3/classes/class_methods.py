# Methods are functions that belong to a class. They define the behavior of objects created from the class.

#1. Create a method in a class:
class Person:
  def __init__(self, name):
    self.name = name
  def greet(self):
    print("Hello, my name is " + self.name)
p1 = Person("Emil")
p1.greet()

#2. Methods can accept parameters just like regular functions:
class Calculator:
  def add(self, a, b):
    return a + b
  def multiply(self, a, b):
    return a * b
calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 7))

#3. Methods can access and modify object properties using self:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def get_info(self):
    return f"{self.name} is {self.age} years old"
p1 = Person("Tobias", 28)
print(p1.get_info())

#4. Methods can modify the properties of an object:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def celebrate_birthday(self):
    self.age += 1
    print(f"Happy birthday! You are now {self.age}")
p1 = Person("Linus", 25)
p1.celebrate_birthday()
p1.celebrate_birthday()

#5. The __str__() method is a special method that controls what is returned when the object is printed:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def __str__(self):
    return f"{self.name} ({self.age})"
p1 = Person("Tobias", 36)
print(p1)