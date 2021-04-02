'use strict;';

const generate = document.querySelector('#generate-tweet');

generate.addEventListener('click', () => {
	$.get('/route', (res) => {});

	document
		.querySelector('.tweets')
		.insertAdjacentHTML('beforeend', '<li>Tweet tweet!</li>');
});
