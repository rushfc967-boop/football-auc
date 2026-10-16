import sqlite3
from config import DB_PATH, BUDGET_PER_TEAM, SQUAD_SIZE

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, owner_username TEXT, budget REAL DEFAULT 100, spent REAL DEFAULT 0, slots_left INTEGER DEFAULT 15)")
    c.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, position TEXT, base_price REAL, status TEXT DEFAULT 'pending', set_id INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS sold (id INTEGER PRIMARY KEY AUTOINCREMENT, player_id INTEGER, team_id INTEGER, price REAL, timestamp TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS auction_state (id INTEGER PRIMARY KEY CHECK (id = 1), status TEXT DEFAULT 'idle', host_id INTEGER, host_username TEXT, current_player_id INTEGER, current_set INTEGER DEFAULT 1, highest_bid REAL DEFAULT 0, highest_team_id INTEGER, last_bid_time REAL DEFAULT 0, last_reminder INTEGER, live_message_id INTEGER, chat_id INTEGER)")
    c.execute("INSERT OR IGNORE INTO auction_state (id) VALUES (1)")
    conn.commit()
    conn.close()

def get_state():
    conn = get_conn()
    row = conn.execute("SELECT * FROM auction_state WHERE id=1").fetchone()
    conn.close()
    return dict(row)

def update_state(**kwargs):
    if not kwargs: return
    fields = ", ".join([f"{k}=?" for k in kwargs])
    values = list(kwargs.values())
    conn = get_conn()
    conn.execute(f"UPDATE auction_state SET {fields} WHERE id=1", values)
    conn.commit()
    conn.close()

def add_team(name, owner_username):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO teams (name, owner_username, budget, spent, slots_left) VALUES (?,?,?,0,?)", (name, owner_username, BUDGET_PER_TEAM, SQUAD_SIZE))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_teams():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM teams ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_team(team_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM teams WHERE id=?", (team_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_team(team_id, **kwargs):
    if not kwargs: return
    fields = ", ".join([f"{k}=?" for k in kwargs])
    values = list(kwargs.values()) + [team_id]
    conn = get_conn()
    conn.execute(f"UPDATE teams SET {fields} WHERE id=?", values)
    conn.commit()
    conn.close()

def add_player(name, position, base_price):
    conn = get_conn()
    conn.execute("INSERT INTO players (name, position, base_price, status) VALUES (?,?,?, 'pending')", (name, position, base_price))
    conn.commit()
    conn.close()

def get_player(player_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM players WHERE id=?", (player_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_player(player_id, **kwargs):
    if not kwargs: return
    fields = ", ".join([f"{k}=?" for k in kwargs])
    values = list(kwargs.values()) + [player_id]
    conn = get_conn()
    conn.execute(f"UPDATE players SET {fields} WHERE id=?", values)
    conn.commit()
    conn.close()

def count_players():
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    conn.close()
    return total

def count_by_position():
    conn = get_conn()
    rows = conn.execute("SELECT position, COUNT(*) as c FROM players GROUP BY position").fetchall()
    conn.close()
    return {r["position"]: r["c"] for r in rows}

def get_min_base_price():
    conn = get_conn()
    row = conn.execute("SELECT MIN(base_price) FROM players WHERE status='pending'").fetchone()
    conn.close()
    return row[0] if row[0] else 0.5

def log_sold(player_id, team_id, price):
    import datetime
    conn = get_conn()
    conn.execute("INSERT INTO sold (player_id, team_id, price, timestamp) VALUES (?,?,?,?)", (player_id, team_id, price, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_sold_by_team(team_id):
    conn = get_conn()
    rows = conn.execute("SELECT p.name, p.position, s.price FROM sold s JOIN players p ON p.id = s.player_id WHERE s.team_id=? ORDER BY s.id", (team_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def reset_auction():
    conn = get_conn()
    conn.execute("DELETE FROM teams")
    conn.execute("DELETE FROM sold")
    conn.execute("UPDATE players SET status='pending', set_id=NULL")
    conn.execute("UPDATE auction_state SET status='idle', host_id=NULL, host_username=NULL, current_player_id=NULL, current_set=1, highest_bid=0, highest_team_id=NULL, last_bid_time=0, last_reminder=NULL, live_message_id=NULL WHERE id=1")
    conn.commit()
    conn.close()


# ============================================================
# SETS — build & query (ROUND-ROBIN order)
# ============================================================
# Set order:
# 1=GK p1, 2=DEF p1, 3=MID p1, 4=FWD p1,
# 5=GK p2, 6=DEF p2, 7=MID p2, 8=FWD p2,
# 9=GK p3, 10=DEF p3, 11=MID p3, 12=FWD p3
# ============================================================

POSITIONS = ["GK", "DEF", "MID", "FWD"]

# Map: set_id → (position, part)
SET_MAP = {
    1: ("GK", 1), 2: ("DEF", 1), 3: ("MID", 1), 4: ("FWD", 1),
    5: ("GK", 2), 6: ("DEF", 2), 7: ("MID", 2), 8: ("FWD", 2),
    9: ("GK", 3), 10: ("DEF", 3), 11: ("MID", 3), 12: ("FWD", 3),
}


def build_sets():
    """
    Randomly shuffle each position's players, split into 3 parts,
    assign set_ids in ROUND-ROBIN order:
    GK p1→1, DEF p1→2, MID p1→3, FWD p1→4,
    GK p2→5, DEF p2→6, MID p2→7, FWD p2→8,
    GK p3→9, DEF p3→10, MID p3→11, FWD p3→12
    """
    import random
    conn = get_conn()
    conn.execute("UPDATE players SET set_id=NULL")

    # For each position, shuffle and split into 3
    parts = {}  # parts[pos] = [part1_ids, part2_ids, part3_ids]
    for pos in POSITIONS:
        rows = conn.execute("SELECT id FROM players WHERE position=?", (pos,)).fetchall()
        ids = [r[0] for r in rows]
        random.shuffle(ids)
        n = len(ids)
        parts[pos] = [
            ids[:n//3],
            ids[n//3:2*n//3],
            ids[2*n//3:],
        ]

    # Now assign set_ids in round-robin
    for set_id, (pos, part) in SET_MAP.items():
        part_ids = parts[pos][part - 1]
        for pid in part_ids:
            conn.execute("UPDATE players SET set_id=? WHERE id=?", (set_id, pid))

    conn.commit()
    conn.close()
    return len(SET_MAP)


def get_set_players(set_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM players WHERE set_id=? ORDER BY id", (set_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_set_position(set_id):
    """Returns (position, part) for a given set_id."""
    return SET_MAP.get(set_id, ("?", 1))


def get_next_player_in_set(set_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM players WHERE set_id=? AND status='pending' ORDER BY RANDOM() LIMIT 1",
        (set_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def count_pending_in_set(set_id):
    conn = get_conn()
    row = conn.execute("SELECT COUNT(*) FROM players WHERE set_id=? AND status='pending'", (set_id,)).fetchone()
    conn.close()
    return row[0] if row else 0


def count_total_in_set(set_id):
    conn = get_conn()
    row = conn.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,)).fetchone()
    conn.close()
    return row[0] if row else 0


def get_total_sets():
    return len(SET_MAP)
