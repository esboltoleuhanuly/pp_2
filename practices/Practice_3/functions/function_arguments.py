#1. Here is a simple function with one argument 'fname'
def my_function(fname):
  print(fname + " Refsnes")
my_function("Emil")
my_function("Tobias")
my_function("Linus")

#2. A parameter is the variable listed inside the parentheses in the function definition.
#An argument is the actual value that is sent to the function when it is called.
def my_function(name): # name is a parameter
  print("Hello", name)
my_function("Emil") # "Emil" is an argument

#3. The numbers of parameters and arguments must match
def my_function(fname, lname):
  print(fname + " " + lname)
my_function("Emil", "Refsnes")

#4. You can also set a default value for a parameter
def my_function(name = "friend"):
  print("Hello", name)
my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

#5. Example of keyword arguments
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function(animal = "dog", name = "Buddy")