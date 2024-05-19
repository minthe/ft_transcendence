
async function renderTourns() {
	console.log('In renderTourns');
	const matches = websocket_obj.game.invites;
  
	  const container = document.getElementById('tournGameSessionContainer');
	  container.innerHTML = generateHTMLContentTourns(matches);
  
	  container.querySelectorAll('.join-tourn-btn').forEach(button => {
		button.addEventListener('click', async function() {
		  const tournId = this.getAttribute('data-tournid');
		//   userState.currPage = 'tournPage';
		//   userState.tournId = tournId;
		  joinTourn(tournId, matches);
		//   handleButtonClick("");
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
	
	matches.forEach(match => {
		if (match[0][0].tourn_host === tournId) {
			const joinButtons = document.querySelectorAll('#displayTourn .join-game-div');

			joinButtons.forEach(joinButton => {
				joinButton.remove();
			});
			for (let i = 1; match[i]; i++) {
				if (match[i][0].stage === "semi")
					stageSemi(match[i][0], userId);
				else if (match[i][0].stage === "final")
					stageFinal(match[i][0], userId);			
			}	
			return ;
		}
	});


	document.getElementById('tournInvitesScreen').classList.add('hidden');
	document.getElementById('displayTourn').classList.remove('hidden');

	let container = document.getElementById('displayTourn');
	container.querySelectorAll('.join-game-btn').forEach(button => {
		button.addEventListener('click', async function() {
		  	const gameId = this.getAttribute('data-gameid');
			// console.log(gameId);
			joinGame(gameId);
		});
	  });
}



// alias_one: "jkroger"
// alias_two:"julien"
// game_id:1
// loser_id:null
// player_one:"5"
// player_two:"2"
// stage:"semi"
// winner_id:null
// counter_semi
// : 
// 2

function stageSemi(semi, userId) {
	if (semi.counter_semi === 1)
		firstSemi(semi, userId);
	else
		secondSemi(semi, userId);
}

function firstSemi(semi, userId) {
	let playerOne = document.getElementById('playerTopLeft');
	let playerTwo = document.getElementById('playerBottomLeft');
	let winnerGameOne = document.getElementById('playerLeftCenter');

	playerOne.textContent = semi.alias_one;
	playerTwo.textContent = semi.alias_two;
	if (semi.player_one === semi.winner_id) {
		playerOne.classList.add('winner-tourn-game');
		playerTwo.classList.add('loser-tourn-game');
		winnerGameOne.textContent = semi.alias_one;
	}
	else if (semi.player_two === semi.winner_id) {
		playerOne.classList.add('loser-tourn-game');
		playerTwo.classList.add('winner-tourn-game');
		winnerGameOne.textContent = semi.alias_two;
	}
	else if (semi.player_one === userId 
		|| semi.player_two === userId) {
			document.getElementById('displayTourn').innerHTML += `<div style="left: 15.5vw; top: 44vh;" class="join-game-div basic-tourn-element">
			<button style="background-color: #ecc85d; color: black;" class="btn btn-secondary join-game-btn" data-gameid="${semi.game_id}">Join Game</button>
		  	</div>`;
	}
}

function secondSemi(semi, userId) {
	let playerThree	= document.getElementById('playerTopRight');
	let playerFour	= document.getElementById('playerBottomRight');
	let winnerGameTwo = document.getElementById('playerRightCenter');
	
	playerThree.textContent = semi.alias_one;
	playerFour.textContent = semi.alias_two;
	if (semi.player_one === semi.winner_id) {
		playerThree.classList.add('winner-tourn-game');
		playerFour.classList.add('loser-tourn-game');
		winnerGameTwo.textContent = semi.alias_one;
	}
	else if (semi.player_two === semi.winner_id) {
		playerThree.classList.add('loser-tourn-game');
		playerFour.classList.add('winner-tourn-game');
		winnerGameTwo.textContent = semi.alias_two;
	}
	else if (semi.player_one === userId 
		|| semi.player_two === userId) {
			document.getElementById('displayTourn').innerHTML += `<div style="right: 8.5vw; top: 44vh;" class="join-game-div basic-tourn-element">
			<button style="background-color: #ecc85d; color: black;" class="btn btn-secondary join-game-btn" data-gameid="${semi.game_id}">Join Game</button>
		</div>`;
	}
}

function stageFinal(final, userId) {
	let winnerGameOne = document.getElementById('playerLeftCenter');
	let winnerGameTwo = document.getElementById('playerRightCenter');
	
	if (final.winner_id) {
		document.getElementById('tournamentWinner').textContent = final.winner_id;
		if (final.winner_id === final.player_one) {
			winnerGameOne.classList.add('winner-tourn-game');
			winnerGameTwo.classList.add('loser-tourn-game');
		}
		else {
			winnerGameOne.classList.add('loser-tourn-game');
			winnerGameTwo.classList.add('winner-tourn-game');
		}
	}
	else if (final.player_one === userId || final.player_two === userId) {
		document.getElementById('displayTourn').innerHTML += `<div style="left: 50.5vw; top: 35vh;" class="join-game-div basic-tourn-element">
		<button style="background-color: #ecc85d; color: black;" class="btn btn-secondary join-game-btn" data-gameid="${final.game_id}">Join Game</button>
		</div>`
	}
}
