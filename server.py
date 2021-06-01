"""Server for Markov chains Tweet generator app"""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import jinja2

from models.model import db, connect_to_db
from models.User import User 
from models.UG_Tweet import UG_Tweet 
from models.Author import Author 
from models.Original_Tweet import Original_Tweet
from models.association import link_ug_tweet_authors
import crud

from markov_helpers import str_to_bool, markov_algo
 
from markovchain.text import MarkovText

import os
import sys 

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SERVER_KEY")

# Configurations to use Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


####################################################################
#                          Login Routes                            #
####################################################################

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
        flash(u'Oops, looks like an account already exists with that email! Please log in 🙏', 'error')
        return redirect('/login')
    elif '@' not in email and len(password) < 7:
        flash(u'Please enter a valid email address and ensure your password is at least 7 characters long 🔒', 'error')
        return redirect('/')
    elif '@' not in email:
        flash(u'Please enter a valid email address 💌', 'error')
        return redirect('/')
    elif len(password) < 7:
        flash(u'Password must be at least 7 characters long 🔒', 'error')
        return redirect('/')
    else:
        crud.create_user(fname, email, password)
        flash("Hooray, you successfully signed up for an account! Please log in 🎉")
        return redirect('/login')


@app.route('/login')
def show_login():
    """Display landing page with login to existing account details"""

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
        flash(u'''Oops, we couldn't find an account under that email address.
                Please create a new account and try again! 👾''', 'error')
        return redirect('/')
    elif password != user.password:
        flash(u'Wrong password, please try again 😁', 'error')
        return redirect('/login')
    else:
        greeting = user.fname.capitalize()
        flash(f'Welcome to ChatterBot, {greeting}! 🦄')
        login_user(user)
        return redirect('/generate')


####################################################################
#                   Routes Using Markov Library                    #
####################################################################

@app.route('/markov')
@login_required
def generate_markov():
    """Generate markov tweet using stored Tweets in database"""
    
    selected_twitter_people = [
        {'handle': 'elonmusk',
        'status': str_to_bool(request.args.get('elonmusk'))},
        {'handle': 'kimkardashian',
        'status': str_to_bool(request.args.get('kimkardashian'))},
        {'handle': 'britneyspears',
        'status': str_to_bool(request.args.get('britneyspears'))},
        {'handle': 'justinbieber',
        'status': str_to_bool(request.args.get('justinbieber'))},
        {'handle': 'ladygaga',
        'status': str_to_bool(request.args.get('ladygaga'))}
        ]

    accounts = []

    for person in selected_twitter_people:
        if person['status'] == True:
            accounts.append(person['handle'])

    return markov_algo(accounts)


####################################################################
#                     Routes to Display Tweets                     #
####################################################################

@app.route('/get-tweets')
@login_required
def get_ug_tweets():
    """Return id and text for all Markov Tweets a user has generated"""

    tweets_text = []

    for tweet in current_user.tweets:

        tweets_text.append({'id': tweet.ug_tweet_id, 
                            'text': tweet.text,
                            'fav_status': tweet.fav_status,
                            'botname': tweet.botname}) 

    return jsonify(sorted(tweets_text, key = lambda i: i['id']))


@app.route('/generate')
@login_required
def show_tweet_generator():
    """Show tweet generator page and generate new tweets"""
    tweets = current_user.tweets
    no_tweets = True
    if len(tweets) != 0:
        no_tweets = False

    return render_template('generate.html', no_tweets=no_tweets)


@app.route('/favorites')
@login_required
def show_favorites():
    """Display favorite generated tweets"""

    tweets = current_user.tweets
    no_favs = True
    for tweet in tweets:
        if tweet.fav_status == True:
            no_favs = False
            break

    return render_template('favorites.html', no_favs=no_favs)


@app.route('/toggle-fav', methods=['POST']) 
@login_required
def toggle_fav():
    """Toggle favorite status of a tweet"""

    tweet_id = request.form.get('id')
    clicked_tweet = UG_Tweet.query.get(tweet_id)
    clicked_tweet.fav_status = False if clicked_tweet.fav_status else True
    db.session.commit()

    return redirect('/generate') 


####################################################################
#                  Logout & Error Handler Routes                   #
####################################################################

@app.route('/logout')
@login_required
def logout():
    """Log user out of session"""

    logout_user()

    flash('Ciao for now! 👋')
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    """Return error message for unfound routes"""

    return render_template('page-not-found.html'), 404


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")