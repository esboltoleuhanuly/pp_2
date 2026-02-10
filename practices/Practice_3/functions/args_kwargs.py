#1. Example of arbitrary arguments, function accepts any number of arguments
def my_function(*kids):
  print("The youngest child is " + kids[2])
my_function("Emil", "Tobias", "Linus")

#2. Accessing individual arguments with args
def my_function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)
my_function("Emil", "Tobias", "Linus")

#3. Finding the maximum number
def my_function(*numbers):
  if len(numbers) == 0:
    return None
  max_num = numbers[0]
  for num in numbers:
    if num > max_num:
      max_num = num
  return max_num
print(my_function(3, 7, 2, 9, 1))

#4. Here is an example of using kwargs. 
# The **kwargs parameter allows a function to accept any number of keyword arguments.
# Inside the function, kwargs becomes a dictionary containing all the keyword arguments:
def my_function(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)
my_function(name = "Tobias", age = 30, city = "Bergen")

#5. Combining args and kwargs in one function
def my_function(title, *args, **kwargs):
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)
my_function("User Info", "Emil", "Tobias", age = 25, city = "Oslo")