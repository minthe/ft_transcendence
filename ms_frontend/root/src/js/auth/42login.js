
let isFetching = false;

function openAuthPopup() {
	const url = `${window.location.origin}/user/oauth2/login`;
	const windowName = 'AuthWindow';
	const windowFeatures = `width=${window.outerWidth / 3},height=${window.outerHeight / 1.2}
	, left=${window.outerWidth / 2.85},top=${window.outerHeight / 9},resizable=yes`;
	const popup = window.open(url, windowName, windowFeatures);

	if (popup) {
		popup.focus();
		checkForToken(popup);
	}
	else
		alert('Please allow popups for this website.');
	// return popup;
}


function checkForToken(popup) {
	const url = `${window.location.origin}/user/login`
	const interval = setInterval(() => {
		if (popup.closed) {
			clearInterval(interval);
			return ;
		}
		if (!isFetching) {
			isFetching = true;
			fetch(url, {
				method: 'GET',
				headers: {
				'Content-Type': 'application/json',
				},
			})
			.then(async response => {
				const data = await response.json();
				
				//check again
				if (!response.ok && !data.second_factor) {
					if (response.status === 400 || response.status === 500) {
						popup.close();
						loginErrors(data);
					}
					await logoutUser();
					throw new Error('User has no token');

				}
				popup.close();
				if (data.second_factor) {
					setUpTwoFaPage();
					await verifyButtonClick();
					if (checkTwoFaCode()) {
						const url = `${window.location.origin}/user/2fa/verify`;

						return fetch(url, {
							method: 'POST',
							headers: headerTwoFa(),
							body: JSON.stringify(bodyTwoFa(data.user_id))
						})
						.then(async response => {
							if (!response.ok) {
								return response.json().then(data => {
									loginErrors(data);
								});
							}
							else {
								await afterAuthLogin42(data);
								setDownTwoFaPage();
							}
						});
					}
					data.message = 'Not enough digits or non numeric characters';
					loginErrors(data);
				}
				else
					await afterAuthLogin42(data);
				document.getElementById("reloadScreen").style.display = "block";
				setTimeout(function() {
				document.getElementById("reloadScreen").style.display = "none";
				hideDiv('userIsNotAuth');
				showDiv('userIsAuth');
				}, 500);
			})
			.catch(error => {
				clearLoginInput42();
				setDownTwoFaPage();
			})
			.finally(() => {
				isFetching = false;
			});
		}
		
	}, 2000);
}

async function afterAuthLogin42(data) {
	initUserData(data, data.username)
	authSucces();
	await getTwoFaStatus();
	clearLoginInput42();
}

function clearLoginInput42() {
	document.getElementById('loginUsername').value = "";
	document.getElementById('loginPassword').value = "";
	document.getElementById('twoFaCode').value = '';
}
