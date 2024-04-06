
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
}


// dont add sidebar to push state
function showSiteHideOthers(site_to_show) {
  console.log(site_to_show);

  if (state.currPage === site_to_show)
    return ;

  const sites = ['gameSite', 'statsSite', 'homeSite', 'chat', 'profileSite', 'creatorsSite'];//gameSiteStart, gameSiteInvite, gameSitePlay, gameSiteEnd
  sites.forEach(site => {
    if (site === site_to_show) showDiv(site)
    else hideDiv(site)
  });
  state.currPage = site_to_show;
  // state.bodyText = document.body.innerHTML;

  handleButtonClick("");
}



function submitForm() {
  const img = document.getElementById('profilePictureInput')
  if (img.files && img.files[0]) {
      const file = img.files[0];
      const reader = new FileReader();
      reader.onload = function (e) {
        const imageData = e.target.result;
        const formData = new FormData();
        formData.append('avatar', file);
        // if response good, assign new image && display Image
        const url = `${window.location.origin}/user/upload/avatar/${websocket_obj.username}/`
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
          websocket_obj.avatar = imageData
          displayImagePreview(imageData);
        })
        .catch(error => {
            console.error('Error:', error);
        });
      };
    reader.readAsDataURL(file);
  }
}

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
