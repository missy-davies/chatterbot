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

os.system(f'dropdb {os.environ['DATABASE_NAME']}')
os.system(f'createdb {os.environ['DATABASE_NAME']}')

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


def clean_tweet(line):
    """Clean a Tweet by removing retweets, mentions, links, and other random symbols"""

    old_line_arr = line.split(' ')
    new_line_arr = []
    
    # FIXME: This may be inefficient and slow the program. May need to refactor later
    for word in old_line_arr:

        # remove retweets and mentions, links, and random symbols
        if word != 'RT' and word != '"RT' and '@' not in word \
                    and 'http' not in word \
                    and 'www' not in word \
                    and '.com' not in word \
                    and word != ':' and word != '!' and word != '-' \
                    and 'amp;' not in word:
            
            # remove trailing period 
            if len(word) > 1:
                if word[-1] == '.':
                    word = word[0:-1]
                    new_line_arr.append(word)
                else: 
                    new_line_arr.append(word)

    return (' ').join(new_line_arr)


# Seed database with tweets from each above Twitter account
for account in twitter_accounts:
    name = account['name']
    twitter_handle = account['twitter_handle']

    author = crud.create_author(name, twitter_handle)

    for status in tweepy.Cursor(client.user_timeline, screen_name=twitter_handle).items(500): # add a number inside the parenthesis of items to limit # of tweets
        text = clean_tweet(status.text)

        db_musk_tweet = crud.create_original_tweet(text, author)


# Random names to create users and seed database
# names = ['Aurora', 'Beatrice','Claudia','Domiziana', 'Eva',
#          'Francesca','Giovanna', 'Helena', 'Ilaria', 'Jessica']

# for name in names:
#     email = f'{name.lower()}@libero.it'
#     password = f'supersafe{name.lower()[0]}{names.index(name)}'

#     user = crud.create_user(name, email, password)

# Demo User
crud.create_user('Missy', 'demo@gmail.com', 'demo123')