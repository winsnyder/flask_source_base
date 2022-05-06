from datetime import datetime
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, default='{}')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),
                         nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Task {}>'.format(self.id)
