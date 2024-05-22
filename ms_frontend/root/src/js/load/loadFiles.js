document.addEventListener('DOMContentLoaded', function () {
	loadContent('html/userIsNotAuth.html', 'userIsNotAuth');
	loadContentIsAuth('html/userIsAuth.html', 'userIsAuth');
});

function loadContent(file, targetId) {
  fetch(file)
    .then(response => response.text())
    .then(html => {
      document.getElementById(targetId).innerHTML = html;
    })
    .catch(error => console.error('Error loading content:', error, 'try reloading'));
}

function loadContentIsAuth(file, targetId) {
  fetch(file)
    .then(response => response.text())
    .then(html => {
      document.getElementById(targetId).innerHTML = html;
      addEventListenersIsAuth();
    })
    .catch(error => console.error('Error loading content:', error, 'try reloading'));
  }

function loadContentGame(file, targetId) {
	fetch(file)
	.then(response => response.text())
	.then(html => {
		document.getElementById(targetId).innerHTML = html;
		gameDom();
	})
	.catch(error => console.error('Error loading content:', error, 'try reloading'));
}

function loadContentChat(file, targetId) {
	fetch(file)
	.then(response => response.text())
	.then(html => {
		document.getElementById(targetId).innerHTML = html;
	})
	.catch(error => console.error('Error loading content:', error, 'try reloading'));
}

function loadContentProfile(file, targetId) {
	fetch(file)
	.then(response => response.text())
	.then(html => {
		document.getElementById(targetId).innerHTML = html;
	})
	.catch(error => console.error('Error loading content:', error, 'try reloading'));
}

function loadStats(file, targetId) {
	fetch(file)
	.then(response => response.text())
	.then(html => {
		document.getElementById(targetId).innerHTML = html;
	})
	.catch(error => console.error('Error loading content:', error, 'try reloading'));
}

function loadCreators(file, targetId) {
    fetch(file)
	.then(response => response.text())
	.then(html => {
		document.getElementById(targetId).innerHTML = html;
	})
	.catch(error => console.error('Error loading content:', error, 'try reloading'));
}
