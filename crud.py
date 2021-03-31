"""CRUD operations"""

from model import db, User, Musk_Tweet, UG_Tweet, Fav_Tweet, connect_to_db

def create_user(fname, email, password):
    """Create and return a new user
    
    For example: 
    
    paste doctests here"""

    user = User(fname=fname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user 


if __name__ == '__main__':
    from server import app
    connect_to_db(app)