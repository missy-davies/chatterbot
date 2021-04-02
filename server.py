"""Server for Markov chains Tweet generator app"""

from flask import Flask, render_template, request, flash, session, redirect

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import jinja2

from model import connect_to_db, User

import crud


app = Flask(__name__)
app.secret_key = 'TEMPORARYKEY'

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


@app.route('/favorites')
@login_required
def show_favorites():
    """Display favorite generated tweets"""

    return render_template('favorites.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()

    flash(f'See you later!')
    return redirect('/login')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")