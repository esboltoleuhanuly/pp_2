#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

#2
for x in "banana":
  print(x)

#3
for x in range(6):
  print(x)

#4
for x in range(2, 6):
  print(x)

#5
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")