from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/signUp')
def signUp():
    return render_template('signUp.html')

# @views.route("/signUp", methods=['GET', 'POST'])
# def signUp():
#     if request.method == 'POST':
#         restaurant_name = request.form.get('restaurant_name')
#         username = request.form.get('username')
#         street = request.form.get('street')
#         plz = request.form.get('plz')
#         description = request.form.get('description')
#         picture = request.form.get('picture')
#         password = request.form.get('password')

#     try:
#         # Verbindung zur Datenbank
#         conn = sqlite3.connect("database.db")
#         cursor = conn.cursor()

#         # Nutzer in die Tabelle einfügen
#         cursor.execute("INSERT INTO restaurant_users (restaurant_name, username, street, plz, description, picture, password) VALUES (?, ?, ?)", 
#                        (restaurant_name, username, street, plz, description, picture, password))
#         conn.commit()
#         conn.close()

#         flash("Account erfolgreich erstellt!", "success")
#         return redirect("/login")  # Nach erfolgreicher Registrierung weiterleiten

#     except Exception as e:
#         flash(f"Ein Fehler ist aufgetreten: {e}", "error")
#         return render_template('signUp.html')

# return render_template('signUp.html')

@views.route("/login")
def login():
    return render_template('login.html')

@views.route("/menu")
def menu():
    items = Item.query.all()
    return render_template('menu.html', items=items)

@views.route("/addItem")
def addItem():
    return render_template('addItem.html')
    

