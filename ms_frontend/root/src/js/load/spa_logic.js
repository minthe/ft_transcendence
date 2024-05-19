
let logedOutSpaCount = 0;

let userState = { 
  bodyText: "<div id=userIsNotAuth></div>",
  currPage: null,
  chatObj: {},
  chatOpen: false,
  userName: null,
  
  // tournId: null,
  currPageNotLogedIn: null
}
// groupChatName: "",
//   idxState : 0
// logedOut: false


  
function render() {
  document.body.innerHTML = userState.bodyText;
}
  
// (function initialize() {
//   window.history.replaceState(state, null, "");
//   render(state);
// })();

function handleButtonClick(url) {



  userState.bodyText = document.body.innerHTML;

// userState.currPage = url;
  window.history.pushState(userState, null, url);
}



window.onpopstate = async function (event) {
  console.log('onpopstate triggered')

  console.log(websocket_obj.game.active_state)
  console.log(websocket_obj.game)

  if (websocket_obj.game.active_state === true)
  {  console.log('You left the game!')
    console.log(websocket_obj.game.active_state)
    websocket_obj.game.active_state = false
    sendDataToBackend('user_left_game')
  }
  else
  {
    console.log('onpop ignored')

  }

  if (event.state)
    userState = event.state;

  const url = `${window.location.origin}/user/token/existence`
  fetch(url)
    .then(async response => {
      if (!response.ok) {
        const data = await response.json()
       
        location.reload();
        throw new Error(data.message);
      }
      updatePage();
    })
    .catch(error => {
      console.error('There was a problem showing the page:', error);
    });
};

function showSiteHideOthersSpa(site_to_show) {
  if (userState.currPage === site_to_show)
    return ;

  const sites = ['gameSite', 'statsSite', 'homeSite', 'chat', 'profileSite', 'creatorsSite'];
  sites.forEach(site => {
    if (site === site_to_show) showDiv(site)
    else hideDiv(site)
  });
  userState.currPage = site_to_show;
}

async function handleClickEvent(event) {
  const url = `${window.location.origin}/user/token/existence`

  if (event.target.closest('#loginUserButton'))
    loginUserButton();
  else if (event.target.closest('#RegisterUserButton'))
    RegisterUserButton();
  else if (event.target.closest('#changeToLoginPageButton'))
    changeToLoginPageButton();
  else if (event.target.closest('#changeToRegisterPage'))
    showRegisterPage();
  else if (event.target.closest('#login42Button'))
    openAuthPopup();
  
  else if (event.target.closest('#infoButton')) {
    document.getElementById('infoButton').classList.add('hidden');
    document.getElementById('passwordInfo').classList.remove('hidden');

    setTimeout(() => {
      document.getElementById('infoButton').classList.remove('hidden');
      document.getElementById('passwordInfo').classList.add('hidden');
    }, 5000);
  }
  
  fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization':'Bearer {access-token}'
    },
	})
	.then(async response => {
    if (!response.ok) {
      await logoutUser();
      const data = await response.json();
			userState.bodyText = document.body.innerHTML;
			// userState.currPage = "homeSite";
			userState.chatObj = {};
			userState.chatOpen = false;
			userState.userName = null;
			throw new Error(data.message);
		}
    
    
    if (event.target.closest('#homeButton'))
      showSiteHideOthers('homeSite', 'homeButton');
    else if (event.target.closest('#gameButton'))
      gameSiteClicked();
    else if (event.target.closest('#statsButton'))
      statsSiteClicked();
    else if (event.target.closest('#showChatButton'))
      await chatSiteClicked();
    else if (event.target.closest('#profileButton'))
      profileButtonClicked();
    else if (event.target.closest('#creatorsButton'))
      showSiteHideOthers('creatorsSite', 'creatorsButton');
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
    else if (event.target.closest('#challengeUserToTourn')) {
      await challengeTournClicked();
    }
    else if (event.target.closest('#challengeUserToGame')) {
      await challengeUserClicked();
    }
    else if (event.target.closest('#editButton'))
      editProfile();
    else if (event.target.closest('#saveButton'))
      saveChanges();
    else if (event.target.closest('#changeProfileImage'))
      changeProfileImage();
    
    else if (event.target.closest('#renderTourn')) {
      tournInvSiteClicked();
    }
    else if (event.target.closest('#twoFAButtonE'))
      updateTwoFactor('PUT');
    else if (event.target.closest('#twoFAButtonD'))
      updateTwoFactor('DELETE');
    
    else if (event.target.closest('#userStatsBtn'))
      statsBtnClicked();
    else if (event.target.closest('#userHistoryBtn'))
      historyBtnClicked();
    
  })
	.catch(error => {
    console.error('Error during login:', error);
	});
  
  
  
  
}



function spaNotLogedIn(site_to_show) {
  logedOutSpaCount++;
  userState.currPageNotLogedIn = site_to_show;
  handleButtonClick("");
  
  // if (site_to_show === 'registerPage')
  //   window.history.replaceState(userState, null, "");
  
}


