from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# Task 1: Use map() and filter()
squared = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Task 2: Aggregate with reduce()
total_sum = reduce(lambda x, y: x + y, numbers)

print(f"Original: {numbers}")
print(f"Squared: {squared}")
print(f"Evens: {evens}")
print(f"Sum via reduce: {total_sum}")