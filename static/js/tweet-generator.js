'use strict;';

// helper function to add click listener to toggle heart color on a tweet and
// update database with new fav_status
const toggleHeart = () => {
	$('.heart').click(function () {
		$(this).toggleClass('heart-fav');

		$.post('/toggle-fav.json', { id: this.id });
	});
};

// Append all tweets to the box of tweets
const showTweets = (apiData) => {
	for (const tweet of apiData) {
		if (tweet.fav_status == true) {
			$('.tweets, .fav-tweets').prepend(
				`<p><span id="${tweet.id}" class="heart heart-fav">&hearts;</span>${tweet.text}</p>`
			);
		} else {
			$('.tweets').prepend(
				`<p><span id="${tweet.id}" class="heart">&hearts;</span>${tweet.text}</p>`
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
	let data = {
		kimkardashian: $('#kimkardashian').is(':checked'),
		elonmusk: $('#elonmusk').is(':checked'),
	};

	$.get('/markov', data, function (res) {
		if (res != null) {
			refreshTweets();
		}
	});
});
