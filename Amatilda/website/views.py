# storing routes here
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/') #main page is just /
def home():
    return render_template("home.html")