#1. Functions can also return values and then we can assign them to variables
def get_greeting():
  return "Hello from a function"
message = get_greeting()
print(message)

#2. In this case, we are directly printing the return value of the function without assigning
def get_greeting():
  return "Hello from a function"
print(get_greeting())

# If a function doesn't have a return statement, it returns None by default.

#3. Another example with integers
def my_function(x, y):
  return x + y
result = my_function(5, 3)
print(result)

#4. Returns a list
def my_function():
  return ["apple", "banana", "cherry"]
fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])

#5. And a tuple
def my_function():
  return (10, 20)
x, y = my_function()
print("x:", x)
print("y:", y)