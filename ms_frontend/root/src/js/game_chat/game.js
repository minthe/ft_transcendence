
function gameDom() {
  // HERE EVENTLISTENERS FOR GAME:
  // if (document.getElementById('createGameButton'))
  //   document.getElementById('createGameButton').addEventListener('click', createGame);
  // if (document.getElementById('tournamentsContainer'))
  //   document.getElementById('tournamentsContainer').addEventListener('click', requestTourns);

}

async function joinedGameSuccessfully(gameId) {
  console.log('In joinedGameSuccessfully');

  const gameScreen = document.getElementById("game-screen");

  const canvas = document.getElementById("pongCanvas");
  const ctx = canvas.getContext("2d");

  // Draw paddles
  ctx.fillStyle = "black";

  websocket_obj.game.left_pedal = 0.75
  console.log("websocket_obj.game.left_pedal: ", websocket_obj.game.left_pedal);
  websocket_obj.game.right_pedal = 0.75


  ctx.fillRect(canvas.width / 80, canvas.height / 2 - (canvas.height / 4 / 2), canvas.width / 80, canvas.height / 4);
  ctx.fillRect(canvas.width - canvas.width / 80, canvas.height / 2 - (canvas.height / 4 / 2), canvas.width / 80, canvas.height / 4);

  // ctx.fillRect(canvas.width - 10, canvas.height / 2 - 50, 10, 100);


//   websocket_obj.game.game_id = gameId;
  websocket_obj.game.key_code = 0;
  websocket_obj.game.is_host = false;



  console.log("IN joinedGameSuccessfully");

  async function updateCanvasSize() {
    const canvas = document.getElementById("pongCanvas");
    canvas.width = window.innerWidth * 0.75;  // Set canvas width to window width
    canvas.height = window.innerHeight * 0.75;  // Set canvas height to window height

  }

  window.addEventListener("resize", updateCanvasSize);

  // window.addEventListener("load", updateCanvasSize);

  document.getElementById("invites-screen").classList.add("hidden");
  document.getElementById('displayTourn').classList.add('hidden');

  document.getElementById("pongCanvas").classList.remove("hidden");

  gameScreen.classList.add('show');
  gameScreen.classList.remove('hidden');


  document.getElementById('mainSidebar').classList.add('hidden');
  document.getElementById('siteContent').classList.remove('site-content');
  document.getElementById('siteContent').classList.add('site-content-game');

  // await sendDataToBackend('init_game');
  if (websocket_obj.game.active_state)
    window.addEventListener('popstate', function(event) {
        // Your code to handle the back button press here
        console.log('Back button pressed!');
        
    });


    document.addEventListener("keydown", async function(event) {
        // Log the key code to the console
        console.log("Key pressed: " + event.keyCode);
        if (event.keyCode == 40 || event.keyCode == 38)
        {
            websocket_obj.game.key_code = event.keyCode;
            // websocket_obj.game.game_id = gameId;
            console.log("in key event listener:");

            console.log(websocket_obj.game.is_host);

            await sendDataToBackend('game_new_move');
            websocket_obj.game.key_code = 0;
        }
    });

    console.log('end of JoinedGameSuccessfully');
    // return true;
}

async function joinGame(gameId) {

    console.log('In joinGame');
    console.log('websocket_obj.game.active_state: ', websocket_obj.game.active_state);
    // if (websocket_obj.game.active_state == false)
    // {
    console.log('In joinGame');
    websocket_obj.game.game_id = gameId;
    await sendDataToBackend('init_game');
    websocket_obj.game.active_state = true;
    // }
}
  


  // const gameScreen = document.getElementById("game-screen");

  // const canvas = document.getElementById("pongCanvas");
  // const ctx = canvas.getContext("2d");

  // // Draw paddles
  // ctx.fillStyle = "black";

  // websocket_obj.game.left_pedal = 0.75
  // console.log("websocket_obj.game.left_pedal: ", websocket_obj.game.left_pedal);
  // websocket_obj.game.right_pedal = 0.75


  // ctx.fillRect(canvas.width / 80, canvas.height / 2 - (canvas.height / 4 / 2), canvas.width / 80, canvas.height / 4);
  // ctx.fillRect(canvas.width - canvas.width / 80, canvas.height / 2 - (canvas.height / 4 / 2), canvas.width / 80, canvas.height / 4);

  // // ctx.fillRect(canvas.width - 10, canvas.height / 2 - 50, 10, 100);


  // websocket_obj.game.game_id = gameId;
  // websocket_obj.game.key_code = 0;
  // websocket_obj.game.is_host = false;



  // console.log("IN JOINGAME");

  // async function updateCanvasSize() {
  //   const canvas = document.getElementById("pongCanvas");
  //   canvas.width = window.innerWidth * 0.75;  // Set canvas width to window width
  //   canvas.height = window.innerHeight * 0.75;  // Set canvas height to window height

  // }

  // window.addEventListener("resize", updateCanvasSize);

  // // window.addEventListener("load", updateCanvasSize);

  // document.getElementById("invites-screen").classList.add("hidden");

  // document.getElementById("pongCanvas").classList.remove("hidden");
  // gameScreen.classList.add('show');
  // gameScreen.classList.remove('hidden');
  // // await sendDataToBackend('init_game');

  // window.addEventListener('popstate', function(event) {
  //     // Your code to handle the back button press here
  //     console.log('Back button pressed!');
      
  // });


  // document.addEventListener("keydown", async function(event) {
  //     // Log the key code to the console
  //     console.log("Key pressed: " + event.keyCode);
  //     if (event.keyCode == 40 || event.keyCode == 38)
  //     {
  //         websocket_obj.game.key_code = event.keyCode;
  //         // websocket_obj.game.game_id = gameId;
  //         console.log("in key event listener:");

  //         console.log(websocket_obj.game.is_host);

  //         await sendDataToBackend('game_new_move');
  //         websocket_obj.game.key_code = 0;
  //     }
  // });

  // console.log('end of JoinGame');

  // }


async function requestInvites() {
  document.getElementById("start-screen").classList.add("hidden");
  document.getElementById("invites-screen").classList.remove("hidden");
  await sendDataToBackend('request_invites');
}


async function requestTournHis() {
    console.log('In requestTournHis');
    if (userState.currPage !== 'tournPage') {
      document.getElementById("start-screen").classList.add("hidden");
      document.getElementById("tournInvitesScreen").classList.remove("hidden");
    }
    await sendDataToBackend('request_tourn_history');
  }

async function requestTourns() {
  console.log('In requestTourns');
  if (userState.currPage !== 'tournPage') {
    document.getElementById("start-screen").classList.add("hidden");
    document.getElementById("tournInvitesScreen").classList.remove("hidden");
  }
  await sendDataToBackend('request_tourns');
}

async function generateFrontendRepresentation(data) {
  const tournamentsContainer = document.getElementById('tournamentsContainer');

    console.log('In generateFrontendRepresentation');
    console.log(typeof data);
    console.log(data);

 
}



async function renderInvites() {
  // console.log(websocket_obj.game);

  if (websocket_obj.game.invites != 0)
  {
    // const htmlContent = await response.text();

    // const container = document.getElementById('game-session-container');
    // container.innerHTML = htmlContent;
    // websocket_obj.game.active_game = false;
    const username = websocket_obj.username;
    const matches = websocket_obj.game.invites;
    console.log(matches);
    const container = document.getElementById('game-session-container');

    container.innerHTML = generateHTMLContentInv(matches);

    container.querySelectorAll('.join-game-btn').forEach(button => {
      // let userName = '';
      button.addEventListener('click', async function() {

        const gameId = this.getAttribute('data-gameid');

          joinGame(gameId); // Call your function with gameId
      });
    });
  }
}

function generateHTMLContentInv(matches) {
  let htmlContent = '';
  console.log('length of matches : ', matches.length);
  if (matches.length > 0) {
    htmlContent += '<ul style="justify-content: center; margin-left: 30vw;">';
    matches.forEach(match => {
      htmlContent += `<li style="color: #ef7267; margin-bottom: 20px; margin-top: 20px;">Opponent: ${match.opponent_name}, Game ID: ${match.game_id}</li>`;
      htmlContent += `<button style="background-color: #ecc85d; color: black;" class="join-game-btn btn btn-secondary" data-gameid="${match.game_id}">Join Game</button>`;

    });
    htmlContent += '</ul>';
  }
  // else {
  //   htmlContent = '<p>No matches found.</p>';
  // }
  return htmlContent;
}


  async function  displayError(){
    console.log('hi');

  }


async function sendGameInvitation() {


  console.log('In invite user to game');

  let userNameInput = document.getElementById("guestUser");

  // Access the value property to get the entered data
  let guestUser = userNameInput.value;

  console.log("User Name: " + guestUser);


  let theButton = document.getElementById('createGameButton');
  theButton.style.display = 'none';
  let username = websocket_obj.username
  let game_id = websocket_obj.active_game;
  let guest_user_name = guestUser;
  try {
    const response = await fetch(`${window.location.origin}/game/invite/${username}/${game_id}/${guest_user_name}/`);
    const data = await response.json();

    console.log('DATA ', data);

    if (response.ok) {
    displayError(null);
    // Perform actions on successful login, e.g., set isLoggedIn and userData
      websocket_obj.active_game = null;

        console.log(data);
    } else {
    displayError(data.error);
    }
  } catch (error) {
    console.error('Error fetching user data:', error);
    displayError('Error fetching user data');
  }
}

async function createGame() {


  console.log("IN CREATEGAME");


  let element = document.getElementById('createGameButton');
  console.log(element);



let theButton = document.getElementById('createGameButton');
theButton.style.display = 'none';
try {
  const response = await fetch(`${window.location.origin}/game/create/${websocket_obj.username}/`);
  const data = await response.json();



  console.log('DATA ', data);
  websocket_obj.active_game = data.id;
  console.log('active game ', data.id);


  if (response.ok) {
  displayError(null);
  websocket_obj.active_game = data.id;
  // console.log(data.id); // Check the console for the result

  // Perform actions on successful login, e.g., set isLoggedIn and userData
      console.log(data);
  } else {
  displayError(data.error);
  }
} catch (error) {
  console.error('Error fetching user data:', error);
  displayError('Error fetching user data');
}


}


function drawPaddles() {

  // console.log("in drawPaddles WEBSOCKETS.JS");
  const canvas = document.getElementById("pongCanvas");

  const ctx = canvas.getContext("2d");

  // console.log("left pedal: ", websocket_obj.game.left_pedal);
  // console.log("right pedal: ", websocket_obj.game.right_pedal);
  left_pedal = canvas.height * websocket_obj.game.left_pedal / 2
  right_pedal = canvas.height * websocket_obj.game.right_pedal / 2


  const paddleHeight = canvas.height / 4;

  // Ensure paddles stay within canvas boundaries
  if (left_pedal < 0) {
    left_pedal = 0;
    websocket_obj.game.left_pedal = 0;
  } else if (left_pedal + paddleHeight > canvas.height) {
    left_pedal = canvas.height - paddleHeight;
    websocket_obj.game.left_pedal = left_pedal * 2 / canvas.height;
  }

  if (right_pedal < 0) {
    right_pedal = 0;
    websocket_obj.game.right_pedal = 0;
  } else if (right_pedal + paddleHeight > canvas.height) {
    right_pedal = canvas.height - paddleHeight;
    websocket_obj.game.right_pedal = right_pedal * 2 / canvas.height;
  }

  ctx.fillStyle = "#131615";

  ctx.fillRect(
    canvas.width / 80,
    left_pedal,
    canvas.width / 80,
    canvas.height / 4);

  ctx.fillRect(
    canvas.width - 2 * canvas.width / 80,// canvas.width - canvas.width / 80,
    right_pedal,
    canvas.width / 80,
    canvas.height / 4);
}

function drawBall() {
  // console.log("in drawBall WEBSOCKETS.JS");

  const canvas = document.getElementById("pongCanvas");

  const ctx = canvas.getContext("2d");


  ctx.beginPath();
  // radius = canvas.width / 80
  radius = canvas.height / 40

  ctx.arc(websocket_obj.game.ball_x, websocket_obj.game.ball_y, radius, 0, Math.PI * 2);
  // console.log("BALL canvas.width / 80", canvas.width / 80)
  // ctx.arc(canvas.width / 2, canvas.height / 2, canvas.width / 80, 0, Math.PI * 2);

  ctx.fill();
  ctx.closePath();
}

async  function update() {
  const canvas = document.getElementById("pongCanvas");

  const ctx = canvas.getContext("2d");

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // moveBall();
  drawPaddles();
  drawBall();

  drawDashedLine(canvas, ctx);
}

async function drawDashedLine(canvas, ctx){
  const lineWidth = 5;

  ctx.strokeStyle = 'black';
  ctx.lineWidth = lineWidth;
  ctx.setLineDash([13, 13]); // Dashed pattern
  ctx.beginPath();
  ctx.moveTo(canvas.width / 2, 0);
  ctx.lineTo(canvas.width / 2, canvas.height);
  ctx.stroke();
}

async function updateScore() {
  let hostScoreElem = document.getElementById('score1');
  let guestScoreElem = document.getElementById('score2');
  hostScoreElem.textContent = websocket_obj.game.host_score;
  guestScoreElem.textContent = websocket_obj.game.guest_score;

}

async function launchGame()
{
  console.log('In launchGame');

  // document.getElementById("waitingScreen").style.display = "none";

  const canvas = document.getElementById("pongCanvas");
  const ctx = canvas.getContext("2d");

  const gameState = {
    ball: {
      x: canvas.width / 2,
      y: canvas.height / 2,
      radius: canvas.width / 80,
      dx: 5,
      dy: 5,
    },

  };

  await update()
}







//
// async function renderGame() {
//
//   console.log("in ACTUAL rendering");
//   console.log(websocket_obj.game.is_host);
//
//   const canvas = document.getElementById("pongCanvas");
//   const ctx = canvas.getContext("2d");
//
//   // Clear the canvas
//   ctx.clearRect(0, 0, canvas.width, canvas.height);
//
//   ctx.fillStyle = "black";
//
//   ctx.fillRect(canvas.width / 80, canvas.height / 2 - canvas.height / 8, canvas.width / 80, canvas.height / 4);
//   ctx.fillRect(canvas.width / 80 - canvas.width / 80, canvas.height / 2 - canvas.height / 8, canvas.width / 80, canvas.height / 4);
//   console.log ("canvas.width: ", canvas.width);
//   console.log ("canvas.height: ", canvas.height);
//   console.log ("canvas.width / 80: ", canvas.width / 80);
//   console.log ("canvas.height / 8: ", canvas.height / 8);
//   console.log ("canvas.height / 4: ", canvas.height / 4);
//
//
//   // Draw the ball
//   ctx.beginPath();
//   // ctx.arc(canvas.width / 2, canvas.height / 2, 10, 0, Math.PI * 2);
//   ctx.arc(canvas.width / 2, canvas.height / 2, canvas.width / 80, 0, Math.PI * 2);
//
//   ctx.fill();
//   ctx.closePath();
// }


function gameSiteClicked() {
  document.getElementById('start-screen').classList.remove('hidden');
  document.getElementById('invites-screen').classList.add('hidden');
  document.getElementById('tournInvitesScreen').classList.add('hidden');
  document.getElementById('displayTourn').classList.add('hidden');
  document.getElementById('waitingScreen').classList.add('hidden');
  document.getElementById('game-screen').classList.add('hidden');
  document.getElementById('winningScreen').classList.add('hidden');
  document.getElementById('endScreen').classList.add('hidden');
  showSiteHideOthers('gameSite', 'gameButton');
}

function invSiteClicked() {
  userState.currPage = 'invites';
  handleButtonClick("");
}

function tournInvSiteClicked() {
  userState.currPage = 'invitesTourn';
  handleButtonClick(""); 
}


function gameOver(data) {
  document.getElementById('mainSidebar').classList.remove('hidden');
  document.getElementById('siteContent').classList.add('site-content');
  document.getElementById('siteContent').classList.remove('site-content-game');

  document.getElementById('game-screen').classList.add('hidden');
  document.getElementById('pongCanvas').classList.add('hidden');
  document.getElementById('winningScreen').classList.remove('hidden');

  document.getElementById('fireworkCanvas').style.zIndex = 1;
  console.log("GAME_OVER");
  console.log(websocket_obj.game.game_id);
  console.log(data.game_id);
  if (websocket_obj.game.game_id === data.game_id)
    activateFireworks();
  
  let hostScoreElem = document.getElementById('score1');
  let guestScoreElem = document.getElementById('score2');
  if (hostScoreElem.textContent > guestScoreElem.textContent)
    document.getElementById('winnerName').textContent = document.getElementById('playerOne').textContent + ' Won';
  else
    document.getElementById('winnerName').textContent = document.getElementById('playerTwo').textContent + ' Won';

  websocket_obj.game.hostname
  websocket_obj.game.active_state = false
  websocket_obj.game.host_score = 0
  websocket_obj.game.guest_score = 0
  websocket_obj.game.game_id = 0
  updateScore();
}

// guest_id
// : 
// "jkroger"
// host_id
// : 
// "julien"
// is_host
// : 
// "False"
// is_tourn
// : 
// "False"


async function initGame(data) {
  console.log(data);
  document.getElementById("waitingScreen").style.display = "block";
  if (data.is_tourn === "True") {
    document.getElementById('playerOne').textContent = data.alias_one;
    document.getElementById('playerTwo').textContent = data.alias_two;
  }
  else {
    document.getElementById('playerOne').textContent = data.host_id;
    document.getElementById('playerTwo').textContent = data.guest_id;
  }

  document.getElementById('imgHost').src = await getProfilePicture(data.num_id_one);
  document.getElementById('imgGuest').src = await getProfilePicture(data.num_id_two); 

  if (data.is_host === 'True')
    websocket_obj.game.is_host = true
  else
    websocket_obj.game.is_host = false
  // websocket_obj.game.game_joined = true;
}