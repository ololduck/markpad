from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from markpad import config


app = Flask(__name__)
app.config.from_object(config)
logger = app.logger

db = SQLAlchemy(app)

from markpad import views
from markpad import models


def init_db():
    db.create_all()
    logger.info("created a new database")
