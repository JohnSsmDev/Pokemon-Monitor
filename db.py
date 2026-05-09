import sqlite3

# =========================
# DATABASE
# =========================

conn = sqlite3.connect(
    "market.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================
# TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# =========================
# SAVE PRICE
# =========================

def save_price(name, price):

    cursor.execute(
        "INSERT INTO prices (name, price) VALUES (?, ?)",
        (name, price)
    )

    conn.commit()

# =========================
# GET AVERAGE
# =========================

def get_average_price(name):

    cursor.execute(
        "SELECT AVG(price) FROM prices WHERE name=?",
        (name,)
    )

    result = cursor.fetchone()

    if result and result[0]:

        return float(result[0])

    return None