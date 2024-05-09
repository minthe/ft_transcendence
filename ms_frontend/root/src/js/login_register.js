
async function afterAuthLogin(data, usernameElement, passwordElement) {
  initUserData(data, usernameElement.value)
  authSucces();
  await getTwoFaStatus();
  clearLoginInput(usernameElement, passwordElement);
}

async function afterAuthRegister(data, usernameElement, passwordElement, mail) {
  initUserData(data, usernameElement.value)
  authSucces();
  await getTwoFaStatus();
  clearRegisterInput(usernameElement, passwordElement, mail);
}

async function afterAuthLogin42(data) {
  initUserData(data, data.username)
  authSucces();
  await getTwoFaStatus();
  clearLoginInput42();
}

function initUserData(data, username) {
	showDiv('userIsAuth')
	hideDiv('userIsNotAuth')

	websocket_obj.username = username


	console.log('INIT USER DATA: USER_ID: ', data.user_id)
	websocket_obj.user_id = data.user_id


  document.getElementById('profileName').textContent = websocket_obj.username;
  // if (!websocket_obj.game_alias)

  // document.getElementById('gameAlias').value = websocket_obj.username;

  // document.getElementById("profilePicture").src = websocket_obj.profile_picture;

}


function clearLoginInput(usernameElement, passwordElement) {
  usernameElement.value = "";
  passwordElement.value = "";
  document.getElementById('twoFaCode').value = '';
}

function clearRegisterInput(usernameElement, passwordElement, mail) {
  usernameElement.value = "";
  passwordElement.value = "";
  mail.value = "";
}

function clearLoginInput42() {
  document.getElementById('loginUsername').value = "";
  document.getElementById('loginPassword').value = "";
  document.getElementById('twoFaCode').value = '';
}


function authSucces() {
  showDiv('showUserProfile')
  document.getElementById('displayUserName').textContent = 'Hey '+ websocket_obj.username +' 🫠';

  establishWebsocketConnection()
  userState.userName = websocket_obj.username;
  userState.bodyText = document.body.innerHTML;
  // handleButtonClick("");

  if (userState.currPage === 'loginPage' || userState.currPage === 'RegisterPage')
    userState.currPage = 'homeSite'
  // window.history.go(-logedOutSpaCount);
  // logedOutSpaCount = 0;
  window.history.replaceState(userState, null, "");
}

function loginErrors(data) {
  document.getElementById("wrong-password").classList.remove("hidden");
  document.getElementById("wrong-password").textContent = data.message;
  throw new Error(data.message);
}

function registerErrors(data) {
  document.getElementById("wrong-register").classList.remove("hidden");
  document.getElementById("wrong-register").textContent = data.message;
  throw new Error(data.message);
}

function setUpTwoFaPage() {
  document.getElementById('loginHeader').classList.add('hidden');
  document.getElementById('loginPage').classList.add('hidden');
  document.getElementById('twoFA').classList.remove('hidden');
}

function setDownTwoFaPage() {
  document.getElementById('loginHeader').classList.remove('hidden');
  document.getElementById('loginPage').classList.remove('hidden');
  document.getElementById('twoFA').classList.add('hidden');
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

function loginUserButton() {
	const usernameElement = getUsername();
  const passwordElement = getPassword();

  if (sqlCheckLogin(usernameElement, passwordElement))
    return ;

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
                  console.log('that would be the error: ', data.message);
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
    console.log('Error during login:', error);
  });
}

function RegisterUserButton() {
  const usernameElement = getUsernameRegister();
  const passwordElement = getPasswordRegister();
  const mail = getMail();

  if (sqlCheckRegister(usernameElement, passwordElement, mail))
    return ;
  
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
  // spaNotLogedIn('loginPage');
}

function showRegisterPage() {
  hideDiv('loginPage')
  console.log("in the show function");
  showDiv('registerPage')
  document.getElementById("wrong-password").classList.add("hidden");
  document.getElementById('loginUsername').value = null;
  document.getElementById('loginPassword').value  = null;
  document.getElementById("loginUsername").style.border = "";
  document.getElementById("loginPassword").style.border = "";
  // spaNotLogedIn('registerPage');
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
    localStorage.clear();
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

let isFetching = false;

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
          await logoutUser();
          throw new Error('User has no token');
        }
        popup.close();
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
                console.log('after 2fa data: ', data);
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
        
        // console.log('Error during login:', error);
      })
      .finally(() => {
        isFetching = false;
      });
    }
    
  }, 2000);
}






