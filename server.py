"""Server for Markov chains Tweet generator app"""

from flask import Flask, render_template, request, flash, session, redirect

import jinja2


app = Flask(__name__)
app.secret_key = 'TEMPORARYKEY'


@app.route('/')
def show_homepage():
    """Display landing page."""

    return render_template('homepage.html')


# TODO: Create 'login' route 
# @app.route('/login')


# TODO: Create 'create account' route
# @app.route('/create-account')


@app.route('/generate')
def show_tweet_generator():
    """Show tweet generator page and generate new tweets"""

    return render_template('generate.html')


@app.route('/favorites')
def show_favorites():
    """Display favorite generated tweets"""

    return render_template('favorites.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")