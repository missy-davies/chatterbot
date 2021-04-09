'use strict;';

// Display all existing tweets

// FIXME: This currently reloads all tweets every time you visit the page
// in the future to optimize, this could save the tweets, then check for new ones
// to display instead
const showTweets = (apiData) => {
	for (const tweet of apiData) {
		$('.tweets').prepend(
			'<p>' + '<span class="heart">&hearts;</span>' + tweet + '</p>'
		);
	}
};

$.get('/get-tweets', showTweets);

// On click, generate another tweet and add to the list
$('#generate-tweet').on('click', (evt) => {
	evt.preventDefault();

	const makeTweet = (apiData) => {
		$('.tweets').prepend(
			'<p>' + '<span class="heart">&hearts;</span>' + apiData + '</p>'
		);
	};

	$.get('/markov', makeTweet);
});

// TODO: WORKING ON THIS NOW |
// on heart click also need to access the DB and change the fav_status attribute for the tweet
$('.heart').click(function () {
	$(this).toggleClass('heart-fav');
});

// Display all favorited tweets
const showFavTweets = (apiData) => {
	for (const tweet of apiData) {
		$('.fav-tweets').prepend(
			'<p>' + '<span class="heart-fav">&hearts;</span>' + tweet + '</p>'
		);
	}
};

$.get('/get-fav-tweets', showFavTweets);
