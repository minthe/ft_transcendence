
function initUserData(data, username, password) {
	showDiv('userIsAuth')
	hideDiv('userIsNotAuth')
	websocket_obj.username = username
	websocket_obj.password = password
	console.log('INIT USER DATA: USER_ID: ', data.user_id)
	websocket_obj.user_id = data.user_id


  document.getElementById('profileName').textContent = websocket_obj.username;
  // if (websocket_obj.game_alias)
  document.getElementById('gameAlias').value = websocket_obj.username;

  // document.getElementById("profilePicture").src = websocket_obj.profile_picture;

  if (getJwtTokenFromCookie()) {
		console.log('found token');
		// await establishWebsocketConnection();
	}
}


function clearLoginInput(usernameElement, passwordElement) {
  usernameElement.value = "";
  passwordElement.value = "";
}

function clearRegisterInput(usernameElement, passwordElement, mail) {
  usernameElement.value = "";
  passwordElement.value = "";
  mail.value = "";
}


function authSucces() {
  showDiv('showUserProfile')
  document.getElementById('displayUserName').textContent = 'Hey '+ websocket_obj.username +' 🫠';

  establishWebsocketConnection()
  state.bodyText = document.body.innerHTML;
  window.history.replaceState(state, null, "");
}

function loginErrors(response) {
  document.getElementById("wrong-password").classList.remove("hidden");
  switch (response.status) {
    case 404:
      document.getElementById("loginUsername").style.border = "1px solid red";
      document.getElementById("wrong-password").innerHTML = "This User does not exist!";
      throw new Error('This User does not exist!');
    case 401:
      document.getElementById("loginPassword").style.border = "1px solid red";
      document.getElementById("wrong-password").innerHTML = "Credentials are wrong!";
      throw new Error('Credentials are wrong!');
    default:
      document.getElementById("wrong-password").innerHTML = "Unexpected Error: Failed to check Credentials!";
      throw new Error('Unexpected Error: Failed to check Credentials')
  }
}

function registerErrors(response) {
  document.getElementById("wrong-register").classList.remove("hidden");
  switch (response.status) {
    case 409:
      document.getElementById("registerUsername").style.border = "1px solid red";
      document.getElementById("wrong-register").innerHTML = "This Username already exist!";
      throw new Error('This Username already exist')
    default:
      document.getElementById("wrong-register").innerHTML = "Unexpected Error: Failed to create new Account!";
      throw new Error('Unexpected Error: Failed to create new Account')
  }
}

function setUpTwoFaPage() {
  document.getElementById('loginHeader').classList.add('hidden');
  document.getElementById('loginPage').classList.add('hidden');
  document.getElementById('twoFA').classList.remove('hidden');
}

function loginUserButton() {
	const usernameElement = document.getElementById('loginUsername')
  const passwordElement = document.getElementById('loginPassword')

  usernameElement.style.border = ""
  passwordElement.style.border = ""

  if (containsSQLInjection(usernameElement.value) || containsSQLInjection(passwordElement.value)) {
    clearLoginInput(usernameElement, passwordElement);
    document.getElementById("wrong-password").innerHTML = "Entered not allowed input!";
    return;
  }  
    
    // for testing purposes | delete later
    const email = 'marie.a.mensing@gmail.com'
    const enable2FA = true

    const url = `${window.location.origin}/user/login`
    fetch(url, {
      method: 'POST',
      headers: headerLogin(),
      body: JSON.stringify(bodyLogin(usernameElement, passwordElement))
    })
    .then(async response => {
      if (!response.ok) {
        loginErrors(response)
      }
      document.getElementById("wrong-password").classList.add("hidden");
      return response.json();
    })
    .then(async data => {
      if (data.twoFactorAuth) {
        setUpTwoFaPage();
        await verifyButtonClick();
        if (websocket_obj.two_fa_code.length === 6) {   
          const url = `${window.location.origin}/user/2fa/verify`
          fetch(url, {
              method: 'POST',
              headers: headerTwoFa(),
              body: JSON.stringify(bodyTwoFa())
            })
          .then(async response => {
            if (!response.ok) {
              // location.reload();
              throw new Error('2FA Code was not correct!');
            }
            console.log("CORRECT 2FA CODE")
            document.getElementById('twoFA').classList.add('hidden');
          })
          .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            // document.getElementById('twoFA').classList.add('hidden');
            return ;//back to loginpage or 2fa page?
          });
        }
      }
      initUserData(data, usernameElement.value, passwordElement.value)
      authSucces();
      clearLoginInput(usernameElement, passwordElement);
    })
    .catch(error => {
      clearLoginInput(usernameElement, passwordElement);
      // setErrorWithTimout('info_login', error, 9999999)
      console.log('Error during login:', error);
    });
}

function RegisterUserButton() {
	const usernameElement = document.getElementById('registerUsername')
  const passwordElement = document.getElementById('registerPassword')
  const mail = document.getElementById('registerMail');

  usernameElement.style.border = ""
  passwordElement.style.border = ""
  mail.style.border = ""

  if (containsSQLInjection(usernameElement.value) || containsSQLInjection(passwordElement.value)
    || containsSQLInjection(mail.value)) {
      clearRegisterInput(usernameElement, passwordElement, mail);
    document.getElementById("wrong-password").innerHTML = "Entered not allowed input!";
    return;
  }

  
  const url = `${window.location.origin}/user/register`;
  fetch(url,
  {
    method: 'POST',
    headers: headerRegister(),
    body: JSON.stringify(bodyRegister(usernameElement, passwordElement, mail))
  })
  .then(response => {
    if (!response.ok) {
      registerErrors(response);
    }
    document.getElementById("wrong-register").classList.add("hidden");
    showDiv('loginPage'); //maybe not needed
    hideDiv('registerPage'); //maybe not needed
    return response.json();
  })
  .then(data => {
    initUserData(data, usernameElement.value, passwordElement.value)
    authSucces();
    clearRegisterInput(usernameElement, passwordElement, mail);
  })
  .catch(error => {
    clearRegisterInput(usernameElement, passwordElement, mail);
    // setErrorWithTimout('info_register', error, 9999999)
    console.log('Error during login:', error);
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
}

function openPopUpWin() {
	hideDiv('loginPage')
  document.getElementById('loginPagePopUp').classList.remove('hidden');
}

function showRegisterPage() {
  document.getElementById('loginPagePopUp').classList.add('hidden');
  showDiv('registerPage')
  document.getElementById("wrong-password").classList.add("hidden");
  document.getElementById('loginUsername').value = null;
  document.getElementById('loginPassword').value  = null;
  document.getElementById("loginUsername").style.border = "";
  document.getElementById("loginPassword").style.border = "";
}

function closePopUpWin() {
  document.getElementById('loginPagePopUp').classList.add('hidden');
  document.getElementById('loginPage').classList.remove('hidden');
}

function registerWith42() {
  window.location.href = '/user/oauth2/login';
  //window.location.href = ''; redirect back
  // if token true
  //   sillyLogin();
  //   establishWebsocketConnection();
  //   hideDiv('userIsNotAuth'); with delay if dom content needs to load
  //   showDiv('userIsAuth');
}



// user_logged_out:
// value: {"message": "User successfully logged out"}
// user_not_logged_in:
// value: {"message": "User was not logged in"}
async function logoutUser() {
  const url = `${window.location.origin}/user/logout`

  fetch(url,
  {
    method: 'POST',
    headers: headerLogout(),
  })
  .then(response => {
    if (!response.ok) { // Marie commented this cause it threw errors all the time lol
      throw new Error('Problems deleting the token!');
    }

    // let websocket_obj = null
    showDiv('userIsNotAuth')
    hideDiv('userIsAuth')
    document.cookie = 'test' + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    // state.logedOut = true;
    // userLogedIn = false;
    // websocket_obj.websocket.close();
    // return response.json();
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });
  // .then(data => {
  //   console.log(data); // Here you can handle the JSON data returned by the endpoint
  // })
}


function moveToNextIfNumber(input, event) {
  // Remove non-numeric characters
  input.value = input.value.replace(/\D/g, '');

  // Check if the input value is a number
  if (!isNaN(parseInt(input.value))) {
    websocket_obj.two_fa_code += input.value;
    console.log(codeTwoFa);
    if (input.nextElementSibling) {
      input.nextElementSibling.focus();
    }
  }
}
