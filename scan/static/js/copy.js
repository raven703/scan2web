function copyToClipboard(str) {
  let area = document.createElement('textarea');

  document.body.appendChild(area);
    area.value = str;
    area.select();
    document.execCommand("copy");
  document.body.removeChild(area);
}



$("#btnCopy").on("click", function(){
	let myUrl = $(location).attr('href')
   copyToClipboard(myUrl)

});

$("#submit").on("click", function (){
	$("#load").addClass("loader");

})


let source = new EventSource("/progress");
	source.onmessage = function(event) {
		$('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
		$('.progress-bar-label').text(event.data+'%');

		if(event.data == 100){
			source.close()
		}
	}