'use strict;';

// TODO: Fix this so it interacts properly with the server, gets the tweet and displays it
// and maybe can speed up the first fetch somehow?

$('#generate-tweet').on('click', () => {
	const makeTweet = (apiData) => {
		$('.tweets').append('<li>', apiData, '</li>');
	};

	$.get('/markov', makeTweet);
});
