from flask import Flask, request, render_template, Response, redirect, Blueprint, flash, url_for
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
        
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('''
                       select password from users where email = ?
                       ''', (email_eingabe,))
        result = cursor.fetchone()
        connection.close()

        if result and password_eingabe == result[0]:
            flash('Sie sind eingeloggt!', category='success')
            #Sessiondaten für Kunde speichern
            return redirect(url_for('views.homeKunde')) 
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('''
                       select password from restaurants where email = ?
                       ''', (email_eingabe,))
        result = cursor.fetchone()
        connection.close()

        if result and password_eingabe == result[0]:
            flash('Sie sind eingeloggt!', category='success')
            #Sessiondaten für Restaurant speichern
            return redirect(url_for('views.homeRestaurant'))
        
        flash('Ungültige E-Mail oder Passwort. Bitte versuche es erneut.', 'error')

    return render_template("login.html", text="Testing", user="Name", boolean=True)


#@views.route('/logout')
#def logout():
#Um sessiondaten zu löschen und auf die Startseite zu leiten
#Muss für Kunde und Restaurant getrennt implementiert werden
#Wir benutzt pop() um die Sessiondaten zu löschen

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
def homeRestaurant():                                   #Entweder homeRestaurantNeu als ersatz für homeRestaurant und überall einfügen
    return render_template('homeRestaurantNeu.html')    #oder homeRestaurantNeu zu homeRestaurant umbenennen

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

@views.route('/menue')
def menue():
    return render_template("menue.html")

@views.route('/verwaltung')
def verwaltung():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    if request.method == 'POST':
        for day in ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']:
            opening_time = request.form.get(f'{day}_opening_time', '')
            closing_time = request.form.get(f'{day}_closing_time', '')
            restaurant_email = 'restaurant@example.com'  # Beispiel

            # Update der Datenbank für jeden Tag
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
        WHERE restaurant_email = 'restaurant@example.com'
    ''')
    opening_hours = cursor.fetchall()
    connection.close()

    # Umwandeln in ein Wörterbuch
    opening_hours_dict = {day: {'opening_time': opening_time, 'closing_time': closing_time}
                          for day, opening_time, closing_time in opening_hours}

    return render_template('verwaltung.html', opening_hours=opening_hours_dict)