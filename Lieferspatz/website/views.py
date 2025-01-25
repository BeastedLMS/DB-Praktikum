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

@views.route('/homeRestaurantNeu')
def homeRestaurant():                                   
    return render_template('homeRestaurantNeu.html')

@views.route('/homeKunde')
def homeKunde():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''
                   SELECT restaurant_name, caption, address, city, zip FROM restaurants
                   ''')
    restaurantListe = cursor.fetchall()
    connection.close()

    restaurants = [{"name": row[0], "beschreibung": row[1], "adresse": row[2], "stadt": row[3], "plz": row[4]} for row in restaurantListe]

    return render_template("homeKunde.html", restaurants=restaurants)

@views.route('bestellen')
def bestellungZusammenstellen():
    return render_template("bestellungZusammenstellen.html")

@views.route('/bestellhistorie')
def bestellhistorie():
    return render_template("bestellhistorie.html")

@views.route('/warenkorb')
def warenkorb():
    return render_template("warenkorb.html")

@views.route('/menue', methods=['GET', 'POST'])
def menue():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        name = request.form.get('name')
        price = request.form.get('price')
        restaurant_email = session.get('restaurant_email')

        if item_id:  # Vorhandenen Artikel aktualisieren
            cursor.execute('''
                           UPDATE menue
                           SET item_name = ?, price = ?
                           WHERE item_id = ? AND restaurant_email = ?
                           ''', (name, price, item_id, restaurant_email))
        else:  # Neuen Artikel hinzufügen
            cursor.execute('''
                           INSERT INTO menue (item_name, price, restaurant_email)
                           VALUES (?, ?, ?)
                           ''', (name, price, restaurant_email))

        connection.commit()

    cursor.execute('''
                   SELECT item_id, item_name, price FROM menue WHERE restaurant_email = ?
                   ''', (session.get('restaurant_email'),))
    items = cursor.fetchall()
    connection.close()

    menu_items = [{"id": row[0], "name": row[1], "price": row[2]} for row in items]

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

    return render_template('verwaltung.html', opening_hours=opening_hours_dict)


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
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
                        INSERT INTO delivery_areas (restaurant_email, zip)
                        VALUES (?, ?)
                        ''', (restaurant_email, plz))
        connection.commit()
        connection.close()
        return redirect(url_for('views.verwaltung'))
    
@app.route('/delete_plz/<int:area_id>', methods=['POST'])
def delete_plz(area_id):
    if request.method == 'POST':
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
                        DELETE FROM delivery_areas
                        WHERE da_id = ?
                        ''', (area_id,))
        connection.commit()
        connection.close()
        return redirect(url_for('views.verwaltung'))
    
@views.route('/show_delivery_area')
def show_delivery_area():
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute('''
                            SELECT da_id, zip
                            FROM delivery_areas
                            WHERE restaurant_email = ?
                            ''', (session.get('restaurant_email'),))
            areas = cursor.fetchall()
            connection.close()
            return render_template('verwaltung.html', areas=areas)