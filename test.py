"""Script to test Flask routes and server"""

from unittest import TestCase
from server import app
from flask import session
import crud
from model import connect_to_db, db, User, UG_Tweet, Original_Tweet, Author
import os
import json 

def example_data():
    """Create sample data"""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    UG_Tweet.query.delete()
    Original_Tweet.query.delete()
    Author.query.delete()

    # Add sample users 
    aurora = crud.create_user('Aurora', 'aurora@libero.it', 'test1')
    beatrice = crud.create_user('Beatrice', 'beatrice@libero.it', 'test2')
    claudia = crud.create_user('Claudia', 'claudia@libero.it', 'test3')

    # Add sample authors
    elon = crud.create_author('Elon Musk', 'elonmusk')
    kim = crud.create_author('Kim Kardashian West', 'kimkardashian')

    # Add sample Elon test tweets
    etweet1 = crud.create_original_tweet('Doge Barking at the Moon', elon)
    etweet2 = crud.create_original_tweet('Tesla AI/Autopilot engineering is awesome! Making excellent progress solving real-world AI.', elon)
    etweet3 = crud.create_original_tweet('The art In Cyberpunk is incredible', elon)

    # Add sample Kim test tweets
    ktweet1 = crud.create_original_tweet("You’re always so cute in skims!!!", kim)
    ktweet2 = crud.create_original_tweet('Hands down - Eye Contour Duo in Medium and the Glossy Lip Balm. The best for a quick natural look', kim)
    ktweet3 = crud.create_original_tweet("Jeff Leatham or my collaboration w my mom is the perfect gift for Mother’s Day!", kim)

    db.session.add_all([aurora, beatrice, claudia, etweet1, etweet2, etweet3, ktweet1, ktweet2, ktweet3])
    db.session.commit()


class FlaskTestsBasic(TestCase):
    """Flask server tests"""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True


    def tearDown(self):
        """Stuff to do after every test"""

        self.client = None
        app.config['TESTING'] = False


    def test_create_account(self):
        """Test displaying create account homepage"""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Sign up to generate Tweets', result.data)


    def test_login(self):
        """Test displaying login to existing account homepage"""

        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Sign in to generate Tweets', result.data)


    def test_generate(self):
        """Test displaying generate page"""

        result = self.client.get('/generate')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'generate tweets', result.data)
   
   
    def test_favorites(self):
        """Test displaying favorites page"""

        result = self.client.get('/favorites')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<div class="fav-tweets">', result.data)


class FlaskTestsDatabaseLoggedIn(TestCase):
    """Flask tests that use the database while user is logged in""" 

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb', echo=False)

        db.create_all()
        example_data()


    def tearDown(self):
        """Stuff to do after each test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


    def test_create_account_post(self):
        """Test getting client data on create account homepage"""

        result = self.client.post('/',
                                  data={'fname': 'Domiziana', 
                                        'email': 'domiziana@libero.it',
                                        'password': 'testing4'},
                                  follow_redirects=True)
        self.assertIn(b'Hooray, you successfully signed up', result.data)    


    def test_login_post(self):
        """Test getting client data on login homepage"""

        result = self.client.post('/login',
                                  data={'login-email': 'aurora@libero.it', 
                                        'login-password': 'test1'},
                                  follow_redirects=True)
        self.assertIn(b'Logged in as', result.data)


class APITest(TestCase):
    """Flask tests for routes returning API data""" 

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb', echo=False)

        db.create_all()
        example_data()

        # logs user in 
        self.client.post('/login', data={"login-email": "aurora@libero.it", "login-password": "test1"}, follow_redirects=True)


    def tearDown(self):
        """Stuff to do after each test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


    # def test_markov(self):
    #     """Test generating a markov tweet"""

    #     result = self.client.get('/markov')
    #     self.assertEqual(result.status_code, 200)
    #     data = json.loads(result.get_data(as_text=True))

    #     self.assertEqual(data['id'], 1)


    # def test_get_tweets(self):
    #     """Test getting all generated tweets"""

    #     result = self.client.get('/get-tweets')
    #     self.assertEqual(result.status_code, 200)
    #     data = json.loads(result.get_data(as_text=True))
    
    #     self.assertEqual(data[0]['id'], 1)


#------------------------------------------------------------------#
if __name__ == '__main__':
    import unittest

    os.system('dropdb testdb')
    os.system('createdb testdb')
    
    unittest.main(verbosity=2)