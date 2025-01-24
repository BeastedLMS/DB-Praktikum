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

        email_eingabe = request.form.get['email']
        password_eingabe = request.form.get['password']
        
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute('''
                       select password from users where email = ?
                       ''', (email_eingabe))
        password = cursor.fetchall()

        if password_eingabe == password:
            flash('Sie sind eingeloggt!', category='success')
            return redirect(url_for('')) #Route zur Hauptseite des Kunden einfügen

        cursor.execute('''
                       select password from restaurants where email = ?
                       ''', (email_eingabe))
        password = cursor.fetchall()

        if password_eingabe == password:
            flash('Sie sind eingeloggt!', category='success')
            return redirect(url_for('')) #Route zur Hauptseite des Restaurants einfügen
        
    return render_template("login.html", text="Testing", user="Name", boolean=True)