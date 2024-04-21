function verifyButtonClick() {
	return new Promise(resolve => {
		document.getElementById('verifyButton').addEventListener('click', () => {
			if (document.getElementById('userIsNotAuth').classList.contains('hidden'))
				two_fa_code = document.getElementById('twoFaCodeProfile').value;
			else
				two_fa_code = document.getElementById('twoFaCode').value;
			resolve();
		});
	});
}
