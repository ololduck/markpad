import os
basedir = os.path.abspath(os.path.dirname(__file__))

MARKDOWN_EXTS = [
    'extra',
    'nl2br',
    'wikilinks',
    'headerid',
    'codehilite',
    'admonition'
]

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
    'sqlite:///' + os.path.join(basedir, 'markpad.db'))

SECRET_KEY = os.environ.get("SECRET_KEY", 'super-secret-of-death')
HOST_URL = 'localhost:5000'
