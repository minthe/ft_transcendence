
let two_fa_code = '';

function enableTwoFactor() {
	const url = `${window.location.origin}/user/2fa`
  
	changeToTwoFa();
	fetch(url, {
	  method: 'PUT',
	//   headers: headerEnableTwoFa()
	})
	.then(async function(response) {
	  if (response.ok) {
		await verifyButtonProfileClick();
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
	  changeToProfile();
	})
	.catch(error => {
	  updateTwoFaStatus(false);
	  changeToProfile();
	  console.error('There was a problem with the fetch operation:', error);
	});
	// changeToProfile();
}
  
function disableTwoFactor() {
	const url = `${window.location.origin}/user/2fa`;
	
	changeToTwoFa();
	fetch(url, {
		method: 'Delete',
		// headers: headerDisableTwoFa()
	})
	.then(async function(response) {
	  if (response.ok) {
		await verifyButtonProfileClick();
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
	  changeToProfile();
	})
	.catch(function(error) {
	changeToProfile();
	  updateTwoFaStatus(false);
	  console.error('Error processing your request:', error);
	});
	// changeToProfile();
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
	document.getElementById('profilePage').classList.add('hidden');
	document.getElementById('twoFAProfile').classList.remove('hidden');
}

function changeToProfile() {
	document.getElementById('twoFAProfile').classList.add('hidden');
	document.getElementById('profilePage').classList.remove('hidden');
	document.getElementById('twoFaCodeProfile').value = '';
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

function verifyButtonProfileClick() {
	return new Promise(resolve => {
		document.getElementById('verifyButtonProfile').addEventListener('click', () => {
			if (document.getElementById('userIsNotAuth').classList.contains('hidden'))
				two_fa_code = document.getElementById('twoFaCodeProfile').value;
			else
				two_fa_code = document.getElementById('twoFaCode').value;
			resolve();
		});
	});
}
