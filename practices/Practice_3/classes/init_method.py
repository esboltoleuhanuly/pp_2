# The __init__() method is used to assign values to object properties, 
# or to perform operations that are necessary when the object is being created.

#1. Create a class named Person, use the __init__() method to assign values for name and age:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("Emil", 36)
print(p1.name)
print(p1.age)

#2. Create a class without __init__():
class Person:
  pass
p1 = Person()
p1.name = "Tobias"
p1.age = 25
print(p1.name)
print(p1.age)

#3. With __init__(), you can set initial values when creating the object:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("Linus", 28)
print(p1.name)
print(p1.age)

#4. You can also set default values for parameters in the __init__() method:
class Person:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age
p1 = Person("Emil")
p2 = Person("Tobias", 25)
print(p1.name, p1.age)
print(p2.name, p2.age)

#5. The __init__() method can have as many parameters as you need:
class Person:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country
p1 = Person("Linus", 30, "Oslo", "Norway")
print(p1.name)
print(p1.age)
print(p1.city)
print(p1.country)