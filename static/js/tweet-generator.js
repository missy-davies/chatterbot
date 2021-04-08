'use strict;';

// Display all existing tweets

// FIXME: This currently reloads all tweets every time you visit the page
// in the future to optimize, this could save the tweets, then check for new ones
// to display instead
const showTweets = (apiData) => {
	for (const tweet of apiData) {
		$('.tweets').append(
			'<div>' + '<span class="heart">&hearts;</span>' + tweet + '</div>'
		);
	}
};

$.get('/get-tweets', showTweets);

// On click, generate another tweet and add to the list

$('#generate-tweet').on('click', (evt) => {
	evt.preventDefault();

	const makeTweet = (apiData) => {
		$('.tweets').append(
			'<div>' + '<span class="heart">&hearts;</span>' + apiData + '</div>'
		);
	};

	$.get('/markov', makeTweet);
});

// TODO: on click, add tweet to favorites and change color of heart to red
