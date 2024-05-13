//add page refreash and spa logic


function historyBtnClicked() {
	document.getElementById('userStats').classList.add('hidden');
	document.getElementById('userHistory').classList.remove('hidden');
}

function statsBtnClicked() {
	document.getElementById('userHistory').classList.add('hidden');
	document.getElementById('userStats').classList.remove('hidden');
}

async function statsSiteClicked() {
	await requestStats();
	await requestHistory();
	document.getElementById('userStats').classList.remove('hidden');
	document.getElementById('userHistory').classList.add('hidden');
	showSiteHideOthers('statsSite', 'statsButton');
}

async function requestHistory() {
	console.log('In requestHistory');
	await sendDataToBackend('request_history');
}

async function requestStats() {
	console.log('In requestStats');
	await sendDataToBackend('request_stats');
}

function displayStats() {
	document.getElementById('gamesPlayed').textContent = "Games Played: " + websocket_obj.game_stats.total_games;
	document.getElementById('wonGames').textContent = "Wins: " + websocket_obj.game_stats.won_games;
	document.getElementById('lostGames').textContent = "Defeats: " + websocket_obj.game_stats.lost_games;
	let winRate = (websocket_obj.game_stats.won_games / websocket_obj.game_stats.total_games * 100);
	if (isNaN(winRate))
		document.getElementById('winRate').textContent = "Win Rate: 0%";
	else
		document.getElementById('winRate').textContent = "Win Rate: " + winRate.toFixed(2) + '%';
}

function displayHistory() {
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
	historyHTML += '<button id="userStatsBtn" class="stats-btn btn btn-outline-dark">Your Stats</button></div>';
	userHistory.innerHTML = historyHTML;
}

function getUserStats(stats) {
	console.log(stats);
	websocket_obj.game_stats.lost_games = stats.lost_games;
	websocket_obj.game_stats.total_games = stats.total_games;
	websocket_obj.game_stats.won_games = stats.won_games;
}
