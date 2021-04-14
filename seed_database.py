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


# Seed database with Tweets using a Twitter API call with the Tweepy wrapper
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


# TODO: Change Twitter account and number of tweets to seed database 
twitter_user = 'kimkardashian' 
client = get_twitter_client()

for status in tweepy.Cursor(client.user_timeline, screen_name=twitter_user).items(500): # add a number inside the parenthesis of items to limit # of tweets
    text = status.text

    db_musk_tweet = crud.create_musk_tweet(text)


# Random names and words to create users and demo texts out of
names = ['Aurora', 'Beatrice','Claudia','Domiziana', 'Eva',
         'Francesca','Giovanna', 'Helena', 'Ilaria', 'Jessica']

for name in names:
    email = f'{name.lower()}@libero.it'
    password = f'supersafe{name.lower()[0]}{names.index(name)}'

    user = crud.create_user(name, email, password)

