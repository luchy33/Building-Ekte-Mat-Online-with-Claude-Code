import os

from dotenv import load_dotenv

load_dotenv()  # read .env so `python seed.py` gets the same settings as `flask run`


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-not-secret")
    # Relative paths are resolved against the Flask instance folder.
    DATABASE = os.environ.get("DATABASE", "ektemat.sqlite")
    TESTING = False


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test"
