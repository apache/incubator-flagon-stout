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

