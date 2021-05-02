# ChatterBot
## Overview
ChatterBot is a web app that allows users to generate parody Tweets based 
on celebrity Twitter accounts using a Markov chain algorithm. Users can select
1-5 celebs from a pre populated list to mash together the voices of multiple 
personalities for more fun. Users can also "like" any Tweet to add it to their 
'Favorites'. 

ChatterBot is built with Python Flask on the backend with a PostgrSQL database,
and Javascript/jQuery on the frontend along with HTML/CSS and Bootstrap. 

## Features 
#### Create Account / Login 
Users can create / login to an account using the homepage widget.
![Create Account and Login](/static/img/create-account.gif)

#### Generate Tweets 
Users can select any number of celebrities from the provided list - then click 
'Generate' and a new Tweet will appear. Tweets are created by mixing together 
hundreds of original Tweets from the chosen celebrities' real Twitter accounts 
with a Markov chain algorithm. Selecting more than 1 celeb creates a mashup Tweet. 
![Generate Tweets](/static/img/generate-tweets.gif)

#### Favorite Tweets
Users can favorite parody Tweets by clicking the heart 
![Favorite Tweets](/static/img/favorite-tweets.gif)

#### Manage Favorite Tweets 
Users can view and manage their Favorite tweets.
![View Favorite Tweets](/static/img/view-favorites.gif)

### Technologies
Languages:
- Python 3
- JavaScript (AJAX, JSON)
- HTML
- CSS

Frameworks & Libraries:
- Flask
- Flask-Login
- Jinja
- jQuery
- Bootstrap 
- Tweepy'
- Markov Chain

Database:
 - PostgreSQL / SQLAlchemy

APIs:
- Twitter API 

#### Coming Soon...
A few ideas of features to add in the future: 
- Allow users to search for any public Twitter rather than from pre-populated list 
- Login in / [create account with Twitter](https://developer.twitter.com/en/docs/authentication/overview)
- Ability to download favorited Tweets in a CSV file 
- Allow users to auto-publish tweets 