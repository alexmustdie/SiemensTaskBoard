from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from task_board.api import *


@app.route('/')
def index():
    return 'Siemens Task Board'
