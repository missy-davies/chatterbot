'use strict;';
// MISSY'S NEW REFACTORED CODE

const showTweets = (apiData) => {
	$('.tweets').empty();
	for (const tweet of apiData) {
		if (tweet.fav_status == true) {
			$('.tweets').prepend(
				`<p><span id="${tweet.id}" class="heart heart-fav">&hearts;</span>${tweet.text}</p>`
			);
		} else {
			$('.tweets').prepend(
				`<p><span id="${tweet.id}" class="heart">&hearts;</span>${tweet.text}</p>`
			);
		}
	}
	$('.heart').click(function () {
		$(this).toggleClass('heart-fav');

		$.post('/toggle-fav.json', { id: this.id });
	});
};

const refreshTweets = () => {
	$.get('/get-tweets', showTweets);
};

refreshTweets();

$('#generate-tweet').on('click', (evt) => {
	evt.preventDefault();

	$.get('/markov', function () {
		refreshTweets();
	});
});

// OLD SPAGHETTI CODE
// TODO: On some tweets, the favoriting function doesn't work properly. Sometimes you can't click the button if you nav away from the page
// Display all existing tweets
// const showTweets = (apiData) => {
// 	for (const tweet of apiData) {
// 		if (tweet.fav_status == true) {
// 			$('.tweets').prepend(
// 				`<p><span id="${tweet.id}" class="heart heart-fav">&hearts;</span>${tweet.text}</p>`
// 			);
// 		} else {
// 			$('.tweets').prepend(
// 				`<p><span id="${tweet.id}" class="heart">&hearts;</span>${tweet.text}</p>`
// 			);
// 		}
// 	}
// 	$('.heart').click(function () {
// 		$(this).toggleClass('heart-fav');

// 		$.post('/toggle-fav.json', { id: this.id });
// 	});
// };

// $.get('/get-tweets', showTweets);

// On click, generate another tweet and add to the list
// $('#generate-tweet').on('click', (evt) => {
// 	evt.preventDefault();

// 	const makeTweet = (apiData) => {
// 		$('.tweets').prepend(
// 			`<p><span id="${apiData.id}" class="heart">&hearts;</span>${apiData.text}</p>`
// 		);

// 		$('.heart').click(function () {
// 			$(this).toggleClass('heart-fav');

// 			$.post('/toggle-fav.json', { id: this.id });
// 		});
// 	};
// 	$.get('/markov', makeTweet);
// });

// Display all favorited tweets where on click you can unfavorite them
// const showFavTweets = (apiData) => {
// 	for (const tweet of apiData) {
// 		$('.fav-tweets').prepend(
// 			`<p><span id="${tweet.id}" class="heart heart-fav">&hearts;</span>${tweet.text}</p>`
// 		);
// 	}
// 	$('.heart').click(function () {
// 		$(this).toggleClass('heart-fav');
// 		$.post('/toggle-fav.json', { id: this.id });
// 	});
// };

// $.get('/get-fav-tweets', showFavTweets);
