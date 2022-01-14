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




