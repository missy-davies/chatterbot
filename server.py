"""Server for Markov chains Tweet generator app"""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import jinja2

from model import db, connect_to_db, User, Musk_Tweet, UG_Tweet
import crud

from markovchain.text import MarkovText

import os
import sys 


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SERVER_KEY")

# Configurations to use Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """Reload the user object from the user_id stored in the session"""
    
    return User.query.get(int(user_id))


@app.route('/')
def show_create_account():
    """Display landing page with create new account details"""

    if current_user.is_authenticated:
        return redirect('/generate')
    else: 
        return render_template('create-account.html')


@app.route('/', methods=['POST'])
def create_account():
    """Create a new user account"""

    fname = request.form.get('fname')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Oops, looks like an account already exists with that email! Please log in.')
        return redirect('/login')
    else:
        crud.create_user(fname, email, password)
        flash("Hooray, you successfully signed up for an account! Please log in")
        return redirect('/login')


@app.route('/login')
def show_login():
    """Display landing page with login to existing account details"""
    
    # TODO: Add email and password criteria to ensure email is real and 
    # password meets requirements 

    if current_user.is_authenticated:
        return redirect('/generate')
    else: 
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Logs user into their account"""

    user = crud.get_user_by_email(request.form['login-email'])
    password = request.form['login-password']

    if user == None:
        flash('''Oops, we couldn't find an account under that email address. 
                Please create a new account and try again!''')
        return redirect('/')
    elif password != user.password:
        flash('Incorrect password. Please try again.')
        return redirect('/login')
    else:
        flash(f'Logged in as {user.fname}!')
        login_user(user)
        return redirect('/generate')


@app.route('/generate')
@login_required
def show_tweet_generator():
    """Show tweet generator page and generate new tweets"""

    return render_template('generate.html')


def clean_tweet(line):
    """Clean a Tweet by removing retweets, mentions, links, and other random symbols
    
    TODO: Add doctest!! 
    """

    old_line_arr = line.split(' ')
    new_line_arr = []
    
    # FIXME: This may be inefficient and slow the program. May need to refactor later
    # Move this to the seed_database file so that the database has cleaned data to generate tweets
    # use this to check date of last fetch on Tweets too 
    for word in old_line_arr:

        # remove retweets and mentions, links, and random symbols
        if word != 'RT' and word != '"RT' and '@' not in word \
                    and word[0:4] != 'http' \
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


@app.route('/markov')
@login_required
def generate_markov():
    """Generate markov tweet using stored Tweets in database
    
    TODO: Add doc tests! 
    """

    markov = MarkovText() 

    for tweet_obj in Musk_Tweet.query.all():
        new_tweet = clean_tweet(tweet_obj.text)
        markov.data(new_tweet)

    tweet = markov(max_length=40)
    # there are 6.1 chars on average in a word, Twitter's char limit is 280, 
    # so that makes for approx 45 words max in a tweet, rounding down to 40 for some margin

    tweet_obj = crud.create_ug_tweet(user=current_user, fav_status=False, text=tweet)

    return jsonify({'id': tweet_obj.ug_tweet_id, 'text': tweet_obj.text})


@app.route('/get-tweets')
@login_required
def get_ug_tweets():
    """Return id and text for all Markov Tweets a user has generated"""

    tweets_text = []

    for tweet in current_user.tweets:
        tweets_text.append({'id': tweet.ug_tweet_id, 
                            'text': tweet.text,
                            'fav_status': tweet.fav_status}) 

    return jsonify(tweets_text)


@app.route('/favorites')
@login_required
def show_favorites():
    """Display favorite generated tweets"""

    return render_template('favorites.html')


@app.route('/toggle-fav.json', methods=['POST']) 
@login_required
def toggle_fav():
    """Toggle favorite status of a tweet"""

    tweet_id = request.form.get('id')
    clicked_tweet = UG_Tweet.query.get(tweet_id)
    clicked_tweet.fav_status = False if clicked_tweet.fav_status else True
    db.session.commit()

    return redirect('/generate') # TODO: Is this the right thing to return here? 


@app.route('/get-fav-tweets')
@login_required
def get_fav_tweets():
    """Show all Markov Tweets a user has favorited"""

    fav_tweets_text = []
    
    for tweet in current_user.tweets:
        if tweet.fav_status == True:
            fav_tweets_text.append({'id': tweet.ug_tweet_id, 'text': tweet.text})

    return jsonify(fav_tweets_text)


@app.route('/logout')
@login_required
def logout():
    """Log user out of session"""

    logout_user()

    flash(f'See you later!')
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    """Return error message for unfound routes"""

    return render_template('page-not-found.html'), 404


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")