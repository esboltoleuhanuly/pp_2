#1. Generates the squares of numbers up to some number n.
def generate_square_numbers(n):
    for i in range(n + 1):
        yield i ** 2

#2. Generates the even numbers up to some number n.
def generate_even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

#3. Generates numbers divisible by 3 and 4 up to some number n.
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

#4. Generates the squares of numbers in a given range.
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

#5. Generates a countdown from a given number n.
def countdown(n):
    while n >= 0:
        yield n
        n -= 1