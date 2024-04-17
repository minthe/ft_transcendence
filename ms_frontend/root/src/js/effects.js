let startTime;
let c;
let ctx;
let cwidth, cheight;
let shells = [];
let pass= [];

let colors = ['#FF5252', '#FF4081', '#E040FB', '#7C4DFF', '#536DFE', '#448AFF', '#40C4FF', '#18FFFF', '#64FFDA', '#69F0AE', '#B2FF59', '#EEFF41', '#FFFF00', '#FFD740', '#FFAB40', '#FF6E40'];
let lastRun = 0;

function activateFireworks() {
	if (document.getElementById("fireworkCanvas")) {
		c = document.getElementById("fireworkCanvas");
		ctx = c.getContext("2d");
	}
	startTime = getCurrentTime();
	reset();
	Run();
	window.onresize = function() { 
		reset();
	}
}


function reset() {
	cwidth = window.innerWidth;
	cheight = window.innerHeight;
	c.width = cwidth;//problem
	c.height = cheight;
}

function newShell() {

  let left = (Math.random() > 0.5);
  let shell = {};
  shell.x = (1*left);
  shell.y = 1;
  shell.xoff = (0.01 + Math.random() * 0.007) * (left ? 1 : -1);
  shell.yoff = 0.01 + Math.random() * 0.007;
  shell.size = Math.random() * 6 + 3;
  shell.color = colors[Math.floor(Math.random() * colors.length)];

  shells.push(shell);
}

function newPass(shell) {

  let pasCount = Math.ceil(Math.pow(shell.size, 2) * Math.PI);

  for (i = 0; i < pasCount; i++) {

	let pas = {};
	pas.x = shell.x * cwidth;
	pas.y = shell.y * cheight;

	let a = Math.random() * 4;
	let s = Math.random() * 10;

	pas.xoff = s *  Math.sin((5 - a) * (Math.PI / 2));
	pas.yoff = s *  Math.sin(a * (Math.PI / 2));

	pas.color = shell.color;
	pas.size = Math.sqrt(shell.size);

	if (pass.length < 1000)
		pass.push(pas);
  }
}



function Run() {
	console.log("run the fireworks");
	
	const currentTime = getCurrentTime();
	const elapsedTime = currentTime - startTime;
	
	// Stop the animation loop after 5 seconds (5000 milliseconds)
	if (elapsedTime >= 8000)
		return stopFirework();


  let dt = 1;
  if (lastRun != 0)
  	dt = Math.min(50, (performance.now() - lastRun));

  lastRun = performance.now();

  //ctx.clearRect(0, 0, cwidth, cheight);
	ctx.fillStyle = "rgba(0,0,0,0.25)";
	ctx.fillRect(0, 0, cwidth, cheight);

  if ((shells.length < 10) && (Math.random() > 0.96))
  	newShell();

  drawShellsLoop(shells, dt);
  drawParticleLoop(pass, dt);
  requestAnimationFrame(Run);
}

function drawShellsLoop(shells, dt) {
for (let ix = 0; ix < shells.length; ix++) {

	var shell = shells[ix];

	ctx.beginPath();
	ctx.arc(shell.x * cwidth, shell.y * cheight, shell.size, 0, 2 * Math.PI);
	ctx.fillStyle = shell.color;
	ctx.fill();

	shell.x -= shell.xoff;
	shell.y -= shell.yoff;
	shell.xoff -= (shell.xoff * dt * 0.001);
	shell.yoff -= ((shell.yoff + 0.2) * dt * 0.00005);

	if (shell.yoff < -0.005) {
		newPass(shell);
		shells.splice(ix, 1);
	}
}
}

function drawParticleLoop(pass, dt) {
for (let ix = 0; ix < pass.length; ix++) {

	var pas = pass[ix];

	ctx.beginPath();
	ctx.arc(pas.x, pas.y, pas.size, 0, 2 * Math.PI);
	ctx.fillStyle = pas.color;
	ctx.fill();

	pas.x -= pas.xoff;
	pas.y -= pas.yoff;
	pas.xoff -= (pas.xoff * dt * 0.001);
	pas.yoff -= ((pas.yoff + 5) * dt * 0.0005);
	pas.size -= (dt * 0.002 * Math.random())

	if ((pas.y > cheight)  || (pas.y < -50) || (pas.size <= 0))
		pass.splice(ix, 1);
}
}


function stopFirework() {
	document.getElementById('fireworkCanvas').style.zIndex = -1;
	document.getElementById('winningScreen').classList.add('hidden');
	document.getElementById('endScreen').classList.remove('hidden');
	state.currPage = 'endScreen';
	handleButtonClick("");
}

function getCurrentTime() {
    return performance.now(); // Returns the current time in milliseconds since the page started to load
}










  // Variables for countdown
  let countdown;
  let countdownInterval;

  // Function to draw countdown
function drawCountdown() {
	const canvas = document.getElementById('pongCanvas');
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = '48px Arial';
    ctx.fillStyle = 'black';
    ctx.textAlign = 'center';
    ctx.fillText(countdown, canvas.width / 2, canvas.height / 2);
  }

  // Function to start countdown animation
function startCountdownAnimation() {
	countdown = 3;
    countdownInterval = setInterval(() => {
      countdown--;
      if (countdown <= 0) {
        clearInterval(countdownInterval);
        // Start your game here after countdown
        console.log('Game started!');
        return;
      }
      drawCountdown();
    }, 1000);
  }





async function updatePage() {

    // if (state.userName === websocket_obj.username) {
		if (state.currPage === 'homeSite') {
			showSiteHideOthers('homeSite', 'homeButton');
			document.getElementById('displayUserName').innerHTML = websocket_obj.username;
		}
		else if (state.currPage === 'gameSite')
			gameSiteClicked();
		else if (state.currPage === 'profileSite')
			showSiteHideOthers('profileSite', 'profileButton')
		else if (state.currPage === 'creatorsSite')
			showSiteHideOthers('creatorsSite', 'creatorsButton');
		else if (state.currPage === 'statsSite')
			showSiteHideOthers('statsSite', 'statsButton');
		if (state.currPage === 'chat' || state.currPage === 'group_chat') {
			await sendDataToBackend('get_current_users_chats')
			await sendDataToBackend('get_blocked_by_user')
			await sendDataToBackend('get_blocked_user') // NEW since 02.02
		  }
		if (state.currPage === 'group_chat') {
		if (state.chatOpen)
		state.chatOpen = false;
		else
		state.chatOpen = true;
		await handleClickedOnChatElement(state.chatObj);
		}
		if (state.currPage === 'invites')
			await requestInvites();
		render(state);
		if (state.currPage === 'chat') {
		hideDiv('messageSide');
		document.getElementById('right-heading-name').textContent = "";
		chat_avatar.src = "../img/ballWithEye.jpg";
		}
		// }
		// else {
		//   console.log('goes into else of popstate');
		//   // showSiteHideOthers('homeSite');
		//   showSiteHideOthersSpa('homeSite')
		//   state.bodyText = document.body.innerHTML;
		//   state.userName = websocket_obj.username;
		//   window.history.replaceState(state, null, "");
		//   render(state);
		//   // state.userName = websocket_obj.username;
		// }
}



window.addEventListener('beforeunload', function(event) {
	const myData = {
		ws_obj: websocket_obj,
		bodyText: state.bodyText,
		currPage: state.currPage,
		chatObj: state.chatObj,
		chatOpen: state.chatOpen
	};
	localStorage.clear();
	localStorage.setItem('myData', JSON.stringify(myData));
})

window.addEventListener('load', function() {
	const myData = JSON.parse(localStorage.getItem('myData'));
	localStorage.clear();
	websocket_obj = myData.ws_obj
	username = myData.ws_obj.username
	password = myData.ws_obj.password
	user_id = myData.ws_obj.user_id

	state.bodyText = myData.bodyText;
	state.currPage = myData.currPage;
	state.chatObj = myData.chatObj;
	state.chatOpen = myData.chatOpen;

	// sillyLogin(websocket_obj.username, websocket_obj.password, websocket_obj.user_id)
	checkPageState();
});


function sillyLogin(username, password, user_id) {
	websocket_obj.username = username
	websocket_obj.password = password
	websocket_obj.age = 69
	websocket_obj.user_id = user_id

	establishWebsocketConnection()
}

function checkPageState() {
	const url = `${window.location.origin}/user/token/existence`
fetch(url, {
  method: 'GET',
  headers: {
	'Content-Type': 'application/json',
	'Authorization':'Bearer {access-token}'
	// 'Authorization': `Basic ${btoa(`${usernameElement.value}:${passwordElement.value}`)}`
  },
//   body: JSON.stringify({ username: usernameElement.value, password: passwordElement.value })
})
  .then(async response => {
	if (!response.ok) {
		await logoutUser();
		state.bodyText = document.body.innerHTML;
		state.currPage = "homeSite";
		state.chatObj = {};
		state.chatOpen= false;
		throw new Error('User has no token');
	  }
	  sillyLogin(websocket_obj.username, websocket_obj.password, websocket_obj.user_id)
	  hideDiv('userIsNotAuth');
	  document.getElementById("reloadScreen").style.display = "block";
	  setTimeout(function() {
		  document.getElementById("waitingScreen").style.display = "none";
			  updatePage();
	  }, 500);
  })
  .catch(error => {
	console.log('Error during login:', error);
  });


	// if (getJwtTokenFromCookie()) {
	// 	hideDiv('userIsNotAuth');
	// 	document.getElementById("reloadScreen").style.display = "block";
	// 	setTimeout(function() {
	// 		document.getElementById("waitingScreen").style.display = "none";
	// 			updatePage();				
	// 	}, 500);
	// }
	// else {
	// 	state.bodyText = document.body.innerHTML;
	// 	state.currPage = "homeSite";
	// 	state.chatObj = {};
	// 	state.chatOpen= false;
	// }
}


function getJwtTokenFromCookie() {
	const cookies = document.cookie.split(';');
	console.log(document.cookie);
	for (let i = 0; i < cookies.length; i++) {
		const cookie = cookies[i].trim();
		console.log(cookies[i]);
	  if (cookie.startsWith('test='))
		return true;
	}
	return false;
}
