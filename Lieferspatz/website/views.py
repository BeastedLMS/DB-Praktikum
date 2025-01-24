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
            return redirect(url_for('views.restaurants')) #Route zur Hauptseite des Kunden einfügen

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('''
                       select password from restaurants where email = ?
                       ''', (email_eingabe,))
        result = cursor.fetchone()
        connection.close()

        if result and password_eingabe == result[0]:
            flash('Sie sind eingeloggt!', category='success')
            return redirect(url_for('')) #Route zur Hauptseite des Restaurants einfügen
        
        flash('Ungültige E-Mail oder Passwort. Bitte versuche es erneut.', 'error')

    return render_template("login.html", text="Testing", user="Name", boolean=True)


@views.route('/signupKunde', methods=['GET', 'POST'])
def signupKunde():
    if request.method == 'POST':

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        address = request.form["address"]
        city = request.form["city"]
        zip = request.form["zip"]

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

@views.route('/restaurants')
def restaurants():
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
    return render_template("restaurants.html", restaurants=restaurantListe)

