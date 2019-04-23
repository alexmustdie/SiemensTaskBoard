import enum
import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(os.path.dirname(__file__), 'task-board.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tasks = db.relationship('Task', backref='user', lazy=True)


class TaskStatus(enum.Enum):
    TODO = 0
    IN_PROGRESS = 1
    ON_REVIEW = 2
    DONE = 3


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(TaskStatus), nullable=False)


db.create_all()
db.session.commit()


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/users.add', methods=['GET'])
def add_user():
    user = User()
    db.session.add(user)
    db.session.commit()
    return jsonify({'response': user.id})


@app.route('/api/users.assignTask', methods=['GET'])
def assign_task():
    user_id = request.args.get('user_id')
    task_id = request.args.get('task_id')
    task = db.session.query(Task).get(task_id)
    task.user_id = user_id
    db.session.commit()
    return jsonify({'response': 1})


@app.route('/api/tasks.add', methods=['GET'])
def add_task():
    user_id = request.args.get('user_id')
    task = Task(user_id=user_id, status=TaskStatus.TODO)
    db.session.add(task)
    db.session.commit()
    return jsonify({'response': task.id})


@app.route('/api/tasks.setStatus', methods=['GET'])
def set_task_status():
    task_id = request.args.get('task_id')
    status = request.args.get('status')
    task = db.session.query(Task).get(task_id)
    task.status = TaskStatus(int(status))
    db.session.commit()
    return jsonify({'response': 1})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
