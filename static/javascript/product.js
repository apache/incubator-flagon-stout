function toggle(id) {
  var el = document.getElementById(id);
  var img = document.getElementById("arrow");
  var box = el.getAttribute("class");
  if(box == "closed container") {
    el.setAttribute("class", "show container");
    delay(img, "//10.1.93.234:8081/static/images/arrowdown.png", 400);
  }
  else{
    el.setAttribute("class", "closed container");
    delay(img, "//10.1.93.234:8081/static/images/arrowup.png", 400)
  }
}

function delay(elem, src, delayTime) {
  window.setTimeout(function() {elem.setAttribute("src", src);}, delayTime);
}

var myVar = setInterval(function(){myTimer()},1000);
var time = 30*60;

function myTimer() {
  time = time - 1;
  minutes = parseInt(time / 60);
  seconds = time % 60;
  document.getElementById("minutes").innerHTML = pad(minutes);
  document.getElementById("seconds").innerHTML = pad(seconds);
}

function pad(n) {return (n<10) ? ("0"+n) : n;}