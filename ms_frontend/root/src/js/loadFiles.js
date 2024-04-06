

document.addEventListener('DOMContentLoaded', function () {
  loadContent('html/userIsNotAuth.html', 'userIsNotAuth');
  loadContentIsAuth('html/userIsAuth.html', 'userIsAuth');
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
