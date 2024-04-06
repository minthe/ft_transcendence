
function gameDom() {
  // HERE EVENTLISTENERS FOR GAME:
  if (document.getElementById('createGameButton'))
    document.getElementById('createGameButton').addEventListener('click', createGame);
}

// HERE FUNCTIONS FOR GAME:


async function joinGame(gameId) {

  console.log('In JoinGame');
  // document.getElementById("showGameField").style.display = "block";
  // const startScreen = document.getElementById("start-screen");

  // const startScreenBtn = document.getElementById("renderInv");

  const gameScreen = document.getElementById("game-screen");

  // const waitingScreen = document.getElementById("waitingScreen");

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


  websocket_obj.game.game_id = gameId;
  websocket_obj.game.key_code = 0;
  websocket_obj.game.is_host = false;



  console.log("IN JOINGAME");

  async function updateCanvasSize() {
    const canvas = document.getElementById("pongCanvas");
    canvas.width = window.innerWidth * 0.75;  // Set canvas width to window width
    canvas.height = window.innerHeight * 0.75;  // Set canvas height to window height

  }

  window.addEventListener("resize", updateCanvasSize);

  // window.addEventListener("load", updateCanvasSize);

  document.getElementById("invites-screen").classList.add("hidden");
  // document.getElementById("game-session-container").style.display = "none";
  // waitingScreen.classList.add("show");
  // console.log("waitingScreen show");
  // waitingScreen.classList.remove("show");
  // console.log("waitingScreen remove show");

  document.getElementById("pongCanvas").classList.remove("hidden");
  gameScreen.classList.add('show');
  gameScreen.classList.remove('hidden');
  await sendDataToBackend('init_game');

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

  console.log('end of JoinGame');

}

async function requestInvites() {
  document.getElementById("start-screen").classList.add("hidden");
  document.getElementById("invites-screen").classList.remove("hidden");
  await sendDataToBackend('request_invites');
}


async function renderInvites() {
  if (websocket_obj.game.invites != 0)
  {
    // const htmlContent = await response.text();

    // const container = document.getElementById('game-session-container');
    // container.innerHTML = htmlContent;

    const username = websocket_obj.username;
    const matches = websocket_obj.game.invites;
    console.log(matches);
    const container = document.getElementById('game-session-container');
    container.innerHTML = generateHTMLContent(matches);

  //   <ul style="justify-content: center; margin-left: 30vw;">
  //   <li style="color: #ecc85d; margin-bottom: 20px; margin-top: 20px;">Opponent: ${match.opponent_name}, Game ID: ${match.game_id}</li>
  //   <button class="join-game-btn btn btn-secondary" data-gameid="${match.game_id}">Join Game</button>
  // </ul>

  function generateHTMLContent(matches) {
    let htmlContent = '';
    if (matches.length > 0) {
      htmlContent += '<ul style="justify-content: center; margin-left: 30vw;">';
      matches.forEach(match => {
        htmlContent += `<li style="color: #ef7267; margin-bottom: 20px; margin-top: 20px;">Opponent: ${match.opponent_name}, Game ID: ${match.game_id}</li>`;
        htmlContent += `<button style="background-color: #ecc85d; color: black;" class="join-game-btn btn btn-secondary" data-gameid="${match.game_id}">Join Game</button></li>`;

      });
      htmlContent += '</ul>';
    } else {
      htmlContent = '<p>No matches found.</p>';
    }
    return htmlContent;
  }

    // function generateHTMLContent(matches) {
    //   let htmlContent = '';
    //   if (matches.length > 0) {
    //     htmlContent += '<ul>';
    //     matches.forEach(match => {
    //       htmlContent += `<li>Opponent: ${match.opponent_name}, Game ID: ${match.game_id}</li>`;
    //       htmlContent += `<button class="join-game-btn" data-gameid="${match.game_id}">Join Game</button></li>`;

    //     });
    //     htmlContent += '</ul>';
    //   } else {
    //     htmlContent = '<p>No matches found.</p>';
    //   }
    //   return htmlContent;
    // }

    container.querySelectorAll('.join-game-btn').forEach(button => {
      // let userName = '';


      button.addEventListener('click', async function() {

        const gameId = this.getAttribute('data-gameid');

          joinGame(gameId); // Call your function with gameId
      });
    });
  }
}

// async function renderInvites() {

//   console.log('In renderInvites:');


//   const username = websocket_obj.username;
//   const matches = websocket_obj.matches_data;



//   // var theButton = document.getElementById('createGameButton');
//   // theButton.style.display = 'none';
//   try {

// // _+_+_+_+_+_+_

//     const response = await fetch(`${window.location.origin}/user/game/render/invites/${username}/`);
//     const htmlContent = await response.text();

//     const container = document.getElementById('game-session-container');
//     container.innerHTML = htmlContent;
// // _+_+_+_+_+_+_

// } catch (error) {
//     console.error('There was a problem with the fetch operation:', error);
// }



//   }

  async function  displayError(){
    console.log('hi');

  }


async function sendGameInvitation() {


  console.log('In invite user to game');

  var userNameInput = document.getElementById("guestUser");

  // Access the value property to get the entered data
  var guestUser = userNameInput.value;

  console.log("User Name: " + guestUser);


  var theButton = document.getElementById('createGameButton');
  theButton.style.display = 'none';
  var username = websocket_obj.username
  var game_id = websocket_obj.active_game;
  var guest_user_name = guestUser;
  try {
    const response = await fetch(`${window.location.origin}/user/game/invite/${username}/${game_id}/${guest_user_name}/`);
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


  var element = document.getElementById('createGameButton');
  console.log(element);



var theButton = document.getElementById('createGameButton');
theButton.style.display = 'none';
try {
  const response = await fetch(`${window.location.origin}/user/game/create/${websocket_obj.username}/`);
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


  // console.log("left pedal: ", left_pedal);
  // console.log("right pedal: ", right_pedal);

  // console.log ("canvas.width: ", canvas.width);
  // console.log ("canvas.height: ", canvas.height);
  // console.log ("canvas.width / 80: ", canvas.width / 80);
  // console.log ("canvas.height / 8: ", canvas.height / 8);
  // console.log ("canvas.height / 4: ", canvas.height / 4);


  // ctx.fillStyle = "black";
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
}

async function updateScore() {
  var hostScoreElem = document.getElementById('score1');
  var guestScoreElem = document.getElementById('score2');
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



function handleDOMChangesGame() {

}


const observerGame = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
    // Check if the desired elements are added or modified
    handleDOMChangesGame();
  });
});

// Start observing the DOM
observerGame.observe(document.body, { childList: true, subtree: true });





function gameSiteClicked() {
  document.getElementById('start-screen').classList.remove('hidden');
  document.getElementById('invites-screen').classList.add('hidden');
  document.getElementById('waitingScreen').classList.add('hidden');
  document.getElementById('game-screen').classList.add('hidden');
  document.getElementById('winningScreen').classList.add('hidden');
  document.getElementById('endScreen').classList.add('hidden');
  showSiteHideOthers('gameSite');
}