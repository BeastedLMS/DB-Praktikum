import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('INSERT INTO users (first_name, last_name, email, password, address, city, zip) VALUES (?, ?, ?, ?, ?, ?, ?)',
               ('Test', 'User', 'test@example.com', 'password123', 'Teststraße 1', 'Teststadt', '12345'))

conn.commit()
conn.close()
