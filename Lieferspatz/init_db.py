import sqlite3

connection = sqlite3.connect("users.db")

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    password TEXT,
    address TEXT,
    city TEXT,
    zip TEXT
    )
''')

connection.commit()
connection.close()