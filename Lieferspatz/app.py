from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template("KontoAnlegen.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        address = request.form["address"]
        city = request.form["city"]
        zip = request.form["zip"]

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.executemany('''
                       insert into users (first_name, last_name, email, password, address, city, zip)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       '''), (first_name, last_name, email, password, address, city, zip)
        
        connection.commit()
        connection.close()

        return "Sie sind nun ein glückliches Mitlgied, welches sich Essen bestellen kann"
    

    
    

if __name__ == '__main__':
    app.run(debug=True)