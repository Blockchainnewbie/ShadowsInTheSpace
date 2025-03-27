# backend/app/__init__.py
from flask import Flask, logging
from .config import Config
from .models import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # Importiere Flask-Migrate
from flask_cors import CORS # Importiere Flask-CORS

def create_app():
    app = Flask(__name__)
    # Lade die Konfiguration aus der Config-Klasse
    app.config.from_object(Config)

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
        file_handler = logging.FileHandler('error.log')
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)
    else:
        # Für die Entwicklung: Erlaube CORS von localhost
        CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Initialisiere die Datenbank und binde sie an die App
    db.init_app(app)

    # Initialisiere den JWT-Manager zur Handhabung von JSON Web Tokens
    jwt = JWTManager(app)

    # Initialisiere Flask-Migrate zur Verwaltung von Datenbankmigrationen
    migrate = Migrate(app, db)

    # Importiere und registriere den Blueprint zur Modularisierung der API-Routen (z.B. Authentifizierung)
    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    # Gib die vollständig konfigurierte App-Instanz zurück
    return app
