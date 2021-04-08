'use strict;';

// Display all existing tweets

// FIXME: This currently reloads all tweets every time you visit the page
// in the future to optimize, this could save the tweets, then check for new ones
// to display instead
const showTweets = (apiData) => {
	for (const tweet of apiData) {
		$('.tweets').append(
			'<p>' + '<span class="heart">&hearts;</span>' + tweet + '</p>'
		);
	}
};

$.get('/get-tweets', showTweets);

// On click, generate another tweet and add to the list
$('#generate-tweet').on('click', (evt) => {
	evt.preventDefault();

	const makeTweet = (apiData) => {
		$('.tweets').append(
			'<p>' + '<span class="heart">&hearts;</span>' + apiData + '</p>'
		);
	};

	$.get('/markov', makeTweet);
});

// TODO: WORKING ON THIS NOW, adapt to situation | on click, add tweet to favorites and change color of heart to red
// $('.heart').on('click', (evt) => {
// 	evt.preventDefault();

// 	$('.heart').removeClass('heart').addClass('heart-fav');
// });

// $('.heart').click(function () {
// 	$(this).toggleClass('.heart-fav');
// });

$('.heart').on('click', () => {
	alert('You clicked a heart class!');
});

// Display all favorited tweets
const showFavTweets = (apiData) => {
	for (const tweet of apiData) {
		$('.fav-tweets').append(
			'<p>' + '<span class="heart-fav">&hearts;</span>' + tweet + '</p>'
		);
	}
};

$.get('/get-fav-tweets', showFavTweets);
