'use strict;';

// Display all existing tweets

const showTweets = (apiData) => {
	for (const tweet of apiData) {
		$('.tweets').append('<li>' + tweet + '</li>');
	}
};

$.get('/get-tweets', showTweets);

// On click, add another tweet to the list

$('#generate-tweet').on('click', (evt) => {
	evt.preventDefault();

	const makeTweet = (apiData) => {
		$('.tweets').append('<li>' + apiData + '</li>');
	};

	$.get('/markov', makeTweet);
});
