from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from markpad import config
import os
import logging

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, static_folder=os.path.join(PROJECT_ROOT, 'static'), static_url_path='/static')
app.config.from_object(config)
logger = app.logger

app.deltas = {}
app.client_states = {}
app.current_serial_id = 0

db = SQLAlchemy(app)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)
logger.info('markpad starting up...')

from markpad import views
from markpad import models

def init_db():
    db.create_all()
    logger.info("created/updated database")

logger.debug("initiating DB connection")
init_db()
logger.info("markpad started")

