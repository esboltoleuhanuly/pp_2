#1
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")

#2
a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

#3
number = 7
if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")  

#4
temperature = 22
if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")

#5    
username = "Emil"
if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")