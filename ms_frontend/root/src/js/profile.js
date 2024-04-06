function handleDOMChangesProfile() {
    // const sidebar = document.getElementById("sidebar")
    // const sidebarToggle = document.getElementById("sidebar-toggler");
    // const profileSite = document.getElementById("profileSite");

    // sidebarToggle.addEventListener('click', function () {
    //     console.log("profile shrinkin");
    //   if (sidebar.classList.contains("show-sidebar")) 
    //     profileSite.classList.add("shrink");
    //   else
    //     profileSite.classList.remove("shrink");
    // });
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
    profileImageInput.addEventListener("change", function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function(e) {
          const profilePicture = document.querySelector('.profile-picture');
          const imageSidebar = document.getElementById("imageSidebar");

          profilePicture.src = e.target.result;
          imageSidebar.src = e.target.result;
        };
      }
    });
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


function toggleEdit() {
  let inputs = document.querySelectorAll('input[readonly]');

  inputs.forEach(input => input.removeAttribute('readonly'));
  editButton.style.display = 'none';
  saveButton.style.display = 'block';
}

function saveChanges() {
  let emailValue = document.getElementById("email").value;
  let locationValue = document.getElementById("location").value;
  let ageValue = document.getElementById("age").value;

  document.getElementById("email").setAttribute('readonly', true);
  document.getElementById("location").setAttribute('readonly', true);
  document.getElementById("age").setAttribute('readonly', true);
  editButton.style.display = 'block';
  saveButton.style.display = 'none';
}
