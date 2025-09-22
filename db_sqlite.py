import sqlite3

def connect_db():
    conn = sqlite3.connect("database.db")
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cidades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        estado TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def insert_city(nome, estado):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cidades (nome, estado) VALUES (?, ?)', (nome, estado))
    conn.commit()
    conn.close()

def query_cities():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cidades')
    results = cursor.fetchall()
    conn.close()
    return results