'use strict;';

$('#generate-tweet').on('click', (evt) => {
	evt.preventDefault();

	const makeTweet = (apiData) => {
		$('.tweets').append('<li>' + apiData + '</li>');
	};

	$.get('/markov', makeTweet);
});
