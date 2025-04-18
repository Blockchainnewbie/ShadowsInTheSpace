import os
from app import create_app
from app import db
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# Create a Flask app instance to access configuration before create_app()
app = Flask(__name__)
app.config.from_object('app.config.Config')
app = create_app()

# It's generally better practice to let Flask-Migrate handle table creation,
# but this ensures tables exist if migrations haven't run.
# Consider removing if you consistently use migrations.
with app.app_context():
    db.create_all() 

if __name__ == "__main__":
    app.run()
