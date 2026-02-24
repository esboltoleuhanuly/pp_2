import math

#1: Degree to radian
degree = float(input("Input degree: "))
radian = math.radians(degree)
print(f"Output radian: {radian:.6f}")

#2: Area of a trapezoid
h = float(input("Height: "))
a = float(input("Base, first value: "))
b = float(input("Base, second value: "))
area_trap = ((a + b) / 2) * h
print(f"Expected Output: {area_trap}")

#3: Area of regular polygon
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
area_poly = (n * s**2) / (4 * math.tan(math.pi / n))
print(f"The area of the polygon is: {area_poly:.0f}")

#4: Area of a parallelogram
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
print(f"Expected Output: {float(base * height)}")