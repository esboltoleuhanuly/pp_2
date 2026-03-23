import psycopg2, csv
from config import load_config

def execute_query(query, params=None, fetch=False):
    """A helper function to handle all DB interactions in one place"""
    with psycopg2.connect(**load_config()) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall() if fetch else None

def create_table():
    execute_query("CREATE TABLE IF NOT EXISTS phonebook (user_name VARCHAR(100), phone_number VARCHAR(20))")

def insert_contact(name=None, phone=None):
    name = name or input("Name: ")
    phone = phone or input("Phone: ")
    execute_query("INSERT INTO phonebook VALUES (%s, %s)", (name, phone))

def upload_csv(file):
    with open(file) as f:
        for r in csv.reader(f): insert_contact(r[0], r[1])

def update_contact():
    execute_query("UPDATE phonebook SET phone_number=%s WHERE user_name=%s", (input("New Phone: "), input("Name: ")))

def search_contact():
    res = execute_query("SELECT * FROM phonebook WHERE user_name=%s", (input("Name: "),), fetch=True)
    print(res[0] if res else "Not found")

def delete_contact():
    execute_query("DELETE FROM phonebook WHERE user_name=%s", (input("Name: "),))

def show_all():
    for r in execute_query("SELECT * FROM phonebook", fetch=True): print(f"{r[0]}: {r[1]}")

if __name__ == "__main__":
    create_table()
    menu = {"1": insert_contact, "2": lambda: upload_csv('contacts.csv'), "3": update_contact, 
            "4": search_contact, "5": delete_contact, "6": show_all}
    while True:
        cmd = input("\n1:Add, 2:CSV, 3:Upd, 4:Sch, 5:Del, 6:Show, 7:Exit\nChoice: ")
        if cmd == "7": break
        menu.get(cmd, lambda: print("Invalid"))()