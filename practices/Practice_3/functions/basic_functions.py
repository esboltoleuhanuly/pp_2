#1. Firstly, we create a basic function with 'def' and call it
def my_function():
  print("Hello from a function")
my_function()

#2. We can call it many times
my_function()
my_function()
my_function()

#3. A function name can only contain letters, numbers, and underscores. It`s also case sensitive
#calculate_sum()
#_private_function()
#myFunction2()

#4. Our code without function and it`s hard to read
temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)
temp2 = 95
celsius2 = (temp2 - 32) * 5 / 9
print(celsius2)
temp3 = 50
celsius3 = (temp3 - 32) * 5 / 9
print(celsius3)

#5. We can improve our code readability by using functions
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9
print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))