"""Original tweet model for Markov chains Tweet generator app"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.model import db
from models.Author import Author
from models.association import link_ug_tweet_authors

class Original_Tweet(db.Model):
    """An original Tweet from a given Twitter user"""

    __tablename__ = 'original_tweets'

    original_tweet_id = db.Column(db.Integer,
                                  primary_key=True,
                                  autoincrement=True)
    text = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id')) 

    author = db.relationship('Author')         

    def __repr__(self):
        """Show info about an original Tweet"""

        return f'<Original_Tweet original_tweet_id={self.original_tweet_id} text={self.text} author={self.author.name}>'
