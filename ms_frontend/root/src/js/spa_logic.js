let state = { 
	bodyText: "<div id=userIsNotAuth></div>",
	currPage: "home",
  chatObj: {},
  chatOpen: false,
  // groupChatName: "",
  //   idxState : 0
  // logedOut: false
};
  
function render() {
  document.body.innerHTML = state.bodyText;
}
  
// (function initialize() {
//   window.history.replaceState(state, null, "");
//   render(state);
// })();

function handleButtonClick(url) {



state.bodyText = document.body.innerHTML;

// state.currPage = url;
  window.history.pushState(state, null, url);
}



// Tell your browser to give you old state and re-render on back
window.onpopstate = async function (event) {
  console.log('onpopstate triggered')


//   const url = `${window.location.origin}/user/token/existence`
//  fetch(url)
//   .then(async response => {
//     if (!response.ok) {
//       location.reload();
//       throw new Error('Token could not be deleted!');
//     }

  if (event.state)
    state = event.state;
  updatePage();

  // })
  // .catch(error => {
  //   console.error('There was a problem with the fetch operation:', error);
  // });
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
		showSiteHideOthers('homeSite', 'homeButton');
  else if (event.target.closest('#gameButton'))
      gameSiteClicked();
  else if (event.target.closest('#statsButton'))
		showSiteHideOthers('statsSite', 'statsButton');
  else if (event.target.closest('#showChatButton'))
		await chatSiteClicked();
  else if (event.target.closest('#profileButton'))
		showSiteHideOthers('profileSite', 'profileButton');
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
  else if (event.target.closest('#challengeUserToGame')) {
    await challengeUserClicked();
  }
  else if (event.target.closest('#loginUserButton'))
    loginUserButton();
  else if (event.target.closest('#RegisterUserButton'))
    RegisterUserButton();
  else if (event.target.closest('#changeToLoginPageButton'))
    changeToLoginPageButton();
  else if (event.target.closest('#changeToRegisterPage'))
    showRegisterPage();
  else if (event.target.closest('#Register42Button'))
    registerWith42();

  else if (event.target.closest('#twoFAButtonE')) {
    enableTwoFactor();
  }
  else if (event.target.closest('#twoFAButtonD')) {
    disableTwoFactor();
  }

  // else if (event.target.closest('#login42UserButton'))
  //   loginWith42();
}



function enableTwoFactor() {
  document.getElementById('twoFAButtonE').classList.add('hidden');
  document.getElementById('twoFAButtonD').classList.remove('hidden');

  const url = `${window.location.origin}/user/2fa/update`
  fetch(url,
  {
    method: 'PUT',
    headers: headerEnableTwoFa(),
    body:  JSON.stringify(bodyEnableTwoFa())
  })
  .then(function(res) {
      return res.json();
  }).then(function(body) {
      console.log(body);
  });
}

function disableTwoFactor() {
  const url = `${window.location.origin}/user/2fa/update`;

  fetch(url, {
      method: 'PUT',
      headers: headerDisableTwoFa(),
      body: JSON.stringify(bodyDisableTwoFa())
  })
  .then(function(res) {
      if (res.status === 401) {
          document.getElementById('profilePanel').classList.add('hidden');
          document.getElementById('twoFAProfile').classList.remove('hidden');

          return fetch(url, { //enter url here
              method: 'Delete',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ action: 'reauthenticate' })
          })
          .then(function(secondRes) {
              // Check if the second fetch was successful
              if (!secondRes.ok) {
                  throw new Error(`Authentication failed: ${secondRes.status}`);
              }
              return secondRes.json();  // Assuming JSON response is expected
          });
      }
      return res.json();
  })
  .then(function(body) {
    document.getElementById('twoFAProfile').classList.add('hidden');
    document.getElementById('profilePanel').classList.remove('hidden');
    document.getElementById('twoFAButtonD').classList.add('hidden');
    document.getElementById('twoFAButtonE').classList.remove('hidden');
      // This will handle both responses from the initial and the reauthentication fetch
      console.log('Response received:', body);
  })
  .catch(function(error) {
      // This will catch errors from the initial fetch, the reauthentication fetch, or JSON parsing errors
      console.error('Error processing your request:', error);
  });

}


//change the header and body
function loginWith42() {
  const url = `${window.location.origin}/user/oauth2/login`
  fetch(url, {
    method: 'POST',
    headers: headerLogin(),
    // body: JSON.stringify(bodyLogin(usernameElement, passwordElement))
  })
  .then(async response => {
    if (!response.ok) {
      loginErrors(response)
    }
    document.getElementById("wrong-password").classList.add("hidden");
    return response.json();
  })
  .then(async data => {
    if (data.second_factor) {
      document.getElementById('twoFAButtonE').classList.add('hidden');
      document.getElementById('twoFAButtonD').classList.remove('hidden');

      setUpTwoFaPage();
      await verifyButtonClick();
      if (two_fa_code.length === 6) {  
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
          initUserData(data, usernameElement.value, passwordElement.value)
          authSucces();
          clearLoginInput(usernameElement, passwordElement);
          console.log("CORRECT 2FA CODE")
          setDownTwoFaPage();
        })
        .catch(error => {
          console.error('There was a problem with the fetch operation:', error);
          // document.getElementById('twoFA').classList.add('hidden');
          return ;//back to loginpage or 2fa page?
        });
      }
    }
    else {
      initUserData(data, usernameElement.value, passwordElement.value)
      authSucces();
      clearLoginInput(usernameElement, passwordElement);
    }

  })
  .catch(error => {
    clearLoginInput(usernameElement, passwordElement);
    // setErrorWithTimout('info_login', error, 9999999)
    console.log('Error during login:', error);
  });
}