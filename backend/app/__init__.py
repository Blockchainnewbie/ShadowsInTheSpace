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
from .config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    """
    Erstellt und konfiguriert die Flask-Anwendung.

    Returns:
        Flask: Die konfigurierte Flask-App-Instanz.
    """
    app = Flask(__name__)

    # Configure CORS
    CORS(app, resources={r"/api/*": {                                           
        
    # Get Config from Config Class                                               
        "origins": ["http://localhost:5173", "https://shadowsinthe.space"],
        "supports_credentials": True
    }})

    app.config.from_object(Config)

    # Initialisiere die Datenbank und binde sie an die App
    db.init_app(app)
    
    # Initialisiere den JWT-Manager mit der App
    jwt.init_app(app)

    # Initialisiere Flask-Migrate zur Verwaltung von Datenbankmigrationen
    Migrate(app, db)

    # Import and register Blueprints and initialize extensions in the app context
    from .routes import auth_bp, main_bp
    limiter.init_app(app)  # Initialize limiter here
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # return the fully configured app instance
    return app

