import psycopg2
import re
from config import load_config

def insert_many_with_validation(user_list):
    """Task 3: Loop, Validate, and Return Errors"""
    config = load_config()
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    
    invalid_data = []
    for name, phone in user_list:
        # Check if phone is 10-12 digits using Regex
        if re.fullmatch(r'\d{10,12}', phone):
            cur.execute("CALL upsert_phonebook(%s, %s)", (name, phone))
        else:
            invalid_data.append((name, phone))
            
    conn.commit()
    cur.close()
    conn.close()
    return invalid_data

def show_page(limit, offset):
    """Task 4: Pagination"""
    config = load_config()
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_users_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

if __name__ == "__main__":
    # 1. Add users (Task 3)
    users_to_add = [("Asel", "7071112233"), ("Akniet", "7475556677"), ("ErrorUser", "123")]
    errors = insert_many_with_validation(users_to_add)
    print(f"Invalid entries skipped: {errors}")

    # 2. Show Results (Task 4)
    print("\n--- PhoneBook Page 1 ---")
    for user in show_page(5, 0):
        print(f"User: {user[0]} | Phone: {user[1]}")