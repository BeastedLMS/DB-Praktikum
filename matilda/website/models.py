from . import db
from flask_login import UserMixin

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    vorname = db.Column(db.String(150))
    notes = db.relationship('Note')

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    adresse = db.Column(db.String(150))
    stadt = db.Column(db.String(150))
    plz = db.Column(db.Integer)
    password = db.Column(db.String(150))
    beschreibung = db.Column(db.String(10000))



