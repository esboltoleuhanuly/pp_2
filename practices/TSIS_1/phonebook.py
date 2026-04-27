"""
TSIS 1 — Extended PhoneBook
Builds on Practice 7 & 8. New features:
  - Filter by group, search by email, sort, paginated console nav
  - Export / Import JSON  (with duplicate handling on import)
  - Extended CSV import (email, birthday, group, phone type)
  - DB procedures: add_phone, move_to_group, search_contacts
"""

import psycopg2
import json
import csv
import os
from datetime import date, datetime
from config import load_config


# ─────────────────────────────────────────────
# DB helpers
# ─────────────────────────────────────────────

def get_conn():
    return psycopg2.connect(**load_config())


# ─────────────────────────────────────────────
# Task 3.4.1  add_phone
# ─────────────────────────────────────────────

def add_phone(contact_name: str, phone: str, phone_type: str):
    """Call the add_phone stored procedure."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, phone_type))
        conn.commit()
    print(f"  ✔ Phone {phone} ({phone_type}) added to '{contact_name}'.")


# ─────────────────────────────────────────────
# Task 3.4.2  move_to_group
# ─────────────────────────────────────────────

def move_to_group(contact_name: str, group_name: str):
    """Call the move_to_group stored procedure."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
        conn.commit()
    print(f"  ✔ '{contact_name}' moved to group '{group_name}'.")


# ─────────────────────────────────────────────
# Task 3.4.3  search_contacts (extended)
# ─────────────────────────────────────────────

def search_contacts(query: str):
    """Search by name, email, or any phone number."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        return cur.fetchall()


# ─────────────────────────────────────────────
# Task 3.2.1  Filter by group
# ─────────────────────────────────────────────

def filter_by_group(group_name: str):
    sql = """
        SELECT c.user_name, c.email, c.birthday, g.name AS grp
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        WHERE g.name ILIKE %s
        ORDER BY c.user_name
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (group_name,))
        return cur.fetchall()


# ─────────────────────────────────────────────
# Task 3.2.2  Search by email (partial match)
# ─────────────────────────────────────────────

def search_by_email(email_fragment: str):
    sql = """
        SELECT user_name, email, birthday
        FROM contacts
        WHERE email ILIKE %s
        ORDER BY user_name
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (f'%{email_fragment}%',))
        return cur.fetchall()


# ─────────────────────────────────────────────
# Task 3.2.3  Sort results
# ─────────────────────────────────────────────

SORT_COLUMNS = {"name": "user_name", "birthday": "birthday", "date": "created_at"}

def get_all_sorted(sort_by: str = "name"):
    col = SORT_COLUMNS.get(sort_by, "user_name")
    sql = f"""
        SELECT c.user_name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.{col} NULLS LAST
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


# ─────────────────────────────────────────────
# Task 3.2.4  Paginated console navigation
# ─────────────────────────────────────────────

PAGE_SIZE = 5

def paginated_console():
    """Interactive page navigator using the existing DB function."""
    offset = 0
    while True:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_users_paginated(%s, %s)",
                (PAGE_SIZE, offset)
            )
            rows = cur.fetchall()

        if not rows and offset == 0:
            print("  (no contacts found)")
            break

        page_num = offset // PAGE_SIZE + 1
        print(f"\n── Page {page_num} ──────────────────────")
        if rows:
            for r in rows:
                print(f"  {r[0]:<20} {r[1]}")
        else:
            print("  (end of list)")

        cmd = input("\n[n]ext  [p]rev  [q]uit › ").strip().lower()
        if cmd == 'n':
            if len(rows) == PAGE_SIZE:
                offset += PAGE_SIZE
            else:
                print("  Already on the last page.")
        elif cmd == 'p':
            offset = max(0, offset - PAGE_SIZE)
        elif cmd == 'q':
            break


# ─────────────────────────────────────────────
# Task 3.3.1  Export to JSON
# ─────────────────────────────────────────────

def export_to_json(filepath: str = "contacts.json"):
    sql = """
        SELECT c.user_name, c.email,
               c.birthday::TEXT,
               g.name AS grp,
               COALESCE(
                   json_agg(json_build_object('phone', p.phone, 'type', p.type))
                   FILTER (WHERE p.phone IS NOT NULL),
                   '[]'
               ) AS phones
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        GROUP BY c.user_name, c.email, c.birthday, g.name
        ORDER BY c.user_name
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    contacts = []
    for row in rows:
        contacts.append({
            "name":     row[0],
            "email":    row[1],
            "birthday": row[2],
            "group":    row[3],
            "phones":   row[4],
        })

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

    print(f"  ✔ Exported {len(contacts)} contacts → {filepath}")


# ─────────────────────────────────────────────
# Task 3.3.2  Import from JSON (with duplicate handling)
# ─────────────────────────────────────────────

def import_from_json(filepath: str = "contacts.json"):
    if not os.path.exists(filepath):
        print(f"  File '{filepath}' not found.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    with get_conn() as conn, conn.cursor() as cur:
        for c in contacts:
            name = c.get("name", "").strip()
            if not name:
                continue

            # Check duplicate
            cur.execute("SELECT id FROM contacts WHERE user_name = %s", (name,))
            existing = cur.fetchone()

            if existing:
                choice = input(
                    f"  '{name}' already exists. [s]kip / [o]verwrite? › "
                ).strip().lower()
                if choice != 'o':
                    print(f"    Skipped '{name}'.")
                    continue
                # Overwrite: update fields, delete old phones
                cur.execute("""
                    UPDATE contacts
                    SET email = %s, birthday = %s, group_id = (
                        SELECT id FROM groups WHERE name = %s
                    )
                    WHERE user_name = %s
                """, (c.get("email"), c.get("birthday"), c.get("group"), name))
                cur.execute(
                    "DELETE FROM phones WHERE contact_id = %s", (existing[0],)
                )
                contact_id = existing[0]
            else:
                cur.execute("""
                    INSERT INTO contacts (user_name, email, birthday, group_id)
                    VALUES (%s, %s, %s, (SELECT id FROM groups WHERE name = %s))
                    RETURNING id
                """, (name, c.get("email"), c.get("birthday"), c.get("group")))
                contact_id = cur.fetchone()[0]

            # Insert phones
            for ph in c.get("phones", []):
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                    (contact_id, ph.get("phone"), ph.get("type"))
                )
            print(f"    ✔ Imported '{name}'.")

        conn.commit()
    print("  Import complete.")


# ─────────────────────────────────────────────
# Task 3.3.3  Extended CSV import
# Fields: name, email, birthday (YYYY-MM-DD), group, phone, phone_type
# ─────────────────────────────────────────────

def import_from_csv(filepath: str):
    if not os.path.exists(filepath):
        print(f"  File '{filepath}' not found.")
        return

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with get_conn() as conn, conn.cursor() as cur:
        for row in rows:
            name      = row.get("name", "").strip()
            email     = row.get("email", "").strip() or None
            birthday  = row.get("birthday", "").strip() or None
            group     = row.get("group", "").strip() or None
            phone     = row.get("phone", "").strip() or None
            ph_type   = row.get("phone_type", "mobile").strip()

            if not name:
                continue

            # Upsert contact
            cur.execute("""
                INSERT INTO contacts (user_name, email, birthday, group_id)
                VALUES (%s, %s, %s, (SELECT id FROM groups WHERE name = %s))
                ON CONFLICT (user_name) DO UPDATE
                SET email    = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id
            """, (name, email, birthday, group))
            contact_id = cur.fetchone()[0]

            if phone:
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                    (contact_id, phone, ph_type)
                )

        conn.commit()
    print(f"  ✔ CSV import complete ({len(rows)} rows processed).")


# ─────────────────────────────────────────────
# Console Menu
# ─────────────────────────────────────────────

def print_rows(rows, headers):
    if not rows:
        print("  (no results)")
        return
    print("  " + " | ".join(f"{h:<20}" for h in headers))
    print("  " + "-" * (23 * len(headers)))
    for r in rows:
        print("  " + " | ".join(f"{str(v or ''):<20}" for v in r))


MENU = """
╔══════════════════════════════════════╗
║        PhoneBook  TSIS 1            ║
╠══════════════════════════════════════╣
║  1. Search (name / email / phone)   ║
║  2. Filter by group                 ║
║  3. Search by email                 ║
║  4. Sort all contacts               ║
║  5. Browse pages (next/prev)        ║
║  6. Add phone to contact            ║
║  7. Move contact to group           ║
║  8. Export to JSON                  ║
║  9. Import from JSON                ║
║  10. Import from CSV                ║
║  0. Exit                            ║
╚══════════════════════════════════════╝
"""

def main():
    while True:
        print(MENU)
        choice = input("Choose › ").strip()

        if choice == '1':
            q = input("  Search query: ").strip()
            rows = search_contacts(q)
            print_rows(rows, ["Name", "Email", "Phone", "Type", "Group"])

        elif choice == '2':
            g = input("  Group name (Family/Work/Friend/Other): ").strip()
            rows = filter_by_group(g)
            print_rows(rows, ["Name", "Email", "Birthday", "Group"])

        elif choice == '3':
            e = input("  Email fragment: ").strip()
            rows = search_by_email(e)
            print_rows(rows, ["Name", "Email", "Birthday"])

        elif choice == '4':
            s = input("  Sort by [name/birthday/date]: ").strip()
            rows = get_all_sorted(s)
            print_rows(rows, ["Name", "Email", "Birthday", "Group"])

        elif choice == '5':
            paginated_console()

        elif choice == '6':
            name = input("  Contact name: ").strip()
            phone = input("  Phone number: ").strip()
            ptype = input("  Type (home/work/mobile): ").strip()
            try:
                add_phone(name, phone, ptype)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == '7':
            name = input("  Contact name: ").strip()
            group = input("  Group name: ").strip()
            try:
                move_to_group(name, group)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == '8':
            path = input("  Output file [contacts.json]: ").strip() or "contacts.json"
            export_to_json(path)

        elif choice == '9':
            path = input("  Input file [contacts.json]: ").strip() or "contacts.json"
            import_from_json(path)

        elif choice == '10':
            path = input("  CSV file path: ").strip()
            import_from_csv(path)

        elif choice == '0':
            print("  Goodbye!")
            break

        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()