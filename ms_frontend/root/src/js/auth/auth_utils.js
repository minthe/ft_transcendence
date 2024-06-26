
function initUserData(data, username) {
	showDiv('userIsAuth')
	hideDiv('userIsNotAuth')
	websocket_obj.username = username
	websocket_obj.user_id = data.user_id
  document.getElementById('profileName').textContent = websocket_obj.username;
}

//test

async function authSucces() {
  showDiv('showUserProfile')
  document.getElementById('displayUserName').textContent = 'Hey '+ websocket_obj.username +' 🫠';

  establishWebsocketConnection()
  userState.userName = websocket_obj.username;
  userState.bodyText = document.body.innerHTML;


  // handleButtonClick("");

  // if (userState.currPage === 'loginPage' || userState.currPage === 'RegisterPage')
  //   userState.currPage = 'homeSite'
  window.history.go(-logedOutSpaCount);
  logedOutSpaCount = 0;
  userState.currPageNotLogedIn = null;
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
  if (document.getElementById('loginHeader'))
   document.getElementById('loginHeader').classList.remove('hidden');
  if (document.getElementById('loginPage'))
   document.getElementById('loginPage').classList.remove('hidden');
  if (document.getElementById('twoFA'))
   document.getElementById('twoFA').classList.add('hidden');
}
