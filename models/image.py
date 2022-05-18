from datetime import datetime
from app import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), index=True)
    url = db.Column(db.String())
    comments = db.relationship(
        'Comment', backref='image', lazy=True, cascade="all,delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.now())
