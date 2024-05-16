let emailBeforeEdit;
let gameAliasBeforeEdit;

//combine function with the one from twofa
function updateProfileMessage(success, message) {
	const twoFaStatus = document.getElementById('updateTwoFa');

	setTimeout(function() {
	twoFaStatus.classList.add('hidden');
	}, 3500);
	twoFaStatus.classList.remove('hidden');
	if (success)
		twoFaStatus.style.color = 'green';
	else
		twoFaStatus.style.color = 'red';
	twoFaStatus.textContent = message;
}


function editProfile() {
  emailBeforeEdit = document.getElementById('email').value;
  gameAliasBeforeEdit = document.getElementById('gameAlias').value;
  let inputs = document.querySelectorAll('input[readonly]');

  inputs.forEach(input => input.removeAttribute('readonly'));
  editButton.style.display = 'none';
  saveButton.style.display = 'block';
}

function saveChanges() {
  const mail = document.getElementById("email");
  const gameAlias = document.getElementById("gameAlias");
  if (containsSQLInjection(mail.value) || containsSQLInjection(gameAlias.value)) {
    console.log('are malicious for user profile')
    setTimeout(function () {
      document.getElementById('wrongSavedInput').classList.add('hidden');
    }, 3000);
    document.getElementById('wrongSavedInput').classList.remove('hidden');
    mail.value = emailBeforeEdit;
    gameAlias.value = gameAliasBeforeEdit;
    mail.setAttribute('readonly', true);
    gameAlias.setAttribute('readonly', true);
    editButton.style.display = 'block';
    saveButton.style.display = 'none';
    return ;
  }

  const url = `${window.location.origin}/user/profile`
  fetch (url, {
    method: 'PUT',
    header: headerProfileChange(),
    body: JSON.stringify(bodyProfileChange(mail.value, gameAlias.value))
  })
  .then(async response => {
    if (!response.ok) {
      const data = await response.json();
      throw Error(data.message);
    }
    updateProfileMessage(true, "Profile updated successfully");
  })
  .catch(error => {
    mail.value = emailBeforeEdit;
    gameAlias.value = gameAliasBeforeEdit;
    updateProfileMessage(false, error);
    console.error('There was a problem with the fetch operation:', error);
  });

  mail.setAttribute('readonly', true);
  gameAlias.setAttribute('readonly', true);
  editButton.style.display = 'block';
  saveButton.style.display = 'none';
}


//fetch to get picture, gamealias, mail
//fetch for new picture
//fetch for gameAlias and Mail


function changeProfileImage() {
  const profileImageInput = document.querySelector('.change-profile-image input[type="file"]');
  
  profileImageInput.addEventListener("change", function() {
    const file = this.files[0];


  if (file) {
    if (!file.type.startsWith('image/')) {
      setTimeout(function () {document.getElementById('fileError').style.display = 'none';}, 3000);
      document.getElementById('fileError').style.display = 'block';
      return;
    }
    // console.log('this is the file type: ', file.type);
    const reader = new FileReader();

    reader.readAsDataURL(file);
    reader.onload = function(e) {
      const dataURI = e.target.result;

    
      const url = `${window.location.origin}/user/avatar`
      fetch (url, {
        method: 'PUT',
        header: headerProfilePictureChange(),
        body: JSON.stringify(bodyProfilePictureChange(dataURI))
      })
      .then(async response => {
        const data = await response.json();
        if (!response.ok) {
          throw Error(data.message);
        }
        document.getElementById('profilePicture').src = data.avatar;
        updateProfileMessage(true, "Avatar updated successfully");
      })
      .catch(error => {
        updateProfileMessage(false, error);
        console.error('There was a problem with the fetch operation:', error);
      });


    };
  }
});
}



//needs to be called when clicked on profile page, traversing in spa or refresh
async function getProfileData() {
  const url = `${window.location.origin}/user/profile`
  fetch (url, {
    method: 'GET',
    // header: headerProfilePictureChange(),
  })
  .then(async response => {
    const data = await response.json();
    if (!response.ok)
      throw Error(data.message);
    console.log('data for profile: ', data);
    document.getElementById('profilePicture').src = data.avatar;
    document.getElementById("email").value = data.email;
    document.getElementById("gameAlias").value = data.alias;
    // updateProfileMessage(true, "Avatar updated successfully");
  })
  .catch(error => {
    // updateProfileMessage(false, error);
    console.error('There was a problem with the fetch operation:', error);
  });
}

async function profileButtonClicked() {
  await getTwoFaStatus();
  await getProfileData();
  document.getElementById('profileName').textContent = websocket_obj.username;
  showSiteHideOthers('profileSite', 'profileButton');
}

async function getProfilePicture(id) {
  let avatarUrl;
  const url = `${window.location.origin}/user/avatar?user_id=${id}`;
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: headerProfilePictureChange(),
    });
    const data = await response.json();
    console.log('data getting picture: ', data);
    if (!response.ok) {
      throw new Error(data.message);
    }
    avatarUrl = data.avatar;
    console.log("in fetch avatarUrl: ", avatarUrl);
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
  console.log("avatarUrl: ", avatarUrl);
  return avatarUrl;
}