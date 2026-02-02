ly = int(input())
if (ly % 4 == 0 and ly % 100 != 0) or (ly % 400 == 0):
    ly = True
else:
    ly = False

if ly == True:
    print("YES")
else:
    print("NO")
