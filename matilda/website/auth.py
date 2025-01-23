from flask import Blueprint, render_template, request, flash, redirect, url_for #???
from .models import User, Restaurant
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/bestellen', methods=['GET', 'POST'])
def bestellen():
    
    itemListe = [('Insalata al Formaggio di Pecora',
              'gebackener Hirtenkäse auf Tomate-Rucola', 
              '9,50'),
             ('Insalata al Filetto di Manzo',
              'gebratene, argentinische Rinderfiletspitzen mit Rucola, Champignons und Cherrytomaten',
              '11,50'), 
              ('Insalata ai Gamberoni',
               'gemischter Salat mit gebratenen Black Tiger Garnelen',
               '10,50')]

    return render_template("bestellungZusammenstellen.html", items=itemListe)

@auth.route('/bestellhistorie')
def bestellhistorie():
    return render_template("bestellhistorie.html")

@auth.route('/restaurants')
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

@auth.route('/warenkorb', methods=['GET', 'POST'])
def warenkorb():
    if request.method == 'POST':
        flash('Ihre Bestellung wurde aufgegeben!', category='success')
        return redirect(url_for('auth.restaurants')) 
    return render_template("warenkorb.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
 #data = request.form
 # #print(data)
 if request.method == 'POST':
    password = request.form.get('password')
    email = request.form.get('email')

    if password == 'einloggen':
        flash('Sie sind eingeloggt!', category='success')
        return redirect(url_for('auth.restaurants'))

    elif password == 'existiert':
        flash('Dieser Account existiert nicht.', category='error')

    elif password == 'falsch':
        flash('Geben Sie bitte das richtige Passwort an.', category='error')
    
    return redirect(url_for('views.home')) 

    
    # user = User.query.filter_by(email=email).first
    # geschaeft = Restaurant.query.filter_by(email=email).first

    # if geschaeft:
    #     if geschaeft.password == password:
    #         flash('Sie sind eingeloggt!', category='success')
    #     else:
    #         flash('Geben Sie bitte das richtige Passwort an.', category='error')

    # if user:
    #     if check_password_hash(user.password, password):
    #         flash('Sie sind eingeloggt!', category='success')
    #     else:
    #         flash('Geben Sie bitte das richtige Passwort an.', category='error')


    
    # else:
    #     flash('Dieser Account existiert nicht.', category='error')

    # if (user and check_password_hash(user.password, password) or (geschaeft and (geschaeft.password == password))):
    #     flash('Sie sind eingeloggt!', category='success')
    # elif user or geschaeft:
    #     flash('Geben Sie bitte das richtige Passwort an.', category='error')
    # else:
    #     flash('Geben Sie bitte das richtige Passwort an.', category='error')



    
 return render_template("login.html", text="Testing", user="Name", boolean=True)

@auth.route('/logout')
def logout():
    flash('Sie wurden ausgeloggt!', category='success')
    return render_template("home.html")

@auth.route('/signupKunde', methods=['GET', 'POST'])
def signupKunde():
    if request.method == 'POST':
        email = request.form.get('email')
        vorname = request.form.get("vorname")
        password = request.form.get("passwort")
        
        user = User.query.filter_by(email=email).first
        if user:
            flash('Dieses Konto existiert bereits. Melden sie sich bitte an.', category='error')


        elif len(email) < 4:
            flash('Bitte gültige Email Adresse eingeben.', category='error')
        elif len(vorname) < 2:
            flash('Bitte gültigen Namen eingeben.', category='error')
        elif len(password) < 7:
            flash('Das Passwort muss länger als 6 Zeichen sein.', category='error')
        else:
            #add user to database
            new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), vorname=vorname)
            db.session.add(new_user)
            db.session.commit()
            flash('Der Account wurde erstellt!', category='success')
            return redirect(url_for('views.home')) 
        
    return render_template("signupKunde.html")

@auth.route('/signupGeschaeft', methods=['GET', 'POST'])
def signupGeschaeft():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get("name")
        password = request.form.get("passwort")
        adresse = request.form.get("adresse")
        stadt = request.form.get("stadt")
        plz = request.form.get("plz")
        bild = request.form.get("datei")
        beschreibung = request.form.get("beschreibung")

        geschaeft = Restaurant.query.filter_by(email=email).first
        if geschaeft:
            flash('Dieses Konto existiert bereits. Melden sie sich bitte an.', category='error')

        elif len(email) < 4:
            flash('Bitte gültige Email Adresse eingeben.', category='error')
        elif len(name) < 2:
            flash('Bitte gültigen Namen eingeben.', category='error')
        elif len(password) < 7:
            flash('Das Passwort muss länger als 6 Zeichen sein.', category='error')
        else:
            #add user to database
             newRestaurant = Restaurant(email=email, name=name, adresse=adresse, stadt=stadt, plz=plz,  password=password, beschreibung=beschreibung)            
             db.session.add(newRestaurant)
             db.session.commit()
             flash('Der Account wurde erstellt!', category='success')
             #return redirect(url_for('views.home')) 
             return render_template("bestellungZusammenstellen.html", Restaurantname=name, Adresse=adresse, Stadt=stadt, postLeihZahl=plz, Beschreibung=beschreibung)   

    return render_template("signupGeschaeft.html")
