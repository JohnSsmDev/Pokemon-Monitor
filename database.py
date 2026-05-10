import sqlite3

conn = sqlite3.connect("precos.db", check_same_thread=False)
cursor = conn.cursor()

def init():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL,
        media REAL,
        score REAL,
        data TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alertas (
        nome TEXT PRIMARY KEY
    )
    """)

    conn.commit()


def salvar(nome, preco, media, score, data):
    cursor.execute("""
    INSERT INTO historico (nome, preco, media, score, data)
    VALUES (?, ?, ?, ?, ?)
    """, (nome, preco, media, score, data))
    conn.commit()


def ja_alertado(nome):
    cursor.execute("SELECT 1 FROM alertas WHERE nome=?", (nome,))
    return cursor.fetchone() is not None


def marcar(nome):
    cursor.execute("INSERT OR IGNORE INTO alertas VALUES (?)", (nome,))
    conn.commit()