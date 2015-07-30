$(".expTrayNavBtn").hover(function(){
	$(this).find(".expTrayNavBtnLabel").show();
	var labelWidth = parseInt($(this).find(".expTrayNavBtnLabel").css("width"));
	var btnWidth = parseInt($(this).css("width"));
	var newWidth = labelWidth + btnWidth + 18;
	$(this).css("width", newWidth + "px");
}, function(){
	$(this).css("width", "60px");
	$(this).find(".expTrayNavBtnLabel").hide();
})

$(".expTrayNavBtn").on("click", function(){
	$(this).parent().find(".expTrayNavBtn").removeClass("active");
	$(this).addClass("active");
	$(this).find(".expTrayNavBtnLabel").show();
})