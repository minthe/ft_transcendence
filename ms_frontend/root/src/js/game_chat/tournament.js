
async function renderTourns() {
	console.log('In renderTourns');
	const matches = websocket_obj.game.invites;
  
	  const container = document.getElementById('tournGameSessionContainer');
	  container.innerHTML = generateHTMLContentTourns(matches);
  
	  container.querySelectorAll('.join-tourn-btn').forEach(button => {
		button.addEventListener('click', async function() {
		  const tournId = this.getAttribute('data-tournid');
		  userState.currPage = 'tournPage';
		  userState.tournId = tournId;
		  joinTourn(tournId, matches);
		  handleButtonClick("");
		  // joinGame(gameId);
		});
	  });
  }


function generateHTMLContentTourns(matches) {
	let htmlContent = '';
	if (matches.length > 0) {
	  htmlContent += '<ul style="justify-content: center; margin-left: 30vw;">';
	  matches.forEach(match => {
		htmlContent += `<li style="color: #ef7267; margin-bottom: 20px; margin-top: 20px;">Host: ${match[0][0].tourn_host}, Tournament ID: ${match[0][0].tourn_host}</li>`;
		htmlContent += `<button style="background-color: #ecc85d; color: black;" class="join-tourn-btn btn btn-secondary" data-tournid="${match[0][0].tourn_host}">Enter Tournament</button>`;
 
	  });
	  htmlContent += '</ul>';
	}
	// else {
	//   htmlContent = '<p>No matches found.</p>';
	// }
	return htmlContent;
}




function joinTourn(tournId, matches) {
	let userId = `${websocket_obj.user_id}`;
	console.log('userId : ', userId);

	// let idx = 0;
	let playerOne = document.getElementById('playerTopLeft');
	let playerTwo = document.getElementById('playerBottomLeft');
	let playerThree	= document.getElementById('playerTopRight');
	let playerFour	= document.getElementById('playerBottomRight');
	let winnerGameOne = document.getElementById('playerLeftCenter');
	let winnerGameTwo = document.getElementById('playerRightCenter');
	
	matches.forEach(match => {
		if (match[0][0].tourn_host === tournId) {
			const joinButtons = document.querySelectorAll('#displayTourn .join-game-div');

			joinButtons.forEach(joinButton => {
				joinButton.remove();
			});

			playerOne.textContent = match[1][0].alias_one;
			playerTwo.textContent = match[1][0].alias_two;
			playerThree.textContent = match[2][0].alias_one;
			playerFour.textContent = match[2][0].alias_two;
			
			if (match[1][0].winner_id) {
				if (match[1][0].player_one === match[1][0].winner_id) {
					playerOne.classList.add('winner-tourn-game');
					playerTwo.classList.add('loser-tourn-game');
					winnerGameOne.textContent = match[1][0].alias_one;
				}
				else {
					playerOne.classList.add('loser-tourn-game');
					playerTwo.classList.add('winner-tourn-game');
					winnerGameOne.textContent = match[1][0].alias_two;
				}
			}
			else if (match[1][0].player_one === userId 
				|| match[1][0].player_two === userId) {
					document.getElementById('displayTourn').innerHTML += `<div style="left: 15.5vw; top: 44vh;" class="join-game-div basic-tourn-element">
					<button style="background-color: #ecc85d; color: black;" class="btn btn-secondary join-game-btn" data-gameid="${match[1][0].game_id}">Join Game</button>
				  </div>`
			}
				// document.getElementById('leftJoin').classList.remove('hidden');

			if (match[2][0].winner_id) {
				if (match[2][0].player_one === match[2][0].winner_id) {
					playerThree.classList.add('winner-tourn-game');
					playerFour.classList.add('loser-tourn-game');
					winnerGameTwo.textContent = match[2][0].alias_one;
				}
				else {
					playerThree.classList.add('loser-tourn-game');
					playerFour.classList.add('winner-tourn-game');
					winnerGameTwo.textContent = match[2][0].alias_one;
				}
			}
			else if (match[2][0].player_one === userId 
				|| match[2][0].player_two === userId) {
					document.getElementById('displayTourn').innerHTML += `<div style="right: 8.5vw; top: 44vh;" class="join-game-div basic-tourn-element">
				<button style="background-color: #ecc85d; color: black;" class="btn btn-secondary join-game-btn" data-gameid="${match[2][0].game_id}">Join Game</button>
			  </div>`;
				}

			if (match[0][0].tourn_winner) {
				document.getElementById('tournamentWinner').textContent = match[0][0].tourn_winner;
				if (match[1][0].winner_id === match[0][0].tourn_winner) {
					winnerGameOne.classList.add('winner-tourn-game');
					winnerGameTwo.classList.add('loser-tourn-game');
				}
				else {
					winnerGameOne.classList.add('loser-tourn-game');
					winnerGameTwo.classList.add('winner-tourn-game');
				}
			}
			else if (!match[0][0].tourn_winner && match[1][0].winner_id && match[2][0].winner_id 
				&& (match[1][0].winner_id === userId || match[2][0].winner_id === userId)) { //!no winner yet
					document.getElementById('displayTourn').innerHTML += `<div style="left: 50.5vw; top: 35vh;" class="join-game-div basic-tourn-element">
					<button style="background-color: #ecc85d; color: black;" class="btn btn-secondary join-game-btn" data-gameid="${match[3][0].game_id}">Join Game</button>
					</div>`
				}
				
			return ;
		}
		// idx++;
	});

	// matches[idx]

	document.getElementById('tournInvitesScreen').classList.add('hidden');
	document.getElementById('displayTourn').classList.remove('hidden');

	//render players in right fields
	//check for available game
	//link joing game function to the buttons
	
	//change later and make it at the start
	let container = document.getElementById('displayTourn');
	container.querySelectorAll('.join-game-btn').forEach(button => {
		// let userName = '';
		button.addEventListener('click', async function() {
	
		  const gameId = this.getAttribute('data-gameid');
			console.log(gameId);
			joinGame(gameId); // Call your function with gameId
		});
	  });
}



