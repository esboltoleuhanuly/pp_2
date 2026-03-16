# Task 3: Use enumerate() and zip()
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

print("Iterating with enumerate:")
for index, name in enumerate(names):
    print(f"{index}: {name}")

print("\nIterating with zip:")
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

# Task 4: Demonstrate type checking and conversions
val = "100"
if isinstance(val, str):
    num = int(val)
    print(f"\nConverted '{val}' (type: {type(val)}) to {num} (type: {type(num)})")