
function bodyLogin(usernameElement, passwordElement) {
	return {
		"username": usernameElement.value,
		"password": passwordElement.value
	};
}

function headerLogin() {
	return {
		'Content-Type':'application/json',
		'Accept':'application/json'
	};
}

function bodyTwoFa(user_id) {
	return {
		"user_id": user_id,
		"code": two_fa_code
	};
}

function headerTwoFa() {
	return {
		'Content-Type':'application/json',
		'Accept':'application/json'
	};
}

function bodyRegister(usernameElement, passwordElement, mail) {
	return {
		"username": usernameElement.value,
		"password": passwordElement.value,
		"email": mail.value
	};
}

function headerRegister() {
	return {
		'Content-Type':'application/json',
		'Accept':'application/json'
	};
}

function headerLogout() {
	return {
		'Accept':'application/json',
  		'Authorization':'Bearer {access-token}'
	};
}

function headerEnableTwoFa() {
	return {
		'accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization':'Bearer {access-token}'
	};
}

function bodyEnableTwoFa() {
	return {
		"second_factor": true
	};
}

function headerDisableTwoFa() {
	return {
		'accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization':'Bearer {access-token}'
	};
}

function bodyDisableTwoFa() {
	return {
		"second_factor": false
	};
}
