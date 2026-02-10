#1. A lambda function can take any number of arguments, but can only have one expression.
x = lambda a : a + 10
print(x(5))

#2. A lambda function can take any number of arguments.
x = lambda a, b : a * b
print(x(5, 6))

#3. Use that function definition to make a function that always doubles the number you send in:
def myfunc(n):
  return lambda a : a * n
mydoubler = myfunc(2)
print(mydoubler(11))

#4. Or, use the same function definition to make a function that always triples the number you send in:
def myfunc(n):
  return lambda a : a * n
mytripler = myfunc(3)
print(mytripler(11))

#5. Or, use the same function definition to make both functions, in the same program:
def myfunc(n):
  return lambda a : a * n
mydoubler = myfunc(2)
mytripler = myfunc(3)
print(mydoubler(11))
print(mytripler(11))