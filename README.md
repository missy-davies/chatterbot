## Project Proposal

### Overview

An app where users can generate psueudo Tweets from Elon Musk's Twitter profile using the concept of Markov chains.

### Technologies required (besides typical Hackbright tech stack)

- Twitter API
- [Tweepy library](https://www.tweepy.org/) (make using Twitter API easy)
- [Markov Chain library](https://github.com/dead-beef/markovchain) (hard lifting of Markov chain work is done here)
- [Demoji library](https://pypi.org/project/demoji/) (clean strings and remove emojis, characters, and otherwise)

### APIs
- [Twitter offers an API](https://developer.twitter.com/en/portal/products) where you can make:
    - 900 request / 15 min PER USER AUTH
    - 300 request / 15 min PER APP AUTH
- I will query that to pull a public user's tweets.
- I will also use the [Tweepy](https://www.tweepy.org/) library to help facilitate using the Twitter API.
- Website digram and user flow ideas [here](https://miro.com/app/board/o9J_lNxBVfs=/)

### Data
Drafting data model [here](https://dbdiagram.io/d/60622ab3ecb54e10c33dd1f7)

User Data:
- Name
- Email 
- Password
- Favorite Tweets

Twitter Data (temporarily store the original tweets, need to expire old chain):
- store Tweets for a select few famous folks (Musk to start), will need to query to get all Tweets then have it maintained every month or so
    - need 280 character string output
- Favorited generated tweets by user

### Flow Diagram
Drafting [here](https://miro.com/app/board/o9J_lNxBVfs=/)

### Roadmap

#### MVP

A Markov tweet generator that pulls all tweets from Elon Musk's profile (to start) then parses the info into a string, and generate a 280 character pseudo tweet.

Users can create and log into accouts to save generated Tweets to their 'favorites'. 

#### 2.0

- Make the UI really nice, minimal but beautiful using Bootstrap
- Add a second option to create pseudo tweets (Kim Kardashian)
- Allow option to mosh together 2 pre-querried Twitter accounts

#### 3.0

- Allow users to search for any public Twitter 
- Login in / [create account with Twitter](https://developer.twitter.com/en/docs/authentication/overview)
- Allow users to select second pre-filled funky text to create mashup generated tweet
- Ability to download favorited Tweets in a CSV file 
- Add tour tips? 
