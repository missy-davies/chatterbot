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

# TODO: select Twitter account and number of tweets to seed database 
twitter_user = 'kimkardashian' 
client = get_twitter_client()

for status in tweepy.Cursor(client.user_timeline, screen_name=twitter_user).items(50): # add a number inside the parenthesis of items to limit # of tweets
    text = status.text

    db_musk_tweet = crud.create_musk_tweet(text)


# Random names and words to create users and demo texts out of
names = ['Aurora', 'Beatrice','Claudia','Domiziana', 'Eva',
         'Francesca','Giovanna', 'Helena', 'Ilaria', 'Jessica']

words = ['Doggo', 'ipsum', 'fluffer', 'noodle', 'horse', 'blep', 'most', 
         'angery', 'pupper', 'I', 'have', 'ever', 'seen', 'you', 'are', 
         'doing', 'me', 'the', 'shock', 'much', 'ruin', 'diet,', 'fluffer', 
         'pupper', 'many', 'pats', 'very', 'taste', 'wow.', 'Blop', 'fat', 
         'boi', 'bork', 'fat', 'boi', 'long', 'doggo', 'heckin', 'angery', 
         'woofer', 'what', 'a', 'nice', 'floof,', 'extremely', 'cuuuuuute', 
         'smol', 'wow', 'very', 'biscit', 'heckin.', 'Clouds', 'sub', 'woofer', 
         'you', 'are', 'doin', 'me', 'a', 'concern', 'most', 'angery', 
         'pupper', 'I', 'have', 'ever', 'seen', 'very', 'hand', 'that', 'feed', 
         'shibe,', 'waggy', 'wags', 'ur', 'givin', 'me', 'a', 'spook', 'very', 
         'jealous', 'pupper.', 'heck', 'big', 'ol', 'pupper', 'tungg.', 'Big', 
         'ol', 'pupper', 'tungg', 'wrinkler', 'doggo', 'boof', 'many', 'pats,', 
         'clouds', 'thicc', 'you', 'are', 'doin', 'me', 'a', 'concern.', 'very', 
         'jealous', 'pupper', 'puggo.', 'Heckin', 'clouds', 'super', 'chub', 
         'heckin', 'ur', 'givin', 'me', 'a', 'spook,', 'lotsa', 'pats', 'what', 
         'a', 'nice', 'floof', 'mlem.', 'Maximum', 'borkdrive', 'length', 'boy', 
         'ruff', 'very', 'good', 'spot', 'super', 'chub', 'he', 'made', 'many', 
         'woofs', 'borking', 'doggo', 'big', 'ol,', 'adorable', 'doggo', 'vvv', 
         'thicc', 'doing', 'me', 'a', 'frighten', 'you', 'are', 'doin', 'me', 
         'a', 'concern.', 'Clouds', 'pupper', 'tungg', 'snoot', 'aqua', 'doggo', 
         'lotsa', 'pats']

# create 10 users, each of whom has 10 random Tweets generated from Doggo Ipsum

for name in names:
    email = f'{name.lower()}@libero.it'
    password = f'supersafe{name.lower()[0]}{names.index(name)}'

    user = crud.create_user(name, email, password)

    for _ in range(10):
        new_tweet = []

        for _ in range(5):
            new_tweet.append(choice(words))

        str_tweet = (" ").join(new_tweet).capitalize()

        ug_tweet = crud.create_ug_tweet(user, False, str_tweet)
