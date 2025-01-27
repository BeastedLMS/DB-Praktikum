from flask import Flask, request, render_template, Response, redirect, Blueprint, flash, url_for, session
import sqlite3

views = Blueprint('views', __name__)

app = Flask(__name__)

@views.route('/') #main page is just /
def home():
    return render_template("home.html")

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email_eingabe = request.form.get('email')
        password_eingabe = request.form.get('password')
        
        #Kunde login
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('''
                       select password from users where email = ?
                       ''', (email_eingabe,))
        result = cursor.fetchone()

        if result and password_eingabe == result[0]:
            flash('Sie sind eingeloggt!', category='success')
            #Sessiondaten für Kunde speichern
            cursor.execute('''
                           SELECT first_name, last_name, email, address, city, zip, guthaben FROM users WHERE email = ?
                           ''', (email_eingabe,))
            rowsKunde = cursor.fetchall()

            session['user_name'] = rowsKunde[0][0] + " " + rowsKunde[0][1]
            session['user_email'] = rowsKunde[0][2]
            session['user_address'] = rowsKunde[0][3]
            session['user_city'] = rowsKunde[0][4]
            session['user_zip'] = rowsKunde[0][5]
            session['user_guthaben'] = rowsKunde[0][6]
            #Sessiondaten für Kunde speichern
            connection.close()
            return redirect(url_for('views.homeKunde')) 
        connection.close()


        #Restaurant Login
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('''
                       select password from restaurants where email = ?
                       ''', (email_eingabe,))
        result = cursor.fetchone()

        if result and password_eingabe == result[0]:
            flash('Sie sind eingeloggt!', category='success')
            #Sessiondaten für Restaurant speichern
            cursor.execute('''
                           SELECT restaurant_name, email, address, city, zip, caption, bild, guthaben FROM restaurants WHERE email = ?
                           ''', (email_eingabe,))
            rowsRestaurant = cursor.fetchall()

            session['restaurant_name'] = rowsRestaurant[0][0]
            session['restaurant_email'] = rowsRestaurant[0][1]
            session['restaurant_address'] = rowsRestaurant[0][2]
            session['restaurant_city'] = rowsRestaurant[0][3]
            session['restaurant_zip'] = rowsRestaurant[0][4]
            session['restaurant_caption'] = rowsRestaurant[0][5]
            session['restaurant_bild'] = rowsRestaurant[0][6]
            session['restaurant_guthaben'] = rowsRestaurant[0][7]
            #Sessiondaten für Restaurant speichern
            connection.close()
            return redirect(url_for('views.homeRestaurant'))
        connection.close()
        flash('Ungültige E-Mail oder Passwort. Bitte versuche es erneut.', 'error')

    return render_template("login.html", text="Testing", user="Name", boolean=True)

#Um sessiondaten des Users zu löschen und auf die Startseite zu leiten

@views.route('/logoutUser', methods=['GET', 'POST'])
def logoutUser():
    session.pop('user_name', None)
    session.pop('user_email', None)
    session.pop('user_address', None)
    session.pop('user_city', None)
    session.pop('user_zip', None)
    session.pop('user_guthaben', None)
    session.pop('order_id', None)
    return redirect(url_for('views.home'))

#Um Sessiondaten des Restaurants zu löschen und auf die Startseite zu leiten
@views.route('/logoutRestaurant', methods=['GET', 'POST'])
def logoutRestaurant():
    session.pop('restaurant_name', None)
    session.pop('restaurant_email', None)
    session.pop('restaurant_address', None)
    session.pop('restaurant_city', None)
    session.pop('restaurant_zip', None)
    session.pop('restaurant_caption', None)
    session.pop('restaurant_bild', None)
    session.pop('restaurant_guthaben', None)
    return redirect(url_for('views.home'))

@views.route('/signupKunde', methods=['GET', 'POST'])
def signupKunde():
    if request.method == 'POST':

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        address = request.form.get("address")
        city = request.form.get("city")
        zip = request.form.get("zip")

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute('''
                       SELECT email FROM users WHERE email = ?;    
                       ''', (email,))
        
        ex_check = cursor.fetchone()
        if ex_check:
            connection.close()
            flash('Dieser Account existiert bereits.', category='error')
            return render_template("signupKunde.html")

        cursor.execute('''
                       insert into users (first_name, last_name, email, password, address, city, zip, guthaben)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (first_name, last_name, email, password, address, city, zip, 100))
        
        connection.commit()
        connection.close()
        flash('Sie haben sich erfolgreich registriert!', category='success')
        return redirect(url_for("views.home"))
    
    return render_template("signupKunde.html")


@views.route('/signupGeschaeft', methods=['GET', 'POST'])
def signupGeschaeft():
    if request.method == 'POST':

        restaurant_name = request.form.get("restaurant_name")
        email = request.form.get("email")
        password = request.form.get("password")
        address = request.form.get("address")
        zip = request.form.get("zip")
        city = request.form.get("city")
        caption = request.form.get("caption")
        bild = request.form.get("bild")

        if not restaurant_name or not caption or  not email or not password or not address or not city or not zip:
            flash('Bitte füllen Sie Felder aus.', category='error')
            return render_template("signupGeschaeft.html")

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute('''
                       SELECT email FROM restaurants WHERE email = ?;    
                       ''', (email,))
        
        ex_check = cursor.fetchone()
        if ex_check:
            connection.close()
            flash('Dieser Account existiert bereits.', category='error')
            return render_template("signupGeschaeft.html")

        cursor.execute('''
                       insert into restaurants (restaurant_name, email, password, address, city, zip, caption, bild, guthaben)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (restaurant_name, email, password, address, city, zip, caption, bild, 0))
        
        connection.commit()
        connection.close()
        flash('Sie haben sich erfolgreich registriert!', category='success')
        return redirect(url_for("views.home"))
    
    return render_template("signupGeschaeft.html")

@views.route('/homeRestaurant')
def homeRestaurant():     
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # # Testdaten für Bestellungen
    # cursor.execute('''
    #     INSERT INTO orders (restaurant_email, items, total_price, delivery_address, date, time, status)
    #     VALUES 
    #     ('admin@1', 'Pizza, Cola', 20.50, 'Musterstraße 123, Musterstadt', '2025-01-25', '18:30', 'in Bearbeitung'),
    #     ('admin@1', 'Burger, Pommes', 15.00, 'Beispielstraße 45, Teststadt', '2025-01-20', '17:00', 'old')
    # ''')
    # connection.commit()


    # neue Bestellunguen aus der Datenbank holen
    cursor.execute('''
        SELECT order_id, total_price, delivery_address, order_date
        FROM orders
        WHERE status = 'in Bearbeitung' OR status = 'in Zubereitung'
    ''')
    new_orders = cursor.fetchall()

    # alte Bestellungen aus der Datenbank holen
    cursor.execute('''
        SELECT order_id, total_price, delivery_address, order_date
        FROM orders
        WHERE status = 'abgeschlossen' OR status = 'storniert'
    ''')

    

    old_orders = cursor.fetchall()

    connection.close()                              
    return render_template('homeRestaurant.html', new_orders=new_orders, old_orders=old_orders)

def update_order_status(order_id, status):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE orders 
        SET status = ? 
        WHERE order_id = ?
        ''', (status, order_id))
    conn.commit()
    conn.close()

@views.route('/accept_order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    update_order_status(order_id, 'in Zubereitung')
    return redirect(url_for('homeRestaurant.html'))

@views.route('/reject_order/<int:order_id>', methods=['POST'])
def reject_order(order_id):
    update_order_status(order_id, 'storniert')
    return redirect(url_for('homeRestaurant.html'))

@views.route('annehmen/<int:order_id>', methods=['POST'])
def annehmen(order_id):
    return redirect(url_for('homeRestaurant.html'))
@views.route('/homeKunde')
def homeKunde():
    user_zip = session.get('user_zip')
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''
                    SELECT DISTINCT restaurants.restaurant_name, restaurants.caption, restaurants.address, restaurants.city, restaurants.zip, restaurants.email
                    FROM restaurants
                    JOIN delivery_areas ON restaurants.email = delivery_areas.restaurant_email
                    WHERE delivery_areas.zip = ?
                    ''', (user_zip,))
    restaurantListe = cursor.fetchall()
    connection.close()

    restaurants = [{"name": row[0], "beschreibung": row[1], "adresse": row[2], "stadt": row[3], "plz": row[4], "email": row[5]} for row in restaurantListe]

    return render_template("homeKunde.html", restaurants=restaurants)

@views.route('/bestellungZusammenstellen', methods=['GET', 'POST'])
def bestellungZusammenstellen():
    restaurant_email = request.form.get("restaurant_email")
    if not restaurant_email:
        restaurant_email = request.args.get("restaurant_email")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''
                        SELECT restaurant_name, caption, address, city, zip, bild
                        FROM restaurants
                        WHERE email = ?
                        ''', (restaurant_email,))
    restaurant = cursor.fetchone()

    cursor.execute('''
                        SELECT day_of_the_week, opening_time, closing_time
                        FROM oeffnungszeiten
                        WHERE restaurant_email = ?
                        ''', (restaurant_email,))
    opening_hours = cursor.fetchall()

    cursor.execute('''
                        SELECT item_name, caption, price
                        FROM menue
                        WHERE restaurant_email = ?
                        ''', (restaurant_email,))
    menu_items = cursor.fetchall()
    connection.close()

    restaurant_details = {
        "name": restaurant[0],
        "beschreibung": restaurant[1],
        "adresse": restaurant[2],
        "stadt": restaurant[3],
        "plz": restaurant[4],
        "bild": restaurant[5],
        "restaurant_email": restaurant_email,
        "oeffnungszeiten": {day: {'opening_time': opening_time, 'closing_time': closing_time} for day, opening_time, closing_time in opening_hours}
    }
    
    return render_template("bestellungZusammenstellen.html", restaurant=restaurant_details, items=menu_items)

@views.route('/bestellhistorie')
def bestellhistorie():
    return render_template("bestellhistorie.html")

@views.route('/warenkorb')
def warenkorb():
    #restaurant_email = request.form.get("restaurant_email")
    order_id = session.get('order_id')
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''
                    SELECT item_name, quantity, price
                    FROM order_details
                    WHERE order_id = ?
                    ''', (order_id,))
    items = cursor.fetchall()

    cursor.execute('''
                    SELECT total_price
                    FROM orders
                    WHERE order_id = ?
                    ''', (order_id,))
    total_price = cursor.fetchone()
    connection.close()
    return render_template("warenkorb.html", items=items, total_price=total_price)

@views.route('/menue', methods=['GET', 'POST'])
def menue():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        name = request.form.get('name')
        price = request.form.get('price')
        caption = request.form.get('caption')
        restaurant_email = session.get('restaurant_email')

        if item_id:  # Vorhandenen Artikel aktualisieren
            cursor.execute('''
                           UPDATE menue
                           SET item_name = ?, price = ?, caption = ?
                           WHERE item_id = ? AND restaurant_email = ?
                           ''', (name, price, caption, item_id, restaurant_email))
        else:  # Neuen Artikel hinzufügen
            cursor.execute('''
                           INSERT INTO menue (item_name, price, restaurant_email, caption)
                           VALUES (?, ?, ?, ?)
                           ''', (name, price, restaurant_email, caption))

        connection.commit()

    cursor.execute('''
                   SELECT item_id, item_name, price, caption FROM menue WHERE restaurant_email = ?
                   ''', (session.get('restaurant_email'),))
    items = cursor.fetchall()
    connection.close()

    menu_items = [{"id": row[0], "name": row[1], "price": row[2], "caption": row[3]} for row in items]

    return render_template("menue.html", items=menu_items)

@views.route('/verwaltung', methods=['GET', 'POST'])
def verwaltung():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    if request.method == 'POST':

        restaurant_email = session.get('restaurant_email') # Hier wird die E-Mail-Adresse des Restaurants aus der Session geholt

                    # Überprüfen, ob bereits Öffnungszeiten für das Restaurant in der Datenbank existieren
        cursor.execute('''
                        SELECT * FROM oeffnungszeiten WHERE restaurant_email = ?
                        ''', (restaurant_email,))
        ex_check = cursor.fetchone()
        
        
            
        # Wenn keine Öffnungszeiten existieren, werden sie in die Datenbank eingefügt
        if not ex_check:
                
                for day in ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']:
                    opening_time = request.form.get(f'{day}_opening_time', '')
                    closing_time = request.form.get(f'{day}_closing_time', '')

                    cursor.execute('''
                                    INSERT INTO oeffnungszeiten (restaurant_email, day_of_the_week, opening_time, closing_time)
                                    VALUES (?, ?, ?, ?)
                                    ''', (restaurant_email, day, opening_time, closing_time))
            
        # Wenn bereits Öffnungszeiten existieren, werden sie aktualisiert
        else:
                for day in ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']:
                    opening_time = request.form.get(f'{day}_opening_time', '')
                    closing_time = request.form.get(f'{day}_closing_time', '')

                    cursor.execute('''
                                    UPDATE oeffnungszeiten
                                    SET opening_time = ?, closing_time = ?
                                    WHERE restaurant_email = ? AND day_of_the_week = ?
                     ''', (opening_time, closing_time, restaurant_email, day))
                   
        connection.commit()


    # Holen der aktuellen Liefergebiete aus der Datenbank
    cursor.execute('''
                            SELECT restaurant_email, zip
                            FROM delivery_areas
                            WHERE restaurant_email = ?
                            ''', (session.get('restaurant_email'),))
    areas = cursor.fetchall()    

    # Holen der aktuellen Öffnungszeiten aus der Datenbank
    cursor.execute('''
        SELECT day_of_the_week, opening_time, closing_time
        FROM oeffnungszeiten
        WHERE restaurant_email = ?
    ''', (session.get('restaurant_email'),))
    opening_hours = cursor.fetchall()
    connection.close()

    # Umwandeln in ein Wörterbuch
    opening_hours_dict = {day: {'opening_time': opening_time, 'closing_time': closing_time}
                          for day, opening_time, closing_time in opening_hours}

    return render_template('verwaltung.html', opening_hours=opening_hours_dict, areas=areas)


@views.route('/remove_item/<int:item_id>', methods=['POST'])
def remove_item(item_id):
    if request.method == 'POST':
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
                        DELETE FROM menue
                        WHERE item_id = ?
                        ''', (item_id,))
        connection.commit()
        connection.close()
        return redirect(url_for("views.menue"))



@views.route('/neue_plz', methods=['POST'])
def neue_plz():
    if request.method ==  'POST':
        restaurant_email = session.get('restaurant_email')
        plz = request.form.get('plz')

        # Überprüfen, ob eine PLZ eingegeben wurde
        if not plz: 
            flash("Bitte geben Sie eine PLZ an.", "error")
            return redirect(url_for('views.verwaltung'))

        # Überprüfen ob die PLZ bereits in der Datenbank existiert
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
                        SELECT 1
                        FROM delivery_areas
                        WHERE restaurant_email = ? AND zip = ?
                        ''', (restaurant_email, plz))
        ex_check = cursor.fetchone()

        if ex_check:    #Wenn die PLZ bereits in der Datenbank existiert, wird eine Fehlermeldung ausgegeben
            flash(f"Die PLZ {plz} ist bereits in Ihrer Lieferzone vorhanden.", "warning")

        else: #Wenn die PLZ noch nicht in der Datenbank existiert, wird sie hinzugefügt
            cursor.execute('''
                            INSERT INTO delivery_areas (restaurant_email, zip)
                            VALUES (?, ?)
                            ''', (restaurant_email, plz))
            flash(f"Die PLZ {plz} wurde erfolgreich hinzugefügt.", "success")
            connection.commit()
        
        connection.close()
        return redirect(url_for('views.verwaltung'))
    

@views.route('/delete_plz', methods=['POST'])
def delete_plz():
        restaurant_email = session.get('restaurant_email') # Hier wird die E-Mail-Adresse des Restaurants aus der Session geholt
        plz = request.form.get('plz') # Hier wird die PLZ aus dem Formular geholt

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
                        DELETE FROM delivery_areas
                        WHERE restaurant_email = ? AND zip = ?
                        ''', (restaurant_email, plz))
        connection.commit()
        connection.close()

        return redirect(url_for('views.verwaltung'))


# Hier kommt der Abschnitt für die Bestellungen, bzw. das erstellen und hinzufügen von Items und Bestellungen
@views.route('/add_to_order', methods=['POST'])
def add_to_order():
    #Daten aus der Seite bestellungZusammenstellen holen
    item_name = request.form.get('item_name')
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('item_price'))
    user_email = session.get('user_email')  # Benutzer-Email aus Session
    restaurant_email = request.form.get("restaurant_email") # Restaurant-Email aus der Seite
    user_address = session.get('user_address')  # Lieferadresse
    user_plz = session.get('user_zip')  # Liefer-PLZ

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    #Überprüfen, ob bereits eine Bestellung für den Benutzer existiert
    order_id = session.get('order_id')
    if not order_id:
        #Neue Bestellung Anlegen, da keine vorhanden ist
        cursor.execute('''
                        INSERT INTO orders (user_email, restaurant_email, total_price, delivery_address, delivery_plz, status)
                        VALUES (?, ?, 0, ?, ?, 'in Bearbeitung')
                        ''', (user_email, restaurant_email, user_address, user_plz))
        connection.commit()
        order_id = cursor.lastrowid
        session['order_id'] = order_id

    #Items zur Bestellung hinzufügen
    # Prüfen, ob ein Eintrag mit derselben order_id und item_name existiert
    cursor.execute('''
        SELECT quantity
        FROM order_details
        WHERE order_id = ? AND item_name = ?
    ''', (order_id, item_name))

    existing_entry = cursor.fetchone()

    if existing_entry:
        # Wenn der Eintrag existiert, erhöhe die quantity
        new_quantity = existing_entry[0] + quantity  # Addiere die neue Menge
        cursor.execute('''
            UPDATE order_details
            SET quantity = ?
            WHERE order_id = ? AND item_name = ?
        ''', (new_quantity, order_id, item_name))
    else:
        # Wenn kein Eintrag existiert, füge einen neuen hinzu
        cursor.execute('''
            INSERT INTO order_details (order_id, item_name, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', (order_id, item_name, quantity, price))
    connection.commit()

    #Gesamtpreis der Bestellung aktualisieren
    cursor.execute('''
                   UPDATE orders
                     SET total_price = total_price + ?
                     WHERE order_id = ?
                     ''', (price * quantity, order_id))
    connection.commit()
    connection.close()

    return redirect(url_for('views.bestellungZusammenstellen', restaurant_email=restaurant_email))

@views.route('/remove_item_order', methods=['POST'])
def remove_item_order():
    item_name = request.form.get("item_name")  # Namen des Items
    remove_count = int(request.form.get("remove_count"))  # Menge
    order_id = session.get('order_id')  # Bestellungs-ID

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    #Menge des Items holen
    cursor.execute('''
                    SELECT quantity, price
                    FROM order_details
                    WHERE order_id = ? AND item_name = ?
                    ''', (order_id, item_name))
    item = cursor.fetchone()


    if item:
        current_quantity = item[0]
        new_quantity = current_quantity - remove_count

        if new_quantity > 0:
            cursor.execute('''
                    UPDATE orders
                    SET total_price = total_price - ?
                    WHERE order_id = ?
                    ''', (item[1] * remove_count, order_id))
            
            cursor.execute('''
                        UPDATE order_details
                        SET quantity = quantity - ?
                        WHERE order_id = ? AND item_name = ?
                        ''', (remove_count, order_id, item_name))

        else:
            cursor.execute('''
                        DELETE FROM order_details
                        WHERE order_id = ? AND item_name = ?
                        ''', (order_id, item_name))

    connection.commit()   
    connection.close()
    return redirect(url_for('views.warenkorb'))