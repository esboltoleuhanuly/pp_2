import psycopg2
from config import load_config

def register_sql(filename):
    config = load_config()
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    with open(filename, 'r') as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()
    print(f"Registered {filename} successfully.")

if __name__ == "__main__":
    register_sql('functions.sql')
    register_sql('procedures.sql')