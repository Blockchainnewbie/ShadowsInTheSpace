"""
Dieses Modul initialisiert und konfiguriert die Flask-Anwendung für das Backend.
Es enthält die Funktion `create_app`, die die App-Instanz erstellt und konfiguriert.
Die Konfiguration unterscheidet zwischen Entwicklungs- und Produktionsumgebungen.
Zusätzlich werden Erweiterungen wie Flask-Migrate, Flask-CORS und Flask-JWT-Extended initialisiert.
"""

from flask import Flask, logging
from .models import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter # Import Limiter
from flask_limiter.util import get_remote_address # Import get_remote_address

jwt = JWTManager() # Define jwt globally
limiter = Limiter(key_func=get_remote_address) # Define limiter globally

def create_app():
    """
    Erstellt und konfiguriert die Flask-Anwendung.

    Returns:
        Flask: Die konfigurierte Flask-App-Instanz.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
    # Setze die SQLALCHEMY_DATABASE_URI aus der Konfiguration vor der Initialisierung der Datenbank
   
    # Produktionsspezifische Einstellungen für den Hetzner Server
    if app.config.get('ENV') == 'production':
        # Deaktiviere den Debug-Modus in der Produktion
        app.config['DEBUG'] = False
        # Stelle sicher, dass Cookies nur über HTTPS übertragen werden
        app.config['SESSION_COOKIE_SECURE'] = True
        # Erzwinge die Nutzung von HTTPS
        app.config['PREFERRED_URL_SCHEME'] = 'https'
        # Konfiguriere CORS: Erlaube nur Anfragen von einer sicheren, produktionsrelevanten Domain
        allowed_origin = app.config.get('CORS_ORIGIN', 'https://shadowsinthe.space')
        CORS(app, resources={r"/api/*": {"origins": allowed_origin}})
        
        # Richte ein Logging-Handler ein, um Fehler in der Produktion zu protokollieren
        file_handler = logging.FileHandler('error.log')  # Fehler werden in 'error.log' protokolliert
        file_handler.setLevel(logging.ERROR)  # Nur Fehler-Level-Logs werden erfasst
        app.logger.addHandler(file_handler)
    else:
        # Für die Entwicklung: Erlaube CORS von localhost
        CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Initialisiere die Datenbank und binde sie an die App
    db.init_app(app)  # Initialisieren der Datenbank

    # Initialisiere den JWT-Manager mit der App
    jwt.init_app(app)

    # Initialisiere Flask-Migrate zur Verwaltung von Datenbankmigrationen
    migrate = Migrate(app, db)

    # Importiere und registriere Blueprints und initialisiere Erweiterungen im App-Kontext
    with app.app_context():
        from .routes import auth_bp
        limiter.init_app(app) # Initialize limiter here
        app.register_blueprint(auth_bp)

    # Gib die vollständig konfigurierte App-Instanz zurück
    return app
