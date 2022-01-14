let source = new EventSource("/progress");

source.onmessage = function(event) {
	let queries = $.parseJSON(event.data)
	let current = queries["current"]
	let max_num = queries["max"]

	$('.progress-bar').css('width', current + '%').attr('aria-valuenow', current);
	$('.progress-bar-label').text(current +'%');

	console.log("New message", queries["max"], queries["current"])

	}