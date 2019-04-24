import enum

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)


class TaskStatus(enum.Enum):
    TODO = 0
    IN_PROGRESS = 1
    ON_REVIEW = 2
    DONE = 3


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
