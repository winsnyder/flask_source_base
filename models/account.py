from datetime import datetime
from app import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(500), index=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    posts = db.relationship('Post', backref='account', lazy=True, cascade="all,delete-orphan")

    def __repr__(self):
        return '<User {}>'.format(self.username)
