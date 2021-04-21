"""CRUD operations"""

from model import db, User, Original_Tweet, UG_Tweet, Author, connect_to_db

def create_user(fname, email, password):
    """Create and return a new user"""

    user = User(fname=fname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user 


def get_user_by_email(email):
    """Return a user object by email"""

    return User.query.filter(User.email == email).first()


def create_author(name, twitter_handle):
    """Create and return an author for a tweet"""

    author = Author(name=name, twitter_handle=twitter_handle)

    db.session.add(author)
    db.session.commit()

    return author


def create_original_tweet(text, author):
    """Create and return an original Tweet from an author"""

    original_tweet = Original_Tweet(text=text, author=author)

    db.session.add(original_tweet)
    db.session.commit()

    return original_tweet


def create_ug_tweet(user, fav_status, text, authors):
    """Create and return a user generated Markov Tweet"""

    ug_tweet = UG_Tweet(user=user, fav_status=fav_status, text=text, authors=authors)

    db.session.add(ug_tweet)
    db.session.commit()

    return ug_tweet


def get_authors_ug_tweet():
    """Given a generated tweet, return the authors of that tweet"""

    # TODO: Maybe need a function like this? 


if __name__ == '__main__':
    from server import app
    connect_to_db(app)