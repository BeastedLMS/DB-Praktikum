import sqlite3

def init_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menue (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            price REAL NOT NULL,
            restaurant_email TEXT NOT NULL,
            FOREIGN KEY (restaurant_email) REFERENCES restaurants(email)
        )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_db()