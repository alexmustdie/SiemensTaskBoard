from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
db.create_all()
db.session.commit()


@app.route('/')
def index():
    return 'Siemens Task Board'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
