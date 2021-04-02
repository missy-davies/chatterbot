"""Server for Markov chains Tweet generator app"""

from flask import Flask, render_template, request, flash, session, redirect

import jinja2

from model import connect_to_db

import crud


app = Flask(__name__)
app.secret_key = 'TEMPORARYKEY'


@app.route('/')
def show_create_account():
    """Display landing page with create new account details"""

    if session['current_user']:
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
    
    if session['current_user']:
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
        session['current_user'] = user.user_id
        return redirect('/generate')


@app.route('/generate')
def show_tweet_generator():
    """Show tweet generator page and generate new tweets"""

    # TODO: Check if user is in session, if not then redirect to home 

    return render_template('generate.html')


@app.route('/favorites')
def show_favorites():
    """Display favorite generated tweets"""

    # TODO: Check if user is in session, if not then redirect to home 

    return render_template('favorites.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")