
async function afterAuthLogin(authMethod, data, usernameElement, passwordElement) {
  initUserData(data, usernameElement.value, passwordElement.value)
  authSucces();
  await getTwoFaStatus();
  if (authMethod === 'login')
    clearLoginInput(usernameElement, passwordElement);
}

async function afterAuthRegister(data, usernameElement, passwordElement, mail) {
  initUserData(data, usernameElement.value, passwordElement.value)
  authSucces();
  await getTwoFaStatus();
  clearRegisterInput(usernameElement, passwordElement, mail);
}

function initUserData(data, username, password) {
	showDiv('userIsAuth')
	hideDiv('userIsNotAuth')
	websocket_obj.username = username
	websocket_obj.password = password
	console.log('INIT USER DATA: USER_ID: ', data.user_id)
	websocket_obj.user_id = data.user_id
  websocket_obj.game.active_state = false



  document.getElementById('profileName').textContent = websocket_obj.username;
  // if (!websocket_obj.game_alias)

    document.getElementById('gameAlias').value = websocket_obj.username;

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


function authSucces() {
  showDiv('showUserProfile')
  document.getElementById('displayUserName').textContent = 'Hey '+ websocket_obj.username +' 🫠';

  establishWebsocketConnection()
  state.bodyText = document.body.innerHTML;
  window.history.replaceState(state, null, "");
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
                await afterAuthLogin('login', data, usernameElement, passwordElement);
                setDownTwoFaPage();
          }
      });
      }
      data.message = 'Not enough digits or non numeric characters';
      loginErrors(data);
    }
    else
      await afterAuthLogin('login', data, usernameElement, passwordElement);
  })
  .catch(error => {
    console.log('error for less digits activated thrice');

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
}

function showRegisterPage() {
  hideDiv('loginPage')
  console.log("in the show function");
  // document.getElementById('loginPagePopUp').classList.add('hidden');
  showDiv('registerPage')
  document.getElementById("wrong-password").classList.add("hidden");
  document.getElementById('loginUsername').value = null;
  document.getElementById('loginPassword').value  = null;
  document.getElementById("loginUsername").style.border = "";
  document.getElementById("loginPassword").style.border = "";
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











//change the header and body
// function loginWith42() {

//   console.log('inside login for 42 #####');

//   const url = `${window.location.origin}/user/oauth2/login`
//   fetch(url, {
//     method: 'POST',
//     headers: headerLogin(),
//     mode: 'no-cors'
//     // body: JSON.stringify(bodyLogin(usernameElement, passwordElement))
//   })
//   .then(async response => {
//     if (!response.ok) {
//       loginErrors(response)
//     }
//     document.getElementById("wrong-password").classList.add("hidden");
//     return response.json();
//   })
//   .then(async data => {
//     if (data.second_factor) {
//       document.getElementById('twoFAButtonE').classList.add('hidden');
//       document.getElementById('twoFAButtonD').classList.remove('hidden');

//       setUpTwoFaPage();
//       await verifyButtonClick();
//       if (two_fa_code.length === 6) {  
//         const url = `${window.location.origin}/user/2fa/verify`
//         fetch(url, {
//             method: 'POST',
//             headers: headerTwoFa(),
//             body: JSON.stringify(bodyTwoFa())
//           })
//         .then(async response => {
//           if (!response.ok) {
//             // location.reload();
//             throw new Error('2FA Code was not correct!');
//           }
//           afterAuthLogin('42Login', data);
//           console.log("CORRECT 2FA CODE")
//           setDownTwoFaPage();
//         })
//         .catch(error => {
//           console.error('There was a problem with the fetch operation:', error);
//           // document.getElementById('twoFA').classList.add('hidden');
//           return ;//back to loginpage or 2fa page?
//         });
//       }
//     }
//     else
//       afterAuth('42Login', data);

//   })
//   .catch(error => {
//     // setErrorWithTimout('info_login', error, 9999999)
//     console.log('Error during login:', error);
//   });
// }





function loginWith42() {

  const url = `${window.location.origin}/user/oauth2/login`
  fetch(url, {
    method: 'POST',
    headers: headerLogin(),
    // mode: 'no-cors'
    // body: JSON.stringify(bodyLogin(usernameElement, passwordElement))
  })
  .then(async response => {
    console.log('first then in 42 login###');
    return response.json().then(data => {
      return { ok: response.ok, status: response.status, data };
    });
  })
  .then(async ({ok, status, data}) => {
    console.log('before error detected');
    if (!ok && status !== 401) {
      console.log('error detected');
      loginErrors(data)
    }
    document.getElementById("wrong-password").classList.add("hidden");
    if (data.second_factor) {
      showTwoFaDisableBtn();
      setUpTwoFaPage();      
      await verifyButtonClick();
      if (checkTwoFaCode()) {
        const url = `${window.location.origin}/user/2fa`
        fetch(url, {
            method: 'POST',
            headers: headerTwoFa(),
            body: JSON.stringify(bodyTwoFa(data.user_id))
          })
        .then(response => {
          if (!response.ok) {
            // location.reload();
            throw new Error(response.data.message);
          }
          // afterAuthLogin('login42', data, usernameElement, passwordElement);
          setDownTwoFaPage();
        });
      }
    }
    // else
      // afterAuthLogin('login42', data, usernameElement, passwordElement);
  })
  .catch(error => {
    // clearLoginInput(usernameElement, passwordElement);
    // setErrorWithTimout('info_login', error, 9999999)
    console.log('Error during login:', error);
  });
}
