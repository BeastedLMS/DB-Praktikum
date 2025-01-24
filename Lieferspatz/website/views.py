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
            return redirect(url_for('views.homeKunde')) #Route zur Hauptseite des Kunden einfügen

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('''
                       select password from restaurants where email = ?
                       ''', (email_eingabe,))
        result = cursor.fetchone()
        connection.close()

        if result and password_eingabe == result[0]:
            flash('Sie sind eingeloggt!', category='success')
            return redirect(url_for('views.homeRestaurant')) #Route zur Hauptseite des Restaurants einfügen
        
        flash('Ungültige E-Mail oder Passwort. Bitte versuche es erneut.', 'error')

    return render_template("login.html", text="Testing", user="Name", boolean=True)


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
                       ''', (restaurant_name, email, password, address, city, zip, caption, bild, 100))
        
        connection.commit()
        connection.close()
        flash('Sie haben sich erfolgreich registriert!', category='success')
        return redirect(url_for("views.homeRestaurant"))
    
    return render_template("signupGeschaeft.html")

@views.route('/homeRestaurant')
def homeRestaurant():
    return render_template('homeRestaurant.html')

@views.route('/homeKunde')
def homeKunde():
    restaurantListe =[{"name": "Dui Sushi", 
                       "beschreibung": "Leckeres Sushi", 
                       "adresse": "Moltkestraße 1", 
                       "stadt": "Essen",
                       "plz": "45128"}, 
                       {"name": "Pizzeria Märchenwald Holsterhausen", 
                        "beschreibung": "Köstliche Pizza", 
                        "adresse": "Kaulbachstraße 61", 
                        "stadt": "Essen",
                        "plz": "45147"},
                        {"name": "Falafel Haus", 
                        "beschreibung": "Super Falafel", 
                        "adresse": "Altenessener Straße 387", 
                        "stadt": "Essen",
                        "plz": "45326"}]
    return render_template("homeKunde.html", restaurants=restaurantListe)

