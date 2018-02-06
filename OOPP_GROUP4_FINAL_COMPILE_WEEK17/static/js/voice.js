var beep = new Audio();
beep.src = "blop.mp3";
function loadContent(num){
	beep.play();
}

function openNav(){
	document.getElementById('nav').style.height="100%";
}

function closeNav(){
	document.getElementById('nav').style.height="0%";
}

function openNav1(){
	document.getElementById('nav1').style.width="100%";
}

function closeNav1(){
	document.getElementById('nav1').style.width="0%";
}