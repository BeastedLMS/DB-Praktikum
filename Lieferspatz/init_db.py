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
    guthaben NUMERIC(10,2),
    PRIMARY KEY(email)
    )
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_name TEXT,
    email TEXT,
    password TEXT,
    address TEXT,
    zip TEXT,
    caption TEXT,
    guthaben NUMERIC(10,2),
    PRIMARY KEY(email)
    )
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS menue (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    price NUMERIC(10,2) NOT NULL,
    restaurant_email TEXT,
    FOREIGN KEY(restaurant_email) REFERENCES restaurants(email)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    )
''')


connection.commit()
connection.close()