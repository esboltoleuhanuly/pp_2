# Task 3: Append new lines and verify content
with open("sample.txt", "a") as f:
  f.write(" Now the file has more content!")

with open("sample.txt") as f:
  print(f.read())