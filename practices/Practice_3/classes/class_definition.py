# A Class is like an object constructor, or a "blueprint" for creating objects.
#1. Create a class named MyClass, with a property named x:
class MyClass:
  x = 5

#2. Create an object named p1, and print the value of x:
p1 = MyClass()
print(p1.x)

#3. You can delete objects by using the del keyword:
del p1

#4. You can create multiple objects from the same class:
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()
print(p1.x)
print(p2.x)
print(p3.x)

#5. Class definitions cannot be empty, but if you for some reason have a class definition with no content, 
# put in the pass statement to avoid getting an error.
class Person:
  pass