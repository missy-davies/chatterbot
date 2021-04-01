"""Server for Markov chains Tweet generator app"""

from flask import Flask, render_template, request, flash, session, redirect

import jinja2

from model import connect_to_db

import crud


app = Flask(__name__)
app.secret_key = 'TEMPORARYKEY'


@app.route('/')
def show_homepage():
    """Display landing page with create account details."""
    
    # TODO: leave for later - check if user is in session, then bounce to login form or create account
    # user = crud.get_user_by_email(email)

    return render_template('create-account.html')

# TODO: Following routes need to check if user is in session, if they're not 
# then they should redirect to '/'


@app.route('/', methods=['POST'])
def register_user():
    """Create a new user."""

    fname = request.form.get('fname')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Oops, looks like an account already exists with that email! Please log in.')
        return redirect('/user-login')
    else:
        crud.create_user(fname, email, password)
        # TODO: add user to session!  
        flash("Hooray! You're all signed up. Go ahead and log in.")
        return redirect('/')
   

# @app.route('/log-in')
# def 

#     return render_template('log-in.html')

# @app.route('/user-login', methods=['POST'])
# def log_user_in():
#     """Logs user into their account."""

#     user = crud.get_user_by_email(request.form['email'])

#     password = request.form['password']

#     if user == None:
#         flash('''Oops, we couldn't find an account under that email address. 
#                 Please create a new account and try again!''')
#     elif password != user.password:
#         flash('Incorrect password. Please try again.')
#     else:
#         flash('Logged in!')
#         session['user-id'] = user.user_id

#     return redirect('/generate')
    

# TODO: Create route for user to log into account. Use dom manipulation to switch form. 

@app.route('/generate')
def show_tweet_generator():
    """Show tweet generator page and generate new tweets"""

    return render_template('generate.html')


@app.route('/favorites')
def show_favorites():
    """Display favorite generated tweets"""

    return render_template('favorites.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")