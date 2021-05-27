"""Association table between authors and generated tweets"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.model import db
 
link_ug_tweet_authors = db.Table('link_ug_tweet_authors', db.Model.metadata,
    db.Column('author_id', db.Integer, db.ForeignKey('authors.author_id')),
    db.Column('ug_tweet_id', db.Integer, db.ForeignKey('ug_tweets.ug_tweet_id'))
)