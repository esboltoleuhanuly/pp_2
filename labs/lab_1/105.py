a = input("")
b = input("")
a = int(a)
b = int(b)
c = int(a/b)
d = float(a/b)
if a == -b and b == -a:
    c += 1
if a < 0 and b < 0:
    c += 0
if a < 0 and b > 0:
    c -= 1
if b < 0 and a > 0:
    c -= 1
print(c)
print(d)