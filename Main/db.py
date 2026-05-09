import sqlite3

conn = sqlite3.connect("market.db", check_same_thread=False)
cursor = conn.cursor()

# =========================
# TABELAS
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    vip INTEGER DEFAULT 0,
    requests INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    name TEXT,
    price REAL,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# =========================
# USUÁRIOS
# =========================
def register_user(user_id):

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,)
    )

    conn.commit()


def is_vip(user_id):

    cursor.execute(
        "SELECT vip FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cursor.fetchone()

    return result and result[0] == 1


def set_vip(user_id):

    cursor.execute(
        "UPDATE users SET vip=1 WHERE user_id=?",
        (user_id,)
    )

    conn.commit()


# =========================
# LIMITES FREE
# =========================
def can_use(user_id):

    cursor.execute(
        "SELECT requests FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cursor.fetchone()

    if not result:
        return True

    return result[0] < 10


def add_request(user_id):

    cursor.execute(
        "UPDATE users SET requests = requests + 1 WHERE user_id=?",
        (user_id,)
    )

    conn.commit()


# =========================
# PREÇOS
# =========================
def save_price(name, price):

    cursor.execute(
        "INSERT INTO prices (name, price) VALUES (?, ?)",
        (name, price)
    )

    conn.commit()


def get_average_price(name):

    cursor.execute(
        "SELECT price FROM prices WHERE name=?",
        (name,)
    )

    data = cursor.fetchall()

    if not data:
        return None

    prices = [x[0] for x in data]

    return sum(prices) / len(prices)