function verifyButtonClick() {
	return new Promise(resolve => {
		document.getElementById('verifyButton').addEventListener('click', () => {
			two_fa_code = document.getElementById('codeInput').value;
			resolve();
		});
	});
}
