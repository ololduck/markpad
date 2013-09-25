from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from tpassist import config


app = Flask(__name__)
app.config.from_object(config)
logger = app.logger

db = SQLAlchemy(app)

from tpassist import views
from tpassist import models
from tpassist import base_pages


def init_db():
    db.create_all()
    logger.info("created a new database")
