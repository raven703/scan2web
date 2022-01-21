let chartData2 = ['test']
let chartLabels2 =0




let source = new EventSource("/progress");

	source.onmessage = function (event) {

		let queries = $.parseJSON(event.data)
		let current = queries["current"]
		let max_num = queries["max"]

		let chartData = queries["c_data"]
		let chartLabels = queries["labels"]



		$('.progress-bar').css('width', current + '%').attr('aria-valuenow', current);
		$('.progress-bar-label').text(current + '%');

		console.log("ESI queries", queries["max"], queries["current"])

		chartData2 = chartData
		  console.log("inside event chartData2 from progress.js:", chartData2)

	}

	console.log("outside event func data2 from progress.js", chartData2)
