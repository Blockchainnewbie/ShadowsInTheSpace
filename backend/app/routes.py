# backend/app/routes.py
import traceback # Add traceback import
import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    verify_jwt_in_request
)

import re
from sqlalchemy.exc import SQLAlchemyError
# Remove local Limiter import and initialization below
from argon2 import PasswordHasher, exceptions  # noqa: F401
from .models import db, User, TokenBlacklist
from datetime import datetime, timedelta
from . import jwt, limiter # Import jwt and limiter from __init__

ph = PasswordHasher(
    time_cost=3,       # Erhöht die CPU-Kosten
    memory_cost=65536, # 64MB Speicher
    parallelism=4,     # Anzahl der Threads
    hash_len=32,       # Länge des Hash
    salt_len=16        # Länge des Salts
)

# JWT Callbacks
# Limiter initialization is removed as it's now done in __init__.py
@jwt.token_in_blocklist_loader
def check_if_token_revoked(_jwt_header, jwt_payload):
    """Checks if the JWT token is present in the blacklist."""
    jti = jwt_payload['jti']
    token = TokenBlacklist.query.filter((TokenBlacklist.jti == jti)).first()
    return token is not None

# Blueprint für Authentifizierungs-Routen
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute", error_message="Zu viele Anmeldeversuche. Bitte versuchen Sie es in einer Minute erneut.")
def login():
    """
    Authentifizierung eines Nutzers.
    Erwartet JSON-Daten: { 
        "email": "gültige@email.de", 
        "password": "SicheresPasswort123" 
    }
    
    Sicherheitsmaßnahmen:
    - Rate-Limiting (5 Versuche pro Minute)
    - Argon2id Passwort-Hashing
    - HTTP-Only Cookies für Tokens
    - Konsistente Fehlermeldungen
    """
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({
            "message": "E-Mail und Passwort erforderlich",
            "details": {
                "required_fields": ["email", "password"]
            }
        }), 400

    email = data['email'].strip().lower()
    password = data['password'].strip()

    # E-Mail Validierung
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return jsonify({
            "message": "Ungültige E-Mail-Adresse",
            "details": {
                "expected_format": "user@example.com"
            }
        }), 400

    # Grundlegende Passwortvalidierung
    if len(password) < 12:
        return jsonify({
            "message": "Ungültige Anmeldedaten",
            "details": {
                "hint": "Passwort muss mindestens 12 Zeichen lang sein"
            }
        }), 401

    try:
        # Suche Nutzer in der Datenbank
        user = User.query.filter_by(email=email).first()
        if not user:
            # Konsistente Fehlermeldung auch bei nicht existierendem Nutzer
            return jsonify({
                "message": "Ungültige Anmeldedaten",
                "details": {
                    "hint": "E-Mail oder Passwort falsch",
                    "attempted_email": email,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }), 401

        # Überprüfe Passwort-Hash mit Argon2id
        try:
            ph.verify(user.password, password)
        except exceptions.VerifyMismatchError:
            # Logge fehlgeschlagene Anmeldeversuche
            return jsonify({
                "message": "Ungültige Anmeldedaten",
                "details": {
                    "hint": "E-Mail oder Passwort falsch",
                    "attempted_email": email,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }), 401

        # Erstelle neue Tokens
        access_token = create_access_token(identity=str(user.id), additional_claims={"token_type": "access"})
        refresh_token_jti = str(uuid.uuid4())
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims={"token_type": "refresh", "jti": refresh_token_jti})
        now = datetime.utcnow()


        try:
            # Save the refresh token in the database
            db.session.add(TokenBlacklist(
                jti=refresh_token_jti,
                token_type='refresh',
                user_id=user.id,
                expires_at=now + timedelta(days=7),
                reason='login'
            ))    
            # Update last_login timestamp
            user.last_login = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
        response = jsonify({
            "message": "Erfolgreich angemeldet",
            "user_id": str(user.id),
            "details": {
                "email": user.email,
                "name": user.name,
                "last_login": user.last_login.isoformat(),
                "token_expires": "15 Minuten",
                "refresh_token_expires": "7 Tage"
            }
        })
        
        # Setze sichere HTTP-Only Cookies
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)


        return response, 200

    except Exception as e:
        traceback.print_exc() # Print the full traceback to the console
        return jsonify({
            "message": "Fehler bei der Anmeldung",
            "error": str(e),
            "details": {
                "hint": "Bitte versuchen Sie es später erneut",
                "error_type": "database_error" if isinstance(e, SQLAlchemyError) else "server_error",
                "timestamp": datetime.utcnow().isoformat()
            }
        }), 500

@auth_bp.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Abmeldung eines Nutzers.
    Invalidiert die aktuellen Tokens und löscht Cookies.
    
    Sicherheitsmaßnahmen:
    - Access Token wird in Blacklist eingetragen (1 Stunde gültig)
    - Refresh Token wird in Blacklist eingetragen (30 Tage gültig)
    - HTTP-Only Cookies werden gelöscht
    - Transaktionssicherheit für Datenbankoperationen
    """
    try:
        # Erfasse Metadaten für Logging
        user_id = get_jwt_identity()
        now = datetime.utcnow()
        access_jti = get_jwt()['jti']
        
        # Starte Transaktion für Token-Blacklisting
        db.session.begin()
        
        # Blacklist Access Token
        db.session.add(TokenBlacklist( 
            jti=access_jti, 
            token_type='access', 
            user_id=user_id, 
            expires_at=now + timedelta(minutes=15), 
            reason='logout', 
            
            created_at=now
        ))

        # Blacklist Refresh Token falls vorhanden
        refresh_jti = None
        try:
            verify_jwt_in_request(refresh=True)
            refresh_jti = get_jwt()['jti']
            db.session.add(TokenBlacklist(
                jti=refresh_jti,
                token_type='refresh',
                user_id=user_id,
                expires_at=now + timedelta(days=30),
                reason='logout',
                created_at=now
            ))
        except:
            pass  # Kein Refresh Token vorhanden
        
        # Führe alle Datenbankoperationen in einer Transaktion durch
        db.session.commit()
        
        # Erstelle Response mit Cookie-Löschung
        response = jsonify({
            "message": "Erfolgreich abgemeldet",
            "user_id": user_id,
            "details": {
                "invalidated_tokens": {
                    "access_token": access_jti,
                    "refresh_token": refresh_jti or "none"
                },
                "logout_time": now.isoformat(),
                "access_token_expires": "1 Stunde",
                "refresh_token_expires": "30 Tage" if refresh_jti else "none"
            }
        })
        
        # Lösche alle JWT Cookies
        unset_jwt_cookies(response)
        return response, 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Fehler bei der Abmeldung",
            "error": str(e),
            "details": {
                "hint": "Bitte versuchen Sie es erneut oder melden Sie sich manuell ab",
                "error_type": "database_error" if isinstance(e, SQLAlchemyError) else "server_error",
                "timestamp": now.isoformat()
            }
        }), 500

@auth_bp.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
@limiter.limit("10 per minute", error_message="Zu viele Token-Aktualisierungen. Bitte versuchen Sie es in einer Minute erneut.")
def refresh():
    """
    Aktualisierung des Access Tokens mit einem gültigen Refresh Token.
    
    Sicherheitsmaßnahmen:
    - Rate-Limiting (10 Anfragen pro Minute)
    - Nur gültige Refresh Tokens werden akzeptiert
    - HTTP-Only Cookies für neuen Access Token
    - Konsistente Fehlermeldungen
    
    Anforderungen:
    - Gültiger Refresh Token im Cookie oder Authorization Header
    """
    try:
        # Identität aus Refresh Token extrahieren
        identity = get_jwt_identity()
        now = datetime.utcnow()
        refresh_jti = get_jwt()['jti']
        
        # Prüfe ob Refresh Token in Blacklist
        if TokenBlacklist.query.filter_by(jti=refresh_jti,token_type='refresh').first():
            return jsonify({
                "message": "Ungültiger Refresh Token",
                "details": {
                    "hint": "Token wurde widerrufen",
                    "token_id": refresh_jti,
                    "timestamp": now.isoformat(),
                }
            }), 401

        # Erstelle neuen Access Token
        access_token = create_access_token(identity=identity)
        
        response = jsonify({
            "message": "Token erfolgreich aktualisiert",
            "token": access_token,
            "details": {
                "expires_in": "15 Minuten",
                "token_type": "Bearer",
                "refresh_token_id": refresh_jti,
                "timestamp": now.isoformat()
            }
        })
        
        # Setze neuen Access Token als HTTP-Only Cookie
        set_access_cookies(response, access_token)
        return response, 200
        
    except Exception as e:
        return jsonify({
            "message": "Fehler bei der Token-Aktualisierung",
            "error": str(e),
            "details": {
                "hint": "Bitte melden Sie sich erneut an",
                "error_type": "database_error" if isinstance(e, SQLAlchemyError) else "server_error",
                "timestamp": datetime.utcnow().isoformat()
            }
        }), 500

@auth_bp.route('/api/register', methods=['POST'])
@limiter.limit("3 per minute", error_message="Zu viele Registrierungsversuche. Bitte versuchen Sie es in einer Minute erneut.")
def register():
    """
    Registrierung eines neuen Nutzers.
    Erwartet JSON-Daten: { 
        "email": "gültige@email.de", 
        "password": "SicheresPasswort123", 
        "name": "Max Mustermann" 
    }
    
    Sicherheitsmaßnahmen:
    - Rate-Limiting (3 Anfragen pro Minute)
    - Argon2id Passwort-Hashing
    - Strikte E-Mail-Validierung
    - Strenge Passwortanforderungen:
      - Mindestens 12 Zeichen
      - Groß- und Kleinbuchstaben
      - Zahlen und Sonderzeichen
    - HTTP-Only Cookies für automatische Anmeldung
    - Transaktionssicherheit
    
    Rückgabewerte:
    - 201 Created bei Erfolg
    - 400 Bad Request bei ungültigen Daten
    - 409 Conflict bei existierendem Nutzer
    - 500 Internal Server Error bei technischen Fehlern
    """
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({
            "message": "Alle Felder sind erforderlich",
            "details": {
                "required_fields": ["email", "password", "name"]
            }
        }), 400

    email = data['email'].strip().lower()
    password = data['password'].strip()
    name = data['name'].strip()

    # E-Mail Validierung
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return jsonify({
            "message": "Ungültige E-Mail-Adresse",
            "details": {
                "expected_format": "user@example.com"
            }
        }), 400

    # Name Validierung
    if len(name) < 2:
        return jsonify({
            "message": "Name muss mindestens 2 Zeichen lang sein"
        }), 400

    # Erweiterte Passwort Validierung
    if len(password) < 12:
        return jsonify({
            "message": "Passwort muss mindestens 12 Zeichen lang sein"
        }), 400
    if not any(c.isupper() for c in password):
        return jsonify({
            "message": "Passwort muss mindestens einen Großbuchstaben enthalten"
        }), 400
    if not any(c.islower() for c in password):
        return jsonify({
            "message": "Passwort muss mindestens einen Kleinbuchstaben enthalten"
        }), 400
    if not any(c.isdigit() for c in password):
        return jsonify({
            "message": "Passwort muss mindestens eine Zahl enthalten"
        }), 400
    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for c in password):
        return jsonify({
            "message": "Passwort muss mindestens ein Sonderzeichen enthalten"
        }), 400

    # Prüfe, ob der Nutzer bereits existiert
    if User.query.filter_by(email=email).first():
        return jsonify({
            "message": "Nutzer existiert bereits",
            "details": {
                "email": email
            }
        }), 409  # 409 Conflict

    try:
        now = datetime.utcnow()
        
        # Erzeuge einen sicheren Passwort-Hash mit Argon2id
        password_hash = ph.hash(password)
        
        # Erstelle ein neues User-Objekt
        new_user = User(
            email=email, 
            password=password_hash, 
            name=name,
            created_at=now,
            last_login=now
        )
        
        # Führe alle Datenbankoperationen in einer Transaktion durch
        db.session.begin()
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
        # Erstelle Tokens für automatische Anmeldung
        access_token = create_access_token(identity=str(new_user.id), additional_claims={"token_type": "access"})
        refresh_token_jti = str(uuid.uuid4())
        refresh_token = create_refresh_token(identity=str(new_user.id), additional_claims={"token_type": "refresh", "jti": refresh_token_jti})
        db.session.commit()
        response = jsonify({
            "message": "Benutzer erfolgreich registriert",
            "user_id": str(new_user.id),
            "token": access_token,
            "refresh_token": refresh_token,
            "details": {
                "email": email,
                "name": name,
                "created_at": now.isoformat(),
                "last_login": now.isoformat(),
                "token_expires": "15 Minuten",
                "refresh_token_expires": "7 Tage",
                "refresh_token_id": refresh_token_jti,
                "timestamp": now.isoformat()
            }
        })
        
        # Setze sichere HTTP-Only Cookies
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Fehler bei der Registrierung",
            "error": str(e),
            "details": {
                "hint": "Bitte überprüfen Sie die Eingabedaten und versuchen Sie es erneut",
                "error_type": "database_error" if isinstance(e, SQLAlchemyError) else "server_error",
                "timestamp": datetime.utcnow().isoformat()
            }
        }), 500

# Hier kommt unser geschützter Endpoint
@auth_bp.route('/api/protected', methods=['GET'])
@jwt_required()  # Diese Dekoration stellt sicher, dass nur Anfragen mit gültigem JWT zugelassen werden
def protected():
    current_user_id = get_jwt_identity()  # Extrahiert die User-ID aus dem Token
    return jsonify({
        "message": f"Hallo, Benutzer {current_user_id}! Du hast Zugriff auf diese geschützte Route."
    }), 200

# Blueprint für allgemeine Routen
main_bp = Blueprint('main', __name__)

@main_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Einfacher Health-Check Endpoint zur Überprüfung, ob die API läuft.
    """
    return jsonify({
        "status": "ok",
        "message": "Der Server läuft",
        "timestamp": datetime.utcnow().isoformat()
    }), 200