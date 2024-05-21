
async function logoutUser() {
	const url = `${window.location.origin}/user/logout`

	fetch(url,
	{
	  method: 'POST',
	  headers: headerLogout(),
	})
	.then(response => {
	  if (!response.ok) { // Marie commented this cause it threw errors all the time lol
		throw new Error('Problems deleting the token!');
	  }
  
	  // let websocket_obj = null
	  localStorage.clear();
	  showDiv('userIsNotAuth')
	  hideDiv('userIsAuth')
	})
	.catch(error => {
	//   console.error('There was a problem loging out:', error);
	});
}
