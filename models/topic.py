from datetime import datetime
from app import db

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(300), index=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())
    post = db.relationship('Post', backref='topic', lazy=True, cascade="all,delete-orphan")
