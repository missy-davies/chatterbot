'use strict;';

// Display all existing tweets
const showTweets = (apiData) => {
	for (const tweet of apiData) {
		$('.tweets').prepend(
			`<p><span id="${tweet.id}" class="heart">&hearts;</span>${tweet.text}</p>`
		);
	}
	$('.heart').click(function () {
		$(this).toggleClass('heart-fav'); // separate from toggling the class, also do a call to the database, Ajax, make a change this.id
		// not sure if this is the right place for this info to go
		const tweetId = {
			id: this.id,
		};

		$.post('/toggle-fav', tweetId);
	});
};

$.get('/get-tweets', showTweets);

// On click, generate another tweet and add to the list
$('#generate-tweet').on('click', (evt) => {
	evt.preventDefault();

	const makeTweet = (apiData) => {
		$('.tweets').prepend(
			`<p><span id="${apiData.id}" class="heart">&hearts;</span>${apiData.text}</p>`
		);

		$('.heart').click(function () {
			$(this).toggleClass('heart-fav');
		});
	};
	$.get('/markov', makeTweet);
});

// TODO: Make sure this works to: Display all favorited tweets
const showFavTweets = (apiData) => {
	for (const tweet of apiData) {
		$('.fav-tweets').prepend(
			'<p>' + '<span class="heart-fav">&hearts;</span>' + tweet + '</p>'
		);
	}
};

$.get('/get-fav-tweets', showFavTweets);
