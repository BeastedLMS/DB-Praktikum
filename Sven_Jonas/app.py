from flask import Flask, request, render_template, Response, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def start_anmeldung():
    return render_template("StartAnmeldung.html")

@app.route('/konto-anlegen-kunde', methods=['GET'])
def konto_anlegen_kunde():
    return render_template("KontoAnlegenKunde.html")

@app.route('/konto-anlegen-restaurant', methods=['GET'])
def konto_anlegen_restaurant():
    return render_template("KontoAnlegenRestaurant.html")

@app.route('/login-kunde', methods=['GET'])
def login_kunde():
    return render_template("LoginKunde.html")

@app.route('/login-restaurant', methods=['GET'])
def login_restaurant():
    return render_template("LoginRestaurant.html")



@app.route('/registerkunde', methods=['GET', 'POST'])
def registerK():
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
                       insert into users (first_name, last_name, email, password, address, city, zip)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       ''', (first_name, last_name, email, password, address, city, zip))
        
        connection.commit()
        connection.close()

    return render_template("KontoAngelegt.html")


@app.route('/registerrestaurant', methods=['GET', 'POST'])
def registerR():
    if request.method == 'POST':

        restaurant_name = request.form["restaurant_name"]
        email = request.form["email"]
        password = request.form["password"]
        address = request.form["address"]
        zip = request.form["zip"]
        caption = request.form["caption"]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('''
                       insert into restaurants (restaurant_name, email, password, address, zip, caption)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ''', (restaurant_name, email, password, address, zip, caption))
        
        connection.commit()
        connection.close()

    return render_template("KontoAngelegt.html")
    

    
    

if __name__ == '__main__':
    app.run(debug=True)