
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
		  return fetch(url, {
			method: 'POST',
			headers: headerTwoFa(),
			body: JSON.stringify(bodyTwoFa(websocket_obj.user_id))
		  })
		  .then(async responseTwoFa => {
			if (!responseTwoFa.ok) 
				return { twoFaUpdated: false};
			return { twoFaUpdated: true};
		  });
		}
	  }
	  return { twoFaUpdated: true};
	})
	.then(result => {
		if (!result.twoFaUpdated)
			throw Error("update failed");
		updateTwoFaStatus(true);
		showTwoFaDisableBtn();
		changeToProfile();
	})
	.catch(error => {
		changeToProfile();
		updateTwoFaStatus(false);
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
		  return fetch(url, {
			method: 'POST',
			headers: headerTwoFa(),
			body: JSON.stringify(bodyTwoFa(websocket_obj.user_id))
		  })
		  .then(function(responseTwoFa) {
			if (!responseTwoFa.ok)
				return { twoFaUpdated: false};
				//   throw new Error(responseTwoFa.status);
			return { twoFaUpdated: true};
		  });
		}
	  }
	  return { twoFaUpdated: true};
	})
	.then(result => {
		if (!result.twoFaUpdated)
			throw Error("update failed");
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
  
function updateTwoFaStatus(success, message) {
	const twoFaStatus = document.getElementById('updateTwoFa');

	// if (success) {
	setTimeout(function() {
	twoFaStatus.classList.add('hidden');
	}, 2500);
	twoFaStatus.classList.remove('hidden');
	if (success)
		twoFaStatus.style.color = 'green';
	else
		twoFaStatus.style.color = 'red';
	twoFaStatus.textContent = message;
	// }
	// else {
	// 	setTimeout(function() {
	// 	twoFaStatus.classList.add('hidden');
	// 	}, 2500);
	// 	twoFaStatus.classList.remove('hidden');
	// 	twoFaStatus.style.color = 'red';
	// 	twoFaStatus.textContent = 'Failed to Update 2FA';
	// }
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


//needs to be added in login, refresh and spa logic
async function getTwoFaStatus() {
	const url = `${window.location.origin}/user/2fa`

	fetch(url, {
		method: 'GET'
	})
	.then(async response => {
		return response.json().then(data => {
			return { ok: response.ok, data};
		});
	})
	.then(async result => {
		if (!result.ok)
			throw Error(result.data.message);
		if (response.data.second_factor)
			showTwoFaDisableBtn();
		else
			showTwoFaEnableBtn();
	})
	.catch(error => {
		console.log('Get 2fa status error: ', error);
	})
}








function updateTwoFactor(correctMethod) {
	const url = `${window.location.origin}/user/2fa`
  
	changeToTwoFa();
	fetch(url, {
	  method: 'POST',
	//   headers: headerEnableTwoFa()
	})
	.then(async function(response) {
	  if (response.ok) {
		await verifyButtonProfileClick();
		if (checkTwoFaCode()) {
		  return fetch(url, {
			method: correctMethod,
			headers: headerUpdateTwoFa(),
			body: JSON.stringify(bodyUpdateTwoFa())
		  })
		  .then(async responseTwoFa => {
			if (!responseTwoFa.ok) 
				return { twoFaUpdated: false, message: response.message};
			return { twoFaUpdated: true, message: 'Updated 2FA succesfully'};
		  });
		}
	  }
	  return { twoFaUpdated: false, message: response.message};
	})
	.then(async result => {
		if (!result.twoFaUpdated)
			throw Error(result.message);
		updateTwoFaStatus(true, result.message);
		await getTwoFaStatus();
		changeToProfile();
	})
	.catch(error => {
		changeToProfile();
		updateTwoFaStatus(false, result.message);
		console.error('There was a problem with the fetch operation:', error);
	});
	// changeToProfile();
}