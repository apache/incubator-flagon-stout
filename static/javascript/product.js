function toggle() {

  if ($("#ot_menu").hasClass('ot-show')) {
    $("#ot_menu").removeClass('ot-show');
    $("#ot_menu").addClass('ot-hide');

    $("#ot_menu .glyphicon").removeClass('glyphicon-chevron-down');
    $("#ot_menu .glyphicon").addClass('glyphicon-chevron-up');
    ac.logUserActivity('Closed menu', 'open-close', ac.WF_OTHER);
  } else {
    $("#ot_menu").removeClass('ot-hide');
    $("#ot_menu").addClass('ot-show');

    $("#ot_menu .glyphicon").removeClass('glyphicon-chevron-up');
    $("#ot_menu .glyphicon").addClass('glyphicon-chevron-down');
    ac.logUserActivity('Opened menu', 'open-close', ac.WF_OTHER);
  }
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