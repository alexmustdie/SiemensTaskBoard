import os

PROJECT_PATH = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(PROJECT_PATH, 'schema.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False
