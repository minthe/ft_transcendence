
// user_logged_out:
// value: {"message": "User successfully logged out"}
// user_not_logged_in:
// value: {"message": "User was not logged in"}
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
	  document.cookie = 'test' + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
	  // state.logedOut = true;
	  // userLogedIn = false;
	  // websocket_obj.websocket.close();
	  // return response.json();
	})
	.catch(error => {
	  console.error('There was a problem with the fetch operation:', error);
	});
	// .then(data => {
	//   console.log(data); // Here you can handle the JSON data returned by the endpoint
	// })
  }