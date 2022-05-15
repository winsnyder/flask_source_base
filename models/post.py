from datetime import datetime
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), index=True)
    summary = db.Column(db.String(500))
    content = db.Column(db.Text)
    image = db.Column(db.String())
    is_publish = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
        nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'),
        nullable=False)