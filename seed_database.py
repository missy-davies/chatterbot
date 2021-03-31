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

with open('data/elon_musk_tweets.json') as f:
    musk_data = json.loads(f.read())

