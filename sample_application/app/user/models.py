"""User - Models."""

import datetime

from app.database import db

from sqlalchemy.orm.interfaces import MapperExtension
from geoalchemy2.types import Geometry

class User(db.Model):
    """Class: User."""
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    email_id = db.Column(db.String, nullable=False, index=True)
    phone_number = db.Column(db.Integer, nullable=False, index=True)
    createdDateTime = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedDateTime = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def save(self):
        db.session.begin(subtransactions=True)
        db.session.add(self)
        db.session.commit()