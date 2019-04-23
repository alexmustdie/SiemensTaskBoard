import os
import enum

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(os.path.dirname(__file__), 'task-board.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


db.create_all()
db.session.commit()


@app.errorhandler(Exception)
def handle_exception(exc):
    return jsonify(error=str(exc))


@app.route('/')
def index():
    return 'Siemens Task Board'


@app.route('/api/users.add', methods=['GET'])
def add_user():

    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    user = User(first_name=first_name, last_name=last_name)

    db.session.add(user)
    db.session.commit()

    return jsonify(id=user.id)


@app.route('/api/users.edit', methods=['GET'])
def edit_user():

    user_id = int(request.args['user_id'])
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    user = db.session.query(User).get(user_id)

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    db.session.commit()

    return jsonify(result=True)


@app.route('/api/users.assignTask', methods=['GET'])
def assign_task():

    user_id = int(request.args['user_id'])
    task_id = int(request.args['task_id'])

    user = db.session.query(User).get(user_id)
    task = db.session.query(Task).get(task_id)

    task.user_id = user.id
    db.session.commit()

    return jsonify(result=True)


@app.route('/api/tasks.add', methods=['GET'])
def add_task():

    title = request.args['title']
    description = request.args['description']
    user_id = int(request.args.get('user_id') or 0)

    user = db.session.query(User).get(user_id)
    task = Task(title=title, description=description, user_id=user.id if user else 0)

    db.session.add(task)
    db.session.commit()

    return jsonify(id=task.id)


@app.route('/api/tasks.edit', methods=['GET'])
def edit_task():

    task_id = int(request.args['task_id'])
    title = request.args.get('title')
    description = request.args.get('description')

    task = db.session.query(Task).get(task_id)

    if title:
        task.title = title

    if description:
        task.description = description

    db.session.commit()

    return jsonify(result=True)


@app.route('/api/tasks.setStatus', methods=['GET'])
def set_task_status():

    task_id = int(request.args['task_id'])
    status = int(request.args['status'])

    task = db.session.query(Task).get(task_id)
    task.status = TaskStatus(status)

    db.session.commit()

    return jsonify(result=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
