from flask import Flask, request, render_template, Response, redirect
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    #Hier wird auf die Main Seite verwiesen
    return render_template("KontoAnlegenKunde.html")

#Verweis von Main auf KontoAnlegen, sowohl Kunde als auch Restaurants, muss noch hierhin

@app.route('/', methods=['GET', 'POST'])
def registerR():
    
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

        return Response("Sie sind nun ein glückliches Mitlgied, welches sich Essen bestellen kann")
    
    

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

        return Response("Sie sind nun ein glückliches Mitlgied, welches sich Essen bestellen kann")
    

    
    

if __name__ == '__main__':
    app.run(debug=True)