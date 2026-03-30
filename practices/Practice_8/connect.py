import psycopg2
from config import load_config

def connect():
    """ Connect to the PostgreSQL database server """
    config = load_config()
    conn = psycopg2.connect(**config)
    print('Connected to the PostgreSQL database.')
    return conn

if __name__ == '__main__':
    connect()