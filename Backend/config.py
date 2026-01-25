import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "dev-secret-key"
    DATABASE_PATH = os.path.join(BASE_DIR, "instance", "app.db")
    DEBUG = True
