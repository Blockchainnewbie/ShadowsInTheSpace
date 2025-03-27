# backend/app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env.local file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), '.env.local'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')


