#1
print(bool("Hello"))
print(bool(15))

#2
x = "Hello"
y = 15
print(bool(x))
print(bool(y))

#3
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

#4
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#5
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))