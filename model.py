"""Models for Markov chains Tweet generator app"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

# association table 
link_ug_tweet_authors = db.Table('link_ug_tweet_authors', db.Model.metadata,
    db.Column('author_id', db.Integer, db.ForeignKey('authors.author_id')),
    db.Column('ug_tweet_id', db.Integer, db.ForeignKey('ug_tweets.ug_tweet_id'))
)


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