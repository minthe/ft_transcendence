
function historyBtnClicked() {
	document.getElementById('userStats').classList.add('hidden');
	document.getElementById('tournHistory').classList.add('hidden');
	document.getElementById('userHistory').classList.remove('hidden');
}

function statsBtnClicked() {
	document.getElementById('userHistory').classList.add('hidden');
	document.getElementById('tournHistory').classList.add('hidden');
	document.getElementById('userStats').classList.remove('hidden');
}

function tournHistoryBtnClicked() {
	document.getElementById('userHistory').classList.add('hidden');
	document.getElementById('userStats').classList.add('hidden');
	document.getElementById('tournHistory').classList.remove('hidden');
}

async function statsSiteClicked() {
	await requestStats();
	await requestHistory();
	await requestTournHistory();

	document.getElementById('userStats').classList.remove('hidden');
	document.getElementById('userHistory').classList.add('hidden');
	document.getElementById('tournHistory').classList.add('hidden');

	showSiteHideOthers('statsSite', 'statsButton');
}

async function requestHistory() {
	await sendDataToBackend('request_history');
}

async function requestStats() {
	await sendDataToBackend('request_stats');
}

async function requestTournHistory() {
	await sendDataToBackend('request_tourn_history');
}

function displayStats() {
	let winRate = (websocket_obj.game_stats.won_games / websocket_obj.game_stats.total_games * 100);

	document.getElementById('gamesPlayed').textContent = "Games Played: " + websocket_obj.game_stats.total_games;
	document.getElementById('wonGames').textContent = "Wins: " + websocket_obj.game_stats.won_games;
	document.getElementById('lostGames').textContent = "Defeats: " + websocket_obj.game_stats.lost_games;

	document.getElementById('tournsPlayed').textContent = "Tournaments Played: " + websocket_obj.game_stats.all_tourns;
	document.getElementById('wonTourns').textContent = "Tournaments Won: " + websocket_obj.game_stats.won_tourns;
	if (isNaN(winRate))
		document.getElementById('winRate').textContent = "Win Rate: 0%";
	else
		document.getElementById('winRate').textContent = "Win Rate: " + winRate.toFixed(2) + '%';
}

function displayHistory() {
	console.log('display history');

	const userHistory = document.getElementById('userHistory');
	let historyHTML = '<h2 class="stats-item">Your History</h2><div class="stats">';

	userHistory.innerHTML = '';
	historyHTML += '<div class="scroll-history">'
	for (let i = 0; websocket_obj.history[i]; i++) {
		historyHTML += '<div class="stats-item"><span id="gamesPlayed">'
		+ 'won: ' + websocket_obj.history[i][0].winner_id + ' lost: ' + websocket_obj.history[i][0].loser_id 
		+ ' game id: ' + websocket_obj.history[i][0].game_id + ' date: ' + websocket_obj.history[i][0].date + '</span></div>';
	}
	historyHTML += '</div>';
	historyHTML += '<button id="userStatsBtn" class="stats-btn btn btn-outline-dark">Your Stats</button><button id ="tournHistoryBtn" class="stats-btn btn btn-outline-dark">Tournament History</button></div>';
	userHistory.innerHTML = historyHTML;
}

function getUserStats(stats) {
	websocket_obj.game_stats.lost_games = stats.lost_games;
	websocket_obj.game_stats.total_games = stats.total_games;
	websocket_obj.game_stats.won_games = stats.won_games;
}






function displayTournHistory() {
	const tournHistory = document.getElementById('tournHistory');
	let historyHTML = '<h2 class="stats-item">Tourn History</h2><div class="stats">';
	let tourns = websocket_obj.tourn_history;

	console.log('tourn history: ', websocket_obj.tourn_history[0]);
	tournHistory.innerHTML = '';
	historyHTML += '<div class="scroll-history">'
	for (let i = 0; tourns[i]; i++) {
		historyHTML += '<div class="stats-item"><span id="tournsPlayed">';
		historyHTML += `<li style="color: #ef7267; margin-bottom: 20px; margin-top: 20px;">Host: ${tourns[i][0][0].tourn_host}, Tournament ID: ${tourns[i][0][0].tourn_id}</li>`;
		historyHTML += `<button class="join-tourn-btn btn btn-outline-dark" data-tournid="${tourns[i][0][0].tourn_host}">View Tournament</button>`;
		historyHTML += '</span></div>';
	}
	historyHTML += '</div>';
	historyHTML += `<button id="userStatsBtnTwo" class="stats-btn btn btn-outline-dark">Your Stats</button>
	<button id ="userHistoryBtnTwo" class="stats-btn btn btn-outline-dark">Your History</button></div>`;
	tournHistory.innerHTML = historyHTML;


	tournHistory.querySelectorAll('.join-tourn-btn').forEach(button => {
		button.addEventListener('click', async function() {
			const tournId = this.getAttribute('data-tournid');
			
			joinTourn(tournId, tourns);
			document.getElementById('gameSite').classList.remove('hidden');
			document.getElementById('displayTourn').classList.remove('hidden');
			document.getElementById('start-screen').classList.add('hidden');
		  	handleButtonClick("");
		});
	});
}

function renderTournHistory() {
	const matches = websocket_obj.tourn_history;
	const container = document.getElementById('tournGameSessionContainer');
  
	container.innerHTML = generateHTMLContentHistory(matches);

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