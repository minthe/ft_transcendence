function handleDOMChangesProfile() {

}

function handleDOMChangesProfileBtn() {
  const editButton = document.getElementById("editButton");
  const saveButton = document.getElementById("saveButton");
  const globalStatsButton = document.getElementById("globalStatsButton");
  const statsButton = document.getElementById("yourStatsButton");
  const userStats = document.getElementById("userStats");
  const globalStats = document.getElementById("globalStats");


  const profileImageInput = document.querySelector('.change-profile-image input[type="file"]');
  
  if (profileImageInput) {
    addNewProfileImage(profileImageInput);
  }


  if (editButton) {
    editButton.addEventListener('click', function () {
      toggleEdit();
    });
    saveButton.addEventListener('click', function () {
      saveChanges();
    });
  }

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
    handleDOMChangesProfile();
    handleDOMChangesProfileBtn();
  });
});

// Start observing the DOM
observerProfile.observe(document.body, { childList: true, subtree: true });


function addNewProfileImage(profileImageInput) {
//   profileImageInput.addEventListener("change", function() {
//     const file = this.files[0];


//     if (file) {
//       if (!file.type.startsWith('image/')) {
//         setTimeout(function () {document.getElementById('fileError').style.display = 'none';}, 3000);
//         document.getElementById('fileError').style.display = 'block';
//         return;
//       }
//       // console.log('this is the file type: ', file.type);
//       const reader = new FileReader();
//       websocket_obj.profile_picture = websocket_obj.username + '.' + file.type.substring(6);
//       // websocket_obj.file_data = e.target.result;
//       reader.readAsDataURL(file);
//       reader.onload = function(e) {
//         const dataURI = e.target.result;
  
//         // Send the data URI to the Django backend
//         // fetch(`${window.location.origin}/game/create/${websocket_obj.username}/`);
//         fetch(`/user/picture/${username}/`, { // Using template literal to construct the URL
//           method: 'POST',
//           headers: {
//               'Content-Type': 'application/json',
//           },
//           body: JSON.stringify({ data_uri: dataURI, file_name: websocket_obj.profile_picture, file_type: file.type.substring(6)}),
//           // body: JSON.stringify({ data_uri: dataURI }),
//       })
//       .then(response => response.json())
//       .then(data => {
//           console.log(data.message);
//           // Handle response from backend if needed
//       })
//       .catch(error => console.error('Error:', error));



//         document.getElementById('profilePicture').src = websocket_obj.profile_picture;
//       };
//       // sendDataToBackend('new_profile_picture')
//     }
//   });
}

function toggleEdit() {
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
    //mail.value = websocket_obj.mail;
    //gameAlias = websocket_obj.gameAlias;
  }
  mail.setAttribute('readonly', true);
  gameAlias.setAttribute('readonly', true);

  //sendNewDataToBackend
  editButton.style.display = 'block';
  saveButton.style.display = 'none';
}
