
function initUserData(data, username, password, age) {
	showDiv('userIsAuth')
	hideDiv('userIsNotAuth')
	websocket_obj.username = username
	websocket_obj.password = password
	// websocket_obj.age = age
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





// Function to open the popup | short prototype to test 2FA
function openPopup() {
    var textInput = prompt("Enter text:");

    if (textInput !== null) {
        // User clicked OK in the prompt
        return (submitText(textInput));
    } else {
        // User clicked Cancel in the prompt
        alert("No text entered.");
        return ""
    }
}
// Function to submit the text from the input field
function submitText(text) {
    if (text.trim() === "") {
        alert("Text cannot be empty.");
        return ""
    } else {
        // You can perform further actions with the submitted text here
        console.log("Submitted text:", text);
        return text
    }
}




function loginUserButton() {
	const usernameElement = document.getElementById('loginUsername')
  const passwordElement = document.getElementById('loginPassword')

  if (containsSQLInjection(usernameElement.value) || containsSQLInjection(passwordElement.value)) {
    usernameElement.value = "";
    passwordElement.value = "";
    document.getElementById("wrong-password").innerHTML = "Entered not allowed input!";
    return;
  }

  usernameElement.style.border = ""
  passwordElement.style.border = ""

  const inputBody = {
    "username": usernameElement.value,
    "password": passwordElement.value
  };
  const headers = {
    'Content-Type':'application/json',
    'Accept':'application/json'
  };
    
    // fetch(`${window.location.origin}/user/login/`,
    // {
    //   method: 'POST',
    //   body: inputBody,
    //   headers: headers
    // })
  

    // for testing purposes | delete later
    const email = 'marie.a.mensing@gmail.com'
    const enable2FA = true

    const url = `${window.location.origin}/user/login/`
    fetch(url, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(inputBody)
    })
      .then(response => {
        if (!response.ok) {
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
        document.getElementById("wrong-password").classList.add("hidden");
        return response.json();
      })
      .then(data => {
        // if 2FA enabled, render digit pop-up
        if (data.twoFactorAuth)
        {
          const code = openPopup();
          if (code.trim() !== "")
          {
            // verify in backend
            const url = `${window.location.origin}/game/verifyTwoFactorCode/${code}/${usernameElement.value}/`
            fetch(url)
            .then(async response => {
              if (!response.ok) {
                // location.reload();
                throw new Error('2FA Code was not correct!');
              }
              console.log("CORRECT 2FA CODE")
              initUserData(data, usernameElement.value, passwordElement.value, 69)
              showDiv('showUserProfile')
              document.getElementById('displayUserName').textContent = 'Hey '+websocket_obj.username+' 🫠';
              establishWebsocketConnection()
              state.bodyText = document.body.innerHTML;
              window.history.replaceState(state, null, "");
              usernameElement.value = "";
              passwordElement.value = "";
            })
            .catch(error => {
              console.error('There was a problem with the fetch operation:', error);
            });
          }
          else
          {
            throw new Error('Unexpected Error: Wrong 2FA Code')
          }
          return
        }


        initUserData(data, usernameElement.value, passwordElement.value, 69)
        showDiv('showUserProfile')
        document.getElementById('displayUserName').textContent = 'Hey '+websocket_obj.username+' 🫠';

        establishWebsocketConnection()
        state.bodyText = document.body.innerHTML;
        window.history.replaceState(state, null, "");
        usernameElement.value = "";
        passwordElement.value = "";
      })
      .catch(error => {
        usernameElement.value = "";
        passwordElement.value = "";
        // setErrorWithTimout('info_login', error, 9999999)
        console.log('Error during login:', error);
      });
}

function RegisterUserButton() {
	const usernameElement = document.getElementById('registerUsername')
    const passwordElement = document.getElementById('registerPassword')
    usernameElement.style.border = ""
    passwordElement.style.border = ""

    const mail = document.getElementById('registerMail');


    if (containsSQLInjection(usernameElement.value) || containsSQLInjection(passwordElement.value)
      || containsSQLInjection(mail.value)) {
      usernameElement.value = "";
      passwordElement.value = "";
      mail.value = "";
      document.getElementById("wrong-password").innerHTML = "Entered not allowed input!";
      return;
    }
    const inputBody = {
      "username": usernameElement.value,
      "password": passwordElement.value,
      "email": mail.value
    };
    const headers = {
      'Content-Type':'application/json',
      'Accept':'application/json'
    };
    
    const url = `${window.location.origin}/user/register/`;
    fetch(url,
    {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(inputBody)
    })
      .then(response => {
        if (!response.ok) {
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
        document.getElementById("wrong-register").classList.add("hidden");
        showDiv('loginPage');
        hideDiv('registerPage');
        return response.json();
      })
      .then(data => {
        initUserData(data, usernameElement.value, passwordElement.value, 69)
        showDiv('showUserProfile')
        document.getElementById('displayUserName').textContent = 'Hey '+websocket_obj.username+' 🫠';

        establishWebsocketConnection()
        state.bodyText = document.body.innerHTML;
        window.history.replaceState(state, null, "");
        usernameElement.value = "";
        passwordElement.value = "";
        mail.value = "";
      })
      .catch(error => {
        usernameElement.value = "";
        passwordElement.value = "";
        mail.value = "";
        // setErrorWithTimout('info_register', error, 9999999)
        console.log('Error during login:', error);
      });
}

function changeToLoginPageButton() {
	showDiv('loginPage')
    hideDiv('registerPage')
    document.getElementById("wrong-register").classList.add("hidden");
    document.getElementById('registerUsername').value = null;
    document.getElementById('registerAge').value  = null;
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

async function logoutUser() {
  const url = `${window.location.origin}/user/logout/`
  fetch(url)
  .then(response => {
    // if (!response.ok) { // Marie commented this cause it threw errors all the time lol
    //   throw new Error('Token could not be deleted!');
    // }
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

let codeTwoFa = "";

function moveToNextIfNumber(input, event) {
  // Remove non-numeric characters
  input.value = input.value.replace(/\D/g, '');

  // Check if the input value is a number
  if (!isNaN(parseInt(input.value))) {
    // Move focus to the next input field
    // codeTwoFa += input.stringify();
    codeTwoFa += input.value;
    console.log(codeTwoFa);
    if (input.nextElementSibling) {
      input.nextElementSibling.focus();
    }
  }
}
