

document.addEventListener('DOMContentLoaded', function () {
  loadContent('html/userIsNotAuth.html', 'userIsNotAuth');
  loadContentIsAuth('html/userIsAuth.html', 'userIsAuth');

// 	console.log(state.bodyText);
//   if (state.bodyText === "notInit") {
//     state.bodyText = document.body.innerHTML;
//     window.history.replaceState(state, null, "");
//   }
// 	render(state);



	const url = `${window.location.origin}/user/token/existence`
	fetch(url)
	 .then(async response => {
	   if (!response.ok) {
		 throw new Error('Token could not be deleted!');
	   }
	   	// showDiv('userIsAuth');
    	// hideDiv('userIsNotAuth');
		// handleButtonClick("");
	//    await establishWebsocketConnection();
	})
	 .catch(error => {
	   console.error('There was a problem with the fetch operation:', error);
	 });
});

function loadContent(file, targetId) {
  fetch(file)
    .then(response => response.text())
    .then(html => {
      document.getElementById(targetId).innerHTML = html;
    //   addEventListenersNotAuth();
    })
    .catch(error => console.error('Error loading content:', error));
}

function loadContentIsAuth(file, targetId) {
  fetch(file)
    .then(response => response.text())
    .then(html => {
      document.getElementById(targetId).innerHTML = html;
      addEventListenersIsAuth();
    })
    .catch(error => console.error('Error loading content:', error));
  }

function loadContentGame(file, targetId) {
	fetch(file)
	.then(response => response.text())
	.then(html => {
		document.getElementById(targetId).innerHTML = html;
		gameDom();
	})
	.catch(error => console.error('Error loading content:', error));
}

function loadContentChat(file, targetId) {
	fetch(file)
	.then(response => response.text())
	.then(html => {
		document.getElementById(targetId).innerHTML = html;
		chatDom();
	})
	.catch(error => console.error('Error loading content:', error));
}

function loadContentProfile(file, targetId) {
	fetch(file)
	.then(response => response.text())
	.then(html => {
		document.getElementById(targetId).innerHTML = html;
		// chatDom();
	})
	.catch(error => console.error('Error loading content:', error));
}

function loadStats(file, targetId) {
	fetch(file)
	.then(response => response.text())
	.then(html => {
		document.getElementById(targetId).innerHTML = html;
	// chatDom();
	})
	.catch(error => console.error('Error loading content:', error));
}

function loadCreators(file, targetId) {
    fetch(file)
	.then(response => response.text())
	.then(html => {
		document.getElementById(targetId).innerHTML = html;
		// chatDom();
	})
	.catch(error => console.error('Error loading content:', error));
}
