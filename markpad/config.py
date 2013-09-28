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

if("DATABASE_URL" in os.environ):
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
else:
    dbpath = os.path.join(basedir, 'markdown.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + dbpath

if("SECRET_KEY" in os.environ):
    SECRET_KEY = os.environ["SECRET_KEY"]
else:
    SECRET_KEY = "super-secret-of-death"
