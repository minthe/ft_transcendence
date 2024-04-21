
let two_fa_code = '';

function enableTwoFactor() {
	const url = `${window.location.origin}/user/2fa`
  
	changeToTwoFa();
	fetch(url, {
	  method: 'PUT',
	  headers: headerEnableTwoFa(),
	})
	.then(async function(response) {
	  if (response.status === 401) {
		await verifyButtonClick();
		if (checkTwoFaCode()) {
		  fetch(url, {
			method: 'POST',
			headers: headerTwoFa(),
			body: JSON.stringify(bodyTwoFa(websocket_obj.user_id))
		  })
		  .then(async responseTwoFa => {
			if (!responseTwoFa.ok)
			  throw new Error(!responseTwoFa.status);
		  });
		}
	  }
	  showTwoFaDisableBtn();
	  updateTwoFaStatus(true);
	})
	.catch(error => {
	  updateTwoFaStatus(false);
	  console.error('There was a problem with the fetch operation:', error);
	});
	changeToProfile();
}
  
function disableTwoFactor() {
	const url = `${window.location.origin}/user/2fa`;
	
	changeToTwoFa();
	fetch(url, {
		method: 'Delete',
		headers: headerDisableTwoFa(),
	})
	.then(async function(response) {
	  if (response.status === 401) {
		await verifyButtonClick();
		if (checkTwoFaCode()) {
		  fetch(url, {
			method: 'POST',
			headers: headerTwoFa(),
			body: JSON.stringify(bodyTwoFa(websocket_obj.user_id))
		  })
		  .then(function(responseTwoFa) {
			  if (!responseTwoFa.ok)
				  throw new Error(responseTwoFa.status);
		  });
		}
	  }
	  updateTwoFaStatus(true);
	  showTwoFaEnableBtn();
	})
	.catch(function(error) {
	  updateTwoFaStatus(false);
	  console.error('Error processing your request:', error);
	});
	changeToProfile();
}
  
function updateTwoFaStatus(success) {
	const twoFaStatus = document.getElementById('updateTwoFa');

	if (success) {
		setTimeout(function() {
		twoFaStatus.classList.add('hidden');
		}, 2500);
		twoFaStatus.classList.remove('hidden');
		twoFaStatus.style.color = 'green';
		twoFaStatus.value = 'Updated 2FA succesfully';
	}
	else {
		setTimeout(function() {
		twoFaStatus.classList.add('hidden');
		}, 2500);
		twoFaStatus.classList.remove('hidden');
		twoFaStatus.style.color = 'red';
		twoFaStatus.value = 'Failed to Update 2FA';
	}
}
  
  
function changeToTwoFa() {
	document.getElementById('profilePanel').classList.add('hidden');
	document.getElementById('twoFAProfile').classList.remove('hidden');
}

function changeToProfile() {
	document.getElementById('twoFAProfile').classList.add('hidden');
	document.getElementById('profilePanel').classList.remove('hidden');
}

function showTwoFaEnableBtn() {
	document.getElementById('twoFAButtonD').classList.add('hidden');
	document.getElementById('twoFAButtonE').classList.remove('hidden');
}

function showTwoFaDisableBtn() {
	document.getElementById('twoFAButtonE').classList.add('hidden');
	document.getElementById('twoFAButtonD').classList.remove('hidden');
}

function checkTwoFaCode() {
	if (two_fa_code.length !== 6)
		return false;
	for (let i = 0; i < two_fa_code.length; i++) {
		if (isNaN(parseInt(two_fa_code[i])))
		return false;
	}
	return true;
}
