# Importiere notwendige Module aus der Anwendung und Bibliotheken
from app import create_app, db  # Importiere die create_app-Funktion und das db-Objekt
from app.models import User  # Importiere das User-Modell
from argon2 import PasswordHasher  # Importiere den PasswordHasher für das Passwort-Hashing
import sys  # Importiere das sys-Modul für Kommandozeilenargumente
import os  # Importiere das os-Modul, um mit der Umgebung zu arbeiten

# Hole Umgebungsvariablen, falls sie gesetzt sind. Wenn nicht, verwende die Standardkonfiguration
datenbank_uri = os.environ.get('DATABASE_URL', 'sqlite:///./instance/database.db')

# Konstanten
MINDESTLAENGE_PASSWORT = 12

# Initialisiere den PasswordHasher für sicheres Passwort-Hashing
passwort_hasher = PasswordHasher()

def erstelle_benutzer(email, passwort, name):
    """
    Erstellt einen neuen Benutzer in der Datenbank mit den gegebenen Anmeldeinformationen.

    Args:
        email (str): Die E-Mail-Adresse des neuen Benutzers.
        passwort (str): Das Passwort für den neuen Benutzer.
        name (str): Der Name des neuen Benutzers.

    Raises:
        ValueError: Wenn die E-Mail oder das Passwort ungültig ist.
        Exception: Wenn es ein Problem beim Verbinden oder Modifizieren der Datenbank gibt.
    """
    # Validiere E-Mail, Passwort und Name
    if not email or not isinstance(email, str):
        raise ValueError("Ungültiges E-Mail-Format")
    if not passwort or len(passwort) < MINDESTLAENGE_PASSWORT:
        raise ValueError(f"Passwort muss mindestens {MINDESTLAENGE_PASSWORT} Zeichen lang sein")
    if not name or not isinstance(name, str):
        raise ValueError("Ungültiges Namensformat")
    # Erstelle einen Flask-App-Kontext
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = datenbank_uri
    with app.app_context():
        # Initialisiere die Datenbank, falls sie noch nicht initialisiert wurde.
        if not os.path.exists(app.instance_path + "/database.db"):
            db.init_app(app)
            db.create_all()

        # Prüfe, ob der Benutzer bereits existiert
        existierender_benutzer = User.query.filter_by(email=email).first()
        if existierender_benutzer:
            raise ValueError(f"Benutzer mit E-Mail '{email}' existiert bereits")

        # Hashe das Passwort für sichere Speicherung
        passwort_hash = passwort_hasher.hash(passwort)

        # Erstelle ein neues Benutzer-Objekt
        neuer_benutzer = User(email=email, password=passwort_hash, name=name)

        # Verwende eine Transaktion, um die Datenintegrität sicherzustellen
        try:
            db.session.begin()
            # Füge den Benutzer zur Datenbanksitzung hinzu
            db.session.add(neuer_benutzer)
            # Übertrage die Transaktion
            db.session.commit()
        except Exception as e:
            # Mache ein Rollback im Fehlerfall
            db.session.rollback()
            raise Exception(f"Fehler beim Erstellen des Benutzers: {e}")

        print(f"Benutzer '{name}' mit E-Mail '{email}' erfolgreich erstellt.")


if __name__ == "__main__":
    # Prüfe, ob die korrekte Anzahl von Argumenten angegeben wurde
    if len(sys.argv) != 4:
        print("Verwendung: python create_user.py <email> <passwort> <name>")
        sys.exit(1)  # Beende mit einem Fehlercode

    try:
        # Extrahiere die Benutzerdetails aus den Kommandozeilenargumenten
        email, passwort, name = sys.argv[1], sys.argv[2], sys.argv[3]
        # Erstelle den Benutzer
        erstelle_benutzer(email, passwort, name)
    except ValueError as e:
        print(f"Fehler: {e}")
        sys.exit(1)  # Beende mit einem Fehlercode
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        sys.exit(1)  # Beende mit einem Fehlercode
