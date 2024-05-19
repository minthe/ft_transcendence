
// BUTTON TO SEND MESSAGE IN CHAT
function addEventListenersIsAuth() {
  loadContentGame('html/game.html', 'gameSite');
  loadContentChat('html/chat.html', 'chat');
  loadContentProfile('html/profile.html', 'profileSite');
  loadStats('html/stats.html', 'statsSite');
  loadCreators('html/creators.html', 'creatorsSite');

  document.addEventListener('click', async function(event) {   
    handleClickEvent(event);
  });
  document.addEventListener('keypress', async function(event) {
    if (event.key === 'Enter') {//|| event.keyCode === 13
        event.preventDefault();
        if (await enterKeyEvent(event))
          return ;
        handleClickEvent(event);
      }
  });
}

async function enterKeyEvent(event) {
  if (event.target.closest('#changeToLoginPageButton') || event.target.closest('#changeToRegisterPage')
    || event.target.closest('#login42Button'))
    return false;
  if (!document.getElementById('loginPage').classList.contains('hidden')
    && !document.getElementById('userIsNotAuth').classList.contains('hidden')) {
    loginUserButton();
    return true;
  }
  else if (!document.getElementById('registerPage').classList.contains('hidden') 
    && !document.getElementById('userIsNotAuth').classList.contains('hidden')) {
    RegisterUserButton();
    return true;
  }
  else if (!document.getElementById('chat').classList.contains('hidden')
    && userState.chatOpen && !document.getElementById('sendMessageButton').disabled) {
    await sendMessage();
    return true;
  }
  else if (!document.getElementById('profileSite').classList.contains('hidden')
    && document.getElementById('saveButton').style.display !== 'none') {
    saveChanges();
    return true;
  }
  return false;
}


function showSiteHideOthers(site_to_show, btnToColor) {
  if (userState.currPage === site_to_show)
    return ;
  
  // userState.bodyText = document.body.innerHTML;
  changeCurrSite(site_to_show);
  changeCurrBtn(btnToColor);
  handleButtonClick("");
}

function changeCurrSite(site_to_show) {
  const sites = ['gameSite', 'statsSite', 'homeSite', 'chat', 'profileSite', 'creatorsSite'];//gameSiteStart, gameSiteInvite, gameSitePlay, gameSiteEnd
  sites.forEach(site => {
    if (site === site_to_show) showDiv(site)
    else hideDiv(site)
  });
  userState.currPage = site_to_show;
}

function changeCurrBtn(btnToColor) {  
  const buttons = ['profileButton', 'homeButton', 'showChatButton', 'statsButton', 'gameButton', 'creatorsButton'];
  buttons.forEach( button => {
    if (button === btnToColor)
      document.getElementById(button).style.backgroundColor = '#ef7267';
    else
      document.getElementById(button).style.backgroundColor = '#f8efb5';
  })
}



// function submitForm() {
//   const img = document.getElementById('profilePictureInput')
//   if (img.files && img.files[0]) {
//       const file = img.files[0];
//       const reader = new FileReader();
//       reader.onload = function (e) {
//         const imageData = e.target.result;
//         const formData = new FormData();
//         formData.append('avatar', file);
//         // if response good, assign new image && display Image
//         const url = `${window.location.origin}/game/upload/avatar/${websocket_obj.username}/`
//         fetch(url, {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => response.json())
//         .then(data => {
//           websocket_obj.avatar = imageData
//           displayImagePreview(imageData);
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
//       };
//     reader.readAsDataURL(file);
//   }
// }

function displayImagePreview(imageData) {
  document.getElementById('previewImage').src = imageData;
  document.getElementById('previewContainer').style.display = 'block';
}

function setErrorWithTimout(element_id, error_message, timout) {
  const obj = document.getElementById(element_id)
  obj.textContent = error_message;
  obj.style.display = 'block';
  obj.style.color = 'red'
  setTimeout(function() {
    obj.style.display = 'none';
  }, timout);
}

async function setMessageWithTimout(element_id, message, timout) {
  const obj = document.getElementById(element_id)
  obj.textContent = message;
  obj.style.display = 'block';
  obj.style.color = 'green'
  setTimeout(async function() {
    obj.style.display = 'none';
  }, timout);
}

function hideDiv(element_id) {
  document.getElementById(element_id).classList.add('hidden')
}

function showDiv(element_id) {
  document.getElementById(element_id).classList.remove('hidden')
}
