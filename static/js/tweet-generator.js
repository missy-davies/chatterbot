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

// Helper function to figure out which checkboxes are checked
const checkCheckboxes = () => {
	if ($('#elonmusk').is(':checked') && $('#kimkardashian').is(':checked')) {
		// execute AJAX request here
		$.post('/markov', { twitter_handles: ['elonmusk', 'kimkardashian'] });
	} else if ($('#kimkardashian').is(':checked')) {
		$.post('/markov', { twitter_handles: ['kimkardashian'] });
	} else if ($('#elonmusk').is(':checked')) {
		$.post('/markov', { twitter_handles: ['elonmusk'] });
	} else {
		// that means nothing is checked, so we should flash an error?
		alert('Please select at least one Twitter account');
	}
};

// On click, generate a new tweet and fully refresh the page of tweets
$('#generate-tweet').on('click', (evt) => {
	evt.preventDefault();

	$.get('/markov', function () {
		refreshTweets();
	});
	// add post request here to send data of which twitter accounts to use based on the checkCheckboxes function above?
});
