"""User generated tweet model for Markov chains Tweet generator app"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.model import db
from models.Author import Author
from models.association import link_ug_tweet_authors

class UG_Tweet(db.Model):
    """A user generated Markov chain tweet"""

    __tablename__ = 'ug_tweets'

    ug_tweet_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    fav_status = db.Column(db.Boolean, default=False)
    text = db.Column(db.String, nullable=False)
    authors = db.relationship('Author', secondary=link_ug_tweet_authors, back_populates='ug_tweets') 
    botname = db.Column(db.String, nullable=False)

    user = db.relationship('User')

    def __repr__(self):
        """Show info about a user generated Markov chain Tweet"""

        return f'<UG_Tweet ug_tweet_id={self.ug_tweet_id} fav_status={self.fav_status} botname={self.botname} text={self.text}>'
