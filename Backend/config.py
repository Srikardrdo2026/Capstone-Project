import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = BASE_DIR  # backend directory

class Config:
    DATABASE_PATH = os.path.join(PROJECT_ROOT, "instance", "app.db")
