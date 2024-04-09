let state = { 
	bodyText: "notInit",
	currPage: "homeSite",
  chatObj: {},
  chatOpen: false,

  userName: null
  // groupChatName: "",
  //   idxState : 0
  // logedOut: false
};

let userLogedIn = true;
  
function render() {
  document.body.innerHTML = state.bodyText;
}
  
// (function initialize() {
//   if (state.bodyText === "notInit") {
//     state.bodyText = document.innerHTML;
//     window.history.replaceState(state, null, "");
//   }
//   render(state);
// })();

function handleButtonClick(url) {



  state.bodyText = document.body.innerHTML;
  state.userName = websocket_obj.username;

// state.currPage = url;
  window.history.pushState(state, null, url);
}
  
  
// Tell your browser to give you old state and re-render on back
window.onpopstate = async function (event) {
  console.log('onpopstate triggered')


  const url = `${window.location.origin}/user/token/existence`
 fetch(url)
  .then(async response => {
    if (!response.ok) {
      location.reload();
      throw new Error('Token could not be deleted!');
    }

    if (event.state)
      state = event.state;

    if (state.userName === websocket_obj.username) {
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
      if (state.currPage === 'invites')
        await requestInvites();
      
      render(state);
      if (state.currPage === 'chat') {
        hideDiv('messageSide');
        document.getElementById('right-heading-name').textContent = "";
        chat_avatar.src = "../img/ballWithEye.jpg";
      }
    }
    else {
      console.log('goes into else of popstate');
      // showSiteHideOthers('homeSite');
      showSiteHideOthersSpa('homeSite')
      state.bodyText = document.body.innerHTML;
      state.userName = websocket_obj.username;
      window.history.replaceState(state, null, "");
      render(state);
      // state.userName = websocket_obj.username;
    }
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });
};

function showSiteHideOthersSpa(site_to_show) {
  console.log(site_to_show);

  if (state.currPage === site_to_show)
    return ;

  const sites = ['gameSite', 'statsSite', 'homeSite', 'chat', 'profileSite', 'creatorsSite'];//gameSiteStart, gameSiteInvite, gameSitePlay, gameSiteEnd
  sites.forEach(site => {
    if (site === site_to_show) showDiv(site)
    else hideDiv(site)
  });
  state.currPage = site_to_show;
}

async function handleClickEvent(event) {
  // console.log(event);
	if (event.target.closest('#homeButton'))
		showSiteHideOthers('homeSite');
  else if (event.target.closest('#gameButton'))
      gameSiteClicked();
  else if (event.target.closest('#statsButton'))
		showSiteHideOthers('statsSite');
  else if (event.target.closest('#showChatButton'))
		await chatSiteClicked();
  else if (event.target.closest('#profileButton'))
		showSiteHideOthers('profileSite');
  else if (event.target.closest('#creatorsButton'))
		showSiteHideOthers('creatorsSite');
  else if (event.target.closest('#logoutButton'))
		await logoutUser();
  else if (event.target.closest('#renderInv'))
      invSiteClicked();
  else if (event.target.closest('#goBackToStart'))
    gameSiteClicked();
  else if (event.target.closest('#sendMessageButton'))
    await sendMessage();
  else if (event.target.closest('#invite_user_button')) {
      await inviteUserClicked();
	}
  else if (event.target.closest('#create_public_chat_button'))
		await createPublicChat()
  else if (event.target.closest('#create_private_chat_button'))
		await createPrivateChat() 
  else if (event.target.closest('#close_button_clicked_user')) {
      await closeButtonClicked();
  }
  else if (event.target.closest('#goToChatButton'))
    await openChat();
  else if (event.target.closest('#blockUserButton')) {
      await blockUserClicked();
  }
  else if (event.target.closest('#unblockUserButton')) {
      await unblockUserClicked();
	}
  else if (event.target.closest('#right-heading-name')) {
      await rightHeadingClicked();
	}
  else if (event.target.closest('#challengeUserToGame')) {
    await challengeUserClicked();
  }
  else if (event.target.closest('#loginUserButton'))
    loginUserButton();
  else if (event.target.closest('#RegisterUserButton'))
    RegisterUserButton();
  else if (event.target.closest('#changeToLoginPageButton'))
    changeToLoginPageButton();
  else if (event.target.closest('#changeToRegisterPageButton'))
    changeToRegisterPageButton();

  else if (event.target.closest('#Register42Button')) {
    // initUserData(data, usernameElement.value, passwordElement.value, 69)
    // showDiv('userIsAuth');
    // hideDiv('userIsNotAuth');
    // showDiv('homeSite');
    
    // state.bodyText = document.body.innerHTML;
    // window.history.replaceState(state, null, "");
    window.location.href = 'https://localhost/user/oauth2/login';
    // window.location.href = 'https://localhost/';
    // establishWebsocketConnection();
    // hideDiv('userIsNotAuth');
    // showDiv('userIsAuth');

    establishWebsocketConnection()
  }
}



// window.onpopstate = async function (event) {
//  	if (event.state)
// 		state = event.state;
//   console.log('onpopstate ######');
//   // if (!getJwtTokenFromCookie()) {
//   //   console.log('session over!!!!!!!!!!!');

   
//   //   // render(state);
//   //   location.reload();
//   //   return ;
//   //   // console.log('log out this user');
//   //   // await logoutUser();
//   // }
// 	// let stateJson = JSON.stringify(event.state);

// 	if (state.currPage === 'chat' || state.currPage === 'group_chat') {
// 		await sendDataToBackend('get_current_users_chats')
// 		await sendDataToBackend('get_blocked_by_user')
// 		await sendDataToBackend('get_blocked_user') // NEW since 02.02
//   }
// 	if (state.currPage === 'group_chat') {
//     if (state.chatOpen)
//       state.chatOpen = false;
//     else
//       state.chatOpen = true;
// 		await handleClickedOnChatElement(state.chatObj);
//   }
//   if (state.currPage === 'invites')
//     await requestInvites();

//   render(state);
//   if (state.currPage === 'chat') {
//     hideDiv('messageSide');
//     document.getElementById('right-heading-name').textContent = "";
//     chat_avatar.src = "../img/ballWithEye.jpg";
//   }
// // attachEventListeners();
// };