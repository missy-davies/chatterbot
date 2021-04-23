"""Server for Markov chains Tweet generator app"""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import jinja2

from model import db, connect_to_db, User, Original_Tweet, UG_Tweet, Author
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


#################| Login Routes |#################

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
    elif '@' not in email and len(password) < 7:
        flash('Please enter a valid email address and ensure your password is at least 7 characters long')
        return redirect('/')
    elif '@' not in email:
        flash('Please enter a valid email address.')
        return redirect('/')
    elif len(password) < 7:
        flash('Password must be at least 7 characters long')
        return redirect('/')
    else:
        crud.create_user(fname, email, password)
        flash("Hooray, you successfully signed up for an account! Please log in")
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


#################| Routes Using Markov Library |#################

@app.route('/generate')
@login_required
def show_tweet_generator():
    """Show tweet generator page and generate new tweets"""

    return render_template('generate.html')


def clean_tweet(line):
    """Clean a Tweet by removing retweets, mentions, links, and other random symbols"""

    old_line_arr = line.split(' ')
    new_line_arr = []
    
    # FIXME: This may be inefficient and slow the program. May need to refactor later
    # Move this to the seed_database file so that the database has cleaned data to generate tweets
    # use this to check date of last fetch on Tweets too 
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


def make_bot_username(list_authors): 
    """Take in a list of author objects and return a new 'bot' fake username"""

    bot_name = []

    if len(list_authors) == 1:
        bot_name.extend(list_authors[0].name.split(' '))
        bot_name.append('bot')
    else:
        for author in list_authors[1:]:
            # extend bot_name with all last names
            # ex. Kim Kardashian West would extend with 'Kardashian West'
            bot_name.extend(author.name.split(' ')[1:])

        # insert first name of first author in list to the bot_name 
        bot_name[0:0] = [[list_authors[0].name.split(' ')[0]]]
    return '_'.join(bot_name).lower()


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
                new_tweet = clean_tweet(tweet_obj.text)
                markov.data(new_tweet)

        tweet = markov(max_length=40)
        # there are 6.1 chars on average in a word, Twitter's char limit is 280, 
        # so that makes for approx 45 words max in a tweet, rounding down to 40 for some margin
        
        tweet_obj = crud.create_ug_tweet(user=current_user, fav_status=False, text=tweet, authors=author_objs)

        return jsonify({'id': tweet_obj.ug_tweet_id, 'text': tweet_obj.text, 'bot-username': make_bot_username(tweet_obj.authors)})
    else:
        return ValueError('No Twitter accounts selected') 


def str_to_bool(string_val):
    """Take in a string of 'true' or 'false' and convert to Python boolean"""

    if string_val[0] == 'f':
        return False
    elif string_val[0] == 't':
        return True 


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


#################| Routes to Display Tweets |#################

@app.route('/get-tweets')
@login_required
def get_ug_tweets():
    """Return id and text for all Markov Tweets a user has generated"""

    tweets_text = []

    for tweet in current_user.tweets:

        tweets_text.append({'id': tweet.ug_tweet_id, 
                            'text': tweet.text,
                            'fav_status': tweet.fav_status}) 

    return jsonify(sorted(tweets_text, key = lambda i: i['id']))


@app.route('/favorites')
@login_required
def show_favorites():
    """Display favorite generated tweets"""

    return render_template('favorites.html')


@app.route('/toggle-fav', methods=['POST']) 
@login_required
def toggle_fav():
    """Toggle favorite status of a tweet"""

    tweet_id = request.form.get('id')
    clicked_tweet = UG_Tweet.query.get(tweet_id)
    clicked_tweet.fav_status = False if clicked_tweet.fav_status else True
    db.session.commit()

    return redirect('/generate') # TODO: Can also just remove return all together 


#################| Logout & Error Handler Routes |#################

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