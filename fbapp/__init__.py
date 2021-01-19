from flask import Flask

from .views import app
from . import models

def _nothing(x):
    return x
# Connect sqlalchemy to app
models.db.init_app(app)
models.init_db()
@app.cli.command('init_db') #Ask the db to create itself only once
def init_db():
    models.init_db()
