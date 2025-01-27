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
    guthaben REAL,
    PRIMARY KEY(email)
    )
''')    #Guthaben später nochmal als numeric(10,2) testen

cursor.execute('''
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_name TEXT,
    email TEXT,
    password TEXT,
    address TEXT,
    city TEXT,
    zip TEXT,
    caption TEXT,
    bild TEXT,
    guthaben REAL,
    PRIMARY KEY(email)
    )
''')    #Guthaben später nochmal als numeric(10,2) testen

cursor.execute('''
CREATE TABLE IF NOT EXISTS menue (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    price REAL NOT NULL,
    restaurant_email TEXT,
    caption TEXT,
    FOREIGN KEY(restaurant_email) REFERENCES restaurants(email)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    )
''')



cursor.execute('''
CREATE TABLE IF NOT EXISTS oeffnungszeiten (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_email TEXT NOT NULL,
    day_of_the_week TEXT NOT NULL,
    opening_time TEXT,
    closing_time TEXT,
    FOREIGN KEY(restaurant_email) REFERENCES restaurants(email)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    )            
''')

cursor.execute('''
create table IF NOT EXISTS delivery_areas (
    restaurant_email TEXT NOT NULL,
    zip TEXT NOT NULL,
    Primary Key(restaurant_email, zip),
    FOREIGN KEY(restaurant_email) REFERENCES restaurants(email)
        ON DELETE CASCADE
        ON UPDATE CASCADE          
    )         
''')

# tabelle für die Bestellungen
cursor.execute('''
create table IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    restaurant_email TEXT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_price REAL NOT NULL,
    delivery_address TEXT NOT NULL,
    delivery_plz TEXT NOT NULL,
    caption TEXT,
    status TEXT NOT NULL,
    FOREIGN KEY(restaurant_email) REFERENCES restaurants(email)
        ON UPDATE CASCADE
    FOREIGN KEY(user_email) REFERENCES users(email)
)
''')

# Tabelle für Details der Bestellungen
cursor.execute('''
create table IF NOT EXISTS order_details (
    order_details_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL,
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
)
''')

connection.commit()
connection.close()