"""
Diese Datei enthält die Konfigurationseinstellungen für die Anwendung.
Die Konfiguration umfasst:
- Geheimschlüssel für die Anwendung und JWT-Token
- Datenbankverbindungsdetails
- JWT-spezifische Einstellungen wie Token-Ablaufzeiten, Speicherorte und Sicherheitsmaßnahmen
- Aktivierung der Blacklist-Funktionalität für Token

Die Umgebungsvariablen werden aus einer .env.local-Datei geladen, 
die sich im übergeordneten Verzeichnis befindet. Diese Datei sollte 
sensible Informationen wie Schlüssel und Datenbank-URIs enthalten.
"""

# backend/app/config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der Datei .env.local
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), '.env.local'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # Geheimschlüssel für die Anwendung (z. B. für Sitzungen)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    
    # Deaktiviert die Nachverfolgung von Änderungen in SQLAlchemy (spart Ressourcen)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT-Konfiguration
    # Geheimschlüssel für die JWT-Token-Signierung
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    # Gibt an, wo JWT-Token gespeichert werden (Header und Cookies)
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    
    # Aktiviert die sichere Übertragung von Cookies nur über HTTPS
    JWT_COOKIE_SECURE = True
    
    # Aktiviert den CSRF-Schutz für Cookies
    JWT_COOKIE_CSRF_PROTECT = True
    
    # Speichert CSRF-Token in Cookies
    JWT_CSRF_IN_COOKIES = True
    
    # Ablaufzeit für Zugriffstoken (1 Stunde)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Ablaufzeit für Refresh-Token (30 Tage)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Aktiviert die Blacklist-Funktionalität für JWT-Token
    JWT_BLACKLIST_ENABLED = True
    
    # Gibt an, welche Token-Typen (Zugriff und Refresh) auf der Blacklist überprüft werden
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # Schlüsselname für Fehlermeldungen in JWT-Antworten
    JWT_ERROR_MESSAGE_KEY = 'message'
