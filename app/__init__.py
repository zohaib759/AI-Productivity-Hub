from flask import Flask ,render_template
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    from app.models import user
    @app.route('/')
    def home():
        return render_template('index.html')
    
    return app