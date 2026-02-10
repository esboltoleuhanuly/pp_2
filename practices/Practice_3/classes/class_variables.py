# Properties are variables that belong to a class. They store data for each object created from the class.

#1. Create a class with properties:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("Emil", 36)
print(p1.name)
print(p1.age)

#2. You can access object properties using dot notation:
class Car:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model
car1 = Car("Toyota", "Corolla")
print(car1.brand)
print(car1.model)

#3. You can modify the value of properties on objects:
p1 = Person("Tobias", 25)
print(p1.age)
p1.age = 26
print(p1.age)

#4. You can delete properties from objects using the del keyword:
p1 = Person("Linus", 30)
del p1.age
print(p1.name) # This works
# print(p1.age) # This would cause an error

#5. Properties defined inside __init__() belong to each object (instance properties).
# Properties defined outside methods belong to the class itself (class properties) and are shared by all objects:
class Person:
  species = "Human" # Class property
  def __init__(self, name):
    self.name = name # Instance property
p1 = Person("Emil")
p2 = Person("Tobias")
print(p1.name)
print(p2.name)
print(p1.species)
print(p2.species)