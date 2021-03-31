"""CRUD operations"""

from model import db, User, Musk_Tweet, UG_Tweet, Fav_Tweet, connect_to_db

def create_user(fname, email, password):
    """Create and return a new user"""

    user = User(fname=fname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user 


def create_musk_tweet(text):
    """Create and return an original Tweet from Elon Musk"""

    musk_tweet = Musk_Tweet(text=text)

    db.session.add(musk_tweet)
    db.session.commit()

    return musk_tweet


def create_ug_tweet(user_id, fav_status, text):
    """Create and return a user generated Markov Tweet"""

    ug_tweet = UG_Tweet(user_id=user_id, fav_status=fav_status, text=text)

    db.session.add(ug_tweet)
    db.session.commit()

    return ug_tweet


def create_fav_tweet(user_id, ug_tweet_id):
    """Create and return a favorited user generated Markov Tweet"""

    fav_tweet = Fav_Tweet(user_id=user_id, ug_tweet_id=ug_tweet_id)

    db.session.add(fav_tweet)
    db.session.commit()

    return fav_tweet


if __name__ == '__main__':
    from server import app
    connect_to_db(app)