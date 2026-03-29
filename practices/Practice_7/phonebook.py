import csv
from connect import execute_query # Import the helper you just moved

def create_table():
    execute_query("CREATE TABLE IF NOT EXISTS phonebook (user_name VARCHAR(100), phone_number VARCHAR(20))")

def insert_contact(name=None, phone=None):
    name = name or input("Name: ")
    phone = phone or input("Phone: ")
    execute_query("INSERT INTO phonebook VALUES (%s, %s)", (name, phone))

def upload_csv(file='contacts.csv'):
    with open(file) as f:
        for r in csv.reader(f): 
            execute_query("INSERT INTO phonebook VALUES (%s, %s)", (r[0], r[1]))
    print("CSV Data Uploaded.")

def update_contact():
    print("1. Update Name\n2. Update Phone")
    choice = input("Choice: ")
    if choice == '1':
        execute_query("UPDATE phonebook SET user_name=%s WHERE phone_number=%s", (input("New Name: "), input("Current Phone: ")))
    else:
        execute_query("UPDATE phonebook SET phone_number=%s WHERE user_name=%s", (input("New Phone: "), input("Current Name: ")))

def search_contact():
    # Requirement 5: Querying with filters (Name or Phone Prefix)
    val = input("Enter Name or Phone Prefix: ") + '%'
    res = execute_query("SELECT * FROM phonebook WHERE user_name LIKE %s OR phone_number LIKE %s", (val, val), fetch=True)
    for r in res: print(f"{r[0]}: {r[1]}")
    if not res: print("No results.")

def delete_contact():
    # Requirement 6: Delete by username OR phone number
    val = input("Enter Name or Phone to delete: ")
    execute_query("DELETE FROM phonebook WHERE user_name=%s OR phone_number=%s", (val, val))
    print("Record removed.")

if __name__ == "__main__":
    create_table()
    menu = {"1": insert_contact, "2": upload_csv, "3": update_contact, "4": search_contact, "5": delete_contact}
    while True:
        cmd = input("\n1:Add, 2:CSV, 3:Update, 4:Search, 5:Delete, 6:Exit\nChoice: ")
        if cmd == "6": break
        menu.get(cmd, lambda: print("Invalid"))()