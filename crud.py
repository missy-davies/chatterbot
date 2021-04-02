"""CRUD operations"""

from model import db, User, Musk_Tweet, UG_Tweet, connect_to_db

def create_user(fname, email, password):
    """Create and return a new user"""

    user = User(fname=fname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user 


def get_user_by_email(email):
    """Return a user object by email"""

    return User.query.filter(User.email == email).first()


def create_musk_tweet(text):
    """Create and return an original Tweet from Elon Musk"""

    musk_tweet = Musk_Tweet(text=text)

    db.session.add(musk_tweet)
    db.session.commit()

    return musk_tweet


def create_ug_tweet(user, fav_status, text):
    """Create and return a user generated Markov Tweet"""

    ug_tweet = UG_Tweet(user=user, fav_status=fav_status, text=text)

    db.session.add(ug_tweet)
    db.session.commit()

    return ug_tweet


if __name__ == '__main__':
    from server import app
    connect_to_db(app)