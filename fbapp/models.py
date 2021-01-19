from flask_sqlalchemy import SQLAlchemy
import logging as lg
from .views import app

import enum

# Create database connection object
db = SQLAlchemy(app)
#lg.warning('Loading classifier !')

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.Column(db.String(200),nullable=False)
    title = db.Column(db.String(300),nullable=False)
    body = db.Column(db.String(1000),nullable=False)

    def __init__(self, body, tags='[]',title='' ):
        self.body = body
        self.tags = tags
        self.title = title


def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Content(body='I would like my whole csv sheet to be converted to comma separate list so I can use pandas easily.',
                           title='Convert CSV file in Python',
                           tags= "['python']"))
    db.session.commit()
    lg.warning('Database initialized!')
