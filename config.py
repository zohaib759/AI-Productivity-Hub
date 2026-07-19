import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(basedir, "instance", "app.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")