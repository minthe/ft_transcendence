async function updatePage() {

    // if (state.userName === websocket_obj.username) {
		if (state.currPage === 'homeSite') {
			showSiteHideOthers('homeSite', 'homeButton');
			document.getElementById('displayUserName').innerHTML = websocket_obj.username;
		}
		else if (state.currPage === 'gameSite')
			gameSiteClicked();
		else if (state.currPage === 'profileSite') {
			//profileButtonClicked
			await getProfileData();
			await getTwoFaStatus();
			showSiteHideOthers('profileSite', 'profileButton')
		}
		else if (state.currPage === 'creatorsSite')
			showSiteHideOthers('creatorsSite', 'creatorsButton');
		else if (state.currPage === 'statsSite')
			showSiteHideOthers('statsSite', 'statsButton');
		if (state.currPage === 'chat' || state.currPage === 'group_chat') {
			await sendDataToBackend('get_current_users_chats')
			await sendDataToBackend('get_blocked_by_user')
			await sendDataToBackend('get_blocked_user') // NEW since 02.02
		  }
		if (state.currPage === 'group_chat') {
		if (state.chatOpen)
		state.chatOpen = false;
		else
		state.chatOpen = true;
		await handleClickedOnChatElement(state.chatObj);
		}
		if (state.currPage === 'invites') //refresh the invites
			await requestInvites();
		render(state);
		if (state.currPage === 'chat') {
		hideDiv('messageSide');
		document.getElementById('right-heading-name').textContent = "";
		chat_avatar.src = "../img/ballWithEye.jpg";
		}
		// }
		// else {
		//   console.log('goes into else of popstate');
		//   // showSiteHideOthers('homeSite');
		//   showSiteHideOthersSpa('homeSite')
		//   state.bodyText = document.body.innerHTML;
		//   state.userName = websocket_obj.username;
		//   window.history.replaceState(state, null, "");
		//   render(state);
		//   // state.userName = websocket_obj.username;
		// }
}



window.addEventListener('beforeunload', function(event) {
	const myData = {
		ws_obj: websocket_obj,
		bodyText: state.bodyText,
		currPage: state.currPage,
		chatObj: state.chatObj,
		chatOpen: state.chatOpen
	};
	localStorage.clear();
	localStorage.setItem('myData', JSON.stringify(myData));
})

window.addEventListener('load', function() {
	const myData = JSON.parse(localStorage.getItem('myData'));
	localStorage.clear();
	websocket_obj = myData.ws_obj
	username = myData.ws_obj.username
	password = myData.ws_obj.password
	user_id = myData.ws_obj.user_id

	state.bodyText = myData.bodyText;
	state.currPage = myData.currPage;
	state.chatObj = myData.chatObj;
	state.chatOpen = myData.chatOpen;

	// sillyLogin(websocket_obj.username, websocket_obj.password, websocket_obj.user_id)
	checkPageState();
});


function sillyLogin(username, password, user_id) {
	websocket_obj.username = username
	websocket_obj.password = password
	websocket_obj.age = 69
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
	// 'Authorization': `Basic ${btoa(`${usernameElement.value}:${passwordElement.value}`)}`
  },
//   body: JSON.stringify({ username: usernameElement.value, password: passwordElement.value })
})
  .then(async response => {
	if (!response.ok) {
		await logoutUser();
		state.bodyText = document.body.innerHTML;
		state.currPage = "homeSite";
		state.chatObj = {};
		state.chatOpen= false;
		throw new Error('User has no token');
	}
	  sillyLogin(websocket_obj.username, websocket_obj.password, websocket_obj.user_id)
	  document.getElementById("reloadScreen").style.display = "block";
	  setTimeout(function() {
		  document.getElementById("reloadScreen").style.display = "none";
		  hideDiv('userIsNotAuth');
		  showDiv('userIsAuth');
		  updatePage();
	  }, 500);
  })
  .catch(error => {
	console.log('Error during login:', error);
  });


	// if (getJwtTokenFromCookie()) {
	// 	hideDiv('userIsNotAuth');
	// 	document.getElementById("reloadScreen").style.display = "block";
	// 	setTimeout(function() {
	// 		document.getElementById("waitingScreen").style.display = "none";
	// 			updatePage();				
	// 	}, 500);
	// }
	// else {
	// 	state.bodyText = document.body.innerHTML;
	// 	state.currPage = "homeSite";
	// 	state.chatObj = {};
	// 	state.chatOpen= false;
	// }
}