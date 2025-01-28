from flask import Flask, request, render_template, Response, redirect, Blueprint, flash, url_for, session, jsonify
import sqlite3, time
from decimal import Decimal, ROUND_HALF_UP


views = Blueprint('views', __name__)

app = Flask(__name__)

# Decimal-Konvertierung für SQLite
def adapt_decimal(value):
    return str(value)  # Decimal zu String für die Datenbank

def convert_decimal(value):
    return Decimal(value.decode())  # String aus der DB zu Decimal

# Registrierung der Adapter und Konverter
sqlite3.register_adapter(Decimal, adapt_decimal)
sqlite3.register_converter("DECIMAL", convert_decimal)

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
            session['user_guthaben'] = str(rowsKunde[0][6])
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
            session['restaurant_guthaben'] = str(rowsRestaurant[0][7])
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
    connection = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    restaurant_email = session.get('restaurant_email')
    restaurant_guthaben = Decimal(session.get('restaurant_guthaben'))

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
        SELECT order_id, total_price, delivery_address, order_date, status, user_email
        FROM orders
        WHERE (status = 'in Bearbeitung' OR status = 'in Zubereitung') AND restaurant_email = ?
    ''', (restaurant_email,))
    new_orders = cursor.fetchall()

    # alte Bestellungen aus der Datenbank holen
    cursor.execute('''
        SELECT order_id, total_price, delivery_address, order_date, status, user_email
        FROM orders
        WHERE (status = 'abgeschlossen' OR status = 'storniert') AND restaurant_email = ?
    ''', (restaurant_email,))

    

    old_orders = cursor.fetchall()

    connection.close()                              
    return render_template('homeRestaurant.html', new_orders=new_orders, old_orders=old_orders, restaurant_guthaben=restaurant_guthaben)


@views.route('/check_new_orders')
def check_new_orders():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    
    restaurant_email = session.get('restaurant_email')

    # Anzahl neuer Bestellungen holen
    cursor.execute('''
        SELECT COUNT(*) FROM orders
        WHERE status = 'in Bearbeitung' AND restaurant_email = ?
    ''', (restaurant_email,))
    
    new_orders_count = cursor.fetchone()[0] #von den neuen Bestellungen die neuste holen
    connection.close()

    return jsonify({'new_orders': new_orders_count})



@views.route('/send_order/<int:order_id>', methods=['POST'])
def send_order(order_id):
    connection = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE orders 
        SET status = ? 
        WHERE order_id = ?
        ''', ('abgeschlossen', order_id))
    connection.commit()
    connection.close()
    return redirect(url_for('views.homeRestaurant'))


@views.route('/accept_order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    connection = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE orders 
        SET status = ? 
        WHERE order_id = ?
        ''', ('in Zubereitung', order_id))
    connection.commit()

    #Gesamtpreis der Bestellung holen
    cursor.execute('''
                   select total_price
                     from orders
                     where order_id = ?
                     ''', (order_id,))
    order_details = cursor.fetchone()
    total_price = Decimal(order_details[0])

    #Bezahlen und Geld aufteilen
    lieferspatz_share = total_price * Decimal('0.15')
    restaurant_share = total_price * Decimal('0.85')

    lieferspatz_share = lieferspatz_share.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    restaurant_share = restaurant_share.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Guthaben des Restaurants erhöhen
    cursor.execute('''
            UPDATE restaurants
            SET guthaben = guthaben + ?
            WHERE email = ?
            ''', (restaurant_share, session.get('restaurant_email')))

    # Guthaben von Lieferspatz erhöhen
    cursor.execute('''
            UPDATE restaurants
            SET guthaben = guthaben + ?
            WHERE email = 'Lieferspatz@gmail.com'
            ''', (lieferspatz_share,))
    
    session['restaurant_guthaben'] = str(Decimal(session.get('restaurant_guthaben')) + restaurant_share)
    connection.commit()
    connection.close()
    return redirect(url_for('views.homeRestaurant'))

@views.route('/reject_order/<int:order_id>', methods=['POST'])
def reject_order(order_id):
    
    total_price = request.form.get('total_price')
    user_email = request.form.get('user_email')

    # Umwandlung von total_price in Decimal
    total_price_decimal = Decimal(total_price)
        
    # Sicherstellen, dass der Preis auf zwei Dezimalstellen gerundet wird
    total_price_decimal = total_price_decimal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE orders 
        SET status = ? 
        WHERE order_id = ?
        ''', ('storniert', order_id))
    connection.commit()

    cursor.execute('''
            UPDATE users
            SET guthaben = guthaben + ?
            WHERE email = ?
            ''', (total_price_decimal, user_email))
    connection.commit()
    connection.close()
    session['user_guthaben'] = str(Decimal(session.get('user_guthaben')) + total_price_decimal)
    return redirect(url_for('views.homeRestaurant'))

@views.route('/homeKunde')
def homeKunde():
    user_zip = session.get('user_zip')
    user_guthaben = Decimal(session.get('user_guthaben'))
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

    return render_template("homeKunde.html", restaurants=restaurants, user_guthaben=user_guthaben)

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
    user_guthaben = Decimal(session.get('user_guthaben'))
    user_email = session.get('user_email')
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    

    # neue Bestellungen anzeigen
    cursor.execute('''
                   SELECT orders.order_id, orders.total_price, orders.order_date, orders.status, 
                    order_details.item_name, order_details.price, 
                    restaurants.restaurant_name
                        FROM orders
                        INNER JOIN order_details ON orders.order_id = order_details.order_id
                        INNER JOIN restaurants ON orders.restaurant_email = restaurants.email
                        WHERE (orders.status = 'in Bearbeitung' OR orders.status = 'in Zubereitung') AND orders.user_email = ?;
    ''', (user_email,))
    new_orders = cursor.fetchall()

    
    # alte Bestellungen anzeigen
    cursor.execute('''
                   SELECT orders.order_id, orders.total_price, orders.order_date, orders.status, 
                    order_details.item_name, order_details.price, restaurants.restaurant_name
                        FROM orders
                        INNER JOIN order_details ON orders.order_id = order_details.order_id
                        INNER JOIN restaurants ON orders.restaurant_email = restaurants.email
                        WHERE (orders.status = 'abgeschlossen' OR orders.status = 'storniert') AND orders.user_email = ?;
    ''', (user_email,))
    old_orders = cursor.fetchall()

    return render_template("bestellhistorie.html", new_orders=new_orders, old_orders=old_orders, user_guthaben=user_guthaben)

@views.route('/warenkorb')
def warenkorb():
    order_id = session.get('order_id')
    user_guthaben = Decimal(session.get('user_guthaben'))

    connection = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
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
    order_details = cursor.fetchone()
    total_price = Decimal(order_details[0]) if order_details else Decimal("0.00")

    connection.close()
    return render_template("warenkorb.html", items=items, total_price=total_price, user_guthaben=user_guthaben)

@views.route('/menue', methods=['GET', 'POST'])
def menue():
    restaurant_guthaben = Decimal(session.get('restaurant_guthaben'))
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        name = request.form.get('name')
        price = (request.form.get('price'))
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

    return render_template("menue.html", items=menu_items, restaurant_guthaben=restaurant_guthaben)

@views.route('/verwaltung', methods=['GET', 'POST'])
def verwaltung():
    restaurant_guthaben = Decimal(session.get('restaurant_guthaben'))
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

    # Holen der aktuellen Beschreibung aus der Datenbank
    cursor.execute('''
        SELECT caption
        FROM restaurants
        WHERE email = ?
    ''', (session.get('restaurant_email'),))
    current_caption = cursor.fetchone()[0]

    connection.close()

    # Umwandeln in ein Wörterbuch
    opening_hours_dict = {day: {'opening_time': opening_time, 'closing_time': closing_time}
                          for day, opening_time, closing_time in opening_hours}

    return render_template('verwaltung.html', opening_hours=opening_hours_dict, areas=areas, current_caption=current_caption, restaurant_guthaben=restaurant_guthaben)

@views.route('/update_description', methods=['POST'])
def update_description():
    new_description = request.form.get('description')
    restaurant_email = session.get('restaurant_email')
    
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE restaurants
        SET caption = ?
        WHERE email = ?
    ''', (new_description, restaurant_email))
    connection.commit()
    connection.close()
    
    flash('Beschreibung erfolgreich aktualisiert!', 'success')
    return redirect(url_for('views.verwaltung'))

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
    price = request.form.get('item_price')
    user_email = session.get('user_email')  # Benutzer-Email aus Session
    restaurant_email = request.form.get("restaurant_email") # Restaurant-Email aus der Seite
    user_address = session.get('user_address')  # Lieferadresse
    user_plz = session.get('user_zip')  # Liefer-PLZ

    # Umwandlung von String in Decimal
    price_decimal = Decimal(price)  

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    #Überprüfen, ob bereits eine Bestellung für den Benutzer existiert
    order_id = session.get('order_id')
    if not order_id:
        #Neue Bestellung Anlegen, da keine vorhanden ist
        cursor.execute('''
                        INSERT INTO orders (user_email, restaurant_email, total_price, delivery_address, delivery_plz, status)
                        VALUES (?, ?, 0, ?, ?, 'new')
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

    # Berechnung des Gesamtpreises
    total_item_price = price_decimal * quantity

    #Gesamtpreis der Bestellung aktualisieren
    cursor.execute('''
                   UPDATE orders
                     SET total_price = total_price + ?
                     WHERE order_id = ?
                     ''', (total_item_price, order_id))
    connection.commit()
    connection.close()

    return redirect(url_for('views.bestellungZusammenstellen', restaurant_email=restaurant_email))

@views.route('/remove_item_order', methods=['POST'])
def remove_item_order():
    item_name = request.form.get("item_name")  # Namen des Items
    remove_count = int(request.form.get("remove_count"))  # Menge
    order_id = session.get('order_id')  # Bestellungs-ID

    connection = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    #Menge des Items holen
    cursor.execute('''
                    SELECT quantity, price
                    FROM order_details
                    WHERE order_id = ? AND item_name = ?
                    ''', (order_id, item_name))
    item_details = cursor.fetchone()


    if item_details:
        current_quantity = item_details[0]
        new_quantity = current_quantity - remove_count
        price_decimal = Decimal(item_details[1]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if new_quantity > 0:

            total_price_to_subtract = price_decimal * remove_count
            total_price_to_subtract = total_price_to_subtract.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            cursor.execute('''
                    UPDATE orders
                    SET total_price = total_price - ?
                    WHERE order_id = ?
                    ''', (total_price_to_subtract, order_id))
            
            cursor.execute('''
                        UPDATE order_details
                        SET quantity = quantity - ?
                        WHERE order_id = ? AND item_name = ?
                        ''', (remove_count, order_id, item_name))

        else:

            total_price_to_subtract = price_decimal * current_quantity
            total_price_to_subtract = total_price_to_subtract.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            cursor.execute('''
                    UPDATE orders
                    SET total_price = total_price - ?
                    WHERE order_id = ?
                    ''', (total_price_to_subtract, order_id))
            cursor.execute('''
                        DELETE FROM order_details
                        WHERE order_id = ? AND item_name = ?
                        ''', (order_id, item_name))

    connection.commit()   
    connection.close()
    return redirect(url_for('views.warenkorb'))

@views.route('/bestellen', methods=['POST'])
def order_comments():
    order_id = session.get('order_id')
    comments = request.form.get('comments')
    user_guthaben = Decimal(session.get('user_guthaben'))

    connection = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    #BeÜberprüfen ob der Kunde genug Geld hat
    cursor.execute('''
                   select total_price
                     from orders
                     where order_id = ?
                     ''', (order_id,))
    order_details = cursor.fetchone()
    total_price = Decimal(order_details[0]) 

    #Bei zu wenig Guthaben wird die Bestellung nicht abgeschickt
    if total_price > user_guthaben:
        flash('Nicht genug Guthaben!', 'danger')
        connection.close()
        return redirect(url_for('views.warenkorb'))
    
    #Bei genug Guthaben wird die Bestellung abgeschickt
    else:
        cursor.execute('''
            UPDATE orders
            SET caption = ?
            WHERE order_id = ?
        ''', (comments, order_id))
        cursor.execute('''
                    UPDATE orders 
                    SET status = 'in Bearbeitung' 
                    WHERE order_id = ?
                    ''', (order_id,))
          
        # Guthaben des Kunden verringern
        cursor.execute('''
            UPDATE users
            SET guthaben = guthaben - ?
            WHERE email = ?
        ''', (total_price, session.get('user_email')))
     
        connection.commit()
        connection.close()

        session['user_guthaben'] = str(user_guthaben - total_price)
        session.pop('order_id', None)   #Damit bei der nächsten Bestellung eine neue Order_id erstellt wird
        flash('Bestellung erfolgreich abgeschickt!', 'success')
        return redirect(url_for('views.homeKunde'))