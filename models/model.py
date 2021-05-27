"""Models for Markov chains Tweet generator app"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Original_Tweet(db.Model):
#     """An original Tweet from a given Twitter user"""

#     __tablename__ = 'original_tweets'

#     original_tweet_id = db.Column(db.Integer,
#                                   primary_key=True,
#                                   autoincrement=True)
#     text = db.Column(db.String, nullable=False)
#     author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id')) 

#     author = db.relationship('Author')         

#     def __repr__(self):
#         """Show info about an original Tweet"""

#         return f'<Original_Tweet original_tweet_id={self.original_tweet_id} text={self.text} author={self.author.name}>'


def connect_to_db(flask_app, db_uri='postgresql:///tweetgenerator', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Yay, you successfully connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)