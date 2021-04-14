"""Script to test Flask routes and server"""

from unittest import TestCase
from server import app
from flask import session
import crud
import model
import os
import seed_database

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True


    def tearDown(self):
        """Stuff to do after each test."""


    def test_home(self):
        """Test displaying create account homepage"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn('create-account.html', result.data)


    def test2(self):
        """Some other test"""