"""Author model for Markov chains Tweet generator app"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.model import db
from models.association import link_ug_tweet_authors

class Author(db.Model):
    """A user on Twitter who authors tweets"""

    __tablename__ = 'authors'

    author_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True)
    name = db.Column(db.String, nullable=False)
    twitter_handle = db.Column(db.String, nullable=False)

    original_tweets = db.relationship('Original_Tweet')
    ug_tweets = db.relationship('UG_Tweet', secondary=link_ug_tweet_authors, back_populates='authors')


    def __repr__(self):
        """Show info about an author"""

        return f'<Author author_id={self.author_id} name={self.name} twitter_handle={self.twitter_handle}>'
