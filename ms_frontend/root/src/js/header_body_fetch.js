
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

function bodyTwoFa() {
	return {
		"user_id": websocket_obj.user_id,
		"code": websocket_obj.two_fa_code
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