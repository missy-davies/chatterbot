"""CRUD operations"""

from models.model import db, connect_to_db
from models.User import User
from models.UG_Tweet import UG_Tweet
from models.Author import Author 
from models.Original_Tweet import Original_Tweet 

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


def create_ug_tweet(user, fav_status, text, authors, botname):
    """Create and return a user generated Markov Tweet"""

    ug_tweet = UG_Tweet(user=user, fav_status=fav_status, text=text, authors=authors, botname=botname)

    db.session.add(ug_tweet)
    db.session.commit()

    return ug_tweet


def make_bot_username(list_authors): 
    """Take in a list of author objects and return a new 'bot' fake username"""

    bot_name = []

    if len(list_authors) == 1:
        bot_name.extend([list_authors[0].twitter_handle, 'bot'])
    else:
        for author in list_authors[1:]:
            # extend bot_name with all last names
            # ex. Kim Kardashian West would extend with 'Kardashian West'
            bot_name.extend(author.name.split(' ')[1:])

        # insert first name of first author in list to the bot_name 
        bot_name[0:0] = [list_authors[0].name.split(' ')[0]]
        bot_name.append('bot')

    return '_'.join([name.lower() for name in bot_name])


if __name__ == '__main__':
    from server import app
    connect_to_db(app)