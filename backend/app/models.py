"""
Dieses Modul definiert die Datenbankmodelle für die Anwendung.
Es verwendet SQLAlchemy, um die Datenbanktabellen und deren Beziehungen zu definieren.
- `User`: Repräsentiert einen Benutzer der Anwendung.
- `TokenBlacklist`: Speichert ungültige oder revozierte JWT-Tokens, um deren weitere Verwendung zu verhindern.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    Repräsentiert einen Benutzer der Anwendung.
    Enthält grundlegende Informationen wie E-Mail, Passwort (als Hash gespeichert) und Erstellungsdatum.
    """
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID für jeden Benutzer
    email = db.Column(db.String(255), unique=True, nullable=False)  # Eindeutige E-Mail-Adresse
    password = db.Column(db.String(255), nullable=False)  # Passwort-Hash zur sicheren Speicherung
    name = db.Column(db.String(255), nullable=False)  # Name des Benutzers
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Zeitpunkt der Erstellung des Benutzers

class TokenBlacklist(db.Model):
    """
    Speichert ungültige oder revozierte JWT-Tokens.
    Diese Tabelle wird verwendet, um sicherzustellen, dass Tokens, die abgelaufen oder widerrufen wurden,
    nicht mehr verwendet werden können.
    """
    __tablename__ = 'token_blacklist'
    __table_args__ = (
        db.Index('idx_token_blacklist_jti', 'jti'),  # Index für schnelle Suche nach JWT ID
        db.Index('idx_token_blacklist_user', 'user_id'),  # Index für schnelle Suche nach Benutzer-ID
    )

    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID für jeden Blacklist-Eintrag
    jti = db.Column(db.String(36), nullable=False, unique=True, 
                  comment='Eindeutige JWT ID (JWT ID Claim)')  # JWT ID, die das Token eindeutig identifiziert
    token_type = db.Column(db.String(10), nullable=False,
                        comment='Token-Typ: access oder refresh')  # Typ des Tokens (z. B. Access oder Refresh)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), 
                       nullable=False, index=True)  # Verknüpfung mit der Benutzer-ID
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow,
                         comment='Zeitpunkt der Revokation')  # Zeitpunkt, zu dem das Token widerrufen wurde
    expires_at = db.Column(db.DateTime, nullable=False,
                         comment='Geplantes Ablaufdatum des Tokens')  # Ablaufdatum des Tokens
    reason = db.Column(db.String(100), 
                     comment='Grund für Revokation (logout, password_change etc.)')  # Grund für die Revokation

    def __init__(self, jti, token_type, user_id, expires_at, reason=None):
        """
        Initialisiert einen neuen Blacklist-Eintrag.
        :param jti: Eindeutige JWT ID
        :param token_type: Typ des Tokens (z. B. Access oder Refresh)
        :param user_id: ID des Benutzers, dem das Token gehört
        :param expires_at: Ablaufdatum des Tokens
        :param reason: Optionaler Grund für die Revokation
        """
        self.jti = jti
        self.token_type = token_type
        self.user_id = user_id
        self.expires_at = expires_at
        self.reason = reason

    def is_expired(self):
        """
        Prüft, ob der Eintrag abgelaufen ist.
        :return: True, wenn das Token abgelaufen ist, sonst False
        """
        return datetime.utcnow() > self.expires_at

    @classmethod
    def cleanup_expired(cls):
        """
        Löscht abgelaufene Einträge aus der Blacklist.
        Diese Methode wird verwendet, um die Tabelle sauber zu halten und Speicherplatz freizugeben.
        """
        cls.query.filter(cls.expires_at < datetime.utcnow()).delete()
        db.session.commit()
