import psycopg2
from config import load_config

def get_connection():
    return psycopg2.connect(**load_config())

if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print("Connected:", cur.fetchone()[0])
    conn.close()