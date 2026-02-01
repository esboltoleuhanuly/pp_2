#1
a = 5
b = 2
if a > b: print("a is greater than b")

#2
a = 2
b = 330
print("A") if a > b else print("B")

#3
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)

#4
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")

#5
x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)