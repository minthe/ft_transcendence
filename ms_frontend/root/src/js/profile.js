
function handleDOMChangesProfileBtn() {

  const globalStatsButton = document.getElementById("globalStatsButton");
  const statsButton = document.getElementById("yourStatsButton");
  const userStats = document.getElementById("userStats");
  const globalStats = document.getElementById("globalStats");




  if (globalStatsButton) {
    globalStatsButton.addEventListener('click', function() {
      console.log("gloabl statst");
      userStats.classList.add("hidden");
      globalStats.classList.remove("hidden");
    });

    statsButton.addEventListener('click', function() {
      console.log("normal stats");
      globalStats.classList.add("hidden");
      userStats.classList.remove("hidden");
    });
  }
}
  
const observerProfile = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
    handleDOMChangesProfileBtn();
  });
});

// Start observing the DOM
observerProfile.observe(document.body, { childList: true, subtree: true });


//combine function with the one from twofa
function updateProfileMessage(success, message) {
	const twoFaStatus = document.getElementById('updateTwoFa');

	setTimeout(function() {
	twoFaStatus.classList.add('hidden');
	}, 2500);
	twoFaStatus.classList.remove('hidden');
	if (success)
		twoFaStatus.style.color = 'green';
	else
		twoFaStatus.style.color = 'red';
	twoFaStatus.textContent = message;
}

let emailBeforeEdit = document.getElementById('email').value;
let gameAliasBeforeEdit = document.getElementById('email').value;

function editProfile() {
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
        if (!response.ok) {
          const data = await response.json();
          throw Error(data.message);
        }
        document.getElementById('profilePicture').src = dataURI;
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
function getProfileData() {
  const url = `${window.location.origin}/user/profile`
  fetch (url, {
    method: 'GET',
    // header: headerProfilePictureChange(),
  })
  .then(async response => {
    const data = await response.json();
    if (!response.ok)
      throw Error(data.message);
    document.getElementById('profilePicture').src = data.avatar;
    document.getElementById("email").value = data.email;
    document.getElementById("gameAlias").value = data.alias;
    updateProfileMessage(true, "Avatar updated successfully");
  })
  .catch(error => {
    updateProfileMessage(false, error);
    console.error('There was a problem with the fetch operation:', error);
  });
}