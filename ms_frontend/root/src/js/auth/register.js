
function RegisterUserButton() {
	const usernameElement = getUsernameRegister();
	const passwordElement = getPasswordRegister();
	const mail = getMail();
	
	const url = `${window.location.origin}/user/register`;
	fetch(url,
	{
	  method: 'POST',
	  headers: headerRegister(),
	  body: JSON.stringify(bodyRegister(usernameElement, passwordElement, mail))
	})
	.then(response => {
	  return response.json().then(data => {
		return { ok: response.ok, data };
	  });
	})
	.then(async ({ ok, data }) => {
	  if (!ok) {
		  registerErrors(data);
	  }
	  document.getElementById("wrong-register").classList.add("hidden");
	  showDiv('loginPage'); //maybe not needed
	  hideDiv('registerPage'); //maybe not needed
	  await afterAuthRegister(data, usernameElement, passwordElement, mail);
	  // return response.json();
	})
	.catch(error => {
	  clearRegisterInput(usernameElement, passwordElement, mail);
	});
}

function changeToLoginPageButton() {
	showDiv('loginPage')
  hideDiv('registerPage')
  document.getElementById("wrong-register").classList.add("hidden");
  document.getElementById('registerUsername').value = null;
  document.getElementById('registerPassword').value  = null;
  document.getElementById("registerUsername").style.border = "";
  document.getElementById("registerPassword").style.border = "";
  
  
  spaNotLogedIn('loginPage');

}


function getUsernameRegister() {
	const usernameElement = document.getElementById('registerUsername');
  
	usernameElement.style.border = "";
	return usernameElement;
}
  
function getPasswordRegister() {
	const passwordElement = document.getElementById('registerPassword');
  
	passwordElement.style.border = "";
	return passwordElement;
}
  
function getMail() {
	const mail = document.getElementById('registerMail');
  
	mail.style.border = "";
	return mail;
}

function clearRegisterInput(usernameElement, passwordElement, mail) {
	usernameElement.value = "";
	passwordElement.value = "";
	mail.value = "";
}

async function afterAuthRegister(data, usernameElement, passwordElement, mail) {
	initUserData(data, usernameElement.value)
	authSucces();
	await getTwoFaStatus();
	clearRegisterInput(usernameElement, passwordElement, mail);
}
