"""Script to seed database"""

import os
import sys 
import json
import requests 
from random import choice

import crud
import model
import server 

os.system('dropdb tweetgenerator')
os.system('createdb tweetgenerator')

model.connect_to_db(server.app)
model.db.create_all()


# TWITTER API CODE GOES HERE 

def auth():
    """Get Twitter Bearer token"""

    return os.environ.get("BEARER_TOKEN")

def create_url():
    """Build URL to query Twitter API for the text from a user's Tweets"""

    query = "from:missy_davies_ -is:text"
 
    tweet_fields = "tweet.fields=text"
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&{tweet_fields}"

    return url


# FIXME: This is the code to load a small sample of a few Elon Musk Tweets, 
# I'll need to replace with seeding from the Twitter API 
# with open('data/sample_elon_musk_tweets.json') as f:
#     musk_data = json.loads(f.read())

# musk_tweets_in_db = []
# for musk_tweet in musk_data['tweets']:
#     text = musk_tweet['Text']

#     db_musk_tweet = crud.create_musk_tweet(text)
#     musk_tweets_in_db.append(db_musk_tweet)


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
