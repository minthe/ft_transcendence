let emailBeforeEdit;
let gameAliasBeforeEdit;

//combine function with the one from twofa
// function updateProfileMessage(success, message) {
// 	const twoFaStatus = document.getElementById('updateTwoFa');

// 	setTimeout(function() {
// 	twoFaStatus.classList.add('hidden');
// 	}, 3500);
// 	twoFaStatus.classList.remove('hidden');
// 	if (success)
// 		twoFaStatus.style.color = 'green';
// 	else
// 		twoFaStatus.style.color = 'red';
// 	twoFaStatus.textContent = message;
// }


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
  // if (containsSQLInjection(mail.value) || containsSQLInjection(gameAlias.value)) {
  //   console.log('are malicious for user profile')
  //   setTimeout(function () {
  //     document.getElementById('wrongSavedInput').classList.add('hidden');
  //   }, 3000);
  //   document.getElementById('wrongSavedInput').classList.remove('hidden');
  //   mail.value = emailBeforeEdit;
  //   gameAlias.value = gameAliasBeforeEdit;
  //   mail.setAttribute('readonly', true);
  //   gameAlias.setAttribute('readonly', true);
  //   editButton.style.display = 'block';
  //   saveButton.style.display = 'none';
  //   return ;
  // }

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
    updateTwoFaStatus(true, "Profile updated successfully");
  })
  .catch(error => {
    mail.value = emailBeforeEdit;
    gameAlias.value = gameAliasBeforeEdit;
    updateTwoFaStatus(false, error);
  });

  mail.setAttribute('readonly', true);
  gameAlias.setAttribute('readonly', true);
  editButton.style.display = 'block';
  saveButton.style.display = 'none';
}

function changeProfileImage() {
  const profileImageInput = document.querySelector('.change-profile-image input[type="file"]');
  
  profileImageInput.addEventListener("change", function() {
    const file = this.files[0];


    if (file) {
      if (!file.type.startsWith('image/')) {
        updateTwoFaStatus(false, 'Invalid file type. Please select an image file.');
        this.value = '';
        return;
      }
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
          updateTwoFaStatus(true, "Avatar updated successfully");
        })
        .catch(error => {
          updateTwoFaStatus(false, error);
          console.error('There was a problem with the fetch operation:', error);
        });
      };
    }
    this.value = '';
  });
}

async function getProfileData() {
  const url = `${window.location.origin}/user/profile`
  fetch (url, {
    method: 'GET',
  })
  .then(async response => {
    const data = await response.json();
    if (!response.ok)
      throw Error(data.message);
    document.getElementById('profilePicture').src = data.avatar;
    document.getElementById("email").value = data.email;
    document.getElementById("gameAlias").value = data.alias;
  })
  .catch(error => {
    console.error('There was a problem getting profile data: ', error);
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
    if (!response.ok)
      throw new Error(data.message);
    avatarUrl = data.avatar;
  }
  catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
  return avatarUrl;
}
