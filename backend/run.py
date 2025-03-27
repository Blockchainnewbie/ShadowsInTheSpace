# backend/run.py
from app import create_app

# Erstelle die Flask-Anwendung über die Application Factory
app = create_app()

if __name__ == '__main__':
    app.run()
