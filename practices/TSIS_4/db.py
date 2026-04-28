# db.py — PostgreSQL persistence via psycopg2
#
# Edit DB_CONFIG to match your local PostgreSQL setup.
# Run init_db() once at startup; it is safe to call repeatedly.

import psycopg2

DB_CONFIG = {
    'dbname':   'snake_game',
    'user':     'postgres',
    'password': 'Esbol_123',
    'host':     'localhost',
    'port':     5432,
}


def _connect():
    return psycopg2.connect(**DB_CONFIG)


# ── schema ────────────────────────────────────────────────────────────────────

def init_db() -> bool:
    """Create tables if they don't exist. Returns True on success."""
    try:
        conn = _connect()
        cur  = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id       SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id            SERIAL PRIMARY KEY,
                player_id     INTEGER REFERENCES players(id),
                score         INTEGER   NOT NULL,
                level_reached INTEGER   NOT NULL,
                played_at     TIMESTAMP DEFAULT NOW()
            )
        """)
        conn.commit()
        cur.close(); conn.close()
        return True
    except Exception as e:
        print(f"[DB] init_db failed: {e}")
        return False


# ── players ───────────────────────────────────────────────────────────────────

def get_or_create_player(username: str):
    """Return player_id for username, creating the row if new."""
    try:
        conn = _connect()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING",
            (username,)
        )
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        row = cur.fetchone()
        conn.commit()
        cur.close(); conn.close()
        return row[0] if row else None
    except Exception as e:
        print(f"[DB] get_or_create_player failed: {e}")
        return None


# ── sessions ──────────────────────────────────────────────────────────────────

def save_session(player_id: int, score: int, level: int) -> bool:
    try:
        conn = _connect()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
            (player_id, score, level)
        )
        conn.commit()
        cur.close(); conn.close()
        return True
    except Exception as e:
        print(f"[DB] save_session failed: {e}")
        return False


def get_personal_best(player_id: int) -> int:
    try:
        conn = _connect()
        cur  = conn.cursor()
        cur.execute(
            "SELECT COALESCE(MAX(score), 0) FROM game_sessions WHERE player_id = %s",
            (player_id,)
        )
        pb = cur.fetchone()[0]
        cur.close(); conn.close()
        return pb
    except Exception as e:
        print(f"[DB] get_personal_best failed: {e}")
        return 0


def get_leaderboard() -> list:
    """Return top-10 rows as [(username, score, level, date_str), ...]."""
    try:
        conn = _connect()
        cur  = conn.cursor()
        cur.execute("""
            SELECT p.username,
                   gs.score,
                   gs.level_reached,
                   TO_CHAR(gs.played_at, 'YYYY-MM-DD') AS date
            FROM   game_sessions gs
            JOIN   players p ON gs.player_id = p.id
            ORDER  BY gs.score DESC
            LIMIT  10
        """)
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
    except Exception as e:
        print(f"[DB] get_leaderboard failed: {e}")
        return []