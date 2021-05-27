"""User model for Markov chains Tweet generator app"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.model import db

class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    fname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    tweets = db.relationship('UG_Tweet')

    # Methods for Flask Login 
    def is_authenticated(self):
        """Return True if user is authenticated"""

        return True


    def is_active(self):  
        """Return True if user is active""" 

        return True           


    def is_anonymous(self):
        """Return True if user is anonymous. Real users should return False"""

        return False          


    def get_id(self):
        """Return unique user id"""

        return str(self.user_id)


    def __repr__(self):
        """Show info about user"""

        return f'<User user_id={self.user_id} fname={self.fname} email={self.email}>'