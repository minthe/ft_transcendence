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
	userState.currPage = 'endScreen';
	handleButtonClick("");
}

function getCurrentTime() {
    return performance.now(); // Returns the current time in milliseconds since the page started to load
}










//   // Variables for countdown
//   let countdown;
//   let countdownInterval;

//   // Function to draw countdown
// function drawCountdown() {
// 	const canvas = document.getElementById('pongCanvas');
//     const ctx = canvas.getContext('2d');

//     ctx.clearRect(0, 0, canvas.width, canvas.height);
//     ctx.font = '48px Arial';
//     ctx.fillStyle = 'black';
//     ctx.textAlign = 'center';
//     ctx.fillText(countdown, canvas.width / 2, canvas.height / 2);
//   }

//   // Function to start countdown animation
// function startCountdownAnimation() {
// 	countdown = 3;
//     countdownInterval = setInterval(() => {
//       countdown--;
//       if (countdown <= 0) {
//         clearInterval(countdownInterval);
//         // Start your game here after countdown
//         console.log('Game started!');
//         return;
//       }
//       drawCountdown();
//     }, 1000);
//   }







const sentences = ["Welcome to our website!", "Enjoy your stay!", "Have fun playing!", "It`s a feature not a bug!"];
let currentSentence = 0;

function changeText() {
    const textElement = document.getElementById('text');
	if (textElement) {
		textElement.style.opacity = 0;  // Hide text to reset animation
		setTimeout(() => {
			textElement.textContent = sentences[currentSentence];
			textElement.style.opacity = 1;
			textElement.style.animation = 'none';  // Reset animation
			textElement.offsetHeight;  // Trigger reflow
			textElement.style.animation = null;  // Re-apply animation
	
			currentSentence = (currentSentence + 1) % sentences.length;
		}, 1500);  // Wait a bit longer for the animation to finish
	}
}

setInterval(changeText, 5000);