import psycopg2
from config import load_config

def execute_query(query, params=None, fetch=False):
    """A helper function to handle all DB interactions in one place"""
    with psycopg2.connect(**load_config()) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall() if fetch else None