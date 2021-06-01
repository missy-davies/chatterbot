"""Markov algorithm helpers"""

from flask_login import current_user
from flask import Flask, jsonify

from models.Author import Author 
from models.Original_Tweet import Original_Tweet
import crud

from markovchain.text import MarkovText


def markov_algo(list_twitter_accounts): 
    """Use Markov library to create and return a string based given twitter account(s)"""

    if len(list_twitter_accounts) != 0:
        markov = MarkovText() 

        # Create list of author objects by iterating through given list of selected twitter accounts
        author_objs = []
        for index, twitter_account in enumerate(list_twitter_accounts):
            author_objs.append(Author.query.filter_by(twitter_handle=list_twitter_accounts[index]).one())

        # Get and clean all of the original tweets for each selected author 
        for author_obj in author_objs:
            for tweet_obj in Original_Tweet.query.filter_by(author=author_obj).all():
                new_tweet = tweet_obj.text
                markov.data(new_tweet)

        tweet = markov(max_length=40)
        # there are 6.1 chars on average in a word, Twitter's char limit is 280, 
        # so that makes for approx 45 words max in a tweet, rounding down to 40 for some margin
        
        tweet_obj = crud.create_ug_tweet(user=current_user, fav_status=False, 
                                         text=tweet, authors=author_objs, botname=crud.make_bot_username(author_objs))
        
        return jsonify({'id': tweet_obj.ug_tweet_id, 'text': tweet_obj.text, 'botname': tweet_obj.botname})
    else:
        return ValueError('No Twitter accounts selected') 


def str_to_bool(string_val):
    """Take in a string of 'true' or 'false' and convert to Python boolean"""

    if string_val[0] == 'f':
        return False
    elif string_val[0] == 't':
        return True 
