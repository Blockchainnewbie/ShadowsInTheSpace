# backend/app/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Passwort-Hash speichern
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TokenBlacklist(db.Model):
    """Speichert ungültige/revozierte JWT-Tokens zur Blacklist-Prüfung"""
    __tablename__ = 'token_blacklist'
    __table_args__ = (
        db.Index('idx_token_blacklist_jti', 'jti'),
        db.Index('idx_token_blacklist_user', 'user_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True, 
                  comment='Eindeutige JWT ID (JWT ID Claim)')
    token_type = db.Column(db.String(10), nullable=False,
                        comment='Token-Typ: access oder refresh')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), 
                       nullable=False, index=True)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow,
                         comment='Zeitpunkt der Revokation')
    expires_at = db.Column(db.DateTime, nullable=False,
                         comment='Geplantes Ablaufdatum des Tokens')
    reason = db.Column(db.String(100), 
                     comment='Grund für Revokation (logout, password_change etc.)')

    def __init__(self, jti, token_type, user_id, expires_at, reason=None):
        """Initialisiert einen neuen Blacklist-Eintrag"""
        self.jti = jti
        self.token_type = token_type
        self.user_id = user_id
        self.expires_at = expires_at
        self.reason = reason

    def is_expired(self):
        """Prüft ob der Eintrag abgelaufen ist"""
        return datetime.utcnow() > self.expires_at

    @classmethod
    def cleanup_expired(cls):
        """Löscht abgelaufene Einträge aus der Blacklist"""
        cls.query.filter(cls.expires_at < datetime.utcnow()).delete()
        db.session.commit()
