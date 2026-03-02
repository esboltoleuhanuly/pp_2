import re
import json

with open('raw.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 1. Extract all prices
all_prices = re.findall(r'Стоимость\n([\d\s]+,\d{2})', content)

# 2. Find all product names
product_names = re.findall(r'\d+\.\n(.*?)\n\d,', content, re.DOTALL)

# 3. Calculate total amount 
total_match = re.search(r'ИТОГО:\n([\d\s]+,\d{2})', content)
total_amount = total_match.group(1) if total_match else "0,00"

# 4. Extract date and time information
date_time = re.search(r'\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}', content).group()

# 5. Find payment method
payment_method = re.search(r'(.*?):\n[\d\s]+,\d{2}\nИТОГО:', content).group(1)

# 6. Create a structured output 
output = {
    "items": [name.strip() for name in product_names],
    "item_prices": all_prices,
    "total": total_amount,
    "date_time": date_time,
    "payment_method": payment_method.strip()
}

print(json.dumps(output, ensure_ascii=False, indent=4))

#Regex tasks:

# 1. Matches 'a' followed by zero or more 'b's
def task1(text):
    return re.findall(r"ab*", text)

# 2. Matches 'a' followed by two to three 'b'
def task2(text):
    return re.findall(r"ab{2,3}", text)

# 3. Find sequences of lowercase letters joined with a underscore
def task3(text):
    return re.findall(r"[a-z]+_[a-z]+", text)

# 4. Find sequences of one upper case letter followed by lower case letters
def task4(text):
    return re.findall(r"[A-Z][a-z]+", text)

# 5. Matches a string that has an 'a' followed by anything, ending in 'b'
def task5(text):
    return re.findall(r"a.*b$", text)

# 6. Replace all occurrences of space, comma, or dot with a colon
def task6(text):
    return re.sub(r"[ ,.]", ":", text)

# 7. Convert snake case string to camel case string
def task7(text):
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), text)

# 8. Split a string at uppercase letters
def task8(text):
    res = re.split(r"(?=[A-Z])", text)
    return [s for s in res if s]

# 9. Insert spaces between words starting with capital letters
def task9(text):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", text)

# 10. Convert camel case string to snake case
def task10(text):
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text).lower()


print("1:", task1("ab, a, abbb, c"))
print("2:", task2("abb, abbb, abbbb, a, ab"))
print("3:", task3("hello_world, Python_code, test_case"))
print("4:", task4("Apple, orange, Banana, cherry"))
print("5:", task5("axxxb")) 
print("6:", task6("Hello world, how.are you"))
print("7:", task7("this_is_snake_case"))
print("8:", task8("SplitThisString"))
print("9:", task9("InsertSpacesBetweenWords"))
print("10:", task10("CamelCaseString"))