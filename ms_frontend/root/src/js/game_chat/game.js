async function joinedGameSuccessfully(gameId) {
  const gameScreen = document.getElementById("game-screen");
  const canvas = document.getElementById("pongCanvas");
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = "black";

  websocket_obj.game.left_pedal = 0.75
  websocket_obj.game.right_pedal = 0.75

  ctx.fillRect(canvas.width / 80, canvas.height / 2 - (canvas.height / 4 / 2), canvas.width / 80, canvas.height / 4);
  ctx.fillRect(canvas.width - canvas.width / 80, canvas.height / 2 - (canvas.height / 4 / 2), canvas.width / 80, canvas.height / 4);

  websocket_obj.game.key_code = 0;
  websocket_obj.game.is_host = false;

  async function updateCanvasSize() {
    const canvas = document.getElementById("pongCanvas");
    canvas.width = window.innerWidth * 0.75;  // Set canvas width to window width
    canvas.height = window.innerHeight * 0.75;  // Set canvas height to window height
  }

  window.addEventListener("resize", updateCanvasSize);
  document.getElementById("invites-screen").classList.add("hidden");
  document.getElementById('displayTourn').classList.add('hidden');
  document.getElementById("pongCanvas").classList.remove("hidden");

  gameScreen.classList.add('show');
  gameScreen.classList.remove('hidden');

  document.getElementById('mainSidebar').classList.add('hidden');
  document.getElementById('siteContent').classList.remove('site-content');
  document.getElementById('siteContent').classList.add('site-content-game');

  if (websocket_obj.game.active_state)
    window.addEventListener('popstate', function(event) {
        // Your code to handle the back button press here
    });

    document.addEventListener("keydown", async function(event) {
        if (event.keyCode == 40 || event.keyCode == 38)
        {
            websocket_obj.game.key_code = event.keyCode;
            await sendDataToBackend('game_new_move');
            websocket_obj.game.key_code = 0;
        }
    });
}

async function joinGame(gameId) {
    websocket_obj.game.game_id = gameId;
    await sendDataToBackend('init_game');
    websocket_obj.game.active_state = true;
}

async function requestInvites() {
  document.getElementById("start-screen").classList.add("hidden");
  document.getElementById("invites-screen").classList.remove("hidden");
  await sendDataToBackend('request_invites');
}

async function requestTourns() {
  if (userState.currPage !== 'tournPage') {
    document.getElementById("start-screen").classList.add("hidden");
    document.getElementById("tournInvitesScreen").classList.remove("hidden");
  }
  await sendDataToBackend('request_tourns');
}

async function renderInvites() {
  const matches = websocket_obj.game.invites;
  const container = document.getElementById('game-session-container');

  container.innerHTML = generateHTMLContentInv(matches);
  if (websocket_obj.game.invites != 0) {
    container.querySelectorAll('.join-game-btn').forEach(button => {
    button.addEventListener('click', async function() {
      const gameId = this.getAttribute('data-gameid');
        joinGame(gameId); // Call your function with gameId
      });
    });
  }
}

function generateHTMLContentInv(matches) {
  let htmlContent = '';

  if (matches.length > 0) {
    htmlContent += '<ul style="justify-content: center; margin-left: 30vw;">';
    matches.forEach(match => {
      htmlContent += `<li style="color: #ef7267; margin-bottom: 20px; margin-top: 20px;">Opponent: ${match.opponent_name}, Game ID: ${match.game_id}</li>`;
      htmlContent += `<button style="background-color: #ecc85d; color: black;" class="join-game-btn btn btn-secondary" data-gameid="${match.game_id}">Join Game</button>`;
    });
    htmlContent += '</ul>';
  }
  return htmlContent;
}

async function sendGameInvitation() {
  let userNameInput = document.getElementById("guestUser");
  let guestUser = userNameInput.value;
  let theButton = document.getElementById('createGameButton');
  theButton.style.display = 'none';
  let username = websocket_obj.username
  let game_id = websocket_obj.active_game;
  let guest_user_name = guestUser;
  try {
    const response = await fetch(`${window.location.origin}/game/invite/${username}/${game_id}/${guest_user_name}/`);
    const data = await response.json();
    if (response.ok) {
    displayError(null);
    // Perform actions on successful login, e.g., set isLoggedIn and userData
      websocket_obj.active_game = null;
    } else {
    displayError(data.error);
    }
  } catch (error) {
    displayError('Error fetching user data');
  }
}

function drawPaddles() {
  const canvas = document.getElementById("pongCanvas");
  const ctx = canvas.getContext("2d");

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
  const canvas = document.getElementById("pongCanvas");
  const ctx = canvas.getContext("2d");

  ctx.beginPath();
  radius = canvas.height / 40

  ctx.arc(websocket_obj.game.ball_x, websocket_obj.game.ball_y, radius, 0, Math.PI * 2);
  ctx.fill();
  ctx.closePath();
}

async  function update() {
  const canvas = document.getElementById("pongCanvas");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

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

async function initGame(data) {
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
}
