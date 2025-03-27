# backend/app/routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from .models import db, User

# Blueprint für Authentifizierungs-Routen
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    # Lese die JSON-Daten aus der Anfrage (z.B. { "email": "user@example.com", "password": "geheim" })
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "E-Mail und Passwort erforderlich"}), 400

    email = data['email']
    password = data['password']

    # SQLAlchemy verwendet intern Prepared Statements, was SQL-Injections verhindert.
    # So wird hier nach einem Nutzer mit der angegebenen E-Mail gesucht:
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Ungültige Anmeldedaten"}), 401

    # Überprüfe, ob das übermittelte Passwort zum gespeicherten Passwort-Hash passt.
    # Hier kommt werkzeug.security.check_password_hash zum Einsatz:
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Ungültige Anmeldedaten"}), 401

    # Bei korrekter Authentifizierung wird ein JWT-Token erstellt.
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"token": access_token}), 200

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """
    Registrierung eines neuen Nutzers.
    Erwartet JSON-Daten: { "email": "...", "password": "...", "name": "..." }
    """
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({"message": "Alle Felder (email, password, name) sind erforderlich"}), 400

    email = data['email']
    password = data['password']
    name = data['name']

    # Prüfe, ob der Nutzer bereits existiert
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Nutzer existiert bereits"}), 400

    # Erzeuge einen sicheren Passwort-Hash mit werkzeug.security.generate_password_hash.
    password_hash = generate_password_hash(password)
    
    # Erstelle ein neues User-Objekt und füge es der Datenbank hinzu.
    new_user = User(email=email, password=password_hash, name=name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Benutzer erfolgreich registriert"}), 201

# Hier kommt unser geschützter Endpoint
@auth_bp.route('/api/protected', methods=['GET'])
@jwt_required()  # Diese Dekoration stellt sicher, dass nur Anfragen mit gültigem JWT zugelassen werden
def protected():
    current_user_id = get_jwt_identity()  # Extrahiert die User-ID aus dem Token
    return jsonify({
        "message": f"Hallo, Benutzer {current_user_id}! Du hast Zugriff auf diese geschützte Route."
    }), 200
