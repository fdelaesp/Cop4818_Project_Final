from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    pw_hash  = db.Column(db.String(128), nullable=False)
    joined   = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.pw_hash, password)

class Indicator(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    latest_val  = db.Column(db.Float, nullable=True)
    updated_at  = db.Column(db.DateTime, nullable=True)

class QueryLog(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey("user.id"))
    indicator = db.Column(db.String(150))
    ts        = db.Column(db.DateTime, default=datetime.utcnow)


class DataPoint(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    indicator_id = db.Column(db.Integer, db.ForeignKey("indicator.id"))
    year       = db.Column(db.Integer, nullable=False)
    month      = db.Column(db.String(15), nullable=False)  # e.g. "Enero"
    value      = db.Column(db.Float, nullable=True)
    unidad     = db.Column(db.String(50))
    grupo      = db.Column(db.String(100))
    subgrupo   = db.Column(db.String(100))
    categoria  = db.Column(db.String(100))

    indicator  = db.relationship("Indicator", backref="data_points")
