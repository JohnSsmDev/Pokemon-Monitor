import sqlite3

conn = sqlite3.connect("market.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    name TEXT,
    price REAL,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

def save_price(name, price):

    cursor.execute(
        "INSERT INTO prices(name, price) VALUES (?, ?)",
        (name, price)
    )

    conn.commit()

def get_history(name):

    cursor.execute(
        "SELECT price FROM prices WHERE name=?",
        (name,)
    )

    return [x[0] for x in cursor.fetchall()]