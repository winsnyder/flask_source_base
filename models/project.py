from datetime import datetime
from app import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(500), index=True)
    tag = db.Column(db.String(100))
    deadline = db.Column(db.String(100))
    tasks = db.relationship('Task', backref='project',
                            lazy=True, cascade="all,delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Project {}>'.format(self.project_name)
