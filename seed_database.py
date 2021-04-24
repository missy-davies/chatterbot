"""Script to seed database"""

import os
import sys 
import json
import requests 
from random import choice

import crud
import model
import server 

import tweepy 

os.system('dropdb tweetgenerator')
os.system('createdb tweetgenerator')

model.connect_to_db(server.app)
model.db.create_all()


# Set up to use Twitter API with the Tweepy wrapper
def twitter_auth():
    """Authenticate Twitter API connection with secret keys"""

    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['SECRET_KEY']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    return auth


def get_twitter_client():
    """Get Twitter client"""

    auth = twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client 


twitter_accounts = [{'name': 'Elon Musk',
                     'twitter_handle': 'elonmusk'},
                    {'name': 'Britney Spears',
                    'twitter_handle': 'britneyspears'},
                    {'name': 'Justin Bieber',
                    'twitter_handle': 'justinbieber'},
                    {'name': 'Kim Kardashian West',
                     'twitter_handle': 'kimkardashian'},
                    {'name': 'Lady Gaga',
                    'twitter_handle': 'ladygaga'}
                     ] 
client = get_twitter_client()

# Seed database with tweets from each above Twitter account
for account in twitter_accounts:
    name = account['name']
    twitter_handle = account['twitter_handle']

    author = crud.create_author(name, twitter_handle)

    for status in tweepy.Cursor(client.user_timeline, screen_name=twitter_handle).items(150): # add a number inside the parenthesis of items to limit # of tweets
        text = status.text

        db_musk_tweet = crud.create_original_tweet(text, author)


# TODO: Remove fake users, maybe seed with demo user 
# Random names to create users
names = ['Aurora', 'Beatrice','Claudia','Domiziana', 'Eva',
         'Francesca','Giovanna', 'Helena', 'Ilaria', 'Jessica']

for name in names:
    email = f'{name.lower()}@libero.it'
    password = f'supersafe{name.lower()[0]}{names.index(name)}'

    user = crud.create_user(name, email, password)
