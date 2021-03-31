"""Script to seed database"""

import os
import json
from random import choice, randint

import crud
import model
import server 

os.system('dropdb tweetgenerator')
os.system('createdb tweetgenerator')

model.connect_to_db(server.app)
model.db.create_all()

# FIXME: This is loading a small sample of a few Elon Musk Tweets, 
# I'll need to change to the full file later
with open('data/sample_elon_musk_tweets.json') as f:
    musk_data = json.loads(f.read())

musk_tweets_in_db = []
for musk_tweet in musk_data:
    text = musk_tweet['Text']

    db_musk_tweet = crud.create_musk_tweet(text)
    musk_tweets_in_db.append(db_musk_tweet)


# TODO: Finish seed script, need to test the above function, left off at 'Back to seeding the db' 
# here https://fellowship.hackbrightacademy.com/materials/ft34a/exercises/ratings-v2/index-2.html


