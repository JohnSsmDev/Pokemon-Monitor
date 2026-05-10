import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    vip INTEGER DEFAULT 0,
    requests INTEGER DEFAULT 0
)
""")

conn.commit()


def create_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (user_id,))
    conn.commit()


def get_user(user_id):
    cursor.execute("SELECT telegram_id, vip, requests FROM users WHERE telegram_id=?", (user_id,))
    return cursor.fetchone()


def set_vip(user_id):
    cursor.execute("UPDATE users SET vip=1 WHERE telegram_id=?", (user_id,))
    conn.commit()


def add_request(user_id):
    cursor.execute("UPDATE users SET requests = requests + 1 WHERE telegram_id=?", (user_id,))
    conn.commit()