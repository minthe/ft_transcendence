
function loginUserButton() {
	const usernameElement = getUsername();
  const passwordElement = getPassword();

  const url = `${window.location.origin}/user/login`
  fetch(url, {
    method: 'POST',
    headers: headerLogin(),
    body: JSON.stringify(bodyLogin(usernameElement, passwordElement))
  })
  .then(response => {
    return response.json().then(data => {
      return { ok: response.ok, status: response.status, data };
    });
  })
  .then(async ({ok, status, data}) => {
    if (!ok && status !== 401)
      loginErrors(data)
    document.getElementById("wrong-password").classList.add("hidden");
    if (data.second_factor) {
      setUpTwoFaPage();      
      await verifyButtonClick();
      if (checkTwoFaCode()) {
        const url = `${window.location.origin}/user/2fa/verify`
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

              await afterAuthLogin(data, usernameElement, passwordElement);
              setDownTwoFaPage();
          }
        });
      }
      data.message = 'Not enough digits or non numeric characters';
      loginErrors(data);
    }
    else
      await afterAuthLogin(data, usernameElement, passwordElement);
  })
  .catch(error => {
    setDownTwoFaPage();
    clearLoginInput(usernameElement, passwordElement);
  });
}





function showRegisterPage() {
  hideDiv('loginPage')
  showDiv('registerPage')
  document.getElementById("wrong-password").classList.add("hidden");
  document.getElementById('loginUsername').value = null;
  document.getElementById('loginPassword').value  = null;
  document.getElementById("loginUsername").style.border = "";
  document.getElementById("loginPassword").style.border = "";
  
  spaNotLogedIn('registerPage');

}

function getUsername() {
	const usernameElement = document.getElementById('loginUsername');
  
	usernameElement.style.border = "";
	return usernameElement;
}
  
function getPassword() {
	const passwordElement = document.getElementById('loginPassword');
  
	passwordElement.style.border = "";
	return passwordElement;
}

function clearLoginInput(usernameElement, passwordElement) {
	usernameElement.value = "";
	passwordElement.value = "";
	document.getElementById('twoFaCode').value = '';
}


async function afterAuthLogin(data, usernameElement, passwordElement) {
	initUserData(data, usernameElement.value)
	authSucces();
	await getTwoFaStatus();
	clearLoginInput(usernameElement, passwordElement);
}
