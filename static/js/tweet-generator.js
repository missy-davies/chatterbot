'use strict;';

// helper function to add click listener to toggle heart color on a tweet and
// update database with new fav_status
const toggleHeart = () => {
	$('.heart').click(function () {
		$(this).toggleClass('heart-fav');

		$.post('/toggle-fav', { id: this.id });
	});
};

// Append all tweets to the box of tweets
const showTweets = (apiData) => {
	for (const tweet of apiData) {
		if (tweet.fav_status == true) {
			$('.tweets, .fav-tweets').prepend(
				`<div><div id="${tweet.id}" class="heart heart-fav">&hearts;</div><div class="tweet-package"><div class="botname">@${tweet.botname}</div><div>${tweet.text}</div></div></div>`
			);
		} else {
			$('.tweets').prepend(
				`<div><div id="${tweet.id}" class="heart">&hearts;</div><div class="tweet-package"><div class="botname">@${tweet.botname}</div><div>${tweet.text}</div></div></div>`
			);
		}
	}
	toggleHeart();
};

// Helper function to refresh all tweets on the page and then show them
const refreshTweets = () => {
	$('.tweets').empty();
	$.get('/get-tweets', showTweets);
};

refreshTweets();

// On click, generate a new tweet and fully refresh the page of tweets
// Pass in the selected twitter accounts as data
$('#generate-tweet').on('click', (evt) => {
	evt.preventDefault();

	// Only send request if at least one Twitter account is selected
	if (
		!$('#kimkardashian').is(':checked') &&
		!$('#elonmusk').is(':checked') &&
		!$('#britneyspears').is(':checked') &&
		!$('#justinbieber').is(':checked') &&
		!$('#ladygaga').is(':checked')
	) {
		alert('Oops, please select at least one Twitter account.');
	} else {
		let data = {
			kimkardashian: $('#kimkardashian').is(':checked'),
			elonmusk: $('#elonmusk').is(':checked'),
			britneyspears: $('#britneyspears').is(':checked'),
			justinbieber: $('#justinbieber').is(':checked'),
			ladygaga: $('#ladygaga').is(':checked'),
		};

		$.get('/markov', data, function (res) {
			if (res != null) {
				refreshTweets();
			}
		});
	}
});
