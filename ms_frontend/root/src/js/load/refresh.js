
async function updatePage() {

    if (userState.userName === websocket_obj.username) {

		if (userState.currPage === 'homeSite') {
			showSiteHideOthers('homeSite', 'homeButton');

			document.getElementById('displayUserName').innerHTML = 'Hey '+ websocket_obj.username +' 🫠';
		}
		else if (userState.currPage === 'gameSite')
			gameSiteClicked();
		else if (userState.currPage === 'profileSite') {
			//profileButtonClicked
			await getProfileData();
			await getTwoFaStatus();
			showSiteHideOthers('profileSite', 'profileButton')
		}
		else if (userState.currPage === 'creatorsSite')
			showSiteHideOthers('creatorsSite', 'creatorsButton');
		else if (userState.currPage === 'statsSite')
			statsSiteClicked();
		if (userState.currPage === 'chat' || userState.currPage === 'group_chat') {
			await sendDataToBackend('get_current_users_chats')
			await sendDataToBackend('get_blocked_by_user')
			await sendDataToBackend('get_blocked_user')
		  }
		if (userState.currPage === 'group_chat') {
		if (userState.chatOpen)
			userState.chatOpen = false;
		else
			userState.chatOpen = true;
		await handleClickedOnChatElement(userState.chatObj);
		}
		if (userState.currPage === 'invites')
			await requestInvites();
		if (userState.currPage === 'invitesTourn')
			await requestTourns();

		render(userState);
		if (userState.currPage === 'chat') {
			hideDiv('messageSide');
			document.getElementById('right-heading-name').textContent = "";
			// chat_avatar.src = "../img/ballWithEye.jpg";
		}
	}
	else {
		// showSiteHideOthers('homeSite');
		showSiteHideOthersSpa('homeSite');
		document.getElementById('displayUserName').innerHTML = 'Hey '+ websocket_obj.username +' 🫠';
		userState.bodyText = document.body.innerHTML;
		userState.userName = websocket_obj.username;
		window.history.replaceState(userState, null, "");
		render(userState);
	}
}

window.addEventListener('beforeunload', function(event) {
	const myData = {
		ws_obj: websocket_obj,
		ls_state: userState
	};

	localStorage.clear();
	localStorage.setItem('myData', JSON.stringify(myData));
})

window.addEventListener('load', function() {
	const myData = JSON.parse(localStorage.getItem('myData'));

	if (myData) {
		// localStorage.clear();
		websocket_obj = myData.ws_obj
		username = myData.ws_obj.username
		password = myData.ws_obj.password
		user_id = myData.ws_obj.user_id
		userState = myData.ls_state;
	}
	checkPageState();
});


function sillyLogin(username, password, user_id) {
	websocket_obj.username = username
	websocket_obj.password = password
	websocket_obj.user_id = user_id

	establishWebsocketConnection()
}

function checkPageState() {
	const url = `${window.location.origin}/user/token/existence`
	fetch(url, {
	method: 'GET',
	headers: {
		'Content-Type': 'application/json',
		'Authorization':'Bearer {access-token}'
	},
	})
	.then(async response => {
		if (!response.ok) {
			const data = await response.json();
			
			await logoutUser();
			userState.bodyText = document.body.innerHTML;
			// userState.currPage = "homeSite";
			userState.chatObj = {};
			userState.chatOpen = false;
			userState.userName = null;

			//problem of storing currPage from before maybe new var in userState needed
			if (userState.currPageNotLogedIn === null) {
				userState.currPageNotLogedIn = 'loginPage'
				window.history.replaceState(userState, null, "");
			}
			else if (userState.currPageNotLogedIn === 'loginPage'){
				showDiv('loginPage')
				hideDiv('registerPage')
				document.getElementById("wrong-register").classList.add("hidden");
				document.getElementById('registerUsername').value = null;
				document.getElementById('registerPassword').value  = null;
				document.getElementById("registerUsername").style.border = "";
				document.getElementById("registerPassword").style.border = "";
				
				
				// spaNotLogedIn('loginPage');
				// changeToLoginPageButton();
			}
			else if (userState.currPageNotLogedIn === 'registerPage') {
				hideDiv('loginPage')
				showDiv('registerPage')
				document.getElementById("wrong-password").classList.add("hidden");
				document.getElementById('loginUsername').value = null;
				document.getElementById('loginPassword').value  = null;
				document.getElementById("loginUsername").style.border = "";
				document.getElementById("loginPassword").style.border = "";
				
				// spaNotLogedIn('registerPage');
				// showRegisterPage();
			}
			// else
			// 	spaNotLogedIn(userState.currPage);
			throw new Error(data.message);
		}
		sillyLogin(websocket_obj.username, websocket_obj.password, websocket_obj.user_id)
		document.getElementById("reloadScreen").style.display = "block";
		setTimeout(function() {
			document.getElementById("reloadScreen").style.display = "none";
			hideDiv('userIsNotAuth');
			showDiv('userIsAuth');
			updatePage();
			setDownTwoFaPage();
		}, 500);
	})
	.catch(error => {
		console.error('Error during login:', error);
	});
}
