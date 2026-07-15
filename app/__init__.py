from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from config import Config
from flask_login import login_required, current_user
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return db.session.get(User, int(user_id))
    

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    from app.notes import notes
    app.register_blueprint(notes)
    from app.auth import auth
    app.register_blueprint(auth)
    from app.dashboard import dashboard
    app.register_blueprint(dashboard)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app