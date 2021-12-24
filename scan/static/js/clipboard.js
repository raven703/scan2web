let copyUrlBtn = document.querySelector('.copyToClipBoardBtn');

if (copyUrlBtn) {
	copyUrlBtn.addEventListener('click', () => {
		let tempInput = document.createElement('textarea');

		// tempInput.style.fontSize = '12pt';
		// tempInput.style.border = '0';
		// tempInput.style.padding = '0';
		// tempInput.style.margin = '0';
		// tempInput.style.position = 'absolute';
		// tempInput.style.left = '-9999px';
		// tempInput.setAttribute('readonly', '');

		tempInput.value = window.location.href;

		copyUrlBtn.parentNode.appendChild(tempInput);

		tempInput.select();
		tempInput.setSelectionRange(0, 99999);

		document.execCommand('copy');

		tempInput.parentNode.removeChild(tempInput);
	});
}
