from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Importiere und registriere die Routen
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    return app
 