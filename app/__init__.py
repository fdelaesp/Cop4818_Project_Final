from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints
    from .auth import auth_bp
    from .main import main_bp
    from .analytics import analytics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(analytics_bp)

    # CLI ‑> flask create-db
    @app.cli.command("create-db")
    def create_db():
        db.create_all()
        print("Database created.")

    return app
