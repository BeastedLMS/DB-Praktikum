import sqlite3

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    password TEXT,
    address TEXT,
    city TEXT,
    zip TEXT,
    PRIMARY KEY(email)
    )
''')

connection.commit()
connection.close()