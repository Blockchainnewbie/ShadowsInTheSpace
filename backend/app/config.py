# backend/app/config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env.local file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), '.env.local'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT Konfiguration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['headers', 'cookies']  # Unterstützung für Cookies und Headers
    JWT_COOKIE_SECURE = True  # Nur über HTTPS
    JWT_COOKIE_CSRF_PROTECT = True  # CSRF-Schutz aktivieren
    JWT_CSRF_IN_COOKIES = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 1 Stunde
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 30 Tage
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ERROR_MESSAGE_KEY = 'message'  # Standard-Fehlermeldungsschlüssel
