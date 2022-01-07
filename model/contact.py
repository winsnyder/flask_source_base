from datetime import datetime
from app import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(300), index=True)
    email = db.Column(db.String(300), index=True)
    phone = db.Column(db.String(20))
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Contact {}>'.format(self.fullname)
