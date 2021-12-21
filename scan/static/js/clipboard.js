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


[].map.call(document.querySelectorAll('[anim="ripple"]'), el=> {
    el.addEventListener('click',e => {
        e = e.touches ? e.touches[0] : e;
        const r = el.getBoundingClientRect(), d = Math.sqrt(Math.pow(r.width,2)+Math.pow(r.height,2)) * 2;
        el.style.cssText = `--s: 0; --o: 1;`;  el.offsetTop;
        el.style.cssText = `--t: 1; --o: 0; --d: ${d}; --x:${e.clientX - r.left}; --y:${e.clientY - r.top};`
    })
})


